# CONTENT (LFC): Arms & Shoulders Workout, Round 4

Start now in **Arms Shoulders Workout LFC R4**, using **GPT-6.1 Sol, high effort**, resolved from the current supported destination catalog. This video started on Codex. This is an authorized automatic continuation of Dan's October 23 revisions, not a new full-film render request.

## Scope and approval boundary

Deliver TWO checked, playable previews for Dan:
1. A closer fixed crop for overhead triceps near 1:14, about 20 percent closer if the actual full movement permits. Keep the raised dumbbell, hands and hair inside with visible clearance throughout the whole set. Use a natural cut into the closer composition; do not animate a horizontal zoom or track him. Show before/after and moving context, including the highest dumbbell extension. Determine the exact start from the actual film, not the approximate note.
2. Replace the final rest card with a 30-second completion screen: a large title at the top, moving real clips of Dan doing EACH of the three exercises on the left, and his exact instructions on the right. Preserve the 30-second rest countdown. Use Soft Blue Light HyperFrames continuous motion and the shared templates/method. Start the exercise clips on actual repetitions, not setup or between-takes footage.

Exact title: "Congratulations you completed the round."
Exact right copy: "For beginners replay 2 more rounds. For advanced guys replay 4 more rounds."
Do not rewrite the wording or add a spoken ending, site mark or invented claims. Typographic line breaks are fine. A few seconds of curls, lateral raises and overhead triceps can cycle across 30 seconds. Use approved color B on clean camera excerpts, without duplicated burned timers. Keep full useful exercise action visible inside the left panel.

**STOP after the previews for Dan's two approvals. Do not re-render the full film yet.** R3 remains the current complete film and is not finalized. No thumbnails, Shorts, publishing, setup or scheduling.

Authoritative exact request and immutable lock manifest: `Handoffs/video-editing/ro04-round4-plan/decisions.json` and `locks.json`.
Revision ID: `01a16918-0e30-7af1-90a7-267206829cad`. Previous task: `01a15a62-8443-72f2-885b-f2bbb0a1483b`.
Round key: `RO-04:R4`. Journal: `Media/video-edits/RO-04/round4/round-controller.json`.
Before any production, require that journal phase is complete and productionOwner is YOUR exact task ID. During bootstrap prepare read-only and stop if transfer is pending. Process this revision once; resume checkpoints, never duplicate the round.

## Edit slot and queues

Before first production and on resume run `python3 .claude/skills/_shared/editcap/editcap.py acquire RO-04 --title "Arms Shoulders Workout LFC R4" --type LFC`.
At handoff prep the five-edit cap is full. If exit 3, do not render or spend: arm the required 10-minute thread heartbeat from the editcap README, report the position once, and stop. It should acquire again, pause itself on success and continue this exact handoff. Do not poll the busy render queue or use old two-build loops. The parent has no active RO-04 production claim: queue currently delivered from R3.
Use the shared render queue for all heavy builds and checks. Read current VIDEO-RULES, editcap and renderq runbooks. Production intermediates go in queue-selected work/scratch storage, never the synced project tmp directory. Keep this round's journal at its stable stated path even if a render work folder is selected elsewhere.

## Existing exact media and recipe

Project alias `/Users/danielrose/Documents/Claude/Projects/Abs By AI` and canonical `/Users/danielrose/Projects/Claude/Projects/Abs By AI` are verified os.path.samefile true. The desktop registered project uses the first, native old-thread cwd uses the second. Do not move the project or alter other tasks.

R3 work: `Media/video-edits/RO-04/round3/`.
Current native: `Arms Shoulders Workout LFC R3 - full workout.mp4`.
SHA256: `2a37855812c91260004ed53e56c84d4a0545dd92e5513c8bcc97446f911f318d`.
163110774 bytes, 1920x1080, 30000/1001 fps, 3772 frames, 125.8590667 seconds.
Camera ends at 95.8624333 seconds; the R3 rest lasts 899 frames (29.9966333 seconds).
Ready-to-curls at 5.872533; curls-to-laterals at 35.86917; laterals-to-triceps at 65.8658. Source start 66.6003, nine opening frames ALREADY trimmed. No further trim.

Raw: `/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1586.MP4`.
Original stereo editor reference: `Zeeshan Content Videos/arms and shoulders home workout - video 2/arms and shoulders home workout | zeeshan | 16x9 | video 2.mp4`, 858396944 bytes, MD5 `49c7dfb3d189043dbb2bc4b326e8fd81`. Reference camera audio start 497.96455.
Current fixed source crop: x100,y18,w1776,h1000 scaled1920x1080. Only overhead triceps crop is reopened.
Color B exact implementation in R3 `recipe/build.py` and `qa/calibration.json`: fitted RGB polynomial, multipliers1.012/1/.99, saturation1.48, contrast1.075, brightness-.003. Grade camera before graphics. Do not grade graphic layers.
Camera B-roll for the end screen must come from this camera with approved color B or the clean graded R3 `camera-before-graphics.mp4` / relevant source-picture intermediate after inspecting exact filenames. Never use the old ungraded whole reference as the new recap picture.

Recipe: R3 `recipe/render_full.py`, `assemble_exact.py`, `build.py`, `prepare_qa.py`, `edit_sheet.py`, `page.py`, `README.txt`.
R3 state()/paint() exercise timers approved. New completion card is a requested graphic revision, so it uses HyperFrames, not a new static softblue.py fallback.
Original AAC camera payloads/timing are preserved exactly in R3. See `qa/exact-audio-timing-proof.json`, `qa/audio-assembly.json`, `qa/assembly-repair-notes.txt` before any future whole-film assembly. Do not apply the old container-rounded remux mistake. Reuse exact R3 mix slices for previews; no new EQ, bass, limiter or mono conversion.

Music source: `/Volumes/Extreme/_edit_work/music-check-20260922/knox-gym-energy-gym-thunder-538872.mp3`, gain0.07449345290660858. R3 matched phase across rest; 1.5-second ending fade on rest only. New recap normally uses this same R3 rest audio unchanged.

## Known QA evidence and limits

R3 native and phone audio gates PASS; delivery gate2.6.1 PASS with 25 measured rows plus14 declared N/A (CLI counts all39 as passed). This is evidence for R3, never a new preview stamp.
Full native scan3772 frames, all14 watch images inspected, 4 boundaries, 5 scenes, zero verified defects. Full4fps visual model review plus separate full-export audio review; no human native-rate continuous watch claimed.
The original automatic hair test failed227/384 valid (59.1% vs unchanged60%). An independent, film-specific exception was documented after dense actual-frame crop checks, including all901 lateral native frames. Functional timer OCR and song lyrics also caused bounded false positives. Preserve these original findings, do not copy their exceptions blindly to new tighter framing.
R3 review notes and independent report are in `qa/independent-review.md`, `qa/independent-review.json`, `notes-round3.txt`. Exact full-film receipt is tracked at `Handoffs/video-editing/ro04-round3-plan/review-receipt.json`.
R3 requested wider-to-tighter overhead change and old rest-card rejection must be recorded with Dan's words in the QC corpus before making fixes, without changing thresholds.

For the NEW crop: calibrate actual dumbbell, hands and hair, check every native frame of the complete overhead set for top-edge safety, sample rendered native/phone at least every0.25s, inspect lowest-margin full-resolution images, and review motion. Clipped equipment or unresolved hair blocks the preview. About20% is a target, not permission to cut off the weight.
For the NEW card: all three exercises visibly move, no frozen-frame filler, title/copy large and readable, 30-second countdown correct, field and accents move across the whole card, original music retained. Check entrance from last exercise and full30s. Obtain one fresh independent consolidated review after editor self-QA, not parallel redesigns. The applicable long-form edit skill expressly calls for this reviewer.
Keep cost estimates before paid reviews; no paid generation needed. Prior R3 quality review estimate under$2, exact billed amount unavailable. R4 starts$0; no generation needed.

## Review delivery

Preserve R1/R2/R3 and the old service at8974 until R4 previews are ready. Then use the maintained managed review_server.py with this video's port, identify service owner first, retain repaired play/seek/restart/speed controls, test muted and leave paused/muted. New page shows just the changed items with the unchanged R3 film available for reference, clearly labelled.
Show end card as a still plus its full30s moving preview with about3-5s of actual preceding workout/audio context. Show triceps before/after plus affected moving action. Do not build a replacement full film as a context preview.
Deliver review link first and exact R3 locations plus preview watch ranges. Request only the crop and new completion-card approvals. Any review video45s or longer also gets a native copy in Videos to Review and folder reveal; shorter previews remain on the page.
Public Drive R3 backup: https://drive.google.com/drive/folders/1lSinVSCnvlo9zO6Fxm1nCT5IAuesWkI- .
R3 file IDs: native1moXNuqVxDCSlZOI1Os5g0aeXnd4i6glD, phone1rHViibvfrSGFan9MaxgIMhcpyohV7Tl3, recipe1gZxkJH1uxBGTMwuhjsoQDNSNX0jlfOmA. Create public R4 sibling folder if backing up previews; read Google Drive skill first.
Release RO-04 edit slot with --review at delivery. Update only this job's queue/board/decision entries; do not touch other active edits. No Victory Dashboard.

## Recovery starter prompt

CONTENT (LFC). Name this chat Arms Shoulders Workout LFC R4. Use GPT-6.1 Sol at high effort. Execute Handoffs/handoff-20261023-ro04-round4-zoom-completion-preview.md after verifying the round journal names you production owner. Make a checked closer overhead-triceps preview and a moving30-second completion/rest screen with Dan's exact title, three exercise clips on the left and beginner/advanced replay text on the right. Show both for approval before rendering the full film again. Preserve approved B color, original stereo audio, timers and R3 evidence. Acquire edit slot RO-04 before production; on exit3 arm the standard automatic wait and stop.

