# SixPackAbs video sync repair, 2026-10-04

## Cause

The YouTube feed and WordPress import were both hourly. The feed returned at 9:47 AM CDT had been fetched at 8:56:33 AM and contained 33 public videos. The Sunday 9:01 AM check ran before today's video became public at 9:03:04 AM. That check could not discover the release, and the two hourly schedules could exceed the requested 15-minute limit.

Latest public upload: `v2R4QpnURqA`, Your Belly Fat Is an Emergency: 7 Reasons to Take It Seriously. Sunday 9 AM Central is the usual long-form slot, but the queue also contains Wednesday releases on Oct 7 and Oct 14. Detection now runs throughout the week.

## Changes

- YouTube's feed cache and background refresh now run every five minutes. Instagram retains its hourly cache.
- Video-feed responses use `Cache-Control: no-store` to prevent another five-minute HTTP cache from stacking on top.
- WordPress registers `spa_five_minutes` and migrates the existing `spa_sync` event from hourly. Initialization is idempotent and schedules the first attempt within one minute.
- Each Railway background refresh finishes fetching the feed before requesting WordPress's public cron endpoint. This wakes due imports without visitor traffic or a running desktop app. HTTP failures are logged.
- The Sunday 9:01 AM Central attempt remains as an extra check and follows daylight saving time.
- The admin status displays the next scheduled check. Existing editorial notes, public-only filtering, and private/unlisted handling retain their tested behavior.

Normal discovery plus import budget is at most about ten minutes, leaving time for processing and homepage cache invalidation before the 15-minute target. Outages, unavailable upstream data, and continuous backend restarts can exceed that target; this is not a provider uptime guarantee.

## Verification

- 15 Node feed checks passed, including newly public release discovery at five minutes, public-only filtering, Instagram hourly caching, and refresh-before-cron ordering.
- 34 real WordPress Playground checks passed, including hourly schedule migration, first run within a minute, no duplicate jobs, preservation of edited notes, and video lifecycle behavior.
- `node --check server.js` passed on the deployed version.
- Live WordPress theme editor saved successfully. Readback matches the tested PHP after whitespace normalization.
- Backend fix commit: `0ce082630bdbcf8c982dd75258ea4bc5278c42ad`. Railway deployment `113e780b-8f84-460a-a6b8-69b2a6c71a71` completed successfully. The later successful deployment `7be7271f-6cf1-42aa-9383-26073c741a36` contains the same fix.
- Railway logged automatic WordPress triggers at 9:58:07 and 9:59:12 AM CDT.
- Live feed returned today's upload and `no-store`, fetched at 9:57:59 AM CDT.
- WordPress's automatic import reported 34 feed videos, 1 new, 1 updated, with the next check at 10:04:31 AM CDT.
- Anonymous, normal-URL homepage and /videos/ requests returned HTTP 200 and today's video ID and title. No cache-busting query string or logged-in cookie was needed. Browser inspection confirms today's thumbnail, player button, and latest-video heading.
- Screenshot: local Codex visualization folder for chat 01a10762-59b6-7bc3-bf7b-76aff121aabe, sixpackabs-video-sync-fixed.jpg.

## Deployment detail

The shared main checkout's safe-push stopped because six unrelated files held other sessions' edits: VIDEO-RULES.md, framing-motion.md, kit9x16/README.md, reference/render.py, AI_COORDINATION.md and WEB_CART.md. The fix was cherry-picked onto current origin/main in a clean checkout and pushed successfully. None of those edits were overwritten. The shared checkout retains its original local commit 206364e; production contains the equivalent 0ce0826.
