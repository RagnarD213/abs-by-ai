# RO-03 "The Vacuum: Workout Only": round 2, the full film with three differently filmed sets (written 2026-10-09)

**CONTENT, long-form family (LFC).** Sidebar name for this session: `Vacuum Workout Only LFC R2`.

## Goal
Build and deliver the full 16:9 film: a follow-along of three 20-second standing vacuum holds with 30 seconds of rest
between (Dan's Shoot 4 outline), with **each set a different filmed hold**, then every gate and one independent review.

## Dan's words (2026-10-09), recorded in `round2-plan/decisions.json`
- Before round 1: "Don't model it on Zeeshan's videos. He's not the best editor. Model it on Muhammad's workout videos."
- After round 1: "Okay, everything looks good in the first minute and the review panel." and "Let me see it with the
  three differently filmed vacuum sets if we have that, or if you can't find it anywhere, then we can do the loop.
  I'm pretty sure we have all three sets in there."

## Locked by that reply (do not reopen, do not ask again)
The first minute as shown (sha256 40bbd85a05c816e3a2f5903621475c6abbd48b171c63f4a68d4e91a0c854b60d), the title chip, the set and rest countdown chip, the six lower thirds (copy and
style), the opening clip, the music and its levels, the flash into each set, the talking pieces and their order, colour
A and far / near framing on the 8/14 rolls, the sound mix method. Round 1 page: http://127.0.0.1:8877/ (folder
`/Volumes/Extreme/_edit_work/ro03/round1`, never overwrite it; build in `round2/`).

## The one change: the sets
Round 1 showed the single 8/14 hold (C1625) three times. Dan remembered more takes, and he was right. They are not on
the 8/14 rolls (every silent stretch in C1614 to C1629 is him walking off to read his notes); they are B-roll on two
other shoots, same pool:

| source | what | notes |
|---|---|---|
| 8/14 **C1625** 33.40-55.60 | side-on, 20 s timed hold, phone timer beep at 55.08 | the set his intro line leads into; sunglasses, olive shorts; already built |
| 8/28 **C1677** 1:40-2:52 (front pass 2) | front-on, hands on hips; a short hold near 1:47-1:58, then one long hold from about 2:12 to 2:50 | eyes open, mouth closed; DS-04 took its front cue here (2:03.0-2:07.6) |
| 8/28 **C1677** 0:47-1:20 (profile pass) | side-on: slump 0:50-0:55, upright 0:56, draw in 0:57, hold | the shoot report measured the hold to about 1:10; my 1 fps look shows him still drawn in to about 1:18 with his hands moved behind him near 1:12. Check at native frames |
| 8/28 **C1677** 0:00-0:28 (front pass 1) | front-on hold 0:08-0:27 | he strains: mouth open, eyes shut for most of it. Last choice |
| 7/8 **C1490** 0:14-0:28 front, 0:38-1:04 profile | high camera angle, 1080p, holds about 14 s | backup only |

C1677: `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1677.MP4`,
3840x2160, S-Log3, untagged (decode BT.709), no usable sound (crew audio only). Details: `Docs/SHOOT_828_FOOTAGE_REPORT.md` section B2
and the roll sidecar. C1490: `/Volumes/Extreme/abs by ai 7:8 Jeff Chagrin shoot/main camera/C1490.MP4`.

**My pick for the three sets:** set 1 = C1625 (it follows "I'm going to time out 20 seconds on my phone timer. Here we
go."), set 2 = C1677 front pass 2 (the long hold), set 3 = C1677 profile pass. If the profile hold is under 20 clean
seconds at native frames, one filmed hold is still one set: use front pass 1 or C1490's profile for set 3 instead,
and say so on the page. Never split the long front hold into two sets.

What the build has to solve for the two 8/28 sets:
1. **Exact holds.** Find each hold's draw-in frame and release frame at native frame rate. The countdown runs the 20
   seconds he is actually holding. The seconds before it (slump, straighten, draw in) are the GET READY lead-in.
2. **Rests stay 30.0 s** from the end of one hold to the start of the next. In round 1 set 2 opened on him starting the
   phone timer; that lead-in goes away. Fill each rest with the talking piece plus the new set's own lead-in, and set
   the length by moving the set's in point, never by trimming his speech.
3. **Crop.** 4K source, he is about a quarter of the frame height: a 1080p far window and a near window both fit with
   no upscale or close to it. Hair-anchored, fixed per shot, one size change inside each hold (`shots.SETCUT`,
   `build.FORCE`). The form-cue lower third sits on the far framing only, clear of his waist.
4. **Colour.** Dan approved the filmed B-roll grade for these hard-sun rolls on 10-01: the 8/28 LUT at 1.15 to 1.30,
   recipe in `/Volumes/Extreme/_edit_work/broll-cuts-20260929/cut.py` (`_shared/cliplib/README.md`). Trim it per clip
   so his skin sits beside the 8/14 colour A shots (raw torso-skin band 0.38 to 0.50 in `frames.py`). RO-02 found the
   library clip B0428 (cut from this roll) dark next to the 8/14 footage, so put a set 1 frame and a set 2 frame side
   by side before rendering.
5. **Sound.** The 8/28 sets have no beep and no usable track: music only, with the countdown chip as the timer. Keep
   set 1's real beep.
6. **Continuity Dan will notice.** In the 8/28 footage he wears no sunglasses and greener shorts, and the background is
   the hedge and spa wall, not the house. The rests (8/14) cut to and from it. That is what "differently filmed"
   means here; state it in one line under "What I decided" so he can overrule it.

## Order of work
1. Re-hash the round 1 files against `round2-plan/decisions.json` (expected vs actual) before touching anything.
2. `roll_sidecar.py show` for C1677 and C1490. Native-frame strips of each hold: first and last second, draw-in, release.
3. `edl.py` (new set2 / set3 pieces; `E.src` must take a roll from another shoot folder), `shots.py`, `measure.py`,
   `skin.py`, `frames.py` (a 4K roll and its own grade), `resolve.py` (holds and beeps per set: `HOLD_SRC` is per
   piece now), `build.py framings`, `build.py audio`.
4. Stills of the two new sets on their graded frames, one grade pair (set 1 beside set 2), then the full film:
   `build.render_range(0, total)` in `round2/`.
5. SRT (uploaded, not burned) from the final words, chapters, edit sheet + `validate.py`, hair check on the whole film,
   `audio_gate.py`, `speechcheck.py` plus the gate on the speech alone, the watch pass, the delivery gate
   `--format longform`, one independent reviewer (`ra-reviewer`) on the finished file.
6. Deliver to `claude edited long form content/13 - The Vacuum Workout Only/`: master, SRT, chapters, 540p review copy,
   audio A/B, stamps, `notes-RO03.md`, recipe. Full film to `Videos to Review/Vacuum Workout Only LFC R2 - full film.mp4`
   and delete the R1 first-minute copy there. Round 2 page on port 8877 (same port, new folder) showing only what is
   new: the two sets, the grade pair, the full film, "What I decided", the checks.
7. `roll_sidecar.py mark-used` for every source range (C1624, C1625, C1626, C1629, C1677). `queue.py set RO-03 delivered`
   plus the artifact mirror. Replace the board entry. Add the lessons to `reference/ro03/README.md`.

## Gate status, stated honestly
Nothing has been gated as a delivery yet. Known before building: the whole-file audio gate fails four rows because the
holds are music only (tone, processing damage, word endings, loudness -15.3); the speech alone passes every row at
-13.4 LUFS. The delivery gate will also fail the rows RO-02 failed on this poolside framing (headroom, no-wide-level,
splice visibility, the two caption rows). Report them as they read. Tune nothing.

## Cost
$0 so far. No AI clip and no stock is planned. Cap $5.

## Files
- Work: `/Volumes/Extreme/_edit_work/ro03/` (`recipe/`, `round1/`, `round2-plan/decisions.json`, `film_audio.wav`,
  `FIT.json`; `cache` and `hf/renders` are symlinks into `~/.cache/absbyai/ro03/`).
- Recipe in git: `.claude/skills/longform-edit/reference/ro03/` (README: order of scripts and the traps).
- Job doc: `Handoffs/video-editing/RO-03-the-vacuum-workout-only.md`.

## Recommended model and effort
Claude Opus 5.5, high. Recipe-backed, but two new 4K sources need framing and colour judgment, then gates and a reviewer.

## Starter prompt
> CONTENT (LFC). Rename this task `Vacuum Workout Only LFC R2`. Read `Handoffs/handoff-20261009-ro03-round2-full-film.md` and `.claude/skills/longform-edit/reference/ro03/README.md`, then run round 2 of RO-03 "The Vacuum: Workout Only" with /longform-edit: keep everything I approved in round 1, replace the repeated hold with three differently filmed sets (C1625 from 8/14, then the front and profile passes of 8/28 roll C1677), keep both rests at 30 seconds, build the full film, run every gate and one independent review, and send me the full film for review. Update the edit queue.
