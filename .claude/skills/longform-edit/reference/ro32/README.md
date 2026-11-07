# RO-32 "I'm 41. Here Are The 10 Exercises I Do Every Week" (10/15 C1776): round 1 recipe (Claude Opus 5.5, 2026-11-05)

10/15 studio set, one roll (C1776), cut to 4:37 from 18 pieces, with gym B-roll of Dan from the 10/23 shoot (B05xx to B07xx) and
two 10/15 pool rolls. Starts from RO-31's round 1 recipe (`../ro31/`, same set): same pipeline, paths swapped. Work dir
`/Volumes/Extreme/_edit_work/RO-32/round1/` (recipe, review, logs). Never commit media.

## What is new here
- **`broll_crop.py`:** per-source auto person crop for gym B-roll (Vision personmask, largest connected component, 16:9 window, at least
  1080 rows, 4% headroom), cached in `framing/broll/<key>.json`. `resolve.py` fills `crops` (one per source in a montage); `build.py`'s
  ClipReader reads `crops[k]`. Turn it off per item (`autocrop_off=True`) where the action is wider than the person mask (hamstring curl:
  the crop centred on his torso and lost the legs).
- **`clip_audit.py`:** one sheet of every clip through the build's own grade and crop (`checks/clip_audit.jpg`). Look at it before the page.
- **Gym grade:** reuse RO-23's locked 10/23 gym grade; pool rolls get their own (`plan.py` GYM / POOL).
- **Lower-third stills show the clip under them** (`stills.py`): an lt that rides over B-roll must be judged on the gym frame, not on Dan.
- **Side-list recap past item 9:** `_shared/hyperframes/side-list/build.py` widens the number column when the last number has two digits
  (it printed "10.Tricep"). Split a 10-item recap into three cards with `first=` (the template holds at most 4 points).

## Traps this round paid for
1. **Library labels lie.** C1752 is planks, not crunches (use C1751); library A0142 has burned-in text ("AI Generated", "Barbell Row").
   Open every candidate before planning it.
2. **Most C1745 side-lateral reps go overhead.** Under "up to shoulder height" pick a window by frame (24.3 s, at most 2.25 s) or use the
   machine (B0676). The swinging rep (15.9 s) is the mistake demo only.
3. **Whisper writes numbers as list markers** ("Number four is the glute" became "4."). Anchor graphics on a word next to the number.
4. **Restarts folded into stretched words** ("It's what-", "These build-", "without ma-") only show on the level strip; the hook's real
   start was 0.1 s before medium.en's first word.
5. **The independent check caught 13 faults** after the editor's own pass, including: the RO-31 title and date left on the page, three
   consecutive cuts from one static take, a clip whose rep went too high under "shoulder height", the lockout cue shown at the top of the
   rep, the SixPackAbs lower third landing out of spoken order. Change the page title and release line first when copying a recipe.
6. **All six first AI ideas failed both image models twice.** Simpler single-action ideas (one person, one move, plain room) passed.

## Round 3 (2026-11-06): one-graphic opening and background-face blur

7. **Before then after as ONE graphic** (Dan: "look like one graphic"): `gfx.py` scene `slate_swap` draws the three before photos on
   the Soft Blue field, fades them out fully over 0.22 s at `switch`, then lets the three after panels rise in; one label throughout.
   Never crossfade a before into an after: the ripped body shows through the fat photo (rule: never a before and an after on one screen).
8. **Blurring a bystander's face** (Dan approved for two prominent gym members; small far-off people stay as filmed). Apple Vision
   missed both faces (side-on, small), so: seed a box by hand on an exact-frame grid (a 1 fps extraction frame is NOT the frame at t),
   track with OpenCV CSRT at 1920x1080 (0 lost over 16 s), smooth +-7 frames, scale x2 to 4K, pixelate /24 then Gaussian sigma 18 in a
   soft ellipse. Grow the ellipse 0.75 and shift it 0.22 box-widths toward the crown for a head seen from the side (0.45 left his bald
   crown showing). Write a new copy (x264 CRF 12, BT.709 tags) on the source timeline and point the plan at the copy with a
   "/path@start" src; never alter the library original. Scripts: /Volumes/Extreme/_edit_work/RO-32/round1/blur/ (track.py, blur.py).
   The copy ends 0.5 s after the last tracked frame; check every plan use fits inside it.
