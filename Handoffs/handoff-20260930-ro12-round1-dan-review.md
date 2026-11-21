# RO-12 "Top 5 Zepbound Tips": round 1 delivered, next is Dan's notes

Written 2026-09-30 by Claude (Opus 5.5) after delivering the first full cut. Job doc: `Handoffs/video-editing/RO-12-top-5-zepbound-tips.md`.
Recommended model for the revision round: **Claude Opus 5.5, medium** (bounded revision on a working recipe; raise to high only if
Dan asks for new AI clips or a restructure).

## What exists
- Delivery: `claude edited long form content/09 - Top 5 Zepbound Tips/` (master `Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4`,
  `REVIEW 540p`, `.srt`, chapters, audio A/B, stamps, `notes-RO12.md`, both review reports, `recipe-RO12/`).
- Work dir: `/Volumes/Extreme/_edit_work/ro12/` (recipe in `recipe/`, outputs in `out/`, checks in `check/`, stock in `stock/`).
- Recipe: `edl.py` (kept source ranges, one line per passage with why), `plan.py` (every graphic and insert anchored to Dan's words),
  `build.py` (timeline / stills / picture / audio), `finish.py` (SRT from the delivered audio's own transcript, chapters, gate plan),
  `rebuild_r2.sh` (the whole chain), `deliver.sh`.

## Locks (reuse, do not redesign)
- Look: WV-01's 9/23 studio look. W2 `3552:1998:144:162`, T2 `2608:1466:616:184`, `wv01-edit/round2/recipe/grade-C.cube`.
- Audio B method: `voice_chain.py` fitted EQ on C1706 (`out/FIT.mp4.voice_chain.json`) + `bass=g=0.9:f=150`, no dereverb, bed at
  -50 dB (BED_TRIM -10; the quiet lav's +18.6 dB lift pushed the RO-05 bed level into the floor row). Audio gate 13/13 PASS.
- Graphics: Soft Blue Light, RO-05 title scene, Motivation lower thirds, 3A cards, RO-05's approved iPhone shell.
- Takes: see `notes-RO12.md` (intro take 3 for the "Zepbound" pronunciation; every restart verified by a verbatim listen).

## How to apply Dan's notes
1. Record his words verbatim in `round2-plan/decisions.json` with the delivered master's sha256.
2. Change only `plan.py` / `edl.py` entries he names (graphics are anchored to words, so timing follows the cut automatically).
3. `python3 recipe/build.py timeline`, `stills <IDs>` for every changed graphic, then `zsh recipe/rebuild_r2.sh` (about 60 minutes,
   two workers; check the two-build cap first). Gate, independent review, deliver with `recipe/deliver.sh`.

## Open for Dan (also in notes-RO12.md)
- Keep or cut his ad-lib at about 2:40 ("most of the time Zepbound comes in individual vials, so you just empty the entire vial").
- "WATCH NEXT" lower third at 8:32 points at RO-01 (not published yet): add the YouTube card at upload.

## Cost ledger
Generation $0. Gemini listening about $1.10 (editor) plus the reviewers' calls (under $2.30 together), standing quality-review authorization.

## Starter prompt
> Read `Handoffs/handoff-20260930-ro12-round1-dan-review.md`, then apply my notes on RO-12 "Top 5 Zepbound Tips": <paste notes>.
> Change only what I name, rebuild with the recipe, gate it, independent review, deliver the new review copy and update the master list.
