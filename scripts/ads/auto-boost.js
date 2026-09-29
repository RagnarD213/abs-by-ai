#!/usr/bin/env node
/* eslint-disable no-console */
//
// IG AUTO-BOOST: every new @danrosefit post gets a $10 lifetime "profile visits"
// test ad on the REAL post; one champion ad runs at $6.50/day; tests and the
// champion are ranked on ESTIMATED COST PER FOLLOWER, a test that beats the
// champion replaces it. Caps: $300/month on tests, $500/month total.
//
// Design locked with Dan 2026-09-02: Handoffs/handoff-20260902-ig-auto-boost.md.
// Changed by Dan 2026-09-29 ($10 tests, champion on cost per follower):
// Handoffs/handoff-20260929-ig-autoboost-cost-per-follower.md.
// The numbers below are HIS decisions, not tunables — change them only if he does.
//
// HOW FOLLOWS ARE ESTIMATED (method B, Docs/AUTO_BOOST.md): Meta's ads insights
// carry no follow count, and Instagram's per-post `follows` counts organic follows
// only (and is refused on reels). So each day's new followers (IG `follower_count`,
// period=day, persisted to Postgres because the API only keeps ~30 days) are split
// across that day's running ads in proportion to their profile visits. Organic
// follows are spread the same way, so the number RANKS posts; it is not a true cost.
//
// RUN:   node scripts/ads/auto-boost.js [--dry-run] [--verify] [--out PATH] [--print]
//   Hourly Railway cron ("15 * * * *", service `auto-boost`, must exit when done).
//   --dry-run   plan everything, write NOTHING to Meta, and do not record events.
//               The run report is still written locally (brief-autoboost.json) and
//               to Postgres flagged dry_run=true, so the morning brief can show what
//               the system WOULD have done while it is switched off.
//   --backfill  read-only: estimated cost per follower for every post the campaign
//               ran in the last 30 days, by post and by type (IMAGE vs REEL).
//   --verify    print every insights action type Meta returns for the campaign, per
//               ad, next to the pinned metric names — for matching the API strings
//               to Ads Manager's "Instagram profile visits" and "Follows or likes"
//               columns once real data exists. Read-only.
//   AUTO_BOOST_ENABLED=1 in the environment is what makes it live. Anything else
//   behaves as --dry-run. This is the single switch.
//
// META IS THE LEDGER. The Instagram media id lives in the ad-set name
// ("REEL | <title> | TEST::<media_id>" — type first, Dan's rule 2026-09-08), so "has this post been tested?" is answered by Meta, never
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

const TEST_BUDGET_CENTS   = 1000;    // $10 lifetime per post (Dan, 2026-09-29; was $5)
const TEST_WINDOW_DAYS    = 5;       // evaluate at end_time at the latest
const TEST_EVAL_SPEND     = 9.00;    // ...or as soon as this much is spent
const CHAMPION_DAILY_CENTS = 650;    // $6.50/day ≈ $200/month — verified, not set, here
const CAP_TESTS_MTD       = 300;     // stop creating tests past this
const CAP_TOTAL_MTD       = 500;     // ...or this, champion included
const PROMOTE_MIN_FOLLOWS = 2;       // estimated follows a test needs to be believed (Claude's default, 2026-09-29:
                                     // at ~$3 a follower $10 buys ~3, so fewer is noise)
const FOLLOW_SETTLE_DAYS  = 2;       // a day's follower count is trusted once it is this many days old
const FOLLOWER_HISTORY_DAYS = 29;    // IG returns at most 30 days of follower_count per call
const CHAMPION_MIN_SPEND  = 35;      // 7-day spend before the champion is judged
const CHAMPION_KILL_CPF   = 5.00;    // pause at > $5 per estimated follower
const CHAMPION_SCALE_CPF  = 3.00;    // report as scale candidate at < $3 per follower (never auto-scaled)
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
// ── Names (Dan's rule 2026-09-08): "<TYPE> | <title> | <TAG>::<media_id>" ──
// The post type comes FIRST so a reel and an image can be told apart at a glance,
// then the title (first sentence of the caption), then the machine tag. The tag
// stays in the name because the media id in the name IS the ledger.
const TYPE_LABEL = { VIDEO: 'REEL', IMAGE: 'IMAGE', CAROUSEL_ALBUM: 'CAROUSEL' };
const typeLabel  = (m) => TYPE_LABEL[(m && m.media_type) || ''] || String((m && m.media_type) || 'POST').toUpperCase();
const titleOf    = (m) => {
  const c = String((m && m.caption) || '').replace(/\s+/g, ' ').trim();
  const first = (c.split(/(?<=[.!?])\s+/)[0] || c).replace(/[.!?]+$/, '').trim();
  const t = first.length > 60 ? first.slice(0, 57).replace(/\s+\S*$/, '') + '…' : first;
  return t || 'untitled';
};
const nameFor    = (m, tag) => `${typeLabel(m)} | ${titleOf(m)} | ${tag}::${m.id}`;
const tagOf      = (name) => { const m = /\b(TEST|CHAMPION|RETIRED)::\d+/.exec(name || ''); return m ? m[1] : null; };
const isTest     = (adset) => tagOf(adset.name) === 'TEST';

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

// IG `follower_count` (period=day) values -> { 'YYYY-MM-DD': new followers }.
// Meta stamps each value with the END of its day (07:00 UTC = midnight Pacific),
// so the day a value counts is the calendar day before its end_time.
function followerDaysFrom(values) {
  const out = {};
  for (const v of values || []) {
    if (!v || !v.end_time) continue;
    out[ymd(new Date(v.end_time).getTime() - 86400e3)] = num(v.value);
  }
  return out;
}

// Method B. Each settled day's new followers are split across that day's ads in
// proportion to their profile visits. adDays = [{ day, spend, visits, ... }].
// Returns the rows with `estFollows` set, or null when the day is not settled
// yet (younger than FOLLOW_SETTLE_DAYS) or has no follower reading.
function attributeFollows(adDays, followsByDay, settledThrough) {
  const visitsByDay = {};
  for (const r of adDays || []) visitsByDay[r.day] = (visitsByDay[r.day] || 0) + num(r.visits);
  return (adDays || []).map(r => {
    const f = (followsByDay || {})[r.day];
    if (r.day > settledThrough || f === undefined) return { ...r, estFollows: null };
    return { ...r, estFollows: visitsByDay[r.day] > 0 ? f * num(r.visits) / visitsByDay[r.day] : 0 };
  });
}

// Sum attributed rows for one post / ad set. Cost per follower divides only the
// spend on SETTLED days by the follows estimated for those days.
function followStats(rows) {
  let spend = 0, visits = 0, settledSpend = 0, unsettledSpend = 0, estFollows = 0, lastSpendDay = null;
  for (const r of rows || []) {
    spend += num(r.spend); visits += num(r.visits);
    if (num(r.spend) > 0 && (!lastSpendDay || r.day > lastSpendDay)) lastSpendDay = r.day;
    if (r.estFollows === null || r.estFollows === undefined) unsettledSpend += num(r.spend);
    else { settledSpend += num(r.spend); estFollows += r.estFollows; }
  }
  return {
    spend: round2(spend), visits, settledSpend: round2(settledSpend), unsettledSpend: round2(unsettledSpend),
    estFollows: Math.round(estFollows * 10) / 10,
    costPerFollow: estFollows > 0 ? round2(settledSpend / estFollows) : null,
    costPerVisit: visits > 0 ? round2(spend / visits) : null,
    settled: unsettledSpend === 0, lastSpendDay,
  };
}

// The verdict on one finished test against the champion's trailing window.
//   test     = followStats(...) + { followsReadable }
//   champion = { costPerFollow: number|null, hasActive: boolean }
// Results: win / lose (recorded, final), wait / unmeasured (not recorded, re-judged next run).
function verdict(test, champion) {
  const est = Math.round(num(test.estFollows) * 10) / 10;
  const cpf = est > 0 ? round2(test.settledSpend / test.estFollows) : null;
  const base = { costPerFollow: cpf, estFollows: est, costPerVisit: test.visits > 0 ? round2(test.spend / test.visits) : null };
  if (!test.followsReadable) {
    return { ...base, result: 'unmeasured', reason: 'follower counts not readable from Instagram, not judged' };
  }
  if (!test.settled) {
    return { ...base, result: 'wait',
             reason: `follower count for ${test.lastSpendDay || 'its last day'} not settled yet (${FOLLOW_SETTLE_DAYS}-day lag), judged when it is` };
  }
  if (est < PROMOTE_MIN_FOLLOWS) {
    return { ...base, result: 'lose',
             reason: `${est} estimated follows on ${usd(test.spend)}, needs ${PROMOTE_MIN_FOLLOWS} to be believed` };
  }
  if (!champion || !champion.hasActive || champion.costPerFollow === null || champion.costPerFollow === undefined) {
    return { ...base, result: 'win',
             reason: `${usd(cpf)}/follower on ${est} estimated follows and the champion slot is empty` };
  }
  if (cpf < champion.costPerFollow) {
    return { ...base, result: 'win',
             reason: `${usd(cpf)}/follower beats the champion's ${usd(champion.costPerFollow)}/follower (${est} estimated follows)` };
  }
  return { ...base, result: 'lose',
           reason: `${usd(cpf)}/follower does not beat the champion's ${usd(champion.costPerFollow)}/follower (ties keep the champion)` };
}

// Champion health over the trailing settled window.
//   stats = { spend, visits, follows, followsReadable }: follows are ESTIMATED (method B)
function championHealth(stats) {
  const cpv = stats.visits > 0 ? round2(stats.spend / stats.visits) : null;
  const cpf = stats.followsReadable && stats.follows > 0 ? round2(stats.spend / stats.follows) : null;
  const base = { costPerVisit: cpv, costPerFollow: cpf, followsReadable: !!stats.followsReadable };
  if (!stats.followsReadable) {
    return { ...base, action: 'unjudged',
             reason: 'follower counts not readable from Instagram, no kill rule applied' };
  }
  if (stats.spend < CHAMPION_MIN_SPEND) {
    return { ...base, action: 'ok', reason: `${usd(stats.spend)} in ${CHAMPION_WINDOW_DAYS} settled days, under the ${usd(CHAMPION_MIN_SPEND)} judging floor` };
  }
  const effectiveCpf = stats.follows > 0 ? stats.spend / stats.follows : Infinity;
  if (effectiveCpf > CHAMPION_KILL_CPF) {
    return { ...base, action: 'pause',
             reason: `${stats.follows === 0 ? 'zero estimated follows' : usd(effectiveCpf) + '/follower'} on ${usd(stats.spend)}, over the ${usd(CHAMPION_KILL_CPF)}/follower kill line` };
  }
  if (effectiveCpf < CHAMPION_SCALE_CPF) {
    return { ...base, action: 'scale_candidate',
             reason: `${usd(effectiveCpf)}/follower (estimated) on ${usd(stats.spend)}, under the ${usd(CHAMPION_SCALE_CPF)}/follower scale line (budget cap is fixed; reported only)` };
  }
  return { ...base, action: 'ok', reason: `${usd(effectiveCpf)}/follower (estimated) on ${usd(stats.spend)}` };
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
        CREATE TABLE IF NOT EXISTS auto_boost_follows_daily (
          day        DATE PRIMARY KEY,
          follows    INTEGER NOT NULL,
          fetched_at TIMESTAMPTZ NOT NULL DEFAULT now()
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
    // Instagram keeps ~30 days of follower_count; every run upserts what it can
    // see (late data overwrites the provisional value) so the history outlives it.
    async saveFollows(byDay) {
      for (const [day, follows] of Object.entries(byDay || {})) {
        await pool.query(`INSERT INTO auto_boost_follows_daily (day, follows) VALUES ($1, $2)
                          ON CONFLICT (day) DO UPDATE SET follows = EXCLUDED.follows, fetched_at = now()`, [day, follows]);
      }
    },
    async follows() {
      const r = await pool.query("SELECT to_char(day, 'YYYY-MM-DD') AS day, follows FROM auto_boost_follows_daily");
      return Object.fromEntries(r.rows.map(x => [x.day, Number(x.follows)]));
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
// FOLLOWS + DAILY AD ROWS (method B inputs)
// ============================================================

// New followers per day: Instagram's last 30 days, persisted and merged with the
// stored history. readable=false (and a reason) when Instagram refuses.
async function loadFollowerDays({ meta, db, now }) {
  let fresh = {}, error = null;
  try {
    const r = await meta.get(`${IG_USER_ID}/insights`, {
      metric: 'follower_count', period: 'day',
      since: Math.floor(daysAgo(FOLLOWER_HISTORY_DAYS, now).getTime() / 1000), until: Math.floor(now.getTime() / 1000),
    });
    fresh = followerDaysFrom(((r.data || [])[0] || {}).values);
  } catch (e) { error = e.message; }
  let byDay = fresh;
  if (db) {
    if (Object.keys(fresh).length) await db.saveFollows(fresh);
    byDay = { ...(await db.follows()), ...fresh };
  }
  return { byDay, readable: !error && Object.keys(byDay).length > 0, error };
}

// Spend + profile visits per ad per day for the whole campaign, last 30 days.
async function loadAdDays({ meta, now }) {
  const rows = await meta.all(`${CAMPAIGN_ID}/insights`, {
    level: 'ad', time_increment: 1,
    time_range: { since: ymd(daysAgo(FOLLOWER_HISTORY_DAYS, now)), until: ymd(now) },
    fields: `ad_id,ad_name,adset_id,adset_name,spend,actions,${VISITS_FIELD}`,
  });
  return rows.map(r => {
    const m = metricsFrom(r);
    return { day: r.date_start, adId: r.ad_id, adsetId: r.adset_id, adsetName: r.adset_name,
             mediaId: mediaIdOf(r.ad_name) || mediaIdOf(r.adset_name), spend: m.spend, visits: m.visits };
  });
}

const settledThroughFor = (now) => ymd(daysAgo(FOLLOW_SETTLE_DAYS, now));

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
  // Follows: method B (see the header). Tests and the champion are judged only on
  // days whose follower count has settled.
  const [followerDays, adDaysRaw] = await Promise.all([loadFollowerDays({ meta, db, now }), loadAdDays({ meta, now })]);
  const settledThrough  = settledThroughFor(now);
  const adDays          = attributeFollows(adDaysRaw, followerDays.byDay, settledThrough);
  const followsReadable = followerDays.readable && visitsReadable;
  const recentFollowDays = Object.keys(followerDays.byDay).sort().slice(-14).map(d => ({ day: d, follows: followerDays.byDay[d] }));
  report.metrics = {
    visitsField: VISITS_FIELD, visitsReadable, followsReadable,
    followsSource: 'Instagram follower_count per day, split across that day\'s ads by profile-visit share (estimate, for ranking)',
    settledThrough, followerDays: recentFollowDays, followerError: followerDays.error,
    campaignLifetime: { spend: campTotals.spend, visits: campTotals.visits },
  };
  if (!followerDays.readable) warn(`follower counts not readable from Instagram (${followerDays.error || 'no rows'}), no test is judged and no kill rule applies`);
  if (!visitsReadable && campTotals.spend >= 5) {
    warn(`campaign has spent ${usd(campTotals.spend)} and "${VISITS_FIELD}" is still 0 — run --verify and check the metric name`);
  }

  // ── 1. Caps ────────────────────────────────────────────────────────────
  let testsMtd = 0, totalMtd = 0;
  for (const r of mtdRows) {
    const s = num(r.spend);
    totalMtd += s;
    if (tagOf(r.adset_name) === 'TEST') testsMtd += s;
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
  report.candidates = candidates.map(m => ({ id: m.id, type: m.media_type, label: nameFor(m, 'TEST'), postedAt: m.timestamp,
                                             permalink: m.permalink, caption: captionOf(m) }));

  // ── 3. Create a test per candidate ─────────────────────────────────────
  let runningCaps = report.caps;
  for (const m of candidates) {
    if (runningCaps.capReached) break;
    const label = nameFor(m, 'TEST');
    const line = `create "${label}" (${usd(TEST_BUDGET_CENTS / 100)} lifetime, ${TEST_WINDOW_DAYS}d) ${m.permalink}`;
    const created = await act(line, async () => {
      const start = Math.floor(now.getTime() / 1000);
      const adset = await meta.post(`${ACT}/adsets`, {
        name: label, campaign_id: CAMPAIGN_ID, status: 'ACTIVE',
        optimization_goal: 'VISIT_INSTAGRAM_PROFILE', destination_type: 'INSTAGRAM_PROFILE',
        billing_event: 'IMPRESSIONS', bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
        lifetime_budget: TEST_BUDGET_CENTS, start_time: start, end_time: start + TEST_WINDOW_DAYS * 86400,
        promoted_object: { page_id: PAGE_ID },
        targeting: champ.targeting,   // copied from the champion, never hand-typed
      });
      try {
        const creative = await meta.post(`${ACT}/adcreatives`, {
          name: label, object_id: PAGE_ID, instagram_user_id: IG_USER_ID, source_instagram_media_id: m.id,
        });
        const ad = await meta.post(`${ACT}/ads`, {
          name: label, adset_id: adset.id, status: 'ACTIVE', creative: { creative_id: creative.id },
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
      report.created.push({ mediaId: m.id, label, permalink: m.permalink, type: m.media_type, ...(created || {}) });
      if (created) await record(m.id, 'created', { ...created, permalink: m.permalink });
      runningCaps = capState({ testsMtd, totalMtd, committedTests: committed += TEST_BUDGET_CENTS / 100 });
    }
  }

  // ── Champion state (needed by 4, 5, 6) ─────────────────────────────────
  const championAds = await meta.all(`${CHAMPION_ADSET_ID}/ads`,
    { fields: 'id,name,status,effective_status,created_time,creative{source_instagram_media_id}' });
  const adMedia = (a) => (a.creative && a.creative.source_instagram_media_id) || mediaIdOf(a.name);
  const activeChampionAds = championAds.filter(a => a.status === 'ACTIVE');
  // The champion's window is the last 7 SETTLED days, so its cost per follower is
  // measured on the same footing as a test's.
  const until = settledThrough;
  const since = ymd(daysAgo(CHAMPION_WINDOW_DAYS - 1, new Date(`${until}T12:00:00Z`)));
  const c7 = followStats(adDays.filter(r => r.adsetId === CHAMPION_ADSET_ID && r.day >= since && r.day <= until));
  const championCpf = followsReadable ? c7.costPerFollow : null;
  // The raw media object for any id — from this run's /media page when it is
  // there, otherwise fetched once and cached. `{ id }` alone when Meta cannot
  // return it (deleted post), which names as "POST | untitled | TAG::id".
  const mediaCache = new Map();
  const mediaFull = async (id) => {
    if (!id) return null;
    if (mediaBy.has(id)) return mediaBy.get(id);
    if (mediaCache.has(id)) return mediaCache.get(id);
    let m;
    try { m = await meta.get(id, { fields: 'id,media_type,media_product_type,permalink,caption,timestamp' }); }
    catch { m = { id }; }
    mediaCache.set(id, m);
    return m;
  };
  const describeMedia = async (id) => {
    const m = await mediaFull(id);
    if (!m) return null;
    return { id, type: m.media_type || null, permalink: m.permalink, caption: captionOf(m), title: titleOf(m), postedAt: m.timestamp };
  };

  // ── Names are the ledger: heal any that drift from the convention ──────
  // Renames only — never a status or budget change. Covers ad sets and ads
  // created before the naming rule (2026-09-08) and anything renamed by hand.
  const healName = async (obj, expected, what) => {
    if (!obj || obj.name === expected) return;
    await act(`rename ${what} "${obj.name}" → "${expected}"`, () => meta.post(obj.id, { name: expected }));
    obj.name = expected;
  };
  for (const t of testAdsets) {
    const expected = nameFor(await mediaFull(mediaIdOf(t.name)), 'TEST');
    if (t.name !== expected) {
      await healName(t, expected, 'test ad set');
      for (const ad of await meta.all(`${t.id}/ads`, { fields: 'id,name' })) await healName(ad, expected, 'test ad');
    }
  }
  for (const a of championAds) {
    const tag = tagOf(a.name) === 'RETIRED' || a.status === 'PAUSED' ? 'RETIRED' : 'CHAMPION';
    await healName(a, nameFor(await mediaFull(adMedia(a)), tag), 'champion ad');
  }
  report.champion = {
    adsetStatus: champ.effective_status, dailyBudget: num(champ.daily_budget) / 100,
    window: { since, until, days: CHAMPION_WINDOW_DAYS },
    spend: c7.spend, visits: c7.visits, follows: c7.estFollows, followsEstimated: true, costPerVisit: c7.costPerVisit,
    costPerFollow: championCpf, followsReadable,
    activeAds: await Promise.all(activeChampionAds.map(async a => ({ adId: a.id, name: a.name, media: await describeMedia(adMedia(a)) }))),
  };

  // ── 4 + 5. Evaluate finished tests, promote winners ───────────────────
  let championForVerdicts = { costPerFollow: championCpf, hasActive: activeChampionAds.length > 0 };
  const promote = async (mediaId, source) => {
    const label = nameFor(await mediaFull(mediaId), 'CHAMPION');
    const line = `promote "${label}"; pause + retire ${activeChampionAds.length} other champion ad(s)`;
    await act(line, async () => {
      const creative = await meta.post(`${ACT}/adcreatives`, {
        name: label, object_id: PAGE_ID, instagram_user_id: IG_USER_ID, source_instagram_media_id: mediaId,
      });
      const ad = await meta.post(`${ACT}/ads`, {
        name: label, adset_id: CHAMPION_ADSET_ID, status: 'ACTIVE', creative: { creative_id: creative.id },
      });
      for (const a of activeChampionAds) {
        await meta.post(a.id, { status: 'PAUSED', name: nameFor(await mediaFull(adMedia(a)) || { id: a.id }, 'RETIRED') });
      }
      await record(mediaId, 'promote', { adId: ad.id, creativeId: creative.id, retired: activeChampionAds.map(a => a.id), source });
      activeChampionAds.length = 0; activeChampionAds.push(ad);
      return ad;
    });
    // Later tests judged in this same run must beat the test that just won — not
    // an empty window (which `verdict` treats as a win by default). Tests are also
    // ranked cheapest-first below, so the best of a batch wins and the rest lose.
    championForVerdicts = { costPerFollow: (source && source.costPerFollow) || null, hasActive: true };
  };
  const statsBy = new Map(testAdsets.map(t => [t.id, followStats(adDays.filter(r => r.adsetId === t.id))]));
  const cpfOf = (t) => { const st = statsBy.get(t.id); return st.costPerFollow === null ? Infinity : st.costPerFollow; };
  testAdsets.sort((a, b) => cpfOf(a) - cpfOf(b));

  for (const t of testAdsets) {
    const mediaId = mediaIdOf(t.name);
    const life = lifeBy.get(t.id) || metricsFrom({});
    const row = {
      adsetId: t.id, mediaId, label: t.name, status: t.effective_status, createdAt: t.created_time, endTime: t.end_time,
      spend: life.spend, visits: life.visits, impressions: life.impressions,
      costPerVisit: life.visits > 0 ? round2(life.spend / life.visits) : null,
      estFollows: statsBy.get(t.id).estFollows, costPerFollow: followsReadable ? statsBy.get(t.id).costPerFollow : null,
      media: await describeMedia(mediaId), phase: null, verdict: null,
    };
    if (verdictIds.has(mediaId)) {
      row.phase = 'done';
      row.verdict = (events.filter(e => e.event === 'verdict' && e.media_id === mediaId).pop() || {}).detail || null;
      report.tests.push(row); continue;
    }
    row.phase = testPhase({ spend: life.spend, endTime: t.end_time }, now);
    if (row.phase === 'ready') {
      const v = verdict({ ...statsBy.get(t.id), followsReadable }, championForVerdicts);
      row.verdict = v;
      if (v.result === 'win' || v.result === 'lose') {
        report.verdicts.push({ mediaId, adsetId: t.id, ...v, spend: life.spend, visits: life.visits, permalink: row.media && row.media.permalink });
        if (v.result === 'win') await promote(mediaId, { testAdset: t.id, spend: life.spend, visits: life.visits, estFollows: v.estFollows, costPerFollow: v.costPerFollow });
        if (t.status !== 'PAUSED') await act(`pause finished "${t.name}" (${v.result})`, () => meta.post(t.id, { status: 'PAUSED' }));
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
      await meta.post(pair.keep.id, { name: nameFor(await mediaFull(pair.keep.mediaId), 'CHAMPION') });
      await meta.post(pair.retire.id, { status: 'PAUSED', name: nameFor(await mediaFull(pair.retire.mediaId), 'RETIRED') });
      await record(pair.keep.mediaId, 'pair_resolved', { kept: pair.keep.id, retired: pair.retire.id, reason: pair.reason });
    });
  }

  // ── 6. Champion health ────────────────────────────────────────────────
  const health = championHealth({ spend: c7.settledSpend, visits: c7.visits, follows: c7.estFollows, followsReadable });
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
// BACKFILL: estimated cost per follower for every post, last 30 days (read-only)
// ============================================================

// Group attributed rows by post and by post type. `typeOf(mediaId)` -> 'IMAGE' | 'REEL' | ...
function backfillTable(adDays, typeOf) {
  const byPost = new Map();
  for (const r of adDays) {
    if (!r.mediaId) continue;
    if (!byPost.has(r.mediaId)) byPost.set(r.mediaId, []);
    byPost.get(r.mediaId).push(r);
  }
  const posts = [...byPost].map(([mediaId, rows]) => ({ mediaId, type: typeOf(mediaId), ...followStats(rows) }))
                           .filter(p => p.spend > 0)
                           .sort((a, b) => (a.costPerFollow ?? Infinity) - (b.costPerFollow ?? Infinity));
  const byType = {};
  for (const p of posts) {
    const t = (byType[p.type] = byType[p.type] || { type: p.type, posts: 0, spend: 0, settledSpend: 0, visits: 0, estFollows: 0 });
    t.posts++; t.spend += p.spend; t.settledSpend += p.settledSpend; t.visits += p.visits; t.estFollows += p.estFollows;
  }
  const types = Object.values(byType).map(t => ({
    ...t, spend: round2(t.spend), settledSpend: round2(t.settledSpend), estFollows: Math.round(t.estFollows * 10) / 10,
    costPerFollow: t.estFollows > 0 ? round2(t.settledSpend / t.estFollows) : null,
    costPerVisit: t.visits > 0 ? round2(t.spend / t.visits) : null,
    followsPer100Visits: t.visits > 0 ? Math.round(1000 * t.estFollows / t.visits) / 10 : null,
  }));
  return { posts, types };
}

async function runBackfill({ meta, db, now = new Date() }) {
  const [followerDays, adDaysRaw] = await Promise.all([loadFollowerDays({ meta, db, now }), loadAdDays({ meta, now })]);
  if (!followerDays.readable) throw new Error(`follower counts not readable: ${followerDays.error || 'no rows'}`);
  const settledThrough = settledThroughFor(now);
  const adDays = attributeFollows(adDaysRaw, followerDays.byDay, settledThrough);
  const nameBy = new Map(adDaysRaw.map(r => [r.mediaId, r.adsetName]));
  const media = new Map();
  for (const id of new Set(adDaysRaw.map(r => r.mediaId).filter(Boolean))) {
    try { media.set(id, await meta.get(id, { fields: 'id,media_type,caption' })); } catch { media.set(id, { id }); }
  }
  const typeOf = (id) => typeLabel(media.get(id));
  const table = backfillTable(adDays, typeOf);
  for (const p of table.posts) p.title = titleOf(media.get(p.mediaId)) || nameBy.get(p.mediaId);
  return { settledThrough, followerDays: followerDays.byDay, ...table };
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
  L.push(`Champion (${ch.window.days} settled days to ${ch.window.until}): ${usd(ch.spend)} spend, `
       + `${ch.followsReadable ? `${ch.follows} est. follows${ch.costPerFollow !== null ? ` (${usd(ch.costPerFollow)}/follower)` : ''}` : 'follows not readable'}, `
       + `${ch.visits} visits${ch.costPerVisit !== null ? ` (${usd(ch.costPerVisit)}/visit)` : ''}; `
       + `active ads: ${ch.activeAds.length ? ch.activeAds.map(a => a.name).join(', ') : 'NONE'}; health: ${ch.health.action} — ${ch.health.reason}`);
  if (r.pair) L.push(`First-run pair: ${r.pair.resolved ? 'RESOLVED' : 'open'} — ${r.pair.reason}`);
  L.push(`Candidates (new posts since ${SYSTEM_START} with no test): ${r.candidates.length}`);
  for (const m of r.candidates) L.push(`   ${m.label} (${m.postedAt.slice(0, 10)})`);
  L.push(`Tests in flight: ${r.tests.filter(t => t.phase === 'running').length}, judged this run: ${r.verdicts.length}, done before: ${r.tests.filter(t => t.phase === 'done').length}`);
  for (const t of r.tests) L.push(`   ${t.label || `TEST::${t.mediaId}`} ${t.phase} ${usd(t.spend)}, ${t.estFollows ?? '?'} est. follows${t.costPerFollow != null ? ` ${usd(t.costPerFollow)}/follower` : ''}, ${t.visits} visits${t.verdict ? ` → ${t.verdict.result}: ${t.verdict.reason}` : ''}`);
  if (r.skips.length) for (const s of r.skips) L.push(`   SKIP ${s.mediaId}: ${s.reason}`);
  L.push(`Actions (${r.actions.length}):`);
  for (const a of r.actions) L.push(`   ${a}`);
  if (!r.actions.length) L.push('   none');
  for (const w of r.warnings) L.push(`⚠ ${w}`);
  L.push(`Metrics: visits via "${r.metrics.visitsField}" (${r.metrics.visitsReadable ? 'readable' : 'NOT YET OBSERVED'}); follows ${r.metrics.followsReadable ? `estimated from follower_count, settled through ${r.metrics.settledThrough}` : `NOT READABLE (${r.metrics.followerError || 'no rows'})`}`);
  if (r.metrics.followerDays && r.metrics.followerDays.length) L.push(`New followers by day: ${r.metrics.followerDays.map(d => `${d.day.slice(5)} ${d.follows}`).join(', ')}`);
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
  const backfill = argv.includes('--backfill');
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

  if (backfill) {
    const b = await runBackfill({ meta, db });
    if (db) await db.close();
    if (argv.includes('--print')) { console.log(JSON.stringify(b, null, 2)); return; }
    console.log(`ESTIMATED COST PER FOLLOWER: follows settled through ${b.settledThrough} (method B: day's new followers split by visit share)`);
    for (const t of b.types) console.log(`  ${t.type.padEnd(8)} ${t.posts} posts  ${usd(t.spend)}  ${t.visits} visits (${usd(t.costPerVisit)}/visit)  ${t.estFollows} est. follows  ${t.costPerFollow !== null ? usd(t.costPerFollow) + '/follower' : 'n/a'}  ${t.followsPer100Visits}/100 visits`);
    for (const p of b.posts) console.log(`  ${usd(p.costPerFollow ?? 0).padStart(7)}/f  ${String(p.estFollows).padStart(5)} f  ${usd(p.spend).padStart(7)}  ${String(p.visits).padStart(4)} v  ${p.type.padEnd(8)} ${p.title}  (${p.mediaId})${p.settled ? '' : '  [part unsettled]'}`);
    return;
  }

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
  nameFor, titleOf, typeLabel, tagOf, isTest,
  followerDaysFrom, attributeFollows, followStats, backfillTable,
  CONFIG: { SYSTEM_START, FIRST_RUN_PAIR, TEST_BUDGET_CENTS, TEST_WINDOW_DAYS, TEST_EVAL_SPEND, CAP_TESTS_MTD, CAP_TOTAL_MTD,
            PROMOTE_MIN_FOLLOWS, FOLLOW_SETTLE_DAYS, CHAMPION_MIN_SPEND, CHAMPION_KILL_CPF, CHAMPION_SCALE_CPF, PAIR_MIN_SPEND, VISITS_FIELD, FOLLOW_ACTION_TYPES },
};

if (require.main === module) main().catch(e => { console.error('auto-boost crashed:', e.stack || e.message); process.exit(1); });
