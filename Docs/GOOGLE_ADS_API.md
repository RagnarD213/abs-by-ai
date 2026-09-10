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
