AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Never Pay Nutritionist AD R2`.

# RA-15 "Never Pay A Nutritionist Again": round 2, after Dan reviews the round 1 page

**Written 2026-10-14 by the round 1 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-15-never-pay-a-nutritionist-again.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe: `.claude/skills/ad-edit/reference/ra15/` (README: stage order and seven lessons), on top of `../ra05/` and `../ra04/`.

**Do not fire this until Dan has replied to the round 1 page.** His reply goes, word for word, into
`/Volumes/Extreme/_edit_work/ra15/round2-plan/decisions.json` (per item: id, files with sha256, verdict, his words,
scope, next action; `motion_authorized` for each AI idea he says yes to) before anything is built.

## Where it stands

Round 1 page: **http://127.0.0.1:8818/** (managed review service, folder `/Volumes/Extreme/_edit_work/ra15/round1/`).
It shows six decisions, the finished first 31 seconds (to the end of the factory card), four AI clip ideas as start
and end frames, the colour, shot size and voice options (outdoor rule, 10-14), "What I decided", and every graphic and
clip as a still with a play-in-context button. A full 9:16 draft (51.18 s) exists for internal checks only.
Nothing is gated, stamped, audited, delivered or uploaded. Queue state: `in_progress`. Spend: $0 of the $10 ad cap.

## The six decisions waiting for Dan

1. **Hook wording.** A (in the cut): "Nutritionists have gone obsolete. AI just took their job." (his on-set rewording, last
   read, one take with the rest). B: the script's "Never pay a nutritionist again. AI just took their job." (hook take 1,
   C1668 13.1 to 17.4 s). B = `edl_spec_B.json` (49.4 s of talk, one more seam at about 4.0 s).
2. **Colour.** C2 golden (in the cut, his RA-14 pick re-baked: exposure 2.0 here vs 2.4 on C1667), C1 level, C3 cooler.
3. **Shot size.** F2 (in the cut, his RA-14 pick converted: close 594x1056, wide 738x1312), F1 tighter (558x992 /
   684x1216), F3 wider (630x1120 / 774x1376). All in `framing_choice.json` `options`.
4. **Voice.** V1 +1.5 dB at 120 Hz (in the sample, recommended, audio gate PASS), V2 +3 dB as on Cheat Code (fails the tone
   row, max 2.90, the known mismatch), V3 none (PASS).
5. **AI clip ideas, yes or no each.** I1 "Cleared out" (opener 0.00 to 2.34, replaces library A0016), I2 "Chicken and
   broccoli forever" (fridge, 29.03 to 31.26, replaces A0017), I4 "Ask it what to order" (restaurant, 37.07 to 39.01; the
   macro screen keeps 35.57 to 37.07), I5 "The cardboard nutritionist" (39.01 to 42.54, now Dan on camera).
6. **Claim lines as spoken** (captions only): "Thousands of guys are replacing expensive nutritionists with AI." and "A
   nutritionist charges hundreds of dollars per month and sees you twice." A keep, B he names the cut.

## The cut, for the record

- Roll `C1668.MP4` (8/28 portrait pool roll, dual-mono lav; `C1668.MP4.audio_source.json` beside the roll). Main take
  72.06 to 130.5 s is one unbroken read of the whole script. Three ranges (`edl_spec.json`): R1 72.06 to 91.41 (hook to
  "six-pack abs."), R2 94.04 to 121.37 ("Generate an image of yourself with abs" to "sees you twice."), R3 121.99 to 130.5
  ("Start with a picture" to the end).
- Cut out: the hidden restart "Generate an image of yourself." (91.0 to 94.1, heard only by 8 s Replicate windows) and a
  mouth noise after "twice." (121.4 to 121.8). Orphan check on the cut audio: nothing uncovered.
- 15 pause cuts; the beat after "One," "Two," "And three," is kept (`PROTECT` in `s03_edl.py`). Seams 17.45 and 42.54 s,
  both under cards. Head edge pinned at 72.06 (after his inhale). End hold 0.85 s: smile, hands on hips.
- Word list: three Replicate pieces plus isolated windows, merged and corrected in `tx/c1668.whisper.json`, CTC aligned
  (164 of 164 words). Spoken wording kept over the script: "how much body fat", "Start with a picture", "and to get".

## Graphics and clips in round 1 (film time, 51.18 s total)

| id | what | where | source |
|---|---|---|---|
| O1 | museum gag, AI-GENERATED | 0.00 to 2.34 | A0016, window 560x996 at x 680 from the top (plaque below the captions) |
| L1 | 1 of 3 / Knows The Fat You Need To Lose | 10.84 to 16.32 | HyperFrames lower third |
| P1 | his photo refined, then his result alone, AI-GENERATED | 17.45 to 20.89 | B0049 13.0 s, then 28.0 s, crop 1320x1600 at y 170 |
| A1 | analysis card, Soft Blue (RA-05 recolour) | 20.89 to 24.99 | `adkit/analysis_card.py`, the same man's result |
| L2 | 2 of 3 / Built Around Foods You Like | 24.99 to 29.03 | lower third |
| F1 | MEAL PLANS factory, square card, AI-GENERATED | 29.03 to 31.26 | A0017, square at x 440 |
| E1 | man savours steak, square card, AI-GENERATED | 31.26 to 33.30 | A0086 from 0.0 s, square at x 420 |
| L3 | 3 of 3 / With You At Every Meal | 33.30 to 35.57 | lower third |
| M1 | meal photo to macros, phone card | 35.57 to 39.01 | B0035: 0.4 s, 3.5 s, 4.0 s segments |
| K1 | goal picture on a lock screen, AI-GENERATED | 42.54 to 44.68 | A0074 |
| C1 | button "Tap The Button Below To / See Yourself With Abs" | 43.54 to end | HyperFrames glass button |

Insert coverage 38.5 % (gate minimum 38 %). If I5 is approved coverage rises to about 45 %.

## Next action (round 2)

1. Record Dan's reply; re-hash the files below before touching anything; build in `round2/`, serve on a new port
   (8818 is round 1, keep it).
2. Apply his picks: hook (B = `cp edl_spec_B.json edl_spec.json`, rerun from `s03_edl.py`, then remap `framing.json` by
   source time as round 1 did, re-plan), colour (`grade.json` filter to the picked LUT), shot size (`framing_choice.json`
   NEAR/FAR), voice (the mix file the render muxes).
3. AI motion only for the ideas he approves, from their approved frames (`round1/frames/I*-start.png`, `-end.png`).
   Ask the three sense questions of every take; frame strips of the first and last second. I1: the robot must walk to the
   chair, never appear. I5: the cutout tips over and lies flat, never vanishes. AI-GENERATED chip on each, clear of faces.
   Then show each moving in context and stop.
4. Analysis card: switch to the shared Soft Blue HyperFrames card once the RA-14 round 3 session has built it (Dan's 10-14
   standard). Until then the RA-05 recolour stays.
5. When nothing is pending, the full film: 9:16 master, then the 16:9 from the same edit (`ra01lib.Aspect("16x9")`),
   then everything round 1 did not do: frame-lock the mix to the picture, `s04b_holdstart.py`, the land-then-hold check
   (`cut/landing.py motion_stats`), `piccuts.py decide`, `junk.py` on the final cut, `roll_sidecar.py mark-used`, the
   edit sheet for the 16:9, `audio_gate.py` with the A/B clip on the delivered file, `deliver/gate.py --format
   ad9x16|ad16x9`, the watch pass, one fresh independent reviewer (`ra-reviewer`), the negative-imagery scan, REVIEW 540p
   copies, notes, delivery folder `Claude Ad Videos/never pay a nutritionist again - RA-15/`, a copy in `Videos to Review/`,
   `queue.py set RA-15 delivered` plus the artifact db, clip library `add --used-in "RA-15"` for new AI clips.

## Traps found in round 1

- The +3 dB bass lift fails the audio gate's tone row on this roll (the fitted EQ already lifts the lows); RA-14's approved
  `mix_bass.wav` also fails it (2.55), though its handoff said PASS.
- The macro phone card at 574 wide ran to y 1583, into the caption band; 480 wide ends at 1376 (`gfx15.py` asserts it).
- The museum plaque sat under the opening caption in a full-height window.
- `s08_audio.py` with `LOCK=` hung on a saturated machine in RA-05; round 1 here muxed with `-shortest` (mix 16 ms longer).

## Files (work folder `/Volumes/Extreme/_edit_work/ra15/`, sha256 first 16)

| file | sha256 | what |
|---|---|---|
| `round1/DRAFT - RA-15 round 1 - first 31 seconds.mp4` | cc4483d20ab0cdf2 | what Dan reviews (31.27 s) |
| `draft_9x16.mp4` | 1cda66febbbf799b | internal full 9:16 draft, 51.18 s, not shown to Dan |
| `cut.json` | a3ae9f29629a1dd5 | 50.35 s of talk + 0.85 s end hold, 15 pause cuts |
| `edl_spec.json` / `edl_spec_B.json` | 1e5e64eada89e7f5 / fc8691c067d1e728 | take maps, hook A / hook B |
| `tx/c1668.whisper.json` | f5d4533469b4def5 | merged, corrected word list |
| `words_aligned.json` | 733e5141011e10b3 | 164 words, CTC aligned |
| `framing.json` | 3bb8d028900a271a | head and hair track, 245 samples, remapped to this cut |
| `beats.json` | a182643842594678 | cards, holds, lower thirds, button, AI idea slots |
| `grade.json` | cd54130dda466616 | C2 for this roll (not his pick yet) |
| `framing_choice.json` | cd313c42f3439553 | F2 and the options (not his pick yet) |
| `mix_bass15.wav` / `mix_bass.wav` / `mix.wav` | 6cdf0898274c6471 / c05a8be1bdd1973b / e2235bc49802f83e | V1 / V2 / V3 |
| `colour/luts/ra15_C1/C2/C3*.cube` | 7a2cc0a720ac27c6 / 1f78063a62b4e800 / e42207e8bd5bcbfc | the three looks |
| `hf9/manifest.json` | ce79e4d677b8c163 | lower thirds and button |
| `round1/index.html` | 25abd425a3ca7069 | the review page |
| `round1/frames/I1..I5-start/end.png` | I1 3a0b07a0701d3918 / 13fc38f400743063, I2 7916bf8ec21fac74 / ac34d3ebea3ef580, I4 4367184f1a882c14 / a0266def042a31fd, I5 77a55370f59b026c / 09742a16788e20cc | AI idea frames (Codex, $0) |

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Never Pay Nutritionist AD R2`. Read `Handoffs/handoff-20261014-ra15-nutritionist-round2-after-dan-review.md`
> and `.claude/skills/ad-edit/reference/ra15/README.md`, then continue RA-15 "Never Pay A Nutritionist Again" with /ad-edit.
> My answers to the round 1 page are: [paste the reply box]. Record them word for word first. Apply my hook, colour, shot
> size and voice picks, make the motion for any AI clip I said yes to from its approved frames and show it to me moving in
> context; if nothing is pending, build the full 9:16 and the 16:9 from the same edit, run every gate and the independent
> review, deliver, and send me the review copy. Use the Codex subscription to generate the images.

**Recommended model and effort: Opus 5.5, high.** A bounded revision plus a recipe-backed full build with gates.
