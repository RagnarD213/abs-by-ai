# RO-17 "3 Healthy Foods That Made Me Fat": round 2, bring the stalled draft up to the current standard and get Dan's picks

**LFC (long-form content, 16:9).** Sidebar name: `3 Healthy Foods LFC R2`.
Written 2026-10-08 by Claude (Opus 5.5) from a planning session. Recommended: **Claude Opus 5.5, high effort.**
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`,
`.claude/skills/_shared/PRE-RENDER-APPROVAL.md` (the round method), `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/_shared/SOFTBLUE.md`, `.claude/skills/_shared/hyperframes/`, the job doc
`Handoffs/video-editing/RO-17-3-healthy-foods-that-made-me-fat.md`, and memories `review-page-what-i-decided`,
`graphic-lock-and-ai-frames-first`, `decision-budget-per-video`, `clip-library`.

## Why this exists

RO-17 was the Phase 2 queue pilot. Stage one ran unattended on 2026-09-25, made a full placeholder draft and stopped for
Dan's choice on five stock clips. Dan never saw a review page for it, the queue was paused on 09-24, and the job has sat as
"DRAFT: asset choices waiting for Dan" since. The pilot's own goal (proving the queue's placeholder flow) is no longer the
point. The point now is to finish the video.

The draft is also older than most of the current standard: Soft Blue Light graphics and the HyperFrames templates
(09-27, 09-30), the review page format with "What I decided" (09-30), the clip library (09-29), the AI opener rule
(09-27) and the round method. So do not just swap five clips into the old draft and call it final.

## What exists (all in `/Volumes/Extreme/_edit_work/RO-17/`, never overwrite; build in `round2/`)

- `RO-17-3-Healthy-Foods-That-Made-Me-Fat-DRAFT.mp4` (1080p, about 7:41, sha256 `c00e7fd1...a051` in `DRAFT-DELIVERY.json`)
  and `RO-17-REVIEW-540p-DRAFT.mp4`.
- `notes.md` (the take and cut choices), `SCENE_PLAN.md`, `WATCH-LOG.md`, `notes-audio.md`, `recipe-ro17/`, `RO-17-subtitles.srt`.
- `placeholders.json`: five free Pexels clips, all pending, each 6.006 s: trail mix, dried fruit, coconut water,
  hard-boiled egg, rotisserie chicken. Sources in `assets/raw/`.
- Source roll C1713 (9/23 shoot). Opening take from 00:54.68, wrap from 10:45.58. Spoken Chipotle price is about $7; the
  written $4 never goes on screen.

## Keep from stage one (re-verify, do not redo)

The take selection and dialogue cut, the lav pull (`pan=mono|c0=0.5*c0+0.5*c1`, stream 0), and the subtitle text. Re-run
the current audio gate and the current cut-continuity check on them; stage one passed the 09-25 versions only. Dan has
approved none of it yet.

## Redo to the current standard

1. **Graphics:** the draft uses Muhammad-style pills, stacks and chips. Rebuild every graphic in Soft Blue Light with the
   approved HyperFrames templates (lower-third, side-list, before-card), text landing on the spoken word.
2. **Framing and grade:** stage one used one static crop per cut. Apply the current framing standard (hair-anchored,
   NEAR/FAR punch-ins that hide the cuts) and check the grade against the current 9/23-shoot recipe used on RO-10 to RO-13.
3. **B-roll:** five stock inserts in 7:41 is thin. Search the clip library first (`clip_library.py find`) for owned
   footage of each food and for Dan eating or shopping, before keeping any Pexels pick. No source repeats.
4. **Opener:** look for an AI opener that is specific to this story. If one fits, make START and END frames only (Codex
   subscription, `codex-image.sh`); no AI motion until Dan approves the frames.

## Deliver this round, then stop

One review page in the standard format (`review_server.py`, three items per row): the rebuilt first minute, the opener
frame pair if there is one, "What I decided", every graphic as a still in context, and every B-roll clip moving in its
slot with one alternative where a real choice exists. Keep Dan's total decisions for the whole video inside 10 to 15.
**No full film this round.** Write a short round-2 review handoff with the page address and a starter prompt for round 3
(full film after his picks).

## Limits

- Max two video builds on the machine. Check the board before starting: RO-11 and Codex's WV-01 B were both building on
  10-08. If two are running, do the planning and library search first and render when a slot frees.
- The overnight queue stays paused. Do not use `dispatcher.py launch-one` or `resume`; run this by hand. Set the job state
  with `scripts/edit-queue/queue.py` so the master list and the Edit Queue page stay right.
- Spend: $5 AI-motion cap for the video, none this round. No upload, no setup, no shorts (SL job comes after approval).

## Starter prompt

> CONTENT (LFC). Name this task `3 Healthy Foods LFC R2`. Read and execute
> `Handoffs/handoff-20261008-ro17-round2-current-standard-review-page.md`. Keep the stage-one cut and audio after
> re-checking them, rebuild the graphics, framing and B-roll to the current standard, and show me one review page with
> the first minute, the graphics and the clip choices. Use the Codex subscription to generate any images. No full film
> until I have picked.
