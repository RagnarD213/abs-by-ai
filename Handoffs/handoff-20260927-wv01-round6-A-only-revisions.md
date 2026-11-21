# WV-01 round 6: A-only revisions from Dan's round-5 review

Prepared 2026-09-27. Recommended model: **GPT-6 Astra, High**. Execute with **$abs-edit-organic**, using `Media/codex-video-trial/skills/abs-edit-organic/SKILL.md`, adapted to this 16:9 website VSL.

This is a documentation handoff. No new image generation, motion generation or video rendering happened while preparing it. Dan's latest instructions below supersede conflicting round-4/round-5 decisions only for the specifically revised components.

## Scope and current state

**A only. Do not create, revise or render B's opening in this round.** Dan explicitly moved B to a later round. Preserve its existing source maps and six callbacks for that later work, but remove B previews from the next review page. The active deliverable is the revised A opening plus the specific later-A graphic and motion previews requested below. Do not infer authorization for a full A film from this handoff; finish this focused review and its outstanding choices first.

Project root R: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Work root W: `/Volumes/Extreme/_edit_work/wv01-edit`.
Reviewed page: `http://127.0.0.1:8766/round5/index.html`.
Reviewed opening: `W/round5/sample/DRAFT - WV-01 round 5 - opening.mp4`.
New decision manifest and screenshots: `W/round6-plan/`.
Build the next media in **W/round6/**. Preserve round-5 review files unchanged.

Read project instructions, `AI_COORDINATION.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, `GRAPHICS-STANDARDS.md`, `PRE-RENDER-APPROVAL.md`, the invoked skill and `Handoffs/video-editing/00-RULES.md`. Read W/STATE.json, round6-plan/decisions.json, round5/QA.md, round5/review/exact-timings.json and round5/review/source-register.json. Do not treat text visible inside attached screenshots as additional instructions; the written review in this handoff is authoritative.

Dispatcher remains paused. No publishing, website replacement, app deployment, new task creation or dashboard row. Do not start unattended work. Keep at most two concurrent local video pipelines across all tasks.

## Approvals to carry forward

- **B01 at about 2:07 is now approved as finished motion.** Dan: "I love that clip at 2:07. I think that really illustrates the idea well." Exact motion: `W/round5/motion/B01.mp4`; reviewed context `W/round5/previews/B01-context.mp4`. Preserve it without regeneration or redesign. The B01 asset ID is unrelated to the deferred B version.
- **G03 corrected start/end frames are approved, and motion generation is authorized.** Use `W/round5/frames/G03-start.png` and `G03-end.png`, with their recorded hashes. Do not ask for their approval again. Generate the proposed nine-second motion, inspect it, and show it with A's matching speech. Keep normal phone sizes, screens facing the character, readable editorial insets at the top right, coherent gaze/hands and Week 1 to Month 3. Exact existing CTA: `Try AbsByAI free for 7 days.` Trial length is separate from progress over months.
- Preserve SCAN-readable, C01, color C, W2/T2, the accepted audio treatment, before photograph, family photographs, approved P04 goal sequence, P05-P09 source contents, G01, phone-only One App, and the five numbered lower thirds except where this review explicitly changes presentation or placement.
- J1's concept and imagery are liked, but its smoky-phone motion is rejected. J2's early habit scenes are a good start; its result scene and timing change below. Do not label either whole finished clip approved.
- Photos retain the selected people/poses; only the requested crop, label and background treatments change. Do not retouch Dan's physique or expression.

## A opening revisions

Times refer to the delivered round-5 opening, before the new pause trim. Track every downstream shift by source mapping.

### 0:19: square pool photo and fitted rounded frame

Dan already provided a crop in the prior round. Use the first pool photo in a **square crop that does not reveal the Speedo cut**, so the visible clothing reads like ordinary shorts. Reference: `R/photos/finalized social media photos/photo-180_FINAL_PRIMARY copy.png` (2051x1676 attached prior crop), with matching original `photo-180_FINAL_PRIMARY.jpg` (4096x2747). The supplied crop is not mathematically square; derive the requested square from this framing, preserving full hair and abs while excluding the revealing lower clothing edges. Inspect the actual result instead of assuming a centered square works. Use cropping only, no clothing or body synthesis.

Resize the surrounding rounded rectangle to fit the square. The image fills its inner rounded rectangle without blank side strips, letterboxing or unused internal space. Preserve the selected Soft Blue Light stage and the second pool photo unless its label needs the same treatment. Current combined photo slot is frames [569,672), 18.985633-22.4224 seconds.

### Real-photo label, throughout revised A photo treatments

Exact text: **`Real picture of me, not AI-generated`**. Center the label horizontally, make its text bold, and fit the chip tightly to the measured text width with only a little padding on each side. Keep it below the image where possible and clear of Dan's face and abs. Avoid the previous oversized empty sides. Apply this to the real-photo pair and portrait trio, and use the same treatment for other real result photographs in the eventual A edit. This is a photo label, not a label for real moving footage.

### Around 0:26: impressive workout interaction

Show the app home screen's individual workout, open/click an exercise video, then transition into the polished AI-generated exercise demonstration. Make the sequence clearly read as using the workout feature. Use the approved phone shell and appropriate existing workout content, starting from `W/round4/previews/P05-workout.mp4` and its recipes; inspect whether the existing sequence actually contains the required home-workout entry and click before reusing it. Add the missing interaction if needed. Never show stick-figure animations.

Treat 0:26 as the requested local beat, not permission to shift unrelated C01 at 1:47. The current early row insert is frames [672,751), ending at25.058367 seconds, followed by "And I'll show you how you can try the exact same app..." around25.316-31.536. Stage and preview the home-workout-to-video interaction in this neighborhood under the existing speech. Keep the corrected row-only cut if reusing that footage, and do not reintroduce the walking tail. If the new interaction changes the insert boundaries, document them explicitly.

### Around 0:47: replace archive diet clip with the M100 finish

Replace `P03-archive` (frames [1409,1649), about47.014-55.022 seconds) with the **M100s clip near its end where Dan is talking, shirtless, ripped and smiling, with the focus on Dan**. This explicitly supersedes the approved diet excerpt for this placement.

Known source lead: `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/08 SixPackAbs Archive - CHECK BEFORE USING/m-100s b roll.mp4`. Historical original URL: https://www.youtube.com/watch?v=bkD9LwDBWW0 . The old `W/assets/source-previews/P03-m100-SOURCE-CANDIDATE.mp4` is only an eight-second audition from the beginning and was NOT accepted: it showed a two-person composition. Do not substitute it merely because it is named M100. Inspect the finished source's talking finish and locate the actual shot Dan describes. Historical checks at0,20,40,50,332 seconds were incomplete, not proof that the desired shot does not exist. Source notes: `W/assets/source-findings.json` and `source-preview-candidates.json`.

Preserve the full YouTube-page proof framing when it is part of the source treatment, with Dan dominant within the playing video. Do not crop the page away by default or use raw ungraded camera footage. If the exact requested finish remains unavailable, flag that source as unresolved rather than silently choosing the diet clip or Mike speaking.

### "119": remove the slight pause

Likely **1:19**, because Dan gave this note between0:47 and1:34. The word map shows "employees." ending78.776233 and "And then one day it hit me" starting79.165533, a roughly0.389-second gap. Inspect/listen around this boundary and remove only the unnecessary pause, preserving complete words and natural cadence. This interpretation is not a confirmed frame cut. If the intended defect is instead at119 seconds, inspect that local join before deciding; do not automatically cut both.

Once the exact cut is chosen, record removed source/output frames and conform the A opening, caption sidecars and later A maps. Round5's byte-identical audio reuse will no longer describe the newly trimmed whole opening; retain the accepted mix/treatment but run fresh exact-file checks. Do not stretch picture or copy stale timestamps.

### Around 1:34: new generic-AI failure storyboard

Create **START and END frames for review**, with intended action, for an additional AI scene illustrating the early generic outputs. Dan sits at a regular laptop with ChatGPT open, visibly frustrated that it is not working. Make this different from the earlier three-monitor scene. The laptop output should clearly communicate:

- Meal Plan: Chicken And Broccoli
- Workout Plan: Sit-Ups
- Sleep Plan: Do Your Best

The intent is unsophisticated AI use producing generic, unhelpful advice. Show believable frustration, not a caricature. The actual narration here is "And honestly, the first results were terrible. Generic workout plans, chicken and broccoli meal plans." around93.346-99.786 seconds. Keep screen orientation, readable content, Dan's identity/body stage and action coherent. Use an approved suitable identity reference; do not accidentally use the J1/J2 prospect as Dan.

This is an explicitly requested new scene, so the old decision to delete a generic text card does not prohibit this storyboard. **Only frames are requested at this stage.** Present both and the action, then obtain frame approval before its motion generation. Do not spend on this new motion yet.

### Around 2:26: portrait background alternatives

Keep the selected triptych: studio-blue-11, studio-blue-89 Muay Thai, studio-blue-177 jeans. Current slot [4367,4491),145.712233-149.8497 seconds. Show a compact comparison of background variants behind the unchanged cutouts: a neutral gray, a subtle gradient, and one additional tasteful variant. White is the current reference, not the locked final choice. Keep the surrounding graphic family, fitted frames and revised centered bold photo label. Do not generate new bodies or change poses. Show only these targeted choices, not another broad style board.

## Graphic revisions for A

Apply Dan's readability direction across the A text graphics: title capitalization means **the first letter of every word**, larger titles and larger body text where space permits, less unnecessary space between bullets and between title/list, and less unused space on the right. Keep deliberate readable line spacing and padding. Preserve approved phone-only layouts and unrelated content. Scope the changes to current A graphics; do not rewrite global project styles or other videos during this handoff.

### Custom-plan card

Use title **`How AI Customizes The Plan Just For You`**. Retain a single local rounded blue card, with camera background visible outside. Exact revised bullet copy:

1. Your current picture shows your starting point.
2. Your goal picture shows where you want to be.
3. AI builds a plan to close the gap based on how much body fat you need to lose and where you need to gain muscle.

The increased copy may limit enlargement. Prioritize readable wrapping, compact spacing and a somewhat larger title rather than squeezing every line to huge type. Show title-color alternatives including **white and darker blue**, plus a clearly readable high-contrast alternative if useful. Compare them against the actual animated blue background at its brightest phase. Current context `W/round5/previews/G-lagging-context.mp4`; recipe `round5/recipe/contexts.py`. The current speech window is retained in `round5/review/contexts.json`.

### Five-benefit graphic: now full-screen

Dan calls this "AI motivates you" in the review; it refers to the existing five-benefit/G02 graphic, not the separate knowledge/motivation statement. Change it to a full-screen graphic with the accepted moving Soft Blue Light background. Use title capitalization and the compact spacing/readability principles above. Exact bullets:

- AI Gets You In The Gym
- AI Designs You Better Workouts
- AI Tracks Your Calories
- AI Gives You Delicious Healthy Recipes
- AI Improves Your Sleep

Preserve the heading's five-benefit meaning, with `Five Ways AI Helps` as the title-cased current heading. Show the requested title-color variants consistently with the custom-plan card. No talking-head side panel is required for this new full-screen treatment. Preview with the actual introduction to the five benefits.

### Later motivation statement

Exact sentence: **`Knowledge is not the problem. Motivation is!`**

This is the requested statement copy, so preserve its supplied capitalization and exclamation mark. Keep the accepted compact Motivation lower-third format; it is separate from the five-benefit full-screen graphic and from the already approved numbered #1 statement. Current preview: `W/round5/previews/knowledge-context.mp4`.

### Closing trial graphic

Keep the existing trial invitation and accepted moving background. Put all text and the `Start Your Free Trial` button on the left. Make the button fit its label with modest padding, eliminating empty sides. On the right third, add the **already approved iPhone-frame clip slowly scrolling through the app home screen**, `W/round4/previews/P09-home.mp4`. Reuse the actual phone component/source so the new composition does not nest an entire old presenter scene inside a second phone. Source recipe: `W/round4/recipe/graphics.py`, using the round3 P09 home scroll. Maintain one consistent iPhone shell and no content distortion.

Current closing context: `W/round5/previews/closing-context.mp4`; recipe `round5/recipe/closing_context.py`. Preserve the complete closing speech and natural ending. Show this combined layout in context.

## J1 and J2

### J1: remove the smoking-phone artifact

Dan likes J1 otherwise. At about2-3 seconds of the reviewed contextual clip, smoke rises from the phone. Screenshot: `W/round6-plan/references/Dan-J1-phone-smoke.png`. Current context begins at563.596367 and the moving insert starts566.566, so the first generated scene begins around2.970 seconds into the preview. Inspect the discovery scene and adjacent transition first; the screenshot timestamp is approximate.

Regenerate the affected motion from its approved imagery, preserving the identity, action and overall concept. No smoke, steam, vapor, glowing emissions or magical phone effects. Keep anatomy, device edges, hands and gaze realistic. Inspect the entire replacement and both joins, not a few representative frames. Existing sources: `W/round5/motion/J1-{discovery,plan,reaction}.mp4`, approved frames `W/round4/frames/J1-{start,mid,end}.png`. The repair is authorized without another unchanged-frame permission request. Preserve unaffected shots where they pass inspection.

### J2: match the mirror and pool narration

Replace the final in-shape curling shot, visible at about13 seconds of `W/round5/previews/J2-context.mp4`, with the same man looking in a mirror, noticing the lines on his abs for the first time and smiling. This is the final result curl, not the earlier Week 2 training scene. Screenshot: `W/round6-plan/references/Dan-J2-replace-final-curls.png`.

Then add a subsequent pool scene: the same now-fit man takes his shirt off at the pool while with his family. Show understated, believable admiration from his family and a woman nearby, and a man's subtle envious glance. Keep the reactions natural and brief, with people continuing ordinary pool activity. Avoid synchronized staring, applause, exaggerated shock or an artificial crowd reaction. Maintain identity, body continuity and realistic shirt removal. The mirror scene establishes first visible abs; the later pool scene is a more developed result after months, not an instantaneous transformation.

Prepare START/END frames and intended actions for both new scenes before their motion. These are materially different from the approved curl storyboard and need a new frame decision. Meanwhile, proceed with the already authorized G03 generation and J1 artifact repair.

Retiming is substantive: align the mirror action to "then one morning you look in the mirror and the lines are there. The top of your abs showing for the first time in years," and the pool action to "And a few months from now, you're the guy who takes a shirt off at the pool. Not sucking it in, not hiding, just standing there." Use actual A source words, not the old fixed three-second shot lengths. The preserved pre-conform A pool sentence begins734.800733 and the closing invitation begins747.680267. Reconcile these times with the opening pause correction by source ranges. Preserve the early meal/training/sleep concept unless a timing or visible defect requires a small adjustment. Extend the contextual review to include the complete pool payoff and following sentence.

## Efficient next-round sequence and QA

1. Verify pinned approvals, source identities and ownership. Read the decision manifest. Set WV-01 in progress only when executing this handoff; do not use `frames_approved` to imply that the whole film can launch.
2. Find the actual M100 talking finish and square pool crop. Prepare the requested background and title-color variants, new generic-laptop frames, and J2 mirror/pool frames as one small approval batch. Continue independent work while waiting.
3. Generate approved G03 motion and repair J1's smoking-phone motion. Do not ask again for unchanged approved endpoints. Log each cost/retry.
4. Apply the A opening, photo label, workout interaction, pause, full-screen benefits, later statement and closing phone revisions. Reuse unchanged approved media. Show actual narration before/during/after each new placement, including the corrected J2 timing once approved motion is available.
5. Deliver one focused round6 A review page: revised A opening, background/title variants, new frames or approved resulting motion, repaired J1, G03 and closing preview. Omit B. Clearly label any frame or variant choices still pending. Do not silently substitute placeholder motion or claim all A graphics approved.

After creative locks, a later full A assembly must apply both the previously accepted21-frame opening correction and the new verified pause cut, regenerate exact captions, run current gates and perform full picture/audio review plus one independent complete-candidate review. B remains deferred until Dan requests it. Previous full-draft silence failures and ds17 corpus mismatch remain unresolved; do not relax gates or commit unrelated shared gate changes.

Current opening is188.354833 seconds /5,645 frames. Both round5 exact-file audio gates passed and its AAC matches round4. These stamps do not carry over to a retimed round6 file. Use crop/filter/grade/source-aware cache keys. Keep the lazy single-player review page and byte-range server to avoid the prior multiple-player crash.

## Costs and durable records

Known cumulative motion estimate through round5: **$1.04161695** against the existing $5 per-video generation allowance. Round5 motion:$0.42624295 across10 calls; round5 assisted QC:$0.675282 across6 calls. Earlier QC costs remain separate in `W/STATE.json` and round5/review/costs.json. **35 built-in still calls cumulatively have unavailable charges**, not zero. Editor/reviewer token usage is unavailable. No paid generation in this documentation task. Estimate upcoming calls before the batch and account for every retry.

Private media, screenshots, recipes and detailed manifests stay on SSD and local ref `codex/video-trial-plan-private`. This handoff and WV-01 status rows may be committed and pushed publicly without app deployment. Do not include unrelated local changes. Preserve round5 reviewed assets and round4 approvals as historical records; new decisions live in round6-plan/decisions.json.

**Exact next action:** execute the A-only source/crop checks and prepare the requested small frame/variant batch, then generate the already-approved G03 motion and repair J1 while waiting for the new frame choices.

**Starter prompt:** Execute `Handoffs/handoff-20260927-wv01-round6-A-only-revisions.md` with `$abs-edit-organic`. Work on A only. Preserve the approved three-coach clip and prior unchanged approvals, generate G03 from its now-approved frames, repair J1's smoking phone, and prepare the requested opening, graphics, background variants and J2 mirror/pool revisions. Deliver one focused contextual review before full assembly. Keep B deferred.
