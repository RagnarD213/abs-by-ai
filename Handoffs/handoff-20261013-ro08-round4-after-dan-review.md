# RO-08 "Intermittent Fasting: The Best Way To Get Abs": after Dan's review of the round 3 film (written 2026-10-13)

**CONTENT, long-form (LFC). Task name for the next session: `Intermittent Fasting LFC R4`.**
Job doc: `Handoffs/video-editing/RO-08-intermittent-fasting.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md` (top section, 2026-10-13), `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Skill: `/longform-edit`.
Recipe and traps: `.claude/skills/longform-edit/reference/ro08/README.md`, section "Round 3".

## Where it stands

The round 3 film is delivered and waits on Dan. Page: `http://127.0.0.1:8872/` (folder `/Volumes/Extreme/_edit_work/ro08/round3/`).
The film is NOT finalized.

- Film: `/Volumes/Extreme/_edit_work/ro08/round3/RO-08 round 3 - full film.mp4`, sha256 `976b9761bc1e8455...`, 14:41, 26,396 frames.
- Delivery folder: `claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs/` (files named `... claude round 3 ...`).
- VLC copy: `Videos to Review/Intermittent Fasting LFC R3 - full film.mp4`.
- Earlier renders of this round, kept only as the judged references the verdict carry reads: `round3/render1/` to `render4/`.
  Delete them when the film is finalized (about 5 GB).

## What round 3 did (times in the round 3 film)

Dan's three revisions:
1. 1:58 to 2:04: the office worker and sandwich AI clip is out. One framing change with it: 1:53.35 to 2:04.42 is the camera frame
   (`build.OVERRIDE`, shot `mine2.0r1`), so no shot holds over 22 s.
2. 6:07.71 to 6:11.67: the donut clip is a two-shot cut of the round 2 take (`a5_cut.py`): bite and full box at nine, hard cut, empty
   box at ten and he sinks onto the keyboard on "food coma". The clock is steadied in both shots and an orange smear in the box is
   painted out. No money spent.
3. 7:16 to 7:22: the stomach rumble AI clip is out.

Two changes Dan did not ask for, made because the three quality questions caught them, and put to him as decisions 1 and 2 at the top
of the page with the round 2 version of each beside it:
4. 12:11.09 to 12:14.93: the fridge raid ends 1.4 s earlier, on the frozen stare (`end_at=734.9347` in `plan.py`). The held leg is out.
5. 4:55.13 to 4:59.90: the cell cartoon ends on "for fuel", before the furnace flares and the junk clears by itself
   (`end_at=299.9005`). Dan is on camera for "renews your cells and makes you younger". A version with the sweep replaced by a hard cut
   to the clean cell (`a8_cut.py`) was built and the fourth reviewer stopped it: the take has no clean second shot.

Everything else is frame for frame the round 2 film: 789 of 26,396 frames differ, all inside those five spots. The sound is bit for bit
the round 2 sound; the subtitles and the 15 chapters are the round 2 files.

## What Dan was asked

1. Fridge raid at 12:11: keep the shorter clip, or put the ending back. Recommended: keep.
2. Cell cartoon at 4:55: keep the shorter clip, put the sweep back, or remake the ending for $0.80 (two short takes, one from each of
   his approved frames, joined by a cut; `NOLAST=1`, 4 s each; no prompt may ask for junk to clear). Recommended: keep the shorter clip.
3. Finalize: yes or notes with a time.
4. AI budget for long-form videos from now on: $15 per video or $15 per clip (he said "per clip" on 2026-10-13; recorded as per video
   until he confirms).

Record his reply word for word in `/Volumes/Extreme/_edit_work/ro08/round4-plan/decisions.json` before doing anything.

## If he puts an ending back

- Fridge raid: delete `end_at=734.9347` from A6 in `recipe/plan.py`.
- Cell cartoon, sweep back: delete `end_at=299.9005` from A8 in `recipe/plan.py`.
- Cell cartoon, remake: `gen_motion08.py` (A8 start frame alone: the crew loads and wheels the junk; A8 end frame alone: the clean cell, they
  tip the barrows in), run the self-change map on each take (`a5_cut.py` has it) and the three questions BEFORE building, pre-cut the two
  into one file (the `a8_cut.py` pattern, `subcuts=`), one fresh reviewer on the clip. If a take fails, one retake each, then leave the
  shorter clip. Ledger: `round2/motion/ledger.json`.
- Then `resolve.py` -> `build.py segs` (no jump, no hold over 22 s) -> `r3_render.py` into a new `round4/` folder -> the short finish chain
  (`r3_finish_chain_short.sh` pattern: the sound is unchanged) -> `r3_carry.py` pattern against the round 3 film -> one fresh `ra-reviewer`
  on the changed images -> edit sheet -> delivery gate. Compare every frame with the round 3 film and say which frames changed. Then
  finalize without another review round unless he asked to see it.
- Do not run a context clip while the full render is starting (they collide in the segment cache), and expect the external drive to
  drop a read when another session renders to it: the readers retry now, a failed step is run again before it is debugged.

## When Dan finalizes

Mark the footage ranges used on the C1486 sidecar, register the AI clips that are in the final film and the opener in the clip library
(`--status used-final --used-in RO-08`: the opener, the boxing glove is already there, the cell cartoon as it ends in the final film, the
donut two-shot cut, A1, A2, A6 as trimmed, A7; never A3, A4, the first A5, O6 or the rejected takes), add the approval to the corpus, mark the edit sheet
approved, set the queue to `finalized`, add the Shorts job (List 2) to `00-MASTER.md`, delete the VLC copy and `round3/render1..4/`,
and remove the review services on ports 8869, 8870, 8871 and 8872 (`review_server.py PORT --remove`). Then write the one Claude handoff
for thumbnails and `/video-setup` ("Use the Codex subscription to generate the images.").

## Gate status on the round 3 film, stated honestly

- Audio gate 12 of 13 (tone: voice 1a, his pick).
- Watch pass: every image judged, 0 open defects. The hair-at-the-top-edge entries the reviewers logged on the newly visible camera frames
  carry `accepted_by_dan` with his round 1 words ("Everything else is looking good.", answering the page's hair question).
- Delivery gate: 32 pass, 7 fail, the same seven rows as round 2: audio stamp (tone), cover 22 % against 40 %, hair top and headroom
  (camera framing, as shot), splice visibility 20 of 149, a burned-captions false alarm (lower thirds), a repeated-take false alarm
  (10:51). No bound was changed.
- Five independent reviews, one per render: `round3/ROUND-3-REVIEW-1.md` to `-5.md`.

## Cost ledger

- Replicate, AI motion and lip sync: **$10.57** of the **$15** Dan set for this video (`round2/motion/ledger.json`). Round 3 spent nothing.
- Codex images on the subscription: 28. Gemini: nothing since round 1.

## Starter prompt

Model: **Claude Opus 5.5, high effort.**

> Intermittent Fasting LFC R4. CONTENT, long-form. Read `Handoffs/handoff-20261013-ro08-round4-after-dan-review.md` and
> `.claude/skills/longform-edit/reference/ro08/README.md` (section "Round 3"), then act on my reply to the round 3 page
> (pasted below): record it word for word, put back either ending I asked for (or neither), re-run the checks if anything
> changed, and if I said finalize, close RO-08 out (clip library, corpus, edit sheet, queue, Shorts job, clean-up) and write
> the one Claude handoff for thumbnails and `/video-setup`. Rename this task `Intermittent Fasting LFC R4`.
>
> My reply: [paste the reply box from the page]
