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

Final measurements and approval status are recorded in `proof-receipt.json`, `checks.json` and `new.mp4.edit-sheet.json` beside the review page. This is a graphics proof, not a full-film delivery gate. Dan's approval is pending. No approved video is rebuilt, replaced or uploaded.

## Verification

All three skills passed skill validation. Both new Python modules and proof scripts compiled. The integration rejected whole-second graphic edges, numeric reveal drivers and mismatched spoken edge phrases in negative tests. The code deployed successfully on Railway; absbyai.com returned HTTP 200.

The shared graphics checks and browser review verification must complete before the page is delivered to Dan.
