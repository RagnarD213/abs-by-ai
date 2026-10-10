# RO-03 "The Vacuum: Workout Only": round 2, the full film (written 2026-10-09, revised 2026-10-10)

**CONTENT, long-form family (LFC).** Sidebar name for this session: `Vacuum Workout Only LFC R2`.

## Goal
Build and deliver the full 16:9 film exactly as round 1 planned it: a 2:32 follow-along of three 20-second standing
vacuum holds with 30 seconds of rest between (Dan's Shoot 4 outline), all from the 8/14 shoot. Then every gate and one
independent review.

## Dan's words, recorded in `round2-plan/decisions.json`
- 10-09, before round 1: "Don't model it on Zeeshan's videos. He's not the best editor. Model it on Muhammad's workout videos."
- 10-09, after round 1: "Okay, everything looks good in the first minute and the review panel." He also asked for three
  differently filmed sets if they existed, "or if you can't find it anywhere, then we can do the loop."
- 10-10, after seeing where the other sets are: "We don't have it filmed in the same round of footage or the same
  shoot... I feel like it's going to look weird if we cut in footage from a different shoot and I change outfits and
  tan and everything." and "I just want to make sure we avoid mixing the two shoots."

## The sets: the one 8/14 hold, three times. Do not mix shoots.
The only hold filmed on the 8/14 shoot is C1625 33.40-55.60. Other vacuum holds exist, but on other shoots: 8/28 roll
C1677 (front, profile, front) and 7/8 roll C1490. In the 8/28 footage he wears no sunglasses, a chain in place of the
cord necklace and brighter green shorts, his skin is oiled, and the background is the white wall and hedge instead of
the house. Side by side: `Videos to Review/Vacuum Workout Only LFC - 8-14 vs 8-28 footage side by side.jpg`.
**Do not use C1677 or C1490 in this film.** Round 1's build already does it the approved way: each repeat changes size
at a different moment and set 2 opens on him starting the phone timer.

## Locked (do not reopen, do not ask again)
The first minute as shown (sha256 40bbd85a05c816e3a2f5903621475c6abbd48b171c63f4a68d4e91a0c854b60d), the cut (15 shots, 4,544 frames, rests 29.98 and 30.02 s), the title chip, the
set and rest countdown chip, the six lower thirds, the opening clip, the music and its levels, the flash into each set,
colour A and far / near framing, the sound mix (film mixed once, target -14.5). Round 1 page: http://127.0.0.1:8877/
(folder `/Volumes/Extreme/_edit_work/ro03/round1`; never overwrite it, build in `round2/`).

## Order of work
1. Re-hash the round 1 files against `round2-plan/decisions.json` (expected vs actual) before touching anything.
2. Full film: `build.render_range(0, total)` into `round2/`. Nothing in the plan changes.
3. SRT (uploaded, not burned) from the final words, chapters (Set 1, Rest, Set 2, Rest, Set 3, How to start), the edit
   sheet + `validate.py`, hair check on the whole film, `audio_gate.py`, `speechcheck.py` plus the gate on the speech
   alone, the watch pass, the delivery gate `--format longform`, one independent reviewer (`ra-reviewer`) on the
   finished file. Ask the reviewer one extra question: watching at normal speed, does the repeated hold read as a loop?
4. Deliver to `claude edited long form content/13 - The Vacuum Workout Only/`: master, SRT, chapters, 540p review copy,
   audio A/B, stamps, `notes-RO03.md`, recipe. Full film to `Videos to Review/Vacuum Workout Only LFC R2 - full film.mp4`;
   delete the R1 first-minute copy and the side-by-side picture there. Round 2 page on port 8877 (same port, new
   folder): the full film, "What I decided", the checks. No questions unless the reviewer raises one.
5. `roll_sidecar.py mark-used` for every source range (C1624, C1625, C1626, C1629). `queue.py set RO-03 delivered` plus
   the artifact mirror. Replace the board entry. Add any new lessons to `reference/ro03/README.md`.

## Gate status, stated honestly
Nothing has been gated as a delivery yet. Known before building: the whole-file audio gate fails four rows because the
holds are music only (tone, processing damage, word endings, loudness -15.3); the speech alone passes every row at
-13.4 LUFS. The delivery gate will also fail the rows RO-02 failed on this poolside framing (headroom, no-wide-level,
splice visibility, the two caption rows). Report them as they read. Tune nothing.

## Cost
$0 so far. No AI clip and no stock. Cap $5.

## Files
- Work: `/Volumes/Extreme/_edit_work/ro03/` (`recipe/`, `round1/`, `round2-plan/decisions.json`, `film_audio.wav`,
  `FIT.json`; `cache` and `hf/renders` are symlinks into `~/.cache/absbyai/ro03/`).
- Recipe in git: `.claude/skills/longform-edit/reference/ro03/` (README: order of scripts and the traps).
- Job doc: `Handoffs/video-editing/RO-03-the-vacuum-workout-only.md`.

## Recommended model and effort
Claude Opus 5.5, medium. Everything is built and locked; this is a render, the gates and one reviewer.

## Starter prompt
> CONTENT (LFC). Rename this task `Vacuum Workout Only LFC R2`. Read `Handoffs/handoff-20261009-ro03-round2-full-film.md` and `.claude/skills/longform-edit/reference/ro03/README.md`, then run round 2 of RO-03 "The Vacuum: Workout Only" with /longform-edit: build the full film exactly as I approved it in round 1 (the one 8/14 hold shown three times, no footage from any other shoot), run every gate and one independent review, and send me the full film for review. Update the edit queue.
