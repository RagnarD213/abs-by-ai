# RO-07 "Why You MUST Work Out Every Day": round 2, Dan's revisions (written 2026-10-10)

**CONTENT, long-form (LFC). Task name: `Work Out Every Day LFC R2`.** Skill: `/longform-edit`.
This replaces `handoff-20261009-ro07-round1-dan-review.md` (round 1 has been reviewed).

## Read first, in this order

1. `/Volumes/Extreme/_edit_work/ro07/round2-plan/dan-notes-20261009-verbatim.md` : every note Dan gave, word for word, with what is done and not done.
2. `/Volumes/Extreme/_edit_work/ro07/round2-plan/decisions.json` : verdicts, locks, hashes, `motion_authorized`.
3. `.claude/skills/longform-edit/reference/ro07/README.md` : script order and traps. Work dir: `/Volumes/Extreme/_edit_work/ro07/` (`recipe/` is the live copy).
4. `.claude/skills/_shared/VIDEO-RULES.md`, top section (capital letters in graphics, B-roll choice: both written from this review).

Re-hash before touching anything: `round2-plan/round1-hashes.sha256`, plus the two locks below.

## Dan's verdict on round 1

"This is one of the worst edits that you have done in a long time." Colour and sound rejected, capital letters overused in the graphics, weak B-roll choices. He liked: workout clips at the start (the idea), the A2 frames, the cut itself drew no notes.

## Locked on 2026-10-10 (his words: "Let's go with D for the color... Let's go with 4 for the voice warm less kitchen echo. Agree with both of your recommendations.")

- **Colour D** for both kitchen rolls. `look_option.txt` is already `D`; the grade strings are in `grades.json` (`D`: light denoise, shadow blue removed, skin Y90 to 0.57, saturation 1.08, hue +4). Reference sample `round1b/colour/option-D.mp4`, sha256 in `decisions.json`. The poolside B-roll keeps its own grade.
- **Voice 4** : lav (channel index 1 on both rolls), light dereverb (alpha 0.30, floor -10 dB), EQ `highpass=f=70,equalizer=f=140:t=q:w=1.0:g=+1.5,equalizer=f=450:t=q:w=1.2:g=-3.0,equalizer=f=3200:t=q:w=1.5:g=-1.0`, NO expander, NO fitted EQ, shared finisher to -14 LUFS. Reference `round1b/audio/4-warm-less-room.wav` (built by `recipe/audio_options.py`), sha256 in `decisions.json`.

## Work, in order

1. **Regression corpus first** (`.claude/skills/_shared/qc_corpus/README.md`): add the rejected round 1 first minute (colour C and the fitted-EQ + expander voice, Dan's words) and the two approvals above, before building fixes. The audio gate passed the rejected mix 12 of 12: report that as a finding, do not tune a threshold.
2. **Voice through the shared chain.** `voice_chain.py` always applies its expander, so add an opt-out flag (shared file: run `selftest.sh`, push at once). Then `build.render_voice` passes the EQ above with `--eq`, `--dereverb-because "Dan heard the room on the RO-07 round 1 first minute and picked audition 4 (2026-10-10)"` and the new flag. Delete `FIT.voice_chain.json` (it holds the rejected fitted EQ and `build.py` reads it). Prove the chain output matches the approved audition on the same 31 s (output 13.8 to 44.8 s). Run the audio gate and report every row honestly; Dan's pick is the approval.
3. **Graphics text.** Apply his capitalization list exactly (G13, G15, G17, G19, G23, G24, G26, G28, G35, G36, G38, G39, G40, G41, G42, G44: title case). Then thin the rest by judgment: keep full caps on about six of the 46 at most and list them in "What I decided". Split G43 into two lower thirds, both with topic "How many circuits?": "Beginners: 2 circuits, about 5 minutes total." and "Advanced: 3 or 4 rounds, 7.5 to 10 minutes." Re-render EVERY lower third (the template now adds the missing space between parts, commit b49eca7; only G01 and G02 are re-rendered). Check widths before the long render (the layout check in the recipe README).
4. **Clips.** Compare two or three candidates' previews for every slot and take the one where he looks best; start on the first rep.
   - Opener C01: already set in `plan.py` to B0448 (correct fast jump rope), B0456 (handstand push-ups), B0453 (decline push-ups), 0 to 6.2 s. Not rendered. He also named kettlebell deadlifts: no horizontal cut exists (source 8/28 roll C1671); cut one if it looks good.
   - C18 also uses B0448: no source twice. Change one.
   - C20: remove the posing clip; use workout clips of him not used elsewhere.
   - C21: start where the squat reps start.
   - C22: push-ups WITH the handles (7/8 roll C1492, or B0452). C23 uses the angle he disliked in the opener (C1491, from behind): replace it too.
   - C24: his real knee push-ups, not the AI demo. Look through C1491, C1492 and the 8/28 push-up roll C1671 ("five levels of pushups", 152 to 193 s).
5. **AI clips.** A1 is removed. A2: motion exists, `round2/motion/A2-t1.mp4` (8 s, $0.80); read it frame by frame, judge at speed, trim to its 6.3 s slot, show it in context. A3: new END frame `aiframes/A3-end-r1b.png` (giant glove from outside the door, knocks him down) has NOT been looked at or shown; get Dan's approval of START + new END, then one take with `recipe/gen_motion.py` (add A3 to `motion_authorized` only after he approves).
6. **Still unanswered from round 1** (never infer approval from silence; ask again in one short list): the two framing sizes, hair at the top edge, length (18:07 as cut, or about 16:50), a Gymboss screen recording, the "$50 for all that stuff" line, music bed, no timer in the workout section.
7. **Owed cutaways.** Cover is about 19 % against the delivery gate's 40 % floor: add about 20, his own B-roll first, and show them as new items.
8. **Review page for round 2** (new folder `round2/`, new port; only what changed or is new): the rebuilt first minute in D with voice 4 and the new opener, the changed graphics, the new and changed clips, A2 moving, A3 frames, "What I decided", the open list from step 6. Copy the first minute to `Videos to Review/`. Then stop for Dan.
9. **Full film only when nothing is pending**, then edit sheet, audio gate, watch pass, one independent review (`ra-reviewer`), delivery gate, delivery folder `claude edited long form content/14 - Why You MUST Work Out Every Day/`, queue `delivered`.

## Status of gates

Round 1 first minute: audio gate PASS 12 of 12 on a mix Dan rejected (see step 1). Nothing else has been gated. No full film exists.

## Cost ledger (cap $5 for this video, all rounds)

Replicate: $0.80 (A2, one Veo 3.1 Fast take). Codex: 8 images on the subscription. Gemini listens: 4 short calls, cents. Next expected: A3 one 6 s take, $0.60.

## Pages and files

Round 1: http://localhost:8857/ . Colour and sound: http://localhost:8858/ . VLC copies in `Videos to Review/` (delete them only when Dan finalizes the video). Queue state `draft_review`; board entry `RO-07`.

## Model and effort

Opus 5.5, high.

## Starter prompt

> Work Out Every Day LFC R2. CONTENT, long-form. Read `Handoffs/handoff-20261010-ro07-round2-revisions.md` and the four files it lists, then continue RO-07 with /longform-edit. Colour D and voice 4 are locked. Do the work in the handoff's order: corpus entries, the voice through the shared chain, my capitalization and G43 notes, the clip changes (pick footage where I look best, start on the first rep), A2 in context, the new A3 end frame for my approval, the open questions from round 1. Then show me a round 2 page with the rebuilt first minute and only what changed or is new. Build the full film only when nothing is pending.
