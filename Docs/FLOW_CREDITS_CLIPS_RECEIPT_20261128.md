# Flow credits: AI clips for the next edits (receipt, running; final by 2026-11-28)

Handoff: `Handoffs/handoff-20261107-flow-credits-ai-clips-for-next-edits.md` (budget up to 14,000 credits; Ultra 20x drops Nov 29).
Batches 2 and 3: `Handoffs/handoff-20261113-flow-credits-ai-clips-batch-2-3.md` (executed). Next batch: `Handoffs/handoff-20261115-flow-credits-ai-clips-batch-4.md`. Credit log: `Media/flow-credit-log.md`.

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

## Batch 2 video: approved and filed (Dan, 2026-11-13)

Dan approved all five ideas and kept **both** versions where there were two, so the editor has a choice ("they are both good. I want to
give the editors options"). All eight clean cuts are in the clip library, tag `flow-credits-batch2`, status usable-unused, sheet refreshed.
Each ID is under "Pre-made AI clips" in its job doc. Blind log: `blind.py pick` recorded X1,X2 for B2-01, B2-02, B2-05; `veo.py pick`
recorded "same" for B2-01 and B2-05 (their two versions came from different video models).

| Library ID | Clip | Video (job) | Clean cut |
|---|---|---|---|
| A0255 | Can't Go In, front view | Why I Use Machines And Cables Instead Of Barbells At 41 (DS-99) | 3.0 s |
| A0256 | Can't Go In, side view | same (DS-99) | 4.3 s |
| A0257 | Sitting On His Phone, closer view | Why You Should Walk Between Your Sets (DS-103) | 2.3 s |
| A0258 | Sitting On His Phone, wider view | same (DS-103) | 4.1 s |
| A0259 | Laid Up | Why You Must Stretch After Every Workout (DS-104) | 2.9 s |
| A0260 | The Straddle Stretch, front view | same (DS-104) | 3.0 s |
| A0261 | The Straddle Stretch, side view | same (DS-104) | 2.5 s |
| A0262 | Thermostat On 63 | Why I Sleep At 63 Degrees (DS-50) | 2.0 s (a start-frame-only retake `B2-06s`, 2 takes, was screened out: the duvet moved by itself and "63" flipped to "62" again) |

Work folder `~/Projects/_edit_work/FLOWCLIPS/vid-b2/` (prompts/, specs/, picks.json, windows.json, motion_results.txt, build_review.py,
file_library.py, library_ids.json). Review page http://127.0.0.1:9244/ . Every clip passed `clipcheck.py` and a fresh motion reviewer;
library entries hold only the clean window, the full takes stay in `vid-b2/veo/`.

Lesson for the next video batch: every Omni 1.1 Flash 6 s take re-rendered (went soft, changed texture) at frame 128, about 5.3 s in, so only
the first 5 s of an Omni take is usable; Veo Fast takes showed talking mouths and hands passing through feet late in the take. Two of three
thermostat takes flipped "63" to "62": quote on-screen numbers in the prompt and check them on every frame.

## Batch 3 frames: Dan selected 7 of 14 (2026-11-13)

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
**Dan's selections (2026-11-13):** B3-02 Bored To Sleep, B3-03 First Day, B3-08 Lighter And Fine With It, B3-12 Only Five,
B3-13 Lighter But Weaker, B3-14 Movie Snack, B3-15 A Thousand Sit-Ups (7 ideas, one version each; `blind.py pick` recorded for B3-02, B3-08, B3-12),
plus the three existing clips A0159 (already in the DS-95 job doc), A0241 and A0188 (now in the DS-51 job doc). Not selected, so out:
B3-01, B3-05, B3-06, B3-07, B3-21, B3-16, B3-17.

## Batch 3 video: made, waiting for Dan's picks (2026-11-13)

Work folder `~/Projects/_edit_work/FLOWCLIPS/vid-b3/` (setup.py, clips.json, prompts/, specs/, picks.json, windows.json, motion_results.txt,
build_review.py). Flow project https://flow.google.com/project/52f3eb0e-cff4-4795-9bbd-ce43e678c7fb . 21 takes (14 Veo Fast, 7 Omni), no failures.
Review page http://127.0.0.1:9246/ (Select buttons; untouched means out). Every clip passed `clipcheck.py` and a fresh motion reviewer and
plays only its clean window.

| Clip | Video (job) | Take | Clean window |
|---|---|---|---|
| Bored To Sleep | How To Use The Stairmaster To Burn Fat (DS-94) | Omni | 4.3 s |
| First Day | What To Do Your First Day At The Gym (DS-95) | Veo Fast | 4.9 s (frozen and nervous; the head turn itself is outside the window) |
| Lighter And Fine With It | How To Pick The Right Weight On Every Exercise (DS-96) | Omni | 4.6 s |
| Only Five | The Only 5 Machines You Need At The Gym (DS-98) | Omni | 3.0 s |
| Lighter But Weaker | 3 Ways To Lose Fat Without Losing Muscle (DS-51) | Omni | 4.3 s |
| Movie Snack | same (DS-51) | Omni | 4.8 s |
| A Thousand Sit-Ups: the sit-up | The Only 2 Exercises You Need For Lower Abs (DS-46) | Omni | 3.3 s |
| A Thousand Sit-Ups: worn out on the floor | same (DS-46) | Veo Fast | 4.3 s |

Screened out before review: Fast takes with dumbbell curls (B3-08), an arm raised to the head (B3-12, both), a second egg falling (B3-14).
Six of the eight kept clips are Omni takes: with a window planned inside the first 5 s (before the frame-128 re-render) Omni followed the
"nothing else moves" prompts more closely than Veo Fast in this batch.
Next: Dan's picks, then `clip_library.py add <window cut> --kind ai --status usable-unused --used-in "<job> <title> (planned)" --tags flow-credits-batch3`
(copy `vid-b2/file_library.py`), `clip_library.py sheet`, IDs under "Pre-made AI clips" in the DS-94, DS-95, DS-96, DS-98, DS-51, DS-46 job docs.

## Batch 3: seven clips selected and filed (Dan, 2026-11-14)

Dan's picks on the redo page: Bored To Sleep (redone), First Day (redone), Only Five, Lighter But Weaker, Movie Snack and both
A Thousand Sit-Ups moments. Filed with tag `flow-credits-batch3`, status usable-unused, sheet refreshed (1,014 clips); IDs are under
"Pre-made AI clips" in the DS-94, DS-95, DS-98, DS-51 and DS-46 job docs. Library adds ran on the M2 (`vid-b3/file_library.py`, `library_ids.json`).

| Library ID | Clip | Video (job) | Clean cut |
|---|---|---|---|
| A0263 | Bored To Sleep (steps running) | How To Use The Stairmaster To Burn Fat (DS-94) | 3.8 s |
| A0264 | First Day (looks around, fidgets) | What To Do Your First Day At The Gym (DS-95) | 5.3 s (strict window 2.2 s, frames 75-127) |
| A0265 | Only Five | The Only 5 Machines You Need At The Gym (DS-98) | 3.0 s |
| A0266 | Lighter But Weaker | 3 Ways To Lose Fat Without Losing Muscle (DS-51) | 4.3 s |
| A0267 | Movie Snack | same (DS-51) | 4.8 s |
| A0268 | A Thousand Sit-Ups: the sit-up | The Only 2 Exercises You Need For Lower Abs (DS-46) | 3.3 s |
| A0269 | A Thousand Sit-Ups: worn out on the floor | same (DS-46) | 4.3 s |

Dumbbell clips (DS-96): Dan picked X1 for both ("I like X1, but I want to change the weight ... It just looks ridiculously light now.
Make the lighter strict-form basically one plate lighter than the current X1, and then the current X1 one plate heavier"). `blind.py pick`
recorded X1 for B3-22b and B3-23. His two X1 picks were different men.

Round 2 frames, page http://127.0.0.1:9248/ (M6, `vid-b3r/review2`, builder `vid-b3r/build_frames2.py`, keys `b3r2picks`):
- Strict form `B3-23c`, two plates per end, drawn in both men; both pairs gate + fresh reviewer PASS (page labels A and B).
- Cheat, one plate heavier (`B3-22c`): DROPPED after three routes in the source of his pick. END-first: a bright line down the wrist and
  mismatched small discs; END-first again: the dumbbell drawn as two plate stacks with no handle or hand; START-first: clean skin and a
  21 degree lean, but the lifted dumbbell changes type and plate count between START and END. The page offers the two cheat pairs that
  already passed: his pick as seen (about three plates per end) and the other version (heaviest dumbbells, the man from his strict pick).
Lesson: Nano Banana Pro does not keep a plate-loaded dumbbell identical between two frames when the pose changes a lot; ask for fixed
one-piece dumbbells, or draw the heavy pair in one source only. All attempts and reviews: `/Volumes/Extreme/_edit_work/FLOWCLIPS/b3r/review_results.txt`.
Next: Dan's picks on 9248, `veo.py add` for the chosen pairs (paths on the Extreme are the same on both Macs), video, reviews, page, file.

## Dumbbell clips: approved and filed (Dan, 2026-11-15, "Keep both")

| Library ID | Clip | Video (job) | Clean cut |
|---|---|---|---|
| A0270 | Cheating The Heavy Ones (side view, three fast jerky reps) | How To Pick The Right Weight On Every Exercise (DS-96) | 3.4 s |
| A0271 | Lighter, Strict Form (same man, back against a wall) | same (DS-96) | 5.0 s |

Tag `flow-credits-batch3`, status usable-unused, sheet refreshed (1,017 clips); both IDs are under "Pre-made AI clips" in the DS-96 job doc
(`vid-b3d/file_library.py` on the M2). **Batches 1 to 3 are finished: 25 new clips, A0247 to A0271, for 1,060 of the 14,000 credits.**
Next batch: `Handoffs/handoff-20261115-flow-credits-ai-clips-batch-4.md`.

## Dumbbell clips video: how round 2 was made (2026-11-14)

Dan picked **X2 with B** on the frames page (cheat pair with the heaviest dumbbells, strict pair with the same man; `blind.py pick` recorded
for B3-22b and B3-23c). Round 1 video (cheat heave-and-hold, free-standing strict reps) came back with: "Regenerate both. On the top one,
have him do a quicker rep ... quickly and jerkily going down. For the strict ones, he's rocking a little bit. Just have him not rock and do
strict reps." Round 2 is on http://127.0.0.1:9249/ (M6, `vid-b3d/review`, keys `b3dpicks`).

| Clip | Take | Clean window | Checks |
|---|---|---|---|
| Cheating The Heavy Ones (`B3-22e`) | Omni, START frame only | 3.4 s, frames 0-80: three fast jerky reps (borderline hard drop at 47-48; 0-47 if nothing borderline is wanted; never past 80) | clipcheck PASS, fresh reviewer PASS |
| Lighter, Strict Form (`B3-23g`) | Veo Fast, new frames `B3-23w` with his back against a wall | 5.0 s, frames 8-127: one full rep plus most of a second | frame pair gate + reviewer PASS (second draw); clipcheck PASS; fresh reviewer PASS: head 3.7 px side / 8.0 px up-down (rejected take 21 / 17) |

Job `~/Projects/_edit_work/FLOWCLIPS/vid-b3d/` (M6; setup.py, setup_r2.py, setup_wall.py, picks.json, windows.json, motion_results.txt,
sway.py, sway2.py, build_review.py); takes, specs, stamps and reviews at `/Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b3d/`. Flow project
https://flow.google.com/project/c7d70179-327f-44ff-8027-bfd4eb581b15 . 27 takes over five Flow runs.

Lessons (also in `vid-b3d/motion_results.txt`):
- A man standing free and curling: Veo Fast and Omni both dip his head 15-23 px on every rep whatever the prompt says ("statue", "head stays at
  the same height"). Wording and Omni cut side-to-side sway by half; only a physical anchor in the frame (back and head against a wall) stopped
  the dip. Stage strict or "no movement" exercises against a wall, a pad or a bench.
- Measure rocking before spending a reviewer: `vid-b3d/sway2.py TAKE:A-B` (tracked points on head and chest).
- A motion that must come back down needs the START frame only; an END frame at the top forces a slow hold. Veo Fast turned the plate dumbbells
  into one-piece hex dumbbells in the fast cheat takes; Omni kept them.
- Omni takes often pout, part the lips or close the eyes during effort; say eyes on the camera and screen the face frame by frame.
Next: Dan's picks on 9249, then library adds on the M2 (`--tags flow-credits-batch3`), sheet, IDs in the DS-96 job doc.

## Batch 3 redo: on Dan's page (2026-11-14)

Dan on the batch 3 video page: Bored To Sleep unrealistic because the machine is not moving ("he'd have the treadmill moving slowly with him
being bored"); First Day "too frozen ... looking around from side to side, slightly shifting his weight"; Lighter And Fine With It replaced by
two clips of the slim guy, slightly more muscular, in a tank top: one cheating with weights like the bodybuilder's, one with correct form
and lighter weights. The other five clips (Only Five, Lighter But Weaker, Movie Snack, A Thousand Sit-Ups x2) are unchanged and unpicked.

One page for everything still open: http://127.0.0.1:9247/ (served on the M6 from `~/Projects/_edit_work/FLOWCLIPS/vid-b3r/review`;
keys `b3rpicks`). Work folders: M6 `~/Projects/_edit_work/FLOWCLIPS/vid-b3r/` (setup.py, picks.json, windows.json, motion_results.txt,
build_review.py) and, so both Macs see the same paths for the gates, `/Volumes/Extreme/_edit_work/FLOWCLIPS/{b3r,vid-b3r}/`
(frames, specs, stamps, reviews, `b3r/review_results.txt`). Flow ran in the M2's Chrome (the only one connected); downloads came back by scp.

| Item | What is on the page | Checks |
|---|---|---|
| Bored To Sleep (DS-94), redone | Omni take from the START frame only, steps running, eyes open; 3.8 s (frames 36-127) | clipcheck PASS with a documented 18 px bound (machine floats about 10 px, background within 1 px); fresh reviewer PASS |
| First Day (DS-95), redone | Omni take from the START frame only, looks right, back left, regrips, shifts; 5.3 s shown (0-127), strict window 75-127 | clipcheck PASS (camera 1.3 px); fresh reviewer PASS |
| Cheating The Heavy Ones (DS-96), new frames `B3-22b` | side view, two versions (blind X1/X2) | both pairs gate + fresh reviewer PASS |
| Lighter, Strict Form (DS-96), new frames `B3-23` | front view, two versions (blind X1/X2), each labelled with the cheat version that has the same man | both pairs gate + fresh reviewer PASS |

Dropped on the way: the front-view cheat pair in both sources (a lean back does not read head-on; END failed twice), a strict pair with
elbows flared wide (redrawn), a strict pair whose dumbbells changed type between frames (redrawn without stamps).
Flow projects: video https://flow.google.com/project/2dadf483-422d-4f64-b3b6-b36a13bc2044 , images
https://flow.google.com/project/a9ede1c5-b49a-4395-b20c-e8e6064802cf .
Next: Dan's picks; file the kept clips (`--tags flow-credits-batch3`, library adds run on the M2, which holds the catalog); video for the
frame versions he selects (`blind.py pick /Volumes/Extreme/_edit_work/FLOWCLIPS/b3r/sets/<id> --chose Xn` first).

Lessons: a clip with the START frame only gives freer motion (fidgeting, a running machine) but the picture floats; Omni floated least.
A lean BACK must be shot from the side. Give each image source its own man for every clip in a set, and say on the page which versions match.
`veo.py collect` cannot find ffprobe on the M6 (its repo path is one folder short); put `Media/video_edit/bin` on PATH for collect.

## Credits

| batch | Flow credits | notes |
|---|---|---|
| batch 1 frames (40 Google images + redos) | 0 | Nano Banana Pro images cost 0 on Ultra |
| batch 1 video (8 clips x 2 Veo Fast + 1 Omni = 24 takes) | 240 | balance 21,826 to 21,586 |
| batch 2 frames (24 Google images) | 0 | |
| batch 2 video (16 clips, 24 takes: 16 Veo Fast + 8 Omni at 10 each) | 240 | balance 21,396 to 21,156 |
| batch 3 frames (49 Google images) | 0 | |
| batch 2 retake (sleep clip, 2 Veo Fast takes) | 20 | balance 21,156 to 21,136 |
| batch 3 video (7 clips, 21 takes: 14 Veo Fast + 7 Omni at 10 each) | 210 | balance 21,042 to 20,832 |
| batch 3 redo video (8 takes: 6 Veo Fast + 2 Omni at 10 each) and 7 Google images | 80 | balance 20,702 to 20,622 |
| dumbbell clips video (6 takes: 4 Veo Fast + 2 Omni at 10 each) and 16 Google images | 60 | balance 20,582 to 20,522 |
| dumbbell clips redo (21 takes over four runs: faster cheat, strict free-standing x3 rounds, strict against the wall) | 210 | balance 20,522 to 20,312 |
| **total for this handoff so far** | **1,060** | of 14,000 |

## Dropped (no version passed after two tries per model, or Dan rejected)

Nobody Is Watching, Price Tags, Staring At The Clock, Jogging Between Sets (now on `Docs/NEXT_SHOOT_LIST.md` as real footage,
with the thermostat-at-63 shot), plus Dan's batch 1 rejects (map, plan card, dusty gym bag, bouncer, recliner, hospital curls,
seated fold, ski goggles, penguin). His notes: memory `ai-clip-gags-injury-and-sense`.
Batch 3 (failed twice, or failed on concept): Not On Day One, Way Too Heavy, Everyone Heard That, The Checkered Flag, Doesn't Fit,
Too Many Machines, Not Tonight. Reasons per pair: `b3/review_results.txt`.

## Batch 4 frames: on Dan's page (2026-11-15)

Handoff `Handoffs/handoff-20261115-flow-credits-ai-clips-batch-4.md`. Work folder (same path on both Macs) `/Volumes/Extreme/_edit_work/FLOWCLIPS/b4/`
(ideas.py, prompts/, codex/, google/, pairs/, sets/, review_results.txt, review_queue.json, build_page.py, GOOGLE-BRIEF.md, GOOGLE-REDO*.md, REVIEWER-BRIEF.md).
Frames page **http://127.0.0.1:9251/** (M6; Select buttons, each version selectable on its own so Dan can keep both; untouched means out; keys `b4picks2`).
Flow image projects: https://flow.google.com/project/5cdf6f93-b6d6-4c02-891e-96680411db96 (A + redraws), https://flow.google.com/project/e9f527cd-aab6-43fe-ac4b-dbfefb106742 (B).
Credits: 0 spent (20,312 before and after); 62 Google images, 61 Codex images, 58 fresh frame reviews.

Videos: the five 11/13 long-forms (16:9) RO-39 Tesla, RO-40 I'm 41 / 25 Again, RO-41 15 Healthy Foods, RO-42 Bulking Is a Scam, RO-43 7 Made-Up Rules;
Shorts (9:16) DS-106 Sardines and DS-101 Wide Back. Skipped: DS-107 (already approved R2), DS-54/DS-62/DS-60 (how-to lines only; Dan passed on last ideas), DS-57 (no fresh line; A0271 offered).

| id | Idea | Video | On the page |
|---|---|---|---|
| B4-02 | Stuck In Traffic | RO-39 | X1/X2 |
| B4-03 | Learning To Love It | RO-40 (also fits RO-42) | X1/X2 |
| B4-04 | Can't Look (scale peek) | RO-40 | 1 (Codex) |
| B4-05 | The Health Food Aisle | RO-41 | X1/X2 |
| B4-06 | Just A Quarter Cup | RO-41 | X1/X2 |
| B4-07 | Where Did It Go (opaque pouch) | RO-41 | 1 (Codex) |
| B4-08 | Cola For Breakfast | RO-41 | 1 (Codex) |
| B4-09 | Two Tablespoons | RO-41 | X1/X2 |
| B4-10 | Three Cans | RO-41 | X1/X2 |
| B4-11 | Second Plate | RO-42 | 1 (Google) |
| B4-12 | I Bench 315 | RO-42 | X1/X2 |
| B4-13 | Won't Button | RO-42 | X1/X2 |
| B4-14 | Steps Before Bed | RO-43 | X1/X2 (START-only video planned) |
| B4-15 | Eight Glasses | RO-43 | 1 (Codex) |
| B4-16 | Treadmill Milkshake | RO-43 | X1/X2 (START-only video planned) |
| B4-17 | Kitchen Closed | RO-43 | X1/X2 |
| B4-18 | Meal Four Of Six | RO-43 | X1/X2 |
| B4-19 | The Rule Book | RO-43 | 1 (Codex) |
| B4-21 | The Gym Bag | DS-106 | X1/X2 |
| B4-22 | Sit Up Straight | DS-101 | X1/X2 |

Dropped after two failures in both sources: B4-01 Blinders (head turn never read; hair and harness redrawn), B4-20 The Desk Drawer (drawer across his lap, then
a drawer with no front; Google's tin never left the grid). Existing library clips offered on the same page: A0239 (RO-42), A0143, A0181, A0183, A0185 (RO-41),
A0243, A0173, A0144 (RO-40), A0188 (DS-106), A0270, A0271 (DS-64; A0271 also fits DS-57).

Lessons (frames): props that a person uses must exist and change in both frames (containers drawn already open, a lid from nowhere; a see-through bag
emptying by itself; a tin that never leaves a full drawer). Say "every one closed with its lid on" / "opaque pouch" / "one fewer in the drawer". Codex ENDs
came back one pixel narrower twice (1671 vs 1672): resize to the START size before `gate.py`. Google turned a cola into a beer (clear bottle, creamy head)
and misspelled a book title in an END ("PITNESS"). Reviewers recording on the M6 waited 10 to 25 minutes behind a heavy render; record on the M2
(`record_reviews.sh`, or `ssh m2 ... gate.py --review`). Moving a pair aside while its reviewer is still recording leaves that review orphaned in `r1/`.
Next: Dan's picks on 9251, then `blind.py pick` for X1/X2 sets, `veo.py add` per picked pair (Veo Fast x2 + Omni x1; START-only for B4-14/B4-16), video.

## Batch 4 video: made, reviews handed off (2026-11-15)

Dan picked 18 frame pairs plus all 11 existing clips (existing ones now listed in the RO-40, RO-41, RO-42, DS-106, DS-64, DS-57 job docs; blind picks
recorded). Video: 54 takes in `/Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/veo/` (Flow projects
https://flow.google.com/project/15feecac-1a20-4287-8325-f08eba3351be and https://flow.google.com/project/61011229-2dbc-4824-9eb7-77f6e0128d56);
all passed clipcheck. Credits: 20,312 before; 19,822 read while half B was finishing (about 540 expected for 54 takes); final read pending.
Motion reviews stopped when Claude's weekly limit ran out (resets Nov 19, 10 AM Central): handed to Codex in
`Handoffs/handoff-20261115-flow-clips-batch4-motion-reviews.md`.
