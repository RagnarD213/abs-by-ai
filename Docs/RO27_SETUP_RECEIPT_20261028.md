# Boring Abs At 40: completed upload and scheduling

Updated: 2026-10-28. CONTENT (LFC). Owner: Codex.

**Uploaded to Blotato and scheduled on all four destinations. Not yet public.** Dan approved exact R3 design1, title-capitalized, and asked to finish upload and scheduling. Approved full R5 preserved.

Title: **This Boring Daily Routine Got Me Abs At 41**.

| Platform | Release, America/Chicago | Schedule ID |
|---|---|---|
| YouTube | Wednesday November4,2026,9AM | 6164756 |
| Facebook | Thursday November5,2026,noon | 6164753 |
| Instagram @danrosefit | Thursday November5,2026,noon | 6164754 |
| TikTok | Thursday November5,2026,noon | 6164755 |

The October28 phased calendar supersedes the handoff's old November15/16 target. Live November4/5 slots were clear; existing posts were not displaced. Four new schedules fill the queue from196 to200. No waitlist entry or per-video queue automation.

## Approved files and backups

[Google Drive delivery folder](https://drive.google.com/drive/folders/1Mnv9NA8fxzsSWsqGPx4VUBUL2hd9nvno). Project/Extreme/Drive bytes and SHA256 agree for all three files:

- `Boring Abs At 40 - thumbnail FINAL.jpg`: 450994 bytes, SHA256 `0aa533016c08de2e37ce6cc2f5a6c758e5eea99953d4ff90c4c2b92ba4836e3f`.
- `Boring Abs At 40 | codex | 16x9 | RO-27.mp4`: 216405614 bytes, SHA256 `903b9913061a152f5c8cac326971a69b430e53eb489ed6cf6a7c6855a0d469ec`.
- `Boring Abs At 40 | codex | 16x9 | RO-27.srt`: 15120 bytes, SHA256 `07628c6201d33548357c5dcf89ded0725ea812f5920c8218aaad8988560eddc2`.

The actual saved media URLs for all four schedules were downloaded and checked by SHA256; all match their intended master/TikTok source. Both YouTube/Instagram cover fields retain the exact approved JPEG URL, which was downloaded/decoded/hash-verified. Facebook cover added to repository and live installer; exact hook and approved file hashes match, schedule6164753 registered. TikTok frame zero was visually inspected and passed51.26dB PSNR;14,417 source frames became14,418,22,551 audio packets unchanged, exact audio payload SHA256 preserved, full decode no errors.

## Packaging and release work

Config: `scripts/blotato/configs/ro27-boring-abs-at-40.json`. Description, actual SRT-derived chapters,9 keyword tags and all platform captions/UTMs prepared. Organic product links use the app homepage. The Daily Salad link uses site search because its new public YouTube ID does not exist until November1 release. Both internal article links returnHTTP200.

Article: `sixpackabs/articles/TBD-ro27-boring-abs-at-40.md`, 1005 words, build.py --check OK; exact queued title. Publishes automatically after release through existing `sixpackabs-article-gap-daily`. `cta_path: /` makes its product link use the homepage; optional rendering added and tested for six block types and rejected invalid destinations. Existing article default remains unchanged.

Pinned comment: "What is one thing you do every day that helps you stay in shape?" Posts and pins after release through existing `youtube-pinned-comment-daily`. English SRT and actual public cover checks remain post-release work, as no public YouTube ID exists yet. YouTube keyword tags are saved in config; no unsupported Blotato target field or live tag application is claimed.

Realistic AI-motion flags retained: YouTube containsSyntheticMedia=true and TikTok isAiGenerated=true. This was determined by the film, not the thumbnail. Final ending is organic: subscribe and SixPackAbs.com, no tap/click button CTA.

Ad guard before/after: clean. Complete queue cover audits before/after:0 issues. Exact saved targets, text, times and media checked from fresh schedule pulls. Existing release checks must confirm YouTube public before next-day socials; postpone those if public release fails. Saved cover fields are not claims about future public tiles.

## State and records

RO-27 marked uploaded rev6 and Drive status file upload confirmed. SL-26 remains registered, ready, unattended false;3 Shorts need transcript shortlist/segment picks and separate editing. Its stale November15 parent note was updated to the actual November4 booking. No Shorts edit launched. Dispatcher and old editing heartbeat were not resumed. No Victory Dashboard.

Setup evidence: `Codex Content Videos/Boring Abs At 40 - RO-27/setup/`, including actual saved schedule readbacks,5 downloaded URL hash proofs, upload state, three-copy Drive readback, article/writer checks and TikTok verification. This task used clean writer fallback after Claude OAuth failed before inference; approved transcript facts and hard rules passed. No new metered image/motion generation or external stock downloads in this phase. Original movie gates and approvals retained honestly; no new film numerical PASS claim.

Repository changes pushed through safe-push. App homepage returnedHTTP200. Automatic Railway app deployments were queued when checked, not complete; unrelated concurrent builds remain untouched. Offline publishing utility/config changes only, no native retest trigger.
