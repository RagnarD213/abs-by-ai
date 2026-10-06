---
name: vertical-clip-fill-rule-and-calmer-camera
description: "10-01: horizontal clips in a vertical fill the frame, else centre square, else whole clip; hard cuts; Dan wants about 30% less tracking camera movement"
metadata:
  type: feedback
---

Dan, 2026-10-01, on the RO-10 vertical graphic-lock page: a horizontal clip in a vertical fills the phone frame by default ("Use B unless there's a strong reason not to"); if that cuts something critical at the sides or cuts body parts, use the centre square; if the square still cuts too much, show the whole clip. Returns from cards are hard cuts. He also finds the crop that follows him "excessive and distracting" and wants about 30% less camera movement with more tolerance for being off centre, without returning to no movement.

**Why:** small cards leave too much empty space on a phone; over-eager tracking distracts.

**How to apply:** rule text in `VIDEO-RULES.md` ("A horizontal clip in a vertical"). Tracking lives in `kit9x16/kit_track.py` and `_shared/cut/landing.py`. Both are queued in `Handoffs/handoff-20261001-vertical-kit-round2-full-build-after-lock.md`. Related: [[edit-sheet-and-kit-sheet-path]], [[no-height-crop-horizontal-in-vertical]].
