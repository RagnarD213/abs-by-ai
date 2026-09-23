# RO-05 recipe: organic long-form from a HANDHELD multi-roll kitchen shoot (8/3, C1535-C1556 + GoPro)

First Claude build on the Codex/Muhammad organic component kit (06-organic-r4 muhammad_graphics.py). Work dir
`/Volumes/Extreme/_edit_work/ro05/` (media stays there). Order: `ranges.py` -> longform-edit `build_edl_multisource.py ro05
ranges.py` -> `timeline.py` (speed splits, frame-exact pieces, word map) -> `build_voice.py` (lav ch1, sample-exact) ->
`measure_heads.py` (5 samples/piece, keyed by source@src_in) -> `framing.py` -> `gfx_plan.py` -> `place.py` -> `build_beds.py`
-> `make_srt.py` -> `run_r6.sh` (render, NOGFX render, voice_chain, audio_gate, final Whisper, plan, watch pass).

What this build learned (fold into the skill when it is approved):
- pick_lav chose the far mic on C1538/C1550 by arrival time; a 10-band tone match against neighbouring rolls proved ch1.
- A 30 fps finished master cannot be reused as pixels on a 29.97 cut: rebuild the split screen from raw + the old build's
  per-beat screen map (build_graded.py BEATS) instead.
- Handheld source: strict W/T alternation within a roll, measured head size across rolls, 28% punch (Muhammad depth),
  never punch a >=40% close-up; the synced GoPro as a second angle for same-size joins and operator whip pans.
- Graphics: place per graphic by measuring face+hair on 5 rendered frames with a 60 px margin; if every position hits the
  face, change the content (move onto a cutaway, or make it a full-screen stat card), never accept the overlap.
- A cutaway longer than its remaining source makes ffmpeg pad frames; every scene is frame-counted after encode.
- Clipped lav transients overshoot after AAC even with --oversample 4; --tp -4.0 fixed true peak; the bed then needed -40.
