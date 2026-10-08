# Handoff: RO-11 round 3, a picture on the right of each of the 7 section cards (approval page only) (2026-10-08)

**CONTENT, long-form (LFC).** Task name: `Calories Don't Matter LFC R3`. Recommended: Claude Opus 5.5, effort high.
Use the Codex subscription to generate the images (only if nothing existing or stock fits).
A long-form content video gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version here.
This replaces `handoff-20261008-ro11-round2-build-full-film-opener-locked.md` (executed, deleted; in git history).

**Goal.** Redesign the seven full-screen section title cards of RO-11 "When Calories Don't Matter For Fat Loss" so each
has a picture on its right, show Dan all seven on one review page, and stop. **Do not rebuild the film this round.** The
full re-edit is round 4, after he approves the cards.

**Dan's words (2026-10-08, after watching the round 2 film in VLC).** *"All right, everything is looking good except the
full-screen graphics for each of the points, like sleep and alcohol, and all the full-screen graphics you made for, I
believe, 7 points. Those look a little empty. What I want you to do is to add an image to the right on each of those
full-screen graphics to fill them out. For sleep, add a stock image of somebody sleeping, or you could use a photo,
maybe even that photo of me sleeping on the chair from the pool photo shoot. For alcohol, you could use that AI image
that we made for a thumbnail before, of me holding a beer. Basically, look through all the stuff that we made before,
stock images, and put an image on the right side of all those full-screen graphics for each of the points. Use stock
or something that we already made when possible and when necessary. If there's nothing that fits, generate something
new. Make a handoff document to show me all those graphics for approval in the next round, and then once those are
approved, we'll reedit the full thing."* Record: `/Volumes/Extreme/_edit_work/ro11/round3-plan/decisions.json`.

**Read first.** `_shared/VIDEO-RULES.md` (new 10-08: round 1 shows everything, later rounds only what changed; review
videos of 45 s or more go in `Videos to Review/`), `_shared/PRE-RENDER-APPROVAL.md` (the review page layout),
`_shared/GRAPHICS-STANDARDS.md`, `_shared/SOFTBLUE.md`, `_shared/IMAGE-GENERATION.md`,
`.claude/skills/longform-edit/reference/ro11/README.md` (the full-film traps are at the bottom).

**Locked (do not change). Re-hash before starting.** Work dir `/Volumes/Extreme/_edit_work/ro11/`.
- Delivered round 2 film `round2/RO11_MASTER.mp4` sha256 `34cea69f...5b598b` (Dan: everything good except the 7 cards).
- `plan_resolved.json` `9361ab4e...36c8be`, `hf/manifest.json` `dd75eba5...020038`, `edl.json` `30470add...2c6eb6`,
  `shots.json` `1e22e21f...533944`, `aiframes/C_motion_v2.mp4` `3b48ec73...06f69b`.
- The opener, cut, look, audio, every lower third, fact card, side list, the cycle card, recap G21 and clips C01 to C12.
- On each section card: the words (`FACTOR n OF 7` and the headline), their times, and the Soft Blue Light field.

**The seven cards today.** `recipe/gfx.py title_card(t, step, headline)`: full-screen field, cyan accent bar,
`FACTOR n OF 7` at 30 px, headline at 76 px, all left-aligned at x 150, centred vertically. The right two thirds are
empty. Each is on screen 2.4 s (T7 2.75 s).

| ID | film time | headline | candidate picture (found 10-08; verify, then choose) | label it needs |
|---|---|---|---|---|
| T1 | 0:26.5 | Sleep | `photos/finalized social media photos/photo-21_FINAL_PRIMARY.jpg`: Dan asleep on the pool lounge chair (he named it). A lying photo stays uncropped under the Speedo rule | Real picture chip |
| T2 | 1:25.1 | Alcohol | `social media graphics/youtube/thumbnails/Can You Drink Alcohol And Still Have Abs/_build-2026-10-05/assets/ai_dan.png`: the AI image of Dan holding a beer, clean plate with no type (he named it) | AI-GENERATED chip |
| T3 | 2:19 | Hormones | nothing found in the library. Stock still first (a blood test vial, a lab report); it must not be the blood-draw scene already at 3:01 | none for stock |
| T4 | 3:30 | Meal Timing | nothing found. Stock still first (a plate beside a clock, a kitchen at night); not `assets/latemeal.jpg` or the late-night eating clip | none for stock |
| T5 | 5:13 | Protein | look in our own kitchen B-roll first (salad and meal-prep shoots, `clip_library.py find`), then stock (steak, eggs); not `assets/plate.jpg`, the chicken pan clip or the skillet clip B0287 | none for stock |
| T6 | 6:26 | Exercise | pool-shoot photos of Dan with a kettlebell: `photo-29`, `photo-38`, `photo-49` in the same folder | Real picture chip |
| T7 | 8:09.8 | Daily Movement | `assets/stairs.jpg` is in the work dir and unused, but check it is not the same scene as clip C12 (a man on outdoor stairs at 8:38); else stock of someone walking outdoors | none for stock |

Order of preference is Dan's standing rule: our real B-roll and photos, then an existing AI image of ours, then stock
(Pexels and known-rights only), and a new image last. A new image is made with
`.claude/skills/_shared/codex-image.sh` on the subscription, never a paid API. No stock source may repeat inside the
film, and a different angle of the same scene counts as a repeat. Already used: clips C01 to C12 and the card photos
`sleep.jpg`, `drinks.jpg`, `latemeal.jpg`, `plate.jpg`, `lift.jpg`, `jog.jpg`, `walk.jpg`.

**Rules that bind the design.**
- A picture is on screen for 2.4 s: one clear subject, readable at a glance. The words stay on the left, same size.
- A real photo of Dan carries "Real picture of me. Not AI-generated."; an AI image carries AI-GENERATED. Measure him on
  the rendered card and keep the chip off his face and his abs.
- Keep it inside Soft Blue Light: reuse the fact card's photo frame (rounded, hairline border) rather than inventing a
  new treatment. Do not put the picture in a small box with empty field around it: fill the right side.
- No belly close-ups; nothing built around belly fat.
- No AbsByAI.com mark.

**Next action (in order).**
1. Rename the task. `queue.py set RO-11 in_progress --by Claude`, mirror it, board entry to IN PROGRESS. Re-hash the locks.
2. Choose the seven pictures: `clip_library.py find` per card and look at the contact previews, check the two Dan named,
   search Pexels where nothing of ours fits, generate with Codex only for a card that still has nothing. Note the source
   and licence of each.
3. Add an optional picture to `gfx.title_card` (and a `photo` and `label` field on the seven `title` items in
   `recipe/plan.py`). Build in a new `round3/` folder; never overwrite `round2/`. Draw two layouts on ONE card (for
   example the framed photo card, and a larger picture that fades into the field) so Dan can pick, then all seven in
   the layout you recommend.
4. Render each card as a still at its settled frame and as a moving context clip with about 3 s of speech either side
   (`build.render_range` on the short range; names `context/<ID>-context - REVIEW 540p.mp4`). Check the picture's
   entrance against the headline's, the cut in and out, and the chip positions.
5. Build the standard review page (start from `recipe/page.py`): header with what is locked and Dan's words, "Your
   decisions", "What I decided", the seven cards three per row with source and label under each, one docked player
   for "Play it moving, in context", one reply box. Serve it with `_shared/review_server.py`; check a byte-range
   request returns 206 before sending the link. Context clips are under 45 s, so nothing goes in `Videos to Review/`.
6. Decisions to put to Dan (keep it to these): the layout (two options, recommendation first); any card where two
   pictures are close; and the ending, still unanswered: "add about 0.7 s of your smile after the last word, or leave
   it?" (on the roll he holds a smile from src frame 25619 to 25651; recommendation: add it).
7. Stop. Write the round 4 handoff (rebuild the full film with the approved cards, every gate, one independent review,
   deliver, replace the copy in `Videos to Review/`), with a starter prompt and model in the chat message.

**For round 4, so nothing is rediscovered.** Order: render (13 min), `finish_chain.sh`, own negative-events scan, one
`ra-reviewer` that writes `logs/findings.json`, `watch.py --judge`, `finish.py` again, delivery gate (25 min),
`deliver.sh`. Copy `hf/renders` aside before any `from_plan.py --render`. The gate plan needs each new chip: a real
photo's chip goes in `real_photos`, and the labels row needs 0.85 or better. An end hold adds frames only at the tail,
so no graphic time moves. Known and approved: G20 reads -211 px at 9:15.25 (hands under the card).

**Not done yet (do not claim).** No picture is chosen or licensed, no card is redrawn, no page exists. Dan has not
answered the ending question. The clip library entries for the opener clip and the used stock wait for final approval.

**Current state.** Round 2 film delivered and watched: `claude edited long form content/11 - When Calories Don't Matter
For Fat Loss/` (notes `notes-RO11.md`), VLC copy `Videos to Review/Calories Don't Matter LFC R2 - full film.mp4` (leave
it until the round 4 film replaces it), 540p https://drive.google.com/open?id=12ZEHeUhzHNG61W0SQXMd5Rp4FuwQuHVz.

**Spend.** About $3.50 of the $5 cap, all before round 2. Codex images are on the subscription and cost nothing here.

**Open risks.** Seven new pictures can drift off the film's look: grade stock stills toward the footage and keep one
frame treatment. A photo of Dan asleep on a lounge chair is shirtless: the chip must clear his abs.

**Starter prompt (Claude Opus 5.5, effort high):**

Name this task `Calories Don't Matter LFC R3`. This is CONTENT (long-form). Read and execute
`Handoffs/handoff-20261008-ro11-round3-section-cards-with-pictures.md`. I approved the RO-11 film except the seven
full-screen section cards, which look empty. Put a picture on the right of each one (the pool photo of me asleep on
the chair for Sleep, the AI image of me holding a beer for Alcohol, existing material or stock for the rest, and use
the Codex subscription to generate the images only if nothing fits), show me all seven on a review page, and stop. Do
not rebuild the film until I approve them.
