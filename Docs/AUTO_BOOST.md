# IG auto-boost — every new @danrosefit post gets a $5 test, one champion runs at $6.50/day

**Built 2026-09-02** from `Handoffs/handoff-20260902-ig-auto-boost.md`. The design decisions in
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
| the ledger | **Meta.** The post id is in the ad-set name (`TEST::<media_id>`, `CHAMPION::<media_id>`, `RETIRED::<media_id>`), so "was this post tested?" is answered by Meta and a re-run can never double-create |
| the memory | Postgres `auto_boost_events` (skip / created / verdict / promote / pair_resolved / champion_paused / scale_candidate) and `auto_boost_runs` (one report per run; the brief reads the latest) — both created by the job itself, idempotently |
| the brief | `scripts/ads/ads-digest.js` reads the latest run into `brief-ads.json` as `autoBoost`; the morning brief renders an **"Auto-boost"** block (spec in the morning-brief task's `SKILL.md`) |
| the tests | `node scripts/ads/auto-boost.test.js` — 48 cases pinning every rule to Dan's numbers |

Campaign `120250753198730682` ("[AUTO] IG PROFILE VISITS - danrosefit"), champion ad set
`120250753601020682` ("CHAMPION"), ad account `act_2143998876461525`, Page `1380236418500031`,
@danrosefit IG user `17841401601139982`. Env on the cron service: `META_ADS_TOKEN`,
`META_APP_SECRET`, `DATABASE_URL` (internal), `AUTO_BOOST_ENABLED`.

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

## The two metric names — one verified, one still to match (read this before trusting a verdict)

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
tests keep spending to their $5 and then stop on their own — a lifetime budget needs no supervision.
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
