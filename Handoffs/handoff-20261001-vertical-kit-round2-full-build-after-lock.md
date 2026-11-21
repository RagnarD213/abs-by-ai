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

## Dan's answers so far (2026-10-01, verbatim in `sbl-ro10/review/decisions.json`)

- **Clips (decisions 2 and 3): one three-step rule for every horizontal clip.** Fill the phone frame by default; if
  that cuts something critical at the sides (or cuts body parts), the centre square; if the square still cuts too
  much, the whole clip in a card. His examples: O2 (man on the scale) fills; C02 (overhead salad) is a square. Now in
  `VIDEO-RULES.md`. Build it into `sheet_to_kit.py` in place of `--ai-clips` / `--card-shape`: for each clip compare
  the three crops and pick the tightest that loses nothing critical. The person-mask extent alone is NOT enough (it
  read C02 as 90 % wide and O2 as 35 %): use a cheap vision call on the three candidate crops through `ai_calls.py`
  (ledgered, a fraction of a cent each; real-or-AI labels stay facts from the sheet), and record each verdict and its
  reason in `sheet_report.json`. Show Dan all 19 clips' results on the round 2 page.
- **Transitions (4): hard cut.** Already the default.
- **New: calm the camera.** The crop that follows him has become "excessive and distracting"; he wants about 30 %
  less movement with more tolerance for being off centre, without going back to no movement (where he left the
  frame). Do it in this job: `kit_track.py` (`--slope` 170 px/s, `--fixed-under` 40 px) and the shared smoother
  `_shared/cut/landing.py`. Measure total crop travel and p90 pan speed on RO-10 before and after (round 1: p90
  67 px/s, 0 of 25 takes held fixed), aim for about 30 % less, keep his head inside the frame on every sample and the
  gate's framing rows passing, and show the first minute before and after. `landing.py` is shared with `/shorts`:
  check who else calls it and say so; a gate-measured change needs the corpus entries that exercise framing.
- **Still open: 1 (the 9:16 look of the graphics) and 5 (proof film and which gate rows apply).** Dan's 10-01 evening
  message left both as unfilled brackets. They are asked again on the round 2 page with two new ones (below).

## Round 2a, done 2026-10-01 evening (clip rule + calmer camera; no full film)

Page: `http://127.0.0.1:8807/` from `sbl-ro10/review2/` (restart: `cd` there, `python3 -m http.server 8807`). First
minute before / after / calmest, the camera numbers, and all 19 clips with verdict, reason and the three crops.

- **Clip rule built:** `kit9x16/clip_fit.py`, called by `sheet_to_kit.py` (the `--ai-clips` / `--card-shape` flags are
  gone). RO-10: 6 fill (O2, H01, C04, C05, C08, C14), 12 square, 0 whole, P01 phone. Dan's flips go in
  `sbl-ro10/clip_overrides.json` `{"C08": {"verdict": "square", "dan": "<his words>"}}`, then `--from sheet`.
- **Calmer camera built:** `landing.py` `tolerance` (off by default; `facetrack3.py` / `facetrack4.py` unchanged),
  `kit_track.py --tolerance` default 6 px. RO-10 travel 10,759 to 7,194 px (-33 %), p90 pan 62.9 to 36.4 px/s (-42 %).
  `--tolerance 20` (-68 % / -64 %) is rendered as the CALMEST option. Tracks: `facetrack.tol0/6/20.json`.
- **Dan owes four answers:** 1 camera (AFTER / CALMEST), 2 clip flips by ID, 3 the graphics look, 4 the proof film.
- Round 1 state of the build is in `sbl-ro10/round1-state/`. Spend $0.55 (clip rule tuning; one pass is about 11 cents).
- Timing note: the machine ran at load 70 to 140 all evening (four sessions). Conform 573 s, graphics 321 s, and
  `kit_labels.py` 2,152 s for two chips (normally about 2 min). Do not put that labels number in the timing table.
- NOT started: Work items 3 to 6 below (gate stages on a sheet build, the full film, cutdown, delivery).

## Work

1. Record Dan's answers verbatim in `sbl-ro10/review/decisions.json` (id, verdict, his words, scope).
2. Apply them: clip flips in `clip_overrides.json`; the camera choice is `kit_track.py --tolerance` (make CALMEST the
   default there if he picks it). Any look note is fixed in the TEMPLATE or `vertical.py`, then `sbl_graphics.py`
   re-renders only what changed.
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

> Name this task `Calories Reason AD-kit R3`. Read `Handoffs/handoff-20261001-vertical-kit-round2-full-build-after-lock.md`
> and the files it lists. Dan's answers to the round 2 page (http://127.0.0.1:8807/) are: [paste the reply box: camera,
> clip flips, the graphics look, the proof film]. Record them, apply them, make the gate stages
> run on a sheet build, then build the full RO-10 9:16 and its 59 s cutdown from the edit sheet with no hand edit,
> through the gate pre-check, three fresh judges, fold, cutdown and deliver, and send me the review copies with the
> timing and cost against the old path. Explain the results in plain language.

Model and effort: Claude Opus 5.5, high.
