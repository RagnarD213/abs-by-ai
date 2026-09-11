#!/usr/bin/env node
/* eslint-disable no-console */
//
// SUBSCRIBER STORE — server fixture tests (no network, no real Postgres).
//
// Boots server.js against pg-mem with `node-fetch` stubbed, then exercises the
// 2026-09-11 move of the marketing list off subscribers-data.json (a file in a
// PUBLIC GitHub repo, world-readable at raw.githubusercontent.com) and into the
// `subscribers` table:
//   (a) the one-time migration seeds the table from the legacy JSON, exactly —
//       same count, same digest, byte-equal entries — and is idempotent;
//   (b) the awkward shapes survive: a welcomeStep that is ABSENT (the flag that
//       tells the sweep to backfill) stays absent, welcomeNextAt:null stays
//       falsy, and a field with no column of its own round-trips via `extra`;
//   (c) /api/subscribe, the welcome sweep and /api/unsubscribe all write to the
//       DB, not just to memory — reload and the change is still there;
//   (d) NOTHING is ever PUT to the GitHub contents API for this file again.
//       That is the whole point of the change, so it is asserted, not assumed;
//   (e) /api/subscribers/status is gated and leaks no address.
//
// RUN: node scripts/subscribers/subscribers.test.js
'use strict';

const os = require('os');
const fsx = require('fs');
const pathx = require('path');

const FIXTURE_DIR = fsx.mkdtempSync(pathx.join(os.tmpdir(), 'subs-test-'));
const FIXTURE_FILE = pathx.join(FIXTURE_DIR, 'subscribers-data.json');

// Synthetic list, deliberately NOT the real one: a test fixture lives in the
// public repo, which is the exact mistake this change exists to undo. The
// SHAPES are copied from production — a finished sequence with welcomeNextAt
// null, an excluded @example.com row, a mid-sequence subscriber, an entry from
// before the welcome fields existed, an unsubscribe, a sixpackabs source tag.
const FIXTURE = {
  emails: {
    'finished@fixture.test': {
      subscribedAt: '2026-07-04T02:07:47.645Z',
      deviceId: 'dev-1783035492121-rr3he75n',
      synced: true,
      welcomeStep: 5,
      welcomeNextAt: null,
      welcomeSentAt: {
        '1': '2026-07-17T21:05:54.620Z', '2': '2026-07-20T21:06:01.110Z',
        '3': '2026-07-24T21:06:08.220Z', '4': '2026-07-29T21:06:15.330Z',
        '5': '2026-08-03T21:06:22.440Z',
      },
      unsubscribed: false,
    },
    'excluded@example.com': {
      subscribedAt: '2026-07-03T22:09:57.849Z',
      deviceId: 'prod-check',
      synced: true,
      welcomeStep: 5,
      excluded: true,
    },
    'midway@fixture.test': {
      subscribedAt: '2026-09-01T10:00:00.000Z',
      deviceId: 'dev-mid',
      synced: false,
      welcomeStep: 2,
      welcomeNextAt: '2099-01-01T00:00:00.000Z', // far future → sweep must skip
      welcomeSentAt: { '1': '2026-09-01T10:00:05.000Z', '2': '2026-09-04T10:00:05.000Z' },
      unsubscribed: false,
    },
    'due@fixture.test': {
      subscribedAt: '2026-09-05T10:00:00.000Z',
      deviceId: 'dev-due',
      synced: false,
      welcomeStep: 1,
      welcomeNextAt: '2026-09-06T10:00:00.000Z', // past → sweep must send #2
      welcomeSentAt: { '1': '2026-09-05T10:00:05.000Z' },
      unsubscribed: false,
      source: 'sixpackabs',
    },
    'ancient@fixture.test': {
      // Predates the welcome sequence: NO welcomeStep at all. `undefined` here
      // is load-bearing — ensureWelcomeFields keys off it to backfill.
      subscribedAt: '2026-07-01T00:00:00.000Z',
      deviceId: 'dev-old',
      synced: true,
    },
    'gone@fixture.test': {
      subscribedAt: '2026-08-01T00:00:00.000Z',
      deviceId: 'dev-gone',
      synced: true,
      welcomeStep: 3,
      welcomeNextAt: '2026-08-20T00:00:00.000Z',
      welcomeSentAt: { '1': '2026-08-01T00:00:05.000Z' },
      unsubscribed: true,
      unsubscribedAt: '2026-08-10T00:00:00.000Z',
      deletedAccount: true,
    },
    'futurefield@fixture.test': {
      subscribedAt: '2026-09-09T00:00:00.000Z',
      deviceId: 'dev-extra',
      synced: true,
      welcomeStep: 0,
      welcomeNextAt: '2099-01-01T00:00:00.000Z',
      welcomeSentAt: {},
      unsubscribed: false,
      // No column of its own: must come back intact out of `extra`.
      someFieldAddedLater: { nested: ['a', 'b'], n: 7 },
    },
  },
};
fsx.writeFileSync(FIXTURE_FILE, JSON.stringify(FIXTURE, null, 2));

process.env.DATABASE_URL = 'pgmem://test';
process.env.SUBSCRIBERS_LEGACY_FILE = FIXTURE_FILE;
process.env.DASH_SECRET = 'test-dash-secret';
process.env.WELCOME_ENABLED = 'true';
process.env.RESEND_API_KEY = 're_test_stub';
process.env.GITHUB_TOKEN = 'ghp_test_stub'; // so a stray GitHub write would be ATTEMPTED, and caught
process.env.UNSUBSCRIBE_SECRET = 'test-unsub-secret';
process.env.GEMINI_API_KEY = 'dummy';
process.env.ANTHROPIC_API_KEY = 'dummy';
process.env.PORT = process.env.PORT || '3561';
process.env.SITE_URL = 'https://absbyai.com';
delete process.env.MAILERLITE_API_KEY;

const Module = require('module');
const path = require('path');

// ── fetch stub: record every outbound call, send nothing anywhere ──
const realFetch = global.fetch;
const outbound = [];
const stubFetch = async (url, opts) => {
  const u = String(url);
  if (u.startsWith('http://localhost') || u.startsWith('http://127.0.0.1')) return realFetch(url, opts);
  outbound.push({ url: u, method: (opts && opts.method) || 'GET' });
  if (u.startsWith('https://api.resend.com/emails')) {
    return { ok: true, status: 200, json: async () => ({ id: 'email_stub' }), text: async () => '' };
  }
  // Any GitHub read of the subscribers file must look like "not there".
  return { ok: false, status: 404, json: async () => ({}), text: async () => '' };
};
global.fetch = stubFetch;
const realLoad = Module._load;
Module._load = function (request) {
  if (request === 'node-fetch') return stubFetch;
  return realLoad.apply(this, arguments);
};

const realLog = console.log;
console.log = () => {};
const realWarn = console.warn;
console.warn = () => {};

const server = require(path.join(process.cwd(), 'server.js'));
const {
  db, welcomeSweep, loadSubscribersStore, persistSubscribersStore,
  getSubscribersStore, setSubscribersStore, subscribersReady,
} = server;
const { subscribersDigest, canonEntry } = require(path.join(process.cwd(), 'scripts/subscribers/digest.js'));
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
async function rowFor(email) {
  const { rows } = await db.query('SELECT * FROM subscribers WHERE email = $1', [email]);
  return rows[0] || null;
}
async function rowCount() {
  const { rows } = await db.query('SELECT COUNT(*) AS n FROM subscribers');
  return Number(rows[0].n);
}
async function waitForReady() {
  for (let i = 0; i < 100; i++) {
    try {
      await db.query('SELECT 1 FROM subscribers LIMIT 1');
      await realFetch(BASE + '/health');
      return;
    } catch (e) { await new Promise(r => setTimeout(r, 100)); }
  }
  throw new Error('server never became ready');
}
const githubSubscriberWrites = () => outbound.filter(
  o => o.url.includes('api.github.com') && o.url.includes('subscribers-data.json') && o.method !== 'GET'
);

(async () => {
  await waitForReady();
  await subscribersReady; // the boot-time load runs the migration; don't race it

  // ── (a) migration ──
  realLog('\n(a) one-time migration off the public JSON file');
  const fixtureEmails = Object.keys(FIXTURE.emails);
  check(`all ${fixtureEmails.length} addresses became rows`, (await rowCount()) === fixtureEmails.length, await rowCount());

  const loaded = await loadSubscribersStore();
  check('reload returns every address', Object.keys(loaded.emails).length === fixtureEmails.length);

  // `ancient@` is compared separately: boot deliberately backfills welcome
  // fields onto any entry that predates the sequence, so its post-boot state is
  // SUPPOSED to differ from the file. Everything else must be untouched.
  const BACKFILLED = 'ancient@fixture.test';
  const subset = (emails) => Object.fromEntries(
    Object.entries(emails).filter(([e]) => e !== BACKFILLED)
  );
  check('digest of the DB copy === digest of the file',
    subscribersDigest(subset(loaded.emails)) === subscribersDigest(subset(FIXTURE.emails)),
    { db: subscribersDigest(subset(loaded.emails)), file: subscribersDigest(subset(FIXTURE.emails)) });

  let entriesMatch = true, firstMismatch = null;
  for (const email of fixtureEmails) {
    if (email === BACKFILLED) continue;
    const a = JSON.stringify(canonEntry(FIXTURE.emails[email]));
    const b = JSON.stringify(canonEntry(loaded.emails[email]));
    if (a !== b) { entriesMatch = false; firstMismatch = firstMismatch || { email, file: a, db: b }; }
  }
  check('every entry round-trips field for field', entriesMatch, firstMismatch);

  const before = await rowCount();
  await loadSubscribersStore(); // must NOT re-seed or duplicate
  check('migration is idempotent (no duplicate rows)', (await rowCount()) === before, await rowCount());

  // ── (b) the shapes that break naive column mapping ──
  realLog('\n(b) awkward shapes');
  // The backfill is itself the proof that an ABSENT welcomeStep survived the
  // migration as absent: ensureWelcomeFields only fires on `=== undefined`, so
  // had the migration written 0 (or read NULL back as 0) this entry would have
  // been skipped and would never receive its first email.
  const ancient = loaded.emails[BACKFILLED];
  check('a pre-sequence entry was recognised and backfilled at boot', ancient.welcomeStep !== undefined, ancient);
  check('...and its original fields were not disturbed',
    ancient.deviceId === 'dev-old' && ancient.synced === true &&
    ancient.subscribedAt === '2026-07-01T00:00:00.000Z', ancient);

  // The same mapping, tested directly and free of the boot sequence.
  const store = getSubscribersStore();
  store.emails['nosequence@fixture.test'] = { subscribedAt: '2026-07-02T00:00:00.000Z', deviceId: 'dev-ns', synced: true };
  await persistSubscribersStore(['nosequence@fixture.test']);
  check('an absent welcomeStep is stored as SQL NULL, not 0',
    (await rowFor('nosequence@fixture.test')).welcome_step === null,
    (await rowFor('nosequence@fixture.test')).welcome_step);
  check('...and a NULL column reads back as absent, not 0',
    (await loadSubscribersStore()).emails['nosequence@fixture.test'].welcomeStep === undefined);
  await db.query('DELETE FROM subscribers WHERE email = $1', ['nosequence@fixture.test']);
  delete store.emails['nosequence@fixture.test'];

  check('welcomeNextAt:null stays falsy (finished sequence)', !loaded.emails['finished@fixture.test'].welcomeNextAt);
  check('welcomeSentAt map survives with all 5 keys',
    Object.keys(loaded.emails['finished@fixture.test'].welcomeSentAt).length === 5);
  check('a field with no column survives via `extra`',
    JSON.stringify(loaded.emails['futurefield@fixture.test'].someFieldAddedLater) === JSON.stringify({ nested: ['a', 'b'], n: 7 }),
    loaded.emails['futurefield@fixture.test'].someFieldAddedLater);
  check('excluded flag survives', loaded.emails['excluded@example.com'].excluded === true);
  check('deletedAccount + unsubscribedAt survive',
    loaded.emails['gone@fixture.test'].deletedAccount === true &&
    loaded.emails['gone@fixture.test'].unsubscribedAt === '2026-08-10T00:00:00.000Z');
  check('source tag survives', loaded.emails['due@fixture.test'].source === 'sixpackabs');

  // ── (c) the live write paths persist to Postgres ──
  realLog('\n(c) subscribe / sweep / unsubscribe write to the DB');
  setSubscribersStore(loaded);

  const sub = await api('/api/subscribe', { email: 'NewPerson@Fixture.test', deviceId: 'dev-new', source: 'sixpackabs' });
  check('/api/subscribe → {ok:true}', sub.status === 200 && sub.data.ok === true, sub);
  await new Promise(r => setTimeout(r, 150)); // fire-and-forget write
  const newRow = await rowFor('newperson@fixture.test');
  check('new subscriber is a row (lowercased)', !!newRow, newRow);
  check('new subscriber starts the sequence at step 0', newRow && newRow.welcome_step === 0, newRow && newRow.welcome_step);
  check('source recorded', newRow && newRow.source === 'sixpackabs');
  check('device id recorded', newRow && newRow.device_id === 'dev-new');

  await api('/api/subscribe', { email: 'newperson@fixture.test', deviceId: 'dev-new2' });
  await new Promise(r => setTimeout(r, 150));
  check('repeat subscribe does not duplicate', (await rowCount()) === fixtureEmails.length + 1, await rowCount());

  await welcomeSweep();
  const dueRow = await rowFor('due@fixture.test');
  check('sweep advanced the due subscriber IN THE DB', dueRow.welcome_step === 2, dueRow.welcome_step);
  check('sweep recorded the send timestamp', !!(dueRow.welcome_sent_at && dueRow.welcome_sent_at['2']), dueRow.welcome_sent_at);
  const midRow = await rowFor('midway@fixture.test');
  check('sweep left the not-yet-due subscriber alone', midRow.welcome_step === 2);
  check('sweep never mails an unsubscribed address',
    (await rowFor('gone@fixture.test')).welcome_step === 3);
  check('sweep never mails an excluded address',
    (await rowFor('excluded@example.com')).welcome_step === 5);
  const ancientAfter = await rowFor('ancient@fixture.test');
  check('the backfilled pre-sequence entry then got its first email',
    ancientAfter.welcome_step === 1 && !!ancientAfter.welcome_sent_at['1'], ancientAfter);

  // Survives a reload — i.e. it really is in Postgres, not just in memory.
  const reloaded = await loadSubscribersStore();
  check('sweep progress survives a reload', reloaded.emails['due@fixture.test'].welcomeStep === 2);
  check('new subscriber survives a reload', !!reloaded.emails['newperson@fixture.test']);

  const crypto = require('crypto');
  const unsubTok = crypto.createHmac('sha256', process.env.UNSUBSCRIBE_SECRET)
    .update('finished@fixture.test').digest('hex');
  const bad = await realFetch(`${BASE}/api/unsubscribe?email=finished@fixture.test&token=${'0'.repeat(64)}`);
  check('a forged unsubscribe token is refused', bad.status === 400, bad.status);
  check('...and changes nothing', (await rowFor('finished@fixture.test')).unsubscribed === false);
  const un = await realFetch(`${BASE}/api/unsubscribe?email=finished@fixture.test&token=${unsubTok}`);
  check('a valid unsubscribe link responds 200', un.status === 200, un.status);
  await new Promise(r => setTimeout(r, 150));
  const unsubRow = await rowFor('finished@fixture.test');
  check('unsubscribe flag written to the DB', unsubRow.unsubscribed === true, unsubRow.unsubscribed);
  check('unsubscribe survives a reload',
    (await loadSubscribersStore()).emails['finished@fixture.test'].unsubscribed === true);

  // ── (d) the actual security property ──
  realLog('\n(d) nothing reaches the public repo');
  check('zero writes to the GitHub contents API for subscribers-data.json',
    githubSubscriberWrites().length === 0, githubSubscriberWrites());
  check('no outbound call carried a subscriber address',
    !outbound.some(o => /newperson%40|newperson@|fixture\.test/i.test(o.url)),
    outbound.filter(o => /fixture\.test/i.test(o.url)).slice(0, 3));

  // ── (e) the status endpoint ──
  realLog('\n(e) /api/subscribers/status');
  const open = await api('/api/subscribers/status');
  check('unauthenticated → 401', open.status === 401, open);
  const gated = await api('/api/subscribers/status', undefined, { 'X-Dash-Key': process.env.DASH_SECRET });
  check('with the dash key → 200', gated.status === 200, gated);
  check('reports postgres persistence', gated.data.persistence === 'postgres', gated.data);
  check('row count matches memory', gated.data.dbRows === gated.data.inMemory, gated.data);
  check('digest matches a locally computed one',
    gated.data.digest === subscribersDigest(getSubscribersStore().emails), gated.data.digest);
  const blob = JSON.stringify(gated.data);
  check('response contains no email address', !/@/.test(blob), blob.slice(0, 200));

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
