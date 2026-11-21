---
name: vertical-kit-autofill
description: "10-01: kit_run.py builds a 9:16 vertical + 59s cutdown from an editor's master with no editing session; AV-09 (Ad 8) delivered that way; routing change proposed, not applied"
metadata:
  node_type: memory
  type: project
  originSessionId: 79243625-fc3b-429b-8974-a9358c705292
  modified: 2026-10-01T13:41:30.041Z
---

Since 2026-10-01 the 9:16 vertical kit fills in its own content sheet. `kit9x16/kit_run.py --master HIS.mp4 --build B
--name "<title> | claude | 9x16 | ad N" [--deliver <ad folder>]` runs recover, measure, content, render, the gate
pre-check, then stops for the judged watch pass (3 fresh session judges), then fold, cutdown, deliver. Proven on the
Ad 10 and Ad 1 answer keys (`answer_keys/PROOF1.md`, `PROOF2.md`); AV-09 (Ad 8) full + 59s delivered by it, both
gate PASS, awaiting Dan's review.

**Why:** Dan wanted verticals as one command, no editing session, never asking the editors for anything.

**How to apply:**
- Read `kit9x16/README.md` first (For Dan paragraph, build order, what escalates, round lessons).
- The session judges are still required: Gemini as judge missed most defects (0 to 4 of 13). AI cost per clean
  vertical is about 15 cents (physique checks half a cent, cutdown pick about a dime).
- An escalation or a judge finding is fixed in the KIT, then the build reruns; never hand-edit content.json.
- After a small fix use `carry_verdicts.py` so only changed watch images are re-judged.
- Routing change (AV/AS jobs run kit_run first, a model session only on escalation) was PROPOSED to Dan 10-01, not
  applied; `scripts/edit-queue/config.json` is unchanged until he says so.
- Traps: never put a work tree under `/private/tmp` (a restart wiped it mid-build, see [[qc-corpus-worktree-trap]]);
  run `gate.py` detached (`nohup ... &`), in the foreground of an agent shell it can hang for hours; the picture
  library re-indexes (about 40 min) whenever [[clip-library]] files change.
