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
