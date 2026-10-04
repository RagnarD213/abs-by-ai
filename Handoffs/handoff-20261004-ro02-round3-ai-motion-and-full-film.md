# Handoff: RO-02 round 3. Round 2 approved: generate the opener's AI motion and build the full film (2026-10-04)

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else: no vertical, no square, no 1-minute version.

**Goal.** Finish RO-02 "The Vacuum: The Best Ab Exercise For Belly Fat" (8/14 poolside rolls C1614 to C1629; job doc
`Handoffs/video-editing/RO-02-the-vacuum-explainer.md`). Round 2 put the opener frames, the opener graphic, every other
graphic and clip as a still, and the finished first minute in front of Dan. **Dan approved round 2 on 10-04** ("Okay,
everything is looking good. Give me the handoff document to build the next round."). Session name: `The Vacuum LFC R3`. This replaces
`handoff-20261004-ro02-round2-graphics-and-first-minute.md` (keep it for Dan's round 1 answers).

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/hyperframes/README.md`,
`.claude/skills/longform-edit/reference/ro02/README.md`, then `../ro10/README.md` (the full-film chain: `clipscan.py`,
`finish_chain.sh`, `finish.py`, `haircheck.py`, `dupscan.py`). Work dir: `/Volumes/Extreme/_edit_work/ro02/` (recipe that
ran: `recipe/`; skill copy: `reference/ro02/`).

## Dan's round 2 answer (2026-10-04; recorded with 42 file hashes in `round3-plan/decisions.json`)

His exact words: "Okay, everything is looking good. Give me the handoff document to build the next round." Read as:

1. First minute: approved.
2. Opener clip A (crunches) frames: approved. Motion authorized.
3. Opener clip B (sit-ups) frames: approved. Motion authorized.
4. The opener graphic: approved as built (ends at 0:06.56 on the cut to him at "stop doing all those ab exercises").
5. The anatomy card (AN1): approved.
6. Sound: approved.
7. Length: **he named no option.** Build the cut as shown, 11:49.9, nothing removed. Do not remove the aside (C1617
   18.24 to 24.94) or trim the three types piece unless he says so in the round 3 prompt. If he does, see step 1 below.

Everything listed under "What I decided" on the round 2 page stands (the three step lower thirds, the live-set clip at
0:26, the demo on its olive card, the countdown, the recap card). Re-hash the files in `decisions.json` before touching
anything. Round 2 page for reference: http://127.0.0.1:8826/ (`round2/`).

## State at handoff

- Locked from round 1: colour A; the cut (29 pieces, 66 shots, 11:49.9). Applied: half the headroom (`frames.py` `PAD`
  F 25 / N 20, bottoms held by `PAD0`; FAR about x1.50, NEAR about x1.86).
- Transcript re-run on 10-04 (`asr_assembled_medium.json`, `words_out.json`): current, read end to end, clean.
- Plan: `recipe/plan.py` -> `resolve.py` -> `plan_resolved.json` (29 items). HyperFrames renders in `hf/renders`
  (a symlink to `~/.cache/absbyai/ro02-hf-renders`: the Extreme drive ran out of room mid-render; exFAT stores every
  captured frame as a 1 MB file). 13 template graphics: 9 lower thirds, 1 fact card, 4 side lists (L1, L2, L3, L5).
- `build.py`: segments solved for the whole film (F/N alternate at every join, a left card slides his crop window left
  inside the 1080p frame via `frames.crop(card=True)`); zero same-size joins. `gfx.py`: the opener, section titles
  (PART n OF 6), recap card, anatomy card, countdown, URL chip.
- Opener frames: `aiframes/A-start.png`, `A-end.png`, `B-start.png`, `B-end.png` (Codex subscription, prompts in
  `aiframes/prompts/`). B-start has a small N on the shoe: paint it out before generating motion.
- First minute: `round2/first-minute/DRAFT - RO-02 round 2 - first minute.mp4`, audio gate PASS 13 of 13, hair 36 px
  minimum. The opener in it is the labelled placeholder (`build.opener_frames`).
- Spend: $0 of $5.

## Round 3 work, in order

1. Length only if Dan asks for it in the prompt. If he changes length, edit `recipe/edl.py`, then re-run `shots.py`, `assemble_audio.py`,
   `asr_assembled.py`, `words_out.py`, `resolve.py`, and re-check every phrase. Length (b) removes the aside from the
   first minute, so every time after 0:49 moves 6.7 seconds earlier.
2. AI motion for the approved frames only (VIDEO-RULES: $5 per video; Kling or Veo on the API, not Codex). Each clip:
   START to END, one simple body action. The graphic needs about 6.6 s per panel: play START to END forward, then the
   same clip reversed, so he does a rep or two. Check every frame for hands and morphing limbs. Put the finished clips
   at `aiframes/A.mp4` and `B.mp4` and change `build.opener_frames` to read their frames (850 x 478 per panel). Show
   Dan the finished opener moving if anything about the motion is uncertain.
3. Full film: `dupscan.py` on the cache, `build.render_range(0, total)`, then the RO-10 finish chain (audio gate,
   finished transcript, SRT and chapters, watch pass, hair check on the whole film, hyperframes `checks.py`), one
   independent reviewer (`ra-reviewer`), the delivery gate (`--format longform`; the drug-name rows are the known
   organic mismatch). Look at all 65 joins, not only the first minute's.
4. Deliver to `claude edited long form content/`, register the new AI clips in the clip library, run
   `roll_sidecar.py mark-used`, check the dashboard row off, hand off to `/video-setup`.

## Traps this round paid for

- **The library's vacuum clip (B0428) is in shade and reads dark and small beside this film.** The 0:26 beat uses four
  seconds of this film's own live set (`assets/vacuum_teaser.mp4`, C1625 from 41.0 s, graded and framed like the set).
- **A side list over the step-by-step demo fails:** his elbows cross 144 px into the card on `steps.0r1`. The steps are
  three lower thirds (G07 to G09). The Routine list ends on the cut at 9:39.35 (he was 12 px inside the card past it).
- **A two-part lower third lost the space between its parts** when part 2 began with a capital T ("BREATHSThrough").
  G06 is one part. Look at every multi-part lower third's still.
- `checks.py` flags the side cards' fill as 10,38,73 (one level off in blue). Looked at; not visible; recorded in
  `round2/flag_notes.json`.
- Two-build cap: other sessions held four to five builds all morning and the wait never cleared. The transcript and
  the renders ran at `nice` with the cap exceeded; say so to Dan if it happens again.
- Disk: Extreme had under 5 GB free, the internal disk 13 GB. Delete `round2/context/*.work` style intermediates as you
  go, and expect the full render to need about 6 GB.

## Not done (do not claim)

No AI motion, no full film, no SRT or chapters, no delivery gate, no watch pass, no independent review. Only the first
minute's eight picture changes have been looked at frame by frame. Nothing registered in the clip library.
`roll_sidecar.py mark-used` not run. The queue file `Handoffs/video-editing/jobs.json` was not updated this round (it
carries another session's uncommitted edits).

## Git state

See the board entry. Round 1's commit `73c7464` and this round's commit are local unless `safe-push.sh` got through.

## Starter prompt (Claude Opus 5.5, effort high)

Read `Handoffs/handoff-20261004-ro02-round3-ai-motion-and-full-film.md`. Name this session "The Vacuum LFC R3". This is
a CONTENT long-form. I approved round 2. Build RO-02 round 3: generate the AI motion for the two approved opener clips
(crunches and sit-ups), put it in the opener graphic, build the full film at its current length, run every gate and one
independent review, and deliver. Stop and show me the finished opener moving if anything about the motion is uncertain.
