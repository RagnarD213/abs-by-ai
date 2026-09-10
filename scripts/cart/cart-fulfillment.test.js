#!/usr/bin/env node
/* eslint-disable no-console */
//
// WEB PAY-FIRST CART — server fixture tests (no card, no Stripe network).
//
// Boots server.js against pg-mem with the `stripe` module and global fetch
// stubbed, then drives fulfillMembershipSession() and the /api/stripe/claim,
// /api/auth/set-password and /api/auth/login endpoints with fixture sessions:
//   (a) a NEW email creates the account, applies the membership, records the
//       gclid, queues the set-password email, and the claim logs that browser in
//       exactly once;
//   (b) an EXISTING email gets the membership attached, no claim, a log-in email;
//   (c) a webhook racing the browser's claim yields one account, one fulfilment,
//       one email;
//   (d) buildMembershipCheckout builds an anonymous session with no
//       customer_email and the click id in metadata, and a logged-in one as before.
//
// RUN: node scripts/cart/cart-fulfillment.test.js
'use strict';

process.env.DATABASE_URL = 'pgmem://test';
process.env.STRIPE_SECRET_KEY = 'sk_test_stub';
process.env.STRIPE_PUBLISHABLE_KEY = 'pk_test_stub';
process.env.STRIPE_WEBHOOK_SECRET = 'whsec_stub';
process.env.RESEND_API_KEY = 're_test_stub';
process.env.GEMINI_API_KEY = 'dummy';
process.env.ANTHROPIC_API_KEY = 'dummy';
process.env.PORT = process.env.PORT || '3557';
process.env.SITE_URL = 'https://absbyai.com';

const Module = require('module');
const path = require('path');

// ── Stripe stub ──
const stripeCalls = { sessionsCreate: [], subscriptionsRetrieve: [] };
const fixtureSessions = {};
const stripeStub = {
  checkout: {
    sessions: {
      create: async (params) => { stripeCalls.sessionsCreate.push(params); return { id: `cs_test_${stripeCalls.sessionsCreate.length}`, client_secret: 'cs_secret' }; },
      retrieve: async (sid) => { const s = fixtureSessions[sid]; if (!s) throw new Error('No such session: ' + sid); return s; },
    },
  },
  subscriptions: { retrieve: async (id) => { stripeCalls.subscriptionsRetrieve.push(id); return { id, status: 'trialing', trial_end: Math.floor(Date.now() / 1000) + 7 * 86400 }; } },
  coupons: { create: async () => ({ id: 'coupon_stub' }) },
  webhooks: { constructEvent: () => { throw new Error('not used'); } },
};
// ── fetch stub: capture Resend, pass localhost through, swallow the rest ──
const realFetch = global.fetch;
const resendCalls = [];
const stubFetch = async (url, opts) => {
  const u = String(url);
  if (u.startsWith('http://localhost') || u.startsWith('http://127.0.0.1')) return realFetch(url, opts);
  if (u.startsWith('https://api.resend.com/emails')) {
    resendCalls.push(JSON.parse(opts.body));
    return { ok: true, status: 200, json: async () => ({ id: 'email_stub' }), text: async () => '' };
  }
  return { ok: true, status: 200, json: async () => ({}), text: async () => '' };
};
global.fetch = stubFetch;

const realLoad = Module._load;
Module._load = function (request, parent, isMain) {
  if (request === 'stripe') return () => stripeStub;
  if (request === 'node-fetch') return stubFetch;
  return realLoad.apply(this, arguments);
};


const logs = [];
const realLog = console.log;
console.log = (...a) => { logs.push(a.join(' ')); };

const server = require(path.join(process.cwd(), 'server.js'));
const { db, fulfillMembershipSession, buildMembershipCheckout } = server;
const BASE = `http://localhost:${process.env.PORT}`;

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; realLog(`  ✓ ${name}`); }
  else { fail++; realLog(`  ✗ ${name}${extra !== undefined ? ' — ' + JSON.stringify(extra) : ''}`); }
}
async function api(p, body, token) {
  const r = await realFetch(BASE + p, {
    method: body === undefined ? 'GET' : 'POST',
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return { status: r.status, data: await r.json().catch(() => ({})) };
}
function anonSession(sid, email, extra = {}) {
  return {
    id: sid, status: 'complete', payment_status: 'paid', customer: 'cus_' + sid, subscription: 'sub_' + sid,
    customer_details: { email },
    metadata: { kind: 'membership', plan: 'monthly', anon: '1', deviceId: 'dev-' + sid, creditDiscountCents: '0', adClickId: 'gclid_' + sid, adClickType: 'gclid', ...extra },
  };
}
async function userByEmail(email) {
  const { rows } = await db.query('SELECT * FROM users WHERE email = $1', [email]);
  return rows[0] || null;
}
async function waitForDb() {
  for (let i = 0; i < 100; i++) {
    try { await db.query('SELECT ads_offline_uploaded_at FROM users LIMIT 1'); await db.query('SELECT 1 FROM checkout_claims LIMIT 1'); await realFetch(BASE + '/health'); return; } catch (e) { await new Promise(r => setTimeout(r, 100)); }
  }
  throw new Error('server never became ready');
}

(async () => {
  await waitForDb();

  // ── (d) session builder ──
  realLog('\n(d) buildMembershipCheckout');
  const anon = await buildMembershipCheckout({ user: null, plan: 'monthly', deviceId: 'dev-x', adClickId: 'gclid_build', adClickType: 'gclid' });
  const p1 = stripeCalls.sessionsCreate[0];
  check('anonymous: no customer_email', !('customer_email' in p1));
  check('anonymous: metadata.anon = 1 and no userId', p1.metadata.anon === '1' && !p1.metadata.userId);
  check('anonymous: click id rides in metadata', p1.metadata.adClickId === 'gclid_build' && p1.metadata.adClickType === 'gclid');
  check('anonymous: 7-day trial + card required', p1.subscription_data?.trial_period_days === 7 && p1.payment_method_collection === 'always');
  check('anonymous: monthly price 1999/month', p1.line_items[0].price_data.unit_amount === 1999 && p1.line_items[0].price_data.recurring.interval === 'month');
  check('anonymous: returns anon flag', anon.anon === true && anon.sessionId);
  const bad = await buildMembershipCheckout({ user: null, plan: 'lifetime' }).catch(e => e);
  check('invalid plan → 400', bad.status === 400);

  // logged-in path unchanged
  const su = await api('/api/auth/signup', { email: 'member@example.com', password: 'password123', deviceId: 'dev-m', adClickId: 'gclid_m' });
  check('signup works (fixture user)', su.status === 200 && su.data.token, su);
  const memberRow = await userByEmail('member@example.com');
  const li = await buildMembershipCheckout({ user: { id: memberRow.id, email: memberRow.email }, plan: 'annual', deviceId: 'dev-m' });
  const p2 = stripeCalls.sessionsCreate[stripeCalls.sessionsCreate.length - 1];
  check('logged in: customer_email set, userId in metadata, no anon', p2.customer_email === 'member@example.com' && p2.metadata.userId === String(memberRow.id) && !p2.metadata.anon);
  check('logged in: annual 6999/year', p2.line_items[0].price_data.unit_amount === 6999 && li.anon === false);

  // ── (a) new email ──
  realLog('\n(a) new email creates the account');
  const sidA = 'cs_test_a_' + 'x'.repeat(12);
  fixtureSessions[sidA] = anonSession(sidA, 'New.Buyer@Example.com ');
  const okA = await fulfillMembershipSession(fixtureSessions[sidA]);
  check('fulfil returns true', okA === true);
  const ua = await userByEmail('new.buyer@example.com');
  check('account created with normalised email', !!ua);
  check('membership applied: trialing / monthly / sub id / period end', ua && ua.membership_status === 'trialing' && ua.membership_plan === 'monthly' && ua.stripe_subscription_id === 'sub_' + sidA && !!ua.membership_period_end, ua && { s: ua.membership_status, p: ua.membership_plan });
  check('gclid recorded on the account', ua && ua.ads_click_id === 'gclid_' + sidA && ua.ads_click_type === 'gclid');
  check('device id from the cart', ua && ua.device_id === 'dev-' + sidA);
  const { rows: tokA } = await db.query('SELECT * FROM password_reset_tokens WHERE user_id = $1', [ua.id]);
  check('set-password token stored (hashed, 7 days)', tokA.length === 1 && tokA[0].token_hash.length === 64 && (new Date(tokA[0].expires_at) - Date.now()) > 6 * 86400 * 1000);
  const mailA = resendCalls.filter(m => m.to[0] === 'new.buyer@example.com');
  check('set-password email queued once, with a reset link', mailA.length === 1 && /set your password/i.test(mailA[0].subject) && /\?reset=[0-9a-f]{64}&welcome=1/.test(mailA[0].html), mailA.map(m => m.subject));
  const again = await fulfillMembershipSession(fixtureSessions[sidA]);
  check('second fulfil is a no-op', again === false && resendCalls.filter(m => m.to[0] === 'new.buyer@example.com').length === 1);

  // claim → logged in once
  const c1 = await api('/api/stripe/claim', { session_id: sidA });
  check('claim logs the paying browser in', c1.status === 200 && c1.data.created === true && c1.data.token && c1.data.email === 'new.buyer@example.com' && c1.data.deviceId === 'dev-' + sidA, c1);
  const me = await api('/api/auth/me', undefined, c1.data.token);
  check('claim token is a real session', me.status === 200 && me.data.email === 'new.buyer@example.com', me);
  const c2 = await api('/api/stripe/claim', { session_id: sidA });
  check('claim is single use', c2.status === 410 && !c2.data.token, c2);
  const mem = await api('/api/membership?deviceId=dev-' + sidA, undefined, c1.data.token);
  check('/api/membership says active', mem.status === 200 && mem.data.active === true && mem.data.status === 'trialing', mem.data);
  const sp = await api('/api/auth/set-password', { password: 'newpass123' }, c1.data.token);
  check('set-password accepted', sp.status === 200 && sp.data.ok === true, sp);
  const lg = await api('/api/auth/login', { email: 'new.buyer@example.com', password: 'newpass123', deviceId: 'dev-' + sidA });
  check('login with the new password works', lg.status === 200 && !!lg.data.token, lg);
  const { rows: tokA2 } = await db.query('SELECT * FROM password_reset_tokens WHERE user_id = $1', [ua.id]);
  check('emailed set-password link retired after set-password', tokA2.length === 0);
  const short = await api('/api/auth/set-password', { password: 'short' }, c1.data.token);
  check('set-password rejects < 8 chars', short.status === 400);
  const badClaim = await api('/api/stripe/claim', { session_id: 'cs_nope' });
  check('claim with a bad id → 400', badClaim.status === 400);
  const unknownClaim = await api('/api/stripe/claim', { session_id: 'cs_test_unknown_' + 'y'.repeat(12) });
  check('claim for an unknown session → 500 (retrieve failed), no token', unknownClaim.status >= 400 && !unknownClaim.data.token);

  // ── (b) existing email ──
  realLog('\n(b) existing email attaches, never logs in');
  const sb = await api('/api/auth/signup', { email: 'old@example.com', password: 'password123', deviceId: 'dev-old' });
  const ub0 = await userByEmail('old@example.com');
  await db.query("UPDATE users SET stripe_subscription_id = 'sub_previous', membership_status = 'canceled' WHERE id = $1", [ub0.id]);
  const before = (await db.query('SELECT count(*)::int AS n FROM users')).rows[0].n;
  const sidB = 'cs_test_b_' + 'x'.repeat(12);
  fixtureSessions[sidB] = anonSession(sidB, 'OLD@example.com');
  const okB = await fulfillMembershipSession(fixtureSessions[sidB]);
  const after = (await db.query('SELECT count(*)::int AS n FROM users')).rows[0].n;
  const ub = await userByEmail('old@example.com');
  check('fulfil returns true, no new account', okB === true && after === before);
  check('membership attached to the existing account', ub.membership_status === 'trialing' && ub.stripe_subscription_id === 'sub_' + sidB && ub.password_hash === ub0.password_hash);
  check('gclid recorded on the existing account', ub.ads_click_id === 'gclid_' + sidB);
  const mailB = resendCalls.filter(m => m.to[0] === 'old@example.com');
  check('"log in to continue" email, not a set-password one', mailB.length === 1 && /log in/i.test(mailB[0].subject) && !/reset=/.test(mailB[0].html), mailB.map(m => m.subject));
  const { rows: tokB } = await db.query('SELECT * FROM password_reset_tokens WHERE user_id = $1', [ub.id]);
  check('no reset token minted for the existing account', tokB.length === 0);
  check('TRIAL_REUSE logged', logs.some(l => l.startsWith('TRIAL_REUSE') && l.includes(`user ${ub.id}`)));
  const cb = await api('/api/stripe/claim', { session_id: sidB });
  check('claim returns existingAccount and NO token', cb.status === 200 && cb.data.existingAccount === true && !cb.data.token && cb.data.email === 'old@example.com', cb);
  const meB = await api('/api/auth/me', undefined, sb.data.token);
  check('the existing account itself still logs in normally', meB.status === 200);

  // ── (c) race ──
  realLog('\n(c) webhook racing the claim');
  const sidC = 'cs_test_c_' + 'x'.repeat(12);
  fixtureSessions[sidC] = anonSession(sidC, 'race@example.com');
  const [r1, r2, cc] = await Promise.all([
    fulfillMembershipSession(fixtureSessions[sidC]),
    fulfillMembershipSession(fixtureSessions[sidC]),
    api('/api/stripe/claim', { session_id: sidC }),
  ]);
  const { rows: usersC } = await db.query('SELECT id FROM users WHERE email = $1', ['race@example.com']);
  const { rows: claimsC } = await db.query('SELECT created FROM checkout_claims WHERE session_hash = $1', [server.sessionHash(sidC)]);
  check('both fulfils resolve, exactly one account', r1 === true && r2 === true && usersC.length === 1, { r1, r2, n: usersC.length });
  check('one claim row, created=true', claimsC.length === 1 && claimsC[0].created === true);
  check('one set-password email', resendCalls.filter(m => m.to[0] === 'race@example.com').length === 1);
  check('the racing claim logged the browser in', cc.status === 200 && cc.data.created === true && !!cc.data.token, cc);
  check('exactly one "activated" log line for the session', logs.filter(l => l.includes(`session ${sidC}`) && l.startsWith('Membership activated')).length === 1);

  // ── logged-in session regression ──
  realLog('\n(e) logged-in session (meta.userId) unchanged');
  const sidE = 'cs_test_e_' + 'x'.repeat(12);
  fixtureSessions[sidE] = { id: sidE, status: 'complete', payment_status: 'paid', customer: 'cus_e', subscription: 'sub_e', customer_details: { email: 'member@example.com' }, metadata: { kind: 'membership', plan: 'annual', userId: String(memberRow.id), deviceId: 'dev-m', creditDiscountCents: '0' } };
  const okE = await fulfillMembershipSession(fixtureSessions[sidE]);
  const ue = await userByEmail('member@example.com');
  check('member row updated: annual / trialing', okE === true && ue.membership_plan === 'annual' && ue.membership_status === 'trialing');
  check('no claim row, no email for a logged-in purchase', (await db.query('SELECT 1 FROM checkout_claims WHERE session_hash = $1', [server.sessionHash(sidE)])).rows.length === 0 && resendCalls.filter(m => m.to[0] === 'member@example.com').length === 0);
  const ce = await api('/api/stripe/claim', { session_id: sidE });
  check('claim on a logged-in session → 409 (no row), no token', ce.status === 409 && !ce.data.token, ce);
  const noEmail = { ...anonSession('cs_test_f_' + 'x'.repeat(12), ''), };
  fixtureSessions[noEmail.id] = noEmail;
  check('anonymous session without an email is refused', (await fulfillMembershipSession(noEmail)) === false);

  realLog(`\n${pass} passed, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { realLog('TEST CRASH', e); process.exit(2); });
