# CONTENT: Meal Prep SFC Setup

Updated: 2026-10-17. Job: DS-28. Status: complete, scheduled on all four organic destinations.

Approved covers installed: option 3, revised tall lettering for YouTube; clean navy A for Instagram, Facebook and TikTok. Dan: "The tall looks good. Let's go with A, the clean navy. Go ahead and install that".

## Saved release

**Saturday, October 24, 2026 at 9 AM America/Chicago (CDT).** All four use `2026-10-24T14:00:00.000Z`. Live queue and recent channel uploads were inspected before choosing the next free Tue/Thu/Sat slot.

| Destination | Account | Saved schedule | Cover |
|---|---|---|---|
| facebook | 47105 | 5694638 | Clean navy A |
| instagram | 67203 | 5694640 | Clean navy A |
| tiktok | 58181 | 5694641 | Clean navy A |
| youtube | 46963 | 5694642 | Revised tall option 3 |

Title: **Stop Cooking Your Meals: Use A Meal Prep Service**. Config: `scripts/blotato/configs/ds28-meal-prep.json`. Each saved post was read back for account, time, caption, AI flag and target settings. Blotato copied media to a separate URL per post; all four actual per-post downloads were hashed against their approved upload files. No duplicate post was created. Queue moved from 195 to 199 of 200. No waitlist entry is needed.

## Film and cover verification

- Exact approved R5 master: `Short-form video content/Meal Prep - DS-28/Meal Prep SFC R5 - complete Short.mp4`, 124,841,554 bytes. SHA-256: `200afaaab059109b3fc168624136c0bb074d809d521d733ffee5b94ddf4298da`. YouTube, Facebook and Instagram queued media match these bytes.
- SRT: `Meal Prep SFC R5.srt`, 4,497 bytes. SHA-256: `1e0c6077df27e05a6f22b04325269c8a0d82962ac21e8bf0ccd6ad8eebfe5d18`.
- Film, captions, timing and approved mix preserved. Historical measurements and exact-file final approval remain in their original records. No new film render or paid review.
- The maintained TikTok helper added only the required cover frame: 1,785 source frames to 1,786 frames. Full decode had no error; cover PSNR 52.15 dB. Original 2,793 AAC packets retained, and extracted AAC bytes hash-identical (`72dc18a349f860e85b90a28dac6c33fa446f37b61b2667b9672907178c1de52c`). TikTok queued file: 124,962,424 bytes. Actual uploaded frame zero was extracted and visually inspected. `videoCoverTimestamp: 0`.
- Both supplied image URLs were downloaded, decoded and hash-compared with the approved 1080x1920 RGB JPEGs. YouTube cover: 569,790 bytes. Clean navy A: 457,640 bytes.
- Facebook cover registered for exact caption first line "Stop cooking your own meals." and schedule 5694638. Live installer registry and `~/.absbyai/fb-reel-covers/covers/ds28-meal-prep-clean-navy.jpg` match the approved cover. Existing 20-minute LaunchAgent is loaded.
- Live ad scan before and after: no ad content in the queue. Cover audit before and after: zero issues. These are scheduling checks, not a claim about public tiles before release.

## Backups and reproducible files

Google Drive: [https://drive.google.com/drive/folders/1QStsSUo4DJZU3QRdKR3dvtm2ovcgTl9a](https://drive.google.com/drive/folders/1QStsSUo4DJZU3QRdKR3dvtm2ovcgTl9a). Anyone-with-link reader permission was read back through the Drive connector. The master, SRT and both selected covers were downloaded from Drive and matched their local byte counts and SHA-256 hashes. The selected AI source image, upscale, prompt and round 2 recipe/assets are filed there. Project and Extreme copies are preserved.

Local package: `Short-form video content/Meal Prep - DS-28/setup/`. Tracked records and cover recipe: `Handoffs/video-editing/DS-28-cover-review/`. `installation-receipt.json` records upload URLs, actual per-post URLs, checksums, IDs and exact approval. Personal media stays out of the public Git repository.

## Release follow-through

Pinned comment: **"What meal prep service have you tried?"**. Saved in the config. The existing `youtube-pinned-comment-daily` routine posts and pins it after release. No YouTube holding copy or native scheduling. Blotato creates the YouTube video at release. Realistic AI scenes are flagged on the supported platforms.

Article: dedicated Short, handled by existing `sixpackabs-article-gap-daily` after release, or its documented skip.

Public cover checks remain outstanding until release: actual YouTube Shorts portrait tile, Facebook cover, Instagram tile and TikTok static grid image. Existing `check-youtube-shorts-covers` checks all four platforms. A wrong YouTube tile is repaired in desktop Studio on the public video ID, without deleting or re-uploading the film. No new monitor or per-video queue routine was created.

DS-28 is `uploaded` in the Edit Queue. `queue.py` uploaded the Drive status file; the next Claude pending sync mirrors the artifact fallback. Dispatcher remains paused. Victory Dashboard untouched. The executed handoff was removed from OPEN and this completed task was removed from the coordination board.
