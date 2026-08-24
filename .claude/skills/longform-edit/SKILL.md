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

**Proven again 2026-08-21 on the SPRAY-TAN REVISION — the first cut to get a full
clip-and-graphics pass.** 19:00 -> 18:53 with **95 inserts** (71 Pexels cutaways, 19 J2
cards, 5 before/after panels) on top of the existing 26 chips, so no gap exceeds 18.8 s;
10 % zoom cuts on every join not already hidden by a cutaway; three hallucinated
sentences removed from the SRT. **$0.00** — Pexels needs no key. That round added
Step 5.5 (cutaways and cards), the SRT de-clumping rule in Step 8, and lessons 22-27.

**REBUILT 2026-08-24 after the ab-wheel video was rejected.** Dan on the cut this skill
produced: *"substantially better than what we made — it looks better, it sounds better,
and the graphics are better."* **Seven of the nine techniques the outside editor used were
ALREADY IN THIS REPO, and the video passed 6/6 of the QC anyway.** `motionlib.py` and
`sfxlib.py` had been written in August for exactly this; Step 5.5's coverage rule and
Step 5.6's microphone check were already written down. They were skipped.

> **THE META-LESSON, and it is the reason this skill was restructured:**
> **a quality bar that exists only in prose will be skipped under time pressure.
> If it matters, it fails the build.**
> This is the third time a metric or a rule — not the media — has been the problem.

So every style rule is now **code that fails**, in `reference/qc_style.py`. Run it before
you deliver. It was calibrated on three cuts of the same footage, and it separates them:

| | the editor's 6:58 cut | this skill's rebuild | the cut Dan rejected |
|---|---|---|---|
| gate result | 6 pass / 5 fail\* | **13 pass / 0 fail** | **5 pass / 7 fail** |
| visual changes | 68 (9.8/min) | 109 (15.1/min) | 19 (2.1/min) |
| longest static stretch | 41.3 s | 12.7 s | 79.2 s |
| cutaway coverage | 65% | 58% | 9% |
| voice centred (L/R) | +0.993 | +0.9996 | −0.002 |
| pace | 189 wpm | 188 wpm | 151 wpm |

\* his file is a 854x480 review copy, quieter than target and 0.31 dBTP over — and his
cut breaches Dan's own 30-second rule once, at 5:37. The gate is not "be like him"; it is
the floor below which a cut is not finished.

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

## Step 0.4 — CHECK THE MICROPHONES BEFORE ANYTHING ELSE

**Jeff's rolls are not stereo. They carry two different microphones**, and using both is
the single worst-sounding thing we have shipped. Verified on the 8/14 ad roll (C1591) and
the 8/3 longform rolls (C1512/C1513/C1514):

* The **right** channel is a close lav. The **left** is a mic ~2.6–2.7 m away.
* The same voice appears in both, **7.4–7.9 ms apart**. On the 8/14 ad roll the two are
  also **polarity inverted** (cross-correlation −0.77 rather than +0.7).
* Carrying both puts a dry voice in one ear and a roomy, delayed copy in the other, and
  collapses to a hard comb filter on any mono speaker. **It is heard as echo, and no EQ
  will fix it.** On the 8/14 roll the left channel is additionally clipped in 24,368
  samples; the right has zero.

**So: take the right channel, as mono.**

    -af "pan=mono|c0=c1"

Confirm it per roll rather than assuming, because the wiring can change between shoots:

    ffmpeg -ss 120 -t 15 -i ROLL.MP4 -af "pan=mono|c0=c0" -ar 48000 -c:a pcm_s16le L.wav
    ffmpeg -ss 120 -t 15 -i ROLL.MP4 -af "pan=mono|c0=c1" -ar 48000 -c:a pcm_s16le R.wav
    # cross-correlate with a +/-20 ms lag search: a strong peak at a non-zero lag means
    # two mics. The channel that arrives EARLIER, decays FASTER after each word, and has
    # the LOWER noise floor is the lav -- that is the one to keep.

The three delivered 8/3 longforms were all cut carrying both mics. Re-rendering any of
them is one filter change.

**Flag to Jeff before the next shoot:** the far mic is opposite polarity on at least one
roll, and the left input has been recorded hot enough to clip. Fix the polarity or drop
the second mic, and lower the gain.

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

## Step 2.5 — THE STYLE PASS IS NOT OPTIONAL. Read this before you cut.

These used to sit at Steps 5.5–8, which is where a session runs out of room, and that is
exactly why they got skipped on the ab-wheel video. **Every one of them is a hard failure
in `reference/qc_style.py`.** Plan for them now, not after the cut is locked.

| # | requirement | gate | where |
|---|---|---|---|
| 1 | **Right microphone only.** Check the channels before you touch tone. | channel SNR ≥ 10 dB **and** L/R correlation ≥ +0.90 | Step 5.6 |
| 2 | **Pace.** Remove dead air; cuts must land BETWEEN two spoken words. | ≥ 170 wpm, dead air ≤ 25% | Step 3 |
| 3 | **Punch-ins.** A locked wide shot for nine minutes scene-detects as one cut. | ≥ 4 visual changes/min | Step 5.4 |
| 4 | **Coverage.** No long stretch of the same unbroken shot. | ≥ 40% coverage, longest static stretch ≤ 30 s | Step 5.5 |
| 5 | **Animated graphics**, not static PNG chips. | (visual-change and coverage gates) | Step 7 |
| 6 | **Music bed**, licensed and ducked. | 2nd-percentile frame level ≥ −52 dBFS | Step 7 |
| 7 | **Captions**, burned, on talking-head content. | present on ≥ 45% of sampled frames | Step 8 |
| 8 | **Loudness and peak.** | −14 LUFS ±1, true peak ≤ −0.5 dBTP | Step 7.6 |

**The gate measures the FINISHED FILE, not your build plan.** A `spec.py` can claim thirty
cutaways; only the file proves it. That is deliberate — the old QC read `chip_timings.json`
and would happily certify a plan that never made it to the picture.

```bash
python3 reference/qc_style.py FINAL.mp4 --plan plan.json --srt captions.srt --talking-head
```

### The three failures this gate exists to catch

1. **A dead or duplicated microphone.** Two separate shoots shipped with it (8/3: two mics
   hard-panned 7.5 ms apart; 8/14: the left input dead, SNR 0.6–1.4 dB). Both were
   inaudible to a QC that only measured LUFS. Both reached Dan.
2. **One locked shot for the whole runtime.** 2.1 visual changes per minute against the
   reference cut's 9.8.
3. **A plan that was written and then not built.** Steps 5.5 and 5.6 were correct, written
   down, and skipped.

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

## Junk-footage detection — run ALL of these before calling a cut done

Dan reviewed two rounds of the 8/19 invest-health cut and found junk both times.
The giveaways he listed: looking away from camera, immediately repeating the previous
take's line, adjusting glasses, >1 s pause then repeating, drinking, burping, drifting
off-center. Lessons that became mandatory passes:

1. **Pause-capper** — tighten every hold ≥1.3 s inside kept ranges to ~0.5 s
   (keep 0.30 s tail + 0.20 s lead-in). Use THREE detectors together, because each
   misses cases: `silencedetect -32dB` (defeated by kitchen room tone), word-timestamp
   gaps ≥1.5 s, and **stretched words ≥1.5 s** (Whisper folds the pause INTO a word —
   keep 0.65 s for the spoken word, cut the rest). Auto cuts must never merge across a
   hand-placed EXTRA_SPLIT — a merged cut swallowed a retake once.
2. **Re-transcribe every stretched-word region FROM SOURCE AUDIO** before cutting near
   it. A 4 s "word" at 527 s turned out to contain an entire aborted take ("deal with
   if you don't kee—") followed by its retake — invisible in the full-roll transcript.
3. **Phrase-level repeat scan, not sentence-level.** Sentence-fuzzy-matching found no
   repeats while Dan found several: "all kinds of problems" twice in 8 s, a doubled
   Oura-ring introduction. Scan for repeated 3-5-word shingles within a ±30 s window
   across the KEPT timeline and inspect each hit; his rhetorical repeats (anaphora)
   are deliberate, re-INTRODUCTIONS of the same item are junk.
4. **Visual junk pass**: 1 fps contact sheets around every joint and every capped
   pause — look for off-center framing, look-aways, glasses adjustments. The 14:30
   junk (off-center recomposure while already talking) had NO audio signature.
5. **Zoom cuts must be ≥10%.** A 6% alternating punch-in still read as a jump cut to
   Dan wherever his posture shifted between takes. Anchor the crop top (y=0) — his
   head sits ~10 px from the frame edge at this framing.
6. Shell hygiene that burned an hour: piping the EDL builder through `grep` swallowed
   its traceback and a **stale edl.json rode through a full re-render**. Run builders
   bare with `set -e`, and verify the changed range values in edl.json before
   rendering.
7. **Cut the whole repeated SENTENCE, not the aborted take inside it.** v2 cut only the
   flub out of "There's all kinds of problems that you have to deal with [abort] if you
   don't take care of your health." — and Dan flagged it again, because the *sentence*
   restates "all kinds of problems" from 6 s earlier. When a phrase-repeat hit is a
   restatement, the fix is to delete the restatement, not to clean up its delivery.
8. **A cut point Whisper says is impossible may still exist — measure the envelope.**
   Dropping "if you're middle class." meant cutting between "in" and "if", and Whisper
   had them butted at 3058.20/3058.21 with no gap. A 20 ms RMS profile (`-45 dB` floor)
   showed a real 0.12 s trough at 3058.13–3058.25: speech ends, then "if" starts at
   −27 dB. `silencedetect` never reports a gap that short. Profile the region before
   concluding a word can't be dropped.
9. **The SRT must drop words that STRADDLE a new cut, or the caption shows deleted
   speech.** `to_render()`'s ±0.02 s tolerance mapped the first word of a deleted
   sentence ("Your" from "Your three options are…") and the last word before a deletion
   ("if"), so the captions read text that is no longer in the audio. Map a word only
   when its **midpoint** is strictly inside a kept range.
10. **Never ship a political term Whisper invented.** It renders "GLP-1" as "GOP"
   throughout. Keep a brand/drug fix table in `make_srt.py` applied to the JOINED cue
   text (so multi-token names like "Aura ring" → "Oura Ring" are caught) and assert the
   forbidden strings are absent from the written SRT before the run exits.
11. **The <0.20 s "artificial mid-speech split" test is a PROXY — measure the notch
   before re-rendering.** It flagged two joins on v3. A 2 ms RMS envelope put their
   notches at 14.0 and 19.6 dB below the local median, against a 50-sample control
   distribution of p50 **18.6** / p90 **35.9** dB at ordinary non-join points — i.e. both
   joins were quieter-than-average dips, and re-transcribing them returned clean
   continuous speech. Fail on a **measured notch above the file's own p90**, and use
   **≥40 controls**: at N=6 the ceiling swung from 18.4 to 165.9 dB between seeds and
   produced a false failure. Same lesson as the splice metric — verify the metric first.
12. **Third-party b-roll: expect only 360p from YouTube.** Every DASH format for the
   Bryan Johnson clip 403'd at ~8 % of the download across every client and chunk size;
   only the `android` progressive 640×360 completed. Size the insert to the source
   (600×338 window, a slight DOWNscale) instead of blowing a soft 360p frame up to a
   large PiP. `composite.py` grew a `video_pip` overlay kind (placed at x,y instead of
   0:0) plus a separate full-frame PNG carrying the olive frame and the persistent
   "Bryan Johnson / YouTube" attribution.

## Cut-downs: deriving a shorter variant from an APPROVED edit

Proven 2026-08-21 on the invest-health video: **53:15 approved → 43:31 conservative +
28:25 sub-30**, ~260 new cut points, one render each, $0.00. Scripts are
`reference/cutdown_*.py`; `cutdown_cutlib.py` is the engine.

13. **Subtract intervals from the approved `edl.json`. Never re-derive the cut.** The
   variant builder loads the shipped EDL, subtracts resolved deletion spans, drops any
   leftover sliver under ~0.6 s, and re-applies zoom parity. Every approved decision —
   ranges, pause-capper, EXTRA_SPLITS, out-overrides, grade, `fps` — rides through
   untouched, and the diff you review is only what the variant removes.
14. **Resolve prev/next against KEPT words only.** A deletion that swallows a whole
   approved range sits next to source words that were ALREADY cut; using the raw word
   list picks a join Dan will never hear, and makes non-overlapping deletions look like
   they collide. Merge deletions that resolve into each other and re-resolve the union.
15. **Snap every edge to a SENTENCE boundary, not just to silence.** Dan speaks
   continuously — on this roll 49 of 180 first-pass edges had no measured pause at ANY
   threshold within the search window. Scoring sentence-end far above pause-present
   (6 vs 2) and searching ±8 kept words fixed both problems at once: a cut-down reads
   as writing rather than as an edit, AND the edge lands in real silence. Cap the shift
   per cut (`snap=(head, tail)`) for the few cuts that must stay word-exact.
16. **The snapper will happily produce a grammatical wreck — read every join.** Printing
   9 kept words either side of each join surfaced ~30 broken joins out of ~260 that all
   automated checks passed: orphaned "I'm not.", a dangling "But even if…", "such as
   rent. I'm ]|[ I'm talking about…". There is no metric for this. Read them.
17. **Protect chip anchors by ASSERTION, not by interval overlap.** "This cut interval
   overlaps the chip's 6.4 s window" false-alarms every time a cut merely ends where a
   chip's sentence begins. Assert instead that each chip's source time still falls
   inside a kept range of the finished EDL — exact, and it correctly reported the ONE
   chip legitimately dropped with its section.
18. **A cut-down's targets collide with the never-cut list — say so, don't quietly
   obey one.** The sub-30 beat map asked for 45 s of the restaurants section whose
   AbsByAI plug alone is 43 s, and 50 s of a 64 s outro marked "conversion, light touch".
   Both targets were computed without the protection. Keep the protected material,
   land over target, and flag the contradiction.
19. **`silencedetect` at −45 dB is not a fallback — the room tone is often above it.**
   At three suspected clipped fricatives on this roll, −45 dB reported no silence at
   all. Build the whole-roll −45 dB map anyway (one pass, seconds) to PLACE edges where
   it does see a trough, but expect to fall back to a 10 ms RMS envelope.

### Revision lessons (spray-tan rev 1, 2026-08-21)

22. **A per-range `vf` that changes PIXEL FORMAT changes the whole frame, not just
   your box.** The deodorant fix as `format=gbrp,geq,format=yuv420p` was measured
   end-to-end against an identical render without it: **~560,000 pixels changed
   OUTSIDE the box, max delta 199.** That is the yuv->rgb->yuv chroma round trip, and
   it would have made six beats visibly different from the other 38. Two fixes,
   both needed: apply the effect as an **alpha-masked patch** (`split`, `crop` to the
   region, compute `a='255*W'`, `overlay`) so every pixel with W=0 passes through
   byte for byte; and **pin `format=yuv420p` at the end of the grade for EVERY
   range**, so the patched ranges and the plain ones take the identical scaler path.
   With both, the measured change outside the box is exactly **0**.
23. **Never A/B a filter through a lossy encode.** Comparing two CRF-20 encodes showed
   1.3M changed pixels outside the box — x264's rate allocation is global, so a
   19k-pixel edit in one corner changes every macroblock in the frame. Encode both
   sides with `-c:v ffv1` and the same difference reads 0. This wasted two cycles.
   Equally: a PNG dumped mid-chain measures the PNG conversion, not the edit.
24. **A colour-keyed fix needs a box, and a box needs the subject to hold still.**
   The residue key (sat<0.45, val<0.62) separates residue from skin and hair
   perfectly *inside an armpit*, and fires happily on doorway wood (sat 0.19), the
   wall (sat 0.42) and a shadowed white fridge (val 0.55-0.62) outside one. On a
   talking head the armpit is on screen for well under a second at a time: a static
   box over 2-3 s lands on the tank top or the palm and does nothing, and a box
   generous enough for the whole gesture paints a grey smudge on the background —
   worse than the blemish. **Ship it only on windows <=0.8 s with a tight box, and
   verify every one.** Say plainly which moments you did not fix.
25. **Use the filter as a filter, not as a locator.** Scoring the key's mass over a
   wide band to FIND the blemish reported 1043 of 1140 frames as hits. What actually
   located the shots was an unrelated, cheap signal — bare forearm skin reaching the
   outer thirds of the frame, 0.199-0.223 arms-spread against 0.010-0.011 arms-down,
   a 20x gap. **Then extract those frames and look at them**: half the "left armpit"
   detections were the white door frame.
26. **Zoom-cut parity should skip joins a cutaway already hides.** Walk the ranges
   keeping a zoom state; flip it at each join UNLESS a full-frame insert spans that
   join, in which case both sides keep the same framing. On this cut 35 joins flipped
   and 8 were left alone. A zoom nobody can see is a wasted flip. Cards do not count
   as cover — they are side panels and the cut is fully visible beside them.
27. **Changing the grade string blows the whole segment cache.** The grade is in the
   cache key, so pinning `format=yuv420p` onto it re-extracted all 44 segments
   (0 cached). That is the correct trade here, but know the cost before you touch the
   grade in a revision: a cut-only change reuses everything, a grade change reuses
   nothing.

28. **Recasting stock is a one-line-per-slot edit if the insert list is a data file.**
   Dan reviewed rev 1 and asked for stock cast to the target demographic. Because
   `inserts.py` maps each slot to `(pexels_file, seek)`, recasting 12 clips meant
   repointing 12 entries, re-running `build_inserts.py` for those keys only, and
   re-running the two composite passes. The cut, the EDL, the SRT and the chapters
   never moved. **Build a contact sheet of the RENDERED inserts to audit casting** —
   the source thumbnails on a search page do not tell you what the framed 16:9 crop
   actually shows.
29. **`pgrep -f <script>` matches the watcher's own shell.** Two "wait until the
   render finishes" loops deadlocked because each one's own command line contained
   the pattern it was grepping for. Match on `python3 <script>`, or watch the output
   file for a completion marker instead.

### The clipped-word check needs a control set, or it lies

**Word-presence on a joint re-transcription is not evidence.** On this pair of cut-downs
it flagged 9 joints — goals→goal, tracker→track, injections→injection, proteins→protein,
thighs→thigh. Every single one was intact. Whisper re-spells the last word of a phrase
whenever the phrase AFTER it changed, which is exactly what a cut-down does to every
joint. (The skill already recorded `proteins→protein` as a false positive on 8/3; it
recurs at scale here.)

**What actually decides it** (`reference/cutdown_tailtest.py`, folded into
`cutdown_final_gate.py`):
1. **Correct for render drift first.** Per-segment frame rounding at 29.97 accumulates —
   ~1.1 s by mid-file on a 163-range cut, ~2.9 s total on a 167-range one. A window at the
   planned out-time compares the wrong audio entirely. Cross-correlate the render's
   envelope against the source envelope leading into the cut to find the true offset.
2. **Compare the last 150 ms** of the render against the source, gain-aligned.
3. **Score against joints INHERITED from the approved edit, in the SAME file** — same
   encoder, same loudnorm, same 30 ms fade. Control band here: −3.8…−56 dB, median −8.
   All 9 flagged joints measured −2.5…−13.2 dB, i.e. inside it. The dip is render.py's
   deliberate 30 ms fade, present at every joint Dan already signed off.
Fail only below the control floor. **Same lesson as the splice metric, the notch metric
and the circular cut-cleanliness metric — the metric was wrong, not the media, five
times running now. Build the control set before you believe a failure.**

**The chips on/off test is a third instance.** A raw luminance comparison failed on both
variants; an olive-pixel test failed too, because the dark-olive door panel behind Dan
matches the J2 olive within any usable tolerance. What works is a difference of
differences (chip box minus a chip-free box in the SAME frame, on a chip-up frame vs a
chip-down frame) — and even that flips sign legitimately, because a J2 chip raises
luminance over the dark doorway and lowers it over a bright frame. **Write an on/off PNG
pair per chip and look at them.** Six checked visually here, including the two worst
scorers: all correct.

### Two SRT defects inherited from the approved edit

Both were shipped in v3 and only surfaced when a stricter gate was applied:
20. **`wrap()` was greedy, not midpoint-balanced** — it packed line 1 to the 45-char cap
   and left line 2 uncapped. Minimise the LONGER line instead.
21. **The cue cap is measured on RAW Whisper tokens, but the cue is written AFTER
   `fix_text()`, and every substitution LENGTHENS it** (GOP→GLP-1, Aura ring→Oura Ring,
   Set Down→Zepbound). Capping at the full 90 shipped 53-character lines. Cap at 84.
Together: worst line 53 → **46 chars, zero over 48, zero 3-line cues.**

---

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

## Step 5.4 — PUNCH-INS: a locked camera has to be cut into shots  **REQUIRED — gate: ≥ 4 visual changes/min**

The 8/14 ab-wheel shoot is one locked wide shot in which Dan occupies 18–56% of the frame
width. Delivered untouched it scene-detects as **one cut in nine minutes**. The outside
editor's cut of the same footage has 68. He did not have a second camera — he punched in.

**The system** (`reference/subject.py` + the framing half of `reference/plan_punchins.py`):

1. **Find the subject.** The camera is locked, so the per-pixel MEDIAN of the programme is
   a clean plate of the empty set. Anything far from the plate is Dan — except water and
   trees, which is why columns are scored rather than pixels, and why the row scan is
   restricted to the columns already claimed. Scoring the whole frame put every box's top
   edge on the roofline and shifted its centre ~5% right.
2. **Three crop levels: 1.00 / 0.86 / 0.74 of frame width**, centred on the tracked
   subject, never on the frame. **0.74 is the floor.** Measured on a torso crop, sharpness
   falls 124 → 64 → 34 going 1.00 → 0.86 → 0.74, and 0.62 both drops to 21 and cuts his
   feet off during rollouts.
3. **A SHOT spans several kept pieces.** Hold the exact crop across pause cuts. If the crop
   re-centres at every removed pause, every pause becomes a small unmotivated pan.
4. **Change framing at every join big enough to see, and every ~7 s regardless.** A pause
   removal under 0.5 s barely moves the body on a locked shot and needs no coverage;
   anything bigger does. The ~7 s cadence is the reference cut's own (68 changes / 418 s).
5. **Split long kept pieces purely to reframe.** Nothing is removed at those splits — the
   audio runs straight through — so they are pure punch-in cuts. Nudge each to the quietest
   40 ms inside ±0.9 s so it lands between words. Without this, framing can only change
   where a pause was removed, and the rebuild capped out at 3.1 changes/min instead of 7.4.
6. **Never crop through the subject.** Widen a level if the tracked box plus 10% margin
   does not fit. Assert it afterwards; the check found 38 pieces worth inspecting and all
   38 turned out to be the tracker's box including his shadow, not real clipping.

**Render per piece, not as one filter graph.** Referencing `[0:v]` 85 times makes ffmpeg
split the decoded stream 85 ways and buffer every branch until concat reaches it.

**Two rounding traps, both of which cost a re-render here:**
- `-t <duration>` emits `ceil()` frames on some pieces and `floor()` on others. 27 of 85
  came out one frame long and the audio finished 0.9 s behind the picture. Use
  **`-frames:v N`** with N computed from the frame duration.
- Do **not** cut the audio per piece either — that drifted 13 ms a piece the other way.
  Cut the whole voice track in ONE graph (85 `atrim`s off a single `asplit`, concatenated),
  using the same frame-snapped durations the picture got. Zero drift, by construction.

---

## Step 5.5 — cutaways and cards: breaking up a talking head  **REQUIRED — gate: ≥ 40% coverage, longest static stretch ≤ 30 s**

Dan's rule, given on the spray-tan revision: **"generally there shouldn't be more than
30 seconds without a clip or some kind of graphic… I'd rather have a little bit too much
and eliminate them than not enough."** On a 19-minute video that is ~40 inserts minimum.
What shipped was 95, covering 51 % of the running time, with the longest bare stretch at
18.8 s. `reference/verify_cover.py` asserts the rule and prints the longest gaps.

**Map the EXISTING chips first, then fill the gaps.** Chips count toward the rule and they
are already timed to the narration; starting from zero re-does that work and produces
collisions. `reference/plan_map.py` prints the output timeline, the chip windows, and
every gap with the transcript text inside it, so each insert can be chosen for the line it
illustrates rather than for a slot. `reference/out_transcript.py` gives sentence-level
output-time text for placing an insert on the word.

- **Pexels, no key.** `https://www.pexels.com/download/video/<ID>/` curls straight to the
  CDN at full resolution. The SEARCH pages are Cloudflare-gated and 403 to curl at any
  user-agent, and the internal `api/v3` endpoint wants a key — but a page loaded in the
  in-app browser can `fetch('/search/videos/<term>/')` **same-origin**, which returns the
  HTML with the cookies attached. One `javascript_tool` call sweeps a dozen search terms
  and returns slug+id for each; the slugs are descriptive enough to pick from. 70 clips,
  1.9 GB, $0.
- **Pre-render every insert to an exact-duration 1920x1080 MP4** (`build_inserts.py`)
  before compositing. The composite opens one decoder per insert; a 4-second file costs
  nothing to hold open, a 30-second 4K source does.
- **Vertical stock gets a blurred-fill background, not a centre-crop** — cropping 9:16 to
  16:9 cuts the subject's head off. Landscape gets cover-scale + centre-crop.
- **Alpha lives in the GRAPH, not on disk.** `format=rgba,fade=alpha=1` on the decoded
  clip gives the dissolve; storing 70 four-second inserts as ProRes 4444 would be 11 GB
  for a 0.15 s fade.
- **Two composite passes, not one.** Pass 1 = video cutaways (CRF 17), pass 2 = every PNG
  (cards, panels, chips, watermark, CRF 18). ~9 minutes each at this length. One extra
  encode generation, deliberately accepted, and it keeps the two input types separate.
- **Cards go viewer-LEFT and must clear the chip band.** x 44-610, top at y 168, bottom
  asserted above y 796. Then a card and a lower-third chip can share the screen. A phone
  screenshot inside a 610 px card is unreadable — give app cards the FULL frame instead,
  and place them where no chip is running.
- **A full-frame insert HIDES a chip.** Assert it: `composite_gfx.py` refuses to run if a
  chip window intersects a full-frame photo panel. On this pass the title chip had to move
  from source 138.0 to 147.4 to get out from under the item-1 panels.
- **Panels that hand over to each other must not cross-fade through the video.** Give the
  outgoing panel NO fade-out and start the incoming one 0.3 s early: it is later in the
  overlay chain, so it draws on top and the handover is clean. Fading both dips to the
  live footage for a third of a second.
- **Prune by deleting lines.** Keep the insert list as a data file (`inserts_spraytan.py`)
  with the line of narration each insert illustrates in a comment. Removing one is a
  one-line edit plus the two composite passes — the cut never re-renders.

---

## Step 5.6 — AUDIO: check the CHANNELS before you touch tone  **REQUIRED — gate: channel SNR ≥ 10 dB, L/R correlation ≥ +0.90**

**Run `reference/chan_analyse.py` on every new roll, before any EQ.** Two rolls from
this shoot turned out not to be stereo at all: they carry **two different microphones
hard-panned against each other** — a close lav one side, a mic a few metres away the
other. Measured on C1512 over 60 s:

```
peak cross-correlation +0.688 at lag -358 samples = -7.46 ms
zero-lag correlation   +0.071          <- a real stereo pair is near +1
channel           SNR      comb ripple (mono fold)
right (lav)      45.5 dB      0.53 dB
left  (far mic)  34.1 dB      0.49 dB
naive L+R sum    36.8 dB      0.69 dB   <- what shipped
```

**Every phone, laptop and TV speaker sums L+R**, and a 7.46 ms offset summed is a comb
filter with notches every ~134 Hz. **No EQ can undo it.** The ad roll from the other
shoot measured 7.83 ms with polarity ALSO inverted — same rig, same defect. The fix is
always the same: **take the better channel, as mono, then `pan=stereo|c0=c0|c1=c0`** so
the voice sits centred instead of in one ear. Verify: the delivered file should measure
correlation **+1.000 at lag 0**.

This shipped undetected in three delivered videos before anyone caught it, because
every automated check passed — LUFS, splice discontinuity and SRT overlap are all blind
to it. **The channel check is cheap; make it Step 0 of audio.**

### Fit the voice, don't copy a curve

`reference/fitvoice_longform.py` scores a candidate chain against a reference voice
over ten bands, averaged across five windows (one window over-fits), using only frames
above the 55th percentile of RMS so it measures SPEECH and not room tone. Copying the
ad roll's chain onto this roll would have made it worse: that curve cuts 320 Hz for a
chest bump, and this roll measured **9.4 dB LIGHT** at 80-150 Hz. Fitted: mean band
error **3.33 dB -> 0.99 dB**, worst band 1.89.

Three things that decided the chain, all measured:
- **Gate BEFORE the EQ, and firmer than an ad chain wants.** A fitted treble shelf
  (+6.2 dB above 5.2 kHz) restores the air a chest lav never had — and lifts lav hiss
  with it. At matched loudness the soft gate left the noise floor 2.2 dB WORSE than
  the un-EQ'd original; a firmer one (0.016 / 2.2 / range 0.30) landed at parity.
- **Prove a gate is taking room tone and not word tails** by re-transcribing windows
  with and without it: 100 % word overlap across four 25 s windows here.
- **`afftdn` is a trap on a voice you just added air to.** `nr=8` dropped the floor a
  further 3 dB but pushed the band error 0.97 -> 1.73 dB, eating exactly the 5-10 kHz
  the shelf exists to restore.

### Re-cutting audio onto a picture you are NOT re-rendering

`reference/build_audio_singlemic.py`. render.py rounds every segment to whole frames
and those roundings accumulate — **+0.65 s over 44 ranges here** — so rebuilding audio
from the EDL's float ranges drifts most of a second by the end. Cut each range to the
duration its **already-rendered video segment** actually has, read back out of the
segment cache, and the sum matches by construction. Two traps inside that:
- Use the segment's **video** stream duration, not its audio: each AAC segment's audio
  stream reads ~15 ms short (encoder priming) and the concat demuxer already
  compensates. Summing the audio durations loses 0.56 s.
- **Assert the result against the finished picture before muxing** (>0.10 s = refuse).
  That assertion caught the audio-duration mistake on the first attempt.

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

### Static chips are the FLOOR, not the deliverable  **REQUIRED**

The static-PNG chip system above is what longform shipped for five videos, and it is the
single biggest reason the ab-wheel cut lost to an outside editor. Use the **animated** pack
instead: `.claude/skills/_shared/motionlib.py` (shared with `/ad-edit` — a fix in one now
reaches both) and `.claude/skills/_shared/sfxlib.py`.

⚠ **`_shared/` was already the tracked home; `/ad-edit/reference/` held an UNTRACKED
duplicate.** So the pack existed, was in git, and this skill still never imported it.
Both per-skill copies are now import shims. Import from `_shared/`, never copy.

The house style is measured off the outside editor's frames and recoloured to Dan's
revision note *"make green used in graphics slightly darker, military green"*. See
`reference/HOUSE_STYLE.md` for the numbers. Components, all in `motionlib`:

| component | what it is | used for |
|---|---|---|
| `title_plate` | bracketed field + gradient plate + oblique caps wiping on line by line | chapter cards |
| `section_label` | numbered green chip + light plate, sliding in from the left | "02 — It Has A Built In Progression" |
| `stack_build` | items appearing ONE AT A TIME, synced to when each is spoken | the three ab muscles as he names them |
| `lower_third_bar` | accent bar + dark plate | form cues |
| `number_pop` | letter-by-letter snap-in | the "$17" callout |
| `inset_frame` | bracketed field with a rounded WINDOW punched through it | B-roll presented on brand, not cut to full-frame |
| `bracket_frame` | J2 corner brackets + tick marks | on every full-screen graphic |

**A vertical source needs a phone-shaped window, not the 16:9 one.** Fitted into the wide
window, a 1320×2868 screen recording is 352 px across and reads as lost on the field.

**End on the product, not on a text box.** The reference edit ends on an app screen and so
does every ad we ship. `build_endcard.py` in the delivery folder is the template: brand
field, phone-shaped window running the real generation flow, URL beside it. Use the app
recording **from 3.0 s only** — from 25.25 s it reaches the "Meet the new you" BEFORE/AFTER
screen and then an email-capture screen, and Dan's standing rule is no side-by-side
before/after in ANY video, and email capture never.

**Product/insert cards go viewer-LEFT over the door, and must clear the lower-third
chips.** At this framing Dan sits centre-right; x = 55…495 is free. But a 440×520 card at
y=300 collides with a chip's eyebrow bar at y=796 — the first pass overlapped the SLEEP
TRACKER chip. Card top at **y=225** leaves a 50 px gap. Also: a Copperplate eyebrow at 22 pt
overflows a 440 px card at ~24 characters ("SLEEP TRACKER // OPTION 01" was clipped) — put
the distinction in the Impact title, not the eyebrow. Official press renders work well
inside a J2 frame with a light product well; a near-black product (the navy WHOOP band)
disappears on a dark well, so the well is near-white and the J2 branding comes from the
frame and name plate. `reference/build_product_cards.py`.

**NEVER split a range just to hang a chip.** Chips are placed by SOURCE time and mapped
through the EDL, so a single range carries as many chips as you like. Splitting one anyway
removes ~0.02 s of source and leaves render.py's 30 ms fade-out immediately followed by its
30 ms fade-in **in the middle of continuous speech** — the only genuine audio defect this
batch produced, and the one join that legitimately failed QC. Assert it away: any adjacent
pair whose gap is < 0.20 s should be merged into one range.

---

## Step 7.5 — MUSIC AND SFX  **REQUIRED — gate: 2nd-percentile frame level ≥ −52 dBFS**

Longform shipped five videos with no music bed at all. A bed is most of the difference
between "a talking head" and "a video", and its measurable signature is that the programme
floor never falls to room tone.

**Licence is settled and is not a blocker.** Use **Pixabay**: the Pixabay Content Licence
permits commercial use with **no attribution**, chosen deliberately over CC-BY so nothing
has to be credited in perpetuity. `/ad-edit` rev-5 settled this.

**Pick the track by MEASUREMENT, not by taste** — `reference/pick_bed.py`. It scores every
candidate on two axes against a reference edit's own bed, sampled in that edit's speech
gaps (found from its word timings):

1. **Spectral shape** — a bed with energy at 400–3000 Hz fights the dialogue and is what
   makes a mix sound amateur.
2. **Flatness** — the std-dev of 4-second RMS blocks. If energy swings, the sidechain
   pumps and the bed starts drawing attention to itself.

**Shape is fixable; flatness is not. Pick on flatness, then EQ the shape.** The ab-wheel
winner had the best flatness of seven (0.4 dB) and 4.5 dB of shape error; a four-band
scoop took it to **0.53 dB** against the reference bed. Picking on the raw combined score
would have taken a track that swings 5.5 dB.

Duck it under the voice with `sidechaincompress`, **long release (~420 ms)** — a short one
lets the bed spring back between words, which is where it masked a quiet "n't".

**SFX are synthesised, not sourced** (`_shared/sfxlib.py`): no account-walled library, no
per-asset licence to track for the life of the channel. One cue per graphic entrance —
`riser` + `whoosh` + `sub` into a full-screen card, `whoosh_soft` on a lower third or a
framed inset, `pop_soft` on each item of a build. Start each cue ~0.10 s BEFORE the cut so
it reads as being ON it.

### Step 7.6 — the loudness finish  **gate: −14 LUFS ±1, true peak ≤ −0.5 dBTP**

Two-pass measured `loudnorm`, always. **Target TP −2.5, not −1.5, when the deliverable is
AAC** — measured on the ab-wheel mix at 256k:

| loudnorm TP target | PCM dBTP | delivered AAC dBTP | integrated |
|---|---|---|---|
| −1.5 | −1.50 | **+0.28** FAIL | −14.15 |
| −2.0 | — | **−0.44** FAIL | −14.46 |
| −2.5 | — | **−1.47** PASS | −14.74 |

The AAC encoder overshoots ~1.8 dB on this material, and the headroom costs ~0.3 LUFS per
0.5 dB. Take that trade. It is **not** the `alimiter` trade the skill warns about, which
costs a dB of loudness per dB of peak — here the peak is not what binds the gain.

---

## Step 8 — subtitles  **REQUIRED for talking-head content — gate: captions on ≥ 45% of sampled frames**

**Burn captions on talking-head content. Ship an `.srt` either way.**

The old rule here said "SRT, not burned in", full stop. That was decided for the meal-prep
**split-screen tutorial**, where a screen recording occupies the left 570 px and burned
captions fight the app UI. It was never a rule about longform in general, and reading it
as one is why the ab-wheel video shipped with no captions at all.

| content | burned captions | `.srt` |
|---|---|---|
| talking head, demo, workout, anything with no screen recording | **yes** | yes |
| split-screen tutorial where a screen recording holds the frame | no | yes |

The `/shorts` burned-ASS spec applies to the first row. Placement has to cooperate with
the graphics — this is the part the reference edit never had to solve, because it carries
no captions:

* **Full-screen cards → SUPPRESS the caption.** The card carries its own headline; a
  caption on top is two texts saying different things. 21 of 212 cues were dropped this way.
* **Drop the fragment that arrives out of a card, too.** Suppressing mid-sentence leaves
  the tail behind: the viewer saw "…and I'll", then a card, then "to be using it." Drop
  any cue that follows a suppressed one and starts lowercase.
* **Set MarginV so the band clears everything else.** Section labels and lower thirds live
  at y 796–884; a framed inset window ends at y 933; the watermark sits bottom-right.
  MarginV 62 with a 58 px face puts captions at roughly y 950–1020, clear of all three.
* **Chunk on PHRASE boundaries, not on a word count.** A fixed 5-word cap produced
  "I'll show you why you" / "need to be buying an". Break on sentence punctuation, on a
  pause ≥ 0.26 s, or when the line would exceed ~40 characters — whichever comes first —
  and fold one-word orphans into a neighbour.
* **Word-time them from the FINAL VOICE**, then diff that re-transcription against the
  source words. The ab-wheel rebuild scored **99.26%** overlap, which is what proves the
  re-cut did not eat a word; the eight differences were transcription variants
  ("alright"/"all right") plus two real Whisper errors worth correcting in the caption text.

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

**A CLUSTER of zero-length word timestamps is text Whisper INVENTED — drop it, or the
captions narrate a sentence that was never spoken.** Three shipped in the spray-tan rev-0
SRT and all three were proved absent by re-transcribing the source audio: "you're going
to be getting a shower before you get into bed at night.", "the amount of money you get to
spend on a spray tan is", and "you want to get the best effect. So, really,". Each is an
echo of a nearby real sentence. The rule that removes them without touching real speech
(`reference/make_srt_declump.py`): a **clump** is >=3 consecutive words that each last
<=0.05 s and together span <0.10 s. Drop the clump; drop the word AFTER it when that word
carries the clump's **dominant** timestamp (comparing against the clump's first or last
member fails both ways — a 0.04 s fragment can open the clump early, and a clump can END
on the timestamp where a perfectly real word begins); drop the word BEFORE it when that
word is itself a <=0.05 s fragment ending there. **Isolated** zero-length words are kept —
those are ordinary glitches on real speech.

**Break a timestamp tie on READING ORDER, never on the text.** `mapped.sort()` on
`(t0, t1, text)` tuples sorts a zero-length cluster ALPHABETICALLY, and the rev-0 file
shipped "is a amount get money of on spend spray the to you is tan that". Sort on
`(t0, original_index)`.

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

## Step 9 — QC, automated  **BOTH gates, every time**

```bash
python3 reference/qc_style.py FINAL.mp4 --plan plan.json --srt captions.srt --talking-head
python3 reference/qc_generic.py <slug> FINAL.mp4        # the technical checks below
```

**`qc_style.py` is the one that matters and it is the reason this skill was rebuilt.** It
measures the FINISHED FILE — not `chip_timings.json`, not the EDL, not your plan — because
the ab-wheel video's plan was fine and its picture was not. Every failure message names the
fix and the step number. Run it on the reference cut you are trying to beat as well; that
is how its thresholds were calibrated, and it is how you find out that a competitor's cut
breaches Dan's 30-second rule too.

### The technical checks (the original six)


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

**Intermediates on the external drive; FINISHED VIDEOS in the project folder.**
Dan's standing instruction (2026-08-21): *"Going forward, save your final videos in the
project folder rather than on the hard drive."* So:
- **Working dirs → the external drive `/Volumes/Extreme/`.** Raw rolls, extracted audio, `clips_graded/` and the pre-loudnorm
  intermediates are tens of GB. The 8/3 shoot alone is 118 GB and the boot disk sits near
  99 % full — never point a working directory at it.
- **`FINAL_*.mp4` + `.srt` + chapters + the recipe files → the project folder**, in
  `claude edited long form content/<NN - Title>/`.
- **NEVER delete `clips_graded/`.** It IS the segment cache — deleting it turns a
  one-beat revision back into a full re-render. That is the whole point of the cache.

**The repo is PUBLIC, and finished videos now live inside it.** `.gitignore` carries a
global `*.mp4` / `*.mov` / … rule for exactly this reason: two folder-name rules have
already failed after a rename (`YouTube Content/` leaked 8.3 GB in 2026-08;
`EDITED 8-20-26/` arrived unignored when Dan renamed it). Extensions don't get renamed.
**Still run `git check-ignore -v` on the delivery folder after any rename** — the rule is a
backstop, not a licence to skip the check.

**Ship the recipe next to the video.** Each delivered folder carries `FINAL_*.mp4`,
`FINAL_*.srt`, the pre-graphics `CUT_v1_graded.mp4` as a rollback point, plus `edl.json`,
`ranges.py` and `chips.py`. With the segment cache working, those three text files are all
a revision needs.

Then `/youtube-packaging` for title, description, chapters and thumbnail.

### Long renders: NEVER poll for a filename, and always signal DONE

A spray-tan rev-1 background task sat "Running" for **20 hours after the render had
finished** (2026-08-22). Nothing was wrong with the video — it was complete and QC'd on
disk at 18:12 the previous day. The watcher was a `while [ ! -f "$OUT" ]; sleep` loop, and
it was watching a filename the render never wrote under that name. Dan saw a blinking dot
and did not review a finished video for a day. **That is the real cost: not machine time,
review latency.**

Rules, in order of preference:

1. **Run the render in the foreground where it fits.** A backgrounded job you have to
   watch is worse than a job that just blocks and returns. Only background a render that
   genuinely exceeds a single tool call.
2. **When you must background it, wait on the PROCESS, not on a file.** A process either
   exits or it doesn't; a filename can be renamed, moved by an atomic-write, or written to
   a temp path and only then moved into place. Capture the pid and `wait $PID` (or poll
   `kill -0 $PID`). Never `[ -f "$OUT" ]` as the loop condition.
3. **Every wait gets a hard timeout** sized to the job (a 30-minute video is ~90 min of
   render; cap at 3x and report). A loop with no ceiling is a loop that strands.
4. **The loop must print WHY it exited** — `RENDER COMPLETE`, `RENDER FAILED (code N)`, or
   `TIMEOUT after Ns`. A watcher that ends silently is indistinguishable from one still
   running.
5. **Verify the artifact after the wait, don't infer it from the wait.** `ffprobe` the
   output for duration and stream count. The wait tells you the process ended; only the
   probe tells you the video is good.

**Ending a session: the delivery message must be unmistakable.** Dan reads the task list,
not the transcript. End with the finished file's **path, size and duration as measured by
`ffprobe`** and the words *ready to review*. If any background task is still listed as
running when the work is actually done, say so explicitly and tell him to clear it.

**Dan's own 10-second check, when a dot is blinking and he isn't sure:**

```bash
ps aux | grep -Ei "ffmpeg|whisper" | grep -v grep
```

Empty output means no video work is running anywhere on the machine, whatever the panel
says. Then check the file itself — if it has a recent timestamp and a sane size, it's done.


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
