---
name: edit-sheet-and-kit-sheet-path
description: "10-01: every 16:9 writes <master>.edit-sheet.json; kit_run.py --sheet builds the 9:16 from it with Soft Blue Light HyperFrames graphics; state and traps"
metadata:
  type: project
---

Since 2026-10-01 a finished 16:9 (Claude or Codex) writes `<master>.edit-sheet.json` (`_shared/edit-sheet/`: README, `validate.py`, `sheet_from_claude_build.py`, `CODEX.md`). The vertical kit has a second way in, `kit9x16/kit_run.py --sheet SHEET --build B --name "..."`, which skips recover / measure / content (planning takes about 12 s) and draws every graphic at 9:16 with HyperFrames (`_shared/hyperframes/vertical.py`, new templates `title-card/`, `media-card/`, `cta/`; `kit9x16/sbl_graphics.py`, `render_sbl.py`, `sbl_preview.py`, `sbl_page.py`).

**Why:** Dan: "I plan to edit all videos with Claude and Codex going forward" and no more olive graphics ([[old-graphics-retired-soft-blue-hyperframes]]). Reverse-engineering our own edits was over an hour per vertical and the main source of stops.

**How to apply:**
- Plan items for clips and photos must carry `people` (dan / other / none) and `physique` (true / false) beside `label`; the sheet writer refuses to guess (a `--facts` file covers older builds).
- Codex's builds cannot be converted: layout differs per job and the newest (RO-17) records no head position, no graphic text as data, no real/AI label. Codex must write the sheet itself (`Handoffs/handoff-20261001-codex-write-the-edit-sheet.md`).
- State on 10-01: proven through the first minute and every graphic of RO-10 on a review page; the 9:16 look awaits Dan's lock. NOT yet run on a sheet build: `kit_plan.py`, the gate pre-check, judges, fold, cutdown.
- The ad gate's ranges (Muhammad's ads) do not fit an organic long-form vertical (RO-10 plans 0 flashes, 0 CTAs, 49 s longest talk). Never move the bounds; it is Dan's ruling.
- Traps: grade in the 16:9's order (`grade.order`) or the conform crawls; a killed conform leaves a half segment the next run skips; exFAT `._` twins break globs; work tree `~/abs-worktrees/kit-sheet`. Related: [[vertical-kit-autofill]], [[hyperframes-decision]], [[review-page-what-i-decided]].
