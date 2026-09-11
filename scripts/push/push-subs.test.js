#!/usr/bin/env node
/* eslint-disable no-console */
//
// WEB-PUSH SUBSCRIPTION STORE — server fixture tests (no network, no real Postgres).
//
// Boots server.js against pg-mem with `node-fetch` and `web-push` stubbed, then
// exercises the 2026-09-11 move of the push subscriptions off push-subs.json (a
// file savePushSubs() used to PUT to the GitHub contents API) and into the
// `push_subscriptions` table.
//
// A push subscription is a CREDENTIAL: the endpoint URL plus its p256dh and
// auth keys are together everything needed to send a notification to that
// person's device. Nothing ever leaked — the file was never created, because
// nobody has subscribed to web push yet — so this is the fix landing before the
// feature is switched on rather than after.
//
//   (a) the one-time migration seeds the table from the legacy JSON, exactly,
//       and is idempotent;
//   (b) the awkward shapes survive: a legacy dashboard subscription with NO
//       meta stays without one (the reminder sweep keys off that), the per-user
//       meta round-trips whole, and a top-level key with no column of its own
//       survives via `extra`;
//   (c) subscribe / unsubscribe write to the DB, not just to memory — reload
//       and the change is still there;
//   (d) an endpoint the push service reports as gone (410) is deleted from the
//       TABLE, not just dropped from the in-memory copy, on both send paths;
//   (e) NOTHING is ever PUT to the GitHub contents API for this file again.
//       That is the whole point of the change, so it is asserted, not assumed.
//
// RUN: node scripts/push/push-subs.test.js
'use strict';

const os = require('os');
const fsx = require('fs');
const pathx = require('path');

const FIXTURE_DIR = fsx.mkdtempSync(pathx.join(os.tmpdir(), 'push-test-'));
const FIXTURE_FILE = pathx.join(FIXTURE_DIR, 'push-subs.json');
const EMPTY_SUBS_FILE = pathx.join(FIXTURE_DIR, 'subscribers-data.json');

// Synthetic subscriptions. The SHAPES are the two the code actually produces:
// a bare PushSubscription (the legacy dashboard subscribe, no meta at all) and
// the { subscription, tzOffset, prefs } form the app sends, which becomes
// `meta` on the stored record.
const LEGACY_ENDPOINT = 'https://fcm.googleapis.com/fcm/send/legacy-dashboard-0001';
const MEMBER_ENDPOINT = 'https://fcm.googleapis.com/fcm/send/member-0002';
const FIXTURE = {
  subs: [
    {
      endpoint: LEGACY_ENDPOINT,
      expirationTime: null, // no column of its own → must round-trip via `extra`
      keys: { p256dh: 'BL-legacy-p256dh-key', auth: 'legacy-auth-key' },
    },
    {
      endpoint: MEMBER_ENDPOINT,
      expirationTime: null,
      keys: { p256dh: 'BL-member-p256dh-key', auth: 'member-auth-key' },
      meta: { userId: 4242, tzOffset: -300, prefs: { weigh: true, photo: false, mealPrep: true, workout: false } },
    },
  ],
};
fsx.writeFileSync(FIXTURE_FILE, JSON.stringify(FIXTURE, null, 2));
// Keep the real marketing list out of this run entirely.
fsx.writeFileSync(EMPTY_SUBS_FILE, JSON.stringify({ emails: {} }, null, 2));

process.env.DATABASE_URL = 'pgmem://test';
process.env.PUSH_SUBS_LEGACY_FILE = FIXTURE_FILE;
process.env.SUBSCRIBERS_LEGACY_FILE = EMPTY_SUBS_FILE;
process.env.VAPID_PUBLIC_KEY = 'test-vapid-public';
process.env.VAPID_PRIVATE_KEY = 'test-vapid-private';
process.env.MONARCH_PUSH_SECRET = 'test-push-secret';
process.env.GITHUB_TOKEN = 'ghp_test_stub'; // so a stray GitHub write would be ATTEMPTED, and caught
process.env.DASH_SECRET = 'test-dash-secret';
process.env.GEMINI_API_KEY = 'dummy';
process.env.ANTHROPIC_API_KEY = 'dummy';
process.env.PORT = process.env.PORT || '3563';
process.env.SITE_URL = 'https://absbyai.com';
delete process.env.WELCOME_ENABLED;
delete process.env.MAILERLITE_API_KEY;

const Module = require('module');
const path = require('path');

// ── fetch stub: record every outbound call, send nothing anywhere ──
const realFetch = global.fetch;
const outbound = [];
const stubFetch = async (url, opts) => {
  const u = String(url);
  if (u.startsWith('http://localhost') || u.startsWith('http://127.0.0.1')) return realFetch(url, opts);
  outbound.push({ url: u, method: (opts && opts.method) || 'GET', body: (opts && opts.body) || '' });
  return { ok: false, status: 404, json: async () => ({}), text: async () => '' };
};
global.fetch = stubFetch;

// ── web-push stub: record the sends, and report a chosen endpoint as gone ──
const pushCalls = [];
const GONE = new Set();
const webPushStub = {
  setVapidDetails() {},
  async sendNotification(sub, payload) {
    pushCalls.push({ endpoint: sub.endpoint, keys: sub.keys, payload });
    if (GONE.has(sub.endpoint)) {
      const e = new Error('push subscription gone');
      e.statusCode = 410;
      throw e;
    }
    return { statusCode: 201 };
  },
};

const realLoad = Module._load;
Module._load = function (request) {
  if (request === 'node-fetch') return stubFetch;
  if (request === 'web-push') return webPushStub;
  return realLoad.apply(this, arguments);
};

const realLog = console.log;
console.log = () => {};
const realWarn = console.warn;
console.warn = () => {};

const server = require(path.join(process.cwd(), 'server.js'));
const { db, loadPushSubs, loadPushSubsStore, pushSubsReady, reminderSweep } = server;
const BASE = `http://localhost:${process.env.PORT}`;

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; realLog(`  ✓ ${name}`); }
  else { fail++; realLog(`  ✗ ${name}${extra !== undefined ? ' — ' + JSON.stringify(extra) : ''}`); }
}
async function api(p, body, headers = {}) {
  const r = await realFetch(BASE + p, {
    method: body === undefined ? 'GET' : 'POST',
    headers: { 'Content-Type': 'application/json', ...headers },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return { status: r.status, data: await r.json().catch(() => ({})) };
}
async function rowFor(endpoint) {
  const { rows } = await db.query('SELECT * FROM push_subscriptions WHERE endpoint = $1', [endpoint]);
  return rows[0] || null;
}
async function rowCount() {
  const { rows } = await db.query('SELECT COUNT(*) AS n FROM push_subscriptions');
  return Number(rows[0].n);
}
async function waitForReady() {
  for (let i = 0; i < 100; i++) {
    try {
      await db.query('SELECT 1 FROM push_subscriptions LIMIT 1');
      await realFetch(BASE + '/health');
      return;
    } catch (e) { await new Promise(r => setTimeout(r, 100)); }
  }
  throw new Error('server never became ready');
}
const githubPushWrites = () => outbound.filter(
  o => o.url.includes('api.github.com') && o.url.includes('push-subs.json') && o.method !== 'GET'
);

(async () => {
  await waitForReady();
  await pushSubsReady; // the boot-time load runs the migration; don't race it

  // ── (a) migration ──
  realLog('\n(a) one-time migration off the JSON file');
  check('both fixture subscriptions became rows', (await rowCount()) === 2, await rowCount());
  const legacyRow = await rowFor(LEGACY_ENDPOINT);
  check('the endpoint is the primary key', !!legacyRow && legacyRow.endpoint === LEGACY_ENDPOINT);
  check('p256dh landed in its own column', legacyRow.p256dh === 'BL-legacy-p256dh-key', legacyRow.p256dh);
  check('auth landed in its own column', legacyRow.auth === 'legacy-auth-key', legacyRow.auth);

  const loaded = await loadPushSubs();
  check('reload returns both subscriptions', loaded.length === 2, loaded.length);
  const byEndpoint = Object.fromEntries(loaded.map(s => [s.endpoint, s]));
  check('the in-memory shape is unchanged (keys nested under `keys`)',
    JSON.stringify(byEndpoint[LEGACY_ENDPOINT].keys) === JSON.stringify(FIXTURE.subs[0].keys),
    byEndpoint[LEGACY_ENDPOINT].keys);

  const before = await rowCount();
  await loadPushSubsStore(); // must NOT re-seed or duplicate
  check('migration is idempotent (no duplicate rows)', (await rowCount()) === before, await rowCount());

  // ── (b) the shapes that break naive column mapping ──
  realLog('\n(b) awkward shapes');
  check('a legacy dashboard sub keeps NO meta (the sweep keys off that)',
    byEndpoint[LEGACY_ENDPOINT].meta === undefined && legacyRow.meta === null,
    { mem: byEndpoint[LEGACY_ENDPOINT].meta, col: legacyRow.meta });
  check('the per-user meta round-trips whole',
    JSON.stringify(byEndpoint[MEMBER_ENDPOINT].meta) === JSON.stringify(FIXTURE.subs[1].meta),
    byEndpoint[MEMBER_ENDPOINT].meta);
  check('a top-level key with no column survives via `extra`',
    'expirationTime' in byEndpoint[MEMBER_ENDPOINT] && byEndpoint[MEMBER_ENDPOINT].expirationTime === null,
    byEndpoint[MEMBER_ENDPOINT]);

  // ── (c) the live write paths persist to Postgres ──
  realLog('\n(c) subscribe / unsubscribe write to the DB');
  const NEW_ENDPOINT = 'https://updates.push.services.mozilla.com/wpush/v2/new-0003';
  const bad = await api('/api/push/subscribe', { keys: { p256dh: 'x', auth: 'y' } });
  check('a subscription with no endpoint → 400', bad.status === 400, bad);

  const sub = await api('/api/push/subscribe', {
    endpoint: NEW_ENDPOINT, expirationTime: null, keys: { p256dh: 'BL-new-p256dh', auth: 'new-auth' },
  });
  check('/api/push/subscribe → {ok:true}', sub.status === 200 && sub.data.ok === true, sub);
  check('...and reports the new count', sub.data.count === 3, sub.data);
  const newRow = await rowFor(NEW_ENDPOINT);
  check('the new subscription is a row', !!newRow, newRow);
  check('its keys were stored', newRow.p256dh === 'BL-new-p256dh' && newRow.auth === 'new-auth', newRow);
  check('a bare PushSubscription gets no meta', newRow.meta === null, newRow.meta);

  await api('/api/push/subscribe', {
    endpoint: NEW_ENDPOINT, expirationTime: null, keys: { p256dh: 'BL-rotated', auth: 'rotated-auth' },
  });
  check('re-subscribing the same endpoint does not duplicate', (await rowCount()) === 3, await rowCount());
  check('...and the rotated keys replaced the old ones',
    (await rowFor(NEW_ENDPOINT)).p256dh === 'BL-rotated', (await rowFor(NEW_ENDPOINT)).p256dh);

  const APP_ENDPOINT = 'https://updates.push.services.mozilla.com/wpush/v2/app-0004';
  const appSub = await api('/api/push/subscribe', {
    subscription: { endpoint: APP_ENDPOINT, keys: { p256dh: 'BL-app', auth: 'app-auth' } },
    tzOffset: -300,
    prefs: { weigh: true, mealPrep: true },
  });
  check('the app form ({subscription, tzOffset, prefs}) → {ok:true}', appSub.status === 200 && appSub.data.ok === true, appSub);
  const appRow = await rowFor(APP_ENDPOINT);
  check('tzOffset and prefs were stored as meta',
    appRow.meta && appRow.meta.tzOffset === -300 && appRow.meta.prefs.weigh === true, appRow.meta);
  check('an anonymous subscriber gets meta.userId null', appRow.meta.userId === null, appRow.meta);

  const afterReload = await loadPushSubsStore();
  check('a subscription survives a reload — it really is in Postgres',
    afterReload.some(s => s.endpoint === APP_ENDPOINT && s.meta && s.meta.tzOffset === -300),
    afterReload.map(s => s.endpoint));

  const unsub = await api('/api/push/unsubscribe', { endpoint: NEW_ENDPOINT });
  check('/api/push/unsubscribe → {ok:true}', unsub.status === 200 && unsub.data.ok === true, unsub);
  check('the row is gone', (await rowFor(NEW_ENDPOINT)) === null);
  check('...and stays gone after a reload',
    !(await loadPushSubsStore()).some(s => s.endpoint === NEW_ENDPOINT));
  const noEndpoint = await api('/api/push/unsubscribe', {});
  check('unsubscribe with no endpoint → 400', noEndpoint.status === 400, noEndpoint);

  // ── (d) an expired endpoint is deleted from the TABLE ──
  realLog('\n(d) expired endpoints are removed from the table, not just from memory');
  GONE.add(LEGACY_ENDPOINT);
  pushCalls.length = 0;
  const send = await api('/api/send-push', { title: 'Victory Dashboard', body: 'test' },
    { 'X-Push-Secret': process.env.MONARCH_PUSH_SECRET });
  check('/api/send-push → 200', send.status === 200, send);
  check('it sent to every stored subscription', pushCalls.length === 3, pushCalls.map(c => c.endpoint));
  check('it sent the keys the table gave back',
    pushCalls.every(c => c.keys && c.keys.p256dh && c.keys.auth), pushCalls.map(c => c.keys));
  check('it reported one stale endpoint', send.data.removed_stale === 1 && send.data.sent === 2, send.data);
  check('the 410 endpoint was DELETED from the table', (await rowFor(LEGACY_ENDPOINT)) === null);
  check('...and does not come back on a reload',
    !(await loadPushSubsStore()).some(s => s.endpoint === LEGACY_ENDPOINT));
  check('the healthy endpoints were left alone', (await rowCount()) === 2, await rowCount());

  // The reminder sweep is the second send path, and it prunes the same way.
  const { rows: userRows } = await db.query(
    `INSERT INTO users (email, password_hash, device_id, weigh_reminder)
     VALUES ($1,$2,$3,true) RETURNING id`,
    ['pushtest@fixture.test', 'x', 'dev-push']
  );
  const userId = userRows[0].id;
  // Put this subscription's LOCAL clock inside the 8 AM reminder window.
  const nowUtcMinutes = new Date().getUTCHours() * 60 + new Date().getUTCMinutes();
  const tzOffset = 8 * 60 + 30 - nowUtcMinutes;
  const SWEEP_ENDPOINT = 'https://fcm.googleapis.com/fcm/send/sweep-0005';
  await db.query(
    `INSERT INTO push_subscriptions (endpoint, p256dh, auth, meta, extra)
     VALUES ($1,$2,$3,$4,'{}')`,
    [SWEEP_ENDPOINT, 'BL-sweep', 'sweep-auth', JSON.stringify({ userId, tzOffset, prefs: { weigh: true } })]
  );
  GONE.add(SWEEP_ENDPOINT);
  pushCalls.length = 0;
  await reminderSweep();
  check('the reminder sweep reached the per-user subscription',
    pushCalls.some(c => c.endpoint === SWEEP_ENDPOINT), pushCalls.map(c => c.endpoint));
  check('...and its 410 deleted the row too', (await rowFor(SWEEP_ENDPOINT)) === null);

  // ── (e) the actual security property ──
  realLog('\n(e) nothing reaches the GitHub repo');
  check('zero writes to the GitHub contents API for push-subs.json',
    githubPushWrites().length === 0, githubPushWrites());
  const leaked = outbound.filter(o =>
    /p256dh|auth-key|BL-legacy|BL-member|BL-app|BL-rotated|fcm\.googleapis|mozilla/i.test(o.url + o.body));
  check('no outbound call carried an endpoint or a push key', leaked.length === 0,
    leaked.slice(0, 3).map(o => ({ url: o.url, method: o.method })));
  check('server.js contains no GitHub contents write for push-subs.json',
    !/PUSH_SUBS_FILE[\s\S]{0,400}method:\s*'PUT'/.test(fsx.readFileSync(path.join(process.cwd(), 'server.js'), 'utf8')));

  realLog(`\n${fail === 0 ? '✅' : '❌'} ${pass} passed, ${fail} failed`);
  try { fsx.rmSync(FIXTURE_DIR, { recursive: true, force: true }); } catch (_) {}
  console.log = realLog; console.warn = realWarn;
  process.exit(fail === 0 ? 0 : 1);
})().catch(e => {
  console.log = realLog;
  realLog('TEST HARNESS ERROR:', e && e.stack || e);
  try { fsx.rmSync(FIXTURE_DIR, { recursive: true, force: true }); } catch (_) {}
  process.exit(1);
});
