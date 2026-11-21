# Handoff: Exercise demo videos — 3-exercise review batch, then the remaining ~93

**Written:** 2026-08-19 · **Author:** Claude Code (the session that locked the recipe)
**Status:** READY TO EXECUTE. The pipeline is fully proven and Dan-approved on `bw-squat`
(`Media/exercise-demos/bw-squat/bw-squat-AIDAN-narrated.mp4` — AI-Dan likeness, logo tank, canonical
gym, his cloned voice). Everything repeatable is captured in the **`/exercisegeneration` skill**
(`.claude/skills/exercisegeneration/SKILL.md`) — invoke it first; this doc only adds batch scope and
sequencing.

## Dan's explicit instruction (2026-08-19)
**Batch 1 = THREE exercises only, delivered as a review set for his eyeball. STOP after three.**
Only after he approves the batch does the follow-on work (the remaining ~93) run, in subsequent
sessions. He was near his usage limit when he ordered this — keep the session lean.

## Batch 1 scope — recommended picks (executor may swap with reason)
Chosen to stress three different pose classes so his review covers the recipe's range, not three
near-identical squats:
1. **`pushup`** — floor-horizontal movement (tests camera angle + floor contact physics).
2. **`reverse-lunge`** — asymmetric stance with a stepping motion (tests the extract-clean-rep step on
   a move whose "loop" involves a step back and return).
3. **`plank`** — static hold (tests the skill's static-hold variant: one still + Kling i2v breathing
   clip, no keyframe pair).

All three are `equip: 'none'`, `cat` variety (push / legs / core), copy in `public/exercises.js`.

## Per-exercise procedure
Follow `/exercisegeneration` exactly. Summary: 2 start-still candidates from
`Media/exercise-demos/_character/ai-dan-canonical.jpg` → depth-explicit end-still edit → self-QC at
frame level → ONE Veo 3.1 `image`+`last_frame` leg (1280x720 inputs, 6s) → extract one clean rep
(sample ≤0.5s, diff the loop-join frames) → VO in voice `R8_NE3EBC2N` opening "Here's how to do the
[name]." + cues from the library copy → loop + mux → send the three finished MP4s together.

## Budget
~$3.50/exercise with retries → **batch 1 ≈ $9–12, inside the standing $25/session cap.** State the
estimate before generating. The full remaining library (~93 more) is ~$280–330 total across follow-on
sessions; Dan sizes those batches when he green-lights them.

## Definition of done (batch 1)
- Three finished narrated MP4s sent to Dan in one message, each: likeness matches the canonical still,
  form correct at frame level, loop seam clean, VO opens with the intro line, 15–25s.
- Working files under `Media/exercise-demos/<id>/` (gitignored — verify).
- AI_COORDINATION.md updated; this handoff's dashboard task **checked off only when Dan approves the
  batch** (Rule 9 completion bar is his approval, since the deliverable IS the review set).
- Do NOT start the remaining 93, app integration, labels, or hosting — separate tasks.

## Open items that ride along (flag, don't fix)
- `public/exercises.js` bw-squat setup says "toes slightly out"; Dan's approved VO says "toes about
  parallel" — he hasn't ruled which wins. Flag if a squat-family exercise lands in a batch.
- Hosting decision for ~100 MP4s (public repo, ~20 GB .git) — pending, blocks app integration only.

## Model/effort recommendation
- **Low usage: Claude Fable 5 (or Opus 5), medium effort.** The load-bearing skill is frame-level
  visual QC — wrong sled/foot/joint geometry caught at the 13¢ still stage instead of shipping wrong
  form. Both pilot failures were caught only visually.
- **High usage: Claude Sonnet 5 standard is acceptable** now that the recipe + prompt patterns are
  written down, but it MUST still do the frame-level QC honestly and stop at 3 exercises.

## Starter prompt (paste into a new session)
> Execute Handoffs/handoff-20260819-exercise-demo-batch1.md — generate the 3-exercise review batch
> (pushup, reverse-lunge, plank) using the /exercisegeneration skill. Budget: up to $15 this session.
> Stop after sending me the three finished videos.
