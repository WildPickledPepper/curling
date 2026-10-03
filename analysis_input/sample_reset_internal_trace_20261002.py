"""Observe actual Reset solver steps 5/6, preserving the production calculation."""
import hashlib
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx, _resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native-trace-control', type=Path)
    parser.add_argument('--native-trace-step', type=int, default=6)
    parser.add_argument('--native-trace-through-step', type=int)
    parser.add_argument('--allow-baseline-change', action='store_true',
                        help='Record a production repair; compare outputs to Unity separately')
    parser.add_argument('--baseline', type=Path,
                        default=ROOT / 'analysis_input/native_reset_settling_fixed_20261002.json')
    parser.add_argument('--output', type=Path,
                        default=ROOT / 'analysis_input/native_reset_internal_trace_20261002.json')
    opts = parser.parse_args()
    scene = PersistentPhysxFrontHalfScene(stone_count=16, ice_mesh_mode='unity-source-once')
    frames = []
    native_scene = scene.scene
    trace_names = ('solver_setup', 'solve_block', 'solve_writeback', 'narrowphase', 'finalizer')
    original_step = scene._simulate_unity_step
    current = {}

    def await_file(name):
        import time
        deadline = time.monotonic() + 90
        while not (opts.native_trace_control / name).exists():
            if time.monotonic() > deadline:
                raise TimeoutError(name)
            time.sleep(.05)

    class ObservedScene:
        def __getattr__(self, name):
            return getattr(native_scene, name)

        def simulate(self, dt):
            traced = 1 <= current['step'] <= max(6, opts.native_trace_through_step or 6)
            if traced:
                for name in trace_names:
                    getattr(scene.pyphysx, 'clear_scene_' + name + '_trace')()
                    getattr(scene.pyphysx, 'set_scene_' + name + '_trace_enabled')(True)
            control = opts.native_trace_control if current['step'] == opts.native_trace_step else None
            if control:
                import ctypes, os
                (control / 'arm.json').write_text(json.dumps(dict(pid=os.getpid(),
                    threadId=ctypes.windll.kernel32.GetCurrentThreadId(),
                    module=str(_resolve_bundled_extension()), resetPhysicsStep=current['step'])))
                await_file('go')
            result = native_scene.simulate(dt)
            through = opts.native_trace_through_step or opts.native_trace_step
            if opts.native_trace_control and current['step'] == through:
                (opts.native_trace_control / 'done').write_text('done')
                await_file('resume')
            current['afterNative'] = scene.raw_native_state(2)
            if traced:
                for name in trace_names:
                    current[name] = getattr(scene.pyphysx, 'get_scene_' + name + '_trace')(False)
                    getattr(scene.pyphysx, 'set_scene_' + name + '_trace_enabled')(False)
            return result

    scene.scene = ObservedScene()

    def observed_step():
        current.clear()
        current.update(step=len(frames) + 1, before=scene.raw_native_state(2))
        result = original_step()
        current.update(after=scene.raw_native_state(2), sleeping=scene.slots[2].body.is_sleeping())
        frames.append(dict(current))
        return result

    scene._simulate_unity_step = observed_step
    position = [0.] * 32
    position[4:6] = [2.375, 5.2]
    scene.reset_positions(position)
    baseline = json.loads(opts.baseline.read_text())
    unchanged = len(frames) == len(baseline['frames']) and all(
        all(row[key] == old[key] for key in ('step', 'before', 'after', 'sleeping'))
        for row, old in zip(frames, baseline['frames']))
    if not opts.allow_baseline_change:
        assert unchanged, 'Observer changed native Reset output'
    result = dict(moduleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest(),
                  baselineOutputsUnchanged=unchanged, frames=frames)
    path = opts.output
    path.write_text(json.dumps(result, indent=2))
    print('steps', len(frames), 'observerUnchanged', unchanged)
    for row in frames[:6]:
        print('step', row['step'], {name: len(row[name]) for name in trace_names})


if __name__ == '__main__':
    main()
