# Handoff: Clear the claimed music bed from V5 (Ultimate 1 Minute Ab Workout — Workout Only)

**Date:** 2026-08-28
**Project:** Abs By AI
**Handing off from:** Claude Code
**Handing off to:** Claude Code or Codex
**Business goal this serves:** Protecting the YouTube channel's monetisation and reach — a
Content ID claim on a long-form video diverts its revenue to the claimant, and the same track
already got our Short blocked globally.

**Do V5 before V4.** V5 is the cheap one (no speech to preserve) and it proves the recipe on a
real long-form before the harder job.

---

## Objective

`V5 - Ultimate 1 Minute Ab Workout-Workout Only` — the follow-along cut, **no talking** — appears
to carry the same music bed family that got our Short claimed. Replace its bed with a cleared
track at the **file** level, and decide what to do about the copy already published on YouTube.

**Scope note:** V4 is a separate handoff (`handoff-20260828-v4-longform-bedswap.md`). Do not
touch V4 here.

---

## Current state — measured this session, not assumed

| | |
|---|---|
| Local file | `YouTube Long Form Video Content/V5 - Ultimate 1 Minute Ab Workout-Workout Only(1) - READY FOR UPLOAD.mp4` |
| Duration | **281.12 s** (4:41) |
| Audio | stereo, integrated RMS −10.8 dBFS, **quietest second −25.3 dB, zero seconds below −60 dB** |
| YouTube video id | **`8BaCYcGhRPY`** — scheduled to publish **Sun 2026-08-23 9:00 AM CT**, so it is live now |
| Claim status on YouTube | ⚠ **UNKNOWN — this is step 1** |

### V5 contains NO speech — this is what makes the job easy

Three independent readings agree:

1. **Dan says so himself, on the source recording.** In the raw cutdown at 454.88 s he says the
   follow-along video is *"the full workout being done without any talking, without any
   explanations and you just want to follow along."* V5 is that video.
2. **Syllable-rate modulation test** (3–8 Hz amplitude modulation in the 300–3000 Hz band, the
   acoustic signature of speech), with controls:

   | sample | index |
   |---|---|
   | control — known speech (short5 1.8–5.0 s) | 1.670 |
   | control — known speech (V4 30–60 s) | 1.542 |
   | control — known **music** (short5 20–50 s) | 1.174 |
   | **V5 at 20 s / 120 s / 220 s** | **1.249 / 1.241 / 1.271** |

   V5 sits with the music control, clearly below both speech controls.
3. Whisper returns the identical string *"Thanks for watching guys!"* at 20 s, 120 s and 220 s —
   the classic hallucination-over-music signature, not real speech.

⚠ **Do not use `no_speech_prob` to check this.** It was tried and it does not discriminate:
0.21–0.27 on V5's music, 0.25 on short5's known-good speech. It looks like a clean test and is
worthless here.

**Consequence: the entire audio track can be replaced wholesale. There is no voice to preserve,
no EDL to recover, no lip sync to hold.** That is the whole reason this handoff is short.

### What is actually known about the claim

⚠ **The fingerprint evidence for V5 is WEAKER than for V4 and must not be overstated.**

Matching V5 against a 60-second music-only reference lifted from short5's bed:

| file | score | reading |
|---|---|---|
| control — same bed under a *different* voiceover | 3.79 | what a true match looks like |
| V4 longform | 0.78 | exactly what length-dilution predicts for an 81.5 s match inside a 494 s file — **V4 contains the track** |
| **V5 longform** | **0.28** | above the 0.01–0.05 noise floor, but implies only ~16 s of matching material |

The reference is **one specific 60-second stretch** of the bed. A score of 0.28 is consistent with
either "V5 uses a different part of the same track" or "V5 uses a different track that shares
some material". **It is not proof that V5 is claimed.** Step 1 resolves this properly.

---

## The claimed track, and the trap in the previous fix

The track that got the Short blocked is **"Hard Rap Beat" by Artiss** (global audio claim on
Short `I_trw1PaMhc`, no strike; recorded in `AI_COORDINATION_ARCHIVE.md`, 2026-08-13 entry).

That claim was cleared with YouTube Studio's **Replace song**, swapping in **"Get A Move On" by
Audionautix, CC-BY 4.0**.

⚠ **The CC-BY replacement carries a live attribution obligation** — the credit line is in the
YouTube description and was mirrored into the IG and FB captions, and `BLOTATO_QUEUE_PROGRESS.md`
says it must not be removed.

⚠ **Do not reach for a CC-BY track again.** CC-BY libraries are heavily Content-ID fingerprinted
(the same reason Kevin MacLeod's "Werq" was rejected for the ad-1 vertical), and they bind us to
perpetual credit. Use Pixabay.

### The replacement bed to use

`/Volumes/Extreme/_edit_work/abwheel/r2/music/organic_flow.mp3`

- **131.7 s**, Pixabay Content Licence — **commercial use, no attribution**
- Provenance is documented in `/Volumes/Extreme/_edit_work/abwheel/r2/pick_bed.py`'s docstring:
  all seven tracks in that folder are Pixabay
- Already used successfully in the short5 bed swap on 2026-08-27
- ⚠ **131.7 s does not cover V5's 281.1 s.** You must either loop it (choose a loop point on a
  bar line, not an arbitrary cut) or pick a longer track. The other six candidates in that folder
  are 122–152 s, so **none of them covers 281 s in one pass** — looping or a fresh download is
  unavoidable. Say so in the delivery notes rather than hiding a seam.

---

## Steps

### Step 1 — Establish whether V5 is actually claimed (do this first; it may end the task)

Open `https://studio.youtube.com` → Content → V5 (`8BaCYcGhRPY`) → **Restrictions** column.

- If it reads **"None"**: there is nothing to clear on YouTube. **Stop and ask Dan** whether he
  still wants the local file's bed swapped as a precaution before it gets mirrored to
  TikTok/IG/FB. Do not do the work unasked.
- If it names a claim: **record the exact claimed track title and claimant** and continue. The
  Studio claim detail view also shows the **time ranges** the claim covers — copy those down, they
  tell you whether the bed runs the full 4:41 or only part of it.

### Step 2 — Confirm the track in the local file independently

Run the fingerprint tool against the file to confirm what is actually in the local master, rather
than trusting that the local file matches what YouTube holds:

```bash
python3 Handoffs/assets/bedswap-20260828/fingerprint.py <reference.wav>
```

Build the reference from a music-only stretch of the **local short5 pre-swap master**
(`Short-form video content/short5_1-minute-workout_PRE_BEDSWAP.mp4`, use 10–70 s — that window is
verified music-only). **Always run a positive control in the same pass** — the tool prints one.
A true match scores 3.8–4.8; unrelated audio scores 0.01–0.05. Anything in between needs
explaining before you act on it, which is exactly the situation V5's 0.28 is in.

If V5's bed turns out **not** to be the claimed track, stop and report. The job is then closed.

### Step 3 — Rebuild the audio

Because there is no speech, this is a straight swap:

1. Render the new bed to exactly 281.12 s (loop with a beat-aligned join if using `organic_flow`).
2. Match the perceived level of the old bed, then normalise the finished file to the house spec:
   **I = −14 LUFS, TP = −1.5 dBTP, LRA = 11**, two-pass loudnorm.
3. Short fade in (~0.4 s) and fade out (~2.5 s).
4. Mux against the original picture with **`-c:v copy`** — the video must not be re-encoded.

⚠ **Two-pass loudnorm parses ffmpeg's stderr.** Do not run the measurement pass with `-v error`;
it suppresses the JSON. Use `-hide_banner -nostats` and read stderr.

⚠ **zsh trap that cost time on 2026-08-27:** `"$M:linear=true"` silently applies zsh's `:l`
lowercase modifier and corrupts the filter string. Write `"${M}:linear=true"`.

### Step 4 — Verify on the delivered file, not the build plan

Every one of these must pass:

| check | how | pass condition |
|---|---|---|
| old track gone | `fingerprint.py` vs the old-bed reference | collapses to the 0.01–0.10 band |
| picture untouched | `ffmpeg -i out.mp4 -map 0:v -c copy -f md5 -` on both files | **identical MD5** |
| loudness | two-pass loudnorm measurement | −14 ±0.2 LUFS, TP ≤ −1.0 |
| audio integrity | per-second RMS scan | **zero** seconds below −50 dBFS |
| duration | `ffprobe` both streams | video and audio both 281.12 s, matching within 0.15 s |
| loop seam | listen at the join, and check the per-second envelope for a step | no discontinuity |

### Step 5 — Decide the YouTube side (Dan's call — do not act alone)

⚠ **YouTube will not let you replace an existing video's file.** The options are:

| option | keeps URL/views? | cost |
|---|---|---|
| Studio **Replace song** | yes | fast, precedent exists (used on the Short), but **YouTube marks the edit permanent** and the library skews CC-BY |
| Studio **Erase song** | yes | on V5 this is **viable** because there is no speech to lose — but it can leave stretches of silence, which would gut a follow-along workout |
| Delete + re-upload the fixed file | **no** — new URL, loses views, comments and watch history | full control of the audio |

**On the Short, Replace was chosen over Erase specifically because Erase would have left ~70
seconds of silence.** That reasoning does not automatically carry to V5 — V5 is nothing but
music, so Erase would leave 4:41 of silence, which is worse, not better. **Recommendation:
Replace song, or re-upload.** Put both to Dan with the view count attached; he decides.

---

## Acceptance criteria

- [ ] V5's claim status on YouTube is **recorded as a fact**, not assumed
- [ ] The track in the local V5 master is identified with a positive control in the same run
- [ ] If claimed: local master rebuilt with a cleared, no-attribution bed and all six Step 4
      checks pass on the delivered file
- [ ] Previous master preserved alongside as `*_PRE_BEDSWAP.mp4`
- [ ] The YouTube-side decision is put to Dan with the trade-offs, and not executed unilaterally
- [ ] `AI_COORDINATION.md` updated; the dashboard task checked off only once the work is really done

## Risks and cautions

- ⚠ **Do not delete anything on YouTube without Dan's explicit go-ahead.** Deleting a published
  video is irreversible and loses its watch history. This is outside the standing
  bias-toward-action authorisation.
- ⚠ **`/Volumes/Extreme` must be mounted** — the replacement bed lives there.
- The repo is public and gitignores `*.mp4`; the media stays untracked. Do not commit video.
- $0.00 AI spend expected. No production code, no deploy, no native-retest trigger.

## Exact next action

Open YouTube Studio and read V5 (`8BaCYcGhRPY`)'s Restrictions column. If it says "None", stop
and ask Dan before doing anything else.
