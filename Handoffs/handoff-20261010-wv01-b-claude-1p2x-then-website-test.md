AD: Fired Them All, website VSL Version B, finalized R5

# Claude handoff: 1.2x version, then website setup and split test

Created 2026-10-10. Immediate task name: **Fired Them All AD R6**.
Recommended: **Claude Opus 5.5, high effort**. The render is simple, but the complete-film sound, readability and transition review require judgment.

## Goal and authorization

Dan approved the exact R5 film: "All right this video looks great. This is finalized." He then requested a website upload and split-test setup handoff. After noticing Version A already runs at 1.2x, he instructed: "We need to accelerate this to 1.2x. Make the handoff for Claude to accelerate this to 1.2x".

Create a separate uniform 1.2x Version B from the approved R5 master. Preserve voice pitch, the complete narration, all scenes, graphics, framing, color, audio treatment and closing words. Deliver the new full film for VLC review. Keep the finalized normal-speed master intact. The immediate task is acceleration and review delivery. Website installation and split-test launch follow after review and the separate software/test-plan decision. This handoff records that future setup request without selecting software now.

## Exact approved source

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

- Local finalized master: `Website Videos/WV-01 Version B/Fired Them All AD R5 - complete Version B 1080p.mp4`.
- External identical master: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round5/final/Fired Them All AD R5 - complete Version B 1080p.mp4`.
- SHA256: `903eca4cd69ba19203394ee2a1c51ebb7bc9fce5d9bd6a9d8710c05297bf16fa`.
- 1,195,262,710 bytes, 25,792 frames, 1920x1080, 30000/1001 fps. Duration: 860.593067 seconds, 14:20.593. Target at 1.2x: about **717.160889 seconds, 11:57.161**, allowing encoder/frame rounding.
- SRT and VTT are beside both masters with the same filename stem.
- Final approval and evidence: `Media/wv01-r5-20261010/review/final-approval-20261010.json`, `DELIVERY.json`, `review/final-qc-summary.json`, `review/website-delivery-gate.json`, `review/independent/final-review.md`. Packaged evidence is git-ignored. Heavy recipes, accepted PCM and source maps remain in external `round5/`.
- Public receipt: `Docs/WV01_R5_REVIEW_RECEIPT_20261010.md`. WV-01B is finalized. R5 review copies and its old localhost review service were removed after final approval.

R5 restored the approved physical-phone goal scene and completed "I have never felt better in my life" before P6. Use this R5 master, never the rejected R4 film or original A with its frozen phone. The approved opening and remaining scenes are locked.

## Acceleration and repaired QC procedure

Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, `CUT-CONTINUITY-QC.md` section 5, the current VSL skill's adaptation boundary, and `Docs/WV01_R4_QC_POSTMORTEM_20261009.md`. Respect the two-build machine cap and other sessions' ownership. Existing A speed-variation recipes at `/Volumes/Extreme/_edit_work/wv01-edit/speed-1p2/` are reference only; inspect before copying and never run historical recipes in place.

1. Verify the approved source hash. Work in a new isolated directory such as `/Volumes/Extreme/_edit_work/wv01-edit/version-b/speed-1p2/`. Uniformly retime the full picture and soundtrack by 1.2, with pitch-preserving audio tempo processing. A typical FFmpeg approach uses `setpts=PTS/1.2` and `atempo=1.2`; explicitly retain 1920x1080 and 30000/1001 output cadence. Do not add EQ, gain changes, music, creative cuts, assets or frozen padding. Keep every spoken word and full closing animation.
2. Create a separately named 1080p MP4: `Fired Them All AD R6 - Version B 1.2x 1080p.mp4`. Divide every SRT/VTT cue start/end by 1.2. Preserve cue text. Derive any lightweight review copy from this exact new timeline.
3. Verify full decode, geometry, duration, pitch, intelligibility, synchronization, final word tails and subtitle timing. Build an output/source time map, accounting for actual cadence rounding. Retiming must include timed gate-plan joins, graphics, captions, speech references and inspection locations. Build the audio comparison reference from the accepted R5 PCM with the same tempo operation; do not compare accelerated audio against an unretimed reference.
4. Inspect the whole new candidate chronologically in moving and audio context, including all scenes, actual frozen flags, six callback entries/exits and complete sentence order. Inspect phone content against the approved P04 asset and the complete ending against R5. Native consecutive frames and independent assets are required where motion, pose resets or scene meaning matter; sheets and ASR alone do not establish these. Check fast graphics remain readable and intentional phone-photo holds remain correct.
5. Run fresh exact-file audio and website gates, native seek checks, subtitle validation and complete ending-word-order verification. Obtain one fresh independent full-candidate review using the actual delivered file, original references and denser transition context. Follow the repaired QC procedure rather than carrying forward old cleared judgments. Record coverage honestly, including any sampled playback limits. Separate inherited findings from new speed-induced faults. Do not modify gate thresholds or turn a human approval into an automated PASS.
6. Copy the complete full-quality film and subtitles to project `Videos to Review/`, verify the copied hash, and open it in VLC. Follow standing review-page delivery rules without reopening the previous review-panel troubleshooting. Deliver a concise change list, exact final-film timestamps to check, runtime, paths and actual QC results. Keep the original master and finalized queue state intact.

Predicted review points below are reference values. Measure and report the actual encoded R6 timestamps:

| What to check | Approved R5 | Predicted 1.2x |
|---|---|---|
| Opening, natural voice pitch | 0:00 onward | 0:00 onward |
| Restored physical-phone scene | 4:35.208 - 4:38.211 | 3:49.340 - 3:51.843 |
| Complete sentence, then P6 | P6 starts 14:08.815 | P6 starts 11:47.346 |
| P6 into uninterrupted full closing animation | 14:11.151 - 14:20.593 | 11:49.292 - 11:57.161 |

Historical R5 strict gate remains **FAIL**, with six failed rows. Two initially unmeasured rows passed a separate evidence-only recheck; that did not create a new full-run verdict. Inherited native findings were the pose reset at 6:30.757 and overhead hand/forearm crop at 14:00.506. Dan finalized the exact film after disclosure. Preserve the records and accepted edit; speed-induced defects require correction and recheck.

## Budgets

No new AI generation is needed. Saved cross-round Replicate generation cap is $50 total, never reset; prior total charges remain unknown. R5 generation calls/spend were zero. R5 Gemini QC token-cost estimate was $0.894088; historical R4 QC estimate was $0.388944. Preserve accounting and inspect actual receipts before any paid call. Announce the estimate for one necessary new QC batch, record actual usage, and follow the standing $5 QC approval boundary. Do not buy software or upgrade a plan for this task.

## Subsequent website setup and split test

A separate website-test brief was saved concurrently: `Handoffs/handoff-20261010-start-vsl-split-test-a-vs-b.md`. Read it when setup begins and follow Dan's actual approved decisions from that task. It proposes a page-code split with PostHog scoring and includes its own speed-render step. Reuse the verified R6 1.2x deliverable from this acceleration task instead of rendering a second independent copy. The original request here left the test software undecided; that separate task settles the test plan. Latest direct instructions from Dan take precedence over either brief.

Use the reviewed 1.2x B for the website test. Rename the subsequent task **Fired Them All AD Setup**. Before activation, retrieve Dan's separate decision for software, player/hosting requirements, traffic allocation, success metrics and test duration/stopping rule. Use the separately approved plan for these decisions. Prepare independently where possible if approval of that plan is absent, then leave activation waiting. Do not invent the platform/settings or send everyone to B.

Recheck the live page and concurrent ownership before changes. Current target is `https://absbyai.com/start`. Control is finalized WV-01 A at 1.2x, directly hosted at `/video/wv01-a-720.mp4` and `/video/wv01-a-1080.mp4`. The page is `letter-v1`, generated by `.claude/skills/design-sales-page/reference/round2-letter/build_live.py`; modify the generator and rebuild, never hand-edit generated `public/start.html`. Use `verify_live.py` after reading its current instructions. `public/site-video.js` does not control this current `/start` player. The old `control/analysis` layout test in the historical lower portion of `Docs/VSL_LANDING.md` is a different experiment.

Upload web delivery copies through the chosen supported hosting/player path. Current setup uses 720p mobile and 1080p desktop. Keep full approved content, sound and framing when compressing. Use unique immutable B filenames and fast-start/range-capable playback; existing `/video/:name` also supports numbered `.mp4.part1`, `.part2` files assembled by `server.js`. The full master exceeds GitHub's 100 MB file limit and must stay out of public git. Preserve A for rollback.

Change only the video unless the separate test plan explicitly changes more. Preserve page copy, poster, offer, cart, CTAs, muted preview and tap-to-unmute/restart behavior. Keep UTMs and click IDs through checkout. Distinguish experiment arm from the existing `landing_variant: letter-v1`; persist the actual video shown into trial and paid-conversion attribution. Verify stable assignment, forced QA views, both complete films, mobile/desktop playback, captions, final CTA, events without duplication and checkout routing. Judge business results on cost per started trial and paying customer, with the seven-day trial lag; player engagement is supporting evidence. Do not choose numeric thresholds now.

When the software and reviewed film are ready, launch the authorized test, verify real live assignment and tracking, and deliver media URLs, page URL, experiment ID/settings, launch time, verification and rollback steps. Use safe-push for named task files, verify Railway and production. Flag any native retest caused by changed app-facing code. No YouTube/social upload, ad creation, thumbnail job or unrelated formats belong to this website task.

## Ready-to-paste starter prompt

Continue as Fired Them All AD R6 using Handoffs/handoff-20261010-wv01-b-claude-1p2x-then-website-test.md. This is a website AD. Create a separate uniform 1.2x version of the exact finalized R5 film, preserving natural voice pitch, complete narration, all scenes and the repaired phone and ending. Retime subtitles and QC references, follow the repaired QC procedure and saved budgets, and deliver the complete 1080p film for VLC review with a concise change list and exact timestamps to check. Keep the approved original intact. Website upload and split-test launch follow review and the software/test plan I will settle separately; do not choose the software or launch a test during the acceleration task.
