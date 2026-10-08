# Handoff: RO-11 round 2, build the full film (the opener is locked; nothing is pending) (2026-10-08)

**CONTENT, long-form (LFC).** Task name: `Calories Don't Matter LFC R2`. Recommended: Claude Opus 5.5, effort high.
A long-form content video gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version here.
This replaces `handoff-20261004-ro11-round2-build-full-film.md` (deleted; in git history).

**Goal.** Build, gate, review and deliver the full RO-11 film, "When Calories Don't Matter For Fat Loss" (9/23 roll
C1705, 9:58). No creative decision and no generation is pending. Do not generate anything.

**Dan's words.** Round 1 (2026-10-04): *"Other than that, everything looks good."* Opener frames: *"All right, that looks
good."* Opener motion (2026-10-08): *"let's go with your recommendation for the [you] first, then the clean clip. I'm
choosing that, though, because I think it flows better that way than putting the full clip. I think the clip was actually
acceptable. Those small faults that you notice, I don't think they would be noticed by humans."* Record with hashes:
`/Volumes/Extreme/_edit_work/ro11/round2-plan/decisions.json` (13 entries; `PLAN-R2` and `A01-MOTION` are the new ones).

**Read first.** `_shared/VIDEO-RULES.md` (new on 10-08: review copies go in `Videos to Review/`; AI clip faults are judged
at playback speed), `_shared/PRE-RENDER-APPROVAL.md`, `_shared/CUT-CONTINUITY-QC.md`, `_shared/hyperframes/README.md`,
`.claude/skills/longform-edit/reference/ro11/README.md`, then `../ro10/README.md` (RO-10's full-film round is the model;
its work dir is `/Volumes/Extreme/_edit_work/ro10/round2/`, its delivery notes
`claude edited long form content/10 - Calories The Reason You're Not Losing Weight/notes-RO10.md`).

**Locked (do not change). Re-hash before building.**
- `plan_resolved.json` sha256 `4674e724...6b0d35` (round 1's plan with one change, A01). `hf/manifest.json` `05dd6fec...982692`.
  `edl.json` `30470add...2c6eb6`. `aiframes/C_motion_v2.mp4` `3b48ec73...06f69b`.
- Cut, takes, shots: `edl.json`, `shots.json` (17 pieces, 53 shots, 17,928 frames = 598.2 s), words `words_out.json`.
- Look and audio: colour C, W2/T2, framing solved by `recipe/build.py all_segments()` (57 segments, 0 jumps); audio = the
  fit in `FIT.mp4.voice_chain.json` + 0.9 dB at 150 Hz.
- All 21 HyperFrames graphics (`hf/manifest.json`, `hf/BEATS.md`), the 7 section titles, recap G21, clips C01 to C12.
- **The opener (A01), as Dan chose it:** the film opens on Dan for "You can still gain fat,". The AI clip
  (`aiframes/C_motion_v2.mp4@3.29`: the man lowers his fork to the tiny plate and looks up at the camera) plays from
  1.82 s to 4.50 s under "even if you're not eating too many calories", with the AI-GENERATED chip top right. Dan is back
  at "I'll show you how to prevent this". Approved preview: `round2/opener-preview/B_dan-first_then-clip.mp4`.

**Already done in the 10-08 session (do not redo).**
- `recipe/plan.py` A01 edited; `resolve.py` run; only A01 differs from round 1 (`round2/plan_resolved.before-opener.json`).
- `from_plan.py` without `--render` reports 21 graphics and leaves the manifest hash unchanged.
- `build.py` has RO-10's repeated-first-frame fix. All 57 presenter segments are in `cache/`; `dupscan.py` lists 0.
- `clipscan.py`: all 14 cutaway sources long enough, no dark edges, no internal cut (`round2/logs/clipscan.json`).
- `junk_report.json` (pre-render, from `ranges.json`). `recipe/finish.py`, `finish_chain.sh`, `deliver.sh` are written for
  RO-11 but have never run: read their first output carefully.

**Next action (in order).**
1. Rename the task. `queue.py set RO-11 in_progress --by Claude`, mirror it, board entry to IN PROGRESS. Re-hash the locks.
2. `cd /Volumes/Extreme/_edit_work/ro11`. Check `ps` for the two-build cap, then
   `python3 -c "import sys; sys.path.insert(0,'recipe'); sys.argv=['x']; import build; build.render_range(0, 598.20, '/Volumes/Extreme/_edit_work/ro11/round2/RO11_MASTER.mp4')"`
   in the background (RO-10 took about an hour).
3. `recipe/finish_chain.sh`: audio gate, transcript of the delivered audio, `finish.py` (SRT, chapters = intro, 7 factors,
   recap, gate plan), watch pass, dense hair check, HyperFrames `checks.py`. Known and approved: **G20 reads -211 px at
   555.25 s because both hands swing wide UNDER the card; Dan saw the flag and approved it, so leave it and say so.**
4. Proofread the SRT against the delivered audio (`round2/srt_fixes.json`, same shape as RO-10's). Settle any doubled word
   Whisper reports by re-transcribing 5 s alone before calling it junk.
5. Jump-cut and junk pass on the exact file. **New footage to look at:** Dan's first 1.82 s and 4.50 to 4.56 s were under a
   placeholder in round 1 and were first seen in the 10-08 preview (clean on stills: speaking to camera from frame 0, hair in frame).
6. Negative-events scan of the watch sheets into `round2/negative_events_scan.json` (RO-10's file is the shape). The AI
   clip is a clothed man at a table, stomach hidden: frames approved by Dan 10-04, motion 10-08.
7. `_shared/deliver/gate.py RO11_MASTER.mp4 --format longform --plan plan.json` in the background (about 35 minutes; do not
   restart the session under it). Report every row honestly. Rows that failed on RO-10 for known reasons:
   `captions:burned`, `captions:card_collision`, `framing:push_coverage`, `cut:splice_visibility` at side-card cuts.
8. One independent `ra-reviewer` on the exact file (it must not read the notes). Fix what it finds, 3-round cap, then
   `watch.py --judge`.
9. `recipe/deliver.sh` to `claude edited long form content/11 - When Calories Don't Matter For Fat Loss/` (master, SRT,
   chapters, REVIEW 540p, audio A/B, stamps, notes `round2/notes-RO11.md`, recipe). Copy the master to
   `Videos to Review/Calories Don't Matter LFC R2 - full film.mp4`, delete the four `... - opener ...` clips there, open the
   folder. Upload the 540p copy to Drive (anyone with the link) and send Dan the link and the file name.
   `queue.py set RO-11 delivered`, mirror it.
10. Notes for setup (in `notes-RO11.md`): one realistic AI clip, so YouTube's altered/synthetic flag is TRUE; links to the
    glycine video, the alcohol video and the first calories video (RO-10); study list in
    `Docs/SCRIPTS_CALORIES_PAIR_20260921.md` production notes. Ending is subscribe-only, no AbsByAI call to action.
11. After Dan approves the film: register the opener clip and the used stock in the clip library, delete the copies in
    `Videos to Review/`, delete this handoff's rows in `Handoffs/README.md` and the board.

**Not done yet (do not claim).** No full film, SRT, chapters, delivery gate, watch pass or independent review. The RGB
compositor proof was not re-run on this film (RO-10's used the same unchanged code).

**Spend.** About $3.50 of $5: Gemini listening $1.10, rejected A and B frames $0.60, motion take 1 $0.60 (not used),
motion take 2 $1.20 (used). Nothing more to buy. Tell Dan the take 1 line in the delivery note.

**Open risks.** `finish.py` builds the AI chip reference with `softblue.py` (right for A01, which is drawn by `gfx.ai_chip`);
if the labels row reads under 0.85, check the chip position before anything else. Push with `scripts/git/safe-push.sh`
naming only your own files.

**Starter prompt (Claude Opus 5.5, effort high):**

Name this task `Calories Don't Matter LFC R2`. This is CONTENT (long-form). Read and execute
`Handoffs/handoff-20261008-ro11-round2-build-full-film-opener-locked.md`. Everything in RO-11 is approved and locked,
including the opener (I open on camera, then the clean AI clip). Build the full film, run every gate and the independent
review, deliver it, put the master in Videos to Review and send me the review copy.
