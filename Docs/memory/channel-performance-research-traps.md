---
name: channel-performance-research-traps
description: "11-12: how to pull YouTube organic + Google Ads subscriber data for content research, and the 4 traps (Oct 7 ad-cost drop, no ad-by-country, uniform Shorts first audience, US skew by type)"
metadata:
  node_type: memory
  type: reference
  originSessionId: be1381c2-fa47-4d80-93c9-112e445fc9f8
  modified: 2026-11-12T18:15:28.719Z
---

Found 2026-11-12 while writing the next-shoot research brief (`Research/Shoot Research Claude 2026-11-12/`, README there; review doc https://claude.ai/artifact/JdZV2BrhWaHxkWKgDKJqAm). Codex wrote a parallel brief the day before in `Research/Shoot Research 2026-11-11/`; raw numbers matched.

**How to pull it fast**
- Organic per video: YouTube Studio Advanced mode in Dan's Chrome accepts the filter in the URL: `...&ur_dimensions=AD_STATUS&ur_values='AD_STATUS_ORGANIC'` (add `ur_dimensions=COUNTRY&ur_values='US'` for US only), `dimension=VIDEO` / `TRAFFIC_SOURCE_TYPE` / `COUNTRY`, metrics `EXTERNAL_VIEWS, ENGAGED_VIEWS, EXTERNAL_WATCH_TIME, AVERAGE_WATCH_PERCENTAGE, SHORTS_FEED_IMPRESSIONS_VTR` (stayed to watch). Export CSV from the download icon. The API token has no Analytics scope. Subscribers and thumbnail CTR are hidden under the Organic filter.
- Ads: `scripts/ads/api/client.js` `search()`; subscribers = `metrics.all_conversions` with `segments.conversion_action_name = 'YouTube channel subscriptions'` (cost needs a separate query). Scripts to reuse: `pull_ads.js`, `analyze_ads.py`, `pull_peers2.py` in that folder.

**Traps**
1. **Ad cost per subscriber fell ~85% on 2026-10-07 for every video and country at once** ($1.3 to $3.4 a sub before, $0.22 to $0.52 after; same ads). Cause not found. Never rank videos on cost per sub across that date: use Oct 7 onward, or compare each video with others running the same week.
2. Google Ads refuses ad x viewer country (`segments.geo_target_country` on `ad_group_ad`). US per-video cost exists only in the US-only campaign `24422704023` (from 2026-11-03). Tier 1 results are ~64% Ireland.
3. About half of October's Shorts landed at 1,180 to 1,500 organic views whatever the topic (a standard first audience). Rank Shorts on stayed-to-watch, engaged views and US views, not raw views.
4. US share of organic views swings by type: food/supplement claims, reactions and "why" explainers 50 to 74% US; exercise demos ~30% (Jump Rope's search traffic is "skipping", largely non-US). Dan cares most about the US.

Related: [[shorts-organic-research]], [[google-ads-api-client]], [[longform-strength-ranking]].
