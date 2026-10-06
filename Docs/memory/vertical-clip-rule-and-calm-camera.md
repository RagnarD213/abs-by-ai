---
name: vertical-clip-rule-and-calm-camera
description: "10-01: horizontal clip in a vertical = fill, else centre square, else whole (kit9x16/clip_fit.py decides per clip); Dan wants the follow-camera about 30% calmer (kit_track --tolerance)"
metadata:
  type: feedback
---

Dan's two rulings on the RO-10 vertical (2026-10-01): every horizontal clip in a 9:16 fills the frame unless something critical is at the sides, then the centre square, then the whole clip; and the crop that follows him was "excessive and distracting", about 30 % less movement with more tolerance for being off centre, never back to no movement.

**Why:** small whole-clip cards waste the phone frame; a camera chasing every small lean reads as distracting.

**How to apply:** `kit9x16/clip_fit.py` (called by `sheet_to_kit.py`) makes the call with two small vision calls per clip; his flips go in `<build>/clip_overrides.json`. A neutral "is anything lost" prompt picks the square for everything: the prompt must state fill as the default and list the strong reasons. `kit_track.py --tolerance 6` is the 30 % setting (20 is the calmer option he was shown). A square card must end above the caption line. Related: [[edit-sheet-and-kit-sheet-path]].

**2026-10-02 update (standing rule):** in verticals and squares, fill as much of the screen as the clip allows: crop the sides as far as the content goes, at any shape between whole clip and full screen, placed on the subject; blank space only when the sides must be kept (the salad table). Dan found round 2's squares still too timid ("be a little bit more aggressive"). Also applies to phone demos (larger, higher) and photos in fact cards. In VIDEO-RULES "Verticals and squares".
