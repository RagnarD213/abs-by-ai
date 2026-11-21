# SL-03 Daily Salad shorts: round 2 (the look is approved; cut the six shorts)

**Written 2026-10-02 by Claude (Opus 5.5). Task name: `Daily Salad SFC R2`. Recommended: Claude Opus 5.5, high.**
Ready to fire: Dan approved the whole round 1 page on 2026-10-02.

## Dan's verdict on round 1 (2026-10-02)

*"Everything is approved. Excellent job getting everything ready for this review with no further revisions needed."*
Recorded with file hashes in `/Volumes/Extreme/_edit_work/sl03/round2-plan/decisions.json`. Nothing below is asked again:

1. **Title band:** Soft Blue Light band, y 0 to 310, cyan topic line + white two-line headline, on screen the whole short, picture under it.
2. **Title copy, all six:** 1 INTERMITTENT FASTING / BREAK YOUR FAST WITH THIS. 2 MEAL PREP / THE $20 SALAD YOU CAN MAKE FOR $4.
   3 MEAL PREP / KEEP YOUR SALADS FRESH FOR 7 DAYS. 4 DAILY SALAD / STOP BUYING SALAD DRESSING.
   5 AI MACRO TRACKING / TRACK A WEEK OF MEALS FROM 1 PHOTO. 6 AI CALORIE TRACKING / THE ONE LINE THAT MAKES IT ACCURATE.
3. **Key-point bar:** the HyperFrames lower third, box 68,1130 to 1012,1378, two lines, lines landing on words, under his face, captions from y1412.
4. **Short 1 key points:** G1 `Break Your Fast With CARBS / And Fasting Barely Works`; G2 `A LOW-CARB First Meal / Means Far More FAT LOSS`.
5. **Salad shots fill the frame** (not the centre square).
6. **App shorts: phone beside Dan** (shell 1.2x, Dan 440 x 1190, captions on the field under both). The stacked layout is dropped.
7. **Hair at the top edge:** accepted as camera framing.
8. **Small AbsByAI.com in the corner:** kept.
9. Everything under "What I decided" stands: the trimmed openings and endings, the lengths, two steady crop levels, the
   following window on short 1's last line.

Round 1 page (record only): `http://127.0.0.1:8809/`, files in `/Volumes/Extreme/_edit_work/sl03/round1/`. Spend $0.

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
- Short 1 plan: `sl03/round1/shots_S1.json` (windows, face ranges, graphics with word times; its opener and cutaway are the fill option). Layout: title band
  y 0 to 310, picture 1080x1610 under it; full window 724x1080, closer 604x900, both from source row 0; bar box
  68,1130 to 1012,1378 (two lines only); captions from y1412.
- Hair: the camera framed his hair at source row 0 in every short 1 shot (`sl03/hair/S1*.json`).
- Queue: SL-03 is `in_progress` (Claude). Extreme has about 116 GB free.

## Work

1. Re-hash the approved stills against `round2-plan/decisions.json` before touching anything. Write the approved band,
   bar position and phone layout into `GRAPHICS-STANDARDS.md` and the `/shorts` skill as the Soft Blue shorts standard
   (Dan, 2026-10-02), so later batches reuse it without a look round.
2. Ear-check the three open cut points, then run boundscan on all six.
3. Shot plans for shorts 2 to 6 (same method: `hair/measure.py` per piece, windows from row 0, a real size step at
   every same-framing join, face bottom under every bar). Shorts 1 to 4 open on the finished salad, filling the frame
   (C1550 raw about 116.3). App shorts: per-piece Dan window (he moves; long-form cx ranged 824 to 1412), the phone never shrinks.
4. Key points for shorts 2 to 6: distilled, two lines, landing on words. Claude checks and locks each one as a still
   and moving, inside the approved look. Bring Dan a question only if something is materially uncertain.
5. Build short 1 complete first and check it moving (bar entrance, cutaway, captions, the following window, audio
   joins) before cutting the other five. This is an internal check, not a stop for Dan.
6. The batch: renderer in `shorts/reference/softblue-sl03/` (HyperFrames overlays via `composite.Compositor(manifest,
   wh=(1080, 1920))`, captions from word times with CTC re-timing), `piccuts`/`junk` passes, audio cut only with
   15 ms de-click fades and `audio_gate.py --reference-mix <same cut of MASTER> --verbatim`, the delivery gate
   (`--format short`), watch pass, fresh-reviewer audit, review copies, `sl03-SHORTS.md`, `queue.py set SL-03 delivered`
   and the Edit Queue page. Deliver all six on one review page with a "What I decided" list.
7. No covers, no upload, no queueing. Nothing posts before RO-05 is public on Oct 18. Post shorts 5 and 6 far apart.

## Traps

- At most two builds at once; other sessions render on this machine.
- The long-form's music bed is in the mix: cuts land in voice pauses but the bed jumps at a join. Dip each internal
  join (15 ms) and listen; if a join is audible, move it to a quieter bar of the bed, never reprocess.
- `hfbuild.snapshot` leaves `._` twins on the exFAT drive; unlink inside try/except.
- zsh does not word-split unquoted variables in `for` loops; drive ffmpeg batches from Python.

## Starter prompt

> Name this task `Daily Salad SFC R2`. Read `Handoffs/handoff-20261002-sl03-salad-shorts-round2.md` and the files it
> lists. I approved everything on the round 1 page, so nothing there is asked again. Lock the Soft Blue shorts look
> into the standards, plan shorts 2 to 6, then cut all six shorts with gates, a watch pass and an independent audit,
> and send me the review copies on one page. No covers, no upload.

Model and effort: Claude Opus 5.5, high.
