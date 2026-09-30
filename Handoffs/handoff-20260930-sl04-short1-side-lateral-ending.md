# Handoff: SL-04 short 1, new side-lateral ending (2026-09-30)

## Goal
Re-cut the ending of SL-04 short 1, "Make Your Waist Look Smaller"
(`Short-form video content/arms-shoulders-short1_make-your-waist-look-smaller.mp4`, 57.2 s), per Dan's round-2 note,
then gate, get an independent review, and send Dan the new review copy. Everything else about the short stays exactly
as delivered on 2026-09-29.

Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`,
`.claude/skills/shorts/reference/zeeshan-master/README.md` (the pipeline and every trap it hit, including round 2).

## Dan's note (2026-09-30, verbatim)
> "For the first one, from 35 seconds to 57 seconds, I feel like it seems kind of incomplete at the end. It's not clear
> why I'm showing them the arm angle when I don't show the complete exercise. I want you to cut that part and then,
> instead, just tell them to do side laterals and show a few reps of the side laterals. Use that time at the end to tell
> them to use side laterals to build their shoulders. A very brief explanation of how to do it, and then show some reps
> of the side laterals for that first one. Everything else before 35 seconds is looking good on the first one."

He also said of short 2: *"I like how you showed brief demonstrations of the exercise at the end. I feel like that
really gets the point across better than the end of the first video."* Short 2's live-round cards are the model for the
reps.

## Decisions already made (do not reopen)
- **0:00-0:35 is locked**: picture, grade (per-shot `GRADE_SAT` in `render.js`), captions, title band. Zeeshan's audio
  stays untouched (cut only, `--verbatim` gate).
- **Hair at the top edge is accepted for this video.** Dan saw the camera-framing evidence
  (`Short-form video content/arms-shoulders REVIEW/R2_hair_camera-framing.jpg`) and finalized shorts 2-5 on 09-30. Keep
  the `framing:hair_top` declaration in `gate/A/declare.json`, reworded to "accepted by Dan 2026-09-30" (see
  `gate/C/declare.json` for the wording).
- **No source second may appear in two shorts** (assert in `segments.js`). Taken: A 27.6-59.8 and 213.15-238.1 (being
  cut back), C 208.9-211.37 and 264.22-292.62, F 546.0-550.0, K 179.7-208.18, H 125.2-176.76.
- No covers in this task (Codex does covers). No upload.

## What is in short 1 now (output time = 32.2 + source - 213.15 for piece 2)
- Piece 2 starts at output 32.2 on source 213.15: "(light) dumbbells. I'm doing 15 pounds, most of you guys should be
  doing 5 or 10 pounds for this." (words to 218.28; measured gap 218.34-218.94). Output 35 s falls inside that sentence.
- Then 218.99-238.1: "So, with the side laterals, I'll demonstrate without the weight first. I have my hands in this
  position... About that angle in your arms is what you want." (the arm-angle demo Dan wants gone). Shots A-s05 (full
  wide, 218.94) and A-s06 (card, 223.33).

## Recommended new ending (verify every source time on the picture before building)
1. **Keep through the weight line.** Piece 2 = 213.15 to ~218.6 (cut inside the 218.34-218.94 gap). "Most of you guys
   should be doing 5 or 10 pounds" is useful and ends a thought; Dan's "35 seconds" is approximate.
2. **Name the exercise:** keep "So, with the side laterals," (218.99-~220.4, check the gap after "laterals" before "I'll").
3. **Brief how-to, unused in any short:** source 239.76-~244.3, "if you guys look at my thumbs right now, I'm going to be
   like this at the top" (medium shot, arms demonstrating the top position, no weights; see `r2chk/src238.jpg`).
   ⚠ Zeeshan's whip transition runs about 243.9-244.5, over the word "top." Do not show it: end the picture before the
   blur, cover the tail with the first reps card, or hold the last clean frame for no more than 7 frames while silent.
   Measure the words' real onsets (Whisper runs early on his mix; `work/ctc_source.py`).
4. **Reps:** the live round, source 550.0 to ~558.5 (side laterals with his timer and "Side Lateral Raises" pill; music
   only, Zeeshan's track with sung vocals; tricep extensions start ~559). Show it as a card like short 2's live-round cards
   (`cardCrop [0, 0.85, 0, 1]`, `cardY 470`), with a J2 chip such as "SIDE LATERALS" or "5-10 LB, 30 SECONDS". Keep his
   timer and pill whole on every frame, including fades at the card edges. End on a clean rep, with the audio fading out.
- Target length about 48-52 s. If the "So, with the side laterals," + thumbs splice does not read as one thought, the
  fallback is: weight line, then the thumbs line from 238.14 ("So I have my angle and if you guys look at my thumbs..."),
  then reps. The fuller "two jugs of water" explanation is NOT in Zeeshan's master (he cut it); it exists only in the raw
  8/3 rolls (C1582-C1587) and would need a different audio treatment, so do not use it without asking Dan.

## Current state
- Build folder (Extreme SSD): `/Volumes/Extreme/_edit_work/sl04/build/`. Edit `segments.js` (piece list for A),
  `plan_shots.py` (A rows: replace the 218.94 full and 223.327 card rows; add the new rows with reasons), `overlays.json`
  (any J2 chip), then `./build.sh A`, `./deliver_all.sh A`.
- Plan options added in round 2 (see the zeeshan-master README): `cw`/`ch` custom windows, `slideFrom`/`slideDelay`/
  `slideFrames`, `xKeys`, card `slow`, piece `fadeOut`, per-shot `GRADE_SAT`. New rows for A need a `GRADE_SAT` entry
  (measure skin sat on the rendered file with `grade/skin.py`; target ~0.62 like the rest of the short).
- Round-2 delivered file sha is in `Short-form video content/arms-shoulders-short1_make-your-waist-look-smaller.mp4.deliver_gate.json`.
- Edit queue: SL-04 is `ready` with a note pointing here (shorts 2-5 finalized). Board: HANDOFFS line.

## Steps
1. Claim: `python3 scripts/edit-queue/queue.py set SL-04 in_progress --by Claude` + `ArtifactData` set
   (procedure: `.claude/skills/_shared/edit-queue/README.md`); one ACTIVE line on the board.
2. Verify the recommended source times on frames and audio; build the ending; self-check with person masks and full-rate
   frame grabs (no sliced pill or timer, no whip blur, no freeze while he talks).
3. `./build.sh A`, `./deliver_all.sh A`, update `gate/A/negative_events_scan.json` (inspect `gate/A/neg.jpg`),
   `make_plan.py A`, `watch.py`, a FRESH Opus 5.5 reviewer (judge + full-res audit), `gate.py --format short`. Expect at
   least one fix round; every re-render needs a new judge.
4. New 540p review copy in `Short-form video content/arms-shoulders REVIEW/`; `queue.py set SL-04 delivered`; commit
   scripts/docs only (never media; the shared checkout's `main` may be diverged: build the commit on `origin/main` with a
   temp index as in commit 4b6ed1b) and push.
5. Message Dan in plain words, numbered action items at the bottom, review copy sent last.

## Risks
- The splice between "So, with the side laterals," and the thumbs line crosses two camera setups (wide to medium); it
  must read as a clean cut, not a jump.
- The live round is music only: the switch from his voice to the music bed must not jump in level (verbatim gate bounds).
- Machine cap: two video builds at once across all sessions (`wait_and_build.sh` waits for a slot).

## Starter prompt
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20260930-sl04-short1-side-lateral-ending.md`: re-cut the ending of SL-04 short 1 so it tells viewers to do side laterals, gives the brief thumbs-at-the-top cue and shows a few reps, keep everything before 0:35 as is, gate it, get a fresh independent review, and send me the new review copy.

**Model: Claude Opus 5.5, high effort** (a bounded re-cut, but it crosses a camera change, a whip transition and a
music-only card, and round 2 needed three reviewer rounds).
