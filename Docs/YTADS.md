# YouTube engagement champion — every new video gets a $5 test ad in each Demand Gen campaign, one champion per campaign

**Built 2026-09-03** from `Handoffs/handoff-20260902-google-ads-engagement-champion-automation.md`.
The design decisions in that handoff are Dan's and are final; this doc is how the built thing works
and how to operate it. The Meta twin is `Docs/AUTO_BOOST.md`.

## What it does, in one paragraph

Dan wants YouTube subscribers. Every hour a small Google Ads Script inside account 342-717-0837 reads
every ad in the three Demand Gen campaigns (tier 2, tier 1, remarketing) and posts that snapshot to
absbyai.com. The server reads the channel's public RSS feed; any video published on or after the
go-live date (**2026-09-03**, long-forms and Shorts alike, skip list honoured) that has no ad in a
campaign gets **one Demand Gen video ad there, enabled immediately**, with headlines written by Claude
in Dan's existing style and passed through a hard compliance lint. The ad runs inside the campaign's
normal budget until Google reports it has **spent $5**, then it is paused and judged on **cost per
conversion**: fewer conversions than the campaign minimum (tier 2: 5, tier 1: 2, remarketing: 1) is
"no read"; cheaper than the champion's trailing 30 days is a **win** (the test becomes champion, the
old one is paused); otherwise a loss. **Day one**, the cheapest hand-made ad per campaign became
champion and the other enabled hand-made ads were paused — the id list was written to Postgres first,
so it can be reversed with one command per ad. Budgets never change ($15 / $15 / $5 a day). The system
never edits an existing ad: Dan's headline edits in the UI are always preserved.

## Where it runs

| piece | where |
|---|---|
| the hands | a Google Ads Script in account 342-717-0837 (Tools → Scripts → "Abs by AI — YouTube engagement champion"), hourly. Canonical source: `scripts/ads/ytads/ads-script.js` (paste a copy; only the `KEY` line differs) |
| the brain | `scripts/ads/ytads/engine.js` — pure rules, driven by `engine.test.js` (88 cases). `lint.js` is the compliance gate, `headlines.js` the writer, `feed.js` the channel feed, `brief.js` the brief block |
| the routes | `scripts/ads/ytads/routes.js`, mounted from `server.js`: `POST /api/ytads/sync`, `POST /api/ytads/results` (header `X-YTADS-Key` = `YTADS_KEY`), `GET /api/ytads/state` (dashboard-gated) |
| the switch | `YTADS_ENABLED=1` on Railway service `abs-by-ai`. Anything else = dry run: the server plans, records, and returns every command with `dryRun:true`; the script logs them and writes nothing |
| the ledger | **Google.** Ad names carry the video id (`AUTO test yt:<id> · tier2 · 2026-09-03`), labels carry the state (`AUTO`, `AUTO:TEST`, `AUTO:CHAMPION`, `AUTO:RETIRED`, `AUTO:RETIRED-DAY1`). "Has this video been tested here?" is answered by the snapshot, so a re-run can never double-create |
| the memory | Postgres `ytads_runs` (one row per hourly sync: snapshot, commands, report, results) and `ytads_events` (headlines, created, verdict, promote, skip, error, policy, dayone, dayone:executed). Both created by the routes, idempotently |
| the brief | `scripts/ads/ads-digest.js` reads the latest run into `brief-ads.json` → `ytads`; the morning brief renders a **"YouTube engagement ads"** block (spec: morning-brief task `SKILL.md`, section 7c) |
| the style | `scripts/ads/ytads/headline-style.md` — extracted from Dan's own ads; Dan's feedback is appended as rules and applies to FUTURE ads only |
| the skip list | `scripts/ads/ytads/skiplist.json` — by video id or title pattern (ab-wheel short 1 is matched by title until it has an id) |

## The hourly cycle

1. Script: GAQL over the Demand Gen campaigns (campaigns, ad groups, labels, YouTube video assets, every
   ad with its copy, lifetime cost/conversions, trailing-30-day cost/conversions, policy status).
2. Server: read the RSS feed (public videos only, so a scheduled Short appears the hour it goes live).
3. Server: for each new video with no headlines yet, Claude writes 5 headlines / 3 long headlines / 3
   descriptions → lint → up to 3 regenerations → failing lines are dropped; under 3/1/1 survivors the
   video gets a permanent `skip` event with the failing text and no ad. Headlines are written once per
   video and shared by the three campaigns. A 20-second budget keeps the script's request fast; overflow
   is written after the response and the ad is created the next hour.
4. Server: the engine produces commands — `createAd` (copying business name, final URL, logo and CTA
   assets from the campaign's champion or most-spent hand-made ad), `pauseAd`, `label` — and a report.
   The run is recorded; any day-one pause list is written to `ytads_events` before it is returned.
5. Script: executes in order (creates the YouTube video asset if the account lacks one, creates the ad,
   applies labels; pauses; relabels) and posts every outcome with Google's error text verbatim.
6. Server: outcomes → events (`created` with the headlines that went live — Dan's review surface).

Policy: a DISAPPROVED `AUTO` ad is paused and retired and that video is never retried in that
campaign (its ad stays in the ledger). "Eligible (Limited)" is reported, not acted on. Hand-made ads'
policy state is never touched.

## Running / checking by hand

```bash
node scripts/ads/ytads/engine.test.js        # rules
curl -s -H "X-Dash-Key: $DASH_SECRET" https://absbyai.com/api/ytads/state | jq '.ok,.enabled,.dryRun,.ageHours,.counts,.warnings'
```

Reverse a day-one pause: the `dayone` event's `reversal` list is `enableAd` commands; run them as a
one-off in the Ads Script (`execute(cid, cmd, labels, snapshot)`) or in the UI.

## Interpretations made in the build (stated to Dan 2026-09-03)

1. One champion **per campaign**, compared only within its campaign.
2. `MIN_CONV = { tier2: 5, tier1: 2, rmktg: 1 }` before a test can win.
3. Champion judged on trailing 30 days, test on its lifetime; a champion with 0 conversions in 30 days
   is beaten by any test that clears `MIN_CONV`.
4. Zero conversions at $5 = paused.
5. No time deadline on a test; the brief shows days waiting.
6. No qualifying hand-made ad on day one → nothing paused; the first qualifying test crowns itself and
   the hand-made ads are paused then.
7. The system never edits an existing ad.
