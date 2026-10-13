# RO-08 "Intermittent Fasting: The Best Way To Get Abs": round 3, Dan's revisions to the full film (written 2026-10-13)

**CONTENT, long-form (LFC). Task name for the next session: `Intermittent Fasting LFC R3`.**
Job doc: `Handoffs/video-editing/RO-08-intermittent-fasting.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md` (read the NEW top section, 2026-10-13, before anything else),
`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Skill: `/longform-edit`.
Recipe and traps: `.claude/skills/longform-edit/reference/ro08/README.md` (round 2 section and "After Dan's round 2 review").

## Where it stands

Dan reviewed the round 2 film (page `http://127.0.0.1:8871/`) on 2026-10-13. His reply is recorded word for word in
`/Volumes/Extreme/_edit_work/ro08/round3-plan/decisions.json`. The film is NOT finalized.

- Reviewed film: `/Volumes/Extreme/_edit_work/ro08/round2/RO-08 round 2 - full film.mp4`, sha256 `75d08be47b45b3a7...`.
  Hashes of everything he saw: `round3-plan/round2-hashes.sha256`. Its framing solve: `round3-plan/segs.round2.json`.
- Delivery folder: `claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs/`.
- VLC copies in `Videos to Review/`: three files named `Intermittent Fasting LFC R2 - ...`. Replace them this round (the
  opener B first minute is no longer needed).

## Locked by this reply

- **Opener A, the time-lapse.** "let's go with opener A time-lapse." It is the opener already in the film (frames 0 to 230,
  `round2/motion/OT-final.mp4`). Opener B is dropped.
- Everything he did not name stands as built (editor's reading; he listed his revisions and closed with "Those are the
  revisions"): A1 (lip-synced), A2 (no lip sync), A6, A7, A8, the moved G20 lower third, the cut, colour, voice 1a, the bed.

## The three revisions (film times are in the round 2 film)

1. **A4, 1:58.70 to 2:04.42: remove.** "Let's eliminate that clip at 202. I don't think that illustrates the idea well, or
   the joke really lands here." Delete A4 from `recipe/plan.py`; Dan is on camera there.
   ⚠ With A4 gone, shots `mine2.0r0`, `mine2.0r1` and `mine2.0r2` run 1:44.77 to 2:14.77 at one size (the punch-in) with nothing
   over them: 30 seconds, past the 22 second hold rule. Make ONE named framing change: `mine2.0r1` (1:53.35 to 2:04.42) goes to
   the camera frame (W) through `build.OVERRIDE` after the pin. It is a reframe inside one take, so no jump. Print `build.py segs`
   and confirm no jump and no hold over 22 s. Say it on the page.
2. **A3, 7:16.54 to 7:22.05: remove.** "This clip at 7:18 doesn't work. The water jumps up in the air for no reason. Not clear
   how that water jumping in the air is connected to the guy or that it is hungry. Eliminate that clip at 7:19." Delete A3 from
   the plan. The pancake stock clip before it (C23, to 7:16.54) and A1 after it (from 7:24.37) stay; Dan is on camera between.
3. **A5, 6:05.86 to 6:11.67: regenerate so it looks natural.** "when he grabs the muffin out at the end, all the donuts just
   disappear, vaporize, and go nowhere... regenerate this so it looks natural. Use a part of the clip only. If you can't make it
   look natural, eliminate all the food just vaporizing into the air and disappearing. If you can't make it look natural, then
   just use the camera scene here." His order of fallbacks is the order to work in:
   - **First, free: a two-shot cut of the existing take** (`round2/motion/A5-t1.mp4`). Shot one: he bites the donut, box full,
     clock at nine (take 0.00 to about 1.15 s, before any hand reaches for the box). HARD CUT (the hour passing). Shot two: clock at
     ten, box already empty, his eyelids droop and he sinks onto the keyboard (take from about 2.9 s, only once the muffin and both
     hands are at rest, to 5.8 s). Read every frame either side of the cut: nothing may be in the air, fading or half gone in a
     frame that is used. Pre-cut it into one file (the `opener_ot.py` pattern) because a two-source plan clip splits its slot evenly.
     It runs about 4.0 s against a 5.81 s slot: start the clip later (on "consume energy", about 6:06.7) so the sink still lands on
     "food coma" (6:09.6). Tell `finish08.py` about the cut inside the clip (it only knows cuts between sources) or the watch pass
     reports an unexplained jump.
   - **If shot two does not start clean, paid: two short takes from the approved frames, each from ONE frame** (`NOLAST=1`, 4 s,
     $0.40 each): from A5-start, natural speed, he eats the donut with relish and reaches toward the box; from A5-end (use it as the
     image), he sleeps on the keyboard, breathing, the muffin slipping in his hand. Cut between them. No prompt may ask for a
     fast-forward or for food to leave the box.
   - **If neither passes the three questions below: no clip.** Delete A5 from the plan and leave Dan on camera, then put the
     lower third G20 back where round 1 had it (`end="to digest", tail=0.3`, part phrase "heavy breakfast") since nothing is under it.

## The new standing rule this round must meet (VIDEO-RULES.md, top section, 2026-10-13)

Dan: "We need better quality control on these clips, so things that look like AI slop like this get caught in quality control
and don't make it to my review." Every AI take is asked three questions at playback speed, by the editor and again by the
independent reviewer, one written answer per clip:

1. Does everything obey cause and effect (nothing vanishes, appears or moves by itself)?
2. With the sound off, would a stranger say what the clip is showing?
3. Does it show the line he is saying, and if it is a joke, does it land in one viewing?

Ask them of the new A5 AND of the five AI clips that stay (A1, A2, A6, A7, A8) and the opener. Known weak spots to look at
first: A8 around its fifth second (the junk clears in one sweep and the background changes with it), A6 as his arms fill at the
fridge, A7 as he slides off the stool. If one of the clips he did not name fails a question, do not change it silently and do
not ship it silently: tell Dan on the page, first, with the fix and its price (trim to the part that works, one retake, or the
camera scene).

Budget rule from the same reply: at the cap with a clip that still has an obvious problem, ask for more budget; never ship it.

## Build order

Re-hash against `round3-plan/round2-hashes.sha256`. Point `build._PIN` at `round3-plan/segs.round2.json` (then the one named
override above). `plan.py` (A4 and A3 out, A5 new) -> `resolve.py` -> `from_plan.py --render` (only G20 may change, and only on
the no-clip path) -> pre-flight every clip against its slot -> context clips for the three spots -> full render into a new
`round3/` folder -> the finish chain (copy `finish_chain_r2.sh`; the sound is unchanged, so `srt_words.json`, `srt_drop.json`
and `srt_fixes.json` carry over from `round2/`) -> `carry_r2.py` pattern against the round 2 film -> one fresh `ra-reviewer`
on the changed images, with the three questions per AI clip in its brief -> edit sheet -> delivery gate -> round 3 page on a
new port (8872 is free as of today) listing the three changes with exact timestamps in the NEW film and watch ranges -> deliver,
replace the VLC copies.

## Gate status on the round 2 film, stated honestly (expect the same rows in round 3)

- Audio gate 12 of 13 (tone: voice 1a, his pick). Watch pass 494 of 494 images judged, 0 open defects.
- Delivery gate 32 pass, 7 fail: audio stamp (tone), cover 24 % against 40 % (it will drop to about 23 % with two clips out),
  hair top and headroom (camera framing, as shot), splice visibility 17 of 149, a burned-captions false alarm (lower thirds),
  a repeated-take false alarm (10:51). No bound was changed.
- Corpus entry for this rejection: `ro08-r2-full-film-ai-clips-rejected-20261013`.

## Cost ledger

- Replicate, AI motion and lip sync: **$10.57** of the **$15** Dan set for this video on 2026-10-12 (`round2/motion/ledger.json`).
  Room left: $4.43. The A5 paid path is $0.80.
- ⚠ Open question put to Dan on 2026-10-13: he said the standard budget for long-form content is now "$15 per clip". Recorded
  as $15 per long-form content VIDEO until he confirms which he meant. It does not change this round.
- Codex images on the subscription: 28. Gemini: nothing since round 1.

## When Dan finalizes

Mark the footage ranges used on the C1486 sidecar, register the AI clips that are in the final film and the opener in the clip
library (`--status used-final --used-in RO-08`; never A3, A4, the first A5, O6 or the rejected takes), add the approval to the
corpus, mark the edit sheet approved, set the queue to `finalized`, add the Shorts job (List 2) to `00-MASTER.md`, delete the VLC
copies, and remove the review services on ports 8869, 8870, 8871 and the round 3 port (`review_server.py PORT --remove`). Then
write the one Claude handoff for thumbnails and `/video-setup`.

## Starter prompt

Model: **Claude Opus 5.5, high effort** (a small revision round; Fable only if this round fails twice).

> Intermittent Fasting LFC R3. CONTENT, long-form. Read `Handoffs/handoff-20261013-ro08-round3-revisions.md`, the new top
> section of `.claude/skills/_shared/VIDEO-RULES.md` and `.claude/skills/longform-edit/reference/ro08/README.md`, then run
> round 3 of RO-08 with /longform-edit: remove the AI clips at 2:02 and 7:18, rebuild the donut clip at 6:07 so nothing
> vanishes (a part of the clip, a retake, or the camera scene, in that order), ask the three quality questions of every AI
> clip that stays, render the film, run every gate and one independent review, and send me the round 3 page with the
> changes and their timestamps. Rename this task `Intermittent Fasting LFC R3`.
