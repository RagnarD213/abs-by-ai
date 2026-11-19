AD (Great Again T upsell video). Task name: `GAT Upsell 4 AD R2`.

# Great Again T Upsell 4: Abs By AI (WV-07): round 2 handoff (2026-11-19)

Written by the original "GAT Upsell 4 AD R1" chat after Dan's round 1 review. **Model: Claude Opus 5.5, high effort.** **Mac: the M6** (Dan's
choice; the job lives at `~/Projects/_edit_work/WV-07`, internal SSD; never work through the M2 share). Round 1 was built by the
"M6 second edit" chat, which is closed; this file plus its notes are the full context.

One native 9:16 upsell (1080x1920, 29.97), Dan on green screen over Wood Kitchen 1, roll C1904 Upsell 4 range (local copy in `src/`).

## 0. Read first
- `~/Projects/_edit_work/WV-07/round1/ROUND-1-NOTES.md` (source mapping, recipes, what was fixed, what is left) and `round1/ROUND-1-REVIEW.md`.
- `plan/take_map.md`, `film/recipe/` (graphics.py, captions.py, phone_insert.py, chain_*.sh), `app/CAPTURE.md`.
- `.claude/skills/_shared/VIDEO-RULES.md` top sections, including the two rules Dan set in this review (real B-roll exercise demos in
  every video; funnel CTA = text with down arrows), `Handoffs/video-editing/WV-04-round-2-revisions.md` sections 1-2 (upsell style),
  `/ad-edit`, `PRE-RENDER-APPROVAL.md`, `CUT-CONTINUITY-QC.md`.
- **All 30 key pieces are done** (K001-K030 `.done`, lanes ended CHAIN_DONE 05:33 Nov 19). Never re-key a done piece.

## 1. Dan's round 1 words (verbatim, 2026-11-19)
> Okay, at 57 seconds, there is a very slight pause in the transition. I want you to make that transition smooth around 57 seconds. Let's go with match for the color. House bass for the voice.
>
> A01 app custom workouts, AI trainer, exercise demos. I want to use the real workout or the real exercise demonstrations with the real B-roll that we made. Let's make this a standing rule going forward that we always use the real B-roll, not the AI stuff, when we're doing demos from here on out.
>
> Now that we have that, use one where I'm looking as ripped as possible, maybe the side laterals, and actually show two of them: one in the pool and one at the gym. Show that we have gym stuff and home stuff. For the accept offer, same feedback as the other videos. I want to make this just text with an arrow pointing down. This looks like they should click the button or tap the button within the video. I want to avoid confusing the prospect, maybe in their 60s or 70s. I want to have the text say, "Click the button below to try Abs By AI," then arrows pointing downwards, to make it obvious that they shouldn't tap on the button within the video and that it's on the page below the screen.
>
> Real meal plans built around food you like. Remember our rule here: we always need to show the image. A screen like this would be good, but I need the image on here, and then scroll through a few different ones to show a few different options. Just put the image right below the honey garlic and sweet potato bowls, and below the smaller gray text there, and that's good. Show one other one. Just show we have options.

Save them as `round2-plan/notes_r1.txt` (already saved there) and your reading as `round2-plan/decisions.json`.

## 2. What to change
1. **Colour Matched, voice House bass:** locked.
2. **~0:57 transition (round 1 film time; the reviewer's D10 "56.6 s beat"):** a very slight pause at the join. Tighten it so the join flows
   (trim the gap, keep natural breath and word decay; seamscan the join and look at the picture join; zoom step stays).
3. **A01 (app custom workouts / AI trainer / exercise demos):** replace the app's AI exercise demos with REAL B-roll demos. Two of them, Dan
   looking as ripped as possible: side laterals at the pool and side laterals (or the closest real lateral) at the gym, so viewers see gym
   and home. Search the clip library and the real-demo library first (`clip_library.py find "side lateral"`; batch 9 real side lateral B0450
   is accepted by Dan; real-demo handoff `Handoffs/handoff-20261109-real-broll-exercise-demos.md`). Colour correct each to the film and
   inspect it in the final frame. Keep them inside the app/phone treatment if that reads as the app's demo, or full frame if clearer; your call, say which.
4. **Meal plans (decision 3 on the round 1 page):** Dan wants the real meal-plan screen WITH food photos. On the app screen he saw (the
   "Honey Garlic ... and Sweet Potato Bowls" plan), put the food image right below that recipe title and below its smaller grey text,
   then scroll to one other recipe with its image, to show there are options. Use real app images if the app has them for those recipes;
   otherwise generate appetizing food photos for those exact dishes (non-person food illustration: no AI label needed under the
   deception-risk rule; Google subscription first, Codex comparison per the blind rule). Never the rejected chicken-and-broccoli plate.
   This places A02 on the meal-plan line ("Abs By AI builds your whole meal plan ... instead of against it", take S09).
5. **Accept-offer CTA (C01/C02 button + pill, from the first "click/accept" to the end):** remove every in-video button and pill. Replace
   with text "Click The Button Below To Try Abs By AI" with arrows pointing down (Soft Blue Light, HyperFrames motion; arrows may pulse),
   clear of face, hair and captions. This also removes the round 1 C01 caption collision at 4:39. The spoken close ("Click Accept Offer
   below ...") stays as filmed.
6. Everything else Dan did not mention on the round 1 page is accepted as shown (key, L01 list, P01 phone + bottle, S01 study, other app
   scenes, O01 price, K01 guarantee). Say so in "What I decided".

## 3. Order of work
1. `python3 .claude/skills/_shared/editroute/editroute.py pick WV-07 --kind VSL --round 2 --chroma --host m6`, `resume.py check WV-07`,
   then `editcap.py acquire WV-07 --title "Great Again T Upsell 4: Abs By AI" --type AD`. If it waits, arm `editcap.py wait WV-07`.
2. Build the new A01 real demos, the meal-plan screen with photos, the new CTA, and the 0:57 fix. Then the WHOLE upsell at 1080p
   (round 1 approved the look, voice, key and graphic family; the new items are not new kinds except the food photos, which are shown on
   the page with the film).
3. Full checks on the exact file: hair clearance, caption proof, sync, audio gate with seamscan on every join, `deliver/gate.py --format
   ad9x16` with its plan, watch pass, CUT-CONTINUITY-QC, then a fresh independent `ra-reviewer` (expect DOES NOT SHIP first; fix).
4. Deliver to `Claude Ad Videos/Great Again T Upsell 4 Abs By AI - WV-07/` (notes, recipe, stamps), round 2 review page (1080p, side pane
   800/1150 px, silent checks then owner handoff), timestamps of every change in chat, copy to `Videos to Review/` replacing the R1 file,
   `editcap.py release WV-07 --review`, `queue.py set WV-07 delivered` + Edit Queue page mirror, update the board line. Stop for Dan.
5. No covers, uploads or scheduling. On Dan's final approval, write the Codex setup handoff (`/ad-setup`).
