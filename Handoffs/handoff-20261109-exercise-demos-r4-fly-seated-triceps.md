# Handoff: Dumbbell Fly (bent elbows) and Seated Overhead Triceps Extension, app demos R4 (2026-11-09)

**Type:** in-app exercise demo (not content, not an ad). **Owner:** Claude, Opus 5.5 high (started on Claude). Sidebar name: `Fly and Seated Triceps Demos R4`.
**Authorization:** Dan, 2026-11-09: weighted crunch "looks good, we can ship" (DONE, see below); "Dumbbell fly: I want to redo this because his arms aren't bent enough. His arms are excessively straight." "Overhead triceps extension: the motion looks right, but I want them sitting." Do every step without asking; stop only for Dan's review page. Do not install fly or triceps until Dan says ship.

## Rules that changed since the first handoff (read AGENTS.md)
- **Google subscription first (11-08):** images get a Google (Flow, Nano Banana Pro, 0 credits) attempt alongside Codex, unlabeled blind pairs (`_shared/blind-image/blind.py`, `FLOW-IMAGE-RUNBOOK.md`); a Google frame that fails twice is dropped and Codex goes forward. **Video: Flow Veo Fast on the subscription first** (`veo.py add` then the `flow-veo` agent; Flow frames mode is 8 s; download 1080p Upscaled). Paid Replicate only after a recorded Flow failure (cap: $25/session; earlier rounds already spent $5.00 paid, R3 spent $0).
- **Empty-gym background (11-08):** `reference/background.py VIDEO --plate --masks --report` on the final unit and the narrated review master; masks only on the person/held props, reviewed. Mask builder made this session: `~/Projects/_edit_work/EXDEMO-3MORE/tools/mkmasks.py <demo_dir> <outdir>` (lockbg math + MediaPipe Pose segmentation; plate written to `<outdir>.plate.png`, NOT inside the mask folder). Crunch passed 469/469 frames with it.
- Fable 5.2 reviewer trial: 3 runs were already logged by another session before this one; this session logged 2 extra (memory `fable-5-2-release`). Default frame-reviewer (Opus) is fine now.

## Done in R3
- **Weighted Crunch shipped:** `public/exercise-demos/db-crunch.mp4` + `.jpg`, id added to `EXERCISE_DEMO_IDS`, commit 676645f pushed (that push also cleared the folder's backlog, ahead 0), live on absbyai.com (hash verified). Stamps in `Media/exercise-demos/_flowpilot/app-staging/db-crunch-public.*`.
- Voice-overs for both remaining demos exist and stay valid: `Media/exercise-demos/<id>/fp-vo.mp3`.

## What failed in R3 (frames only, no video made) and why
All frames in `Media/exercise-demos/db-fly/r3/` and `db-tricep-extension/r3/`, reviews in their `framecheck/*.review.md`.
- **Fly, side camera (elevated, bench parallel):** 5 Codex attempts + 2 Google. Every START failed on the NEAR arm: its bend points at the camera, so on screen it reads 143-158 deg (straight) even when the 3D bend is ~115 deg. Far elbow kept pointing at the hips. Best END so far: `cx3-end.png` (both arms ~100-120 deg 3D, near dumbbell under the shoulder; reviewer had no must-fix on END except the far arm in one review). Google START `gg-start.png` looked natural but its ENDs straightened the arm.
- **Seated triceps:** near-front camera (Codex `cx-*`, Google `gs*`) always drew a half rep with forearms across the top of the head. Three-quarter side seated (`sit-start.png` Codex, `gsit-start.png` Google, made by editing the R2 reviewed standing frame `../fq-start.png`): STARTs look right; every END failed: Codex `sit-end.png` upper arms +20 %, dumbbell +15 %; Google `gsit-end.png` half rep and far elbow flared 23 deg.

## Recommended R4 plan
1. `editcap.py acquire EXDEMO-3MORE`; work folder `~/Projects/_edit_work/EXDEMO-3MORE` (exercise folders are symlinked from `Media/exercise-demos/<id>`).
2. **Fly: change the camera** to high and behind his head (or at his feet) looking down the length of the bench, so both arms open left/right across the frame and the elbow bend is in the picture plane; chest print readable. Make START (arms over chest, elbows ~120 deg bowed out) and END (arms open, elbows lowest at bench height, same bend) with Codex AND Google, lock, gate, fresh reviewer. Measure elbows yourself before spending a review (posecheck.py).
3. **Seated triceps:** keep the three-quarter side seated START (`sit-start.png` or `gsit-start.png`, get it reviewed). For END, edit the R2 reviewed standing bottom frame `../fq-end.png` into seated (same prompt as `r3/T-sit-start-prompt.txt`) with the seated START as a second reference, then paste START's lower body; measure upper-arm length and dumbbell length against START before review. Alternative if ENDs keep failing: Flow Veo from the reviewed START only with the motion prompt `r3/T1.txt`, cut the clean lowering and let the motion reviewer decide (veo.py needs `--skip-gate "<reason>"`).
4. Flow takes (8 s, Veo Fast, 2 per exercise), clipcheck, motion reviewer, build with `~/Projects/_edit_work/EXDEMO-3MORE/build2.sh <id> <leg> <t0> <t1> 1.0 <tag> "--hold 0.17"` (palindrome, lockbg, ghost, qcunit, finish.sh), then `mkmasks.py` + `background.py` on unit and narrated master.
5. Review page: `~/Projects/_edit_work/EXDEMO-3MORE/entries.json` + `mkpage.py`, `review_server.py 9317 ~/Projects/_edit_work/EXDEMO-3MORE/review`, silent check at phone width, `AbsReviewAudio.handoff()`. Show the Codex and Google results unlabeled if both survive; log Dan's pick with `blind.py pick`.
6. On "ship": install like db-crunch (copy app-staging file, poster at 1.0 s, audio + delivery gates on the public file, move stamps to app-staging, add id, safe-push, verify live).

Motion prompts already written: `db-fly/r3/F1.txt` (rewrite camera wording if the camera changes), `db-tricep-extension/r3/T1.txt`.

## R4 result (2026-11-09, executed)
- **Fly: on the review page** (`http://127.0.0.1:9317/`), file `db-fly/db-fly-AIDAN-narrated-FINAL-CANDIDATE-r4c.mp4`, app file `Media/exercise-demos/_flowpilot/app-staging/db-fly-r4c.mp4` (audio + delivery gates PASS). Frames `db-fly/r4/cxg-start.png`/`cxg-end.png` (gate + reviewer PASS), take `veo-r4f/veo/F4c-flow-t1.mp4` frames 0-36, clipcheck PASS, background PASS 71/71 + 497/497, motion review PASS (`db-fly/r4/motion-r4c.review.md`). On "ship": install r4c like db-crunch (step 6 above).
- **Seated triceps: not ready.** All END routes failed review; details in `db-tricep-extension/r4/framecheck/*.review.md`. Default picked: film it for real at the next gym shoot (added to `Docs/NEXT_SHOOT_LIST.md`, section 2), then build it with the `exercise-demo-real` format. Dan can override (keep standing, or accept a hands-on-handle grip).
- Spend: $0 paid; Flow credits 21,586 -> 21,506 (8 Veo Fast clips, images 0 credits).
