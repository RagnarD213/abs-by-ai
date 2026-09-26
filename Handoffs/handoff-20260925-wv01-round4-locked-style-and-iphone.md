# WV-01 round 4: locked style, credible phones and revised AI scenes

Written 2026-09-25 from Dan's complete round-3 review. Recommended model: **GPT-6 Astra, High**. Use `$abs-edit-organic`, adapted to this 16:9 website VSL. This document supersedes the open actions in the round-3 handoff. It records the next task; no round-4 rendering or generation happened while writing it.

## Goal and boundaries

Deliver a revised opening and one consolidated graphics/AI review package. Preserve the parts Dan likes, implement every revision below and make the remaining scene decisions easy to review in context. Finish the opening before rebuilding complete A/B films. No publishing, website-video replacement, app-feature deployment, automatic dispatcher launch or new dashboard row.

Read the project instructions, `.claude/skills/_shared/VIDEO-RULES.md` in full, its new `GRAPHICS-STANDARDS.md`, `Handoffs/video-editing/00-RULES.md` including the Codex environment table, the invoked skill, current coordination board and WV-01 queue row. Then read the prior round-3 handoff for underlying sources and the original `WV-01-EDIT-PLAN-20260924.md`, research and source map in `Handoffs/video-editing/` as needed. Current feedback here overrides older instructions and stale pending labels.

Work root **W**: `/Volumes/Extreme/_edit_work/wv01-edit/`. Read `W/STATE.json`, `W/round4-plan/decisions.json`, `W/round3/QA.md` and `W/round3/review/source-register.json`. Keep reviewed media unchanged; build under a new `W/round4/` directory. The local round-3 review is `http://127.0.0.1:8766/round3/index.html`. If necessary restart `W/round3/recipe/serve_review.py`, retaining HTTP byte-range seeking and `preload="none"`. Do not preload all 39 videos, which previously crashed the embedded browser.

## Locked choices and approval boundaries

- **W2 wide:** `3552:1998:144:162`; **T2 tight:** `2608:1466:616:184`. Keep fixed presenter compositions. Recheck moving clearance in changed layouts.
- **Color C and audio B remain approved.** Dan again said the color looks great and audio sounds great. Grade: `W/round2/recipe/grade-C.cube`, BT.709. Audio uses the shared chain with the accepted EQ plus `bass=g=0.9:f=150:width_type=q:width=0.7`, then the approved 0.9 dB level reduction. Do not redesign either. These coefficients are specific to this shoot.
- **Soft Blue Light, option 1, is the locked graphics style for this video and all website videos.** Use `round3/recipe/blueglass.py` style 0 and the approved moving references. This does not approve rejected photo sources, phone borders or opaque list panels within that demonstration.
- **Motivation lower-third format is locked for all lower thirds in all videos.** Keep its pre-header hierarchy, accent, glass strip and movement. Revised gym text is exactly `#1 AI got me back in the gym`, with `MOTIVATION` above it. Do not retain the word `One`.
- **G-oldwork manual food tracking and G-preferences are approved.** Reuse unchanged.
- Existing real before photograph, both F01/F02 family photographs, full YouTube archive proof and exact P04 goal-generation sequence remain approved. Keep all disclosures and source identities.
- P05 workout, P06 food tracking, P07 recipes and P09 homepage **inner content** is approved. Their outer phone treatment is rejected. P08 sleep requires the content revisions below as well as the new device.

Approval hashes and scoped review evidence are saved separately; creative acceptance is not a full-film delivery PASS. Do not ask Dan to approve unchanged approved components again.

## Opening and photo revisions

Times are approximate round-3 output positions, not source timecodes. Anchor changes to the heard words and regenerate the output map and SRT after timing edits.

1. **About 00:20:** show a couple of horizontal real result photos consecutively, like Muhammad Ad 1. Inspect that actual moving reference for pacing and presentation. Dan first called them his after pictures, then later said "before pictures at 20 seconds." Working interpretation is the real result photos he initially requested, with the consecutive horizontal treatment. Verify against the spoken line; do not silently replace the separate approved 200-pound before-photo beat around 00:36. His new photo request supersedes any overlapping earlier customer-journey allocation.
2. **About 02:27:** keep the three-picture format and placement, but replace the mixed-aspect source set with **three vertical portraits** that fill the tall frames. Choose maximally ripped, smiling or strong natural expressions, no slumping, frowning or awkward expressions. This overrides earlier approval of the three specific source selections. Always use three portraits in this format; horizontal photos play sequentially. Preserve complete heads/abs and truthful labels.
3. Keep the intro's otherwise approved placement and rhythm, including both family photos and the goal sequence. Change only the explicitly revised slots and any necessary adjacent joins.
4. Apply the new numbered gym lower-third copy. Use the approved format for subsequent numbered points, grounded in the actual narration.

The current master is `W/round3/sample/DRAFT - WV-01 round 3 - opening.mp4`; the adjacent `DRAFT - WV-01 round 3 - REVIEW 540p.mp4` is the lighter review. Duration 188.354833 seconds, 5645 frames at 30000/1001. The 21-frame pause repair before "And slowly" is already done and sounds complete. Preserve it. Full-film A/B plans have not yet received that timing change.

## AI scenes: exact authorization per item

| Item | Decision and next action |
|---|---|
| **C01 five AI models** | Approved and **motion generation explicitly authorized**. Use `round3/frames/C01-start.png` and the corrected `C01-end.png` showing the intended three-monitor setup. Never use `C01-end-r1-rejected-monitor.png`. Preserve Dan's identity and readable purpose: prompting, comparing and refining five models. |
| **SCAN body-scan alternative** | Concept approved. Add a fourth callout at lower right, pointing to the right side of his abs, with exact text **"Train transverse abdominis to tighten waist."** Preserve the existing shoulder, stomach and head callouts. Edit `round3/frames/SCAN-end.png`, check readability/arrow target, then **generate motion as explicitly authorized**. The requested edit does not require another permission stop. Use imagegen for editing the frame. |
| **H2 life-size plan** | Dan likes the generated `round3/motion/H2.mp4`. Show it **side by side with the new moving SCAN alternative**, matched to the same opening narration and duration, so he can select the opening. Do not silently replace H2 before that comparison. |
| **J1/J2 customer journey** | Existing start/end frames approved, but the transition is insufficiently explained. Preserve `round3/frames/J1-{start,end}.png` and `J2-{start,end}.png`. Make intermediate images and a clear storyboard before generating motion: same prospect begins using the app, repeats workout/food/sleep behaviors and improves over visible calendar progression. No instantaneous body morph. Show the new intermediate frames in one batch for review before motion. Keep this available for its later functionality placements if the new 00:20 photos displace the early excerpt. |
| **B01, dictated BO1 / three AI roles** | Generated clip rejected. Create **new START and END frames** of three identifiable cyborg coaches side by side: AI trainer, AI chef/nutrition coach and AI sleep coach. They emerge from a phone with symbols. Suggested readable sleep identity: moon/sleep-wave symbols, sleep-metric display and wearable/sleep equipment, not an indistinct third robot. Keep all three visibly cyborg and distinct. This replaces the old trainer/nutritionist/meal-planner role set. Show new frames before motion. |
| **G03, dictated GO3** | Current interpretation rejected. Create **new START and END frames** grounded in the actual later CTA speech, with a visibly understandable connection between app use and progress over time. Check PLAN-A/B and the spoken source before designing it. Show workout, food and sleep support coherently across weeks/months, not just corridor walking, shirt removal or a changed body. Keep the trial distinct from the time needed for results. Exact CTA remains `Try AbsByAI free for 7 days.` Show the new concept/frame pair before motion. |
| **P06-early existing workout option** | Not yet selected for the film. Dan specifically authorizes an **in-context audition**: place the exact proposed excerpt in its early slot and provide the surrounding narration/presenter footage, about ten seconds of context around it. Include roughly five seconds before and after where practical. Do not show only the isolated clip again. Reconcile its placement with the new early horizontal-photo sequence. |

P06-early exact preview: `W/round3/previews/P06-early-existing-option.mp4`, 2.8028 seconds from source 11.5-14.3028 in `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/ai-motivation-lockscreen-sequence.mp4`. It shows the gray-shirt prospect doing a dumbbell row; his abs are covered. Use the real short action then return to Dan rather than stretching it to fill the old eight-second slot.

Generate real motion for authorized scenes, not endpoint slideshows or long held frames. Use exact-duration labelled placeholders for choices still awaiting new-frame review. State estimated paid cost before running a batch; keep the existing $5 WV-01 motion budget and project limits unless Dan extends them. Do not rerun an approved clip merely to obtain another option. Keep generated-media disclosures.

## Replace the phone shell, preserve approved demonstrations

Dan rejected the current device as a square rectangle pasted into a phone. Build a credible modern iPhone with rounded outer body and rounded screen masking, consistent bezel and an integrated Dynamic Island/sensor treatment. His description included "a dynamic island and a notch"; use one coherent modern iPhone design, not two incompatible sensor cutouts. No rectangular corner spill or nested phone. Keep the phone on the left and Dan clearly centered in the remaining right space, with his arm intact throughout moving footage.

Make one short working phone prototype using approved P05 content, inspect full-size moving corners and screen fit, then apply the same treatment consistently across all revised demos for the consolidated review. Preserve the inner scenes rather than redesigning the accepted interactions.

| Item | Content to retain or revise |
|---|---|
| **P05 workout** | Exact approved workout preview/content, including the existing exercise clip. Reference `round3/previews/P05-workout.mp4`. Source demonstration is `Media/exercise-demos/db-goblet-squat/db-goblet-squat-AIDAN-narrated-FINAL.mp4`. |
| **P06 food tracking** | Exact latest `round3/previews/P06-log-meal.mp4`, 11.011 seconds. Keep analysis, Log Meal, settled confirmation and totals 620 then 1,395 after logging 775. Use the final tracked-total recipe, not earlier rejected versions. |
| **P07 recipes** | Exact approved `round3/previews/P07-recipes.mp4` contents and interactions, three choices and matching recipe results. |
| **P08 sleep** | Use **all Oura sleep contributor bars**, including timing and restfulness, in the colorful graph. Verify the complete current official list rather than guessing or retaining only duration/REM/deep sleep. Enlarge the graph and first text bubble, adding more believable context text. At the bottom show **"Here are a few tips to improve your sleep for tonight"** as the lead-in to the response; the tips themselves must be below the visible viewport. No actual tips visible in the video. Preserve internally documented illustrative data. |
| **P09 homepage** | Exact approved smooth homepage content from `round3/previews/P09-home.mp4`, inside the new device. |

Implementation references: `round3/recipe/phone_assets.py`, `round3/review/phone-provenance.json` and `phone-final-verification.json`. The native salmon source `Media/codex-video-trial/06-organic-r3/assets/salmon-phone.mov` already contains a phone treatment; isolate the inner viewport so the replacement is not a phone inside a phone. Keep the final template-tracked totals synchronized during scrolling. No changes to Dan's actual food history.

The website capture is `W/round2/stills/tools-live-0.png`. P05/P07/P08 include simulated UI; internally retain that provenance and unverified feature-readiness status. The visible prototype banner remains removed at Dan's instruction. Required AI imagery disclosures still apply.

## Remaining graphic revisions

- **G01, three hours versus 165:** return to the earlier array of little horizontal bars, with only three highlighted, on the new moving Soft Blue Light background. Eliminate the bottom progress bar. Earlier visual references: `W/assets/graphics/G01-week-trainer.png` and `G01-week-remaining.png`. Dan explicitly requested **165 little bars with three highlighted**. Preserve that requested count in the revision, while retaining the 3 versus 165 spoken distinction. The old plan used 168 cells for a literal week; do not silently substitute its count or label a 165-bar illustration as an exact 168-hour ledger.
- **G02 five benefits:** remove the panel background, use a bullet list, make text larger and bolder. Center Dan in the remaining right-hand space. His head should be roughly equidistant from the graphic and right edge; do not cut off his arm/body.
- **G-lagging, Find the Gap:** same larger/bolder bullets, no background panel, Dan centered safely on the right.
- **G-simple, One App:** remove title and background. Show only the credible iPhone beside Dan, with the same fixed, safe right-hand composition.
- **G-oldwork and G-preferences:** approved, reuse unchanged.
- Keep earlier deletions: G-split, G-total and G-generic remain deleted; keep their underlying speech. No renewed price/renewal/cancellation graphics. Preserve exact approved CTA wording.

Reframe side layouts deliberately using the available source pixels. Do not animate Dan to recenter him. Check his moving arms and head throughout each affected passage, not just the first frame.

## Evidence, work state and checks

The reusable rules were updated in `.claude/skills/_shared/GRAPHICS-STANDARDS.md`, linked from VIDEO-RULES, website-video and the shared Codex standards. Both installed Codex adapters are symlinks to `Media/codex-video-trial/skills/`; their common standards file is `Media/codex-video-trial/05-recipes/shared/standards.md`. No install step is needed. New scoped approvals/rejections are in the shared corpus with pending semantic checks, not fake automated passes.

Preserve the repaired full maps `W/selection/EDL-{A,B}-REPAIRED.json` and `W/drafts/PLAN-{A,B}.json`. Six B callbacks remain mandatory. Preserve their source words and remap output times if the accepted opening pause cut later propagates into full films.

Round-3 opening master and review audio gates PASS; junk verifier found zero confirmed repeats/high unresolved candidates; the full audio listen confirmed complete words. Hair sampled every quarter-second across 508 selected source points had minimum 24 source pixels of clearance. These are previous findings, not a substitute for checking the revised output.

Prior full A/B drafts still fail silence. Shared audio self-test has six failures; the full regression run failed on ds17 artifact mismatch and historical NOT MEASURED gaps. Do not claim these passed, relax thresholds or rerun the expensive whole corpus blindly. Shared delivery/ASCII-placeholder changes and unrelated concurrent work remain uncommitted and unvalidated; do not include them in this task's commit. No independent complete-film reviewer should review a placeholder draft.

Cache warning: the old talking-head cache omits the crop/filter string. Use a fresh round-4 namespace or include source range, crop, grade hash and filter in the key. Reuse accepted source/audio assets by fingerprint; rebuild only affected picture layers and joins. Limit concurrent video builds to two.

Known round-3 provider estimate: $0.443897 motion plus $0.35275 QC, about $0.80. Prior QC $2.167282 and an older failed-call upper bound $0.1333 remain separate. Ten round-3 built-in still calls plus twelve earlier stills have unreported charges; do not call them free or zero. Editor/reviewer token measurements are unavailable. No generation spend in this documentation task.

## Deliver in the next task

One review page with: revised opening; H2 versus SCAN in matched opening context; early workout in context; authorized C01/SCAN motion; J1/J2 intermediate storyboard and new B01/G03 frame pairs; corrected phones and sleep viewport; revised photo layouts, bar grid and side lists. Preserve approved components and identify only decisions still needed. Update source hashes, decisions, exact timings, SRT, costs and the work packet. Keep placeholders explicit. Stop at this review checkpoint before the full A/B finish.

The dispatcher remains paused. Queue state stays parked with a handoff note; it is not an invitation to launch unattended work. No new task was created automatically.

**Starter prompt:** Execute `Handoffs/handoff-20260925-wv01-round4-locked-style-and-iphone.md` with `$abs-edit-organic`. Preserve W2/T2, color C, audio B, Soft Blue Light and the Motivation lower-third format. Apply my round-3 feedback, generate the authorized C01 and revised SCAN clips, prepare the new storyboard/frame choices, and deliver the round-4 opening and consolidated review package.
