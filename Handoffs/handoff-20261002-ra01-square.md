# RA-01 "The AI Trick That Got Me Abs": make the 1:1 square for the trial campaign

Created 2026-10-02. Recommended: **Claude Opus 5.5, High** (secondary cut from an approved build).
Session name: `AI Got Me Abs AD R1`.

## Why

RA-01 is one of the six ads in the trial campaign `24316364155` (ad group `206348100928`). Today it runs as 16:9 (`OUw788sF1KY`,
ad `826595554299`) and 9:16 (`rfCsWNxuNV0`, ad `826595554302`). Dan counts horizontal, vertical, square and the short cutdowns
as ONE ad unit, so it needs the square.

**Only one file is owed.** Both approved RA-01 masters are 57.19 s, already under 0:59, so the 9:16 and 16:9 are their own
"59 s" versions and a separate cutdown would be a duplicate. Build ONE 1:1 at 57.19 s. (A hook variant is not part of this task.)

## Deliver

1. 1:1 (1080x1080), same edit as the approved 9:16, ≤ 0:59.

Name: `the ai trick that got me abs | claude | 1x1 | RA-01.mp4` in `Claude Ad Videos/the ai trick that got me abs - RA-01/`,
with REVIEW 540p copy, gate JSON, audio stamp, `notes-square.md`, `recipe-square/`.

## What a square is here

A 1080x1080 **re-layout of the approved 9:16 build**, not a new edit. It keeps the vertical's timeline, EDL (`cut.json`),
beats, grade, caption timing and audio **bit for bit** (the approved audio stays untouched: Dan approved it as-is on 09-18,
SHA-256 in `Docs/DGEN_CONVERSION_CAMPAIGN.md` "2026-09-18 RA-01"). Only geometry and per-beat renderers change.
The 9:16 build is a Claude build from raw (C1663), so there is no editor master to recover: start from its recipe.

## Read first

- `.claude/skills/_shared/VIDEO-RULES.md` in full, then `Handoffs/video-editing/00-RULES.md`.
- `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` (the square translation rules).
- `.claude/skills/shortad-from-longform/SKILL.md` [S1] START HERE and `reference/a11_sq_ad1/` (approved Ad 1 square template).
  Most recent approved square: Ad 3 R2.1 (`/Volumes/Extreme/_edit_work/ad3-sq-r2/`, `notes-square-r2.md` lists what Dan rejected in R1).
- `.claude/skills/_shared/framing-motion.md` (steady wider shots).
- `Handoffs/video-editing/RA-01-ai-trick-that-got-me-abs.md` and `RA-01-plan.md`; the build recipe
  `Claude Ad Videos/the ai trick that got me abs - RA-01/recipe-RA-01/REBUILD.md` (copy its scripts to a new work folder,
  e.g. `/Volumes/Extreme/_edit_work/ra01-sq/`; the old `/ra01/` stays untouched).
- Memory: `untagged-video-bt601-trap` (decode `accurate_rnd`), `framing-standard-hair-anchored`, `caption-trailing-entry-overprint`,
  `cutdown-seams-single-source`, `decision-budget-per-video`, `review-page-what-i-decided`.
- The RA-01 build is not an editor master in Soft Blue Light; check how its graphics (cards, chips, CTA pill) are made
  (`s06_assets.py`, `s11_cta.py`) before re-laying them for 1:1. The 9:16 uses a person-mask face box inside 8-92 % of the width:
  keep the same face-box rule at 1:1.

## Order of work

1. Copy the recipe and the 9:16 build inputs to the new work folder. Confirm the 9:16 still reproduces (frame count, hash of the audio mix).
2. Re-lay the geometry for 1:1 (framing, caption position and size, card rectangles, CTA pill). Claim the queue row first with
   `scripts/edit-queue/queue.py` (add an AS row for RA-01 if none exists).
3. Run every gate at the current `GATE_VERSION` on the delivered file, three fresh judges per the pre-render method,
   then an independent `ra-reviewer`.
4. Per Dan's 10-01 rule, if a 1:1 look decision is needed (graphics placement), show ONE short square look page first;
   otherwise build straight through.

## Done when

One file delivered with gate PASS and a reviewer SHIP, queue row DELIVERED, review copy linked in chat with a numbered action list.
Do NOT upload to YouTube or Google Ads: after Dan approves, `/ad-setup` uploads it Unlisted, sets its own thumbnail, and adds it to the
RA-01 ad group `206348100928` in campaign `24316364155`. Ads never go out organically. No em dashes.

## Starter prompt

> Read `Handoffs/handoff-20261002-ra01-square.md` and the files it lists. Name this session "AI Got Me Abs AD R1". Build the
> single 1:1 square of RA-01 (57.19 s, no separate cutdown) as a re-layout of the approved 9:16 build from its recipe, through
> every gate and an independent review, and send me the review copy with a numbered action list. Do NOT upload anything. No em dashes.

Model and effort: Claude Opus 5.5, High.
