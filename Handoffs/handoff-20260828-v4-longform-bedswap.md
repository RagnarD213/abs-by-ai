# Handoff: Clear the claimed music bed from V4 (The Ultimate 1 Minute Ab Workout)

**Date:** 2026-08-28
**Project:** Abs By AI
**Handing off from:** Claude Code
**Handing off to:** Claude Code (this one wants the full pipeline; not a good Codex task)
**Business goal this serves:** Protecting the channel's monetisation and reach. V4 is **published
and public** (went out 2026-08-11), and it provably contains the same music bed that got our Short
blocked worldwide.

**Do the V5 handoff first** (`handoff-20260828-v5-longform-bedswap.md`). V5 has no speech, so it
proves the bed-swap recipe on a real long-form for a fraction of the effort. V4 is the hard one.

---

## Objective

Rebuild V4's audio so it carries a cleared, no-attribution music bed **while preserving every word
Dan speaks, in sync with the picture**, then decide with Dan what to do about the published copy.

---

## Why this is harder than short5 or V5

| | short5 (done 2026-08-27) | V5 | **V4** |
|---|---|---|---|
| duration | 81.5 s | 281.1 s | **494.1 s (8:14)** |
| speech | 5.2 s, in two clean blocks | **none** | **throughout** |
| fix | paste 2 voice clips onto silence | replace whole audio | **conform the whole voice track** |

On short5 the voice only existed at 0:01.8–0:05.0 and 1:19.8–1:21.3, so the rest could be pure
bed. **V4 talks all the way through**, so the voice has to be reconstructed across the full 8:14
and stay in sync with the picture.

---

## Current state — measured, not assumed

| | |
|---|---|
| Local file | `YouTube Long Form Video Content/V4 - The Ultimate 1 Minute Ab Workout(2).mp4 - READY FOR UPLOAD.mp4` |
| Duration | **494.13 s** |
| Audio | voice + music mixed; **floor never drops below −40.9 dB** (a continuous bed) |
| YouTube video id | **`Sv5wZha_a8c`** — `https://youtu.be/Sv5wZha_a8c`, uploaded 2026-07-31, **public since 2026-08-11** |
| Claim status on YouTube | ⚠ **UNKNOWN — step 1** |

### V4 provably contains the claimed track

Two independent proofs:

1. **short5 is a sample-exact slice of V4.** `short5_1-minute-workout.mp4` aligns into V4 at
   **371.500 s** with a raw sample correlation of **+0.999**. short5's bed is the track TikTok's
   copyright check flagged on 2026-08-27.
2. **Fingerprint, with controls.** Against a 60-second music-only reference from short5's bed:

   | | score |
   |---|---|
   | control — same bed under a *different* voiceover | 3.79 |
   | control — short5 against itself | 4.75 |
   | **V4** | **0.78** |
   | unrelated audio (the other 26 shorts) | 0.011–0.048 |

   0.78 is precisely what length-dilution predicts: 4.75 × (81.5 s ÷ 494 s) = 0.78. **V4 contains
   the track**; the low absolute number is an artifact of V4 being six times longer than the match,
   not weak evidence.

The track is **"Hard Rap Beat" by Artiss** — the global audio claim on Short `I_trw1PaMhc`,
recorded in `AI_COORDINATION_ARCHIVE.md` (2026-08-13).

### THE KEY ENABLER: a clean, music-free source of Dan's voice exists

`/Volumes/Extreme/Abs By AI Photo Shoots/The Ultimate 1 Minute Ab Workout - DESCRIPT RAW CUTDOWN.mp4`

| source | audio floor | verdict |
|---|---|---|
| **RAW cutdown** (507.18 s) | **67 seconds sit below −60 dB** | real silence gaps → **voice only, no bed** |
| V4 master (494.13 s) | never below −40.9 dB | music baked in |

A continuous bed holds the noise floor up. The raw's floor drops to true silence 67 times, which
is impossible with music mixed in. **This is why the job is tractable at all.**

Also verified: **the raw has NO two-mic fault.** L/R correlate **+0.9996 at 0.00 ms lag** — it is
dual mono, safe to sum. This is an older shoot than Jeff's 8/3 and 8/14 rolls, so the
right-channel-only rule in `/longform-edit` Step 5.6 does **not** apply here. Do not "fix" it.

### V4 is a LIGHT conform of the raw — this is the single most useful measurement in this document

Band-limited (900–3500 Hz) envelope correlation of V4 against the raw, in 12-second windows:

| V4 time | offset into raw | confidence |
|---|---|---|
| 20 s | −1.28 s | 0.94 |
| 80 s | −2.95 s | 0.96 |
| 150 s | −1.12 s | 0.97 |
| 220 s | −0.82 s | 0.94 |
| 290 s | +0.83 s | 0.94 |
| 360 s | +1.66 s | 0.91 |
| 430 s | (+14.25 s) | **0.19 — failed** |
| 470 s | (+11.84 s) | **0.21 — failed** |

**Reading:** across 20–360 s the offset drifts smoothly over a ~3-second range at 0.91–0.97
confidence. V4 is the raw with a **modest number of small trims** — 507.18 − 494.13 = **13.05 s
removed in total** — not a heavily re-cut edit. Recovering the EDL is realistic.

⚠ **The two failures at 430 s and 470 s are expected and are not a problem.** That region is the
workout itself — music with almost no speech — so a *voice-band* correlation has nothing to lock
onto. It is a limitation of the probe, not a gap in the raw: the raw's outro line was located
there by hand at 451.98–453.36 s. Use a different anchor (or full-band correlation) in that
stretch rather than concluding the raw does not cover it.

---

## The traps that already cost time on short5 — do not re-learn these

⚠ **1. V4 is NOT contiguous with the raw. A single global offset will drag in outtakes.**
The first short5 build assumed one offset and pasted in *"just because that's going to make your
form suffer"* — a discarded take sitting immediately before the intro line — because the edit has
internal cuts. **Recover per-segment offsets. Verify by transcribing the result, not by trusting
the alignment score.**

⚠ **2. Whisper's word onsets are unreliable at take boundaries; measured energy outranks them.**
On the raw outro Whisper put the first word at 451.32 s. The actual speech onset, from a 20 ms
RMS scan, is **451.90 s** — 0.6 s later. Trusting Whisper cost a clip that carried 0.8 s of
leading silence, pushing the line late and truncating the end of the sentence. **Always confirm a
cut point against the energy envelope.**

⚠ **3. Whisper hallucinates fluent sentences over music. It will do this on V4's workout stretch.**
Verified on short5: the voice track was *exactly zero* through 76.0–79.75 s, and Whisper still
reported *"Girl bring me some more poached eggs with the truffle on the side"*. Also seen: *"Fresh
squeeze"*, *"Organic place"*, and — on V5 — the same *"Thanks for watching guys!"* at three
different timestamps. **Never treat a transcript over music as evidence of speech. Check the
source track's energy.**

⚠ **4. Check whether the picture carries burned-in captions.** short5 does, and that turned out to
be the best sync reference available — caption onsets are frame-accurate ground truth the audio
must match. Detect them by differencing a captioned frame against an uncaptioned one to find the
caption band, then scanning for the ink transition. On short5 that gave the outro at **79.867 s**,
which settled a dispute between two audio methods. **Establish early whether V4 has them** — if it
does, they are your sync ruler *and* a hard constraint.

⚠ **5. The ffmpeg sidechain compressor does not duck enough.** On short5 it pulled the bed to only
**68%** under speech, which Dan heard immediately. Use explicit gain automation instead:
`Handoffs/assets/bedswap-20260828/duck_envelope.py` — Dan's chosen depth is **0.30 (a 70%
reduction)**, with the duck starting **0.35 s before** speech, because a duck that starts on the
first syllable is always late.

⚠ **6.** Two-pass loudnorm parses stderr — do not run the measurement pass with `-v error`.
And in zsh write `"${M}:linear=true"`, never `"$M:linear=true"` (`:l` is a lowercase modifier).

---

## Steps

### Step 1 — Establish the claim status (may change the whole plan)

YouTube Studio → Content → V4 (`Sv5wZha_a8c`) → **Restrictions**. Record the exact claimed track,
claimant, and the **time ranges** the claim covers. If it reads "None", stop and ask Dan whether
he wants the local master cleaned anyway before it feeds any further re-use.

### Step 2 — Recover the EDL (raw → V4)

Use the `/longform-edit` and `/shortad-from-longform` recovery method: word-level alignment of the
raw transcript against V4's transcript, then per-segment envelope refinement. The measured drift
table above is your sanity check — any segment whose recovered offset falls outside roughly
−3 s to +2 s is suspect and should be re-examined rather than accepted.

Sanity anchors already established, free of charge:
- short5 = **V4 371.500 s**, sample correlation +0.999
- raw intro line: speech starts **373.50 s**, preceded by clean silence 373.02–373.48 s, and the
  discarded take before it ends at **373.00 s**
- raw outro line: speech **451.90–453.36 s**; *"Thanks for joining us today"* starts 453.50 s and
  must not be included

### Step 3 — Build the voice track

Place each recovered segment onto a silent 494.13 s timeline at 44100 Hz, with ~25 ms fades at
every edge to avoid clicks. Then the voice chain that was fitted on short5:

```
highpass=f=80,
acompressor=threshold=0.05:ratio=3:attack=10:release=200,
volume=11dB,
treble=g=5:f=3500:w=0.7,
alimiter=limit=0.89
```

⚠ **The +11 dB is fitted to this roll and this compressor, in that order.** The raw voice peaks at
−9.5 dBFS, so applying gain *before* compression clips. Re-measure rather than assuming the number
transfers.

⚠ **A tone fit was attempted on short5 and deliberately not fully applied.** Measuring the
finished mix against the raw suggested +4.3 dB at 80–200 Hz and +6.5 dB at 3–8 kHz — but the
low-band figure is contaminated by the bed's own bass energy sitting under the speech, so only a
conservative presence lift was used. **Do not apply a bass boost fitted this way.** If you want a
real tone match, fit it on a window where the bed is provably absent.

### Step 4 — Bed, duck, mix, normalise

1. New bed: `/Volumes/Extreme/_edit_work/abwheel/r2/music/organic_flow.mp3` — Pixabay Content
   Licence, **commercial use, no attribution**. ⚠ **131.7 s does not cover 494 s.** All seven
   Pixabay candidates in that folder are 68–152 s, so you must loop on a bar line or source a
   longer track. Whatever you choose, log it.
2. ⚠ **Do not replace with a CC-BY track.** The previous fix used **"Get A Move On" by Audionautix,
   CC-BY 4.0**, which binds us to perpetual credit and is exactly the kind of library that gets
   Content-ID fingerprinted. Pixabay only.
3. Duck with `duck_envelope.py` at **0.30**, driven off the voice-only track.
4. Mix, then two-pass loudnorm to **−14 LUFS / −1.5 dBTP / LRA 11**.
5. Mux with **`-c:v copy`**.

### Step 5 — Verify on the delivered file

| check | pass condition |
|---|---|
| old track gone | fingerprint vs the old-bed reference collapses to the 0.01–0.10 band |
| **word fidelity** | re-transcribe the finished render and diff against V4's transcript — **≥98%**, the standard the pipeline already holds |
| **no outtakes** | every recovered segment's transcript matches V4's; no discarded take anywhere |
| lip sync | per-segment cross-correlation against V4's own audio within **±10 ms** |
| captions (if present) | speech onsets land on the burned caption onsets |
| duck depth | measured in a voice-free window inside a ducked stretch: **−10.5 dB**, allowing for the track's own level variation between the compared moments |
| picture untouched | video-stream MD5 identical to the source |
| audio integrity | zero seconds below −50 dBFS; audio and video durations match within 0.15 s |
| loudness | −14 ±0.2 LUFS, TP ≤ −1.0 |

⚠ **A format-only gate is not enough and this project has been burned by that before.** short5
passed loudness, duration and fingerprint checks while still carrying a stray outtake and a
truncated final word. **Transcribe the head and tail of the finished file and read them.**

### Step 6 — The YouTube decision (Dan's call — do not act alone)

⚠ **YouTube will not let you replace a published video's file.**

| option | keeps URL/views? | cost |
|---|---|---|
| Studio **Replace song** | yes | fast; precedent on the Short. But **YouTube marks the edit permanent**, and its library skews CC-BY |
| Studio **Erase song** | yes | ⚠ on the Short this was **rejected** because it would have left ~70 s of silence. V4 is a talking video, so Erase is more viable here than it was there — but verify what it does to the workout stretch, which is music-only |
| Delete + re-upload | **no** — new URL, loses views, comments, watch history, and the thumbnail A/B test | full control |

V4 has been public since 2026-08-11. **Bring Dan the view count with the options.**

---

## Acceptance criteria

- [ ] V4's claim status recorded as fact
- [ ] EDL recovered and **verified by transcript**, not by alignment score alone
- [ ] Word fidelity ≥98%, zero outtakes, lip sync within ±10 ms
- [ ] Bed is cleared and attribution-free; duck measured at −10.5 dB under speech
- [ ] All Step 5 checks pass **on the delivered file**
- [ ] Previous master preserved as `*_PRE_BEDSWAP.mp4`
- [ ] YouTube-side decision put to Dan, not executed unilaterally
- [ ] `AI_COORDINATION.md` updated; dashboard task checked off only when genuinely done

## Risks and cautions

- ⚠ **Never delete a published YouTube video without Dan's explicit instruction.** Irreversible,
  outside the standing authorisation.
- ⚠ **`/Volumes/Extreme` must be mounted** — both the raw source and the replacement bed live there.
- ⚠ **There is a live licence obligation in the IG/FB queue that this work touches.**
  `BLOTATO_QUEUE_PROGRESS.md` says short5's queued captions carry a CC-BY credit for Audionautix's
  "Get A Move On" and must not be removed. **That line describes the YouTube copy's audio, not the
  local file's** — and after the 2026-08-27 swap the local master's bed is Pixabay, needing no
  attribution at all. **Flag this to Dan; do not silently edit those captions.**
- Repo is public and gitignores `*.mp4` — media stays untracked.
- $0.00 AI spend expected. No production code, no deploy, no native-retest trigger.

## Exact next action

Read V4 (`Sv5wZha_a8c`)'s Restrictions column in YouTube Studio and record exactly what the claim
says — including the time ranges it covers. Everything downstream depends on that.
