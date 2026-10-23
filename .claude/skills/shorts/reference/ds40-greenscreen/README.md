# Green screen keying (DS-40, the first green screen video, 2026-10-19)

Fat 90 Year Old SFC (DS-40), roll C1730 of the 10/15 shoot (portrait green screen reactions). Round 1 was key, colour
and voice only, on a 9.3 s sample (Dan's request: dial in the foundations before anything else). Work folder (media,
not in git): `/Volumes/Extreme/_edit_work/ds40/r1/`. Code here is the recipe; run from a copy in your own work folder.

## Pipeline (run in order)

| file | job |
|---|---|
| `common.py` | BT.709 10-bit decode of the portrait roll to float RGB (ffmpeg autorotates; never add a transpose) |
| `plate.py` | clean plate: per-pixel temporal median of the screen over ~100 frames of the take (1.5 fps), pixels where Dan never moved filled by normalised convolution. Saved at quarter res; the screen is smooth enough |
| `keylib.py` | the keyer (below) |
| `stage1_key.py T0 DUR OUT` | keys every frame at 4K (4 workers, about 1 s a frame), garbage-mattes the screen's top edge, crops above the laptop, then downsamples the PREMULTIPLIED foreground and alpha 2x2 to output scale and caches them (`fNNNN.npy`, float16 RGBA) |
| `grade.py` | foreground grade in BT.709 Y'CbCr: tone curve with a highlight shoulder (forehead shine), chroma gain, hue turn, warmth. `LOOKS` holds the three round 1 options |
| `stage2_comp.py CACHE LOOK OUT.mp4 CARD.png|pale AUDIO` | despeckle, unpremultiply, grade, composite over the Soft Blue field + clip card (or a pale key-check backdrop), light wrap, encode |
| `stage15_temporal.py IN_CACHE SRC_U8.npy OUT_CACHE [watch.json]` | R2 finishing pass on the cache (section below) |
| `page_r1.py` | the round 1 page from the rendered files (stills and 2x edge close-ups are cut from the delivered pixels) |
| `listen_trials.py` | blind voice ranking, repeated with fresh letters and order |

## The keyer (what each step fixed, measured on C1730)

1. **Clean-plate colour difference.** `e = (G - max(R,B)) / (plate G - max(plate R,B))`: 1 on screen, 0 or less on Dan.
   Keying against the plate instead of one screen colour handles the darker top, the side falloff and the creases.
2. **Linear edges plus a separate solid core.** A levels-style "hi" clip (alpha 0.8 becomes 1) left up to 20% of screen
   colour unsubtracted on every edge pixel: an olive line on skin over dark backgrounds. Keep the edge linear
   (`lo` 0.12 only kills screen noise) and get solidity from an eroded core of alpha > 0.85.
3. **Denoise the difference, not the picture** (Gaussian 1.2 px at 4K): screen grain read as foreground speckle.
4. **Per-frame local plate** (`local_plate`): the screen right beside Dan is a little darker than the plate (his
   shadow); the frame's own pure-screen pixels, as a ratio to the plate and filled inward, correct it.
5. **Positivity floor:** a pixel darker than the screen in any channel cannot be mostly screen,
   `alpha >= 1 - min(P/S)`. The colour difference alone read the black tank-top's green-lit edge and dark hair as half
   transparent (dark outline after subtraction).
6. **Screen subtraction:** foreground = `P - (1 - alpha) * S`, premultiplied, then zeroed where alpha is about 0
   (otherwise screen grain leaks into the new background as faint noise).
7. **Despill with the average limiter**, `G <= (R + B) / 2`, plus 35% neutral luminance back. The max(R,B) limiter turns
   spilled skin yellow; the average limiter returns it to skin.
8. **Fill enclosed see-through patches** that are not screen-coloured (dark hair gaps, shadow between hands and tank, any
   shine reflecting the screen). A true gap between arm and torso reads e ~ 1 inside and stays open.
9. **Despeckle and haze clip at output scale:** keep only components of alpha > 0.03 over 400 px plus a 3 px edge
   zone, then beyond 3 px from alpha >= 0.25 re-level alpha so anything under 0.15 is background. The dark left edge of
   the screen leaves a ~3% alpha haze (12k to 31k px a frame) whose peaks twinkle as specks beside the arm: the
   independent reviewer counted 428 across the sample; after this, 4 single faint pixels. Fast-hand blur unchanged.
11. **Watch hold-out (tracked):** the Apple Watch's green activity rings and its glossy case mirror the screen. Find the
    grey band per frame (neutral, luma 0.25 to 0.62, over 1,200 px, low in frame), and inside a 70 px zone treat pixels
    much darker than the screen as solid, plus the closed and convex outline of the black case. Still open: when the
    glass face is seen edge-on at the OUTER edge of the case (C1730 1408.5 s, about 6 frames) it is a perfect mirror of
    the screen, outside every shape rule. Plan: a hand-drawn mask on those frames. Any watch or glasses on a green
    screen roll needs this check: composite over saturated pink to see see-through pixels, pale and navy hide them.
10. **Key at 4K, composite at output size:** the premultiplied 2x2 downsample is the anti-aliasing. Light wrap 0.12,
    sigma 10 px at output.

Check every fix on the delivered pixels over a dark, a pale AND a saturated pink backdrop, at 2x, on hair, glasses, ear, shoulder
strap, and the fastest hand frame (largest frame-to-frame alpha change). A dark background hides grain and fringe.

## Set facts (10/15 portrait green screen)

- Laptop top edge is tilted: about y 3,515 on the right to 3,660 on the left (source px). Crop bottom at 3,490.
  Source rows above ~480 are the screen's top edge (not green): garbage matte them. Hair top here: 628 to 744.
- Screen excess (G - max(R,B)) 0.13 to 0.23; plate G 0.28 to 0.59. Raw skin: brightness 0.42 to 0.43, saturation
  0.52 to 0.55, highlight p90 0.59 (hot forehead shine). Approved studio film from the same camera (RO-25): 0.35 / 0.63.
- **Voice:** this lav sat close; the fitted house EQ already cuts ~6 dB at 110 Hz. The standard +3 dB bass lift was
  called boomy by the blind listener 6 of 20 times and ranked behind the house chain (5.8 vs 4.6 average over 20
  shuffled trials). A mic that already reads full gets less (VIDEO-RULES bass rule). Room EDT 61 ms raw: no dereverb.
- The voice audition needs 30 s of continuous speech; the 9 s video sample is too short for the gate's comb and tone
  rows (they fail even on the untreated mic). Gate the 30 s window, cut the sample from it.
- YouTube clip download: `~/.cache/absbyai/ytdlp/yt-dlp_macos --js-runtimes node` (the python 3.9 yt-dlp gets "The page
  needs to be reloaded"). The Maher clip is 720p max.

## Round 2 finishing pass (2026-10-20): steadier than the camera, no dark rim, solid watch

Dan on R1: "about even with Codex... work on that chroma key a little bit more". R2 kept the R1 4K key and added
`stage15_temporal.py` between stage 1 and stage 2, on the output-scale cache (about 1 s a frame with 4 workers).
Source frames at output scale for it: `srcprep.py T0 N src_u8.npy`; plate at output scale: `plate_out.npy` (plate_q.npy zoomed x2 with order 1, rows [:1745]; it sits beside src_u8.npy).
Full chain as run: `run_final.sh` (waits for a build slot). Work folder: `/Volumes/Extreme/_edit_work/ds40/r2/`.

1. **Motion-compensated temporal matte.** Each frame's alpha averaged with 3 neighbours each side (weights .85/.6/.35),
   warped with DIS optical flow on the source picture. A neighbour counts only where the warped picture matches
   (sigma 10 grey levels), the flow round-trips (sigma 1 px) and its alpha agrees (sigma 0.2). Only pixels within 10 px
   of a partly transparent pixel change, and alpha above 0.92 is kept as is. Fast blurred hands keep their blur.
   Premultiplied colour is averaged with the same weights in the band.
2. **Edge colour from deeper in.** The dark rim was the positivity floor rating the outermost mixed pixels opaque while
   they still held screen-subtraction error; decontaminating toward "alpha > 0.95" pixels just copied that dark edge.
   Take the colour from solid pixels eroded 3 px (normalised convolution, scales 1.5/4/12/36 px) and replace fully within
   2 px of the outline, fading by 4 px, plus more as alpha falls. Rim 14.9% to 2.7% (source 8%). RIM=3 gave 1.3% on test
   frames; 2 kept the natural edge shading.
3. **Speck rule.** A pixel 2 px or more from anything over 0.9, in an alpha > 0.1 island NOT joined to the body, cannot
   exceed the 5x5 max of both warped neighbours + 0.1 (picture match only; flow is loose on flat screen beside a fast
   hand). Removed the 0:04.74 grain clump. Without the island test it notched a blurred thumb (frame 234): the reviewer
   caught it.
4. **Watch glass edge-on** (`watch_r2.json`: frame range + box, output px). In the box: pixels under 0.65 of the plate's
   brightness that join the black case (ratio < 0.25), holes filled, grown 2 px into anything under 0.85; plus slits
   under ~8 px (disk radius 4) between solid (> 0.95) pieces closed (glass at grazing angle mirrors the screen at FULL brightness, frame
   236). Forced solid, colour = despilled source, 0.8 px feather. Real strap/hand gaps (screen brightness, wide) stay open.

**Measure flicker with motion removed (`mcflicker.py`).** The R1 reviewer's edge-flicker ratio is dominated by real
head movement (mean band change ~0.2 a frame), so any key that follows Dan reads ~1.0 and smoothing barely moves it
(R1 1.018, R2 1.003). Warp the previous frame onto the current one with flow on the source, drop pixels whose flow does
not round-trip within 0.5 px, then compare: R1 0.87 overall / 0.91 hair, R2 0.69 / 0.68 (source = 1.0).
`measure_r2.py` reproduces the R1 reviewer's numbers in one decode pass (pass2 flicker, outline rim, seethru4, islands).
Check the watch over saturated pink (`stage2_comp.py CACHE LOOK OUT.mp4 pink`).

**Render queue (2026-10-20).** `Media/video_edit/bin/ffmpeg` is now a shim onto `_shared/renderq/`: every heavy call waits
its turn, and a rawvideo decode for measurement is filed as heavy. Run measurement scripts with
`renderq.py run --light --group ds40 -- python3 metrics.py ...` (analysis is the light lane) and renders with
`renderq.py run --group ds40 -- ...`. On a busy evening the heavy lane was 40 deep and a 9 s render waited over an hour.
Independent review: `/Volumes/Extreme/_edit_work/ds40/r2/audit/R2-REVIEW.md` (SHIP, then SHIP on re-check).

## Round 3 (2026-10-21): reaction opening, clip full screen with small Dan in the corner

`comp_opening_r3.py`: the clip full screen (fixed vertical crop on the speaker), Dan keyed small (0.33) bottom-left over it
using his REAL reaction (the roll where the clip played on his laptop: find it by the clip audio in the roll's words.json),
then a 0.5 s move (clip shrinks into its card, Dan grows) into the R2 layout. Lessons from four independent re-checks:
- Cut the clip on word boundaries measured in the clip's own transcript: 0.1 s early let a stray "But" in; ending at the word's
  start clipped "lie" into "law". Check both ends with Whisper.
- At small size Dan's body fills the camera width: his footage must sit FLUSH on the screen edge on one side (an arm 14 px in
  from the edge ends in a straight line); on the other side use a narrow fade (12 px on screen), widened (40 px) only on the
  frames where a hand leaves the camera. A wide fade all the time makes the shoulder see-through.
- A seek's first decoded frame repeats the next one (ffmpeg -ss): never trust frame 0 of a resumed decode; seek a few frames early.
- Dissolve between two takes during the grow: 3 frames, while he is still small (8 frames showed a double image).
- 10 ms fades are too short for a voice that starts on a breath: 25 ms.

## Round 6 (2026-10-22/23): the whole Short in the locked B format, approved by Dan

Code: `r6/` (plan, renderer `comp_r6.py`, captions, graphics build, audio mix, gate plan, QA chain). Work folder (media):
`/Volumes/Expansion/_edit_work/ds40/r6/`. Delivered: `Short-form video content/Fat 90 Year Old - DS-40/`.
- **One plan file drives everything** (`r6/plan.py`): film frames, the cuts as whole-frame lengths (picture and sound stay
  locked after a cut), the BMI-table span that hides them, the card shots, every graphic time (word starts mapped to the film).
- **Roll frame grid:** C1730 frames sit on n*1001/30000 s and `-ss T` lands on frame ceil(T*30000/1001). Compute cache
  offsets from that, not from typed seconds (an earlier guess was one frame off).
- **The move from B (0.40, flush left and bottom) to full size** needs a FULL-HEIGHT key of the scripted take for those
  15 frames (`Y_BOTTOM=3840`, `ROWS=1920`): with the 3490 crop his footage would end 70 px above the screen bottom while
  small. Top goes linearly from B's position to OY 175 while the scale grows, so the bottom edge never rises above the screen.
- **Silent card footage:** download the whole episode (720p, AV1 decodes fine), locate the reaction clip in it by matching a
  frame (it was episode time + 130 s), and measure every candidate shot frame to frame for camera cuts AND for a graphic
  still sliding out at its start (the first R6 draft opened on a leaving quote card; text clears 0.4 s after the slide).
- **Watch hold-out for the B corner footage** (`r6/track_watch.py`): box per frame from the grey band, 60 px each side and
  100 px below it (the face hangs below the band); stage15's boxes are in layout px, so add 175 for a full-height cache.
  Worst frame 596 -> 17 see-through px over pink.
- **Captions during the clip** sit at top 1040 (under Maher's face, lowest y 1014, above the small Dan's head, about 1290);
  the name lower third goes right of the small Dan (x 452..1000, top 1318).
- **BMI table** = new HyperFrames template `_shared/hyperframes/bmi-table/` (dark numbers on amber: white reads 2.6:1).
- A rawvideo-decoding check over every cache frame is very slow in a 2-core light slot (44 min and not done): sample.
