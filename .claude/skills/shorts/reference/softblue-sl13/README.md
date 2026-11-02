# SL-13 Calories Don’t Matter Shorts, R1

Dan chose A, B and C on November 2, 2026. The first-Short crop/graphics checkpoint builds A only. B/C remain selected and must be added as data after that checkpoint. No covers or uploads here.

Work: `/Volumes/Extreme/_edit_work/SL-13/round1/`. Parent R4 source hash and complete chosen transcripts: `Docs/SL13_SEGMENT_SHORTLIST_R1.md`; work `../shortlist-r1.json`. Parent original build now lives at `/Volumes/Expansion/_edit_work/ro11/`; do not run scripts there. C1705 remains on Extreme. Its sidecar was built by harvesting the existing raw transcript/lav, with no new transcription or paid description.

The batch renderer, CTC captions, source mapping, proof, audio preservation, render, watch/gate plan are adapted from SL-15 / SL-07. One 1080p file is used for review and VLC. New persistent header and study comparison use HyperFrames title-card; lower thirds use the existing vertical templates. Header advances 1.5 seconds into its animation, so frame zero is settled. Study v2 fixes row timing to actual number onsets and leaves room for captions. No new AI footage.

Camera: grade-C, original 4K strip. Wider 670×1000 and nearer 536×800 in 1920-space, y=68 / 76, measured minimum source hair row 108. Both have about 64 pixels of rendered headroom. Shared `landing.vertical_track` provides the standard dead band and speed, using the existing face track. The nearer crop is shot 3 only; bars remain on the wider crop. Verify delivered centering separately.

Sequence: prepare_media.py, refine_study.py, batch.py audio/words/plan/track/gfx/proof/render A, post.py, independent exact-file watch judgment, shared delivery gate. Wrap heavy work in the render queue; acquire/release SL-13 edit slot. Inspect proof before rendering. `post.py` writes the first-Short review under `review/`; this is not the final batch delivery. `page.py` supplies all asset stills and context controls on the same exact file. Preserve stereo and the parent voice; caption text comes from the corrected SRT, aligned with CTC.

Known environment issue: the shared audio selftest reported four failures because two historical Ad 1 test MP4s are missing. The pinned reference FLAC resolved successfully; exact-file verbatim audio gate passed. Do not change audio or shared thresholds to fix absent fixtures. Shared delivery gate outcomes and independent audit are separate and recorded in the work folder.

Review service: port 9296; use managed review_server.py. Browser checks used automation mode, verified mute, played/sought silently, then handed off paused with muted=false. Keep using the shared sound-ready workflow. R1 is awaiting Dan’s crop/graphics review, not final approval or publication.
