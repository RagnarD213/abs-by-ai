#!/usr/bin/env node
/* eslint-disable no-console */
//
// ADS DIGEST — daily Meta + Google Ads spend brief with anomaly and winning-ad
// detection. Writes `brief-ads.json` at the repo root; the 6:30am morning-brief
// job runs this first and renders the result as one section.
//
// WHY THIS EXISTS (2026-08-26 paid audit + 2026-08-31 pull, both in
// AI_COORDINATION.md). Three failures, none of which a human noticed for days:
//   1. BOTH Meta campaigns were toggled OFF. IG GEO spent $13.26 early in the
//      window and then simply stopped. Nobody saw it until a manual pull six
//      days later. That is why SPEND_STOP below is a first-class anomaly and
//      not an afterthought — a campaign going quiet is the failure mode that
//      actually happened here, and a naive "alert on spikes" digest is blind
//      to it.
//   2. Google search ran $63 with ZERO conversions, twice.
//   3. Three unpublished Meta draft edits sat pending, unreviewed.
// Everything this script detects is one of those three shapes: money moving
// when it shouldn't, money buying nothing, or a change nobody published.
//
// RUN:  node scripts/ads/ads-digest.js [--day YYYY-MM-DD] [--out PATH] [--print]
// Exits 0 even when a platform is unreachable — a missing credential is DATA
// (rendered as a one-line "the digest is blind" row), not a crash. The morning
// brief must never fail because an ad token expired.
//
// CREDENTIALS: read from the environment, falling back to ~/.absbyai-secrets.env.
// Neither platform is readable as of 2026-09-02 — see Docs/ADS_DIGEST.md for the
// one-time setup. The script says exactly which credential is missing and how to
// get it, in the output, every run, until it is fixed.

'use strict';

const fs   = require('fs');
const os   = require('os');
const path = require('path');

// ============================================================
// CONFIG
// ============================================================

const REPO_ROOT   = path.resolve(__dirname, '..', '..');
const SECRETS_ENV = path.join(os.homedir(), '.absbyai-secrets.env');
const OUT_DEFAULT = path.join(REPO_ROOT, 'brief-ads.json');

// Account identifiers. Both already appear in the (public) coordination file, so
// defaulting them here adds no exposure and removes a setup step.
const META_ACCOUNT_DEFAULT   = 'act_2143998876461525';
const GOOGLE_CUSTOMER_DEFAULT = '3427170837';   // 342-717-0837, "Abs by AI"
const GOOGLE_LOGIN_CUSTOMER   = '3244586445';   // 324-458-6445, Daniel Rose Marketing MCC
const META_API = 'https://graph.facebook.com/v21.0';

// ── The ~2x conversion inflation ────────────────────────────
// MEASURED 2026-08-26, not assumed: Demand Gen campaign 24122099676 reported
// 1,553 "conversions" on $136.75 while its own ad-group view reported 792 EARNED
// SUBSCRIBERS over the same window. 1553 / 792 = 1.96. So Google's conversions
// column runs ~2x the real subscriber count on this account, and cost/conv
// understates cost-per-subscriber by the same factor.
//
// This is applied ONLY to derive an explicitly-labelled estimate. The raw number
// is always carried alongside it. Silently deflating a platform's own metric and
// presenting the result as fact is how a dashboard starts lying; the estimate is
// named `est*` everywhere and the ratio travels with it in `basis`.
const GOOGLE_CONVERSION_INFLATION = 1.96;
const GOOGLE_INFLATION_BASIS =
  'measured 2026-08-26: 1,553 reported conversions vs 792 earned subscribers on campaign 24122099676';

// ── Detection thresholds ────────────────────────────────────
// Every one of these exists to keep a $2 rounding difference off Dan's page.
// At this account's volume ($10-15/day budgets) noise is the enemy, not misses.
const MIN_SPEND_TO_JUDGE   = 5.00; // below this a day's numbers mean nothing
const SPEND_SPIKE_RATIO    = 2.00; // yesterday vs its own 7-day mean
const SPEND_SPIKE_MIN_DELTA = 10.00; // ...and at least this many dollars of it
const SPEND_STOP_RATIO     = 0.10; // fell to <10% of a baseline that was real
const SPEND_STOP_MIN_BASE  = 3.00; // ...where the baseline was ≥$3/day
const CPA_DEGRADE_RATIO    = 1.50; // cost/result vs its own 7-day mean
const CPA_MIN_BASE_RESULTS = 5;    // ...with enough baseline results to mean it
const ZERO_RESULT_SPEND    = 15.00; // spent this much over the window, got nothing
const WINNER_RATIO         = 0.70; // cost/result ≤70% of the platform mean
const WINNER_MIN_RESULTS   = 8;    // ...over the window, so it is not one lucky click
const BASELINE_DAYS        = 7;

// Preference order for "what counts as a result" on Meta. Their live campaigns
// optimise for ThruPlays, but the order is deliberately purchase-first so that
// the day a conversion campaign runs, the digest grades it on the sale and not
// on a video view. First action type present wins, per campaign/ad.
const META_RESULT_PRIORITY = [
  { key: 'offsite_conversion.fb_pixel_purchase', label: 'purchase' },
  { key: 'purchase',                             label: 'purchase' },
  { key: 'offsite_conversion.fb_pixel_lead',     label: 'lead' },
  { key: 'lead',                                 label: 'lead' },
  { key: 'onsite_conversion.lead_grouped',       label: 'lead' },
  { key: 'link_click',                           label: 'link click' },
  { key: 'video_view',                           label: 'video view' },
  { key: 'post_engagement',                      label: 'engagement' },
];

// ============================================================
// SMALL UTILITIES
// ============================================================

const round2 = (n) => Math.round((Number(n) || 0) * 100) / 100;
const num    = (v) => { const n = Number(v); return Number.isFinite(n) ? n : 0; };
const usd    = (n) => `$${round2(n).toFixed(2)}`;
const pct    = (n) => `${n >= 0 ? '+' : ''}${Math.round(n * 100)}%`;

function ymd(d) { return d.toISOString().slice(0, 10); }
function addDays(dateStr, delta) {
  const d = new Date(`${dateStr}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + delta);
  return ymd(d);
}

// Load ~/.absbyai-secrets.env WITHOUT `source` — a line in that file breaks
// shell sourcing (documented 2026-08-31, cost a session). Parse it directly and
// never let a stored value override one already set in the real environment.
function loadSecrets() {
  if (!fs.existsSync(SECRETS_ENV)) return;
  for (const raw of fs.readFileSync(SECRETS_ENV, 'utf8').split('\n')) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const eq = line.indexOf('=');
    if (eq < 1) continue;
    const k = line.slice(0, eq).trim();
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(k) || process.env[k] !== undefined) continue;
    let v = line.slice(eq + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    process.env[k] = v;
  }
}

async function getJson(url, init) {
  const res  = await fetch(url, init);
  const text = await res.text();
  let body;
  try { body = JSON.parse(text); } catch { body = { _raw: text.slice(0, 400) }; }
  return { ok: res.ok, status: res.status, body };
}

// ============================================================
// SHARED ANALYSIS
// ============================================================
//
// Both platforms reduce to the same shape before any judgement happens, so the
// detection rules are written ONCE and cannot drift between them:
//
//   Row = { id, name, status, days: { 'YYYY-MM-DD': { spend, results, impressions } },
//           resultLabel, link }
//
// This is the part worth protecting. A per-platform copy of "did spend spike"
// is how two dashboards start disagreeing about the same account.

function summarise(row, day, baselineFrom, baselineTo) {
  const d = row.days || {};
  const today = d[day] || { spend: 0, results: 0, impressions: 0 };

  let baseSpend = 0, baseResults = 0, baseDays = 0;
  for (let x = baselineFrom; x <= baselineTo; x = addDays(x, 1)) {
    const e = d[x];
    if (!e) continue;
    baseSpend   += e.spend;
    baseResults += e.results;
    baseDays++;
  }
  const meanSpend = baseDays ? baseSpend / baseDays : 0;

  return {
    id: row.id,
    name: row.name,
    status: row.status || null,
    resultLabel: row.resultLabel || 'result',
    link: row.link || null,
    spend: round2(today.spend),
    results: today.results,
    impressions: today.impressions,
    costPerResult: today.results > 0 ? round2(today.spend / today.results) : null,
    baseline: {
      days: baseDays,
      meanSpend: round2(meanSpend),
      totalSpend: round2(baseSpend),
      results: baseResults,
      costPerResult: baseResults > 0 ? round2(baseSpend / baseResults) : null,
    },
  };
}

// Anomalies, in the three shapes that actually bit this account.
function detectAnomalies(platform, rows, accountLink) {
  const out = [];

  for (const r of rows) {
    const base = r.baseline;

    // 1. STOPPED SPENDING — the 2026-08-31 miss. A campaign that was really
    //    running and is now at (near) zero. Checked BEFORE the spend floor,
    //    because the whole signature of this failure is a small number.
    if (base.meanSpend >= SPEND_STOP_MIN_BASE && r.spend < base.meanSpend * SPEND_STOP_RATIO) {
      out.push({
        severity: 'high',
        platform,
        scope: 'campaign',
        kind: 'spend_stopped',
        name: r.name,
        headline: `${r.name} stopped spending`,
        detail: `${usd(r.spend)} yesterday against a ${BASELINE_DAYS}-day average of ${usd(base.meanSpend)}/day`
              + `${r.status && r.status !== 'ACTIVE' ? ` — status reads ${r.status}` : ''}.`,
        link: r.link || accountLink,
      });
      continue; // a stopped campaign has nothing else worth saying about it
    }

    // 2. SPEND SPIKE — both a ratio and an absolute dollar floor, so a campaign
    //    going $1 → $3 never reaches the page.
    if (r.spend >= base.meanSpend * SPEND_SPIKE_RATIO
        && r.spend - base.meanSpend >= SPEND_SPIKE_MIN_DELTA
        && base.days >= 3) {
      out.push({
        severity: 'high',
        platform,
        scope: 'campaign',
        kind: 'spend_spike',
        name: r.name,
        headline: `${r.name} spent ${usd(r.spend)} — ${round2(r.spend / (base.meanSpend || 1))}x its normal day`,
        detail: `${BASELINE_DAYS}-day average is ${usd(base.meanSpend)}/day.`,
        link: r.link || accountLink,
      });
    }

    // 3. BOUGHT NOTHING — real money, zero results, over the whole window.
    if (base.totalSpend + r.spend >= ZERO_RESULT_SPEND && base.results + r.results === 0) {
      out.push({
        severity: 'high',
        platform,
        scope: 'campaign',
        kind: 'zero_results',
        name: r.name,
        headline: `${r.name} has spent ${usd(base.totalSpend + r.spend)} for zero ${r.resultLabel}s`,
        detail: `Across the last ${base.days + 1} days.`,
        link: r.link || accountLink,
      });
      continue;
    }

    // 4. COST PER RESULT DEGRADING — needs enough baseline results to mean it.
    if (r.costPerResult && base.costPerResult && base.results >= CPA_MIN_BASE_RESULTS
        && r.spend >= MIN_SPEND_TO_JUDGE
        && r.costPerResult >= base.costPerResult * CPA_DEGRADE_RATIO) {
      out.push({
        severity: 'medium',
        platform,
        scope: 'campaign',
        kind: 'cpa_degraded',
        name: r.name,
        headline: `${r.name} cost per ${r.resultLabel} rose to ${usd(r.costPerResult)}`,
        detail: `Its own ${BASELINE_DAYS}-day average is ${usd(base.costPerResult)} `
              + `(${pct(r.costPerResult / base.costPerResult - 1)}).`,
        link: r.link || accountLink,
      });
    }
  }

  return out;
}

// Winners: an ad beating the platform's own blended cost per result by enough,
// on enough volume to be real. Reported as "scale this", with the numbers, so
// the act is a budget move and not "go look at the ads tab".
function detectWinners(platform, adRows, accountLink) {
  const scored = adRows
    .map(a => ({
      ...a,
      windowSpend:   round2(a.baseline.totalSpend + a.spend),
      windowResults: a.baseline.results + a.results,
    }))
    .filter(a => a.windowResults >= WINNER_MIN_RESULTS && a.windowSpend >= MIN_SPEND_TO_JUDGE);

  if (!scored.length) return [];

  const totalSpend   = scored.reduce((s, a) => s + a.windowSpend, 0);
  const totalResults = scored.reduce((s, a) => s + a.windowResults, 0);
  if (!totalResults) return [];
  const blended = totalSpend / totalResults;

  return scored
    .map(a => ({ ...a, cpr: a.windowSpend / a.windowResults }))
    .filter(a => a.cpr <= blended * WINNER_RATIO)
    .sort((x, y) => x.cpr - y.cpr)
    .slice(0, 3)
    .map(a => ({
      platform,
      scope: 'ad',
      name: a.name,
      headline: `${a.name} is buying ${a.resultLabel}s at ${usd(a.cpr)}`,
      detail: `${pct(a.cpr / blended - 1)} against the account's ${usd(blended)} average, `
            + `on ${a.windowResults} ${a.resultLabel}s / ${usd(a.windowSpend)} over ${BASELINE_DAYS + 1} days.`,
      costPerResult: round2(a.cpr),
      accountCostPerResult: round2(blended),
      results: a.windowResults,
      spend: a.windowSpend,
      link: a.link || accountLink,
    }));
}

// ============================================================
// META
// ============================================================

function metaResultFrom(insight) {
  // ThruPlay lives in its own field, not in `actions`.
  const thru = num((insight.video_thruplay_watched_actions || []).find(a => a.action_type === 'video_view')?.value)
            || num((insight.video_thruplay_watched_actions || [])[0]?.value);

  const actions = insight.actions || [];
  for (const p of META_RESULT_PRIORITY) {
    const hit = actions.find(a => a.action_type === p.key);
    if (hit) return { results: num(hit.value), label: p.label };
  }
  if (thru) return { results: thru, label: 'ThruPlay' };
  return { results: 0, label: 'result' };
}

async function fetchMeta(day, baselineFrom) {
  const token = process.env.META_ADS_TOKEN
             || process.env.FACEBOOK_ADS_ACCESS_TOKEN
             || process.env.FACEBOOK_PAGE_ACCESS_TOKEN
             || '';
  const account = process.env.META_AD_ACCOUNT_ID || META_ACCOUNT_DEFAULT;
  const link = `https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=${account.replace(/^act_/, '')}`;

  const blind = (reason, setup) => ({
    ok: false, platform: 'meta', account, reason, setup, link,
    spend: null, campaigns: [], anomalies: [], winners: [],
  });

  if (!token) {
    return blind(
      'No Meta ads token configured.',
      'Set META_ADS_TOKEN — see Docs/ADS_DIGEST.md (5 min, Business Settings → System users).'
    );
  }

  const params = (extra) => new URLSearchParams({
    time_range: JSON.stringify({ since: baselineFrom, until: day }),
    time_increment: '1',
    limit: '500',
    access_token: token,
    ...extra,
  });

  const campaignsUrl = `${META_API}/${account}/insights?` + params({
    level: 'campaign',
    fields: 'campaign_id,campaign_name,spend,impressions,actions,video_thruplay_watched_actions',
  });

  const r = await getJson(campaignsUrl);
  if (!r.ok) {
    const msg = r.body?.error?.message || `HTTP ${r.status}`;
    // The exact failure the stored Page token produces today. Naming it beats a
    // generic "Meta unavailable", which would send the next session re-deriving it.
    const isScope = /ads_management or ads_read/i.test(msg) || r.body?.error?.code === 200;
    return blind(
      isScope ? 'The stored Facebook token is a PAGE token and carries no ads_read permission.' : msg,
      isScope
        ? 'Create a system-user token with ads_read on ad account ' + account
          + ' and store it as META_ADS_TOKEN — Docs/ADS_DIGEST.md has the click path.'
        : 'Check the token has not expired; re-issue it per Docs/ADS_DIGEST.md.'
    );
  }

  // Fold the daily rows into one Row per campaign.
  const byCampaign = new Map();
  for (const ins of (r.body.data || [])) {
    const id = ins.campaign_id;
    if (!byCampaign.has(id)) {
      byCampaign.set(id, {
        id, name: ins.campaign_name, days: {}, resultLabel: 'result',
        link: `https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=${account.replace(/^act_/, '')}&selected_campaign_ids=${id}`,
      });
    }
    const row = byCampaign.get(id);
    const { results, label } = metaResultFrom(ins);
    if (label !== 'result') row.resultLabel = label;
    row.days[ins.date_start] = {
      spend: num(ins.spend), results, impressions: num(ins.impressions),
    };
  }

  // Campaign status — the "toggled OFF and nobody noticed" signal, and the only
  // way to tell a paused campaign from a delivery problem.
  const statusRes = await getJson(
    `${META_API}/${account}/campaigns?fields=name,status,effective_status,issues_info&limit=200&access_token=${encodeURIComponent(token)}`
  );
  const statuses = new Map();
  if (statusRes.ok) {
    for (const c of (statusRes.body.data || [])) {
      statuses.set(c.id, c.effective_status || c.status);
      if (!byCampaign.has(c.id) && c.effective_status === 'ACTIVE') {
        // Active but zero delivery all window — worth existing as a row so the
        // stop/zero-result rules can see it.
        byCampaign.set(c.id, { id: c.id, name: c.name, days: {}, resultLabel: 'result', link });
      }
    }
  }
  for (const [id, row] of byCampaign) row.status = statuses.get(id) || null;

  // Ad level, same window, for winner detection.
  const adsRes = await getJson(`${META_API}/${account}/insights?` + params({
    level: 'ad',
    fields: 'ad_id,ad_name,campaign_name,spend,impressions,actions,video_thruplay_watched_actions',
  }));
  const byAd = new Map();
  if (adsRes.ok) {
    for (const ins of (adsRes.body.data || [])) {
      const id = ins.ad_id;
      if (!byAd.has(id)) {
        byAd.set(id, { id, name: ins.ad_name, days: {}, resultLabel: 'result', link });
      }
      const row = byAd.get(id);
      const { results, label } = metaResultFrom(ins);
      if (label !== 'result') row.resultLabel = label;
      row.days[ins.date_start] = { spend: num(ins.spend), results, impressions: num(ins.impressions) };
    }
  }

  const baselineTo = addDays(day, -1);
  const campaigns  = [...byCampaign.values()].map(r => summarise(r, day, baselineFrom, baselineTo));
  const ads        = [...byAd.values()].map(r => summarise(r, day, baselineFrom, baselineTo));

  const anomalies = detectAnomalies('meta', campaigns, link);

  // Disapproved / issue-flagged ads. Zero across all 29 ads at the 8/26 audit;
  // this exists so the first one is caught the morning it happens.
  const reviewRes = await getJson(
    `${META_API}/${account}/ads?fields=name,effective_status&limit=500&access_token=${encodeURIComponent(token)}`
  );
  if (reviewRes.ok) {
    const bad = (reviewRes.body.data || [])
      .filter(a => ['DISAPPROVED', 'WITH_ISSUES', 'PENDING_BILLING_INFO', 'ADSET_PAUSED'].includes(a.effective_status)
                && a.effective_status !== 'ADSET_PAUSED');
    for (const a of bad.slice(0, 3)) {
      anomalies.push({
        severity: 'high', platform: 'meta', scope: 'ad', kind: 'ad_rejected',
        name: a.name,
        headline: `Ad "${a.name}" is ${String(a.effective_status).toLowerCase().replace(/_/g, ' ')}`,
        detail: 'It is not delivering until this is resolved.',
        link,
      });
    }
  }

  const spendToday = round2(campaigns.reduce((s, c) => s + c.spend, 0));
  const meanDaily  = round2(campaigns.reduce((s, c) => s + c.baseline.meanSpend, 0));

  return {
    ok: true, platform: 'meta', account, link,
    spend: spendToday,
    spend7dMean: meanDaily,
    deltaPct: meanDaily > 0 ? round2(spendToday / meanDaily - 1) : null,
    campaigns: campaigns.sort((a, b) => b.spend - a.spend),
    anomalies,
    winners: detectWinners('meta', ads, link),
  };
}

// ============================================================
// GOOGLE ADS
// ============================================================
//
// NOT REACHABLE AS OF 2026-09-02 and the reason is specific, not a shrug:
// Phase 1 of Handoffs/handoff-20260831-google-ads-api-setup-engagement-ad-automation.md
// is unexecuted, so there is no developer token, and the stored GOOGLE_REFRESH_TOKEN
// is scoped to calendar.readonly only (verified 2026-09-02 against tokeninfo).
// Two separate credentials are missing, and neither can be minted from here.
//
// The query and the whole response mapping below are written and ready. When the
// developer token and an adwords-scoped refresh token exist, this leg starts
// returning data with no further code — that is the point of writing it now
// rather than leaving a TODO.
async function fetchGoogle(day, baselineFrom) {
  const customer = (process.env.GOOGLE_ADS_CUSTOMER_ID || GOOGLE_CUSTOMER_DEFAULT).replace(/-/g, '');
  const link = `https://ads.google.com/aw/campaigns?__c=${customer}`;

  const blind = (reason, setup) => ({
    ok: false, platform: 'google', account: customer, reason, setup, link,
    spend: null, campaigns: [], anomalies: [], winners: [],
  });

  const devToken = process.env.GOOGLE_ADS_DEVELOPER_TOKEN || '';
  const refresh  = process.env.GOOGLE_ADS_REFRESH_TOKEN || '';
  const clientId = process.env.GOOGLE_CLIENT_ID || '';
  const secret   = process.env.GOOGLE_CLIENT_SECRET || '';

  if (!devToken) {
    return blind(
      'No Google Ads developer token — API access was never set up (handoff Phase 1 unexecuted).',
      'Apply for a developer token in MCC 324-458-6445 → Tools → API Center, then set GOOGLE_ADS_DEVELOPER_TOKEN.'
    );
  }
  if (!refresh || !clientId || !secret) {
    return blind(
      'No adwords-scoped OAuth refresh token (the stored GOOGLE_REFRESH_TOKEN is calendar.readonly only).',
      'Run the OAuth consent flow for https://www.googleapis.com/auth/adwords and set GOOGLE_ADS_REFRESH_TOKEN.'
    );
  }

  // Exchange the refresh token.
  const tok = await getJson('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: clientId, client_secret: secret,
      refresh_token: refresh, grant_type: 'refresh_token',
    }),
  });
  if (!tok.ok || !tok.body.access_token) {
    return blind(`OAuth refresh failed: ${tok.body?.error_description || tok.body?.error || tok.status}`,
                 'Re-run the adwords OAuth consent flow.');
  }

  // GAQL. `metrics.conversions` is the inflated column — see
  // GOOGLE_CONVERSION_INFLATION above; the deflation happens after the fetch and
  // is labelled, never folded into the raw number.
  const gaql = `
    SELECT campaign.id, campaign.name, campaign.status,
           segments.date,
           metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions
    FROM campaign
    WHERE segments.date BETWEEN '${baselineFrom}' AND '${day}'
  `.trim();

  const res = await getJson(
    `https://googleads.googleapis.com/v18/customers/${customer}/googleAds:searchStream`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${tok.body.access_token}`,
        'developer-token': devToken,
        'login-customer-id': (process.env.GOOGLE_ADS_LOGIN_CUSTOMER_ID || GOOGLE_LOGIN_CUSTOMER).replace(/-/g, ''),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: gaql }),
    }
  );
  if (!res.ok) {
    const msg = res.body?.error?.message
             || res.body?.[0]?.error?.message
             || `HTTP ${res.status}`;
    return blind(`Google Ads API error: ${msg}`, 'Check the developer token is approved and the login-customer-id is the MCC.');
  }

  const byCampaign = new Map();
  const batches = Array.isArray(res.body) ? res.body : [res.body];
  for (const batch of batches) {
    for (const r of (batch.results || [])) {
      const id = r.campaign?.id;
      if (!id) continue;
      if (!byCampaign.has(id)) {
        byCampaign.set(id, {
          id, name: r.campaign.name, status: r.campaign.status,
          days: {}, resultLabel: 'conversion',
          link: `https://ads.google.com/aw/campaigns?__c=${customer}&campaignId=${id}`,
        });
      }
      byCampaign.get(id).days[r.segments.date] = {
        spend: num(r.metrics?.costMicros) / 1e6,
        results: num(r.metrics?.conversions),
        impressions: num(r.metrics?.impressions),
      };
    }
  }

  const baselineTo = addDays(day, -1);
  const campaigns = [...byCampaign.values()].map(r => {
    const s = summarise(r, day, baselineFrom, baselineTo);
    // The estimate, always alongside the raw figure, never instead of it.
    const windowSpend   = s.baseline.totalSpend + s.spend;
    const windowResults = s.baseline.results + s.results;
    const estSubs = windowResults / GOOGLE_CONVERSION_INFLATION;
    return {
      ...s,
      estSubscribers: round2(estSubs),
      estCostPerSubscriber: estSubs >= 1 ? round2(windowSpend / estSubs) : null,
      estimateBasis: GOOGLE_INFLATION_BASIS,
    };
  });

  const spendToday = round2(campaigns.reduce((s, c) => s + c.spend, 0));
  const meanDaily  = round2(campaigns.reduce((s, c) => s + c.baseline.meanSpend, 0));

  return {
    ok: true, platform: 'google', account: customer, link,
    spend: spendToday,
    spend7dMean: meanDaily,
    deltaPct: meanDaily > 0 ? round2(spendToday / meanDaily - 1) : null,
    conversionInflation: GOOGLE_CONVERSION_INFLATION,
    conversionInflationBasis: GOOGLE_INFLATION_BASIS,
    campaigns: campaigns.sort((a, b) => b.spend - a.spend),
    anomalies: detectAnomalies('google', campaigns, link),
    winners: [], // ad-level Demand Gen reporting needs its own query; campaign-level first
  };
}

// ============================================================
// MAIN
// ============================================================

async function main() {
  loadSecrets();

  const argv = process.argv.slice(2);
  const argOf = (flag) => { const i = argv.indexOf(flag); return i >= 0 ? argv[i + 1] : null; };

  // Default to YESTERDAY: today's numbers are partial all morning, and a digest
  // that grades a half-finished day invents anomalies every time it runs.
  const day = argOf('--day') || addDays(ymd(new Date()), -1);
  const baselineFrom = addDays(day, -BASELINE_DAYS);
  const outPath = argOf('--out') || OUT_DEFAULT;

  const [meta, google] = await Promise.all([
    fetchMeta(day, baselineFrom).catch(e => ({
      ok: false, platform: 'meta', reason: `Fetch threw: ${e.message}`,
      setup: 'See Docs/ADS_DIGEST.md.', spend: null, campaigns: [], anomalies: [], winners: [],
    })),
    fetchGoogle(day, baselineFrom).catch(e => ({
      ok: false, platform: 'google', reason: `Fetch threw: ${e.message}`,
      setup: 'See Docs/ADS_DIGEST.md.', spend: null, campaigns: [], anomalies: [], winners: [],
    })),
  ]);

  const live = [meta, google].filter(p => p.ok);
  const blind = [meta, google].filter(p => !p.ok);

  const anomalies = [...meta.anomalies, ...google.anomalies]
    .sort((a, b) => (a.severity === 'high' ? -1 : 1) - (b.severity === 'high' ? -1 : 1));
  const winners = [...meta.winners, ...google.winners];

  const spendYesterday = live.length ? round2(live.reduce((s, p) => s + (p.spend || 0), 0)) : null;
  const spend7dMean    = live.length ? round2(live.reduce((s, p) => s + (p.spend7dMean || 0), 0)) : null;

  const digest = {
    generatedAt: new Date().toISOString(),
    day,
    window: { from: baselineFrom, to: day, baselineDays: BASELINE_DAYS },
    // `blind` is the honest headline state: the digest ran, and it could not see.
    // The morning brief renders one line for it. It disappears by itself the
    // moment a credential lands — no code change, no follow-up task.
    blind: blind.map(p => ({ platform: p.platform, reason: p.reason, setup: p.setup })),
    totals: {
      spendYesterday,
      spend7dMean,
      deltaPct: (spendYesterday !== null && spend7dMean > 0) ? round2(spendYesterday / spend7dMean - 1) : null,
      platformsLive: live.map(p => p.platform),
    },
    anomalies,
    winners,
    platforms: { meta, google },
    thresholds: {
      minSpendToJudge: MIN_SPEND_TO_JUDGE,
      spendSpikeRatio: SPEND_SPIKE_RATIO,
      spendStopRatio: SPEND_STOP_RATIO,
      cpaDegradeRatio: CPA_DEGRADE_RATIO,
      winnerRatio: WINNER_RATIO,
      winnerMinResults: WINNER_MIN_RESULTS,
      googleConversionInflation: GOOGLE_CONVERSION_INFLATION,
    },
  };

  fs.writeFileSync(outPath, JSON.stringify(digest, null, 2) + '\n');

  // One-line stdout summary — this is what the morning-brief job reads off the
  // console when it decides whether the section prints at all.
  const parts = [];
  if (spendYesterday !== null) parts.push(`spend ${usd(spendYesterday)}`);
  parts.push(`${anomalies.length} anomal${anomalies.length === 1 ? 'y' : 'ies'}`);
  parts.push(`${winners.length} winner${winners.length === 1 ? '' : 's'}`);
  if (blind.length) parts.push(`BLIND: ${blind.map(b => b.platform).join(', ')}`);
  console.log(`ads-digest ${day} → ${outPath}: ${parts.join(', ')}`);

  if (argv.includes('--print')) console.log(JSON.stringify(digest, null, 2));
}

// Exported so `scripts/ads/ads-digest.test.js` can drive the detection rules
// against fixtures. The rules are the part that must be right and the part that
// no live credential currently exercises — see the test for why that matters.
module.exports = { summarise, detectAnomalies, detectWinners, addDays, metaResultFrom,
                   GOOGLE_CONVERSION_INFLATION };

// Only run when executed directly, so requiring this file from the test does not
// fire a live API pull.
if (require.main === module) main().catch(e => {
  // Still exit 0: a crashed digest must not take the morning brief down with it.
  console.error('ads-digest failed:', e.stack || e.message);
  try {
    fs.writeFileSync(OUT_DEFAULT, JSON.stringify({
      generatedAt: new Date().toISOString(),
      error: String(e.message || e),
      blind: [{ platform: 'meta', reason: 'digest crashed', setup: 'See Docs/ADS_DIGEST.md.' },
              { platform: 'google', reason: 'digest crashed', setup: 'See Docs/ADS_DIGEST.md.' }],
      anomalies: [], winners: [], totals: { spendYesterday: null },
    }, null, 2) + '\n');
  } catch { /* nothing left to do */ }
});
