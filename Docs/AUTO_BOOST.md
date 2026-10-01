# IG auto-boost: every new @danrosefit post gets a $10 test, one champion runs at $6.50/day

**Changed 2026-09-29 (Dan's decisions):** tests are **$10** (was $5) and the champion is the post with the **lowest
estimated cost per follower** (was cost per profile visit). Spec: `Handoffs/handoff-20260929-ig-autoboost-cost-per-follower.md`
(executed). The paragraph below describes the original build; where it says $5, $4.50, 10 visits or cost per visit, read the
"How follows are estimated" section instead.

**Built 2026-09-02** from `Handoffs/handoff-20260902-ig-auto-boost.md`. **Switched LIVE 2026-09-08 ~21:00 UTC**
(Dan's word; `AUTO_BOOST_ENABLED=1` on the `auto-boost` service). The first live pass renamed the campaign and
champion and created six $5 tests on the Sep 2–7 posts; the champion had $40.02 / 418 visits at that point. The design decisions in
that handoff are Dan's and are final; this doc is how the built thing works and how to operate it.

## What it does, in one paragraph

Dan wants followers on @danrosefit. Meta cannot optimise for follows, so the system buys the step
before a follow — **Instagram profile visits** — and measures follows after the fact. Every hour,
the job looks at @danrosefit's recent posts; any post published on or after **2026-09-02** that has
no test yet gets a **$5 lifetime ad** on the real post (reels, images and carousels), targeted
exactly like the champion. When a test has spent $4.50 or reached 5 days, it is judged on **cost
per profile visit**: at least 10 visits and cheaper than the champion's trailing 7 days → it becomes
the new champion, the old one is paused and renamed `RETIRED::`. The single **champion** ad set runs
at **$6.50/day** and is judged weekly on **cost per follow**: over $5/follow with $35+ spent → paused
(the next winning test refills the slot); under $3/follow → reported as a scale candidate, never
scaled automatically. Script-enforced caps: **$300/month on tests, $500/month total**, counting
money already committed to running tests so the cap holds even when Meta's numbers lag.

## Where it runs

| piece | where |
|---|---|
| the job | `scripts/ads/auto-boost.js`, Railway service **`auto-boost`** (same repo), cron `15 * * * *`, start command `node scripts/ads/auto-boost.js` |
| the switch | `AUTO_BOOST_ENABLED=1` on that service. Anything else = dry run: it plans, writes nothing to Meta, and still records what it would have done |
| the ledger | **Meta.** The post id is in the ad-set / ad name — `REEL \| <title> \| TEST::<media_id>` (also `CHAMPION::`, `RETIRED::`) — so "was this post tested?" is answered by Meta and a re-run can never double-create |
| the memory | Postgres `auto_boost_events` (skip / created / verdict / promote / pair_resolved / champion_paused / scale_candidate) and `auto_boost_runs` (one report per run; the brief reads the latest) — both created by the job itself, idempotently |
| the brief | `scripts/ads/ads-digest.js` reads the latest run into `brief-ads.json` as `autoBoost`; the morning brief renders an **"Auto-boost"** block (spec in the morning-brief task's `SKILL.md`) |
| the tests | `node scripts/ads/auto-boost.test.js`: 69 cases pinning every rule to Dan's numbers |
| follower history | Postgres `auto_boost_follows_daily` (day, new followers). Instagram keeps only ~30 days, so every run upserts what it can see |

Campaign `120250753198730682` ("[AUTO] IG PROFILE VISITS - danrosefit"), champion ad set
`120250753601020682` ("CHAMPION"), ad account `act_2143998876461525`, Page `1380236418500031`,
@danrosefit IG user `17841401601139982`. Env on the cron service: `META_ADS_TOKEN`,
`META_APP_SECRET`, `DATABASE_URL` (internal), `AUTO_BOOST_ENABLED`.

## Names — type first, then the title, then the tag (Dan's rule 2026-09-08)

Every ad set and ad the job creates is named `<TYPE> | <title> | <TAG>::<media_id>`, for example
`REEL | Hire a maid instead of a personal trainer | TEST::18122536861661975` or
`IMAGE | Pick a sport, not a cardio machine | TEST::17983238982111705`. `REEL` is a video post, `IMAGE` a single
image, `CAROUSEL` a carousel; the title is the first sentence of the post's caption, cut to 60 characters. The tag
(`TEST`, `CHAMPION`, `RETIRED`) and the media id stay at the end because they are the ledger. **The job heals
names every run**: any ad set or ad in the campaign whose name does not match the convention is renamed (never a
status or budget change), so a hand-renamed object drifts back within the hour. Old bare `TEST::<id>` names are
still recognised.

## Running it by hand

```bash
cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI" && node scripts/ads/auto-boost.js --dry-run
```

Reads `META_ADS_TOKEN`, `META_APP_SECRET` and `DATABASE_PUBLIC_URL` from `~/.absbyai-secrets.env`
(the internal `DATABASE_URL` does not resolve from the Mac). Prints a human summary and writes
`brief-autoboost.json` at the repo root (git-ignored). Add `--verify` to print every insights action
type Meta returns next to the pinned metric names (see below); `--print` dumps the full report JSON.
A dry run also records a `dry_run=true` row in `auto_boost_runs` so the brief can show it.

To make a local run LIVE (it will spend): `AUTO_BOOST_ENABLED=1 node scripts/ads/auto-boost.js`.

## How follows are estimated (method B, since 2026-09-29)

`META_ADS_TOKEN` now carries `instagram_manage_insights` (added to app `1598463548528030` under Use cases →
Instagram API → Permissions and features; token re-minted by API 2026-09-29 without `public_profile`, which the mint
now rejects; never expires). What that unlocked, tested on the live account:

- `GET /17841401601139982/insights?metric=follower_count&period=day` works: new followers per day, last 30 days.
  Each value's `end_time` is the END of its day (07:00 UTC), so it counts for the calendar day before.
- `GET /{media}/insights?metric=follows` works on IMAGE posts but counts **organic follows only** (the champion
  image with 448 paid visits reads `follows=0`, `profile_visits=4`), and on REELS Meta refuses `follows`,
  `profile_visits` and `profile_activity` outright. So method A (per-post follows) is **rejected**.

**Method B, what the job uses:** each day's new followers are split across that day's running ads in proportion
to their profile visits. A post's estimated follows = the sum of its daily shares; estimated cost per follower =
its spend on settled days / its estimated follows. A day counts once it is **2 days old** (the newest value is
often a provisional 0). Organic follows are spread the same way, so the number **ranks posts, it is not a true
cost**. Within one day it reduces to cost per visit; it separates posts only across days.

Rules: a test is judged at $9 spent or 5 days, and only once its last day has settled (`wait` until then). It
needs **at least 2 estimated follows** (Claude's default, not Dan's: $10 at ~$3 a follower buys ~3) and must beat the
champion's estimated cost per follower over its **last 7 settled days**; ties keep the champion. Champion health:
over $5/follower with $35+ spent → paused; under $3 → reported as a scale candidate. `--backfill` prints the
estimate for every post of the last 30 days, by post and by type.

**Caveat (2026-09-29 analysis):** day to day, new followers barely move with ad visits (correlation about 0.1 to
0.2 in either day alignment; roughly 5 a day whether visits were 50 or 180; 3 to 4 a day on Aug 31 and Sep 1,
before ads). A large share of the "estimated follows" is organic, so treat small differences as noise.

**Caps vs $10 tests:** at ~35 posts a month, tests alone would be ~$350, so the $300 test cap stops new tests in
the last days of a month. Caps unchanged; raising them is Dan's call.

## Follower readings

| reading (UTC) | followers | lifetime spend | visits | since previous |
|---|---|---|---|---|
| 2026-09-08 ~21:00 | 566 | $40.02 | 418 | baseline |
| 2026-09-11 14:49 | 586 | $80.45 | 747 | +20 follows / $40.43 = **$2.02/follow**, 6.1 % of visits followed |
| 2026-09-29 19:20 | 654 | $298.37 | 2,999 | +68 / $217.92 = **$3.20/follow** all-in, 3.0 % of visits |

Net of unfollows and of every source. Gross new followers from `follower_count`: 138 in the 30 days to Sep 28.

**Backfill 2026-09-29** (settled through Sep 27): IMAGE 14 posts, $162.48, 62.8 est. follows = **$2.29/follower**
(3.1 per 100 visits); REEL 18 posts, $134.64, 62.2 est. follows = **$2.13/follower** (6.5 per 100 visits). The reel
total is carried by the retired first-run reel "A three-minute total body workout" ($1.31/follower on $61, mostly
Sep 2 to 11); individual reel TESTS ran $3 to $20 per follower, image tests $1.40 to $4. Champion then: "Three-minute
rounds at home" IMAGE, $1.80/follower lifetime, $2.04 over its last 7 settled days.

The Sep 26 reel test "Never start your day with carbs" had its creative refused ("Permissions error", subcode
1487194) while the ad account was inactive for billing; relaunched by hand at $10 on 2026-09-29 (ad
`120251239324840682`, event `relaunched`). If a skip reason is that error, retry once the account is active.

## The two metric names (history: follows are now estimated as above, not read from ads insights)

Probed against the live account on 2026-09-02, zero-spend, everything deleted afterwards:

- **Profile visits:** `instagram_profile_visits` is an accepted top-level insights field (Meta
  rejects made-up names with error 100; this one returns rows). Pinned as `VISITS_FIELD`, with a
  fallback scan of `actions` for `instagram_profile_visit` / `ig_profile_visit` / `profile_visit`.
- **Follows:** Meta added an "Instagram follows" ads metric in August 2025 but the API string is not
  documented anywhere reachable, and every guessed top-level field (`instagram_follows`, `follows`,
  `follows_or_likes`, `page_likes`) is rejected. The job scans `actions` for a candidate list
  (`instagram_follow`, `ig_follow`, `follow`, `onsite_conversion.ig_follow`, `onsite_conversion.follow`,
  `onsite_conversion.instagram_follow`, `page_like`, `like`) and treats the metric as **readable only
  once a candidate has appeared with a non-zero count** on the campaign. Until then the champion is
  judged on cost/visit only, **no kill rule fires**, and the brief says so. Dan accepted this risk.
- **Both are self-verifying, not assumed:** a test is judged `unmeasured` (never `lose`) while the
  visit metric has never been observed on the account, and the champion is `unjudged` while follows
  are unobserved. The campaign had ~1 hour of delivery and no insights rows when this was built, so
  the API-string → Ads-Manager-column match is still open. **The check, once spend exists:**

  ```bash
  cd "/Users/danielrose/Documents/Claude/Projects/Abs By AI" && node scripts/ads/auto-boost.js --dry-run --verify
  ```

  Then Ads Manager → Columns → Customize → search "Instagram profile visits" and "Follows" for the
  same date range. The API string whose count equals the column is the metric; if it is not in the
  candidate list, add it at the front of `FOLLOW_ACTION_TYPES` (or fix `VISITS_FIELD`) and re-run
  the tests. Record the answer here.

Other things Meta accepted on 2026-09-02 (VERIFY items 3 and 4 of the handoff): a **$5 lifetime
budget over 5 days** passes validation (no minimum-budget error), and the creative shape works on a
**`CAROUSEL_ALBUM`** post and on an **`IMAGE`** post, not only reels. Nothing is on the permanent
skip list; the job adds a post to it only when Meta refuses that specific post.

## How to read the brief block

- **Champion** — the post, 7-day spend, visits and cost/visit, follows and cost/follow (or "follows
  not readable yet"), and the health verdict: `ok`, `scale_candidate`, `pause` (it has been paused —
  the slot is empty until a test wins), or `unjudged`.
- **First-run pair** — the two ads Dan launched on 2026-09-02 both run until each has $10 of spend;
  then the cheaper cost/visit stays as `CHAMPION::` and the other is retired. Until then "exactly
  one active champion ad" is suspended on purpose.
- **Tests** — each `TEST::` ad set with its post, spend, visits, cost/visit and phase (`running`,
  `ready`, `done`) plus the verdict once judged.
- **Caps** — month-to-date spend on tests and in total, plus what is committed to running tests,
  against $300 / $500. When a cap is reached, no tests are created; evaluation still runs.
- **Skips** — posts Meta refused, with Meta's message. Skips are permanent for that post.
- **Warnings** — the job's own doubts: metric never observed after real spend, champion slot empty,
  campaign not delivering, champion daily budget not 650 cents (it reports, it never changes budgets).

## Switching it off

Set `AUTO_BOOST_ENABLED=0` on the Railway `auto-boost` service (or delete the variable). Running
tests keep spending to their $10 and then stop on their own: a lifetime budget needs no supervision.
The champion keeps running at $6.50/day until someone pauses ad set `120250753601020682`. Nothing the
job does is a deletion: ads are paused and renamed, never removed, so the history stays in Meta.

## Traps already paid for (do not rediscover)

- Ads Manager cannot set the Instagram identity for this ad account; the only creative shape that
  runs as @danrosefit is the top-level one (`object_id` + `instagram_user_id` +
  `source_instagram_media_id`, no `object_story_spec`, no `call_to_action`). The job uses nothing else.
- Never click the global "Review and publish" in Ads Manager — it republishes abandoned 9/01 drafts.
- `promoted_object` is immutable after ad-set creation; IG `explore` placement is deprecated
  (`explore_home`); targeting is **copied from the champion ad set at run time**, never hand-typed.
- New ads sit in review for hours; the 5-day window is measured from creation so a slow review
  cannot turn a good post into a $0 "loser" — a test with $0 spend is only judged at `end_time`.
- The secrets cache `~/.absbyai-secrets.env` contains Railway's own `RAILWAY_*` markers, so a script
  cannot use `RAILWAY_ENVIRONMENT` to tell the Mac from the cron; the job prefers
  `DATABASE_PUBLIC_URL` when set and the cron service is simply not given that variable.
