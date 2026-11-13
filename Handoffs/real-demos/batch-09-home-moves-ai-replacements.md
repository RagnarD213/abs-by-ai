# Real Exercise Demos, Batch 9: Home moves AI replacements

**Type:** app asset (Trainer exercise demos; not content, not an ad). **Owner:** Claude Opus 5.5, high effort.
**Written:** 2026-11-13, after Dan approved the pilot and said: "Let's redo everything that we have B-roll with, with
real stuff, and only things we don't have B-roll with will be done with AI." **Job id:** `REALDEMOS-B09`.
**Outcome:** build, gate, review, then install in the app on Dan's approval.
Batches are independent and can run at the same time (edit cap 5); only the install step touches shared lines.

## The exercises

| app id | movement | main take (`*` = favorite) | detail angles | notes |
|---|---|---|---|---|
| `bw-squat` | Bodyweight squat | B0460, B0464, B0475 | none | No demo installed today; new coverage. |
| `battle-ropes` | Battle ropes | B0457 | none | New coverage (continuous movement). |
| `pushup` | Push-up | B0547, B0461 | none | Replaces the AI demo. |
| `knee-pushup` | Knee push-up | B0433 | none | Replaces the AI demo. |
| `db-shoulder-press` | Dumbbell shoulder press | B0449 | none | Seated (matches Dan's standard), bottom just below 90 degrees. Replaces the AI demo. |
| `db-curl` | Dumbbell curl | B0432, B0031 | none | Elbows tucked, torso vertical. Replaces the AI demo. |
| `db-lateral-raise` | Side lateral | B0450 | none | Check against Dan's 'Side Lateral' pour standard (elbows lead, finish slightly above shoulder height, pinky up). If the footage misses it, hold this one and keep the AI demo. Otherwise replaces it. |

**Home/poolside footage (Dan is shirtless by the pool; the AI demos are in the gym).** Dan's 2026-11-13 rule replaces the
earlier "home replaces AI only after a side-by-side" default: real replaces AI wherever footage exists. Still put the
current AI demo beside each real one on the review page. These clips are 16:9 at about 4-11 s each, so a demo may need
two takes or angles; never slow down or reverse a rep. **Grade check:** the B-roll rule applies ("never raw footage";
B0455, B0456 and B0434 carried a LUT and still read very dark). Match each clip's black share, median saturation and
brightness to approved pool B-roll from the same shoot and look at stills side by side before building.

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

## Starter prompt

> Real Exercise Demos Batch 9 R1. Read `Handoffs/real-demos/batch-09-home-moves-ai-replacements.md` and build real-footage Trainer demos for bw-squat, battle-ropes, pushup, knee-pushup, db-shoulder-press, db-curl, db-lateral-raise from the B-roll in the clip library, exactly as the approved pilot was built (Phase 0 result section of the master handoff). Pass every gate and an independent review, put them on a 1080p review page with the current AI demo beside each one, and stop for my review. Dan has authorized the whole batch, including installing the approved demos in the app and deploying.

**Model:** Claude Opus 5.5, high effort.
