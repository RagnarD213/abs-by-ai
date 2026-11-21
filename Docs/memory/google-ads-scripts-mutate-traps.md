---
name: google-ads-scripts-mutate-traps
description: Building Google Ads campaigns through an Ads Script — the mutate/mutateAll traps measured 2026-09-10; PREFER scripts/ads/api/client.js (API live since 09-10)
metadata:
  type: reference
---

**Prefer the API now:** since 2026-09-10 `scripts/ads/api/client.js` does search / atomic mutate / validate-only dry run with these Demand Gen traps linted in (`Docs/GOOGLE_ADS_API.md`). Ads Scripts are the fallback only. On REST, criteria creates simply omit `resourceName` — the derived-name trap below was the Scripts wrapper's.

Measured 2026-09-10 (`scripts/ads/oneoff/build-video-campaign.js`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`):

- `AdsApp.mutateAll(ops, {partialFailure:false})` with temporary ids (`customers/C/campaigns/-2`) builds budget → campaign → video assets → ad groups → ads atomically, and **Preview is a real Google-validated dry run** of it.
- Any create WITHOUT a `resourceName` gets a temporary one stamped by the wrapper; a criterion whose id is a constant (country 2840, language 1000, an audience) is then refused ("field's contents don't match another field… At create.resourceName"). Send those one at a time, `AdsApp.mutate(op, {partialFailure:false})`, with the exact derived name `…/adGroupCriteria/<ag>~2840`.
- Demand Gen: `maximizeConversions.targetCpaMicros` refused → plain `targetCpa`. API-made DG ad groups are always **audience grouped** → demographics + custom segments go in an `Audience` resource attached as an `audience` criterion. Location/language live on the AD GROUP (campaign-level returns "error code is not in this version").
- Campaign conversion goals: `{partialFailure:false}` and write the wanted goal `biddable:true` first.
- Per-line policy verdicts: `ad_group_ad_asset_view.policy_summary` + `asset.text_asset.text`; swap a line with `adOperation.update` + mask `demand_gen_video_responsive_ad.descriptions` (re-triggers review, id kept).
- Editor: clipboard paste (`pbcopy` + ⌘V) only takes once the page has settled (sometimes after a reload); big `setValue` injections get blocked as code injection, small targeted `cm.setValue(v.replace(...))` edits are fine. Click Save/Run/Preview via `material-button` text from JS; the "Run without preview" dialog button needs a coordinate click (≈846,414 at 1568-wide). Preview of an unsaved editor runs the SAVED copy. Results via `POST /api/ytads/dump` → `ytads_events`.

Related: [[google-ads-api-client]], [[google-ads-ui-automation]], [[ad-retry-rule-and-no-trick]].
