#!/usr/bin/env python3
"""PreToolUse hook (Bash): refuse `python -m http.server` / SimpleHTTPServer.

Dan, 2026-10-16: a review page's video timeline could not be scrubbed (clicking or dragging the slider did nothing) because the page was
served with `python3 -m http.server`, which ignores HTTP byte ranges. The standing rule (VIDEO-RULES, "Review pages must survive...")
already said to use the managed server; this makes the harness enforce it. Exit 2 = blocked, the message goes back to the session.
"""
import json, re, sys
try:
    cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")
except Exception:
    sys.exit(0)
if re.search(r"-m\s+http\.server\b|python[0-9.]*\s+-m\s+SimpleHTTPServer|\bSimpleHTTPServer\b\s+\d", cmd) and "review_server.py" not in cmd:
    sys.stderr.write(
        "BLOCKED: python's http.server cannot seek (no byte ranges), so Dan cannot drag the video timeline on the page.\n"
        "Serve review pages with:  python3 .claude/skills/_shared/review_server.py PORT DIR\n"
        "then prove it:  curl -s -o /dev/null -D - -r 0-99 http://127.0.0.1:PORT/<a video>   (must say 206 Partial Content)\n"
        "and seek a video in the browser (set currentTime, read it back) before sending the link.\n")
    sys.exit(2)
sys.exit(0)
