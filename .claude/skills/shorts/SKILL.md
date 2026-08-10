---
name: shorts
description: >
  Cut vertical Shorts/Reels/TikToks (1080x1920) from an existing long-form Abs By AI
  video — pick segments with Dan, snap the cuts to silence, handle every graphic so
  nothing is sliced or covers him, burn word-timed captions, QC and deliver. Use
  whenever Dan asks to cut Shorts/Reels/TikToks from a video, mine a longform for
  short-form, or to REVISE a short that was already cut — even if he doesn't say
  "/shorts". For packaging a longform for upload (titles, description, thumbnails)
  use /youtube-packaging. For a fully AI-generated video ad use /make-ad.
---

# Cutting Shorts from a long-form video

Built from three passes: V1 channel-intro (2026-08-04, none cut — Dan's call), V4
1-minute ab workout (2026-08-06, 5 shorts), V2 six-ways-AI-abs (2026-08-10, 7 shorts),
and the V4 short1 rebuild (2026-08-10) that produced the band layout.

**Working pipelines are preserved in `reference/`.** Copy one and adapt, do NOT rewrite
from scratch. `reference/full-bleed/` is the V2 pipeline (talking head cropped full-bleed,
graphics as cards). `reference/band/` is the V4 short1 rebuild (dedicated graphics band).
Paths inside them are relative to `YouTube Long Form Video Content/<slug>/` — fix those first.

> **Why the scripts live in the skill folder:** `YouTube Long Form Video Content/` and
> `Short-form video content/` are both git-ignored. The original V4 shorts pipeline lived
> in a session scratchpad and **was lost**, which is why revising V4 short1 meant a full
> rebuild from source. Keep working code here, in git. Media stays out.

---

## Step 0 — what has already been mined

Check before starting. As of 2026-08-10:

| Video | Status |
|---|---|
| V1 channel intro | **Deliberately none** — Dan 2026-08-04, "the intro is promise, not payload" |
| V2 six ways AI abs | 7 shorts, delivered `v2-short1..7_*` |
| V3 My Top 10 Tips | **unmined — biggest remaining yield (up to 10), needs a Whisper pass first** |
| V4 1-minute ab workout | 5 shorts, `short1..5_*`; short1 rebuilt with the band layout |
| V5 | skip — same footage as V4 |
| V6 / V7 3-min home workout | unmined |

## Step 1 — transcript with WORD timestamps

Non-negotiable: captions come only from word timestamps, never estimates. Estimated
caption windows do not survive any change to the cut and drift immediately.

If `<slug>/<v>-words.json` already exists, use it. Otherwise run Whisper via Replicate:
`vaibhavs10/incredibly-fast-whisper` with `timestamp: "word"` (community model → generic
`/v1/predictions` + version id, data-URI audio input). Token in `bakeoff/.env`. Costs cents.

Shape is `{ chunks: [{ text, timestamp: [start, end] }] }`.

## Step 2 — Dan picks the segments

**This is his call, not yours** (standing rule since 2026-08-04). Give him a shortlist
with, for each candidate: a title, the timecodes, and the **verbatim spoken text**. He
picks by letter. On V2 he chose 7 from a shortlist of 11.

A short must **stand alone with its own reason to watch** — a complete idea, tip or story.
"Random clips from the video" was explicitly rejected. Flag anything spicy in the text you
send him (drug references, claims about named people, anything that would trip ad review)
so he chooses with that in mind.

## Step 3 — snap every cut to measured silence

Whisper word timestamps are **contiguous** — there is no gap between words — so any padding
you add clips a syllable off the neighbour. Cut inside real measured silence instead.

```
ffmpeg -i SRC -vn -af "silencedetect=noise=-26dB:d=0.05" -f null -
```

- **Use -26dB / 0.05s.** The obvious -32dB/0.12s found silence for only **7 of 18** cut
  points on V2, because Dan barely pauses.
- **Bound the snap to the neighbouring word.** Without a bound, a sub-threshold gap between
  two sentences sends the search back past a whole phrase — on V2 this dragged
  "…they get started" into the front of a short.
- **Assert every cut lands inside a silence interval** before rendering. `segments.js` does.

## Step 4 — shot-detect and classify EVERY shot

A produced longform is not one continuous take. V2 had **56 distinct shots** across 7
segments. Detect them, pull one frame each, build a contact sheet **with the 9:16 crop
window drawn on**, and classify every one:

| Treatment | When | What |
|---|---|---|
| **talk** | subject on a locked camera | full-bleed 9:16 crop at one offset that covers every talking-head shot in the video |
| **broll** | stock footage, **no text** | full-bleed crop at a per-shot offset |
| **card** | anything with text, numbers, UI or a designed graphic | the **whole 16:9 frame** scaled into the vertical frame on the J2 background, with an olive mission chip beneath |
| **pip** | subject + a corner graphic that falls outside the crop | crop to the subject, re-composite the graphic inside the vertical frame |

**Never crop through a graphic.** Cropping plain footage looks like a vertical video;
cropping through text looks broken. If meaning depends on seeing the whole frame — a
lower third, a phone UI, a readout, or a **horizontal pose like a plank** — it is a card.

## Step 5 — crop offsets: automate, then LOOK

Auto-picking offsets by image energy / centroid / silhouette is a starting point and
**it is wrong often enough that you must review it**. On V2, 9 of 23 b-roll offsets had
locked onto background detail — a window, an empty hotel chair, trees — instead of the
subject. On the V4 rebuild all three automated methods failed and hand-set values were used.

Always render a contact sheet of the **actual proposed vertical frames** and fix by eye.
`choose-crops.py` does this.

## Step 6 — does the subject leave room for graphics? MEASURE IT

**This is the decision that produced the band layout, and it is the one Dan cared about.**

Before placing any overlay, sample frames across the segment and measure how often each
candidate region is clear of the subject. On V4 short1 the best of eight candidate slots
was clear **33% of the time and 0% in its worst frame**. There was nowhere to put anything.

- If regions are reliably clear → full-bleed footage, overlays in the clear region.
  Use `reference/full-bleed/`.
- If nothing is reliably clear → **make space, don't hunt for it.** Use `reference/band/`:
  footage in the lower ~74%, a graphics-only band across the top ~430px.

Two things that make the band the better default when the subject fills the frame:

1. **It is sharper.** A full-bleed 9:16 crop of 1080p upscales 1.78×; a band block
   upscales ~1.32×.
2. **The bottom is the worst real estate in a vertical video** — YouTube Shorts, TikTok
   and Reels all overlay their own UI on the bottom ~15% and the right edge. If Dan asks
   to "move the graphics to the bottom", this is the reason to push back.

## Step 7 — overlay rules

- **A title must not sit on screen for the whole video.** V4 short1 shipped with the title
  up for all 61 seconds and chips accumulating into a permanent stack over Dan's face —
  that was the complaint that triggered the rebuild. Either fade it (~3.2s) or move it
  into a band, where it costs nothing and can persist small.
- **One chip at a time, not an accumulating stack.** Add a "MUSCLE n OF 4" style counter —
  it paces with the voice and opens a small loop that holds people to the end.
- **Sync chips to the audio, but not slavishly.** When two items are named ~1s apart,
  a strict one-word-one-chip sync leaves one on screen for ~1s and unreadable. Give the
  first the whole naming phrase and switch on the *end* of the second's name.
- **Check title clearance numerically.** At Impact 106/102 line-height, a 3-line headline's
  ink ends ~y455. Dan's eyes on the kitchen camera are ~y560, and a card's top edge is
  y420. Assert it in the asset build — `build-assets.py` fails the build if a card-opening
  short gets a title too tall.
- **Fitcards top-aligned, never centred.** A 1000×562 card centred in a 1425-tall block
  spans y861–1424 and the caption band starts ~y1150 — centring draws captions across
  the artwork.

## Step 8 — captions

Canonical spec, unchanged since V1. Arial **86** bold white, outline 7, shadow 3,
Alignment 2, **MarginV 690**, PlayRes 1080×1920. Group into 2–4 word chunks, break on
punctuation or a >0.6s gap. Uppercase `ABS` and `AI`.

- **Remap timestamps to OUTPUT time** when a short is stitched from non-contiguous pieces.
- **A word counts as spoken only if >50% of it is inside the cut**, or boundary fragments
  get captions for audio nobody hears.
- **Close spaced punctuation.** Whisper tokenises "p.m." as `["p", ".m."]`, which joins to
  "11 p .m.". Regex `\s+([.,!?%])` → `$1`.

## Step 9 — render architecture

Per-shot clip → concat → one finishing pass (overlays + captions). Reasons this shape:
each shot needs its own filtergraph, and doing overlays once at the end is far faster than
per shot.

**Audio: pull it ONCE for the whole segment. Do not cut audio per shot.** Shot boundaries
are picture cuts inside continuous audio; slicing per shot splices it back together across
N independent input seeks, measured at **23–34ms of per-shot offset** on the V4 rebuild —
a small content jump at every cut. Render shots `-an`, then map audio from a single
`-ss START -i SRC` in the finishing pass. Verified result: 0ms drift, 0.999+ correlation.

## Step 10 — QC, automated

`qc.js`. Assert: 1080×1920, **24fps**, AAC 48kHz stereo, duration within 0.25s of plan,
no black frames, last caption inside the video, and no click at any splice.

**The splice test is easy to get wrong — it took three attempts.** Comparing loudness
either side of a join always looks like a huge step, because the cut is deliberately in
silence and speech follows. Peak-across-the-join fails the same way. The correct measure is
**discontinuity**: max sample-to-sample jump at the join vs. the same measure at four
control points in the same file. Healthy joins score **~0.1×** control.

Then look at a contact sheet of every card/pip moment from the **finished file**. That is
the check against the actual requirement.

---

## ffmpeg traps — all of these cost real time

1. **`execFileSync` returns stdout only, and ffmpeg logs `showinfo`/`silencedetect` to
   STDERR.** Scene detection silently reported "0 cuts" for every segment. Use `spawnSync`
   and **assert the log is non-empty**.
2. **`-loop 1` stills are INFINITE streams.** A finishing pass with no `-t` encodes forever
   — 10+ minutes on a 21s clip before it was killed. Needs `-t` **and** `shortest=1` on
   every overlay that mixes a still with real video.
3. **`-loop 1` stills default to 25fps, and `overlay` adopts its FIRST input's rate.** Card
   and pip shots came out 25fps, and `concat -c copy` then stamped the whole short 25fps
   whenever it opened on one. Pin `-framerate 24` on every still input and `-r 24` on every
   encode.
4. **ffmpeg eats stdin inside `while read` loops** — pass `-nostdin` or the loop consumes
   one line per iteration and silently skips frames.
5. **PiP repositioning renders the graphic TWICE** unless the subject's crop starts to the
   *right* of the PiP box. Measure the box, assert `x0 >= box.right`.
6. **Regenerate derived files after editing the plan.** Hand-editing crop offsets in
   `plan.js` without re-running `choose-crops.py` left a stale `crops.json`, and the preview
   showed a hotel room with no housekeeper in it.
7. Source is 1920×1080 → a 9:16 window is 607.5px. Use **608** (even); the 0.09% aspect
   error is invisible.

## Locked design system (do not redesign)

From `shorts-production-style` memory, settled 2026-08-06 after ~4 rounds of mockups.

- One **1080×1920, 24fps** master per clip, **uploaded natively** to each platform — never
  cross-post watermarked downloads.
- **J2 tactical frame** — near-black `#0D0E0B`, faint 90px grid, olive `#8C9858` perimeter
  with rangefinder ticks + white corner brackets. **Only for horizontal footage forced into
  vertical.** Native-vertical-croppable footage gets **no frame**, just large overlaid title
  text with a drop shadow. **No blur-pad fill — Dan rejected it. No static intro title cards.**
- **Type:** headlines Impact all-caps white; eyebrows/labels Copperplate letter-spaced olive;
  chips are square-cornered olive-bordered rects with mission framing ("TARGET: LOWER ABS").
- **`AbsByAI.com`** camel case, small and muted, on **every** short from video #1 — rip
  protection. Never all-caps.
- **Titles must sell the click to someone who never saw the source video** — benefit-first,
  split as eyebrow + big headline.
- Long eyebrows wrap to two lines rather than shrink below ~50px.
- **Post one every 2–3 days after the longform**, not all at once.

## Delivery

- Work folder: `YouTube Long Form Video Content/<video-slug>/`
- Output: `Short-form video content/`, prefixed by source video (`v2-short1_…`) so batches
  from different longforms don't collide.
- Write a `SHORTS.md` in the work folder: posting order, per-short title, description with
  `utm_source=youtube&utm_medium=short&utm_campaign=<slug>&utm_content=<id>`, per-short
  editorial notes, and how the graphics were handled.
- Both media folders are git-ignored — verify with `git check-ignore` before staging anything.
- Check the dashboard for a matching task and check it off (AI_COORDINATION Rule 9).

## Judgement calls Dan has endorsed

- Skipping a drug reference that sat in a hook position, rebuilt as setup → hard cut →
  payoff (V2 gum short).
- Flagging but not removing a spicy true claim ("of course they're using steroids") so he
  can decide whether it runs anywhere paid.
- Shortening an on-screen title to clear a card rather than moving the card into the
  caption band.
- Treating a horizontal pose as a card rather than cropping it.
