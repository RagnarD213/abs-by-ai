# RA-15 "Never Pay A Nutritionist Again": rounds 1 and 2 (2026-10-14)

A 9:16 ad from portrait pool roll C1668 (72 to 131 s, one unbroken read of the whole script) on the RA-05 recipe.
Work dir: `/Volumes/Extreme/_edit_work/ra15/`. Only the files that differ from `../ra05/` and `../ra04/` are here.
Round 1 = the outdoor options page (colour, shot size, voice), four AI clip ideas as frames, every graphic and clip,
the finished first 31 s. Review page `http://127.0.0.1:8818/`. Handoff: `Handoffs/handoff-20261014-ra15-nutritionist-round2-after-dan-review.md`.

## Order

| # | command | makes |
|---|---|---|
| 1 | `pick_lav.py` on the roll, `s01_env.py` | lav pull (dual-mono), `env.json` |
| 2 | `replicate_words.js` on three overlapping pieces (8-53, 64-122, 112-138 s), then 8 s windows over the main take | word list; the windows are the hidden-restart check |
| 3 | `HEAD_SRC=72.06 python3 s03_edl.py` (PROTECT adds the beat after "One," "Two," "three,") | `cut.json`, 50.35 s of talk |
| 4 | `r1_chain_a.sh` | `mix.wav`, `mix_bass.wav`, `words_aligned.json`, `framing.json` (+ `mix_bass15.wav` by hand, below) |
| 5 | `s31_bake.py 1.5 2.0`, `r1_options.py` | the three looks for this roll, option stills |
| 6 | `s05_plan15.py` | `beats.json` |
| 7 | `r1_chain_c15.sh` then `r1_chain_d15.sh` | graphics, inserts, captions, 9:16 picture, sample, `round1/index.html` |

## What this ad taught

1. **One long take still hides a restart.** The big transcription pass read "Generate an image of yourself with abs" as
   one sentence; 8 s windows on Replicate (under a cent each, no build slot) heard "Generate an image of yourself."
   stop, a 1.3 s pause, then the restart. Window the whole kept take, not only the stretched words.
2. **Keep the beat after a spoken list number.** Cutting the 0.2-0.3 s pause after "One," "Two," "And three," put a
   splice 0.4 s after a take seam, and the plan then made three 0.4 s shot changes. `PROTECT` in `s03_edl.py` keeps them.
3. **Re-bake the approved look by face brightness, per roll.** C1668 reads about 0.2 stop brighter than RA-14's C1667:
   Dan's C2 at exposure 2.0 here (2.4 there) lands the face at 91.9 against RA-14's 91.7. Convert the approved shot sizes
   by his height in frame (person mask: 953 px vs 937), keeping the bottoms on the same body landmark.
4. **The +3 dB bass lift fails the tone row when the fitted EQ already reads full.** Lowest band without the lift was
   already +0.5 dB over the reference; +3 dB went to +2.9 and failed (RA-14's approved bass mix also fails it, 2.55).
   +1.5 dB passes every row. Offer it as the recommended option and the +3 dB as his RA-14 strength.
5. **A caption can land on a clip's punchline.** The museum gag's plaque ("Human Nutritionist 1985-2025") sat in the
   caption band in a full-height window. A 560x996 window from the top moves it below the captions.
6. **A 16:9 clip whose point needs both sides goes in a square card** (the factory's two signs; the steak man's face
   and plate). Write the reason on the page.
7. **Phone and square cards must end above y 1376**: B0035 at 574 wide ran to 1583; 480 wide ends at 1376.

## Round 2: AI motion in the ad (2026-10-14)

Dan's round 1 picks: `round2-plan/decisions.json` in the work dir. Round 2 page `http://127.0.0.1:8828/`. Handoff for round 3:
`Handoffs/handoff-20261014-ra15-nutritionist-round3-full-build.md`. Motion spend $3.00 of $10 (7 takes, 6 charged).

| # | command | makes |
|---|---|---|
| 1 | `round2/batch.sh "I2 I2-t1 4" ...` (calls `round2/gen_motion15.py`, prompts in `round2/motion-prompts/`) | Veo 3.1 Fast takes, 9:16, ledger with the $10 cap enforced |
| 2 | `round2/check15.py <take> [a b]` | numbered contact sheet, first/last-second strips, first-vs-tenth self-change map with people masked, cut spikes |
| 3 | `s05_plan15.py` | `fridge` replaces `factory`, `macro` ends at "Eating at a restaurant", `restaurant`, `cutout` |
| 4 | `round2/r2_chain.sh` (`SKIP_GFX=1 INSERTS=cutout` re-runs one card) | plates, cards, captions (`s07_captions15.py`), 9:16 picture, mux with `mix_bass.wav` |
| 5 | `round2/page15r2.py --media` | round 2 page |

8. **Veo cannot drop a rigid cardboard cutout.** Three takes (two start+end pairs, one start-only) all spun it to show its back,
   stood it back up, then laid it down. Fix with no new spend: the camera measured locked (scale 1.000, < 0.3 px) between the
   standing part and the landed tail, so the clip is two shots joined by a cut (frames 6-35, then 89-143), the fall never shown.
   An independent reviewer read it as "a moment later, she fell over". Check the camera with an ORB partial-affine fit before
   cutting a take to itself.
9. **Veo bakes hard cuts into a take** (I4 frame 11/12 and 29/30: the menu teleports flat). The frame-difference spike in
   `check15.py` finds them; start the used range after the last one. I4 take 1 also grew a disembodied arm and a second phone:
   name "the only phone in the scene" and "the waiter's hands never leave the notepad" in the prompt; take 2 obeyed.
10. **A take's first frames are the sharp input still, then softer and about 4 % brighter by frame 5.** A whole-picture glow in
   the first-vs-tenth map is that, not an object change; start the used range at frame 6 when the clip opens on a hard cut.
11. **Measure the AI chip against every person in every used frame** (`round2/chip_place.json`): the default top-left spot
   sat on the fridge man's head.
12. **The punchline can land in the caption band again** (lesson 5): the fallen cutout's face lay at y 1380-1550. Lines that
   START inside that card are lifted whole to y 1215 (`LIFTS` in `s07_captions15.py`), never mid-line.
