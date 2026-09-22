#!/usr/bin/env python3
"""Run one explicit roll manifest under a persistent supervisor.

Exit nonzero only when the source drive disappears or the child crashes, so
launchd can restart safely. Ordinary per-clip errors are recorded for review
instead of causing an endless paid retry loop.
"""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def save_status(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
        temporary = handle.name
    os.replace(temporary, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--log", required=True, type=Path)
    parser.add_argument("--status", required=True, type=Path)
    args = parser.parse_args()
    manifest = args.manifest.expanduser().resolve()
    clips = [Path(line) for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not clips or any(not clip.is_file() for clip in clips):
        print("source drive unavailable or manifest has a missing clip", file=sys.stderr, flush=True)
        return 1
    tool = Path(__file__).with_name("roll_sidecar.py")
    args.log.parent.mkdir(parents=True, exist_ok=True)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    save_status(args.status, {"state": "running", "started_at": started, "manifest": str(manifest), "clips": len(clips)})
    with args.log.open("a", encoding="utf-8") as log:
        log.write("\nSTART {}: {} clips\n".format(started, len(clips)))
        log.flush()
        command = ["/usr/bin/nice", "-n", "10", sys.executable, str(tool), "build", "@" + str(manifest)]
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        ended = dt.datetime.now(dt.timezone.utc).isoformat()
        log.write("END {}: exit {}\n".format(ended, result.returncode))
        log.flush()
    drive_available = all(clip.is_file() for clip in clips)
    state = "complete" if result.returncode == 0 else "retrying-after-drive-loss" if not drive_available else "needs-review"
    save_status(args.status, {"state": state, "started_at": started, "ended_at": ended,
                              "manifest": str(manifest), "clips": len(clips), "tool_exit_code": result.returncode})
    return 1 if result.returncode < 0 or not drive_available else 0


if __name__ == "__main__":
    sys.exit(main())
