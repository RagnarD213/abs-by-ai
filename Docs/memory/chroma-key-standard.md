---
name: chroma-key-standard
description: House green-screen key since 2026-10-21 is Claude's DS-40 R2 key (replaces Codex R3); the bar and where the code is
metadata:
  type: project
---

Dan locked Claude's Bill Maher Fat 90-Year-Old R2 key (DS-40) as the default for every green-screen video on 2026-10-21, after picking it over R1: "lock this chroma key as our default way to chroma key things" and "Let's make all our future chroma keys this clean and make this a standard." It replaced the Codex R3 key he had locked the day before.

**Why:** the R2 finishing pass made edges steadier than the raw camera (motion-free flicker 0.68 hair), removed the dark rim (2.7% vs 14.9%) and the see-through watch; independent review SHIP. Dan said the two rounds "look pretty close" on the blue field; the gains show on light backgrounds and hair at full size.

**How to apply:** key with `.claude/skills/_shared/chroma-key/reference/ds40-claude-r2/` (README in `_shared/chroma-key/`), recalibrate plate, crop and hold-out boxes per source, measure with `measure_r2.py` and `mcflicker.py`, check over saturated pink. Related: [[shoot-1015-format]].
