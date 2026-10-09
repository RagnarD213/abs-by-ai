AD: Fired Them All, Version B, R5 final two fixes

# Handoff, 2026-10-09

Task name: **Fired Them All AD R5**. Recommended: **GPT-6 Astra, high effort**. Own the two final film fixes and exact-candidate QA. Do not reopen approved opening or unrelated creative choices. Do not upload, install or publish. Dan watches in VLC and explicitly dropped review-panel troubleshooting.

## Goal and authorization

Dan reported:

> At 4:38 the video just freezes on a freeze frame of me, where it should be the AI-generated picture of me in the phone frame. Fix that

> Transition at 1407 is awkward and not smooth. Fix that

He requested this handoff for a new task and an analysis/skill repair. Analysis and procedural skill repairs have been completed in R4. Film repair and new full render remain for R5. These instructions authorize the two scoped technical repairs, preservation checks and full review export. Reuse the existing approved phone component and filmed callback. No new generation or creative approval is needed for unchanged assets. Materially new creative assets retain their ordinary approval rules.

Read `Docs/WV01_R4_QC_POSTMORTEM_20261009.md`, shared `VIDEO-RULES.md` and `CUT-CONTINUITY-QC.md` in full, especially section 5. Use `vsl-edit`. Read the previous R4 handoff only for supplementary source/approval history, not to reinstate its erroneous cleared judgments. Never run an old recipe in its historical round directory.

## Authoritative inputs

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

R4 work root: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round4`.

Current film: `round4/final/Fired Them All AD R4 - complete Version B 1080p.mp4`, SHA256 `bd4067e1735e42a75ef37510acc8be6fd744c9185e11c2a4f6894ad77899cf0e`, 25,792 frames, 30000/1001, 860.593067 seconds, 1920x1080. The same file is in project `Videos to Review/`. This is the corrected latest audio version, not an earlier candidate.

Approved B opening: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round3/previews/Fired Them All AD R3 - opening and join 1080p.mp4`, SHA256 `81110e1409266f1e6a07f2f30aa6ee8147315d2a65e504d61fab892e6448c8f3`. Only frames [0,7640) are the opening; the extra A context in that preview is not to be duplicated.

Original A: `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A 1080p.mp4`, SHA256 `acddfb5b3bad7bb6d85f937b74054fafb4be33505f49ae91cd765a8ecac88836`, 22,570 frames. It contains the bad frozen phone scene. Use it for original narration/context, never as proof that that scene is correct.

Phone component: `/Volumes/Extreme/_edit_work/wv01-edit/round2/previews/P04-lock.mp4`, SHA256 `87ae103edb0830b9880325c7f658ce241008b6196954b28c6abca5bee2475500`, 90 frames, 960x540. It is the correct physical-phone goal-image composition, including the approved AI disclosure. Normalize to 1920x1080 before joining it.

Raw callback/ending rolls: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1700.MP4` and `C1698.MP4`, 3840x2160 at 30000/1001, S-Cinetone Rec709. Grade: `/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube`. Existing crop windows are W [3552,1998,144,162], T [2856,1606,492,170], expressed width,height,x,y.

R4 recipe/reference files: `recipe/assemble.py`, `recipe/prepare.py`, `recipe/finalize_audio.py`, `review/assembly-edl.json`, `review/callback-map.json`, `parts/complete-spliced-reference.wav`, `review/delivered-asr.json`, `review/words-mapped.json`, `review/final-qc-summary.json`, `review/complete-receipt.json`, `review/accounting/`. The current accepted PCM reference already contains the corrected callback tone; verify it against the current master before using it. Do not accidentally revert to old callback audio. Public project record: `Media/wv01-r4-20261009/`, git-ignored.

## Fix 1: restore the phone scene at 4:38

Replace R4 picture frames [8248,8338), 275.208267 - 278.211267 seconds, with the exact 90 frames [0,90) of P04-lock, upscaled consistently. This is A [5631,5721). Preserve the original narration and adjacent P1 callback timing. Check the entrance and return in moving context, roughly 4:28 - 4:43. The approved still on the phone is allowed to hold; a studio-camera freeze is not. Verify against P04-lock itself, not a reference cut from A or R4.

Cause: round12 joined a 540p part into a nominal 1080p stream without normalization. OpenCV sequential decoding then returned the previous camera frame throughout those 90 frames. Round17 flattened that hold into A. R4 inherited it. Normalize all parts and use native verified decoding in the new round. Do not rebuild from that mixed-resolution round12 master.

## Fix 2: repair the complete ending transition, roughly 14:04 - 14:12

R4 pool return: frame 25316, 844.710533 seconds. P6: output [25425,25495), 848.347500 - 850.683167, C1700 [3259,3329), 108.741967 - 111.077633. It says "You've been doing this alone long enough." Current picture uses W. Entry resets hands in the same wide composition.

The more serious related error is audio order: R4 says "I have never felt better, you've been doing this alone long enough in my life, so tap...". Original A says the complete phrase "I have never felt better in my life" before "so tap the button below". The old insertion used advanced picture/CTA boundary A22273 instead of sentence completion.

Required order:

1. Complete "That's what this did for me at 40. I have never felt better in my life."
2. P6: "You've been doing this alone long enough."
3. "So tap the button below..." with the complete seven-day trial and final invitation.

Locate the genuine sentence gap in original A audio. Its ASR puts "life" ending at743.50 and "so" starting743.66; inspect the waveform and actual source audio to choose a safe exact boundary. The source map identifies the original complete-phrase join at A22287, baseline22343, before C1698 raw11908 begins the final invitation. This is the concrete candidate insertion point; verify actual word-tail clearance there before locking it. Move the existing processed callback as one complete phrase after the sentence. Protect consonants and tails. Do not use ASR boundaries alone and do not synthesize words.

Solve picture separately. Prefer a fixed T composition for the complete P6 interval, with a genuinely distinct preceding wide shot and then full CTA cover. Measure the entire crop for hair and gestures. Recover the original moving C1698 picture beneath the early CTA if required to finish the preceding sentence on camera. R4 `recipe/heads_and_sheet.py` records A22273's underlay as C1698 [11884,11898), followed by [11908,12155) and room tail [12155,12191). A22273 maps baseline22329, and the complete-phrase join A22287 maps baseline22343. Thus the 14 raw frames [11884,11898) are the concrete moving-camera extension candidate before P6. Verify those against the original source/map before using them. Never hold the last camera frame to fill a gap.

Keep the CTA uninterrupted once it begins. No brief CTA peek, return to camera, one-frame crop island, dissolve hiding a jump, animated horizontal crop or added sound effect. Reuse the approved closing treatment/animation. Its source/extension method is in `/Volumes/Extreme/_edit_work/wv01-edit/round16/recipe/build_cta_tail.py` and `closing_components.py`; do not import/run those scripts in place, because historical recipes can execute mutations. A duration-preserving candidate is: move those 14 frames of remaining A narration before P6, extend the original live picture with C1698 [11884,11898), use fixed T for P6, then start the original 283-frame CTA animation (closing-context source [125,408)) after P6. The old advanced CTA had 14 additional terminal animation frames [408,422); restoring its original 283-frame span should reconcile the 14-frame delay without removing spoken audio or meaningful card content. This candidate places P6 at output [25439,25509), about14:08.815 - 14:11.151, and preserves the 25,792-frame duration. Verify the original source/card timing and complete final speech rather than blindly adopting these arithmetic bounds. If preserving the complete card instead needs a short extra natural room tail, document the frame/duration change and regenerate final time maps. Do not clip final speech or repeat/freeze footage just to preserve the previous duration.

Compare the whole original/candidate ending as moving clips, not just the P6 boundary pair. Check pool exit, all original presenter motion, completed sentence, P6 entry/exit and full CTA through the last spoken line. This is an authorized repair of that ending sequence, not a general redesign.

## Build and quality checks

Work in `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round5/`. Use the current uniform R4 film and verified independent assets to patch only affected picture/audio. Preserve unchanged picture/color, approved opening and P1-P5. Preserve unchanged audio treatment. If P6 audio is reordered, construct the exact accepted reference from the current processed source/PCM, with cuts only and no global EQ/gain/remix. An audio gate against that new reference verifies rendering, while the original-versus-candidate sentence check verifies edit correctness. Both are required.

Use one continuous encoder/native-frame stream, with preflight geometry assertions, rather than mixing differently sized stream-copy parts. Respect the two-build cap across all sessions. Record a frame-accurate R5 edit map and exact hash. Check preservation outside the two repairs and remeasure all affected boundaries, labels and framing.

Apply the repaired shared QC procedure to every required scene and every frozen flag. The old frozen phone must fail the review control; the correct phone still must pass as an intentional static asset. Reassess all six callback entries/exits and complete clause order against original narration. Obtain one fresh independent full-candidate review with original assets and moving source context. Do not carry the erroneous R4 cleared judgments forward.

Run shared audio/website delivery gates, native seek checks, updated sheet validation, SRT/VTT and fresh final ASR on the exact delivered R5 master. Compare ordered ending words, not just global fidelity. R4 had audio PASS but delivery FAIL, 32/39 passed, seven failures: headroom, minimum segment, jump-cut metadata, splice visibility, burned-caption heuristic, watch pass and dead air. Keep these reports as historical findings; report R5's actual results without waivers, false all-row PASS claims or threshold relaxation. Current numeric/automated checks do not implement semantic scene-content or sentence-order guarantees; required direct review remains essential.

## Budget and delivery

No new generation is expected. Saved Replicate cap: $50 total across all website-video rounds, not reset in R5. R4 calls/spend were zero. Prior R3 known success estimate $0.70 and failed reservation $0.90 are not the entire historical total; actual prior charges remain unknown. Read `round4/review/accounting/replicate-budget.json` and original receipts before any paid call. Gemini R4 review accounting is $0.388944; preserve it. Any new quality review uses the separate recorded budget and no more than necessary.

Deliver full R5 1080p master, updated subtitles, the two changed contexts, recipe/edit map, independent scene/freeze/sentence review and exact-file results. Copy the full-quality film to project `Videos to Review/Fired Them All AD R5 - complete Version B 1080p.mp4`, with matching hash, for Dan's VLC review. Keep R4 as a historical rejection until R5 is checked; do not delete unrelated review copies. Dan requested no more review-panel repair. No platform upload, publication, website installation, format derivatives or thumbnail job.

Ready-to-paste prompt:

Continue as Fired Them All AD R5 using Handoffs/handoff-20261009-wv01-b-round5-final-two-fixes.md. Restore the approved phone goal-image scene at4:38. Repair the ending transition around14:07 by moving P6 after the complete "I have never felt better in my life" sentence and fixing its picture joins. Preserve the approved opening and everything else. Follow the repaired QC procedure and saved budgets, then deliver the full film and changed contexts for VLC review. Do not upload or publish.
