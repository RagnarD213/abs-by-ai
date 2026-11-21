# HANDOFF — Build the 60s "modern edit" sample (head-to-head vs Muhammad A's trial)

**From:** Claude Code (ad-1 rev-4 session, 2026-08-21)
**Recommended model/effort:** Opus 5 / high — this is a NEW motion-graphics build with real
aesthetic judgment (easing curves, typography, layout), not recipe execution. Low-usage
alternative: Sonnet 5 / high (acceptable; expect one extra revision round on animation feel).
**Read first:** `.claude/skills/ad-edit/SKILL.md` (esp. lessons 7, 13–18) and this doc. Invoke
`/ad-edit` for context, but note the deliverable is a CONTENT-format sample, not an ad revision.

## Why this exists

Dan sent 4 Upwork editors a paid trial. Muhammad A's 61s edit of the ad-1 script (YouTube-episode
format) beat our rev-4 in Dan's judgment: "sounds better, looks better, graphics are better."
The measured gap analysis (2026-08-21 session; memory file `muhammad-trial-edit-analysis.md`) found
five drivers, ALL replicable in our PIL/ffmpeg pipeline. **The deliverable of this task: rebuild the
same first minute of ad-1 with those five techniques in Abs By AI brand style, so Dan can compare
the pipeline head-to-head against the hire and decide the editing stack** (there's a dashboard task
for that decision).

**Reference video:** `/Volumes/Seagate 4TB/_edit_work/ad1-8-14/reference/muhammad_a.mp4` (61.5s,
1080p, Premiere export). His transcript with segment timings: `reference/ma_audio.json` alongside.
WATCH IT FIRST (frame-sample it) — the sample must match its energy, not just its checklist.

## The five gap-closers (with the measurements that define "done")

1. **Airtight pacing, NO speed-up.** His edit has ZERO inter-word gaps ≥0.25s across 61s; density
   206 wpm at true 1.0x (word-level timing of "the knowledge isn't the problem" matches the raw
   roll 1:1). Ours keeps Dan's natural pauses. Build a gap-compression pass (see recipe below).
2. **Music bed.** Upbeat track, ~-20dB RMS under the voice, full length (his keeps playing after
   the last word — confirmed by tail spectrogram). Duck under voice with `sidechaincompress`.
3. **Transition SFX.** Whoosh/pop on every graphic entrance (visible as 22kHz spikes in his
   spectrogram). Free CC0 one-shots (freesound.org or similar); mix via delayed `amix`.
4. **Animated graphics** — the main build. His set (all from a Premiere template pack, pastel-cyan
   theme): cards that scale/slide in with soft shadows; a progressive bullet list that grows
   bullet-by-bullet synced to speech ("IN TODAY'S EPISODE"); lower-third label chips ("The
   Problem" white chip + red strip); full-screen title cards ("VISUALIZING YOUR GOAL"); dashed-
   arrow connectors between photo cards; and an **animated glowing box drawn around the physical
   photo on the door behind Dan** synced to "THIS picture got me abs," followed by a punch-in.
5. **Brighter grade.** His talking-head luma 67 vs our 55 — lift shadows/mids ~20%, slight warmth.

Plus: he burns **no captions at all** — graphics carry emphasis. For this sample, match that
(no captions); captions remain the rule for paid ad cuts.

## Style decision (default chosen, Dan can override)

Do NOT copy his cyan/navy template look. Build the same techniques in **Abs By AI brand**: bright
clean cards — white/light background, dark navy or near-black text (Manrope/Arial Bold per the
thumbnail design system), **red accent** (the brand red ~ (226,34,34)), rounded corners + soft
shadows. The locked dark-J2 style stays for paid-ad graphics until Dan says otherwise; this sample
is the proposed CONTENT style. If Dan replies "just copy Muhammad's look," copy it exactly.

## Build plan

### Step 1 — tight cut of the first minute
Working dir: `/Volumes/Seagate 4TB/_edit_work/ad1-8-14/`. Base: `CUT_v2_graded.mp4` (don't touch).
`layout2.py` already computes render-time word positions (`rwords`, from `C1591.whisper.json` +
`edl.json`) — reuse that exact code. Script span: "This picture got me abs" → "…stare at it every
day." (source ≈ 0–96s of the cut; ends where the crude-photoshop insert ends, render ~69s).
Find every inter-word gap >0.25s in that span, cut it out (video+audio together, cuts on word
boundaries per the longform six rules), concat → `tight60.mp4` (~60–63s target). Re-transcribe the
result and assert no gap ≥0.25s survived. No atempo/speed-up anywhere.

### Step 2 — motionlib.py (the reusable library — this is the point of the task)
PIL frame-sequences → transparent-region MP4/PNG-sequences composited by ffmpeg overlay, exactly
like `assets_v1/stats_scan.mp4` was built (`prep_assets3.py` is the model). Components, each a
function taking (text/image, duration, easing):
- `card_in` — rounded-rect card with drop shadow, scale 0.9→1.0 + fade over ~0.35s, ease-out cubic
- `bullets_build` — list card where bullets appear one at a time at given timestamps (sync each to
  the word that introduces it)
- `lower_third` — label chip + red strip, slide-in from left ~0.3s
- `title_card` — full-screen brand background + big headline + subtitle, headline scales in
- `callout_box` — animated stroke drawing around a given rect over ~0.5s, then a glow pulse
- `arrow_dash` — dashed arrow that draws left→right
- easing helpers (ease-out cubic, ease-in-out, spring-ish overshoot ~1.03)
Put it at `.claude/skills/ad-edit/reference/motionlib.py` (git-tracked) and have the sample's
layout script import it. **Traps that WILL bite:** supersample before any zoompan (lesson 7 —
`scale=7680:4320` first); PIL-not-drawtext for all text; preview every composite on a REAL frame
before rendering; Copperplate small-caps trap if any J2 element is reused.

### Step 3 — graphic beats (mirror his placements, our style)
Use his video as the beat sheet. Minimum set: hook callout-box on the door photo + punch-in
("THIS picture") → before→arrow→phone-after cards ("I generated this picture with AI…" — see
compliance note below) → "200 POUNDS" text pop → progressive 3-bullet episode list (~14–27s) →
lower-third "The Problem | No time, no motivation." (~40s) → title card "VISUALIZING YOUR GOAL"
(~46s) → photoshop-era imagery beat (~52–60s). Sub the black-placeholder beat he left with a real
asset from `assets_v1/`.

### Step 4 — audio
Voice chain: light EQ (high-pass 80Hz, small presence lift ~3–5kHz) — subtle, Dan's voice is
already clean. Music: a free upbeat track (YouTube Audio Library needs Dan's browser — prefer a
CC0 source fetchable by curl; state the source and license in notes). Sidechain-duck ~6–8dB under
speech, target the bed ~-20dB RMS relative. SFX one-shots on each graphic entrance. Final two-pass
loudnorm to −14 LUFS on the full mix (our standard, NOT his −18.4).

### Step 5 — grade + deliver
Lift the talking-head grade toward luma ~65–67 (curves/eq on the base, not the graphics). QC per
the ad-edit suite where applicable. Deliver `sample_modern_60s.mp4` (full-res to the EDITED ADS
folder under `ad1-how-ai-got-me-abs/`, named clearly as a SAMPLE, not a rev) + a 720p review copy
via SendUserFile, **plus a side-by-side comparison clip** (his left / ours right, stacked hstack,
muted-his-audio version optional) so Dan can A/B in one file. Update notes.md, coordination file,
commit motionlib + scripts to the skill reference, push. Check off the dashboard task for this
handoff (added per Rule 8).

## Compliance note

This sample is CONTENT format (YouTube episode), where before/after imagery is acceptable — but
**never put the before-video and after-image on screen simultaneously in anything that could become
a paid ad**. Safe default even here: sequence them (before card → arrow wipe → after card replaces
it) rather than holding both on screen; it demos the same technique without building a banned
pattern into the library. AI-GENERATED labeling rules apply to every AI image shown (lesson 17
placement).

## Money / scope

- Expected AI spend: **$0** (all local: PIL, ffmpeg, existing whisper json). If any AI image/clip
  gen sneaks in, standard caps apply.
- Do NOT touch the rev-4 ad chain (`layout2.py`, `cap_v2.ass`, `ad1_rev4_16x9.mp4`) — the 9:16
  build is a separate pending task gated on Dan approving rev-4.
- Muhammad's video is Dan's property (paid trial) but an external editor's work — reference it,
  don't redistribute it.

## Definition of done

Dan can play the side-by-side and judge: same footage, same minute, our brand — does the pipeline
version match or beat the hire's on sound, motion, and polish? Every reusable piece lives in
`motionlib.py`, committed. Lessons learned appended to the ad-edit LEARNING sections.
