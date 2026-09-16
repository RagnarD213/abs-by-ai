# Ad 3 square setup — 2026-09-16

> **Updated instruction, 2026-09-16:** Dan requested an upload-as-is handoff and a separate future-checker repair handoff after the findings were explained. The previous internal-gate hold below is historical and superseded for this exact approved file. Execute `Handoffs/handoff-20260916-ad3-square-upload-as-is.md` without waiting for `Handoffs/handoff-20260916-video-checker-repair.md`. No upload or Ads change was made while writing the handoffs; the FAIL record remains truthful.

## Completed 2026-09-16

The exact approved square export was uploaded unchanged and unlisted to the Abs by AI channel as
[`DXRkrfvcJEM`](https://youtu.be/DXRkrfvcJEM). YouTube read-back confirmed processing succeeded, 1080×1080 HD,
4:26, embeddable, custom thumbnail, not made for kids, and Studio shows **Yes** for AI use. The existing description,
11 chapters, tags and approved dark-studio thumbnail were reused.

Google validation showed exactly one new video asset and two new ads, reusing the existing audience and groups.
Applied asset `422079967995`; `/start` ad `824906283483`; home ad `824906283486`. Both ads are ENABLED and
`UNKNOWN / REVIEW_IN_PROGRESS`. Campaign budget remains $40/day and target CPA remains $30; prior ads and settings
were unchanged. Both landing pages returned HTTP 200 with the complete UTM parameters intact.

This was uploaded as-is at Dan's explicit 2026-09-16 instruction. The v1.2.0 gate FAIL record remains preserved:
24 measured PASS, 3 N/A, 2 FAIL and 6 NOT MEASURED. This completion is a one-file release exception, not a fabricated
PASS or a relaxation of future checking. Detailed before/after account snapshots, validation/apply logs and YouTube
readback are in `output/ad3-square-setup-20260916/`. Organic/public posting was not done.

## Historical preflight — before Dan’s as-is instruction

**At that time, upload was held because the approved R2.1 export lacked the required delivery-gate PASS.** No YouTube or Google Ads account changes were made. No new video, asset or ad IDs exist.

The exact master fingerprint matches the setup handoff. The current delivery stamp verifier refuses it. Resolving this needs shared-checker support for its caption/composite inputs, validated against the regression corpus, and resolution of the retained uncertain source-content finding. Do not substitute another export, alter the approved audio, upload the short, or treat creative approval as a waiver.

## Pre-upload live setup verified

- Abs by AI channel: `UC236gjadarHAhEhOMYNGJ9g`; upload metadata dry run succeeded, unlisted, category 26, synthetic disclosure selected, not made for kids. Existing description has 11 valid chapters. Existing approved dark-studio thumbnail inspected.
- No Ad 3 square was found in the channel's matching-title inventory, local upload logs, or either existing ad group.
- Campaign `24243839443` remains ENABLED, budget `15862488218` **$40/day**, campaign target CPA **$30**. Both Ad 3 groups remain ENABLED with **$30** target CPA: `/start` `199782847163`, home `199360345839`.
- All six current Ad 3 ads are now `APPROVED / REVIEWED`: `/start` 824617143813, 824617143816, 824617143819; home 824617143822, 824617143825, 824617143828. Superseded ads 824427749693 and 824344861381 remain PAUSED.
- All live Ad 3 copy matches `scripts/ads/api/dgen-ads/ad3.json`. Both proposed destination URLs returned HTTP 200 without redirects or stripped tracking parameters.

## Prepared variant (executed above)

Title: **Stop Paying Human Trainers! Use AI Instead**. Ads version label: **Claude 1:1 R2.1**. UTM content: `claude-square-r2-1-start` / `claude-square-r2-1-home`, campaign `dgen-conv-ad3`. Reuse both groups, audience and current copy. After upload, use a square-only config; validate exactly one new asset and two new ads before applying. No Google Ads validateOnly call was made with a placeholder video ID.

The full 4:25 export exceeds the three-minute Shorts-ad limit; this does not by itself establish ineligibility for other Demand Gen placements. [Google Shorts ad specifications](https://support.google.com/google-ads/answer/16041697?hl=en), [Demand Gen specifications](https://support.google.com/google-ads/answer/17091672?hl=en).

Private operational evidence and detailed blocker assessment: `output/ad3-square-setup-20260916/`. The historical
preflight remains below for auditability; its upload hold was superseded only for this exact file by Dan's later
instruction. Future checker repair continues independently under `Handoffs/handoff-20260916-video-checker-repair.md`.
