# Handoff: three more AI-Dan exercise demos for the trainer app (2026-11-06)

**Type:** in-app exercise demo (not a content video, not an ad). **Owner:** Claude, Opus 5.5 high (this work started on Claude).
**Authorization:** Dan, 2026-11-06: "Give me a handoff to do three more exercises." He approved paid native 1080p Veo for these demos on 2026-11-05 ("Try paid 1080p") and shipped the first three as they were ("I think that's better than a stick figure"). Spend up to $10 of paid Veo in this session (inside the $25 standing cap). Do every step without asking; stop only for Dan's review.

## The three exercises (picked 2026-11-06, Dan can swap)

All three are in-place symmetric moves. The pilot found these work best. None of them has been attempted in any earlier batch.

| id | name | library text (`public/exercises.js`) | camera |
|---|---|---|---|
| `db-tricep-extension` | Overhead Triceps Extension | Standing, one dumbbell in both hands overhead, elbows pointing forward and narrow. Lower it behind the head, extend back to straight. Mistake: elbows flaring wide. | three-quarter front so the chest print is large |
| `db-fly` | Dumbbell Fly | On a flat bench, dumbbells over the chest, palms facing, slight fixed elbow bend. Open in a wide arc to a chest stretch, squeeze back up. Mistake: bending the elbows more on the way down. | side view, bench parallel to the camera |
| `db-crunch` | Weighted Crunch | On the floor, knees bent, dumbbell held on the chest. Curl the shoulder blades off the floor, pause, lower slowly. Mistake: sitting all the way up. | side view on a mat, like the bicycle crunch |

## What worked in the pilot (read before starting)

- **Read first:** `/exercisegeneration` SKILL.md and `Docs/EXERCISE_DEMO_FLOW_PILOT_20261105.md`. The working folder for the shipped three is `Media/exercise-demos/_flowpilot/`. It holds `build.sh`, `finish.sh`, `gen-vo.js`, `mkpage.py`, `entries.json` and the `app-staging/` copies.
- **Generate with paid native 1080p.** Use Replicate `veo-3.1-fast` at 4 s ($0.40 a take): `veo.py api JOBDIR ID --paid-ok "Try paid 1080p (Dan, 2026-11-05)"`. Flow's 720p garbles the chest print on side views. Use one job folder per parallel call (`_flowpilot-paid7`, `-paid8` and so on), because two api calls on one job collide.
- **Frames come first.** Make START and END with Codex (`.claude/skills/_shared/codex-image.sh`) from the canonical character `Media/exercise-demos/_character/ai-dan-canonical.jpg`. Make the END as an edit of the START, and copy the START's background into it with `lockstill.py`. Gate it with `framecheck/gate.py START END --spec spec.json`, then a fresh `frame-reviewer`, then `--review`.
  - The spec needs `person: {"side": ...}`. An empty `{}` counts his body as background.
  - Set `camera: "locked"` and list the props: dumbbell, bench, mat.
  - State depth or range aggressively and name the wrong pose ("this is NOT a ...").
- **Build at native speed.** Never change speed with setpts or minterpolate. Pick the take whose own tempo fits.
  - For these three in-place moves, make a palindrome unit with `_batch5/cutunit.py` from the clean one-way stretch.
  - Run the background lock `_r2/lockbg.py`. First `rm -f <id>/r2-unit-preghost.mp4`, because a stale file gets reused.
  - Run the ghost scan `reference/ghost.py` and the double-pump check `reference/mono.py qcunit`. Run qcunit on an internal copy, because the Seagate's `._` files break it.
- **Motion check:** `clipcheck.py`, then a fresh motion `frame-reviewer`, then `--review`. The pilot's recurring faults were:
  - hands crossing the face;
  - a garbled or morphing logo;
  - face drift: eyes closing, mouth opening, stubble appearing;
  - feet sliding;
  - machines moving on their own.
- **Voice and app files.** Write the voice-over with MiniMax `speech-02-hd`, voice `R8_NE3EBC2N`, from the library's setup, execution and mistake lines, using `gen-vo.js` with a new vo json. Then run `finish.sh`: it does the room tone, the audio gate `--synthetic --profile in-app-demo`, a 960x540 mono 32 kHz encode, and delivery gate format `exercise-demo`.
- **Attempts:** up to 5 takes per exercise. Fix the frame or prompt between takes; don't just re-roll. If a fault repeats in 3 takes, stop and report it.
- **Edit cap:** `editcap.py acquire EXDEMO-3MORE` before the first generation, and `release --review` when the page is ready.

## Shipping bar

Dan's bar for app demos is "better than a stick figure." Run every gate and reviewer, and put the best take of each exercise on the review page even if the reviewer fails it. Next to each one, write in plain words what is right and what is still off, as the 2026-11-06 page did. Do not install anything until Dan says ship.

## Deliver

1. A review page (`review_server.py PORT DIR`, re-run after any edit) with the three best takes. Open it in `?review_mode=automation`, check silently at 1080p, then call `AbsReviewAudio.handoff()`, so it is left paused with sound ready.
2. In chat: the page link, one line per exercise, the spend, and the wrap-up boxes.
3. When Dan says ship, install the way the first three were installed (commit 944ef64 and the lunge/bicycle commit of 2026-11-06):
   - Copy `app-staging/<id>-vN.mp4` to `public/exercise-demos/<id>.mp4` (chmod 644).
   - Make a poster jpg at 1.0 s.
   - Re-run the audio and delivery gates on the public file, then move their stamp json files out of `public/` into `app-staging/`.
   - Add the id to `EXERCISE_DEMO_IDS` in `public/index.html` (around line 9294).
   - Run `safe-push.sh` with those files, confirm the Railway deploy, and check the demo plays on absbyai.com.

## State at handoff

- Shipped in the app and committed locally: chair-squat (944ef64), db-lunge and bicycle-crunch (68cdd00). The push is blocked by the main folder's 12-file merge jam (see the board). The next safe-push carries all three.
- Gemini is testing hammer curl, floor press and hip thrust separately (`handoff-20261105-gemini-exercise-demo-test.md`). Do not touch those three.

## Executed 2026-11-07 (Claude, R1): at Dan's review, nothing installed

Review page: http://127.0.0.1:9317/ (files in `~/Projects/_edit_work/EXDEMO-3MORE/review/`; work folders `Media/exercise-demos/<id>` are symlinks to `~/Projects/_edit_work/EXDEMO-3MORE/<id>`). Paid Veo spend $3.80 (9 paid takes; one free Replicate failure), VO about $0.03.
- **db-crunch:** CR2 frames 6-38 + 0.17 s top hold, `db-crunch-AIDAN-narrated-FINAL-CANDIDATE-v2.mp4`, app file `_flowpilot/app-staging/db-crunch-v2.mp4`. Frames and motion reviewer PASS.
- **db-fly:** FL2 frames 0-36 + hold, `...-v1.mp4` / `app-staging/db-fly-v1.mp4`. Motion FAIL: near dumbbell crosses the face ~0.3 s each way, far arm lags 8 frames. Same in all 4 takes (stop rule). Cause: `fp-end.png` puts the near dumbbell head-side of the shoulder (x 300-500 vs shoulder ~600). Fix: re-edit END with that dumbbell directly beside the shoulder, re-gate, 1-2 takes.
- **db-tricep-extension:** TE2 frames 0-30 + 0.21 s bottom hold, `...-v2.mp4` / `app-staging/db-tricep-extension-v2.mp4`. Motion FAIL: elbows flare ~26 deg per side at the bottom, shallow (dumbbell to top of head). All 3 takes (stop rule). Likely fix: side or three-quarter camera.
On "ship": install per "Deliver" step 3 using the app-staging files above.

## R2 same day (Claude): fly and triceps redone; all three at Dan's review, nothing installed

Total paid Veo $5.00 (12 paid takes). Page http://127.0.0.1:9317/ now shows:
- **db-crunch:** unchanged, `-v2` / `app-staging/db-crunch-v2.mp4` (reviewer PASS).
- **db-fly:** new END (near dumbbell directly below the shoulder, knurled handles matched), FL5 frames 0-39 + hold, `db-fly-AIDAN-narrated-FINAL-CANDIDATE-v2.mp4` / `app-staging/db-fly-v2.mp4`. Frames and motion reviewer PASS (face pass 0.125 s, arms in step).
- **db-tricep-extension:** new three-quarter frames `fq-start/fq-end.png` (reviewer PASS), TQ2 frames 48-80 + 0.21 s hold, `...-v4.mp4` / `app-staging/db-tricep-extension-v4.mp4`. Form fixed; motion FAIL only on a 0.17 s faint double of the dumbbell's lower end behind the forearm. All 5 takes used.
On "ship": install those three app-staging files per "Deliver" step 3.
