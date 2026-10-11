# RO-07 "Why You MUST Work Out Every Day": the full film is with Dan (round 3 delivered 2026-10-10)

**CONTENT, long-form (LFC). Task name for the next round: `Work Out Every Day LFC R4`** (or `Work Out Every Day LFC Setup` if he
finalizes). Skill: `/longform-edit`. This replaces `handoff-20261010-ro07-round3-full-film.md` (executed the same day).

## Where it stands

The finished film (18:06.75, 32,570 frames) is delivered and waiting for Dan's review. Nothing is pending in the build.

- Review page: http://localhost:8860/ (folder `/Volumes/Extreme/_edit_work/ro07/round3/`, `index.html`).
- VLC copy: `Videos to Review/Work Out Every Day LFC R3 - full film.mp4`.
- Delivery folder: `claude edited long form content/14 - Why You MUST Work Out Every Day/`
  (`Why You MUST Work Out Every Day | claude round 3 | 16x9 | RO-07.mp4`, `.srt`, `.chapters.txt`, edit sheet, stamps, both reviews, recipe).
- Master sha256 `cc3456461691c9b073b72b4ba34cefdef3e0c12d5f1286c30b94040aa3126615`.
- Edit queue: `delivered`.

## What round 3 built (do not apply twice)

1. Opener handstand piece (film 0:02.07 to 0:04.14): re-cut from roll C1684 at 15.95 s, 1.2x, `broll/handstand_reps.mp4`.
2. C31 (2:24.31 to 2:27.61): library A0019 from 2.92 s. That clip is a frozen frame from 6.25 s; never use past it.
3. A3 (4:57.10 to 5:00.53): `round3/motion/A3-t1.mp4` from 0 s, 3.4 s of the 6 s take (the last 2 s hang at the end frame). $0.60.
4. Defaults for his three blanks: 18:07 kept, Gymboss as lower thirds G36 and G37, quiet bed at -30 dB (`round3/bed/bed.wav`).
5. Found by the independent review and fixed: C37 (10:08 to 10:15) cropped to remove a crew member and a reflector; three mouth
   clicks turned down (11:01.66, 11:18.07, 13:58.60; `build.DUCK`); subtitles and chapters corrected against the finished sound.
6. Every shot is pinned to the round 2 framing (`build._R2`, `round3-plan/segs.round2.json`).

## Open with Dan

- **His verdict on the film** and on the three changes (0:02, 2:24, 4:57).
- **Hair at the top edge needs his word.** The camera framed his hair at the top row; about 2.5 % of presenter frames touch the edge
  (longest: 10:25, 11:18, 12:26, 13:19, 15:09, 16:42, 16:46, 17:57). Options given: leave as shot, or extend the wall above his
  head (one more round). The watch row of the delivery gate stays open on it until he says.
- The three defaults (length, Gymboss, music) and the two unasked fixes (the C37 crop, the clicks) are his to overrule.

## Gates on the delivered file, stated honestly

Audio gate 12 of 13: tone fails (voice 4, his pick; no limit changed). Delivery gate FAIL on: `audio:stamp` (that tone row),
`style:coverage` 27 % (floor 40; RO-06 was approved at 34), `framing:hair_top` and `framing:headroom` (camera framing),
`cut:splice_visibility` (32 of 170; both reviewers found no jump cut), `captions:burned` and `captions:card_collision` (false alarms:
lower thirds read as captions, sidecar cues during the full-screen card), `junk:repeated_take` (false alarm: two different sentences),
`watch:pass` (29 hair entries open). Exact rows: `round3/logs/gate.log`. Review 1 (first render): DOES NOT SHIP, the C31 freeze.
Review 2 (this file): SHIP for picture and sound. Reviews: `round3/ROUND-3-REVIEW.md`, `ROUND-3-REVIEW-2.md`.

## Next action

- **If he has notes:** new round folder `round4/`, change only what he names, render, re-run the chain (`finish_chain_r3.sh` pattern),
  carry verdicts with `carry_r3.py` against this file, fresh judge on changed images, gate, page on a new port, replace the VLC copy.
- **If he picks the 16:50 length:** apply the five trims listed on the round 2 page in `edl.py`, regenerate time maps, graphics timing
  and the first minute, and show him the first minute before the full film.
- **If he finalizes:** delete this video's copies from `Videos to Review/`; remove the review services on 8857, 8858, 8859 and 8860
  (`review_server.py PORT --remove`); add the corpus approval with his words; register the new clips in the clip library
  (`round3/motion/A3-t1.mp4` first 3.4 s, `round2/motion/A2-t1.mp4`, `broll/handstand_reps.mp4`, the three C1680 push-up cuts) and mark
  the library clips used; edit sheet `--approved "<his words>"`; queue `finalized`; then write the setup handoff (one Claude handoff:
  five thumbnails with the Codex subscription, stop for his pick, then `/video-setup`; Sunday queue rule).

## Cost ledger (cap $5 for this video, all rounds)

Replicate $1.40 ($0.80 A2, $0.60 A3). Gemini listens about 8 cents. Codex: 8 images on the subscription.

## Read first

`.claude/skills/longform-edit/reference/ro07/README.md` (round 3 section), `round3-plan/decisions.json`, the two review files.

## Model and effort

Opus 5.5, high.

## Starter prompt

> Work Out Every Day LFC R4. CONTENT, long-form. Read `Handoffs/handoff-20261010-ro07-round3-dan-review.md` and the files it lists, then continue RO-07 with /longform-edit. My verdict on the round 3 film: [finalize it / change these things: ...]. Hair at the top edge: [leave as shot / add headroom]. Length: [keep 18:07 / trim to about 16:50]. If I finalized it, do the finalize steps in the handoff and write the setup handoff. If I gave notes, change only what I named and give me the new film with the timestamps of each change.
