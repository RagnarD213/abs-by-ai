# Handoff: Flow clips batch 4, motion reviews and video picks page (2026-11-15)

**For Codex (newest Sol, high) and Grokbot.** Dan's standing rule (2026-11-05): a step Claude cannot do goes to Codex and Grokbot. Claude's weekly
limit ran out mid-step (resets Nov 19, 10 AM Central). Dan has authorized this work end to end (parent handoff
`Handoffs/handoff-20261115-flow-credits-ai-clips-batch-4.md`); do every step without asking. No Flow credits are needed for this step.

## State
- Dan picked 18 frame pairs on 2026-11-15; video is generated: 54 takes (2 Veo 3.1 Fast 8 s + 1 Omni 1.1 Flash 6 s per clip) in
  `/Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/veo/` (same path on the M6 and the M2). `B4-11o-flow-t1.mp4` is a byte duplicate of `-t2` (skip it).
- Every take passed `clipcheck.py` (stamps `<take>.mp4.clipcheck.json`, evidence in `veo/clipcheck/`).
- Per-clip take lists, lines and aspect: `vid-b4/review_takes.json`; specs `vid-b4/specs/<id>.spec.json`; prompts `vid-b4/prompts/`.
- Reviewer instructions: `vid-b4/MOTION-REVIEWER-BRIEF.md` (per clip: judge each take, write `veo/clipcheck/<take>.motion-review.md` ending in
  `VERDICT: PASS|FAIL` with `WINDOW: A-B` frames on a PASS, record with `clipcheck.py <take> --review <md>` on the M2). No review files exist yet.
- Video page builder: `vid-b4/build_review.py` (shows only takes with clipcheck + reviewer PASS, verified on the M2, each cut to its WINDOW).

## Do
1. For each of the 18 clips in review_takes.json (B4-02 ... B4-22), review its takes exactly as MOTION-REVIEWER-BRIEF.md says and record each verdict.
   Use one fresh reviewer context per clip (a new `codex exec` per clip is fine). Judge frame by frame like a trainer and a realist (see the brief's
   batch notes: props keep their count, quoted text stays exact, the treadmill belt keeps moving, lips closed, no AI look).
2. `python3 /Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/build_review.py` on the M6, then publish the page:
   `python3 .claude/skills/_shared/review_server.py <free port from editroute.py free-port --from 9260> /Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/review`.
   Check it at 375, 800 and 1150 px (no sideways scroll, videos load), then give Dan the link to pick.
3. After Dan's picks: `clip_library.py add <window cut> --kind ai --status usable-unused --used-in "<job> <title> (planned)" --tags flow-credits-batch4`
   on the M2 (catalog lives there; copy `vid-b3d/file_library.py` from the M2's FLOWCLIPS folder as the model), `clip_library.py sheet`, and list
   the new IDs under "Pre-made AI clips" in each job doc (RO-39 ... RO-43, DS-106, DS-101; the existing-clip sections were added 2026-11-15).
4. Update `Docs/FLOW_CREDITS_CLIPS_RECEIPT_20261128.md` and the credit log `Media/flow-credit-log.md` (M2 master): read the Flow balance
   (avatar menu in the M2's Chrome, Flow) and record the batch 4 video spend (54 takes; balance was 20,312 before; 19,822 read while the second
   half was still finishing).

## Grokbot
These files live only on Dan's Macs; Grokbot cannot reach them, so Grokbot's part is none unless Dan gives it Mac access. If it has access, it follows the same steps.
