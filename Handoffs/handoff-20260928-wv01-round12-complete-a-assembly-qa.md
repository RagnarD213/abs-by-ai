# WV-01 round12: complete A assembly and final review

Prepared 2026-09-28. All creative choices are locked. Dan requested this handoff for execution in a new task. No assembly, new task launch, generation or provider spend occurred while preparing it.

Recommended model: GPT-6 Sol, High. The existing recipes and assets cover the work; the main challenge is assembling the correct versions, preserving the accepted sound and verifying the complete timeline.

## Goal and authorization

Assemble one complete A, approximately 12.5 minutes, from exact approved components. Complete editor self-QA, current exact-file checks and one independent complete-candidate review. Deliver a complete A review copy and sidecars for Dan's full-film verdict. Do not make separate five-minute or ten-minute cuts.

Dan's latest decisions, 2026-09-28:

- "Five benefits build looks good. Let's lock this in"
- "Mirror, joint, and pool closing look good. Let's lock this in"
- "Viset twist clip looks good. Let's lock this in."
- "Everything is locked in and we're good to make the full assembly Create a handoff document to do that in a new task"

The mirror sentence approves the mirror join and pool closing item shown on the review page. All remaining creative decisions are closed. Do not ask again for unchanged opening, graphics, motion, clip choices or permission to assemble. These are scoped creative approvals, not approval of an unseen complete film or numerical gate PASS.

B stays deferred. Preserve `scripts/edit-queue/PAUSE`. No publishing, upload, website-video replacement, application changes/deployment, automatic new task, new dashboard row or new image/motion generation. Use existing assets.

## Read, ownership and authoritative records

Project root R: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Working root P: `/Volumes/Extreme/_edit_work/wv01-edit`.

Use `$abs-edit-organic`, specifically `Media/codex-video-trial/skills/abs-edit-organic/SKILL.md`, and read its linked standards, workflow and runner instructions. Read `.claude/skills/_shared/VIDEO-RULES.md` in full, `GRAPHICS-STANDARDS.md`, `PRE-RENDER-APPROVAL.md`, `AI_COORDINATION.md`, `Handoffs/video-editing/00-MASTER.md`, `00-RULES.md` and `P/STATE.json`.

Verify no other owner is implementing WV-01, then claim this task. Work in new `P/round12/`, preserving historical candidates and recipes. Check the machine-wide two-build cap before render, transcription, heavy QA or watch work. Let the existing edit queue own long build waiting where supported, without resuming the dispatcher. Do not launch an automatic editing/reviewer loop or poll unchanged logs with model turns. Persist the packet and park in a supported state when awaiting a worker.

Read these authoritative records in this order:

1. `P/round11/review/dan-review-locks.json`: latest three exact contextual approvals, installed phone component/source and mirror/pool asset hashes.
2. `P/round10-plan/dan-review-locks.json`: prior opening, before, laptop, portraits and exact3A approvals.
3. `P/round11-plan/decisions.json`: all choices locked, pending list empty; previous pending media retained as historical evidence.
4. `P/round11/WORK_PACKET.json`, `review/contexts.json`, `QA.md`, `review/qc-adjudication.json`, `review/costs.json`.

Latest review: `http://127.0.0.1:8766/round11/index.html`. Its approved previews are unchanged byte for byte. The review page and current packet now mark the choices locked. Older scripts, earlier handoffs and cached records can still say pending; the latest lock record supersedes them. Do not rerun `round11/recipe/page11.py`, which generates the historical pending packet.

## Preserve the exact approved ingredients

- Opening: `P/round10/sample/DRAFT - WV-01 round 10 - opening.mp4`, 5631 frames, 187.8877 seconds. Preserve accepted colorC, framing, speech, picture timing and AAC. Only its phone picture is superseded by the approved V sit twist replacement. No new calibration or opening variants.
- Before: `P/round10/graphics/before.mp4`, output1079-1324, 36.002633-44.177467 seconds. Exact approved title, body, weight, real-photo disclosure and extended hold without stretched narration.
- Laptop: `P/round10/graphics/laptop-insert.mp4`, output2829-2986. Fixed12percent crop from approved native round9 motion, natural speed, intact hair/gesture and disclosure. No regeneration or animated crop.
- Portrait trio: `P/round10/graphics/portrait-results-final.mp4`, output4293-4477. White23, exact blue173, blue240; existing gradient, proportions, plural disclosure, title/subtitle and entry.
- Exact left-third3A: moving reference `P/round10-opacity/previews/option3-A-context.mp4`; recipe `P/round10-opacity/recipe/build.py`. NavyRGBA(10,38,72,232), full-opacity cyan title/plain cyan numbers, white body/divider, title60/body38, bubble(36,42,752,789), equal37px visible top/bottom padding. Context7717-8528, graphic7886-8304. Recover the graphic layer from the recipe/source plates and composite at the mapped boundaries. Do not paste the whole context across unrelated scene boundaries. Alpha249/current and alpha218/3B are historical alternatives, not approved substitutes. Keep presenter fixed and arms intact.
- Phone: `P/round11/graphics/early-app-flow.mp4`, output779-958, 25.992633-31.965267 seconds. Exact source `P/round11/assets/1-v-sit-twist-SILENT-VSL.mp4`, matching `R/Media/exercise-demos/_batch5/review-set/1-v-sit-twist-SILENT-VSL.mp4`. Upright phone/list/tap, then natural-speed landscape player and matching V Sit Twist name/instructions. Source0-4.422633seconds after1.55seconds of list/tap. Locked context: `P/round11/previews/v-sit-twist-context.mp4`. This supersedes the earlier Crunch picture only.
- Five benefits: `P/round11/previews/benefits-entire-build.mp4`, byte-identical carried round8 build. Context A447.2468-494.9945 seconds,1431frames. Preserve sequential reveals, returns to presenter, all five labels and existing design. Do not automatically apply3A opacity/layout to this separate component. Source recipes: `P/round8/recipe/revised_components.py` (`benefit8`) and `build.py`; exact reveal intervals in round11 contexts.
- Closing: `P/round11/previews/mirror-pool-context.mp4`, exact final carried round8 context, A709.642233-745.511433 seconds,1075frames. Complete Tonight entry, tighter mirror audio join and full pool motion are now approved. Mirror: `P/round7/motion/mirror.mp4`; pool: `P/round8/motion/pool.mp4`, exact round8 attempt3. Recipes: `P/round8/recipe/payoff.py`, `finish_context_edges.py`, `finish_payoff_edge.py` and associated receipts. Historical shirt/hand QC flag was unconfirmed; Dan approved this moving context. Do not reopen it merely because that old flag exists.
- Preserve exact approved M100 original288-295seconds with full YouTube-page treatment, J1, G03, B01, SCAN, C01, W2/T2, training/food/sleep treatment, Motivation lower third and final invitation. Later exercise clips from Claude remain optional future substitutions, not dependencies.

Reverify pinned hashes before editing. Keep one short authoritative requested-change/preserve list and record cache reuse for scenes, accepted audio, transcripts and assets.

## Assembly source and timeline

Start from `P/round11/review/PLAN-A-CONFORMED.json`. It explicitly selects3A, installs the V sit twist component and has `round11_pending: []`. Current A map is54segments,22590frames,753.753seconds at30000/1001fps. This is a working assembly plan, not a finished export.

Reuse `P/round10/review/full-A-conformed-words.json`, `INTERNAL - A conformed working subtitles.srt` and `.vtt`, opening source/picture maps and receipts. Refer to round10 `storyboard-timing.json` and `map-caption-validation.json`, plus round9 full-A references where the current recipes link them. Historical round7/round8 override paths and callback-pending wording remain in the plan; resolve current component precedence deliberately. B callbacks stay deferred and do not block A.

The previous65removed narration frames are already applied once, including the approved tighter mirror join. Do not apply removal operations a second time. Do not reconstruct from an old placeholder full master or blindly execute historical full-draft scripts. Assemble from the conformed source map, verified clean scene caches and exact selected layers. Build an isolated reproducible recipe for complete A.

Preserve the approved AAC opening and accepted later sound as far as the current map permits. The phone change is picture-only. Verify the closing approved join against the source map and context. No added silence, repeated narration, stretched speech or held motion endpoint to fit inserts. Any confirmed additional seam repair must be measured, recorded and reflected in all affected maps, graphics and subtitles; do not silently disturb the locked opening. Creative choices are locked; factual/moving-picture verification still applies.

Remove every placeholder. No running burned captions or watermark. Keep required real-photo/AI disclosures and fixed16:9 presenter composition. Produce a correctly timed SRT sidecar.

## QA, independent review and delivery

Run shared audio selftest and current website-format delivery gate on the exact complete candidate with real measured inputs and current maps. Preserve unmodified gate code and thresholds. The accepted opening audio gatesPASS, but round10 website gate2.3.1 retained framing:push_coverage, captions:card_collision, captions:burned and8unmeasured inputs. Prior full-draft silence failures and corpus artifact mismatch/gaps remain unresolved. Round11 phone excerpt audio flags tone/lufs; its picture gate stalled and was terminated as FAIL/unmeasured. Do not carry these short-context findings forward as a full-film result or remix accepted sound merely to clear window-dependent flags. Recheck the complete file, report real failures honestly and never inventPASS.

Complete chronological full picture review and supported full audio review. Check source-word joins, full syllables, hair/arms/action, static framing, readability/reveals, labels and every inserted scene. Contact sheets or sampled frames alone are not full motion review. Do not claim native listening or a continuous human watch that did not occur. New approvals were recorded in the shared corpus with no invented numerical predicates; no corpusPASS is claimed. Run the regression corpus if any quality gate/settings change is proposed, never tune a threshold to pass this build.

After every selected item is installed, placeholders are absent and editor self-QA/exact-file reports exist, obtain one independent complete-candidate reviewer with one consolidated verdict. The skill explicitly authorizes this independent agent audit. No planner/supervisor loops or repeated automatic reviewer cycles. Preserve the first complete candidate even if it receives corrections; park with the consolidated findings if it does not ship.

Deliver complete1080p A,540p review copy, corrected SRT, accepted/untreated audio comparison, gate A/B, exact-file reports, consolidated reviewer verdict, notes and reproducible recipe. Record actual revision, editor/reviewer model/effort and available token/cache usage; unavailable measurements are null with a reason. Keep the job delivered awaiting Dan until he approves the complete film, not finalized solely because its ingredients were locked. No upload or publication.

Reuse persistent launch agent `com.absbyai.wv01-review`, port8766 and cache `~/Library/Application Support/AbsByAI/WV01Review/round12`. Copy every linked asset; verify served bytes, range seeking and browser playback. No competing server. Private media, fingerprints and recipes stay on SSD/local ref `codex/video-trial-plan-private`. Public main gets only this handoff and WV-01 status/index changes via an isolated Git index; preserve shared checkout/staging and unrelated work. No app deployment for this media task.

## Costs and next action

No new image/motion generation. Known cumulative motion estimate remains$12.824017301463925 of Dan's$20 video allowance, including rejected attempts.47prior built-in still calls have unknown charges. Round10 QC estimate$0.213838; round11 owner-assisted contextual QC estimate$0.123632 from returned tokens, distinct from the independent complete-candidate review. Invoices/editor runtime usage unavailable, not zero. Separate Gemini QC standing authorization applies: state the batch estimate before running, ask only if it exceeds$5, retain actual returned usage. No budget reset.

Next action: verify ownership and all current approved hashes, create `P/round12/` with a short complete-A assembly packet and isolated recipe, resolve the current map/component precedence, then submit the complete build. No creative approval request remains.

Starter prompt: Execute `Handoffs/handoff-20260928-wv01-round12-complete-a-assembly-qa.md` with `$abs-edit-organic`. All creative choices are locked, including the five-benefit build, mirror join/pool closing, V sit twist and exact3A. Assemble complete A from the current conformed plan and exact approved existing components, preserve accepted sound/color, perform full QA and current exact-file checks, and obtain one independent complete-candidate review. Deliver1080p,540p,SRT,comparisons,reports and recipe. Keep B deferred and dispatcher paused. No new generation, publishing or site replacement.
