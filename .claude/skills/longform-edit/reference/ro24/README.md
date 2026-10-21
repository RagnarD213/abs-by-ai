# RO-24 "Reacting To Celebrity Ozempic Transformations": the 16:9 green-screen recipe (round 1, Claude Opus 5.5, 2026-10-20)

First 16:9 long-form on the 10/15 green screen (roll C1726, Sony FX30 4K S-Cinetone, lav left channel only). Dan's round-1 scope:
"dial in that chroma key and make sure we have that locked in and as good as it can possibly get before we proceed to other
things", plus audio, colour and the first minute. Work dir `/Volumes/Expansion/_edit_work/RO-24/round1/` (Extreme was 99 % full).

## The key on a 16:9 roll (`key16.py`)
The locked Bill Maher (DS-40) maths, unchanged: R2 body/arm matte (`round3-key_v2.py`) + R3 five-frame fine hair (`round3-key_v3.py`),
prev/next flow smoothing in the hair band, the hair ROI handed over above the forehead. Only geometry was re-measured:
- **Head scale S = 0.75** of the DS-40 portrait head in native pixels (head width 420-480 px vs 640-740; hair top to glasses 280 vs 315).
  Every portrait distance (hair band top+470/fade 180, support band 75/25, colour blur 22, handover 315/160) is multiplied by S.
- **The ROI and the handover follow Dan:** a per-piece box and hair ROI measured at 1/8 scale, handover rows from each frame's own
  hair top (median of the last 9), not fixed rows.
- **Garbage matte:** only the large connected foreground survives; the screen's dust spots and creases far from him are 0.
- **Screen field: a clean plate** (`plate.py`, per-pixel median of 40 frames, filled with the quadratic plus a smoothed residual where
  Dan always stands). The 16:9 screen has vertical folds and low creases; the quadratic missed by up to 0.03 green excess near his
  head (17 % of the screen's own). The plate measured a touch tighter on arm edges and the same elsewhere.
- **Speed:** directed DIS flows are cached by frame pair (each pair was computed twice). 1.7 s/frame on a quiet Mac, 2.5-3 s busy.
- Output: FFV1 gbrap16le (lossless RGB + alpha, no YUV round trip), UNPREMULTIPLIED colour at 2880x1620 (0.75 native; the tight
  0.74 crop is still above 1080p). `comp16.py` grades the foreground once and composites; `assemble16.py` cuts W/T framings.

## The "refined" variant (Dan picks in round 1)
Measured residual flaws of the approved key on this roll, fixed after the merge, alpha shape elsewhere untouched:
1. Solid hair and forehead at alpha 0.83-0.99 (19 % of interior head pixels) let the background tint them: deep inside the
   silhouette (9 px erosion of a > .5) alpha above 0.80 lifts smoothly to 1. Real gaps below 0.80 stay.
2. Olive outline on semitransparent edges: continuous local foreground colour (opaque core, Gaussian-normalised, sigma 6) weighted
   by transparency.
3. Green light wrapping onto opaque skin at the silhouette: inside a 14 px edge band, G may not exceed (R+B)/2 + 0.01.
4. Moving hands (independent review, 2026-10-20): the approved body key measures green as G - max(R, B). Skin is red-heavy, so a
   50/50 blur of skin and screen (R .52, G .50, B .32) reads ZERO green and counts as solid: fast-moving hands came out with a
   3-6 px olive outline and a cut-out look, and the screen seen between fingers stayed as a grey-olive patch. `hands()` projects
   each pixel's chromaticity (colour / its sum: brightness and the shadow between fingers drop out) onto the line from the local
   skin colour to the screen colour; pixels ON that line (residual < 0.03, so not the watch, tank or a highlight) and greener
   than skin get LOWER alpha only (min with the approved alpha), and the colour of the NEAREST opaque skin (keeps its shading).
   **Gated by motion** (DIS flow speed above ~5 native px a frame): green light bouncing onto a STILL arm next to the screen reads
   exactly like partial transparency and the ungated version ate the inner arm into a light rim. Motion blur only exists where
   something moves, so the gate is physical, not a tuning trick.
Result (`keynum.py`): interior holes 19 % -> 0.2 %, edge green halved, edge change frame to frame equal on the same pixels,
head interior steadier; the hand fix verified on the three flagged moments (`handdbg.py` for one native frame).

## Traps
- `ffmpeg` in `Media/video_edit/bin` is the render-queue wrapper: a script outside a queued step that decodes a whole file waits in
  line (an inspection read sat 7 min at 0 % CPU). Few-frame inspection reads use `ffmpeg.real` with `-frames:v`.
- Whisper's own audio loader calls `ffmpeg` on PATH: put `Media/video_edit/bin` on PATH or `whisper_chunked.py` dies at once.
- Frame-exact seeks: frame f has pts f*1001/30000; seek to (f - 0.3)/FPS.
- Hook line 2: Whisper (two models) heard "well", Gemini blind 4/4 heard "while" on the same take; the vowel measurement was
  inconclusive. Recorded on the page instead of silently picking.
- Gemini's `gemini-2.5-pro` is gone for this key; use `GM=gemini-3.1-pro-preview`.
- The coordination board was at 2,499 of 2,500 words; the job is claimed on the edit queue instead.

## Files
`plate.py` `key16.py` `comp16.py` `assemble16.py` `options16.py` `keycompare.py` `keynum.py` `hairclear16.py` (hair clearance
against the known drawn background) `inspect16.py` `audio_options24.py` `listen24.py` `voice_cut.py` `words_out.py` `quiet.py`
`env.py` `disfl.py` `edl_full.py` (whole-film take list) `extra24.py` + `page24.py` (review page) `chain_fm.sh` `post_fm.sh`
`after_keys.sh`.
