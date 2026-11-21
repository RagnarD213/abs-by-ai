# RO-10 vertical, round 4: the full 9:16 and its 59 s cut (everything is locked)

Written: 2026-10-03 by the round 3 session. Recommended: Claude Opus 5.5, high.
Sidebar name: `Calories Reason LFC Vertical R4`. Continues `handoff-20261002-vertical-kit-round3-fill-more-screen.md`
(its Work 6) and `handoff-20261001-vertical-kit-round2-full-build-after-lock.md` (its Work 3 to 6). Read both for traps.

## Goal

Build the full RO-10 9:16 ("Calories: The Reason You're Not Losing Weight", 8:38, organic) and its 59 s cutdown from the
edit sheet with no hand edit, through the gate pre-check, three fresh judges, the fold, the cutdown and its gate, and
give Dan the review copies with wall-clock and AI cost beside the editor-master path (133 to 143 min, about 15 cents).

## What Dan decided (verbatim in `sbl-ro10/review/decisions.json`, `round3_answers`)

2026-10-03: *"I like the calmest one, the two-thirds calmer. That looks the best to me. All the graphics are approved.
Let's make this our standard way of centering for verticals going forward."*

| Question | Answer |
|---|---|
| Camera | CALMEST: `kit_track.py --tolerance 20`, now the default and the standing rule for verticals |
| Graphics look at 9:16 | Approved, all of it, including the new templates (title card, media card, CTA) |
| Proof film | He asked to "continue the edit in the next task": read as A, build RO-10 now, with the five ad-pacing rows marked not applicable to an organic film |
| Round 3 clips | No changes requested. Build with them as shown. H01 stays the wide card unless he says "H01 fill" |

Nothing is open. Do not ask Dan anything before the review copies exist.

## State (verified 2026-10-03)

- Build dir `/Volumes/Extreme/_edit_work/kit9x16/sbl-ro10/`. Sheet `/Volumes/Extreme/_edit_work/kit9x16/sheet-ro10/RO-10.edit-sheet.json`
  (re-hashed against the approved master on 10-02: OK). Work tree `~/abs-worktrees/kit-sheet` (push with plain git).
- Round 3 page `http://127.0.0.1:8808/` (`sbl-ro10/review3/`; restart `python3 <worktree>/.claude/skills/_shared/review_server.py 8808` there).
- Done: sheet, setup, audio, kit, base, track. `facetrack.json` is already the tolerance 20 track (copied from
  `facetrack.tol20.json`). `clip_overrides.json` holds Dan's 10 clip notes. `beats.json`, `content.json`, `assets.py`
  and `sheet_report.json` are the round 3 plan (5 fills, 13 side crops, P01 phone). Round 2 state: `round2-state/`.
- Rendered at the round 3 layouts: cards H01, C06, C07, C09, C10_1, C10_2, C11, C12, C14, P01 and fact cards G02, G04,
  G12. Label chips placed for O1 and O2. Captions (`captions.mov`) are from round 2 and still valid (no beat moved).
- Spend so far $0.69 (all small vision calls for the clip rule).

## Work

1. **Graphics, in full.** `vertical.py` changed in round 3, so every HyperFrames render is stale by its hash even
   though only 13 look different. Run `sbl_graphics.py --build B --sheet SHEET` with no `--only` (about 22 minutes on
   a quiet machine). Then `kit_deliver.py captions`.
2. **Clean one stale label.** H01 is a card now but its beat in `beats.json` and its entry in `label_place.json` still
   carry the full-screen chip from round 2 (`chip_png`, `chip_box`, `chip_label`). Remove them before `kit_plan.py`,
   or the plan lists a chip that is not drawn. The card's own chip is in `hf/plates.json` (`chip`).
3. **Gate stages on a sheet build** (never run yet): `kit_plan.py` (card chips from `hf/plates.json` `chip`, graphic
   regions from `hf/manifest.json` boxes, talking-head windows: talk beats only), prewatch, three fresh judges, fold.
   Run `gate.py` detached. No bound moves. The five ad-pacing rows that cannot apply to an 8:38 organic film
   (`flashes_per_min`, `cta_count`, `inserts_per_min`, `insert_coverage_hand`, `longest_talk_hand_s`) are
   `not_applicable` entries with a reason: that is a gate change, so a corpus run and a `GATE_VERSION` bump.
4. **Full picture and mux:** `kit_run.py --sheet SHEET --build B --name "calories the reason youre not losing weight | claude | 9x16 | RO-10" --from picture`.
5. **The 59 s cutdown** (`cutdown_pick.py`, `kit_cutdown.py`) and its gate. Fix findings in the kit, rerun.
6. **Deliver the review copies** on one page (first minute on top, "What I decided", one reply box), with wall-clock
   and AI cost beside the editor-master path. Then close the round 3 and round 2 handoff lines on the board and in
   `Handoffs/README.md`, and this one when Dan approves.

## Traps (new in round 3; the older ones are in the two handoffs above)

- **Another session has uncommitted edits to kit files in the MAIN project folder** (2026-10-03: `kit_plan.py`,
  `kit_run.py`, `kit_cutdown.py`, `kit_plan_cutdown.py`, `kit_fold.sh`, `cutdown_pick.py`, `kit_labels.py`,
  `sbl_graphics.py`, `render.py`). The work tree does not have them. Before Work 3, read `git -C "<main folder>" diff`
  on those files: part of the gate work may already exist there, and round 3 also changed `sbl_graphics.py`
  (`--only`), so whoever commits second has a merge. Do not overwrite their edits; coordinate on the board.
- `sbl_graphics.py` and `kit_labels.py` both rewrite `beats.json`. Never run them at the same time (round 3 lost
  O1's chip that way). Graphics first, then labels.
- A HyperFrames render started with `nohup ... &` from an agent shell dies when the shell returns
  ("render_cancelled_parent_exited"). Run it as a background task of the agent.
- The Extreme drive is 98 % full (about 100 GB free on 10-02). Check `df -h /Volumes/Extreme` before the full picture.
- The machine has run at load 50 to 140 all week. At most two builds at once; check `uptime` before timing anything.
- A tall card is never shrunk for captions: it runs under them (`media_card_scene`). If the gate reads captions over
  a card's picture as a collision, that is a plan question (declare the hole as picture, not a graphic region), not a
  reason to shrink the card.
- The main folder cannot push right now (`safe-push.sh` stops on another session's `shorts/SKILL.md` edits). Push
  skills from the work tree with plain git; if the main folder is still blocked, say so on the board, do not stack.
- Do not upload or publish. RO-10 is organic.

## Starter prompt

> Name this task `Calories Reason LFC Vertical R4`. Read `Handoffs/handoff-20261003-ro10-vertical-round4-full-build.md`
> and the two handoffs it names. Everything is locked: calmest camera, graphics approved, round 3 clips as shown.
> Re-render the graphics, make the gate stages run on a sheet build, then build the full RO-10 9:16 and its 59 second
> cut from the edit sheet with no hand edit, through the gate pre-check, three fresh judges, the fold, the cutdown and
> its gate. Send me the review copies on one page with the timing and cost against the old path. Do not upload
> anything. Explain the results in plain language.

Model and effort: Claude Opus 5.5, high.
