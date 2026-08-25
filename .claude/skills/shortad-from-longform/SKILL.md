---
name: shortad-from-longform
description: Rebuild a FINISHED, finalized long-form video as a vertical 9:16 short ad, reproducing the finished video's style as closely as possible — recover its edit from the raw footage, measure its grade, palette and graphics, re-lay them out for a phone, then cut a ≤0:59 version. Use whenever Dan asks for a vertical or 9:16 version of a finished video, to "make a short ad from" a long-form cut, to reproduce an editor's finished style in vertical, or to turn a finalized ad or content video into Shorts/Reels creative — even if he doesn't say "/shortad-from-longform". For cutting shorts out of a video we ourselves rendered, /shorts is cheaper. For editing an ad from raw shoot footage use /ad-edit; for content videos use /longform-edit.
---

# /shortad-from-longform — a finished long-form cut, rebuilt vertical

**The finished video cannot be reframed. It has to be REBUILT.** A finalized cut has
graphics, captions and lower thirds burned into the pixels; crop it to 9:16 and you crop
its type. The only honest route is to re-cut from the ORIGINAL RAW FOOTAGE and rebuild
every graphic in a vertical layout.

That sounds like starting over. It isn't — because the finished cut is a complete,
machine-readable specification of itself. **Everything the editor decided can be measured
back out of the render**: which takes they used, every pause they trimmed, their tone
curve, their vignette, their palette, their type, where every insert sits, how loud they
mixed. Recover those, and the rebuild is a conform plus a layout pass, not a re-edit.

Two deliverables, always:
1. **the full-length 9:16 master** — same script, same beats, same order as the reference
2. **a ≤0:59 cutdown** selected out of that master (never re-cut from source)

---

## Step 0 — get the reference and the raw, and never confuse them

```bash
python3 -m gdown <DRIVE_FILE_ID> -O reference.mp4      # installed for python3.9
```
`ffmpeg`/`ffprobe` are NOT on PATH — use `Media/video_edit/bin/`.

**Confirm which video and which editor before you measure anything.** Dan runs tryouts
where several editors cut the same script; a Drive file's owner is often not the person
he names in chat. Check `get_file_metadata` → `owner`.

Probe both, and transcribe the reference with local Whisper `small`, `word_timestamps=True`.
You need the raw roll's word timestamps too — a previous /ad-edit or /longform-edit session
has usually already written one (`<ROLL>.whisper.json`); reuse it.

---

## Step 1 — RECOVER THE REFERENCE'S EDIT (this is the whole trick)

### 1a. Word-sequence alignment gives take selection and the block structure

Needleman–Wunsch the reference's word list against the raw roll's, monotonic, with a
CHEAP gap penalty on the raw side (the roll is full of unused takes) and an expensive one
on the cut side. `reference/wordalign.py`.

- Expect **>99 % of the cut's words to match**. Less than ~95 % means you have the wrong
  raw roll.
- **Normalise apostrophes away on BOTH sides.** Whisper writes `i'm`; a phrase written
  `im` will not match, and the failure looks like "phrase not found", not like a bug.
- Group the matched pairs by their offset `raw_start − cut_start`. Runs of constant
  offset are the editor's takes; the jumps between runs are their take changes.

### 1b. Whole-segment audio matching, with recursive splitting, gives the exact cuts

Word timings are ±50 ms and some splices sit inside a word gap Whisper timed badly. Refine
with `reference/segfit.py`: for each candidate segment, take its whole span of 24-band
log-mel frames and slide it against the raw within ±5 s; if the match score is below ~0.60,
split the segment at its worst-agreeing frame and recurse.

Long windows are what makes this stable. **A per-window (0.4 s) sliding correlation
over-segments badly** — the first attempt produced 199 "segments" with backwards jumps,
because at that length noise in the mel envelope exceeds the offset differences you are
trying to detect.

Expect: mean score ≥ 0.75, and a segment list in the 60–100 range for a 4-minute ad.

### 1c. VERIFY BY CONFORM, NOT BY SCORE

Render a throwaway low-res conform from the recovered EDL and put it side by side with the
reference at a dozen timecodes. **Dan's pose, hand position and mouth shape must match in
every pair.** That is the only check that actually proves the EDL.

⚠ **Do NOT verify with raw pixel correlation.** The reference is graded, punched in and
vignetted, so a correct conform still scores ~0.35 against it. That number means nothing;
the eyeball test means everything.

---

## Step 2 — MEASURE THE LOOK (four separate measurements, never one)

### Framing
Fit `scale` + `(dx,dy)` per sampled frame by searching over a downscaled copy (`reference/geofit.py`).
Editors alternate two or three sizes — a wide at 1.00 and a punch-in around 1.15–1.25,
usually recentred upward. Correlations of 0.85–0.98 mean the fit is real.

### Tone curve — fit on a CENTRE BOX ONLY
Percentile-match raw→reference per channel **inside a small centre box**, where the
vignette is ≈1.0. Fitting over the whole frame smears the vignette into the curve and the
background comes out far too bright. (This happened; the first fit lifted the doorway
behind Dan by 40 levels.)

### Vignette — measured AFTER the tone curve, as a radial gain
Apply the fitted curve to the raw, then take `median(reference_luma / toned_luma)` in
radial bins. A modern editor's vignette is stronger than it looks: ~1.00 at centre, 0.70
at r=0.9, 0.26 at the corners.
**Re-derive it in the OUTPUT frame's coordinates** — do not carry the 16:9 mask over.

### Palette, grid and type
Sample MEDIAN colour inside flat regions of the actual graphics (not a guessed box).
Get the grid pitch from an FFT of a row/column average. Then check `_shared/motionlib.py`
before building anything: the `J2AD` palette already measures identical to what these
editors use (field 13,14,11 · accent 140,152,88), and `field_bg`, `card`, `chip`,
`bullets_build`, `title_plate`, `oblique`, `encode` are all already written.

---

## Step 3 — MEASURE THE STRUCTURE

Classify every half-second of the reference as "talking head" vs "insert/graphic" by
correlating it against the conform at the two or three known framings. Report:

| metric | modern standard | why |
|---|---|---|
| insert/graphic coverage | **58–65 %** | below ~50 % reads as a webcam recording |
| visual changes / min | **≥ 9**, 15 is comfortable | |
| longest stretch with no visual change | **≤ 16 s** | |

Then read one contact sheet of the insert regions and write the beat list by hand. Nothing
automates "what is this insert" — but the classifier tells you exactly where to look, which
turns a 4-minute video into ~16 frames to inspect.

---

## Step 4 — AUDIO, BEFORE ANY OF THE PICTURE WORK

1. **`reference/chan_analyse.py` on BOTH the reference and the raw.** Jeff's rolls are not
   stereo — they carry two different microphones ~7.8 ms apart, sometimes polarity-inverted.
   **Voice comes from the RIGHT channel only, as mono.** A good editor has already fixed
   this in their render (check: L/R correlation ≈ +0.99 at lag 0, zero clipped samples).
2. **Loudness of the reference** — and do not copy it. Editors ship −18 LUFS; ads want
   **−14 LUFS / ≤ −1.5 dBTP**.
3. **Music bed detection: use the SPECTRAL TILT in the speech gaps, not the floor level.**
   A bed shows as 30–120 Hz sitting ~12 dB above the rest of the spectrum in the gaps.
   The "floor above −45 dB ⇒ bed" heuristic false-positives on any hard-limited master.

---

## Step 5 — THE VERTICAL TRANSLATION RULES

These are the decisions that make or break the port. They are not stylistic preferences;
each one was arrived at by getting it wrong first.

1. **Left/right becomes above/below.** The reference puts bullets left and the talking head
   right. A 9:16 frame has no left and right to give. Dan goes in a full-width window at the
   TOP; the text goes underneath on the field.

2. **The window height ADAPTS to the beat's text.** Measure the wrapped text block, then
   size the window to `1920 − text − margins`, clamped to 820–1220 px. One fixed compromise
   size makes short beats look empty and long beats unreadable.

3. **16:9 SOURCE IS NEVER CROPPED TO FULL-BLEED.** Cropping 1280×720 to 9:16 is a **2.7×
   upscale**. Put it in the olive card instead — which is the editor's own design language,
   and is a DOWNSCALE. Full-bleed is only for natively-vertical or ≥1440-tall sources.
   The talking head is the one exception: 1080p → 608×1080 → 1080×1920 is 1.78×, it is
   unavoidable, and `unsharp=5:5:0.85` carries it.

4. **A card's hole matches the MEDIA's aspect ratio, measured from the file.** A fixed 16:9
   hole cover-crops a portrait photo, and what it crops off a photo of a person is their head.

5. **Centre the vertical crop on the subject's HEAD BAND, not their silhouette.** A
   whole-frame difference centroid is dragged sideways by hand gestures — on this shoot by
   114 px, which put Dan a third of the way from the left edge. Restrict the band to the
   head (y ≈ 90–260 of 1080). Locked-off shot ⇒ one fixed crop for the whole video (sd 18 px).

6. **Captions are suppressed wherever a graphic carries its own words.** Bullets, title
   cards, statements and the CTA pill all paraphrase the very sentence being spoken; running
   captions under them puts two text systems in a 1080-wide frame.

7. **Safe area:** nothing that must be read below y≈1660 or above y≈150; captions centred at
   y≈1250. YouTube Shorts takes the bottom ~230 px and the right ~120 px; IG Reels takes ~350.

8. **Render captions with PIL, not libass.** Manrope is a VARIABLE font and libass takes the
   default instance — ASS captions come out Regular while every graphic is ExtraBold. Build
   one PNG per word state and assemble with the concat demuxer (`duration` directives); that
   is fast and keeps one type system.

---

## Step 6 — BUILD ORDER

```
build_base.py   conform the raw to the recovered EDL + tone curve, OUTPUT STAYS 16:9
vlib.py         vertical layout library (plates)
beats.py        beat sheet, phrase-anchored, + timeline() that fills gaps with `talk`
render.py       one output segment per beat -> concat -> overlays
build_audio.py  right-channel voice -> EQ fitted to the REFERENCE mix -> bed -> SFX
finish_audio.py two-pass loudnorm + spectral verification
captions.py     word-timed, suppressed under text graphics
qc.py           the gate
cutdown.py      the <=0:59 selection
```

**Keep the base at the source's 16:9.** All reframing happens downstream, so one base
serves both the full-bleed and the windowed layouts. Rendering two bases doubles the
slowest step for nothing.

### The plate pattern
Every graphic beat renders ONE RGBA plate that is opaque everywhere except a rounded
"media hole"; the media is composited UNDERNEATH at the hole's final size. Animating the
hole (rather than the media) lets a card grow open without ever rescaling the picture in it.

### EQ-fit the voice to the REFERENCE's mix
Ten bands, several windows across both files, speech-active frames only. **Cap the fit at
+6 dB.** The raw fit here wanted +8.8 dB at 9 kHz — partly the reference's own music bed —
and that lifts lav hiss with the air. Gate BEFORE the EQ, always.

---

## Step 7 — QC (`reference/qc.py`) — measured off the FINISHED FILE

1 frame size 1080×1920 · 2 fps 29.97 · 3 duration matches the reference · 4 −14 LUFS ±0.8 ·
5 true peak ≤ −1.0 dBTP · 6 L/R correlation > 0.98 · 7 ≥ 9 visual changes/min ·
8 no stretch > 16 s without a visual change · 9 insert coverage ≥ 55 % ·
10 no banned frames reachable in any product recording · 11 captions present.

---

## Step 8 — THE ≤0:59 CUTDOWN

**Select intervals out of the approved master. Never re-cut from source.** Selection
carries every decision through unchanged; a re-cut re-litigates all of them.

- Content follows Dan's settled shorts-ad doctrine (see `/ad-outlines`): **sell the
  GENERATION almost exclusively**, give the trainer/nutritionist exactly one beat near the
  end, say the CTA twice. Hook, mechanism, proof, CTA.
- **Snap every range edge to the nearest beat boundary** (±0.3 s). A range starting 80 ms
  inside a card shows that card already half-open, which reads as a dropped frame.
- Rebuild the captions (re-timed through the range map), the music bed and the SFX over the
  new duration — those three cannot survive having time removed from under them. Cut the
  picture and the voice; regenerate everything else.
- **Assert `total ≤ 59.0` in code.** Shorts ads must never exceed 0:59.

---

## Standing content rules that override the reference

The reference editor does not know Dan's ad rules. Check every beat you are reproducing:

- **NO side-by-side before/after, ever, in a paid ad.** Muhammad's 0:03 card is exactly
  that (heavier Dan left, goal phone right, arrow between). **Cut it sequentially instead** —
  the before photo, then the goal phone.
- **NEVER show the email-capture screen**, and never the app's "Meet the new you"
  before/after screen. In the product recording `clip_109_replacement.mp4` those start at
  **26 s and 29 s** — the usable window is **0–25 s**. Assert it in QC.
- **Label AI-generated imagery.**
- **Casting: white or Asian men 30–50.** Contact-sheet the RENDERED 9:16 crop of every stock
  clip before committing — 4 of the first 10 picks here were off-demographic and one was a
  woman, and none of that is visible from a search-page thumbnail.
- No drug names in graphics.

---

## Traps that cost time here — read before building

1. **Cumulative frame counts, not per-segment rounding.** Rounding each segment's duration
   on its own put ~16 ms of overshoot into every one of 73 cuts and the conform finished
   **1.17 s long**. Compute `round(cut_out × fps)` cumulatively and take differences.
2. **`-vsync 0` and `-r` are contradictory** and ffmpeg errors out. Use `-r` + `-frames:v N`.
3. **`blend=all_mode=multiply` must run in RGB.** On yuv420p it multiplies the chroma planes
   about their 128 offset as if they were luma and **turns every footage frame bright green**.
   `[a]format=gbrp[x];[b]format=gbrp[y];[x][y]blend=...,format=yuv420p`.
4. **A still used as a filter input needs `-loop 1 -framerate`.** Without it the image is one
   frame and `shortest=1` truncates the whole segment to a single frame — which is exactly
   how 29 footage segments silently became stills.
5. **A filtergraph label can be consumed once.** Feeding the voice to both `sidechaincompress`
   and `amix` needs `asplit=2`.
6. **Phrase anchors need `after=`** whenever a phrase repeats ("tap the button below",
   "stressful life", "lose your belly fat"). Without it the anchor matches the first
   occurrence and the beat gets a negative duration.
7. **Pexels needs no key**: `https://www.pexels.com/download/video/<ID>/` curls straight to the
   CDN. Search pages are Cloudflare-gated, but a page loaded in the in-app browser can
   `fetch('/search/videos/<term>/')` same-origin. Prefer results that come back ≥1440 tall.
8. **Probe every downloaded clip's dimensions.** 8 of 10 came back 2160×4096 — those are a
   downscale to 1080×1920 and look far better than anything cropped from 16:9.
