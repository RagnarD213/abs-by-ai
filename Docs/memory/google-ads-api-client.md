---
name: google-ads-api-client
description: Google Ads API is LIVE (2026-09-10) — scripts/ads/api/client.js; no developer token; login-customer-id = the account itself, NOT the MCC
metadata:
  type: reference
---

Since 2026-09-10 read and change Google Ads account 342-717-0837 with `scripts/ads/api/client.js` (search, atomic
mutate, `--dry-run` = validateOnly, every mutate logged to `ytads_events` with `campaign_key='api'`, `policy <campaignId>`
report). Dan's queued edits (`scripts/ads/ytads/manual.js`) now execute immediately through it. Full doc:
`Docs/GOOGLE_ADS_API.md`.

- Token `GOOGLE_ADS_REFRESH_TOKEN` (adwords scope) in `~/.absbyai-secrets.env` + Railway. **No developer-token header
  needed** (Cloud-project Explorer access on `abs-by-ai`).
- **login-customer-id = 3427170837 itself.** The account is not linked under the Daniel Rose Marketing MCC
  (324-458-6445) — using the MCC returns USER_PERMISSION_DENIED. Older docs/handoffs that say "through the MCC" are wrong.
- API v25. Traps: `ad_group_ad_asset_view.policy_summary` must be selected whole; `change_event` needs both date bounds.
- Re-mint: consent URL with the Playground redirect opened in Dan's Chrome, he passkeys + Allows, read `code=` from the
  tab and exchange by fetch at once; `railway variable set … --stdin` must run from the repo folder.
- The client refuses to enable a campaign unless `ADS_ALLOW_ENABLE_CAMPAIGN=1` (Dan's say-so only).

**How to apply:** any Google Ads read or change → this client first; never the Scripts editor unless the API refuses.
Related: [[google-ads-scripts-mutate-traps]], [[google-ads-ui-automation]], [[ad-copy-no-unbelievable-claims]].
