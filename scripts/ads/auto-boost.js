#!/usr/bin/env node
/* eslint-disable no-console */
//
// IG AUTO-BOOST — every new @danrosefit post gets a $5 lifetime "profile visits"
// test ad on the REAL post; one champion ad runs at $6.50/day; tests are ranked on
// cost per profile visit, the champion is judged on cost per follow, a test that
// beats the champion replaces it. Caps: $300/month on tests, $500/month total.
//
// Design locked with Dan 2026-09-02: Handoffs/handoff-20260902-ig-auto-boost.md.
// The numbers below are HIS decisions, not tunables — change them only if he does.
//
// RUN:   node scripts/ads/auto-boost.js [--dry-run] [--verify] [--out PATH] [--print]
//   Hourly Railway cron ("15 * * * *", service `auto-boost`, must exit when done).
//   --dry-run   plan everything, write NOTHING to Meta, and do not record events.
//               The run report is still written locally (brief-autoboost.json) and
//               to Postgres flagged dry_run=true, so the morning brief can show what
//               the system WOULD have done while it is switched off.
//   --verify    print every insights action type Meta returns for the campaign, per
//               ad, next to the pinned metric names — for matching the API strings
//               to Ads Manager's "Instagram profile visits" and "Follows or likes"
//               columns once real data exists. Read-only.
//   AUTO_BOOST_ENABLED=1 in the environment is what makes it live. Anything else
//   behaves as --dry-run. This is the single switch.
//
// META IS THE LEDGER. The Instagram media id lives in the ad-set name
// ("TEST::<media_id>"), so "has this post been tested?" is answered by Meta, never
// by a file that can drift, and a re-run can never double-create. Postgres holds
// only what Meta cannot: skips (posts Meta refused), verdicts, promotions, and the
// run reports the morning brief renders.
//
// CREATIVE SHAPE (the only one that runs as @danrosefit — everything else is
// proven to fail, see the parent handoff's "SESSION 2 RESULT"):
//   POST /act/adcreatives  object_id=<page> instagram_user_id=<ig> source_instagram_media_id=<media>
//   NO object_story_spec, NO call_to_action.
//
// VERIFIED 2026-09-02 against the live ad account (zero-spend probes, deleted after):
//   - `instagram_profile_visits` is an accepted top-level insights field.
//   - lifetime_budget=500 over 5 days is accepted by Meta's validation.
//   - CAROUSEL_ALBUM and IMAGE posts both accept the creative shape.
//   The champion campaign had ~1 hour of delivery and no insights rows at build
//   time, so the API→Ads Manager column MATCH is still open — run --verify once
//   spend exists. Until a follow-type action is observed with a non-zero count,
//   the champion is judged on cost/visit and the brief says so (Dan accepted this).

'use strict';

const fs     = require('fs');
const os     = require('os');
const path   = require('path');
const crypto = require('crypto');

// ============================================================
// CONFIG — Dan's decisions
// ============================================================

const META_API = 'https://graph.facebook.com/v21.0';
const ACT               = 'act_2143998876461525';
const CAMPAIGN_ID       = '120250753198730682';   // "[AUTO] IG PROFILE VISITS - danrosefit"
const CHAMPION_ADSET_ID = '120250753601020682';   // "CHAMPION", daily_budget 650
const PAGE_ID           = '1380236418500031';     // Daniel Rose Fitness (keeper)
const IG_USER_ID        = '17841401601139982';    // @danrosefit

// Posts published on or after this day get a test. Set to the day the champion
// went live and the system was built. Earlier posts are history, not candidates.
const SYSTEM_START = '2026-09-02';

// The two ads already in the champion ad set. They are the "first-run pair" and
// never get TEST ad sets of their own.
const FIRST_RUN_PAIR = ['18188183254395331', '18192762022391478'];

const TEST_BUDGET_CENTS   = 500;     // $5 lifetime per post
const TEST_WINDOW_DAYS    = 5;       // evaluate at end_time at the latest
const TEST_EVAL_SPEND     = 4.50;    // ...or as soon as this much is spent
const CHAMPION_DAILY_CENTS = 650;    // $6.50/day ≈ $200/month — verified, not set, here
const CAP_TESTS_MTD       = 300;     // stop creating tests past this
const CAP_TOTAL_MTD       = 500;     // ...or this, champion included
const PROMOTE_MIN_VISITS  = 10;      // a test needs this many visits to be believed
const CHAMPION_MIN_SPEND  = 35;      // 7-day spend before the champion is judged
const CHAMPION_KILL_CPF   = 5.00;    // pause at > $5/follow
const CHAMPION_SCALE_CPF  = 3.00;    // report as scale candidate at < $3/follow (never auto-scaled)
const PAIR_MIN_SPEND      = 10;      // each of the first-run pair needs this before one is retired
const CHAMPION_WINDOW_DAYS = 7;

// ── Metric names ─────────────────────────────────────────────
// Profile visits: a top-level insights field (accepted by the API 2026-09-02).
const VISITS_FIELD = 'instagram_profile_visits';
// Fallbacks inside `actions`, in case Meta reports it there for this objective.
const VISIT_ACTION_TYPES = ['instagram_profile_visit', 'ig_profile_visit', 'profile_visit'];
// Follows: Meta added an "Instagram follows" ads metric in Aug 2025; the API string
// is not documented anywhere reachable. Candidates in preference order — the first
// one that appears in `actions` with a non-zero value is the metric, and --verify
// prints every action type so the match to Ads Manager's "Follows or likes" column
// can be pinned by eye. `like` is last because on a Page-identity ad it means Page
// likes; on an Instagram-identity ad it is the closest documented relative.
const FOLLOW_ACTION_TYPES = [
  'instagram_follow', 'ig_follow', 'follow', 'onsite_conversion.ig_follow',
  'onsite_conversion.follow', 'onsite_conversion.instagram_follow', 'page_like', 'like',
];

const REPO_ROOT   = path.resolve(__dirname, '..', '..');
const SECRETS_ENV = path.join(os.homedir(), '.absbyai-secrets.env');
const OUT_DEFAULT = path.join(REPO_ROOT, 'brief-autoboost.json');

// ============================================================
// SMALL UTILITIES
// ============================================================

const round2 = (n) => Math.round((Number(n) || 0) * 100) / 100;
const num    = (v) => { const n = Number(v); return Number.isFinite(n) ? n : 0; };
const usd    = (n) => `$${round2(n).toFixed(2)}`;
const ymd    = (d) => new Date(d).toISOString().slice(0, 10);
const daysAgo = (n, from = new Date()) => new Date(from.getTime() - n * 86400e3);

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

const mediaIdOf = (name) => { const m = /::(\d+)/.exec(name || ''); return m ? m[1] : null; };
const captionOf = (m) => String((m && m.caption) || '').replace(/\s+/g, ' ').trim().slice(0, 80);
const isTest    = (adset) => /^TEST::\d+/.test(adset.name || '');

// ============================================================
// PURE RULES — exported, driven by auto-boost.test.js
// ============================================================

// Read visits/follows out of one insights row. `followsType` is the action type
// that carried the count, or null when none of the candidates appeared.
function metricsFrom(ins) {
  const actions = (ins && ins.actions) || [];
  let visits = num(ins && ins[VISITS_FIELD]);
  if (!visits) {
    for (const t of VISIT_ACTION_TYPES) {
      const hit = actions.find(a => a.action_type === t);
      if (hit) { visits = num(hit.value); break; }
    }
  }
  let follows = 0, followsType = null;
  for (const t of FOLLOW_ACTION_TYPES) {
    const hit = actions.find(a => a.action_type === t);
    if (hit && num(hit.value) > 0) { follows = num(hit.value); followsType = t; break; }
  }
  return { spend: round2(num(ins && ins.spend)), visits, follows, followsType,
           impressions: num(ins && ins.impressions) };
}

// Monthly caps. `committed` counts money already promised to running tests
// (their unspent lifetime budget) so the cap holds even when insights lag.
function capState({ testsMtd, totalMtd, committedTests }) {
  const testsCommitted = round2(testsMtd + (committedTests || 0));
  const totalCommitted = round2(totalMtd + (committedTests || 0));
  let reason = null;
  if (testsCommitted + TEST_BUDGET_CENTS / 100 > CAP_TESTS_MTD) {
    reason = `tests at ${usd(testsCommitted)} of the ${usd(CAP_TESTS_MTD)} monthly cap`;
  } else if (totalCommitted + TEST_BUDGET_CENTS / 100 > CAP_TOTAL_MTD) {
    reason = `total at ${usd(totalCommitted)} of the ${usd(CAP_TOTAL_MTD)} monthly cap`;
  }
  return {
    testsMtd: round2(testsMtd), totalMtd: round2(totalMtd),
    testsCommitted, totalCommitted,
    testsCap: CAP_TESTS_MTD, totalCap: CAP_TOTAL_MTD,
    capReached: !!reason, reason,
  };
}

// Which posts get a test this run.
function findCandidates({ media, testedIds, skippedIds, startDate = SYSTEM_START, neverTest = FIRST_RUN_PAIR }) {
  const tested  = new Set(testedIds || []);
  const skipped = new Set(skippedIds || []);
  const never   = new Set(neverTest || []);
  return (media || [])
    .filter(m => m && m.id && m.timestamp && ymd(m.timestamp) >= startDate)
    .filter(m => !tested.has(m.id) && !skipped.has(m.id) && !never.has(m.id))
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp)); // oldest first
}

// Is a test finished enough to judge?
function testPhase(test, now = new Date()) {
  if (test.spend >= TEST_EVAL_SPEND) return 'ready';
  if (test.endTime && new Date(test.endTime) <= now) return 'ready';
  return 'running';
}

// The verdict on one finished test against the champion's trailing window.
//   champion = { costPerVisit: number|null, hasActive: boolean }
function verdict(test, champion) {
  const cpv = test.visits > 0 ? round2(test.spend / test.visits) : null;
  if (test.spend >= 1 && test.visits === 0 && test.visitsReadable === false) {
    return { result: 'unmeasured', costPerVisit: null,
             reason: 'profile-visit metric not readable on this account yet — not judged' };
  }
  if (test.visits < PROMOTE_MIN_VISITS) {
    return { result: 'lose', costPerVisit: cpv,
             reason: `${test.visits} visits on ${usd(test.spend)} — needs ${PROMOTE_MIN_VISITS} to be believed` };
  }
  if (!champion || !champion.hasActive || champion.costPerVisit === null) {
    return { result: 'win', costPerVisit: cpv,
             reason: `${usd(cpv)}/visit on ${test.visits} visits and the champion slot is empty` };
  }
  if (cpv < champion.costPerVisit) {
    return { result: 'win', costPerVisit: cpv,
             reason: `${usd(cpv)}/visit beats the champion's ${usd(champion.costPerVisit)}/visit (${test.visits} visits)` };
  }
  return { result: 'lose', costPerVisit: cpv,
           reason: `${usd(cpv)}/visit does not beat the champion's ${usd(champion.costPerVisit)}/visit (ties keep the champion)` };
}

// Champion health over the trailing window.
//   stats = { spend, visits, follows, followsReadable }
function championHealth(stats) {
  const cpv = stats.visits > 0 ? round2(stats.spend / stats.visits) : null;
  const cpf = stats.followsReadable && stats.follows > 0 ? round2(stats.spend / stats.follows) : null;
  const base = { costPerVisit: cpv, costPerFollow: cpf, followsReadable: !!stats.followsReadable };
  if (!stats.followsReadable) {
    return { ...base, action: 'unjudged',
             reason: 'follows metric not readable yet — judged on cost/visit only, no kill rule applied' };
  }
  if (stats.spend < CHAMPION_MIN_SPEND) {
    return { ...base, action: 'ok', reason: `${usd(stats.spend)} in ${CHAMPION_WINDOW_DAYS} days — under the ${usd(CHAMPION_MIN_SPEND)} judging floor` };
  }
  const effectiveCpf = stats.follows > 0 ? stats.spend / stats.follows : Infinity;
  if (effectiveCpf > CHAMPION_KILL_CPF) {
    return { ...base, action: 'pause',
             reason: `${stats.follows === 0 ? 'zero follows' : usd(effectiveCpf) + '/follow'} on ${usd(stats.spend)} — over the ${usd(CHAMPION_KILL_CPF)}/follow kill line` };
  }
  if (effectiveCpf < CHAMPION_SCALE_CPF) {
    return { ...base, action: 'scale_candidate',
             reason: `${usd(effectiveCpf)}/follow on ${usd(stats.spend)} — under the ${usd(CHAMPION_SCALE_CPF)}/follow scale line (budget cap is fixed; reported only)` };
  }
  return { ...base, action: 'ok', reason: `${usd(effectiveCpf)}/follow on ${usd(stats.spend)}` };
}

// First-run pair: both original ads run until each has PAIR_MIN_SPEND, then the
// cheaper cost/visit stays. Until then the one-active-ad rule is suspended.
//   ads = [{ id, mediaId, spend, visits, active }]
function pairDecision(ads) {
  const pair = (ads || []).filter(a => FIRST_RUN_PAIR.includes(a.mediaId) && a.active);
  if (pair.length < 2) return { resolved: false, reason: 'pair is not both active' };
  if (pair.some(a => a.spend < PAIR_MIN_SPEND)) {
    return { resolved: false,
             reason: `waiting for both to reach ${usd(PAIR_MIN_SPEND)} (${pair.map(a => usd(a.spend)).join(' / ')})` };
  }
  const scored = pair.map(a => ({ ...a, cpv: a.visits > 0 ? a.spend / a.visits : Infinity }))
                     .sort((x, y) => x.cpv - y.cpv);
  if (!Number.isFinite(scored[0].cpv)) {
    return { resolved: false, reason: 'neither has a profile visit yet — cannot rank' };
  }
  return { resolved: true, keep: scored[0], retire: scored[1],
           reason: `${usd(scored[0].cpv)}/visit beats ${Number.isFinite(scored[1].cpv) ? usd(scored[1].cpv) : 'no visits'}` };
}

// ============================================================
// META CLIENT
// ============================================================

function makeMeta(token, appSecret) {
  const proof = crypto.createHmac('sha256', appSecret).update(token).digest('hex');
  const auth  = { access_token: token, appsecret_proof: proof };

  async function call(method, p, params = {}) {
    const body = new URLSearchParams();
    for (const [k, v] of Object.entries({ ...params, ...auth })) {
      body.set(k, typeof v === 'object' ? JSON.stringify(v) : String(v));
    }
    const url = `${META_API}/${p}` + (method === 'GET' ? `?${body}` : '');
    let last;
    for (let attempt = 0; attempt < 3; attempt++) {
      const res  = await fetch(url, method === 'GET' ? {} : { method, body });
      const text = await res.text();
      let json; try { json = JSON.parse(text); } catch { json = { error: { message: text.slice(0, 300) } }; }
      if (res.ok && !json.error) return json;
      last = json.error || { message: `HTTP ${res.status}` };
      // Retry only on transient server-side codes; a validation error is final.
      if (![1, 2, 4, 17, 341].includes(last.code) && res.status < 500) break;
      await new Promise(r => setTimeout(r, 1500 * (attempt + 1)));
    }
    const err = new Error(`Meta ${method} ${p}: ${last.message}` + (last.error_subcode ? ` (subcode ${last.error_subcode})` : ''));
    err.meta = last;
    throw err;
  }

  return {
    get:  (p, params) => call('GET', p, params),
    post: (p, params) => call('POST', p, params),
    del:  (p)         => call('DELETE', p),
    async all(p, params) { // follow paging
      let out = [], url = null, page = await call('GET', p, { limit: 200, ...params });
      out = out.concat(page.data || []);
      while (page.paging && page.paging.next && out.length < 2000) {
        url = page.paging.next;
        const res = await fetch(url); page = await res.json();
        out = out.concat(page.data || []);
      }
      return out;
    },
  };
}

// ============================================================
// POSTGRES — events + run reports (the only non-Meta state)
// ============================================================

function makeDb(url) {
  if (!url) return null;
  let Pool;
  try { ({ Pool } = require('pg')); } catch { return null; }
  const pool = new Pool({
    connectionString: url,
    ssl: /localhost|127\.0\.0\.1|railway\.internal/.test(url) ? false : { rejectUnauthorized: false },
  });
  return {
    async ensureSchema() {
      await pool.query(`
        CREATE TABLE IF NOT EXISTS auto_boost_events (
          id       SERIAL PRIMARY KEY,
          media_id TEXT,
          event    TEXT NOT NULL,
          detail   JSONB,
          at       TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        CREATE INDEX IF NOT EXISTS auto_boost_events_media_idx ON auto_boost_events (media_id);
        CREATE INDEX IF NOT EXISTS auto_boost_events_at_idx ON auto_boost_events (at);
        CREATE TABLE IF NOT EXISTS auto_boost_runs (
          id      SERIAL PRIMARY KEY,
          at      TIMESTAMPTZ NOT NULL DEFAULT now(),
          dry_run BOOLEAN NOT NULL,
          enabled BOOLEAN NOT NULL,
          report  JSONB NOT NULL
        );
      `);
    },
    async events() {
      const r = await pool.query('SELECT media_id, event, detail, at FROM auto_boost_events ORDER BY at');
      return r.rows;
    },
    async event(mediaId, event, detail) {
      await pool.query('INSERT INTO auto_boost_events (media_id, event, detail) VALUES ($1, $2, $3)',
                       [mediaId, event, JSON.stringify(detail || {})]);
    },
    async run(report, dryRun, enabled) {
      await pool.query('INSERT INTO auto_boost_runs (dry_run, enabled, report) VALUES ($1, $2, $3)',
                       [dryRun, enabled, JSON.stringify(report)]);
      // Keep the table small: the brief only ever reads the latest row.
      await pool.query(`DELETE FROM auto_boost_runs WHERE id NOT IN
                        (SELECT id FROM auto_boost_runs ORDER BY at DESC LIMIT 500)`);
    },
    close: () => pool.end(),
  };
}

// ============================================================
// THE JOB
// ============================================================

async function runJob({ meta, db, dryRun, enabled, verify, now = new Date() }) {
  const report = {
    generatedAt: now.toISOString(),
    dryRun, enabled,
    campaign: CAMPAIGN_ID, championAdset: CHAMPION_ADSET_ID,
    caps: null, champion: null, pair: null, tests: [], created: [], verdicts: [],
    skips: [], events24h: [], warnings: [], actions: [],
  };
  const act = async (line, fn) => {
    if (dryRun) { report.actions.push(`WOULD: ${line}`); return null; }
    const out = await fn();
    report.actions.push(`DID: ${line}`);
    return out;
  };
  const warn = (s) => { report.warnings.push(s); console.log(`  ⚠ ${s}`); };
  const record = async (mediaId, event, detail) => {
    if (dryRun || !db) return;
    await db.event(mediaId, event, detail);
  };

  // ── Guard: the champion ad set is what the handoff says it is ──────────
  const champ = await meta.get(CHAMPION_ADSET_ID,
    { fields: 'name,status,effective_status,daily_budget,optimization_goal,destination_type,targeting,promoted_object' });
  if (champ.optimization_goal !== 'VISIT_INSTAGRAM_PROFILE' || champ.destination_type !== 'INSTAGRAM_PROFILE') {
    throw new Error(`champion ad set ${CHAMPION_ADSET_ID} is not a profile-visits ad set (${champ.optimization_goal}/${champ.destination_type}) — refusing to run`);
  }
  if (String(champ.daily_budget) !== String(CHAMPION_DAILY_CENTS)) {
    warn(`champion daily budget reads ${champ.daily_budget} cents, expected ${CHAMPION_DAILY_CENTS} — not changing it`);
  }
  // Names are the ledger, so make sure they are the ones the handoff specifies.
  const camp = await meta.get(CAMPAIGN_ID, { fields: 'name,status,effective_status' });
  if (camp.name !== '[AUTO] IG PROFILE VISITS - danrosefit') {
    await act(`rename campaign "${camp.name}" → "[AUTO] IG PROFILE VISITS - danrosefit"`,
              () => meta.post(CAMPAIGN_ID, { name: '[AUTO] IG PROFILE VISITS - danrosefit' }));
  }
  if (champ.name !== 'CHAMPION') {
    await act(`rename champion ad set "${champ.name}" → "CHAMPION"`,
              () => meta.post(CHAMPION_ADSET_ID, { name: 'CHAMPION' }));
  }
  if (camp.effective_status !== 'ACTIVE') warn(`campaign is ${camp.effective_status} — nothing in it is delivering`);

  // ── Pull everything once ───────────────────────────────────────────────
  const adsets = await meta.all(`${CAMPAIGN_ID}/adsets`,
    { fields: 'id,name,status,effective_status,lifetime_budget,daily_budget,start_time,end_time,created_time' });
  const testAdsets = adsets.filter(isTest);

  const [mtdRows, lifeRows, campLife] = await Promise.all([
    meta.all(`${CAMPAIGN_ID}/insights`, { level: 'adset', date_preset: 'this_month', fields: 'adset_id,adset_name,spend' }),
    meta.all(`${CAMPAIGN_ID}/insights`, { level: 'adset', date_preset: 'maximum',
                                          fields: `adset_id,adset_name,spend,impressions,actions,${VISITS_FIELD}` }),
    meta.get(`${CAMPAIGN_ID}/insights`, { date_preset: 'maximum', fields: `spend,impressions,actions,${VISITS_FIELD}` }),
  ]);
  const lifeBy = new Map(lifeRows.map(r => [r.adset_id, metricsFrom(r)]));
  const campTotals = metricsFrom((campLife.data || [])[0] || {});
  // The metric is "readable" once the account has ever reported it. Before that
  // a zero is ignorance, not a result, and no test is judged a loser on it.
  const visitsReadable  = campTotals.visits > 0;
  const followsReadable = campTotals.follows > 0;
  report.metrics = {
    visitsField: VISITS_FIELD, visitsReadable, followsType: campTotals.followsType, followsReadable,
    campaignLifetime: { spend: campTotals.spend, visits: campTotals.visits, follows: campTotals.follows },
  };
  if (!visitsReadable && campTotals.spend >= 5) {
    warn(`campaign has spent ${usd(campTotals.spend)} and "${VISITS_FIELD}" is still 0 — run --verify and check the metric name`);
  }

  // ── 1. Caps ────────────────────────────────────────────────────────────
  let testsMtd = 0, totalMtd = 0;
  for (const r of mtdRows) {
    const s = num(r.spend);
    totalMtd += s;
    if (/^TEST::/.test(r.adset_name || '')) testsMtd += s;
  }
  let committed = 0;
  for (const t of testAdsets) {
    if (t.effective_status !== 'ACTIVE') continue;
    const spent = (lifeBy.get(t.id) || { spend: 0 }).spend;
    committed += Math.max(0, num(t.lifetime_budget) / 100 - spent);
  }
  report.caps = capState({ testsMtd, totalMtd, committedTests: committed });
  if (report.caps.capReached) warn(`cap reached: ${report.caps.reason} — no new tests this run`);

  // ── 2. Discover posts ──────────────────────────────────────────────────
  const events = db ? await db.events() : [];
  const skippedIds = events.filter(e => e.event === 'skip').map(e => e.media_id);
  const verdictIds = new Set(events.filter(e => e.event === 'verdict').map(e => e.media_id));
  const media = await meta.get(`${IG_USER_ID}/media`,
    { fields: 'id,media_type,media_product_type,timestamp,permalink,caption', limit: 25 });
  const mediaBy = new Map((media.data || []).map(m => [m.id, m]));
  const testedIds = testAdsets.map(a => mediaIdOf(a.name)).filter(Boolean);
  const candidates = findCandidates({ media: media.data || [], testedIds, skippedIds });
  report.candidates = candidates.map(m => ({ id: m.id, type: m.media_type, postedAt: m.timestamp, permalink: m.permalink,
                                             caption: captionOf(m) }));

  // ── 3. Create a test per candidate ─────────────────────────────────────
  let runningCaps = report.caps;
  for (const m of candidates) {
    if (runningCaps.capReached) break;
    const line = `create TEST::${m.id} ($5 lifetime, ${TEST_WINDOW_DAYS}d) on ${m.media_type} ${m.permalink}`;
    const created = await act(line, async () => {
      const start = Math.floor(now.getTime() / 1000);
      const adset = await meta.post(`${ACT}/adsets`, {
        name: `TEST::${m.id}`, campaign_id: CAMPAIGN_ID, status: 'ACTIVE',
        optimization_goal: 'VISIT_INSTAGRAM_PROFILE', destination_type: 'INSTAGRAM_PROFILE',
        billing_event: 'IMPRESSIONS', bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
        lifetime_budget: TEST_BUDGET_CENTS, start_time: start, end_time: start + TEST_WINDOW_DAYS * 86400,
        promoted_object: { page_id: PAGE_ID },
        targeting: champ.targeting,   // copied from the champion, never hand-typed
      });
      try {
        const creative = await meta.post(`${ACT}/adcreatives`, {
          name: `TEST::${m.id}`, object_id: PAGE_ID, instagram_user_id: IG_USER_ID, source_instagram_media_id: m.id,
        });
        const ad = await meta.post(`${ACT}/ads`, {
          name: `TEST::${m.id}`, adset_id: adset.id, status: 'ACTIVE', creative: { creative_id: creative.id },
        });
        return { adsetId: adset.id, creativeId: creative.id, adId: ad.id };
      } catch (e) {
        // Meta refused the post (licensed music, unsupported format…): remove the
        // empty ad set so it never counts as "tested", and remember the refusal.
        try { await meta.del(adset.id); } catch { /* leave it; it has no ad and cannot spend */ }
        await record(m.id, 'skip', { reason: e.message, mediaType: m.media_type, permalink: m.permalink });
        report.skips.push({ mediaId: m.id, permalink: m.permalink, reason: e.message });
        return null;
      }
    });
    if (created || dryRun) {
      report.created.push({ mediaId: m.id, permalink: m.permalink, type: m.media_type, ...(created || {}) });
      if (created) await record(m.id, 'created', { ...created, permalink: m.permalink });
      runningCaps = capState({ testsMtd, totalMtd, committedTests: committed += TEST_BUDGET_CENTS / 100 });
    }
  }

  // ── Champion state (needed by 4, 5, 6) ─────────────────────────────────
  const championAds = await meta.all(`${CHAMPION_ADSET_ID}/ads`,
    { fields: 'id,name,status,effective_status,created_time,creative{source_instagram_media_id}' });
  const adMedia = (a) => (a.creative && a.creative.source_instagram_media_id) || mediaIdOf(a.name);
  const activeChampionAds = championAds.filter(a => a.status === 'ACTIVE');
  const since = ymd(daysAgo(CHAMPION_WINDOW_DAYS - 1, now)), until = ymd(now);
  const champ7 = await meta.get(`${CHAMPION_ADSET_ID}/insights`,
    { time_range: { since, until }, fields: `spend,impressions,actions,${VISITS_FIELD}` });
  const c7 = metricsFrom((champ7.data || [])[0] || {});
  const championCpv = c7.visits > 0 ? round2(c7.spend / c7.visits) : null;
  const describeMedia = async (id) => {
    if (!id) return null;
    if (mediaBy.has(id)) { const m = mediaBy.get(id); return { id, permalink: m.permalink, caption: captionOf(m), postedAt: m.timestamp }; }
    try { const m = await meta.get(id, { fields: 'permalink,caption,timestamp' });
          return { id, permalink: m.permalink, caption: captionOf(m), postedAt: m.timestamp }; }
    catch { return { id }; }
  };
  report.champion = {
    adsetStatus: champ.effective_status, dailyBudget: num(champ.daily_budget) / 100,
    window: { since, until, days: CHAMPION_WINDOW_DAYS },
    spend: c7.spend, visits: c7.visits, follows: c7.follows, costPerVisit: championCpv,
    costPerFollow: followsReadable && c7.follows > 0 ? round2(c7.spend / c7.follows) : null,
    followsReadable,
    activeAds: await Promise.all(activeChampionAds.map(async a => ({ adId: a.id, name: a.name, media: await describeMedia(adMedia(a)) }))),
  };

  // ── 4 + 5. Evaluate finished tests, promote winners ───────────────────
  let championForVerdicts = { costPerVisit: championCpv, hasActive: activeChampionAds.length > 0 };
  const promote = async (mediaId, source) => {
    const line = `promote ${mediaId} → CHAMPION::${mediaId}; pause + retire ${activeChampionAds.length} other champion ad(s)`;
    await act(line, async () => {
      const creative = await meta.post(`${ACT}/adcreatives`, {
        name: `CHAMPION::${mediaId}`, object_id: PAGE_ID, instagram_user_id: IG_USER_ID, source_instagram_media_id: mediaId,
      });
      const ad = await meta.post(`${ACT}/ads`, {
        name: `CHAMPION::${mediaId}`, adset_id: CHAMPION_ADSET_ID, status: 'ACTIVE', creative: { creative_id: creative.id },
      });
      for (const a of activeChampionAds) {
        await meta.post(a.id, { status: 'PAUSED', name: `RETIRED::${adMedia(a) || a.id}` });
      }
      await record(mediaId, 'promote', { adId: ad.id, creativeId: creative.id, retired: activeChampionAds.map(a => a.id), source });
      activeChampionAds.length = 0; activeChampionAds.push(ad);
      return ad;
    });
    championForVerdicts = { costPerVisit: null, hasActive: true }; // a fresh champion has no window yet; later tests wait for real numbers
  };

  for (const t of testAdsets) {
    const mediaId = mediaIdOf(t.name);
    const life = lifeBy.get(t.id) || metricsFrom({});
    const row = {
      adsetId: t.id, mediaId, status: t.effective_status, createdAt: t.created_time, endTime: t.end_time,
      spend: life.spend, visits: life.visits, impressions: life.impressions,
      costPerVisit: life.visits > 0 ? round2(life.spend / life.visits) : null,
      media: await describeMedia(mediaId), phase: null, verdict: null,
    };
    if (verdictIds.has(mediaId)) {
      row.phase = 'done';
      row.verdict = (events.filter(e => e.event === 'verdict' && e.media_id === mediaId).pop() || {}).detail || null;
      report.tests.push(row); continue;
    }
    row.phase = testPhase({ spend: life.spend, endTime: t.end_time }, now);
    if (row.phase === 'ready') {
      const v = verdict({ spend: life.spend, visits: life.visits, visitsReadable }, championForVerdicts);
      row.verdict = v;
      report.verdicts.push({ mediaId, adsetId: t.id, ...v, spend: life.spend, visits: life.visits, permalink: row.media && row.media.permalink });
      if (v.result === 'win') await promote(mediaId, { testAdset: t.id, spend: life.spend, visits: life.visits });
      if (v.result !== 'unmeasured') {
        if (t.status !== 'PAUSED') await act(`pause finished TEST::${mediaId} (${v.result})`, () => meta.post(t.id, { status: 'PAUSED' }));
        await record(mediaId, 'verdict', { ...v, spend: life.spend, visits: life.visits, adsetId: t.id });
      }
    }
    report.tests.push(row);
  }

  // ── 5b. First-run pair ────────────────────────────────────────────────
  const adLife = await meta.all(`${CHAMPION_ADSET_ID}/insights`,
    { level: 'ad', date_preset: 'maximum', fields: `ad_id,ad_name,spend,actions,${VISITS_FIELD}` });
  const adLifeBy = new Map(adLife.map(r => [r.ad_id, metricsFrom(r)]));
  const pairAds = championAds.map(a => ({ id: a.id, name: a.name, mediaId: adMedia(a), active: a.status === 'ACTIVE',
                                          ...(adLifeBy.get(a.id) || { spend: 0, visits: 0 }) }));
  const pair = pairDecision(pairAds);
  report.pair = { ...pair, ads: pairAds.filter(a => FIRST_RUN_PAIR.includes(a.mediaId))
                                         .map(a => ({ adId: a.id, mediaId: a.mediaId, active: a.active, spend: a.spend, visits: a.visits,
                                                      costPerVisit: a.visits > 0 ? round2(a.spend / a.visits) : null })) };
  if (pair.resolved) {
    await act(`first-run pair resolved: keep ${pair.keep.mediaId} as CHAMPION, retire ${pair.retire.mediaId} (${pair.reason})`, async () => {
      await meta.post(pair.keep.id, { name: `CHAMPION::${pair.keep.mediaId}` });
      await meta.post(pair.retire.id, { status: 'PAUSED', name: `RETIRED::${pair.retire.mediaId}` });
      await record(pair.keep.mediaId, 'pair_resolved', { kept: pair.keep.id, retired: pair.retire.id, reason: pair.reason });
    });
  }

  // ── 6. Champion health ────────────────────────────────────────────────
  const health = championHealth({ spend: c7.spend, visits: c7.visits, follows: c7.follows, followsReadable });
  report.champion.health = health;
  if (health.action === 'pause' && activeChampionAds.length) {
    await act(`PAUSE champion ad(s) ${activeChampionAds.map(a => a.id).join(', ')} — ${health.reason}`, async () => {
      for (const a of activeChampionAds) await meta.post(a.id, { status: 'PAUSED' });
      await record(adMedia(activeChampionAds[0]), 'champion_paused', { ads: activeChampionAds.map(a => a.id), ...health });
    });
  } else if (health.action === 'scale_candidate') {
    const already = events.some(e => e.event === 'scale_candidate' && new Date(e.at) > daysAgo(1, now));
    if (!already) await record(adMedia(activeChampionAds[0]), 'scale_candidate', health);
  }
  if (!activeChampionAds.length && !dryRun) warn('champion slot is EMPTY — nothing is running at $6.50/day until a test wins');

  // ── 7. Report ─────────────────────────────────────────────────────────
  report.events24h = events.filter(e => new Date(e.at) > daysAgo(1, now))
                           .map(e => ({ at: e.at, mediaId: e.media_id, event: e.event, detail: e.detail }));

  if (verify) {
    const perAd = await meta.all(`${CAMPAIGN_ID}/insights`,
      { level: 'ad', date_preset: 'maximum', fields: `ad_id,ad_name,adset_name,spend,impressions,actions,cost_per_action_type,${VISITS_FIELD}` });
    report.verify = {
      pinned: { visitsField: VISITS_FIELD, visitActionFallbacks: VISIT_ACTION_TYPES, followActionCandidates: FOLLOW_ACTION_TYPES },
      campaign: { spend: campTotals.spend, [VISITS_FIELD]: (campLife.data || [])[0]?.[VISITS_FIELD] ?? null,
                  actionTypes: ((campLife.data || [])[0]?.actions || []).map(a => `${a.action_type}=${a.value}`) },
      ads: perAd.map(r => ({ ad: r.ad_name, adset: r.adset_name, spend: r.spend, [VISITS_FIELD]: r[VISITS_FIELD] ?? null,
                             actionTypes: (r.actions || []).map(a => `${a.action_type}=${a.value}`) })),
      howToMatch: 'Ads Manager → Columns → Customize → search "Instagram profile visits" and "Follows" for the same date range; the API string whose count equals the column is the metric.',
    };
  }
  return report;
}

// ============================================================
// HUMAN SUMMARY
// ============================================================

function summarise(r) {
  const L = [];
  L.push(`AUTO-BOOST ${r.dryRun ? 'DRY RUN' : 'LIVE'} — ${r.generatedAt}  (AUTO_BOOST_ENABLED=${r.enabled ? 1 : 0})`);
  const c = r.caps;
  L.push(`Caps: tests ${usd(c.testsMtd)} spent + ${usd(c.testsCommitted - c.testsMtd)} committed of ${usd(c.testsCap)}; total ${usd(c.totalMtd)} of ${usd(c.totalCap)}${c.capReached ? ` — CAP REACHED (${c.reason})` : ''}`);
  const ch = r.champion;
  L.push(`Champion (${ch.window.days}d): ${usd(ch.spend)} spend, ${ch.visits} visits${ch.costPerVisit !== null ? ` (${usd(ch.costPerVisit)}/visit)` : ''}, `
       + `${ch.followsReadable ? `${ch.follows} follows${ch.costPerFollow !== null ? ` (${usd(ch.costPerFollow)}/follow)` : ''}` : 'follows not readable yet'}; `
       + `active ads: ${ch.activeAds.length ? ch.activeAds.map(a => a.name).join(', ') : 'NONE'}; health: ${ch.health.action} — ${ch.health.reason}`);
  if (r.pair) L.push(`First-run pair: ${r.pair.resolved ? 'RESOLVED' : 'open'} — ${r.pair.reason}`);
  L.push(`Candidates (new posts since ${SYSTEM_START} with no test): ${r.candidates.length}`);
  for (const m of r.candidates) L.push(`   ${m.id} ${m.type} ${m.postedAt.slice(0, 10)} "${m.caption}"`);
  L.push(`Tests in flight: ${r.tests.filter(t => t.phase === 'running').length}, judged this run: ${r.verdicts.length}, done before: ${r.tests.filter(t => t.phase === 'done').length}`);
  for (const t of r.tests) L.push(`   TEST::${t.mediaId} ${t.phase} ${usd(t.spend)} ${t.visits} visits${t.costPerVisit !== null ? ` ${usd(t.costPerVisit)}/visit` : ''}${t.verdict ? ` → ${t.verdict.result}: ${t.verdict.reason}` : ''}`);
  if (r.skips.length) for (const s of r.skips) L.push(`   SKIP ${s.mediaId}: ${s.reason}`);
  L.push(`Actions (${r.actions.length}):`);
  for (const a of r.actions) L.push(`   ${a}`);
  if (!r.actions.length) L.push('   none');
  for (const w of r.warnings) L.push(`⚠ ${w}`);
  L.push(`Metrics: visits via "${r.metrics.visitsField}" (${r.metrics.visitsReadable ? 'readable' : 'NOT YET OBSERVED'}), follows via ${r.metrics.followsType || 'no follow-type action observed yet'}`);
  return L.join('\n');
}

// ============================================================
// MAIN
// ============================================================

async function main() {
  loadSecrets();
  const argv = process.argv.slice(2);
  const argOf = (flag) => { const i = argv.indexOf(flag); return i >= 0 ? argv[i + 1] : null; };
  const enabled = process.env.AUTO_BOOST_ENABLED === '1';
  const dryRun  = argv.includes('--dry-run') || !enabled;
  const verify  = argv.includes('--verify');
  const outPath = argOf('--out') || OUT_DEFAULT;

  const token = process.env.META_ADS_TOKEN, secret = process.env.META_APP_SECRET;
  if (!token || !secret) throw new Error('META_ADS_TOKEN and META_APP_SECRET are required (env or ~/.absbyai-secrets.env)');
  const meta = makeMeta(token, secret);
  // On Dan's Mac the internal Railway host does not resolve, so the public proxy
  // URL (DATABASE_PUBLIC_URL in the secrets file) wins when present. The Railway
  // cron service is given only DATABASE_URL (internal), so it takes the fast path.
  const db = makeDb(process.env.DATABASE_PUBLIC_URL || process.env.DATABASE_URL);
  if (!db) console.log('  ⚠ no DATABASE_URL — skips and verdicts will not persist this run');
  if (db) await db.ensureSchema();

  let report;
  try {
    report = await runJob({ meta, db, dryRun, enabled, verify });
  } catch (e) {
    report = { generatedAt: new Date().toISOString(), dryRun, enabled, error: e.message, meta: e.meta || null };
    console.error('auto-boost failed:', e.stack || e.message);
  }
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2) + '\n');
  if (db) { try { await db.run(report, dryRun, enabled); } catch (e) { console.error('could not record run:', e.message); } await db.close(); }

  if (report.error) { process.exitCode = 1; return; }
  console.log(summarise(report));
  if (verify) console.log('\nVERIFY:\n' + JSON.stringify(report.verify, null, 2));
  if (argv.includes('--print')) console.log(JSON.stringify(report, null, 2));
}

module.exports = {
  metricsFrom, capState, findCandidates, testPhase, verdict, championHealth, pairDecision, summarise,
  CONFIG: { SYSTEM_START, FIRST_RUN_PAIR, TEST_BUDGET_CENTS, TEST_WINDOW_DAYS, TEST_EVAL_SPEND, CAP_TESTS_MTD, CAP_TOTAL_MTD,
            PROMOTE_MIN_VISITS, CHAMPION_MIN_SPEND, CHAMPION_KILL_CPF, CHAMPION_SCALE_CPF, PAIR_MIN_SPEND, VISITS_FIELD, FOLLOW_ACTION_TYPES },
};

if (require.main === module) main().catch(e => { console.error('auto-boost crashed:', e.stack || e.message); process.exit(1); });
