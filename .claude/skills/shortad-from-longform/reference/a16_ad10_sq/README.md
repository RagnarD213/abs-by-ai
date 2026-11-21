# Ad 10 square (AS-06, 2026-10-04): the build-local kit patches

Copies of the kit's `sq_render.py`, `sq_plan.py` and `kit_track.py` as run on the Ad 10 square, plus `carry_by_time.py`. They are NOT merged into
the shared kit (other builds were editing it); fold the changes in when the kit is next opened. `HERE` in each file points at the kit folder.

* `sq_render_ad10.py`: sq_copy keys `hold_from` (a lift of the editor's master holds its last clean frame), `trim_bars` (crop the 4 px black bars of
  an AI lift, 8 px each side: a 5 px trim leaves one grey row from resampling), `extra_pushes` (a square-only closer zoom step on a pause splice the
  1080 px window shows), `beat_frames` (re-cut the boundary between two pictures), `mute_caption_frames`; stills pushed at 2x so a slow push lands on
  every frame; CRF 12 (8 to 12 Mbps).
* `sq_plan_ad10.py`: `extra_pushes` also split the plan's framing segments; the cutdown plan drops the vertical cutdown's `label_clearance`.
* `kit_track_ad10.py`: zoom times are not landing anchors (same change as Ad 6's local copy).
* `carry_by_time.py`: carries judged watch images by TIME token (strip names renumber when a boundary changes), pixel-identical image AND its pair image only.
