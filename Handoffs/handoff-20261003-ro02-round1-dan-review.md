# Handoff: RO-02 round 1 (cut + look) is with Dan; round 2 is the graphics, the clips and the finished first minute (2026-10-03)

**Goal.** Finish RO-02 "The Vacuum: The Best Ab Exercise For Belly Fat" (8/14 poolside rolls C1614 to C1629, job doc
`Handoffs/video-editing/RO-02-the-vacuum-explainer.md`). Round 1 put the cut, the colour, the framing and the sound in
front of Dan. Round 2 records his reply, then builds every graphic and clip as stills and the finished first minute.
The full film is round 3, only when nothing is pending. Session name for round 2: `The Vacuum LFC R2`.

**Review page (round 1).** http://127.0.0.1:8822/ (launchctl `com.absbyai.ro02-round1-review`, serving
`/Users/Shared/absbyai-review/ro02-round1/` with `review_server.py`; source `/Volumes/Extreme/_edit_work/ro02/round1/index.html`).
Dan's 5 decisions: (1) colour A or B, (2) framing FAR x1.45 / NEAR x1.80 or wider, (3) sound, (4) the opening: (a) cold
open + his own crunches footage at 0:03, (b) open on his real vacuum, (c) AI opener (frames first), (5) length: (a) all
11:50, (b) remove the "skip ahead about 30 seconds" aside (C1617 18.24 to 24.94), (c) also end the three types piece
after "is the standing vacuum" (C1620 19.32). Record his words against the hashes in
`/Volumes/Extreme/_edit_work/ro02/round2-plan/decisions.json`.

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/hyperframes/README.md`,
`.claude/skills/longform-edit/reference/ro02/README.md`, then `../ro13/README.md`, `../ro11/README.md`, `../ro10/README.md`.

**State.**
- Cut: 29 pieces from 13 rolls, 66 shots, 11:49.9 (`edl.json`, `shots.json`; every take choice and why in
  `recipe/edl.py`). Re-listens at every splice: `logs/verify_asr.txt`. Six pauses tightened (`pauses_cut.json`).
- Words: `words_out.json` is from the medium.en pass BEFORE the last two cut changes (the ending's restart at C1629
  54.75 to 56.72 removed; "So," restored at C1622 84.88). **Re-run `asr_assembled.py` then `words_out.py` before any
  plan work**, and again after decision 5 changes the EDL.
- Look: `recipe/grade.py` bakes the approved poolside colour (Codex organic colour v1) into cubes; `frames.py` places
  FAR / NEAR per shot from `measure.json` and trims exposure per shot from `skin.json`. Colour A = C1630 calibration,
  strength 1.0; B = C1631, 0.8 (`RO02_LOOK=B`).
- First minute (0:00 to 1:01.7, cut + look, no graphics): `round1/first-minute/DRAFT - RO-02 round 1 - first minute.mp4`.
  Audio gate PASS 13 of 13, -14.2 LUFS; fitted EQ in `FIT.json` (reuse it with `--eq` on later builds of this film).
  Hair 70 px minimum, 106 median. Four joins looked at frame by frame: all size changes, no jump.
- Listen-only audio of the whole cut: `round1/cut/RO-02 full cut - listen only (rough mix).mp3` (EQ + loudnorm, not the chain).
- Spend: $0.

**Planned for round 2 (listed on the page; none built).** His own crunches / toe touches from the V4 or V5 1 Minute
Ab Workout exports (the only allowed source, VIDEO-RULES) at 0:03; his real vacuum (clip library B0419, or the 16:9
8/28 roll C1677) at 0:25; six section titles; an anatomy card (six pack muscle in front, transverse abdominis wrapped
behind; drawn, a NEW kind, so it needs its own still approval); fact card SPOT REDUCTION; five KEY POINT lower thirds;
five side lists; the approved self-generation demo (`Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/`)
at 5:50 and in the ending; a 20-second countdown over the live set (new kind); recap card; AbsByAI.com chip in the
ending (no end mark). Side lists over a standing, gesturing presenter on a 1080p source: there is no W4S slide here,
so check every list against every piece it spans (person mask) before proposing it; fall back to lower thirds.

**Not done (do not claim).** No graphics, no clips, no finished first minute, no full film, no SRT or chapters, no
delivery gate, no watch pass, no independent review. The junk and jump-cut pass covered take selection and the first
minute's four joins only; the other 61 joins are unseen. `roll_sidecar.py mark-used` not run (EDL not final).
Only the first 84 s of picture is rendered (`cache/`).

**Known, for round 2's judgement.** The hook (full sun) reads warmer than the cloudy sections after the trim. He says
"supine" for the hands-and-knees vacuum (keep the speech, never the graphic). "you want to pull your shirt out" is what
he says. The Extreme drive has about 50 GB free.

**Next action.** Record Dan's reply in `round2-plan/decisions.json`. Apply decision 5 in `recipe/edl.py`, re-run the
chain from `edl.py` through `words_out.py`. Copy `plan.py`, `resolve.py`, `gfx.py`, `stills.py`, `review_media.py` and
the plan loop of `build.py` from `../ro13/` into the ro02 recipe (keep ro02's `frames.py`, `edl.py`, `shots.py`,
multi-roll `render_seg`). Write the plan from the page's planned list, phrase-anchored. `from_plan.py` without
`--render` first, then render, stills, checks, the finished first minute, the page (RO-10 layout with the context
player). Stop for Dan. Queue state is `draft_review`.

**Starter prompt (Claude Opus 5.5, effort high):**

Read `Handoffs/handoff-20261003-ro02-round1-dan-review.md`. Name this session "The Vacuum LFC R2". Here is my reply to
the RO-02 round 1 page: <paste>. Record the decisions, apply them to the cut, then build round 2: every graphic and
clip as a still on its real frame, the finished first minute, and the review page. Stop for my review.
