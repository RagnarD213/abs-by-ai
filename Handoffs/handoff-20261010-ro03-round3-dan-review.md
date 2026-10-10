# RO-03 "The Vacuum: Workout Only": the full film is with Dan (2026-10-10)

**CONTENT, long-form (LFC). Task name for the next session: `Vacuum Workout Only LFC R3`.**
Skill: `/longform-edit`. Recipe and every trap: `.claude/skills/longform-edit/reference/ro03/README.md` (read it first).

## Where it stands

Round 2 is delivered: the full 2:31.6 film, built from the round 1 plan with nothing changed (the one 8/14 hold three
times, no footage from another shoot). Dan has not replied. Not finalized, not uploaded.

- Review page: `http://127.0.0.1:8877/` (folder `/Volumes/Extreme/_edit_work/ro03/round2/`, generator `recipe/page2.py`).
- VLC copy: `Videos to Review/Vacuum Workout Only LFC R2 - full film.mp4`.
- Delivery: `claude edited long form content/13 - The Vacuum Workout Only/` (master sha256 b18ceaf6...2a7b, SRT,
  chapters, edit sheet, stamps, `notes-RO03.md`, `ROUND-2-REVIEW.md`, `recipe-RO-03/`).
- Work dir: `/Volumes/Extreme/_edit_work/ro03/`. The reviewed first render is in `round2/candidate1/`.

## What Dan was asked (two calls, my pick first)

1. **Set 3.** As planned it is set 1 again (same far picture to hold +11.5 s, same near picture after) and it ends on
   him ducking to his phone, 0.7 s later than sets 1 and 2. A: recut set 3 only. B: leave it.
2. **Capitals.** All six lower thirds carry a FULL CAPS word (HARD twice) against his 10-09 rule (about one in six).
   A: title case on five, keep "Start With ONE Set Every Morning." B: keep as approved.

Offered, no answer needed: lift the three phone-timer beeps (18 dB under the music).

## What to do with his reply

- **Both B, or "finalized":** nothing to render. Record his words in `round2-plan/decisions.json` and in the watch
  log (the one open defect, the end of set 3: `disposition: accepted_by_dan` with his words), re-run `sheet.py` with
  `--approved "<his words>"`, `queue.py set RO-03 finalized`, delete the board entry, delete the VLC copy, remove the
  page service (`review_server.py 8877 --remove`), register the opening clip decision in the notes. Then `/video-setup`
  is its own task.
- **1 A (recut set 3):** in `recipe/edl.py` end piece `set3` at source frame 1666 (as sets 1 and 2; now 1687). In
  `recipe/shots.py SETCUT` and `build.FORCE` give set 3 three shots: far from its start to hold +8.7 s (lower third G05
  runs hold +2.0 to +8.6 and must stay on the far framing), near to hold +14.3 s, far to the end. Lay the three sets'
  size schedules side by side on the hold's clock before rendering: no two sets should match for more than about 9 s
  and set 3 must not end on the near grin. Then the README's round 1 order from `edl.py` on (the outro and sign-off
  move 21 frames earlier; `resolve.py` re-times K00 and G06; `build.py audio` remixes the film once), the round 2 order
  from `render_range`, a fresh `ra-reviewer`, the gates. Prove everything before 1:46 is unchanged against
  `round2/RO03_MASTER.mp4` frame by frame. The remix will not be sample identical to round 2: report the difference.
- **2 A (capitals):** change `point` / `parts` in `recipe/plan.py` for G01 to G05 to title case ("Suck It In As Hard As
  You Can.", "Between Sets, Take Deep Belly Breaths.", "Belly Button Through Your Spine.", "Take Short Breaths Through
  Your Nose.", "Keep Pulling In. This Should Be Hard."), `from_plan.py --render`, new stills for the page.
- Any other note: apply it, show only what changed (later rounds are lighter).

## Gate status, stated honestly

Delivery gate 2.5.1 on the delivered file: FAIL, 32 of 39 rows pass. Audio gate on the whole film: FAIL on 4 rows
(the holds are music only); on the talking sections alone: PASS on every row. The seven delivery rows and why are in
`notes-RO03.md`. Independent review: DOES NOT SHIP on the first render (one-frame "31" on the rest chip: fixed and
confirmed by a second judge; the end of set 3: Dan's call 1; the stamps). Nothing was tuned.

## Cost

$0. Cap $5.

## Recommended model and effort

Claude Opus 5.5, medium. A small re-render or a bookkeeping pass, plus one reviewer.

## Starter prompt

> CONTENT (LFC). Rename this task `Vacuum Workout Only LFC R3`. Read `Handoffs/handoff-20261010-ro03-round3-dan-review.md` and `.claude/skills/longform-edit/reference/ro03/README.md`, then apply my reply to round 2 of RO-03 "The Vacuum: Workout Only" with /longform-edit. My reply: [paste your reply from the review page here]. Show me only what changed, re-run the gates and one independent review, and update the edit queue.
