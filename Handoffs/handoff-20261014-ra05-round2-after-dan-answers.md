AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `How AI Real Abs AD R2`.

# RA-05 "How AI Can Get You REAL Six Pack Abs": round 2 (Dan has answered round 1)

**Written 2026-10-14 by the round 1 session (Claude, Opus 5.5).** Replaces `handoff-20261013-ra05-round2-after-dan-review.md`
(that file is the round 1 record: take map, traps, file hashes; read its "The cut, for the record" and "Traps" sections).
Job doc: `Handoffs/video-editing/RA-05-how-ai-can-get-you-real-six-pack-abs.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`, `_shared/IMAGE-GENERATION.md`.
Recipe: `.claude/skills/ad-edit/reference/ra05/` (README: stage order and eight lessons). Work dir: `/Volumes/Extreme/_edit_work/ra05/`.
Dan's words, per item, with hashes: `/Volumes/Extreme/_edit_work/ra05/round2-plan/decisions.json` (repo copy
`.claude/skills/ad-edit/reference/ra05/round2-plan-decisions.json`).

## What Dan decided (2026-10-14, on the round 1 page http://127.0.0.1:8805/)

1. **Opening, his own version:** *"in the first 3 seconds, I want to show the full generation functionality, but very sped up,
   so that the after shows for a full second at the end. It goes through adding the photo and then loading in less than 2
   seconds, so that they can visibly see the after on screen."*
2. **Length: no line cut, speed it up instead:** *"don't cut any of the lines, but just accelerate the video as necessary to get it
   under 60 seconds."* Every line in is 60.96 s of talk + the 0.85 s end hold. **Use a uniform 1.06x** (pitch kept): 57.51 s of
   talk + the 0.85 s hold at normal speed = **58.36 s**. 1.05x lands at 58.9 s, too close to the job's 0:59 ceiling.
3. **Claim lines: keep both as filmed** (*"The claim lines are fine."*).
4. **AI clips:** *"let's make the first one with the guy on the couch"* (Steps out of the phone: frames first). The robot tailor is
   out. **In its place, the body scan from the start VSL's version A opening:** library **A0044**, the same file as
   `/Volumes/Extreme/_edit_work/wv01-edit/round4/motion/SCAN-readable.mp4` (sha256 68ef87d8c63ac0b6, 1920x1080, 5.0 s, Dan
   approved it on WV-01: *"Alternative body scan concept, I like that."*). It replaces the curls clip B1.
5. **From his RA-14 picks, already applied here and not asked again** (*"Let's go with a wider crop, the recommended crop. Go with
   the brighter golden skin, the recommended color. Redo the analysis card in our graphics in soft blue light with our hyperframes.
   Make that standardized with the rest of our videos. Let's do the voice with a bass lift."*):
   - shot sizes: round 1's `framing_choice.json` (close 648x1152, wide 810x1440) is RA-14's F2 converted to this roll; now locked;
   - colour: round 1's `grade.json` (C2 brighter gold re-baked for C1664, `colour/luts/ra05_C2_brighter_gold.cube`); now locked;
   - voice: **with the bass lift**: the fitted tone plus `equalizer=f=120:t=q:w=0.8:g=+3.0` (RA-04's `mixB` method), re-gated;
   - analysis card: **the Soft Blue HyperFrames template** `_shared/hyperframes/analysis-card/` (approved on RA-14 round 3, kind
     `analysis` in `from_plan.py`), not round 1's recoloured `adkit/analysis_card.py`. Same subject: the app man's result picture.

## Round 2 deliverable: one review page, then stop

The couch clip is an AI clip Dan has not seen, and it sits in the first 8 seconds, so this round is the frames plus the finished
first 30 seconds (the "whole short in one round" rule applies to round 3). Build in `round2/`; serve on a new port (8805 is round 1).

1. **Re-hash** the round 1 files listed in the old handoff (expected against actual) before touching anything.
2. **The cut with every line.** `cp edl_spec_full.json edl_spec.json`, `HEAD_SRC=208.24 python3 s03_edl.py` (60.96 s, 17 pause
   cuts, seams 9.98, 24.09, 48.18, 54.52 s). Then the speed-up, as ONE factor everywhere, `SPEED = 1.06` in `ra01lib.py`:
   - audio: `atempo=1.06` on `cut_audio.wav` in `s08_audio.py` before the voice chain (the music bed is NOT sped up), then the
     end hold appended at normal length;
   - words, pieces, seams, `dur`: film time = tight time / 1.06 (one new step after `s03_edl.py`, keep `src_in/src_out` as they are);
   - picture: in `s10_render05.py` each Dan segment takes `(t - t_in) * 1.06` of source and plays it with `setpts=PTS/1.06`, then
     `fps=30000/1001`; the end hold is normal speed;
   - re-run `s09_align.py` on the sped-up mix so the captions follow the real audio; re-check every caption word at speed.
   Listen to the sped-up voice before building pictures on it (one clean 15 s window that starts on speech, VIDEO-RULES).
3. **The opening card, 0 to about 3.5 s** (to "but", the end of "six-pack abs," at 1.06x). From B0049, the same man throughout: adding the
   photo, the options, the Generate tap and the loading screen compressed into **2.0 s or less**, then the result screen alone
   (from 28.0 s of the recording) for **at least 1.0 s**, with the AI-GENERATED label. Read B0049 frame by frame first: never the
   photo-crop screen (ad-edit lesson 15), never "Meet the new you" (26.8 to 27.6 s), never the email form (the 1320x1600 crop keeps it
   out). A plain fast cut through 4 to 6 moments reads better than one smooth 11x ramp; pick whichever shows each step clearly, and
   say which on the page. Show it as a still strip and moving.
4. **Couch clip frames, "Steps out of the phone"** (plays about 3.5 to 7.9 s, under "but now guys are using AI to get them six-pack
   abs in real life"). START: an ordinary guy (not a model, not Dan) in a plain t-shirt on his couch holds his phone toward camera;
   on its screen, a picture of him shirtless with a six pack. END, a separate shot joined by a CUT, never a morph: the same guy,
   same couch, shirt off, the same abs, holding the phone next to them, grinning. 9:16, subject in the centre third, no stomach
   framing beyond what the beat needs, no generated lettering, his face must read as the same man in both. **Use the Codex
   subscription to generate the images** (`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`). Prompt rules:
   ad-edit Step 4.5. Answer the three sense questions under the frames. Give the motion cost (ad cap $10, spent $0). No motion.
5. **Body scan card** (A0044) under "It will see exactly where you need to gain muscle, and tailor your workout program" (film time
   about 26.0 to 29.9 s after the speed-up). Its four callouts span almost the whole width, so it is a whole-clip card (VIDEO-RULES
   2026-10-01: fill, else centre square, else the whole clip): trim the sides to the callouts only (about x 150 to 1770 of 1920),
   full height, on the Soft Blue field above the caption line, the AI-GENERATED chip clear of his face and the callouts. Play it at
   natural speed from about 1.0 s so the fourth callout has landed before the cut (slowing it is not allowed). Check it is sharp and
   readable at 1080x1920; say how big the callout text is on the page.
6. **Voice with the bass lift**, the analysis card from the HyperFrames template, then re-plan `s05_plan05.py` (cards: opening,
   couch placeholder, lock K1, analysis A1, tour T1, scan, poses B2; LT1, LT2, the button). Every uncovered pause splice still gets
   a size change (the plan asserts it). The insert coverage goes up to about 47 %.
7. **The finished first 30 seconds** with the couch clip as a LABELLED START/END-frame placeholder (VIDEO-RULES "Future contextual
   previews"), every changed item moving in context, the "What I decided" list, a reply box. Look at and listen to it before sending.
8. Handoff for round 3, then stop. Do not fire round 3 before Dan answers.

## Round 3 (for the record)

Couch clip motion from the approved frames only, checked frame by frame and with the three sense questions; then the WHOLE 9:16 on
the page (not 30 s); then, after Dan approves it, the delivery list in the old handoff's "Next action" item 5 and the 16:9.

## Risks, stated plainly

- With the opening card and the couch clip, Dan's face first appears at about 7.9 s ("Seriously"). If the first 30 seconds look
  slow to reach him, the fix is to start the couch clip later (at "in real life") and put him on camera for "but now guys are using
  AI"; say it on the page, do not change it unasked.
- The before photo in the app recording is a heavy shirtless man, now on frame one (his choice). It is the same recording that runs
  in the approved RA-01 and Ad 1.
- 1.06x on the voice: listen for a hurried sound on his fastest lines; the alternative is 1.05x (58.9 s, legal but tight).

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `How AI Real Abs AD R2`. Read `Handoffs/handoff-20261014-ra05-round2-after-dan-answers.md` and run round 2
> of RA-05 "How AI Can Get You REAL Six Pack Abs" with /ad-edit. My answers are already recorded in
> `/Volumes/Extreme/_edit_work/ra05/round2-plan/decisions.json`. Keep every line and speed the ad up to land under 59 seconds,
> build the new sped-up generation opening, the body scan card from the start VSL, the bass-lift voice and the Soft Blue analysis
> card, make START and END frames for the couch clip, and show me the first 30 seconds and the frames on one review page. No AI
> motion until I approve the frames. Use the Codex subscription to generate the images. Write the round 3 handoff and stop.

**Recommended model and effort: Opus 5.5, high.** A bounded revision with one new mechanism (the speed-up) and one frame pair.
