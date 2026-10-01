# Pick the 5 best ads and build the VSL-page campaign

Created 2026-09-30 by Dan's /prioritize session. Recommended model: **Opus 5.5, High effort** (data pull + judgment + Google Ads API writes).
Supersedes `handoff-20260929-start-page-performance-verdict.md`: Dan is folding /start into the new VSL sales page, and the
/start-vs-home numbers are a sub-section of this analysis. Whoever runs this deletes BOTH handoffs' rows from
`Handoffs/README.md` and the HANDOFFS section of `AI_COORDINATION.md` when done.

## Goal

Dan's sales page (design C2 "Video + Offer Hybrid", video WV-01 A, his sales letter) goes live today and replaces /start
for paid traffic. He wants a NEW Google Ads campaign pointed at that page, running the **5 best ads** from the current
Demand Gen campaign. Your job: rank every ad on the data, pick 5, and build the new campaign.

## Read first

- `Docs/DGEN_CONVERSION_CAMPAIGN.md`: campaign `24243839443` in account `342-717-0837`, $40/day shared budget, $30 target
  CPA, one `/start` and one home ad group per ad (Ads 1 to 10, 13, 14, 15), several formats per ad (16:9, 9:16, 9:16 59s,
  1:1, 1:1 59s). Every final URL carries `utm_campaign=dgen-conv-adN` and `utm_content=<video>-<start|home>`.
- `Docs/GOOGLE_ADS_API.md`, memory `google-ads-api-client` (`scripts/ads/api/client.js`, login-customer-id = the account,
  not the MCC), memory `google-ads-scripts-mutate-traps`, `scripts/ads/api/dgen-add-ad.js` + the JSON specs in
  `scripts/ads/api/dgen-ads/` (reuse this pattern to build the new campaign).
- `Docs/VSL_LANDING.md` (PostHog events, `landing_variant`), memory `vsl-landing-page`, `proven-direct-response-only`,
  `ad-retry-rule-and-no-trick`, `ads-never-organic`.
- Secrets: `~/.absbyai-secrets.env` (PostHog, Google Ads, `DATABASE_URL`, Stripe). Never paste values anywhere.

## Step 1: pull the numbers (2026-09-10 to today)

Per ad AND per video asset (format), from the Google Ads API:
impressions, views, view rate, average watch % (quartiles), clicks, CTR, cost, CPC, conversions and cost per conversion
by conversion action (name which action each conversion is; do not blend them), policy status.

Per `utm_campaign` + `utm_content`, from PostHog: landing pageviews, VSL play, photo upload / `generation_started`,
generation complete, `trial_signup_started`, `membership_subscribed`, `paid_conversion_reported`.
Cross-check trials and paid against Stripe / Postgres. Expected: very few or zero trials and sales.

Also split /start vs home (the landing page comparison): same funnel, both pages, so Dan sees whether /start was worse
than home or the whole offer was. Keep this section to one table and one sentence.

## Step 2: rank

Dan's rule: judge paid traffic on **cost per trial and cost per paying customer**. If there are not enough trials to rank
on, say so plainly and step down one rung at a time, stating which rung decided the ranking:

1. cost per paid customer
2. cost per trial started
3. cost per generation started / photo uploaded
4. cost per landing-page VSL play, plus click-through rate
5. YouTube hold: view rate and average watch % (a proxy for how well the ad holds attention)

Rank at the AD (concept) level; pick the best-performing FORMAT for each ad. Flag small samples (under ~$20 spend or under
~50 clicks) instead of treating them as results. Exclude ads that are disapproved or stuck APPROVED_LIMITED unless the
fix is known. Keep the Ad 2 16:9 master problem in mind (banned BEFORE/AFTER screen at 3:11, email screen 3:12 and 3:23:
board, DAN'S DECISIONS): if Ad 2 wins, use its vertical or square only if those beats are absent there, else flag it.

## Step 3: pick 5

Five ads, each with the format(s) to run. Prefer variety of angle (not five versions of the same hook). For each pick,
list which formats already exist on YouTube and which are missing (a 9:16 or 1:1). Missing formats become Claude
video-editing jobs: name the edit-queue job id (`Handoffs/video-editing/jobs.json`, AV-* for verticals, AS-* for
squares) and say whether it is READY. Do not cut them yourself.

## Step 4: build the new campaign

- New Demand Gen campaign, same account, same structure pattern as `24243839443` (one ad group per ad, $30 ad-group
  target CPA, same audiences per ad, US + CA, English), final URL = the new VSL page with fresh UTMs
  (`utm_campaign=dgen-vsl-adN`, `utm_content=<video>-vsl`). Name it `[DAN] [DGEN] [CONVERSION] VSL page | top 5 ads`.
- Build it **PAUSED** with `validateOnly` first, then apply, then read it back.
- **Only when the VSL page is live and verified** (the page-build session reports it; check the URL returns 200 and plays
  WV-01): enable the new campaign at **$40/day** and pause campaign `24243839443` in the same step, so total spend is
  unchanged. This is a budget move, not new spend, so it needs no ask. If the page is not live yet, leave the new
  campaign PAUSED and state the exact one command that flips it.
- Do not delete anything in the old campaign; pausing keeps its history.
- Run the policy check on the new ads (`node scripts/ads/api/client.js policy <campaignId>`) and report status.

## Deliverable

A private Artifact page Dan can read on his phone:
1. The 5 picks at the top, one line of reason each, with the metric rung that decided it.
2. The full ranking table (every ad, best format, spend, clicks, CPC, conversions by action, trials, paid, view rate, watch %).
3. The /start vs home table and one-sentence verdict (expected: fold).
4. The new campaign's id, ad ids, state (PAUSED or ENABLED), and the missing-format edit jobs to fire.
5. A numbered action list at the bottom.

Then update `Docs/DGEN_CONVERSION_CAMPAIGN.md` with the new campaign section, commit, push, and delete the two handoff
rows named at the top. No compliance commentary. No em dashes in anything you write.
