# Handoff: Phase B — Google Ads offline conversion upload for trial→paid memberships

**Date:** 2026-08-18
**Project:** Abs By AI
**Business goal this serves:** Marketing performance → profitability. Phase A made membership sales *visible* to Google Ads; Phase B makes them **completely** visible, including the members Phase A structurally cannot reach (app buyers, ad blockers, and anyone who doesn't reopen the app after their trial converts).

## Objective

Report every trial→paid membership sale to Google Ads **server-to-server**, keyed on the `gclid`/`gbraid`/`wbraid` already stored on `users.ads_click_id`, instead of waiting for the member to reopen the site so a browser tag can fire. Phase A (shipped 2026-08-18, commit `24d9b18`) already reports the sale on the member's next visit; Phase B removes the "next visit" dependency entirely and recovers the three groups Phase A misses. **Start with the credential-free scheduled-fetch route (B1), not the full API build (B2)** — see the Key Decisions.

## Current State

**Phase A is live and working end to end.** Do not rebuild any of it.

- **The click id is captured and stored.** `public/index.html` reads `gclid`/`gbraid`/`wbraid` from the landing URL at module top level (`AD_CLICK_KEY = 'absbyai_ad_click'`, ~line 3300) into localStorage + a 90-day cookie, and sends it on signup and membership checkout. `server.js` validates against `/^[A-Za-z0-9_-]{1,200}$/` and stores **latest-wins** on `users.ads_click_id` / `users.ads_click_at` via `recordAdClickId()` (~4172). Shipped 2026-08-17, commit `72f5697`.
- **The trial→paid moment is detected and stamped.** `syncSubscriptionState()` (~5630) reads the previous `membership_status` before overwriting it and calls `markPaidConversionPending()` (~5596) on `trialing → active`; `applyAppleMembership()` (~5755) does the same for RevenueCat, covering both the webhook and `/api/apple/sync`. The stamp lands on `users.paid_conversion_pending_at`.
- **The client reports it and acks.** `/api/membership` returns `paidConversionPending` / `paidConversionValue` / `paidConversionCurrency` via `paidConversionPayload()` (~5616); `refreshMembership()` in `public/index.html` fires `fireAdConversion(AD_SUBSCRIBE_LABEL, {value, currency})` and POSTs `/api/ads/paid-conversion-ack` (~5315), which sets `users.paid_conversion_fired_at`. Dedupe is per-subscription on the user row, **not** the per-browser `once:` record.
- **The Ads conversion action is configured correctly:** `Subscribe`, conversion type ID **`7703335439`**, **Count: One**, **click-through window: 90 days**, **Value: "Use different values"**, source **Website**, label **`dQUqCI-kntkcEJvEqLNE`** (full: `AW-18361229851/dQUqCI-kntkcEJvEqLNE`). Conversion id is `AW-18361229851`.
- **Live-verified** on absbyai.com with a throwaway account: one conversion, correct value, 3 pings to Google, flag cleared, no re-fire, test account deleted, prod back to baseline.

**What Phase A cannot do, which is the entire reason Phase B exists:**
1. **App members.** The iOS/Android WebViews cannot hold the `_gcl_aw` cookie set in the user's external browser, so an app-only member is weakly attributed no matter what the browser fires.
2. **Members who don't return** after the trial converts — the flag simply sits pending forever.
3. **Ad-blocked browsers** — `fireAdConversion` returns false and we ack anyway (deliberate; re-offering forever would eventually double-report elsewhere).

**Nothing is half-built for Phase B.** No credentials, no developer token, no columns, no endpoints. This is a clean start.

**Business context that should shape urgency:** the Search campaign is currently on **Maximize Clicks with a $2.00 cap**, which uses no conversion data at all. Phase B's value is therefore *measurement* today and *bidding* only once Dan moves to a Smart Bidding strategy. Build it before that switch, not after.

## Key Decisions Already Made

- **Phase B is the upgrade path, and Phase A stays until B is proven.** Settled 2026-08-17 and unchanged. Phase A needed zero Google credentials and covers the common case; Phase B is the only route that survives a device or browser change.
- **Do the credential-free route first (B1), then decide whether to build the API integration (B2).** Google Ads can **fetch a CSV from an HTTPS URL on a schedule** — no developer token, no OAuth, no API review. That gets essentially all of Phase B's value for a fraction of the work, and it validates the whole approach (does our stored click id actually match? do conversions land?) *before* anyone spends days on API access. **This is the recommended path and the reason this handoff is not "go get a developer token."**
- **A new conversion action will almost certainly be required.** The existing `Subscribe` action has source **Website**. Google's offline click-conversion import requires an action created as an **import/API** type; a website-tag action will reject uploads. Plan for creating `Membership Paid (offline)` and treat reusing `Subscribe` as the thing to *verify*, not assume.
- **Two actions reporting the same sale would double-count.** Whatever is built, exactly one of {Phase A client fire, Phase B upload} may be Primary / included in account-level goals for a given member. See the OPEN item in step 6.
- **Value stays the real plan price** — $19.99 monthly / $69.99 annual, falling back to monthly when the plan is unrecorded (under-report rather than invent revenue). Same rule as `paidConversionPayload()`.
- **Never break billing sync for attribution.** Every conversion write in Phase A is fail-open, proven by dropping the column mid-run. Phase B must hold the same line.
- **Do not touch the Demand Gen campaign, the two live conversion tags** (Free Generation Started `KqDxCMzl4dkcEJvEqLNE`, Trial Signup `AqLTCMnl4dkcEJvEqLNE`), **or the Phase A wiring.**

## Detailed Plan

### Step 0 — Confirm the conversion-action constraint before building anything (15 min)

In Ads → Goals → Conversions → **+ New conversion action** → **Import** → check which import sources are offered (expect "Other data sources or CRMs" → "Track conversions from clicks"). Create **`Membership Paid (offline)`**, category **Purchase**, **Count: One**, **click-through window: 90 days**, value **"Use different values"**.

Then confirm whether the existing `Subscribe` (source: Website) appears as a valid target for offline click uploads. **If it does, reusing it is simpler and avoids the double-count problem entirely.** If it doesn't — the expected outcome — the new action is the upload target and step 6's decision becomes live.

> **OPEN:** whether Google now permits click uploads against a website-source action. Verify; don't assume either way.

### Step 1 — Add the upload bookkeeping column (`db.js`)

One column via the existing `ADD COLUMN IF NOT EXISTS` loop, alongside `paid_conversion_pending_at` / `paid_conversion_fired_at`:

- `ads_offline_uploaded_at TIMESTAMPTZ`

Deliberately **separate from `paid_conversion_fired_at`**: the client fire and the offline upload are two independent delivery channels, and collapsing them makes it impossible to tell which one actually reported a given sale — which is exactly the number that decides whether B2 is worth building.

No column is needed for the conversion *time*: `paid_conversion_pending_at` already records the moment trial→paid was detected, which is the sale time.

### Step 2 — Serve the conversion feed (`server.js`)

New route `GET /api/ads/offline-conversions.csv`, guarded by a long random secret in a new Railway env var (`ADS_FEED_SECRET`), compared in constant time — same pattern as `MONARCH_PUSH_SECRET` / the RevenueCat webhook secret. Returns `text/csv`.

Rows: users where `paid_conversion_pending_at IS NOT NULL` **AND** `ads_click_id IS NOT NULL` **AND** `ads_offline_uploaded_at IS NULL` **AND** the click is inside the window (`ads_click_at > paid_conversion_pending_at - 90 days`).

**Do not hand-write the CSV header.** Google's format is picky (it carries a `Parameters:TimeZone=` preamble line above the column names, and the column names have changed over time). **Download the official template from the Ads UI** at the upload screen and mirror it byte-for-byte. Columns are, in substance: Google Click ID · Conversion Name · Conversion Time · Conversion Value · Conversion Currency.

Two things that will bite:
- **Conversion Time format is exact** (`yyyy-MM-dd HH:mm:ss+|-HH:mm`, or a named timezone in the preamble). Generate it deliberately; do not `toISOString()` and hope.
- **Conversion Name must match the action name exactly**, including case and spacing.

### Step 3 — Mark rows uploaded

Google's scheduled fetch gives no per-row success callback, so "uploaded" has to be inferred. Safest design: the feed endpoint stamps `ads_offline_uploaded_at = NOW()` on exactly the rows it just emitted, in the same request, **after** the CSV is successfully serialized.

Accepted trade-off: a fetch that Google starts and abandons would mark rows uploaded that never landed. That is a rare, one-way loss of a signal we never had before — strictly better than the alternative (never marking, and re-uploading the same sale every day, which Google may or may not dedupe depending on whether the action is Count: One). **Include the `Conversion Time` faithfully so Google's own dedupe on {gclid, action, time} is available as a second line of defence.**

### Step 4 — Schedule the fetch in Google Ads

Ads → Goals → Conversions → **Uploads** → **Schedule** → source **HTTPS**, URL = the endpoint with its secret, frequency **daily**. Run one **manual** upload first and read the results screen — it reports per-row errors (unknown gclid, conversion outside the window, malformed time), which is the fastest possible feedback loop on format problems.

### Step 5 — Verify against production, no guessing

- Create a throwaway prod account (the Phase A verification used `paidconv-verify-<ts>@example.com` and deleted it afterwards — `@example.com` is excluded from the welcome sweep). Give it a **real** `ads_click_id` captured by clicking a live ad, or accept that a synthetic gclid will be rejected as unknown (**a rejection for "unknown click id" still proves the format and the pipe are correct** — treat that as a pass for everything except matching).
- Confirm the row leaves the feed after upload, that a second fetch returns it zero times, and that `/health` plus a normal generation are unaffected.
- Delete the test account and confirm prod is back to baseline (`SELECT count(*) FROM users`, and zero rows carrying stamps).

### Step 6 — Retire or scope Phase A's client fire

Once B1 demonstrably lands conversions:

> **OPEN — Dan's call, and it is a real decision, not a cleanup:** does the browser fire stay on?
>
> - **Recommended:** keep the client fire **only for members with no `ads_click_id`** (organic signups, who have nothing to upload) and skip it for members the feed already covers. One condition in `paidConversionPayload()`. Avoids double-counting while losing nothing.
> - **Simplest:** turn the client fire off entirely once the feed is proven. Organic sales then go unreported — which is arguably correct, since an unattributed conversion contributes nothing to bidding anyway.
> - **Do not** leave both channels reporting the same member into two Primary actions.

### Step 7 — Record and close out

Update `AI_COORDINATION.md`, check off the Rule-8 dashboard task, and record the measured recovery rate: **conversions uploaded via the feed vs. conversions the browser fired**. That ratio is the answer to "was Phase B worth it," and it is the number that justifies (or kills) B2.

### Step 8 — B2, the full API integration — ONLY if B1's limits actually bind

Do **not** start here. Reach for it only if the scheduled feed proves insufficient — e.g. Dan wants same-hour reporting rather than daily, or needs conversion *adjustments* (refunds, cancellations) which the CSV route handles poorly.

What it costs, so the decision is informed:
- A **developer token**, applied for through a **manager (MCC)** account — Dan has `Social Response Marketing MCC` (963-322-0811), which is the prerequisite.
- **A new developer token starts at *Test Access*, which can only call test accounts.** Reaching a production account needs **Basic Access**, which is a Google review. Budget days, not minutes. This single fact is why B1 comes first.
- OAuth2 client + a refresh token, stored in Railway.
- Then `ConversionUploadService.UploadClickConversions`, which also unlocks `UploadConversionAdjustments` for refunds.

**Also worth evaluating at that point, as an alternative rather than an addition: Enhanced Conversions for Leads**, which matches on a hashed email instead of a click id. We already hold verified emails, so it would cover members who have **no** stored click id — a group neither Phase A nor B1 can attribute. Different mechanism, overlapping purpose; pick one deliberately.

## Things to Avoid / Lessons Learned

- **A website-source conversion action probably cannot receive click uploads.** Confirm in step 0 before building the feed around the wrong action.
- **Never hand-write Google's CSV header** — take the template from the UI. Time format and exact conversion-name matching are the two most common failure modes, and both surface as silent zero-row imports.
- **Conversions outside the 90-day click window are rejected.** Our funnel (click → free generations → trial → +7 days → paid) can genuinely approach that, which is exactly why the window was raised from 30 to 90 on 2026-08-18. Filter on it in the query rather than letting Google reject rows.
- **Attribution must stay fail-open.** Phase A proves this by dropping the column mid-run and confirming the webhook still 200s and billing still syncs. Any Phase B write must satisfy the same test.
- **A 200 from a data endpoint is not proof.** Verify by re-reading state, and read the Ads upload results screen rather than trusting that the fetch "worked."
- **The Ads console is awkward to automate.** The account is **not** in `danroseconsulting@gmail.com`'s default picker — search **"342"**. Screenshot coordinates are unreliable (innerWidth 2111 vs a 1568 screenshot ≈ 0.74 scale); use `find` refs. Dropdowns are AngularDart and may need the full `pointerdown→mousedown→pointerup→mouseup→click` dispatch inside a single tool call, because the menu closes between calls. The UI has wedged in Claude-driven tabs before — check `list_connected_browsers` and keep it to one instance.
- **Conversion actions are web-UI only.** Google Ads Editor and bulk upload cannot touch them (verified 2026-08-17).
- **Verifying a conversion tag necessarily fires it.** Phase A's live test put one real $19.99 conversion into the account; expect Phase B testing to add a small amount of similar noise, and say so rather than letting it look like revenue.
- **Deploys can be slow.** Phase A's took ~9 minutes (genuinely building — `railway status` said `Building (7m)`). Poll on a content marker, never a status code; the SPA fallback returns 200 for unknown routes.

## Relevant Files & Locations

- `server.js` — `recordAdClickId` (~4172), `/api/ads/paid-conversion-ack` (~5315), `paidConversionPayload` (~5616), `markPaidConversionPending` (~5596), `syncSubscriptionState` (~5630), `applyAppleMembership` (~5755), `MEMBERSHIP_PLANS` (~179). Sweep-job precedents to copy for any periodic work: `trialReminderSweep` / `welcomeSweep` / `sweepOrphanedAuditJobs`, registered ~9509–9523.
- `db.js` — the `ADD COLUMN IF NOT EXISTS` loop holding `ads_click_id`, `ads_click_at`, `paid_conversion_pending_at`, `paid_conversion_fired_at`.
- `public/index.html` — `AD_CONVERSION_ID` / `AD_SUBSCRIBE_LABEL` / `fireAdConversion` (~3281–3400), `reportPaidMembershipConversion` + `refreshMembership` (~7040).
- Google Ads account **342-717-0837** → Goals → Conversions (action `Subscribe`, type ID `7703335439`) and Goals → Conversions → **Uploads**.
- Manager account for the developer-token application (B2 only): `Social Response Marketing MCC` **963-322-0811**.
- Env vars: existing `STRIPE_WEBHOOK_SECRET`, `REVENUECAT_WEBHOOK_SECRET`, `MONARCH_PUSH_SECRET` (secret-compare precedents); new `ADS_FEED_SECRET`.
- Secrets/DB access: `~/.absbyai-secrets.env` (0600) or `~/.npm-global/bin/railway variables --kv`. **`DATABASE_URL` in that file is the Railway-internal host and will not resolve from the laptop** — use `DATABASE_PUBLIC_URL` from `railway variables --service Postgres --kv`.
- `AI_COORDINATION.md` — the Phase A entry ("Google Ads *Subscribe* conversion WIRED", 2026-08-18) carries the full mechanism and the measured verification.

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Codex current flagship, medium effort |

Routine build work against a well-specified plan — one column, one read-only endpoint, one CSV formatter, plus console configuration. The genuinely tricky parts (the action-type constraint, the double-count decision, fail-open) are settled or flagged above, so flagship Claude isn't warranted. **One override:** if step 6's double-count decision gets reopened, or if B2 turns into a real architecture question, that part is an always-Claude planning task — bring it back rather than letting a routine session pick a default. Escalate to Opus with extended thinking only if Google's import behaviour turns out materially different from what step 0 finds.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260818-phase-b-offline-conversion-upload.md` — Google Ads offline conversion upload for trial→paid memberships. Read that handoff and the "Google Ads *Subscribe* conversion WIRED" entry in `AI_COORDINATION.md` first; Phase A is live and must not be rebuilt or broken. **Start with step 0 — confirm in the Ads UI whether offline click uploads require a new import-type conversion action or can target the existing `Subscribe` action — because that answer decides the shape of everything after it.** Then build the credential-free scheduled-CSV route (steps 1–5) and stop at step 6 for Dan's call on whether the Phase A browser fire stays on. Do NOT apply for a Google Ads API developer token or start B2 unless step 5 shows the CSV route genuinely can't do the job.
