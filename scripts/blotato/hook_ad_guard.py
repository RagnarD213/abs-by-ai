#!/usr/bin/env python3
"""PreToolUse hook: block a Blotato MCP write that carries AD content.

`scripts/blotato/ad_guard.py` protects the queue SCRIPTS, but the Blotato MCP tools
(blotato_create_post and friends) are callable directly by any session and would sail
straight past it. That is the same shape of hole that produced the Ad 5 incident on
2026-09-16/17: a rule that only applies where someone remembers to apply it.

This runs in the harness, before the tool call, on the payload itself, so it holds
whatever a session decides to do. Exit 2 blocks the call and shows the reason.

Wired in .claude/settings.json as a PreToolUse hook matching Blotato write tools.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except Exception:
        # A hook that cannot read its input must not silently allow the write.
        print("ad_guard hook: could not parse the tool payload — refusing the Blotato write. "
              "Check scripts/blotato/hook_ad_guard.py.", file=sys.stderr)
        return 2

    payload = json.dumps(event.get("tool_input", {}))

    try:
        from ad_guard import ad_titles, ad_video_ids, norm, ORGANIC_OVERRIDES
    except Exception as exc:
        print(f"ad_guard hook: the ad registry could not be loaded ({exc}) — refusing the Blotato "
              "write rather than passing it unchecked.", file=sys.stderr)
        return 2

    hay = norm(payload)
    matched = [t for t in ad_titles() if t in hay]
    matched += [v for v in ad_video_ids() if v.lower() in hay]
    if not matched:
        return 0

    for o in ORGANIC_OVERRIDES:
        if norm(o.get("title", "")) and norm(o["title"]) in hay:
            return 0

    print(
        f"BLOCKED by ad_guard: this Blotato write carries AD content ({matched[0]!r}).\n"
        "An ad video is never published organically — not Facebook, not Instagram, not TikTok, "
        "not Blotato, not YouTube Public (Dan, 2026-09-17; AGENTS.md).\n"
        "Ads run as paid placements from an UNLISTED YouTube upload: use /ad-setup.\n"
        "Tell Dan plainly: \"this is an ad — ads don't go organic, do you want it posted anyway?\" "
        "and WAIT for his answer. If he says yes, record his words in ORGANIC_OVERRIDES in "
        "scripts/blotato/ad_guard.py first.",
        file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
