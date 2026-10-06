---
name: caption-trailing-entry-overprint
description: The concat demuxer's trailing file line is rendered — Ad 1 and Ad 2's approved 9:16 verticals print a caption over their closing CTA pill
metadata:
  type: project
---

`captions.py` assembles caption states with ffmpeg's concat demuxer, which needs one more
`file` line after the last `duration` — and **that line is rendered**. Writing the last caption
STATE there re-showed its lit word past its own planned end: "six pack abs," printed across the
closing CTA pill's "With Abs" for 7 frames, while `cap/list.txt` ended correctly at the pill's
own mute start, so nothing upstream could see it.

**Why it matters beyond one build:** the lesson was written up on the Ad 2 square (SKILL.md
[S1].6) and never applied in code, so **the APPROVED and UPLOADED 9:16 verticals of Ad 1 and
Ad 2 both carry the identical overprint today.** Fixed in `reference/captions.py` 2026-09-12
(the trailing entry is the blank, held).

**How to apply:** if Dan wants the two verticals cleaned up it is a caption rebuild plus a mux —
no re-render, ~5 minutes each — and then a re-upload, which changes the YouTube video id and
would break the Demand Gen ads pointing at them. Ask before touching anything already running.
See [[cutdown-seams-single-source]].
