# AD: Fired Them All AD R3

2026-10-08. Recommended model: GPT-6 Astra, high effort. Use `$vsl-edit`. Dan requested this next-round handoff after approving the revised firing start/end pair. Next task name: **Fired Them All AD R3**.

## Goal and scope

Generate two selected AI motion clips, then integrate them and the R2 picture revisions into the B opening and its short join into approved A. Work in `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round3/`. Preserve round1 and round2.

Deliver an integrated B-opening review, first-minute review and B/A join context. B is 254.921333 seconds/7640 frames; B plus existing A context is 265.031433 seconds/7943 frames at 30000/1001 fps. These durations and accepted narration timing remain fixed.

Do not build complete B, add the six C1700 callbacks, change approved A, make ad format variations, upload, install or publish. Do not reopen approved color/audio or ask Dan to choose the same endpoints again. Finished generated motion still needs his review in context.

First read the complete project VIDEO-RULES, `$vsl-edit`, IMAGE-GENERATION, PRE-RENDER-APPROVAL, GRAPHICS-STANDARDS, CUT-CONTINUITY-QC, shared HyperFrames README and Handoffs/video-editing/00-RULES.md. The original R2 brief is `Handoffs/handoff-20261008-wv01-b-round2-opening-revisions.md`; R2 results are `Handoffs/results-20261008-wv01-b-opening-r2.md`.

## Exact approvals

Private R2 root: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round2/`. Read `review/decisions.json` and `review/R3-asset-lock.json` first. Those contain exact quotes, paths and SHA256 locks.

- Color/audio: Dan October 8, "color Correction, audio is looking good". R1 presenter grade C, source-fitted voice and no music are locked.
- Firing typography/stamp sequence: "The way you did the firing graphics on the storyboard looks good. We just need less fat people."
- Revised slimmer firing start/end: "Okay those new start n-frames look good. Give me the handoff for the next round". In context this approves both displayed endpoints, not just the start. Use firing-revision1, not the rejected heavier people.
- Phone coach A: "Let's go with A, the phone coach, for the second clip illustrating the AI training." Use the displayed phone pair. Robot and digital twin are unselected alternatives and must not be generated or installed.
- A0055/A0043: "Your reuse of the laptop and three-monitor AI clips looks good. Those are approved." This binds the presentations in R2 planning preview SHA256 `7217de202f763364d799225cef4455bc1937b74fec7d61a09193f646c21b7e00`.

The R2 crop, early portrait trio, exact title and join are requested revisions already built and checked. Carry them into the integrated opening as proposed picture revisions. Dan's last messages did not separately approve them or finalize the entire opening. Let him review these and the finished motion together in the integrated candidate.

## Locked motion inputs

All paths in this table are relative to the private R2 root. Verify SHA256 before generation. Composited approval frames are the target appearance. Give the generator CLEAN endpoints, and add the exact labels/type separately using the approved compositor functions.

| File | SHA256 |
|---|---|
| firing-revision1/start.png | `653d76552609d4af090db50c816f9fa6fb57d779d722264891024f80cee5982e` |
| firing-revision1/end.png | `e4bae0070a670e56420c7071c7fd30badb08a764a9e31fa422c9c140ca3c8d83` |
| firing-revision1/start-clean.png | `cf5fe5e550ecd8007a66a67168e5a51df1e45b8812c7dbd7cdfbc6a7e63d1919` |
| firing-revision1/end-clean.png | `881d6ccdc3f6f774efd1b783dc60047cc3eca26d0a0a4ecf7a6d0391bfb3ec44` |
| frames/phone-start.png | `05fdc9ab838eb578c1b3a045d3b33f7ab7674193036551708f74400087449904` |
| frames/phone-end.png | `299f02be0ac4a3d29106108c230d4c1d004c0a368ad46651311f7a3699473e44` |
| frames/phone-start-clean.png | `ab392c17e04deef51bd28d90730ad7e9e7301d81881dd72344bfc514627a7453` |
| frames/phone-end-clean.png | `528d5ac684172a881f040f0883f2263c3bc11dec8b5ac679fd226e73f7763ef4` |

Firing approved storyboard: `firing-revision1/storyboard.jpg`. Approved stamp/disclosure functions: `recipe/frames.py`; the selective function reuse implementation is `firing-revision1/composite.py`. Do not run the old frames.py top-level script to overwrite historical proposals. It executes immediately. Use these exact Fired letters, font, rotation, size and positions on the new motion.

Firing action: fixed 16:9 camera with three equal panels. Same slimmer, average-size, soft untrained trainer, nutritionist and meal-prep worker throughout. Small disappointed reactions, unchanged environments. No heavy physiques, exaggerated reactions, camera travel or new props. Stamp trainer at "personal" 1.11697s, nutritionist 2.35697s, meal prep 3.61697s. "Replaced" begins 4.89697s; transition to phone training there. Resolve nearest native frames from mapped word starts, not arbitrary rounded whole seconds.

Phone action: one controlled right-arm curl by the approved shirtless Dan. Phone/stand and cyan beam remain visibly connected to life-size coach. Coach indicates tucked elbow; left arm remains down, upper arm stable. Natural dumbbell/hand anatomy. Add approved AI-GENERATED disclosure and the exact 1 REP chip near completion in code. No provider soundtrack is installed.

R2 page's 4-second phone duration was a proposal, not an audio trim. Useful narration window: "replaced all three with AI" 4.89697s through "Then I got six pack abs at 40", ending before "Here's exactly how" 9.75697s. Prefer this approximately 4.86-second window if the generated action/transition works naturally. A roughly 5-second source can supply it without stretching. Return directly to the proper static presenter crop. Verify current provider duration/end-frame support; do not choose an 8-second-only path blindly and lose its final pose by trimming. Adjust picture placement against speech if necessary, keeping voice, overall timing and approved action intact. Do not freeze or stretch clips to cover a mismatch.

## Generation and budget

Use the Codex subscription to generate the images. The stills are already approved; no new still generation is planned. If a true endpoint redesign is needed, show it and obtain the changed frame approval before generating that redesigned motion.

AI video uses the project's metered video provider. Verify current start+end input support, durations, price and schema before submitting. A prior keyframe helper exists at `.claude/skills/ai-clip-ideas/reference/gen-veo-keyframes.js`; inspect it rather than assuming its provider/schema/default duration is current. It hardcodes JPEG MIME for inputs, so convert approved clean PNGs to proper JPEG files if using it. The older direct `.claude/skills/website-video/reference/recipe/ai/veo.js` accepts only a start image; it does not by itself lock the end frame.

State the estimated two-clip batch cost before running. VIDEO-RULES has the specific **$5 total per video** generation allowance, including paid retries across rounds. A new round does not reset it. Audit the existing WV01/B ledger and count any prior applicable spend before using the remainder. Verified new B opening metered generation through R2 is $0: existing clips were reused; stills came from the subscription. Do not assume broader $25/session standing authorization overrides the per-video limit. Ask once if this video's remaining authorized budget would be exceeded, with the proposed total. Gemini QA has its separate $5 batch threshold. Record prediction IDs, model/schema, inputs, cost estimate and actual charge for all attempts. Generate only these two selected clips. No balances, upgrades or production-generation paths.

## R2 picture implementation to carry forward

Private R2 `review/` has `shots.json`, `take-map.json`, `picture-repairs.json`, `assets.json`, `plan_resolved.json`, `custom_graphics.json`, `words_out.json`, `composite-manifest.json`, `crops.json`, `crop-preflight.json` and `join-map.json`. R2 `recipe/revise.py` builds the five scoped contexts, not a complete revised opening. Adapt it with R1 `recipe/build.py` and `finish.py` as historical assembly references. Do not rerun their old audio processing or their old roles/phone-card graphics. Replace G01 with selected generated firing/phone motion.

- Presenter source: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1699.MP4`. Use static WIDE 3552:1998:144:162 and TIGHT 2856:1606:492:170. Grade C cube: `/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube`, applied after 1080 scaling with established BT709 decode. Tight is 9.51% wider than R1. Keep intact hair; densely verify the delivered opening's affected shots, not just the representative comparison. Actual published framing comparison: `stills/framing-comparison.jpg`. Published A bytes differ from local locked A; live download is reference-only.
- Preserve three R1 picture repairs: frames 202:211 land tight; 517:526 return wide after portrait; 2923:2927 extend before-photo cover. New motion may cover early repaired frames, but no old flash is reintroduced at its return. Retain take-map and audio timing.
- P02-now: around 14.887-17.237s, actual frames 446:517. Reuse R2 real trio/stills and portrait compositor. studio-blue-11/127/247 real cutouts only. No identity redrawing, body distortion or overlap with later white-23/blue-173/blue-240 trio. Preserve the clear real-photo disclosure. Sources live in project `photos/finalized social media photos/_cutouts/`.
- G03: 36.11697-44.55697s. Exact blue "What you'll learn today" and white "5 ways AI beats human fitness experts.". Use `topic_case: preserve`, `drift:0`, shared HyperFrames. R2 `hf/` is the changed G03; `review/composite-manifest.json` references unchanged R1 graphic renders for all others. Use maintained `scripts/video/hyperframes_graphics.py`, canonical shared templates and configs. Optional case support landed in 64a3db5. Keep approved cached graphic pixels; a shared-template edit can otherwise change every scene. Never blanket-rebuild unchanged locked graphics.
- Failed laptop: 191.51157-196.7501367s, global frames 5740:5897. Source `/Volumes/Extreme/_edit_work/wv01-edit/round10/graphics/laptop-insert.mp4`, 157 frames at 29.97. Approved fixed crop and disclosure already baked. Natural speed.
- Successful three monitors: 203.37157-209.4109367s, global 6095:6276. Source `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/04 AI-Generated Clips/ai-dan/A0043_ai-dan-typing-three-monitor-desk_16x9_6s.mp4`, 97 frames at 16fps. Convert frame rate in real time to 181 frames at 29.97. Do not play 97 frames as 29.97, which speeds it up. Apply the established AI-GENERATED chip as R2 does. G10-specialists remains 210.9107-222.3221s.

## Audio, A and assembly traps

Accepted whole opening/join audio comes from `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round1/previews/DRAFT - Fired Them All B opening and join 1080p.mp4`, SHA256 `6e60be3d333a603b45bf3a2214d5cc6d341bf44b3a9c59ef170157da376e7bba`. Copy its AAC stream unchanged into the revised 265.031433-second picture. Do not decode/re-encode, remix, add music, add stamp sound effects, change gain or reprocess short excerpts to chase a score. Use exact reference-verbatim gates and packet/time checks.

Local approved A: `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A 1080p.mp4`, SHA256 `acddfb5b3bad7bb6d85f937b74054fafb4be33505f49ae91cd765a8ecac88836`. Join at B frame 7640/254.921333s using original A frames 5111:5414, exclusive end. Preserve local A master and the existing accepted A audio segment from R1. A inherited website delivery gate remains FAIL; creative approval is not a PASS stamp.

R2 initially found unreliable seeking with concat-copy across mixed encode parameter sets. Final R2 contexts normalized picture-only into one consistent H.264 stream before muxing accepted AAC. Apply that fix to R3 assembly. Check sequential and random-seek pixel agreement. R2 `native()` explicitly converts sources to 30000/1001; its `plate()` has one combined crop/scale/LUT/fps filter. Never add a second -vf that silently overrides crop and grade.

## QA and delivery

Check the global two-build/QC-job cap before each video job. Paired decoder/encoder pipes from one build are one job. Wait when both job slots are in use.

Inspect both complete AI clips frame-by-frame for identity, physique, panels, anatomy, dumbbell/elbow mechanics, phone beam and fixed camera. Check stamps against exact speech, label visibility, natural entrances/exits and each native cut. Watch/listen through the entire revised opening/join in sequence and obtain the independent candidate review required by the skill. R2's audit decoded every context, inspected 21 native boundaries and 28 seek samples and checked exact AAC/source-speed matches; it explicitly did not claim continuous human playback/listening. Do not inherit that as a new full-candidate watch pass.

Run current exact-file reference-verbatim audio, cut/junk, framing/hair, graphics/label and website delivery checks and shared hash-bound edit-sheet validation. Do not relabel missing measurements or gate failures as PASS. Recheck affected evidence after a fix. Prior R2 title clearance 26 frames/minimum 278px and G10 clearance 35 frames/minimum 79px were PASS for those files; R3 needs its own relevant composite checks.

Deliver the 265-second revised opening/join, a first-minute preview and a separate B/A join context, with full-quality and phone-friendly files, mapped subtitles, recipes, source/decision map, costs, exact hashes and honest checks. Every review video 45 seconds or longer gets a FULL-QUALITY ACTUAL COPY in `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Videos to Review/`, with clear Fired Them All AD R3 filenames and verified matching bytes. Preserve R1/R2 copies until Dan reviews and finalizes this video's candidate.

Use one-player review page: approved locks, first minute, changed motion/picture contexts, what you decided and only remaining decisions. Current http://127.0.0.1:8870/ serves R2 under launchd with a locally cached snapshot. To move this same video's server to round3, identify/remove only its 8870 registered service/cache, preserving source files and old round pages, then run from project `python3 .claude/skills/_shared/review_server.py 8870 '/Volumes/Extreme/_edit_work/wv01-edit/version-b/round3'` once the new page is valid. Alternatively use a free verified port without displacing another video. Verify all links, actual local cache bytes, browser playback/seeking and HTTP 206 ranges. R2 browser access succeeded. Automatic restart/login startup is configured; no reboot test was performed.

Stop for Dan's integrated opening/motion review. No complete B or publishing.

## Ready-to-paste starter prompt

AD: Start Fired Them All AD R3 using $vsl-edit. Read Handoffs/handoff-20261008-wv01-b-round3-selected-motion-and-opening.md. Use the locked slimmer firing frames and selected phone coach A to generate the two motion clips, then integrate the R2 picture revisions and approved laptop/three-monitor clips into the B opening and A join. Use the Codex subscription to generate the images if revisions are needed. Preserve approved color/audio, narration timing and A. Respect the remaining per-video generation budget. Put review videos 45 seconds or longer in Videos to Review. Show the integrated opening, first minute and join for review. Do not build complete B or publish.
