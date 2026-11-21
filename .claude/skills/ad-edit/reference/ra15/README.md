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

## Round 3: the full build, both masters (2026-10-14)

Dan's round 2 answer: `round3-plan/decisions.json` in the work dir (the three AI clips approved; the macro card shows the salmon meal B0038).
Scripts: `round3/` here (work-dir copies of everything that changed). Order:

| # | command | makes |
|---|---|---|
| 1 | `HEAD_SRC=72.06 EDGE_OVERRIDE="R2.end=121.92,R3.start=122.2469" python3 s03_edl.py` | `cut.json` with "twice" back in (lesson 13) |
| 2 | `round3/r3_twice_a.sh` | cut audio, V2 chain (same EQ), CTC words, head track, hold starts (incl. the end hold), plan |
| 3 | `round3/s_analysis.py` | the Soft Blue HyperFrames analysis card, 9:16 and 16:9 |
| 4 | `round3/r3_twice_b.sh` | `gfx15.py`, `gfx16.py` (16:9 via `hv16.py`), cards both shapes, captions, pictures, frame-locked mix, masters |
| 5 | `round3/r3_measure.sh KEY master`, `s20_neg.py`, `round3/s_chips15.py`, `round3/s_gateplan15.py KEY master` | CTC + Whisper + junk on the delivered file, chips, gate plan |
| 6 | `watch.py` + judge, `gate.py --format ad9x16 / ad16x9`, `round3/s_sheet15.py <16x9 master>` | stamps, edit sheet |

13. **A word Whisper times early can be cut as "a mouth noise".** Round 1's take map dropped "121.4-121.8, a mouth noise after
    'twice.'": it WAS "twice" (envelope 121.42-121.87; an isolated medium.en pass hears " twice."). Whisper on the delivered file
    heard "sees you start with a picture" for two rounds and nobody read it. Before calling a span junk, transcribe it ALONE, and read
    the delivered-file transcript against the script line by line. The independent reviewer caught it.
14. **A clip with no frames left is never slowed or held to fill a slot.** "twice" added 0.62 s and I5 take 1 ends at frame 143, so
    the cutout card keeps its length and Dan says "twice." on camera (0.64 s, NEAR) before the lock card.
15. **B0038 carries its own drawn phone bezel.** Crop it to the screen (538x1016 at 18, 32) and let the media-card plate be the only
    frame; the plate's 44 px corner radius covers the recording's ~22 px screen corners. 640 wide ends at y 1376.
16. **`s04b_holdstart.py` copied from RA-14 still imported RA-14's `ra01lib` (its roll)**; point it at the job's own lib. RA-15's
    planner never read `framing_holdstart.json` until round 3, and nothing sampled the END HOLD, so the last second's crop could not
    follow him (his elbow left the frame). `s04b` now samples the end hold every 0.1 s.
17. **Land-then-hold on this roll took four renders to get right; the answer is three settings together.** RA-14's 170 px/s with a
    20 px band panned 163 px un-eased (judge: "a camera operator hunting"); 70 px/s with a 52 px band was smooth but left him 12 %
    off centre with an arm off the edge. What passed: (a) `TRACK=170,20,8` (standard band, Gaussian ease 8 frames, landing frame
    pinned: peak acceleration 200-300 px/s2 against 1,900); (b) the tracker follows his BODY (`s04c_body.py`: person-mask extent
    from hair to waist, arms included) clamped to 8 % of the crop width of his head; (c) `LEVELS` gives the WIDE size to the holds
    with the biggest gestures, keeping the alternation on every uncovered join. Measure with `round3/s_edgecheck.py` (frames where
    his body touches one side while the other has room): 16/18/29 down to 6/12/11.
18. **16:9 from a 9:16-first build.** `hv16.py` loads `vertical.py` at 1920x1080 (as `square.py` does); lower thirds land on the
    approved 16:9 box (bottom 1016), so captions LIFT whole lines above them (`s07_captions.py` 16:9 block); a line that starts in a
    card and runs into a strip is clipped at the strip's first frame, a lifted line that runs into a card at the card's; a line that
    can do neither (LT2 into the fridge card) ends the strip a frame before it. Vertical clips go full height (852 px) in a
    media-card plate with the chip beside the hole.
19. **`framing:no_wide_level` on a portrait roll in 16:9.** His head is 270-296 px here, so 2144x1206 / 1888x1062 read 22.6-26.6 %
    (needs 27 %). FAR 1696x954, NEAR 1504x846 (`ra01lib.Aspect("16x9")`).
20. **The 16:9 CTA goes where his arms are not, measured on the delivered picture.** Bottom left (RA-01's spot) worked at the wide
    windows and failed at the tight ones (arm inside the box on 53 of 66 frames); upper left beside the shoulder (x 60-641, y 296-416).
21. **The shared edit-sheet writer's ad path is RA-01's** (every card Dan with physique, adkit graphics); `round3/s_sheet15.py` writes
    the same schema from this build with the real people / physique / labels. `validate.py` now accepts `analysis-card`.
22. **`buildcap.wait()` crashed on a process with an empty command line and the caller ran unthrottled** (fixed in `_shared`).
23. **A concat-demuxer caption track drifts a frame.** Per-state PNGs at `duration 0.033367` put a held caption one frame onto
    the next card (35.536 s); `s07_captions.py` now pipes one RGBA frame per output frame from `frame_state`.
24. **Look at the whole 16:9 frame of a 16:9 clip you only ever showed through a 9:16 window.** A0016's first 6 frames show a boy
    who vanishes and walks back in, outside the 9:16 window; the 16:9 starts the clip at 0.25 s. A0074 carries a screen glare from
    2.17 s: use 0.0-2.13 s.
25. **The shared analysis card's band defaults to "YOUR WORKOUT PLAN"**; in a nutrition ad set `band` to "YOUR NUTRITION PLAN".
26. **A scrolling app screen needs a crop per segment** (`segs` may carry their own crop): the B0049 generating screen scrolls, so
    one crop sliced its text at the top in one part and the bottom in another.
27. **In the 9:16 the CTA must not build over an AI picture of Dan** (the lock card): it starts as the card ends.

## Round 4: the cardboard cutout out, Dan on camera (2026-10-16)

Dan's round 3 answer: everything approved except the cutout card ("That clip didn't really land"); use a camera scene. Scripts: `round4/` here
(work-dir copies). Order: delete the `cutout` entry in `s05_plan15.py` (the 41.742 pause splice then splits the span into two holds, so
`LEVELS` has 10 entries: `...NEAR,FAR,NEAR,NEAR,FAR`), `s04b_holdstart.py beats.json`, `s04c_body.py`, `s05_plan15.py`, then `gfx16.py` (the
16:9 manifest drops the cutout plate), `s07_captions.py` and `s10_render05.py` both shapes, mux with the unchanged `mix_bass_r3c.wav`.
Cards, graphics and audio are not rebuilt (their frame counts did not change).

28. **Two holds in a span that had been one card: the size alternation decides which is wide.** Body width in the span is 650-680 px
    against a NEAR crop of 594, so a NEAR hold touches an edge; the short (1.4 s) hold gets NEAR, the 2.7 s hold FAR. Checked with
    `round4/s_edgecheck.py`: 0 touches in the FAR hold, 4 frames in the NEAR one (the same as round 3's "twice" shot).
29. **`Interrupted system call` on the external drive killed two long steps** (`s04c_body.py` at frame 2278, `gfx16.py` on an ffprobe).
    Retry the step; `s04c_body.py` now retries each read.
30. **A watch-pass judge may list the macOS `._sheet_*.jpg` resource-fork files instead of the sheets**; rename the entries before `--judge`.
31. **The delivery gate's framing rows count 9 of 10 holds** here (both independent reviewers measured the skipped one by hand); not a build fault.
