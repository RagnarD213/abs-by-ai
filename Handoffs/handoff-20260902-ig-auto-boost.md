# Handoff — IG auto-boost: every new @danrosefit post gets a $5 profile-visits test, one champion runs at ~$200/month

**Written:** 2026-09-02 (Claude Code, Fable 5.1), details agreed with Dan in chat the same evening.
**Status:** NOT EXECUTED. Design locked, nothing built.
**Prerequisites already done:** Meta app `1598463548528030` is LIVE; `META_ADS_TOKEN` (system user,
never expires) + `META_APP_SECRET` in `~/.absbyai-secrets.env`; the creative shape that runs an ad
as @danrosefit is proven in `scripts/ads/boost_danrosefit_posts.py`; the profile-visits campaign is
live and becomes the first champion.
**Parent handoff (read its "SESSION 2 RESULT" section first):**
`Handoffs/handoff-20260902-ig-engagement-ad-identity.md`.

---

## THE GOAL IN ONE PARAGRAPH

Dan wants **followers** on @danrosefit. Meta cannot optimize for follows, so the system buys the
step before a follow — **Instagram profile visits** — and measures follows after the fact. Every new
@danrosefit post (reels AND images) automatically gets a **$5 lifetime test ad** the hour it goes up.
Tests are ranked on **cost per profile visit**. A single **champion** ad runs continuously at
**$6.50/day (~$200/month)** and is judged weekly on **cost per follow**. A test that beats the
champion replaces it. Losers stop themselves when their $5 is spent. Dan never touches Ads Manager.

## DECISIONS DAN MADE (do not re-open)

| Decision | Value |
|---|---|
| Objective / optimization | Traffic → `VISIT_INSTAGRAM_PROFILE`, destination `INSTAGRAM_PROFILE` (NOT engagement — Dan chose profile visits after the correlation argument) |
| Test budget | **$5 lifetime per post**, one ad set per post |
| Champion budget | **$6.50/day ≈ $200/month**, one active ad at a time |
| Monthly cap (script-enforced) | tests **$300/month**, total **$500/month**; stop creating tests at the cap |
| Which posts | reels **and** images (carousels: try, skip on error) |
| Targeting | identical to ad set `120250753601020682`: men 25–54, US/CA/GB/IE/AU/NZ, Instagram-only placements, Advantage audience off. **Copy it via `GET /120250753601020682?fields=targeting` — do not hand-type it** |
| Test verdict metric | cost per Instagram profile visit |
| Champion verdict metric | cost per follow (Ads Manager "Follows or likes"), trailing 7 days |
| Kill / scale lines (champion) | pause at **>$5/follow** with ≥$35 spend in the window; **<$3/follow** is reported as a scale candidate, NOT auto-scaled (cap is fixed) |
| Promotion rule | test cost/visit **< champion's trailing-7-day cost/visit** AND test has **≥10 visits**; ties keep the champion |
| Test window | evaluate when spend ≥ **$4.50** OR **5 days** after creation, whichever first |

---

## ARCHITECTURE

### Campaign layout (one campaign, ad-set-level budgets)

```
Campaign  120250753198730682   rename → "[AUTO] IG PROFILE VISITS - danrosefit"   (is_adset_budget_sharing_enabled=false)
├─ Ad set 120250753601020682   rename → "CHAMPION"      daily_budget 650   exactly ONE active ad
│    ├─ ad "CHAMPION::18188183254395331"  (channel-intro reel — currently ACTIVE, see "first run")
│    └─ ad "CHAMPION::18192762022391478"  (3-min total body — currently ACTIVE, see "first run")
├─ Ad set "TEST::<media_id>"   lifetime_budget 500, end_time = created + 5d, one ad "TEST::<media_id>"
├─ Ad set "TEST::<media_id>"   …
```

**Meta is the ledger.** The media id lives in the ad-set name, so "has this post been tested?" is
`GET /act_2143998876461525/adsets?fields=name&filtering=[{field:"name",operator:"CONTAIN",value:"TEST::<id>"}]`.
No state file, nothing to drift, and a re-run can never double-create. A tiny Postgres table
(`auto_boost_events`: media_id, event, detail, at) is the only other state, used for skips (posts
Meta refuses to promote) and for the morning brief. `DATABASE_URL` is in the secrets file.

### The hourly job — `scripts/ads/auto-boost.js` (Node, same conventions as `ads-digest.js`)

Runs every hour as a **Railway cron service** (second service on the same repo, start command
`node scripts/ads/auto-boost.js`, schedule `15 * * * *`, must exit when done). Steps, in order:

1. **Guard.** Exit unless `AUTO_BOOST_ENABLED=1`. Read month-to-date spend for the campaign
   (`insights?date_preset=this_month&level=adset`), split champion vs `TEST::*`. If tests MTD ≥ $300
   or total MTD ≥ $500 → skip step 3, still run 4–6, and say so in the brief.
2. **Discover posts.** `GET /17841401601139982/media?fields=id,media_type,media_product_type,timestamp,permalink,caption&limit=25`.
   Candidates = posts with `timestamp` ≥ the system start date (constant in the script, set to the
   go-live day) that have no `TEST::<id>` ad set and no `skip` event.
3. **Create a test per candidate.** Ad set (copy targeting from the champion ad set; `promoted_object
   {page_id: 1380236418500031}`; `optimization_goal VISIT_INSTAGRAM_PROFILE`; `destination_type
   INSTAGRAM_PROFILE`; `billing_event IMPRESSIONS`; `bid_strategy LOWEST_COST_WITHOUT_CAP`;
   `lifetime_budget 500`; `start_time now`; `end_time now+5d`; `status ACTIVE`) → creative (the
   proven top-level shape: `object_id=1380236418500031 instagram_user_id=17841401601139982
   source_instagram_media_id=<id>`, **no `object_story_spec`, no `call_to_action`**) → ad
   (`status ACTIVE`). On any creative error (licensed music, carousel unsupported, dev-mode-style
   blocks) delete the empty ad set, write a `skip` event with Meta's message, move on.
4. **Evaluate finished tests.** For every `TEST::*` ad set with spend ≥ $4.50 or `end_time` passed:
   read `insights?fields=spend,actions,cost_per_action_type` (lifetime). Visits = the profile-visit
   action type (see VERIFY below). Write a `verdict` event. Compare against the champion's trailing
   7-day cost/visit; promote if the rule above passes. Losers need no action — the lifetime budget
   already stopped them; set `status PAUSED` anyway so the table reads clean.
5. **Promote.** Create a new ad `CHAMPION::<media_id>` in the CHAMPION ad set (same creative shape),
   then pause every other ad in CHAMPION and rename it `RETIRED::<media_id>`. Never delete ads —
   history is the point. Write a `promote` event.
6. **Champion health.** Trailing 7 days for the CHAMPION ad set: spend, visits, follows. If spend ≥
   $35 and cost/follow > $5 → pause the champion ad, write a `champion_paused` event, and the brief
   shouts. (With nothing active, the next promotion re-fills it.) If cost/follow < $3 → `scale_candidate`
   event, no budget change.
7. **Report.** Write `brief-autoboost.json`; `ads-digest.js` renders an **"Auto-boost"** block in the
   morning brief: champion (post, 7-day spend, cost/visit, cost/follow), tests in flight (post date,
   spend, visits, cost/visit), verdicts since yesterday, MTD spend vs both caps, skips with Meta's
   reason. Add the render spec to the morning-brief task's `SKILL.md` next to the existing "Ad spend"
   section.

### First run (the two ads already in the champion ad set)

Both existing ads (`120250753783030682`, `120250753783950682`) are ACTIVE in the champion ad set
from 2026-09-02. Treat them as a pair: once each has ≥ $10 lifetime spend, keep the one with the
lower cost/visit as `CHAMPION::…`, retire the other. Until then the "exactly one active ad" rule is
suspended. Do not create `TEST::` ad sets for those two media ids.

---

## VERIFY BEFORE WIRING THE RULES (real data exists by the time this runs)

1. **The profile-visit action type name in `insights.actions`.** The live campaign will have spent
   several days by then. Read its insights and match the count to Ads Manager's "Instagram profile
   visits" column for the same date range. Pin the string as a constant. Do not guess.
2. **The follows action type.** Same method against Ads Manager's **"Follows or likes"** column
   (customize columns → search "Follows"). If Meta does not expose it via the API for Instagram,
   fall back to judging the champion on cost/visit and say so in the brief — Dan accepted this risk.
3. **Minimum lifetime budget.** Meta may reject `lifetime_budget=500` over 5 days. If it does, the
   error names the minimum; shorten the window (3 days) before raising the budget, and record what
   Meta demanded in this doc.
4. **Carousels.** `source_instagram_media_id` on a `CAROUSEL_ALBUM` — try one; if refused, add
   `CAROUSEL_ALBUM` to the skip list permanently.
5. **`META_ADS_TOKEN` / `META_APP_SECRET` in Railway.** They are in the local secrets file; confirm
   `railway variables --service abs-by-ai --kv | grep META_` and add them to the new cron service
   (standing authorization covers Railway env vars).

## META TRAPS ALREADY PAID FOR (read, don't rediscover)

- Ads Manager **cannot** set the Instagram identity for this ad account (read-only Page field; it
  silently runs as @abs.by.ai). The API creative shape above is the only path. Any CTA →
  "The link field is required". Any `object_story_spec` → identity is wrong.
- Unpublished Ads Manager drafts are invisible to the API. **Never click the global "Review and
  publish (7)"** — those are abandoned 9/01 drafts.
- `promoted_object` is immutable after ad-set creation. `explore` placement is deprecated → use
  `explore_home`. Campaign creation requires `is_adset_budget_sharing_enabled`.
- Errors #1487202 / #1341012 in the UI are Meta's async validation lag; they clear on reload.
- New ads sit in `PENDING_REVIEW` / `IN_PROCESS` for hours; the test window is measured from
  creation, so 5 days leaves room. Do not evaluate an ad with $0 spend as a loser before `end_time`.
- Every ad MUST be on the real @danrosefit post (ManyChat "Comment ABS" listens on those comment
  threads). Never upload media.

## DELIVERY CHECKLIST

- [ ] `scripts/ads/auto-boost.js` with `--dry-run` (creates nothing, prints the plan) and a test
      file in the style of `ads-digest.test.js` covering: cap reached, candidate discovery, verdict
      rule (win / lose / not-enough-visits), promotion, champion pause, first-run pair rule.
- [ ] Postgres migration for `auto_boost_events` (idempotent `CREATE TABLE IF NOT EXISTS`).
- [ ] Rename campaign + champion ad set; set champion `daily_budget 650` (already done 2026-09-02 —
      verify it stuck).
- [ ] Railway cron service created, env vars set, one manual run observed end to end.
- [ ] Morning brief "Auto-boost" block rendering; `AUTO_BOOST_ENABLED=1` only after Dan sees one
      dry-run report.
- [ ] Commit, push, live-verify, coordination entry updated, this handoff's Key task checked off.

## MODEL / EFFORT

- **High-usage branch (recommended): Fable 5.1, high effort.** This is API + infra + a rules engine
  with real money attached; the failure mode is a subtle Meta field name or a cap that doesn't hold.
- **Low-usage branch: Opus 5, medium effort**, but only for the script + tests; hand the Railway
  cron + brief wiring to a second short session.

## STARTER PROMPT (paste into a fresh session)

```
Execute Handoffs/handoff-20260902-ig-auto-boost.md.

Build the hourly auto-boost job for @danrosefit: every new post gets a $5 lifetime profile-visits
test ad on the REAL post, tests are ranked on cost per profile visit, one champion ad runs at
$6.50/day and is judged on cost per follow, winners replace the champion, caps are $300/month tests
and $500/month total. The design decisions in the handoff are final — do not re-open them.

Read the parent handoff's "SESSION 2 RESULT" section first: the Ads Manager UI cannot set the
Instagram identity, and only the top-level creative shape in scripts/ads/boost_danrosefit_posts.py
works. Meta app is Live. Tokens are in ~/.absbyai-secrets.env.

Do the VERIFY section against the live campaign's real insights before wiring the rules. Build
with --dry-run first and show me one dry-run report before AUTO_BOOST_ENABLED goes to 1. Never
click the global "Review and publish" in Ads Manager.
```
