# Ad 3 square setup — 2026-09-16

**Held before upload: the approved R2.1 export lacks the required delivery-gate PASS.** No YouTube or Google Ads account changes were made. No new video, asset or ad IDs exist.

The exact master fingerprint matches the setup handoff. The current delivery stamp verifier refuses it. Resolving this needs shared-checker support for its caption/composite inputs, validated against the regression corpus, and resolution of the retained uncertain source-content finding. Do not substitute another export, alter the approved audio, upload the short, or treat creative approval as a waiver.

## Live setup verified

- Abs by AI channel: `UC236gjadarHAhEhOMYNGJ9g`; upload metadata dry run succeeded, unlisted, category 26, synthetic disclosure selected, not made for kids. Existing description has 11 valid chapters. Existing approved dark-studio thumbnail inspected.
- No Ad 3 square was found in the channel's matching-title inventory, local upload logs, or either existing ad group.
- Campaign `24243839443` remains ENABLED, budget `15862488218` **$40/day**, campaign target CPA **$30**. Both Ad 3 groups remain ENABLED with **$30** target CPA: `/start` `199782847163`, home `199360345839`.
- All six current Ad 3 ads are now `APPROVED / REVIEWED`: `/start` 824617143813, 824617143816, 824617143819; home 824617143822, 824617143825, 824617143828. Superseded ads 824427749693 and 824344861381 remain PAUSED.
- All live Ad 3 copy matches `scripts/ads/api/dgen-ads/ad3.json`. Both proposed destination URLs returned HTTP 200 without redirects or stripped tracking parameters.

## Prepared variant

Title: **Stop Paying Human Trainers! Use AI Instead**. Ads version label: **Claude 1:1 R2.1**. UTM content: `claude-square-r2-1-start` / `claude-square-r2-1-home`, campaign `dgen-conv-ad3`. Reuse both groups, audience and current copy. After upload, use a square-only config; validate exactly one new asset and two new ads before applying. No Google Ads validateOnly call was made with a placeholder video ID.

The full 4:25 export exceeds the three-minute Shorts-ad limit; this does not by itself establish ineligibility for other Demand Gen placements. [Google Shorts ad specifications](https://support.google.com/google-ads/answer/16041697?hl=en), [Demand Gen specifications](https://support.google.com/google-ads/answer/17091672?hl=en).

Private operational evidence and detailed blocker assessment: `output/ad3-square-setup-20260916/`. The original setup handoff remains open. Next: obtain a legitimate delivery PASS, refresh live state, upload unlisted, then validate and add only the two intended square ads.
