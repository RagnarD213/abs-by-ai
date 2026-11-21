# Real Exercise Demos, Batch 6: Gym new exercises part 3

**Type:** app asset (Trainer exercise demos; not content, not an ad). **Owner:** Claude Opus 5.5, high effort.
**Written:** 2026-11-13, after Dan approved the pilot and said: "Let's redo everything that we have B-roll with, with
real stuff, and only things we don't have B-roll with will be done with AI." **Job id:** `REALDEMOS-B06`.
**Outcome:** build, gate, review; approved demos are STORED for Dan's library change, not installed.
Batches are independent and can run at the same time (edit cap 5); only the install step touches shared lines.

**Read first, before the sections below (2026-11-13):** the master handoff's "Batch 1 result" section and
`batch-02-gym-machines-new-coverage.md` "How to run this batch". They replace the pilot recipe below wherever they differ
(exact-frame cuts, turnaround trackers, loop seam, line lengths, detail-clip screening, one queued step, `dan-filmed`
category, recipe folder `~/Projects/_edit_work/REALDEMOS-B01/`).

## The exercises

| app id | movement | main take (`*` = favorite) | detail angles | notes |
|---|---|---|---|---|
| `machine-lateral-raise` | Machine Lateral Raise | B0673* | B0674 to B0677 |  |
| `cable-overhead-tricep-extension` | Overhead Rope Triceps Extension | B0716, B0715 | B0717, B0718, B0719 | Upper arms stay vertical, elbows narrow. |
| `preacher-curl` | Preacher Curl | B0695*, B0696 | B0687 |  |
| `bb-curl` | Straight-Bar Curl | B0683* | B0684, B0685, B0686 | Elbows tucked, no hip swing. |
| `rope-hammer-curl` | Rope Hammer Curl | B0720 | B0721, B0722 |  |

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
- **After Dan approves:** store, do not install: these exercises are not in `public/exercises.js` yet (Dan is changing the library). Keep
  finals in `Media/exercise-demos/real/<id>/` and write each exercise's ready-to-paste entry (id, name, equip, cat,
  muscles, setup, execution, mistake, swap) in `Media/exercise-demos/real/NEW-LIBRARY-ENTRIES.js`; show that copy on the
  review page beside each demo so Dan approves words and video together.
- Record each approved demo: clip library `add` (`--kind real --category exercise-demos --used-in "app trainer"`),
  mark source clips `used-final` + `intended_use: correct demonstration`, update `Media/exercise-demos/real/LIBRARY.md`
  (checksummed copies; that folder is on the Seagate, keep the work copy). Delete this batch's board entry and move its
  line in `Handoffs/README.md` OPEN out (executed).

## Starter prompt

> Real Exercise Demos Batch 6 R1. Read `Handoffs/real-demos/batch-06-gym-new-exercises-part-3.md` and build real-footage Trainer demos for machine-lateral-raise, cable-overhead-tricep-extension, preacher-curl, bb-curl, rope-hammer-curl from the B-roll in the clip library, exactly as the approved pilot was built (Phase 0 result section of the master handoff). Pass every gate and an independent review, put them on a 1080p review page with the current AI demo beside each one, and stop for my review. Dan has authorized the whole batch, including storing the approved demos and writing their library copy.

**Model:** Claude Opus 5.5, high effort.
