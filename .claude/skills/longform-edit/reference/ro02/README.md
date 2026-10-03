# RO-02 "The Vacuum: The Best Ab Exercise For Belly Fat" (8/14 poolside, C1614-C1629): round 1 recipe (Claude Opus 5.5, 2026-10-03)

First long-form in this recipe family cut from MANY rolls, outdoors, from a 1080p source. Round 1 is the cut and the
look only (colour, framing, sound); graphics and clips join in round 2 from `../ro13/` (`plan.py`, `resolve.py`,
`gfx.py`, `stills.py`, the plan loop in its `build.py`). Work dir and media: `/Volumes/Extreme/_edit_work/ro02/`.

Order: lav per roll from each roll sidecar's measured filter -> `edl.py` (pieces carry their roll) -> `verify_asr.py`
on every splice -> `shots.py` -> `assemble_audio.py` -> `asr_assembled.py` (medium.en) -> `words_out.py` ->
`measure.py` (where he is) -> `skin.py` (how bright he is) -> `grade.py` (colour cubes) -> `frames.py` ->
`lookstills.py` -> `build.py range` -> `hair_first.py` -> `page.py`.

What is new against RO-10/11/13:
- `edl.py`: `(id, roll, in, out, ...)`; the voice threshold is measured per roll (room floor + 10 dB), because the pool,
  the waterfall and traffic put the floor near -55 dB where the studio sat at -65.
- `frames.py`: no fixed crops. FAR (x1.45) and NEAR (x1.80) are placed per shot from `measure.json`: centred on his
  head, top edge 50 / 40 source px above the highest his hair gets in that shot. Fixed inside a shot.
- `grade.py`: the approved poolside colour (Codex organic colour v1: per-channel LUT, matrix, tone curve) is pointwise,
  so it bakes into a 3D cube for `lut3d`. `pre_gamma` is the per-shot exposure trim.
- `build.py`: sizes alternate at every join; the opening size is chosen so the forced shot (the live set, FAR) falls on
  its own turn.

Traps this build paid for:
- **The roll sidecars' whisper-small words are fine for finding takes and wrong for cutting.** It timed a 3 s stop
  inside one word (`for[16.48-19.30]`), put "You" 1.3 s early, and merged a restart in the ending ("That means your
  waist will get... That means your waist will get smaller"). medium.en on the ASSEMBLED cut found that restart. Read
  the assembled transcript end to end before building anything.
- **medium.en alone on a window that is mostly silence invents a sentence** ("in the next video."). Keep verify windows
  on speech, 3 to 6 s.
- **The person mask grows a stray blob on the chimney cap**, 40 px above his hair. Take the largest connected blob.
- **Clouds.** Raw torso-skin luma runs 0.275 to 0.54 across the kept pieces (0.37 to 0.52 on the rolls the colour was
  approved on). One fixed gamma per shot pulls it into 0.38 to 0.50; capped at 0.75 to 1.15. Sun and cloud still differ
  in warmth; that is the light, not the grade.
- **A tightened pause can leave a 1.2 s shot.** `shots.py KEEP` lists pauses that stay (also the teaching pause where
  he shows the nose breath).
- **`grep render` in a `ps` check matches every app's "Renderer" helper.** Grep for the script name.
