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
   **Four limits, each from a defect an independent check found:** (a) motion: only from 40 native px a frame (full at 60);
   green light bouncing onto a still or slowly drifting arm reads exactly like partial transparency (light rim on the inner arm);
   the flagged fast hands move 100-170; (b) brightness: a blend cannot be much darker than both the skin and the screen beside it,
   floor max(0.20, 0.72 x the darker of the two), or olive shorts, the watch glass reflecting the screen, shaded skin and the
   mouth go see-through (they sit on the same skin-screen colour line); (c) reach: only within 6 px + 0.6 x speed of a screen
   pixel (blur cannot reach deeper than the hand travelled); (d) colour: every clear blend pixel takes the nearest skin's colour
   fully, or a khaki rim stays. Test harness: `handtest2.py <out> <frames...>` (real motion from the neighbouring frames, counts
   lowered solid pixels that are dark or deep, saves raw | approved | refined | lowered tiles). Frames that need nothing must
   come back with 0 lowered pixels.
Result (`keynum.py`, final r5 keys, re-check 3): see-through head/hair 20.1 % -> 0.4 % of interior pixels, edge green 0.0143 ->
0.0058, edge change frame to frame equal on the same pixels. Moving hands: about half the finger-gap green is opened (49-52 % of
what the ungated version opened); costs a 0.1 s pale streak on the shorts at film 25.0 s and a watch-bezel ring at alpha ~0.8.
Verdict: refined is better on balance for this roll; the remaining flaws are listed with times on the round 1 page.

## Traps
- `review_server.py` serves a CACHED copy of the page (`~/Library/Application Support/AbsByAI Reviews/<port>/page`). Rebuilding
  `review/index.html` changes nothing Dan sees: re-run `review_server.py <port> <review dir>` after every rebuild, then compare the
  served video's sha256 with the file (re-check 3 found the page still serving a version two rebuilds old).
- Moving-hands balance point (five versions, four independent checks): each version that opened more finger gaps also opened
  the olive shorts or the watch. Speed gate 40-60 px kept the shorts solid but opened ~40 % of gaps; 12-24 px opens ~50 % and
  brings back a short streak where a moving hand meets the shorts. Requiring screen-coloured seeds to be screen-bright changed
  nothing (those openings are not seed-driven). Untested next idea: a motion-compensated test of whether the screen shows at that
  pixel when the hand is not there (true for finger gaps, false for hand-over-shorts).
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
