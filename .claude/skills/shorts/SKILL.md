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

Check before starting. As of 2026-08-10 **every long-form video has been mined; there is
nothing left to cut** unless a new video is shot.

| Video | Status |
|---|---|
| V1 channel intro | **Deliberately none** — Dan 2026-08-04, "the intro is promise, not payload" |
| V2 six ways AI abs | 7 shorts, delivered `v2-short1..7_*` |
| V3 My Top 10 Tips | **11 shorts, `v3-short1..11_*`** (2026-08-10) |
| V4 1-minute ab workout | 5 shorts, `short1..5_*`; short1 rebuilt with the band layout |
| V5 | skip — workout-only cut of V4, no narration |
| V6 3-min home workout | **5 shorts, `v6-short1..5_*`** (2026-08-10) |
| V7 | skip — workout-only cut of V6, no narration |

**V5 and V7 are music/rep-count only.** Their Whisper transcripts come back as pages of
`"Hey. Hey. Hey."` — that is not a transcription failure, there is no speech. They cannot
yield a talking Short, but they do hold clean uninterrupted exercise demos usable as b-roll.

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

**The reason to watch must be something the VIEWER walks away with, not something Dan
achieved.** Before a candidate goes on the shortlist, answer "what does the viewer get?"
If the honest answer is "that Dan is in shape," cut it from the shortlist — his own result
is the proof behind the product, never the payload of a Short. This is a hard rule as of
2026-08-17: `v6-short1_gained-muscle-in-quarantine` ("I GOT LEANER WITH NO GYM") was cut,
captioned and scheduled as the first Instagram/Facebook post before Dan killed it —
*"It's just more me bragging."* **Note it had been annotated "best standalone hook" in the
V6 notes, so a strong hook is not evidence a Short passes this test.** Replaced with
`v3-short6_vacuum-exercises` ("DO THIS INSTEAD OF CRUNCHES"), which hands the viewer an
exercise. The failure mode is a clip that is compelling *about* Dan rather than *useful* to
the viewer — those read worse on Instagram/Facebook than on YouTube, where the audience
arrived already interested in him.

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
- **Assert every cut lands inside a silence interval** before rendering, and run the
  assertion in a REPORT mode that lists every failure at once. Fixing them one-per-run is
  slow: V3+V6 had seven.

**Whisper inflates short words across real pauses, and its timestamps then deny the pause
exists.** V6 times `"the"` at 148.28–149.00 while the audio is measurably silent
148.44–148.63. This is the single biggest source of failed cut points. **Measured silence is
ground truth; the word timestamp is not.** Give `piece()` `inAt`/`outAt` overrides for these
— the silence assertion still applies to an override, so it cannot smuggle in a bad cut.

**Do NOT fix it by widening the snap lookahead.** Tried on V3+V6 and it is strictly worse:
it starts the clip 0.3–0.5s late and clips the FIRST word instead ("This" 48%, "use" 47%).
Keep the snap tight and move the editorial in/out point.

**Some sentences have no cut point at all.** `"deadlifts."` runs into `"All right"` with a
*zero-length* gap; `"excuses."` into `"If"`. When that happens, end the short on an earlier
complete thought rather than forcing a cut through speech. Three of the 16 V3/V6 shorts
ended earlier than first planned for exactly this reason, and all three are better for it.

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

**A third-party clip with an on-screen credit is a card, always.** V3 uses footage carrying
`@FraserWilsonFit` and `@ChrisBumstead` in the bottom-right; a 9:16 crop deletes the
attribution. Preserving it is both the safer and the honest call.

**Crop a card to its real content if the frame is mostly flat fill.** V3's bubble-gut photo
is 70% white surround and a designed graphic was 65% black, so scaling the whole frame put a
postage stamp inside a big empty card. Measure the non-flat bounding box, crop to it, and
scale with `force_original_aspect_ratio=decrease` so a cropped card is never stretched.

**Do not judge a shot from one frame.** The contact sheet samples the shot MIDPOINT, which
missed a burned-in lower-third on two long V3 takes where the bar is only up for the first
4–5s. Scan candidate shots end-to-end. Expect false positives too — the same scan flagged
six bright-but-clean b-roll shots (white rocks, glassware, lab coats) that had to be
rejected by eye.

### `zoom` — the variant for a burned-in bottom lower-third

V3 burns a chapter lower-third across the bottom of each tip's opening shot. It occupies
source rows **888–978** (measured on five separate tips, identical every time), so a
full-height 9:16 window slices it mid-sentence, half-visible under our own captions.

`zoom: true` crops **496x880 from the TOP** instead of the full height, dropping the band
entirely for ~18% of the headroom. Measure the band before picking the number — an
initial 940 (87%) still included it and looked fine on the sheet until asserted.

Zoom the WHOLE shot, even a 43s one. A mid-shot pull-out reads as a mistake; the viewer
never sees the wider framing, so a consistently tighter shot costs nothing.

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
- **That regex is not enough on its own — a chunk boundary can fall between the two tokens.**
  A V3 short opened on a caption reading just `.m.`, because "2 p" ended one chunk and ".m."
  began the next, so the within-chunk regex never saw them together. **Merge any token that
  begins with punctuation into the previous token BEFORE chunking.** The same fix cleaned up
  "90%" and "sixpackabs.com".

## Step 8b — bleeping a word

Dan may ask for a word to be censored (V3 short 11, "steroids", his call). Two halves, both
required:

- **Audio.** Mute the span and mix in a 1 kHz tone. **ffmpeg's `sine` source emits at
  amplitude 0.125 (−18 dBFS), not full scale** — a naive `volume=0.20` produced a bleep 11x
  quieter than the dialogue. `volume=2.0` puts it just above speech.
- **Captions.** Replace the word with `[BLEEP]`. Bleeping the audio while printing the word
  in 86pt letters defeats the entire point.

Keep the windows in SOURCE time in a `bleeps.js` and shift them into piece-local time at
render, so re-cutting a segment cannot silently move a bleep off its word. Pad the Whisper
span by ~50ms — under-covering the target is the worse failure.

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
control points in the same file. Healthy joins score **~0.1×** control (V3/V6 measured
0.03–0.70×).

**Assert the bleeps too**, in the finished file: a ~1 kHz tone at the right output times,
and the word absent from the `.ass`. Use a Goertzel at 1 kHz — but **normalise it correctly**:
a Hann window has coherent gain 0.5, so a pure sine scores 0.707 on a naive `magnitude/rms`
and a verified-pure tone gets flagged as impure. Against `rms*sqrt(1/2)` a pure tone reads
1.00 and speech 0.01. The first version of this check failed a bleep that was already
perfect — when a QC metric fails, confirm the metric before "fixing" the media.

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

## Long renders: never poll for a filename, always signal DONE

A backgrounded render watcher once ran **20 hours after its render had finished** because it
polled for a filename the render never wrote (2026-08-22) — Dan saw a blinking dot and left a
finished video unreviewed for a day. Wait on the **process** (`wait $PID`), never on
`[ -f "$OUT" ]`; give every wait a hard timeout; make it print why it exited; and end the
session with the file path, size and *ready to review*. Helper that does all of this:
`.claude/skills/longform-edit/reference/render_wait.sh`. Full rule: the Delivery section of
`/longform-edit`.
