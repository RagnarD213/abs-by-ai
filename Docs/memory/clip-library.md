---
name: clip-library
description: "09-29: every reusable AI clip + B-roll clip is catalogued (IDs A####/B####); search it before generating, register new clips after"
metadata:
  node_type: memory
  type: project
  originSessionId: 222454e2-6d28-4d50-8d25-8325eee18c0c
  modified: 2026-09-30T00:02:04.598Z
---

Dan asked on 2026-09-29 for one organized home for all AI clips and B-roll so editors reuse clips instead of generating new ones or hunting.

Built: `clip_library.py` in `.claude/skills/_shared/cliplib/` (README there). Files in the Extreme Video Asset Library folders 03/04 by category, mirrored to Drive folder `1Hby8O4mB4HZS341qvrVKHSHyCGBgP8mi`; catalog `Media/clip-library/catalog.json`; human view is a Google Sheet in that Drive folder. First sweep: ~560 clips (mostly Pexels stock, ~150 AI).

**Why:** Dan wants reuse by default; generation and stock hunting cost money and time.

**How to apply:** any clip-sourcing job runs `clip_library.py find` first and `add` when done (rule in `_shared/VIDEO-RULES.md`). Filmed B-roll cutting is a separate handoff (`Handoffs/handoff-20260929-cut-broll-into-clip-library.md`). The Sheets API is off on rclone's project, so the Sheet is refreshed by uploading an .xlsx over it. Related: [[drive-always-public]], [[ai-clip-artifact-giveaways]], [[home-ab-demos-reuse]].

November16 sweep: all18 Batch4 picks installed (A0272–A0289),52 checked clean alternates (A0290–A0341) and five shipped AI demos (A0342–A0346) registered.343 usable AI clips at this snapshot. `07 AI Generation Source Archive` separately preserves1,168 source/alternate exports, including rejected/unreviewed takes; these are not cleared for edits. Audit and current library/archive links: `Docs/AI_CLIP_LIBRARY_AUDIT_20261116.md`.

Mandatory standard, Dan 2026-11-16: every new business AI video take is preserved promptly in the library source archive, including rejected/unreviewed/unused takes. Every cleared clean keeper gets a permanent usable ID, Drive verification, sheet refresh and job-doc reference. A job cannot close until output counts reconcile to archive entries and keeper IDs. See the canonical all-output filing section in `_shared/cliplib/README.md`; this supersedes save-only-used-keepers and omit-rejected-source instructions.
