# Ronaldo Ab Belt SFC setup receipt, October 25, 2026

CONTENT, dedicated Short (DS-33). Title: **Does Cristiano Ronaldo's Electric Shock Ab Belt Work?**

## Status

Dan approved cover 3, expression revision 3: "Okay this looks good. Go ahead and install this thumbnail" (2026-10-25). Exact approved covers installed locally, uploaded to Blotato storage and registered with the Facebook live cover installer. All four remote media files were downloaded and SHA-256 matched. The original film was preserved.

**WAITLISTED, not scheduled or published.** Blotato readback: 197/200 posts; the four-post dry run would reach 201/200 and refused. No schedule was created or replaced. One `DS-33`, `kind: short` entry is saved in `scripts/blotato/video_waitlist.json`. The existing daily `social-queue-daily-refresh` routine queues it as room frees. No per-video automation was created.

Planned slot: **Thursday, December 24, 2026, 9 AM America/Chicago**, `2026-12-24T15:00:00.000Z`, all four platforms. Earlier Thursdays belong to live or waiting dedicated Shorts. December 24 has no 9 AM clash in the live queue. The calendar moves the not-yet-edited DS-13 to December 31, DS-16 to January 7, 2027 and DS-01 to January 14. The routine must recheck the slot and read each saved schedule back when queuing.

## Approved film and backups

- Source: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/Short-form video content/Ronaldo Ab Belt - DS-33/Ronaldo Ab Belt SFC R5 - complete Short.mp4`
- Master SHA-256: `b78674a331cd51c6003614ea149dc89095fc1e2539406a0826a5a100f65e80d0`; 62,004,027 bytes; 1,867 frames, 1080x1920, about 62.30 seconds.
- SRT SHA-256: `810c7e13a186f6c807f49af73cb868af3c6488b5f72d023286cab747f551b4fa`.
- Project and Extreme master hashes match the locked R5 approval. Extreme SRT matches.
- [Google Drive backup folder](https://drive.google.com/open?id=1Sbz5RfSPnWwcwx1eZLc5v99A-bngRIwP): master, SRT, approved covers and description. `rclone check --download`: two matching film/SRT files and five matching cover/approval files, zero differences.
- Classification from exact ending: "Subscribe and go to SixPackAbs.com for all my newest videos." Organic content, no button CTA.
- `ai_generated: false`; the approved film contains no AI footage. AI thumbnail imagery alone does not trigger the video altered/synthetic flag.

## Approved cover and platform installation

Approval file: `Short-form video content/covers/approved-ds33/APPROVAL.json`. Full review source preserved under `Short-form video content/covers/review/ds33-ronaldo-20261023/option-3-laugh-r3/`.

| Platform | Account | Media / cover |
|---|---|---|
| YouTube | 46963 | Exact R5 master; approved YouTube JPEG in `thumbnailUrl`, under 2 MB |
| Facebook | 47105, page 1294282227094660 | Exact R5 master; approved YouTube-layout JPEG registered in repository and live installer |
| Instagram @danrosefit | 67203 | Exact R5 master; approved Instagram PNG in `coverImageUrl` |
| TikTok | 58181 | Lossless cover-first copy of R5; approved Instagram cover at frame 0; `videoCoverTimestamp: 0` |

TikTok verification: source 1867 frames, derivative 1868 frames; 2921 source and 2921 output audio packets; no decode errors; first-frame cover PSNR 49.14 dB. The additional frame is the required cover, with the original video/audio copied. No new edit or format.

Facebook exact first caption line: "Cristiano Ronaldo will sell you a belt that shocks your abs. But does it really work?". Both registries point at byte-identical approved JPEGs. Live copy: `~/.absbyai/fb-reel-covers/covers/ds33-ronaldo-ab-belt-approved.jpg`.

## Remote assets, downloaded and hash verified

| Asset | Bytes | SHA-256 | URL |
|---|---:|---|---|
| master | 62004027 | `b78674a331cd51c6003614ea149dc89095fc1e2539406a0826a5a100f65e80d0` | [asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/6cf90993-0227-459d-8358-4deb0ad53ff8.mp4) |
| tiktok | 62141443 | `ea064ba34a74fc8b9eea31c858ecbab07c5ad4f4682aec9883a32fe31933df36` | [asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/f857ea0a-2344-46ac-a186-7c1ed927652a.mp4) |
| instagram | 1818978 | `11a3232175d2d10a8c1cea96af3b6c22a759a27d89a6b9b3f5341a1c80f2c8c0` | [asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/daffd2be-0f44-4249-8c40-eba9a08ee552.png) |
| youtube | 356838 | `bea467903d0c79b6d8f0120122b51ac8950f6761da11fd7e3424a49f908f3c63` | [asset](https://database.blotato.io/storage/v1/object/public/public_media/a836fa29-cde6-464e-8712-36d8a0de9f32/781c9459-be00-496b-b878-1058a554df7d.jpg) |

## Packaging and release checks

Config: `scripts/blotato/configs/ds33-ronaldo-ab-belt.json`. Exact title preserved. Captions use the filmed points; each platform carries the absbyai.com root with its own UTMs. No free-image offer. Pinned question and caption drafted by the clean `dan-voice-writer` from the voice helper's real passages; the Claude CLI writer was unavailable because its OAuth session had expired, so a clean Codex writer used the same prepared prompts. No paid generation calls.

**Pinned comment:** "Have you ever tried one of these electric shock ab belts before?". Saved and verified in config, not posted yet. Posts and pins after release through the existing `youtube-pinned-comment-daily` routine. A public YouTube ID does not exist yet. Release check: `node scripts/youtube/pinned_comment_gap.js`; the public thread must visibly show it pinned.

**Article:** dedicated Short, nothing to write at setup. The existing `sixpackabs-article-gap-daily` routine writes a 300-500 word article or records a duplicate-topic skip after release.

Before/after: `ad_guard.py --scan` clean; `cover_audit.py` no cover issues. The four generated payloads pass `assert_video_cover` including both Facebook registries. The approved cover review checks also pass.

**Still unobserved:** actual public YouTube, Facebook, Instagram and TikTok tiles can only be checked after release. The existing cover monitor performs those checks; stored URLs and frame-zero verification are preparation, not proof of public tiles. Repair a wrong YouTube tile in Studio without deleting the video.

Edit Queue remains **finalized** while waitlisted. Set DS-33 to uploaded only after all four saved schedules exist and read back.

Evidence, including queue snapshots, upload hashes, cover-first check, post plan and dry runs: `/Volumes/Extreme/_edit_work/ds33-publish/`.
