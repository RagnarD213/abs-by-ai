# `clean-master/` — cutting Shorts from OUR OWN clean long-form master

Built for the eight Shorts cut from `03 - The Supplements I Actually Take` (2026-08-28).
Copy it and adapt `config.js`, `segments.js` and `plan.js`; do not rewrite from scratch.

Use this one — not `scored-source/`, `full-bleed/` or `band/` — when the source is a long-form
**we rendered ourselves** and a `CUT_*_NO-GRAPHICS.mp4` exists beside the delivered master.
Four things are different from the other pipelines and all four matter:

## 1. ⚠ RUN `work/preflight.py` FIRST. THE SOURCE MAY HAVE TWO TIMELINES.

**A master assembled by concatenating segments can hold more audio samples than its container
declares, spread through the file.** The supplements master (62 ranges) holds 0.76 s more.
Whisper word timestamps and every silence measurement live on the DECODED-SAMPLE timeline;
`-ss`, and therefore every cut and the whole picture, live on the CONTAINER timeline. They
agree at t=0 and drift ~0.5 ms per second — **669 ms apart by the end of that video.**

The first build of this batch shipped **captions 280–650 ms late** and **clipped the first word
off two shorts**, while passing QC 12/12, the splice test, loudness, duration and the centring
audit. Nothing compared delivered audio against delivered captions.

Extract analysis audio on the container timeline:

```
ffmpeg -i SRC -vn -af "aresample=async=1:first_pts=0" -ac 1 -ar 48000 -c:a pcm_s16le work/audio48k.wav
```

Residual lag then collapses to a constant −20…−42 ms — inside one AAC frame. Full write-up:
`work/TIMELINE_TRAP.md`.

## 2. `syncgate.py` is a HARD GATE and `qc.js` will not pass without it

It transcribes each DELIVERED short and matches every caption's first word against the heard
audio. It is the only check that measures what a viewer experiences. `qc.js` refuses to pass a
file the gate has not seen, keyed on mtime so a re-render invalidates the stamp.

⚠ **It carries a calibration, and the calibration is not a fudge.** The gate uses `base.en`
while captions come from `medium.en`, and base.en reports word onsets a median of **exactly
−80 ms** earlier — measured on the same source audio over three spans, n=414, −80 ms in all
three independently. Uncorrected it fails good builds. Re-measure if either model changes.

## 3. Shot boundaries come from the EDL, not from scene detection

We own the cut, so `edl.json` lists every splice. `work/edl_splices.py` computes their nominal
positions and `work/splices.py` **measures** each one as a full-frame-rate frame-difference
peak, because `render.py` rounds every range to whole frames and the error accumulates
monotonically (+1.137 s over 62 ranges — exactly the amount by which the EDL undershoots the
master). All 61 boundaries came back at 3.2x–22x the local median. `detect-shots.js` then just
intersects that table with the chosen pieces. This is strictly better than the 320x180 `scene`
detector, which put a boundary 0.60 s early on the ab-wheel batch.

## 4. Cut points are the INTERSECTION of two silence measurements

A clean master has no music bed, so `silencedetect -26dB/0.05` is valid here — which makes it a
free independent control on `work/vad.py`'s speech-band map rather than a replacement for it.
`work/gaps.py` intersects them, so every cut is both "nobody is talking" and "nothing is
audible". They agreed on 85 % of silencedetect's intervals; the intersection kept 1082 gaps.

⚠ **`snapIn` must accept a gap that CONTAINS Whisper's claimed word start**, not only one that
ends before it. Whisper stretches short words backwards across real pauses; without that clause
short E opened on "...from there. So this is the biggest mistake" — a fragment of the previous
sentence. When the claimed start is inside measured silence, the word begins at the gap's end.

## Also fixed here, and it affects every earlier batch

**`captions.js` silently dropped every zero-duration Whisper word.** The `>50 % overlap` test
computes `0/1e-6 = 0` for a word with `start == end`. Nine such words on this roll; it ate one
in five of the eight shorts, turning "creatine is not an **option** for me" into "not an for
me". Also fixed: mis-hearing corrections now run **per word, before chunking** (a two-word fix
straddled a four-word chunk boundary and the line-level regex never saw it), hyphen-initial
tokens merge like punctuation ("sub -step"), and the first word of each piece is capitalised.

## Layout notes specific to a locked talking-head master

* **Measure whether the set is payload before choosing a layout.** `work/stackscan.py` takes the
  temporal median of a region and reports departures from it. Here the supplement stack moved by
  1.07 grey levels over 23 minutes, so the band layout would have cost 60 % of subject height to
  preserve wallpaper. Full-bleed won.
* **Cropping the top off IS the right direction when the subject sits low.** It narrows the
  window (the documented trap) but makes the subject bigger, and the trade is measurable:
  644x960 at 1.68x beats a full-height 608x1080 at 1.78x on both size AND sharpness.
  `work/vertgeom.py` picks it from the global minimum head position.
* ⚠ **The Vision mask leaves a faint sliver along the top frame edge on some frames**, so raw
  mask-top is not head-top — it reported row 15 against a true ~180 on three beats, a 160 px
  error that would have set the batch's geometry. Take the largest connected component and
  require a real run width (`work/vertgeom.py`).

---

# Rev 2 (2026-08-28) — Dan's revision notes, and what they turned into

His notes named four "awkward cut"/"jump cut" timecodes, two "junk footage" ones, one long
pause, three title changes, one audio complaint, and "double-check everything". Every named
timecode turned out to be an instance of a CLASS, so each was fixed as a class.

## `work/junkscan.py` — run this before delivering, every time

Reports, per short: measured pauses over 0.55s, picture cuts inherited from the source edit,
and how late speech starts. It found all six of Dan's timecodes and nine more he had not
reached yet. **It is what turns "double-check everything" into a list.**

## ⚠ A PAUSE CANNOT SIMPLY BE REMOVED. `work/pausejump.py` proves it.

Cutting a pause joins two moments in time, and Dan MOVES while he is not talking. Measured as
mean-abs-difference across the join, against a 1.30 adjacent-frame baseline:

| | score |
|---|---|
| adjacent frames (no jump) | 1.30 |
| an inherited source splice — what "awkward cut" means | 7.64 |
| **removing a pause** | **4.97 – 12.46** |

So a pause removal is as visible as the fault it is meant to fix. **Every join must be
HIDDEN, not just made** — `plan.js` alternates wide/tight at each one (`tight: true`), which
reads as a camera change. Geometry in `layout.json`: 578x862 @ top 126 against 644x960 @ 120,
set so his head lands at the same delivered y, i.e. only the framing moves.

Corollary: do not remove every pause the scan finds. Five 0.57-0.65s pauses were deliberately
kept — they are breathing rhythm, and cutting them would have added five more joins.

## Whisper hides the junk inside a word — `work/fixonsets.py`

Dan's "junk footage in the beginning at 0:01" was a 0.95s HESITATION that the pause scan could
not see, because Whisper timed the word "you're" at 1046.94-1048.82, swallowing it. Three
corrections against measured silence, run right after the gaps are built:
onset inside a gap → the gap's end; offset inside a gap → the gap's start; **a gap of >=0.25s
wholly inside a word → the word begins at that gap's end.** On this roll: 363 onsets, 328
offsets, and **51 words that had swallowed a pause.**

This also fixes two caption faults, because a word straddling a piece boundary otherwise fails
the >50%-overlap test and is spoken but never captioned.

## Cutting from the RAW ROLL when the master has no better take

Dan asked for a better take on one opener. The master is a finished cut, so the alternative
existed only in the raw. It works, and the checks that make it safe:

* **Orientation and grade.** A graded raw frame correlates **0.9999** with the master frame it
  became (0.15 against its mirror). The EDL's own `grade` curve is all that is needed.
* **Audio is the hard part** — the raw is the camera's two-mic recording, not the master's
  repaired single-mic chain. `work/fitraw.py` takes the RIGHT channel and fits a per-band EQ.
  ⚠ **Fit it against the content it will NEIGHBOUR, not against a take present in both files.**
  Fitting on the shared take left a 1.45 dB seam, because the insert is a different take with
  its own mic distance. ⚠ And **close the loop** (`work/rawiter.py`): the whole-short EQ and
  limiter move it again afterwards. 1.45 → 1.14 → **0.50 dB**, inside the batch's own spread.
* ⚠ **ONE `-af` ONLY.** The raw EQ and the fades were pushed as two separate `-af` flags and
  ffmpeg honours the last, so the correction was silently discarded through three rebuilds.

## Tonal matching across the batch — `finishaudio.py` (replaces `normalize.js`)

Dan: one short "doesn't sound as good as the other ones". All eight were already at -14 LUFS,
so level was never it. **Tone was**: cut from different points of a 23-minute take, their
low/high tilt spanned 5.1 dB, and the short he named was the thinnest.

Fit each short to the batch MEDIAN octave profile, **one peaking filter per band** (a
three-knob shelf/peak/shelf model could only halve the spread, and left the named short still
worst). Gains damped 0.85 and clamped to ±4 dB so it stays a correction. Result: tilt spread
**5.1 → 1.5 dB**, worst band error **1.36 → 0.92 dB**, the named short **1.36 → 0.76 dB**.

No broadband noise reduction: /longform-edit already tried `afftdn` on this material and
rejected it. Tone is the fixable part.

## Titles: fit the TYPE to his words, not his words to the type

Dan's new headline for one short measured 1352px against a 976px limit at the batch's 98pt.
`build-assets.py` now picks the largest size at which both lines fit (that short landed at
78pt) instead of forcing a rewrite or a third line, which would break the title-clearance rule.

## Caption rules added

* A chunk may never span a piece join — the raw opener ended "...taking supplements is" and the
  next piece began "I bought", which printed as "taking supplements is I".
* Capitalise a piece's first word **only if a sentence actually ended**. Two of rev 2's joins
  continue a sentence, and blanket capitalising printed "So let's say You're taking nothing"
  and "muscle building For your brain health".
* `TAIL_COMMA` marks a join where a whole clause was removed, so the caption gets its comma.

---

# Rev 3 (2026-08-28) — the audio was wrong at the source for two whole revisions

## ⚠ VERIFY THE SOURCE'S CHANNELS. DO NOT TAKE A HANDOFF'S WORD FOR IT.

The handoff said the clean master's audio "is already the fixed single-mic chain". **It is
not.** `work/chancheck.py`, run on the file itself:

| file | L/R corr | best lag | verdict |
|---|---|---|---|
| `CUT_v1_graded_NO-GRAPHICS.mp4` (what we cut) | **+0.069** | **−7.58 ms** | two mics, unrepaired |
| `FINAL_supplements.mp4` | +0.9997 | 0.00 ms | repaired 2026-08-23 |
| `FINAL_supplements_PRE_AUDIOFIX.mp4` | +0.069 | −7.58 ms | known bad |
| raw roll `C1514.MP4` | +0.057 | −7.58 ms | the camera's two mics |

The clean master has the SAME signature as the file explicitly named `PRE_AUDIOFIX`. Only the
delivered master ever got the repair. **Rev 1 and rev 2 both shipped comb-filtered audio**, and
Dan heard it before any metric did — the gates measured level, sync, splices and tone, and
none of them measures whether the two channels are the same microphone.

**Run `work/chancheck.py` on the source before Step 1, every batch.**

## The right channel is also the best source available

| source | SNR | note |
|---|---|---|
| summed pair (what rev 1/2 used) | 26.6 dB | comb-filtered |
| **right channel only, mono** | **29.8 dB** | the close lav |
| the repaired `FINAL` master | 19.9 dB | its treble shelf lifted the lav hiss |

So do not pull audio from the repaired master either — go back to the right channel and do the
repair here.

## Making it sound like Muhammad's — `work/muhfit.py`, `work/voicechain.py`

Dan's reference is Muhammad's ab-wheel cut. Measured against it, relative to the 320–640 Hz
body band, our lav was **3.8 dB short of weight, 3.8 dB short of presence, 8.7 dB short of air
(5–9 kHz) and 12.0 dB short above 9 kHz.** Dull. That is what "doesn't sound as good as
Muhammad's" means, and it is fixable — our SNR was 30.2 dB against his 21.2, so there was room
to add top end without exposing hiss.

`work/voicechain.txt` (right channel → weight → de-honk → presence → air shelf → top octave →
de-ess) takes the octave-band shape difference from **4.05 dB RMS to 0.62**, lands sibilance
within 1.2 dB of his, and leaves our noise floor 5.6 dB cleaner than his.

⚠ **The chain already folds to mono. Anything appended must not `pan` again** — a second
`pan=mono|c0=c1` asks for a channel that no longer exists and ffmpeg renders **silence**, not an
error. It blanked the first 4.48 s of a short. `qc.js` now scans the MASTER for silent seconds
(only the review copies were scanned before, and that gap let it through).

## AI cover clips over the joins — `inserts.js`, `aigen/`

Dan asked for generated clips over the cuts, illustrating what is being said. Veo 3.1 Fast via
the Gemini API, native 9:16, ~$1.20 each. An insert straddles a join, taking `pre` off the
outgoing shot and the rest off the incoming one, so **runtime is unchanged and the audio
underneath never moves.** Each carries an AI GENERATED label.

Things that bit:
* ⚠ **Anything with a label surface invites invented lettering.** A pill organiser came back
  reading "MON MON THE 2ND FRI". Ask for objects that carry no text at all.
* ⚠ **The casting rule applies to hands-only shots too.** A regenerated clip came back with
  hands that did not match it; state the casting in the prompt.
* **Pick the in-point by looking at a frame strip.** The ironing clip fills with steam after
  ~2 s and only its first second reads as ironing; the creatine clip does not reach the brain
  until 5 s, so its insert starts at 4.6 s to catch muscles AND brain in one 2.2 s window.
* **Bias the crop up (0.30, not centred).** These are 9:16 into a shorter picture area, so
  filling the width crops 310 rows — centred, that cut the subject's hairline.

## Two more measurement traps

* ⚠ **Whisper hallucinates a lead-in when a clip starts mid-sentence.** `base.en` invented "So
  let's say" in front of a short that opens "You're taking nothing right now", and compressed
  the real words to fit — which failed `syncgate.py`'s first-word test on a correct build. The
  gate now accepts the caption's first word anywhere in the opening second.
* ⚠ **Vision's mask bleeds a couple of rows past the picture's top edge**, so a subject
  starting exactly at `dropTop` reads as inside the title. `work/titleclear.py` now ignores an
  overlap under 2% of the title's own ink area.

## `work/mkplan.py`

The SHOTS table is generated, not hand-written. Editing it by hand broke the build twice when
the shot list changed. It also assigns the punch alternation and skips AI clips.

---

# Rev 4 (2026-08-30) — "make it sound like Muhammad's"

Dan, on rev 3: *"the audio is improved but still sounding a little weird. There's a weird
under sound, especially in the beginning. It doesn't sound clean, doesn't sound like
Muhammad."* Four separate faults, three of them mine.

## ⚠ 1. COMPARE AGAINST HIS **AD**, NOT HIS ORGANIC CUT

Rev 3 fitted the tone against `mrepro/ref_hd.mp4` — the ab-wheel **organic** video, shot
OUTDOORS. Its low end carries wind and a different room, so matching it prescribed **+4 dB at
110 Hz**. That single boost:

* raised our noise floor by **4.6 dB** in the 80–250 Hz band, and
* took the reverb tail from **65 ms to 120 ms**.

It is the largest single cause of the "weird under sound". `Muhammad Ad Videos/` is an indoor
talking head on the same two-mic rig — the like-for-like reference. Fitted against the ad, the
prescription is only +2.6 dB low and +4.2/+8.4 top, and the shape difference falls 2.93 → 0.67 dB.

## ⚠ 2. THE FLOOR, NOT THE TONE, WAS THE COMPLAINT

Rev 3 matched only the SPEECH spectrum. Measured in true silence, our floor sat **6–8 dB above
his right through the vocal band**. `work/floorprobe.py` and `work/noisecmp.py` measure it.

The chain that closes it (`work/voicechain.txt`): right channel → `highpass=75` → `afftdn` →
a soft `agate` → the tone EQ → `deesser`. **The gate's RELEASE is the real lever** — at 300 ms it
never closes during a normal inter-sentence pause and the floor barely moves; the useful range
is 180–200 ms. Word integrity stays at 99% (`work/validate_chain.py` transcribes the processed
audio and diffs it, because neither a floor nor a tone measurement can see an eaten word tail).

## ⚠ 3. loudnorm SILENTLY FELL BACK TO **DYNAMIC** AND COMPRESSED

This is the subtle one. Our shorts measure −18.8 to −21.2 LUFS, so reaching −14 needs +5 to
+7 dB — which would push true peak past the −1.5 target. **loudnorm cannot do that linearly, so
it switches to dynamic mode without erroring**, lifting quiet passages toward the voice. It cost
**1.0–1.8 dB** of floor-to-voice cleanliness — undoing part of the gate.

Replaced with a **pure gain plus a limiter**, which cannot change the floor-to-voice ratio at
all, then one corrective trim. Check for this whenever the gain needed exceeds the peak headroom.

## Measuring the floor fairly

Compare the floor **relative to the voice**, never absolutely: his ad masters to −18.2 LUFS and
ours to −14, so an absolute comparison flatters him by ~4 dB for free.

Final: ours sits **32.5 / 37.9 / 32.2 dB** below the voice in the 80–250, 250–1k and 1–4k bands
against his **33.6 / 40.5 / 34.2** — a 1.0–2.6 dB gap, from 6–8 dB at rev 3. The residue is our
room, which is live granite and tile; his is deader.

## A dead end worth not repeating

`work/bedprobe.py` tested whether his "clean" sound comes from a music bed masking the room.
It does not — no steady beat in the quiet frames of either of his videos (autocorrelation
0.04–0.05). Do not add a bed to chase this.

## Caption artifacts the cleaned audio introduced

Re-transcribing on the cleaned right channel changed three words, all caught by reading the
finished captions: `being...about` for a stumble before "about 70%", `Shila` + `Jeet` for
`Shilajit` (added `PAIR_FIXES`, because a two-token name can straddle a chunk), and a
lower-cased `i` where a piece continues a sentence (never lower-case a standalone "I").
