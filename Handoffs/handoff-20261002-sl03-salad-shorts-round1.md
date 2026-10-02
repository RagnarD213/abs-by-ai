# SL-03 Daily Salad shorts: round 1 (look and graphics for short 1), then the batch

**Written 2026-10-02 by Claude (Opus 5.5). Task name: `Daily Salad SFC R1`. Recommended: Claude Opus 5.5, high.**

## Goal

Cut six vertical shorts (1080x1920) from the approved RO-05 "How I Make My Daily Salad" master. Dan picked the
segments on 2026-10-02. This task does the first approval round: short 1's look and every graphic as stills, on a review
page, then stops for Dan. The batch is cut only after he approves that page.

## Read first

1. `.claude/skills/_shared/VIDEO-RULES.md` (in full), then `Handoffs/video-editing/00-RULES.md`.
2. `Handoffs/video-editing/SL-03-meal-prep-app-demo-shorts.md` (the job doc).
3. `/shorts` skill, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/GRAPHICS-STANDARDS.md`, `_shared/SOFTBLUE.md`,
   `_shared/hyperframes/README.md` (9:16 templates in `vertical.py`).
4. `Handoffs/handoff-20261001-vertical-kit-round2-full-build-after-lock.md`: check whether Dan has answered the RO-10
   vertical graphic-lock page. Whatever he approved there (title treatment, key-point bar, cards, caption placement) is
   reused here and is not asked again. Whatever is still open goes on this round's page.

## Source

`claude edited long form content/08 - How I Make My Daily Salad (Fable recut)/How I Make My Daily Salad | claude round 4 | 16x9 | RO-05.mp4`
(14:54, approved 2026-09-30), with its `.srt` and `.chapters.txt`. Its rebuild recipe is `recipe-RO-05-round4/` in the
same folder; work files from the long-form are in `/Volumes/Extreme/_edit_work/ro05*`. Look there for a no-graphics
master and the EDL before cutting from the delivered file (skill Step 0 and Step 4). Never run scripts inside those
folders; work in a new `/Volumes/Extreme/_edit_work/sl03/`.

## Dan's picks (letters from the shortlist; timecodes are master time from the SRT, to be snapped to measured silence)

| # | Working title | Ranges | About |
|---|---|---|---|
| 1 (A) | Break Your Fast With This | 0:28.4-1:07.0, 1:37.8-1:40.7 | 42 s |
| 2 (B) | The $20 Salad You Can Make For $4 | 1:07.0-1:37.8, 9:33.5-9:46.0 | 50 s |
| 3 (C) | Keep Your Salads Fresh For 7 Days | 6:15-7:09.8, the silent boxing-up stretch near 6:57-7:02 tightened | 50 s |
| 4 (D) | Stop Buying Salad Dressing | 2:25.3-2:52.2, 8:05.9-8:13.9, 8:41.4-9:00 | 54 s |
| 5 (E) | Track A Week Of Meals From One Photo (app) | 12:24.3-12:31.8, 12:38.4-12:51.4, 13:08.6-13:21.3, 13:36-14:04.1 | 55 s |
| 6 (F) | The One Line That Makes AI Calorie Tracking Accurate (app) | 12:51.4-13:33.8, 13:40-13:53.3 | 50 s |

Not picked: G (make it your own) and H (onions). Dan did not change any title. Short 2 opens on "But let's talk about":
start on "let's" if a silence allows, otherwise open with 0:10.8-0:16.9 ("it only costs a few dollars").
E and F share the "7 salads" note and the 683 vs 720 result, so post them far apart.

## Decisions already told to Dan (he did not overrule any)

1. Graphics are Soft Blue Light from the HyperFrames templates, not the J2 olive set (new batch rule, 2026-10-01).
2. App shorts (5 and 6) stack the phone screen over Dan at full size so the screen stays readable. Never shrink it.
3. Each food short (1 to 4) opens on the finished salad (about 11:16-11:19 in the master) for a second or two.
4. Audio is RO-05's approved mix, cut only, gated with `audio_gate.py --reference-mix <master> --verbatim`.
5. No covers, no upload, no queueing in this job. Nothing posts before RO-05 is public on Oct 18.
6. No AbsByAI.com end mark (Dan, 2026-10-01).

## Completed

* Job claimed: `queue.py set SL-03 in_progress --by Claude`, mirrored to the Edit Queue page and marked synced.
* Transcript read from the delivered `.srt`; shortlist of eight sent; Dan picked A, B, C, D, E, F.
* Nothing is rendered. No work directory exists yet. No word-level transcript yet (skill Step 1).

## Exact next action (this round)

1. Rename the task `Daily Salad SFC R1`. Check the two-build cap.
2. Word-timestamp transcript and the timeline preflight (skill Steps 0.9 and 1), silence snap for all six shorts,
   shot detection and treatment per shot (talk, broll, card, the phone stack).
3. For short 1 only: crop and framing proof (hair never leaves the frame), the title treatment, each key-point bar or
   card as a still on its real frame with the words spoken around it, caption placement. For short 5: one still of the
   phone-over-Dan stack, since that layout is new.
4. Build the review page in the standard order (first frames, "What I decided", every item three per row) and stop
   for Dan. Keep it to 20 decisions or fewer.
5. End the round with a handoff for round 2 (the full batch, gates, watch pass, independent audit, review copies,
   `sl03-SHORTS.md`, `queue.py set SL-03 delivered`).

## Open risks

* The vertical Soft Blue Light kit was still waiting on Dan's answers on 2026-10-02 (see item 4 under Read first).
* The salad table shots are wide; per Dan's rule the overhead table is a centre square, not a full-frame crop.
* GitHub pushes from the main folder were blocked on 2026-10-01 by another session's uncommitted files; use
  `scripts/git/safe-push.sh` and report if it stops.
* The board is at its 2,500-word limit; keep the SL-03 entry to a few words.

## Starter prompt

> Name this task `Daily Salad SFC R1`. Read `Handoffs/handoff-20261002-sl03-salad-shorts-round1.md` and do its "Exact next action": prepare the six salad shorts I picked (A to F), then show me short 1's crop, title and every graphic as stills on a review page, plus the phone-over-me layout for the app short, and stop for my approval before cutting the batch. Soft Blue Light graphics, no covers, no upload.
