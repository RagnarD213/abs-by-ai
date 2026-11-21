# RO-17 "3 Healthy Foods That Made Me Fat": round 4, One can and done motion, then the full film

**LFC (long-form content, 16:9).** Sidebar name: `3 Healthy Foods LFC R4`.
Written 2026-10-15 by Claude (Opus 5.5) at the end of round 3. Recommended: **Claude Opus 5.5, high effort.**

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (top sections), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`
("The full video"), `.claude/skills/longform-edit/SKILL.md` (edit sheet, delivery gate, watch pass, Step 8.6), `.claude/skills/longform-edit/reference/ro17/README.md`
and this file. Decisions with hashes: `/Volumes/Extreme/_edit_work/RO-17/round4-plan/decisions.json`.

## Dan's decision (2026-10-15)

*"Everything looks good. Give me the handoff to build the full film in the next round."* That approves the new One can and done (A10) frames
(a ripped, lean man in a tank top; motion authorized) and everything shown in round 3. Nothing is pending from Dan. This round builds and delivers the film.

## Where things are

- Work dir: `/Volumes/Extreme/_edit_work/RO-17/round3/` (links to round 2 inputs: lav, shots, words, look, fit, framing, stock, assets, hf, cache).
  Recipe `round3/recipe/` (repo copy `.claude/skills/longform-edit/reference/ro17/round3/`). Build round 4 there in place (round 3 was never rendered as a film);
  put the master in `round3/final/`.
- Locked AI clips (gate + fresh reviewer PASS, reviews in `round3/motion/takes/clipcheck/`), cut to `round3/motion/final/<ID>.mp4`, chip corners in
  `motion/final/chips.json`. `plan.py` turns every AI slot listed in chips.json into a labelled clip (AI-GENERATED, max_len = clip length):

| ID | name | take, frames | length | note |
|---|---|---|---|---|
| A3 | The calorie scale (opener) | A3_t4 0-84 (Veo) | 3.54 s | white yogurt raisins; cut before f86 where the beam swings back; 3 takes failed (jug marks, pour through glass) |
| A2 | Couch snacking | A2_t1 16-143 (Veo) | 5.33 s | white yogurt raisins |
| A4 | Candy in the nut jar | A4_t2 8-128 (Veo) | 5.04 s | ends on a full wink |
| A1 | The hiker at his desk | A1_t2 0-45 (Veo) | 1.92 s | only the typing part; starts on "sitting at a desk"; 3 takes failed once the hand entered the bag |
| A5 | Grapes vs raisins | A5_t3 18-120 (Kling, 720p, light sharpen) | 4.29 s | starts on "and all the water in it" |
| A7 | Nothing left for dinner | A7_t3 10-115 (Kling, 720p, light sharpen) | 4.42 s | Veo's filter refused these frames twice |
| A8 | The boardroom | A8_t2 24-119 (Veo) | 4.00 s | one toss |

- C13 is cut (`plan.py`); the join at 4:21 is T2 to W2, `build.jumps()` empty.
- Round 3 frames page: http://127.0.0.1:8879/ (managed service; remove it with `review_server.py 8879 --remove` once the film page is up).

## Then, in order

1. **A10 motion.** Frames `round3/aiframes/A10-start.png` / `-end.png` (gate + reviewer PASS; `require_pass` holds). Prompt beats in order (the reviewer's
   note): he bites and eats the last sardine (a real bite and chew, the fish never vanishes), drops the fork into the empty tin, sets the tin on the sofa back
   beside his left shoulder (it must not slide or shrink), puts his hands behind his head, leans back content. `cd round3/motion && python3 gen_motion.py
   A10:6` (prompt `prompts/A10.txt`, write it first). Slot 4.06 s. Then `clipq.py A10_t1:A:B` (one at a time, it waits on `buildcap`), a fresh
   `frame-reviewer` with the three questions, `prep_clips.py A10=A10_t1:A:B`. Budget: $13.90 spent of $15 (conservative); one take $0.90. **If it fails,
   use a clean part or Dan on camera; a retake needs Dan's OK for more budget (ask alone, with the number).**
2. **Resolve and graphics.** `python3 recipe/resolve.py` (check A10 is `clip`), then `from_plan.py` dry run against `round2/hf` (no graphic changed, so nothing
   should re-render; if one must, copy `hf/` into round3 first: it is a link to round 2 and must not be overwritten). `dupscan.py`.
3. **Render.** `build.render_range(0, 452.15, round3/final/RO17_MASTER.mp4)` (check the end time against `shots.json`). Mind the two-build cap
   (`buildcap.py`); the machine has been busy all week.
4. **Finish chain:** `recipe/finish_chain.sh` (adapted for RO-17 this round: RO17 names, chapters intro/Trail Mix/Dried Fruit/Coconut Water/What I snack on
   instead/recap, `audio_joins`). Audio gate, transcript, SRT from the delivered audio, chapters, watch pass, `haircheck.py`, hyperframes `checks.py`.
   Then your own negative-events scan into `plan.json`, `watch.py --judge` with a fresh judge, edit sheet + `validate.py --hash`, delivery gate
   `--format longform`.
5. **Independent review:** one fresh `ra-reviewer` on the delivered file: every image incl. pair strips; the three AI questions per clip; the cuts around A1
   (1.9 s cutaway) and A3 (3.5 s opener); the 720p softness of A5/A7 next to studio footage; labels clear of faces. Fix, re-render, re-gate.
6. **Deliver** to `claude edited long form content/<NN> - 3 Healthy Foods That Made Me Fat/` (REVIEW 540p, audio A/B, stamps, notes, recipe). Copy the full
   film to `Videos to Review/3 Healthy Foods LFC R4 - full film.mp4`, open the folder, film page with a "What I decided" list (the round 3 calls above),
   and a revision list with timestamps for what changed since round 2 (A-clips now moving, C13 gone, A1/A5 slot moves).
7. `queue.py set RO-17 delivered`, mirror to the Edit Queue page, board entry, register the seven used AI clips plus A10 in the clip library
   (`clip_library.py add ... --status used-final --used-in RO-17`), copy recipe changes to the repo, `safe-push.sh`.

## Traps this round paid for (also go in `reference/ro17/README.md`)

1. **Veo prints measuring marks on a glass measuring jug** mid-pour, then they vanish (2 of 2 takes). Painting them out failed twice (faint ticks stay, rim
   breaks, glass goes mushy). Calling it "a plain glass water pitcher, no markings" in the prompt fixed it.
2. **Kling keeps hands and props steadier but pours through glass** and keeps the jug full while the pan fills; it outputs 720p (about 3x softer upscaled).
3. **The motion gate cannot see gaze, bag fill levels, beam angles or vessel markings**; the reviewers caught every one. Expect one or two fails per clip.
4. **Replicate 429 on submit is free; E005 (filter) failures show no billable seconds** in the prediction metrics. Count both as $0 after checking.
5. **`pkill -f <pattern>` matched the parent shell** that held the pattern in its command line and killed a running generation; queue with `after.sh`.
6. **Hand-stamped orbs read as stickers**; edit a 4x crop with Codex and paste it back instead (A2's third frame review passed that way).

## Cost ledger

Known: motion $13.90 (Veo 3.1 Fast $0.15/s, Kling v3 standard about $1.00 a take; ledger `round3/LEDGER.json`, rows `round3/motion/spend.jsonl`),
Gemini $0.75 (round 2), Codex images on the subscription ($0). Cap $15. Unknown: Kling's exact per-take price (estimate used).

## Starter prompt

> CONTENT (LFC). Name this task `3 Healthy Foods LFC R4`. Read and execute
> `Handoffs/handoff-20261015-ro17-round4-a10-motion-and-full-film.md`. I approved everything in round 3, including the new One can and done guy.
> Make his clip, check it, then build the full film, every gate, independent review, and send me the review copy with timestamps of what changed.
