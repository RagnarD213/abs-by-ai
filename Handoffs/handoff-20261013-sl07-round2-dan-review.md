CONTENT | SL-07 | If I Had Belly Fat SFC R3

# SL-07: apply Dan's round 2 answers, put the studio pickups in, close out the five Belly Fat shorts

Written 2026-10-13 by Claude (Opus 5.5) at the end of round 2. All five shorts are rendered with Dan's 10-13 answers.
Three are finished candidates; two wait on studio pickups. Dan has the round 2 page and has not answered it.
Supersedes `handoff-20261012-sl07-round1-dan-review.md` and `handoff-20261012-sl07-belly-fat-shorts-pickups-and-build.md`
(kept for the picks, the spoken text and the standing decisions).

**Recommended: Claude Opus 5.5, high effort** for the round after Dan answers (one AI clip, re-renders, reviews, gates).
The pickup swap after the 10/17 shoot is mechanical once the takes are filed: **Opus 5.5, medium**.

## Where things are

- Review page: http://127.0.0.1:8874/ (`/Volumes/Extreme/_edit_work/sl07/r2/review/`, `page_r2.py` + `notes_r2.py`).
- Work folder: `/Volumes/Extreme/_edit_work/sl07/`. A short is data in `plans.py`. Tools and lessons:
  `.claude/skills/shorts/reference/softblue-sl07/README.md` (read it first).
- Dan's round 1 answers with frame hashes: `round2-plan/decisions.json`. Motion ledger: `motion/ledger.json` ($2.92:
  B $1.40, E $0.40, F $1.12 estimated on Kling).
- Delivered (`Short-form video content/`, REVIEW copies in `belly-fat-90-days REVIEW/`, VLC copies in `Videos to Review/`):

| Short | File | State |
|---|---|---|
| Stop Trying To Lose 1 Pound A Week | `belly-fat-90-days-short1_stop-trying-to-lose-1-pound-a-week.mp4` | finished candidate; second review SHIP, then one pause lengthened (third check was running at handoff) |
| Weigh Yourself Every Morning | `belly-fat-90-days-short2_weigh-yourself-every-morning PLACEHOLDER PICKUP.mp4` | complete except the pickup (desk-mic placeholder, tagged on screen) |
| Work Out Every Morning, Not 3 Times A Week | `belly-fat-90-days-short3_work-out-every-morning PLACEHOLDER PICKUP.mp4` | complete except the pickup; the vacation clip waits on Dan's frame answer |
| The 3-Pound Rule That Keeps Belly Fat Off | `belly-fat-90-days-short4_the-3-pound-rule.mp4` | finished candidate; second review SHIP, judged (0 open defects) |
| Track Your Calories With A Photo | `belly-fat-90-days-short5_track-your-calories-with-a-photo.mp4` | finished candidate; phone demos rebuilt twice after review, last render made at handoff: needs its watch judge |

- Reviews: `r2/reviews/ROUND-2-REVIEW-<S>.md` (first pass, all five DOES NOT SHIP), `ROUND-2B-*` (A, E SHIP; F no),
  `ROUND-2C-*` (A, F third checks). `build/<S>/gate/logs/findings.json` is the judge's file for the current watch pass
  only when its sha matches the delivered file: check before running `watch.py --judge`.
- **The delivery gate has not produced a stamp for any of the five.** It waits while two other builds are active
  (`speech.wait_for_build_slot`), and other sessions were rendering all afternoon. Run it when the machine is quiet:
  `rungate.sh A|E|F` after `watch.py --judge`. Expect the known organic mismatches named in VIDEO-RULES; report every
  failing row with its numbers and never change a bound.

## Waiting on Dan (the round 2 page)

1. The "working out on vacation" frames (`aiframes/D3_start.jpg`, `D3_end.jpg`): yes, change, or no. If yes: add D3 to
   `decisions.json` with the frame hashes, `gen_motion.py D3 D3_v1 4 pair` (prompt: he finishes a push-up, stands and drops
   into bodyweight squats; the family watches; locked camera), check it against the three AI sense questions
   (VIDEO-RULES 2026-10-13), then replace the `abwheel` cover in `plans.py` (321.70 to 325.73, `fy=1.0`, chip placed by
   `chipplace.py`). That short then needs its review again.
2. Four reworded key points (old and new on the page): keep, or his wording.
3. Any other notes.

## The studio pickups (after the 10/17 shoot)

Both lines are on `Docs/PICKUPS_1017_SHOOT.md`. When the takes are filed: cut each line from the roll (lav through
`pick_lav.py`), put it through the film's own voice chain so it matches the film (same set, same mic), write
`pickups/B.wav` and `pickups/D.wav` (stereo, dual mono, with the lead and tail `pickup.py make` uses), remove
`placeholder=True` from `plans.PICKUP`, then `batch.py audio|words|plan|gfx|render` for B and D (the pickup length
changes, so everything after it shifts). The file names lose "PLACEHOLDER PICKUP" by themselves (`deliver.dname`).
Then watch pass, a fresh reviewer and the gate for both. Do not spend time matching the desk recording: Dan's rule.

## What changed in round 2 (all on the page under "What I decided")

- AI clips in: the metronome needle and praying to the scale (two shots) in "Weigh Yourself Every Morning"; one beer on
  the patio in "The 3-Pound Rule"; buried in measuring cups in "Track Your Calories With A Photo" (Kling; Veo refused
  the frame). Killed by Dan: A1, A2, A3, D1, D2, E1, E2, F1.
- After the reviews: the film's AI busy dad replaced by real stock (B0073) in the first short; the dark gym stock
  replaced by the stairs clip (A0159, approved in RO-07) and the ending by Dan's curls (B0031) in the workout short;
  the overhead scale clip opens the weighing short; "sacrifice" whole; chips at u=1.6 placed by person mask; captions
  end on cuts; phone demos rebuilt.
- Key points reworded: B G1, E G1, F G1; A G2 line break. The film's own wording kept on A G2 and D G1.

## Open risks

- The gate has never completed on these files; rows about captions under the phone, hair, coverage and B-roll may need
  `declare` entries with Dan's words, as SL-03 did (`softblue-sl03/README.md`, "Gate plumbing").
- `plan.json`'s `negative_events_scan` text says a reviewer judged the frames; three reviewers objected that it is written
  before the review. Write it after the judge, or reword it.
- The scale clip in "The 3-Pound Rule" shows "90.9 kg" for its last 0.5 s (0:29). Dan was told.
- The metronome needle sweeps more than it bounces. Dan was told.

## Starter prompt

> Name this task "If I Had Belly Fat SFC R3". This is CONTENT. Read `Handoffs/handoff-20261013-sl07-round2-dan-review.md` and execute it: apply my round 2 answers (pasted below), make the vacation clip if I approved its frames, re-render what changed, then run the watch judge, a fresh independent review and the delivery gate on every finished short. The two shorts with pickups stay placeholders until the 10/17 studio takes are in. Use the Codex subscription for any new images. No covers, no upload.
>
> My round 2 answers: [paste the reply box here]
