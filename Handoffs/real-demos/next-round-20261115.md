# Real Exercise Demos: next round (batches 4 to 11)

## Progress update, 2026-11-16

This supersedes the original scheduling snapshot below: Batch8 has five real demos installed/live-verified; Dan also approved the fly after testing its picture and sound in the app. Swing requires correct real footage. Batch9 has seven independently cleared R2 demos awaiting review at http://127.0.0.1:9870/ (including Hammer Curl, not supinated db-curl). Batches4-7,10,11 contain29 planned demos still to build/store for future library additions. Do not relaunch Batch9 or install its unapproved R2 files from this status update. Latest batch receipts are in Docs/REALDEMOS_B08_FLY_INSTALLED_20261115.md and Docs/REALDEMOS_B09_R2_REVIEW_20261115.md.

**Type:** app asset (Trainer exercise demos from Dan's real B-roll; not content, not an ad). **Written:** 2026-11-15 by the Batch 3
session, after Dan asked for "a Handoff document to fire the next round of these". **Owner per batch:** Claude Opus 5.5, high effort.
Dan has authorized every batch end to end, including installing approved demos in the app and deploying.

## Where it stands

- **Done and live in the app (14 real demos):** Pilot (cable-crunch, leg-press, pullup), Batch 1 (leg-curl, cable-tricep-pushdown,
  seated-cable-row, lat-pulldown), Batch 2 (pec-deck, machine-chest-press, machine-row, machine-rear-delt-fly), Batch 3 (sled-push,
  walking-lunge, chinup; all installed 2026-11-15).
- **Original planning snapshot (2026-11-15):8 batches,42 exercises.** See the progress update above for current status.

| batch | outcome | count | exercises | file |
|---|---|---|---|---|
| 8 | install | 6 | ab-wheel-rollout, kb-deadlift, kb-swing, deficit-pushup, db-rear-delt-fly, db-russian-twist | `batch-08-home-moves-new-coverage.md` |
| 9 | install | 7 | bw-squat, battle-ropes, pushup, knee-pushup, db-shoulder-press, db-curl, db-lateral-raise | `batch-09-home-moves-ai-replacements.md` |
| 4 | store | 5 | captains-chair-leg-raise, machine-calf-raise, machine-hip-thrust, assisted-pullup, assisted-dip | `batch-04-gym-new-exercises-part-1.md` |
| 5 | store | 5 | dip, weighted-dip, cable-curl, decline-situp, incline-db-press | `batch-05-gym-new-exercises-part-2.md` |
| 6 | store | 5 | machine-lateral-raise, cable-overhead-tricep-extension, preacher-curl, bb-curl, rope-hammer-curl | `batch-06-gym-new-exercises-part-3.md` |
| 7 | store | 4 | machine-shoulder-press, stair-climber, stationary-bike, stomach-vacuum | `batch-07-gym-new-exercises-part-4-and-cardio.md` |
| 10 | store | 5 | plank-up-down, spiderman-plank, toe-touch-crunch, medicine-ball-v-up, medicine-ball-situp | `batch-10-home-new-exercises-part-1.md` |
| 11 | store | 5 | handstand-pushup, feet-elevated-pushup, jump-rope, towel-pull-apart, walking-lunge-home + close-out | `batch-11-home-new-exercises-part-2-and-close-out.md` |

Install batches (8, 9: 13 exercises) change the app; store batches (29 exercises) build demos for exercises not in the library
yet and store them with ready-to-paste library copy. **Fire 8 and 9 first**, then 4 to 7 and 10, then 11 last (it writes the
pickup list for the next shoot and needs the others' results).

**How many at once:** every batch is an edit and holds an edit slot (M2: 3 slots, M6: 2; other edits share them). Fire two or three
at a time; a batch that cannot get a slot waits automatically. Batches are independent; only the install step touches shared lines
in `public/index.html` (re-read it first).

## Read before cutting (in this order)

1. The batch file (exercises, clip IDs, notes).
2. `Handoffs/handoff-20261109-real-broll-exercise-demos.md`: "The demo format", then the **Batch 1, Batch 2 and Batch 3 results**.
3. AGENTS.md "Exercise demos: real B-roll first", including the **length rule (Dan, 2026-11-15): target 15 s, never under 10 s.**
   Dan: "It seems too brief if it's just 1 or 2 reps." Plan about five cues (setup, the movement, a form point, a common mistake,
   the pace of the reps) and enough reps or angles to carry them. Approved demos before 11-15 were not redone.
4. Recipe to copy (never edit in place): `/Volumes/Extreme/_edit_work/REALDEMOS-B03/` on the M2 (`build.py` with `vo_pick`,
   `vo_at`, `vo_gain_db`, multi-shot cuts by exact frame; `make_plan.py`; `gates.sh`; `finish.sh`; `make_review.py`;
   `REVIEW-BRIEF.md`; `tools/` including `loopfind.py`, `appdiff.py`, `frames.py`; `vo/gen.js`). A checksummed copy also goes to
   `Media/exercise-demos/real/b03-recipe/`.

## What Batch 3 learned (do these from round 1)

- **Screen every frame for edges:** feet, knees, hands and hair at all four edges on every frame of every shot, not a contact sheet.
  Batch 3 lost five review rounds to a foot or knee dipping out of frame for 4 to 14 frames.
- **Moving exercises (walking, carries, sled):** cut only at standing passes found on a 1-frame leg strip, and check that the legs
  alternate at every cut AND across the loop restart (a knee sleeve makes it readable). Front angles often lose the front foot.
- **Loops:** pick the seam by measured full-frame difference (end+1 vs start, 480x270 grey) against the in-window frame steps, and
  loop on the same rep phase. A handheld shot never loops invisibly: disclose the framing jump (Dan accepted it on the sled push).
- **Lines:** a line ends on the phase it names (a "bottom" cue ends on the bottom, not on the next pull). If the read joins two cues
  in one sentence, regenerate it as two sentences. Gaps between lines at least 0.2 s.
- **App audio:** encode at AAC 128k (96k put a short distortion on the first word); check with `tools/appdiff.py`.
- **Edit slot:** read `editcap.py acquire` exit code directly (`> file; echo $?`), never through a pipe (Batch 3 rendered once while
  it said wait). Arm `editcap.py wait JOB` in the background when it says wait.
- **Reviewer verdicts:** never change a reviewer's findings yourself. Apply the stated fix, then have a fresh judge confirm it.
- **Pushing:** use current AGENTS.md delivery rules. If safe-push.sh commits then stops on other owners' live files, checkout-sync.py pushes the existing commit without touching their working files. Do not duplicate that commit from a clean worktree.
- **Dan's form standards** in `/exercisegeneration` "Batch 2 revision round" win over the app copy; narrate only what the picture shows.

## Starter prompts (one session per batch, Claude Opus 5.5 high)

> Real Exercise Demos Batch 8 R1. Read `Handoffs/real-demos/next-round-20261115.md`, then `Handoffs/real-demos/batch-08-home-moves-new-coverage.md`, and build real-footage Trainer demos for every exercise in it from the clip-library B-roll, on the Batch 3 recipe, each targeting 15 s and never under 10 s. Pass every gate and the independent review, put them on a 1080p review page with the current AI demo beside any it replaces, and stop for my review. Dan has authorized the whole batch, including installing the approved demos in the app and deploying.

For the others, change the batch number and file name: Batch 9 `batch-09-home-moves-ai-replacements.md`; Batch 4 `batch-04-gym-new-exercises-part-1.md`;
Batch 5 `batch-05-gym-new-exercises-part-2.md`; Batch 6 `batch-06-gym-new-exercises-part-3.md`; Batch 7 `batch-07-gym-new-exercises-part-4-and-cardio.md`;
Batch 10 `batch-10-home-new-exercises-part-1.md`; Batch 11 `batch-11-home-new-exercises-part-2-and-close-out.md` (store batches: "stop for my
review; approved demos are stored with their library copy, not installed").

## When a batch finishes

Install (install batches) per the master handoff, record each approved demo (clip library `add`, source clips `used-final`, checksummed copy
and `LIBRARY.md` row in `Media/exercise-demos/real/`), mark the batch executed in `real-demos/README.md`, remove its line from
`Handoffs/README.md` OPEN when the last batch is done, and delete its board entry.
