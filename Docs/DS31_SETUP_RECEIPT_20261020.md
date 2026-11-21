# CONTENT: AI Homework SFC Setup

Updated: 2026-10-20. Job: DS-31. Status: complete, scheduled on all four organic destinations.

Approved cover: round 2 option **B** (pull-ups, amber banners: a college student does pull-ups while a robot types his homework on a laptop resting on textbooks). Top text "Make Time To Work Out", bottom "Let AI Do Your Homework". Dan: "Let's go with B: finalizing install B." Round 1's five covers were rejected ("I don't like any of these"); Dan then specified the robot-does-homework concept and the two text lines. Same B design on all platforms: full-bleed layout for YouTube, framed-panel layout for the Instagram/TikTok grid crop and Facebook.

## Saved release

**Thursday, December 3, 2026 at 9 AM America/Chicago (CST)**, the DS-31 Thursday on `Docs/SHORTS_RELEASE_CALENDAR.md`. All four use `2026-12-03T15:00:00.000Z`. Queue 183 to 187 of 200; no waitlist entry needed.

| Destination | Account | Saved schedule | Cover |
|---|---|---|---|
| facebook | 47105 | 5822390 | B (registry + live installer) |
| instagram @danrosefit | 67203 | 5822391 | B grid layout |
| tiktok | 58181 | 5822392 | B as frame 0, `videoCoverTimestamp: 0` |
| youtube | 46963 | 5822394 | B full layout |

Title: **Let AI Do Your Homework So You Have Time To Work Out**. Config: `scripts/blotato/configs/ds31-ai-homework.json` (`content_type: organic`, exact source, `ai_generated: true`, keyword COACH, UTM campaign `ai-homework`). Every saved post was read back for account, time, caption, AI flag and cover; Blotato's per-post media copies were downloaded and hashed: YouTube, Facebook and Instagram equal the master; TikTok equals the cover-first copy. Record: `Handoffs/video-editing/DS-31-cover-review/saved-schedules.json`.

## Film and cover verification

- Exact approved R2 master: `Short-form video content/AI Homework - DS-31/AI Homework SFC R2 - complete Short.mp4`, 94,943,517 bytes, SHA-256 `69213798dd2c34fe88eace189c869d5169ca990f67e877aafde3c15d7777c2ba`. Not re-rendered or edited.
- TikTok copy (maintained `tiktok_cover.build`): 1,848 to 1,849 frames, 2,891 audio packets unchanged, zero decode errors, cover PSNR 49.48 dB; uploaded frame 0 extracted and inspected (cover B, film starts after it). SHA-256 `8fb0881a1c6c1f0c5382006e120684f0a486d9064332ae7a2ef98cf888bd5bdd`.
- Cover URLs downloaded and hash-matched to the approved 1080x1920 JPEGs: YouTube 589,572 bytes (under 2 MB), grid layout 498,794 bytes.
- Facebook cover registered for first caption line "If you're in college and you have no time to work out, I'm about to solve that problem for you." and schedule 5822390, in the repo registry and the live installer (`~/.absbyai/fb-reel-covers/covers/ds31-ai-homework-B.jpg`); LaunchAgent loaded.
- `ad_guard.py --scan` before and after: clean. `cover_audit.py` before and after: zero issues. These are queue checks, not public-tile checks.

## Backups

Google Drive: https://drive.google.com/drive/folders/1JDWRjptIeh4hxtI_ZirstggZaw7YTeWn (anyone-with-link reader, read back through the Drive connector). Master, SRT, APPROVAL.json, both covers and the Codex source image were downloaded back and match by SHA-256. Project and Extreme copies preserved. Cover recipes, prompts and manifests: `Handoffs/video-editing/DS-31-cover-review/`; media under `Short-form video content/AI Homework - DS-31/covers/` and `setup/` (git-ignored).

## Release follow-through

Pinned comment: "How many hours a week do you spend on homework right now?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).

Article: dedicated Short; handled after release by `sixpackabs-article-gap-daily` (article or recorded skip).

Public cover checks remain outstanding until release: YouTube Shorts portrait tile, Facebook cover, Instagram tile, TikTok static grid image (existing `check-youtube-shorts-covers` covers all four). A wrong YouTube tile is repaired in desktop Studio, never by re-uploading.

DS-31 is `uploaded` in the Edit Queue (Drive status file and artifact db mirrored). Codex image use: round 1, 5 images (one regenerated); round 2, 3 images plus one edit. No paid spend.
