# Handoff — Google Ads engagement champion: every new YouTube video gets a $5 test ad in all three Demand Gen campaigns, one champion per campaign runs until beaten

**Written:** 2026-09-02 (Claude Code, Fable 5.1). Design agreed with Dan in chat the same evening.
**Status:** NOT EXECUTED. Design locked, nothing built.
**Supersedes:** the loop/approval sections of
`Handoffs/handoff-20260831-google-ads-api-setup-engagement-ad-automation.md`. That doc's
**"account facts"** and **"PHASE 1 — API access"** sections are still correct and are referenced
below rather than repeated. Its $20/$100 loop and its approve-copy-first gate are dead.
**Sibling system (same shape, Meta side):** `Handoffs/handoff-20260902-ig-auto-boost.md`. Read its
architecture section once — this is the YouTube twin, and the two should feel identical to Dan in
the morning brief.

---

## THE GOAL IN ONE PARAGRAPH

Dan wants **YouTube subscribers**. Every new public video on the channel (long-forms AND Shorts) gets
**one new engagement ad in each of the three existing Demand Gen campaigns** the hour it goes up,
with conservative headlines written automatically. Each new ad runs **inside its campaign's normal
budget** until it has spent **$5 in that campaign**, then the system pauses it — by reading its spend,
never by a Google automated rule or a separate campaign. Each campaign keeps **one champion ad**, the
ad with the lowest cost per conversion. A test that beats the champion on cost per conversion becomes
the new champion; the old one is paused. The champion runs permanently, or until beaten. Dan reviews
headlines **after** they go live and edits them in the UI if they are bad; the system never overwrites
his edits. Dan never touches the loop.

## DECISIONS DAN MADE 2026-09-02 (do not re-open)

| Decision | Value |
|---|---|
| Campaign structure | **Inside the three existing Demand Gen campaigns.** No per-video campaigns — "$5 campaigns that get paused out quickly won't optimize." |
| Which campaigns | **All three**: tier-2 geo (`24122099676`), tier-1 geo clone, remarketing (`[DGEN] [RMKTG] youtube viewers`). One new ad per campaign per video. |
| Test budget | **$5 lifetime spend per ad, per campaign**, measured by reading the ad's spend. **No Google automated rule, no campaign total budget.** |
| Many active ads in remarketing | **Accepted.** At $5/day that campaign will carry a long tail of tests each waiting to reach $5. That is the intended state. |
| Campaign budgets | **Unchanged: $15/day tier 2, $15/day tier 1, $5/day remarketing.** No extra monthly cap — the daily budgets are the cap. |
| Existing 29 hand-made ads | **Day one: the lowest cost-per-conversion ad in each campaign becomes champion #1, the rest are paused** (recommendation 3, accepted). |
| Approval gate | **None. Publish immediately.** Copy must be very conservative. Dan reviews after launch, edits bad headlines in the UI, and gives feedback that goes into the style rules for next time. |
| Which videos | **All public uploads, including Shorts.** Skip list honoured (ab-wheel short 1 never runs paid). |
| Scoreboard metric | **Cost per conversion** (Google's `conversions` column, ≈2x real subscribers on this account, consistently — ranking is unaffected). |
| Access path | **Start with Google Ads Scripts, apply for the API developer token on day one, migrate the executor when Basic access lands.** Dan asked which is better long term: the API. Detail in "Access path". |

## INTERPRETATIONS I MADE (state them to Dan in the first build report; change on his word)

1. **One champion PER CAMPAIGN, compared only within its campaign.** Dan said "the champion should run
   in all campaigns." Read together with his locked 8/31 rule (compare within the same campaign only —
   tier 2 conversions cost $0.09–0.35, tier 1 $2–3, so a cross-campaign comparison always crowns tier
   2), this means each campaign has its own champion and every campaign always has one running. The
   same video can be champion in tier 2 and a paused loser in tier 1.
2. **Minimum conversions before a test can win**, per campaign, as constants:
   `MIN_CONV = { tier2: 5, tier1: 2, rmktg: 1 }`. Rationale: $5 buys ~15–50 conversions in tier 2 (a
   real reading), ~2 in tier 1, and remarketing has 0 conversions on ~$9 lifetime. A test with fewer
   conversions than the minimum at $5 spend is paused as "no read", not promoted. Dan agreed to
   "rank on cost per conversion" and did not object to a minimum; these numbers are mine.
3. **The champion is judged on its trailing 30 days**, the test on its lifetime (it only lives to
   $5). Comparing a test to a champion's all-time average would let an ad that was great in July hold
   the seat forever. If the champion has zero conversions in the trailing 30 days, any test that
   clears `MIN_CONV` beats it.
4. **Zero conversions at $5 = paused** (the 8/31 edge rule, unchanged).
5. **No time deadline on a test.** Dan: "read how much it's spent before deciding when to turn it
   off." A test runs until it reaches $5, however long that takes. The brief shows how long each has
   been waiting so a stuck one is visible.
6. **Day-one no-champion case.** If a campaign has no hand-made ad with ≥$5 spend and ≥`MIN_CONV`
   conversions (remarketing will be this), pause nothing there yet; the first test that qualifies
   becomes champion and the day-one pause of the hand-made ads happens at that moment.
7. **The system never edits an ad that exists.** It creates, pauses, enables, and labels. Dan's
   headline edits in the UI are therefore always preserved. Feedback on headlines is applied to
   `scripts/ads/ytads/headline-style.md` for FUTURE ads only.

---

## ARCHITECTURE — brain on our server, hands inside Google Ads

The decision logic lives in our repo where it can be unit-tested; the thing that talks to Google is a
thin, dumb executor. That split is what makes the Scripts→API migration cheap: only the executor
changes.

```
YouTube RSS  ─┐
              ▼
   absbyai.com (Railway)  — the BRAIN
   ├─ scripts/ads/ytads/engine.js       pure function: (snapshot, videos, state) → commands
   ├─ scripts/ads/ytads/headlines.js    Claude writes headlines from the video title/description
   ├─ scripts/ads/ytads/lint.js         compliance lint — a headline that fails is never used
   ├─ scripts/ads/ytads/headline-style.md   style rules, seeded from Dan's existing headlines
   ├─ scripts/ads/ytads/skiplist.json   video ids that never run paid
   ├─ server.js routes  POST /api/ytads/sync   POST /api/ytads/results   GET /api/ytads/state
   └─ Postgres  ytads_events (video_id, campaign, ad_id, event, detail, at)  — the only server state
              ▲                          │
   snapshot   │                          │ commands
              │                          ▼
   Google Ads Script (hourly, inside the account)  — the HANDS   scripts/ads/ytads/ads-script.js
   ├─ GAQL: every ad in the 3 campaigns: id, name, labels, status, policy status,
   │        lifetime cost + conversions, trailing-30d cost + conversions
   ├─ POST snapshot → receives commands
   ├─ executes: createAd / pauseAd / enableAd / label
   └─ POST results (ids created, errors verbatim)
```

**Google is the ledger.** Ad names carry the video id (`AUTO test yt:<videoId> · tier2 · 2026-09-03`),
labels carry the state (`AUTO`, `AUTO:TEST`, `AUTO:CHAMPION`, `AUTO:RETIRED`, `AUTO:RETIRED-DAY1`).
"Has this video been tested in this campaign?" is answered by the snapshot, never by a state file, so
a re-run can never double-create. `ytads_events` exists for the brief and for reversibility (the
day-one pause list is written there before it is executed). `DATABASE_URL` is in the secrets file.

**The Ads Script's hourly run is the clock.** There is no separate cron: every hour the script posts
the snapshot, the server checks the RSS feed and computes commands in the same request, the script
executes them and posts the results. One round trip plus one results post.

### The hourly cycle, in order

1. **Guard.** Server returns `dryRun: true` on every command unless `YTADS_ENABLED=1` in Railway. In
   dry-run the script logs the commands and executes nothing.
2. **Discover videos.** `https://www.youtube.com/feeds/videos.xml?channel_id=UC236gjadarHAhEhOMYNGJ9g`
   (verified live 2026-09-02; lists public videos including Shorts, no API key). Candidates =
   videos with `published` ≥ `START_DATE` (constant, the go-live day) that are not in
   `skiplist.json` and have no `AUTO` ad in a given campaign.
3. **Write headlines** for each new video (once per video, cached in `ytads_events` as a
   `headlines` event so the three campaigns share them): Claude, given the video title, description,
   the style rules file, and the lint rules. Run every headline through `lint.js`; regenerate up to
   3 times; if still failing, **do not create the ad**, write a `skip` event with the failing text,
   and the brief shows it. Conservative beats clever. Claude API usage: load the `claude-api` skill in
   the build session; a small model is plenty (it writes five 40-character lines).
4. **Create the ads.** For each (video, campaign) pair with no `AUTO` ad: Demand Gen video responsive
   ad in the campaign's existing ad group, status ENABLED, labels `AUTO` + `AUTO:TEST`, name as above.
   Business name, logo image, final URL, and call-to-action are **copied from that campaign's
   existing ads** (read in Phase 0) — never invented. The video asset is a YouTube video asset for
   the new video id. On any creation error: write a `skip` event with Google's message verbatim,
   move on, and the brief shows it.
5. **Pause finished tests.** For every `AUTO:TEST` ad with lifetime cost ≥ **$5.00**: read its
   lifetime conversions.
   - conversions < `MIN_CONV[campaign]` → pause, label `AUTO:RETIRED`, event `verdict:no-read`.
   - else cost/conv < champion's trailing-30d cost/conv (or champion has none) → **promote**: relabel
     the test `AUTO:CHAMPION`, pause the old champion and relabel it `AUTO:RETIRED`, event `promote`.
   - else → pause, label `AUTO:RETIRED`, event `verdict:lose` with both numbers.
   Overshoot is bounded by one hour of the campaign's budget split across its active ads — well under
   $1 on a $15/day campaign — and Google's spend reporting is near-live; conversions lag hours, which
   is why a test is judged at ≥$5 spend and not at the moment it is created.
6. **Policy watch.** Any `AUTO` ad whose policy status is DISAPPROVED → pause it, event
   `policy:disapproved` with the policy topic, never retry the same video in that campaign. "Eligible
   (Limited)" is reported, not acted on (the existing Demand Gen creative already carries that under
   the body-image policy).
7. **Day-one pass (runs once, when no `AUTO:CHAMPION` exists in a campaign).** Among ENABLED
   non-`AUTO` ads with lifetime cost ≥ $5 and conversions ≥ `MIN_CONV`, pick the lowest lifetime
   cost/conv → label `AUTO:CHAMPION` (it keeps its name; it was Dan's ad). Pause every other
   non-`AUTO` ENABLED ad in that campaign, label `AUTO:RETIRED-DAY1`, and write the full id list to
   `ytads_events` FIRST so it can be reversed with one command (`enableAd` for each). If no ad
   qualifies, do nothing in that campaign (interpretation 6).
8. **Report.** `GET /api/ytads/state` renders into `brief-ytads.json` → a **"YouTube engagement ads"**
   block in the morning brief, styled like the Meta "Auto-boost" block: per campaign the champion
   (video, 30-day spend, conversions, cost/conv, ≈cost/subscriber at the 1.96 correction — shown
   beside the raw number, never instead of it), tests in flight (video, spend/$5, conversions, days
   waiting), **every ad created since yesterday WITH ITS HEADLINES** (this is Dan's review surface),
   verdicts, skips with Google's reason, policy issues, and the day-one pause list the first morning.
   Add the render spec to the morning-brief task's `SKILL.md` next to "Ad spend" / "Auto-boost".

### Headlines — conservative, in Dan's existing style

- **Phase 0 reads Dan's current headlines** (all 29 ads: headlines, long headlines, descriptions,
  business name, CTA, final URL) via the first snapshot, and writes `headline-style.md` from them:
  the shapes he uses, the words he uses, length, tone. Do not describe the style from memory.
- **`lint.js` is a hard gate**, built from memory `ad-suspension-prevention` and the 8/11 copy fixes:
  no physical-result promises ("get abs", "get a six pack", "lose", "burn", "shred", "transform your
  body", "real results"), no timeframes ("in 30 days", "in 2 weeks"), no before/after language, no
  disease, drug, or medication names (no "Zepbound", "Ozempic", "GLP-1" — the Zepbound video gets a
  headline about the video's topic that never names the drug), no "guaranteed", no "®"/"™", no
  superlatives about the viewer's body, no negative self-image phrasing ("out of shape", "fat",
  "embarrassing"), no all-caps, no exclamation marks, ≤40 chars for headlines and ≤90 for long
  headlines/descriptions, and each must be about **the video** (what the viewer will see), never the
  product's results. Sell the video and the visualization, never the body.
- Dan's feedback loop: he edits headlines in the UI (the system never touches an existing ad) and
  tells Claude what was wrong; that session appends a rule to `headline-style.md`. Rules accumulate;
  nothing is relaxed without Dan.

### Access path — Scripts now, API long term

- **Google Ads Scripts** (Tools → Scripts in the account) run JavaScript inside the account on an
  hourly schedule with no developer token and no OAuth setup — one authorization click from Dan.
  `AdsApp.search()` runs GAQL; `AdsApp.mutate()` performs Google Ads API mutate operations;
  `UrlFetchApp` reaches our server. It is the fastest way to be live this week.
- **The Google Ads API** is better long term: the executor lives in our repo under test, on the same
  Railway footing as the Meta automation, with no code living in Google's editor, no hourly-only
  cadence, and no 30-minute execution limit. It needs the developer token (Phase 1 of the 8/31
  handoff: apply in MCC `324-458-6445` → API Center; Basic access takes days; Dan accepts the API
  Terms and clicks the OAuth consent — both explicit-permission moments) and an `adwords`-scoped
  refresh token (`GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_OAUTH_CLIENT_ID/SECRET`,
  `GOOGLE_ADS_REFRESH_TOKEN` in `~/.absbyai-secrets.env`, never in the repo). It also unblinds the
  Google leg of `scripts/ads/ads-digest.js`, which is already written for it.
- **Plan: do both.** Build the brain server-side (unchanged in either world), ship the Ads Script
  executor first, and apply for the developer token in the same session so the wait runs in parallel.
  When Basic access arrives, a short follow-up session replaces the executor with
  `scripts/ads/ytads/run.js` (Node, direct API, Railway cron `15 * * * *`) and deletes the Ads
  Script. The engine, lint, headlines, events, and brief do not change.

---

## VERIFY BEFORE WIRING THE RULES

1. **`AdsApp.mutate` can create a Demand Gen video responsive ad and a YouTube video asset.** This
   is the one genuinely uncertain piece. Test with ONE PAUSED ad in the tier-2 campaign referencing an
   already-advertised video, headlines copied from an existing ad; confirm it appears in the UI;
   remove it. If Scripts cannot create this ad type: the script still does reads, pauses, promotions
   and the day-one pass (plain status mutations, certainly supported), and ad creation waits for the
   API token — say so in the coordination file rather than driving the Ads UI by browser (documented
   fragile, 2026-08-22).
2. **Ad group ids.** Each campaign's single enabled ad group id, from the first snapshot. If a
   campaign has more than one, ask which; do not guess.
3. **Required fields on the existing ads** (final URL, business name, logo asset id, CTA, long
   headlines, descriptions) — copy the exact resource names from an existing ad in each campaign.
4. **The conversion column.** `metrics.conversions` at `ad_group_ad` level for one campaign must
   match the UI's conversions for the same range; the ≈1.96 subscriber correction is from
   `ads-digest.js` and is reported alongside, never applied silently.
5. **Spend-report lag.** Note the difference between a test's spend in the snapshot and in the UI
   an hour later; if it is materially over $1, judge tests at ≥$4.50 instead of ≥$5 and record the
   measurement here.
6. **Ab-wheel short 1's video id** → `skiplist.json` (find it in
   `SHORTS_UPLOAD_PLAN.json` / the ab-wheel batch, not from memory).
7. **`ANTHROPIC_API_KEY` and `DATABASE_URL` are already in Railway** (`railway variables --service
   abs-by-ai --kv`); add `YTADS_KEY` (new random secret, also pasted into the Ads Script header) and
   `YTADS_ENABLED=0`.

## EXECUTION PHASES

- **Phase 0 — discover.** Install a read-only version of the Ads Script (snapshot only) so the first
  sync returns all 29 ads with full copy and structure. Write `headline-style.md` from it. This also
  settles VERIFY 2–4. Dan-in-the-loop: the one authorization click. Claude drives Dan's real Chrome
  (claude-in-chrome) to paste the script — **warn him before the takeover** (memory
  `computer-takeover-frustration`). The account is under MCC `324-458-6445`, found by typing "abs"
  in the account picker's search box.
- **Phase 1 — brain + tests.** `engine.js` pure and deterministic with `engine.test.js` in the style
  of `ads-digest.test.js`: new-video discovery, skip list, one-ad-per-(video,campaign), $5 pause,
  `MIN_CONV` no-read, win, lose, champion-with-no-conversions, day-one pick, day-one no-qualifier,
  disapproved, dry-run flag, and "never touches a non-AUTO ad after day one". `lint.js` with a test
  per banned pattern plus the 8/11 headlines as must-fail fixtures. Routes + `ytads_events` migration
  (`CREATE TABLE IF NOT EXISTS`). Commit, push, live-verify the gated routes (401 without the key).
- **Phase 2 — executor.** Full Ads Script; VERIFY 1 with the paused test ad; hourly schedule.
- **Phase 3 — dry run.** `YTADS_ENABLED=0`: one full hour observed; the brief block renders the
  planned day-one pause list and the planned ads for any video published since `START_DATE`. Show
  Dan that report. **He said publish immediately, so this is the mechanics check, not a copy
  approval** — it exists so the first live run cannot mass-pause the wrong ads.
- **Phase 4 — enable.** `YTADS_ENABLED=1`. Watch the first live hour: day-one pass executed,
  champions labelled, any pending videos' ads created. Verify in the UI. Report to Dan with the
  headlines that went live.
- **Phase 5 — API application** (same session as Phase 0, while at the account): apply for the
  developer token and Basic access, mint the OAuth refresh token per the 8/31 handoff's Phase 1. Dan
  accepts the Terms and the consent screen. Record state; the migration session waits on Google's
  approval email (Dan's Gmail).
- **Later — migrate the executor** to the API and unblind the ads digest's Google leg.

## TRAPS ALREADY PAID FOR

- Account facts, MCC trap, "type abs in the picker", zero-disapproval baseline: 8/31 handoff.
- Never create a second Google Ads account; this identity carries prior suspensions; boring creative
  and steady budgets are the margin (memory `ad-suspension-prevention`).
- Videos must be public before an ad can reference them — the RSS feed only lists public videos, so
  this is automatic; scheduled Shorts appear when they go live.
- The tier-1 and tier-2 campaigns must keep **separate budgets** (8/22 restructure) — nothing here
  changes budgets, and nothing here should.
- Google's `conversions` ≈ 2x real subscribers on this account (measured 2026-08-26: 1,553 vs 792).
- Ads sit in policy review for hours after creation; a test with $0 spend is never judged.

## DELIVERY CHECKLIST

- [ ] `scripts/ads/ytads/{engine,lint,headlines}.js` + tests green; `headline-style.md` seeded from the real ads; `skiplist.json` with ab-wheel short 1.
- [ ] `ytads_events` migration; routes live and gated; `YTADS_KEY`, `YTADS_ENABLED` in Railway.
- [ ] Ads Script installed and authorized, hourly, VERIFY 1 passed (or its fallback recorded).
- [ ] One dry-run hour shown to Dan; then enabled; first live hour verified in the UI.
- [ ] Morning brief "YouTube engagement ads" block rendering; render spec in the brief task's `SKILL.md`.
- [ ] Developer token + Basic access applied for; OAuth refresh token minted; state recorded.
- [ ] Commit, push, live-verify, coordination entry updated, this handoff's Key dashboard task checked off (`money::Execute handoff: Google Ads engagement champion…`).

## MODEL / EFFORT

- **High-usage branch (recommended): Fable 5.1, high effort**, one long session for Phases 0–4. Real
  money, a mass-pause on day one, and an untested mutate path inside Google Ads Scripts — the
  failure modes are subtle field names and a rule that fires on the wrong ads.
- **Low-usage branch: Opus 5, medium effort** for Phase 1 (pure engine + lint + tests, no account
  access needed), then a second short session on Fable 5.1 for Phases 0, 2–5 at the account.

## STARTER PROMPT (paste into a fresh session)

```
Execute Handoffs/handoff-20260902-google-ads-engagement-champion-automation.md.

Build the YouTube engagement champion system: every new public video on the channel (Shorts included)
gets one new Demand Gen engagement ad in each of the three existing campaigns the hour it goes up,
with conservative auto-written headlines published immediately (no approval gate); each ad runs inside
its campaign's normal budget until it has spent $5, judged by READING its spend, then it is paused;
each campaign keeps one champion (lowest cost per conversion), a test that beats it takes its seat; on
day one the best existing hand-made ad per campaign becomes champion and the rest are paused. Budgets
stay $15/$15/$5 a day. The decisions in the handoff are final; the "interpretations" section lists the
calls I made that you should state back to me in your first report.

Brain lives on our server (engine + lint + headlines + events + morning-brief block), hands are a
Google Ads Script installed in the account; apply for the API developer token in the same session so
the executor can move to the API later. Do Phase 0 first (read all 29 existing ads and write the
headline style rules from them), pass the VERIFY list, build with YTADS_ENABLED=0 and show me one
dry-run report before enabling. Warn me before you take over my Chrome.
```
