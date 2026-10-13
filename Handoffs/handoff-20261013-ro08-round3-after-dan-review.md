# RO-08 "Intermittent Fasting: The Best Way To Get Abs": round 3, after Dan's review of the full film (written 2026-10-13)

**CONTENT, long-form (LFC). Task name for the next session: `Intermittent Fasting LFC R3`.**
Job doc: `Handoffs/video-editing/RO-08-intermittent-fasting.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Skill: `/longform-edit`.
Recipe and traps: `.claude/skills/longform-edit/reference/ro08/README.md` (round 2 section).

## Where it stands

Round 2 is delivered and waits on Dan. The full film exists (14:41), every AI clip is moving, both openers are built.

- Review page: `http://127.0.0.1:8871/` (round 2). Round 1 page 8869 and the notes page 8870 are still up.
- Film: `/Volumes/Extreme/_edit_work/ro08/round2/RO-08 round 2 - full film.mp4`, sha256 `75d08be47b45b3a7...` (all hashes of
  what Dan was shown: `round3-plan/round2-hashes.sha256`). The framing solve of this film: `round3-plan/segs.round2.json`.
- Delivery folder: `claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs/` (master, SRT,
  chapters, edit sheet, both reviews, recipe). VLC copies: three files in `Videos to Review/` named `Intermittent Fasting LFC R2 - ...`.
- The first render and its reviewed images are kept in `round2/render1/` for carrying verdicts (`recipe/carry_r2.py`).

## What Dan was asked (two decisions)

1. **Opener: A (time-lapse, in the film) or B (split screen).** Recommendation A. B is `round2/motion/O6-t2.mp4`; build it with
   `RO08_OPENER=O6 python3 recipe/resolve.py` (the plan reads the variable; its label sits bottom left). Only frames 0 to 230 change.
2. **Finalize, or notes with times.** The page asks him to look hardest at A2 (7:45 to 7:52): a new take with NO lip sync that he
   has not seen (his 2026-10-12 rule; the synced first take failed the independent check). It does not reach his approved end
   frame. If he wants another take: `NOLAST=1 PROMPT=A2b python3 recipe/gen_motion08.py A2 A2-t3` ($0.80).
   A1 (7:24) keeps its lip sync; its measured match is weak and the page says so. No-sync fallback for A1 would be one new take ($0.60).

Record his reply word for word in `round3-plan/decisions.json` before touching anything.

## If he finalizes with opener A (no change)

Mark the footage ranges used on the C1486 sidecar, register the new clips in the clip library (the eight AI clips and the
opener he picked, `--status used-final --used-in RO-08`; never the rejected takes O6-t1, A2-t1, A2-sync1), add the corpus
entry with his words, mark the edit sheet approved (`--approved "<his words>"`), set the queue to `finalized`, add the Shorts
job (List 2) to `00-MASTER.md`, delete the three VLC copies, and remove the review services on ports 8869, 8870 and 8871
(`review_server.py PORT --remove`). Then write the one Claude handoff for thumbnails and `/video-setup`.

## If he picks opener B or sends notes

Re-hash against `round3-plan/round2-hashes.sha256`. Point `build._PIN` at `round3-plan/segs.round2.json`. Make only the named
changes, render, run `finish_chain_r2.sh` (copy it to a round 3 name and folder), `carry_r2.py` against this film, one fresh
`ra-reviewer` on the changed images, the edit sheet, the delivery gate, a round 3 page on a new port with the changes and
their timestamps. Replace the VLC copies.

## Gate status on the delivered file, stated honestly

- Audio gate 12 of 13 (tone: voice 1a, his pick). Watch pass: 494 of 494 images judged, 0 open defects, 0 naked splices, 48 of 48 graphics.
- Independent reviews: the first render DOES NOT SHIP (five findings, all fixed); this file SHIPS (`ROUND-2-REVIEW-2.md`).
- Delivery gate 32 pass, 7 fail, 0 not measured: audio stamp (tone), cover 24 % against 40 %, hair top and headroom (camera
  framing, as shot), splice visibility 17 of 149 (no jump cut found by either reviewer), burned-captions false alarm (lower
  thirds), repeated-take false alarm (the two "If you wake up at..." examples at 10:51). No bound was changed.
- Open notes for Dan on the page: hair as shot; C35 (14:15) still a little darker and warmer than the presenter; A8 clears its
  junk in one sweep; A2's three small faults (towel at 7:46, face from 7:49, ends propped on his hands).

## Cost ledger (cap: $15 for this video, set by Dan on 2026-10-12)

- Replicate, AI motion and lip sync: **$10.57** (`round2/motion/ledger.json`): 13 first takes $8.00, second split screen take
  $0.80, second A2 take $0.80, lip sync $0.97. Room left: $4.43.
- Codex images on the subscription: 28 (unchanged). Gemini: nothing new this round.

## Starter prompt

Model: **Claude Opus 5.5, high effort** (finalization, or a small revision round).

> Intermittent Fasting LFC R3. CONTENT, long-form. Read `Handoffs/handoff-20261013-ro08-round3-after-dan-review.md` and
> `.claude/skills/longform-edit/reference/ro08/README.md`. My reply to the round 2 page (http://127.0.0.1:8871/) is:
> [paste the reply box]. Record it, then either finalize RO-08 or make the changes I named with /longform-edit, run the
> checks and one independent review on what changed, and send me the round 3 page with timestamps. Rename this task
> `Intermittent Fasting LFC R3`.
