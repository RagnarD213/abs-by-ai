# RO-07 "Why You MUST Work Out Every Day": round 3, two trims, the A3 motion, then the full film (written 2026-10-10)

**CONTENT, long-form (LFC). Task name: `Work Out Every Day LFC R3`.** Skill: `/longform-edit`.
This replaces `handoff-20261010-ro07-round2-dan-review.md` (Dan replied the same day).

## Read first, in this order

1. `/Volumes/Extreme/_edit_work/ro07/round3-plan/dan-notes-20261010-verbatim.md` : his round 2 reply, word for word.
2. `/Volumes/Extreme/_edit_work/ro07/round3-plan/decisions.json` : verdicts, locks, `motion_authorized` (A2, A3), the three unanswered items and their defaults.
3. `.claude/skills/longform-edit/reference/ro07/README.md`, sections "Round 1 was rejected" and "Round 2" (script order, traps). Work dir `/Volumes/Extreme/_edit_work/ro07/` (`recipe/` is the live copy).
4. `.claude/skills/_shared/VIDEO-RULES.md`, top section (the 2026-10-10 rule written from this review: funny AI clips; show the rep from the first second; show the lift, not the setup).

Re-hash before touching anything: `round2-plan/round2-hashes.sha256` (12 files, all OK when this was written), plus colour D
`round1b/colour/option-D.mp4` (`509b1bf9...ff5f`) and voice 4 `round1b/audio/4-warm-less-room.wav` (`7ad58a58...01bc`).

## Dan's verdict on round 2 (2026-10-10)

Three changes, then: "Everything else is looking good. Give me the handoff document for the next round." Round 2 page:
http://localhost:8859/ . Everything shown there and not named below is locked (editor's reading of his sentence; recorded as such).

## Work, in order

1. **Opener, the handstand push-up piece (film 2.07 to 4.14 s).** His words: "I like this clip, but I want you to start it immediately
   when I'm doing the reps. This is just me doing the handstand. I want to see the reps from the first second." Today it is library
   B0456 from 0.0 s: he lowers for 0.5 s, sits at the bottom for about 0.5 s (reads as a static headstand at film 3.0 s), and comes up.
   Go back to the source, 8/28 roll C1684 (39.5 s; B0456 is 12 to 22 s of it; grade 1.45 LUT, saturation 0.88, crop 2880x1620+520+440):
   measure his head height frame by frame, pick the reps with the least pause at the bottom, and start the piece on a frame where he is
   already moving down. A slight speed-up is allowed if a full down and up does not fit; never a hold. The three opener pieces may be
   uneven lengths if that shows the reps better. Show it to yourself as a 0.1 s frame strip before rendering. Keep the jump rope and the
   decline push-up pieces as they are.
2. **C31, the AI deadlift before A2 (film 2:24 to 2:27, 3.3 s).** His words: "show the rep itself: show him lifting the weight up, not
   the exit at the end." Today it is library A0019 from 0.3 s (setup only). Measured: he grips the bar until about 3.3 s, the bar leaves
   the floor at about 4.2 s, lockout at about 5.4 s, and a red X is burned in from about 6.75 s. Use A0019 from about 3.1 s (3.1 to 6.43 s)
   and confirm on a 0.05 s strip that no frame of the X is inside the slot. Keep the AI-GENERATED label.
3. **A3 motion (approved: START `aiframes/A3-start.png` `39e6fa6a...`, END `aiframes/A3-end-r1b.png` `0bf1e7cf...`).** `gen_motion.py`
   still reads `round2-plan/decisions.json` and `A3-end.png`: point it at `round3-plan/decisions.json`, at `A3-end-r1b.png` and at
   `round2-plan/round2-hashes.sha256`, write takes to `round3/motion/`. Write a new prompt (`recipe/ai-motion-prompts/A3.txt` describes
   the rejected gym-bag version): he pulls the front door open, a giant red cartoon boxing glove on a metal spring shoots in from outside
   at the right edge, hits him in the face and knocks him off his feet, the gym bag flies; cartoonish, funny, locked camera. One 6 s take
   ($0.60). Read it frame by frame, judge at speed (small faults pass: VIDEO-RULES), trim to the 4.6 s slot (film 4:55, under "punch you
   in the face") so the hit lands on "punch". Replace `frames=[...]`, `pending=True` in `plan.py` with the take. One more take only if a
   viewer would see the fault at speed.
4. **The three items he did not answer** (length, a Gymboss screen recording, music). If his starter prompt fills them in, do that.
   If it does not, use the defaults in `decisions.json` and say so in the delivery: keep 18:07 as cut; Gymboss stays as lower thirds
   G36 and G37; add the quiet bed as on RO-06 (`bed.py`, `RO07_BED`, level set on the audio gate's floor row, transcribe the bed first
   and require zero words). If he picks the 16:50 length, apply the five trims listed on the round 2 page in `edl.py`, regenerate the time
   maps, graphics timing and the first minute, and show him the first minute again before the full film.
5. **Full film** (nothing else is pending): `resolve.py`, `from_plan.py --render` (only what changed), `build.py filmvoice`, the whole
   range. Then the skill's checks on the exact file: jump-cut and junk pass on every join, subtitles (`.srt`, no burned captions),
   chapters, edit sheet, audio gate, watch pass, one independent review (`ra-reviewer`), delivery gate. Copy the film to
   `Videos to Review/Work Out Every Day LFC R3 - full film.mp4`. Delivery folder
   `claude edited long form content/14 - Why You MUST Work Out Every Day/`. Queue `delivered`.
6. **Delivery message** (later-round rule): list the three revisions with exact timestamps in the new film and a short watch range
   around each (opener handstand about 0:02 to 0:04, C31 about 2:24, A3 about 4:55), and say the other approved scenes were kept.
   Build a round 3 page (new folder `round3/`, new port) with the film on top and those three items.

## Built and locked (do not apply twice)

- Round 2's work is all in `plan.py`: capitals, G43A and G43B, clips C08 C18 C20 C21 C22 C23 C24, A2 motion from 0.8 s, cutaways C30
  C32 C33 C34 C35 C37 C38 C39 C42 (C31 changes in step 2). A1, C36, C40, C41 are removed.
- Voice: `build.VOICE4` through the shared chain (`--no-expander-because`). Colour D; the poolside rolls keep their own grade.

## Gates, stated honestly

Audio gate on the round 2 first minute and on the whole-film voice: FAIL on one row, tone (less treble than the reference; that is the
voice he chose). Expect the same row on the film; report it, change no limit. Cutaway cover is 26 % against the delivery gate's 40 %
floor (RO-06 was approved at 34 %): it will fail `style:coverage`; report it. The library has no clip for the alarm clock, commute,
couch and tired-at-night lines; he approved the film's cutaways as shown, so do not add stock unasked. Hair touches the top edge in six
late shots (left as shot): `framing:hair_top` may fail; report it. Nothing else has been gated.

## Cost ledger (cap $5 for this video, all rounds)

Replicate: $0.80 (A2). Gemini listens: about 7 cents. Codex: 8 images on the subscription. Next: A3, one 6 s take, $0.60
(a second take only if needed: $0.60 more).

## When he finalizes

Delete this video's copies from `Videos to Review/`, remove the review services on 8857, 8858, 8859 and the round 3 port
(`review_server.py PORT --remove`), add the corpus approval, mark the library clips used, queue `finalized`, write the setup handoff
(one Claude handoff: thumbnails with the Codex subscription, then `/video-setup`; Sunday queue rule).

## Model and effort

Opus 5.5, high.

## Starter prompt

> Work Out Every Day LFC R3. CONTENT, long-form. Read `Handoffs/handoff-20261010-ro07-round3-full-film.md` and the files it lists, then continue RO-07 with /longform-edit. Do the work in the handoff's order: re-trim the handstand push-up piece so I am doing reps from its first frame, re-trim C31 so it shows the deadlift rep, make the A3 motion from the frames I approved, then build the full film and take it through every check. Three things I did not answer last round. Length: [keep 18:07 / trim to about 16:50]. Gymboss: [I will send a screen recording / lower thirds only]. Music: [quiet bed / voice only]. Where I left one blank, use the default in the handoff. Give me the finished film with the timestamps of the three changes.
