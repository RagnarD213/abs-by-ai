# Real B-roll exercise demos for the app (plan + handoff)

**Type:** app asset (not content, not an ad). Nothing is published or derived from these.
**Written:** 2026-11-09, Claude (Fable 5.2). **Owner of execution:** Claude Opus 5.5, high effort.
**Dan's ask (2026-11-09):** the real gym B-roll plus a voiceover is better than many of the AI exercise demos. Edit ALL the exercise B-roll into demos (even exercises not in the app yet, because he is changing the library soon) and install the ones that match the current library.

## What exists today

- **App library:** 97 exercises in `public/exercises.js`. 38 have an installed demo video (all AI-Dan, all showing an "AI-GENERATED" chip), listed in `EXERCISE_DEMO_IDS` at `public/index.html:9294`, files at `public/exercise-demos/<id>.mp4` + `.jpg` (960x540, 24 fps, about 20 s, narrated by Dan's cloned voice).
- **Real B-roll:** `Media/clip-library/catalog.json` (private). 161 gym clips from the October 23 shoot (4K, 29.97 fps, Color C already applied, no audio, masters on the Extreme drive, IDs B0566 to B0725 and B0736) plus about 45 older home/poolside exercise clips (B0001 to B0548, 16:9, mostly 4 to 11 s, Dan shirtless).
- Almost every gym exercise has one long main take (15 to 36 s, several reps) and 1 to 5 close detail angles. That is the advantage over AI: real reps and a second angle.
- Every gym main take has teaching intent `unknown`. Nobody has confirmed the reps are correct demonstrations. Dan's review of each finished demo is that confirmation; record it in the catalog (`intended_use: correct demonstration`) when he approves.

## The match (clip IDs: `*` = favorite main take)

### A. Gym footage that REPLACES an installed AI demo (6)

| app id | real footage | main take | detail angles |
|---|---|---|---|
| `leg-press` | Leg press | B0621*, B0620 | B0623, B0625, B0622 (loading) |
| `leg-curl` | Lying hamstring curl | B0626* | B0627, B0628, B0629, B0630 |
| `pullup` | Pull-ups | B0642* | B0645, B0641, B0643 |
| `cable-tricep-pushdown` | Bar tricep pushdown | B0651* | B0654, B0652, B0653 |
| `seated-cable-row` | Wide-grip seated cable row | B0648* | B0649, B0650 |
| `lat-pulldown` | Wide-grip lat pulldown | B0688 | B0662, B0663, B0664 |

### B. Gym footage for library exercises with NO demo today (7, plus 1 partial)

| app id | real footage | main take | detail angles |
|---|---|---|---|
| `cable-crunch` | Kneeling cable crunch | B0574*, B0573 | B0582, B0583, B0594 |
| `pec-deck` | Chest fly machine | B0665* | B0666, B0667, B0668 |
| `machine-chest-press` | Chest press machine | B0678* | B0679, B0680, B0681 |
| `machine-row` | Chest-supported T-bar row | B0723* | B0644, B0724, B0725 |
| `machine-rear-delt-fly` | Rear delt fly, reverse pec deck | B0670*, B0669 | B0671, B0672, B0689, B0690 |
| `sled-push` | Sled push | B0699, B0700, B0701 | B0702 to B0705 |
| `walking-lunge` | Walking bodyweight lunges | B0706, B0708, B0709, B0710, B0713 | B0707, B0712, B0711, B0714 |
| `chinup` (partial) | Chin-ups, close-up only | B0646 (front detail, 15 s) | none. Build it; if a close-up alone does not teach the move, hold it and add to the pickup list |

### C. Gym footage NOT in the library yet (19 new exercises, built and stored ready)

| proposed id | name | main take | detail angles |
|---|---|---|---|
| `captains-chair-leg-raise` | Captain's Chair Leg Raise | B0584* | B0585 to B0591 |
| `machine-calf-raise` | Standing Calf Raise Machine | B0631* | B0632 to B0636 |
| `machine-hip-thrust` | Hip Thrust Machine | B0637* | B0638, B0639, B0640 |
| `assisted-pullup` | Assisted Pull-Up | B0611* | B0612, B0613, B0614 |
| `assisted-dip` | Assisted Dip | B0605*, B0609 | B0604, B0606, B0607, B0608, B0610 |
| `dip` | Bodyweight Dip | B0592*, B0593 | B0595, B0596, B0597 |
| `weighted-dip` | Weighted Dip (chain) | B0601, B0602, B0603 | B0598, B0599*, B0600 |
| `cable-curl` | Cable Bicep Curl | B0655*, B0661 | B0656, B0657, B0658, B0659 |
| `decline-situp` | Decline Medicine-Ball Sit-Up | B0616, B0617 | B0615*, B0647, B0618, B0619 |
| `incline-db-press` | Incline Dumbbell Press | B0697* | B0698 |
| `machine-lateral-raise` | Machine Lateral Raise | B0673* | B0674 to B0677 |
| `cable-overhead-tricep-extension` | Overhead Rope Triceps Extension | B0716, B0715 | B0717, B0718, B0719 |
| `preacher-curl` | Preacher Curl | B0695*, B0696 | B0687 |
| `bb-curl` | Straight-Bar Curl | B0683* | B0684, B0685, B0686 |
| `rope-hammer-curl` | Rope Hammer Curl | B0720 | B0721, B0722 |
| `machine-shoulder-press` | Shoulder Press Machine | B0682 | B0693, B0694 |
| `stair-climber` | Stair Climber | B0579*, B0580, B0581 | B0568 to B0572 |
| `stationary-bike` | Stationary Bike (seated, standing intervals) | B0566*, B0567 | B0575 to B0578 |
| `stomach-vacuum` | Stomach Vacuum | B0736, B0732 (poolside) | B0428, B0429 |

B0660 (high-pulley cable curl/pushdown variation) is a spare; use it only if Dan wants that variation as its own exercise.

### D. Home/poolside footage for library exercises (8 new coverage, 5 replace AI)

| app id | status today | real clips |
|---|---|---|
| `ab-wheel-rollout` | no demo | B0427, B0436, B0030 (rule: slow, full extension, arms locked) |
| `kb-deadlift` | no demo | B0431 |
| `kb-swing` | no demo | B0439 |
| `deficit-pushup` | no demo | B0546, B0452, B0548 |
| `db-rear-delt-fly` | no demo | B0451 |
| `db-russian-twist` | no demo | B0454, B0463 (medicine ball, not a dumbbell) |
| `bw-squat` | no demo installed | B0460, B0464, B0475 |
| `battle-ropes` | no demo | B0457 |
| `pushup` | AI demo | B0547, B0461 |
| `knee-pushup` | AI demo | B0433 |
| `db-shoulder-press` | AI demo | B0449 (seated, matches Dan's standard) |
| `db-curl` | AI demo | B0432, B0031 |
| `db-lateral-raise` | AI demo | B0450 (check against Dan's "Side Lateral" pour standard before replacing) |

### E. Home/poolside footage NOT in the library (10 new)

plank up-down (B0455, B0468), spiderman plank (B0423), toe-touch crunch (B0466, B0467), medicine-ball V-up (B0434, B0478), medicine-ball sit-up (B0003, B0048), handstand push-up (B0545, B0456), feet-elevated push-up (B0453), jump rope (B0448, B0542 ONLY; B0430 and B0447 are mistake/beginner clips), towel pull-apart (B0465), walking lunge alternate (B0462, B0477).

### Totals

- About 56 real demos to edit: 33 gym + 23 home.
- 26 go into the app now (27 if the chin-up close-up works): 11 replace AI demos, 15 give a demo to exercises that have none. Demo coverage goes from 38 to 53 of 97.
- 29 are built and stored for the library change.
- 27 AI demos stay (no real footage): bird-dog, dead-bug, face-pull, db-bench-press, db-goblet-squat, db-rdl, db-row, incline-pushup, plank, reverse-lunge, side-plank, wall-sit, hollow-hold, pike-pushup, chair-dip, split-squat, glute-bridge, calf-raise, crunch, lying-leg-raise, superman, leg-extension, russian-twist, reverse-crunch, chair-squat, db-lunge, bicycle-crunch.

## The demo format ("real demo v1")

1. **Picture:** 16:9. Master 1920x1080 at the source 29.97 fps, cut from the 4K library master (Color C is already in the master; never raw footage, never re-grade). Home clips keep their approved grade.
2. **Length:** as long as the narration plus about 1 s lead and 1 s tail, 15 to 25 s.
3. **Cut:** open on the main wide take from the first clean rep (no walking in, no setup fidgeting), 2 full reps; cut to ONE close detail angle on the cue it illustrates (grip, foot position, the squeeze); back to the wide take to finish. End on the rest position so the muted loop in the workout card restarts cleanly. Cuts land between reps, never mid-rep. Only correct reps: apply Dan's settled form standards from `/exercisegeneration` (pull-up chin over the bar with a slight elbow bend at the bottom, row to the stomach, leg curl past 90 degrees, pushdown to locked elbows, and so on). Home clips shorter than the narration: use the second take or angle, never a slowed or reversed rep.
4. **Voiceover:** Dan's approved cloned narrator (MiniMax `speech-02-hd`, voice `R8_NE3EBC2N`, speed 1.0), same script pattern as the AI demos: "Here's how to do the [name]." then 3 or 4 cues from the exercise's `setup` / `execution` / `mistake` copy in `public/exercises.js`. For exercises not in the library, write that copy first (see below) and build the script from it. Room tone under the voice for the full length, as in `Media/exercise-demos/_batch5/mux.py`. The script must match what the picture shows (bar vs rope, wide grip, BOSU under the knees).
5. **No graphics, no captions, no music.** Same as the AI demos; the text lives on the exercise sheet.
6. **App encode:** 960x540, H.264 High, CRF 28, `+faststart`, AAC mono, plus a `.jpg` poster from a frame that shows the exercise mid-rep. Recipe: `Handoffs/handoff-20260821-exercise-demos-in-app.md` step 2 (keep 29.97 fps, do not convert to 24).
7. **Gates:** audio `audio_gate.py --synthetic --profile in-app-demo` (-24 LUFS), then the delivery gate. The existing `exercise-demo` format in `_shared/deliver/formats.py` assumes 24 fps and one looping generated shot, so add a sibling format `exercise-demo-real` (29.97 fps, real cuts allowed, same audio rows, coverage/static rows not applicable with reasons written in). Run `_shared/qc_corpus/run.py` after and keep it green. The AI-only tools (`mono.py`, `ghost.py`, `background.py`) do not apply to real footage.

## New-exercise copy (sections C and E)

For each exercise not in the library, write a ready-to-paste `exercises.js` entry (id, name, equip, cat, muscles, setup, execution, mistake, swap) in `Media/exercise-demos/real/NEW-LIBRARY-ENTRIES.js`. Do NOT add them to `public/exercises.js`: the trainer picks from that list, and Dan is changing the library himself. Show the copy on the review page next to each demo so he approves words and video together.

## App changes (one small code change, done at first install)

- `public/index.html`: add a `EXERCISE_DEMO_REAL` set beside `EXERCISE_DEMO_IDS`. Add each installed real id to both. The "AI-GENERATED" chip renders only when the id is NOT in `EXERCISE_DEMO_REAL` (two places: the day-view card near line 10010 and the exercise sheet near line 10150).
- Replacements overwrite `public/exercise-demos/<id>.mp4` and `.jpg` (same URL; the server sends no long cache and the service worker does not cache media, so no cache-busting is needed). The old AI file stays in git history and in `Media/exercise-demos/<id>/`.
- Deliver the normal way: `safe-push.sh`, Railway deploy, verify on `https://absbyai.com` (open a replaced exercise and a newly covered one, confirm real video, sound, poster, no chip; open an AI one, confirm the chip is still there). Media in workout cards is a native-retest trigger row: flag it.
- Store finished masters and stored-for-later demos in `Media/exercise-demos/real/<id>/` with an index `Media/exercise-demos/real/LIBRARY.md` (id, name, source clip IDs and ranges, installed or stored). Register each approved demo in the clip library and mark the source clips used (`--used-in "app trainer"`).

## Order of work

**Phase 0, pilot (3 demos, then stop for Dan):** `cable-crunch` (new coverage), `leg-press` and `pullup` (replacements). Build the format, the VO, the new gate format and a review page (`review_server.py`, 1080p) that shows each real demo with the current AI demo beside it for the two replacements. Dan approves the format and the form. Nothing is installed in the pilot.

**Phase 1, gym exercises already in the library (11 more):** the rest of sections A and B. Review page, Dan's notes, then install all 13 or 14 with the app change in one deploy.

**Phase 2, gym exercises not in the library (19):** section C. Review page with the proposed library copy. Approved demos are stored, not installed.

**Phase 3, home/poolside footage (23):** sections D and E. Dan is shirtless by the pool in these and the AI demos show the gym, so the review page opens with that side-by-side for `pushup`; if he prefers the gym look for a move, that move keeps its AI demo. Install the approved library ones, store the rest.

**Phase 4, close-out:** update `/exercisegeneration` SKILL.md with one rule at the top: search the real B-roll library first; AI demos are only for exercises with no real footage. Write the pickup list for the next gym shoot into `Docs/PICKUPS_NEXT_STUDIO_SHOOT.txt`: the 44 library exercises still without any demo, plus any take Dan rejected here. Note for the pending AI demo jobs: `db-rear-delt-fly` (in `handoff-20261109-fable-exercise-demos-flow.md`) has real footage (B0451); if Dan approves the real one in Phase 3, the AI one is not needed.

Each phase is one review round. Run `editcap.py acquire` and the render queue as for any edit; work on the internal drive (`renderq.py workdir REALDEMOS --need 30`). The Extreme drive must be mounted for the masters.

## Defaults picked (Dan can change any of them)

1. Narration is the cloned voice already approved for demos, not a new recording by Dan. If he would rather record them himself, the scripts double as his teleprompter list and only the audio step changes.
2. Real demos show no "AI-GENERATED" chip.
3. Gym replaces AI wherever both exist; home footage replaces AI only after Dan sees the side-by-side.
4. Other gym members visible in the background of some takes (for example the leg press) are left as filmed; pick the take and crop with the least of them.

## Cost and time

Voiceover about $0.01 per demo (under $1 total). No image or video generation. Editing is the cost: roughly one session per phase.

## Phase 0 result (2026-11-09, Claude Opus 5.5): pilot APPROVED and INSTALLED 2026-11-13

Dan, 2026-11-13: "This is definitely better than the AI versions... Let's redo everything that we have B-roll with, with real
stuff, and only things we don't have B-roll with will be done with AI." Phases 1-4 are now 11 batch handoffs in
`Handoffs/real-demos/` (README there). Installed: `EXERCISE_DEMO_REAL` in `public/index.html` (commit 10b6bca).

Review page: http://127.0.0.1:9512/ (port 9512, files in `~/Projects/_edit_work/REALDEMOS/review/`). Finals, build
scripts, phase tools and `LIBRARY.md`: `Media/exercise-demos/real/` (Seagate, checksummed; work copies in
`~/Projects/_edit_work/REALDEMOS/out/`). Gate format `exercise-demo-real` is live (commit b664585). All three pass the
audio gate and the delivery gate (39 pass, 0 fail, 0 unmeasured); four independent review rounds. Nothing installed.

Traps for Phase 1 (read before cutting):
- **Narration lines must sit on the rep phase they name** (VIDEO-RULES "Exercise demonstration timing"). Reps run
  2.5-3.5 s, so a 2.5 s sentence cannot cover "lower ... press back up". `build.py` splits the VO at the narrator's
  pauses and places each line with `vo_at`; where a line is longer than the phase it names, regenerate a shorter line
  ("Keep a slight bend at the bottom", "Crunch your ribs down to your hips"). `vo_lines` splices one new line into an
  earlier read (same voice/settings) when a fresh read comes out slower.
- **Measure phases, do not eyeball contact sheets.** Tools in `Media/exercise-demos/real/tools/`: `shorts_y.py`
  (pull-up height from the shorts), `track.py` (rigid object, e.g. leg-press plate, on a locked-off camera),
  `refdist.py` (distance to a reference pose), `frames.py` (exact-frame grids). Handheld takes defeat the trackers.
- **Takes:** B0621 (leg press favorite) is handheld with a push-in and Dan glances at the camera; B0620 is locked off
  (arms crossed on chest), used for the pilot. B0574 (cable crunch favorite) is 17 s, so the pilot continues on B0573.
  B0642's last rep drops into a dead hang (end at 15.27). B0643's top crops Dan's crown (disclosed); B0645 has a grin at
  8.6-9.05; B0641 frames his face at the bottom edge. vidstab tripod mode made handheld takes jitter: do not use.
- **Room tone:** `_batch5/mux.py` amplitude 0.004 measures about -62 dB and fails the silent-second row; 0.026 gives
  the intended -46 dB.
- **Gate plan** comes from `make_plan.py` (punch segments by camera angle, close-ups as covered inserts, exact frames).
- Corpus: `qc_corpus/run.py` needs `--no-selftest` until the audio selftest's Muhammad references (moved to Expansion
  on 2026-10-31) are restored; 3 approved entries (ds52, ds63, ds37) read TIGHT on rows this work did not touch.

## Batch 1 result (2026-11-13): read before cutting any other batch

Batch 1 (leg-curl, cable-tricep-pushdown, seated-cable-row, lat-pulldown) needed four independent review rounds. Every
failure below was avoidable. Copy the Batch 1 recipe, not the pilot's: `~/Projects/_edit_work/REALDEMOS-B01/`
(`build.py`, `make_plan.py`, `make_review.py`, `gates.sh`, `finish.sh`, `REVIEW-BRIEF.md`, `tools/`; a checksummed copy
goes to `Media/exercise-demos/real/b01-recipe/` when the batch is approved).

- **Dan's reps have almost no pause.** A pulldown bottom lasts 1 to 2 frames, a row's reach about 0.1 s, a top about
  0.3 s. A contact sheet at 5 fps cannot place a cut. Find turnaround frames by measurement: `tools/edge.py` (top edge of
  the weight stack, frame-accurate), a colour tracker for a moving pad, or the frame-difference minimum, then look at the
  exact frames. Cut on the turnaround frame on BOTH sides.
- **Cut by frame number, not by seconds.** `build.py` takes (first source frame, last source frame) per shot and trims
  with `trim=end_frame`; `edit.json` records each shot's start frame, and `make_plan.py` reads it. The pilot's
  seconds-based cuts landed 1 to 2 frames off the plan, so the watch strips showed no cut.
- **Loop seam.** First and last frame must be the same pose AND the same framing. Best: end on the rep that precedes the
  opening frame in the same take (last frame = source frame N-1, first = N: a continuous loop). Otherwise compare the
  back edge of his body and the background (phase correlation) between candidate end frames; he drifts on his feet and
  later reps often stop shallower than the first. "Locked-off" takes still pan a few px a second.
- **A line must fit the phase it names.** Pulls and pushes last 0.5 to 1.0 s, returns 1.5 to 2.5 s. Write lines of 1.0
  to 1.5 s for a pull, put "slowly" lines on a wide-shot return, and make the LAST line sit on a pull or push so the
  return that follows is the silent tail (a last line on a return leaves no tail before the rest position).
  "Word" must not start more than about 0.4 s before its movement starts.
- **Screen every detail clip frame by frame before using it:** hands, bar, feet and the working joint in frame for the
  whole insert, hair inside the top edge, no grin, no strain face filling the frame, no gym member standing behind him,
  camera steady. If no detail clip is clean, stay on the wide take (one continuous shot is acceptable and passed review)
  and say so on the page. The defective-source hair clause does not apply when the wide take is a complete alternative.
- **Form that is in every rep is Dan's decision, not a cut problem.** Measure it, do not narrate against it, and put it
  first on the review page as a question (Batch 1: pushdown elbows travel forward at the top; row torso leans back about
  30 degrees). Never write a cue the picture contradicts ("sit tall", "elbows pinned").
- **Narration audio:** regenerate the read whenever the script changes (removing a line from the middle of a read leaves
  the wrong intonation); lead each line in by 0.08 s and out by 0.035 s.
- **Render queue:** these clips are seconds long, but each ffmpeg call and each gate re-joins the queue. When another
  edit holds all the cores (a chroma key), ten small steps wait an hour. Wrap the whole chain as ONE step:
  `stallwatch.py run <JOB> -- renderq.py run --light --group <JOB> -- bash chain.sh`. Tell reviewers to call
  `ffmpeg.real` and a Whisper model directly, never the wrapper, `whisper_chunked.py` or `cut/speech.py` (a reviewer sat
  an hour waiting for a queued transcript). The edit slot lapses after 3 hours without activity: re-acquire it.
- **Reviewer brief:** give each fresh `ra-reviewer` two demos, `REVIEW-BRIEF.md`, and the facts the brief does not cover;
  it writes `watch/findings.json`; then `finish.sh` runs `--judge` and the delivery gate. A review of two demos takes
  about 17 minutes. Crop the wide take off any gym member at the frame edge before the first review.

## Starter prompt (Phase 0)

> Real Exercise Demos Pilot R1. Read `Handoffs/handoff-20261109-real-broll-exercise-demos.md` and run Phase 0 only: build the three pilot demos (cable-crunch, leg-press, pullup) from the real gym B-roll in the clip library with the cloned-voice narration, add the `exercise-demo-real` delivery gate format, pass the gates, and put them on a 1080p review page with the current AI demo beside each replacement. Install nothing. Dan has authorized the whole plan; stop only for his review of the pilot.

**Model:** Claude Opus 5.5, high effort.
