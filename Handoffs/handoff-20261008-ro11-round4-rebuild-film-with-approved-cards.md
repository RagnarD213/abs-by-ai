# Handoff: RO-11 round 4, rebuild the full film with the approved section cards and deliver (2026-10-08)

**CONTENT, long-form (LFC).** Task name: `Calories Don't Matter LFC R4`. Recommended: Claude Opus 5.5, effort high.
A long-form content video gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version here.
Round 3's handoff (`handoff-20261008-ro11-round3-section-cards-with-pictures.md`) is executed and deleted; it is in git history.

**Ready to fire. Dan answered the round 3 page on 2026-10-08. Nothing is waiting on him.**

**Goal.** Put the seven approved section cards into RO-11 "When Calories Don't Matter For Fat Loss" in layout B, add the
0.7 s end hold, rebuild the full film once, run every gate and one independent review, deliver, and replace the copy in
`Videos to Review/`.

**Dan's words (2026-10-08, after the round 3 page).** *"All right, these are all looking good. All the pictures are
approved, and let's use layout B. And let's add that extra 0.7 seconds at the end, as you recommend."*
Recorded with fingerprints: `/Volumes/Extreme/_edit_work/ro11/round4-plan/decisions.json`.

**The three decisions.**
1. **Layout B (`bleed`) on all seven cards.** The picture runs to the top, right and bottom edges and fades into the
   blue field on its left; the label sits on the picture. Claude had recommended A; he chose B. Do not reopen it.
2. **All seven pictures approved as shown**, with their crops and labels:

| ID | picture | source | label | label position in B |
|---|---|---|---|---|
| T1 Sleep | Dan asleep on the pool lounge chair | `photos/finalized social media photos/photo-21_FINAL_PRIMARY.jpg` | Real picture | top right, above him |
| T2 Alcohol | our AI image of Dan holding a beer | `social media graphics/youtube/thumbnails/Can You Drink Alcohol And Still Have Abs/_build-2026-10-05/assets/ai_dan.png` | AI-GENERATED | top, left of his head |
| T3 Hormones | gloved hand holding two blood tubes | Pexels 4040557 | none | |
| T4 Meal Timing | wall clock made of forks and spoons | Pexels 10755460 | none | |
| T5 Protein | salmon, steaks and eggs on a board | Pexels 5463890 | none | |
| T6 Exercise | Dan lifting a kettlebell | `photo-29_FINAL_PRIMARY.jpg` | Real picture | top right, above his head |
| T7 Daily Movement | man walking a park path | Pexels 17944685 | none | |

3. **End hold approved:** add about 0.7 s of his smile after the last word.

**What exists.** Review page http://127.0.0.1:8871/ (folder `round3/`). Approved stills `round3/stills/<ID>_bleed.jpg`.
Prepared crops `assets/titles/<ID>_bleed.jpg` (and `_frame.jpg`, now unused). Sources, fingerprints, crops and what was
passed on: `round3/sources.json`. Code: `recipe/gfx.py title_card(..., photo, label, layout, chip)`, `recipe/titles.py`
(sources, crops, label positions, `prep`, `measure`), `recipe/round3.py`, `recipe/page3.py`; the same files are in
`.claude/skills/longform-edit/reference/ro11/`.

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/longform-edit/reference/ro11/README.md` (the full-film order and traps, and the round 3 section).

**Locked. Re-hash before starting.** Work dir `/Volumes/Extreme/_edit_work/ro11/`.
- Round 2 film `round2/RO11_MASTER.mp4` sha256 `34cea69f4afb38a657b2648dad331096d17e657b2b92ed3f3f00a20feb5b598b`.
- `plan_resolved.json` `9361ab4ef74c5a52f9718857811b979f2cff61424d83625a7d020fe36a71c8be`,
  `hf/manifest.json` `dd75eba5da3eff8352c4fb094095c48c7e9a68facfce63f79861b4f51f020038`,
  `edl.json` `30470add8db2af1905d9dd02bf3c7808e114c56fe3b07517b4d5672a212c6eb6`,
  `shots.json` `1e22e21f2aec7da187f82e72e14cc4e353d123db65897a34576a9b6197533944`,
  `aiframes/C_motion_v2.mp4` `3b48ec734644f288a785ac0b241db3717fe1e6ea30087a52621701600206f69b`.
- The seven approved B stills and their prepared crops: fingerprints in `round4-plan/decisions.json`.
- Everything in the film except the seven cards and the tail, and on the cards the words, their size and their times.
- Rounds 3 and this handoff changed none of the files above.

**Next action (in order).**
1. Rename the task. `queue.py set RO-11 in_progress --by Claude --editor Claude`, mirror it, board entry. Re-hash the
   locks, including the seven prepared `_bleed.jpg` crops.
2. Layout B in the plan: on the seven title items in `recipe/plan.py` add `layout="bleed"`, and on T1, T2 and T6 the
   `chip` from `titles.TITLES` (T1 `((1866, 54), "rt")`, T2 `((1255, 54), "rt")`, T6 `((1866, 40), "rt")`). `photo` and
   `label` are already there. Do not change a crop or a label position: he approved them as shown.
3. Run `resolve.py`, then diff the new `plan_resolved.json` against the locked one: only `photo`, `label`, `layout` and
   `chip` on T1 to T7 may differ, and no time may move. Record the new hash.
4. End hold: the last shot is `end.0`, src 25223 to 25619, out 17532 to 17928; he holds the smile to src 25651. Extend
   it by 21 frames (to src 25640, out 17949). `shots.json` is written by `shots.py` from `edl.json`: make the change
   at its source so a re-run keeps it, then confirm only that shot's end moved and no graphic time changed. Check the
   added tail by eye (he keeps smiling, no blink into a reset) and by ear (room only, no breath or click). Record the
   new hashes.
5. Before the full render, check the six B cards he saw only as stills (T2 to T7) moving: render each with
   `round3.py`'s `contextB` path into `round4/`, read the entrance frames (picture and label fade in together inside
   0.5 s, the left edge fades cleanly into the field, nothing covers the headline). This is an internal check, not a
   question for Dan.
6. Copy `hf/renders` aside. Nothing in the HyperFrames scenes changed, so do not run `from_plan.py --render`.
7. Build in a new `round4/` folder; never overwrite `round2/` or `round3/`. Order: `build.render_range` on the whole
   film (13 min), `finish_chain.sh`, own negative-events scan, one `ra-reviewer` that writes `logs/findings.json`,
   `watch.py --judge`, `finish.py` again, the delivery gate (25 min), `deliver.sh`.
8. Gate plan: `finish.py` already lists every item that has a `label`, so T1 and T6 land in `real_photos` and T2 in
   `ai_inserts` on their own. It locates each chip at the card's midpoint; the labels row needs 0.85 or better. In B the
   chip sits on a picture, not on the field: if a match scores low, look at the frame before touching the gate.
9. Deliver to `claude edited long form content/11 - When Calories Don't Matter For Fat Loss/`, update `notes-RO11.md`,
   replace `Videos to Review/Calories Don't Matter LFC R2 - full film.mp4` with the round 4 file (named
   `Calories Don't Matter LFC R4 - full film.mp4`), open the folder, and give Dan the file name and a short page.
   Per the later-round rule the page shows only what changed: the seven cards in the film, and the ending.
10. After Dan approves the film: register the opener clip, the used Pexels clips and the four Pexels stills in the clip
    library. When he finalizes it, delete the `Videos to Review` copy and remove the review services (port 8871 and
    round 2's).

**Not done yet (do not claim).** `plan.py` does not carry `layout` or `chip` yet. `plan_resolved.json` has not been
re-resolved. The end hold is not applied. T2 to T7 in layout B have not been rendered moving. The film is not rebuilt.

**Checks already made in round 3 (reuse; nothing changed since).** A card with no picture draws pixel for pixel as the
round 2 code did. Label clearance from Dan in layout B, measured with the person outline: T1 35 px, T2 17 px, T6 50 px.
No stock source repeats one of the 12 clips or 7 fact-card photos. Hair is whole on T1, T2 and T6 at the end of the
slow push. `tmp_base.mp4` in the work dir was overwritten by the round 3 clip renders; it is scratch and the full
render rewrites it.

**Known and approved.** G20 reads -211 px at 9:15.25 (his hands pass under the card).

**Spend.** About $3.50 of the $5 cap, all before round 2. Round 3 spent $0. Round 4 needs no generation.

**Open risks.** T2's AI image has about 12 to 15 px above the hair at the end of the push in B: measure it on the
rendered film, and if hair touches the edge, start that card's push smaller rather than re-crop. The bright stock
pictures (T3 tubes, T5 food) fade from a pale background into navy: look at the fade edge moving.

**Starter prompt (Claude Opus 5.5, effort high):**

Name this task `Calories Don't Matter LFC R4`. This is CONTENT (long-form). Read and execute
`Handoffs/handoff-20261008-ro11-round4-rebuild-film-with-approved-cards.md`. I approved all seven section-card
pictures, chose layout B, and want the extra 0.7 seconds of my smile at the end. Rebuild the full RO-11 film once with
those changes, run every gate and one independent review, deliver it, and put the new file in `Videos to Review`.
