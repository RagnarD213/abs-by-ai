# WV-01 round 3: lock the crop, motion graphics and opening

Written 2026-09-25 from Dan's complete round-2 review. Recommended model: **GPT-6 Astra, High**. Use `$abs-edit-organic`, adapted to a 16:9 website VSL.

## Goal and sequence

Lock the framing and a professional Blue Glass graphics system, then revise the first three minutes for one consolidated review. Dan wants the next sample to settle the opening before the rest of A/B is edited. Do not rebuild the complete films yet.

1. **Crop first.** Read the saved crop choices and any subsequent reply from Dan. Show the existing screenshots or a five-second proof. Get his wide/tight choice before rendering another complete opening sample. Do not interpret a recommendation as approval.
2. Establish several genuinely moving Blue Glass variants across full screen, phone/left third and lower third. Show real content with motion, not static cards described as motion graphics. Lock the system with Dan.
3. Generate the three explicitly approved AI concepts, prepare new requested frame pairs and exact existing-source previews, and build the revised opening using approved assets or exact-duration placeholders where choices remain pending. Keep the recorded story and subtitle timing correct.
4. Deliver one consolidated opening/asset package. The full-film finish follows Dan's review of this round.

No publishing, site-video replacement, YouTube setup or production app-feature deployment. No new dashboard task or automatic dispatcher run. This handoff records work for a new task; it did not generate the requested AI motion.

## Required context

Read `.claude/skills/_shared/VIDEO-RULES.md` in full, `Handoffs/video-editing/00-RULES.md` including its linked Codex environment table, the installed organic skill and relevant references, current `AI_COORDINATION.md`, and the WV-01 queue row. Then read:

- Previous instructions and source decisions: `Handoffs/handoff-20260925-wv01-round2-creative-direction.md`.
- Original plan/research/source map: `Handoffs/video-editing/WV-01-{EDIT-PLAN,RESEARCH,SOURCE-MAP}-20260924.md` (three separate files).
- `/Volumes/Extreme/_edit_work/wv01-edit/STATE.json` and `round3-crop-review/round3-decisions.json`.
- Round-2 package: `/Volumes/Extreme/_edit_work/wv01-edit/round2/index.html`.

Work root below is `/Volumes/Extreme/_edit_work/wv01-edit/`, abbreviated W. Preserve `round2/` as reviewed history. Use a new round-3 work directory for revisions. Raw footage is read-only.

## Crop question answered, screenshots prepared

C1697 is **3840 x 2160**. The current wide crop is `3680:2070:80:90` (width:height:x:y). Its bottom is already **2160**, the full recorded bottom edge. There are **zero additional source pixels beneath the current wide crop**. Do not promise more desk or synthesize an extension.

Dan's final instruction: keep that bottom edge, zoom in very slightly to remove space on the sides and about half of the spare headroom. Screenshots use approved color C and the exact source moment at round-2 output 00:08:

| Choice | Crop w:h:x:y | Change from current wide |
|---|---|---|
| W0 | 3680:2070:80:90 | Current comparison |
| W1 | 3616:2034:112:126 | About 1.8% tighter |
| W2 | 3552:1998:144:162 | About 3.6% tighter, editor recommendation |
| W3 | 3488:1962:176:198 | About 5.5% tighter, least headroom |

All three retain bottom y=2160. Keep blue side light and the captured lamp/base visible. W3 is closest to the head and needs particularly careful movement checks.

Dan likes the tight zoom at **01:15**. Keep its size `2608 x 1466` and fixed x=616, but move it down a little. Unlike the wide shot, this tight crop has unused recorded space below it. Screenshots at exactly 01:15:

- T0: current y=120.
- T1: y=160, 40 source pixels lower; editor recommendation.
- T2: y=184, 64 source pixels lower.

Gallery: `W/round3-crop-review/index.html`, served at `http://127.0.0.1:8766/round3-crop-review/index.html`. Full-size individual JPEGs, `wide-comparison.jpg`, `tight-comparison.jpg`, `crop-options.json` and `build_crops.py` are alongside it. **W2/T1 is only recommended, not approved as of this handoff.** Record any subsequent crop reply in the decision file before proceeding. The stills are not complete-motion clearance: measure hair every 0.25 seconds across affected source ranges before applying crops. Keep each presenter crop fixed, with no animated drift.

## Approved choices to preserve

- **Color C, Deeper Contrast and Tan, approved throughout.** Dan's final words: "Let's apply that throughout the video. That is looking really good. That is up to the Muhammad standard." This supersedes his earlier request in the same review for more vivid color. Use `W/round2/recipe/grade-C.cube`, decoded as BT.709. Do not redesign or oversaturate it again. Check source-to-source matching on C1698-C1700 without silently replacing this look.
- **Audio B, subtle bass, approved.** Dan: "Let's lock in B for the audio." Use the exact audition recipe and accepted sound, not a new voice design. Details: `round2/review/audio/comparison.json`, `round2/recipe/audio_and_review.py`. The shared chain used previous source EQ plus `bass=g=0.9:f=150:width_type=q:width=0.7`; the audition was then reduced 0.9 dB to level-match A. `subtle-bass-level-matched.wav` is the chosen listening sample. Apply through shared `voice_chain.py` to the full relevant speech, then verify exact-file audio. Creative approval does not erase the short audition's tone/spread diagnostic findings or authorize threshold changes.
- **Blue Glass selected as the design direction**, but its existing execution is not approved. The main weakness is basic/static graphics. It needs professional moving backgrounds, image motion and purposeful staged reveals.
- **P02 real photo selections approved**, layout rejected. Keep the three selected reference-ad photos, but use improved Blue Glass. Their later result placement around 02:29 is approved.
- **Both family photos F01/F02 approved**, back to back around 01:04. Both exact source previews are in `round2/previews/`. Do not use only the first.
- **P04-lock phone goal clip approved exactly.** `round2/previews/P04-lock.mp4`, clean source from Muhammad Ad 10 93.40-95.05, slowed to about three seconds. No kitchen trailer. Fit the longer slot with a deliberate hold if required, without changing approved identity/source.
- Previously approved **before photograph and disclosure, archive full YouTube page, and same-person goal-generation sequence** remain approved. The goal demo's use around 03:01 is reaffirmed as the right clip and timing. The before graphic's timing around 00:36 is approved; layout still needs Blue Glass.

## Opening revisions, timestamps refer to round-2 sample

Do not treat these as new source timecodes. Fixing the 01:53 pause will move later output times: preserve the spoken anchors, rebuild the source/output map and SRT, and report the revised timings.

| Round-2 position | Required change |
|---|---|
| 00:00 | Hook placeholder placement approved. H2 is selected and motion generation authorized; see below. |
| About 00:13 | Replace the early real-photo montage with an AI prospect customer journey: overweight man discovers the AI app on his phone, experiences a breakthrough, tracks calories, works out and loses belly fat over time. Design one coherent same-person sequence for here and later functionality demonstrations. Dan explicitly permits that reuse. The later real-photo montage stays. Prepare new frame pairs for this new sequence before motion. A short early excerpt can tease a longer later sequence; do not cram all stages into five seconds or imply instant results. |
| About 00:24, P06-early | Remove the list-of-numbers salmon placeholder at this early position. Propose an existing generated clip of the white adult male prospect with six-pack abs working out or meal prepping. Search existing approved AI assets first; show an exact short moving preview before inserting a new selection. This does not reject the later native food-tracking clip. |
| About 00:36 | Keep before-photo timing; replace layout with the approved moving Blue Glass system once selected. |
| About 01:04 | Use both approved shirt-on father/daughter photos consecutively, inside the new graphics treatment. |
| About 01:15 | Keep the tight zoom; reduce headroom by lowering the crop as selected in the crop checkpoint. |
| About 01:47 | Add an AI illustration of Dan at an impressive multi-screen computer setup, prompting and reprompting and comparing five AI models, working out the formula. Preserve recognizable Dan identity from real reference imagery. Produce START and END frames for approval, then motion only after those new frames are approved. |
| About 01:53 | Dan identifies junk: an unnecessary pause before speech resumes. Inspect the exact footage/audio, remove the dead pause while preserving complete words and the thought, smooth the join. Run the shared junk-footage checks and an actual listen across the entire revised sample so similar pauses are caught. Do not confuse the older verified false-start repairs with this new rejection. |
| About 02:29 | Real-result photo placement/timing approved; keep the selected photos in improved Blue Glass. |
| About 02:52 | Add lower third with exact text **"One AI got me back in the gym."** Build matching lower thirds for the subsequent spoken key points, timed to those points. Establish the template first. This explicit requested wording takes precedence over general key-point-copy guidance. |
| About 03:01 | Keep the approved goal-generation clip and spoken placement. |

The current opening is 3:09.0555 to finish a complete sentence. Keep a natural complete-sentence ending after the pause repair; do not cut a word merely to reach exactly 3:00.

## AI motion Dan has now explicitly authorized

These were approved after viewing round-2 endpoints. Do not ask him to choose the same unchanged frames again. Generate **real moving clips**, not frame slideshows or pan-and-hold substitutes.

1. **H2 Life-Size Plan**: `round2/hooks/H2-start.png` and `H2-end.png`. Five-second opening: tangled workout, meal and sleep pathways organize; the prospect begins lifting. Preserve the same person/environment.
2. **B01 three AI roles**, called BL1 in Dan's response: the H5 Invisible Pit Crew pair, `H5-start.png` and `H5-end.png`, also shown in `round2/stills/B01-ai-team-pair.jpg`. Convey AI trainer, nutritionist and meal planner, not human staff. Current B01 picture slot in PLAN-B is 68.8021-75.9092; plan a suitable supported motion duration and fit it naturally. Do not silently regenerate different endpoints.
3. **G03 progress over time**, called GO3: H4 Calendar Corridor pair, `H4-start.png` and `H4-end.png`, shown in `round2/stills/G03-trial-progress-pair.jpg`. He uses workout, sleep and calorie tools, then improves over time. H2 now owns the opening, so H4 can own this later progression. Keep the exact title **"Try AbsByAI free for 7 days."** Do not imply the body change takes seven days. Recorded price speech stays; deleted price/renewal/cancellation graphics stay deleted.

Use the saved approval hashes in `round3-crop-review/round3-decisions.json`. Supporting generated frames remain disclosed as AI-GENERATED in the video. Check generated clips for actual movement, identity, hands, objects, smoke/fog, and usable start/end joins.

**Additional body-scan hook concept, frames only:** a ripped adult man in the prospect demographic, six-pack visible, undergoing an impressive high-tech scan. End frame has readable arrows/callouts pointing to shoulder, stomach and head. Requested example text:

- "Add deltoid volume to make waist look smaller."
- "Deploy fasting for more fat loss."
- "Deploy sleep coaching for better recovery."

Small, sophisticated-looking detail is allowed, but the callouts must remain readable. Prepare START/END frames; do not replace H2 or generate this alternative's motion without selection. This is an AI visual concept, not a diagnostic assessment of a real person.

## Graphics system to establish

Show several Blue Glass motion directions with actual five-to-ten-second moving previews, using the before image, approved result photos, family photos and CTA. Candidate approaches can include restrained moving blue light/gradient depth behind frosted panels, subtle parallax of layered photo cards, and a premium blue footage/texture backdrop. Demonstrate full screen, left third/phone and lower third as one family. Avoid static fields, empty oversized cards, crude frames, gratuitous decoration and numbered circles used in place of real imagery. No swipe sounds. Compare actual Muhammad moving examples, not just static color palettes.

Use full screen only when the picture/content deserves it. For compact information, leave Dan visible and use a lower third or a left-third panel. For app usage, prefer a credible vertical phone on the left with Dan on the right. Content inside the phone may play a horizontal exercise video within the vertical screen.

## App and supporting asset changes

| ID | Next treatment |
|---|---|
| P05 workout | Left-third vertical phone. Show customized workout built around the member's starting point; show a choice of several polished AI exercise thumbnails, tap one and play its horizontal video inside the vertical phone. Keep Dan visible. Match exercise name and plan; no stick figures anywhere. |
| P06 later food demo | Keep the approved native salmon interaction, but extend to **Log Meal**, then show that meal logged and added to daily totals with earlier calories already present. Inspect the complete native recording first. If absent, create an internally documented simulation or safe controlled capture. Do not contaminate Dan's actual food history to obtain the shot. Keep app usage inside a phone/left-third treatment. |
| P07 recipes | Simulated phone usage: three recipe choices in the app; tap one and reveal matching appetizing meal image and simple recipe beneath; tap the next and reveal its own image/recipe beneath. Keep Honey Soy Chicken and Tex Mex Beef Rice Skillet; add a sensible third visible option. No large full-screen recipe card. |
| P08 sleep | Rebuild as sophisticated phone usage. Top shows one night's Oura-style sleep breakdown using colorful horizontal bars for total sleep, REM, deep sleep and other useful categories. Under it, the prospect types one or two sentences about bedtime, alcohol and dinner; then a concise useful coaching response appears. Use internally documented illustrative data, not Dan's private health log. |
| P09 homepage | Real homepage scrolling slowly and smoothly inside a vertical phone on the left; Dan remains visible on the right. Replace the seven jerky still-scroll steps with a proper smooth capture or honest smooth composition from actual captured page content. Avoid banned screens, private details and stick figures. |
| P10 closing | Reject the static-looking CTA. Blue Glass with clearly visible restrained background motion and purposeful text entrance. Keep the viewer's next step central; no Dan result photo. |
| G-motivation | Kill the full-screen card. Use a lower third. |
| G-split and G-total | Delete both graphics entirely. Preserve the recorded discussion. |
| G-lagging | Bullet-point left third alongside Dan, not full screen. |
| G-oldwork | Moving Blue Glass with three relevant pictures: a slightly overweight frustrated man weighing food, looking up/checking the food, and adding calories with a calculator. Use one consistent prospect where appropriate. Replace 1/2/3 circles with the imagery. |
| G-preferences | Retain the idea, use images and Blue Glass motion instead of numbered circles. |
| G-simple / One App | Retain the idea, images and Blue Glass motion instead of numbered circles. |
| G-generic | Delete it. Dan says it adds no value. Preserve the spoken first-AI-attempt story. |
| G01 hours and G02 benefits | Retain approved 3 versus 165 content and five-benefit idea. Adapt to the new system; benefits remain a left third. |

**No "PROPOSED FEATURE PREVIEW" text on these video graphics.** Dan expressly requested its removal for recipe/sleep and the phone-feature treatment, because he intends those features to exist before prospects see the video. This overrides the prior round's visible prototype label. Retain truthful internal source metadata: simulated UI, illustrative data, feature readiness unverified. Do not claim a live integration was verified or deploy app features. Public release remains outside this task. Retain required AI imagery disclosures; removing a prototype banner does not remove those.

## Files, verified work and unresolved technical findings

- Current review sample: `W/round2/sample/DRAFT - WV-01 round 2 - first three minutes.mp4`, and `DRAFT - WV-01 round 2 - REVIEW 540p.mp4`, 5666 frames at 30000/1001. Both exact-file audio gates PASS. Source/output map and SRT are beside them.
- Repaired source maps: `W/selection/EDL-A-REPAIRED.json`, `EDL-B-REPAIRED.json`, `W/drafts/PLAN-A.json`, `PLAN-B.json`. Do not revert to unrepaired selected maps.
- Six B callbacks remain mandatory, currently at 273.607, 444.778, 478.678, 546.079, 767.934 and 852.218 seconds before this round's timing changes. Preserve source ranges and complete words when remapping.
- Round-2 generation/source records: `round2/placeholders.json`, `round2/review/source-register.json`, `file-manifest.json`, `QA.md`, `round2/recipe/`. Approved-source decisions from this feedback supersede their stale pending labels; do not rewrite the historical reviewed media.
- Both previous full A/B drafts still fail the silence row. Dan has now rejected a specific opening pause, but do not assume it is the same full-film gate cause. Inspect and repair proven issues, then rerun exact-file checks.
- Full regression corpus remains FAIL after 2736 seconds: `ds17-r4-final-approved` artifacts mismatch and historical NOT MEASURED gaps. `W/review/website-srt-corpus.json` and associated logs preserve it. Do not rerun the whole corpus blindly or alter thresholds.
- Unshipped shared edits remain in `_shared/deliver/{formats.py,gate.py,README.md}`, website caption test, and `scripts/edit-queue/asset_approval.py` plus its test. Do not commit these as validated. Other edits belong to RO-05/DS-18 and must remain untouched.
- Existing `round2/placeholders.json` is an internal inventory, not a validated queue-owned packet. Update a new revision's approvals, hashes, exact slot durations and source records honestly. Do not claim queue validation or delivery PASS for a placeholder draft.
- Renderer cache trap: the round-2 talking-head cache key does **not** include the crop/filter string for source shots. Changing the crop or grade in the old script can reuse stale shot files. Use a new cache namespace or include source-frame range, crop, grade hash and filter in every picture key. Rebuild only affected scenes/joins.

## Cost, ownership and closeout

No generation was run while writing this handoff. Prior estimated Gemini QC is $1.95112 + $0.216162, plus an unresolved older failed call capped at $0.1333. Ten hook endpoints and two food images were generated with built-in imagegen; its charges were not reported. Generation cost and editor tokens are unknown, not zero.

Dan now explicitly requests H2/B01/G03 generation after the review disclosed the unknown still charges. Preserve that authorization and do not repeat frame-approval questions. Before the batch, state the real provider estimate, reconcile available spend records and preserve any unavailable amount honestly. Do not treat a new task as resetting the $5 per-video generation cap, session cap or retry costs. The prior $1-per-clip planning allowance was not a provider quote. Any genuinely additional authorization required is for a stated budget, not reapproval of unchanged concepts. Gemini QC has its separate standing allowance.

One owner edits through self-QA. Keep at most two local video pipelines across all tasks; DS-18 may be rendering concurrently. Keep dispatcher PAUSE. Use one independent full-candidate reviewer only when a complete placeholder-free candidate exists, not for this creative checkpoint.

Preserve recipes, media and private production records on the SSD and local `codex/video-trial-plan-private`, not the public repository. Permitted public changes are handoff/status documents only. Update the master/Drive queue and verify its visible status; no app deployment. Finish the next task with a single review page and concise choices for Dan.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20260925-wv01-round3-lock-crop-and-graphics.md` and required production rules. Execute WV-01 round 3 with `$abs-edit-organic` as a 16:9 website VSL. First lock Dan's wide/tight crop using the saved screenshots and any subsequent choice. Preserve approved color C and audio B. Establish professional moving Blue Glass full-screen, left-third phone and lower-third templates, then revise only the opening sample. Generate the expressly approved H2, B01 and G03 motion, prepare the new customer-journey, body-scan and Dan-at-computer frame concepts, apply all asset/phone-UI and junk-pause feedback, and retain approved sources plus six B callbacks. Respect budgets, the two-build cap and unresolved gates. Do not build the full films, publish, replace site videos or deploy app features.
