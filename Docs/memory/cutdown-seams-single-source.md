---
name: cutdown-seams-single-source
description: A selection cutdown's seams and caption lists are where the defects hide; derive each number once and prove the picture against the master
metadata:
  type: project
---

A ≤0:59 cutdown selected out of an approved master is where the real defects are, and the
gates do not see them. On the Ad 1 square (2026-09-12) three independent audits refused the
cutdown three times after `qc.py`, the watch pass, the hair gate, the caption gate, the
landing check AND `_shared/deliver/gate.py` had all passed it.

**Why:** `-ss "{t:.4f}"` drops a frame whenever the rounding lands above that frame's own pts,
and the frame COUNTS still come out right — so every duration check is green while the content
is shifted. Whisper word times truncate fricatives, so a range end cut the "s" of "abs." at its
loudest point. And the cutdown's mute list and word list were each derived twice, from sources
that disagreed by milliseconds, which was enough to make the subtitle gate grade a grouping the
renderer never produced.

**How to apply:** seek half a frame early and **assert every range's first and last frame
against the master on the pixels** before the mux; take range edges from the CTC alignment and
carry an end forward until the mix itself goes quiet (not to the word end); write the mute list
and the word list ONCE, from the lists handed to the renderer, and have the gate read those
files. Any number a gate re-derives instead of reading is a number that can disagree with the
render. Tools and the full write-up: `.claude/skills/shortad-from-longform/reference/a11_sq_ad1/`,
SKILL.md [[muhammad-trial-edit-analysis]] section **[S1] 22–24**.
