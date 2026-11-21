# Calories Dont Matter SFL Setup, November 7 2026

CONTENT (SFL). Owner: Codex 01a1b65a-40f1-7ec0-8e5e-113b90dd18d8. **Historical November 7 preparation snapshot. Completed November 8: see [final setup receipt](SL13_SETUP_RECEIPT_20261108.md).**

## Review

[All cover choices, Instagram and YouTube paired](http://127.0.0.1:9341/). Protein 8 choices, Eat Less 8, Steps 5. The three additional comparison images for Steps were unavailable after repeated service errors. No paid fallback. No source labels or hidden mapping are exposed on the review.

The review is managed on port 9341, cached locally with 43 linked files. It returned 200 and all 42 image URLs downloaded. Browser phone-width check found 21 choices, 42 images, no horizontal overflow and no audio/video elements. The gallery opens in the in-app browser. Dan has not picked or approved these cover files.

Forty-two exact 1080x1920 RGB layouts were checked, all YouTube JPEGs under 2 MB. Actual Instagram title glyphs sit inside the profile-grid safe area. Text against measured face/hair guard rectangles has zero overlap. The owner inspected generated scene contacts, real identity references and every paired layout; bottom titles were adjusted to clear abs. The three real-photo choices preserve the existing cutout pixels, with local scaling/placement and generated backgrounds. No original approved film was rerendered.

## Approved films and category

| Short | Approved SHA256 | MP4 bytes | SRT final cue / film duration |
|---|---|---:|---|
| Eat Protein First To Keep Muscle While Losing Fat | b5b5037e1c133971c9a7080f2e96c1d3e76996104ba19252e2b532ac7378cf55 |185526440|57.691 /57.728s|
| Eat Less Without Counting Every Calorie |1a10fea9f9ec9a3f9ada915c664e13b1bceb7ba612e3dae77f33d74f496bd892|148745110|52.319 /52.3523s|
| Keep Your Steps Up While You Diet |6dded1889c38ed4e48c86c52fbb6f6b24b68d185c7dcd8360e8aa6a854912b04|170126005|58.926 /58.944s|

All three were freshly rehashed against the handoff. Matching final transcripts confirm educational organic endings, with no tap/click-the-button CTA. Each ends on the tactic quoted in the original setup handoff. Existing exact-file delivery v2.6.3 and audio stamps and approval remain historical evidence, not a claim that a newer gate ran here. No audible listening or new full-film review is claimed.

Actual edit recipe/provenance: A has real stock food, study cards and a real eggs insert from the approved parent; B has presenter and cards; C has a real stock stair opener, presenter and cards. Set `ai_generated: false` for each Short, independently of the parent’s true setting. Cover generation does not turn on realistic-AI-footage flags. Native checks confirmed the actual presenter set is not the fridge/cabinet kitchen and the egg insert is food footage.

## Backups

Project delivery stays at `Short-form video content/Calories Dont Matter - SL-13/Finalized R2/`. All three MP4s and matching SRTs were copied to `/Volumes/Extreme/Short-form video content/Calories Dont Matter - SL-13/Finalized R2/`; all six SHA-256s match. Original Extreme working masters remain.

[Google Drive backup folder](https://drive.google.com/drive/folders/1QsgJ3Cxn_38qW13LicRufWvi9rAwDDS_): A/C MP4s and three SRTs present, matching sizes and Drive-reported SHA-256s. **B MP4 upload/verification remains incomplete.** rclone’s shared Google API project returned 403 rateLimitExceeded, including the bounded retry. The connected upload tool refused 148745110 bytes because its maximum is 104857600 bytes. Chrome upload was started in the exact folder; its last observed state was 4.6 MB/141.9 MB (3%), still uploading. Preserve/check Chrome tab 1967278889 before retrying or creating duplicates.

Folder sharing was set to anyone-with-link Viewer and independently read back through the Drive connector. This is sharing verification, not completion of the missing backup. No copy is deleted. Google Drive remains a blocking setup-completion condition after picks.

## Metadata prepared

`scripts/covers/sl13-20261107/metadata-draft.json` contains searchable titles, descriptions, all platform caption overrides, root-domain UTMs and pinned questions. Three clean voice-writer calls used the actual final transcripts. No invented free-generation offer; all outward-facing em/en-dash checks passed. Drafts are not live publishing configs.

Pinned questions, to post and pin after public release through the existing shared routine:

- Protein: What's your go-to protein at most meals: meat, fish or eggs?
- Eat Less: What time do you usually eat your first meal of the day?
- Steps: How many steps a day are you getting right now?

Article: no draft required for Shorts at setup. Existing sixpackabs-article-gap-daily writes 300–500 words or records a skip after release; no new per-video automation. Existing cover and pinned-comment monitors are retained; future public tiles/comments/articles have not been observed.

## Queue and release hold

Live Blotato readback: 200/200 scheduled posts. Parent When Calories Don't Matter For Fat Loss (The 7 Other Factors), YouTube schedule 5365814, is saved for **January 27, 2027, 9 AM America/Chicago**. It is not yet public.

Tentative currently unreserved eligible slots, after checking live schedules, the shared waitlist and dated phase rules: Protein January 28, 6 PM; Eat Less January 30, 9 AM; Steps January 30, 6 PM Central. These are prep only, not reservations or schedules. Re-read live state after picks. Preserve parent_config/after for `scripts/blotato/configs/ro11-calories-dont-matter.json`, never release before the parent is public.

Maintained ad_guard scanned 200 posts and found no ads in the organic queue. cover_audit returned no preflight issues. No Blotato mutation has occurred. After selections, final TikTok copies, covers and media verification, use organic_short_queue or the shared waitlist/top-up path. No direct organic YouTube holding upload. No per-video automation.

## Next execution

1. Record Dan’s three exact neutralX choices with maintained blind.py; install immutable originals, not normalized review copies.
2. Finish missing B Drive backup and checksum all required copies; preserve verified Extreme originals.
3. Build/check TikTok frame 0 copies without changing master audio; upload/full-hash-readback media and covers, register Facebook in repo and live installer.
4. Finalize configs and queue or shared waitlist after refreshed live capacity and slot checks; retain parent hold. Re-read actual saved URLs and byte hashes. Save final receipt; update edit queue only under verified setup-completion rule.

Work checkpoint: `/Users/danielrose/Projects/_edit_work/sl13-setup-20261107/RESUME.md`. Gallery asset root: `Short-form video content/covers/review/sl13-20261107/`. Private mappings/provenance stay in the work folder.

## Repository sync

Owned commits remain locally saved; safe-push is blocked by concurrently modified shared files, including `Handoffs/video-editing/00-MASTER.md` and `Handoffs/video-editing/jobs.json`, with additional live ads changes on the final attempt. Do not reset, stash, adopt or commit another active owner’s edits. Reattempt owned-file safe-push at the next phase. No production app code changed or deployment claimed.
