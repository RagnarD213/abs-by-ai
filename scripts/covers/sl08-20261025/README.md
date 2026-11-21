# Calories Shorts covers, 2026-10-25

CONTENT (SFL). Five approved R6 masters remain locked. Phase 1: 25 cover choices, 50 layout exports, awaiting actual cover picks.

Review: http://127.0.0.1:9250/

All assets, exact prompts, reference photos, original generation logs, source cutouts, final PNG/JPEG files and SHA-256 manifest are in the git-ignored `Short-form video content/covers/review/sl08-20261025/` folder. `generation-manifest.json` records 25 successful GPT-6.1 Sol / high helper calls on the Codex subscription, no paid image API.

`build.py` adapts the established SL-17 / SL-18 paired-layout builder. A and B preserve real photographic pixels over Codex backgrounds. C is generated Dan using a real reference. D and E are object scenes. Text is layered locally. Source photo-223 ends at native y2850, lower waistband seam, before brief leg openings. Cutout alpha was generated locally with the existing Apple Vision personmask tool, then isolated to the largest connected component above alpha32 and feather-preserving support dilation12. Source pixels were never redrawn.

Rebuild only the requested keys: `python3 scripts/covers/sl08-20261025/build.py s1` then `python3 scripts/covers/sl08-20261025/qc.py s1` then `python3 scripts/covers/sl08-20261025/review.py`. Do not run build processes concurrently; each updates one manifest. Refresh the durable review cache after any page/image change. The exact JPEG hash/byte augmentation in the review manifest must also be refreshed for revised YouTube files.

Dan authorized January 4, 5, 8, 9 and 11, 2027, at 9 AM America/Chicago, preserving the December 27 parent release. No slots booked. After his five cover picks, follow the setup handoff for Drive backup, transcripts-based metadata, FOOD, pinned questions, media/cover uploads, cover-first TikTok derivatives, cover registries, dry run and all-platform readback or the shared waitlist. Recheck actual parent release dependency and slot availability before writes. No direct YouTube holding upload. No per-video automation. No changes to the paused dashboard or edit heartbeat.

## Setup completed 2026-10-25

Dan approved C for all five. Exact picked files and hashes: `picks.json`. Checked metadata: `captions.json`; verified storage uploads: `media-uploads.json`; cover-first copies and untouched AAC: `tiktok-verification.json`. The five configs are on the existing shared waitlist, January 4/5/8/9/11, 2027, 9 AM Central. No Short schedule IDs exist yet because Blotato remains197/200. Full receipt: `Docs/SL08_SETUP_RECEIPT_20261025.md`.

The build/generation scripts reproduce this historical five-choice round, which is already approved. Future new sets use the changed October25 skill mix: two AI Dan concepts, one real pool OR studio photo, and two history-guided Codex choices. Do not regenerate these approved C files merely to apply the new mix. Setup scripts were run and exact files checked; upload.py resumes verified entries rather than creating duplicate media. No helper here should be used to create new schedules outside the shared client/queue workflow.
