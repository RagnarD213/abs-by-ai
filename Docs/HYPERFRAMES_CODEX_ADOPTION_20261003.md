# Codex HyperFrames adoption

2026-10-03. Implementation commit: `813d7df` (includes `aad0fe9`).

All three Codex video skills now require the shared HyperFrames method for lower thirds, before cards, side lists and cycles. The earlier panel renderers remain historical tools, superseded for these four graphic types. Existing approved videos stay intact.

`scripts/video/hyperframes_graphics.py` is the build integration. It reads graphics as plan data, validates phrase timing against mapped words, calls the shared `from_plan.py`, loads the shared `composite.py`, and verifies the composite with the shared `checks.py`. It checks the pinned version, 0.8.97. It records template, config and spoken drivers in the edit sheet. It neither copies templates nor creates a separate renderer.

## RO-17 proof

The isolated comparison covers 338.138 to 398.131 seconds of the existing RO-17 draft (1,798 frames at 30000/1001, 59.99 seconds). It contains the four protein snacks side list and the Chipotle $7 lower third. Copy stays the same; reveals land on the spoken food names and price.

Proof build: `scripts/video/proofs/ro17_hyperframes.py`. Page packaging: `scripts/video/proofs/ro17_review_page.py`.

Media: `/Volumes/Extreme/_edit_work/hyperframes-codex-ro17-proof/`.
Review: `http://127.0.0.1:8854/`, served from `/Users/Shared/absbyai-reviews/hyperframes-codex-ro17/` so launchd can read it.

Both comparison players use the same clean presenter layer, fixed side composition, existing source cuts, grade and encoded audio. Draft stock placeholders are excluded from both. The original draft excerpt is also provided as a reference. This isolates the graphics change. Original full-video file hashes are checked before delivery.

Final measurements and approval status are recorded in `proof-receipt.json`, `checks.json` and `new.mp4.edit-sheet.json` beside the review page. This is a graphics proof, not a full-film delivery gate. Dan approved the corrected proof on October 4, 2026. No approved video is rebuilt, replaced or uploaded.

## Verification

All three skills passed skill validation. Both new Python modules and proof scripts compiled. The integration rejected whole-second graphic edges, numeric reveal drivers and mismatched spoken edge phrases in negative tests. The code deployed successfully on Railway; absbyai.com returned HTTP 200.

The shared graphics checks passed: 150 side-card frames, minimum body clearance 210 px; 24 lower-third frames, minimum face clearance 362 px. All three card-fill samples passed. The edit sheet validated, original file hashes stayed unchanged, and the encoded audio payload matched between players. All 13 page assets returned HTTP 200; both video range requests returned 206. Chrome playback, synchronized seeking near the end and the context player were verified. The real-frame stills were visually inspected. Dan approved the corrected proof on October 4, 2026; adoption is complete.

## October 4 correction

Dan accepted the treatment except a slight apparent shrink of Sardines near excerpt 12 seconds. Native-frame inspection found no font-size tween: its white glyph bounds stayed 183 x 27 px, but the shared card's fractional drift moved the baseline by a pixel at 11.47 seconds and changed edge rasterization. The revised side-list config uses `drift: 0`; the shared plan and side-list builder now default to zero drift for future cards. Entrance, word reveals, specular sweep, exit, copy and lower third remain intact.

The revision preserves the reviewed first proof in `revision1/`, records Dan's exact feedback in the shared corpus, and rebuilds only the isolated proof's side-list span. The accepted price tail and encoded audio are retained. No full or approved video is re-exported.

Correction verification: all 210 consecutive final-video frames from excerpt 8 to 15 seconds hold identical Sardines glyph bounds (183 x 27 px at one position). All 237 encoded price-tail frames match revision 1. Shared graphics checks passed again (210 px body clearance, 362 px face clearance), and the revised edit sheet validated. The original source hashes and encoded audio remain unchanged.

Final approval, October 4, 2026: Dan said, "Okay this is looking good now." The corrected isolated proof and shared-method adoption are approved. All three installed Codex skills use the shared graphics pipeline; future builds inherit it. No further adoption work is open.
