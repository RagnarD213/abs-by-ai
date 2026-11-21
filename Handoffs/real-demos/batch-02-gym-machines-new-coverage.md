# Real Exercise Demos, Batch 2: Gym machines new coverage

**Type:** app asset (Trainer exercise demos; not content, not an ad). **Owner:** Claude Opus 5.5, high effort.
**Written:** 2026-11-13, after Dan approved the pilot and said: "Let's redo everything that we have B-roll with, with
real stuff, and only things we don't have B-roll with will be done with AI." **Job id:** `REALDEMOS-B02`.
**Outcome:** build, gate, review, then install in the app on Dan's approval.
Batches are independent and can run at the same time (edit cap 5); only the install step touches shared lines.

## The exercises

| app id | movement | main take (`*` = favorite) | detail angles | notes |
|---|---|---|---|---|
| `pec-deck` | Chest fly machine | B0665* | B0666, B0667, B0668 | New coverage (no demo today). |
| `machine-chest-press` | Chest press machine | B0678* | B0679, B0680, B0681 | New coverage. |
| `machine-row` | Chest-supported T-bar row | B0723* | B0644, B0724, B0725 | The app's machine-row copy may describe a different machine: match the script to the T-bar row shown, and flag the copy mismatch for Dan. New coverage. |
| `machine-rear-delt-fly` | Rear delt fly, reverse pec deck | B0670*, B0669 | B0671, B0672, B0689, B0690 | New coverage. |

## Read first

1. `Handoffs/handoff-20261109-real-broll-exercise-demos.md`: "The demo format (real demo v1)" and the **"Batch 1 result"**
   section. Batch 1 (leg curl, pushdown, seated row, lat pulldown) was approved and installed on 2026-11-13 after six
   review rounds; that section lists every avoidable failure. Read it before looking at a single clip.
2. AGENTS.md "Exercise demos: real B-roll first" and `.claude/skills/_shared/VIDEO-RULES.md` (B-roll grade, hair
   clearance, demonstration timing, review page, silent checks, render queue).
3. **Copy the Batch 1 recipe, not the pilot's:** `~/Projects/_edit_work/REALDEMOS-B01/` (work copy) or the checksummed
   archive `Media/exercise-demos/real/b01-recipe/` (`SHA256.json` lists it; the folder is on the Seagate). Files:
   `build.py` (shots by exact source frame, `vo_pick` / `vo_at`), `make_plan.py`, `make_review.py`, `gates.sh`,
   `finish2.sh`, `REVIEW-BRIEF.md`, `tools/` (`edge.py` weight-stack tracker, `csheet.py` exact strips, `colorzone.py`,
   `energy.py`, `frames.py`), `vo/gen.js`. Copy into this batch's work folder and change the ids; never edit Batch 1's.
   The passing reviews (`ROUND-3-REVIEW-B.md`, `ROUND-6-REVIEW.md`) show what a reviewer measures.

## How to run this batch (what made Batch 1 pass)

- `editcap.py acquire REALDEMOS-B02 --title "Real Exercise Demos Batch 2 R1" --type SFC`; work folder
  `renderq.py workdir REALDEMOS-B02 --need 3` (an honest 3 GB keeps it on the internal drive). Extreme must be mounted
  (masters: `/Volumes/Extreme/_edit_work/SHOOT-20261023/library-masters/<legacy_name>` from each catalog entry).
- **Render queue:** run every build and gate chain as ONE step:
  `stallwatch.py run REALDEMOS-B02 -- renderq.py run --light --group REALDEMOS-B02 -- bash chain.sh`. Re-acquire the edit
  slot if 3 hours pass.
- **Per exercise, before any cut:** a 2 fps contact sheet of every listed clip; check camera steadiness
  (`tools/motionsig.py`); then find the turnaround FRAMES by measurement (`tools/edge.py` on the weight stack where one
  is visible, else a colour or frame-difference tracker) and look at the exact frames. These machines all have a
  visible stack or moving arm: track it. Cut on the turnaround frame on both sides.
- **Loop:** end on the rep that precedes the opening frame in the same take where the take allows (last frame = source
  frame N-1, first = N); otherwise compare body edge and background between candidate end frames.
- **Screen every detail clip frame by frame** (hands, handles and the working joint in frame for the whole insert, hair
  inside the top edge, no grin, no strain face filling the frame, no gym member right behind him, steady camera). Crop
  the wide take off any gym member at the frame edge. If no detail clip is clean, use one continuous wide take and gate
  it with `--format exercise-demo-real-onetake`.
- **Script:** from the exercise's `setup` / `execution` / `mistake` copy in `public/exercises.js`, matched to what the
  picture shows; never a cue the picture contradicts. Lines of 1.0 to 1.5 s for a pull or push, "slowly" lines on a
  wide-shot return, the last line on a pull or push so the return is the silent tail. Write the cue-to-phase table
  first, then `gen.js` (about $0.01 a read; regenerate the whole read when the script changes).
- **Form that is in every rep is Dan's decision:** measure it, do not narrate against it, and put it first on the review
  page as a question (Batch 1: pushdown elbows, row torso; Dan approved both as his form and the app copy was changed
  to match). `machine-row` here is a chest-supported T-bar row while the app copy describes a seated machine with
  handles at mid-chest: script to the footage and ask Dan on the page whether to change the copy.
- **Gates:** `gates.sh` (audio gate on both files, plan, watch pass), then the independent review, then `finish2.sh`
  (`watch.py --judge` with the reviewer's `findings.json`, `gate.py --format exercise-demo-real`). All PASS.
- **Independent review:** fresh `ra-reviewer` agents, two demos each, briefed with `REVIEW-BRIEF.md` plus the facts it
  does not cover; tell them to call `ffmpeg.real` and a Whisper model directly, never the queue wrappers. Fix and
  re-review (a fresh reviewer) until each demo SHIPS. Check that each review's word check actually completed.
- **Review page:** new port, `review_server.py PORT DIR`, 1080p. These four have NO demo today, so the second column
  is "No demo today. This would be the first one." (the pilot's `make_review.py` has that branch; Batch 1's shows an AI
  demo beside each). "Your decisions" first, then "What I decided". Silent checks, then Finish checks for owner.
  `editcap.py release REALDEMOS-B02 --review`, board entry, stop for Dan.
- **After Dan approves:** copy each app encode + poster to `public/exercise-demos/<id>.mp4/.jpg`; add the id to BOTH
  `EXERCISE_DEMO_IDS` and `EXERCISE_DEMO_REAL` in `public/index.html` (re-read the file first: other batches edit the
  same two lines); update `public/exercises.js` copy only where Dan approved a change; syntax-check; `safe-push.sh`;
  wait for the Railway deploy (about 9 minutes); verify on https://absbyai.com (file hashes, then
  `openExerciseSheet('<id>')` in the page: video plays, poster loads, no AI-GENERATED chip; `plank` still shows its
  chip). Media in workout cards is a native-retest trigger: say so.
- **Records:** `clip_library.py add <1080 master> --kind real --category dan-filmed --slug <id>-trainer-demo-real
  --status used-final --used-in "app trainer" --tags exercise-demo real-demo <id>`; mark source clips `used-final`,
  `used_in: app trainer`, `intended_use: correct demonstration` under `catalog_lock()`; `clip_library.py sheet`; archive
  `out/<id>/` and the recipe to `Media/exercise-demos/real/` with checksums and add rows to `LIBRARY.md`;
  `review_server.py PORT --remove`; `editcap.py release`; delete the board entry; mark the batch executed in
  `Handoffs/real-demos/README.md`.

## Starter prompt

> Real Exercise Demos Batch 2 R1. Read `Handoffs/real-demos/batch-02-gym-machines-new-coverage.md` and build real-footage Trainer demos for pec-deck, machine-chest-press, machine-row, machine-rear-delt-fly from the B-roll in the clip library, with the Batch 1 recipe (read the "Batch 1 result" section of the master handoff first and copy `~/Projects/_edit_work/REALDEMOS-B01/`). Pass every gate and an independent review, put them on a 1080p review page, and stop for my review. Dan has authorized the whole batch, including installing the approved demos in the app and deploying.

**Model:** Claude Opus 5.5, high effort.
