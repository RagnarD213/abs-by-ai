# SL-03 Daily Salad shorts: round 2 (record Dan's answers, moving previews, then the batch)

**Written 2026-10-02 by Claude (Opus 5.5). Task name: `Daily Salad SFC R2`. Recommended: Claude Opus 5.5, high.**
Fire only AFTER Dan has answered the round 1 page.

## Where round 1 stopped

Review page: `http://127.0.0.1:8809/` from `/Volumes/Extreme/_edit_work/sl03/round1/`
(restart: `python3 .claude/skills/_shared/review_server.py 8809 /Volumes/Extreme/_edit_work/sl03/round1`).
It shows short 1's opener, three crops, two key points, the salad cutaway, the six title bands, hair evidence and two
phone layouts for the app shorts. Nothing is rendered as video. Spend $0.

Dan owes eight answers (the reply box): 1 title band, 2 title copy (six), 3 key-point bar look and position,
4 key-point copy G1 and G2, 5 salad shots fill or square, 6 app layout B (beside) or A (stacked), 7 hair at the top
edge, 8 corner AbsByAI.com.

## Read first

1. `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, `/shorts` skill, `_shared/PRE-RENDER-APPROVAL.md`.
2. `.claude/skills/shorts/reference/softblue-sl03/README.md` (round 1 tooling and what it learned).
3. `Handoffs/handoff-20261002-sl03-salad-shorts-round1.md` (Dan's picks, the decisions already told to him).
4. `_shared/hyperframes/README.md` ("9:16 layouts", `composite.py`), `_shared/cut/README.md`, `shorts/reference/zeeshan-master/README.md` (verbatim audio, 320k AAC).

## State (verified 2026-10-02)

- Source of truth: RO-05 round 4, `/Volumes/Extreme/_edit_work/ro05-fable/round4/full/`: `MASTER.mp4` (sha256
  23fdcb0c86469cb7..., same as the delivered file), `timeline.json` (V pieces: roll, in, f0/f1, scale, cx; A pieces),
  `mapped-words.json` (word times on the film timeline), `voice_raw.wav` (dry voice, same clock). Its `base.mp4` has
  title cards and the phone baked in: do NOT cut picture from it.
- Picture source: RAW rolls `/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C15xx.MP4` (1920x1080) with
  `ro05-fable/round2/grade/luts_B/<roll>.cube` (the long-form's chain, `lib.raw`). Phone: `screen_capture_TAKE2.MP4`
  through `lib.screen_t` (the long-form's SYNC table and banned ranges).
- Audio: the MASTER's approved mix, cut only. Preflight passed (decoded vs container +7 ms; lag 0.0 ms at 10 points).
- Cut points: `/Volumes/Extreme/_edit_work/sl03/segments.json` (S1 38.5 s, S2 44.1, S3 49.0, S4 53.2, S5 57.3, S6 54.5).
  Three need an ear check before rendering: S3 in 378.20 (not in measured silence; fallback 375.90), S4 in 145.33
  (20 ms inside a long-form audio join), S1's pull-out near 46.8.
- Short 1 plan: `sl03/round1/shots_S1.json` (windows, face ranges, graphics with word times). Layout: title band
  y 0 to 310, picture 1080x1610 under it; full window 724x1080, closer 604x900, both from source row 0; bar box
  68,1130 to 1012,1378 (two lines only); captions from y1412.
- Hair: the camera framed his hair at source row 0 in every short 1 shot (`sl03/hair/S1*.json`).
- Queue: SL-03 is `in_progress` (Claude). Extreme has about 116 GB free.

## Work

1. Record Dan's answers verbatim in `sl03/round2-plan/decisions.json` (id, sha256 of the still, verdict, his words, scope).
   Whatever he approves for the title band, bar and phone layout is the lock for every later Soft Blue shorts batch:
   write it into `GRAPHICS-STANDARDS.md` / the `/shorts` skill and do not ask again.
2. Shot plans for shorts 2 to 6 (same method: `hair/measure.py` per piece, windows from row 0, a real size step at
   every same-framing join, face bottom under every bar). Shorts 1 to 4 open on the finished salad (C1550 raw about 116.3).
   App shorts: per-piece Dan window (he moves; long-form cx ranged 824 to 1412), the phone never shrinks.
3. Key points for shorts 2 to 6: distilled, two lines, landing on words. Claude checks and locks them; show Dan only
   what is materially uncertain (decision budget: aim for 10 or fewer this round).
4. Moving previews: short 1's first 30 s finished (title, bar entrance, cutaway, captions, audio) plus one app-layout
   clip, on a small page. Then stop for Dan, or go straight on if he waives it in his answers.
5. The batch: renderer in `shorts/reference/softblue-sl03/` (HyperFrames overlays via `composite.Compositor(manifest,
   wh=(1080, 1920))`, captions from word times with CTC re-timing), `piccuts`/`junk` passes, audio cut only with
   15 ms de-click fades and `audio_gate.py --reference-mix <same cut of MASTER> --verbatim`, the delivery gate
   (`--format short`), watch pass, fresh-reviewer audit, review copies, `sl03-SHORTS.md`, `queue.py set SL-03 delivered`
   and the Edit Queue page.
6. No covers, no upload, no queueing. Nothing posts before RO-05 is public on Oct 18. Post shorts 5 and 6 far apart.

## Traps

- At most two builds at once; other sessions render on this machine.
- The long-form's music bed is in the mix: cuts land in voice pauses but the bed jumps at a join. Dip each internal
  join (15 ms) and listen; if a join is audible, move it to a quieter bar of the bed, never reprocess.
- `hfbuild.snapshot` leaves `._` twins on the exFAT drive; unlink inside try/except.
- zsh does not word-split unquoted variables in `for` loops; drive ffmpeg batches from Python.

## Starter prompt

> Name this task `Daily Salad SFC R2`. Read `Handoffs/handoff-20261002-sl03-salad-shorts-round2.md` and the files it
> lists. My answers to the round 1 page (http://127.0.0.1:8809/) are: [paste the reply box]. Record them, lock the
> Soft Blue shorts look into the standards, plan shorts 2 to 6, show me short 1's first 30 seconds moving plus one
> app-layout clip, then cut the six shorts with gates, a watch pass and an independent audit, and send me the review
> copies. No covers, no upload.

Model and effort: Claude Opus 5.5, high.
