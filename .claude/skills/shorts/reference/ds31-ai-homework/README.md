# DS-31 AI Homework SFC R1: dedicated Short from a raw 9/23 portrait roll (C1720)

Work folder (media, gitignored): `/Volumes/Extreme/_edit_work/ds31/round1/`. Run in order from there:
`prep.py` (cut list, approved voice recipe refit with `audio_refit.py`, word map, captions) > `aichat.py` (full-screen
AI chat screen) > `picture.py` (Pair B camera holds with Color A + land-then-hold tracking, B-roll) > `finish.py`
(Soft Blue ribbon cards, captions, mux) > `gateplan.py` (graphic MOVs, windowed delivered ASR, gate plan) > `page.py`.

Reuses the DS-28 Meal Prep approvals for this studio set (Pair B crops, Color A, caption style, card style).

## Traps this build hit (2026-10-15)
- **A false start hides inside one Whisper word.** medium.en timed "a" across 367.50-369.56 s: really "Use the paid Cl-",
  1 s of silence, then the clean retake. Trimming only the pause kept the false start; the gate's `junk:repeated_take`
  (STRETCH) caught it. Re-transcribe 2-3 s windows either side of any long word before choosing the cut.
- **Whole-file Whisper on the delivered Short skipped two sentences** ("You'll be more likely to use AI..."). Windowed
  passes split at the edit joins read the same audio correctly. `gateplan.py` transcribes in windows.
- **Framing measurements keyed by film frame go stale when the cut list changes.** `picture.py` drops cached rows whose
  stored source time no longer matches.
- **The card font has no single guillemet (U+203A):** it prints a comma. Draw the arrow as a shape (DS-28's cards show the comma).
- **The approved DS-28 voice curve measured 5 dB duller at 5.5 kHz on this take.** Refit the tone to the take, same method.
- **Stock review:** adult college-age subjects only for a college Short; no phone-gazing; the clip must act the line
  with the sound off. Three audits rejected a spreadsheet clip for "use AI", a café writer, a middle-schooler and a
  primary classroom.
- **A kettlebell in-point 5 frames off lands in the upswing blur.** Pick in-points on sharp upright frames.
- **AI frames:** END frames come back 941x1672; resize to 1080x1920 before the gate. A model END that shortens a prop
  (snapped chalk) can be fixed in code by moving the broken tip and filling with the prop's own body, with a connected
  mask limited to the prop's rows. Feather any background lock (45 px) after gain-matching, or the reviewer sees the seam.

## Round 2 (2026-10-18): colour options + A1 motion, recipe in `r2/`
Work folder `/Volumes/Extreme/_edit_work/ds31/round2/`. Order: `col_options.py stills samples` > `col_options.py pick C` (writes
`col/pick.json`, read by `picture.py`) > `col_options.py broll` > `a1_cut.py TAKE 1.042 4.0` > `picture.py` > `finish.py` >
`gateplan.py` > `page.py`. Dan asked for warmer, more vivid colour at the same brightness.
- **Warming the whole picture greys a teal backdrop.** colorbalance red-up / blue-down on this set made skin warmer but cut the
  backdrop's saturation and pushed its hue toward green; global saturation or vibrance on top turned skin orange first. Fix:
  one luma-preserving 3D LUT (BT.709 Y'CbCr) after A's denoise + curve: a warm chroma push on warm hues and near-neutrals only
  (hard-edged mask off the cool band, eased in shadows), a base saturation, an extra lift on the cool band (backdrop, tubes)
  with a few degrees of rotation toward blue, a small lift on skin. `build_lut()` in `r2/col_options.py`.
- **ffmpeg `huesaturation` measured as a no-op** on these frames (backdrop saturation unchanged at every setting). Do not rely on it.
- **Match brightness on MEAN luma with a gamma term.** The median luma sits inside the black tank top's cluster and jumps, and
  `eq=brightness` clips blacks non-linearly; both made the search oscillate. Bisection on `eq=gamma` converges to 0.001.
- **Veo motion (Flow, subscription):** take 1 of the first prompt bent the stack like rubber and dropped it AWAY from him while
  he still ended up buried; the prompt must say which side he is on, that the stack is rigid real books, that it falls
  toward him, and that nothing falls in from above the frame (`r2/A1-motion-used.txt`). Of two retakes, one bent into an arch
  over his head (rejected by eye); the other passed clipcheck and a fresh frame-reviewer. Budget a retake per AI clip.
