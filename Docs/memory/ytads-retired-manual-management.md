---
name: ytads-retired-manual-management
description: "2026-09-27 engagement ads: new videos auto-get ENABLED ads within a minute; automation never pauses except the Sunday routine (09-29); Dan re-enables Tuesday"
metadata:
  node_type: memory
  type: project
  originSessionId: 7356e2c3-35b5-41bc-90a8-f9309b346fc9
  modified: 2026-09-29T18:16:08.649Z
---

Dan's rule 2026-09-27 for the three YouTube engagement campaigns (tier2 24122099676, tier1 24163535721, rmktg 24169507109): every new video gets an ad in all three **as soon as it goes up, ENABLED**, and automation **never pauses, enables or removes** anything. Dan does all pausing by hand.

Built as `scripts/ads/ytads/instant.js` (server polls the RSS feed every 60 s, creates via the Google Ads API, in-feed only for long-form). Switch `YTADS_INSTANT=1`. The old hourly Ads Script is Disabled in Google Ads and `YTADS_ENABLED=0`; do not re-enable them.

**Update 2026-09-29 (Dan):** one exception. The Sunday routine (`scripts/ads/ytads/sunday.js`, `YTADS_SUNDAY=1`, detail in `Docs/YTADS.md` "SUNDAY PAUSE") pauses every long-form ad in tier1 + tier2 except the newest long-form at 10 AM CT each Sunday, leaves Shorts alone, labels the pauses "Sunday pause", and 6 hours later adds a tamer-copy ad if the newest is not fully approved (in review, disapproved or approved-limited). Dan re-enables by hand on Tuesday. instant.js itself still never pauses.

**Why:** the old script ran hourly (missed a 9:01 upload by an hour) and its stale live copy ignored the paused/in-feed rules; Dan wants speed and full manual control of status.

**How to apply:** never add pause/enable/remove logic to this path. If an ad is missing, check `created`/`error` events with `via: "instant"` and the Railway log line "YTADS instant". Detail: `Docs/YTADS.md` "CURRENT BEHAVIOR".
