# Handoff: Flow clips batch 4, motion reviews and video picks page (2026-11-15)

**For Codex (newest Sol, high) and Grokbot.** Dan's standing rule (2026-11-05): a step Claude cannot do goes to Codex and Grokbot. Claude's weekly
limit ran out mid-step (resets Nov 19, 10 AM Central). Dan has authorized this work end to end (parent handoff
`Handoffs/handoff-20261115-flow-credits-ai-clips-batch-4.md`); do every step without asking. No Flow credits are needed for this step.

## Execution status (Codex, 2026-11-15)
Steps 1, 2 and 4 are complete. **SUPERSEDED 2026-11-15 (Claude): Dan asked for one full-length clip per video; awaiting his answers at http://127.0.0.1:9261/ (see receipt, "one clip per video page"). File approved clips from `vid-b4/one_per_clip_manifest.json`.** Old page:9260, 40 checked cuts across 16 clips. Do not redo the reviews or regenerate sources. Three Cans' three original review files are unchanged. All54 verdicts are recorded:41 visual PASS windows,13 FAIL; one additional automatic-window exclusion. Treadmill Milkshake and The Rule Book have no offered take.

Fresh reviews inspected every native frame as still sequences and close-ups; continuous normal-speed perceptual review was unavailable and is disclosed on the page. Layout at375/800/1150, silent functional playback, seeking, saved selections/notes, exact hashes/frame counts and HTTP206 for all40 files passed. Owner page is paused and sound-ready.

Credits receipt and M2 master credit log record19,822 observed balance:490 measured credits from20,312 versus540expected; discrepancy50 unresolved. No new generation or spend in this task.

**Only step3 remains after his choices.** Save his exact selected take IDs, words and date as `{selected:[take IDs],approval_words:<his words>,date:<date>}` to `/Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/picks.json`. On M2 run `python3 /Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/file_library.py /Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/picks.json` (dry-run), then append `--execute`. Verify Drive/library/sheet; use `library_ids.json` and `job-doc-additions.json` to update the current job docs, then update the credits receipt. No repeat authorization. Full proof and details: `Docs/FLOW_CREDITS_CLIPS_RECEIPT_20261128.md`, final Batch4 section. Scripts/reports/manifest/QA evidence remain in `vid-b4/` on the shared Extreme.

## State
- Dan picked 18 frame pairs on 2026-11-15; video is generated: 54 takes (2 Veo 3.1 Fast 8 s + 1 Omni 1.1 Flash 6 s per clip) in
  `/Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b4/veo/` (same path on the M6 and the M2). `B4-11o-flow-t1.mp4` is a byte duplicate of `-t2` (skip it).
- Correction:45 full-take automatic PASS,9 FAIL; three exact windows recovered and one excluded. See execution status above. Original stamps `<take>.mp4.clipcheck.json`, evidence in `veo/clipcheck/`).
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
