#!/usr/bin/env python3
"""/away: tell this Mac Dan is leaving now, so edits get the away core budget at once (M6: 10 cores instead of 6)
instead of after 30 idle minutes. It ends by itself the moment the keyboard or mouse is used again (2 min grace to
walk away), or after --hours (default 8). Only changes how many cores the render queue hands out on THIS Mac.

  away.py on [--hours 8]     away.py off     away.py status
"""
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import hostcfg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["on", "off", "status"])
    ap.add_argument("--hours", type=float, default=8.0)
    a = ap.parse_args()
    if a.cmd == "on":
        hostcfg.away_set(a.hours)
    elif a.cmd == "off":
        hostcfg.away_clear()
    state, why = hostcfg.presence()
    print("{}: {} ({}). Cores for edits now: {}".format(hostcfg.this_host() if hasattr(hostcfg, "this_host") else "this Mac",
                                                       state, why, hostcfg.core_budget()))


if __name__ == "__main__":
    main()
