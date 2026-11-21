# Vertical kit, round 3: fill more of the screen (RO-10 9:16), then the full build

Written: 2026-10-02 by the round 2 session. Recommended: Claude Opus 5.5, high.
Sidebar name: `Calories Reason LFC Vertical R3`. Replaces `handoff-20261001-vertical-kit-round2-full-build-after-lock.md`
(keep it for the state, timings and traps; its Work items 3 to 6 move here).

## Goal

Apply Dan's 2026-10-02 clip notes and his new standing rule (fill as much of the screen as the clip allows), show him
one short page, and once he answers the three questions still open, build the full RO-10 9:16 and its 59 s cutdown
from the edit sheet through the gate and the judges.

## Read first

1. `.claude/skills/_shared/VIDEO-RULES.md`: "Verticals and squares: fill as much of the screen as the clip allows"
   (new, 2026-10-02) and the two clip rules under it.
2. `.claude/skills/shortad-from-longform/reference/kit9x16/README.md` ("The second way in", clip rule, calmer camera).
3. `kit9x16/clip_fit.py`, `sheet_to_kit.py`, `_shared/hyperframes/vertical.py` (`media_card_scene`).
4. `sbl-ro10/review/decisions.json` (`round2b` holds Dan's notes word for word and a per-clip table).
5. The round 2 handoff, for state, traps and the gate work.

## Where things stand

- Build dir `/Volumes/Extreme/_edit_work/kit9x16/sbl-ro10/`. Work tree `~/abs-worktrees/kit-sheet` (push with plain git).
- Round 2 page: `http://127.0.0.1:8807/` (`sbl-ro10/review2/`; restart `python3 -m http.server 8807` there).
  Round 1 page: `http://127.0.0.1:8806/` (`review/`).
- Round 2 built the three-step rule (6 fill, 12 square, 0 whole, phone whole) and the calmer camera
  (`kit_track.py --tolerance 6`, travel down 33 %; `--tolerance 20` rendered as CALMEST). Spend so far $0.55.
- **Dan's notes read like the ROUND 1 page** (he cites "Decision 2 B" and "Decision 3 B", and asks for a square on
  clips round 2 already made square). Apply each note against the round 2 state: some are already done, several go
  further than a square. Do not ask him which page he looked at; show the result.
- The RO-10 16:9 is now approved and queued (board, 2026-10-02). The sheet was written from the round 2 master while
  approval was pending: re-hash the delivered master (`validate.py --hash`). If it changed, rewrite the sheet
  (`sheet_from_claude_build.py`, `--approved "<Dan's words>"`) and rerun from `--from sheet`.

## Dan's notes, clip by clip (verbatim in decisions.json)

| Clip | Round 2 | What he wants |
|---|---|---|
| O1, O2 (AI opener) | square, fill | both fill the frame |
| H01 (man eating) | fill | wider than a fill: trim the spare space right of him and a little left of the Doritos bowl; "more square" |
| G02 (fact card photo) | 920 x 883 photo over the card | photo taller, as near full-screen vertical as the fact text below allows |
| C02 (salad table) | square | approved, "we need the stuff on the sides" |
| C04 | fill | approved |
| C05 (syringe) | fill | crop the left; square or as vertical as possible (check the round 2 fill already does it) |
| C06 (acai bowl) | square | crop left and right, more vertical |
| C07 (phone over food) | square | crop the left, more vertical, fill the screen |
| P01 (app demo) | phone card | slightly larger and higher, less empty space |
| C09 (mug) | square | crop left and right, fill more |
| C10_1 (salad toss) | square | crop left and right, about square |
| C10_2 (man eating) | square | crop the right, fill more |
| C11 (broth soup) | square | much more vertical; crop the left and a little right |
| C12 (chips) | square | crop all the spare left, a little right |
| C13 (candy), C15 (pills) | square | square |
| C14 (soda) | fill | nearly vertical |
| C03, C08 | square, fill | not mentioned: apply the standing rule |

## Work

1. **Make the crop continuous in `clip_fit.py`.** Today it picks one of three shapes. New behaviour: find the NARROWEST
   side crop that keeps what the clip is about, at any width between full screen (9:16) and the whole clip, placed on
   the subject. The `locate` call already returns the left and right edges of what must stay; use them as the crop
   (plus a small margin), clamp the shape to 9:16 at the narrow end, then verify that crop with the judge call and widen
   one step if it is rejected. A crop within about 10 % of full screen becomes a fill. Bias toward tighter: blank space
   needs a stated reason in `sheet_report.json`. Lessons that still hold: stack frames top to bottom when asking for a
   coordinate; cache per source span and prompt; never ask real-or-AI.
2. **Per-clip overrides for his exact notes** in `sbl-ro10/clip_overrides.json`. Extend the format to take a window:
   `{"C11": {"x0": 0.33, "x1": 0.80, "dan": "<his words>"}}` (fractions of the width), as well as `verdict`. Where the
   continuous rule already lands on what he asked, no override is needed; where it does not, the override wins.
   Check each result against his note by eye on the proof sheet before rendering.
3. **Cards any shape:** `media_card_scene` already sizes the hole from `ar`; pass the crop's shape (`ar` between 0.5625
   and 1.78) and its `ox`. Keep the card above the caption line (`CAP_TOP`), as large as the frame allows. A card
   taller than a square leaves no room above the captions: lift or pause the captions the way side cards do
   (`cap_lifts`), never shrink the card to fit them.
4. **P01:** a larger, higher phone (`max_h`, the vertical offset). **G02:** the before-card 9:16 layout in `vertical.py`:
   a taller photo with the chip and fact card kept below it; check the text still fits and nothing touches the captions.
5. **One short page (round 3)** in `sbl-ro10/review3/` on port 8808: only what changed (the clips, P01, G02), each with
   round 2 beside round 3, plus "What I decided". No first minute unless the opener changed materially (it does: O1
   becomes a fill, so include the first 10 seconds). Ask the three open questions in the reply box:
   camera AFTER or CALMEST; the graphics look (approved or notes); proof film (RO-10 now with the five ad-pacing rows
   marked not applicable, or wait for the next ad).
6. **After he answers, the full build** (round 2 handoff, Work items 3 to 6): `kit_plan.py` for a sheet build (card
   chips from `hf/plates.json` `chip`, graphic regions from `hf/manifest.json` boxes, talking-head windows: talk beats
   only), prewatch, three fresh judges, fold, cutdown and its gate, review copies, wall-clock and AI cost beside the
   editor-master path (133 to 143 min, about 15 cents). Run `gate.py` detached. No bound moves; a row that cannot apply
   is a `not_applicable` entry with a reason, a corpus run and a `GATE_VERSION` bump.
7. Write the continuous rule into the kit README and the `/shorts` and `/ad-edit` skills where they place horizontal
   clips. Close the round 2 handoff line on the board and in `Handoffs/README.md`.

## Traps

- At most two builds at once. On 2026-10-01 the machine ran at load 70 to 140 and `kit_labels.py` took 36 minutes for
  two chips; check `uptime` before timing anything.
- A change to `vertical.py` re-renders every HyperFrames graphic (about 22 minutes), not only the cards.
- Wait loops: `pgrep -f` matches its own shell. Use a bracket pattern (`build_medi[a].sh`) or a sentinel line in the log.
- Full-screen fills of AI clips carry the AI-GENERATED chip placed by `kit_labels.py` (slow: it validates on every frame).
- Do not upload or publish. RO-10 is organic.

## Starter prompt

> Name this task `Calories Reason LFC Vertical R3`. Read `Handoffs/handoff-20261002-vertical-kit-round3-fill-more-screen.md`
> and the files it lists. Apply Dan's 2026-10-02 clip notes and the new fill-the-screen rule: make the clip crop
> continuous (the narrowest side crop that keeps what the clip is about), fix each clip he named, enlarge the app demo
> and the G02 photo, and show me one short page with round 2 beside round 3. Ask me the three open questions on that
> page (camera, the graphics look, the proof film). Do not build the full film until I answer.

Model and effort: Claude Opus 5.5, high.
