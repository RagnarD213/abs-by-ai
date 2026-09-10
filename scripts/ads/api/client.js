#!/usr/bin/env node
/**
 * Google Ads API client — direct REST calls against account 342-717-0837 (direct user
 * access; the account is NOT under the Daniel Rose Marketing MCC). Replaces the paste-a-script-into-the-Ads-editor channel
 * (built 2026-09-10; setup + measured answers in Docs/GOOGLE_ADS_API.md).
 *
 *   node scripts/ads/api/client.js whoami
 *   node scripts/ads/api/client.js search "SELECT campaign.id, campaign.name FROM campaign" [--json]
 *   node scripts/ads/api/client.js mutate ops.json [--dry-run] [--note "why"]
 *   node scripts/ads/api/client.js policy <campaignId>
 *
 * From code:
 *   const ads = require('./scripts/ads/api/client.js');
 *   const rows = await ads.search('SELECT …');
 *   await ads.mutate([{ campaignOperation: { update: {…}, updateMask: 'status' } }], { note: 'why', dryRun: true });
 *
 * Operations are the same JSON the Ads Script channel passed to AdsApp.mutate (the REST
 * MutateOperation shape), so queued edits and the one-off builders port unchanged.
 *
 * Credentials (env first, then ~/.absbyai-secrets.env): GOOGLE_CLIENT_ID,
 * GOOGLE_CLIENT_SECRET, GOOGLE_ADS_REFRESH_TOKEN (scope adwords). No developer token is needed (measured
 * 2026-09-10: Cloud-project Explorer access, no developer-token header); one is sent only if
 * GOOGLE_ADS_DEVELOPER_TOKEN is set. DATABASE_PUBLIC_URL / DATABASE_URL for the ledger.
 * No dependency beyond `pg` (already in package.json) and Node's fetch.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');

const API_VERSION = process.env.GOOGLE_ADS_API_VERSION || 'v25';   // current 2026-09-10 (v25.1, 2026-08-19)
const CID = '3427170837';            // Abs by AI, 342-717-0837
// Measured 2026-09-10: 342-717-0837 is NOT linked under the Daniel Rose Marketing MCC
// (324-458-6445) — its customer_manager_link is empty and a call with the MCC as
// login-customer-id returns USER_PERMISSION_DENIED. danroseconsulting@gmail.com has
// DIRECT access, so the login customer is the account being called.
const LOGIN_CID = process.env.GOOGLE_ADS_LOGIN_CUSTOMER_ID || null;   // null → the target cid
const BASE = `https://googleads.googleapis.com/${API_VERSION}`;

function secrets() {
  const out = { ...process.env };
  try {
    for (const line of fs.readFileSync(path.join(os.homedir(), '.absbyai-secrets.env'), 'utf8').split('\n')) {
      const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
      if (m && !out[m[1]]) out[m[1]] = m[2].replace(/^"|"$/g, '');
    }
  } catch (e) { /* on Railway the env is enough */ }
  return out;
}
const S = secrets();

// ---------------------------------------------------------------- auth + transport
let cached = null;
async function accessToken() {
  if (cached && cached.exp > Date.now() + 60e3) return cached.token;
  if (!S.GOOGLE_ADS_REFRESH_TOKEN) throw new Error('GOOGLE_ADS_REFRESH_TOKEN missing (mint recipe: Docs/GOOGLE_ADS_API.md)');
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: S.GOOGLE_CLIENT_ID, client_secret: S.GOOGLE_CLIENT_SECRET,
                                refresh_token: S.GOOGLE_ADS_REFRESH_TOKEN, grant_type: 'refresh_token' }),
  });
  const j = await r.json();
  if (!j.access_token) throw new Error(`OAuth refresh failed: ${j.error_description || j.error || r.status}`);
  cached = { token: j.access_token, exp: Date.now() + (j.expires_in || 3600) * 1000 };
  return cached.token;
}

async function headers(cid) {
  const h = { Authorization: `Bearer ${await accessToken()}`, 'Content-Type': 'application/json' };
  if (LOGIN_CID || cid) h['login-customer-id'] = LOGIN_CID || cid;
  if (S.GOOGLE_ADS_DEVELOPER_TOKEN) h['developer-token'] = S.GOOGLE_ADS_DEVELOPER_TOKEN;
  return h;
}

class AdsApiError extends Error {
  constructor(status, body) {
    super(summarizeError(body) || `HTTP ${status}`);
    this.status = status; this.body = body;
  }
}

// Google's failure shape: { error: { code, message, status, details: [{ errors: [{ errorCode, message, location }] }] } }.
function summarizeError(body) {
  const e = body && (body.error || (Array.isArray(body) && body[0] && body[0].error));
  if (!e) return null;
  const lines = [];
  for (const d of e.details || []) for (const x of d.errors || []) {
    const code = x.errorCode ? Object.entries(x.errorCode).map(([k, v]) => `${k}=${v}`).join(',') : '';
    const at = x.location && x.location.fieldPathElements ? ' at ' + x.location.fieldPathElements.map(p => p.fieldName + (p.index != null ? `[${p.index}]` : '')).join('.') : '';
    lines.push(`${code} ${x.message || ''}${at}`.trim());
  }
  return lines.length ? lines.join(' | ') : `${e.status || e.code}: ${e.message}`;
}

// POST with retry on 429 / 5xx (exponential backoff, honours Retry-After). 4xx other
// than 429 are the request's fault and are thrown at once.
async function post(url, body, { tries = 5, cid = CID } = {}) {
  for (let i = 0; ; i++) {
    const r = await fetch(url, { method: 'POST', headers: await headers(cid), body: JSON.stringify(body) });
    const text = await r.text();
    let j; try { j = text ? JSON.parse(text) : {}; } catch (e) { j = { raw: text }; }
    if (r.ok) return j;
    if ((r.status === 429 || r.status >= 500) && i < tries - 1) {
      const wait = Number(r.headers.get('retry-after')) * 1000 || Math.min(30e3, 1000 * 2 ** i);
      await new Promise(res => setTimeout(res, wait));
      continue;
    }
    throw new AdsApiError(r.status, j);
  }
}

// ---------------------------------------------------------------- read
// All pages of a GAQL query. (search's page size is fixed by Google since v17.)
async function search(query, { cid = CID } = {}) {
  const rows = [];
  let pageToken;
  do {
    const j = await post(`${BASE}/customers/${cid}/googleAds:search`, pageToken ? { query, pageToken } : { query }, { cid });
    rows.push(...(j.results || []));
    pageToken = j.nextPageToken;
  } while (pageToken);
  return rows;
}

async function whoami() {
  const h = await headers(null); delete h['login-customer-id'];
  const r = await fetch(`${BASE}/customers:listAccessibleCustomers`, { headers: h });
  const j = await r.json();
  if (!r.ok) throw new AdsApiError(r.status, j);
  return j.resourceNames || [];
}

// ---------------------------------------------------------------- write
// Atomic by default: Google applies every operation or none. `dryRun` sends
// validateOnly:true — Google runs the full validation (policy, field rules, the Demand Gen
// traps) and changes nothing; that is the preview the Ads Script editor used to give.
// Every call, dry or live, OK or failed, is written to ytads_events.
async function mutate(ops, { cid = CID, dryRun = false, partialFailure = false, note = null, reason = 'api', log = true } = {}) {
  if (!Array.isArray(ops) || !ops.length) throw new Error('mutate needs a non-empty array of operations');
  const problems = lintOps(ops);
  if (problems.length) throw new Error('refused before sending (known Google Ads traps):\n  - ' + problems.join('\n  - '));
  const body = { mutateOperations: ops, partialFailure, validateOnly: !!dryRun };
  let response, error;
  try { response = await post(`${BASE}/customers/${cid}/googleAds:mutate`, body, { cid }); }
  catch (e) { error = e; }
  if (log) await ledger(dryRun ? 'api:validate' : (error ? 'api:error' : 'api:mutate'),
                        { reason, note, cid, ops, response: response || null, error: error ? (error.body || String(error.message)) : null });
  if (error) throw error;
  return { ok: true, dryRun: !!dryRun, results: (response.mutateOperationResponses || []).map(resultName), response };
}
const mutateOne = (op, opts) => mutate([op], opts);

// { campaignResult: { resourceName } } → 'customers/…/campaigns/…'
function resultName(r) { const v = Object.values(r || {})[0]; return (v && v.resourceName) || null; }

// ---------------------------------------------------------------- ledger
let pool = null;
async function ledger(event, detail) {
  const url = S.DATABASE_PUBLIC_URL || S.DATABASE_URL;
  if (!url) { console.error('[ads-api] no DATABASE_URL — mutate NOT logged to ytads_events'); return; }
  try {
    if (!pool) {
      const { Pool } = require('pg');
      pool = new Pool({ connectionString: url, ssl: /railway\.internal/.test(url) ? false : { rejectUnauthorized: false } });
    }
    await pool.query('INSERT INTO ytads_events (video_id, campaign_key, ad_id, event, detail) VALUES (NULL, $1, $2, $3, $4)',
                     ['api', detail.adId || null, event, JSON.stringify(detail)]);
  } catch (e) { console.error('[ads-api] ledger write failed:', e.message); }
}
async function close() { if (pool) { await pool.end(); pool = null; } }

// ---------------------------------------------------------------- resource names
// Criteria whose id is a Google constant (country 2840, language 1000, an Audience) have a
// DERIVED resource name. On REST, creates simply omit resourceName (the Ads Script wrapper
// stamped a temporary one, which Google refused — that trap was the wrapper's, not the API's);
// updates and removes need the derived name built here.
const rn = {
  campaign: (id, cid = CID) => `customers/${cid}/campaigns/${id}`,
  budget: (id, cid = CID) => `customers/${cid}/campaignBudgets/${id}`,
  adGroup: (id, cid = CID) => `customers/${cid}/adGroups/${id}`,
  ad: (id, cid = CID) => `customers/${cid}/ads/${id}`,
  adGroupAd: (ag, ad, cid = CID) => `customers/${cid}/adGroupAds/${ag}~${ad}`,
  adGroupCriterion: (ag, crit, cid = CID) => `customers/${cid}/adGroupCriteria/${ag}~${crit}`,
  campaignConversionGoal: (camp, category, source, cid = CID) => `customers/${cid}/campaignConversionGoals/${camp}~${category}~${source}`,
  audience: (id, cid = CID) => `customers/${cid}/audiences/${id}`,
  geo: (id) => `geoTargetConstants/${id}`,
  language: (id) => `languageConstants/${id}`,
  temp: (kind, n, cid = CID) => `customers/${cid}/${kind}/-${Math.abs(n)}`,   // temp ids for one atomic batch
};
const GEO = { US: 2840, CA: 2124 };
const LANG = { EN: 1000 };

// ---------------------------------------------------------------- Demand Gen helpers
// Measured building campaign 24243839443 (Docs/DGEN_CONVERSION_CAMPAIGN.md).
const dg = {
  // Demand Gen refuses maximizeConversions.targetCpaMicros; the plain targetCpa strategy works.
  targetCpa: (dollars) => ({ targetCpa: { targetCpaMicros: String(Math.round(dollars * 1e6)) } }),
  // Location + language live on the AD GROUP for Demand Gen (campaign-level is refused).
  adGroupLocation: (ag, geoId, cid = CID) => ({ adGroupCriterionOperation: { create: { adGroup: rn.adGroup(ag, cid), location: { geoTargetConstant: rn.geo(geoId) } } } }),
  adGroupLanguage: (ag, langId, cid = CID) => ({ adGroupCriterionOperation: { create: { adGroup: rn.adGroup(ag, cid), language: { languageConstant: rn.language(langId) } } } }),
  // API-made DG ad groups are audience grouped: age / gender / custom segments go in ONE
  // Audience resource, attached here. Loose gender/age/customAudience criteria are refused.
  adGroupAudience: (ag, audienceId, cid = CID) => ({ adGroupCriterionOperation: { create: { adGroup: rn.adGroup(ag, cid), audience: { audience: rn.audience(audienceId, cid) } } } }),
  // Campaign-specific conversion goals: the wanted goal biddable:true FIRST, then the rest
  // false, in one atomic request. Writing only the false ones fails with "campaign override
  // goals but has no goals configured".
  conversionGoals: (campaignId, wanted, unwanted, cid = CID) => [...wanted.map(g => [g, true]), ...unwanted.map(g => [g, false])]
    .map(([g, biddable]) => ({ campaignConversionGoalOperation: { update: { resourceName: rn.campaignConversionGoal(campaignId, g.category, g.origin, cid), biddable }, updateMask: 'biddable' } })),
};

// Refuse the operations we already know Google rejects, before spending a round trip.
function lintOps(ops) {
  const out = [];
  const dgCampaigns = new Set();
  ops.forEach((op, i) => {
    const c = op.campaignOperation && op.campaignOperation.create;
    if (c && c.advertisingChannelType === 'DEMAND_GEN') {
      if (c.resourceName) dgCampaigns.add(c.resourceName);
      if (c.maximizeConversions && c.maximizeConversions.targetCpaMicros)
        out.push(`op ${i}: Demand Gen refuses maximizeConversions.targetCpaMicros — use dg.targetCpa(dollars)`);
    }
    const cc = op.campaignCriterionOperation && op.campaignCriterionOperation.create;
    if (cc && (cc.location || cc.language) && dgCampaigns.has(cc.campaign))
      out.push(`op ${i}: Demand Gen location/language belong on the ad group — use dg.adGroupLocation / dg.adGroupLanguage`);
    const ac = op.adGroupCriterionOperation && op.adGroupCriterionOperation.create;
    if (ac && (ac.gender || ac.ageRange || ac.customAudience || ac.userInterest) && ac.adGroup && /\/adGroups\/-/.test(ac.adGroup))
      out.push(`op ${i}: a new Demand Gen ad group is audience grouped — put demographics/segments in an Audience and attach it with dg.adGroupAudience`);
    for (const k of ['campaignOperation', 'adGroupOperation', 'adGroupAdOperation', 'adOperation', 'campaignBudgetOperation', 'assetOperation'])
      if (op[k] && op[k].update && !op[k].updateMask) out.push(`op ${i}: ${k}.update without updateMask would be refused`);
    if (op.campaignOperation && op.campaignOperation.update && op.campaignOperation.update.status === 'ENABLED' && !process.env.ADS_ALLOW_ENABLE_CAMPAIGN)
      out.push(`op ${i}: enabling a campaign spends money — only on Dan's say-so; re-run with ADS_ALLOW_ENABLE_CAMPAIGN=1`);
  });
  // Conversion goals: a batch that sets biddable:true must set it before any false.
  const goals = ops.map(o => o.campaignConversionGoalOperation && o.campaignConversionGoalOperation.update).filter(Boolean);
  if (goals.length && goals.some(g => g.biddable === true) && goals.findIndex(g => g.biddable === true) > goals.findIndex(g => g.biddable === false))
    out.push('campaign conversion goals: write the biddable:true goal FIRST (use dg.conversionGoals)');
  return out;
}

// ---------------------------------------------------------------- reports
// Per-line policy verdicts on every ad in a campaign (v25 trap: the asset view's policy_summary
// must be selected WHOLE — its sub-fields are UNRECOGNIZED_FIELD). The Demand Gen ads table shows one
// status per ad, this shows which headline / description Google limited and why.
async function policyReport(campaignId) {
  const ads = await search(`
    SELECT ad_group.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status,
           ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status,
           ad_group_ad.policy_summary.policy_topic_entries
    FROM ad_group_ad WHERE campaign.id = ${Number(campaignId)} AND ad_group_ad.status != 'REMOVED'`);
  const lines = await search(`
    SELECT ad_group_ad.ad.id, ad_group_ad_asset_view.field_type, ad_group_ad_asset_view.enabled,
           ad_group_ad_asset_view.policy_summary, asset.id, asset.text_asset.text, asset.youtube_video_asset.youtube_video_id
    FROM ad_group_ad_asset_view WHERE campaign.id = ${Number(campaignId)} AND ad_group_ad_asset_view.enabled = TRUE`);
  const topics = (p) => ((p && p.policyTopicEntries) || []).map(t => `${t.topic}${t.type ? ' (' + t.type + ')' : ''}`);
  return ads.map(a => ({
    adGroup: a.adGroup.name, adId: a.adGroupAd.ad.id, name: a.adGroupAd.ad.name, status: a.adGroupAd.status,
    approval: a.adGroupAd.policySummary.approvalStatus, review: a.adGroupAd.policySummary.reviewStatus,
    topics: topics(a.adGroupAd.policySummary),
    lines: lines.filter(l => l.adGroupAd.ad.id === a.adGroupAd.ad.id).map(l => ({
      field: l.adGroupAdAssetView.fieldType, assetId: l.asset.id,
      text: (l.asset.textAsset && l.asset.textAsset.text) || (l.asset.youtubeVideoAsset && 'video ' + l.asset.youtubeVideoAsset.youtubeVideoId) || null,
      approval: l.adGroupAdAssetView.policySummary && l.adGroupAdAssetView.policySummary.approvalStatus,
      review: l.adGroupAdAssetView.policySummary && l.adGroupAdAssetView.policySummary.reviewStatus,
      topics: topics(l.adGroupAdAssetView.policySummary),
    })),
  }));
}

module.exports = { API_VERSION, CID, LOGIN_CID, search, whoami, mutate, mutateOne, policyReport, lintOps, rn, dg, GEO, LANG, ledger, close, AdsApiError, summarizeError };

// ---------------------------------------------------------------- CLI
if (require.main === module) {
  const argv = process.argv.slice(2);
  const flag = (f) => argv.includes(f);
  const opt = (f) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : null; };
  (async () => {
    const [cmd, arg] = argv;
    if (cmd === 'whoami') {
      console.log((await whoami()).join('\n'));
    } else if (cmd === 'search') {
      const rows = await search(arg);
      console.log(flag('--json') ? JSON.stringify(rows, null, 2) : rows.map(r => JSON.stringify(r)).join('\n'));
      console.error(`${rows.length} row(s)`);
    } else if (cmd === 'mutate') {
      const ops = JSON.parse(fs.readFileSync(arg, 'utf8'));
      const r = await mutate(Array.isArray(ops) ? ops : [ops], { dryRun: flag('--dry-run'), note: opt('--note'), reason: 'api:cli' });
      console.log(r.dryRun ? `VALID (dry run, nothing changed): ${ops.length} operation(s)` : `APPLIED ${r.results.length}:\n${r.results.join('\n')}`);
    } else if (cmd === 'policy') {
      for (const a of await policyReport(arg)) {
        console.log(`\n${a.adGroup} | ad ${a.adId} | ${a.status} | ${a.approval} / ${a.review}${a.topics.length ? ' | ' + a.topics.join(', ') : ''}`);
        for (const l of a.lines) console.log(`   ${String(l.field).padEnd(14)} ${String(l.approval || '-').padEnd(18)} ${String(l.review || '').padEnd(16)} ${l.topics.join(', ').padEnd(20)} ${l.text}`);
      }
    } else {
      console.log('usage: whoami | search "<GAQL>" [--json] | mutate ops.json [--dry-run] [--note why] | policy <campaignId>');
      process.exitCode = 2;
    }
  })().catch(e => { console.error(e.message); if (e.body && process.env.ADS_DEBUG) console.error(JSON.stringify(e.body, null, 2)); process.exitCode = 1; })
      .finally(close);
}
