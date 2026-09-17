#!/usr/bin/env python3
"""Validate one queue work directory's risky-source preview evidence before a full render."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import runner  # noqa: E402


def main():
    if len(sys.argv) != 2:
        print("usage: pre_render_check.py <absolute-work-directory>", file=sys.stderr)
        return 2
    workdir = os.path.abspath(sys.argv[1])
    errors = runner.validate_pre_render(workdir)
    result = {"status": "FAIL" if errors else "PASS", "workdir": workdir, "errors": errors}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
