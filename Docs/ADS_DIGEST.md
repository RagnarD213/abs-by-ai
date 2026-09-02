# Ads digest — daily Meta + Google spend brief

Built 2026-09-02. Runs as part of the 6:30am morning brief and prints one section:
yesterday's ad spend, anomalies worth acting on, and any ad that is outperforming
enough to scale.

| | |
|---|---|
| engine | `scripts/ads/ads-digest.js` (Node, zero dependencies) |
| tests | `scripts/ads/ads-digest.test.js` — 28 cases, run with `node scripts/ads/ads-digest.test.js` |
| output | `brief-ads.json` at the repo root |
| read by | the morning-brief job (Step 1.5) and `GET /api/ads-digest` (gated) |
| cost | $0.00 — plain HTTP against each platform's own API, no model calls |

```bash
node scripts/ads/ads-digest.js            # yesterday, writes brief-ads.json
node scripts/ads/ads-digest.js --day 2026-08-31 --print
```

---

## ⚠ IT CANNOT SEE EITHER PLATFORM YET, AND THAT IS A CREDENTIAL GAP, NOT A BUG

Both legs are written and tested. Neither has a working read credential as of
2026-09-02, and **both fixes need Dan** — Claude cannot mint either one.

The digest reports this itself, every run, in `blind[]`, with the exact reason and
the exact fix. It stops saying so the moment a credential lands. No code change
and no follow-up task is needed on either side.

### Meta — the stored token is the wrong kind of token

`FACEBOOK_PAGE_ACCESS_TOKEN` is a **Page** token. Verified against `debug_token`
on 2026-09-02: its scopes are `pages_read_engagement`, `pages_manage_posts`,
`public_profile`. Asking it for ad insights returns, verbatim:

> `(#200) Ad account owner has NOT grant ads_management or ads_read permission`

A Page token cannot be upgraded — `ads_read` is a different grant on a different
object. What is needed is a **system-user token**, which never expires (a plain
user token dies in 60 days and would silently take the digest down with it).

**Dan, ~5 minutes, once:**

1. business.facebook.com → **Business settings** → Users → **System users** → Add
2. Name it `abs-by-ai-automation`, role **Employee**
3. **Add assets** → Ad accounts → *Abs by AI* (`act_2143998876461525`) → toggle
   **View performance** (that is `ads_read`; do NOT grant Manage — the digest only reads)
4. **Generate new token** → app *abs by ai automation* → tick **`ads_read`** → Generate
5. Copy it, then store it — never paste it into chat:

```bash
echo "META_ADS_TOKEN=<paste>" >> ~/.absbyai-secrets.env
```

Then `node scripts/ads/ads-digest.js` and the Meta leg is live. Optionally add
`META_ADS_TOKEN` to Railway so `/api/ads-digest` is populated from the server too.

### Google — two credentials missing, both gated on the API handoff

1. **No developer token.** Phase 1 of
   `Handoffs/handoff-20260831-google-ads-api-setup-engagement-ad-automation.md` is
   unexecuted. Apply in MCC **324-458-6445** → Tools → **API Center**. Basic access
   is enough for reporting.
2. **The stored OAuth token is calendar-only.** Verified 2026-09-02 against
   `tokeninfo`: `GOOGLE_REFRESH_TOKEN` carries `calendar.readonly` and nothing
   else. The digest needs a separate refresh token scoped to
   `https://www.googleapis.com/auth/adwords`.

```bash
echo "GOOGLE_ADS_DEVELOPER_TOKEN=<token>" >> ~/.absbyai-secrets.env
echo "GOOGLE_ADS_REFRESH_TOKEN=<token>"   >> ~/.absbyai-secrets.env
```

Account ids default correctly (customer `342-717-0837`, login-customer the MCC),
so no other configuration is needed. The GAQL query and the full response mapping
are already written — this leg starts returning data on the credentials alone.

**Until then the Google section prints one line naming the missing token.** There
is no report-export fallback: Google Ads scheduled reports can only be emailed or
dropped in Drive on a schedule Dan would have to configure by hand, and parsing a
CSV attachment is a worse dependency than the API it is standing in for. The gap
is stated rather than papered over.

---

## What it detects, and why each rule exists

Every rule traces to something that actually happened to this account. Nothing
here is a generic best practice.

| rule | fires when | why it exists |
|---|---|---|
| `spend_stopped` | a campaign averaging ≥$3/day falls below 10% of that | **The 2026-08-31 miss.** Both Meta campaigns were toggled OFF; IG GEO spent $13.26 and stopped, and nobody noticed for six days. A spike-only detector is blind to this. |
| `spend_spike` | ≥2x its own 7-day mean **and** ≥$10 more in absolute dollars | Catches a runaway budget without firing on $1.50 → $4.00, which at these budgets is most days. |
| `zero_results` | ≥$15 across the window with zero results | Google search ran **$63 with 0 conversions, twice** (8/26 and 8/31). |
| `cpa_degraded` | cost/result ≥1.5x its own 7-day mean, ≥5 baseline results | Performance decay, judged against the campaign's own history rather than a cross-account average. |
| `ad_rejected` | any ad DISAPPROVED or WITH_ISSUES | Zero disapprovals across all 29 ads at the 8/26 audit. This exists so the first one is caught the morning it happens. |
| winners | an ad at ≤70% of the account's blended cost/result, on ≥8 results | A scale decision with the numbers attached — not "go look at the ads tab". |

**The floors are the design.** `MIN_SPEND_TO_JUDGE`, `SPEND_SPIKE_MIN_DELTA` and
`WINNER_MIN_RESULTS` exist because this account runs $10–15/day budgets, where a
$2 difference is noise. A digest that cries wolf gets skipped, and a skipped
digest is worth less than no digest. Nine of the 28 tests assert **silence** on
realistic noise, which is the half that is easy to get wrong.

## The ~2x conversion inflation

Google's `conversions` column runs about **double** the real subscriber count on
this account. Measured 2026-08-26: campaign 24122099676 reported **1,553
conversions** on $136.75 while its own ad-group view reported **792 earned
subscribers**. 1553 / 792 = **1.96**.

So `$0.09 per conversion` is really **`$0.17 per subscriber`**.

The digest carries `GOOGLE_CONVERSION_INFLATION = 1.96` and emits
`estSubscribers` / `estCostPerSubscriber` **alongside** the raw numbers, never
instead of them, each carrying `estimateBasis` with the derivation. Silently
deflating a platform's own metric and presenting the result as fact is how a
dashboard starts lying.

**Re-measure this ratio when volume changes.** It is one observation on one
campaign, not a law.

## Where it renders

`brief-ads.json` is committed to the repo root, matching `gmail-digest.json` and
`brief-ask.json`. Note that **the repo is public**, so the campaign names and
daily spend in it are world-readable — the same figures the coordination file
already publishes. If that becomes unwanted, move the output to
`~/.absbyai-ads/` (as `daily-watch-history-review` does with its feed) and drop
`brief-ads.json` from the `git add` line in the morning-brief job; the server
endpoint is the only thing that would lose data.

The morning brief renders the section under an **interrupt bar**: on a quiet day
it prints nothing at all. Silence is the correct and expected output.
