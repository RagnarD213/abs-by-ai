# Ad 4 conversion remarketing receipt

## 2026-10-05: Ad 4 formats added to live conversion remarketing

Dan authorized this follow-up: "Yes. Also put them in the live conversion remarketing campaigns not in the engagement campaigns, though". This resolves the pending Ad 4 remarketing decision from 10-04.

The live account has one enabled Demand Gen conversion remarketing campaign, `24305381214`, with Trial Signup (SIGNUP / WEBSITE) as its sole biddable goal. Added the four Ad 4 formats to both existing enabled groups: Website visitors `206411886211`, YouTube viewers `201604959278`. Eight ENABLED ad copies in total, using the existing YouTube video assets and exact live trial-ad copy, logo, business name and CTA. No new uploads, thumbnails or copy.

| Format | YouTube id | Website visitor ad id | YouTube viewer ad id | Initial policy status |
|---|---|---|---|---|
| Claude 9:16 | `Sr9gux0gB5I` | `827113765613` | `827113765616` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 9:16 59s | `TPlpl0LETqw` | `827113765619` | `827113765622` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 1:1 | `kyrAfWkg92k` | `827113765625` | `827113765628` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |
| Claude 1:1 59s | `eJ-dTPw40Hk` | `827113765631` | `827113765634` | ENABLED, REVIEW_IN_PROGRESS / UNKNOWN |

Final URLs follow the existing remarketing convention: `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-rmktg-<site|yt>&utm_content=ad4-<claude-vertical|claude-vertical-59s|claude-square|claude-square-59s>-vsl`. Exact per-ad URLs in the result receipt.

Builder: `scripts/ads/api/dgen-ad4-remarketing.js`. Only eight ad create operations were sent to the two existing conversion groups. Google validateOnly passed before apply. Configured budgets remain unchanged, including conversion remarketing budget `15911284202` at $10/day. Campaign/group bids, statuses, audience definitions, criteria and conversion goals compared exactly before/after across the account. All 222 pre-existing account ads compared exactly, including trial Ad 4 and the live 16:9. Engagement campaigns were untouched. No campaign enabled or paused, no organic posting.

Policy command ran after apply: eight new remarketing ads ENABLED, REVIEW_IN_PROGRESS / UNKNOWN. Also completed the due 10-05 trial policy recheck: all four original Ad 4 format ads are now APPROVED / REVIEWED and ENABLED. Recheck new remarketing ads on **2026-10-06** with `node scripts/ads/api/client.js policy 24305381214`. No automation created.

Before fingerprints, operations, mutation, verified result and policy report: `scripts/ads/api/dgen-ads/ad4-remarketing-20261005*`. Trial policy report: `scripts/ads/api/dgen-ads/ad4-formats.policy-20261005.txt`.
