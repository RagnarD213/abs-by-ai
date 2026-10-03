# Codex: adopt the standard vertical centering (land on Dan, then hold)

**Written:** 2026-10-03 by Claude (Opus 5.5) at Dan's request. **For:** Codex. **Model:** GPT-6 Sol, medium (a bounded
change to how one crop is tracked, with a measured before and after; no creative choices).
Sidebar name: `Vertical Centering Codex Adopt`.

## Why

Dan watched two first minutes of the RO-10 vertical that differed only in how the crop follows him, and chose the
calmer one. His words, 2026-10-03: *"I like the calmest one, the two-thirds calmer. That looks the best to me... Let's
make this our standard way of centering for verticals going forward. I feel like this is better than what we were
doing."* He asked for Codex to adopt it in any vertical video it makes. Two days earlier he had called the old
tracking "excessive and distracting", and he does not want a crop that never moves either (he left the frame).

## The standard (already written into the shared docs)

Read `.claude/skills/_shared/framing-motion.md`, section **"Vertical talking head: land on him, then hold"**, and the
matching entry in `.claude/skills/_shared/VIDEO-RULES.md` ("Verticals: the camera lands on Dan, then holds"). In short,
for the talking-head crop of every 9:16 vertical:

1. Work per picture segment, never across a cut (a new take, a punch-in, a return from a graphic).
2. On the first frame after every cut the crop is centred exactly on his measured head centre.
3. The crop then does not move while his head centre stays within **3.3 % of the crop's width** of the crop's centre
   (20 px on a 608 px wide crop of a 1080-high base; 36 px in the delivered 1080-wide frame).
4. When he leaves that band, follow only far enough to keep him at its edge, eased over 0.75 s, never faster than
   28 % of the crop's width per second.
5. A segment where he wanders less than 6.6 % of the crop's width keeps one fixed centre.
6. Do not pull the end of a segment back to centre.

Scope: 9:16 verticals only. Squares keep the steadier per-shot rule in the same file. Horizontal 16:9 stays completely
static. The delivery gate and its thresholds do not change.

## What to look at

- The two clips Dan compared (540p review copies, same cut, same clips, only the camera differs):
  `/Volumes/Extreme/_edit_work/kit9x16/sbl-ro10/review3/first/AFTER - first minute 9x16 - camera 33 pct calmer - REVIEW 540p.mp4`
  (not chosen) and `.../CALMEST - first minute 9x16 - camera 68 pct calmer - REVIEW 540p.mp4` (chosen). Watch 0:06 to 0:31.
- The code: `.claude/skills/_shared/cut/landing.py`. `landing.track(n, raw_x, segments, slope_px_s=170, k=3,
  fixed_under=40, tolerance=20)` takes the raw head-centre samples and the picture segments and returns the crop
  centre per sample; `python3 landing.py selftest` proves 0 px landing error. The caller that uses it:
  `.claude/skills/shortad-from-longform/reference/kit9x16/kit_track.py` (`--tolerance` default 20). The px values are
  for a 608 px wide crop: scale them by your crop's width.
- What it measured on RO-10 (8:38, 25 takes) against the track that chased every movement: crop travel 10,758 to
  3,413 px (68 % less), p90 pan speed 62.9 to 22.8 px/s (64 % less), the crop moving 31 % of the time instead of
  50 %, him 17 px off centre at the median and 92 px at the worst moment.

## What to change

1. Codex skills `~/.codex/skills/abs-edit-ad/`, `abs-edit-organic/`, `long-form-content-edit/`, `vsl-edit/` and their
   copies under `Media/codex-video-trial/skills/`: wherever a vertical or 9:16 talking-head crop, face tracking,
   recentering or reframing is described or generated, point to the shared section above and state the six steps.
   Remove or mark as superseded any instruction to recenter continuously, and any instruction to hold one fixed centre
   for a whole vertical take regardless of how far he moves.
2. Any Codex script that computes a vertical crop track: call `landing.track` with the values above (scaled to the
   crop width), or reproduce the six steps exactly. Prefer calling the shared code so there is one copy.
3. Every vertical build reports four numbers in its build notes: total crop travel, p90 pan speed, share of time the
   crop is moving, and the median and maximum distance of his head centre from the crop centre.

## Verification

- `python3 .claude/skills/_shared/cut/landing.py selftest` passes.
- On ONE existing Codex vertical excerpt of at least 30 seconds of talking head, render before and after at the
  original frame rate, report the four numbers for both, and confirm by eye that the crop lands on him on the first
  frame after each cut and that his head never touches the frame edge. Do not rebuild, re-export or re-upload any
  approved or published video: the standard applies to new vertical builds and to verticals still in revision.
- Send Dan one short page or message: the before and after excerpt, the four numbers, and the list of skill files
  changed. No decisions are owed unless something could not adopt the method; then say which and why.

## Rules that still hold

- Work in a Codex worktree and push with plain git. The main project folder currently cannot push (another session's
  uncommitted `shorts/SKILL.md` edits stop `safe-push.sh`), so do not commit there.
- No em dashes in anything written. Plain language for Dan. Nothing is uploaded or published.

## Starter prompt

> Name this task `Vertical Centering Codex Adopt`. Read `Handoffs/handoff-20261003-codex-adopt-vertical-centering.md`
> and the shared section it names in `.claude/skills/_shared/framing-motion.md`. Adopt Dan's standard vertical
> centering (the crop lands on him after every cut, then holds until he is 3.3 % of the crop's width off centre) in
> every Codex skill and script that builds a 9:16 vertical, using the shared `landing.py`. Prove it on one existing
> vertical excerpt with a before and after and the four numbers. Do not rebuild or re-upload any approved video.
> Explain the result in plain language.

Model and effort: GPT-6 Sol, medium.
