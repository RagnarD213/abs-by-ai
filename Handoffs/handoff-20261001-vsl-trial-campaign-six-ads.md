# New Demand Gen campaign: six ads to the /start sales page, optimized for free trial signups

Created 2026-10-01 by Dan's planning session. Recommended: **GPT-6 Sol, High** (Google Ads ops by API). Claude fallback: Opus 5.5, High.
Replaces `handoff-20260930-ad-performance-pick-5-for-vsl-campaign.md` (the analysis was done in chat; Dan chose these six himself).

## Dan's spec (do not change)

- New Demand Gen campaign in account `342-717-0837`. Name: `[DAN] [DGEN] [TRIAL] VSL page | 6 ads | MU 25-54 | US+CA`.
- Budget **$50/day**. Bidding: **target CPA**, each ad group's CPA bid **$40**.
- Frequency cap: **4 impressions per user per day**.
- Optimizes for **free trial signups only** (conversion action `Trial Signup`, id `7704441545`). Not Free Generation Started.
- Final URL: `https://absbyai.com/start` with `utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-<ad>&utm_content=<video>-vsl`.
- One ad group per ad. Every approved format of an ad lives in that ad's group as one unit.

## The six ads and the videos that exist today (all Unlisted on YouTube)

| ad group | videos |
|---|---|
| Ad 13 The Cost Of Getting Abs | 16:9 `-SuKGXGcbIg` |
| RA-01 AI Got Me Abs | 16:9 `OUw788sF1KY`, 9:16 `rfCsWNxuNV0` |
| Ad 10 Busy Dad Fitness | 16:9 `Sg3vcEY2P_8`, 9:16 `4nDWFmdjzQQ`, 9:16 59s `CR4WAVmSuXY` |
| Ad 4 Stop Wasting Money On Supplements | 16:9 `R08TPEtkjuQ` |
| Ad 3 Stop Paying Human Trainers | 16:9 `86jbUhqBTUQ`, 9:16 `xlC-tigurnA`, 9:16 59s `-wTErCSi640`, 1:1 `DXRkrfvcJEM` |
| Ad 6 You're Not Too Old | 16:9 `Je2yvk00SHE` |

Verticals and squares for Ads 13, 4 and 6 are being cut in separate tasks (`handoff-20261001-ad13-other-formats.md`,
`…-ad4-…`, `…-ad6-…`). They get added to these ad groups later by `/ad-setup`. Do not wait for them.

## Step 1: prove the trial conversion works BEFORE building

1. Read `Docs/WEB_CART.md`, memory `web-cart-pay-first` and `stripe-trial-end-active-before-charge`. Find where the web cart
   fires the Google Ads `Trial Signup` conversion (gtag id `AW-18361229851`, `AD_CONVERSION_ID` in `public/index.html`) and
   confirm the path from `/start` → cart → trial started reaches that code. The new /start page went live 2026-09-30
   (`build_live.py`); confirm its CTA lands in the same cart and carries the gclid through.
2. Run the flow end to end locally (memory `local-funnel-test-recipe`, Stripe test mode, test card) and confirm the conversion
   request (`.../pagead/conversion/18361229851/...` with the Trial Signup label) is sent exactly once, at trial start.
   Never run a real card on production.
3. In Google Ads, read the `Trial Signup` action: status, last conversion date, tag status. It has recorded at least one
   conversion from this account (Ad 2 home group).
4. If anything is broken, fix it (commit, push, deploy, live-verify, flag the native retest) before Step 2, and say what was wrong.

## Step 2: build

- Model it on campaign `24243839443` (`Docs/DGEN_CONVERSION_CAMPAIGN.md`; `scripts/ads/api/dgen-add-ad.js` and the specs in
  `scripts/ads/api/dgen-ads/`). Reuse each ad's existing video assets, headlines, descriptions, logo, audience, US + CA by
  presence, English. Read memory `google-ads-api-client` and `google-ads-scripts-mutate-traps` first.
- Campaign-level conversion goal: Trial Signup only (campaign-specific goal, so the account default goals are untouched).
- Frequency cap 4 per user per day. If the API version does not expose it for Demand Gen, set it in the Ads UI
  (memory `google-ads-ui-automation`) and read it back.
- `validateOnly` dry run, then apply, built **PAUSED**. Read everything back. Run `node scripts/ads/api/client.js policy <newId>`.

## Step 3: switch

When every ad is approved (or approved-limited with a known cause): enable the new campaign and **pause campaign
`24243839443` in the same step**, so spend stays at $50/day total, not $100. Pause only, never remove. If review is still
running when the session ends, leave the old campaign on and write the exact command that makes the switch.

## Done when

New campaign id, ad group ids, ad ids, policy status and state reported in chat with a numbered action list; a dated section
added to `Docs/DGEN_CONVERSION_CAMPAIGN.md`; a PostHog annotation at the switch; committed and pushed; this handoff's rows
deleted from `Handoffs/README.md` and `AI_COORDINATION.md`; dashboard row "Pick the 5 best ads and launch the VSL-page
campaign" checked off after the switch. Report after 3 days if the $40 target is producing no delivery. No em dashes.
