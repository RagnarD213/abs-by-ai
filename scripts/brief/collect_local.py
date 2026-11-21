#!/usr/bin/env python3
"""Local brief intake, with Dan's paused dashboard excluded before any read."""
import collect_inputs


def paused_dashboard(_credentials):
    return {"status": "not_checked", "reason": "Victory Dashboard reads paused by Dan; no dashboard request made"}


if __name__ == "__main__":
    collect_inputs.dashboard = paused_dashboard
    raise SystemExit(collect_inputs.main())
