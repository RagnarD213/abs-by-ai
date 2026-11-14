#!/usr/bin/env python3
"""Resume an existing edit from its original chat, on the Mac holding its work.

    resume.py check JOB [--json]       0 = local/new, 5 = use remote, 6 = cannot locate safely
    resume.py run JOB [--cwd PATH] -- COMMAND [ARG ...]

run streams the command on the owning Mac (default cwd: its project checkout),
preserves its exit code and stdin, and never starts another AI or moves files.
It does not replace editcap/renderq: run those commands on that Mac as usual.
"""
import argparse
import base64
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

import editroute as er

EXIT_REMOTE = 5
EXIT_UNRESOLVED = 6


def locate(job, statuses=None, config=None, here=None):
    """Read-only ownership, distinct from preferences for a NEW edit."""
    job = er.job_code(job)
    config = er.cfg() if config is None else config
    here = er.me() if here is None else here
    if not here or here not in config.get("hosts", {}):
        # Keep the old single-Mac/test behavior outside this two-Mac installation.
        return dict(job=job, host=here, here=here, state="unmanaged", reason="No two-Mac configuration here.")
    statuses = er.gather(job, config) if statuses is None else statuses
    unavailable = [h for h in config["hosts"] if not statuses.get(h, {}).get("reachable")]
    if unavailable:
        return dict(job=job, host=None, here=here, state="unresolved",
                    reason="Cannot verify edit ownership; {} did not answer. Retry the check; do not start a local copy."
                    .format(", ".join(unavailable)))
    host, reason = er.holder(job, statuses)
    folders = ((statuses.get(host) or {}).get("job") or {}).get("folders", [])
    return dict(job=job, host=host, here=here, state="existing" if host else "new",
                reason=reason or "No existing edit found; use editroute.py pick for a new edit.",
                folders=[f["path"] for f in folders])


def check(job, as_json=False):
    try:
        info = locate(job)
    except Exception as ex:
        info = dict(job=job, host=None, state="unresolved", reason="Ownership check failed: {}".format(ex))
    code = (EXIT_UNRESOLVED if info["state"] == "unresolved" else
            EXIT_REMOTE if info.get("host") and info["host"] != info.get("here") else 0)
    if as_json:
        print(json.dumps(info, indent=2))
    else:
        print("{}: {}. {}".format(job, info.get("host") or info["state"], info["reason"]))
        if code == EXIT_REMOTE:
            helper = er.REPO / ".claude/skills/_shared/editroute/resume.py"
            print("REMOTE_EDIT: keep Dan's original chat as the editor. Do not acquire a slot or produce here.")
            print("Continue automatically without asking Dan for routing instructions: run commands with")
            print("  python3 {} run {} -- <command and arguments>".format(shlex.quote(str(helper)), shlex.quote(job)))
            print("First run editcap.py acquire on that Mac, then its normal render queue. Read/write build files there;")
            print("preserve approval checkpoints and use the existing review mirroring/delivery workflow. Do not start")
            print("a second AI editor or move the job. Read editroute/README.md, 'Continuing in the original chat'.")
        elif code == EXIT_UNRESOLVED:
            print("No production slot was acquired. Report a persistent connection blocker; do not ask Dan to choose a Mac.")
    return code


def command_for(info, command, config, cwd=None):
    """Construct argv, never interpolate user command arguments as shell code."""
    host = info.get("host") or info.get("here")
    hc = config["hosts"][host]
    cwd = cwd or hc["repo"]
    if not Path(cwd).is_absolute():
        raise ValueError("--cwd must be an absolute path on the edit's Mac")
    # argv is JSON inside base64 so quotes, spaces, $() and newlines stay literal.
    payload = base64.b64encode(json.dumps(dict(argv=command, cwd=cwd, job=info["job"])).encode()).decode()
    worker = ("import base64,json,os,subprocess,sys; "
              "p=json.loads(base64.b64decode(sys.argv[1])); os.chdir(p['cwd']); "
              "os.environ['GATE_GROUP']=p['job']; "
              "sys.exit(subprocess.call(p['argv']))")
    runner = ["python3", "-u", "-c", worker, payload]
    if host == info.get("here"):
        return runner
    return ["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=3", "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=3", hc.get("ssh", host), " ".join(shlex.quote(s) for s in runner)]


def run(job, command, cwd=None):
    info = locate(job)
    if info["state"] != "existing":
        print(info["reason"], file=sys.stderr)
        return EXIT_UNRESOLVED
    argv = command_for(info, command, er.cfg(), cwd)
    print("{}: running on {} from the original chat".format(info["job"], info["host"]), file=sys.stderr, flush=True)
    # No timeout or automatic retry: a disconnected build may still be alive.
    return subprocess.call(argv)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("check")
    p.add_argument("job")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("run")
    p.add_argument("job")
    p.add_argument("--cwd")
    argsv = sys.argv[1:] if argv is None else argv
    before, sep, command = argsv, False, []
    if "--" in argsv:
        cut = argsv.index("--")
        before, sep, command = argsv[:cut], True, argsv[cut + 1:]
    args = parser.parse_args(before)
    if args.action == "check":
        return check(args.job, args.json)
    if not sep or not command:
        parser.error("run needs -- COMMAND [ARG ...]")
    try:
        return run(args.job, command, args.cwd)
    except (OSError, ValueError, KeyError) as ex:
        print("resume: {}. Nothing retried or moved.".format(ex), file=sys.stderr)
        return EXIT_UNRESOLVED


if __name__ == "__main__":
    sys.exit(main())
