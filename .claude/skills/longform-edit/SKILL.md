---
name: longform-edit
description: >
  Turn a folder of raw longform shoot footage into a finished YouTube-ready MP4 —
  rough cut (retakes/flubs/dead air removed), screen-recording split screen, color
  correction, J2 graphics, and a subtitle file. Use whenever Dan asks to edit a
  longform video, cut down raw shoot footage, add the screen capture to a video,
  color correct a video, add graphics to a longform, or REVISE a longform that was
  already cut — even if he doesn't say "/longform-edit". For vertical Shorts use
  /shorts. For a fully AI-generated video ad use /make-ad. For titles, descriptions
  and thumbnails use /youtube-packaging.
---

# Editing a longform video from raw shoot footage

Built from one full pass: the **2026-08-03 meal-prep / Macro Tracker tutorial**
(`C1541.MP4`, 5:45 raw → 3:48 finished), taken end to end — bake-off, rough cut,
split screen, color, graphics, subtitles. Dan approved every stage.

**Proven again 2026-08-20 on the 8/14 ab-wheel video — the first cut assembled from FOUR SEPARATE
ROLLS** (`C1630`–`C1633`, 17:27 raw → 8:58). Every generic script here assumes ONE source and
breaks silently on a multi-roll video, because identical timecodes exist in every roll; the
multi-source variants are in `reference/` and are documented in its README. That video also added
the trailing-fricative rule and `tailcheck.py` in Step 3, the bright-outdoor grade in Step 6, and
the clipped-source loudness reality in Step 9.

**Proven again 2026-08-20 on a THREE-VIDEO batch from the same 8/3 shoot** — spray tan
(`C1512`, 30:42 → 19:00), Zepbound update (`C1513`, 40:16 → 30:26) and supplements
(`C1514`, 37:39 → 23:28), cut start-to-finish in one session for **$0.00**. That batch is
where the generic scripts in `reference/` come from: give them a `ranges.py` and a
`chips.py` per video and the rest of the pipeline is unchanged. It also added Step 0.5
(identify the videos before transcribing), three more Whisper-timestamp rules in Step 3,
per-roll grading in Step 6, and the SRT token rules in Step 8.

**Working scripts are preserved in `reference/`. Copy one and adapt; do NOT rewrite
from scratch.** They are in git on purpose: `Media/` and `YouTube Long Form Video
Content/` are git-ignored, and the original `/shorts` V4 pipeline was **lost** that
way once. Keep code here, keep media out.

**Cost: $0.00.** Local Whisper, static ffmpeg, open-source analysis. No metered
provider is called anywhere in this pipeline. If a step seems to need a paid API,
you have taken a wrong turn — see Step 1.

---

## Step 0 — get the footage and know its shape

Ask Dan which folder. Raw shoots live in his Google Drive, not on the Mac.

**Download with `curl`, not the browser.** Chrome stalls on multi-GB Drive files
(died at 503 MB in testing). If the folder is link-shared, this works unauthenticated
at ~660 Mbps and resumes:

```bash
curl -sS -L -C - -o "$DEST/C1541.MP4" \
  "https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t"
```

Verify the byte count against Drive's reported `fileSize` before using the file.

**Never download the whole shoot.** The 8/3 shoot was 100+ GB across ~80 files against
~70 GB free. Read durations first — the `.XML` sidecars beside each Sony clip are 2 KB
and contain `<Duration value="FRAMES"/>` plus the exact codec/fps. Pick the one or two
long continuous rolls (the teleprompter takes); the short clips are b-roll.

`ffmpeg`/`ffprobe` are **not on PATH** on this Mac (no Homebrew). Use the static 6.0
builds at `Media/video_edit/bin/`. Symlink them into a dir and prepend to `PATH`.

### Step 0.5 — identify WHICH VIDEO each clip is, before transcribing anything

A shoot folder is unlabelled: 84 clips named `C1444…C1587`. Do **not** guess from
file size or read a whole transcript to find out. Extract a **100-second audio probe**
from every clip over ~55 s and transcribe the probes with Whisper **`base`**
(`reference/probe_identify.py`). Dan opens every take by saying what the video is
("Today I'm going to show you my full supplement stack"), so 40 probes map an entire
shoot in one pass, in minutes, for $0. Only then pull full audio for the chosen rolls.

`-t 100` after `-i` reads just the head of each file, so this costs ~1 % of the I/O
of decoding 118 GB.

**Two ffmpeg-in-a-loop traps, both hit here:**
- **ffmpeg eats stdin** and will swallow a `while read` loop's input, consuming the
  clip list and emitting `Parse error, at least 3 arguments were expected`. Pass
  `-nostdin` (and `</dev/null`) on every ffmpeg call inside a loop.
- **zsh does not word-split unquoted parameters.** `for p in "C1512 1842"; do set -- $p`
  leaves `$1` holding the whole string and `$2` empty. Pipe into `while read a b` instead.

**The long continuous rolls are the talking videos; everything else is b-roll.**
On the 8/3 shoot four rolls over 30 min held four complete videos, and the ~60 short
clips were the kitchen and workout demos.

---

## Step 1 — transcript with WORD timestamps (free)

`reference/whisper_run.py` → local Whisper `small`, word timestamps, **41s for 5:45
of audio** on the M2 Pro. Then `reference/whisper_to_scribe.py` converts it to the
ElevenLabs Scribe response shape.

**Why the converter exists:** it makes `video-use` usable without paying ElevenLabs.
`video-use`'s `transcribe_one()` returns early if `edit/transcripts/<stem>.json`
already exists, so writing a Scribe-shaped file there means Scribe is never called.
Its **unmodified** `pack_transcripts.py` then produces `takes_packed.md`. Verified.

**Do NOT buy an ElevenLabs key for this pipeline.**

---

## Step 2 — Dan picks the beats (never Claude alone)

Same rule as `/shorts`. Read the packed transcript, find retakes, flubs, dead air,
and propose a keep-list. Dan approves before anything renders.

**Find the ground truth first — it is usually explicit in the audio.** The 8/3 clip
contained three retakes including a verbal one: *"hold on… I'm going to redo that last
bit"* then a slate, *"Rolling."* Grep the transcript for `redo|hold on|again|rolling|
let me start over` before reading anything else. Record the retakes and dead air in a
`ground_truth.json` (see `reference/`) so the cut can be scored objectively instead of
by opinion.

---

## Step 3 — cut placement: word boundaries PLACE, silence VALIDATES

**This rule was established by a measured bake-off and then REVERSED. Read it before
touching cut points.**

The Phase 1 bake-off compared video-use's rule (cut on transcript word boundaries)
against the `/shorts` rule (snap into measured `silencedetect` silence), with an
identical keep-list so cut placement was the only variable. Result: both produced
**zero pops** (splice discontinuity 1.09–1.20× control, well under the 3× threshold)
and both hit −14.5 LUFS. But:

- **Silence-snapping CLIPPED THE OPENING WORD on 17 of 20 segments.** Worst case,
  *"Take a good shot of that."* rendered as *"of that."* — the in-point was 1080 ms late.
- **Cause:** `silencedetect` only ends a silence when level rises above the threshold
  (`-32dB`), but soft word onsets ("Take") *begin* below it. So `silence_end` already
  sits inside the word.
- It also dragged one out-point **1.56 s backwards**, silently dropping a clause, because
  no measured silence existed near the intended cut and the search window was ±1.6 s.

**The rule that ships:**

```
in-point  = first word's start − ~120 ms pad
out-point = last word's end + ~80 ms, may snap to silence (safe direction)
then ASSERT each edge is inside, or within ~80 ms of, a measured silence.
If not, keep the word boundary and FLAG the join. Never let the search reach
more than ~400 ms — at ±1.6 s it drops content silently.
```

Word boundaries still come from Whisper, which lies: it emitted **3 zero-length word
timestamps out of 882** (`'set.'` at 305.00–305.00), leaving one edge 190 ms short of
the real word end. That is exactly what the silence *assertion* catches. Use both — one
places, one checks.

**Three more Whisper-timestamp traps, all paid for on the 8/19 invest-health cut
(69-min roll, 98-range EDL — builder preserved as `reference/build_edl_investhealth.py`):**
1. **A CLUSTER of zero-length words is hallucinated text — never cut inside it.**
   Whisper emitted "not just a lot of stuff. And" as six zero-length words where the
   audio contains no such phrase; a different cluster around "Just electricity" carried
   garbage boundaries, and cutting on them rendered *"utility, tricity"*. When the words
   around a planned cut are degenerate, keep the region contiguous (a half-word
   self-correction in the audio beats a clipped joint) and listen-QC it.
2. **A stretched first word (>0.8 s) means Whisper folded the pre-retake pause INTO
   the retake's first word** — an in-point at `word.start − 0.12` lands mid-pause or
   clips the aborted take. Refine: last `silence_end` inside the word span − 0.10.
3. **Clamp every in-point to the previous word's end.** The −0.12 pad otherwise bites
   the tail of the CUT take's last word and puts an audible fragment at the segment head.
   Symmetrically, an out-point snapped forward must never cross the next word's onset.
4. **Do NOT clamp the in-point to a STRETCHED previous word.** Rule 3 backfires when the
   preceding word is itself stretched: Whisper set its `end` to the *next* word's onset,
   so clamping there starts the beat 10–20 ms INSIDE the word you meant to keep. Skip the
   clamp when the previous word's duration is > 0.8 s.
5. **A stretched LAST word is the mirror of trap 2 — its `end` is equally fake.** An
   end-based filter then drops the word entirely and the out-point lands on the word
   *before* it, clipping real speech ("…it should be nearly" instead of "…nearly
   painless"). Admit a stretched last word on its START, then snap the out-point to the
   first measured silence ≥ 0.25 s after that start.
6. **Measured silence outranks Whisper's claimed next-word onset.** Whisper has no
   silence model and routinely starts the next word early; clamping the out-point to that
   claim chops the tail off the last KEPT word ("nothing." cut 0.2 s short because "But"
   claimed to begin 0.12 s before the measured silence did). If the out-point already sits
   inside a measured silence, the silence is ground truth — skip the clamp entirely.

7. **A trailing FRICATIVE is the mirror of the soft-onset trap in rule (1), and `silencedetect`
   at −30 dB cannot see it.** On the 8/14 ab-wheel cut, "…beats crunches." had a −30 dB silence
   starting at 25.70 s, so the out-point at 25.75 passed every assertion — and the finished render
   said **"crunch"**. Re-measured at −45 dB, speech actually runs to 25.99: the unvoiced "-es" sits
   *between* −30 and −45 dB. Whenever the **stretched-last-word** rule fires and the word ends in
   s / sh / f / th / ch, snap the out past the −45 dB boundary (`reference/sil45.py`), or set it by
   hand with `rawout`. **Do NOT promote −45 dB to a general assertion** — on outdoor footage almost
   nothing is that quiet, and a blanket −45 dB audit on this video flagged 19 of 36 edges, nearly
   all room tone.

All six rules are implemented in **`reference/build_edl_generic.py`**, which takes a
`ranges.py` of approximate `(start, end, beat)` triples plus the grade and source path,
resolves every edge, prints the head/tail text of each beat, and **flags** every edge it
could not place in silence. Read the flags: on this batch they caught six genuinely
clipped words across three videos, and the rest were benign Whisper inflation.

**Re-transcribe EVERY beat's tail from the finished render, not just the flagged ones**
(`reference/tailcheck.py`). It is the only check that sees a clipped trailing fricative, and on
the ab-wheel cut it found the one real defect among 18 beats after every other metric passed.

**The window MUST extend ~1.5 s PAST the join.** Ending it at the join truncates Whisper's audio
and it silently drops the final word — that produced **7 false "last word missing" reports** on a
clean cut. The same truncation makes Whisper *stutter*: a 6 s window that ended mid-phrase
reported "So I'm going to run you. So I'm going to run you." and read as a doubled take; an 11 s
window over the identical audio was clean. **With trailing context the real signature is
different — the word is PRESENT but mis-spelled** (crunches → crunch).

**Validate flagged joints by transcribing 6 s of the FINISHED render around each one**
(qc script does this) — it caught the clipped joint that every duration/loudness metric
missed. Also: the full-roll transcript can *miss real words* inside a stretched-word
pause (a whole "a maid service" surfaced at a joint that looked like residue but was
genuine speech) — judge joints by the re-transcription, not by the source transcript.

**A cut-cleanliness QC metric must compare the render against the INTENDED editorial
span, never against the engine's own output ranges.** The first version derived expected
words from each engine's own EDL, so a word the engine had already chopped was never in
the expected set — it reported "0 clipped words" for a cut that was clipping 17 of them.

---

## Step 4 — the rough cut engine: video-use, adopted

Phase 1 verdict, do not relitigate. **`video-use` is not a take-selection algorithm** —
its own SKILL.md says the LLM reasons from the transcript. Take selection is Claude
reading `takes_packed.md`, which is what "build our own" would also be. The real choice
was adopt its infrastructure vs rewrite it, and its `render.py` already implements the
exact finish chain we need: per-segment extract → grade → **30 ms audio fades** →
lossless concat → **two-pass loudnorm to −14 LUFS** → subtitle compositing, plus HDR
tonemapping and portrait handling.

Installed at `~/Developer/video-use`, symlinked into `~/.claude/skills/video-use`.

**Install facts that contradict its own README:**
- **Python 3.10+ is NOT required.** All six helpers carry `from __future__ import
  annotations` and run on the system **Python 3.9.6**. `uv` is not needed.
- Only `requests`/`numpy`/`PIL` are needed. `librosa`+`matplotlib` are used **only** by
  the optional `timeline_view.py` waveform view — skip them.

**Selects and ButterCut were NOT adopted.** Both need a desktop-app install plus account
creation, and both export **Premiere/FCP/Resolve timelines** — the timeline-handoff model
Dan's plan explicitly rejects. Do not revisit without new evidence.

**Segment cache — FIXED 2026-08-19** in `~/Developer/video-use/helpers/render.py`:
each segment is keyed on `sha1(source|start|end|grade|mode)` and the hash is in the
FILENAME (not the range index), so inserting or deleting one beat re-extracts only
that beat. Extraction writes to a `.tmp.mp4` and renames on success, so an interrupted
run can never leave a truncated file the cache would trust. Verified: a two-range EDL
rendered, one beat edited, re-render printed `[cached]` for the untouched beat and
`segment cache: 1/2 reused`. Production-proven on the 8/19 invest-health revision:
**97/98 segments reused, one merged beat re-extracted — minutes instead of an hour.**
Note `clips_*` dirs accumulate stale hashed segments across revisions — harmless;
delete the dir to reclaim space after delivery.

`render.py` also now honors an optional **`"fps"` field in the EDL** (string, ratios
allowed — `"30000/1001"`). It used to hardcode `-r 24`, which silently retimed 29.97p
Sony footage; set the EDL fps to the source rate for talking-head longform. Default
stays 24 when the field is absent.

---

## Step 5 — the screen recording: split screen, not PiP

A phone screen recording is ~1320×2868. The video is 1920×1080. **Scaled to full frame
height the phone is only ~500 px = 26% of the width** — it can never fill a horizontal
frame, so something must occupy the other 74%.

**Locked layout (Dan chose it from three built mockups): phone left at native size,
Dan cropped to fill the right.** Nothing is upscaled.

```
screen: crop=1320:2500:0:175, scale=570:1080     # removes iOS status bar AND Safari
camera: crop=1350:1080:375:0                     # 570 + 1350 = 1920 exactly
        hstack
```

The `crop=…:175` is load-bearing: it strips the status bar and the `absbyai.com` address
bar so the demo reads as an **app**, not a website. The camera x-offset 375 keeps Dan
centered because he is framed center-right — re-check per shoot.

Rejected and not to be re-proposed: **true PiP** (shrinks Dan to a box, 40% of frame is
blur) and **zooming into the phone** (huge text but dead space and a thumbnail-sized Dan).
Punching into the phone column is fine for a few seconds on a key number, not as a default.

### Syncing the screen recording

**Each beat pulls its OWN window from the screen recording.** Dan narrates at a different
pace than he tapped, so a single global offset drifts badly. Per-beat windows jump-cut
between actions, which reads as normal tutorial editing. See `BEATS` in
`reference/build_graded.py` — a 4-tuple of `(beat, cam_start, cam_end, screen_start)`.

**Build the event index first:** sample the screen recording every ~8 s into contact
sheets and note when each action happens. Scene detection is useless here — scrolling
produced **441 false hits** on a 320 s recording.

**QC the sync by comparing frames against WHAT HE IS SAYING at that instant.** Duration
and loudness assertions cannot catch a sync error. This caught two real misses:
the itemized-results beat showed the top of the list while he said *"683 total calories
per salad"* (screen start moved 205 → 214.5), and the clarifying-questions beat had the
answer taps landing ~22 s after he narrated them (168 → 183).

**Watch for bloopers in the screen recording** — the 8/3 take had an accidental iOS
"Undo Typing" dialog at ~248 s. Route around it.

**Picking between multiple screen-recording takes: match the NUMBERS in the narration.**
Dan's take 1 showed 711 cal, take 2 showed 683, and he says "683" on camera. Also match
the on-screen answers to the answers he speaks aloud.

---

## Step 6 — color: analyze, don't eyeball

Use `color-grade-ai` (github.com/isaacrowntree/color-grade-ai). **Its analysis path
`auto_grade.py` needs only numpy and runs on Python 3.9. Ruby 2.7+ is NOT required**
(this Mac has 2.6.10) — the `.rb` scripts are LUT bakers and Resolve exporters we don't
use, because we apply the grade as an ffmpeg filter chain in our own render.

**NEVER diagnose white balance from a whole-frame channel average.** Doing that on the
8/3 footage gave "R/B 1.39, strong warm cast" and led to a wrong prescription. A warm
*scene* — wood cabinets, travertine, terracotta — is not a warm *cast*. The robust
Shades-of-Gray estimator put the real WB deviation at **0.015**, and the best in-frame
neutral (a stainless microwave) read 1.14–1.20.

Sample **8+ frames across the whole video** (`reference/parse_grade.py`) and grade the
medians. On 8/3 the real defects were consistent and were about **contrast, not colour**:
black point **0.060** (milky/lifted) and median luminance **0.388** (dark). Lifted blacks
plus dark mids is what reads as "washed out."

The shipped grade:

```
colorchannelmixer=rr=0.984:gg=1.000:bb=1.017,
curves=all='0/0 0.050/0.004 0.25/0.27 0.50/0.565 0.80/0.855 1/1'
```

**Validate closed-loop: re-run the analyser on the graded frames.** Black point
0.060 → 0.009, milky blacks YES → NO, and — the thing grades usually ruin — **skin hue
moved TOWARD the 20° target** (19.5→20.6, 19.6→19.9, 18.8→19.4). Saturation untouched.

**GRADE PER ROLL, NOT PER SHOOT.** Three rolls shot the same night in the same doorway
had black points **0.079 / 0.069 / 0.054** and median luminance 0.244 / 0.225 / 0.308.
One grade for the shoot would have crushed one roll and left another milky. Anchor the
curve's crush point on *that roll's* measured black point:

```
curves=all='0/0 <black_point>/0.006 0.25/0.262 0.50/0.552 0.80/0.862 1/1'
```

Measured closed-loop on all three (8 frames each): black point → 0.004–0.008,
**milky blacks YES → no on every frame**, highlight clip ≤ 0.3 %, skin hue held or moved
toward the 20° target, colorfulness lifted into the plausible 25–95 band.

**A WARM SUBJECT IS NOT A WARM CAST — and on a spray-tan video the warmth IS the product.**
C1512's WB deviation read 0.051, triple the other two rolls. That was Dan's fresh spray
tan, the literal subject of the video. Correcting it would have graded away the thing the
viewer is there to judge. **Never apply a white-balance correction to a video whose
subject is skin tone**; check the skin-tone node first (it read "skin natural, 21.7°"),
and fix contrast only. The black crush alone pulled WB deviation 0.0425 → 0.0344 anyway.

**A BRIGHT OUTDOOR ROLL NEEDS THE OPPOSITE CURVE FROM A DARK INTERIOR — read the numbers, do not
reuse the 8/3 curve.** The 8/14 pool footage measured black point **0.104–0.112** (much milkier
than 8/3), median luminance **0.52–0.55** (already at target, NOT dark) and **highlight clip
already 6.2 %**. The 8/3 curve lifts mids (0.50→0.552) and highlights (0.80→0.862), which here
would blow out an already-clipping sky for no gain. What shipped crushes the blacks and holds
everything else near identity:

```
curves=all='0/0 <black_point>/0.005 0.30/0.294 0.55/0.550 0.85/0.848 1/1'
```

Closed-loop: black point 0.108 → 0.006, **milky blacks YES → no on all 8 frames**, median
luminance 0.548 → 0.549 (unmoved), highlight clip +0.15 pp, skin hue held, colorfulness 36.9 → 37.8.

**GRADE THE CAMERA SIDE ONLY.** The screen recording is a digital capture and is already
neutral (**R/B 0.958**); running a warm-correction over it tints the app UI blue and
misrepresents the product. Verified: screen half 0.953 → 0.951 (untouched) while the
camera half's black point went 14.0 → 0.7. Apply per-segment during extraction, never
post-concat.

---

## Step 7 — graphics: the J2 system, reused not reinvented

Constants are lifted **verbatim** from `.claude/skills/shorts/reference/band/assets.py`
into `reference/build_gfx.py`: `BG=(13,14,11)`, `OLIVE=(140,152,88)`, Impact headlines,
Copperplate letter-spaced eyebrows, the `spaced()` tracking helper. Do not redesign.

For longform: **lower-third chips**, roughly one per major step (8 on a 3:48 video),
0.35 s alpha fade in/out, plus a persistent `AbsByAI.com` watermark for rip protection.
Time any number callout to the word — the `683 CALORIES` chip runs 176.0–182.4 s because
he says it at 176.6.

**Dan's rule "No static intro title cards" applies to longform too.** Open on his face;
brand with a lower-third chip a couple of seconds in.

**Two traps, both caught only by compositing a chip onto a REAL frame before rendering —
do this every time:**
1. **Copperplate is a SMALL-CAPS face.** `AbsByAI.com` rendered as `ABSBYAI.COM`,
   violating the J2 rule *"camel case … Never all-caps."* **Use Manrope**
   (`~/Library/Fonts/Manrope.ttf`) for the watermark. Copperplate stays correct for
   eyebrows, which are all-caps by design — the bug only affects lowercase.
2. **Olive eyebrow text is illegible over bright footage.** In `/shorts` it sits on the
   dark J2 background; over granite and glass it vanished. Give each eyebrow its own
   `BG@225` dark bar.

Graphics are **one overlay pass over the finished cut at CRF 18**, not baked per-segment —
chips span beat boundaries. One extra encode generation, deliberately accepted.

**NEVER split a range just to hang a chip.** Chips are placed by SOURCE time and mapped
through the EDL, so a single range carries as many chips as you like. Splitting one anyway
removes ~0.02 s of source and leaves render.py's 30 ms fade-out immediately followed by its
30 ms fade-in **in the middle of continuous speech** — the only genuine audio defect this
batch produced, and the one join that legitimately failed QC. Assert it away: any adjacent
pair whose gap is < 0.20 s should be merged into one range.

---

## Step 8 — subtitles: SRT, not burned in

**Longform gets an uploaded `.srt`; it does NOT get burned captions.** This is a
desktop/TV tutorial and burned captions fight the app UI occupying the left 570 px.
The `/shorts` burned-ASS caption spec does **not** apply here.

**Subtitles must be timed to the FINAL EDIT.** Source timestamps are meaningless after
cutting — on 8/3, 114 of 882 words no longer existed and every survivor had shifted.
`reference/make_srt.py` maps each word through the EDL:

```
render_t = beat_offset + (word_t − beat_start)
```

accumulating offsets from the **same 3-dp-rounded durations the build used**, so it
cannot drift, and dropping any word outside a kept beat.

**Validate by transcribing the FINISHED video and comparing the SRT against its own
audio** — 82/82 cues aligned on 8/3. **Never validate against the source transcript;
that only proves the mapping matches itself.**

**Never `" ".join()` Whisper tokens.** Whisper splits `y'all` into `["y", "'all"]` and
`0.8` into `["0", ".8"]`, so a naive join renders **"What do y 'all guys think?"** and
**"0 .8 grams per pound"** in the finished captions. Suppress the space before any token
opening with `'`, `.`, `,`, `%`, `)` or `-`.

**Close a cue BEFORE appending a word that would overrun the character cap**, and wrap on
the word boundary nearest the MIDPOINT. Checking the cap after appending lets a cue run a
whole word past it, and a greedy first-line fill leaves the second line uncapped — that
combination produced 65-character lines. Closing early + balanced wrap took the worst line
from 65 → 48 chars with zero 3-line cues.

Format: max 2 lines, ≤45 chars/line, break on measured pauses ≥0.45 s, sentence ends, or
5.5 s; min 0.5 s per cue; no overlaps. **Extend the final cue to the true container
duration** — summed rounded beat durations come up fractionally short and clip the last
line (228.32 vs 228.648 on 8/3).

Upload in YouTube Studio: Subtitles → Add → **Upload file → With timing**. Never
"Without timing" — that discards our timings and lets YouTube re-sync.

---

## Step 9 — QC, automated

Port the `/shorts` assertion suite and add:

- **Splice discontinuity** — max sample-to-sample jump at each join vs controls elsewhere
  in the same file. 8/3 scored 1.09–1.20× the control median. **Never compare loudness
  either side of a join** — the cut is deliberately in silence and speech follows, so it
  always false-alarms.
  **Normalise against the control DISTRIBUTION, not its median.** On the 30-minute Zepbound
  cut the controls spanned p50 = 613 … p90 = 2455 … max = 4069, so a join landing beside a
  loud syllable scored 6.4× the *median* while being completely ordinary for the file.
  A "> 3× median" rule reported **4 failures; re-transcribing all four from the finished
  render showed clean, continuous speech at every one.** Allow ~1.25× headroom over the
  ceiling too — one sample beating the max of 120 controls by 14 % is chance, not a pop. Fail a join only when its jump
  exceeds the file's own natural ceiling (the control max), and keep reporting the
  ×median figure so it stays comparable with the 8/3 baseline. This is the same lesson as
  the circular cut-cleanliness metric — the metric was wrong, not the media.
- **Loudness** — measured integrated LUFS within ±1 of −14. **When the SOURCE audio clips,
  render.py's own loudnorm will undershoot** — the 8/14 rolls peak at **+2.94 dBTP in camera**, so
  the −1 dBTP ceiling dragged the programme to −15.09 LUFS. Fix with a corrective measured-value
  pass on the finished cut (`-c:v copy`, audio only), feeding back the measured I/TP/LRA/thresh and
  `linear=true`; that landed −14.59 LUFS / +0.54 dBTP, better than the render on both axes.
  **Do not chase −1 dBTP with `alimiter`** — measured on this cut, every dB of true-peak control
  cost a dB of loudness (limit 0.79 → −15.08 LUFS, 0.63 → −16.25), because the clipping is baked
  into the recording. Hit the loudness target, report the true peak, and tell the shooter to drop
  the mic gain.
- **Duration vs plan.**
- **Sync spot-checks** — frames vs what he is saying. The only check that catches sync.
- **Graphics on/off** — sample mid-chip AND between chips to prove `enable=between()`
  windows actually close. **Assert a clear separation in EITHER direction, never that
  "chip == brighter".** A J2 chip is a dark box: on the doorway videos it raised the
  region's mean luminance (white Impact on near-black, 61→83 vs 35 between chips), but on
  the supplements video — a bright granite counter — it *lowered* it (107→115 vs 123). A
  `max(off) < min(on)` test reported a false failure on a video whose chips were rendering
  perfectly.
- **No artificial mid-speech splits** — assert no two adjacent ranges are closer than
  0.20 s. **Guard this on `source` when the video is cut from several rolls**: across a roll change
  the arithmetic is meaningless and reports gaps like −72 s as "artificial splits" (it did, three
  times, on the ab-wheel cut). This is the one defect the splice metric structurally cannot see: render.py's
  30 ms fades produce a brief amplitude *dip*, and max-sample-to-sample-jump only detects a
  *step*. The builder now flags it too.

**When a QC metric fails, verify the METRIC before "fixing" the media.** This has now
paid for itself repeatedly: the word-presence check produced two false clip reports on
8/3 (Whisper re-transcribed "proteins"→"protein" and "set"→"saved" — the audio was fine),
and the circular cut-cleanliness metric in Step 3 reported the exact opposite of the truth.

---

## ffmpeg traps paid for in this pipeline

- **`drawtext` is broken in the static build** (`Fontconfig error: Cannot load default
  config file`) — it silently produces empty text even with `textfile=`. Burn text with
  **PIL into a PNG** and `overlay` it. That is what `reference/build_gfx.py` does.
- **Overlay fades need a timeline shift.** A `-loop 1` PNG starts at t=0 while the main
  video is at T0: `format=rgba,fade=…:alpha=1,setpts=PTS+T0/TB` then
  `overlay=…:enable='between(t,T0,T1)'`.
- **`silencedetect` parsing:** `sed 's/.*silence_/silence_/'` is greedy and turns
  `silence_end: … | silence_duration: …` into `silence_duration`. Regex the raw output.
- **`volumedetect` logs at info level** — `-v error` suppresses `mean_volume` entirely.
- **zsh eats `$VAR:l`** as a case modifier. Use `${VAR}:linear=true` in loudnorm args.
- **Python 3.9 f-strings cannot contain backslashes** — write regex parsers as files.
- All the `/shorts` traps still apply: `-loop 1` stills are infinite (need `-t` +
  `shortest=1`) and default 25 fps (pin `-framerate`/`-r`); `overlay` adopts its first
  input's rate; `execFileSync` loses ffmpeg's stderr.

---

## Delivery

Keep **every stage** as its own file so any single stage can be A/B'd or rolled back:

```
roughcuts/
  A_<engine>.mp4              rough cut, camera only
  SPLITSCREEN_v1.mp4          + screen recording
  SPLITSCREEN_v2_graded.mp4   + color
  SPLITSCREEN_v3_graphics.mp4 + J2 graphics      <- the deliverable
  SPLITSCREEN_v3_graphics.srt subtitles
  edl_*.json, ground_truth.json, *.py            the recipes
```

Media stays out of git — **run `git check-ignore -v` on the output folder before staging
anything.** Copy any new script into this skill's `reference/`.

**Work on the external drive, not the boot disk.** The 8/3 shoot is 118 GB and the finished
files run 0.8–1.8 GB each; the invest-health session left 41 GB of intermediates (including
a 27.5 GB duplicate of the source roll) on the internal disk, which is now 99 % full.
Point every working directory at the Seagate and only the ~50 KB of recipe files come back.

**Ship the recipe next to the video.** Each delivered folder carries `FINAL_*.mp4`,
`FINAL_*.srt`, the pre-graphics `CUT_v1_graded.mp4` as a rollback point, plus `edl.json`,
`ranges.py` and `chips.py`. With the segment cache working, those three text files are all
a revision needs.

Then `/youtube-packaging` for title, description, chapters and thumbnail.

---

## Judgement calls Dan has endorsed

- **Split screen over PiP** for a vertical screen recording in a horizontal video.
- **SRT over burned-in captions** for longform.
- **No static intro title cards** — open on his face.
- **Rough cut A (word-boundary cuts)** over the silence-snapped alternative.
- The **`®` is not used** on YouTube titles or channel metadata.

## Production notes for the shoot

- **Shoot 4K.** The 8/3 shoot was 1920×1080, so there is **no headroom to punch in or
  reframe** — any crop softens. Recommended to Jeff: **XAVC S-I 4K, 3840×2160, 29.97p,
  10-bit 4:2:2, S-Cinetone, LPCM** — same All-Intra format he already shoots, just bigger.
  All-Intra matters for us specifically because we extract ~20 short segments at arbitrary
  timecodes and Long-GOP has to decode back to a keyframe every time. Cost: ~2 GB/min vs
  ~400 MB now. Fallback if storage binds: XAVC HS 4K 10-bit 4:2:2 200 Mbps (H.265).
- **Keep S-Cinetone, not S-Log3** — it graded cleanly and needs no conversion LUT.
- **Shoot 2 seconds of a grey card at the head of each lighting setup.** Its absence is
  why white balance had to be inferred from a microwave door, and why it was misdiagnosed
  the first time.
