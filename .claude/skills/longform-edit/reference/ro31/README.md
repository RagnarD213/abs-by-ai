# RO-31 "How To Get Rid Of Man Boobs" (10/15 C1775): round 1 recipe (Claude Opus 5.5, 2026-10-31)

Same 10/15 studio set as RO-28 and RO-29. Start from `../ro29/` (round 2 recipe) and `../ro28/`; only what differs is kept here. Work dir
`/Volumes/Expansion/_edit_work/RO-31/round1/`. One roll, 5:56 raw, cut to 3:52, 15 pieces. Never commit media.

## Traps this round paid for
1. **The sidecar's `small` transcript hides restarts.** It printed one clean line where he stopped and started again: On Zepbound (a whole sentence),
   "Then track" (a third read), "So don't assume". Run medium.en on the roll before writing the EDL, then read medium.en on the ASSEMBLED voice:
   three more surfaced there ("If you want a diag-", "The second step is", "Push-up"). The tell on the assembled words is one word over 1.5 s.
2. **Confirm a restart with a Gemini listen on 4 s clips** (`GM=gemini-3.1-pro-preview gemini_listen.py`; gemini-2.5-pro now returns 404). Whisper base and
   small both print the clean sentence. Use `recipe/env.py` level strips for the edges.
3. **Codex refuses anatomy of a chest.** "The image tool rejected the medical illustration request." Do not reword around it: the diagram is SVG inside a
   HyperFrames scene (`chest/`), no AI label, and every part can animate.
4. **A side view of a chest alone reads as a woman's breast**, twice, even shallow. Draw the whole man in profile (head, neck, stomach running on past the
   chest with no fold under it). An independent reviewer caught the second version; the eye of the person who drew it did not.
5. **`stills.py` opens `aiframes/<id>-start.png` for kind "ai"** through `ai_placeholder`; a blind-test round has no such files. Point stills at `review/aiframes/<id>/X1.jpg`.
6. **(Superseded 2026-11-05: Dan now sees START and END together from the first step, VIDEO-RULES top.) Blind pairs, START only:** `blind.py build` refuses a set with one source. An idea whose other frame was refused or failed twice goes on the page as a plain
   X1 copy. End frames wait for the pick, so the frame gate cannot run in round 1: one fresh frame-reviewer over all the start frames instead.
7. **`review/options/` must exist** before `colour_options.py`; its failure is silent inside the chain and the page breaks later.
8. **Probe a library clip against its slot before the chain** (A0050 is 3.06 s; the assert killed the context pass at item 15). `chain_r1.sh` reported CONTEXT done with only 15 of 39.
9. **Library clips carry readable gym names:** the 10/23 gym's wall logo and a Jacob's Ladder show in the front and side chest-fly clips (B0665 to B0667), and the camera moves, so a crop will not hold. B0668 (low angle) is clean.
10. **B0546 reads neon orange in low sun.** `eq=saturation=0.72:brightness=0.015,colorbalance=rm=-0.07:gm=-0.01:bm=0.03`.
11. **A0077's T-shirt vanishes after about 2.2 s.** Use only `max_len=2.1`.
12. **Side card over a take join:** cover the part before the join with a clip and start the card on the join (C08 then P01).
13. **Lower third hold:** measure 1.5 s after the LAST part lands, not after the first. `over_full=True` lets one ride onto the next clip.
14. **The board can be full of other sessions' entries.** It stood at 2,498 of 2,500 words; a three-word entry is what fit.

## Round 2 (2026-11-04): AI frames only
15. **Codex's image tool refuses man boobs** as "sexual content" (opener, bodybuilder gynecomastia). Do not reword; Google Flow drew them.
16. **Google cannot draw a bodybuilder with gynecomastia:** five tries gave hard pecs, a puffy nipple at most, or a logo tank instead of bare chest.
17. **A prop that leaves the hand changes shape between START and END** (the juice jug, six tries across both models, even building START backward from END). Use stock for that kind of line.
18. **Reviewers' common catches:** a mirror reflection looking the other way, fake embossed fabric (Codex), letter-like marks on a wet shirt, a hanger through the shirt, a shirt from nowhere, a belly-centred END.
19. **Specs with `may_change` everything make the gate a formality** (RO-29 trap 18): the fresh reviewer is the check. `require_pass` raises SystemExit, so catch BaseException when building a page that skips failed pairs (`page_r2.py`).

## Round 3 (2026-11-04): motion, stock, full film
Work dir `round3/` (recipe copied from round1 with paths swapped; heavy inputs symlinked; `hf/` cloned with `cp -c`). Plan: the R3 block at the bottom of `recipe/plan.py`.
20. **Fresh reviewers failed 9 of 12 motion takes that passed `clipcheck.py`.** The gate only tracks things vanishing; faces, mirrors and acting are the reviewer's. Budget three Flow rounds for any clip with a person reacting, and screen every take yourself first with face/hand strips every 0.25 s (`ai/strip.py`): only send a reviewer the take you would ship.
21. **Mirror scenes break once a hand reaches for something** (A5, A7): the reflection moves an arm the foreground man does not, or the face changes identity while the head is down. Use the clean part before the reach and shorten the slot (A7 now ends on "they cause"; the lower third keeps running).
22. **A seated reaction with a shirt tug always ends on the belly** (A2: 13 takes): the shirt lifts, hands pinch, or a prop vanishes from a waving hand. Do not write "tugs his shirt down" for a heavy man; pick an action with no hands on the stomach.
23. **"Small closed-mouth smile" still gives toothy grins and eyes-shut savoring** (A5, 13 takes). Veo and Omni both. Mild reactions of strangers are the hardest kind of AI clip; offer fewer of them.
24. **Pexels has no "juice poured down a sink" clip** (about 25 searches). Liquid-calorie lines: one drink per spoken word (`stock/build_j1.py`, cuts on the word times, per-clip grades in `stock/grades.json`), crop away brand text (the whipped-cream can).
25. **Omni twins fit 4 s slots whole but failed review more often than Veo windows here** (faces and hands); keep queueing both.
26. **Voice without the between-words expander:** `build.py` passes `--no-expander-because` (the round 1 first minute failed the artifacts row on gap pumping).

## Round 4 (2026-11-05): Dan's note on the chest diagram, then judge passes
Dan: "For the fat, make the man boob smaller and give him a small belly beneath that... everything just bulges out evenly." Words: `round4-plan/decisions-r3.json`.
27. **Anatomy of the fat figure:** a thin layer at the collarbone, a small rounded chest mound with the nipple at its front, a soft crease, then a modest belly about level with the chest (`round3/recipe/chest/chest-diagram.template.htm`, BODY.fat and FATIN). A first redraw still read as a breast (straight slope from the neck to the nipple) and the gland disc poked out of the body: a fresh reviewer caught both. Keep the gland disc inside the outline, behind the nipple; labels sit on the part they name.
28. **`recipe/chest/*.py` carries its own W path:** copying a recipe and swapping paths in `recipe/*.py` missed the subfolder, so the first render wrote round 1's folder.
29. **Each fresh watch-pass judge found one new AI-clip fault the last one missed** (library A0077: shirt slides off without passing the head, then the head passes back through the shirt; A0166: a pen appears in an empty hand). Decode every AI clip in full at playback order before the first judge, and tell the judge to block only on what shows at normal speed and list frame-only items as BORDERLINE; otherwise every pass costs an hour's rebuild.
30. **A clip boundary can land on a tongue-on-lip frame** (0:56 after D02): extend the card's tail a few frames.
