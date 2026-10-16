CONTENT | SL-07 | If I Had Belly Fat SFC R4

# SL-07 round 4: act on Dan's round 3 notes

Written 2026-10-16 by Claude (Opus 5.5). Supersedes `handoff-20261016-sl07-round3-studio-pickups-and-full-review.md`
(executed). **Fire only after Dan has replied on the round 3 page.** Recommended: Claude Opus 5.5, high effort.

## Where things are

- Round 3 page: http://127.0.0.1:8874/ (`/Volumes/Extreme/_edit_work/sl07/r3/review/`, `notes_r3.py` + `page_r3.py`;
  `review_server.py 8874 <dir>` after any change). VLC copies: `Videos to Review/If I Had Belly Fat SFC R3 - <title>.mp4`.
- Work folder `/Volumes/Extreme/_edit_work/sl07/` (a short is data in `plans.py`). Tools, lessons and the round 3 section:
  `.claude/skills/shorts/reference/softblue-sl07/README.md` (read "Round 3" first).
- Delivered (`Short-form video content/belly-fat-90-days-short{1..5}_*.mp4`): **all five pass the delivery gate 39/39
  (GATE 2.6.1, stamped) and a fresh independent review (SHIP, 0 defects)**. Reviews: `r3/reviews/ROUND-3B-*`, `ROUND-3C-REVIEW-D.md`.
- Pickups: B ships the band-matched treatment (`pickups/lavfit/match_B.json`), D ships the film voice EQ
  (`pickups/filmchain/` keeps the other). Both crossfade into the film room tone (`plans.PICKUP xfade`; D also `preroll=0.2`).
  The other version of each is on the page; swapping is `pickup.py make ... --eq-json` + `batch.py audio S` + `remux.sh`.
- AI clips: every one has a clipcheck stamp plus a frame-reviewer PASS on its used range (`clips/*.clipcheck.json`).
  AI_B1 is now `clips/AI_B1_fix.mp4` (dial rebuilt by `r3_needle.py`); AI_B2a is out; AI_F2 ends on frame 102.

## Dan's open decisions on the page

1. Pickups: which version of each, or how it sounds off.
2. New and changed clips (A scale/rope/curls/kitchen, E salad/ab wheel, D stairs, B needle): keep or swap.
3. Vacation frames (`aiframes/D3_start.jpg`, `D3_end.jpg`): if yes, `gen_motion.py D3 D3_v1 4 pair` (about $0.60), clipcheck
   and a fresh frame-reviewer, replace the `abwheel` cover in D (now 24.7 to 28.7 s), re-review D.
4. Four reworded key points: keep or his wording.
5. "Track Your Calories" 0:37 to 0:40: "Today's total" back or not.
6. Capital-letter labels ("LOSE YOUR BELLY FAT", "KEY POINT"...): title case if he asks.

## Method for each change

Edit `plans.py` (or the pickup), then `batch.py audio|words|plan|gfx|render S` as needed, `r3_post.py S` (deliver copy, watch,
plan), a fresh `ra-reviewer` with `r3_brief.py S` (one findings entry per watch image, pairs included), `watch.py --judge`,
`deliver.py plan S`, then `r3_gates.py S` (one gate at a time). Replace the VLC copy, refresh the page, list each change with
timestamps (later-round rule). When Dan finalizes: delete the VLC copies and stop port 8874 (`review_server.py 8874 --remove`),
register new clip uses (`clip_library.py add`: B0019, B0448, B0031, B0073, p6719385 uses; AI_B1_fix as a new clip).

## Risks

- `/Volumes/Extreme` was full (0 bytes) on 10-16; write frame dumps to the session scratchpad.
- Never `sed -i` a log another process appends to; never `pgrep -f` from a shell line containing the pattern.

## Starter prompt

> Name this task "If I Had Belly Fat SFC R4". This is CONTENT. Read `Handoffs/handoff-20261016-sl07-round4-after-dan-r3-review.md` and my round 3 notes below, then make the changes, re-run the review and gate on every changed short, and give me the round 4 page with timestamps for each change. No covers, no upload.
> [paste Dan's round 3 reply]
