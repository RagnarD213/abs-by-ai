#!/usr/bin/env python3
"""Validate one queue work directory's risky-source preview evidence before a full render."""
import json
import fcntl
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runner  # noqa: E402


def reserve_full_render(workdir):
    """Atomically reserve one full render after preview evidence passes."""
    path = os.path.join(workdir, "BUDGET.json")
    lock_path = path + ".lock"
    with open(lock_path, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            with open(path) as fh:
                budget = json.load(fh)
        except FileNotFoundError as exc:
            raise ValueError("BUDGET.json is missing; the queue must set a budget before a full render") from exc
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            raise ValueError(f"BUDGET.json is unreadable: {exc}") from exc
        used = budget.get("renders_used")
        allowed = budget.get("max_full_renders")
        if not isinstance(used, int) or used < 0:
            raise ValueError("BUDGET.json renders_used must be a non-negative integer")
        if allowed is not None and (not isinstance(allowed, int) or allowed < 1):
            raise ValueError("BUDGET.json max_full_renders must be a positive integer or null")
        if allowed is not None and used >= allowed:
            raise ValueError(f"full-render budget exhausted: {used}/{allowed} already used; no render was reserved")
        budget["renders_used"] = used + 1
        tmp = path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(budget, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
        return budget["renders_used"], allowed


def main():
    if len(sys.argv) != 2:
        print("usage: pre_render_check.py <absolute-work-directory>", file=sys.stderr)
        return 2
    workdir = os.path.abspath(sys.argv[1])
    errors = runner.validate_pre_render(workdir)
    render = None
    if not errors:
        try:
            used, allowed = reserve_full_render(workdir)
            render = {"used": used, "allowed": allowed}
        except ValueError as exc:
            errors.append(str(exc))
    result = {"status": "FAIL" if errors else "PASS", "workdir": workdir, "errors": errors,
              "full_render": render}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
