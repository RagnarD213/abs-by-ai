# WV-01 round 7: A-only edits after Dan's round-6 review

Prepared 2026-09-27. Execute with `$abs-edit-organic` at `Media/codex-video-trial/skills/abs-edit-organic/SKILL.md`, adapted to this 16:9 website VSL.

Recommended model: **GPT-6 Astra, High**. The source identification, laptop camera-angle revision, two title-layout alternatives and newly authorized character motion need creative judgment alongside precise source timing.

This is a documentation handoff. No media was generated or rendered while preparing it. Dan's latest written decisions below supersede conflicting round-6 choices. **A only. B remains deferred.** No full A assembly until the remaining graphics, opening changes and finished new clips are approved.

## Where to resume

Project R: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Work P: `/Volumes/Extreme/_edit_work/wv01-edit`.
Reviewed page: `http://127.0.0.1:8766/round6/index.html`.
Reviewed opening: `P/round6/sample/DRAFT - WV-01 round 6 - opening.mp4`.
Authoritative new decision manifest: `P/round7-plan/decisions.json`, including hashes of approved files and Dan's wording.
Build new media in **P/round7/**. Preserve the round-6 page, exports, frames and receipts unchanged.

Read `AI_COORDINATION.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, `GRAPHICS-STANDARDS.md`, `PRE-RENDER-APPROVAL.md`, the invoked skill and `Handoffs/video-editing/00-RULES.md`. Then read `P/STATE.json`, the round7 decision manifest, `round6/QA.md`, `round6/WORK_PACKET.json`, `round6/review/contexts.json`, `round6/review/storyboard-timing.json` and the current source maps listed below.

Dispatcher stays paused. No publishing, website replacement, app deployment, new task creation or dashboard row. Claim WV-01 in progress only when executing the edits. Do not mark the whole job finalized or use frame approval to imply full-film authorization. At most two concurrent local video pipelines across all tasks.

## New approvals: preserve these exact assets

- **J1 finalized.** Dan: "J1 is looking good. That's finalized." Lock `round6/motion/J1-assembled.mp4` and its placement in `round6/previews/J1-context.mp4`. Do not regenerate or reopen the smoke repair.
- **G03 finished motion approved.** Dan: "G03 looks good." Lock `round6/motion/G03-assembled.mp4` and `round6/previews/G03-context.mp4`, including the separately repaired exercise panel, fixed editorial insets/calendar/CTA and explicit Week 1 to Month 3 cut. Earlier rejected attempts are not candidates. Do not reopen the unsupported automated finding after Dan's approval.
- **Mirror and pool START/END frames approved; motion generation authorized.** Use `round6/frames/mirror-start.png`, `mirror-end.png`, `pool-start.png`, `pool-end.png`. Do not use `pool-start-rejected.png`. Dan explicitly said both look good and "We're good to generate." The scene order, narration alignment and extended payoff in `round6/previews/J2-storyboard-context.mp4` are accepted. This is frame/action/placement approval, not approval of nonexistent finished motion.
- **Later motivation lower third approved:** `round6/previews/knowledge-context.mp4`, exact sentence `Knowledge is not the problem. Motivation is!`.
- **Final trial invitation approved:** `round6/previews/closing-context.mp4`. Preserve complete closing speech, fitted button/copy left, approved scrolling home phone right and natural ending.
- **After-portrait background selected:** subtle blue-gray gradient, `round6/graphics/portraits-gradient.jpg`. Keep the same three original cutouts and poses. Only the plural-label correction below remains for that display.
- **Five-benefit title color selected:** light cyan, `round6/previews/benefits-cyan-context.mp4`. Preserve its full-screen Soft Blue Light layout and five bullets, changing the heading as requested below.
- Carry forward B01 three-coach motion, SCAN, C01, color C, W2/T2, the accepted audio treatment, before/family photographs, P04 goal sequence, P05-P09 source contents, G01, phone-only One App, numbered lower thirds and other unchanged approvals. The explicit early-workout replacement below supersedes only that placement.

## Opening edits

All review times refer to the **round-6** opening before the new cut. Keep picture-only replacements at their intended times; conform subsequent placements only when narration is actually trimmed.

### Early workout: phone-only goblet squat, end at 0:28

Dan: "I just want to see a couple of reps of him doing the goblet squat in the phone frame. Don't go full screen with this and then end it at 28 seconds."

Replace the current home/list/tap/full-screen exercise sequence with a couple of complete goblet-squat repetitions inside the already approved iPhone shell. Remove the full-screen demonstration. End this insert at approximately **28.000 seconds**, on the nearest valid frame, then return to the presenter under uninterrupted speech. Do not cut the narration to shorten the insert. No new home-screen or clicking sequence is requested.

Current insert: round6 output frames [672,946), 22.4224-31.5649 seconds. Use the neighborhood before 0:28 for the repetitions; preserve the preceding photo exit. Inspect actual rep boundaries and keep natural speed, intact hair/body/dumbbell and undistorted phone content. No partial repetition substituted merely to hit a count; no stick figures or walking tail. Preserve the later C01 placement.

Existing polished source: `R/Media/exercise-demos/db-goblet-squat/db-goblet-squat-AIDAN-narrated-FINAL.mp4`. Phone helpers: `P/round6/recipe/components.py` and `P/round4/recipe/graphics.py`. Reuse the actual approved shell, not a whole old presenter scene nested inside a phone. Preview the complete revised early beat with surrounding speech.

### M100: correct video, rejected excerpt

Dan says the video is correct but the selected clip still focuses on the other man. He wants **the moment immediately after he finishes the exercise, smiling and looking at the camera, centered and clearly the focus**. Do not reuse the round-6 excerpt or call its moving camera selection approved.

Original finished video: https://www.youtube.com/watch?v=bkD9LwDBWW0 . Known library lead: `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/08 SixPackAbs Archive - CHECK BEFORE USING/m-100s b roll.mp4`.

Round6 downloaded only a late section, `round6/assets/m100-finish.mp4`; its selected local range 12.42-15.423 seconds was rejected. That limited section does not prove the requested post-exercise shot is unavailable. Inspect the actual exercise finish and immediately following reaction in the complete finished video, using Dan's identity reference to distinguish him from Mike. Choose the native centered, smiling, camera-facing Dan shot, not a two-person/Mike-led view or a camera pan that eventually approaches Dan. Its exact source time remains unresolved; do not invent one.

Keep the full YouTube-page proof treatment when inserting the correct excerpt. The original page capture is `round6/review/m100-page.png`. Use finished edited footage, not raw camera footage. Current round6 archive occupies [1409,1499), 47.0136-50.0166 seconds, then returns to presenter. Choose the smallest useful post-exercise passage within the existing local narration beat; document any picture-boundary change. Flag the source unresolved if the exact shot cannot be found rather than silently choosing another wrong excerpt. Show the corrected selection in context.

### Laptop placement at about 1:34

The generic-AI laptop scene belongs in the actual opening under "And honestly, the first results were terrible. Generic workout plans, chicken and broccoli meal plans." It must not remain permanently separate from the edit.

Current conformed A position: approximately93.1792-99.6192 seconds; original pre-conform source-map position93.346-99.786. See `round6/review/storyboard-timing.json`. Correct the camera/laptop angle first, as described below. Once the revised endpoints and then motion are approved, insert the resulting clip there. Pending frames may be shown in an explicitly labelled short contextual audition, not passed off as finished motion.

### Around 2:14: remove only the slight unnecessary pause

Inspect/listen around132.5-136.2 seconds in the exact round-6 opening. A likely boundary is the source join at output frame4002, approximately133.5334 seconds, between C1697 source ranges [4612,4885) and [5469,5953). The word map has "published." ending133.437 and "By" starting133.611, around0.174 seconds apart. This is a lead, **not an approved automatic cut**; Dan identified the audible transition, not an exact frame count.

Remove only verified excess silence, preserving complete "published" and "By combining five different AIs" and natural cadence. Do not trim approved B01 action or remove a meaningful breath to satisfy a guess. Record the new removed source/output frames and conform the opening, SRT/VTT, word maps and all later A placements. Do not reapply the already completed 21-frame and five-frame cuts.

## Photo label and graphic changes

### Plural disclosure for multiple photographs

Use **`Real pictures of me, not AI-generated`** when a full-screen photo treatment displays multiple photographs, including the three-portrait screen. Singular **`Real picture of me, not AI-generated`** stays appropriate for one photograph. Apply the plural rule consistently to multi-picture treatments in the active A plan; do not put a photo label on real moving footage or on a text-only graphic.

Retain the centered bold fitted chip with modest padding, clear of faces and abs. Install the selected subtle blue-gray portrait gradient. Do not alter poses, bodies or expressions. Preserve the square pool crop and follow the current standing waistband crop rule for Speedo photos.

### Custom-plan card: two larger-title alternatives above the light

This note applies to the custom-plan graphic, based on the order of Dan's review. Preserve its accepted three bullets and meaning. Title remains **`How AI Customizes The Plan Just For You`**.

Make the title slightly larger and move it into clear upper-left space **fully above the bright blue light**, with the graphic/list beginning below it. The point is to stop similarly colored light behind the lettering from reducing readability. Show both requested layouts:

1. A larger title on **two lines**, fully above the light.
2. A larger title on **one line**, fully above the light, with a somewhat wider graphic if needed.

Both are contextual alternatives, not a new broad style board. Keep one local rounded blue card/list treatment with camera visible outside, fixed presenter composition and intact arms. Avoid a second full-height field. Check the title against the brightest part of the animation, not only a dark still. If widening is needed, do it without crowding Dan or squeezing the body text. Do not assume the five-benefit cyan selection separately approves a new custom-card color; use the reviewed white version as the working reference for these layout auditions.

Exact unchanged bullets:

1. Your current picture shows your starting point.
2. Your goal picture shows where you want to be.
3. AI builds a plan to close the gap based on how much body fat you need to lose and where you need to gain muscle.

Sources: `round6/recipe/components.py`, `round6/previews/custom-white-context.mp4`. Current conformed insertion263.4298-277.3771 seconds, before the next pause correction. Preserve its matching speech.

### Five-benefit heading and selected color

Use the **light cyan** alternative. Replace the heading with exactly:

**`Five Ways AI Beats Human Trainers`**

Preserve the full-screen moving Soft Blue Light treatment and these five bullets:

- AI Gets You In The Gym
- AI Designs You Better Workouts
- AI Tracks Your Calories
- AI Gives You Delicious Healthy Recipes
- AI Improves Your Sleep

Fit the longer heading cleanly with readable spacing. Keep the existing larger, compact type treatment. Show the revised heading with the actual introduction to the five benefits; no additional color-choice round is needed.

## New scene work

### Laptop: change camera and screen angle before motion

Dan likes his appearance and the laptop. He rejects the unnatural staging where the laptop faces the camera while he is not looking directly at it. Move the camera more to Dan's side and point the laptop more toward **his face**. He should visibly look at the screen as a person using it would, rather than presenting the screen to the viewer. Keep enough oblique visibility for the generic output to be understandable without rotating the laptop back toward the camera.

Preserve Dan's approved identity/body stage, ordinary single-laptop setting and believable frustration. Keep these exact screen concepts: `Meal Plan: Chicken And Broccoli`, `Workout Plan: Sit-Ups`, `Sleep Plan: Do Your Best`. Preserve sensible screen perspective, hands and gaze. Use `round6/frames/laptop-start.png` and `laptop-end.png` as appearance/room references, not locked camera geometry.

Prepare a revised START/END pair and intended action in the same approval packet. **The current laptop endpoints are not motion-approved.** The new camera angle is a material frame change; get that pair approved before spending on laptop motion. Meanwhile, execute the already authorized mirror/pool generation and other edits.

### Mirror and pool: generate now from approved round6 frames

No further unchanged-frame permission is needed. Preserve the same J1/J2 prospect, distinct from Dan.

- **Mirror:** notices first upper-ab lines and gives a small proud smile, with coherent mirror reflection, anatomy and gaze. No body transformation within the shot. Duration8.1081 seconds, original A726.6926-734.8007; current conformed A725.8251-733.9332.
- **Pool:** months later, naturally removes his T-shirt, lowers it into one hand and stands relaxed. Wife smiles warmly, nearby woman briefly glances, nearby man gives a subtle sidelong glance. People continue ordinary activity. No synchronized staring, applause or exaggerated reactions. Duration8.7087 seconds, original A734.8007-743.5094; current conformed A733.9332-742.6419.

Align actions to the complete mirror and pool sentences, then preserve "That's what this did for me at 40. I have never felt better in my life" and the subsequent closing invitation. Earlier training, meal and sleep shots remain approved in concept/placement; preserve them. Current complete context: `round6/previews/J2-storyboard-context.mp4`; scene recipe `round6/recipe/storyboards.py`.

Inspect all generated frames and both joins for shirt/hand/body mutations, reflection errors, smoke, frozen tails and unnatural reactions. Do not stretch a provider's shorter clip to fill the speech or silently hold the endpoint. Round6's Wan runner returned121 frames at16fps, 7.5625 seconds, despite a9-second request. Inspect actual duration; plan a supported native-duration generation or coherent continuation to cover the authorized action and words. Preview finished motion with narration for Dan's final clip decision.

## Source maps, checks and efficient delivery

Current opening is188.188 seconds /5640 frames. The original full-A map has already been conformed by26 frames: the previous21-frame correction plus round6's five-frame pause trim. New baseline files:

- `round6/sample/PLAN-opening.json` and `source-mapped-words.json`.
- `round6/review/PLAN-A-CONFORMED.json` and `full-A-conformed-words.json`.
- `round6/review/contexts.json` and `storyboard-timing.json`.
- `round6/review/source-register.json`, `protected-hashes.json`, `G03-edit.json`.

Use those maps deliberately. The round6 context renderer still addresses the older full-draft source timeline and records conformed positions separately; do not subtract the26 frames twice or copy old preview times into a new assembly. The new2:14 pause trim will additionally shift later placements, not earlier1:34 laptop placement.

The final round6 opening and540p review both pass exact-file audio checks at-14.90 LUFS, after a recorded0.2 dB finishing gain. Preserve the accepted sound; do not stack that gain again. A new pause edit requires fresh exact-file checks, captions and maps. Preserve grade C, W2/T2, phone shell and approved graphic assets. Use source/crop/filter/grade-aware cache keys. No shared gate changes. Prior full-draft silence failures and ds17 corpus mismatch remain unresolved.

Execute the authorized mirror/pool motion while preparing the new laptop frames, title variants, phone-only squat, correct archive source and small pause edit. Deliver **one focused round7 A review page**: revised opening, both custom-title alternatives, cyan benefits with new heading, revised laptop pair/context, and generated mirror/pool payoff. Do not make Dan reapprove unchanged J1, G03, B01, motivation or closing. Keep their locks visible as carried-forward records rather than redundant decision requests. B has no previews in this round.

Retain the lazy single-player page and byte-range server to prevent multiple-player crashes. Full A assembly and one independent complete-candidate review follow the remaining creative locks; no complete placeholder film. No publishing or app deployment in this task.

## Budget and records

Known cumulative motion estimate through round6: **$2.18401730** of the existing **$5 per-video allowance**. Round6 motion:$1.14240035 across5 calls, including retries. Round6 assisted QC:$0.396306 across4 calls, separate from generation. **42 built-in still calls cumulatively have unavailable charges**, not zero. Editor/reviewer token usage is unavailable. Estimate each upcoming batch and record every attempt; do not reset totals because the round/task changed. The prior mirror/pool planning estimate was about$0.65 together, but re-estimate for the actual model and required native durations.

Private media, recipes and detailed decisions stay on SSD and local ref `codex/video-trial-plan-private`. The new handoff, its index entry and own coordination row may be committed/pushed publicly without an app deployment. Preserve unrelated local/staged work. No new dashboard row. Keep WV-01 unfinalized and the dispatcher paused until Dan explicitly starts the next round.

**Exact next action:** verify the pinned new approvals, claim WV-01 for the user-started edit task, then source the actual post-exercise M100 reaction and prepare the phone-only squat/laptop-angle/title revisions while generating the approved mirror and pool actions within the recorded budget.

**Starter prompt:** Execute `Handoffs/handoff-20260927-wv01-round7-A-only-revisions.md` with `$abs-edit-organic`. Work on A only. Preserve the newly approved J1, G03, motivation and closing. Generate the approved mirror/pool scenes; revise the laptop camera angle for frame review; apply the phone-only squat ending at0:28, correct M100 post-exercise shot, slight2:14 pause trim, gradient/plural photo labels, two larger custom-title layouts and cyan `Five Ways AI Beats Human Trainers` heading. Deliver one focused contextual review. Keep B deferred.
