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
`reference/scored-source/` is the ab-wheel batch (somebody else's finished, scored 16:9 cut).
**`reference/clean-master/` is the supplements batch — our own long-form, cut from its
`CUT_*_NO-GRAPHICS.mp4`. Start there for any of the remaining 8/3-shoot long-forms.**
Paths inside them are relative to `YouTube Long Form Video Content/<slug>/` — fix those first.

> **Why the scripts live in the skill folder:** `YouTube Long Form Video Content/` and
> `Short-form video content/` are both git-ignored. The original V4 shorts pipeline lived
> in a session scratchpad and **was lost**, which is why revising V4 short1 meant a full
> rebuild from source. Keep working code here, in git. Media stays out.

---

## Step 0 — what has already been mined

Check this first, and **re-derive it from the filesystem rather than trusting the table** — it went
stale once already. This version audited 2026-08-28.

⚠ **A previous version of this table said "every long-form video has been mined; there is nothing
left to cut." That was true on 2026-08-10 and wrong by 2026-08-20**, because five long-forms were
finished after it was written and nobody updated it. The audit that catches this is two commands:
list the long-form masters, list `Short-form video content/*.mp4`, and diff the prefixes.

**Mined:**

| Video | Status |
|---|---|
| V1 channel intro | **Deliberately none** — Dan 2026-08-04, "the intro is promise, not payload" |
| V2 six ways AI abs | 7 shorts, `v2-short1..7_*` |
| V3 My Top 10 Tips | **11 shorts, `v3-short1..11_*`** (2026-08-10) |
| V4 1-minute ab workout | 5 shorts, `short1..5_*`; short1 rebuilt with the band layout |
| V5 | skip — workout-only cut of V4, no narration |
| V6 3-min home workout | **5 shorts, `v6-short1..5_*`** (2026-08-10) |
| V7 | skip — workout-only cut of V6, no narration |
| Ab-wheel organic (Muhammad's 6:58 cut) | **5 shorts, `abwheel-short1..5_*`, FINAL 2026-08-28.** A sixth was cut by Dan |
| Ab wheel ($17, Muhammad's cut) | 5 shorts, `abwheel-short1..5_*`, rev 3 (2026-08-28) |

**NOT mined — the 8/3 shoot, all five in `claude edited long form content/`:**

| Video | Runtime | Note |
|---|---|---|
| ~~02 My Honest Zepbound Update~~ | ~~30:28~~ | **MINED 2026-09-01 — 8 shorts, `zep-short1..8_*`**, work folder `YouTube Long Form Video Content/zepbound-honest-update/` (6 alternates shortlisted in its SHORTS.md) |
| ~~03 The Supplements I Actually Take~~ | ~~23:29~~ | **MINED 2026-08-28 — 8 shorts, `supp-short1..8_*`** |
| ~~01 My First Spray Tan~~ | ~~19:54~~ | **MINED 2026-09-02 — 8 shorts, `tan-short1..8_*`**, work folder `YouTube Long Form Video Content/spray-tan-first/` (6 alternates in its SHORTS.md) |
| 04 Why You Should Invest More In Your Health | 53:17 | longest; still on the old v3 master |
| 05 Meal Prep Macro Tracking (app demo) | 4:49 | too short and too UI-heavy to mine like the others, but it is the app-demo asset the IG growth plan called the only thing no competitor can copy |

**V5 and V7 are music/rep-count only.** Their Whisper transcripts come back as pages of
`"Hey. Hey. Hey."` — that is not a transcription failure, there is no speech. They cannot
yield a talking Short, but they do hold clean uninterrupted exercise demos usable as b-roll.

### ⚠ On a rebuilt long-form, cut from the NO-GRAPHICS master

The 8/27 style pass took 01/02/03 to **43–48 % insert coverage**. Cutting shorts from a delivered
master at that coverage makes nearly half of every short a full-frame graphic that Step 4 forces
into a `card` — shorts that are mostly not-Dan. Each of those folders keeps a
`CUT_v*_graded_NO-GRAPHICS.mp4` alongside: same picture edit, graded, no graphics and no stock
inserts. On 03 the two measure **within 0.03 s**, so the SRT and every timecode transfer directly.
**Prove the alignment with matched frame grabs before relying on it**, and never use a
`*_PRE_AUDIOFIX.mp4` — that is the comb-filtered two-mic voice.

## ⚠ Step 0.9 — TWO DEFECTS THAT SHIPPED PAST EVERY GATE (2026-08-28)

Both were found on the supplements batch by **reading the finished captions and transcribing
the finished file** — not by any metric. Both affect earlier batches too.

### The source may have TWO TIMELINES, and the captions will be late

A master assembled by concatenation can hold more audio samples than its container declares,
spread through the file. The supplements master (62 ranges) held **0.76 s more**. Whisper word
timestamps and every silence measurement live on the DECODED-SAMPLE timeline; `-ss` — and so
every cut and the whole picture — lives on the CONTAINER timeline. They agree at t=0 and drift
about **0.5 ms per second**, reaching 669 ms.

That build shipped **captions 280–650 ms late** and **clipped the first word off two shorts**,
while passing QC 12/12, the splice test, loudness, duration and the centring audit.

**Preflight, every time** (`reference/clean-master/work/preflight.py`): compare decoded sample
count against container duration. More than ~50 ms apart and the timelines disagree. Fix:

```
ffmpeg -i SRC -vn -af "aresample=async=1:first_pts=0" -ac 1 -ar 48000 -c:a pcm_s16le out.wav
```

**Then gate it on the delivered file.** `reference/clean-master/syncgate.py` transcribes each
finished short and matches every caption's first word to the heard audio; `qc.js` refuses to
pass a file the gate has not seen. ⚠ It carries a measured **−80 ms** correction because the
gate's `base.en` and the pipeline's `medium.en` disagree on word onsets by exactly that much
(n=414, identical across three spans). Without it the gate fails good builds — the fourth time
in this pipeline's history that a QC metric was wrong rather than the media.

### Zero-duration Whisper words were silently dropped from captions

`segWords`' `>50 % overlap` test computes `0/1e-6 = 0` for a word Whisper times with
`start == end`. **Nine such words on one roll; it ate a word in five of eight shorts** —
"creatine is not an **option** for me" burned in as "not an for me". A zero-duration word is
inside the piece if its START is; give it a nominal 120 ms.

Three smaller caption faults fixed alongside, all in `reference/clean-master/captions.js`:
mis-hearing corrections must run **per word before chunking** (a two-word fix straddled a
four-word chunk boundary and the line-level regex never saw it); hyphen-initial tokens need the
same merge as punctuation ("sub" + "-step" printed as "sub -step"); and the first word of each
piece needs capitalising, since a piece can start mid-sentence.

## ⚠ Step 0.8 — CHECK THE SOURCE'S AUDIO CHANNELS YOURSELF

**Jeff's rolls are not stereo: they carry two microphones, and the left one is a room mic
~7.5 ms late.** Summing them combs the voice, and no gate in this pipeline measures it.

⚠ **A HANDOFF SAYING THE AUDIO IS ALREADY FIXED IS NOT EVIDENCE.** On the supplements batch the
handoff stated the clean master carried "the fixed single-mic chain"; measured, it had L/R
correlation **+0.069 at a −7.58 ms lag** — the same signature as the raw camera roll and as the
file explicitly named `*_PRE_AUDIOFIX`. Only the DELIVERED master had ever been repaired. Two
full revisions shipped comb-filtered audio and Dan caught it, not the gates.

Run **`.claude/skills/_shared/audio/pick_lav.py SOURCE`** before anything else (`chancheck.py` is a shim
to it). It measures which stream/channel is the lav — on this shoot the right channel (SNR 29.8 dB
against 26.6 for the summed pair and 19.9 for the repaired master, whose treble shelf lifted the lav
hiss); on the 8/28 rolls it is stream `a:1` of four — and writes `SOURCE.audio_source.json`, which
`render.js` reads for its pull. **Nothing in `render.js` says `c0=c1` any more.**

**Then the voice is matched to Muhammad's ad by `finishaudio.py`, which runs
`_shared/audio/voice_chain.py` on every rendered short** (dereverb if the room measures wet, EQ fitted
per file on the gate's own metric, expander, measured gain + limiter) and then `audio_gate.py`, which
STAMPS it. Measured on this shoot our lav was 3.8 dB short of weight, 3.8 dB short of presence, **8.7 dB
short of air and 12 dB short above 9 kHz** — dull; the fit closes that. `work/voicechain.py` is a shim.

⚠ **The chain folds to mono, so nothing appended may `pan` again.** A second `pan=mono|c0=c1`
asks for a channel that no longer exists and ffmpeg renders **silence**, not an error — it
blanked the first 4.48 s of a delivered short. `qc.js` scans the master for silent seconds, the gate's
silence row does too, and `voice_chain.py` REFUSES silent input outright (`selftest.sh` case 5).

## ⚠ Step 0.7 — FOUR THINGS THE ZEPBOUND BATCH PAID FOR (2026-09-01)

Full write-up: `YouTube Long Form Video Content/zepbound-honest-update/README.md`.

**1. The two-timeline trap has a second cause, and `async=1` alone does not fix it.** The Zepbound
master's AAC holds 622 ms more samples than its container, as ~13 ms **pts overlaps at every one of
its 48 joins**. `aresample=async=1` soft-corrects at a rate that cannot keep up (residual drift
+20 → +84 ms); `async=1000` pads 20 s of silence into the file; per-segment `-ss/-t` cuts come out
13 ms LONG each because a pull that spans a join delivers both takes' overlapping samples. What
works: **`aresample=async=1:min_hard_comp=0.005:first_pts=0`** (the default hard-comp threshold is
0.1 s, so a 13 ms overlap is never hard-trimmed) — wav +0.6 ms, lag ±4 ms at eight points. **Put
the same filter at the head of the renderer's audio pull** (`render.js` `TIMELINE_FIX`) or a piece
spanning a join carries the overlap into the delivered audio. Always verify the wav against `-ss`
by cross-correlation at 6–8 points; `preflight.py`'s length check alone passed the bad wav.

**2. Verify the ANCHOR on drawn frames before trusting any centring number.** The torso-block
anchor is bimodal when the subject is framed cut at the waist with arms hanging into the 60 %
coverage band — the same shot read 0.50 and 0.58 on alternate frames while his silhouette edges
did not move. On that framing use the **head median per shot**; on the supplements framing
(behind a counter) the torso block was right. `work/measure_shots.py` measures per SHOT over the
shot's own span — a per-BEAT median was 130 px off on a 41 s shot inside a 45 s beat.

**3. Scan every piece boundary against `splices.json`.** A long-form that cut its pauses tight
puts the join IN the pause, and `snapOut`'s 0.34 s tail then walks 0.04–0.30 s into the next take
— 11 of 20 boundaries on this batch, a 1–9 frame flash of a different take before every cut.
`outAt`/`inAt` 20 ms inside the splice; the silence assertion still applies.

**4. Measure the floor before you clean it.** The afftdn + gate chain the supplements batch needed
was measured against Muhammad's AD on this roll: the plain right channel was already 3 dB cleaner
in every band, and the gate only cost word tails (98.7 % → 100 % without) and pumping (14.2 →
7.8 dB). Fit the tone EQ; add cleanup only when the floor comparison says so.


## ⚠ Step 0.75 — FOUR MORE FROM THE SPRAY-TAN BATCH (2026-09-02)

Full write-up: `reference/spray-tan/README.md`. Tools: `reference/spray-tan/`.

**1. THE LENGTH CHECK PASSES A BAD WAV. Always cross-correlate.** `preflight.py` compares decoded
samples against container duration; on this roll **both** candidate extractions passed it
(−3.8 ms and +0.9 ms) and one of them drifts **+16 to +94 ms against `-ss`, wandering with the
joins**. The only test that separates them is a normalised cross-correlation of the analysis wav
against `-ss` pulls at 6–8 points across the file. Do it every batch; it costs seconds.
`aresample=async=1:min_hard_comp=0.005:first_pts=0` is now the default recipe, not the fallback.

**2. A RECONNAISSANCE SAMPLE CANNOT CLEAR THE ANCHOR — the failure is per-shot by nature.** A
12-frame sweep of this video said head and torso agreed to 13 px, which would have justified
either. Measuring all 22 shots found one where they diverge by **121 px** (cross-shot spread:
head 114 px, torso 230 px). **Measure both anchors on every shot, compare, and use head unless
drawn frames say otherwise** (`reference/spray-tan/measure_shots.py` records both).

**3. `work/boundscan.py` is now a required step, and it also checks the IN side.** Three of
thirteen boundaries walked past a splice here. The entry side matters too: a short whose first
word follows a source cut must be pinned 20 ms **after** the splice, or it opens on a frame of the
previous take.

**4. A GATE THAT COMPARES TWO WHISPER MODELS MUST COMPARE THEM FUZZILY.** `syncgate.py` failed a
provably-correct short twice: it transcribes with `base.en` while captions come from `medium.en`,
and the two both tokenise *and spell* differently — caption "All right," → `allright`, heard
`alright`. Neither prefixes the other, so word identity cannot pass it, and the same gate read
"When" as "and" on another short. It now falls back to a **similarity ratio on the opening ~12
letters** (0.80 threshold). ⚠ It also read `build/<ID>.ass` where the renderer writes
`build/<ID>/<ID>.ass` — it had only ever run in a folder carrying stale top-level copies.
**Fix the gate, never override it**; the corrected file is in `reference/spray-tan/syncgate.py`
and has been copied over the `clean-master` and `zepbound` versions.

## ⚠ Step 0.6 — MEASURE THE ROOM. This is the one Dan keeps rejecting.

**Dan has rejected the audio on four deliverables from the 8/3 shoot in the same words** — "the
audio is no good", "it sounds echoey", "make it sound like Muhammad's". Every session fixed
something genuinely broken and shipped anyway, because **nothing in this pipeline measured the
room**, and reverb is the thing a listener hears first.

Measured 2026-09-02, our shipped spray-tan short against `Muhammad Ad Videos/…16x9.mp4`:

| | early decay time (ms to fall 20 dB after a speech offset) |
|---|---|
| his reference ad | **40 ms** (37 ms high-passed at 250 Hz — a genuinely dry voice) |
| our shipped short | **85 ms** |

Everything else already matched: right-channel-only (**+0.9912** correlation, verified), floor
36.0 vs his 36.2 dB, octave shape 0.74 dB, −14 LUFS, no clipping. **All of that can be right and
the audio still be wrong.**

**The room is row 2 of `_shared/audio/audio_gate.py`, which `finishaudio.py` runs on every delivered
file and which `qc.js` and `deliver.js` REQUIRE a PASS stamp from** (⚠ the earlier claim here that
`audiogate.py` was "wired into qc.js" was false — nothing referenced it; corrected 2026-09-02). It fails
over 80 ms — the approved/rejected boundary (website rev 2 approved at 75, this batch rejected at 85). The fix is automatic: `voice_chain.py` runs `_shared/audio/dereverb.py` — spectral
subtraction of the late field (`alpha=0.62 d1_ms=20 d2_ms=150 floor_db=-24 smooth=0.30`) — whenever the
raw lav measures > 55 ms, and re-fits the EQ after it. ffmpeg cannot do this: there is no dereverb filter,
`arnndn` has no model here, and a broadband expander only reached 63 ms and pumped.

⚠ **`floor_db` is the lever, and it is counter-intuitive.** Raising `alpha` past 0.62 makes EDT
*worse* — the tail starts riding the floor instead of decaying. Dropping the floor from −14 to
−24 dB is what took EDT from 50 ms to 40.

⚠ **Re-fit the octave EQ AFTER dereverb** (`work/dereverb_eq.txt`); removing the tail changes the
shape.

### ⚠ Do NOT accept a stated cause without measuring it

Dan attributed this to the two-mic fault ("you use both channels, we only want the right channel
in mono"). **It was not that** — the delivered file correlated **+0.9912** with the source's right
channel through the identical EQ, against 0.60 for left and 0.69 for the sum. Reproduce that
table before touching the channel logic; re-applying a fix that is already applied burns a session
and ships the same rejection again.

### ⚠ A stereo WAV read as mono is invisible to a byte-size check

The first dereverb build read `audio.wav` with Python's `wave` module ignoring `nchannels`. On a
dual-mono stereo file that treats L,R,L,R as consecutive samples — a zero-order hold, i.e. a
brutal lowpass. The finished shorts came back **11–16 dB down above 450 Hz**, and the guard
(`Math.abs(size0 - size1) > 4096`) passed, because **a mono file with twice the frames is exactly
the same number of bytes.** De-interleave on read, and assert **duration and channel count** via
ffprobe, never file size.

### The general rule this batch bought

When Dan rejects something on a quality your metrics cannot see, another pass at the metrics that
already pass is the wrong move. **Find the number that separates his reference from ours, then
make that number a gate.** The gate list here grew for months — channels, floor, tone, loudness,
peaks, silence, caption sync — and never once asked how big the room sounded.

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

### If we rendered the source ourselves, take the shots from its EDL

`edl.json` lists every splice, which beats scene detection outright. But the cumulative
positions are NOT usable raw: `render.py` rounds each range to whole frames and the error
accumulates monotonically (+1.137 s over 62 ranges on the supplements master — exactly the
amount by which the EDL undershoots the master's duration). MEASURE each boundary as a
full-frame-rate frame-difference peak inside a window around its prediction, and assert the
correction is monotonic. See `reference/clean-master/work/splices.py`.

## ⚠ Step 4.5 — SCAN FOR JUNK, PAUSES AND INHERITED JUMP CUTS

Run `reference/clean-master/work/junkscan.py` on every batch before delivering. It reports, per
short, every measured pause over 0.55s, every picture cut inherited from the source edit, and
how late speech starts. On the supplements batch Dan named six timecodes and the scan found all
six plus nine more — it is what turns "check everything" into a list.

⚠ **A PAUSE CANNOT SIMPLY BE REMOVED, and this is the counter-intuitive part.** Cutting one
joins two moments in time, and Dan moves while he is not talking. Measured as mean-abs-
difference across the join (`work/pausejump.py`), against a 1.30 adjacent-frame baseline: an
inherited source splice — what Dan calls an "awkward cut" — scores **7.64**, and **removing a
pause scores 4.97-12.46**, i.e. as bad or worse. So every join has to be HIDDEN, by alternating
a wide and a tight framing across it (see Step 6). And do not remove every pause the scan
finds: 0.55-0.65s is breathing rhythm, and cutting those adds joins for no gain.

⚠ **WHISPER HIDES A HESITATION INSIDE A WORD, so the scan cannot see it until the word
timestamps are corrected.** Dan's "junk footage in the beginning at 0:01" was a 0.95s stumble
that Whisper had swallowed into the word "you're". Run
`reference/clean-master/work/fixonsets.py` immediately after building the gap table: it moves
an onset out of measured silence, an offset out of measured silence, and — the one that
mattered — **a word that wholly contains a gap of >=0.25s begins at that gap's end**. On one
roll that corrected 363 onsets, 328 offsets and 51 swallowed pauses, and it also stops a word
straddling a piece boundary from being spoken but never captioned.

## Step 5 — crop offsets: automate, then LOOK

Auto-picking offsets by image energy / centroid / silhouette is a starting point and
**it is wrong often enough that you must review it**. On V2, 9 of 23 b-roll offsets had
locked onto background detail — a window, an empty hotel chair, trees — instead of the
subject. On the V4 rebuild all three automated methods failed and hand-set values were used.

Always render a contact sheet of the **actual proposed vertical frames** and fix by eye.
`choose-crops.py` does this.

### ⚠ ONE `TALK_X` FOR A WHOLE VIDEO IS WRONG. It shipped 10 off-centre Shorts.

**Dan caught this live on 2026-08-27**, on `v2-short3_supplements-3-percent` the day it
posted to Instagram: *"off-center… one of my arms is cut off and there's space on the other
side."* V2 and V3 both set `const TALK_X = 0.478` with the comment "one value covers every
talking-head shot in the video". It does not. **He shifts in the doorway between takes** —
his measured torso centre wanders **0.411 → 0.505** across V2+V3, and a 9:16 window is only
0.317 of the frame wide, so a 0.06 error moves him ~200 px in a 1080-wide delivered frame.
V6's plan had already found this the hard way ("there is NO single TALK_X") and the lesson
was never carried back to V2/V3. **Measure a centre per SHOT. Never reuse one constant.**

**The measurement that works, and the two that do not.** Anchor on the **torso block** —
the columns where the mask fills ≥60 % of its own tallest column:

- ❌ *Mask centroid* and ❌ *head centroid* both move 100–500 px between adjacent frames,
  because his hands fly in and out of frame while he talks. Same median, useless per frame.
- ❌ *Edge-energy column search* (`choose-crops.py`'s `auto_x`) locks onto the fridge.
- ✅ **Torso block**: ~23–31 px frame-to-frame spread, which is his real sway, not noise.
  A per-shot constant is then enough — **no time-varying pan is needed** and a pan on a
  locked tripod reads as a mistake.

**Get the mask from Apple's Vision framework, not from colour.** A skin+dark-garment
heuristic bled straight into the stainless fridge and reported centres 0.15 too far right.
A ~40-line Swift CLI over `VNGeneratePersonSegmentationRequest` (`.accurate`) gives a clean
mask offline, no model download, ~1.5 s/frame:

```swift
let req = VNGeneratePersonSegmentationRequest()
req.qualityLevel = .accurate
req.outputPixelFormat = kCVPixelFormatType_OneComponent8
```

⚠ **It segments EVERY person, so a `pip` shot's poster subject counts too** — exclude pip
shots or mask to the presenter's side of the frame first.

**Two numbers, and they answer different questions.** `offset` = `(x_used − torso) ×
1920 × 1080/cropW`, i.e. how far off centre he sits in the delivered frame. `cut-off` =
`min(clipped one side, background margin on the other)`, i.e. what a pure shift would give
back. **Both matter**: `v3-short4` was clipping almost nothing yet sat 135 px off centre and
still read as wrong. Calibration point — the short Dan rejected measured **133 px offset /
68 px cut-off**. Thresholds that matched his eye: re-cut at **≥60 px weighted or ≥110 px on
any one shot**; ≤35 px is invisible.

⚠ **AND THEN LOOK, because the metric over-fires on anything that is not the locked
camera.** It flagged 4 of the 5 V6 Shorts; the A/B sheets showed only **1** was genuinely
bad, and adopting the other three would have made them **worse** — V6 is handheld, outdoors
and shirtless, its offsets were already hand-tuned, and "torso centred" is not the goal for
a standing kettlebell demo where the weight on the ground is part of the frame. Render
**5 frames across the shot**, shipped beside proposed; one midpoint frame is not enough.

⚠ **Check the treatment before you audit anything.** The five V4 Shorts use the band
layout — the whole 16:9 frame sits inside the vertical frame, uncropped — so they *cannot*
have this defect. Only `talk`/`broll` full-bleed crops are at risk.

**Re-cutting is cheap and provably surgical.** Edit `shots/crops.json` (keep the shipped
values in a `.pre-recentre` backup and always recompute from that, never from a previous
edit) and re-run `node render.js <SEG>`. ~1–3 min per short. Assert against the shipped
file afterwards: **identical frame count, duration, resolution, fps and audio MD5** — the
crop is the only thing that may differ.

### ⚠ A RE-CUT IS NOT FINISHED UNTIL EVERY QUEUE HOLDING THE FILE HAS BEEN SWAPPED (2026-09-02)

**Dan's rule, stated 2026-09-02: "No centering issues like this can be allowed in posted content."**
The 8/27 re-centre fixed ten masters and swapped 25 Blotato posts, and then left the natively
scheduled YouTube copies "for Dan to decide". Nobody decided. **YouTube kept publishing the old
off-centre files on schedule** — four went live (`y0XIbNoA2Xo`, `P9VUGyWeNtY`, `VOlZHV1ibmU`,
`rqyK5IDsxX0`) before Dan caught one on 2026-09-01. One Blotato post was also missed.

1. **Inventory every queue before you re-cut**: Blotato (`fetch_schedules`, all four accounts —
   IG `67203` + `65632`, Facebook `47105`, TikTok `58181`), YouTube Studio's Shorts list (read the
   schedule with `row.polymerController.__data.video`), and anything Dan posts natively. Write
   the list down; the swap is done when every row on it is verified.
2. **Blotato: create-then-delete, or delete-then-create at the 200 cap.** `scripts/blotato/swap_media.py MAP.json --apply`
   recreates each post with the identical account, target (cover, first comment, privacy flags),
   caption and `scheduledTime`, backs the old body up to `scripts/blotato/swap_backup/` first, and
   the Starter plan refuses creates at 200 with a clean 422 (code 20010) — so at the cap the
   script deletes first. **Verify by downloading the new media and MD5-matching the master**;
   Blotato re-hosts under a new UUID and URL comparison proves nothing. Allow ~10 s before the new
   schedule appears in the list.
3. **YouTube cannot swap a file. A scheduled Short gets: old → Private (unscheduled), corrected
   master uploaded as a NEW video with the identical title / description / tags / made-for-kids /
   date / 5:00 PM time, then the old one deleted after the new one reads Scheduled.** Never leave
   this "for Dan" — it is the step that shipped four off-centre Shorts.
   - **The upload needs no file picker and no Dan.** The Studio page can `fetch()` a public https
     URL (Blotato's storage, `access-control-allow-origin: *`; localhost is blocked by Chrome's
     private-network rules) and hand the blob to the dialog:
     `input[type=file][name=Filedata]` ← `DataTransfer` + `change` event. 34 MB uploads in ~5 s.
   - Title/description: `execCommand('insertText')` into `#title-textarea #textbox` /
     `#description-textarea #textbox` inside `ytcp-uploads-dialog`. Kids: click
     `tp-yt-paper-radio-button[name=VIDEO_MADE_FOR_KIDS_NOT_MFK]`. Tags: `#toggle-button` (Show
     more) then per tag set the input value via the native setter + `input` event, dispatch
     keydown+keyup `,`, clear. 15 channel tags are inherited — add only the video's five.
   - Schedule: date via a REAL click on the date chevron then a real click on the day in the
     calendar (typing into the field does not land); time via a real click on the field, then
     JS `scrollIntoView` on the `tp-yt-paper-item` whose text is `5:00 PM`, then a real click on
     it. Verify both by zoom, THEN click Schedule, THEN read the confirmation dialog.
   - Making the old one Private from its details page: JS click
     `ytcp-video-metadata-visibility #select-button` (a real click after a fresh navigation is
     swallowed until the page hydrates), then `#first-container-expand-button`, the
     `tp-yt-paper-radio-button[name=PRIVATE]`, and the dialog's own `ytcp-button#save-button`
     (that is its Done). The page Save must be `setTimeout(()=>save.click(),100)` and returned
     from immediately — awaiting anything after the page Save inside one evaluate hangs CDP for
     45 s. Verify `ytcp-button#save` is disabled and `#visibility-text` reads Private.
   - Deleting the old copy: ⋮ next to Save → Delete → tick "I understand" → Delete forever. Use REAL clicks
     — a script-driven delete is refused by the permission classifier. After any fresh navigation the first
     real click on the ⋮ is swallowed until the page hydrates (~12 s); click, wait, click again. Likewise the
     upload dialog's title/description only accept `insertText` in a SEPARATE evaluate after the wizard has
     been walked once (Next×3, back to `#step-badge-0`) and the header reads "Saved as private", not
     "Saving...". Verify at the end on the Shorts list: every new id Scheduled, no old id present.
   - The metadata read-back JS must mask query strings (`.replace(/\?utm[^\s]*/g,'?UTM')`) or the
     tool refuses to return it; rebuild the UTM from the plan's campaign + slug.
4. **Run `recentre/delivered_gate.py` on the delivered file and LOOK at the strip** before any of
   the above; nothing ships on the numbers alone. Metric verdicts from this audit: the torso
   anchor under-reports a SEATED subject whose legs extend to one side (`v6-short2` measured head
   −2 px / upper body +7 px in the delivered file and was left alone against the handoff's
   instruction to re-cut it), and over-reports a standing subject next to a floor prop (`v6-short3`
   at +186 px was genuinely off and was re-cut to 0.555).

### ⚠ STANDING RULES: contain the body, never slice a graphic (2026-08-28)

Dan, after rev 3: *"make sure I'm not going off screen when I do the ab wheel rollout. Center
me... do a more thorough double-check for graphics that are cropped out or which don't make any
sense in the video (where you only see part of the graphic or you're not seeing anything
meaningful)."* Both are now measured before a frame is encoded — `work/shotgeom.py` measures,
`work/framecheck.py` asserts.

**1. Measure the subject's SILHOUETTE UNION over the whole shot, not the torso centre.** The
torso anchor answers "is he centred"; it says nothing about whether his hands are still in
shot. On the ab-wheel cut the two answers are wildly different: his torso barely moves, but
**during a rollout his silhouette spans 0.03 → 0.97 of the 16:9 width** — hands and wheel at
one edge, shoes at the other. A crop set from eyeballed extremes ([0.29, 0.94]) looked right on
a contact sheet and cut his hands off on every single rep.

**2. On a source like this there is no crop that is both tighter than the frame and safe.**
When the subject spans ~94% of the width and the burned graphics span 90–96%, **the full frame
IS the correct card.** Do not treat that as giving up — it is the only window that keeps the
whole body in shot and every graphic whole, and it makes the card size identical across the
batch. Reach for a tighter `cardCrop` only for a genuine inset (a TV, a graphic-in-graphic),
and verify that inset is contained whole.

**3. A graphic must be entirely IN or entirely OUT — never straddling the window edge.** The
failure looks like a stray white sliver at the frame edge and reads as a rendering fault. Dan
caught two (0:10 and 0:19 of one short): Muhammad's muscle-name pills sit on a translucent
olive panel that extends ~70px past the pills themselves, and a `minX0` set from the pills
alone sliced the panel. **Measure the union across the shot — these graphics typewrite in, so
one frame under-reports the width — and pad for whatever sits behind them.**

⚠ **Split the graphic scan by REGION.** A bright sky fills the top band exactly the way a white
pill does. A whole-frame union then merges a real bottom lower-third with a spurious top hit
and reports one box spanning the entire height, which fails every containment test. Scan
`rows < 0.32` and `rows > 0.58` separately and require text-coloured ink inside the same rows.

### ⚠ The Vision mask can leave a sliver at the frame edge — mask-top is not head-top

On the supplements roll a faint low-confidence band along the top of frame put three beats'
"head" at source row 15 against a true ~180 — a 160 px error that would have set the whole
batch's vertical geometry. Take the largest connected component and require a real run width
(>=20 px at 640) before calling a row the head. `reference/clean-master/work/vertgeom.py`.

## Step 6 — does the subject leave room for graphics? MEASURE IT

**This is the decision that produced the band layout, and it is the one Dan cared about.**

Before placing any overlay, sample frames across the segment and measure how often each
candidate region is clear of the subject. On V4 short1 the best of eight candidate slots
was clear **33% of the time and 0% in its worst frame**. There was nowhere to put anything.

**And measure whether the set dressing is PAYLOAD before paying for it.** The supplements
handoff called for the band layout on product shorts because Dan stands behind his whole
supplement stack. Measured with `reference/clean-master/work/stackscan.py` (temporal median of
a region, then departures from it): the stack moved by **1.07 grey levels over 23 minutes** and
he never picked anything up in 25 sampled frames. It was wallpaper, and the band would have
cost 60 % of his height to preserve it. Full-bleed won on measurement.

**Cropping the top off is the RIGHT direction when the subject sits low in frame.** It narrows
the window (the trap above) but it also makes the subject bigger, and the trade is measurable:
644x960 -> 1080x1610 is **1.68x**, which beats a full-height 608x1080 crop at 1.78x on size AND
sharpness. Pick it from the GLOBAL MINIMUM head position across every beat, leaving >=60 px of
clearance under the title band.

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

## Step 6.5 — cover a join with an AI clip when the cut still shows

Dan, 2026-08-28: *"Cover that awkward cut with an AI-generated clip illustrating what's being
said in the video at the time."* Veo 3.1 Fast via the Gemini API, native 9:16, ~$1.20 each; the
working generator is `reference/clean-master/aigen/`. An insert straddles the join, taking part
of its length off each neighbour, so **runtime is unchanged and the audio underneath never
moves.** Label each one AI GENERATED.

Four things that cost a regeneration or a re-render:
* **Anything with a label surface invites invented lettering** — a pill organiser came back
  reading "MON MON THE 2ND FRI". Ask for objects carrying no text at all.
* **The casting rule applies to hands-only shots.** State it in the prompt.
* **Choose the in-point off a frame strip**, not the head of the file: one clip filled with
  steam after 2 s, another did not reach the payoff (a lit brain) until 5 s.
* **Bias the crop up (0.30, not centred)** — a 9:16 clip in the shorter picture area loses 310
  rows, and centred that cuts the subject's hairline.

## Step 7 — overlay rules

⚠ **STANDING RULE (Dan, 2026-08-28): THE TITLE STAYS ON SCREEN FOR THE WHOLE SHORT — every
short, vertical source or horizontal.** *"For all videos, vertical or horizontal, that we make
in the shorts, let's always keep the title on screen the entire time. Put it on the black space
and move the video frame down as necessary to accommodate that."* His reason is composition:
a 16:9 clip in a 9:16 frame leaves a lot of black, and a title that fades leaves the top band
dead for the rest of the video.

**This SUPERSEDES the old V4 rule** ("a title must not sit on screen for the whole video").
That rule was written when the title sat **on Dan's face** and chips stacked over him — the
fault was the position, not the duration. Read the two together: **the title holds, and the
picture moves down so the title never touches it.**
- **One chip at a time, not an accumulating stack.** Add a "MUSCLE n OF 4" style counter —
  it paces with the voice and opens a small loop that holds people to the end.
- **Sync chips to the audio, but not slavishly.** When two items are named ~1s apart,
  a strict one-word-one-chip sync leaves one on screen for ~1s and unreadable. Give the
  first the whole naming phrase and switch on the *end* of the second's name.
⚠ **STANDING RULE (Dan, 2026-08-28): THE TITLE MAY NEVER SIT ON HIS FACE OR HIS ABS.** His
words: *"Don't block face or abs with title - move me down or if not possible move title to
bottom of captions."* On a full-bleed 9:16 crop there is no vertical slack to give - his head
starts at source row 35, i.e. y62 in the delivered frame, and a 2-line Impact headline runs to
y300 - so **drop the picture instead**: render it into 1080 x (1920 - dropTop) at the BOTTOM of
the canvas and let the J2 field carry the title in a band of its own.
`scored-source/layout.json` uses **dropTop 310**; his head then starts at y362.

Two things this buys that are not obvious:
- **It is SHARPER.** The source crop widens from 608 to 724 to fill the shorter picture, so the
  upscale falls from 1.78x to 1.49x (and 2.60x to 2.15x on a zoom shot). The cost is 16% of
  picture height, not of resolution.
- **The eyebrow can then persist**, which it should - the band would otherwise sit empty from
  3.2s on. Split the assets: `title-<ID>.png` (scrim + headline, fades) and `header-<ID>.png`
  (eyebrow, holds).

**Cards need it too.** The first pass exempted them on the grounds that a title only crosses
the sky at the top of a card; Dan came back and asked for the title on black *only*, never over
the picture. **One line: everything - card or full-bleed - starts at `dropTop`.**

**Assert it on the DELIVERED file, not on the plan** - `work/titleclear.py` takes the title's
solid-glyph bbox and the Vision person mask's top 55% (head through navel) and fails if the two
rectangles intersect on both axes, sampled six times across the title window.

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
⚠ **STANDING RULE (Dan, 2026-08-28): captions print `abs`, in LOWER CASE.** Video #1 set an
`/\babs\b/gi -> 'ABS'` rule and it ran unchallenged for 30 shorts; he killed it batch-wide.
**`AI` stays upper case** - that is an initialism, `abs` is just a word.

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
no black frames, last caption inside the video, no click at any splice, **and the `_shared/audio`
gate stamp for this exact file** (`requireStamp` — no stamp, another build's stamp, or a FAIL is not
deliverable; `deliver.js` checks it again).

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

## Cutting from a FINISHED, SCORED edit (added 2026-08-27, ab-wheel batch)

When the source is an editor's finished 16:9 product rather than our own cut, use
`reference/scored-source/`. Six shorts came out of Muhammad's ab-wheel cut this way; these are
the things that were not true of any earlier batch.

**`silencedetect` is the wrong ground truth once there is a music bed, and it fails in BOTH
directions.** On that cut the pause at 43.54-43.98 s measures **-16 dB — louder than the speech
before it**, because his bed swells into the gap, while a real gap elsewhere reads -33 dB. So the
snap either refuses every cut or lands one on a music swell. Measure voice-band energy against a
rolling local floor instead (`work/vad.py`, 300-7000 Hz). **Band to 7000, not 3400:** at 3400 the
trailing /s/ of "scams" is invisible and the out-cut eats the fricative.

**Fade the head and tail, and dip every internal join.** A bed that starts mid-bar and stops dead
is the giveaway that a short was carved out of something longer. 0.18 s in, 0.45 s out, 60 ms
either side of a splice. Never `acrossfade` — it shortens the audio and unlocks it from picture.

**Normalise loudness across the batch AFTER rendering.** A dynamic master (his LRA was 13.6) gives
every short a different level: six sections produced -13.2 to -18.0 LUFS, a 4.8 dB spread that a
viewer hears the moment they scroll from one to the next. `normalize.js`, linear loudnorm to -14
with a limiter, video copied.
⚠ **`linear=true` is a request, not a guarantee** — when the source is already near 0 dBTP ffmpeg
silently falls back to dynamic mode and compresses the mix, which is what Dan rejected on the Ad-1
vertical on 2026-09-02 ("sounds horrible ... never deliver anything again that doesn't sound like
Muhammad's videos"). Prefer an explicit `volume=<gain>dB` + `alimiter=level=disabled`, and prove it
on the finished MP4 with `/shortad-from-longform reference/gain_flatness.py SOURCE OUT --gain G`.

**Burned graphics are shown whole or cropped off — never sliced.** Measure them (`work/gfxbox.py`,
`work/ltwindows.py`); on that cut the top pill was 1595 px wide, 83% of the frame, so no horizontal
crop dodges it. ⚠ **And check whether the graphic is still TRUE inside the short you are building:**
his cut carried a stale "How Intermediate Guys Should Do It" across the standing-wall beat, which
would have been a factual error on screen in a short about that beat. It is cropped out.

⚠ **CROPPING THE TOP OFF A 16:9 FRAME MAKES THE CARD SHORTER, NOT BIGGER.** This was got wrong once
and shipped into a review render. Trimming height makes the aspect WIDER, and a wider card fitted
to a fixed width is shorter: the "closer" crop measured 522 px tall against 643 px for the
untouched frame. To make a card bigger you must crop WIDTH. The card gets bigger by cropping the
dead sides, not the dead sky.

**A card-heavy short needs a STAGE, not the 1000x562 inset.** When the source movement is
horizontal - an ab-wheel rollout spans 0.30-1.00 of the frame at full extension, against a 9:16
window's 0.317 - most shots have to be cards, and the old inset leaves the frame reading as
unfinished. `scored-source/layout.json` uses **1080 x 830 at y=170** with the title sitting ON the
picture over a scrim baked into the title PNG. Roughly 2.4x the area.

**Two ffmpeg faults that both present as a black frame, and neither is a concat artefact:**
- `overlay` follows its FIRST input, and a `-loop 1` still is INFINITE, so the last frames of every
  card shot rendered as bare background. Needs `shortest=1` on the overlay as well as `-t`.
- `-ss` leaves the first decoded frame with a non-zero PTS while the looped background starts at 0,
  so overlay emitted one background-only frame BEFORE the picture. Needs
  `[0:v]setpts=PTS-STARTPTS` at the head of the card filtergraph.

**`blackdetect` cannot see either of them.** The title, captions and wordmark still draw, so the
frame is not black and the gate passes. `work/stagescan.py` measures the stage rectangle itself at
full frame rate; that is what caught both.

**A finished cut joins its sections with white flash blooms, so check every in and out point.**
`work/flashscan.py`. Three of sixteen boundaries had to move on the ab-wheel batch, one of them a
1.25 s bloom the short would have opened on.

**Set the framerate from the source.** That cut is 29.97; resampling to the batch's usual 24 drops
one frame in five and every shot carries a constant slow push, so the judder is visible on all of
them. The masters ship at 29.97.

### Rev-2 lessons from the ab-wheel batch (2026-08-28)

**A hand-picked crop number IS a guess, and this pipeline's own contact sheet will not catch
it.** Every talk crop in rev 1 was set by eye off a 480 px thumbnail and reviewed on a
`choose-crops.py` sheet, and six of them were **291-508 px off** in the delivered frame. Dan
screenshotted the worst one. **Measure with `recentre/` on EVERY build from now on, not only
when a short is already off** - the audit is ~10 minutes of compute and it is the difference
between "looked fine in the sheet" and 0 px.

**The audit now covers cards too, not just 9:16 crops.** `recentre/audit2.py` projects the
measured torso through whatever geometry a shot uses - talk window, zoom window, or `cardCrop`
rectangle - and reports one number: pixels off centre on the delivered 1080x1920 canvas. A card
can be just as wrong as a crop; two of the ab-wheel cards were 670 px and 466 px off.

⚠ **CENTRE A STATIC SUBJECT, CONTAIN A MOVING ONE.** This is the rule that decides which flags
to adopt. An ab-wheel rollout crosses the frame, so the crop has to hold the whole path and the
subject is CORRECTLY off centre for most of the shot. The audit flagged every rollout card at
100-316 px - including five in a short Dan had just reviewed and passed as having no centring
issues. Adopting them would have clipped his feet. **The over-fire is not noise, it is the
metric asking the wrong question of a travelling shot.**

⚠ **RE-CHECK SHOT BOUNDARIES AGAINST FULL FRAME RATE, because a wrong boundary presents as a
framing bug.** The scene detector runs on a 320x180 downscale and can land a cut EARLY when the
outgoing shot is already moving. On this batch a boundary was **0.60 s early, so 18 frames of
gym b-roll were given a talking-head crop** - which is what Dan saw and called "off-centre
b-roll". `work/boundcheck.py` compares every boundary to a frame-difference peak at native rate;
`CUT_FIX` in `detect-shots.js` overrides the bad ones. It also tells you when a "boundary" is not
a cut at all: two shots on this build were one continuous take split spuriously, which is why
their crops must stay identical.

⚠ **CROPPING THE TOP OFF A 16:9 FRAME MAKES THE CARD SHORTER, NOT BIGGER.** Trimming height
widens the aspect, and a wider card fitted to a fixed width is shorter - 522 px against 643 px
for the untouched frame. **To make a card bigger you crop WIDTH.** This shipped into a review
render before it was measured.

**Native-vertical b-roll beats any crop, and it is worth going to find.** The `extern` treatment
in `scored-source/render.js` drops a 9:16 source clip in full-bleed at ~1.0x, against the 1.78x
a 9:16 window costs out of 16:9. Pexels' search API needs a token, but the rendered search page
is scrapeable same-origin in the in-app browser (`a[href*="/video/"]`), and the detail pages
carry `videos.pexels.com/video-files/<id>/<id>-hd_<w>_<h>_<fps>fps.mp4` in plain text. Grade it
lightly toward the batch - measured, not guessed; the reference cut's own b-roll already ranged
Y 58-172, so match cohesion, not numbers.

**When a title has to work cold, name the thing in the HEADLINE, not the eyebrow.** Dan, rev 2:
*"the titles need to make sense to someone who hasn't watched the video. A lot of the titles
assume watching the long form."* A headline reading "THE $17 TOOL THAT BEATS CRUNCHES" with the
subject only in the eyebrow does not survive the scroll.

**Never re-run `normalize.js` across the whole batch to fix one short.** It gave three finished
files a second loudnorm + AAC pass for no gain. Both `normalize.js` and `qc.js` now take a
segment filter.

## What the ab-wheel batch cost, and what would have avoided it (2026-08-28)

Five shorts, **four review rounds**. Everything Dan rejected was something a contact sheet
showed me and I read wrong. These are the generalisable lessons; the rule statements are in the
steps above.

**THE CONTACT SHEET IS NOT A GATE. Every framing fault in this batch survived one.** Rev 1 shipped
six talk crops 291–508 px off centre, and rev 2 shipped demo crops that cut his hands off on every
rep — both after I had rendered the proposed vertical frames and looked at them. A 170 px-wide
thumbnail cannot show you a 300 px error on a 1080 px frame, and it cannot show you that the hand
at the edge is *cut* rather than *ending there*. **Look to catch what a metric cannot describe;
measure everything a metric can.** The pipeline now measures: subject silhouette, graphic boxes,
title clearance, shot boundaries, centring — all asserted before or on the delivered file.

**Ask "is he still IN the shot", not just "is he centred".** These are different questions and
this batch answered only the second one for two rounds. The torso anchor is right for centring and
blind to clipping. `work/shotgeom.py` measures the silhouette UNION over every frame;
`work/framecheck.py` asserts containment. **Run both on every build, not only when something looks
wrong** — the audit is ~10 minutes of compute against a re-render plus a review round.

**When a measurement contradicts your crop, verify the MEASUREMENT before you act — and when it
contradicts an APPROVED short, believe the short.** Both directions bit here. The Vision spans
looked implausibly wide until `work/verifyspan.py` drew them back onto their own frames and they
were exactly right. And the centring metric flagged every rollout card in a short Dan had just
approved — adopting those would have clipped his feet. **A metric that disagrees with an approved
deliverable is asking the wrong question of that shot.**

**A finished cut from another editor is a constraint, not a canvas.** Muhammad's graphics are
burned in at 90–96 % of the frame width and his subject spans 94 % during a rollout, so the full
frame was the only safe window. **Establish that early**: measure the widest graphic and the widest
subject pose in the first pass, and let those two numbers decide whether a tighter crop is even
available. Two rounds were spent discovering it one shot at a time.

**Re-derive, don't re-guess, when the working drive disappears.** The Extreme SSD detached
mid-task. A byte-identical copy of the source was on the internal drive, and the pipeline is in
git, so the rebuild cost one transcription. **What made that cheap was that the plan is code** —
phrase-anchored cut points, measured crops, and asserted gates all re-ran and reproduced the same
shot list. Absolute in/out overrides (`inAt`/`outAt`) survived a new transcript; phrase anchors
did not, in three places ("wanna" for "want to"), and `find()` threw immediately rather than
silently shifting a cut.

**Two operational traps worth remembering.** A filesystem that needs AppleDouble companions puts a
`._<name>` beside every file, and those match `*.png` globs — they silently doubled every frame
count in the centring audit and made it report "no subject in most frames". And something on this
Mac creates ` 2.mp4` conflict copies in the delivery folder: five superseded rev-2 masters
reappeared next to the finals, same durations, different bytes. **Check the delivery folder for
duplicates before calling a batch final** — the wrong file is one click from being uploaded.

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
