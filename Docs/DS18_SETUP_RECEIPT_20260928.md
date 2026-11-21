# DS-18 organic setup receipt (2026-09-28)

DS-18 "How To Kettlebell Deadlift" is an ORGANIC Short. On 2026-09-27 a handoff set it up as a paid ad by mistake;
Dan caught it on 09-28 and it was moved to the organic path the same day.

## Source

- Master: `Short-form video content/ds-18_how-to-kettlebell-deadlift.mp4`, 81,989,796 bytes, SHA-256 `aa7fe8747dcb3a4a8b26e1b32b598c1c502606ee00efe878ee99aaf2d1b60ba2`, 1080x1920, 41.94 s. Dan finalized R8 on 09-25.
- Closing words: "Get yourself a kettlebell and start kettlebell deadlifting at home. Leave me a comment and let me know how these tips work for you." No tap-the-button CTA, so organic.
- Delivery gate: FAIL, 33 passed, 6 failed, 3 n/a (`audio:stamp`, `framing:no_wide_level`, `framing:push_coverage`, `captions:burned`, `captions:sync`, `compliance:placeholder`); Dan finalized it with these known.
- Real footage only (C1671/C1673 + graphics): synthetic / AI flags false everywhere.

## Undoing the ad setup

- Google Ads ad groups `201586678778` (/start, ad `826267702259`) and `200462519173` (home, ad `826267702268`) PAUSED 09-28 after 90 impressions and $0.62. Campaign `24243839443` budget unchanged at $50/day.
- Removed from `Docs/AD_VIDEO_IDS.md`, so `ad_guard.py` no longer treats it as an ad.

## YouTube holding copy

- `CMsb0qbo2vM`, switched Unlisted → **Private** in Studio on 09-28 (the upload token has no scope to change visibility). API readback: `privacyStatus: private`, no `publishAt`, processed, 1080x1920, file size equal to the master. Thumbnail: approved cover C r5 (JPG export). Its description still carries the ad-path UTM; it stays private, so nobody sees it.

## Blotato release: Sat Oct 3, 2026, 9:00 AM CDT (`2026-10-03T14:00:00Z`)

| Destination | Schedule |
|---|---:|
| Facebook | `4938171` |
| Instagram @danrosefit (cover C r5, keyword `TRAIN`) | `4938172` |
| TikTok (cover-first copy, `videoCoverTimestamp: 0`) | `4938174` |
| YouTube public release (Blotato account 46963, cover C r5) | `4938175` |

All four verified on a fresh pull (0 problems); queue 110/200; `ad_guard.py --scan` clean. Config
`scripts/blotato/configs/ds18-kettlebell-deadlift.json`, UTM `utm_campaign=kettlebell-deadlift&utm_content=ds-18`.
Blotato media hashes matched the local files: master `aa7fe874…`, TikTok copy `da1adeed…`, cover `60215892…`.

## TikTok cover proof

- `Short-form video content/ds-18-support/platform-derivatives/ds-18_how-to-kettlebell-deadlift_tiktok-cover-C-r5.mp4`, SHA-256 `da1adeed83a0417cfd4624e5b5cef27f2868f6aee79d196423706f45d9258468`.
- Frames 1,257 → 1,258; audio packets 1,966 → 1,966; zero decode errors; cover match 50.9 dB.
