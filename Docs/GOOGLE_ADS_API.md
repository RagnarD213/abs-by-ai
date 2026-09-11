# Google Ads API — how this project reads and changes account 342-717-0837

Live since 2026-09-10. Direct REST calls through `scripts/ads/api/client.js` are now the normal way to read and
change the Abs by AI Google Ads account. The paste-a-script-into-the-Ads-editor channel is the fallback only; the
hourly engagement-champion Ads Script (`Docs/YTADS.md`) keeps running as it is.

## Everyday use

```bash
node scripts/ads/api/client.js whoami                         # accounts this login can reach
node scripts/ads/api/client.js search "SELECT campaign.id, campaign.name, campaign.status FROM campaign"
node scripts/ads/api/client.js policy 24243839443             # per-line policy verdicts for a campaign
node scripts/ads/api/client.js mutate ops.json --dry-run      # Google validates, nothing changes
node scripts/ads/api/client.js mutate ops.json --note "why"   # applies, all-or-nothing
```

Dan's one-off edits keep going through the queue, which now **executes immediately**:

```bash
node scripts/ads/ytads/manual.js headlines <adId> "H1" "H2" --note "why"            # queued AND sent now
node scripts/ads/ytads/manual.js pause customers/3427170837/adGroupAds/<ag>~<ad> --dry-run   # validate only
node scripts/ads/ytads/manual.js raw '<json op>' --note "why" --defer              # old path: next hourly run
node scripts/ads/ytads/manual.js run [<id>]                                        # send pending row(s) now
```

A row sent by the API is claimed `pending → api` first, so the hourly script (which only takes `pending`) can
never send it twice. It ends `done` / `failed` with `result.channel = "api"` and a `manual` / `error` event in
`ytads_events`, same as a script-run edit.

From code: `const ads = require('./scripts/ads/api/client.js')` → `ads.search(gaql)`, `ads.mutate(ops, {dryRun,
note})`, `ads.policyReport(campaignId)`, resource-name helpers `ads.rn.*`, Demand Gen helpers `ads.dg.*`.
Operations are the REST `MutateOperation` JSON — the same shape `AdsApp.mutate` took, so script-era ops port as is.

**Ledger:** every `mutate` (dry run, applied or failed) writes a row to `ytads_events` with `campaign_key = 'api'`,
event `api:validate` / `api:mutate` / `api:error`, and the operations plus Google's response verbatim in `detail`.

**Guard rails built into `mutate`** (refused before any request is sent):
- enabling a campaign (`status: ENABLED`) — spends money, only on Dan's say-so (`ADS_ALLOW_ENABLE_CAMPAIGN=1`);
- Demand Gen `maximizeConversions.targetCpaMicros` — use `dg.targetCpa(dollars)`;
- campaign-level location/language on a Demand Gen campaign — they go on the ad group (`dg.adGroupLocation/Language`);
- loose gender / age / custom-segment criteria on a new Demand Gen ad group — audience grouped, use an `Audience`
  + `dg.adGroupAudience`;
- conversion-goal batches that write a `biddable:false` before the `biddable:true` one — use `dg.conversionGoals`;
- any `update` without an `updateMask`.

## Measured answers (2026-09-10)

| question | answer |
|---|---|
| Developer-token header needed? | **No.** Access is per Cloud project now (Explorer level on `abs-by-ai`); calls with only the OAuth token succeed. The client sends `developer-token` only if `GOOGLE_ADS_DEVELOPER_TOKEN` is ever set. |
| login-customer-id | **The account itself (3427170837), not the MCC.** 342-717-0837 is NOT under the Daniel Rose Marketing MCC 324-458-6445: its `customer_manager_link` is empty and a call with the MCC as login returns `USER_PERMISSION_DENIED`. `danroseconsulting@gmail.com` has direct access. |
| API version | **v25** (v25.1, 2026-08-19). Override with `GOOGLE_ADS_API_VERSION`. |
| Access level | Explorer: 2,880 production operations/day, campaign management + reporting. Nothing so far has been refused for access level; if something is, that is the trigger for the Basic application (Dan's form, company details). |
| Writes | Proven: a label created, read back and removed (events 151–153). Validate-only proven on an ad pause. |

## Traps

- **v25: `ad_group_ad_asset_view.policy_summary` must be selected whole** — its sub-fields
  (`.approval_status`, `.review_status`, `.policy_topic_entries`) return `UNRECOGNIZED_FIELD`.
  `ad_group_ad.policy_summary.*` sub-fields still work.
- **`change_event` needs a bounded date range** (both `>=` and `<=` on `change_event.change_date_time`, within 30
  days) plus a `LIMIT`, or it returns `CHANGE_DATE_RANGE_INFINITE`. It records who changed what and from which
  client (`GOOGLE_ADS_WEB_CLIENT`, `GOOGLE_ADS_SCRIPTS`, API).
- The Ads Script trap "constant-id criteria need a derived resourceName" belonged to the Scripts wrapper (it
  stamped temporary names). On REST, creates omit `resourceName`; the derived names (`ads.rn.adGroupCriterion`)
  are for updates and removes.
- The Demand Gen rules themselves (audience grouped, ad-group locations, plain `targetCpa`, goal ordering) are
  Google's and apply to REST too — see `Docs/DGEN_CONVERSION_CAMPAIGN.md`.

## Credentials and re-minting the token

- `GOOGLE_ADS_REFRESH_TOKEN` (scope `https://www.googleapis.com/auth/adwords`) lives in `~/.absbyai-secrets.env`
  and on Railway service `abs-by-ai`. Minted 2026-09-10. Never paste it anywhere; the repo is public.
- OAuth client: `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`, Cloud project `abs-by-ai` (768453214640) — the
  project that holds the Explorer grant. Its only registered redirect URI is the OAuth Playground.
- To re-mint: open
  `https://accounts.google.com/o/oauth2/v2/auth?client_id=<GOOGLE_CLIENT_ID>&redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fadwords&access_type=offline&prompt=consent&login_hint=danroseconsulting%40gmail.com`
  in Dan's Chrome; Dan confirms with his passkey and clicks Allow (the only hands-on step). The tab lands on the
  Playground with `code=` in the address bar — read it from the tab and exchange it at
  `https://oauth2.googleapis.com/token` (`grant_type=authorization_code`, same redirect_uri) at once. Store with
  `railway variable set GOOGLE_ADS_REFRESH_TOKEN --stdin --skip-deploys --service abs-by-ai` run **from the repo
  folder** (elsewhere the CLI says "No linked project").
- Unlike the Playground's own client, our client's refresh tokens are not auto-revoked after 24 h. If the OAuth
  consent screen is ever set back to "Testing", Google expires refresh tokens after 7 days — re-mint then.

## Who uses it

- `scripts/ads/ytads/manual.js` — Dan's edits, immediate.
- `scripts/ads/ads-digest.js` — the morning brief's Google spend section (blind until 2026-09-10).
- Future one-off builds: write the ops as JSON, `--dry-run` them, then apply — no Scripts editor.
- Later, optional: move the engagement-champion engine off the hourly Ads Script onto a Railway cron that calls
  this client — only after the client has run for a few weeks.

## GA4 — property "Abs By AI", linked to the Ads account (2026-09-11)

Built for the Google Ads rep meeting of 2026-09-11 (`Handoffs/handoff-20260911-google-ads-rep-ga4-start-urls-mcc.md`).
GA4 is **additive to PostHog, not a replacement** — PostHog remains product analytics.

| | |
|---|---|
| Analytics account | **SixPackAbs.com `145219380`** — the only GA account on `danroseconsulting@gmail.com`. ⚠ The absbyai property sits inside it because creating a *new* GA account forces a Google Analytics Terms-of-Service acceptance, which Claude is not permitted to click on Dan's behalf. Creating a property inside an existing account raises no such prompt. Renaming the account, or moving the property to its own account, is a later cleanup and changes nothing technical. |
| Property | **Abs By AI `553864929`** — `America/Chicago`, USD, industry Beauty & Fitness, objectives Generate leads + Drive sales. |
| Web data stream | **absbyai.com `15763007741`** → `https://absbyai.com`, enhanced measurement ON. |
| **Measurement ID** | **`G-1M1SY7GGKF`** |
| Ads link | `342-717-0837` "Abs by AI" — Completed, Personalized Advertising **Enabled**, auto-tagging left on the recommended setting (it was already on account-wide, so this was a no-op). **No conversion / key-event import** — see below. |

### How the tag is installed — one loader, two destinations

`public/*.html` already carried `gtag/js?id=AW-18361229851`. GA4 rides that same loader: each of the **11 pages**
that carry it now has a `gtag('config', 'G-1M1SY7GGKF', { send_page_view: true })` immediately after the Ads
config. **Never add a second `gtag/js` loader script.**

⚠ **Do NOT accept Google's "Use the Google tag found on your website" option** in the GA4 stream setup. It warns —
in its own words — that it will *overwrite existing settings* on the `AW-18361229851` tag, and that tag carries
`allow_enhanced_conversions` plus the live enhanced-conversions setup. Choose **Install manually**, take the
measurement ID, and add the config line in code.

### `fireAdVirtualPageview()` now names GA4 as a second destination

`index.html`'s virtual pageview was `send_to: AD_CONVERSION_ID` — Ads only. Left alone, **GA4 would have recorded
exactly one `page_view` per session**: the app changes screens without touching browser history, so GA4's
enhanced measurement sees nothing after the initial load. It is now `send_to: [AD_CONVERSION_ID, GA4_MEASUREMENT_ID]`,
so GA4 reports each funnel stage under its synthetic `/vp/…` address, same as Ads. The `DEMO` guard still suppresses
review visits.

### Conversions: GA4 imports NOTHING, on purpose

The gtag conversion actions (Free Generation Started, Trial Signup, Purchase) stay the **single source of truth and
stay primary**. A GA4 key-event import would double-count against them. If the rep asks for GA4 key events in Ads,
mark the event in GA4 and import it as **secondary / observation-only**, never primary.

### Verified live 2026-09-11

- `G-1M1SY7GGKF` present on all 11 live pages (`/`, `/start`, privacy, faq, how-it-works, contact, terms, about,
  refunds, disclaimer, sources).
- Real hit observed on `/` and `/start`: `google-analytics.com/g/collect?v=2&tid=G-1M1SY7GGKF … &en=page_view`.
- GA4 Realtime showed the visits within a minute (4 active users, 6 `page_view`, page titles "Abs by AI" /
  "See Yourself With Abs").
- ⚠ **Native retest**: the iOS/Android wrappers load the same page, so GA4 counts app sessions as web. Accepted.
- ⚠ The Ads-side confirmation of the link could not be read — the Ads UI wedged in its known
  refuse-to-render state (memory `google-ads-ui-automation`), and Google says the link takes up to 24 h to show
  data there anyway. Check Tools → Data manager after 2026-09-12.

## SixPackAbs.com client account inside the MCC — BLOCKED on a CAPTCHA (2026-09-11)

Task 3 of the same handoff. **Not created.**

- The API cannot do it: `CustomerService.createCustomerClient` on `customers/3244586445` returns
  `DEVELOPER_TOKEN_NOT_APPROVED` — *"This method is not allowed for use with explorer access."* Account creation
  is one of the methods our Explorer-level access does not cover, unlike everything else in this client.
- The UI path (MCC `324-458-6445` → Accounts → **+** → *Create new account*) immediately shows a reCAPTCHA
  **"Let's make sure you're human"** gate. Claude is not permitted to complete CAPTCHAs, so **Dan has to click
  that one checkbox**, then finish the wizard: name **SixPackAbs.com**, `America/Chicago`, USD, **skip billing**,
  and take the "create an account without a campaign" / Expert Mode link so no campaign is made.
