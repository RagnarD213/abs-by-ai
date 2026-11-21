AD (paid ad: it ends on "Tap the button below"). Sidebar name for the next task: `Never Pay Nutritionist AD R2`. Dan's round 1 answers are in (2026-10-14).

# RA-15 "Never Pay A Nutritionist Again": round 2 (Dan's round 1 picks applied; AI clip motion)

**Written 2026-10-14 by the round 1 session (Claude, Opus 5.5).** Job doc: `Handoffs/video-editing/RA-15-never-pay-a-nutritionist-again.md`.
Rules: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `/ad-edit`, `_shared/PRE-RENDER-APPROVAL.md`.
Recipe: `.claude/skills/ad-edit/reference/ra15/` (README: stage order and seven lessons), on top of `../ra05/` and `../ra04/`.

**Dan answered the round 1 page on 2026-10-14.** His words, verbatim, with hashes per item:
`/Volumes/Extreme/_edit_work/ra15/round2-plan/decisions.json`.

> "Hook A, C2, F2, V2, yes to all four ideas except for the cleared-out idea, I want to keep the nutritionist museum clip
> there. Everything else, you can go ahead and generate, keep both give me the handoff for the next round of edits."

## What Dan picked

| item | pick | state in the work folder |
|---|---|---|
| Hook | **A** "Nutritionists have gone obsolete. AI just took their job." | already the cut (`edl_spec.json`, `cut.json`) |
| Colour | **C2** brighter, golden skin (re-baked for C1668, exposure 2.0) | already `grade.json` |
| Shot size | **F2** close 594x1056, wide 738x1312 | already `framing_choice.json` |
| Voice | **V2** +3 dB at 120 Hz, `mix_bass.wav` | ⚠ round 1 muxed `mix_bass15.wav` (V1). Every mux from now on uses `mix_bass.wav`. Its tone row fails (max 2.90 dB): the known mismatch of the bass standard (VIDEO-RULES 2026-10-12), recorded in the notes, never tuned away |
| I1 Cleared out | **No.** Keep library A0016, the museum gag, in the opener | as round 1 |
| I2 Chicken and broccoli forever | **Yes, motion authorized** (replaces A0017 at 29.03 to 31.26) | frames `round1/frames/I2-*.png` |
| I4 Ask it what to order | **Yes, motion authorized** (37.07 to 39.01; the macro screen keeps 35.57 to 37.07) | frames `round1/frames/I4-*.png` |
| I5 The cardboard nutritionist | **Yes, motion authorized** (39.01 to 42.54, now Dan on camera) | frames `round1/frames/I5-*.png` |
| Claim lines | **Keep both** as spoken (captions only) | as round 1 |

Everything else on the round 1 page drew no note and stands as shown. Round 1 page: http://127.0.0.1:8818/ (keep it).
Queue state: `in_progress`. Spend: $0 of $10. Nothing is gated, delivered or uploaded yet.

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

## Round 2 deliverable: the three AI clips moving in context, then stop

Build in `/Volumes/Extreme/_edit_work/ra15/round2/`; serve on a new port (8818 is round 1, keep it).

1. Re-hash the files below against this table before touching anything.
2. **Motion for I2, I4, I5** from their approved frame pairs, 9:16, about 4 to 5 s each (the slots are 2.2, 1.9 and 3.5 s).
   Method: `longform-edit/reference/ro06/gen_motion.py` (motion from a frame pair, as RO-06 and RA-14 did). Ad cap $10 for
   the whole ad, retries included; state the estimate before each batch and keep a running total. No lip sync (nobody
   speaks). Prompts describe only the action between the two frames; nothing appears or vanishes.
3. **Check every take before Dan sees it** (VIDEO-RULES 2026-10-13): the three sense questions per clip, the measured
   first-versus-tenth-frame self-change map with the people masked (`longform-edit/reference/ro08/a5_cut.py`), and frame
   strips of the first and last second. I2: his hand opens the door and the containers are there from the first frame of
   the open fridge; nothing grows or melts. I4: menu down, phone up, finger points, waiter writes; no readable text appears.
   I5: the cutout tips over and lies flat on the floor; it never vanishes or bends. A take that fails is regenerated, cut to
   the part that works, or dropped back to the round 1 picture, never sent with the fault described. At the cap with
   problems left, ask Dan for more budget, first line of the message, with the number.
4. Place each in its slot (`s05_plan15.py` CARDS: `fridge` replaces `factory`; `restaurant` splits `macro` at `t_eat`;
   `cutout` 39.01 to 42.54). Fill the 9:16 frame; AI-GENERATED chip placed by looking at the people. Re-run the plan: the
   inside-hold splice assert must still pass (the cutout removes the 0.8 s hold at 41.74).
5. Rebuild inserts and the 9:16 render, mux with `mix_bass.wav`. Page: the three clips each moving in context (3 s either
   side), stills of anything that changed, a short "What I decided", only real questions. Then stop and write the round 3
   handoff.
6. Round 3 (after his OK on the motion): the full 9:16 master, then the 16:9 from the same edit (`ra01lib.Aspect("16x9")`),
   and everything owed before delivery: frame-lock the mix to the picture, `s04b_holdstart.py`, the land-then-hold check
   (`cut/landing.py motion_stats`), `piccuts.py decide`, `junk.py` on the final cut, `roll_sidecar.py mark-used`, the edit
   sheet for the 16:9, `audio_gate.py` with the A/B clip on the delivered file, `deliver/gate.py --format ad9x16|ad16x9`,
   the watch pass, one fresh independent reviewer (`ra-reviewer`), the negative-imagery scan, REVIEW 540p copies, notes,
   delivery folder `Claude Ad Videos/never pay a nutritionist again - RA-15/`, a copy in `Videos to Review/`,
   `queue.py set RA-15 delivered` plus the artifact db, clip library `add --used-in "RA-15"` for the new AI clips. The
   analysis card switches to the shared Soft Blue HyperFrames card once RA-14 round 3 has built it.

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
| `grade.json` | cd54130dda466616 | C2 for this roll, Dan's pick |
| `framing_choice.json` | cd313c42f3439553 | F2, Dan's pick (options kept for the record) |
| `mix_bass.wav` | c05a8be1bdd1973b | **V2, Dan's pick** (`mix_bass15.wav` 6cdf0898274c6471 and `mix.wav` e2235bc49802f83e are the unpicked V1 and V3) |
| `colour/luts/ra15_C1/C2/C3*.cube` | 7a2cc0a720ac27c6 / 1f78063a62b4e800 / e42207e8bd5bcbfc | the three looks |
| `hf9/manifest.json` | ce79e4d677b8c163 | lower thirds and button |
| `round1/index.html` | 25abd425a3ca7069 | the review page |
| `round2-plan/decisions.json` | see file | Dan's answers, verbatim |
| `round1/frames/I1..I5-start/end.png` | I1 3a0b07a0701d3918 / 13fc38f400743063, I2 7916bf8ec21fac74 / ac34d3ebea3ef580, I4 4367184f1a882c14 / a0266def042a31fd, I5 77a55370f59b026c / 09742a16788e20cc | AI idea frames (Codex, $0) |

## Starter prompt (paste into a fresh Claude Code session)

> AD. Rename this task `Never Pay Nutritionist AD R2`. Read `Handoffs/handoff-20261014-ra15-nutritionist-round2-after-dan-review.md`
> and `.claude/skills/ad-edit/reference/ra15/README.md`, then run round 2 of RA-15 "Never Pay A Nutritionist Again" with /ad-edit.
> My round 1 picks are recorded there (hook A, C2, F2, V2 voice, keep the museum opener, keep both claim lines). Generate the
> motion for the fridge, restaurant and cardboard-cutout clips from their approved frames, check each one for sense before I
> see it, put them in the ad with the V2 voice, and show me each clip moving in context on one review page. Then stop and
> give me the handoff for the full build. Use the Codex subscription to generate the images.

**Recommended model and effort: Opus 5.5, high.** AI motion with sense checks, a re-plan and a 9:16 re-render.
