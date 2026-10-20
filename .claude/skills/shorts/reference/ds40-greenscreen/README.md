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
