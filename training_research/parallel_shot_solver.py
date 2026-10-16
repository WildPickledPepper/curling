"""Warm, bounded parallel search over independent original simulator scenes.

Independent numerical worker processes share one wall-clock budget. Each
worker uses the existing solver and complete forward acceptance predicate.
Reference files and source actions are never opened here.
"""
from __future__ import annotations

import multiprocessing as mp
from multiprocessing.connection import wait
import os
import time


PROFILES = ("wide_dfols", "tangent_micro", "contact_de", "impact_learned")
CPUS = (4, 6, 8, 10)


class Cancelled(Exception):
    pass


def _worker(connection, stop, profile, cpu):
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    if os.name == "nt":
        import ctypes as C
        from tools.cpu_telemetry import CpuTelemetry
        telemetry = CpuTelemetry()
        core = next(c for c in telemetry.topology if c["group"] == 0 and c["logical"] == cpu)
        if core["efficiency"] != max(c["efficiency"] for c in telemetry.topology):
            connection.send({"ready": False, "error": "worker CPU is not a performance core"})
            return
        telemetry.close()
        kernel = C.WinDLL("kernel32", use_last_error=True)
        kernel.GetCurrentProcess.restype = C.c_void_p
        kernel.SetProcessAffinityMask.argtypes = (C.c_void_p, C.c_size_t)
        if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << cpu):
            connection.send({"ready": False, "error": "worker CPU affinity failed"})
            return
    from training_research.shot_solver import BudgetedShotSolver
    from training_research.inverse_dataset.cli import simulate_record
    records = []
    deadline = float("inf")

    def forward(env, scene, proposal, seed, record_id, config):
        if stop.is_set() or time.perf_counter() >= deadline:
            raise Cancelled()
        record = simulate_record(env, scene, proposal, seed, record_id, config)
        records.append(record)
        return record

    try:
        solver = BudgetedShotSolver(search_profile=profile, forward_simulator=forward)
        # Same startup fixture as the serial benchmark, before real requests.
        import json
        from pathlib import Path
        fixture = json.loads((Path(__file__).parent/"fixtures/sampled_goal_draw.json").read_text(encoding="utf-8"))
        solver.solve(fixture, budget_seconds=10.)
        records.clear()
        connection.send({"ready": True, "profile": profile, "cpu": cpu})
    except BaseException as exc:
        connection.send({"ready": False, "error": repr(exc)})
        return
    while True:
        message = connection.recv()
        if message is None:
            break
        if message[0] == "records":
            connection.send(records)
            continue
        _, task_id, request, deadline, max_calls, seed, required = message
        records = []
        started = time.perf_counter()
        try:
            remaining = deadline-time.perf_counter()
            if stop.is_set() or remaining <= 0.:
                raise Cancelled()
            result = solver.solve(request, budget_seconds=remaining, max_calls=max_calls,
                                  seed=seed, required_seed_successes=required, cancelled=stop.is_set)
        except Cancelled:
            result = {"success": False, "shot": None, "status": "CANCELLED_AFTER_OTHER_WORKER_OR_DEADLINE",
                      "diagnostics": {}}
        except Exception as exc:
            result = {"success": False, "shot": None, "status": "WORKER_ERROR",
                      "error": repr(exc), "diagnostics": {}}
        result.update(worker_profile=profile, worker_cpu=cpu,
                      worker_elapsed_ms=1000*(time.perf_counter()-started), physics_calls=len(records))
        connection.send({"task_id": task_id, "result": result})
    connection.close()


class ParallelShotSolver:
    """Construct once; serial requests, configurable simultaneous processes.

    Cancellation occurs before the next actual forward call. In-flight native
    work is allowed to finish. The returned elapsed time includes dispatch and
    draining all workers; evidence transfer is a separate diagnostic operation.
    """

    def __init__(self, *, profiles=PROFILES, cpus=CPUS):
        if not profiles or len(profiles) != len(cpus) or len(set(cpus)) != len(cpus):
            raise ValueError("one distinct CPU is required for each worker")
        context = mp.get_context("spawn")
        self.stop = context.Event()
        self.processes, self.connections = [], []
        self.task_id = 0
        self.worker_profiles = tuple(profiles)
        self.worker_cpus = tuple(cpus)
        self.closed = False
        try:
            for profile, cpu in zip(profiles, cpus):
                parent, child = context.Pipe()
                process = context.Process(target=_worker, args=(child, self.stop, profile, cpu), daemon=True)
                process.start()
                child.close()
                self.connections.append(parent)
                self.processes.append(process)
            for conn in self.connections:
                if not conn.poll(60.):
                    raise RuntimeError("parallel solver startup timed out")
                ready = conn.recv()
                if not ready.get("ready"):
                    raise RuntimeError("parallel worker startup failed: "+ready.get("error", "unknown"))
        except BaseException:
            self.close()
            raise

    def solve(self, scene, *, budget_seconds=10., max_calls=256, seed=20261004,
              required_seed_successes=1, include_records=False):
        import math
        if self.closed:
            raise RuntimeError("parallel solver is closed")
        if not math.isfinite(budget_seconds) or budget_seconds <= 0.:
            raise ValueError("budget_seconds must be finite and positive")
        for name, value in (("max_calls", max_calls), ("required_seed_successes", required_seed_successes)):
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise ValueError(name+" must be a positive integer")
        # Validate once before dispatch; the existing worker API also validates.
        from training_research.inverse_dataset.sampling import validate_scene
        request = validate_scene(scene)
        started = time.perf_counter()
        deadline = started+budget_seconds
        self.task_id += 1
        self.stop.clear()
        for connection in self.connections:
            connection.send(("solve", self.task_id, request, deadline, max_calls, seed, required_seed_successes))
        pending = set(self.connections)
        results, winner = [], None
        first_success_ms = None
        while pending:
            ready = wait(pending, timeout=.05)
            if not ready:
                if time.perf_counter() >= deadline:
                    self.stop.set()
                for process, connection in zip(self.processes, self.connections):
                    if connection in pending and not process.is_alive():
                        raise RuntimeError("parallel search worker exited unexpectedly")
                continue
            for connection in ready:
                message = connection.recv()
                if message["task_id"] != self.task_id:
                    raise RuntimeError("stale parallel search result")
                pending.remove(connection)
                result = message["result"]
                results.append(result)
                if result["success"] and winner is None:
                    winner = result
                    first_success_ms = 1000*(time.perf_counter()-started)
                    self.stop.set()
        elapsed_ms = 1000*(time.perf_counter()-started)
        output = {"status": winner["status"] if winner else "NOT_FOUND_WITHIN_BUDGET",
                  "success": winner is not None, "shot": winner["shot"] if winner else None,
                  "elapsed_ms": elapsed_ms, "budget_seconds": budget_seconds,
                  "physics_calls": sum(r["physics_calls"] for r in results),
                  "required_seed_successes": required_seed_successes,
                  "scene_key": request["scene_key"], "search_profile": "parallel_portfolio",
                  "diagnostics": {"initial_success": winner["diagnostics"].get("initial_success", False) if winner else False,
                                  "refinement_success": winner["diagnostics"].get("refinement_success", False) if winner else False,
                                  "initial_generation_ms": sum(r["diagnostics"].get("initial_generation_ms", 0.) for r in results),
                                  "winning_profile": winner["worker_profile"] if winner else None,
                                  "first_success_ms": first_success_ms,
                                  "worker_results": results},
                  "scope": "Warm numerical processes; common wall deadline. Each worker has an independent persistent original simulator and normal navigation seed. Startup/evidence transport excluded; dispatch and cancellation drain included. In-flight calls may overrun."}
        errors = [r["error"] for r in results if "error" in r]
        if errors:
            raise RuntimeError("parallel worker error: "+repr(errors))
        if include_records:
            output["records"] = self.collect_records()
        return output

    def collect_records(self):
        """Full observed evidence, transferred after search timing ends."""
        for connection in self.connections:
            connection.send(("records",))
        records = []
        for profile, connection in zip(self.worker_profiles, self.connections):
            batch = connection.recv()
            for record in batch:
                record["worker_profile"] = profile
            records.extend(batch)
        return records

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.stop.set()
        for connection, process in zip(self.connections, self.processes):
            if process.is_alive():
                try:
                    connection.send(None)
                except (EOFError, BrokenPipeError, OSError):
                    pass
        for process in self.processes:
            process.join(timeout=2.)
            if process.is_alive():
                process.terminate()
                process.join(timeout=2.)
        for connection in self.connections:
            connection.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
