#!/usr/bin/env python3
"""
PreToolUse hook: the hard writing rules, checked on text before it is written.

WHY THIS EXISTS (2026-10-10, Dan Voice P2B step B8): nothing enforced the rules. A session ran the checker only if it
remembered to. This hook looks at the NEW text of a Write or Edit to a .md or .txt file, and at text going to Google
Docs, Gmail drafts and Drive files, for two things only: an em or en dash (Dan's standing rule, AGENTS.md) and, in
script and copy files, the phrases Dan has cut from drafts (`voice_check.HARD_PHRASES`). The full voice score is not
run here: that happens inside the dan-voice-writer agent.

Old text is never flagged (Dan, 2026-09-18: the rule is forward-looking, no retrofit). Only lines that are new in this
write count.

Report-only until BLOCK_FROM: the hook lets the write through and tells the session what it found. From that date it
stops the write (exit 2) and the session has to fix the text first. To turn it off, delete its entry from
`.claude/settings.json`.
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice_check  # noqa: E402

BLOCK_FROM = datetime.date(2026, 10, 17)
COPY_PATH = re.compile(r"script|teleprompter|vsl|sales|letter|outline|caption|description|\bad[-_ s]|shorts|email|"
                       r"article|revision", re.I)


def new_lines(tool, inp):
    """(text that is new in this call, is it copy that Dan's name goes on)"""
    if tool in ("Write", "Edit", "MultiEdit"):
        path = inp.get("file_path", "")
        if not path.lower().endswith((".md", ".txt")):
            return "", False
        if tool == "Write":
            old = set()
            if os.path.isfile(path):
                with open(path, encoding="utf-8", errors="replace") as fh:
                    old = set(fh.read().splitlines())
            new = [l for l in str(inp.get("content", "")).splitlines() if l not in old]
        else:
            edits = inp.get("edits") or [inp]
            new = []
            for e in edits:
                old = set(str(e.get("old_string", "")).splitlines())
                new += [l for l in str(e.get("new_string", "")).splitlines() if l not in old]
        return "\n".join(new), bool(COPY_PATH.search(os.path.basename(path)))
    # a Google Docs, Gmail or Drive call: every string in the input is outgoing text
    parts = []

    def walk(v):
        if isinstance(v, str) and len(v) > 40:
            parts.append(v)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(inp)
    return "\n".join(parts), True


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return 0
    text, copy = new_lines(data.get("tool_name", ""), data.get("tool_input") or {})
    if not text:
        return 0
    hits = [h for h in voice_check.hard_fails(text) if copy or h[1].startswith("em or en dash")]
    if not hits:
        return 0
    msg = ("Hard writing rule: " + "; ".join(f"{why} in \"{line[:70]}\"" for _, why, line in hits[:4])
           + (f" (and {len(hits) - 4} more)" if len(hits) > 4 else "")
           + ". No em or en dash in anything written for this project (AGENTS.md), and these phrases are ones Dan cuts. "
             "Rewrite with a comma, a colon, brackets or two sentences.")
    if datetime.date.today() >= BLOCK_FROM:
        print(msg + " The write was stopped: fix the text and write it again.", file=sys.stderr)
        return 2
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "additionalContext": msg + " (Report only until 2026-10-17; fix it now anyway.)"}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
