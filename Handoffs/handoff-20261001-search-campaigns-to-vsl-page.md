# Search campaigns: send everything to the /start sales page and optimize for trial signups

Created 2026-10-01 by Dan's planning session. Recommended: **GPT-6 Sol, High** (Google Ads ops by API). Claude fallback: Opus 5.5, High.

## Goal

Dan wants all Google Search traffic landing on the VSL sales page, `https://absbyai.com/start` (his sales letter, live there
since 2026-09-30). Account `342-717-0837`.

## What is already true (read 2026-10-01)

| campaign | id | state | bidding | budget |
|---|---|---|---|---|
| Brand - Search - US | `24086091285` | ENABLED | Target spend | $10/day |
| Search - US - Non-Brand - AI Abs Preview | `24148587722` | ENABLED | Maximize conversions | $5/day |

Every ad in both campaigns (6 enabled, 5 paused) already has the final URL `https://absbyai.com/start`. The ad-level URL
move is done. What is NOT confirmed is everything else that carries a URL, and what the campaigns optimize for.

## Do

1. **Audit every other URL** in both campaigns and at account level: sitelinks, other assets with a link, keyword-level
   final URLs, ad group and campaign tracking templates, final URL suffix. Anything pointing at `/`, `/?join=1` or any
   non-/start page gets repointed to `/start`. Paused ads included. List what you changed.
2. **UTMs:** every final URL carries `utm_source=google&utm_medium=search&utm_campaign=<brand|nonbrand>&utm_content=<ad group>`
   so PostHog can split search from the video ads. Add them where missing (URL suffix at campaign level is cleanest).
3. **Conversion goal:** switch both campaigns to **Trial Signup** (`7704441545`) as a campaign-specific goal. They were
   chasing Free Generation Started, which the sales page no longer produces. Depend on Step 1 of
   `handoff-20261001-vsl-trial-campaign-six-ads.md` for proof that the trial conversion fires; if that task has not run,
   do that check yourself first.
4. **Copy match, report only:** read each enabled ad's headlines and descriptions against the live /start page. The
   non-brand ad groups (AI Abs Generator, Add Abs To Photo, What Would I Look Like With Abs, AI Body Transformation
   Preview) were written to promise a free AI preview, and the page now sells a free trial. List every headline or
   description that promises something the page does not deliver. Do NOT rewrite ad copy; give Dan the list.
5. Run `node scripts/ads/api/client.js policy 24086091285` and `… 24148587722` after the changes.

Dry run first, then apply, then read back. Pause only, never remove. Do not change budgets or bids.
Read `Docs/GOOGLE_ADS_API.md` and memory `google-ads-api-client` first. Note the open decision on the board: Google
auto-apply removed the $2 CPC ceiling on 09-11; leave it as is.

## Done when

Changes listed in chat with a numbered action list (the copy-mismatch list goes last), a dated section added to
`Docs/GOOGLE_ADS_API.md`, a PostHog annotation, committed and pushed, and this handoff's rows deleted from
`Handoffs/README.md` and `AI_COORDINATION.md`. No em dashes.
