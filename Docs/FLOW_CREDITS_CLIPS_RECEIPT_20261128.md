# Flow credits: AI clips for the next edits (receipt, running; final by 2026-11-28)

Handoff: `Handoffs/handoff-20261107-flow-credits-ai-clips-for-next-edits.md` (budget up to 14,000 credits; Ultra 20x drops Nov 29).
Next batch: `Handoffs/handoff-20261113-flow-credits-ai-clips-batch-2-3.md`. Credit log: `Media/flow-credit-log.md`.

## Clips made and approved (Dan, 2026-11-13)

| Library ID | Clip | Video (job) | Clean cut |
|---|---|---|---|
| A0247 | The Muscle Guy Is Self-Conscious Too | How To Stop Feeling Embarrassed At The Gym When You're Fat (DS-97) | 3.5 s |
| A0248 | Home Sweet Gym (bathrobe on the bench) | same (DS-97) | 5.0 s |
| A0249 | Caution Tape | The 3 Gym Exercises I Never Do (DS-100) | 4.2 s |
| A0250 | The Paramedics Wait | same (DS-100) | 2.7 s |
| A0251 | Days Without A Bench Press Injury: 0 | Why I Don't Do Flat Bench Press (DS-102) | 2.5 s |
| A0252 | Museum Of Bad Ideas | same (DS-102) | 4.5 s |
| A0253 | Between Rounds (jiu-jitsu jog) | Why You Should Walk Between Your Sets (DS-103) | 3.3 s |
| A0254 | Waking Up Sweating | Why I Sleep At 63 Degrees (DS-50) | 5.0 s |
| A0159 (existing) | Sore beginner on the stairs | What To Do Your First Day At The Gym (DS-95) | reuse |

Each ID is noted under "Pre-made AI clips" in its job doc. Library entries hold the window cut (only the clean frames); the full
8 s takes and every review stay in `~/Projects/_edit_work/FLOWCLIPS/vid-b1/`.

## Batch 2 video: made, waiting for Dan's picks (2026-11-13)

Work folder `~/Projects/_edit_work/FLOWCLIPS/vid-b2/` (prompts/, specs/, picks.json, windows.json, motion_results.txt, build_review.py).
Review page http://127.0.0.1:9244/ . Every clip passed `clipcheck.py` and a fresh motion reviewer; each plays only its clean window.
Where Dan approved two frame versions, both were made (X1, X2 follow the blind labels in `b2/sets/`); he picks between finished clips.

| Clip | Video (job) | Versions on the page | Clean window |
|---|---|---|---|
| Can't Go In | Why I Use Machines And Cables Instead Of Barbells At 41 (DS-99) | X1, X2 | 3.0 s, 4.3 s |
| Sitting On His Phone | Why You Should Walk Between Your Sets (DS-103) | X1, X2 | 2.3 s, 4.1 s |
| Laid Up | Why You Must Stretch After Every Workout (DS-104) | one | 2.9 s |
| The Straddle Stretch | same (DS-104) | X1, X2 | 3.0 s, 2.5 s |
| Thermostat On 63 | Why I Sleep At 63 Degrees (DS-50) | one | 2.0 s (a calmer start-frame-only retake `B2-06s` is queued for a longer clip) |

Next: Dan's picks, then `blind.py pick b2/sets/<id> --chose Xn`, `veo.py pick` where the two versions' takes came from different models,
`clip_library.py add <window cut> --kind ai --status usable-unused --used-in "<job> <title> (planned)" --tags flow-credits-batch2`,
`clip_library.py sheet`, and the IDs under "Pre-made AI clips" in each job doc.

Lesson for the next video batch: every Omni 1.1 Flash 6 s take re-rendered (went soft, changed texture) at frame 128, about 5.3 s in, so only
the first 5 s of an Omni take is usable; Veo Fast takes showed talking mouths and hands passing through feet late in the take. Two of three
thermostat takes flipped "63" to "62": quote on-screen numbers in the prompt and check them on every frame.

## Batch 3 frames: on Dan's page (2026-11-13)

Work folder `~/Projects/_edit_work/FLOWCLIPS/b3/` (ideas.py, prompts/, codex/, google/, pairs/, review_results.txt, build_page.py).
Frames page http://127.0.0.1:9245/ (Select buttons; untouched means out). 21 ideas for the unedited January Shorts DS-94, DS-95, DS-96, DS-98,
DS-51, DS-57, DS-46, DS-54, DS-56 (none), DS-60, DS-62, DS-64; opinion and "why" lines only (how-to demos use real footage).
49 reviews (38 first round, 11 after one redraw). 14 ideas passed gate + fresh reviewer:

| id | Idea | Video (job) | Passing versions |
|---|---|---|---|
| B3-01 | Stairmaster Concert | How To Use The Stairmaster To Burn Fat (DS-94) | 1 |
| B3-02 | Bored To Sleep | same (DS-94) | 2 |
| B3-03 | First Day | What To Do Your First Day At The Gym (DS-95) | 1 |
| B3-05 | The Tortoise | same (DS-95) | 1 |
| B3-06 | The Coffee Curl | How To Pick The Right Weight On Every Exercise (DS-96) | 2 |
| B3-07 | The Tiny Plate | same (DS-96) | 1 |
| B3-08 | Lighter And Fine With It | same (DS-96) | 2 |
| B3-21 | The Three Dumbbells | same (DS-96) | 1 |
| B3-12 | Only Five | The Only 5 Machines You Need At The Gym (DS-98) | 2 |
| B3-13 | Lighter But Weaker | 3 Ways To Lose Fat Without Losing Muscle (DS-51) | 1 |
| B3-14 | Movie Snack | same (DS-51) | 1 |
| B3-15 | A Thousand Sit-Ups | The Only 2 Exercises You Need For Lower Abs (DS-46) | 1 |
| B3-16 | Everything Must Go | The Only 2 Kettlebell Exercises You Need (DS-54) | 1 |
| B3-17 | The Crown Jewel | How To Do Goblet Squats (DS-62) | 1 |

Existing library clips offered on the same page: A0159 (DS-95), A0241 and A0188 (DS-51).
No idea passed for DS-57 (timer), DS-60 (reverse lunges) or DS-64 (3 rules); DS-56 had no opinion line worth a clip.
Next: Dan's selections, `blind.py pick b3/sets/<id> --chose Xn`, then the batch 2 video routine in a `vid-b3/` folder
(plan Omni takes at 5 s or less; one Flow agent; screen, clipcheck, one fresh motion reviewer per kept take).

## Credits

| batch | Flow credits | notes |
|---|---|---|
| batch 1 frames (40 Google images + redos) | 0 | Nano Banana Pro images cost 0 on Ultra |
| batch 1 video (8 clips x 2 Veo Fast + 1 Omni = 24 takes) | 240 | balance 21,826 to 21,586 |
| batch 2 frames (24 Google images) | 0 | |
| batch 2 video (16 clips, 24 takes: 16 Veo Fast + 8 Omni at 10 each) | 240 | balance 21,396 to 21,156 |
| batch 3 frames (49 Google images) | 0 | |
| **total for this handoff so far** | **480** | of 14,000 |

## Dropped (no version passed after two tries per model, or Dan rejected)

Nobody Is Watching, Price Tags, Staring At The Clock, Jogging Between Sets (now on `Docs/NEXT_SHOOT_LIST.md` as real footage,
with the thermostat-at-63 shot), plus Dan's batch 1 rejects (map, plan card, dusty gym bag, bouncer, recliner, hospital curls,
seated fold, ski goggles, penguin). His notes: memory `ai-clip-gags-injury-and-sense`.
Batch 3 (failed twice, or failed on concept): Not On Day One, Way Too Heavy, Everyone Heard That, The Checkered Flag, Doesn't Fit,
Too Many Machines, Not Tonight. Reasons per pair: `b3/review_results.txt`.
