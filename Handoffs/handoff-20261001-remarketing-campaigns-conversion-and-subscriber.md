# Two new remarketing campaigns: conversion (free trials) and subscriber (YouTube subs)

Created 2026-10-01 by Dan's planning session. Recommended: **GPT-6 Sol, High** (Google Ads ops by API). Claude fallback: Opus 5.5, High.

## Goal

Build two Demand Gen remarketing campaigns in account `342-717-0837` (customer `3427170837`). They show ads only to
people who already visited absbyai.com or already watched one of Dan's YouTube videos.

## Dan's spec (decided 2026-10-01, do not change)

| | Campaign A: conversion remarketing | Campaign B: subscriber remarketing |
|---|---|---|
| Name | `[DAN] [DGEN] [TRIAL] [RMKTG] VSL page \| 6 ads \| US+CA \| site visitors + youtube viewers` | `[DAN] [DGEN] [ENGAGEMENT] [RMKTG] geo tier 1 \| ALL CONTENT \| site visitors + youtube viewers` |
| Budget | **$10/day** | **$10/day** |
| Optimizes for | **Trial Signup only** (`7704441545`), never Free Generation Started | **YouTube channel subscriptions** (`7717762965`) only |
| Bidding | target CPA **$40** (same as the cold trial campaign; planning session's default, Dan did not name a number) | target CPA **$3** (Dan's pick) |
| Countries | US + Canada, by presence, English | the exact country set of tier 1 campaign `24163535721` (copy its positive and negative location criteria and its language) |
| Ads | the same six ads as cold trial campaign `24316364155` | copies of every ad ENABLED in tier 1 campaign `24163535721` at build time (7 on 10-01) |
| Excluded | members and purchasers | members, purchasers **and current subscribers** |

**Both campaigns have the same two ad groups:**

1. **Website visitors**: the 7, 30 and 365 day website lists together in one group.
   Lists: `9452848282` (7 day), `9453529251` (30 day), `9452257061` (365 day).
2. **YouTube viewers**: the 7 and 30 day "watched any video" lists together in one group, any video type.
   Lists: `9453532227` (7 day), `9452269226` (30 day).

Demographics (planning session's default): match the cold campaign each one mirrors. Campaign A copies the age and gender
settings of `24316364155` (male + unknown, 25-54 + unknown). Campaign B copies ad group `206274722584` in tier 1.

## What is already true (read 2026-10-01, verify before relying on it)

- Cold trial campaign `24316364155` is built and ENABLED. Its result file is `scripts/ads/api/dgen-ads/trial-campaign.result.json`;
  it holds the ad copy, video assets, goal setup and frequency cap to copy. Its six ads and videos:
  Ad 13 `-SuKGXGcbIg`; RA-01 `OUw788sF1KY`, `rfCsWNxuNV0`; Ad 10 `Sg3vcEY2P_8`, `4nDWFmdjzQQ`, `CR4WAVmSuXY`; Ad 4 `R08TPEtkjuQ`;
  Ad 3 `86jbUhqBTUQ`, `xlC-tigurnA`, `-wTErCSi640`, `DXRkrfvcJEM`; Ad 6 `Je2yvk00SHE`. If more formats were added to the
  cold campaign since, copy whatever is enabled there on build day.
- List sizes: website visitors about 110 (display) to 430; YouTube "watched any video" about 21,000. The website group
  will read small or "limited" at first. That is expected; build it anyway. It grows as the cold campaign runs.
- **List lifespan mismatch.** `9452257061` is named "365 day" but reports `membership_life_span` 30. Same for most lists
  named 365 or 540. Before building, open each of the five target lists (API, and the Audience manager UI for the YouTube
  rule's lookback window), and make each list's real window match its name. Fixing a lifespan is a routine reversible edit.
- **Members list does not exist yet.** `website | member hub | 540 day` (rule: URL contains `/vp/hub`, 540 days) was specified
  in `handoff-20260908-google-ads-custom-segments.md` (lines 121-132) and never built. Build it first; the `/vp/hub` beacon
  was verified live on 09-08. It will be too small to serve, which is fine for an exclusion.
- Exclusion lists: the new member hub list, `All Converters` `9441311426`, `Purchasers of Abs By AI` `9469016618`.
  Subscribers (Campaign B only): `youtube | subscribed to channel | 540 day` `9452604668`.
- Old remarketing campaign `24169507109` is PAUSED. It paid $55 per subscriber because its target was $50 and it did not
  exclude subscribers. **Leave it paused. Do not remove, edit or re-enable it.**

## Build steps

1. Read memory `google-ads-api-client`, `google-ads-scripts-mutate-traps`, `google-ads-ui-automation`, and the traps section
   of `Docs/DGEN_CONVERSION_CAMPAIGN.md` (lines 355-370). Key trap: an API-made Demand Gen ad group is always "audience
   grouped", so targeting goes in an `Audience` object (age, gender, user lists, exclusions) attached as an `audience`
   criterion, not as loose criteria.
2. Fix the list lifespans and build the member hub list (above).
3. Build four `Audience` objects: site visitors and YouTube viewers, one pair per campaign (Campaign B's pair also
   excludes subscribers). If the audience object cannot carry user-list exclusions through the API, set the exclusions in
   the Ads UI and read them back.
4. **Campaign A.** Copy `24316364155`: campaign-specific conversion goal with only SIGNUP / WEBSITE biddable, frequency
   cap 4 per user per day, same headlines, descriptions, logo and video assets. Two ad groups, each holding all six ads
   (every enabled format). Final URL `https://absbyai.com/start` with
   `utm_source=google&utm_medium=video_ad&utm_campaign=dgen-rmktg-<site|yt>&utm_content=<video>-vsl`.
5. **Campaign B.** Copy tier 1 `24163535721`: same channel settings (in-feed and Shorts), same ad copy and video per ad,
   same geo and language, goal YouTube channel subscriptions only. Two ad groups, each holding a copy of every ad enabled
   in tier 1 on build day. Ad names: keep the tier 1 name and swap `tier1` for `rmktg-site` or `rmktg-yt`.
6. `validateOnly` dry run for each, then apply, built **PAUSED**. Read everything back (budget, bidding, goals, geo,
   audiences, exclusions, ad count). Run `node scripts/ads/api/client.js policy <campaignId>` on both.
7. When every ad is approved (or approved-limited with a known cause), **enable both campaigns**. Dan asked for them built
   and running; no further approval is needed. If review is still running when the session ends, leave them paused and
   write the exact enable command in the report.

## Do not

- Do not touch the budgets, bids or ads of any existing campaign.
- Do not post any ad video organically or change its YouTube visibility (memory `ads-never-organic`).
- Do not extend `scripts/youtube/` engagement automation (`instant.js`, the Sunday pause routine in `Docs/YTADS.md`) to
  Campaign B. Report in chat whether adding it would be a small change, so Dan can decide. Until then Campaign B's ad
  set is a snapshot and will not pick up new videos.

## Open risks to report on

- The website group may be too small to deliver at all. Report its served status after 3 days.
- $3 may be too low for Campaign B to spend. Report spend and cost per subscriber after 3 days; do not raise the target.
- New formats of Ads 13, 4 and 6 (handoffs `handoff-20261001-ad13-other-formats.md`, `…-ad4-…`, `…-ad6-…`) will be added to
  the cold campaign by `/ad-setup`. Note in `Docs/DGEN_CONVERSION_CAMPAIGN.md` that they also belong in Campaign A's two groups.

## Done when

Both campaign ids, ad group ids, ad ids, audience ids, the new member list id, policy status and enabled or paused state
are reported in chat in plain language with a numbered action list; a dated section is added to
`Docs/DGEN_CONVERSION_CAMPAIGN.md` (Campaign A) and `Docs/YTADS.md` (Campaign B); a PostHog annotation is added at
enable time; the work is committed and pushed with `scripts/git/safe-push.sh`; this handoff's rows are deleted from
`Handoffs/README.md` and `AI_COORDINATION.md`. No em dashes in anything written.

## Starter prompt

> Read `Handoffs/handoff-20261001-remarketing-campaigns-conversion-and-subscriber.md` and execute it. Build the two Google
> Ads remarketing campaigns exactly to Dan's spec in that file: conversion remarketing to /start optimized for Trial Signup,
> and subscriber remarketing optimized for YouTube subscriptions, each with a Website Visitors group and a YouTube Viewers
> group at $10/day. Fix the list lifespans and build the member hub exclusion list first. Dry run, build paused, check
> policy, then enable when approved. Report ids and state with a numbered action list.

Model: **GPT-6 Sol, High**. Claude fallback: Opus 5.5, High.
