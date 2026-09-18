# DS-04 setup receipt — 2026-09-18

## Source and accepted gate exception

- Master: `Short-form video content/ds-04_only-ab-exercise-that-shrinks-belly-fat.mp4`
- Size: 70,119,789 bytes
- SHA-256: `3e2a51b76ccf87aed6b02a002c84ccaf9013baf39466fb0345eeff8090df67b9`
- MD5: `5f4b445733fc208cedc17e6ba2535e77`
- Delivery gate: 36 PASS / 1 FAIL. The only failure is Dan’s accepted `audio:stamp` exception; no audio, threshold or render was changed.

## YouTube holding copy

- Video: `GNA1riDIdW4` — `https://www.youtube.com/watch?v=GNA1riDIdW4`
- Title: `How to Do a Stomach Vacuum to Shrink Your Waist`
- Readback: processing succeeded; `privacyStatus: private`; no `publishAt`.
- Synthetic-media flag: false.
- Thumbnail: existing DS-04 cover A; API readback returned a 1280×720 max-resolution thumbnail.

## Blotato release

Main release: Monday, September 21, 2026 at 9:00 AM CDT (`2026-09-21T14:00:00Z`). Mirror: Tuesday, September 22 at 9:00 AM CDT.

| Destination | Schedule | Verification |
|---|---:|---|
| Facebook | `4586862` | account, time, caption, target and media length match |
| Instagram @danrosefit | `4586863` | cover A, keyword `ABS`, account, time, caption and media match |
| TikTok | `4586884` | cover-first derivative, `videoCoverTimestamp: 0`, account, time, caption and media match |
| Instagram @abs.by.ai | `4586865` | cover A, account, time, caption and media match |
| YouTube | `4586866` | cover A, public release target, account, time, description and media match |

Queue readback: 185/200 schedules, zero verification problems. Ad guard scanned 185 schedules against 18 known ads and 31 ad video IDs: clean.

## TikTok cover proof

- Cover: `ds-04_only-ab-exercise-that-shrinks-belly-fat_cover-A.png`
- Derived file SHA-256: `678738a885dd988f110b321b417f073a0bd9e2c12859b86dcae852eb16740aab`
- Video frames: 1,502 → 1,503
- Audio packets: 2,351 → 2,351
- Cover match: 43.3 dB
- Full decode: zero errors

The derivative adds one imperceptible frame and stream-copies every original audio packet, so the accepted audio is untouched.
