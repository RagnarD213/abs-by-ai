# Calories Dont Matter SFC R2: revise A's study list, complete B/C

This is the authorized continuation of the original SL-13 editing request, CONTENT, internally SFL. Dan chose A/B/C. His exact latest revision and scoped approval are in `/Volumes/Extreme/_edit_work/SL-13/round2/dan-decisions.json`. Immutable reviewed media and configuration hashes: `round2/approved-manifest.json`. Do not mistake a technical pass for approval. R1 A was checked and shown, and now approved except the study list. B/C remain unbuilt. No covers, upload or scheduling.

Previous chat: `01a19cd4-d415-7322-b5ac-c7e4447d809f`, Calories Dont Matter SFC R1. This new round handles A's small correction plus the substantial remaining B/C assembly phase. Keep R1 untouched. First verify `round2/round-controller.json` phase complete and productionOwner equals your exact chat ID. Otherwise bootstrap read-only and stop until the transfer wake-up. Acquire SL-13 edit slot before any generation/build. Parent has stopped production and released its slot for this transition. Read the full applicable shared rules and shorts skill. Use current newest stable Sol high, resolved from the supported desktop catalog, currently gpt-6.1-sol/high.

## Current files and approval

Work `/Volumes/Extreme/_edit_work/SL-13/`. R1 complete reproducible recipe under `round1/recipe/`, versioned counterpart `.claude/skills/shorts/reference/softblue-sl13/`. Build outputs under `round1/build/A/`. Reviewed full A `round1/review/calories-dont-matter-short1_eat-protein-first.mp4`, SHA256 `47af9f2c2242a277c878fd18929b4b86f50379ab10894e0b01b649ef556f0f85`, 1080x1920, 1730 frames, 57.724s. Identical build file, review/media/A.mp4, and actual VLC file in `Videos to Review/Calories Dont Matter SFC R1 - A - Eat Protein First.mp4`. Videos to Review directory is a preexisting external-drive symlink, the file itself is an actual copy. Never replace that directory link. `Docs/SL13_R1_REVIEW_RECEIPT.md` records what ran and limitations. Review URL http://127.0.0.1:9296/ is serving round1/review through managed review_server.py. It was handed off paused, sound-ready.

The original source master is `claude edited long form content/11 - When Calories Don't Matter For Fat Loss/When Calories Don't Matter For Fat Loss | claude round 4 | 16x9 | RO-11.mp4`, SHA256 `fea0dd87ffbb37b4311feadaa5059ba69f9156df258a33f3c42540528786a8ad`, 598.8983s, 29.97fps, stereo48k. Corrected same-name SRT is the transcript. Original read-only build now `/Volumes/Expansion/_edit_work/ro11/` (old Extreme path is gone). Raw C1705 on Extreme, full path in lib.py, 4K. Roll sidecar now exists, built from cached lav/transcript, $0 ASR. Don't rebuild it. Same source, original colour LUT `/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube`.

## First action: study list change

Only A's study scene changes, A output 33.50–45.21 (parent351.85–363.55). Original config LIST in `round1/build/A/hf/configs/protein-study-v2.json`; use [0]. Old four rows each have numbers, which Dan wants removed. New structure:

High Protein
• 10.5 lbs. Fat Loss
• 2.5 lbs. Muscle Gain

Low Protein
• 8 lbs. Fat Loss
• No Muscle Gain

Preserve approved Same Calories./Different Results. title, MCMASTER, 2016 eyebrow, Soft Blue field, continuous HyperFrames motion, every other A asset/crop/caption/audio/timing. Header positions can fit around local y400 and760, row y485/610/845/970, h100, x80,w920. These are proposed geometry, inspect actual rendered frames; last rectangle ends local1070 => output1380, captions top1412. Font42; header48. `title-card.template.htm` already supports per-line px and row marker:"•" so no shared template change. Rows t1.64,3.94,7.44,8.84 relative to study local0. High header before first fact, Low header around local5.7 when the lower-protein group begins. Avoid early spoiler reveals.

Reuse approved A wherever practical. Existing source_picture.mp4 is clean caption/bar-free but includes old study/header. Full batch rebuild against approved cache is viable; a surgical base-file overlay must preserve captions, title and watermark and rerun exact-file gates. Do not copy an old PASS stamp onto a new file. Audio is approved untouched and should be stream-copied from R1 if taking a surgical video-only path. Need new exact-file watch evidence and independent review. A's original plans/timeline/words/face track can be copied into round2, not rerun unnecessarily. Extreme is exFAT: use shutil.copyfile, not copy2 (flags unsupported); skip AppleDouble `._*` files. All recipe hardcoded round1 WORK paths must be changed in new copies, never in immutable R1.

## Then complete selected B and C

Read `/Volumes/Extreme/_edit_work/SL-13/shortlist-r1.json` and `Docs/SL13_SEGMENT_SHORTLIST_R1.md` for verbatim scripts. B/C are already selected, don't ask Dan to pick again. A was built alone as mandatory first treatment checkpoint, now satisfied except requested study revision.

B: Eat Less Without Counting Every Calorie. Editorial master ranges258.299–302.198 and305.499–313.738, approx52.138s; snap seams to measured silence. First piece begins Researchers at the University of Illinois… and ends They did just as well as the calorie counters. Second begins When you've got fewer hours to eat… and ends That's one more reason why I fast until 2 every day. Skip So fasting changes your behavior. Open on moving eating-window graphic, no pickup. Parent G11 fact269.8367–276.208:550 fewer calories, after two months, no counting. G12 lower third291.259–302.448: Fasting Until Noon MATCHED Counting Calories. Use A's header/crop/captions, existing real footage and appropriate moving Soft Blue graphic. Plan >=30% off-presenter coverage and no repeated stock within a Short.

C: Keep Your Steps Up While You Diet. Master ranges494.985–521.425 and528.905–560.444, approx57.979s; snap seams. First begins The Mayo Clinic overfed a group… ends and even fidgeting. Second When you cut your calories… ends it protects your deficit you're working so hard for. Skip middle transition. Parent G19 fact504.0374–512.394: 10X Difference, same extra food. Existing stairs stock master517.705–522.344 is `/Volumes/Expansion/_edit_work/ro11/stock/p8550877.mp4` starting1s. Show complete useful action. G20 list539.5729–556.594:8–10K steps,walk after dinner,phone calls on feet,standing desk. Opening existing walking/stairs or existing library footage. No new AI planned. Reuse library/parent B-roll first; original parent source/stock read-only.

## Proven camera and build method

Recipe batch.py adapted SL15/SL07; lib.py full4K source grade-C. 1080x1920 output, top header310,picture1610. Wider crop670x1000 in1920space,y68; nearer536x800,y76. This yields ~64px delivered hair headroom, min raw hair row108. Shared landing.vertical_track exact scaled standard, stable wider shot with deadband, only necessary restraining corrections. A nearer shot3 only, bars wider. Keep approved treatment for B/C. Derive new B/C source ranges through parent shots.json; measure face/hair for each new span. A cached tracks source ranges496.98–507.62,509.16–526.61,538.35–542.12,555.11–559.55 are not B/C ranges.

A SEG318.35–367.38 and376.10–384.78 is final. Original second in was changed to376.10 to keep full So; don't revert. Exact captions CTC-aligned with numeric macros. Existing title/header settles at first frame by starting1.5s into animation. Chicken318.35–322.20, bread332.85–334.37, study351.85–363.55, eggs376.10–380.33. G1 digesting Protein20–30%,Carbs5–10%, output4.87–11.76. G2 Every Meal/Protein First/Then Fit In Your Carbs,53.34–57.59. No CTA added. Full A shots in build/A/shots.json.

Scripts: prepare_media.py/refine_study.py, batch.py audio,words,plan,track,gfx,proof,render; post.py creates exact copies, audio gate, watch scan, page, VLC. Deliver imports need importlib.util to avoid `_shared/deliver` name collision. Existing post/page already fixed. Adapt plans.py, scenes.py and page for A/B/C. Do proof review before encoding. `review_video.py` and `gemini_listen.py` provide supported file-model checks. CTC's installed torch environment is recorded in scripts. Do not start expensive full-source transcription again.

## Queue, checks, delivery

Use renderq wrapper for heavy/light checks; don't wait because other builds exist, submit FCFS. `renderq.py status` and editcap status before production. Parent saw0 jobs, 632GB Extreme free, internal126GB. Never run watch.py --help (takes a queue slot before argparse), read its file instead. System python lacks psutil. Preserve returned exec session_id if a command is still running.

R1 audio gate verdictPASS v2.0.0 reference-verbatim; delivery PASS v2.6.3,39pass,0failed/unmeasured/human. Caption48/48states,median-30ms,worst-46ms. Audio selftest4 historical failures came from TWO missing old Ad1 MP4 fixtures; pinnedFLAC was intact, actualA gatepassed. Don't alter audio or thresholds to fix missing fixtures. Shared watch all1730frames, 25images,11boundaries were judged clean/expected. Independent reviewer `/root/sl13_independent_review` completed; reports in round1, can use followup_task for fresh R2 check as skill requires. R1 actualface220samples,median17px,max55pxfromcenter,0invalid. These checks are exact-R1 only and must not be claimed for R2/B/C.

R1 Gemini audio says clean, natural49.03 join, fullfirst/lastwords. Full video exact190MB submitted Gemini3.1Pro4fpsHIGH; sampled reviewclean. No claimed audible listen or continuous human watch. R1 estimates audio<$.50,video<1.50,actual usage in reports,actual billednotreturned. New review estimates before calls; batches>$5 require approval. No new AI motion or still generation.

Deliver A revised plus B/C at1080p only, same files for managed review and actual VLC copies. Exact-file audio/delivery gates, silent browser playback/range tests, supported model review, independent audit. If a check can't run, report incomplete; never invent PASS. Review server port9296, shared review_server.py (not basichttp.server). Cache sync after page/media changes. Every asset still and same-full-film context buttons, right floating player; page.py is base. Don't give download attributes suggested filenames: server treats attribute values as paths, use boolean download.

Browser: enter automation mode via ?review_mode=automation or Start silent checks before ANY play/seek, verify actual muted. Finish checks for owner cancels recovery, pauses all, verifies paused, then unmutes without play, preserving volume. Don't change Mac/mic/routing. Paused/sound-ready was verified at last R1 handoff. CUA reset/summary requires rewriteDocumentation first. Refresh AX before using indexes; don't mutate via evaluate. Final ask for review must include screenshot if browser worked. Keep markDeliverable tab. For A revisions give watch range33–46s so Dan needn't rewatch all A.

Update Docs receipt, `Handoffs/video-editing/00-MASTER.md` via queue.py as appropriate. Job still in_progress until ALL3 reviewcopies; finalized only Dan finalapproval. Parent release is Wed Jan27,2027 under current calendar, old Dec13 references stale. No upload/cover tasks. Release edit slot --review when stopping for Dan.

## Shared workspace and wrap-up

Only this editor owns SL13. Board own entry must remain <=80words; total2500 (last2492), read from disk before changing/finishing and run bash scripts/board-check.sh. Don't trim others. Board must say revisedA/B/Cactualstatus, not old waiting state. Keep push-pending if relevant.

Public Git: docs/scripts only, media excluded. Shared main checkout has other live work, including staged deletion of sixpackabs/articles/TBD-daily-salad.md. Never stage or reset others. R1 local commits503ef0d and34b3aab. Last safe-push blocked8livepaths; don't force,stash,committhem. `/tmp/sl13_commit_phase.py` demonstrates exact owned-hunk temporary-index commit using HEAD plus only SL13 job object/row/board entry. It preserves other staged data. Adapt carefully for R2. Own work can be committed and markedpushpending, no Dan chores.

Every review/phase final ends two short blockquote boxes What was done and Your next steps, no paths/jargon in first. Review link first; DanwatchrangeA33–46andfullB/C. Distinguish rendered/checked/awaitingreview/approved/uploaded. Automatic handoff starter and newest-model+effort directlyinchat, not just thisdoc. Don't ask Dan to startor pin continuation. Continue the authorized work to finished review delivery.
