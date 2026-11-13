# Real Exercise Demos, Batch 1: Gym AI replacements

**Type:** app asset (Trainer exercise demos; not content, not an ad). **Owner:** Claude Opus 5.5, high effort.
**Written:** 2026-11-13, after Dan approved the pilot and said: "Let's redo everything that we have B-roll with, with
real stuff, and only things we don't have B-roll with will be done with AI." **Job id:** `REALDEMOS-B01`.
**Outcome:** build, gate, review, then install in the app on Dan's approval.
Batches are independent and can run at the same time (edit cap 5); only the install step touches shared lines.

## The exercises

| app id | movement | main take (`*` = favorite) | detail angles | notes |
|---|---|---|---|---|
| `leg-curl` | Lying hamstring curl | B0626* | B0627, B0628, B0629, B0630 | Full range: heels well past 90 degrees toward the glutes; a 2-inch partial is a reject. Replaces the AI demo. |
| `cable-tricep-pushdown` | Bar tricep pushdown | B0651* | B0654, B0652, B0653 | Push to locked elbows, elbows pinned at the sides. Replaces the AI demo. |
| `seated-cable-row` | Wide-grip seated cable row | B0648* | B0649, B0650 | Handle touches the stomach (Dan's rule). The footage is a WIDE grip: script must say so. Replaces the AI demo. |
| `lat-pulldown` | Wide-grip lat pulldown | B0688 | B0662, B0663, B0664 | Watch the AI demo's old trap: a double-take at the bottom. Replaces the AI demo. |

## Read first (every batch)

1. `Handoffs/handoff-20261109-real-broll-exercise-demos.md`: the demo format ("real demo v1"), the new-exercise copy
   rule, and the **"Phase 0 result"** section (traps and tools). Dan approved the pilot on 2026-11-13 ("definitely
   better than the AI versions") and its three demos are installed; copy that recipe, do not reinvent it.
2. AGENTS.md "Exercise demos: real B-roll first" and `.claude/skills/_shared/VIDEO-RULES.md` (B-roll grade, hair
   clearance, demonstration timing, review page, silent checks).
3. Pilot code to copy: `Media/exercise-demos/real/` (`build.py` with `vo_at` / `vo_lines`, `make_plan.py`,
   `make_review.py`, `tools/`), finals and `LIBRARY.md` there. Copy into this batch's work folder; never edit the
   pilot's folder.

## How to run a batch (what made the pilot pass)

- `editcap.py acquire <JOB>`; work folder from `renderq.py workdir <JOB> --need 20` (internal drive). The Extreme drive
  must be mounted (library masters: `/Volumes/Extreme/_edit_work/SHOOT-20261023/library-masters/` for gym clips; home
  clips via each catalog entry's `source_path`).
- For each exercise: contact sheet of every listed clip, pick the cleanest steady take, then **measure rep phases**
  (`tools/track.py`, `refdist.py`, `shorts_y.py`, `frames.py`) before choosing cuts. Every cut joins the same phase on
  both sides; first and last frame are the same rest position; no look into the lens at a cut; hair never clipped where
  the source allows (defective-source clause otherwise, disclosed on the page).
- Script from the exercise's `setup` / `execution` / `mistake` copy in `public/exercises.js` (Dan's settled form
  standards in `/exercisegeneration` "Batch 2 revision round" win over the copy), matched to what the picture shows.
  Generate the cloned-voice VO (`gen.js`, about $0.01 each). Then write a **cue-to-phase table** (each line, its video
  time, the phase under it) and place lines with `vo_at`; shorten a line that is longer than the phase it names. Do this
  before the first independent review: in the pilot, cue timing caused three of four failed review rounds.
- Room tone amplitude 0.026 (not 0.004). Gates: `audio_gate.py --synthetic --profile in-app-demo` on both files, watch
  pass + `--judge`, `gate.py --format exercise-demo-real --plan plan.json` (plan from `make_plan.py`; add each new
  clip's camera angle to its `ANGLE` table). All must PASS.
- Independent review: a fresh `ra-reviewer` (Opus 5.5 high) per round, given the files and rules, not your conclusions.
  Fix and re-review until it passes.
- Review page on a new port with `review_server.py PORT DIR` (1080p, real demo beside the current AI demo where one
  exists, "What I decided" first, Start silent checks / Finish checks for owner handoff). Release the edit slot
  (`--review`) and stop for Dan.
- **After Dan approves:** install: copy each app encode + poster to `public/exercise-demos/<id>.mp4/.jpg`, add the id to
  `EXERCISE_DEMO_IDS` (if new) and to `EXERCISE_DEMO_REAL` in `public/index.html` (re-read the file first: other batches
  edit the same two lines), `node --check` the main script, `safe-push.sh`, confirm the Railway deploy, then verify on
  https://absbyai.com: open each exercise's sheet, real video plays with sound, poster shows, no AI-GENERATED chip; open
  one AI demo and confirm its chip is still there. Media in workout cards is a native-retest trigger: say so.
- Record each approved demo: clip library `add` (`--kind real --category exercise-demos --used-in "app trainer"`),
  mark source clips `used-final` + `intended_use: correct demonstration`, update `Media/exercise-demos/real/LIBRARY.md`
  (checksummed copies; that folder is on the Seagate, keep the work copy). Delete this batch's board entry and move its
  line in `Handoffs/README.md` OPEN out (executed).

## R1 result (2026-11-13, Claude): built, gated, reviewed; WAITING FOR DAN'S REVIEW

Review page: http://127.0.0.1:9513/ (port 9513; files `~/Projects/_edit_work/REALDEMOS-B01/review/`). Work folder
`~/Projects/_edit_work/REALDEMOS-B01/` (`out/<id>/`: `<id>-REAL-1080.mp4`, app encode `<id>.mp4` + `<id>.jpg`, `edit.json`,
stamps; reviews `ROUND-*-REVIEW*.md`; recipe `build.py`, `gates.sh`, `finish2.sh`). Nothing installed.

| id | cut | length | delivery gate | passed review |
|---|---|---|---|---|
| leg-curl | B0626 wide, B0628 rear close-up, B0626 wide | 15.9 s | PASS `exercise-demo-real` | round 6 |
| cable-tricep-pushdown | B0651 one continuous take (no clean detail clip) | 12.6 s | PASS `exercise-demo-real-onetake` | round 4 |
| seated-cable-row | B0648 wide, B0650 front close-up, B0648 wide | 13.3 s | PASS `exercise-demo-real` | round 3 |
| lat-pulldown | B0688 wide, B0662 rear close-up, B0688 wide | 15.5 s | PASS `exercise-demo-real` | round 3 |

Two form questions are first on the page and are Dan's call: pushdown elbows travel forward and up at the top of every
rep (the app's `mistake` copy names that), and the row torso leans back about 15 to 30 degrees on every pull (the app copy
says the torso stays tall). If he approves either as his form, change that exercise's `mistake` / `setup` copy in
`public/exercises.js` in the same deploy (row setup also says "neutral grip": the footage is a wide grip on a long bar).
If he declines one, keep its AI demo and add a strict version to `Docs/PICKUPS_NEXT_STUDIO_SHOOT.txt`.

**Next (after Dan's reply):** install only the ids he approves, exactly as "After Dan approves" above; then the clip
library records, `LIBRARY.md`, a checksummed copy of the recipe to `Media/exercise-demos/real/b01-recipe/`, remove the
review service (`review_server.py 9513 --remove`), delete the board entry and move this batch out of `Handoffs/README.md`
OPEN.

## Starter prompt

> Real Exercise Demos Batch 1 R1. Read `Handoffs/real-demos/batch-01-gym-ai-replacements.md` and build real-footage Trainer demos for leg-curl, cable-tricep-pushdown, seated-cable-row, lat-pulldown from the B-roll in the clip library, exactly as the approved pilot was built (Phase 0 result section of the master handoff). Pass every gate and an independent review, put them on a 1080p review page with the current AI demo beside each one, and stop for my review. Dan has authorized the whole batch, including installing the approved demos in the app and deploying.

**Model:** Claude Opus 5.5, high effort.
