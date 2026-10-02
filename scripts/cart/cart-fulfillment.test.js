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
//   (f)-(n) the v2 cart (2026-10-02): sessions with Stripe's fields on the page,
//       and the Lifetime plan: setup creates the account and the pending row, the
//       sweep charges exactly once, a second sweep does nothing, cancel before
//       day 7 means no charge, a failed charge retries 3 days then access ends,
//       the webhook racing the browser still yields one account and one row.
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
process.env.DASH_SECRET = 'dash_test_stub';

const Module = require('module');
const path = require('path');

// ── Stripe stub ──
const stripeCalls = { sessionsCreate: [], sessionsCreateOpts: [], subscriptionsRetrieve: [], subscriptionsCancel: [], piCreate: [], piCreateOpts: [], customersCreate: [], attach: [] };
const fixtureSessions = {};
// Lifetime charge behaviour, set per test: 'ok', 'decline', 'crash' (not the
// card's fault), or a function. stripeIntents is what paymentIntents.list sees.
let chargeMode = 'ok';
const stripeIntents = [];
const cardError = () => Object.assign(new Error('Your card was declined.'), { type: 'StripeCardError', code: 'card_declined' });
const stripeStub = {
  checkout: {
    sessions: {
      create: async (params, opts) => { stripeCalls.sessionsCreate.push(params); stripeCalls.sessionsCreateOpts.push(opts); return { id: `cs_test_${stripeCalls.sessionsCreate.length}`, client_secret: 'cs_secret' }; },
      retrieve: async (sid) => { const s = fixtureSessions[sid]; if (!s) throw new Error('No such session: ' + sid); return s; },
    },
  },
  subscriptions: {
    retrieve: async (id) => { stripeCalls.subscriptionsRetrieve.push(id); return { id, status: 'trialing', trial_end: Math.floor(Date.now() / 1000) + 7 * 86400 }; },
    cancel: async (id) => { stripeCalls.subscriptionsCancel.push(id); return { id, status: 'canceled' }; },
  },
  setupIntents: { retrieve: async (id) => ({ id, status: 'succeeded', payment_method: 'pm_' + id, customer: 'cus_' + id }) },
  customers: {
    create: async (params) => { stripeCalls.customersCreate.push(params); return { id: 'cus_created_' + stripeCalls.customersCreate.length }; },
    retrieve: async (id) => ({ id, invoice_settings: { default_payment_method: null } }),
    listPaymentMethods: async () => ({ data: [{ id: 'pm_newest' }] }),
  },
  paymentMethods: { attach: async (id, params) => { stripeCalls.attach.push({ id, ...params }); return { id }; } },
  paymentIntents: {
    list: async ({ customer }) => ({ data: stripeIntents.filter((p) => p.customer === customer) }),
    create: async (params, opts) => {
      stripeCalls.piCreate.push(params); stripeCalls.piCreateOpts.push(opts);
      const mode = typeof chargeMode === 'function' ? chargeMode(params) : chargeMode;
      if (mode === 'decline') throw cardError();
      if (mode === 'crash') throw new Error('Stripe is unreachable');
      const pi = { id: 'pi_' + stripeCalls.piCreate.length, status: 'succeeded', customer: params.customer, metadata: params.metadata };
      stripeIntents.push(pi);
      return pi;
    },
    retrieve: async (id) => stripeIntents.find((p) => p.id === id),
    cancel: async (id) => ({ id, status: 'canceled' }),
  },
  accounts: { retrieve: async () => ({ settings: { payments: { statement_descriptor: 'ABS BY AI' } } }) },
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
const { db, fulfillMembershipSession, buildMembershipCheckout, lifetimeChargeSweep, chargeLifetimeRow, handleLifetimeIntentEvent } = server;
const BASE = `http://localhost:${process.env.PORT}`;

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; realLog(`  ✓ ${name}`); }
  else { fail++; realLog(`  ✗ ${name}${extra !== undefined ? ' — ' + JSON.stringify(extra) : ''}`); }
}
async function api(p, body, token, headers) {
  const r = await realFetch(BASE + p, {
    method: body === undefined ? 'GET' : 'POST',
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(headers || {}) },
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
// A completed Lifetime checkout: setup mode, no subscription, a setup intent.
function lifetimeSession(sid, email, extra = {}) {
  return {
    id: sid, mode: 'setup', status: 'complete', payment_status: 'no_payment_required', customer: 'cus_' + sid, subscription: null, setup_intent: 'seti_' + sid,
    customer_details: { email },
    metadata: { kind: 'membership', plan: 'lifetime', anon: '1', deviceId: 'dev-' + sid, creditDiscountCents: '0', adClickId: 'gclid_' + sid, adClickType: 'gclid', ...extra },
  };
}
async function lifetimeRows(userId) {
  const { rows } = await db.query('SELECT * FROM lifetime_pending WHERE user_id = $1 ORDER BY id', [userId]);
  return rows;
}
// Day 7 has arrived for this buyer's waiting row.
async function makeDue(userId) {
  await db.query(`UPDATE lifetime_pending SET next_attempt_at = now() - interval '1 minute' WHERE user_id = $1 AND status = 'pending'`, [userId]);
}
// One Lifetime buyer through checkout, with the browser logged in by the claim.
// The claim shares the login rate limit (20 per 15 minutes), so it is only
// made when the test needs the buyer's token.
async function buyLifetime(tag, email, { login = false } = {}) {
  const sid = `cs_test_${tag}_` + 'x'.repeat(12);
  fixtureSessions[sid] = lifetimeSession(sid, email);
  await fulfillMembershipSession(fixtureSessions[sid]);
  const claim = login ? await api('/api/stripe/claim', { session_id: sid }) : { data: {} };
  return { sid, user: await userByEmail(email.trim().toLowerCase()), token: claim.data.token };
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

  // ════════ v2 cart (2026-10-02) ════════
  const DAY = 86400 * 1000;
  const lastCreate = () => stripeCalls.sessionsCreate[stripeCalls.sessionsCreate.length - 1];
  const lastCreateOpts = () => stripeCalls.sessionsCreateOpts[stripeCalls.sessionsCreateOpts.length - 1];

  realLog('\n(f) v2 session builder: fields on the page, Monthly and Lifetime');
  await buildMembershipCheckout({ user: null, plan: 'monthly', deviceId: 'dev-v2', adClickId: 'gclid_v2', adClickType: 'gclid', ui: 'elements' });
  const pm = lastCreate();
  check('monthly v2: elements ui, subscription, 7-day trial, 1999/month', pm.ui_mode === 'elements' && pm.mode === 'subscription' && pm.subscription_data.trial_period_days === 7 && pm.line_items[0].price_data.unit_amount === 1999 && pm.line_items[0].price_data.recurring.interval === 'month');
  check('monthly v2: return url carries the session id, no embedded-only params', /cart_return=\{CHECKOUT_SESSION_ID\}/.test(pm.return_url) && !('redirect_on_completion' in pm));
  check('monthly v2: card and Link only', JSON.stringify(pm.allowed_payment_method_types) === '["card","link"]' && !('payment_method_types' in pm));
  check('monthly v2: Stripe API version named on the call', !!lastCreateOpts() && /^20\d\d-\d\d-\d\d\./.test(lastCreateOpts().apiVersion));
  check('old overlay session unchanged: embedded, no version override', stripeCalls.sessionsCreate[0].ui_mode === 'embedded' && stripeCalls.sessionsCreateOpts[0] === undefined);
  const lt = await buildMembershipCheckout({ user: null, plan: 'lifetime', deviceId: 'dev-v2', adClickId: 'gclid_v2', adClickType: 'gclid', ui: 'elements' });
  const pl = lastCreate();
  check('lifetime: setup mode, nothing recurring, nothing due', pl.mode === 'setup' && pl.ui_mode === 'elements' && !pl.line_items && !pl.subscription_data && pl.currency === 'usd');
  check('lifetime: a customer is always created, card and Link only', pl.customer_creation === 'always' && JSON.stringify(pl.allowed_payment_method_types) === '["card","link"]');
  check('lifetime: metadata plan + anon + click id', pl.metadata.kind === 'membership' && pl.metadata.plan === 'lifetime' && pl.metadata.anon === '1' && pl.metadata.adClickId === 'gclid_v2' && lt.anon === true);
  check('lifetime: what Stripe stores never says subscription or year', !/subscri|year|annual/i.test(JSON.stringify(pl)));
  await buildMembershipCheckout({ user: { id: memberRow.id, email: memberRow.email }, plan: 'lifetime', deviceId: 'dev-m', ui: 'elements' }).catch(e => e);
  await db.query("UPDATE users SET membership_status = NULL, membership_plan = NULL, membership_period_end = NULL WHERE id = $1", [memberRow.id]);
  await buildMembershipCheckout({ user: { id: memberRow.id, email: memberRow.email }, plan: 'lifetime', deviceId: 'dev-m', ui: 'elements' });
  check('lifetime logged in: email locked to the account, userId in metadata', lastCreate().customer_email === 'member@example.com' && lastCreate().metadata.userId === String(memberRow.id) && !lastCreate().metadata.anon);
  const cfg = await api('/api/config');
  check('/api/config serves the statement name read from Stripe', cfg.data.statementDescriptor === 'ABS BY AI', cfg.data);

  realLog('\n(g) Lifetime checkout: account + pending row, $0 today');
  const piBefore = stripeCalls.piCreate.length;
  const g = await buyLifetime('g', 'Life.Buyer@Example.com', { login: true });
  const gRows = await lifetimeRows(g.user.id);
  check('account created and logged in by the claim', !!g.user && !!g.token);
  check('trialing / lifetime, access ends in 7 days unless charged', g.user.membership_status === 'trialing' && g.user.membership_plan === 'lifetime' && Math.abs(new Date(g.user.membership_period_end) - Date.now() - 7 * DAY) < 60000, { s: g.user.membership_status, p: g.user.membership_plan });
  check('no subscription id, customer stored', !g.user.stripe_subscription_id && g.user.stripe_customer_id === 'cus_' + g.sid);
  check('one pending row: 6999, saved card, due in 7 days', gRows.length === 1 && gRows[0].status === 'pending' && gRows[0].amount_cents === 6999 && gRows[0].payment_method_id === 'pm_seti_' + g.sid && Math.abs(new Date(gRows[0].charge_at) - Date.now() - 7 * DAY) < 60000, gRows[0]);
  check('nothing charged at checkout', stripeCalls.piCreate.length === piBefore);
  check('gclid recorded, set-password email sent once', g.user.ads_click_id === 'gclid_' + g.sid && resendCalls.filter(m => m.to[0] === 'life.buyer@example.com').length === 1);
  check('second fulfil is a no-op, still one row', (await fulfillMembershipSession(fixtureSessions[g.sid])) === false && (await lifetimeRows(g.user.id)).length === 1);
  const gMem = await api('/api/membership?deviceId=x', undefined, g.token);
  check('/api/membership: active, lifetime, charge date for the hub', gMem.data.active === true && gMem.data.plan === 'lifetime' && gMem.data.lifetime && gMem.data.lifetime.state === 'pending' && gMem.data.lifetime.amountCents === 6999, gMem.data);

  realLog('\n(h) the sweep charges exactly once');
  await lifetimeChargeSweep();
  check('before day 7: the sweep charges nothing', stripeCalls.piCreate.length === piBefore);
  await makeDue(g.user.id);
  await lifetimeChargeSweep();
  const charge = stripeCalls.piCreate[stripeCalls.piCreate.length - 1];
  const chargeOpts = stripeCalls.piCreateOpts[stripeCalls.piCreateOpts.length - 1];
  check('day 7: one off-session charge of 6999 on the saved card', stripeCalls.piCreate.length === piBefore + 1 && charge.amount === 6999 && charge.currency === 'usd' && charge.off_session === true && charge.confirm === true && charge.customer === 'cus_' + g.sid && charge.payment_method === 'pm_seti_' + g.sid, charge);
  check('idempotency key built from the row id and the attempt', chargeOpts.idempotencyKey === `lifetime-${gRows[0].id}-attempt-1`, chargeOpts);
  check('receipt wording: one-time, never a subscription', /one-time/i.test(charge.description) && !/subscri|year|month/i.test(charge.description) && charge.receipt_email === 'life.buyer@example.com');
  const gPaid = await userByEmail('life.buyer@example.com');
  check('paid: active / lifetime / no period end (permanent)', gPaid.membership_status === 'active' && gPaid.membership_plan === 'lifetime' && gPaid.membership_period_end === null, { s: gPaid.membership_status, e: gPaid.membership_period_end });
  check('paid conversion stamped from the charge', !!gPaid.paid_conversion_pending_at && logs.some(l => l.startsWith('PAID_CONVERSION_PENDING') && l.includes('lifetime_charge:')));
  check('row is paid with the payment intent', (await lifetimeRows(g.user.id))[0].status === 'paid' && !!(await lifetimeRows(g.user.id))[0].payment_intent_id);
  await makeDue(g.user.id);
  await lifetimeChargeSweep();
  await lifetimeChargeSweep();
  const direct = await chargeLifetimeRow(gRows[0].id);
  check('a second and third sweep, and a direct call, charge nothing', stripeCalls.piCreate.length === piBefore + 1 && direct.result === 'skipped', direct);
  await handleLifetimeIntentEvent('payment_intent.succeeded', { id: 'pi_dup', metadata: { kind: 'lifetime', lifetimeId: String(gRows[0].id) } });
  check('a duplicate webhook does not rewrite the paid row', (await lifetimeRows(g.user.id))[0].payment_intent_id !== 'pi_dup');
  const gMem2 = await api('/api/membership?deviceId=x', undefined, g.token);
  check('/api/membership: lifetime member, paid, value 69.99', gMem2.data.active === true && gMem2.data.lifetime.state === 'paid' && gMem2.data.paidConversionValue === 69.99, gMem2.data);
  const gCancel = await api('/api/membership/cancel-lifetime', {}, g.token);
  check('after the charge there is nothing to cancel', gCancel.status === 400 && (await userByEmail('life.buyer@example.com')).membership_status === 'active', gCancel);
  const again2 = await buyLifetime('g2', 'life.buyer@example.com');
  check('a paid lifetime member checking out again opens no second charge', (await lifetimeRows(g.user.id)).length === 1 && again2.user.membership_status === 'active');

  realLog('\n(i) cancel before day 7: nothing is ever billed');
  const piI = stripeCalls.piCreate.length;
  const i1 = await buyLifetime('i', 'cancel@example.com', { login: true });
  const iCancel = await api('/api/membership/cancel-lifetime', {}, i1.token);
  const iUser = await userByEmail('cancel@example.com');
  check('cancel accepted, access runs to the end of the free 7 days', iCancel.status === 200 && iCancel.data.canceled === true && iCancel.data.active === true && iUser.membership_status === 'canceled' && new Date(iUser.membership_period_end) > new Date(), iCancel);
  check('the pending charge is removed', (await lifetimeRows(i1.user.id))[0].status === 'canceled');
  await db.query(`UPDATE lifetime_pending SET next_attempt_at = now() - interval '1 minute' WHERE user_id = $1`, [i1.user.id]);
  await lifetimeChargeSweep();
  check('day 7 arrives: no charge', stripeCalls.piCreate.length === piI);
  check('cancelling twice is harmless', (await api('/api/membership/cancel-lifetime', {}, i1.token)).status === 200);
  check('cancel needs a login', (await api('/api/membership/cancel-lifetime', {})).status === 401);

  realLog('\n(j) failed charge: retry once a day for 3 days, an email each time, then access ends');
  const j1 = await buyLifetime('j', 'decline@example.com', { login: true });
  const mailsJ = () => resendCalls.filter(m => m.to[0] === 'decline@example.com' && !/set your password/i.test(m.subject));
  chargeMode = 'decline';
  const piJ = stripeCalls.piCreate.length;
  await makeDue(j1.user.id);
  await lifetimeChargeSweep();
  let jRow = (await lifetimeRows(j1.user.id))[0];
  let jUser = await userByEmail('decline@example.com');
  check('day 7 decline: one try, row waits a day', stripeCalls.piCreate.length === piJ + 1 && jRow.status === 'pending' && jRow.attempts === 1 && Math.abs(new Date(jRow.next_attempt_at) - Date.now() - DAY) < 60000, jRow);
  check('still has access while retries remain (past_due)', jUser.membership_status === 'past_due' && new Date(jUser.membership_period_end) > new Date() && (await api('/api/membership?deviceId=x', undefined, j1.token)).data.active === true);
  check('email 1 says it will retry', mailsJ().length === 1 && /did not go through/i.test(mailsJ()[0].subject) && /next 3 days/.test(mailsJ()[0].html), mailsJ().map(m => m.subject));
  await lifetimeChargeSweep();
  check('no retry before a day has passed', stripeCalls.piCreate.length === piJ + 1);
  for (let n = 2; n <= 4; n++) { await makeDue(j1.user.id); await lifetimeChargeSweep(); }
  jRow = (await lifetimeRows(j1.user.id))[0];
  jUser = await userByEmail('decline@example.com');
  const keysJ = stripeCalls.piCreateOpts.slice(piJ).map(o => o.idempotencyKey);
  check('first try + 3 daily retries = 4 charges attempted, each with its own key', stripeCalls.piCreate.length === piJ + 4 && new Set(keysJ).size === 4 && keysJ[3] === `lifetime-${jRow.id}-attempt-4`, keysJ);
  check('a retry uses the newest card on the customer', stripeCalls.piCreate[piJ + 1].payment_method === 'pm_newest' && stripeCalls.piCreate[piJ].payment_method === 'pm_seti_' + j1.sid);
  check('then access ends: row failed, membership expired, not active', jRow.status === 'failed' && jRow.attempts === 4 && jUser.membership_status === 'expired' && jUser.membership_period_end === null && (await api('/api/membership?deviceId=x', undefined, j1.token)).data.active === false, { r: jRow.status, u: jUser.membership_status });
  check('an email each time: 3 retry notices + 1 access-ended', mailsJ().length === 4 && /access has ended/i.test(mailsJ()[3].subject) && mailsJ().slice(0, 3).every(m => /did not go through/i.test(m.subject)), mailsJ().map(m => m.subject));
  check('never stamped as a sale', !jUser.paid_conversion_pending_at);
  await makeDue(j1.user.id);
  await lifetimeChargeSweep();
  check('no further tries after access ended', stripeCalls.piCreate.length === piJ + 4);

  realLog('\n(k) a retry that works, and an outage that is not the card');
  const k1 = await buyLifetime('k', 'retry@example.com');
  await makeDue(k1.user.id);
  await lifetimeChargeSweep(); // declined once
  chargeMode = 'ok';
  await makeDue(k1.user.id);
  await lifetimeChargeSweep();
  const kUser = await userByEmail('retry@example.com');
  check('declined, then paid on the retry: lifetime member', kUser.membership_status === 'active' && kUser.membership_period_end === null && (await lifetimeRows(k1.user.id))[0].status === 'paid');
  const k2 = await buyLifetime('k2', 'outage@example.com');
  const mailsK2 = resendCalls.length;
  chargeMode = 'crash';
  await makeDue(k2.user.id);
  await lifetimeChargeSweep();
  let k2Row = (await lifetimeRows(k2.user.id))[0];
  check('Stripe outage: no strike, no email, row still waiting', k2Row.status === 'pending' && k2Row.attempts === 0 && /^error:/.test(k2Row.last_error) && resendCalls.length === mailsK2 && (await userByEmail('outage@example.com')).membership_status === 'trialing', k2Row);
  // A sweep died after Stripe took the money but before the row was written.
  stripeIntents.push({ id: 'pi_recovered', status: 'succeeded', customer: 'cus_' + k2.sid, metadata: { kind: 'lifetime', lifetimeId: String(k2Row.id) } });
  await db.query(`UPDATE lifetime_pending SET status = 'charging', last_attempt_at = now() - interval '20 minutes' WHERE id = $1`, [k2Row.id]);
  chargeMode = 'ok';
  const piK = stripeCalls.piCreate.length;
  await lifetimeChargeSweep();
  k2Row = (await lifetimeRows(k2.user.id))[0];
  check('crash recovery: the charge Stripe already took is recorded, not repeated', k2Row.status === 'paid' && k2Row.payment_intent_id === 'pi_recovered' && stripeCalls.piCreate.length === piK, k2Row);

  realLog('\n(l) switching plans never bills twice');
  const l1 = await buyLifetime('l', 'switch@example.com');
  const sidL = 'cs_test_l2_' + 'x'.repeat(12);
  fixtureSessions[sidL] = anonSession(sidL, 'switch@example.com');
  await fulfillMembershipSession(fixtureSessions[sidL]);
  const lUser = await userByEmail('switch@example.com');
  check('Lifetime trial then Monthly: the waiting Lifetime charge is removed', lUser.membership_plan === 'monthly' && (await lifetimeRows(l1.user.id))[0].status === 'canceled');
  const piL = stripeCalls.piCreate.length;
  await db.query(`UPDATE lifetime_pending SET next_attempt_at = now() - interval '1 minute' WHERE user_id = $1`, [l1.user.id]);
  await lifetimeChargeSweep();
  check('and the sweep leaves it alone', stripeCalls.piCreate.length === piL);
  const cancelsBefore = stripeCalls.subscriptionsCancel.length;
  const sidL3 = 'cs_test_l3_' + 'x'.repeat(12);
  fixtureSessions[sidL3] = lifetimeSession(sidL3, 'switch@example.com');
  await fulfillMembershipSession(fixtureSessions[sidL3]);
  const lUser2 = await userByEmail('switch@example.com');
  check('Monthly trial then Lifetime: the subscription is cancelled at Stripe', stripeCalls.subscriptionsCancel.length === cancelsBefore + 1 && stripeCalls.subscriptionsCancel[cancelsBefore] === 'sub_' + sidL && lUser2.membership_plan === 'lifetime' && lUser2.membership_status === 'trialing');
  check('existing account: never logged in by the claim', (await api('/api/stripe/claim', { session_id: sidL3 })).data.existingAccount === true);
  const sidL4 = 'cs_test_l4_' + 'x'.repeat(12);
  fixtureSessions[sidL4] = lifetimeSession(sidL4, 'switch@example.com');
  await fulfillMembershipSession(fixtureSessions[sidL4]);
  const lRows = await lifetimeRows(l1.user.id);
  check('two Lifetime checkouts: only the newest can be charged', lRows.filter(r => r.status === 'pending').length === 1 && lRows[lRows.length - 1].status === 'pending' && lRows.length === 3, lRows.map(r => r.status));

  realLog('\n(m) webhook racing the browser, Lifetime');
  const sidM = 'cs_test_m_' + 'x'.repeat(12);
  fixtureSessions[sidM] = lifetimeSession(sidM, 'liferace@example.com');
  const [m1, m2, mc] = await Promise.all([
    fulfillMembershipSession(fixtureSessions[sidM]),
    fulfillMembershipSession(fixtureSessions[sidM]),
    api('/api/stripe/claim', { session_id: sidM }),
  ]);
  const mUsers = (await db.query('SELECT id FROM users WHERE email = $1', ['liferace@example.com'])).rows;
  check('one account, one pending row, browser logged in', m1 === true && m2 === true && mUsers.length === 1 && (await lifetimeRows(mUsers[0].id)).length === 1 && mc.status === 200 && !!mc.data.token, { m1, m2, n: mUsers.length });
  check('one set-password email', resendCalls.filter(m => m.to[0] === 'liferace@example.com').length === 1);
  const noCard = lifetimeSession('cs_test_m2_' + 'x'.repeat(12), 'nocard@example.com');
  noCard.setup_intent = null;
  check('a Lifetime session with no saved card grants nothing', (await fulfillMembershipSession(noCard)) === false && (await userByEmail('nocard@example.com')).membership_status == null);

  realLog('\n(n) charge-now trigger for the live card test');
  const n1 = await buyLifetime('n', 'now@example.com');
  check('refused without the dashboard key', (await api('/api/admin/lifetime/charge-now', { email: 'now@example.com' })).status === 401);
  const piN = stripeCalls.piCreate.length;
  const now1 = await api('/api/admin/lifetime/charge-now', { email: 'now@example.com' }, null, { 'X-Dash-Key': 'dash_test_stub' });
  check('charges that buyer now and reports the result', now1.status === 200 && now1.data.result === 'paid' && now1.data.row.status === 'paid' && now1.data.membership.status === 'active' && now1.data.membership.periodEnd === null && stripeCalls.piCreate.length === piN + 1, now1.data);
  const now2 = await api('/api/admin/lifetime/charge-now', { email: 'now@example.com' }, null, { 'X-Dash-Key': 'dash_test_stub' });
  check('running it again charges nothing', now2.status === 409 && stripeCalls.piCreate.length === piN + 1, now2.data);

  realLog(`\n${pass} passed, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { realLog('TEST CRASH', e); process.exit(2); });
