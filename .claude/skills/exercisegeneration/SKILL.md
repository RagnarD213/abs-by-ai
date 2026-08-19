---
name: exercisegeneration
description: Generate a photorealistic AI exercise demo video for the Abs By AI Trainer — AI-Dan (Dan's likeness in the logo tank top) performing the movement in the canonical gym as a seamless looping rep, narrated by Dan's cloned voice reading the form cues. Use whenever Dan asks to generate exercise demos, demo videos, replace stick figures, or run a batch of exercises from the library — even if he doesn't say "/exercisegeneration". For ad videos use /make-ad; for retouching Dan's real photos use /photo-edit.
---

# Exercise demo generation ("keyframe-locked" AI-Dan demos)

Produces one finished asset per exercise: a 15–25s MP4 of AI-Dan performing clean looping reps with
Dan's cloned voice coaching the form. Proven end to end on `bw-squat` (2026-08-19, Dan-approved).

## Fixed assets — never regenerate these

| asset | path |
|---|---|
| **Canonical character still** (AI-Dan, black tank, white Abs By AI logo, THE gym — Dan-approved) | `Media/exercise-demos/_character/ai-dan-canonical.jpg` |
| **Narrator voice** (clone of Dan's real workout-video voice, Dan-approved) | MiniMax voice_id **`R8_NE3EBC2N`** (`Media/exercise-demos/bw-squat/dan-real-voice-id-v2.txt`) |
| Exercise copy (setup / execution / mistake per exercise) | `public/exercises.js` |
| Image runner (Google-direct; do NOT use Replicate nano-banana-pro — it rate-limits) | `.claude/skills/_shared/gemini-image.js` |
| Working scripts from the proven run (Veo invocation, VO gen, demucs reclone) | `Media/exercise-demos/bw-squat/*.js` |
| Static ffmpeg/ffprobe (no Homebrew on this Mac) | `Media/video_edit/bin/` |

All of `Media/` is gitignored (public repo) — verify with `git check-ignore` before staging anything.

## Per-exercise recipe (~$3, ~10 min)

1. **START still** — `gemini-3-pro-image` via the runner, `--tier draft` (2K, $0.134),
   `--image Media/exercise-demos/_character/ai-dan-canonical.jpg`. Generate **2 candidates**.
   Prompt pattern (see `bw-squat/start-prompt-dan.txt`): "The EXACT same man as in the reference photo —
   reproduce his face with high fidelity (same facial structure, eyes, nose, smile lines, short
   black-and-gray faded haircut, skin tone), same black tank top with the white Abs by AI logo, same
   gym" + an explicit anatomical description of the start position (name every joint angle and contact
   point) + "full body visible head to feet, static tripod framing, 16:9, photorealistic, one person
   only". Side profile for hinge/squat moves; pick the camera angle that makes form legible.
2. **END still** — EDIT the chosen start still with the same model ("Edit this photograph. Keep the
   exact same scene… change ONLY his position…"). **State depth/range EXPLICITLY and aggressively** —
   "until his thighs are FULLY PARALLEL — hips at knee height, NOT a shallow half squat" was required;
   a polite "about 90 degrees" produced a half squat. Name what stays planted ("both feet remain
   completely FLAT in the exact same spot — heels never rise").
3. **QC stills yourself frame-level** (likeness vs canonical, joint angles, contact points, scene
   consistency) — Dan reviews finished videos in batch mode, but a wrong still is a 13¢ fix and a wrong
   video is $2.40, so gate hard here.
4. **ONE Veo leg, not two** — `google/veo-3.1` on Replicate: `image` = start still, `last_frame` = end
   still (both resized to exactly 1280x720 with `sips -z 720 1280`), `duration: 6`, `resolution:
   '1080p'`, `aspect_ratio: '16:9'`. Exact invocation: `bw-squat/run-veo-dan.js`. Motion prompt states
   the coupling ("feet stay planted… the camera and background never move").
5. **Extract the clean rep** — Veo obeys the ENDPOINTS but NOT the rep count: fast bodyweight tempo
   (~3s/rep) means a 6s clip contains ~2 reps, often with a bounce. **Sample frames at ≤0.5s intervals**
   (a sparse sheet lied twice), find one full cycle standing→bottom→standing, cut it with ffmpeg, then
   **diff the cut's first and last frames** and nudge the boundaries until the poses match (bw-squat
   took two recut iterations). Fallback if no clean cycle exists: palindrome (segment + its reverse,
   join at the zero-velocity bottom) — seamless by construction.
6. **Voiceover** — `minimax/speech-02-hd`, `voice_id: 'R8_NE3EBC2N'`, `speed: 1.0`, `emotion: 'auto'`.
   Script: **open with "Here's how to do the [exercise name]."** then 3–5 cues built from the
   exercise's `setup`/`execution`/`mistake` copy in `public/exercises.js`, `<#0.3#>` pauses between
   cues. Target 15–20s spoken. Pattern: `bw-squat/clone-dan-voice-v2.js`.
7. **Assemble** — loop the rep enough times to cover VO + ~1s lead-in + ~1s tail (`-stream_loop N-1`),
   then mux (`adelay=1000|1000`, `-c:v copy -c:a aac`). **Do NOT use `apad` or `-shortest` with
   filter_complex** — this Mac's static ffmpeg 6.0 hangs on the first and segfaults on
   `apad=whole_dur`. Build video first, mux plain.
8. **Deliver** — send the finished MP4 in chat (batch = a review set). Dan is the form authority;
   nothing ships unapproved.

### Static holds (plank, wall-sit, side plank…)
No rep to interpolate: generate ONE still of the hold, then a single short i2v clip ("holds the
position, subtle natural breathing, camera static") — Kling v3 i2v (~$1/5s) is fine here; keyframe
locking is unnecessary. Loop it under the VO the same way.

## Costs
2 stills $0.27 + 1 edit $0.13 + 1 Veo leg $2.40 + VO ~$0.01 ≈ **$2.85/exercise one-take, ~$3.50 with a
still retry**. State the estimated batch cost before running; the standing cap is $25/session unless
Dan authorizes more in the starter prompt.

## Traps (each cost real money or a redo — do not re-derive)
- Replicate's `google/nano-banana-pro` hard rate-limits (E003); the Google-direct runner is the door.
- Veo invents a DIFFERENT voice per clip — never use Veo native dialogue for library narration.
- The READY-FOR-UPLOAD YouTube videos have a continuous music bed; any future voice recloning must run
  demucs vocal isolation first (`ryan5453/demucs`, `stem:'vocals'` — see `bw-squat/reclone-v2.js`).
- Veo `image`+`last_frame` with plain i2v (no end frame) breaks physics mid-rep; with both frames it
  still ignores rep count — hence step 5.
- Dan's cue set for the squat: toes ABOUT PARALLEL (note: `public/exercises.js` says "toes slightly
  out" — unresolved discrepancy, flag when generating squat-family VO), ~90°, chest up/back flat, don't
  bend forward.
- Sparse QC frames (5–6 across 6s) missed a bounce twice; always sample ≤0.5s.

## Later phases (separate tasks, not this skill)
App integration (lazy `<video muted loop playsinline>` behind the stick-figure fallback, 3 call sites
of `getExerciseAnim` in `public/index.html` ~8010/8059/8137, iOS+Android retest — media in workout
cards is a native-retest trigger row), the "AI-generated demonstration" label, and hosting (repo is
public and `.git` is ~20 GB — likely a bucket/CDN, decision pending).
