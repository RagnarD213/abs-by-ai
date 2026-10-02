'use strict';
const express = require('express');
const crypto = require('crypto');
const path = require('path');
const {OAuth2Client} = require('google-auth-library');
const {validate} = require('./document');
const COOKIE = '__Host-absbyai_brief';
const AGE = 90 * 86400000;
const equal = (a, b) => {
  if (typeof a !== 'string' || typeof b !== 'string' || !a || !b) return false;
  const x = Buffer.from(a), y = Buffer.from(b);
  return x.length === y.length && crypto.timingSafeEqual(x, y);
};
function cookie(req, name) {
  try {
    const matches = (req.headers.cookie || '').split(';').map(s => s.trim()).filter(s => s.startsWith(name + '='));
    return matches.length === 1 ? decodeURIComponent(matches[0].slice(name.length + 1)) : '';
  } catch { return ''; }
}
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
const googleVerifier = (client = new OAuth2Client()) => async (token, audience) => (await client.verifyIdToken({idToken: token, audience})).getPayload();
function createRouter({store, env = process.env, verifyToken, now = Date.now}) {
  const router = express.Router();
  verifyToken ||= googleVerifier();
  const email = (env.BRIEF_OWNER_EMAIL || '').toLowerCase();
  const clientId = env.BRIEF_GOOGLE_CLIENT_ID || '';
  const origin = 'https://absbyai.com';
  const configured = () => /^[^\s@]+@gmail\.com$/.test(email) && /^\d+-[A-Za-z0-9_-]+\.apps\.googleusercontent\.com$/.test(clientId);
  const setCookie = (res, token, maxAge = AGE / 1000) => res.set('Set-Cookie', `${COOKIE}=${token}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`);
  router.use((req, res, next) => {
    const p = (req.path || '').toLowerCase().replace(/\/+$/, '');
    if (!['/morningbrief', '/morningbrief.html', '/brief-login', '/brief-publish'].includes(p) && !p.startsWith('/api/brief/')) return next('router');
    req.url = p + (req.url.includes('?') ? req.url.slice(req.url.indexOf('?')) : '');
    res.removeHeader('Access-Control-Allow-Origin');
    res.set({'Cache-Control':'private, no-store', 'Pragma':'no-cache', 'X-Content-Type-Options':'nosniff', 'Referrer-Policy':'no-referrer',
      'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"});
    next();
  });
  async function owner(req, res, next) {
    if (!configured()) return res.status(503).json({error:'Private sign-in is not configured'});
    try {
      const token = cookie(req, COOKIE);
      if (!/^[a-f0-9]{64}$/.test(token)) return deny();
      const [session, pinned] = await Promise.all([store.session(token), store.owner()]);
      if (!session || !pinned || pinned.email !== email || session.google_sub !== pinned.google_sub ||
          (env.BRIEF_OWNER_GOOGLE_SUB && pinned.google_sub !== env.BRIEF_OWNER_GOOGLE_SUB) || !Number.isFinite(new Date(session.expires_at).getTime()) || new Date(session.expires_at).getTime() <= now()) return deny();
      if (new Date(session.expires_at).getTime() < now() + AGE * 2 / 3) { await store.renew(token, now() + AGE); setCookie(res, token); }
      req.briefToken = token;
      return next();
    } catch { return res.status(503).json({error:'Private session check unavailable'}); }
    function deny() {
      if (req.path.startsWith('/api/')) return res.status(401).json({error:'Unauthorized'});
      return res.redirect(303, '/brief-login');
    }
  }
  function ingest(req, res, next) {
    const key = env.BRIEF_INGEST_SECRET || '';
    // Browser publication uses the existing owner session and a same-origin
    // custom-header check. No ingestion secret is needed for the manual proof.
    if (req.headers.origin === origin && req.headers['x-brief-action'] === 'publish') return owner(req, res, next);
    if (key.length < 32) return res.status(503).json({error:'Automated private publication is not configured'});
    return equal(req.headers['x-brief-ingest-key'], key) ? next() : res.status(401).json({error:'Unauthorized'});
  }
  const file = name => (req, res) => res.sendFile(path.join(__dirname, name));
  router.get('/brief-login', (req, res) => {
    if (!configured()) return res.status(503).type('html').send('<!doctype html><title>Private brief</title><p>Private Google sign-in is awaiting setup.</p>');
    res.set('Content-Security-Policy', "default-src 'none'; script-src https://accounts.google.com/gsi/client; style-src 'unsafe-inline' https://accounts.google.com; frame-src https://accounts.google.com; connect-src https://accounts.google.com; frame-ancestors 'none'; base-uri 'none'; form-action https://absbyai.com");
    res.type('html').send(`<!doctype html><html lang="en"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Your private brief</title><style>body{font:18px/1.6 system-ui;background:#f5f7f4;color:#172126;max-width:440px;margin:12vh auto;padding:24px}h1{font-size:30px}</style><h1>Your private morning brief</h1><p>Sign in with your designated Google account. This device can stay signed in.</p><script src="https://accounts.google.com/gsi/client" async></script><div id="g_id_onload" data-client_id="${escape(clientId)}" data-ux_mode="redirect" data-login_uri="${origin}/api/brief/auth/google" data-auto_prompt="false"></div><div class="g_id_signin" data-type="standard" data-size="large" data-text="signin_with"></div></html>`);
  });
  router.post('/api/brief/auth/google', express.urlencoded({extended:false, limit:'32kb'}), async (req, res) => {
    if (!configured()) return res.status(503).json({error:'Private sign-in is not configured'});
    const csrf = cookie(req, 'g_csrf_token');
    if (!equal(csrf, req.body?.g_csrf_token) || typeof req.body?.credential !== 'string' || req.body.credential.length > 20000) return res.status(403).json({error:'Sign-in rejected'});
    try {
      const p = await verifyToken(req.body.credential, clientId);
      if (!p || p.aud !== clientId || !['accounts.google.com','https://accounts.google.com'].includes(p.iss) ||
          !Number.isFinite(p.exp) || p.exp * 1000 <= now() || !Number.isFinite(p.iat) || p.iat * 1000 > now() + 300000 ||
          p.email_verified !== true || String(p.email).toLowerCase() !== email || !/^[A-Za-z0-9_-]{1,255}$/.test(p.sub || '') ||
          (env.BRIEF_OWNER_GOOGLE_SUB && p.sub !== env.BRIEF_OWNER_GOOGLE_SUB)) return res.status(403).json({error:'Sign-in rejected'});
      // Only the configured, verified Gmail owner can initialize this persistent pin.
      const pinned = await store.pinOwner(email, p.sub);
      if (!pinned || pinned.email !== email || pinned.google_sub !== p.sub) return res.status(403).json({error:'Sign-in rejected'});
      const token = crypto.randomBytes(32).toString('hex');
      await store.addSession(token, p.sub, now() + AGE);
      setCookie(res, token);
      return res.redirect(303, '/morningbrief');
    } catch { return res.status(403).json({error:'Sign-in rejected'}); }
  });
  router.get(['/morningbrief','/morningbrief.html'], owner, file('page.html'));
  router.get('/brief-publish', owner, file('publish.html'));
  router.get('/api/brief/page.js', owner, file('page.js'));
  router.get('/api/brief/publish.js', owner, file('publish.js'));
  router.get('/api/brief/style.css', owner, file('style.css'));
  router.get('/api/brief/data', owner, async (req, res) => {
    try {
      const document = await store.readDocument();
      if (!document) return res.status(404).json({error:'No verified brief has been published yet'});
      return res.json(validate(document, now()));
    } catch { return res.status(503).json({error:'Verified brief unavailable'}); }
  });
  router.get('/api/brief/image', owner, async (req, res) => {
    try {
      const image = await store.readImage();
      if (!image || !['image/png','image/jpeg'].includes(image.mime)) return res.sendStatus(404);
      return res.type(image.mime).send(image.bytes);
    } catch { return res.status(503).json({error:'Private image unavailable'}); }
  });
  router.post('/api/brief/logout', owner, async (req, res) => {
    if (req.headers.origin !== origin || req.headers['x-brief-action'] !== 'logout') return res.sendStatus(403);
    try { await store.logout(req.briefToken); setCookie(res, '', 0); return res.json({ok:true}); }
    catch { return res.status(503).json({error:'Sign-out unavailable'}); }
  });
  router.post('/api/brief/publish', ingest, express.json({limit:'512kb'}), async (req, res) => {
    let document;
    try { document = validate(req.body, now()); } catch { return res.status(400).json({error:'Invalid brief document'}); }
    try { await store.writeDocument(document); return res.json({ok:true, forDate:document.forDate, routineEnabled:false}); }
    catch { return res.status(503).json({error:'Private publication unavailable'}); }
  });
  // Image generation/upload remains unconfigured. Future upload must use a separate
  // authenticated ingest path; this owner-only read route never serves public files.
  router.use((req, res) => res.sendStatus(404));
  return router;
}
module.exports = {createRouter, COOKIE, AGE, cookie, googleVerifier};
