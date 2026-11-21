#!/usr/bin/env python3
"""Move the four open handoffs from the business list into the new `handoffs`
list (2026-09-08). Each row carries its doc, a status chip, the model
recommendation and the doc's own starter prompt (read from the doc, not retyped).

Usage:  python3 scripts/dashboard/migrate_handoffs_20260908.py [--apply]
Requires the server to already accept `handoffs` (deploy first; the script refuses otherwise).
"""
import json, os, re, sys, urllib.request, pathlib

BASE = "https://absbyai.com"
ROOT = pathlib.Path(__file__).resolve().parents[2]

def starter_prompt(doc):
    txt = (ROOT / doc).read_text()
    m = re.search(r"^## Starter Prompt.*?$\n(.*?)(?=^## |\Z)", txt, re.S | re.M)
    if not m: return None
    lines = [re.sub(r"^>\s?", "", l) for l in m.group(1).strip().splitlines()]
    return "\n".join(lines).strip()

ROWS = [
  {"text": "RevenueCat restore-behavior audit (one Apple ID, multiple accounts)",
   "doc": "Handoffs/handoff-20260812-revenuecat-restore-behavior-audit.md",
   "status": "waiting on Apple approval", "ready": False, "model": "Sonnet 5, standard", "addedAt": "2026-08-12",
   "old": "Execute handoff: RevenueCat restore-behavior audit (one Apple ID, multiple accounts)"},
  {"text": "Let users purchase before creating an account (iOS)",
   "doc": "Handoffs/handoff-20260812-purchase-before-account.md",
   "status": "after approval + RevenueCat audit", "ready": False, "model": "Opus, extended thinking", "addedAt": "2026-08-12",
   "old": "Execute handoff: Let users purchase before creating an account (iOS)"},
  {"text": "Swap Dan's phone to the public Play build",
   "doc": "Handoffs/handoff-20260818-android-public-build-swap.md",
   "status": "needs your Android phone on adb", "ready": False, "model": "Sonnet 5 or Codex mini, low", "addedAt": "2026-08-18",
   "old": "Execute handoff: Swap Dan's phone to the public Play build"},
  {"text": "Fill the last 7 Instagram image-gap days (63 of 70 done)",
   "doc": "Handoffs/handoff-20260826-danrosefit-abs-image-gap-fill.md",
   "status": "Blotato queue room from ~09-12", "ready": False, "model": "Sonnet 5, standard", "addedAt": "2026-08-26",
   "old": "Execute handoff: fill danrosefit + abs.by.ai image-post gap days (write captions, schedule in Blotato)",
   "prompt": "Read Handoffs/handoff-20260826-danrosefit-abs-image-gap-fill.md in the Abs By AI repo and finish it. 63 of the 70 image posts are already scheduled and verified; the last 7 were blocked on Blotato's 200-post plan cap. First re-pull the live Blotato queue for @danrosefit and @abs.by.ai and confirm there are at least 7 free slots under the cap (it drains ~2 posts/day). If there are, run `scripts/blotato/iggap_fill.py --apply` (idempotent — it only schedules the missing days), then re-read the queue and verify every new post landed with the right account, time and caption. Report the final fill list. No AI generation, no production code, no deploy."},
]

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
    d = req("/api/todos")
    if "handoffs" not in d: sys.exit("server does not return `handoffs` yet — deploy first")
    olds = {r["old"] for r in ROWS}
    biz = d.get("business", [])
    removed = [t["text"] for t in biz if t.get("text") in olds]
    d["business"] = [t for t in biz if t.get("text") not in olds]
    have = {t.get("text") for t in d.get("handoffs", [])}
    added = []
    for r in ROWS:
        if r["text"] in have: continue
        row = {k: v for k, v in r.items() if k not in ("old", "prompt")}
        row["prompt"] = r.get("prompt") or starter_prompt(r["doc"])
        assert row["prompt"], f"no starter prompt for {r['doc']}"
        d["handoffs"].append(row); added.append((row["text"], len(row["prompt"])))
    print(f"business {len(biz)} -> {len(d['business'])}; removing {len(removed)}; handoffs -> {len(d['handoffs'])}")
    for t, n in added: print(f"  + {t}  (prompt {n} chars)")
    if not apply: print("(dry run — pass --apply to write)"); return
    d["allowDeletes"] = [f"business::{t}" for t in removed]
    print("POST:", json.dumps(req("/api/todos", d))[:200])
    back = req("/api/todos")
    print("VERIFY business:", len(back["business"]), "handoffs:", [(t["text"][:30], t["status"]) for t in back["handoffs"]])

if __name__ == "__main__": main()
