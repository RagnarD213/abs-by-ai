# RO-37 round 2 recipe: portrait footage cut out (BiRefNet) on the long-form green-screen background template

Dan approved the cutout on 2026-10-29 ("Yes, this cutout works... edit the video this way"). Live copies:
`/Volumes/Expansion/_edit_work/RO-37/round2/recipe/` (media never committed). Round 1's cut, words, grade, voice, B-roll tune and
HyperFrames graphics are imported read-only from `round1/recipe` (`r2.py`).

Order: `prep_bg.py photos` -> `plan_bg.py` (template rules on this film's facts; overrides in `bg_overrides.json`) ->
`matte.py run geo` (every 15th frame of every cut-out shot: fixes each shot's placement over the WHOLE shot before anything
renders) -> `matte.py run first-minute` -> `prep_bg.py clips` -> `greenscreen-bg/hfbg.py` (big type) -> `stills.py` (one
still per background segment) -> `lt2.py --render` -> `assemble.py` per range -> `mux.sh` -> `matte.py run contexts` ->
context ranges -> `context.py`, `colour.py`, `checks.py`, `make_extra.py`, `page.py`.

Traps this round paid for:
1. **Matting speed:** BiRefNet on Replicate ran 0.6 frames/s at 14 threads (cold), 2-3.5/s later at 32 threads. Mattes are
   stored per roll frame at 1152x2048 (`matte/<roll>/<frame>.png`), grade-independent, so no frame is paid twice. ~$0.002/frame.
2. **Lower thirds beside a cut-out presenter:** measure the TORSO edge (the solid run of the silhouette through the body
   centre, 10th percentile over frames), not the full silhouette: his gesturing hands pushed the edge 60 px left and a point
   would not fit in two lines. `lt2.py` wraps at part boundaries onto a second line (the template's per-part `y`).
3. **Green spill from the pool hedge** on the back of the hair, and a light line on the cheek from the bright wall:
   despill (G <= max(R, B)) in an 8 px band along the silhouette edge, top 55 % of the frame only (his shorts are green),
   plus alpha tightened (a-0.12)/0.88. Visible only at full size: zoom a hair crop before sending.
4. **Forced cuts (lower-third in/out) can leave Dan still while the background swaps**, and a W/T flip to fix it can land on a
   take join (jump). `r2.final_shots` flips, then cascades; `r2.checks()` must print no jump and no still_bg_swap.
5. **Big type behind a tight right shot:** `max_w` 680, or "15 MINUTES" runs behind his head.
6. **Module name collision:** round 1's `build` shadows the shared `lower-third/build.py`; import it by path (importlib).
7. **Glass band must be ints** (composite.py slices with it).
8. **A library take shorter than round 1's slot** (B0691, 2.7 s): start earlier in the take, never hold a frame.
9. **Heavy render line blocked for an hour** behind other videos' keys: the Python compositor (2-3 fps, single-threaded)
   runs honestly in the light lane.
10. Close-up segments have no matte: `stills.py` must not ask the sparse pass for one.
