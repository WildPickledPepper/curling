#!/usr/bin/env python3
"""Stop only the launcher/sampler process trees belonging to one probe session."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path


LAUNCHER_SCRIPTS = (
    "launch_unity_probe_browser.py",
    "launch_a0_last_angular_write_probe.py",
)


def powershell_process_rows() -> list[dict[str, str]]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process | Select-Object ProcessId,Name,CommandLine | ConvertTo-Csv -NoTypeInformation",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=True)
    return list(csv.DictReader(completed.stdout.splitlines()))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-root", type=Path, required=True)
    parser.add_argument("--sampler-output", type=Path)
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Terminate the matched process trees. Omit for a dry-run.",
    )
    args = parser.parse_args()
    log_root_terms = {str(args.log_root), str(args.log_root.resolve())}
    sampler_terms = (
        {str(args.sampler_output), str(args.sampler_output.resolve())}
        if args.sampler_output
        else set()
    )

    matches: list[dict[str, str]] = []
    for row in powershell_process_rows():
        command_line = row.get("CommandLine") or ""
        # Match only real Python children.  The current PowerShell command can itself
        # contain these script names while invoking this cleanup tool.
        is_python = (row.get("Name") or "").lower() in {"python.exe", "pythonw.exe"}
        is_launcher = (
            is_python
            and any(script in command_line for script in LAUNCHER_SCRIPTS)
            and any(term in command_line for term in log_root_terms)
        )
        is_sampler = is_python and "controlled_scene_sampler.py" in command_line and any(
            term in command_line for term in sampler_terms
        )
        if is_launcher or is_sampler:
            matches.append(
                {
                    "pid": row.get("ProcessId") or "",
                    "name": row.get("Name") or "",
                    "role": "launcher" if is_launcher else "sampler",
                    "command": command_line,
                }
            )

    for match in matches:
        print(f"{match['role']} pid={match['pid']} {match['command']}")
    if not args.stop:
        print(f"dry-run matches={len(matches)}")
        return 0

    for match in matches:
        subprocess.run(
            ["taskkill", "/PID", match["pid"], "/T", "/F"],
            check=False,
            capture_output=True,
            text=True,
        )
    print(f"stopped_process_trees={len(matches)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
