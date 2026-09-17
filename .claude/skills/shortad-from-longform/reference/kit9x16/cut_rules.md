# The pose-matched cut — the kit's rule for every picture cut inside a talk beat

**Why this rule exists.** Phase 3 of the video-quality engine (2026-09-16, `_shared/deliver/watch.py`) measured
that, at the picture level, one of the rejected Ad 1 attempt-1 jump cuts is **not distinguishable** from one of
Muhammad's own same-scene cuts: his 16:9 masters carry **7.6–9.5 same-scene cuts per minute** and attempt 1
carried 14.2. What separates his is not the count. It is **where each cut sits**: `a2/piccuts.py` recovered
from his Ad 2 that **22 of 33 picture cuts sit off the audio splice by −15..+10 frames** (confidence ≥ 0.6), on
a frame where the outgoing and incoming takes match in pose. Attempt 1 cut the picture ON every audio splice.
Dan: *"truly awful… definitely won't work."* The gate cannot catch a single splice placed on the audio; only the
rule can. So the kit cuts the way he cuts, and writes down the numbers.

## The rule (`kit_cuts.py`)

For every audio splice `s` whose both sides are TALK (not hidden under a card, a bleed, a window plate or a
flash), the picture cut is placed at `s + k` frames, `k ∈ [−15, +15]`:

1. **From a master** (`--from-master`, his render on disk): `k` is **his** cut, recovered with `piccuts.py`'s
   method — render both takes over ±15 frames at the grade, fit each to his framing (scale / fy search) and
   match against his frame with a high-passed NCC; the crossover frame (last frame that matches the outgoing
   take, first that matches the incoming) is his picture cut. Confidence = min(mean NCC before, mean NCC after).
   Below **0.60** the recovery is not trusted and rule 2 decides.
2. **From raw** (`--from-raw`, no render to recover from): `k` is the frame where the two takes **look most
   alike** — the outgoing take's frame at `src_out + k` against the incoming take's frame at `src_in + k`,
   high-passed NCC over the head-and-torso box at the grade, both frames cropped to the same 9:16 window the
   render will use. Search `k` over −15..+15 in steps of one frame. Pick the maximum; **ties within 0.02 go to
   the smaller |k|**, so the picture stays as close to the audio as the pose allows.
3. **EVERY bare talk-to-talk cut gets a framing LEVEL STEP on the cut frame** — the zoom-cut system of
   the studied ads (`/ad-edit` Step 3: *"alternate strictly — never two identical framings across a
   join"*). **Measured 2026-09-16 on the kit's first Ad 1 render:** the pose-matched frame alone left eight
   cuts reading as jump cuts on the phone, at self-similarities 0.46–0.67, two of them on HIS recovered
   frame (confidence 0.64 / 0.79) and two inside a *ramped* push — at the vertical's 1.78× magnification
   a ramp does not hide a residual jump. So the picture punches in (instantly, 1.00 → 1.20) or pulls out
   (instantly) ON the cut, alternating cut by cut; a cut at a beat boundary or under a flash needs none.
   Ramped pushes then fill only the stretches with no cut, at his cadence. The steps are reported
   separately (`level_steps_per_min`); they are not his ramped pushes — his cuts do not need them
   because his frame choice hides them, which is exactly what our instrument could not reproduce.
3b. **A moved cut keeps at least 8 frames of both takes** (`cut.min_take_frames`): the first render left
   an incoming take on screen for 1 and 2 frames before the next insert (113.9 s, 81.1 s), which reads
   as a flash of a different take. `k` is clamped to the room that exists.
3c. **The similarity cover trigger stays as a warning.** Where the best match is below `cut.cover_below`
   the cut is additionally covered as before: If the best similarity is below the
   **cover threshold** — calibrated, not guessed, by `kit_cuts.py calibrate`, which measures the same
   self-similarity on Muhammad's trusted Ad 2 cuts (corpus `muhammad-ad2-16x9`, at HIS recovered `k`) and on
   attempt 1's naked splices (corpus `ad1-vertical-attempt1`, at `k = 0`) and writes both distributions to
   `piccuts_calibration.json`; the threshold is the midpoint of the two medians and is stored in
   `template.json` `cut.cover_below` with the date — the kit does one of:
   * **a push** — a zoom ramp (template `push.ramp_in_s`) that starts ~0.25 s before the cut and lands after
     it, so the join sits inside a framing change (the eye reads a re-frame, not a jump);
   * **an insert** already scheduled within ±1.0 s is pulled to straddle the cut (its `t0` moved earlier by up
     to 0.5 s) — his own device: an insert covers the trim;
   * only if neither is possible, a **5-frame cross-dissolve in the base** (`build_base_pic.py`'s patches),
     the documented fallback from `/shortad-from-longform` Step 7c. **Never a dissolve on a cut that could
     have been pose-matched** (SKILL.md: *"his frame choice is"* the fix).
4. **Both takes must exist over the shifted range.** A positive `k` extends the outgoing take past its audio
   out-point; a negative `k` starts the incoming take before its audio in-point. If the raw does not have the
   frames (take at the end of a roll, or a splice inside the same take), `k` is clamped to what exists and the
   rule records `clamped: true`.
5. **The audio never moves.** Only the picture cut moves. The conform of the picture (`kit_base.py`) is built
   from `edl_picture.json`; the audio is built from `edl_final.json`; the two share the timeline.
6. **Every decision is written to `piccuts.json`**: splice time, `k`, confidence, method, whether it was
   covered and by what. The plan builder reads it: moved cuts go into `joins` (so the gate's boundary strips
   and `cut:naked_splices` know them), covered cuts into `covered`.

## The numbers the rule carries

| number | value | where it was measured |
|---|---|---|
| search window | ±15 frames | `piccuts.py` W=15; his Ad 2 cuts landed in −15..+10 |
| trusted recovery | confidence ≥ 0.60 | `piccuts.py` (corpus `muhammad-ad2-16x9`: 22 of 33 ≥ 0.6) |
| match box | head + torso, hp-NCC (Gaussian 1.2) | `piccuts.py` (`his_hp[30:200,120:360]` of a 480×270 fit) |
| cover threshold | **0.44** (`template.json` `cut.cover_below`) | `kit_cuts.py calibrate` 2026-09-16: his trusted cuts at his k median 0.501 (p10 0.439); attempt 1 at k=0 median 0.379 (p90 0.517). **They overlap** — similarity is the cover trigger, not the discriminator (rule 3) |
| push ramp | 0.50 s in, 1.5–3.5 s hold, 0.5–0.8 s out | `_shared/reference/picture.json` `pushes_hand_per_min`; Ad 1 `beats.PUSHES` |
| his same-scene cut rate | 7.6–9.5 / min (no plan) | `_shared/reference/picture.json` `naked_splices_per_min` |
| the gate's bound | 12 / min | `_shared/deliver/formats.py` `cut:naked_splices` |

## What this is not

* Not a jump-cut *detector* — that is `cut:naked_splices` in the gate, measured on the delivered pixels.
* Not a licence to move cuts for concealment. A12.1b in the skill: *"where a join is least visible" is a
  different question from "where he cut"*. From a master the answer is his frame; from raw the answer is the
  pose-matched frame, and a cut that does not match is covered.
