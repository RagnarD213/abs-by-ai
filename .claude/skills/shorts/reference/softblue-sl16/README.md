# `softblue-sl16/`: SL-16 Intermittent Fasting shorts (R1, 2026-10-22 to 10-24)

Four Shorts from RO-08 (one 1080p roll, C1486, the 7/8 shoot; look D from the round 3 edit sheet). The `softblue-sl15/` recipe with
`A_pieces()` read from the film's edit-sheet EDL and the grade from `edit-sheet.json` `grade.per_roll`. Work folder:
`/Volumes/Extreme/_edit_work/SL-16/` (run from there; copies here). Raw roll is archived on Expansion (`lib.RAWD`).
Order: `snap.py` -> `batch.py audio, words` -> `chain_build.sh` (plan, track, gfx, proof) -> `chain_full.sh` (plan, track, gfx, render
+ deliver + watch) -> fresh `ra-reviewer` per Short (`REVIEW-BRIEF.md`) -> `rungate.sh S`. Page: `page_r1.py` (stills, transcripts).

## What this batch cost, and what would have avoided it
- **The render must rebuild the shot table.** `chain_full.sh` ran track/gfx/render only; a grade changed in `plans.py` never reached the
  file and a whole review round was spent finding it. `plan` is now the chain's first step. Any cover edit (grade, crop, in-point) needs it.
- **Old approved AI clips failed today's checks: 3 of 5.** RO-08's workday time-lapse (clock melts, laptop folds), fridge raid (box changes
  material, spray can from nowhere) and bar stool (watch appears, face smears, cartoon face from f50) all FAILED fresh frame reviewers,
  and their trimmed ranges failed again. Run `clipcheck_run.py` + a fresh `frame-reviewer` on every film AI clip at the shortlist step,
  before planning around it; replace with the film's real stock rather than spending rounds on trims.
- **Gamma lifts are not grades** (VIDEO-RULES 2026-10-23). Dark stock gets curves with true blacks: `plans.LAPTOP` measured p2/p50/p98
  0.031/0.431/0.887 against Dan's 0.018/0.449/0.924. A lifted dark mug read milky: swap to a brighter clip instead.
- **A panning stock clip will not hold in a fixed 9:16 window.** Measure the person mask on 10+ frames across the used range; a square
  card held the coffee-walk man where both fx 0.5 and fx 0.12 cut him.
- **Pick each clip's in-point from the words**, not the film's: the cold-brew pour, the coffee sip and the couple's faces all needed the
  in-point moved so the action lands on the line.
- **Captions:** "9 a.m. | like me" is not a new sentence (`batch.cmd_cues` now skips a.m./p.m.); a cut into B-roll right before a word
  blinked the caption off: put the cut in the gap after the word.
- **The two-line bar cannot hold a long quote** in the vertical: Tyson's full line wraps to three; keep the short form, captions carry it.
- **Gate false positive:** `junk:repeated_take` calls "if you wake up at nine ... if you wake up at seven" a restart. Reported, not tuned.
- **Edit `plans.py` with care:** replacing `...)` inside `...),  # comment` moves the comma into the comment (it broke the file twice).
