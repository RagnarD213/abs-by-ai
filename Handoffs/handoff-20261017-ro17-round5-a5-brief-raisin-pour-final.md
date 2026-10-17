# RO-17 "3 Healthy Foods That Made Me Fat": round 5, the brief raisin pour, then final

**LFC (long-form content, 16:9).** Sidebar name: `3 Healthy Foods LFC R5`.
Written 2026-10-17 by Claude (Opus 5.5) at the end of round 4. Recommended: **Claude Opus 5.5, high effort.**

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md` (top sections), `.claude/skills/longform-edit/SKILL.md`
(edit sheet, delivery gate, watch pass, Step 8.6) and `.claude/skills/longform-edit/reference/ro17/README.md` (lessons 1 to 25, round 4 at the end).

## Dan's decision (2026-10-17, his words)

*"Okay, final revision. Everything looks good except the grapes versus raisins clip. I want to make this extremely brief, just around 2:58 to 2:59: a
very brief clip of the raisins going into the hand. Make it very brief so that it looks natural. The longer clip looks weird because the hand is frozen
in place. Shorten that, and that's our final edit."*

So: everything else in the round 4 film is approved as delivered. The only change is A5 (Grapes vs raisins). When it passes, the film is FINAL.

## The one change

- Today A5 runs 2:57.48 to 3:00.88 (3.40 s) from `round3/motion/final/A5.mp4` (take A5_t3 frames 18 to 120, Kling, 24 fps, gate + reviewer PASS on
  that range). Dan sees the hand holding still. Make it about 1 s (no more than about 1.3 s) of only the raisins dropping into the palm, placed at
  about 2:58 to 2:59 in the film, then back on Dan.
- Words there (film time): "and 177.48, all 177.82, the 178.04, water 178.24, in 178.50, it 178.62, fills 178.76, you 178.94, up. 179.12 to 179.36,
  The 179.48, raisins 179.82, fit 180.26 ... hand. 181.52". Dan named 2:58 to 2:59, so the pour sits on "water in it fills you up". Keep his timing.
- Find the frames in `A5.mp4` where the raisins are actually falling from the cup into the hand (measure the frame-to-frame change and look
  at the frames) and use only those. A clip source takes a start offset in seconds: `src=[f"{_MF}/A5.mp4@<offset>"]` (`gfx.src_start`), and
  `max_len` caps the slot. In `recipe/plan.py`, the round 4 override block at the end sets `A5` `max_len = 3.40` and chip `((54, 54), "lt")`; change the
  A5 item's `start` phrase (resolve.py anchors it on a word), `src` offset and `max_len` there. Keep the top-left chip. Never hold or slow a clip; a
  slight speed-up is allowed if it reads more natural (VIDEO-RULES, playback-speed rule).
- Watch the resolve rule that slides a length-capped clip to the next framing cut within 0.5 s (`resolve.py`, "no presenter island < 0.5 s"):
  check the resolved A5 t0/t1 land where Dan asked, and that there is no presenter island under 0.5 s either side.
- The sub-range is inside the reviewed range 18 to 120, so no new motion gate is needed, but the fresh reviewer must judge the new cut (three questions,
  no frozen hand, the cut in and out of it).

## Where things are

- Work dir `/Volumes/Extreme/_edit_work/RO-17/round3/` (recipe `recipe/`, plan, words, shots, hf link to round 2). `final/` is a LINK to the internal disk
  `tmp/ro17_r4/` (the Extreme SSD hit 0 bytes free on 10-15; it had 42 GB on 10-17). Render with
  `RO17_BASE="$PWD/final/tmp_base.mp4" python3 -u recipe/build.py range 0 452.15 final/RO17_MASTER.mp4` behind `buildcap.wait`, then
  `recipe/finish_chain.sh` (absolute paths; it skips the audio gate and transcript when their files exist: delete `RO17_MASTER.mp4.*`, `final.whisper.json`,
  `base.mp4`, `watch`, `checks`, `plan.json`, `negative_events_scan.json` first, as round 4 did between renders).
- Then, as in round 4: your own negative-events scan (48 frames, `negative_events_scan.json` with the new sha256), `recipe/finish.py` again so plan.json carries
  it, the edit sheet (`sheet_from_claude_build.py ... --facts tmp/ro17_r4/facts.json --type LFC`) and `validate.py --hash`, a fresh watch judge
  (`watch/JUDGE_PROMPT.md`), `watch.py --judge`, the delivery gate `--format longform`, and a fresh `ra-reviewer` on the new file (verify only A5 changed
  by a frame diff against the round 4 master, then the usual items). Fix and re-render until it ships.
- Round 4 master (keep as the reference for the diff): `claude edited long form content/17 - 3 Healthy Foods That Made Me Fat/3 Healthy Foods That Made Me Fat | claude round 4 | 16x9 | RO-17.mp4`
  (sha256 f9e49903...). It is hard-linked as `tmp/ro17_r4/RO17_MASTER.mp4`, so DO NOT overwrite that path in place: move the round 4 link aside first
  (`mv tmp/ro17_r4/RO17_MASTER.mp4 tmp/ro17_r4/round4_master.mp4`), or the delivery folder copy changes too.
- Round 4 gate: 34 pass, 5 known-mismatch fails (tone from the bass lift, burned-caption false positive, SRT cues over cards, one zoom size on the main
  framing as approved, a drawn-out "and" at 0:59 in the approved first minute). Notes: delivery folder `notes-RO17-round4.md`. Same five are expected.
- Review page port 8880 (`tmp/ro17_r4/review_page`, builder `recipe/page_film_r4.py`, data `page_r4.json`). Update it for round 5 (one change, at its
  new time, "What I decided"), refresh with `review_server.py 8880 <dir>`, test seeking muted.

## Deliver as FINAL

Dan called this the final edit. After the reviewer says SHIP: file round 5 in the same delivery folder (`... | claude round 5 | 16x9 | RO-17.mp4` plus
srt, chapters, stamps, edit sheet, REVIEW 540p, notes, recipe), replace `Videos to Review/3 Healthy Foods LFC R4 - full film.mp4` with
`3 Healthy Foods LFC R5 - full film.mp4`, and send Dan the one timestamp with a watch range. His approval in this message covers everything except A5, so
once he confirms the A5 fix (or if his reply already says final): `queue.py set RO-17 finalized`, mirror to the Edit Queue page, delete the RO-17 board
entry, delete its `Videos to Review/` copies, `review_server.py 8880 --remove`, and write the setup handoff (`/video-setup`, five thumbnail choices,
"Use the Codex subscription to generate the images.") into the OPEN list of `Handoffs/README.md`. Copy recipe changes to
`.claude/skills/longform-edit/reference/ro17/round3/` and `safe-push.sh` them.

## Starter prompt

> CONTENT (LFC). Name this task `3 Healthy Foods LFC R5`. Read and execute
> `Handoffs/handoff-20261017-ro17-round5-a5-brief-raisin-pour-final.md`. Everything in round 4 is approved except the grapes vs raisins clip: make it a
> very brief clip of just the raisins going into the hand at about 2:58 to 2:59, then back on me. Re-render, every gate, independent review, and send me
> the final with the timestamp.
