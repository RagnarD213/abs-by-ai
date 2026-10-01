# Vertical kit, round 2: lock the 9:16 look, then the full RO-10 vertical + 59 s from its edit sheet

Written: 2026-10-01 by the session that built the sheet path (round 1). Recommended: Claude Opus 5.5, high.
Fire only AFTER Dan has answered the review page. Sidebar name: `Calories Reason AD-kit R2` (or as Dan names it).

## Where round 1 stopped

Review page (graphic lock, nothing is a full film): `http://127.0.0.1:8806/` served from
`/Volumes/Extreme/_edit_work/kit9x16/sbl-ro10/review/` (restart: `cd` there, `python3 -m http.server 8806`).
Dan owes five answers (the reply box on the page): 1 the 9:16 look, 2 AI clips card or fill, 3 stock clips whole or
square, 4 hard cut or flash, 5 proof film and which gate rows apply to an organic vertical.

## Read first

1. `.claude/skills/shortad-from-longform/reference/kit9x16/README.md` ("The second way in", sheet-path lessons)
2. `.claude/skills/_shared/edit-sheet/README.md`, `.claude/skills/_shared/hyperframes/README.md` ("9:16 layouts")
3. Memory `edit-sheet-and-kit-sheet-path`; `VIDEO-RULES.md`; `PRE-RENDER-APPROVAL.md`

## State (verified 2026-10-01)

- Work tree `~/abs-worktrees/kit-sheet` (branch `claude/kit-sheet`, merged to main). Build dir
  `/Volumes/Extreme/_edit_work/kit9x16/sbl-ro10/`: sheet stage through track done, all 43 graphics and plates
  rendered at 9:16 (`hf/`), captions built, first minute and one context clip per item in `review/`.
- Sheet: `/Volumes/Extreme/_edit_work/kit9x16/sheet-ro10/RO-10.edit-sheet.json` (facts file beside it). It was written
  from RO-10 round 2's master, whose approval is still PENDING, and that master has a known build fault (one repeated
  frame after seven cuts, its own review). If the RO-10 owner rebuilds or Dan asks for changes, REWRITE the sheet from
  the new master (`sheet_from_claude_build.py`, then `--approved "<Dan's words>"`) and rerun from `--from sheet`.
- Spend so far: $0. Wall-clock of the sheet path on RO-10 (8:38): sheet + plan 12 s, conform 5 to 8 min, track 45 s,
  graphics about 45 min (63 HyperFrames renders, the slow part), words 2 min, captions 1 min. Picture and mux not
  timed yet. The editor-master path was 133 to 143 min and about 15 cents.

## Work

1. Record Dan's answers verbatim in `sbl-ro10/review/decisions.json` (id, verdict, his words, scope).
2. Apply them: `kit_run.py --sheet ... --from sheet` passes nothing for clip treatment today; add `--ai-clips fill`,
   `--card-shape square`, `--flash` as kit_run pass-through flags to `sheet_to_kit.py` (they exist there). Any look
   note is fixed in the TEMPLATE or `vertical.py`, then `sbl_graphics.py` re-renders only what changed.
3. Make the gate stages work on a sheet build (not run yet): `kit_plan.py` (label tracks for card chips now come from
   `hf/plates.json` `chip`; graphic regions from `hf/manifest.json` boxes; talking-head windows: none), then
   prewatch, judges (three fresh sessions), fold. Run `gate.py` detached. Which format: per Dan's answer 5. No bound
   moves; a row that cannot apply is a `not_applicable` entry with a reason, and that is a gate change (corpus run
   for the ad entries, `GATE_VERSION` bump).
4. Full picture: `kit_run.py --sheet ... --from labels` (bleed chips only exist if answer 2 is B), then the cutdown
   (`cutdown_pick.py`, `kit_cutdown.py`) and its gate. Fix findings in the kit, rerun.
5. Deliver the review copies on a first-round review page that already shows the Soft Blue Light graphics, with wall-
   clock and AI cost next to the editor-master numbers.
6. Close the original handoff: remove `handoff-20261001-vertical-kit-from-our-own-edits.md` from the board and
   `Handoffs/README.md`, and this one.

## Traps

- At most two builds at once; RO-10 and RO-16 sessions also render on this machine.
- The 9:16 counter bar (lower third `bar`) has no layout yet; RO-10 has none. `vertical.py` stops on it.
- New templates (`title-card`, `media-card`, `cta`) are not approved until Dan passes the page.
- Do not upload or publish. RO-10 is organic (ends on "video", no tap-the-button CTA).

## Starter prompt

> Read `Handoffs/handoff-20261001-vertical-kit-round2-full-build-after-lock.md` and the files it lists. Dan's answers
> to the RO-10 vertical graphic-lock page are: [paste the reply box]. Record them, apply them, make the gate stages
> run on a sheet build, then build the full RO-10 9:16 and its 59 s cutdown from the edit sheet with no hand edit,
> through the gate pre-check, three fresh judges, fold, cutdown and deliver, and send me the review copies with the
> timing and cost against the old path. Explain the results in plain language.

Model and effort: Claude Opus 5.5, high.
