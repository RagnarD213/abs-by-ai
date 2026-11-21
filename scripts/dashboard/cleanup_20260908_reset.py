#!/usr/bin/env python3
"""Victory Dashboard hard reset (2026-09-08, Dan's instruction): keep ONLY the rows
named below in the business and personal lists, delete everything else. Health
(daily habits with a streak log) and assistant (Brittany's list) are not touched.

Writes through the live API with allowDeletes. Keyed on exact text.
Usage:  python3 scripts/dashboard/cleanup_20260908_reset.py [--apply]
"""
import json, os, sys, urllib.request, pathlib

BASE = "https://absbyai.com"
KEEP = {
  "business": [
    "Execute handoff: RevenueCat restore-behavior audit (one Apple ID, multiple accounts)",
    "Execute handoff: Let users purchase before creating an account (iOS)",
    "Execute handoff: Swap Dan's phone to the public Play build",
    "Execute handoff: fill danrosefit + abs.by.ai image-post gap days (write captions, schedule in Blotato)",
    "Switch on the YouTube engagement champion: Dan authorizes Ads Script 12241942 (hourly) + creates the MCC developer token, then a session sets YTADS_ENABLED=1",
    "Send documents to AMEX",
    "Redo AI Trainer workout program (consider manual programming)",
    "Add shipping costs to app",
    "Make the AI Trainer recovery-aware: scale volume from last night's Oura sleep/HRV",
  ],
  "personal": [
    "Generate new life-visualization desktop backgrounds",
    "Hire someone to powerwash",
  ],
}

def key():
    for line in pathlib.Path(os.path.expanduser("~/.absbyai-secrets.env")).read_text().splitlines():
        if line.startswith("DASH_SECRET="): return line.split("=", 1)[1].strip()
    sys.exit("DASH_SECRET not found")

def req(path, body=None):
    r = urllib.request.Request(BASE + path, headers={"X-Dash-Key": key(), "Content-Type": "application/json"},
                               data=json.dumps(body).encode() if body is not None else None,
                               method="POST" if body is not None else "GET")
    with urllib.request.urlopen(r) as resp: return json.loads(resp.read())

def main():
    apply = "--apply" in sys.argv
    d = req("/api/todos"); deletes = []
    for lst, keep in KEEP.items():
        rows = d.get(lst, []); have = {t.get("text") for t in rows}
        for k in keep:
            if k not in have: print(f"WARNING: keep row not found in {lst}: {k}")
        kept = [t for t in rows if t.get("text") in keep]
        gone = [t for t in rows if t.get("text") not in keep]
        deletes += [f"{lst}::{t['text']}" for t in gone]
        print(f"\n{lst}: {len(rows)} -> {len(kept)}   REMOVING {len(gone)}:")
        for t in gone: print(f"  - [{t.get('priority')}]{' R' if t.get('recurring') else ''} {t['text'][:110]}")
        d[lst] = kept
    if not apply: print("\n(dry run — pass --apply to write)"); return
    d["allowDeletes"] = deletes
    print("\nPOST:", json.dumps(req("/api/todos", d))[:200])
    back = req("/api/todos")
    for lst in KEEP: print(f"VERIFY {lst}: {len(back.get(lst, []))} rows ->", [t['text'][:40] for t in back.get(lst, [])])
    print("health:", len(back.get("health", [])), "assistant:", len(back.get("assistant", [])))

if __name__ == "__main__": main()
