# Handoff: IG auto-boost picks winners on cost per FOLLOWER, $10 per post (2026-09-29)

**Recommended model:** Claude Opus 5.5 / High (step 1 is a browser task in Meta's developer dashboard; the rest is a
code change to a live spending job).

## Goal

Dan's goal for @danrosefit ads is **followers**, not profile visits. Today the auto-boost job
(`scripts/ads/auto-boost.js`, Railway service `auto-boost`, hourly) picks the champion by cheapest **profile visit**,
because Meta will not tell our token who followed. Change it so that:

1. **Every new @danrosefit post gets a $10 lifetime test** (was $5). Dan's decision, 2026-09-29.
2. **The post with the lowest estimated cost per follower becomes the champion.** Dan's decision, 2026-09-29.

Everything else in the locked design stays (Docs/AUTO_BOOST.md): $6.50/day champion, one champion at a time, tests
targeted by copying the champion ad set, Meta as the ledger, pause and rename, never delete.

## Why (the evidence from 2026-09-29)

- Lifetime since Sep 2: $298.16 spend, 2,999 profile visits, followers 566 (Sep 8) to **653** (Sep 29).
- Cost per follower, all-in: **$2.02** Sep 8 to 11 (two REEL champions, about 6 of every 100 visitors followed), **$3.25**
  Sep 11 to 29 (mostly IMAGE champions, about 3 of every 100 visitors followed). Cost per visit stayed about 10 cents throughout.
- Image tests win on visits (9 cents vs 24 cents for reels), which is why images keep taking the champion slot. The
  follower readings hint reels bring visitors who actually follow. Judging on visits is optimising the wrong number.

## Step 1: get the follower-count permission (blocked today, do this first)

Current `META_ADS_TOKEN`: system user `abs-automation` (id `122096883771469881`), app `abs by ai automation`
(`1598463548528030`), never expires. Scopes: pages_show_list, ads_management, ads_read, business_management,
instagram_basic, pages_read_engagement, pages_manage_posts, public_profile. **No `instagram_manage_insights`**, so
`/17841401601139982/insights?metric=follower_count` and `/{media}/insights` return `(#10)`.

Tried 2026-09-29: `POST /122096883771469881/access_tokens` (business_app=1598463548528030, appsecret_proof, scopes
+ `instagram_manage_insights`) returned **`(#100) Invalid Scopes: instagram_manage_insights`**. The app itself does
not have that permission yet. So:

1. developers.facebook.com → app `1598463548528030` → Use cases / Permissions → add **`instagram_manage_insights`**
   (Standard access is enough; the app, the business and the IG account are all Dan's own, so no App Review is
   expected. If Meta demands App Review, stop and tell Dan with the exact screen text).
2. business.facebook.com → Business settings → System users → `abs-automation` → confirm the **@danrosefit Instagram
   account** is an assigned asset (add it if not).
3. Re-mint the token by API exactly as before (the Business Settings token UI silently fails for these scopes;
   see Docs/ADS_DIGEST.md "Meta"): same scope list as today **plus `instagram_manage_insights`**, with `appsecret_proof`.
   Minting a new token does not revoke the old one, so nothing breaks while you swap.
4. Verify: `GET /17841401601139982/insights?metric=follower_count&period=day` returns daily rows, and
   `GET /{media-id}/insights?metric=follows,profile_visits` on one IMAGE and one REEL post (try both; record which
   metrics each media type accepts).
5. Store it: replace `META_ADS_TOKEN` in `~/.absbyai-secrets.env` (never in chat or git), then on Railway services
   `auto-boost` **and** `abs-by-ai` (the ads digest reads it too). Re-run `node scripts/ads/ads-digest.js` and
   `node scripts/ads/auto-boost.js --dry-run` to prove nothing regressed.

Dan explicitly asked for this permission (2026-09-29), so it is authorized. If Meta asks for a password or a
re-login, that is the one moment Dan has to type; everything else is Claude's.

## Step 2: how to estimate cost per follower per post

Pick the first method that step 1 proves works, and record which one in Docs/AUTO_BOOST.md.

**A. Per-post follows from Instagram (preferred if it works).** `/{media}/insights?metric=follows`. Before trusting
it, check it counts follows that came through the ad, not only organic: compare the sum of `follows` across all
running posts on a few days against that day's `follower_count` gain. If the sum is far below the gain, it is
organic-only. Then use method B.

**B. Daily attribution by visit share (fallback, works for every media type).**
- Store each day's new followers from `follower_count` (period=day) in Postgres (new table, e.g.
  `auto_boost_follows_daily`; the API only returns about the last 30 days, so persist every run).
- Pull ad-level insights with `time_increment=1` (spend, `instagram_profile_visits` per ad per day).
- Each day's new followers are split across that day's running ads in proportion to their profile visits.
  A post's estimated follows = the sum of its shares; estimated cost per follower = spend / estimated follows.
- This counts organic follows too, and spreads them evenly, so it is **for ranking posts against each other**,
  not a true cost. Say so in the brief.

## Step 3: change the job (Dan's numbers)

In `scripts/ads/auto-boost.js`:

- `TEST_BUDGET_CENTS` 500 → **1000**; `TEST_EVAL_SPEND` 4.50 → **9.00**; fix the "$5 lifetime" text in log lines,
  the header comment and the brief. Window stays 5 days.
- `verdict()`: rank on **estimated cost per follower**. Promote when a test's estimated cost per follower is lower
  than the champion's trailing-7-day estimated cost per follower. Replace `PROMOTE_MIN_VISITS` with a minimum
  evidence rule. Sensible default: **at least 2 estimated follows** (at about $3 a follower, $10 buys about 3, so a
  test with fewer is noise). Note this default for Dan; he did not set it.
- `championHealth()`: now that follows are readable, the existing kill rule (over $5 a follower with $35 or more
  spent → pause) and scale report (under $3) start working. Keep both numbers.
- Keep visits as a secondary column in the brief for context only.
- Update `auto-boost.test.js` (48 cases today) for the new budget, eval spend and cost-per-follower verdicts;
  all must pass.
- **Caps are unchanged: $300/month tests, $500/month total.** At $10 a post and about 35 posts a month, tests
  alone would be about $350, so the test cap will stop new tests in the last days of each month. Do not raise the caps;
  report it to Dan as his decision.

## Step 4: backfill, so Dan gets his images-vs-reels answer

With the last 30 days of `follower_count` and daily ad insights, run method B (or A) over every past TEST and
champion ad and report estimated cost per follower **by post and by type (IMAGE vs REEL)**. This answers Dan's
question "do image posts get followers cheaper than reels?" with the best data available. Check whether the
current champion ("Three-minute rounds at home, no equipment", IMAGE, `CHAMPION::18020502953723603`) is still the
cheapest per follower; if a retired post is clearly cheaper, report it and ask Dan before re-activating anything.

## Also fix

- Ad set `REEL | Never start your day with carbs | TEST::17901849270581189` is stuck `WITH_ISSUES` with
  "run status of the ad account is not active" (a billing blip around Sep 26 to 27; the account is active again,
  status 1). Relaunch or re-create that test so the post gets its budget, without double-creating.

## Delivery

Commit, push to `main`, confirm the Railway `auto-boost` deploy, watch one live hourly run (logs + the
`auto_boost_runs` row), update Docs/AUTO_BOOST.md (method, new numbers, follower baseline table) and the
morning-brief Auto-boost block if its text says "$5" or "visits". Then delete this handoff's rows from
`Handoffs/README.md` and the HANDOFFS section of `AI_COORDINATION.md`. Report to Dan in plain language: the
images-vs-reels answer, what the champion is now, and the cap question.

## Key ids

Ad account `act_2143998876461525`; campaign `120250753198730682` "[AUTO] IG PROFILE VISITS - danrosefit"
(OUTCOME_TRAFFIC, optimisation VISIT_INSTAGRAM_PROFILE); champion ad set `120250753601020682` ($6.50/day);
Page `1380236418500031`; @danrosefit IG user `17841401601139982`; Meta app `1598463548528030`; system user
`122096883771469881`. Old paused campaigns `[DAN] [ENGAGEMENT]` `120250271323900682` and `[DAN] [ENGAGEMENT] IG GEO`
`120250551172530682` stay off.
