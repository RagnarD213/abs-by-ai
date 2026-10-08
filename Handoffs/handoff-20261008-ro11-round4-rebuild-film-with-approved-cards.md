# Handoff: RO-11 round 4, rebuild the full film with the approved section cards and deliver (2026-10-08)

**CONTENT, long-form (LFC).** Task name: `Calories Don't Matter LFC R4`. Recommended: Claude Opus 5.5, effort high.
A long-form content video gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version here.
This replaces `handoff-20261008-ro11-round3-section-cards-with-pictures.md` (executed, deleted; in git history).

**Fire only after Dan has answered the round 3 page.** His reply goes in the starter prompt. Until then RO-11 waits.

**Goal.** Put the section cards Dan approves into RO-11 "When Calories Don't Matter For Fat Loss", rebuild the full film
once, run every gate and one independent review, deliver, and replace the copy in `Videos to Review/`.

**What round 3 built (all shown to Dan, none approved yet).** Page: http://127.0.0.1:8871/ (folder
`/Volumes/Extreme/_edit_work/ro11/round3/`, generator `recipe/page3.py`). Each of the seven cards T1 to T7 has a picture
on its right in two layouts: **A `frame`** (recommended: the fact card's rounded photo frame, 905 px wide, label under
it) and **B `bleed`** (picture to the screen edges, fading into the field, label on the picture). Seven moving context
clips in A, plus `T1B` in B.

| ID | picture | source | label |
|---|---|---|---|
| T1 Sleep | Dan asleep on the pool lounge chair | `photos/finalized social media photos/photo-21_FINAL_PRIMARY.jpg` | Real picture |
| T2 Alcohol | our AI image of Dan holding a beer | `social media graphics/youtube/thumbnails/Can You Drink Alcohol And Still Have Abs/_build-2026-10-05/assets/ai_dan.png` | AI-GENERATED |
| T3 Hormones | gloved hand holding two blood tubes | Pexels 4040557 | none |
| T4 Meal Timing | wall clock made of forks and spoons | Pexels 10755460 | none |
| T5 Protein | salmon, steaks and eggs on a board | Pexels 5463890 | none |
| T6 Exercise | Dan lifting a kettlebell | `photo-29_FINAL_PRIMARY.jpg` | Real picture |
| T7 Daily Movement | man walking a park path | Pexels 17944685 | none |

Sources, fingerprints, crops and what was considered and passed on: `round3/sources.json`. Stock originals:
`assets/titles/src/`. Prepared crops: `assets/titles/<ID>_frame.jpg` and `_bleed.jpg`.

**The three questions he was asked.** (1) Layout A or B. (2) The seven pictures: approved, or notes by card. (3) The
ending: add about 0.7 s of his smile after the last word, or leave it (recommendation: add; src frames 25619 to 25651).

**Read first.** `_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/longform-edit/reference/ro11/README.md` (the full-film order and traps, and the round 3 section).

**Locked. Re-hash before starting.** Work dir `/Volumes/Extreme/_edit_work/ro11/`.
- Round 2 film `round2/RO11_MASTER.mp4` sha256 `34cea69f4afb38a657b2648dad331096d17e657b2b92ed3f3f00a20feb5b598b`.
- `plan_resolved.json` `9361ab4ef74c5a52f9718857811b979f2cff61424d83625a7d020fe36a71c8be`,
  `hf/manifest.json` `dd75eba5da3eff8352c4fb094095c48c7e9a68facfce63f79861b4f51f020038`,
  `edl.json` `30470add8db2af1905d9dd02bf3c7808e114c56fe3b07517b4d5672a212c6eb6`,
  `shots.json` `1e22e21f2aec7da187f82e72e14cc4e353d123db65897a34576a9b6197533944`,
  `aiframes/C_motion_v2.mp4` `3b48ec734644f288a785ac0b241db3717fe1e6ea30087a52621701600206f69b`.
- Everything in the film except the seven cards, and on the cards the words, their size and their times.
- Round 3 did not touch any of these: it merged the photo fields in memory (`recipe/round3.py`).

**Next action (in order).**
1. Rename the task. `queue.py set RO-11 in_progress --by Claude --editor Claude`, mirror it, board entry. Re-hash the locks.
2. Record Dan's reply word for word in `round4-plan/decisions.json` (layout, each card, the ending), before changing anything.
3. Apply it. A picture he swaps: change that card in `recipe/titles.py` `TITLES`, then `titles.py prep <ID>` and
   `titles.py measure round4/checks/chips` (the label must not touch him; a real-photo label is 931 px wide and only
   fits under the frame or across the top above his head). Layout B: add `layout="bleed"` and the card's `chip` from
   `titles.TITLES` to the seven title items in `recipe/plan.py`. A new picture he has not seen goes back to him as one
   still before the film is built.
4. `plan.py` already carries `photo` and `label` on the seven titles. Run `resolve.py`, then diff the new
   `plan_resolved.json` against the locked one: only `photo`, `label` (and `layout`, `chip`) on T1 to T7 may differ, and
   no time may move. Record the new hash.
5. If he wants the end hold: extend the last shot in `shots.json` by about 21 frames from the roll (he smiles from
   src 25619 to 25651). It adds frames only at the tail, so no graphic time moves. Record the new hash.
6. Copy `hf/renders` aside. Nothing in the HyperFrames scenes changed, so do not run `from_plan.py --render`.
7. Build in a new `round4/` folder; never overwrite `round2/` or `round3/`. Order: `build.render_range` on the whole
   film (13 min), `finish_chain.sh`, own negative-events scan, one `ra-reviewer` that writes `logs/findings.json`,
   `watch.py --judge`, `finish.py` again, the delivery gate (25 min), `deliver.sh`.
8. Gate plan: `finish.py` already lists every item that has a `label`, so T1 and T6 land in `real_photos` and T2 in
   `ai_inserts` on their own. It locates each chip at the card's midpoint; the labels row needs 0.85 or better.
9. Deliver to `claude edited long form content/11 - When Calories Don't Matter For Fat Loss/`, update `notes-RO11.md`,
   replace `Videos to Review/Calories Don't Matter LFC R2 - full film.mp4` with the round 4 file (named
   `Calories Don't Matter LFC R4 - full film.mp4`), open the folder, and give Dan the file name and a short page.
   Per the later-round rule the page shows only what changed: the seven cards in the film, and the ending.
10. Register the clips and stock that made the approved film in the clip library (the opener clip, the used Pexels
    clips, the four Pexels stills) once Dan approves the film. When he finalizes it, delete the `Videos to Review`
    copy and remove the review services on ports 8871 and round 2's.

**Not done yet (do not claim).** Dan has not answered any of the three questions. No card is approved. The film is not
rebuilt. `plan_resolved.json` has not been re-resolved with the photo fields. The clip library entries wait for final approval.

**Checks already made in round 3 (reuse, do not redo unless a picture changes).** A card with no picture draws pixel for
pixel as the round 2 code did. Label clearance from Dan, measured: layout A 16 to 27 px (the label is outside the
picture), layout B 17 to 50 px. No stock source repeats one of the 12 clips or 7 fact-card photos. Hair is whole on
T1, T2 and T6 at the end of the slow push.

**Known and approved.** G20 reads -211 px at 9:15.25 (his hands pass under the card).

**Spend.** About $3.50 of the $5 cap, all before round 2. Round 3 spent $0 (no image was generated).

**Open risks.** If Dan picks layout B, six of the seven B cards were shown to him as stills only: check each one moving
(entrance, label fade) before the full render. T2's AI image has only about 15 px above the hair at the end of the push.

**Starter prompt (Claude Opus 5.5, effort high):**

Name this task `Calories Don't Matter LFC R4`. This is CONTENT (long-form). Read and execute
`Handoffs/handoff-20261008-ro11-round4-rebuild-film-with-approved-cards.md`. My answers on the round 3 section-card
page are: [paste your reply from the page here]. Record them, apply them, rebuild the full RO-11 film once with the
approved cards, run every gate and one independent review, deliver it, and put the new file in `Videos to Review`.
