const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const { pool: db, initDb } = require('./db');

const app = express();

// Middleware
app.use(cors());

// Stripe webhook MUST receive the raw request body for signature verification,
// so it is registered BEFORE the global express.json() parser below. Defined
// here for ordering; the fulfillment logic lives with the other credits code.
app.post('/api/stripe/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const stripe = getStripe();
  if (!stripe || !STRIPE_WEBHOOK_SECRET) return res.status(503).send('webhook not configured');

  let event;
  try {
    event = stripe.webhooks.constructEvent(req.body, req.headers['stripe-signature'], STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Stripe webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  if (event.type === 'checkout.session.completed') {
    try {
      const meta = event.data.object.metadata || {};
      // Three kinds of checkout share this webhook: credit-pack purchases
      // (meta.kind === 'credits'), membership subscriptions (meta.kind ===
      // 'membership'), and printed-product orders (meta.productType).
      if (meta.productType) {
        await fulfillProductOrder(event.data.object);
      } else if (meta.kind === 'membership') {
        await fulfillMembershipSession(event.data.object);
      } else {
        await fulfillCreditsSession(event.data.object);
      }
    } catch (e) {
      console.error('Webhook fulfillment error:', e.message);
      // Return 200 anyway — session-status on return is a fallback path.
    }
  } else if (event.type === 'customer.subscription.updated' || event.type === 'customer.subscription.deleted') {
    // Keep member state in sync across renewals, cancellations, and payment
    // failures. Stripe keeps status 'active' with cancel_at_period_end until
    // the period actually ends, so storing status + period_end is enough.
    try { await syncSubscriptionState(event.data.object); }
    catch (e) { console.error('Subscription sync error:', e.message); }
  }
  res.json({ received: true });
});

app.use(express.json({ limit: '100mb' }));

// Rate limiting: applied ONLY to the expensive AI endpoints (photo check,
// prompt + image generation). Dashboard/task endpoints are polled frequently
// (auto-sync, rapid task toggles), so a global limiter would 429 normal use.
const aiLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  message: 'Too many requests, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// API Keys from environment variables
const ANTHROPIC_API_KEY   = process.env.ANTHROPIC_API_KEY;
const GEMINI_API_KEY      = process.env.GEMINI_API_KEY;
const POSTHOG_API_KEY     = process.env.POSTHOG_API_KEY;
const POSTHOG_PROJECT_ID  = process.env.POSTHOG_PROJECT_ID;
const OURA_ACCESS_TOKEN   = process.env.OURA_ACCESS_TOKEN;
const GOOGLE_CLIENT_ID     = process.env.GOOGLE_CLIENT_ID;
const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const GOOGLE_REFRESH_TOKEN = process.env.GOOGLE_REFRESH_TOKEN;
const GITHUB_TOKEN         = process.env.GITHUB_TOKEN;
const STRIPE_SECRET_KEY    = process.env.STRIPE_SECRET_KEY;
const STRIPE_PUBLISHABLE_KEY = process.env.STRIPE_PUBLISHABLE_KEY;
const STRIPE_WEBHOOK_SECRET  = process.env.STRIPE_WEBHOOK_SECRET;
const PRINTIFY_API_KEY     = process.env.PRINTIFY_API_KEY;
const PRINTIFY_SHOP_ID     = process.env.PRINTIFY_SHOP_ID;
const MAILERLITE_API_KEY   = process.env.MAILERLITE_API_KEY;
const MAILERLITE_GROUP_ID  = process.env.MAILERLITE_GROUP_ID;
const SUBSCRIBERS_FILE     = 'subscribers-data.json'; // persists captured emails (repo is private — contains PII)
const CREDITS_FILE         = 'credits-data.json'; // persists per-device credit balances + fulfilled checkout sessions
const FREE_CREDITS         = 3;  // free generations every new device starts with
// Credit packs offered on the paywall. Prices in cents. Keys must match the
// data-pack attributes in index.html (starter / power).
const COUNSEL_MONTHLY_CAP = 25; // full Supplement Audits per account per calendar month

const CREDIT_PACKS = {
  starter: { credits: 5,  priceInCents: 499,  label: 'Starter Pack' },
  power:   { credits: 20, priceInCents: 1499, label: 'Power Pack' },
};
// Membership plans (Stripe subscriptions). Keys must match data-plan
// attributes in index.html. Annual ≈ $5.83/mo is the anti-churn lever.
const MEMBERSHIP_PLANS = {
  monthly: { priceInCents: 1999, interval: 'month', label: 'Monthly Membership' },
  annual:  { priceInCents: 6999, interval: 'year',  label: 'Annual Membership' },
};
// Free (non-member) allowance of meal-photo analyses — the freemium taste.
const FREE_MEAL_ANALYSES = 3;
// exercises.js lives in public/ (browser loads it at /exercises.js); the server
// also uses its exports here, so require it from the new location.
const { EXERCISE_BY_ID, exercisesForEquipment } = require('./public/exercises');
const MONARCH_PUSH_SECRET  = process.env.MONARCH_PUSH_SECRET;
const MONARCH_DATA_FILE    = 'monarch-data.json';
const GITHUB_REPO          = 'RagnarD213/abs-by-ai';
const WATCH_DATA_FILE      = 'watch-data.json'; // persists parsed watch data across deploys

if (!ANTHROPIC_API_KEY || !GEMINI_API_KEY) {
  console.error('ERROR: Missing ANTHROPIC_API_KEY or GEMINI_API_KEY environment variables');
  process.exit(1);
}

// ============================================================
// DASHBOARD â serve at /dashboard
// ============================================================
app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// ============================================================
// MORNING DATA API â aggregates all data sources
// ============================================================
app.get('/api/morning-data', async (req, res) => {
  const userDate = req.query.date || null;      // YYYY-MM-DD in user's local time
  const tzOffset = parseInt(req.query.tz) || 0; // minutes east of UTC (e.g. -300 for CDT)

  const result = {
    posthog: null,
    stripe: null,
    oura: null,
    watch: null,
    todos: { business: [], health: [], personal: [] },
    task_checks: { checked: [], log: {} },
    plan: { date: null, order: [], excluded: [] },
    business_events: null,
    rel_events: null,
    news: [],
  };

  // Run all fetches in parallel
  await Promise.allSettled([
    fetchPosthog().then(d => { result.posthog = d; }),
    fetchStripe().then(d => { result.stripe = d; }),
    fetchOura().then(d => { result.oura = d; }),
    fetchGoogleCalendar(userDate, tzOffset).then(d => {
      result.business_events = d.business;
      result.rel_events = d.relationships;
    }),
    fetchNews().then(d => { result.news = d; }),
    loadTodos().then(d => { result.todos = d; }),
    loadTaskChecks().then(d => { result.task_checks = { checked: d.checked, log: d.log }; }),
    loadPlan().then(d => { result.plan = d; }),
  ]);

  result.watch = loadWatch();

  await fetchMonarch().then(d => { result.monarch = d; }).catch(() => {});

  res.json(result);
});

// ââ PostHog ââ
async function fetchPosthog() {
  if (!POSTHOG_API_KEY || !POSTHOG_PROJECT_ID) return null;
  try {
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    const twoDaysAgo = new Date(today);
    twoDaysAgo.setDate(today.getDate() - 2);

    const dateStr     = today.toISOString().split('T')[0];
    const yestStr     = yesterday.toISOString().split('T')[0];
    const twoDaysStr  = twoDaysAgo.toISOString().split('T')[0];

    // Query daily active users, signups, and image generations
    const queries = [
      { event: '$pageview',          label: 'dau' },
      { event: 'purchase_completed', label: 'signups' },
      { event: 'generation_created', label: 'images' },
    ];

    const results = {};
    await Promise.all(queries.map(async ({ event, label }) => {
      const body = {
        query: {
          kind: 'TrendsQuery',
          series: [{ kind: 'EventsNode', event }],
          dateRange: { date_from: twoDaysStr, date_to: dateStr },
          interval: 'day',
        },
      };

      const r = await fetch(
        `https://us.posthog.com/api/projects/${POSTHOG_PROJECT_ID}/query`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${POSTHOG_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body),
        }
      );

      if (!r.ok) return;
      const data = await r.json();
      const series = data?.results?.[0];
      if (!series) return;

      const vals = series.data || [];
      const today_val = vals[vals.length - 1] ?? 0;
      const prev_val  = vals[vals.length - 2] ?? 0;
      const chg = prev_val > 0 ? Math.round(((today_val - prev_val) / prev_val) * 100) : 0;

      results[label]          = today_val;
      results[`${label}_chg`] = chg;
    }));

    return Object.keys(results).length ? results : null;
  } catch (e) {
    console.error('PostHog error:', e.message);
    return null;
  }
}

// ââ Oura Ring ââ
// ── Stripe (MRR + active subscribers + 30-day revenue) ──
let stripeClient = null;
function getStripe() {
  if (!STRIPE_SECRET_KEY) return null;
  if (!stripeClient) stripeClient = require('stripe')(STRIPE_SECRET_KEY);
  return stripeClient;
}

async function fetchStripe() {
  const stripe = getStripe();
  if (!stripe) return null;
  try {
    // MRR + active subscriber count: page through active subscriptions.
    let mrrCents = 0;
    let activeSubs = 0;
    let starting_after;
    for (let page = 0; page < 10; page++) { // cap at 1000 subs
      const params = { status: 'active', limit: 100, expand: ['data.items.data.price'] };
      if (starting_after) params.starting_after = starting_after;
      const subs = await stripe.subscriptions.list(params);
      for (const sub of subs.data) {
        activeSubs++;
        for (const item of sub.items.data) {
          const price = item.price;
          if (!price || !price.unit_amount) continue;
          const qty = item.quantity || 1;
          const interval = price.recurring?.interval;
          const count = price.recurring?.interval_count || 1;
          let monthly = price.unit_amount * qty;
          if (interval === 'year')      monthly = monthly / (12 * count);
          else if (interval === 'week') monthly = monthly * (52 / 12) / count;
          else if (interval === 'day')  monthly = monthly * (365 / 12) / count;
          else                          monthly = monthly / count; // month
          mrrCents += monthly;
        }
      }
      if (!subs.has_more) break;
      starting_after = subs.data[subs.data.length - 1]?.id;
    }

    // 30-day gross revenue from succeeded charges.
    const since = Math.floor(Date.now() / 1000) - 30 * 24 * 3600;
    let revenueCents = 0;
    let chargeStart;
    for (let page = 0; page < 10; page++) { // cap at 1000 charges
      const params = { limit: 100, created: { gte: since } };
      if (chargeStart) params.starting_after = chargeStart;
      const charges = await stripe.charges.list(params);
      for (const c of charges.data) {
        if (c.paid && c.status === 'succeeded') revenueCents += (c.amount - (c.amount_refunded || 0));
      }
      if (!charges.has_more) break;
      chargeStart = charges.data[charges.data.length - 1]?.id;
    }

    return {
      mrr: Math.round(mrrCents / 100),
      active_subs: activeSubs,
      revenue_30d: Math.round(revenueCents / 100),
    };
  } catch (e) {
    console.error('Stripe error:', e.message);
    return null;
  }
}

async function fetchOura() {
  if (!OURA_ACCESS_TOKEN) return null;
  try {
    // Oura records sleep under the WAKE date (not fall-asleep date).
    // end_date is exclusive, so to fetch date X we need end_date = X+1.
    // We fetch yesterdayâtomorrow so we get both today's sleep (last night)
    // and yesterday's as a fallback if today hasn't synced yet.
    const now = new Date();
    const yesterday = new Date(now); yesterday.setDate(now.getDate() - 1);
    const tomorrow  = new Date(now); tomorrow.setDate(now.getDate() + 1);
    const weekAgo   = new Date(now); weekAgo.setDate(now.getDate() - 7);
    const yStr   = yesterday.toISOString().split('T')[0];
    const tStr   = now.toISOString().split('T')[0];
    const tmrStr = tomorrow.toISOString().split('T')[0];
    const wStr   = weekAgo.toISOString().split('T')[0];

    // Fetch a 7-day window so we can build trends + rolling averages, plus
    // daily_activity for step history (Oura tracks steps too).
    const oura = (path) => fetch(`https://api.ouraring.com/v2/usercollection/${path}`, {
      headers: { 'Authorization': `Bearer ${OURA_ACCESS_TOKEN}` },
    });
    const [sleepRes, dailySleepRes, readinessRes, activityRes] = await Promise.all([
      oura(`sleep?start_date=${wStr}&end_date=${tmrStr}`),
      oura(`daily_sleep?start_date=${wStr}&end_date=${tmrStr}`),
      oura(`daily_readiness?start_date=${wStr}&end_date=${tmrStr}`),
      oura(`daily_activity?start_date=${wStr}&end_date=${tmrStr}`),
    ]);

    const sleepData      = sleepRes.ok      ? await sleepRes.json()      : null;
    const dailySleepData = dailySleepRes.ok ? await dailySleepRes.json() : null;
    const readinessData  = readinessRes.ok  ? await readinessRes.json()  : null;
    const activityData   = activityRes.ok   ? await activityRes.json()   : null;

    const toMins = (secs) => secs ? Math.round(secs / 60) : 0;

    // Prefer today's long_sleep (last night), fall back to yesterday's
    const allPeriods = sleepData?.data?.filter(p => p.type === 'long_sleep') || [];
    const main = allPeriods.find(p => p.day === tStr) || allPeriods.find(p => p.day === yStr);

    if (!main) return null;

    // Sleep score comes from daily_sleep endpoint, not sleep periods
    const allDailySleep = dailySleepData?.data || [];
    const dailySleep = allDailySleep.find(d => d.day === tStr) || allDailySleep.find(d => d.day === yStr);
    const sleepScore = dailySleep?.score ?? null;

    // Readiness: prefer today's, fall back to yesterday's
    const allReadiness = readinessData?.data || [];
    const readinessScore = (allReadiness.find(r => r.day === tStr) || allReadiness.find(r => r.day === yStr))?.score ?? null;

    // ── 7-day trends + rolling averages ──
    // Build the last 7 calendar days (oldest→newest) and map each metric onto it.
    const days = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date(now); d.setDate(now.getDate() - i);
      days.push(d.toISOString().split('T')[0]);
    }
    const byDay = (arr, key) => {
      const m = {};
      (arr || []).forEach(x => { if (x.day != null && x[key] != null) m[x.day] = x[key]; });
      return m;
    };
    const sleepByDay     = byDay(allDailySleep, 'score');
    const readinessByDay = byDay(allReadiness, 'score');
    const stepsByDay     = byDay(activityData?.data, 'steps');
    // HRV per night from sleep periods (long_sleep), keyed by wake day.
    const hrvByDay = {};
    (allPeriods || []).forEach(p => { if (p.average_hrv != null) hrvByDay[p.day] = Math.round(p.average_hrv); });

    const series = (map) => days.map(d => (map[d] != null ? map[d] : null));
    const avg = (vals) => {
      const nums = vals.filter(v => v != null);
      return nums.length ? Math.round(nums.reduce((a, b) => a + b, 0) / nums.length) : null;
    };
    const sleepSeries     = series(sleepByDay);
    const readinessSeries = series(readinessByDay);
    const stepsSeries     = series(stepsByDay);
    const hrvSeries       = series(hrvByDay);

    const trend = {
      days,
      sleep:     sleepSeries,
      readiness: readinessSeries,
      steps:     stepsSeries,
      hrv:       hrvSeries,
      avg_sleep:     avg(sleepSeries),
      avg_readiness: avg(readinessSeries),
      avg_steps:     avg(stepsSeries),
      avg_hrv:       avg(hrvSeries),
    };

    return {
      trend,
      score: sleepScore,
      total_sleep: toMins(main.total_sleep_duration),
      hrv_avg: main.average_hrv ?? null,
      rem:    toMins(main.rem_sleep_duration),
      deep:   toMins(main.deep_sleep_duration),
      light:  toMins(main.light_sleep_duration),
      awake:  toMins(main.awake_time),
      efficiency: main.efficiency ?? null,           // sleep efficiency %
      latency_mins: toMins(main.latency ?? 0),      // minutes to fall asleep
      readiness: readinessScore,
      contributors: {
        total_sleep: dailySleep?.contributors?.total_sleep ?? null,
        efficiency:  dailySleep?.contributors?.efficiency  ?? null,
        restfulness: dailySleep?.contributors?.restfulness ?? null,
        rem_sleep:   dailySleep?.contributors?.rem_sleep   ?? null,
        deep_sleep:  dailySleep?.contributors?.deep_sleep  ?? null,
        latency:     dailySleep?.contributors?.latency     ?? null,
        timing:      dailySleep?.contributors?.timing      ?? null,
      },
    };
  } catch (e) {
    console.error('Oura error:', e.message);
    return null;
  }
}

// ââ Google Calendar ââ
let googleAccessToken = null;
let googleTokenExpiry = 0;

async function getGoogleToken() {
  if (!GOOGLE_CLIENT_ID || !GOOGLE_CLIENT_SECRET || !GOOGLE_REFRESH_TOKEN) return null;
  if (googleAccessToken && Date.now() < googleTokenExpiry) return googleAccessToken;

  try {
    const r = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id:     GOOGLE_CLIENT_ID,
        client_secret: GOOGLE_CLIENT_SECRET,
        refresh_token: GOOGLE_REFRESH_TOKEN,
        grant_type:    'refresh_token',
      }),
    });
    if (!r.ok) return null;
    const d = await r.json();
    googleAccessToken = d.access_token;
    googleTokenExpiry = Date.now() + (d.expires_in - 60) * 1000;
    return googleAccessToken;
  } catch (e) {
    console.error('Google token error:', e.message);
    return null;
  }
}

// ── Calendar debug endpoint (temp) ──
app.get('/api/calendar-debug', async (req, res) => {
  const token = await getGoogleToken();
  if (!token) return res.json({ error: 'no_token' });

  const userDate = req.query.date || new Date().toISOString().slice(0, 10);
  const tzOffsetMins = parseInt(req.query.tz) || 0;
  const [y, m, d] = userDate.split('-').map(Number);
  const offsetMs = tzOffsetMins * 60 * 1000;
  const startOfDay = new Date(Date.UTC(y, m - 1, d) - offsetMs).toISOString();
  const endOfDay   = new Date(Date.UTC(y, m - 1, d, 23, 59, 59) - offsetMs).toISOString();

  // Get calendar list
  const calListRes = await fetch('https://www.googleapis.com/calendar/v3/users/me/calendarList',
    { headers: { 'Authorization': `Bearer ${token}` } });
  const calListStatus = calListRes.status;
  const calListData = calListRes.ok ? await calListRes.json() : null;
  const calendars = (calListData?.items || []).map(c => ({ id: c.id, summary: c.summary, role: c.accessRole }));

  // Query each calendar individually and collect results
  const perCalendar = [];
  const calIds = ['primary', ...calendars.map(c => c.id)];
  const uniqueIds = [...new Set(calIds)];
  for (const calId of uniqueIds) {
    const r = await fetch(
      `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calId)}/events?timeMin=${encodeURIComponent(startOfDay)}&timeMax=${encodeURIComponent(endOfDay)}&singleEvents=true`,
      { headers: { 'Authorization': `Bearer ${token}` } });
    const status = r.status;
    if (r.ok) {
      const data = await r.json();
      const events = (data.items || []).map(ev => ({ id: ev.id, title: ev.summary, time: ev.start?.dateTime || ev.start?.date, status: ev.status }));
      perCalendar.push({ calId, status, eventCount: events.length, events });
    } else {
      const errText = await r.text().catch(() => '');
      perCalendar.push({ calId, status, error: errText.slice(0, 200) });
    }
  }

  res.json({ token_ok: true, startOfDay, endOfDay, calListStatus, perCalendar });
});

// Dating app keywords to route events to Relationships column
const DATING_KEYWORDS = ['hinge', 'bumble', 'tinder', 'coffee', 'date', 'meet'];

async function fetchGoogleCalendar(userDate, tzOffsetMins) {
  const empty = { business: null, relationships: null };
  const token = await getGoogleToken();
  if (!token) return empty;

  try {
    // Build the user's local-day boundaries in UTC.
    // Railway runs UTC — if we just use new Date(y,m,d) we get UTC boundaries,
    // but a 7 PM Central event = midnight UTC = outside the old end-of-day cutoff.
    let startOfDay, endOfDay;
    if (userDate) {
      const [y, m, d] = userDate.split('-').map(Number);
      // tzOffsetMins < 0 for US (e.g. CDT = -300). offsetMs is also negative.
      const offsetMs = (tzOffsetMins || 0) * 60 * 1000;
      startOfDay = new Date(Date.UTC(y, m - 1, d) - offsetMs).toISOString();
      endOfDay   = new Date(Date.UTC(y, m - 1, d, 23, 59, 59) - offsetMs).toISOString();
    } else {
      // Fallback: ±14 h window covers any timezone
      const now = new Date();
      startOfDay = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()) - 14 * 3600000).toISOString();
      endOfDay   = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 23, 59, 59) + 14 * 3600000).toISOString();
    }

    // Query ALL user calendars, not just `primary`.
    // Events on secondary calendars (dating, family, work) were silently missed.
    const calListRes = await fetch(
      'https://www.googleapis.com/calendar/v3/users/me/calendarList',
      { headers: { 'Authorization': `Bearer ${token}` } }
    );
    let calendarIds = ['primary'];
    if (calListRes.ok) {
      const calListData = await calListRes.json();
      const ids = (calListData.items || [])
        .filter(cal => ['owner', 'writer', 'reader'].includes(cal.accessRole) && !cal.deleted)
        .map(cal => cal.id);
      if (ids.length) calendarIds = ids;
    }

    const allItems = [];
    await Promise.all(calendarIds.map(async (calId) => {
      try {
        const r = await fetch(
          `https://www.googleapis.com/calendar/v3/calendars/${encodeURIComponent(calId)}/events?` +
          `timeMin=${encodeURIComponent(startOfDay)}&timeMax=${encodeURIComponent(endOfDay)}` +
          `&singleEvents=true&orderBy=startTime`,
          { headers: { 'Authorization': `Bearer ${token}` } }
        );
        if (!r.ok) return;
        const data = await r.json();
        allItems.push(...(data.items || []));
      } catch (_) { /* skip individual calendar errors */ }
    }));

    // Deduplicate by event id (shared calendars can surface duplicates)
    const seen = new Set();
    const items = allItems
      .filter(ev => { if (seen.has(ev.id)) return false; seen.add(ev.id); return true; })
      .sort((a, b) => (a.start?.dateTime || a.start?.date || '').localeCompare(b.start?.dateTime || b.start?.date || ''));

    const business = [];
    const relationships = [];

    items.forEach(ev => {
      const title = ev.summary || 'Untitled';
      const startTime = ev.start?.dateTime;
      // Extract wall-clock time directly from the RFC3339 string so the
      // server's UTC timezone doesn't corrupt the displayed time.
      // e.g. "2026-06-22T19:00:00-05:00" → "7:00 PM"
      let timeStr = 'All day';
      if (startTime) {
        const m = startTime.match(/T(\d{2}):(\d{2})/);
        if (m) {
          const h = parseInt(m[1], 10), min = m[2];
          const ampm = h >= 12 ? 'PM' : 'AM';
          const h12 = h % 12 || 12;
          timeStr = `${h12}:${min} ${ampm}`;
        } else {
          timeStr = new Date(startTime).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
        }
      }

      const event = { title, time: timeStr, subtitle: ev.location || '' };
      const lc = title.toLowerCase();

      if (DATING_KEYWORDS.some(k => lc.includes(k))) {
        relationships.push(event);
      } else {
        business.push(event);
      }
    });

    return {
      business:      business.length ? business : [],
      relationships: relationships.length ? relationships : [],
    };
  } catch (e) {
    console.error('Calendar error:', e.message);
    return empty;
  }
}

// ââ News (Google News RSS â no key required) ââ
const NEWS_QUERIES = [
  'AI fitness app',
  'AI body transformation',
  'fitness AI startup',
];

function parseRSS(xml) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/g;
  let match;
  while ((match = itemRegex.exec(xml)) !== null && items.length < 10) {
    const block = match[1];
    const title  = (block.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/) ||
                    block.match(/<title>(.*?)<\/title>/))?.[1] || '';
    const link   = (block.match(/<link>(.*?)<\/link>/))?.[1] ||
                   (block.match(/<guid[^>]*>(.*?)<\/guid>/))?.[1] || '#';
    const pubDate = (block.match(/<pubDate>(.*?)<\/pubDate>/))?.[1] || '';
    const source  = (block.match(/<source[^>]*>(.*?)<\/source>/))?.[1] || 'News';

    const age = pubDate ? relativeTime(new Date(pubDate)) : '';
    if (title) items.push({ title: title.trim(), url: link.trim(), source, age });
  }
  return items;
}

function relativeTime(date) {
  const diff = (Date.now() - date.getTime()) / 1000 / 60;
  if (diff < 60)  return `${Math.round(diff)}m ago`;
  if (diff < 1440) return `${Math.round(diff / 60)}h ago`;
  return `${Math.round(diff / 1440)}d ago`;
}

async function fetchNews() {
  try {
    const query = NEWS_QUERIES[Math.floor(Math.random() * NEWS_QUERIES.length)];
    const url = `https://news.google.com/rss/search?q=${encodeURIComponent(query)}&hl=en-US&gl=US&ceid=US:en`;
    const r = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; Dashboard/1.0)' },
    });
    if (!r.ok) return [];
    const xml = await r.text();
    return parseRSS(xml).slice(0, 6);
  } catch (e) {
    console.error('News error:', e.message);
    return [];
  }
}

// ── Monarch Money (Mac-push model — data synced from user's machine, cached in GitHub) ──
async function fetchMonarch() {
  if (!GITHUB_TOKEN) return null;
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${MONARCH_DATA_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return null;
    const meta = await res.json();
    return JSON.parse(Buffer.from(meta.content, 'base64').toString('utf8'));
  } catch (e) {
    console.error('Monarch cache read error:', e.message);
    return null;
  }
}

async function saveMonarchToGitHub(data) {
  if (!GITHUB_TOKEN) return;
  try {
    const content = Buffer.from(JSON.stringify(data, null, 2)).toString('base64');
    const getRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${MONARCH_DATA_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    const body = { message: 'Update monarch data', content };
    if (getRes.ok) { const cur = await getRes.json(); body.sha = cur.sha; }
    await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${MONARCH_DATA_FILE}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (e) { console.error('Monarch GitHub save error:', e.message); }
}

// Receives pushed data from the Mac sync script
app.post('/api/monarch-push', async (req, res) => {
  const secret = req.headers['x-push-secret'];
  if (MONARCH_PUSH_SECRET && secret !== MONARCH_PUSH_SECRET) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  try {
    const data = { ...req.body, synced_at: new Date().toISOString() };
    await saveMonarchToGitHub(data);
    res.json({ ok: true, synced_at: data.synced_at });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/monarch', async (req, res) => {
  const data = await fetchMonarch();
  if (!data) return res.status(503).json({ error: 'No Monarch data yet — run the sync script on your Mac' });
  res.json(data);
});

// ── Todos (stored in GitHub todos.json so they survive Railway deploys) ──
const TODOS_FILE = 'todos.json';
const EMPTY_TODOS = { business: [], health: [], personal: [] };

// Normalize raw todos.json into the lists the dashboard renders. The legacy
// `money` list is folded into `business` so there is one single Money Tasks
// list everywhere. Done on read so it works no matter what writes the file.
function normalizeTodos(raw) {
  const t = raw || {};
  return {
    business: [...(t.business || []), ...(t.money || [])],
    health:   t.health   || [],
    personal: t.personal || [],
  };
}

async function loadTodos() {
  if (!GITHUB_TOKEN) return EMPTY_TODOS;
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${TODOS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return EMPTY_TODOS;
    const data = await res.json();
    return normalizeTodos(JSON.parse(Buffer.from(data.content, 'base64').toString('utf8')));
  } catch (e) {
    console.error('loadTodos error:', e.message);
    return EMPTY_TODOS;
  }
}

async function saveTodosToGitHub(todos) {
  if (!GITHUB_TOKEN) return;
  try {
    const content = Buffer.from(JSON.stringify(todos, null, 2)).toString('base64');
    const getRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${TODOS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    const body = { message: 'Update todos', content };
    if (getRes.ok) { const cur = await getRes.json(); body.sha = cur.sha; }
    await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${TODOS_FILE}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    console.log('Todos saved to GitHub');
  } catch (e) { console.error('GitHub todos save error:', e.message); }
}

// ── Todos CRUD endpoints ──
app.get('/api/todos', async (req, res) => {
  res.json(await loadTodos());
});

app.post('/api/todos', async (req, res) => {
  try {
    const todos = req.body;
    await saveTodosToGitHub(todos);
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ── Today's Plan (stored in GitHub plan.json so it survives Railway deploys) ──
// Shape: { date: "YYYY-MM-DD", order: [checkId...], excluded: [checkId...] }
//   order    — the arranged sequence of tasks pinned into Today's Plan (key tasks
//              plus lighter tasks the user dragged in).
//   excluded — key-task ids the user dragged OUT today, so they don't auto-return.
// The client rebuilds the plan fresh each new LOCAL day (drag-ins/exclusions clear),
// so no server-side cron is needed — the stored `date` just tells the client which
// day this arrangement belongs to.
const PLAN_FILE = 'plan.json';
const EMPTY_PLAN = { date: null, order: [], excluded: [] };

async function loadPlan() {
  if (!GITHUB_TOKEN) return EMPTY_PLAN;
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${PLAN_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return EMPTY_PLAN;
    const data = await res.json();
    const parsed = JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
    return {
      date:     typeof parsed.date === 'string' ? parsed.date : null,
      order:    Array.isArray(parsed.order) ? parsed.order : [],
      excluded: Array.isArray(parsed.excluded) ? parsed.excluded : [],
    };
  } catch (e) {
    console.error('loadPlan error:', e.message);
    return EMPTY_PLAN;
  }
}

async function savePlanToGitHub(plan) {
  if (!GITHUB_TOKEN) return;
  try {
    const content = Buffer.from(JSON.stringify(plan, null, 2)).toString('base64');
    const getRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${PLAN_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    const body = { message: 'Update today\'s plan', content };
    if (getRes.ok) { const cur = await getRes.json(); body.sha = cur.sha; }
    await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${PLAN_FILE}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    console.log('Plan saved to GitHub');
  } catch (e) { console.error('GitHub plan save error:', e.message); }
}

app.get('/api/plan', async (req, res) => {
  res.json(await loadPlan());
});

app.post('/api/plan', async (req, res) => {
  try {
    const { date, order, excluded } = req.body || {};
    await savePlanToGitHub({
      date:     typeof date === 'string' ? date : null,
      order:    Array.isArray(order) ? order : [],
      excluded: Array.isArray(excluded) ? excluded : [],
    });
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// ── AI priority triage (for the dashboard's "Claude's choice" quick-add) ──
app.post('/api/assign-priority', aiLimiter, async (req, res) => {
  try {
    const { text, list } = req.body || {};
    if (!text || typeof text !== 'string') return res.status(400).json({ error: 'Missing text', priority: 'med' });
    if (!ANTHROPIC_API_KEY) return res.json({ priority: 'med' });

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 8,
        messages: [{
          role: 'user',
          content: `You triage to-do items for a personal productivity dashboard. The task belongs to the "${list || 'general'}" category. Based on urgency and impact, assign a priority. Task: "${text.slice(0, 300)}". Reply with exactly one word: high, med, or low.`,
        }],
      }),
    });

    const data = await response.json();
    if (!response.ok) return res.status(response.status).json({ error: data?.error?.message || 'Claude API error', priority: 'med' });

    const raw = (data?.content?.[0]?.text || '').trim().toLowerCase();
    const priority = ['high', 'med', 'low'].find(p => raw.includes(p)) || 'med';
    res.json({ priority });
  } catch (e) {
    res.status(500).json({ error: e.message, priority: 'med' });
  }
});


// ── Task checks (which todos are checked off — synced across devices via GitHub) ──
// Checked state is keyed by a stable, content-based id (list + task text) so it
// survives reordering, re-prioritizing, and re-rendering. Writes are applied as
// deltas with read-modify-write + retry, so two devices toggling different tasks
// at once don't clobber each other.
//
// Data shape: { checked: [id...], log: { id: [yyyy-mm-dd...] } }
//   checked — sticky one-off tasks; stay checked until explicitly unchecked.
//   log     — completion dates for recurring (daily) tasks. "Done today" and the
//             streak are derived client-side from this log using the client's
//             LOCAL date, so daily reset + streaks are timezone-correct without
//             any server-side cron.
const TASK_CHECKS_FILE = 'task-checks.json';

async function loadTaskChecks() {
  const empty = { checked: [], log: {}, sha: null };
  if (!GITHUB_TOKEN) return empty;
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${TASK_CHECKS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return empty;
    const data = await res.json();
    const parsed = JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
    return {
      checked: Array.isArray(parsed.checked) ? parsed.checked : [],
      log: (parsed.log && typeof parsed.log === 'object') ? parsed.log : {},
      sha: data.sha,
    };
  } catch (e) {
    console.error('loadTaskChecks error:', e.message);
    return empty;
  }
}

async function putTaskChecks(checked, log, sha) {
  const content = Buffer.from(JSON.stringify({ checked, log }, null, 2)).toString('base64');
  const body = { message: 'Update task checks', content };
  if (sha) body.sha = sha;
  return fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${TASK_CHECKS_FILE}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

app.get('/api/task-checks', async (req, res) => {
  const { checked, log } = await loadTaskChecks();
  res.json({ checked, log });
});

// Lightweight combined endpoint for cross-device auto-sync (tasks + their state),
// without the heavy external fetches in /api/morning-data.
app.get('/api/tasks-state', async (req, res) => {
  const [todos, checks, plan] = await Promise.all([loadTodos(), loadTaskChecks(), loadPlan()]);
  res.json({ todos, task_checks: { checked: checks.checked, log: checks.log }, plan });
});

app.post('/api/task-checks', async (req, res) => {
  if (!GITHUB_TOKEN) return res.status(503).json({ error: 'storage not configured' });
  const { id, checked, recurring, date } = req.body || {};
  if (typeof id !== 'string' || typeof checked !== 'boolean') {
    return res.status(400).json({ error: 'expected { id: string, checked: boolean }' });
  }
  if (recurring && (typeof date !== 'string' || !DATE_RE.test(date))) {
    return res.status(400).json({ error: 'recurring toggle requires { date: "YYYY-MM-DD" }' });
  }
  try {
    for (let attempt = 0; attempt < 4; attempt++) {
      const cur = await loadTaskChecks();
      const set = new Set(cur.checked);
      const log = { ...cur.log };
      if (recurring) {
        const dates = new Set(log[id] || []);
        if (checked) dates.add(date); else dates.delete(date);
        if (dates.size) log[id] = [...dates].sort(); else delete log[id];
      } else {
        if (checked) set.add(id); else set.delete(id);
      }
      const nextChecked = [...set];
      const putRes = await putTaskChecks(nextChecked, log, cur.sha);
      if (putRes.ok) return res.json({ ok: true, checked: nextChecked, log });
      if (putRes.status === 409 || putRes.status === 422) continue; // sha race — reload & retry
      const txt = await putRes.text().catch(() => '');
      return res.status(502).json({ error: `github ${putRes.status}: ${txt}` });
    }
    return res.status(503).json({ error: 'write conflict, please retry' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});


// ââ Apple Watch data â stored in GitHub so it survives Railway deploys ââ
// ── Web Push (morning notification) ──
// VAPID keys live in env (VAPID_PUBLIC_KEY / VAPID_PRIVATE_KEY). Subscriptions
// are stored in GitHub (push-subs.json) so they survive deploys. The morning
// summary is sent by POSTing /api/send-push (triggered from the Mac 7am job).
const VAPID_PUBLIC_KEY  = process.env.VAPID_PUBLIC_KEY;
const VAPID_PRIVATE_KEY = process.env.VAPID_PRIVATE_KEY;
const VAPID_SUBJECT     = process.env.VAPID_SUBJECT || 'mailto:danroseconsulting@gmail.com';
const PUSH_SUBS_FILE    = 'push-subs.json';

let webpush = null;
function getWebPush() {
  if (!VAPID_PUBLIC_KEY || !VAPID_PRIVATE_KEY) return null;
  if (!webpush) {
    try {
      webpush = require('web-push');
      webpush.setVapidDetails(VAPID_SUBJECT, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY);
    } catch (e) { console.error('web-push init error:', e.message); return null; }
  }
  return webpush;
}

async function loadPushSubs() {
  if (!GITHUB_TOKEN) return { subs: [], sha: null };
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${PUSH_SUBS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return { subs: [], sha: null };
    const data = await res.json();
    const parsed = JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
    return { subs: Array.isArray(parsed.subs) ? parsed.subs : [], sha: data.sha };
  } catch (e) {
    console.error('loadPushSubs error:', e.message);
    return { subs: [], sha: null };
  }
}

async function savePushSubs(subs, sha) {
  const content = Buffer.from(JSON.stringify({ subs }, null, 2)).toString('base64');
  const body = { message: 'Update push subscriptions', content };
  if (sha) body.sha = sha;
  return fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${PUSH_SUBS_FILE}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}

app.get('/api/push/public-key', (req, res) => {
  res.json({ key: VAPID_PUBLIC_KEY || null });
});

// Accepts either a raw PushSubscription (legacy dashboard) or
// { subscription, tzOffset, prefs } — tzOffset is minutes east of UTC
// (client sends -new Date().getTimezoneOffset()), prefs are per-user reminder
// opt-ins { weigh, photo, mealPrep, workout }. A logged-in caller gets its
// userId attached so the reminder sweep can look up their data.
app.post('/api/push/subscribe', (req, res, next) => optionalAuth(req, res, next), async (req, res) => {
  if (!GITHUB_TOKEN) return res.status(503).json({ error: 'storage not configured' });
  const raw = req.body || {};
  const sub = raw.subscription || raw;
  if (!sub || !sub.endpoint) return res.status(400).json({ error: 'invalid subscription' });
  if (raw.subscription) {
    sub.meta = {
      userId: req.user?.id || null,
      tzOffset: Number.isFinite(Number(raw.tzOffset)) ? Number(raw.tzOffset) : 0,
      prefs: typeof raw.prefs === 'object' && raw.prefs ? raw.prefs : {},
    };
  }
  try {
    for (let attempt = 0; attempt < 4; attempt++) {
      const cur = await loadPushSubs();
      const subs = cur.subs.filter(s => s.endpoint !== sub.endpoint); // dedupe by endpoint
      subs.push(sub);
      const putRes = await savePushSubs(subs, cur.sha);
      if (putRes.ok) return res.json({ ok: true, count: subs.length });
      if (putRes.status === 409 || putRes.status === 422) continue;
      return res.status(502).json({ error: `github ${putRes.status}` });
    }
    return res.status(503).json({ error: 'write conflict, please retry' });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

app.post('/api/push/unsubscribe', async (req, res) => {
  if (!GITHUB_TOKEN) return res.status(503).json({ error: 'storage not configured' });
  const { endpoint } = req.body || {};
  if (!endpoint) return res.status(400).json({ error: 'endpoint required' });
  try {
    for (let attempt = 0; attempt < 4; attempt++) {
      const cur = await loadPushSubs();
      const subs = cur.subs.filter(s => s.endpoint !== endpoint);
      const putRes = await savePushSubs(subs, cur.sha);
      if (putRes.ok) return res.json({ ok: true, count: subs.length });
      if (putRes.status === 409 || putRes.status === 422) continue;
      return res.status(502).json({ error: `github ${putRes.status}` });
    }
    return res.status(503).json({ error: 'write conflict, please retry' });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// Compose the morning summary from current data.
async function buildMorningSummary() {
  const [todos, checks, monarch, oura] = await Promise.all([
    loadTodos(), loadTaskChecks(), fetchMonarch().catch(() => null), fetchOura().catch(() => null),
  ]);
  const today = new Date().toISOString().split('T')[0];
  const checkedSet = new Set(checks.checked);
  const log = checks.log || {};
  const allTasks = [...(todos.business || []), ...(todos.health || []), ...(todos.personal || [])];
  let remaining = 0;
  for (const t of allTasks) {
    const doneToday =
      [...checkedSet].some(id => id.endsWith(`::${t.text}`)) ||
      Object.entries(log).some(([id, dates]) => id.endsWith(`::${t.text}`) && dates.includes(today));
    if (!doneToday) remaining++;
  }
  const bits = [`${remaining} task${remaining === 1 ? '' : 's'} to win today`];
  if (oura?.score != null) bits.push(`Sleep ${oura.score}`);
  if (monarch?.net_worth != null) {
    const nw = monarch.net_worth;
    const s = nw >= 1e6 ? `$${(nw / 1e6).toFixed(2)}M` : `$${Math.round(nw / 1000)}k`;
    bits.push(`Net worth ${s}`);
  }
  return { title: 'Victory Dashboard', body: bits.join(' · ') };
}

app.post('/api/send-push', async (req, res) => {
  const secret = req.headers['x-push-secret'];
  if (MONARCH_PUSH_SECRET && secret !== MONARCH_PUSH_SECRET) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  const wp = getWebPush();
  if (!wp) return res.status(503).json({ error: 'push not configured (set VAPID_PUBLIC_KEY / VAPID_PRIVATE_KEY)' });
  try {
    const { subs, sha } = await loadPushSubs();
    if (!subs.length) return res.json({ ok: true, sent: 0, note: 'no subscriptions' });
    const summary = req.body && req.body.title ? req.body : await buildMorningSummary();
    const payload = JSON.stringify({ ...summary, url: '/dashboard' });

    const stale = [];
    let sent = 0;
    await Promise.all(subs.map(async (s) => {
      try { await wp.sendNotification(s, payload); sent++; }
      catch (e) { if (e.statusCode === 404 || e.statusCode === 410) stale.push(s.endpoint); }
    }));
    if (stale.length) {
      const keep = subs.filter(s => !stale.includes(s.endpoint));
      await savePushSubs(keep, sha).catch(() => {});
    }
    res.json({ ok: true, sent, removed_stale: stale.length });
  } catch (e) { res.status(500).json({ error: e.message }); }
});

// ── Per-user reminder sweep ──
// Every 15 minutes, find subscriptions whose LOCAL time just entered the
// 8:00-8:59 AM window and send at most one reminder each, by priority:
// photo day > missed-photo follow-up > weigh-in > Sunday meal prep > workout
// day. In-memory dedupe per endpoint/kind/local-date (a restart can at worst
// re-send once — acceptable).
const REMINDER_WINDOW_START = 8; // 8 AM local
const sentReminders = new Set();

function localNow(tzOffset) {
  return new Date(Date.now() + (tzOffset || 0) * 60000); // read via getUTC* below
}

async function pickReminder(userId, local) {
  const localDate = local.toISOString().slice(0, 10);
  const day = local.getUTCDay();
  const { rows: u } = await db.query(
    'SELECT photo_day, weigh_reminder, last_photo_nudge FROM users WHERE id = $1', [userId]
  );
  if (!u.length) return null;
  const user = u[0];

  const hasToday = async (table) => {
    const { rows } = await db.query(
      `SELECT 1 FROM ${table} WHERE user_id = $1 AND entry_date = $2 LIMIT 1`, [userId, localDate]
    );
    return rows.length > 0;
  };

  if (user.photo_day === day && !(await hasToday('progress_entries'))) {
    return { kind: 'photo', title: '📸 It\'s photo day', body: 'Same spot, same lighting, same pose. 2 minutes.', url: '/#progress' };
  }
  // Missed photo day: ONE follow-up the day after, then stop.
  const yesterday = new Date(local); yesterday.setUTCDate(yesterday.getUTCDate() - 1);
  if (user.photo_day != null && user.photo_day === yesterday.getUTCDay() &&
      (!user.last_photo_nudge || dateStr(user.last_photo_nudge) < localDate)) {
    const { rows } = await db.query(
      'SELECT 1 FROM progress_entries WHERE user_id = $1 AND entry_date >= $2 LIMIT 1',
      [userId, yesterday.toISOString().slice(0, 10)]
    );
    if (!rows.length) {
      await db.query('UPDATE users SET last_photo_nudge = $1 WHERE id = $2', [localDate, userId]);
      return { kind: 'photo-followup', title: '📸 Yesterday was photo day', body: '2 minutes, same spot, same lighting — your future self will thank you.', url: '/#progress' };
    }
  }
  if (user.weigh_reminder && !(await hasToday('weight_logs'))) {
    return { kind: 'weigh', title: '⚖️ Morning weigh-in', body: 'Step on, log it, done. The trend does the thinking.', url: '/#progress' };
  }
  return null;
}

async function reminderSweep() {
  if (!db || !getWebPush() || !GITHUB_TOKEN) return;
  try {
    const { subs, sha } = await loadPushSubs();
    const wp = getWebPush();
    const stale = [];
    for (const s of subs) {
      const meta = s.meta;
      if (!meta || !meta.userId) continue; // legacy dashboard subs: morning summary only
      const local = localNow(meta.tzOffset);
      if (local.getUTCHours() !== REMINDER_WINDOW_START) continue;
      const localDate = local.toISOString().slice(0, 10);
      try {
        let reminder = await pickReminder(meta.userId, local);
        // Feature nudges (opt-in): Sunday meal prep, Mon/Wed/Fri workout.
        if (!reminder && meta.prefs?.mealPrep && local.getUTCDay() === 0) {
          const { rows } = await db.query('SELECT 1 FROM meal_plans WHERE user_id = $1 LIMIT 1', [meta.userId]);
          if (rows.length) reminder = { kind: 'mealprep', title: '🍱 Meal prep Sunday', body: 'One hour today buys a week of easy wins. Your plan has the grocery list.', url: '/#nutrition' };
        }
        if (!reminder && meta.prefs?.workout && [1, 3, 5].includes(local.getUTCDay())) {
          const { rows } = await db.query('SELECT 1 FROM programs WHERE user_id = $1 LIMIT 1', [meta.userId]);
          if (rows.length) reminder = { kind: 'workout', title: '🏋️ Training day', body: 'Your program is waiting. Go hard.', url: '/#trainer' };
        }
        if (!reminder) continue;
        const dedupeKey = `${s.endpoint}:${reminder.kind}:${localDate}`;
        if (sentReminders.has(dedupeKey)) continue;
        sentReminders.add(dedupeKey);
        await wp.sendNotification(s, JSON.stringify({ title: reminder.title, body: reminder.body, url: reminder.url }));
      } catch (e) {
        if (e.statusCode === 404 || e.statusCode === 410) stale.push(s.endpoint);
        else console.warn('reminder send error:', e.message);
      }
    }
    if (stale.length) {
      const keep = subs.filter((s) => !stale.includes(s.endpoint));
      await savePushSubs(keep, sha).catch(() => {});
    }
    // Keep the dedupe set from growing unbounded.
    if (sentReminders.size > 5000) sentReminders.clear();
  } catch (e) { console.warn('reminderSweep error:', e.message); }
}
setInterval(reminderSweep, 15 * 60 * 1000);

let latestWatchData = null;
let lastRawMetricNames = null; // parsed watch metrics, loaded from GitHub on startup

async function saveWatchToGitHub(parsed) {
  if (!GITHUB_TOKEN || !parsed) return;
  try {
    const content = Buffer.from(JSON.stringify(parsed)).toString('base64');
    // Get current SHA if file exists
    const getRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${WATCH_DATA_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    const body = { message: 'Update watch data', content };
    if (getRes.ok) { const cur = await getRes.json(); body.sha = cur.sha; }
    await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${WATCH_DATA_FILE}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    console.log('Watch data saved to GitHub');
  } catch (e) { console.error('GitHub watch save error:', e.message); }
}

async function loadWatchFromGitHub() {
  if (!GITHUB_TOKEN) return null;
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${WATCH_DATA_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return null;
    const data = await res.json();
    return JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
  } catch (e) { return null; }
}

// Load cached watch data from GitHub on startup
loadWatchFromGitHub().then(d => { if (d) { latestWatchData = d; console.log('Watch data loaded from GitHub:', d); } });

function parseHealthData(raw) {
  // Health Auto Export sends: { data: { metrics: [...], workouts: [...] } }
  // or top-level: { metrics: [...], workouts: [...] }
  const payload = raw?.data || raw || {};
  const metrics = payload.metrics || [];
  const workouts = payload.workouts || [];
  lastRawMetricNames = metrics.map(m => m.name);

  const today = new Date().toISOString().split('T')[0];

  // Sum qty values for a metric (today's data, or last available)
  function getMetric(name) {
    const m = metrics.find(x => x.name === name);
    if (!m || !m.data || !m.data.length) return null;
    const todayRows = m.data.filter(d => (d.date || '').startsWith(today));
    const rows = todayRows.length ? todayRows : m.data.slice(-1);
    return rows.reduce((sum, d) => sum + (d.qty || 0), 0);
  }

  // Average the Avg field for metrics like heart_rate
  function getMetricAvg(name) {
    const m = metrics.find(x => x.name === name);
    if (!m || !m.data || !m.data.length) return null;
    const todayRows = m.data.filter(d => (d.date || '').startsWith(today));
    const rows = todayRows.length ? todayRows : m.data.slice(-1);
    const vals = rows.map(d => d.Avg || d.qty || 0).filter(v => v > 0);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
  }

  const move_cal    = getMetric('active_energy')           || null;
  const exercise    = getMetric('apple_exercise_time') || getMetric('exercise_time') || getMetric('Apple Exercise Time') || getMetricAvg('apple_exercise_time') || null;
  const stand       = getMetric('apple_stand_hour')         || null;
  const steps       = getMetric('step_count')               || null;
  // Use walking HR average as resting HR proxy (closest available without explicit metric)
  const resting_hr  = getMetric('resting_heart_rate')
                   || getMetricAvg('walking_heart_rate_average')
                   || getMetricAvg('heart_rate')
                   || null;

  const workout_min = workouts.reduce((sum, w) => sum + Math.round((w.duration || 0)), 0) || null;

  if (!move_cal && !steps && !stand) return null; // no usable data

  return {
    move_cal:    move_cal    ? Math.round(move_cal)    : null,
    move_goal:   600,
    exercise_min:exercise    ? Math.round(exercise)    : null,
    stand_hrs:   stand       ? Math.round(stand)       : null,
    steps:       steps       ? Math.round(steps)       : null,
    resting_hr:  resting_hr  ? Math.round(resting_hr)  : null,
    workout_min: workout_min || null,
  };
}

function loadWatch() {
  return latestWatchData || null;
}

// ââ Apple Watch webhook (Health Auto Export pushes here) ââ
app.post('/api/health-data', (req, res) => {
  try {
    const secret = req.headers['x-webhook-secret'];
    if (process.env.HEALTH_WEBHOOK_SECRET && secret !== process.env.HEALTH_WEBHOOK_SECRET) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    const parsed = parseHealthData(req.body);
    if (parsed) {
      latestWatchData = parsed;
      saveWatchToGitHub(parsed); // async, don't block response
    }
    res.json({ ok: true, parsed: !!parsed });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Debug: inspect watch data state
app.get('/api/health-debug', (req, res) => {
  res.json({ watch: latestWatchData, github_token_set: !!GITHUB_TOKEN, metric_names: lastRawMetricNames });
});

// ============================================================
// HEALTH CHECK
// ============================================================
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// ============================================================
// ENDPOINT 1: Photo check (Claude Haiku)
// ============================================================
app.post('/api/check-photo', aiLimiter, async (req, res) => {
  try {
    const { photoBase64, photoMime } = req.body;

    if (!photoBase64 || !photoMime) {
      return res.status(400).json({ error: 'Missing photoBase64 or photoMime' });
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 16,
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'image',
                source: {
                  type: 'base64',
                  media_type: photoMime,
                  data: photoBase64,
                },
              },
              {
                type: 'text',
                text: `Review this photo for a fitness transformation app and reply with exactly one of these codes:

OK â the person is shirtless, or wearing a sports bra, bikini, swimsuit, swimwear, athletic wear, or underwear-style clothing that clearly exposes their bare midsection/torso. This includes beach photos, pool photos, gym photos, and mirror selfies. Even glamorous or professional-looking photos are OK as long as the clothing is standard swimwear or athletic wear and the pose is not explicitly sexual.

SUGGESTIVE â the photo is clearly sexually provocative: lingerie specifically intended to be erotic (not athletic/swimwear), explicitly sexual posing (spread legs, simulated sex acts), or nudity beyond what would be seen at a beach or gym.

CLOTHED â the person is fully or mostly clothed and their torso is not clearly visible.

EXPLICIT â the image contains pornographic or sexually explicit content.

ILLEGAL â the image shows visible illegal activity such as drug use, weapons, or similar.

MINOR â the subject appears to be under 18 years old.

When in doubt between OK and SUGGESTIVE, choose OK. Only flag SUGGESTIVE if the photo is clearly inappropriate for a fitness context.

Reply with the single code word, then a space, then the subject's apparent sex: MALE, FEMALE, or UNKNOWN if unclear. Example replies: "OK FEMALE", "CLOTHED MALE", "OK UNKNOWN". Nothing else.`,
              },
            ],
          },
        ],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error?.message || 'Claude API error',
      });
    }

    const raw = data?.content?.[0]?.text?.trim().toUpperCase() || 'OK';
    const [code, sexWord] = raw.split(/\s+/);
    const sex = sexWord === 'MALE' ? 'male' : sexWord === 'FEMALE' ? 'female' : null;
    res.json({ code: code || 'OK', sex });
  } catch (err) {
    console.error('Photo check error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// ENDPOINT 2: Generate prompt (Claude Sonnet)
// ============================================================
app.post('/api/generate-prompt', aiLimiter, async (req, res) => {
  try {
    const { systemPrompt, userJson } = req.body;

    if (!systemPrompt || !userJson) {
      return res.status(400).json({ error: 'Missing systemPrompt or userJson' });
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        // Haiku 4.5 instead of Sonnet 4.6 for the prompt-assembly step: this is
        // templated structured-text generation (Haiku's wheelhouse), and it
        // responds ~2x faster, shaving several seconds off every generation.
        // max_tokens trimmed 2048→1024 (the prompt never approaches 2048).
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1024,
        temperature: 0.4,
        system: systemPrompt,
        messages: [
          {
            role: 'user',
            content: userJson,
          },
        ],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error?.message || 'Claude API error',
      });
    }

    const prompt = data?.content
      ?.filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('\n')
      .trim();

    if (!prompt) {
      return res.status(400).json({
        error: 'Claude returned no text. The prompt may have been blocked by safety filters.',
      });
    }

    res.json({ prompt });
  } catch (err) {
    console.error('Prompt generation error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// MACRO TRACKER: Analyze meal photo (Claude Sonnet)
// ============================================================
// Pipeline: Sonnet itemizes the meal via a strict JSON schema → code enforces
// 4/4/9 macro math per item → a calibration multiplier counters the documented
// systematic underestimation (applied to grams so the itemized card still sums)
// → totals are computed here, never trusted from the model.

// Calibration multipliers by meal context. Starting values are conservative;
// tune them with the eval harness (measured bias per category), not by feel.
// Label reads are near-exact, so they are never inflated.
const MEAL_CALIBRATION = {
  label: 1.0,        // read off a nutrition label
  packaged: 1.0,     // recognizable packaged product
  home: 1.05,        // home-cooked
  restaurant: 1.15,  // restaurant/takeout — hidden oils, larger portions
  unknown: 1.1,
  lowConfidenceFloor: 1.15, // any meal the model itself isn't confident about
};

// Strict schema for the meal analysis (structured outputs — guaranteed parseable).
const MEAL_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['is_food', 'meal_name', 'source', 'context', 'confidence', 'items', 'clarifying_questions', 'matches_recent'],
  properties: {
    is_food: { type: 'boolean', description: 'False if the photo does not show food or drink.' },
    meal_name: { type: 'string', description: 'Short human name for this meal, e.g. "Chicken burrito bowl".' },
    source: { type: 'string', enum: ['estimated', 'label', 'menu'], description: 'label = numbers read directly off a nutrition label in the photo.' },
    context: { type: 'string', enum: ['home', 'restaurant', 'packaged', 'unknown'] },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    items: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'estimated_grams', 'calories', 'protein_g', 'carbs_g', 'fat_g', 'alcohol_g', 'confidence', 'assumptions'],
        properties: {
          name: { type: 'string' },
          estimated_grams: { type: 'number' },
          calories: { type: 'number' },
          protein_g: { type: 'number' },
          carbs_g: { type: 'number' },
          fat_g: { type: 'number' },
          alcohol_g: { type: 'number', description: 'Grams of pure ethanol in the portion (0 for non-alcoholic items). Beer ~4g/100ml, wine ~10g/100ml, spirits ~33g/100ml.' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
          assumptions: { type: 'array', items: { type: 'string' } },
        },
      },
    },
    clarifying_questions: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['question', 'options'],
        properties: {
          question: { type: 'string' },
          options: { type: 'array', items: { type: 'string' } },
        },
      },
    },
    matches_recent: {
      type: ['string', 'null'],
      description: 'If the photo clearly matches one of the user\'s recent meals (provided in the prompt), its exact name; otherwise null.',
    },
  },
};

const MEAL_SYSTEM_PROMPT = `You are the meal-analysis engine for a fitness app. Given one or more photos of food, itemize everything edible and estimate nutrition per item.

Rules:
- If more than one photo is provided, they are the SAME meal from different angles (e.g. an overhead shot and a side shot) — itemize the meal ONCE, not once per photo. Use overhead angles to see what's on the plate and side/angled shots to judge height and depth for volume.
- Estimate each item's volume or weight FIRST using visual references, then convert to macros via standard food densities — don't jump straight to a calorie guess. Use the plate as a ruler: a standard dinner plate is about 10.5in/27cm across, a dinner fork is about 7in/18cm long.
- One entry per distinct food item. Include cooking fats, oils, dressings, and sauces as their own line items when they are plausibly present, even if not directly visible (e.g. "cooking oil" for pan-fried food, "dressing" for a glossy salad).
- estimated_grams is the edible portion as served. Do not default to "standard serving" sizes when the photo shows more or less.
- calories, protein_g, carbs_g, fat_g are for the estimated portion, not per 100g. Keep calories consistent with energy math: 4 kcal/g protein and carbs, 9 kcal/g fat, 7 kcal/g alcohol.
- For alcoholic drinks, set alcohol_g to the grams of pure ethanol in the portion — most of their calories come from alcohol, not macros. Set alcohol_g to 0 for everything else.
- If a photo shows a nutrition label, read it verbatim and set source to "label" with a single item.
- List every assumption that materially moves the numbers (e.g. "assumed whole milk", "assumed cooked in 1 tbsp oil").
- clarifying_questions: at most 2, only questions whose answer would change calories by >10%. Each needs 2-4 short tap-friendly options, most likely option first. If confidence is high, return an empty array.
- If none of the photos contain food or drink, set is_food to false and return an empty items array.`;

// Appended to the system prompt only when the request is flagged mealPrep —
// tells the model these photos are a whole batch to divide later, not a plate.
const MEAL_PREP_ADDENDUM = `

These photos show an ENTIRE WEEK'S MEAL-PREP BATCH, not a single plated portion — raw ingredients and/or packaged items meant to be divided into several servings. Itemize and estimate nutrition for the WHOLE BATCH shown (everything combined across all photos/containers), and read any visible nutrition labels verbatim rather than guessing. The batch will be divided into per-serving numbers after your response, so estimate the full batch quantities as photographed.`;

// Accepts either the new multi-photo shape { photos: [{ base64, mime }] } or
// the legacy single-photo shape { photoBase64, photoMime } (deployed iOS/
// Android wrappers call prod with the legacy shape — never remove it).
function normalizeMealPhotos(body) {
  if (Array.isArray(body.photos) && body.photos.length) {
    return body.photos.slice(0, 3).map((p) => ({ data: p.base64 || p.data, mime: p.mime }));
  }
  if (body.photoBase64 && body.photoMime) {
    return [{ data: body.photoBase64, mime: body.photoMime }];
  }
  return [];
}

// One text label + image block per photo, in the order taken.
function buildMealPhotoContent(photos) {
  const content = [];
  photos.forEach((p, i) => {
    if (photos.length > 1) content.push({ type: 'text', text: `Photo ${i + 1}:` });
    content.push({ type: 'image', source: { type: 'base64', media_type: p.mime, data: p.data } });
  });
  return content;
}

// Scale every item's grams/macros/calories by 1/n (meal-prep batch -> per serving).
function divideItems(items, n) {
  return items.map((item) => ({
    ...item,
    estimated_grams: Math.round(item.estimated_grams / n),
    calories: Math.round(item.calories / n),
    protein_g: Math.round((item.protein_g / n) * 10) / 10,
    carbs_g: Math.round((item.carbs_g / n) * 10) / 10,
    fat_g: Math.round((item.fat_g / n) * 10) / 10,
    alcohol_g: Math.round(((item.alcohol_g || 0) / n) * 10) / 10,
  }));
}

// Enforce calories = 4p + 4c + 9f + 7a per item (a = alcohol grams). If the
// model's calorie figure disagrees with its own macros by >15%, the macros win
// (they're the more constrained estimate) and calories are recomputed here.
function enforceMacroMath(items) {
  return items.map((item) => {
    const alcohol = item.alcohol_g || 0;
    const computed = 4 * item.protein_g + 4 * item.carbs_g + 9 * item.fat_g + 7 * alcohol;
    const stated = item.calories;
    // Zero macros + zero alcohol gives the formula nothing to stand on (water,
    // black coffee — or an item whose energy source the schema doesn't model).
    // Keep the model's figure rather than "correcting" real calories to zero.
    if (computed === 0) {
      return { ...item, alcohol_g: alcohol, calories: Math.round(stated), macro_corrected: false };
    }
    const drift = Math.abs(computed - stated) / Math.max(stated, 1);
    if (drift > 0.15) {
      return { ...item, alcohol_g: alcohol, calories: Math.round(computed), macro_corrected: true };
    }
    return { ...item, alcohol_g: alcohol, calories: Math.round(stated), macro_corrected: false };
  });
}

// Scale grams + macros + calories together so the itemized card stays self-consistent.
function applyCalibration(items, factor) {
  if (factor === 1.0) return items;
  return items.map((item) => ({
    ...item,
    estimated_grams: Math.round(item.estimated_grams * factor),
    calories: Math.round(item.calories * factor),
    protein_g: Math.round(item.protein_g * factor * 10) / 10,
    carbs_g: Math.round(item.carbs_g * factor * 10) / 10,
    fat_g: Math.round(item.fat_g * factor * 10) / 10,
    alcohol_g: Math.round((item.alcohol_g || 0) * factor * 10) / 10,
  }));
}

function sumTotals(items) {
  const r = (n) => Math.round(n * 10) / 10;
  return {
    calories: Math.round(items.reduce((s, i) => s + i.calories, 0)),
    protein_g: r(items.reduce((s, i) => s + i.protein_g, 0)),
    carbs_g: r(items.reduce((s, i) => s + i.carbs_g, 0)),
    fat_g: r(items.reduce((s, i) => s + i.fat_g, 0)),
  };
}

function calibrationFactorFor(analysis) {
  if (analysis.source === 'label') return 1.0;
  const base = MEAL_CALIBRATION[analysis.context] ?? MEAL_CALIBRATION.unknown;
  if (analysis.confidence === 'low') return Math.max(base, MEAL_CALIBRATION.lowConfidenceFloor);
  return base;
}

app.post('/api/analyze-meal', aiLimiter, (req, res, next) => optionalAuth(req, res, next), async (req, res) => {
  try {
    const { note, recentMeals, deviceId, mealPrep, servings } = req.body;

    // Idempotency: a dropped response makes the client replay the same attemptId.
    // Return the cached result (no second model call, no second decrement).
    const attemptId = String(req.body.attemptId || '');
    const cached = getCachedAttempt(attemptId);
    if (cached) return res.status(cached.status).json(cached.body);

    if (Array.isArray(req.body.photos) && req.body.photos.length > 3) {
      return res.status(400).json({ error: 'Maximum 3 photos per analysis' });
    }
    const photos = normalizeMealPhotos(req.body);
    if (!photos.length) {
      return res.status(400).json({ error: 'Missing photoBase64/photoMime or photos' });
    }

    const isMealPrep = !!mealPrep;
    const rawServings = parseInt(servings, 10);
    const servingsCount = isMealPrep ? (rawServings >= 2 && rawServings <= 20 ? rawServings : 0) : null;
    if (isMealPrep && !servingsCount) {
      return res.status(400).json({ error: 'Meal prep requires servings between 2 and 20' });
    }

    // Freemium taste: non-members get FREE_MEAL_ANALYSES total, then each
    // analysis consumes a credit (same balance as image generations). Members
    // unlimited. Refine stays free — it's cheap and resolves ambiguity we caused.
    const isMember = isActiveMembership(req.user);
    const dev = String(deviceId || req.user?.device_id || '');
    let useCredit = false;
    if (!isMember && dev) {
      const used = creditsStore.mealCounts?.[dev] || 0;
      if (used >= FREE_MEAL_ANALYSES) {
        if (getCredits(dev) > 0) {
          useCredit = true; // consumed below only on a successful food read
        } else {
          const payload = {
            error: 'You\'ve used your free meal analyses. Buy credits or become a member for unlimited tracking.',
            needsMembership: true,
            needsCredits: true,
          };
          cacheAttempt(attemptId, 402, payload);
          return res.status(402).json(payload);
        }
      }
    }

    const userContent = buildMealPhotoContent(photos);

    let textParts = [isMealPrep ? 'Analyze this meal-prep batch.' : 'Analyze this meal.'];
    if (note && typeof note === 'string') {
      textParts.push(`User note about the meal: "${note.slice(0, 300)}"`);
    }
    if (Array.isArray(recentMeals) && recentMeals.length) {
      const names = recentMeals.slice(0, 15).map((m) => String(m).slice(0, 80));
      textParts.push(`The user's recently logged meals: ${names.join('; ')}. If this photo clearly shows one of these exact meals again, set matches_recent to its name.`);
    }
    userContent.push({ type: 'text', text: textParts.join('\n') });

    // A stalled connection to Anthropic would otherwise hang this fetch
    // forever (node-fetch has no default timeout) — bound every attempt so
    // the client's error handling can actually kick in. Same pattern as the
    // supplement-audit fix (commit 751fe7b) and /api/refine-leftovers above.
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 240000); // Sonnet, up to 3 images — 4 min
    let response;
    try {
      response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-6',
          max_tokens: 2000,
          system: MEAL_SYSTEM_PROMPT + (isMealPrep ? MEAL_PREP_ADDENDUM : ''),
          output_config: { format: { type: 'json_schema', schema: MEAL_SCHEMA } },
          messages: [{ role: 'user', content: userContent }],
        }),
        signal: controller.signal,
      });
    } finally {
      clearTimeout(timer);
    }

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ error: data?.error?.message || 'Claude API error' });
    }

    let analysis;
    try {
      analysis = JSON.parse(data?.content?.[0]?.text || '');
    } catch {
      return res.status(502).json({ error: 'Model returned unparseable analysis' });
    }

    if (!analysis.is_food) {
      return res.json({ isFood: false });
    }

    const checkedItems = enforceMacroMath(analysis.items);
    const factor = calibrationFactorFor(analysis);
    const adjustedItems = applyCalibration(checkedItems, factor);

    // Charge on successful food reads only: past the free allowance a credit
    // is consumed, otherwise the analysis counts against the free allowance.
    let creditsRemaining;
    if (!isMember && dev) {
      if (useCredit) {
        creditsStore.balances[dev] = getCredits(dev) - 1;
        creditsRemaining = creditsStore.balances[dev];
      } else {
        if (!creditsStore.mealCounts) creditsStore.mealCounts = {};
        creditsStore.mealCounts[dev] = (creditsStore.mealCounts[dev] || 0) + 1;
      }
      persistCreditsStore(); // fire-and-forget
    }

    // Meal prep: the model estimated the WHOLE batch. Divide items/totals down
    // to a single serving so the existing receipt/clarify/refine/log UI can
    // treat it exactly like a regular meal; batchTotals/batchItems carry the
    // whole-batch numbers alongside for display. `raw` stays at serving scale
    // (matching `items`) so /api/refine-meal's math keeps working unmodified.
    const perServingItems = isMealPrep ? divideItems(adjustedItems, servingsCount) : adjustedItems;
    const perServingRawItems = isMealPrep ? divideItems(checkedItems, servingsCount) : checkedItems;

    const payload = {
      isFood: true,
      mealName: analysis.meal_name,
      source: analysis.source,
      context: analysis.context,
      confidence: analysis.confidence,
      matchesRecent: analysis.matches_recent,
      items: perServingItems,
      totals: sumTotals(perServingItems),
      raw: { items: perServingRawItems, totals: sumTotals(perServingRawItems), calibrationFactor: factor },
      clarifyingQuestions: (analysis.clarifying_questions || []).slice(0, 2),
      needsClarification: analysis.confidence !== 'high' && (analysis.clarifying_questions || []).length > 0,
      ...(isMealPrep ? { mealPrep: true, servings: servingsCount, batchItems: adjustedItems, batchTotals: sumTotals(adjustedItems) } : {}),
      ...(creditsRemaining !== undefined ? { creditsRemaining, usedCredit: true } : {}),
    };
    // Cache synchronously right after the decrement (no await between them) so a
    // replayed attemptId returns this exact result without re-charging.
    cacheAttempt(attemptId, 200, payload);
    res.json(payload);
  } catch (err) {
    console.error('Meal analysis error:', err);
    if (err.name === 'AbortError') {
      return res.status(504).json({ error: 'Meal analysis timed out. Please try again.' });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// MACRO TRACKER: Refine meal after clarifying answers (Haiku)
// ============================================================
// Adjusts an existing analysis given the user's answers — no image re-send,
// so it's fast and cheap enough to never charge for. The calibration
// multiplier is NOT re-applied on top (the answers resolve the ambiguity the
// multiplier stood in for); the refined items get the base-context factor only.
app.post('/api/refine-meal', aiLimiter, async (req, res) => {
  try {
    const { analysis, answers } = req.body;

    if (!analysis?.items?.length || !Array.isArray(answers) || !answers.length) {
      return res.status(400).json({ error: 'Missing analysis or answers' });
    }

    const answersText = answers
      .slice(0, 4)
      .map((a) => `Q: ${String(a.question).slice(0, 200)}\nA: ${String(a.answer).slice(0, 100)}`)
      .join('\n');

    const refineSchema = {
      type: 'object',
      additionalProperties: false,
      required: ['items'],
      properties: { items: MEAL_SCHEMA.properties.items },
    };

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1500,
        system:
          'You adjust a meal nutrition estimate given the user\'s answers to clarifying questions. Update only the items the answers affect; keep everything else unchanged. Keep calories consistent with 4/4/9 macro math. Add or remove line items if an answer requires it (e.g. "no oil" removes the cooking-oil item).',
        output_config: { format: { type: 'json_schema', schema: refineSchema } },
        messages: [
          {
            role: 'user',
            content: `Current estimate (raw, uncalibrated):\n${JSON.stringify({ items: analysis.raw?.items || analysis.items })}\n\nUser's answers:\n${answersText}`,
          },
        ],
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ error: data?.error?.message || 'Claude API error' });
    }

    let refined;
    try {
      refined = JSON.parse(data?.content?.[0]?.text || '');
    } catch {
      return res.status(502).json({ error: 'Model returned unparseable refinement' });
    }

    const checkedItems = enforceMacroMath(refined.items);
    // Ambiguity resolved by the user → base context factor only, no low-confidence floor.
    const factor = analysis.source === 'label' ? 1.0 : (MEAL_CALIBRATION[analysis.context] ?? MEAL_CALIBRATION.unknown);
    const adjustedItems = applyCalibration(checkedItems, factor);

    res.json({
      items: adjustedItems,
      totals: sumTotals(adjustedItems),
      raw: { items: checkedItems, totals: sumTotals(checkedItems), calibrationFactor: factor },
    });
  } catch (err) {
    console.error('Meal refinement error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// MACRO TRACKER: Refine "what's left" from a leftover photo (Haiku, free)
// ============================================================
// Uneaten-food subtraction, photo path. Free like refine-meal — charging
// twice for one meal (once for the original analysis, again for the
// leftovers) was explicitly rejected in planning. Modeled on /api/refine-meal.
const LEFTOVER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['items'],
  properties: {
    items: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'fraction_remaining'],
        properties: {
          name: { type: 'string' },
          fraction_remaining: {
            type: 'number',
            description: '0 to 1: the fraction of this line item, by weight, still visible uneaten in the leftover photo(s). 0 if fully eaten / not present.',
          },
        },
      },
    },
  },
};

const LEFTOVER_SYSTEM_PROMPT = `You are shown an itemized estimate of a meal AS SERVED, and one or more photos of what was LEFT UNEATEN after the person finished eating. For each line item in the original estimate, estimate the fraction (0 to 1) of that item, by weight, that is visible remaining in the leftover photo(s). An item completely gone (eaten, or simply not present in the leftover photo) is 0. An item still fully there is close to 1. Return exactly one entry per original item, in the same order, using the same name.`;

app.post('/api/refine-leftovers', aiLimiter, async (req, res) => {
  try {
    const { analysis, photos: rawPhotos } = req.body;
    if (!analysis?.items?.length) {
      return res.status(400).json({ error: 'Missing analysis' });
    }
    if (Array.isArray(rawPhotos) && rawPhotos.length > 3) {
      return res.status(400).json({ error: 'Maximum 3 photos per analysis' });
    }
    const photos = normalizeMealPhotos({ photos: rawPhotos });
    if (!photos.length) {
      return res.status(400).json({ error: 'Missing photos' });
    }

    const userContent = buildMealPhotoContent(photos);
    userContent.push({
      type: 'text',
      text: `Meal as served (in order): ${JSON.stringify(analysis.items.map((it) => ({ name: it.name })))}`,
    });

    // A stalled connection to Anthropic would otherwise hang this fetch
    // forever (node-fetch has no default timeout) — bound every attempt so
    // the client's error handling can actually kick in. Same pattern as the
    // supplement-audit fix (commit 751fe7b).
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 60000); // Haiku, small payload — 1 min
    let response;
    try {
      response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-haiku-4-5-20251001',
          max_tokens: 1000,
          system: LEFTOVER_SYSTEM_PROMPT,
          output_config: { format: { type: 'json_schema', schema: LEFTOVER_SCHEMA } },
          messages: [{ role: 'user', content: userContent }],
        }),
        signal: controller.signal,
      });
    } finally {
      clearTimeout(timer);
    }

    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({ error: data?.error?.message || 'Claude API error' });
    }

    let leftover;
    try {
      leftover = JSON.parse(data?.content?.[0]?.text || '');
    } catch {
      return res.status(502).json({ error: 'Model returned unparseable leftovers analysis' });
    }

    const fractionByName = new Map(
      (leftover.items || []).map((it) => [String(it.name || '').toLowerCase(), it.fraction_remaining])
    );
    // Multiply each original item by (1 - fraction_remaining) — the model only
    // ever supplies a fraction, never a calorie figure, so macro math never
    // has to be "corrected" against a model number here; enforceMacroMath
    // below just re-squares rounding drift after the scaling.
    const revisedItems = analysis.items.map((item, i) => {
      const modelItem = leftover.items?.[i];
      const fraction = typeof modelItem?.fraction_remaining === 'number'
        ? modelItem.fraction_remaining
        : (fractionByName.get(String(item.name || '').toLowerCase()) ?? 0);
      const eatenFraction = Math.max(0, Math.min(1, 1 - fraction));
      return {
        ...item,
        estimated_grams: Math.round(item.estimated_grams * eatenFraction),
        calories: Math.round(item.calories * eatenFraction),
        protein_g: Math.round(item.protein_g * eatenFraction * 10) / 10,
        carbs_g: Math.round(item.carbs_g * eatenFraction * 10) / 10,
        fat_g: Math.round(item.fat_g * eatenFraction * 10) / 10,
        alcohol_g: Math.round((item.alcohol_g || 0) * eatenFraction * 10) / 10,
        fractionRemaining: fraction,
      };
    });
    const checkedItems = enforceMacroMath(revisedItems);

    res.json({ items: checkedItems, totals: sumTotals(checkedItems) });
  } catch (err) {
    if (err.name === 'AbortError') {
      return res.status(504).json({ error: 'Leftover analysis timed out. Please try again.' });
    }
    console.error('Leftover refinement error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// ENDPOINT 3: Generate image (Gemini)
// ============================================================
app.post('/api/generate-image', aiLimiter, (req, res, next) => optionalAuth(req, res, next), async (req, res) => {
  try {
    const { prompt, photoBase64, photoMime, deviceId, intensity, prevImageBase64, isFix, sex, startCondition, distinctId } = req.body;

    // Idempotency: a dropped response makes the client replay the same attemptId.
    // Return the cached result (no second model call, no second decrement).
    const attemptId = String(req.body.attemptId || '');
    const cached = getCachedAttempt(attemptId);
    if (cached) return res.status(cached.status).json(cached.body);

    if (!prompt || !photoBase64 || !photoMime) {
      return res.status(400).json({
        error: 'Missing prompt, photoBase64, or photoMime',
      });
    }

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=${encodeURIComponent(GEMINI_API_KEY)}`;

    const callGemini = async (promptText) => {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [
            {
              role: 'user',
              parts: [
                { text: promptText },
                {
                  inline_data: {
                    mime_type: photoMime,
                    data: photoBase64,
                  },
                },
                ...(prevImageBase64 ? [{ inline_data: { mime_type: 'image/png', data: prevImageBase64 } }] : []),
              ],
            },
          ],
          generationConfig: {
            responseModalities: ['TEXT', 'IMAGE'],
          },
          safetySettings: [
            { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_ONLY_HIGH' },
            { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_ONLY_HIGH' },
            { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
            { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' },
          ],
        }),
      });

      const data = await response.json();
      if (!response.ok) return { ok: false, status: response.status, error: data?.error?.message, data };

      const parts = data?.candidates?.[0]?.content?.parts || [];
      const imgPart = parts.find((p) => p.inline_data || p.inlineData);
      if (!imgPart) return { ok: false, status: 400, data };

      const inline = imgPart.inline_data || imgPart.inlineData;
      return { ok: true, imageBase64: inline.data, imageMime: inline.mime_type || inline.mimeType || 'image/png' };
    };

    // Haiku vision compares before/after and flags edits so subtle they'd read as
    // "looks the same" — Gemini's image editor sometimes barely touches a photo even
    // when the prompt demands change. A near-identical "after" is the most damaging
    // failure (it reads as a broken product) and it hits WOMEN hardest, because the
    // old verifier asked only about a male six-pack — so it both missed weak female
    // results and burned retries rejecting legitimately feminine ones. The verifier
    // is now GENDER-AWARE and its bar scales with intensity: a strong (dramatic/max)
    // result must show real definition; a gentle (subtle/moderate) result only has to
    // clearly beat a true no-op. For women the target is a FEMININE midsection
    // (four-pack / vertical midline / oblique lines / tighter waist-to-hip taper),
    // never a male six-pack. Fail-open on any error — never block a paid generation.
    const buildVerifierQuestion = (who, intens) => {
      const strong = (intens === 'dramatic' || intens === 'max');
      if (who === 'female') {
        return strong
          ? 'Compare these two photos of the same woman. In the AFTER photo, is there CLEARLY VISIBLE feminine abdominal definition (a defined four-pack, a vertical midline groove down the stomach, and/or visible oblique lines) AND a visibly tighter, more tapered waist compared to the BEFORE photo? A tan, better lighting, or a slightly flatter stomach alone do NOT count. Reply with only YES or NO.'
          : 'Compare these two photos of the same woman. In the AFTER photo, is the midsection VISIBLY leaner and tighter than the BEFORE photo — a flatter, firmer stomach with at least a faint feminine ab outline and/or a noticeably tighter waist? A near-identical photo with barely any change is NO; a real but gentle improvement is YES. A tan or better lighting alone is NO. Reply with only YES or NO.';
      }
      return strong
        ? 'Compare these two photos of the same person. In the AFTER photo, is there CLEARLY VISIBLE ab muscle definition (actual separation lines on the stomach, not just a flatter stomach) AND a visibly tighter/more tapered waist compared to the BEFORE photo? A tan, better lighting, or a slightly flatter stomach alone do NOT count — you must be able to see actual muscle definition lines. Reply with only YES or NO.'
        : 'Compare these two photos of the same person. In the AFTER photo, is the midsection VISIBLY leaner and tighter than the BEFORE photo — a flatter, firmer stomach with at least an upper-ab outline and a tighter waist? A near-identical photo with barely any change is NO; a real but moderate improvement is YES. A tan or better lighting alone is NO. Reply with only YES or NO.';
    };

    const looksChanged = async (afterBase64, afterMime, who, intens) => {
      try {
        const response = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
          },
          body: JSON.stringify({
            model: 'claude-haiku-4-5-20251001',
            max_tokens: 8,
            messages: [
              {
                role: 'user',
                content: [
                  { type: 'text', text: 'BEFORE photo:' },
                  { type: 'image', source: { type: 'base64', media_type: photoMime, data: photoBase64 } },
                  { type: 'text', text: 'AFTER photo:' },
                  { type: 'image', source: { type: 'base64', media_type: afterMime, data: afterBase64 } },
                  { type: 'text', text: buildVerifierQuestion(who, intens) },
                ],
              },
            ],
          }),
        });
        const data = await response.json();
        const text = data?.content?.[0]?.text?.trim().toUpperCase() || '';
        return text.startsWith('YES');
      } catch (err) {
        console.error('Change verification error:', err);
        return true; // fail open — never block the flow on a verification hiccup
      }
    };

    let result = await callGemini(prompt);
    if (!result.ok) {
      const retryPreamble = `SAFE FITNESS EDIT: This is a routine body-composition edit for a fitness progress app. The subject is a consenting adult. Keep the exact same clothing and coverage as the input photo. Nothing about this edit is sexual.\n\n`;
      result = await callGemini(retryPreamble + prompt);
    }

    // Change-verifier + intensify-retry ladder (A1 telemetry + A2 gender-aware fix).
    // The old ladder ran ONLY on dramatic/max, so a female subtle/moderate no-op was
    // handed back to the user with no check and no retry. It now runs across intensities:
    //   • female → every intensity (women get the "looks the same" failure most)
    //   • male   → moderate and up (subtle-male opts out; a gentle male edit that
    //              barely changes is acceptable and not worth the extra model spend)
    // When the verifier says the result is still a near-no-op, we re-call Gemini with a
    // gender-specific "you were too subtle, push harder" preamble. Fail-open throughout,
    // and the whole loop runs BEFORE cacheAttempt so retries never re-charge a credit.
    let verifierRan = false;
    let verifierPassedFirstTry = null;
    let retryRungsUsed = 0;
    let finalVerifierPassed = null;

    const rungBudget = sex === 'female' ? 2
      : (intensity === 'dramatic' || intensity === 'max') ? 2
      : (intensity === 'moderate') ? 1
      : 0; // subtle male: no verifier / no retry

    if (result.ok && rungBudget > 0) {
      verifierRan = true;
      // Female preambles push toward a FEMININE result (four-pack / midline / tighter
      // taper) and explicitly forbid a near-identical image or masculine morphology;
      // male preambles keep the existing six-pack wording.
      const femalePreambles = [
        `Your previous attempt barely changed the body — it looks almost identical to the input, which reads as a broken result. Do NOT output a near-identical image. Reduce midsection body fat and reveal a defined FEMININE midsection: a visible four-pack with a clear vertical midline down the stomach and soft oblique lines, plus a tighter waist for a stronger waist-to-hip taper. Keep her unmistakably feminine — NO bulky or blocky muscle, NO veins or vascularity, sculpted-not-bulky shoulders. The face, hair, pose, clothing and coverage, background, framing, and lighting must stay exactly the same — only push the body composition further.\n\n`,
        `Two previous attempts were still too close to the original. This is the final attempt and the change MUST be obvious at a glance: a clearly defined feminine four-pack (vertical midline and oblique definition, not just a flat stomach) and a distinctly tighter, more tapered waist. Stay unmistakably feminine — no vascularity, no blocky or masculine muscle. Keep the face, hair, pose, clothing, framing, and lighting exactly the same — only the body composition gets much more defined.\n\n`,
      ];
      const malePreambles = [
        `Your previous attempt at this edit was too subtle and barely visible — that is a failure. This time you MUST push much harder: make the body-fat reduction, ab definition, and waist tightening dramatically more visible than a typical edit, even if it means a bigger departure from the input photo's body shape. The face, clothing, pose, and framing must still stay exactly the same — only push the body transformation itself much further.\n\n`,
        `Two previous attempts at this edit were both too subtle. This is the final attempt and it MUST show unmistakable, obvious ab muscle definition (visible separation lines, not just a flatter stomach) and a clearly tighter waist. Be aggressive with the transformation — the viewer must be able to see the change instantly without comparing closely to the original. The face, clothing, pose, and framing must still stay exactly the same — only the body transformation itself gets much more dramatic.\n\n`,
      ];
      const intensifyPreambles = sex === 'female' ? femalePreambles : malePreambles;
      let changed = false;
      for (let i = 0; i < rungBudget; i++) {
        changed = await looksChanged(result.imageBase64, result.imageMime, sex, intensity);
        if (i === 0) verifierPassedFirstTry = changed;
        if (changed) break;
        const preamble = intensifyPreambles[i] || intensifyPreambles[intensifyPreambles.length - 1];
        const retried = await callGemini(preamble + prompt);
        retryRungsUsed++;
        if (retried.ok) result = retried;
      }
      finalVerifierPassed = changed;
      // If the last rung was used without re-checking it, verify once more so the
      // "still weak after every retry" signal is accurate — that's the case we most
      // want to see in the data (and it drives the weakChange nudge below).
      if (!changed && retryRungsUsed > 0) {
        finalVerifierPassed = await looksChanged(result.imageBase64, result.imageMime, sex, intensity);
      }
    }

    // Still reads as a near-no-op after every retry: tell the client so it can nudge
    // the user toward a stronger redo instead of silently handing back a same-as-before.
    const weakChange = verifierRan && finalVerifierPassed === false;

    if (!result.ok) {
      const parts = result.data?.candidates?.[0]?.content?.parts || [];
      const textBlock = parts.find((p) => p.text)?.text;
      const blockReason = (result.data?.promptFeedback?.blockReason || '').toString().toUpperCase();
      const finishReason = (result.data?.candidates?.[0]?.finishReason || '').toString().toUpperCase();
      console.error('Image generation blocked after retry:', textBlock, result.data?.promptFeedback, result.data?.candidates?.[0]?.finishReason);
      if (result.status && result.status !== 400) {
        return res.status(result.status).json({ error: result.error || 'Image generation error' });
      }
      // Item 7: turn the raw block reason into specific, actionable guidance instead of
      // one catch-all message. A safety block is almost always a clothing/pose issue; an
      // IMAGE_* failure is usually a photo-quality issue; anything else keeps the generic
      // fallback. (IMAGE_SAFETY is caught by the safety branch first — that's intended.)
      const reason = `${blockReason} ${finishReason}`;
      let error;
      if (/SAFETY|PROHIBITED|BLOCKLIST|SPII|SEXUAL/.test(reason)) {
        error = "Our image generator's safety filter blocked this photo. It usually works with a photo in standard gym wear or swimwear, a neutral straight-on pose, and even lighting.";
      } else if (/IMAGE/.test(reason)) {
        error = "Our image generator couldn't get a clear read on this photo. Try a brighter, front-facing photo where your torso is clearly visible, in standard gym wear or swimwear.";
      } else {
        error = "Our image generator couldn't process this photo. This usually resolves with a slightly different photo — try one with a neutral pose, even lighting, and standard gym wear or swimwear.";
      }
      return res.status(400).json({ error });
    }

    const imageBase64 = result.imageBase64;

    // Credit gating: if the device has credits left, consume one and return the
    // image unlocked. If it's out of credits, still return the image but flag it
    // `locked` so the client blurs it behind the paywall (generate-and-lock).
    // Requests without a deviceId (e.g. legacy clients) are left unlocked.
    // Members generate without consuming credits.
    let locked = false;
    // A legitimate fix pass (isFix + an actual prevImageBase64 to edit) is free,
    // subject to allowFreeFix's per-device daily cap. Note allowFreeFix increments
    // its counter as a side effect, so it's called at most once per request.
    const freeFix = isFix === true && !!prevImageBase64 && allowFreeFix(deviceId);
    if (deviceId && !isActiveMembership(req.user) && !freeFix) {
      const balance = getCredits(deviceId);
      // A device is a paying customer if it has ever purchased credits (persisted
      // flag) or currently holds more than the free grant. Payers spend the credits
      // they bought without any per-IP cap; only free-allowance spends are capped.
      const isPurchaser = !!creditsStore.purchasers?.[deviceId] || balance > FREE_CREDITS;
      if (balance > 0) {
        if (!isPurchaser && !allowFreeGenByIp(req)) {
          // This IP has hit its daily free-generation ceiling — a fresh-deviceId
          // farm. Paywall the image instead of spending the free credit.
          locked = true;
        } else {
          creditsStore.balances[deviceId] = balance - 1;
          persistCreditsStore(); // fire-and-forget; in-memory copy is source of truth
        }
      } else {
        locked = true;
      }
    }

    // Per-generation telemetry (A1). Emitted to Railway logs for immediate visibility
    // and returned to the client so it can forward a PostHog event under the real
    // distinctId (retry-rung counts are only known here on the server). Fail-open.
    const telemetry = {
      sex: (sex === 'male' || sex === 'female') ? sex : null,
      intensity: intensity || null,
      startCondition: startCondition || null,
      verifierRan,
      verifierPassedFirstTry,
      retryRungsUsed,
      finalVerifierPassed,
      weakChange,
      locked,
    };
    try {
      console.log('GEN_TELEMETRY ' + JSON.stringify({ ...telemetry, distinctId: distinctId || null, isFix: !!isFix }));
    } catch (e) {}

    const payload = { imageBase64, locked, weakChange, telemetry };
    // Cache synchronously right after the decrement (no await between them) so a
    // replayed attemptId returns this exact image without re-charging.
    cacheAttempt(attemptId, 200, payload);
    res.json(payload);
  } catch (err) {
    console.error('Image generation error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// CREDITS — pay-for-more-generations
// ============================================================
// Per-device credit balances persisted as JSON in the GitHub repo (same
// pattern as todos / task-checks). Shape:
//   { balances: { [deviceId]: number }, fulfilled: { [sessionId]: true } }
// `fulfilled` makes crediting idempotent across the webhook + return-redirect
// paths so a purchase is never double-counted.
// `purchasers[deviceId] = true` once a device has completed a paid credit
// purchase. Used to exempt paying customers from the per-IP free-generation cap
// (they must never be locked out of credits they paid for).
let creditsStore = { balances: {}, fulfilled: {}, mealCounts: {}, purchasers: {} };

// Idempotency for charge-on-success endpoints: maps attemptId -> { at, status, body }.
// A dropped response makes the client replay the same attemptId (fetchWithRetry
// resends identical opts); we return the cached result instead of re-running the
// (paid) model call and re-charging a credit. In-memory only — ephemeral and the
// image payloads are large, so these never go through persistCreditsStore/the blob.
// This is correct only at a single Railway replica (per-process); if the service is
// ever scaled out, this must move to Postgres like creditsStore (see F4 in AUDIT_membership.md).
// Free "fix my result" passes: per-device daily cap so the isFix flag can't be
// used to generate unlimited free images. In-memory, same single-replica caveat
// as attemptCache below.
const fixCounts = new Map(); // deviceId -> { day: 'YYYY-MM-DD', count }
const FIX_DAILY_CAP = 4;
function allowFreeFix(deviceId) {
  if (!deviceId) return false;
  const day = new Date().toISOString().slice(0, 10);
  const rec = fixCounts.get(deviceId);
  if (!rec || rec.day !== day) { fixCounts.set(deviceId, { day, count: 1 }); return true; }
  if (rec.count >= FIX_DAILY_CAP) return false;
  rec.count += 1;
  return true;
}

// Free-generation abuse cap. Free credits are keyed to a browser-generated
// deviceId, so a farmer can mint unlimited fresh ids (each implicitly starting
// with FREE_CREDITS) and burn real Gemini/Claude money on free generations. This
// adds a per-IP daily ceiling on generations spent from the FREE allowance only
// (non-member, non-fix, non-purchaser). Paid credits and members are never
// affected. In-memory, single-replica caveat (same as fixCounts/attemptCache —
// move to Postgres if the service ever scales out; see F4 in AUDIT_membership.md).
const freeIpCounts = new Map(); // 'ip|YYYY-MM-DD' -> count
const FREE_IP_DAILY_CAP = 6;    // ~2 devices' worth of free generations per IP/day
// Best-effort client IP. Global `trust proxy` is intentionally NOT enabled (that
// would also change the existing express-rate-limit buckets — the separate N2
// audit finding), so we read the forwarded client IP here just for this cap.
// Falls back to the socket address; it never returns a constant, so the cap can
// never collapse into one global bucket that would lock out all users at once.
function clientIp(req) {
  const xff = req.headers['x-forwarded-for'];
  if (xff) { const first = String(xff).split(',')[0].trim(); if (first) return first; }
  return req.socket?.remoteAddress || req.ip || 'unknown';
}
// Returns true if this IP may still spend a FREE generation today, counting it.
// Only called on the free-allowance path, so the counter tracks free gens only.
function allowFreeGenByIp(req) {
  const day = new Date().toISOString().slice(0, 10);
  const key = `${clientIp(req)}|${day}`;
  const n = freeIpCounts.get(key) || 0;
  if (n >= FREE_IP_DAILY_CAP) return false;
  freeIpCounts.set(key, n + 1);
  return true;
}

const attemptCache = new Map();
const ATTEMPT_TTL_MS = 10 * 60 * 1000;
function getCachedAttempt(id) {
  if (!id) return null;
  const hit = attemptCache.get(id);
  if (!hit) return null;
  if (Date.now() - hit.at > ATTEMPT_TTL_MS) { attemptCache.delete(id); return null; }
  return hit;
}
function cacheAttempt(id, status, body) {
  if (!id) return;
  attemptCache.set(id, { at: Date.now(), status, body });
  // opportunistic sweep so the map can't grow unbounded
  if (attemptCache.size > 500) {
    const cutoff = Date.now() - ATTEMPT_TTL_MS;
    for (const [k, v] of attemptCache) if (v.at < cutoff) attemptCache.delete(k);
  }
}

async function loadCreditsStore() {
  const empty = { balances: {}, fulfilled: {}, mealCounts: {}, purchasers: {} };
  if (!GITHUB_TOKEN) return empty;
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${CREDITS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return empty;
    const data = await res.json();
    const parsed = JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
    return { balances: parsed.balances || {}, fulfilled: parsed.fulfilled || {}, mealCounts: parsed.mealCounts || {}, purchasers: parsed.purchasers || {} };
  } catch (e) {
    console.error('loadCreditsStore error:', e.message);
    return empty;
  }
}

async function persistCreditsStore() {
  if (!GITHUB_TOKEN) return;
  try {
    const content = Buffer.from(JSON.stringify(creditsStore, null, 2)).toString('base64');
    const getRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${CREDITS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    const body = { message: 'Update credits', content };
    if (getRes.ok) { const cur = await getRes.json(); body.sha = cur.sha; }
    await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${CREDITS_FILE}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (e) { console.error('persistCreditsStore error:', e.message); }
}

// Balance for a device — new devices implicitly start with FREE_CREDITS.
function getCredits(deviceId) {
  if (!deviceId) return 0;
  const b = creditsStore.balances[deviceId];
  return typeof b === 'number' ? b : FREE_CREDITS;
}

// Idempotently grant a completed checkout session's credits to its device.
async function fulfillCreditsSession(session) {
  if (!session || session.payment_status !== 'paid') return false;
  const sid = session.id;
  if (creditsStore.fulfilled[sid]) return false; // already credited
  const meta = session.metadata || {};
  if (meta.kind !== 'credits') return false;
  const deviceId = meta.deviceId;
  const credits = parseInt(meta.credits, 10);
  if (!deviceId || !credits) return false;

  creditsStore.balances[deviceId] = getCredits(deviceId) + credits;
  creditsStore.fulfilled[sid] = true;
  creditsStore.purchasers = creditsStore.purchasers || {};
  creditsStore.purchasers[deviceId] = true; // exempt paying customers from the per-IP free cap
  await persistCreditsStore();
  console.log(`Credited ${credits} to ${deviceId} (session ${sid})`);
  return true;
}

// ============================================================
// EMAIL SUBSCRIBERS — capture + MailerLite sync
// ============================================================
// Emails captured on the download screen, persisted as JSON in the GitHub
// repo (same pattern as credits) so we always own the raw list, and pushed
// to MailerLite which runs the autoresponder. Shape:
//   { emails: { [email]: { subscribedAt, deviceId, synced } } }
// `synced:false` entries are retried on the next subscribe attempt from the
// same email, so a MailerLite outage never loses an address.
let subscribersStore = { emails: {} };

async function loadSubscribersStore() {
  if (!GITHUB_TOKEN) return { emails: {} };
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${SUBSCRIBERS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return { emails: {} };
    const data = await res.json();
    const parsed = JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
    return { emails: parsed.emails || {} };
  } catch (e) {
    console.error('loadSubscribersStore error:', e.message);
    return { emails: {} };
  }
}

async function persistSubscribersStore() {
  if (!GITHUB_TOKEN) return;
  try {
    const content = Buffer.from(JSON.stringify(subscribersStore, null, 2)).toString('base64');
    const getRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${SUBSCRIBERS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    const body = { message: 'Update subscribers', content };
    if (getRes.ok) { const cur = await getRes.json(); body.sha = cur.sha; }
    await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${SUBSCRIBERS_FILE}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (e) { console.error('persistSubscribersStore error:', e.message); }
}

// Upsert a subscriber into MailerLite (200 = updated, 201 = created).
async function pushToMailerLite(email) {
  if (!MAILERLITE_API_KEY) { console.warn('MAILERLITE_API_KEY not set — subscriber stored locally only'); return false; }
  try {
    const body = { email };
    if (MAILERLITE_GROUP_ID) body.groups = [MAILERLITE_GROUP_ID];
    const res = await fetch('https://connect.mailerlite.com/api/subscribers', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${MAILERLITE_API_KEY}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(body),
    });
    if (!res.ok) console.error(`MailerLite subscribe failed (${res.status}):`, (await res.text()).slice(0, 300));
    return res.ok;
  } catch (e) {
    console.error('pushToMailerLite error:', e.message);
    return false;
  }
}

app.post('/api/subscribe', async (req, res) => {
  const email = String(req.body?.email || '').trim().toLowerCase();
  const deviceId = String(req.body?.deviceId || '');
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  // Capture the user's freshly-generated before/after (sent by the download
  // screen) so the welcome email can embed it. Best-effort, keyed by email;
  // runs before the early-return so a repeat submit can still backfill images.
  saveWelcomeImages(email, String(req.body?.before || ''), String(req.body?.after || '')).catch(() => {});

  const existing = subscribersStore.emails[email];
  if (existing?.synced) return res.json({ ok: true }); // already captured + synced

  const synced = await pushToMailerLite(email);
  const entry = {
    subscribedAt: existing?.subscribedAt || new Date().toISOString(),
    deviceId: existing?.deviceId || deviceId,
    synced,
  };
  // Preserve any existing welcome-sequence progress on a retry; initialize it
  // (welcomeStep 0, due now) only for a genuinely new subscriber.
  if (existing && existing.welcomeStep !== undefined) {
    entry.welcomeStep   = existing.welcomeStep;
    entry.welcomeNextAt = existing.welcomeNextAt;
    entry.welcomeSentAt = existing.welcomeSentAt;
    entry.unsubscribed  = existing.unsubscribed;
    if (existing.excluded) entry.excluded = true;
  } else {
    ensureWelcomeFields(email, entry); // new subscriber → Email 1 on next sweep
  }
  subscribersStore.emails[email] = entry;
  persistSubscribersStore(); // fire-and-forget; in-memory copy is source of truth
  console.log(`Subscriber ${existing ? 'retried' : 'added'}: ${email} (MailerLite sync: ${synced})`);
  res.json({ ok: true });
});

// One-click / link unsubscribe from the welcome sequence. GET is used by the
// footer link; POST is used by Gmail/Apple Mail one-click (List-Unsubscribe-Post).
// The token is an HMAC of the email so the link can't be guessed or enumerated.
function unsubscribePage(message) {
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Abs by AI</title></head>
<body style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#fafafa;color:#111;display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0">
<div style="max-width:440px;text-align:center;padding:32px">
<h1 style="font-size:22px;margin:0 0 12px">${message}</h1>
<p style="color:#666;font-size:15px;line-height:1.5">You can still use everything on <a href="${SITE_URL}" style="color:#111">absbyai.com</a> — this only affects the welcome emails.</p>
</div></body></html>`;
}

async function handleUnsubscribe(req, res) {
  const email = String(req.query?.email || '').trim().toLowerCase();
  const token = String(req.query?.token || '');
  if (!email || !unsubTokenValid(email, token)) {
    return res.status(400).send(unsubscribePage("That unsubscribe link isn't valid."));
  }
  const entry = subscribersStore.emails[email];
  if (entry && !entry.unsubscribed) {
    entry.unsubscribed = true;
    entry.unsubscribedAt = new Date().toISOString();
    persistSubscribersStore();
    console.log(`Unsubscribed from welcome sequence: ${email}`);
  }
  res.status(200).send(unsubscribePage("You're unsubscribed."));
}

app.get('/api/unsubscribe', handleUnsubscribe);
app.post('/api/unsubscribe', handleUnsubscribe);

// Serves a subscriber's stored before/after image for the welcome email.
// Public + token-gated (email clients can't send auth headers). Streams the
// stored data-URI as a real image so inboxes render it (they strip inline
// data-URIs). No watermark — this is the clean original by design.
app.get('/api/welcome-image', async (req, res) => {
  const email = String(req.query.e || '').trim().toLowerCase();
  const kind = req.query.k === 'before' ? 'before_image' : 'after_image';
  const token = String(req.query.t || '');
  if (!email || !welcomeImgTokenValid(email, token)) return res.status(403).end();
  if (!db) return res.status(404).end();
  try {
    const { rows } = await db.query(`SELECT ${kind} AS img FROM welcome_images WHERE email = $1`, [email]);
    const dataUri = rows[0]?.img;
    const m = /^data:(image\/[a-zA-Z0-9.+-]+);base64,(.*)$/s.exec(dataUri || '');
    if (!m) return res.status(404).end();
    res.set('Content-Type', m[1]);
    res.set('Cache-Control', 'public, max-age=86400');
    res.send(Buffer.from(m[2], 'base64'));
  } catch (e) {
    console.error('welcome-image error:', e.message);
    res.status(500).end();
  }
});

// ============================================================
// ACCOUNTS — email/password auth, sessions, meal sync (Postgres)
// ============================================================
// Opaque session tokens (not cookies): the site is served cross-origin from
// the Railway URL and also runs inside the iOS/Android wrappers, where
// third-party cookies are unreliable. Clients send `Authorization: Bearer`.
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 20,
  message: 'Too many attempts, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

const SESSION_DAYS = 90;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function dbUnavailable(res) {
  return res.status(503).json({ error: 'Accounts are unavailable right now.' });
}

async function createSession(userId) {
  const token = crypto.randomBytes(32).toString('hex');
  await db.query(
    `INSERT INTO sessions (token, user_id, expires_at) VALUES ($1, $2, now() + interval '${SESSION_DAYS} days')`,
    [token, userId]
  );
  return token;
}

// Attaches req.user = { id, email, device_id } or 401s.
async function requireAuth(req, res, next) {
  if (!db) return dbUnavailable(res);
  const token = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!token) return res.status(401).json({ error: 'Not logged in' });
  try {
    const { rows } = await db.query(
      `SELECT u.id, u.email, u.device_id FROM sessions s JOIN users u ON u.id = s.user_id
       WHERE s.token = $1 AND s.expires_at > now()`,
      [token]
    );
    if (!rows.length) return res.status(401).json({ error: 'Session expired' });
    req.user = rows[0];
    req.sessionToken = token;
    next();
  } catch (e) {
    console.error('requireAuth error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
}

// ── Admin gate ──
// Allowlisted emails on the existing session auth. No new password/secret — an
// admin logs in with their normal account credentials. If ADMIN_EMAILS is unset
// or empty, every /api/admin/* route returns 503 and the feature is inert.
const ADMIN_EMAILS = (process.env.ADMIN_EMAILS || '')
  .split(',').map(s => s.trim().toLowerCase()).filter(Boolean);

// Runs requireAuth first, then enforces the allowlist. Must be applied to every
// /api/admin/* route — hiding the UI is not access control.
function requireAdmin(req, res, next) {
  requireAuth(req, res, () => {
    if (!ADMIN_EMAILS.length) return res.status(503).json({ error: 'Admin not configured' });
    if (!ADMIN_EMAILS.includes(String(req.user.email || '').toLowerCase())) {
      return res.status(403).json({ error: 'Not authorized' });
    }
    next();
  });
}

app.post('/api/auth/signup', authLimiter, async (req, res) => {
  if (!db) return dbUnavailable(res);
  const email = String(req.body?.email || '').trim().toLowerCase();
  const password = String(req.body?.password || '');
  const deviceId = String(req.body?.deviceId || '');
  if (!EMAIL_RE.test(email) || email.length > 254) return res.status(400).json({ error: 'Invalid email' });
  if (password.length < 8) return res.status(400).json({ error: 'Password must be at least 8 characters' });
  if (!deviceId) return res.status(400).json({ error: 'Missing device id' });
  try {
    const hash = await bcrypt.hash(password, 10);
    const { rows } = await db.query(
      `INSERT INTO users (email, password_hash, device_id) VALUES ($1, $2, $3)
       ON CONFLICT (email) DO NOTHING RETURNING id`,
      [email, hash, deviceId]
    );
    if (!rows.length) return res.status(409).json({ error: 'An account with that email already exists. Log in instead.' });
    const token = await createSession(rows[0].id);
    pushToMailerLite(email).catch(() => {}); // join the email list, same as the capture screen
    console.log(`Account created: ${email}`);
    res.json({ token, email, deviceId });
  } catch (e) {
    console.error('signup error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/auth/login', authLimiter, async (req, res) => {
  if (!db) return dbUnavailable(res);
  const email = String(req.body?.email || '').trim().toLowerCase();
  const password = String(req.body?.password || '');
  const deviceId = String(req.body?.deviceId || '');
  try {
    const { rows } = await db.query('SELECT id, password_hash, device_id FROM users WHERE email = $1', [email]);
    const user = rows[0];
    const ok = user && (await bcrypt.compare(password, user.password_hash));
    if (!ok) return res.status(401).json({ error: 'Invalid email or password' });

    // Credit linking: fold this device's explicit balance into the account's
    // canonical device, then the client adopts the canonical device id so all
    // existing credit/Stripe code keeps working, now effectively per-account.
    if (deviceId && deviceId !== user.device_id) {
      const stray = creditsStore.balances[deviceId];
      if (typeof stray === 'number') {
        creditsStore.balances[user.device_id] = getCredits(user.device_id) + stray;
        delete creditsStore.balances[deviceId];
        persistCreditsStore(); // fire-and-forget, in-memory copy is source of truth
      }
    }

    const token = await createSession(user.id);
    backfillProfile(user.id).catch(() => {}); // fill profile essentials from existing intakes
    res.json({ token, email, deviceId: user.device_id });
  } catch (e) {
    console.error('login error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ── Password reset ──
// Transactional email via Resend (RESEND_API_KEY). Token is random, stored
// hashed, single-use, 60-minute expiry. request-reset always answers 200 so
// the endpoint can't be used to enumerate which emails have accounts.
const RESEND_API_KEY = process.env.RESEND_API_KEY;
const RESET_FROM     = process.env.RESET_FROM || 'Abs by AI <noreply@absbyai.com>';
const SITE_URL       = process.env.SITE_URL || 'https://absbyai.com';

// ── Marketing (welcome autoresponder) sending identity ──
// Sent from a DEDICATED subdomain (mail.absbyai.com) so a marketing spam
// complaint can never taint password-reset / trial deliverability on the root
// domain. MARKETING_FROM must be a Resend-verified sender on that subdomain;
// until it's set we fall back to the transactional identity so nothing breaks,
// but the sweep is also gated on WELCOME_ENABLED so it stays off until DNS is
// verified. Reply-To routes real replies to Dan's inbox (Namecheap forwarding).
const MARKETING_FROM     = process.env.MARKETING_FROM || RESET_FROM;
const MARKETING_REPLY_TO = process.env.MARKETING_REPLY_TO || 'dan@absbyai.com';
// Master on/off switch for the welcome sequence. Off by default so the sweep
// can't send from an unverified subdomain; flip WELCOME_ENABLED=true on Railway
// only after mail.absbyai.com is verified in Resend.
const WELCOME_ENABLED    = process.env.WELCOME_ENABLED === 'true';
// Signs unsubscribe links so they can't be guessed/enumerated. Falls back to an
// existing always-set server secret so links are stable without new config.
const UNSUB_SECRET       = process.env.UNSUBSCRIBE_SECRET || STRIPE_WEBHOOK_SECRET || GITHUB_TOKEN || 'absbyai-unsub';
// CAN-SPAM requires a real physical postal address in every marketing email.
// Baked in as the default so it's always present; MARKETING_ADDRESS on Railway
// can override it without a code change.
const MARKETING_ADDRESS  = process.env.MARKETING_ADDRESS || 'Abs By AI<br>3520 Cavu Rd.<br>Georgetown, TX 78628';

async function sendResetEmail(email, token) {
  if (!RESEND_API_KEY) { console.warn('RESEND_API_KEY not set — reset email skipped for', email); return; }
  const link = `${SITE_URL}/?reset=${token}`;
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: RESET_FROM,
      to: [email],
      subject: 'Reset your Abs by AI password',
      html: `<p>Someone (hopefully you) asked to reset the password for this Abs by AI account.</p>
<p><a href="${link}" style="display:inline-block;padding:12px 22px;background:#111;color:#fff;border-radius:8px;text-decoration:none;font-weight:700">Reset my password</a></p>
<p>Or paste this link into your browser:<br>${link}</p>
<p>This link expires in 60 minutes. If you didn't ask for this, you can safely ignore this email — your password hasn't changed.</p>`,
    }),
  });
  if (!res.ok) console.error('Resend error:', res.status, (await res.text()).slice(0, 300));
}

// Trial-ending reminder (fires 2 days out via trialReminderSweep). Returns true
// only when Resend accepted the email, so the sweep sets the "sent" flag only on
// a real send and retries on the next pass otherwise (incl. when the key is unset).
async function sendTrialEndingEmail(email, plan) {
  if (!RESEND_API_KEY) { console.warn('RESEND_API_KEY not set — trial-ending email skipped for', email); return false; }
  const planDef = MEMBERSHIP_PLANS[plan] || MEMBERSHIP_PLANS.monthly;
  const priceStr = planDef.interval === 'year'
    ? `$${(planDef.priceInCents / 100).toFixed(2)}/year`
    : `$${(planDef.priceInCents / 100).toFixed(2)}/month`;
  const link = SITE_URL;
  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: RESET_FROM,
        to: [email],
        subject: 'Your Abs By AI free trial ends in 2 days',
        html: `<p>Hey — a quick heads-up: your Abs By AI free trial ends in <strong>2 days</strong>.</p>
<p>When it ends, your membership begins and you'll be charged <strong>${priceStr}</strong>. You'll keep everything you've been using: your AI trainer, AI nutritionist, sleep coach, and unlimited transformations &amp; meal tracking.</p>
<p>Happy to keep going? You don't need to do anything. Changed your mind? You can <strong>manage or cancel anytime</strong> — cancel before the trial ends and you won't be charged.</p>
<p><a href="${link}" style="display:inline-block;padding:12px 22px;background:#111;color:#fff;border-radius:8px;text-decoration:none;font-weight:700">Manage or cancel my membership</a></p>
<p>Or paste this link into your browser:<br>${link}</p>
<p>Thanks for giving Abs By AI a try.</p>`,
      }),
    });
    if (!res.ok) { console.error('Resend error (trial-ending):', res.status, (await res.text()).slice(0, 300)); return false; }
    return true;
  } catch (e) {
    console.error('sendTrialEndingEmail error:', e.message);
    return false;
  }
}

// ============================================================
// WELCOME AUTORESPONDER — 5-email sequence over ~10 days (Resend)
// ============================================================
// Every new email-capture (and the existing backfilled subscribers) receives a
// short 5-email welcome sequence: day 0 / 2 / 4 / 7 / 10. Copy lives here (ported
// from MAILERLITE_BUILD.md). Sending is idempotent — welcomeSweep advances a
// subscriber's step ONLY after Resend accepts the send, so an outage defers
// rather than skips, and no step is ever sent twice.

// Days to wait AFTER sending email index i (0-based) before the next is due.
// [after E1 → 2d, after E2 → 2d, after E3 → 3d, after E4 → 3d]; after E5 → done.
const WELCOME_DELAYS_DAYS = [2, 2, 3, 3];
const DAY_MS = 24 * 60 * 60 * 1000;

// Signed, non-enumerable unsubscribe token (HMAC of the lowercased email).
function unsubToken(email) {
  return crypto.createHmac('sha256', UNSUB_SECRET).update(String(email).toLowerCase()).digest('hex');
}
function unsubTokenValid(email, token) {
  const expected = unsubToken(email);
  const a = Buffer.from(String(token || ''), 'utf8');
  const b = Buffer.from(expected, 'utf8');
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
function unsubscribeUrl(email) {
  return `${SITE_URL}/api/unsubscribe?email=${encodeURIComponent(email)}&token=${unsubToken(email)}`;
}

// ── Welcome-email images (the user's own before/after) ──
// Email clients strip data-URI <img>, so the stored images are served from a
// public, token-gated endpoint that the email references by URL. Token is an
// HMAC (distinct salt from unsubscribe) so links aren't guessable/enumerable.
function welcomeImgToken(email) {
  return crypto.createHmac('sha256', UNSUB_SECRET).update('welcome-img:' + String(email).toLowerCase()).digest('hex');
}
function welcomeImgTokenValid(email, token) {
  const a = Buffer.from(String(token || ''), 'utf8');
  const b = Buffer.from(welcomeImgToken(email), 'utf8');
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}
function welcomeImageUrl(email, kind) {
  return `${SITE_URL}/api/welcome-image?e=${encodeURIComponent(email)}&k=${kind}&t=${welcomeImgToken(email)}`;
}

// Cap stored images so a giant payload can't bloat the DB (data-URI chars).
const MAX_WELCOME_IMG_CHARS = 12 * 1024 * 1024; // ~9 MB decoded

// Upsert the before/after captured at signup. Best-effort; never throws to the caller.
async function saveWelcomeImages(email, before, after) {
  if (!db) return;
  if (!before?.startsWith('data:image/') || !after?.startsWith('data:image/')) return;
  if (before.length > MAX_WELCOME_IMG_CHARS || after.length > MAX_WELCOME_IMG_CHARS) return;
  try {
    await db.query(
      `INSERT INTO welcome_images (email, before_image, after_image) VALUES ($1, $2, $3)
       ON CONFLICT (email) DO UPDATE SET before_image = EXCLUDED.before_image,
         after_image = EXCLUDED.after_image, created_at = now()`,
      [email, before, after]
    );
  } catch (e) { console.warn('saveWelcomeImages error:', e.message); }
}

// True if we have both images for this email (so Email 1 can embed them).
async function hasWelcomeImages(email) {
  if (!db) return false;
  try {
    const { rows } = await db.query(
      'SELECT 1 FROM welcome_images WHERE email = $1 AND before_image IS NOT NULL AND after_image IS NOT NULL', [email]
    );
    return rows.length > 0;
  } catch (e) { return false; }
}

// The 5 emails. `body` is the inner HTML; the footer (unsubscribe + postal
// address) is appended by wrapWelcomeHtml. Plain-text-style markup only (no
// images) for best inboxing on a warming subdomain.
const WELCOME_EMAILS = [
  {
    subject: 'Your future self is ready 💪',
    body: `
<p>Hey — it's Dan from Abs by AI.</p>
<p>You just did something most people never do: you actually <em>looked</em> at where you're headed. That image isn't a fantasy — it's a target.</p>
<p>Here's what to do with it right now:</p>
<p><strong>1. Set it as your lockscreen.</strong> You unlock your phone ~150 times a day. That's 150 reminders of where you're going. (Your watermark-free download is unlocked on <a href="${SITE_URL}">absbyai.com</a> — grab it if you haven't.)</p>
<p><strong>2. Tell one person.</strong> Goals you say out loud are the ones that happen.</p>
<p>Over the next week I'll send you a few short emails on how people actually close the gap between the before and the after photo. No fluff, no 45-minute YouTube videos — just the stuff that works.</p>
<p><strong>Do me one favor:</strong> hit reply and tell me your goal — even one line. I read every single one, and it makes sure these emails land in your inbox instead of promotions. (While you're at it, add dan@absbyai.com to your contacts.)</p>
<p>Talk soon,<br>Dan</p>`,
  },
  {
    subject: 'Put your future self on the wall',
    body: `
<p>Quick question: where's your image right now?</p>
<p>If the answer is "buried in my camera roll," it's already losing power. Motivation research is boringly consistent on this — visual cues in your environment beat willpower every time. Out of sight, out of mind isn't a cliché, it's how your brain works.</p>
<p>That's why we print them.</p>
<p><strong>Your future self, on canvas, on your wall.</strong> Gym corner, home office, bathroom mirror wall — wherever you'll see it when the 6am alarm goes off and you're negotiating with yourself.</p>
<ul>
<li>Poster from <strong>$18</strong></li>
<li>Gallery canvas from <strong>$34</strong></li>
<li>Framed canvas from <strong>$75</strong></li>
</ul>
<p>→ <a href="${SITE_URL}">Print my future self</a></p>
<p>Every morning it asks you one question: <em>are we doing this or not?</em></p>
<p>— Dan</p>`,
  },
  {
    subject: 'The 3 levers (ignore everything else)',
    body: `
<p>The fitness industry makes money by making this complicated. It isn't. Getting from your before to your after is three levers:</p>
<p><strong>1. Calorie deficit.</strong> You cannot out-train a surplus. A modest deficit (300–500 cal/day) loses fat without wrecking your energy.</p>
<p><strong>2. Protein.</strong> Roughly 0.7–1g per pound of goal bodyweight. It protects muscle while you cut and keeps you full. Most people are at half that.</p>
<p><strong>3. Consistency over intensity.</strong> Four okay workouts a week for a year beats two perfect weeks followed by quitting. Every time.</p>
<p>That's it. Lever 1 and 2 are won or lost in the kitchen, which is why we built a <strong>free macro tracker</strong> into Abs by AI — snap your meal, get calories and protein instantly. No accounts, no BS.</p>
<p>→ <a href="${SITE_URL}">Track a meal in 10 seconds</a></p>
<p>— Dan</p>`,
  },
  {
    subject: 'What does 6 months vs. 2 years look like?',
    body: `
<p>Here's something interesting from our data: the people most likely to actually follow through generate <strong>more than one</strong> future self.</p>
<p>Makes sense when you think about it —</p>
<ul>
<li>The <strong>6-month version</strong>: realistic, near, keeps you honest</li>
<li>The <strong>2-year version</strong>: the full transformation, keeps you dreaming</li>
<li>The <strong>"what if I really committed"</strong> version: your ceiling</li>
</ul>
<p>One image is a picture. A progression is a plan.</p>
<p>You've got credits waiting at <a href="${SITE_URL}">absbyai.com</a> — and if you're out, the Starter Pack is <strong>5 generations for $4.99</strong> (Power Pack: 20 for $14.99). Try different timeframes, different goals, even different styles.</p>
<p>→ <a href="${SITE_URL}">Generate my 2-year self</a></p>
<p>— Dan</p>`,
  },
  {
    subject: 'You\'re not "trying to lose weight"',
    body: `
<p>Ten days since you saw your future self. Here's the mental trick that separates people who make it from people who don't:</p>
<p>Stop saying "I'm trying to lose weight." Start saying "I'm becoming <em>that guy/girl</em>" — the one in the image.</p>
<p>James Clear calls it identity-based habits: you don't chase outcomes, you vote for an identity. Every workout is a vote. Every tracked meal is a vote. Skipping one isn't failure, it's just a vote the other way — win the count, not every ballot.</p>
<p>This is exactly why a printed future self works so well. It's not decor. It's your identity, staring back at you, asking for your vote today.</p>
<p>If you didn't grab one last week: posters from $18, canvas from $34 → <a href="${SITE_URL}">absbyai.com</a></p>
<p>Proud of you for still being here. Most people's motivation died 6 days ago.</p>
<p>— Dan</p>`,
  },
];

// Wrap an email body with the compliant footer (unsubscribe + postal address).
function wrapWelcomeHtml(email, innerHtml) {
  return `<div style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;font-size:16px;line-height:1.5;color:#111;max-width:560px">
${innerHtml}
<hr style="border:none;border-top:1px solid #e5e5e5;margin:28px 0 14px">
<p style="font-size:12px;color:#888;line-height:1.5">
You're receiving this because you signed up at absbyai.com.<br>
<a href="${unsubscribeUrl(email)}" style="color:#888">Unsubscribe</a> from these emails at any time.<br>
${MARKETING_ADDRESS}
</p>
</div>`;
}

// The user's own transformation, for the top of Email 1: a big "after" hero
// ("your future self") followed by a labeled before → after pair. Images are
// referenced by URL (inboxes strip inline data). Email-safe table markup.
function welcomeImageBlockHtml(email) {
  const afterUrl = welcomeImageUrl(email, 'after');
  const beforeUrl = welcomeImageUrl(email, 'before');
  return `
<div style="margin:24px 0 4px">
  <img src="${afterUrl}" alt="Your future self" width="560" style="width:100%;max-width:560px;height:auto;border-radius:14px;display:block">
  <p style="font-size:13px;color:#888;margin:8px 0 0;text-align:center">Your future self 💪</p>
</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:14px 0 6px;border-collapse:collapse"><tr>
  <td width="50%" style="padding-right:5px;vertical-align:top">
    <img src="${beforeUrl}" alt="Before" width="275" style="width:100%;height:auto;border-radius:10px;display:block">
    <p style="font-size:11px;color:#999;margin:6px 0 0;text-align:center;text-transform:uppercase;letter-spacing:.06em">Before</p>
  </td>
  <td width="50%" style="padding-left:5px;vertical-align:top">
    <img src="${afterUrl}" alt="After" width="275" style="width:100%;height:auto;border-radius:10px;display:block">
    <p style="font-size:11px;color:#999;margin:6px 0 0;text-align:center;text-transform:uppercase;letter-spacing:.06em">After</p>
  </td>
</tr></table>`;
}

// Build the final HTML for email `idx`. For Email 1, embeds the user's own
// before/after (hero + pair) when we captured it at signup; otherwise falls
// back to the text-only body unchanged.
async function buildWelcomeEmailHtml(email, idx) {
  const tmpl = WELCOME_EMAILS[idx];
  let body = tmpl.body;
  if (idx === 0 && await hasWelcomeImages(email)) {
    // Insert the images right after the "…it's a target." opener, so "That
    // image" points at the real picture.
    body = body.replace(
      "<p>Here's what to do with it right now:</p>",
      welcomeImageBlockHtml(email) + "\n<p>Here's what to do with it right now:</p>"
    );
  }
  return wrapWelcomeHtml(email, body);
}

// Send welcome email index `idx` (0-based). Returns true only when Resend
// accepts it, so the sweep advances the subscriber only on a real send.
async function sendWelcomeEmail(email, idx) {
  const tmpl = WELCOME_EMAILS[idx];
  if (!tmpl) return false;
  if (!RESEND_API_KEY) { console.warn('RESEND_API_KEY not set — welcome email skipped for', email); return false; }
  try {
    const html = await buildWelcomeEmailHtml(email, idx);
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: MARKETING_FROM,
        to: [email],
        reply_to: MARKETING_REPLY_TO,
        subject: tmpl.subject,
        html,
        // One-click unsubscribe for Gmail/Apple Mail (RFC 8058).
        headers: {
          'List-Unsubscribe': `<${unsubscribeUrl(email)}>`,
          'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
        },
      }),
    });
    if (!res.ok) { console.error('Resend error (welcome):', res.status, (await res.text()).slice(0, 300)); return false; }
    return true;
  } catch (e) {
    console.error('sendWelcomeEmail error:', e.message);
    return false;
  }
}

// Ensure a subscriber entry has the welcome-sequence fields. Test/junk addresses
// (@example.com) are marked excluded so they never enter the sequence. Returns
// true if it mutated the entry (so the caller can persist).
function ensureWelcomeFields(email, entry) {
  if (!entry || entry.welcomeStep !== undefined) return false;
  if (/@example\.com$/i.test(email)) {
    entry.welcomeStep = WELCOME_EMAILS.length; // done
    entry.excluded = true;
    return true;
  }
  entry.welcomeStep = 0;
  entry.welcomeNextAt = new Date().toISOString();
  entry.welcomeSentAt = {};
  entry.unsubscribed = false;
  return true;
}

// The welcome sweep — clone of trialReminderSweep's send-then-advance pattern.
async function welcomeSweep() {
  if (!WELCOME_ENABLED) return;
  let changed = false;
  const now = Date.now();
  for (const [email, entry] of Object.entries(subscribersStore.emails)) {
    if (!entry) continue;
    // Lazily backfill sequence fields on any entry that predates this feature.
    if (ensureWelcomeFields(email, entry)) changed = true;
    if (entry.excluded || entry.unsubscribed) continue;
    if (entry.welcomeStep >= WELCOME_EMAILS.length) continue;
    if (/@example\.com$/i.test(email)) continue;
    if (entry.welcomeNextAt && new Date(entry.welcomeNextAt).getTime() > now) continue;

    const idx = entry.welcomeStep; // 0-based index of the email to send
    const sent = await sendWelcomeEmail(email, idx);
    if (!sent) continue; // defer to next pass on any failure

    entry.welcomeStep = idx + 1;
    entry.welcomeSentAt = entry.welcomeSentAt || {};
    entry.welcomeSentAt[String(idx + 1)] = new Date().toISOString();
    const delayDays = WELCOME_DELAYS_DAYS[idx];
    entry.welcomeNextAt = delayDays ? new Date(now + delayDays * DAY_MS).toISOString() : null;
    changed = true;
    console.log(`Welcome email ${idx + 1}/${WELCOME_EMAILS.length} sent to ${email}`);
  }
  if (changed) persistSubscribersStore();
}

const sha256 = (s) => crypto.createHash('sha256').update(s).digest('hex');

app.post('/api/auth/request-reset', authLimiter, async (req, res) => {
  if (!db) return dbUnavailable(res);
  const email = String(req.body?.email || '').trim().toLowerCase();
  res.json({ ok: true }); // always — no account enumeration
  if (!EMAIL_RE.test(email)) return;
  try {
    const { rows } = await db.query('SELECT id FROM users WHERE email = $1', [email]);
    if (!rows.length) return;
    const token = crypto.randomBytes(32).toString('hex');
    await db.query(
      `INSERT INTO password_reset_tokens (token_hash, user_id, expires_at) VALUES ($1, $2, now() + interval '60 minutes')`,
      [sha256(token), rows[0].id]
    );
    await sendResetEmail(email, token);
    console.log(`Password reset requested: ${email}`);
  } catch (e) {
    console.error('request-reset error:', e.message);
  }
});

app.post('/api/auth/reset-password', authLimiter, async (req, res) => {
  if (!db) return dbUnavailable(res);
  const token = String(req.body?.token || '');
  const password = String(req.body?.password || '');
  if (!token) return res.status(400).json({ error: 'Missing reset token' });
  if (password.length < 8) return res.status(400).json({ error: 'Password must be at least 8 characters' });
  try {
    const { rows } = await db.query(
      'SELECT user_id FROM password_reset_tokens WHERE token_hash = $1 AND expires_at > now()',
      [sha256(token)]
    );
    if (!rows.length) return res.status(400).json({ error: 'This reset link is invalid or has expired. Request a new one.' });
    const userId = rows[0].user_id;
    const hash = await bcrypt.hash(password, 10);
    await db.query('UPDATE users SET password_hash = $1 WHERE id = $2', [hash, userId]);
    await db.query('DELETE FROM password_reset_tokens WHERE user_id = $1', [userId]); // single-use
    await db.query('DELETE FROM sessions WHERE user_id = $1', [userId]); // log out everywhere
    const { rows: u } = await db.query('SELECT email, device_id FROM users WHERE id = $1', [userId]);
    const sessionToken = await createSession(userId); // sign the resetter straight in
    console.log(`Password reset completed: ${u[0]?.email}`);
    res.json({ token: sessionToken, email: u[0]?.email, deviceId: u[0]?.device_id });
  } catch (e) {
    console.error('reset-password error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/auth/logout', requireAuth, async (req, res) => {
  try { await db.query('DELETE FROM sessions WHERE token = $1', [req.sessionToken]); } catch (e) {}
  res.json({ ok: true });
});

// Session restore on page load. Excludes images (large) — hub fetches those separately.
app.get('/api/auth/me', requireAuth, (req, res) => {
  res.json({ email: req.user.email, deviceId: req.user.device_id });
});

// ============================================================
// SHARED MEMBER PROFILE (users.profile JSONB)
// One record per account. Every AI feature reads it to pre-fill intakes and
// writes back factual updates. All fields optional; unknown keys and invalid
// values are dropped so callers (the pre-trial quiz + feature write-backs) can
// PATCH partial data safely. Behind auth only — never put in URLs or logs.
// ============================================================
const PROFILE_ENUMS = {
  sex: ['male', 'female'],
  bodyType: ['heavier', 'moderate', 'fit', 'very_lean'], // matches generation "condition"
  intensity: ['subtle', 'moderate', 'dramatic', 'max'],
  ageRange: ['18-24', '25-34', '35-44', '45-54', '55+'],
  goal: ['lose_fat', 'build_muscle', 'both'],
  equipment: ['none', 'minimal', 'full'], // maps to Trainer v3 equipment tiers
  weightUnit: ['lb', 'kg'],
};
const PROFILE_DIET_TAGS = [
  'none', 'vegetarian', 'vegan', 'pescatarian', 'no_dairy', 'no_gluten',
  'no_pork', 'halal', 'kosher', 'keto', 'high_protein',
];

// Coerce/validate an incoming patch into a clean object of only the fields we
// recognize. Invalid values are dropped rather than rejected, so a feature
// write-back never fails the whole request over one bad field.
function sanitizeProfilePatch(patch) {
  const out = {};
  if (!patch || typeof patch !== 'object') return out;
  for (const [k, allowed] of Object.entries(PROFILE_ENUMS)) {
    if (patch[k] != null) {
      const v = String(patch[k]);
      if (allowed.includes(v)) out[k] = v;
    }
  }
  if (patch.heightIn != null) {
    const n = Math.round(Number(patch.heightIn));
    if (Number.isFinite(n) && n >= 36 && n <= 96) out.heightIn = n; // 3'0"–8'0"
  }
  if (patch.weight != null) {
    const n = Number(patch.weight);
    if (Number.isFinite(n) && n >= 50 && n <= 1500) out.weight = Math.round(n * 10) / 10;
  }
  if (patch.diet != null) {
    const arr = Array.isArray(patch.diet) ? patch.diet : [patch.diet];
    out.diet = [...new Set(arr.map(String).filter(t => PROFILE_DIET_TAGS.includes(t)))];
  }
  if (patch.dietNote != null) out.dietNote = String(patch.dietNote).slice(0, 200).trim();
  return out;
}

async function readProfile(userId) {
  if (!db) return {};
  try {
    const { rows } = await db.query('SELECT profile FROM users WHERE id = $1', [userId]);
    const p = rows[0]?.profile;
    return (p && typeof p === 'object' && !Array.isArray(p)) ? p : {};
  } catch (e) {
    console.error('readProfile error:', e.message);
    return {};
  }
}

// Render the shared profile as a compact, labeled block to inject into feature
// prompts. ADDITIVE background only — the feature's own inputs/photos/questions
// take precedence. Returns '' when there's nothing useful, so every feature
// degrades gracefully to its current ask-the-user behavior when the profile is
// empty. Never reword a feature's existing instructions — only append this.
const PROFILE_GOAL_LABEL = { lose_fat: 'lose fat', build_muscle: 'build muscle', both: 'lose fat + build muscle (body recomposition)' };
const PROFILE_EQUIP_LABEL = { none: 'no equipment (bodyweight only)', minimal: 'minimal home kit (dumbbells / bands / kettlebell)', full: 'full gym' };
const PROFILE_DIET_LABEL = {
  vegetarian: 'vegetarian', vegan: 'vegan', pescatarian: 'pescatarian', no_dairy: 'no dairy',
  no_gluten: 'no gluten', no_pork: 'no pork', halal: 'halal', kosher: 'kosher', keto: 'keto / low-carb', high_protein: 'high protein',
};
function profileContextBlock(profile, opts = {}) {
  const p = profile || {};
  const lines = [];
  if (p.sex) lines.push(`- Sex: ${p.sex}`);
  if (p.ageRange) lines.push(`- Age range: ${p.ageRange}`);
  if (p.heightIn) { const ft = Math.floor(p.heightIn / 12), inch = p.heightIn % 12; lines.push(`- Height: ${ft}'${inch}" (${p.heightIn} in)`); }
  if (p.weight) lines.push(`- Weight: ${p.weight} ${p.weightUnit || 'lb'}`);
  if (p.goal && PROFILE_GOAL_LABEL[p.goal]) lines.push(`- Primary goal: ${PROFILE_GOAL_LABEL[p.goal]}`);
  if (p.equipment && PROFILE_EQUIP_LABEL[p.equipment]) lines.push(`- Equipment available: ${PROFILE_EQUIP_LABEL[p.equipment]}`);
  if (Array.isArray(p.diet) && p.diet.length) lines.push(`- Dietary preferences: ${p.diet.map(d => PROFILE_DIET_LABEL[d] || d).join(', ')}`);
  if (p.dietNote) lines.push(`- Dietary notes: ${String(p.dietNote).slice(0, 200)}`);
  if (!lines.length) return '';
  const header = opts.header || "MEMBER PROFILE (shared background context — the user's own inputs, photos, and this feature's own questions always take precedence):";
  return `${header}\n${lines.join('\n')}`;
}

// Merge a sanitized patch into the stored profile. Read-modify-write in JS so
// `_meta` (per-field provenance) merges safely and we don't depend on pg jsonb
// operators (pg-mem lacks `||`). `source` tags where the data came from.
async function writeProfileMerge(userId, rawPatch, source) {
  if (!db) return {};
  const patch = sanitizeProfilePatch(rawPatch);
  if (!Object.keys(patch).length) return await readProfile(userId);
  const current = await readProfile(userId);
  const meta = (current._meta && typeof current._meta === 'object') ? { ...current._meta } : {};
  const at = new Date().toISOString();
  for (const k of Object.keys(patch)) meta[k] = { source: source || 'unknown', at };
  const next = { ...current, ...patch, _meta: meta };
  await db.query('UPDATE users SET profile = $1 WHERE id = $2', [JSON.stringify(next), userId]);
  return next;
}

// ── Backfill for existing users ──
// Existing accounts (pre-quiz) have per-feature intakes but no profile. On next
// login (and lazily on first profile read) we derive the essentials from those
// rows and fill only the MISSING fields — never overwrite quiz/funnel data. All
// values pass back through sanitizeProfilePatch, so any vocab we map wrong is
// dropped rather than stored, and the feature simply asks for it later.
const BF_SEX = { man: 'male', male: 'male', woman: 'female', female: 'female' };
const BF_EQUIP = { none: 'none', min: 'minimal', minimal: 'minimal', full: 'full' };
// Trainer age chips use en-dash and slightly different buckets than the profile.
const BF_AGE = {
  '18–25': '18-24', '26–35': '25-34', '36–45': '35-44', '46–55': '45-54', '56+': '55+',
  '18-25': '18-24', '26-35': '25-34', '36-45': '35-44', '46-55': '45-54',
};
const BF_DIET = {
  vegetarian: 'vegetarian', vegan: 'vegan', pescatarian: 'pescatarian',
  halal: 'halal', kosher: 'kosher', dairy_free: 'no_dairy', keto: 'keto',
};
function bfGoal(v) {
  const s = String(v || '').toLowerCase();
  if (!s) return null;
  if (s.includes('recomp') || s === 'both') return 'both';
  if (s.includes('muscle') || s.includes('build') || s.includes('gain')) return 'build_muscle';
  if (s.includes('fat') || s.includes('lose') || s.includes('loss') || s.includes('cut')) return 'lose_fat';
  return null;
}

async function backfillProfile(userId) {
  if (!db) return;
  try {
    const current = await readProfile(userId);
    const has = k => {
      const v = current[k];
      return v != null && !(Array.isArray(v) && v.length === 0);
    };
    const patch = {};
    // Newest AI Nutritionist intake — the richest source.
    const { rows: mp } = await db.query('SELECT intake FROM meal_plans WHERE user_id = $1 ORDER BY id DESC LIMIT 1', [userId]);
    const ni = mp[0]?.intake || {};
    if (!has('sex') && BF_SEX[ni.sex]) patch.sex = BF_SEX[ni.sex];
    if (!has('heightIn') && Number(ni.height_in)) patch.heightIn = Number(ni.height_in);
    if (!has('weight') && Number(ni.weight_lb)) { patch.weight = Number(ni.weight_lb); patch.weightUnit = 'lb'; }
    if (!has('goal') && bfGoal(ni.goal)) patch.goal = bfGoal(ni.goal);
    if (!has('diet') && BF_DIET[ni.diet_style]) patch.diet = [BF_DIET[ni.diet_style]];
    // Newest AI Trainer intake — fills equipment/age and anything nutrition lacked.
    const { rows: pg } = await db.query('SELECT intake FROM programs WHERE user_id = $1 ORDER BY id DESC LIMIT 1', [userId]);
    const ti = pg[0]?.intake || {};
    if (!has('sex') && !patch.sex && BF_SEX[ti.sex_track]) patch.sex = BF_SEX[ti.sex_track];
    if (!has('equipment') && BF_EQUIP[ti.equipment]) patch.equipment = BF_EQUIP[ti.equipment];
    if (!has('ageRange') && BF_AGE[ti.age_range]) patch.ageRange = BF_AGE[ti.age_range];
    if (!has('goal') && !patch.goal && bfGoal(ti.goal)) patch.goal = bfGoal(ti.goal);
    // Latest weigh-in as a last resort for weight.
    if (!has('weight') && patch.weight == null) {
      const { rows: wl } = await db.query('SELECT weight, unit FROM weight_logs WHERE user_id = $1 ORDER BY entry_date DESC LIMIT 1', [userId]);
      if (wl[0] && Number(wl[0].weight)) { patch.weight = Number(wl[0].weight); patch.weightUnit = wl[0].unit === 'kg' ? 'kg' : 'lb'; }
    }
    if (Object.keys(patch).length) await writeProfileMerge(userId, patch, 'backfill');
  } catch (e) {
    console.error('backfillProfile error:', e.message);
  }
}

app.get('/api/profile', requireAuth, async (req, res) => {
  try {
    let profile = await readProfile(req.user.id);
    // Lazy backfill for untouched profiles (existing users who haven't taken the
    // quiz). `_meta` exists once anything has been written, so this runs at most
    // once per account.
    if (!profile._meta) { await backfillProfile(req.user.id); profile = await readProfile(req.user.id); }
    res.json({ profile });
  } catch (e) {
    console.error('get profile error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Merge-patch. Body: { profile: {…fields…}, source?: 'quiz'|'funnel'|… }.
app.patch('/api/profile', requireAuth, async (req, res) => {
  try {
    const source = String(req.body?.source || 'client').slice(0, 24);
    const patch = (req.body && typeof req.body.profile === 'object') ? req.body.profile : req.body;
    res.json({ profile: await writeProfileMerge(req.user.id, patch, source) });
  } catch (e) {
    console.error('patch profile error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ── Latest transformation (before = uploaded photo, after = generated image) ──
app.get('/api/account/transformation', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query('SELECT before_image, after_image FROM users WHERE id = $1', [req.user.id]);
    res.json({ before: rows[0]?.before_image || null, after: rows[0]?.after_image || null });
  } catch (e) {
    console.error('get transformation error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/account/transformation', requireAuth, async (req, res) => {
  const before = String(req.body?.before || '');
  const after = String(req.body?.after || '');
  if (!before.startsWith('data:image/') || !after.startsWith('data:image/')) {
    return res.status(400).json({ error: 'Invalid image data' });
  }
  try {
    await db.query('UPDATE users SET before_image = $1, after_image = $2 WHERE id = $3', [before, after, req.user.id]);
    // Also record it in the gallery (dedupes internally — this endpoint fires
    // on every login/hub load with the same localStorage pair).
    await insertTransformation(req.user.id, before, after, {});
    res.json({ ok: true });
  } catch (e) {
    console.error('save transformation error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ── My Transformations gallery ──
// Every generated before/after pair, newest-first. The is_hero row is the pair
// shown on the member-hub home screen (mirrored into users.before/after_image
// so legacy readers — renderHubHero fallback, trainer photo path — stay in sync).
const TRANSFORMATIONS_CAP = 30;

// Insert a pair as the new hero. Skips (dedupe) when the newest row already has
// the identical after image. Returns the new row id, or null when deduped.
async function insertTransformation(userId, before, after, settings) {
  const { rows: newest } = await db.query(
    'SELECT id, after_image FROM transformations WHERE user_id = $1 ORDER BY id DESC LIMIT 1',
    [userId]
  );
  if (newest.length && newest[0].after_image === after) return null;
  await db.query('UPDATE transformations SET is_hero = false WHERE user_id = $1 AND is_hero = true', [userId]);
  const { rows } = await db.query(
    `INSERT INTO transformations (user_id, before_image, after_image, settings, is_hero)
     VALUES ($1, $2, $3, $4, true) RETURNING id`,
    [userId, before, after, JSON.stringify(settings || {})]
  );
  // Cap the gallery: drop the oldest rows past the newest 30 (the hero is the
  // newest row here, so it's never in the delete set).
  const { rows: keep } = await db.query(
    'SELECT id FROM transformations WHERE user_id = $1 ORDER BY id DESC LIMIT $2',
    [userId, TRANSFORMATIONS_CAP]
  );
  if (keep.length >= TRANSFORMATIONS_CAP) {
    const minId = keep[keep.length - 1].id;
    await db.query('DELETE FROM transformations WHERE user_id = $1 AND id < $2', [userId, minId]);
  }
  return rows[0].id;
}

app.get('/api/transformations', requireAuth, async (req, res) => {
  const PAGE = 10;
  const before = parseInt(req.query.before, 10) || 0;
  try {
    // Lazy migration: users who saved a pair before the gallery existed get it
    // as their first (hero) row on first open.
    const { rows: countRows } = await db.query(
      'SELECT COUNT(*)::int AS n FROM transformations WHERE user_id = $1', [req.user.id]
    );
    if (!countRows[0].n) {
      const u = await getUserRow(req.user.id);
      if (u?.before_image && u?.after_image) {
        await db.query(
          `INSERT INTO transformations (user_id, before_image, after_image, settings, is_hero)
           VALUES ($1, $2, $3, $4, true)`,
          [req.user.id, u.before_image, u.after_image, JSON.stringify({ migrated: true })]
        );
      }
    }
    const params = [req.user.id];
    let where = 'user_id = $1';
    if (before > 0) { params.push(before); where += ' AND id < $2'; }
    const { rows } = await db.query(
      `SELECT id, before_image, after_image, settings, is_hero, created_at
       FROM transformations WHERE ${where} ORDER BY id DESC LIMIT ${PAGE + 1}`,
      params
    );
    res.json({ transformations: rows.slice(0, PAGE), hasMore: rows.length > PAGE });
  } catch (e) {
    console.error('list transformations error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/transformations', requireAuth, async (req, res) => {
  const before = String(req.body?.before || '');
  const after = String(req.body?.after || '');
  const settings = (req.body?.settings && typeof req.body.settings === 'object') ? req.body.settings : {};
  if (!before.startsWith('data:image/') || !after.startsWith('data:image/')) {
    return res.status(400).json({ error: 'Invalid image data' });
  }
  try {
    const id = await insertTransformation(req.user.id, before, after, settings);
    // Mirror to the legacy columns (latest generation is the hub hero).
    if (id) {
      await db.query('UPDATE users SET before_image = $1, after_image = $2 WHERE id = $3', [before, after, req.user.id]);
    }
    res.json({ id, deduped: !id });
  } catch (e) {
    console.error('create transformation error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/transformations/:id/hero', requireAuth, async (req, res) => {
  const id = parseInt(req.params.id, 10) || 0;
  try {
    const { rows } = await db.query(
      'SELECT id, before_image, after_image FROM transformations WHERE id = $1 AND user_id = $2', [id, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Not found' });
    await db.query('UPDATE transformations SET is_hero = false WHERE user_id = $1 AND is_hero = true', [req.user.id]);
    await db.query('UPDATE transformations SET is_hero = true WHERE id = $1', [id]);
    await db.query('UPDATE users SET before_image = $1, after_image = $2 WHERE id = $3',
      [rows[0].before_image, rows[0].after_image, req.user.id]);
    res.json({ ok: true });
  } catch (e) {
    console.error('set hero error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.delete('/api/transformations/:id', requireAuth, async (req, res) => {
  const id = parseInt(req.params.id, 10) || 0;
  try {
    const { rows } = await db.query(
      'SELECT is_hero FROM transformations WHERE id = $1 AND user_id = $2', [id, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Not found' });
    const wasHero = rows[0].is_hero;
    await db.query('DELETE FROM transformations WHERE id = $1 AND user_id = $2', [id, req.user.id]);
    if (wasHero) {
      // Promote the newest remaining pair to hero; empty gallery empties the hub hero.
      const { rows: next } = await db.query(
        'SELECT id, before_image, after_image FROM transformations WHERE user_id = $1 ORDER BY id DESC LIMIT 1',
        [req.user.id]
      );
      if (next.length) {
        await db.query('UPDATE transformations SET is_hero = true WHERE id = $1', [next[0].id]);
        await db.query('UPDATE users SET before_image = $1, after_image = $2 WHERE id = $3',
          [next[0].before_image, next[0].after_image, req.user.id]);
      } else {
        await db.query('UPDATE users SET before_image = NULL, after_image = NULL WHERE id = $1', [req.user.id]);
      }
    }
    res.json({ ok: true });
  } catch (e) {
    console.error('delete transformation error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ── Meal sync ──
app.get('/api/meals', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT id, date, logged_at, meal_name, totals, items FROM meals WHERE user_id = $1 ORDER BY logged_at ASC LIMIT 2000',
      [req.user.id]
    );
    res.json({ meals: rows });
  } catch (e) {
    console.error('get meals error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/meals', requireAuth, async (req, res) => {
  const m = req.body || {};
  if (!m.date || !m.totals) return res.status(400).json({ error: 'Missing meal data' });
  try {
    const { rows } = await db.query(
      `INSERT INTO meals (user_id, date, logged_at, meal_name, totals, items)
       VALUES ($1, $2, COALESCE($3, now()), $4, $5, $6) RETURNING id`,
      [req.user.id, String(m.date), m.loggedAt || null, String(m.mealName || ''),
       JSON.stringify(m.totals), JSON.stringify(m.items || [])]
    );
    res.json({ id: rows[0].id });
  } catch (e) {
    console.error('save meal error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.delete('/api/meals/:id', requireAuth, async (req, res) => {
  try {
    await db.query('DELETE FROM meals WHERE id = $1 AND user_id = $2', [parseInt(req.params.id, 10) || 0, req.user.id]);
    res.json({ ok: true });
  } catch (e) {
    console.error('delete meal error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// MEAL PREP: saved batch recipes (mirrors the /api/meals trio)
// ============================================================
app.get('/api/saved-preps', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT id, name, servings, remaining, per_serving, batch_totals, created_at FROM saved_preps WHERE user_id = $1 ORDER BY created_at ASC',
      [req.user.id]
    );
    res.json({ preps: rows });
  } catch (e) {
    console.error('get saved-preps error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/saved-preps', requireAuth, async (req, res) => {
  const p = req.body || {};
  if (!p.name || !p.perServing || !p.servings) return res.status(400).json({ error: 'Missing meal prep data' });
  try {
    const servings = parseInt(p.servings, 10) || 1;
    const remaining = Number.isFinite(parseInt(p.remaining, 10)) ? parseInt(p.remaining, 10) : servings;
    const { rows } = await db.query(
      `INSERT INTO saved_preps (user_id, name, servings, remaining, per_serving, batch_totals)
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING id`,
      [req.user.id, String(p.name), servings, remaining, JSON.stringify(p.perServing), JSON.stringify(p.batchTotals || null)]
    );
    res.json({ id: rows[0].id });
  } catch (e) {
    console.error('save prep error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.put('/api/saved-preps/:id', requireAuth, async (req, res) => {
  try {
    const remaining = parseInt(req.body?.remaining, 10);
    if (!Number.isFinite(remaining)) return res.status(400).json({ error: 'Missing remaining' });
    await db.query('UPDATE saved_preps SET remaining = $1 WHERE id = $2 AND user_id = $3', [remaining, parseInt(req.params.id, 10) || 0, req.user.id]);
    res.json({ ok: true });
  } catch (e) {
    console.error('update prep error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.delete('/api/saved-preps/:id', requireAuth, async (req, res) => {
  try {
    await db.query('DELETE FROM saved_preps WHERE id = $1 AND user_id = $2', [parseInt(req.params.id, 10) || 0, req.user.id]);
    res.json({ ok: true });
  } catch (e) {
    console.error('delete prep error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// MEMBERSHIP — single subscription that unlocks everything
// ============================================================
// Member state lives on the user record (membership_* columns), kept in sync
// by the Stripe webhook. Credits convert at $1 each (as a one-time coupon on
// the subscription checkout) so early credit buyers aren't punished.

// Like requireAuth but never 401s — attaches req.user when a valid token is
// present, otherwise continues anonymously.
async function optionalAuth(req, res, next) {
  const token = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
  if (!token || !db) return next();
  try {
    const { rows } = await db.query(
      `SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id
       WHERE s.token = $1 AND s.expires_at > now()`,
      [token]
    );
    if (rows.length) req.user = rows[0];
  } catch (e) { /* anonymous on any error */ }
  next();
}

function isActiveMembership(userRow) {
  if (!userRow) return false;
  if (ADMIN_EMAILS.includes(String(userRow.email || '').toLowerCase())) return true;
  const status = userRow.membership_status;
  // Comp = permanent free beta account (admin-granted). No expiry, no Stripe.
  if (status === 'comp') return true;
  if (status === 'active' || status === 'trialing') return true;
  // Canceled-but-paid-through: honor until the period actually ends.
  const end = userRow.membership_period_end;
  return !!(end && new Date(end) > new Date());
}

async function getUserRow(userId) {
  const { rows } = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
  return rows[0] || null;
}

// Credit → membership conversion: only EXPLICIT balances convert (devices that
// bought a pack, or spent from their free allotment, have an entry; untouched
// free devices don't). Capped so the first invoice is never fully zeroed.
function creditDiscountCents(deviceId, plan) {
  const bal = creditsStore.balances[deviceId];
  if (typeof bal !== 'number' || bal <= 0) return 0;
  const planDef = MEMBERSHIP_PLANS[plan] || MEMBERSHIP_PLANS.monthly;
  return Math.min(bal * 100, planDef.priceInCents - 100);
}

// Current membership state + what the user's credits are worth at subscribe time.
app.get('/api/membership', requireAuth, async (req, res) => {
  try {
    const row = await getUserRow(req.user.id);
    const deviceId = String(req.query.deviceId || row.device_id || '');
    res.json({
      active: isActiveMembership(row),
      status: row.membership_status || null,
      plan: row.membership_plan || null,
      periodEnd: row.membership_period_end || null,
      creditDiscountCents: isActiveMembership(row) ? 0 : creditDiscountCents(deviceId, 'monthly'),
      plans: Object.fromEntries(Object.entries(MEMBERSHIP_PLANS).map(([k, v]) => [k, { priceInCents: v.priceInCents, interval: v.interval }])),
    });
  } catch (e) {
    console.error('membership error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create an embedded Stripe Checkout session for a membership subscription.
app.post('/api/stripe/create-membership-checkout', requireAuth, async (req, res) => {
  try {
    const stripe = getStripe();
    if (!stripe) return res.status(503).json({ error: 'Payments are not configured yet.' });
    const { plan, deviceId } = req.body || {};
    const planDef = MEMBERSHIP_PLANS[plan];
    if (!planDef) return res.status(400).json({ error: 'Invalid plan' });

    const row = await getUserRow(req.user.id);
    // A beta (comp) tester may still choose to pay; the webhook then overwrites
    // comp with a real subscription (paying wins). Comp rows have no
    // stripe_subscription_id, so isFirstSubscription stays true → 7-day trial.
    if (isActiveMembership(row) && row.membership_status !== 'comp') {
      return res.status(400).json({ error: 'You already have an active membership.' });
    }

    const dev = String(deviceId || row.device_id || '');
    const discountCents = creditDiscountCents(dev, plan);
    const discounts = [];
    if (discountCents > 0) {
      const coupon = await stripe.coupons.create({
        amount_off: discountCents,
        currency: 'usd',
        duration: 'once',
        name: `Credit conversion (${Math.round(discountCents / 100)} credits)`,
      });
      discounts.push({ coupon: coupon.id });
    }

    // One trial per user: brand-new subscribers get 7 free days; a returning
    // member who previously subscribed (row has a prior subscription id) pays
    // immediately. The credit-conversion coupon is duration:'once', so with a
    // trial it discounts the first real invoice after the trial ends.
    const isFirstSubscription = !row.stripe_subscription_id;

    const session = await stripe.checkout.sessions.create({
      ui_mode: 'embedded',
      mode: 'subscription',
      redirect_on_completion: 'never',
      customer_email: req.user.email,
      // Require a card up front even during the trial, and keep it explicit so
      // a future change can't silently make collection optional.
      payment_method_collection: 'always',
      ...(isFirstSubscription ? { subscription_data: { trial_period_days: 7 } } : {}),
      line_items: [{
        quantity: 1,
        price_data: {
          currency: 'usd',
          unit_amount: planDef.priceInCents,
          recurring: { interval: planDef.interval },
          product_data: {
            name: `Abs By AI ${planDef.label}`,
            description: '7-day free trial, then full access: AI trainer, unlimited transformations & meal tracking. Cancel anytime.',
          },
        },
      }],
      ...(discounts.length ? { discounts } : {}),
      metadata: {
        kind: 'membership',
        plan,
        userId: String(req.user.id),
        deviceId: dev,
        creditDiscountCents: String(discountCents),
      },
    });

    res.json({ clientSecret: session.client_secret, sessionId: session.id, discountCents });
  } catch (err) {
    console.error('create-membership-checkout error:', err.message);
    res.status(500).json({ error: 'Could not start checkout. Please try again.' });
  }
});

// Create a Stripe billing portal session to manage subscription.
app.post('/api/stripe/create-portal-session', requireAuth, async (req, res) => {
  try {
    const stripe = getStripe();
    if (!stripe) return res.status(503).json({ error: 'Payments are not configured yet.' });

    const row = await getUserRow(req.user.id);
    if (!row.stripe_customer_id) return res.status(400).json({ error: 'No customer ID found. Subscribe first.' });

    const session = await stripe.billingPortal.sessions.create({
      customer: row.stripe_customer_id,
      return_url: SITE_URL,
    });

    res.json({ url: session.url });
  } catch (err) {
    console.error('create-portal-session error:', err.message);
    res.status(500).json({ error: 'Could not open billing portal. Please try again.' });
  }
});

// ============================================================
// ADMIN — free beta accounts (see HANDOFF_beta_admin_panel.md)
// A beta account is a normal user row with membership_status='comp',
// membership_plan='beta', membership_period_end=NULL. Permanent by design.
// Every route below is gated by authLimiter + requireAdmin.
// ============================================================
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin.html'));
});

// Create or grant a beta account.
app.post('/api/admin/beta-members', authLimiter, requireAdmin, async (req, res) => {
  if (!db) return dbUnavailable(res);
  const email = String(req.body?.email || '').trim().toLowerCase();
  if (!EMAIL_RE.test(email) || email.length > 254) return res.status(400).json({ error: 'Invalid email' });
  const suppliedPassword = String(req.body?.password || '');
  if (suppliedPassword && suppliedPassword.length < 8) {
    return res.status(400).json({ error: 'Password must be at least 8 characters' });
  }
  try {
    const { rows: existing } = await db.query(
      'SELECT id, membership_status FROM users WHERE email = $1', [email]
    );
    if (existing.length) {
      const cur = existing[0].membership_status;
      // Never overwrite a real paying subscription with a comp.
      if (cur === 'active' || cur === 'trialing') {
        return res.status(409).json({ error: 'That account has a paid membership; not overwriting.' });
      }
      // Also sever any prior Stripe linkage: syncSubscriptionState keys off
      // stripe_subscription_id, so a leftover id from a past (canceled)
      // subscription could let a trailing webhook overwrite this comp grant.
      // A comp account should have no Stripe linkage, same as a fresh one.
      await db.query(
        `UPDATE users SET membership_status='comp', membership_plan='beta', membership_period_end=NULL,
         stripe_subscription_id=NULL, stripe_customer_id=NULL WHERE email=$1`,
        [email]
      );
      console.log(`Beta access granted to existing account: ${email}`);
      return res.json({ created: false, email });
    }

    // New user — create like signup does, then set the comp fields.
    let tempPassword = suppliedPassword;
    if (!tempPassword) tempPassword = crypto.randomBytes(9).toString('base64url');
    const hash = await bcrypt.hash(tempPassword, 10);
    const deviceId = 'beta-' + crypto.randomBytes(6).toString('hex');
    // ON CONFLICT guards the SELECT→INSERT race (a concurrent signup/create for
    // the same email): a lost race returns nothing → 409, not a raw 500.
    const { rows: inserted } = await db.query(
      `INSERT INTO users (email, password_hash, device_id, membership_status, membership_plan, membership_period_end)
       VALUES ($1, $2, $3, 'comp', 'beta', NULL)
       ON CONFLICT (email) DO NOTHING RETURNING id`,
      [email, hash, deviceId]
    );
    if (!inserted.length) {
      return res.status(409).json({ error: 'An account with that email already exists.' });
    }
    // Deliberately NOT pushed to MailerLite — testers didn't opt in.
    console.log(`Beta account created: ${email}`); // never log passwords
    // Return the temp password ONCE only when we generated it.
    const payload = { created: true, email };
    if (!suppliedPassword) payload.tempPassword = tempPassword;
    return res.json(payload);
  } catch (e) {
    console.error('admin create beta-member error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// List current beta accounts.
app.get('/api/admin/beta-members', authLimiter, requireAdmin, async (req, res) => {
  if (!db) return dbUnavailable(res);
  try {
    const { rows } = await db.query(
      `SELECT email, created_at FROM users WHERE membership_status='comp' ORDER BY created_at DESC`
    );
    res.json({ members: rows });
  } catch (e) {
    console.error('admin list beta-members error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Revoke a beta account. The status guard means this can never cancel a real
// subscription — it only matches rows that are currently comp.
app.delete('/api/admin/beta-members/:email', authLimiter, requireAdmin, async (req, res) => {
  if (!db) return dbUnavailable(res);
  const email = String(req.params.email || '').trim().toLowerCase();
  try {
    const { rowCount } = await db.query(
      `UPDATE users SET membership_status=NULL, membership_plan=NULL, membership_period_end=NULL
       WHERE email=$1 AND membership_status='comp'`,
      [email]
    );
    if (!rowCount) return res.status(404).json({ error: 'No beta account with that email.' });
    console.log(`Beta access revoked: ${email}`);
    res.json({ revoked: true, email });
  } catch (e) {
    console.error('admin revoke beta-member error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Idempotently activate membership for a completed subscription checkout.
async function fulfillMembershipSession(session) {
  if (!session || !db) return false;
  const sid = session.id;
  if (creditsStore.fulfilled[`member_${sid}`]) return false;
  const meta = session.metadata || {};
  if (meta.kind !== 'membership' || !meta.userId) return false;
  // Subscription checkouts report payment_status 'paid' (or 'no_payment_required'
  // when a coupon covers the first invoice).
  if (session.payment_status !== 'paid' && session.payment_status !== 'no_payment_required') return false;

  const stripe = getStripe();
  let periodEnd = null;
  let subId = session.subscription || null;
  // With a 7-day trial the real subscription status is 'trialing', not 'active',
  // and its period end is the trial end — which the reminder sweep relies on.
  // Read the actual status/period from Stripe instead of hard-coding 'active'.
  let subStatus = 'active';
  try {
    if (stripe && typeof subId === 'string') {
      const sub = await stripe.subscriptions.retrieve(subId);
      if (sub.status) subStatus = sub.status;
      const endTs = sub.current_period_end || sub.trial_end;
      if (endTs) periodEnd = new Date(endTs * 1000).toISOString();
    }
  } catch (e) { console.warn('subscription retrieve failed:', e.message); }

  await db.query(
    `UPDATE users SET stripe_customer_id = $1, stripe_subscription_id = $2,
       membership_status = $3, membership_plan = $4, membership_period_end = $5
     WHERE id = $6`,
    [session.customer || null, subId, subStatus, meta.plan || 'monthly', periodEnd, parseInt(meta.userId, 10)]
  );

  // Converted credits were spent as the checkout discount — zero the balance.
  if (parseInt(meta.creditDiscountCents, 10) > 0 && meta.deviceId) {
    creditsStore.balances[meta.deviceId] = 0;
  }
  creditsStore.fulfilled[`member_${sid}`] = true;
  await persistCreditsStore();
  console.log(`Membership activated for user ${meta.userId} (${meta.plan}, session ${sid})`);
  return true;
}

// Keep users.membership_* in sync with subscription lifecycle events.
async function syncSubscriptionState(sub) {
  if (!db || !sub?.id) return;
  const periodEnd = sub.current_period_end ? new Date(sub.current_period_end * 1000).toISOString() : null;
  await db.query(
    `UPDATE users SET membership_status = $1, membership_period_end = $2 WHERE stripe_subscription_id = $3`,
    [sub.status || 'canceled', periodEnd, sub.id]
  );
}

// Trial-ending reminder sweep. Dan wants the email exactly 2 days out, so we
// drive it ourselves rather than off Stripe's trial_will_end event (which fires
// at 3 days). Idempotent by construction: a user is picked only while trialing,
// with a period end inside the next 48h, and no reminder yet recorded. The flag
// is set only after a real send, so an unset RESEND_API_KEY simply defers the
// email until the key exists. Safe to run often; hourly is plenty.
async function trialReminderSweep() {
  if (!db) return;
  try {
    const { rows } = await db.query(
      `SELECT id, email, membership_plan FROM users
        WHERE membership_status = 'trialing'
          AND trial_reminder_sent_at IS NULL
          AND membership_period_end IS NOT NULL
          AND membership_period_end > now()
          AND membership_period_end <= now() + interval '48 hours'`
    );
    for (const u of rows) {
      if (!u.email) continue;
      const sent = await sendTrialEndingEmail(u.email, u.membership_plan || 'monthly');
      if (sent) {
        await db.query('UPDATE users SET trial_reminder_sent_at = now() WHERE id = $1', [u.id]);
        console.log(`Trial-ending reminder sent to user ${u.id}`);
      }
    }
  } catch (e) { console.warn('trialReminderSweep error:', e.message); }
}

// ============================================================
// AI TRAINER — intake → personalized 4-week program
// ============================================================
// Claude selects and sequences ONLY from the exercise whitelist (exercises.js),
// filtered to the user's equipment. Structured JSON output (same approach as
// /api/analyze-meal); invalid exercise ids are swapped server-side, never shown.

const PROGRAM_EXERCISE_ITEM = {
  type: 'object',
  additionalProperties: false,
  required: ['exercise_id', 'sets', 'reps', 'rest_sec', 'cue', 'common_mistake'],
  properties: {
    exercise_id: { type: 'string', description: 'Must be an id from the provided exercise list.' },
    sets: { type: 'integer' },
    reps: { type: 'string', description: 'e.g. "8-10", "12", "30 sec"' },
    rest_sec: { type: 'integer' },
    cue: { type: 'string', description: 'One-line personalized form cue.' },
    common_mistake: { type: 'string', description: 'One-line most common mistake to avoid.' },
  },
};

// One training day. Shared by the full-program schema and the per-week schema
// (the trainer now generates one week at a time for reliability).
const PROGRAM_DAY_ITEM = {
  type: 'object',
  additionalProperties: false,
  required: ['day', 'focus', 'warmup', 'main', 'abs_finisher'],
  properties: {
    day: { type: 'integer' },
    focus: { type: 'string', description: 'e.g. "Full body + abs", "Upper body push"' },
    warmup: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['exercise_id', 'prescription'],
        properties: {
          exercise_id: { type: 'string' },
          prescription: { type: 'string', description: 'e.g. "60 sec", "10 each side"' },
        },
      },
    },
    main: { type: 'array', items: PROGRAM_EXERCISE_ITEM },
    abs_finisher: { type: 'array', items: PROGRAM_EXERCISE_ITEM },
  },
};

const PROGRAM_WEEK_ITEM = {
  type: 'object',
  additionalProperties: false,
  required: ['week', 'theme', 'days'],
  properties: {
    week: { type: 'integer' },
    theme: { type: 'string', description: 'Short label, e.g. "Foundation", "Build", "Push", "Peak".' },
    days: { type: 'array', items: PROGRAM_DAY_ITEM },
  },
};

const PROGRAM_ASSESSMENT = {
  type: 'object',
  additionalProperties: false,
  required: ['starting_point', 'goal_summary', 'assigned_level', 'starting_stage'],
  properties: {
    starting_point: { type: 'string', description: "2-3 encouraging, never judgmental sentences on what the before photo shows: rough body-fat range, muscle base, apparent fitness level. If no photo was provided, base it on their answers." },
    goal_summary: { type: 'string', description: "1-2 sentences on the gap between the before and after photos: how much muscle to gain and fat to lose. If no photos, base it on their stated goal." },
    assigned_level: { type: 'string', enum: ['beginner', 'intermediate', 'advanced'], description: 'The MORE CONSERVATIVE of the photo assessment and their stated experience.' },
    starting_stage: { type: 'integer', description: 'Stage 1-7 from the ladder (the block prompt pins it — echo the pinned stage here).' },
  },
};

const PROGRAM_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['why_this_works', 'assessment', 'weeks'],
  properties: {
    why_this_works: { type: 'string', description: "Personalized paragraph referencing the user's photos (starting point → goal), health goals, and injuries — why THIS program works for THEM." },
    assessment: PROGRAM_ASSESSMENT,
    weeks: { type: 'array', items: PROGRAM_WEEK_ITEM },
  },
};

// Fast first call: JUST the assessment + why-this-works (reads the photos,
// picks the stage). Small + quick, so the endpoint returns almost immediately;
// the deterministic weeks it seeds are then upgraded to AI in the background.
const ASSESSMENT_ONLY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['why_this_works', 'assessment'],
  properties: {
    why_this_works: { type: 'string', description: "Personalized paragraph referencing the user's photos (starting point → goal), health goals, and injuries — why THIS program works for THEM." },
    assessment: PROGRAM_ASSESSMENT,
  },
};

const WEEK_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['week'],
  properties: { week: PROGRAM_WEEK_ITEM },
};

const TRAINER_SYSTEM_PROMPT = `You are an expert personal trainer designing a 4-week program for a fitness app called Abs By AI. Users have generated an AI image of their future physique — your program is the path from their before photo to that after photo. Everyone trains DAILY (7 days/week), TOTAL-BODY every session, and every workout ends with an abs finisher — it's Abs By AI.

Photo assessment (when photos are provided):
- The BEFORE photo shows their starting point: estimate a rough body-fat range, muscle base, and apparent fitness level.
- The AFTER photo is an AI-generated image of their goal physique: judge how much muscle to gain and fat to lose.
- Derive the training goal from the GAP between the two photos. Be encouraging and factual — NEVER judgmental about their current body.
- assessment.assigned_level: combine the photo assessment with their stated experience — the MORE CONSERVATIVE of the two wins (photo looks fit but they say beginner → beginner).
- If no photos were provided, base the assessment on their answers (goal + body type).

The 7-STAGE ladder (everyone climbs to Stage 7 over time; the block prompt PINS which stage this block is — build all 4 weeks to it and echo it as assessment.starting_stage):
| Stage | Total | Cardio | Lifting | Load method | Equipment | Functional |
| 1 | 5 min | — | 5 min bodyweight circuit | TIMED (30s work / 30s rest) | none (home) | no |
| 2 | 10 min | — | 10 min circuit | TIMED (30s work / 20s rest) | minimal kit (home) | no |
| 3 | 20 min | — | 20 min circuit | TIMED (40s work / 20s rest, 3 rounds) | minimal kit — final home stage | no |
| 4 | 20 min | 5 min | 15 min | SETS & REPS | full (first gym stage) | no |
| 5 | 30 min | 5 min | 25 min | sets & reps | full | YES |
| 6 | 45 min | 10 min | 35 min | sets & reps | full | yes |
| 7 | 60 min | 15 min | 45 min | sets & reps | full | yes |
- Stages 1–3 are HOME stages (bodyweight → minimal kit → minimal kit, longer) with NO cardio block — the fast circuit is the conditioning. Stage 4 is the FIRST gym stage.
- TIMED vs REPS: Stages 1–3 are timed circuits — write reps as the work interval (e.g. "30 sec") and rest_sec as the rest interval. Stages 4–7 are sets × reps.
- CARDIO (Stages 4+ only): the app renders a separate zone-2 cardio block (member picks treadmill/bike/rower/incline walk) BEFORE the lifting. Do NOT put cardio machines in the exercise list — just build the lifting portion to the "Lifting" minutes above.

Two tracks — the block prompt tells you the SEX TRACK and (Stage 4+) the EQUIPMENT TRACK:
- SEX TRACK — both tracks are total-body (upper + lower + abs) every day; the difference is EMPHASIS, and it only really shows once time budgets open up (Stages 5–7):
  · WOMAN → emphasize LOWER BODY, SUPER-emphasize GLUTES. More lower-body than upper each session. Glute-biasing choices: sumo/wide goblet & leg press, hip thrust as a staple, walking lunges, single-leg glute bridge. At Stages 5–7 add a dedicated glute isolation move (cable-glute-kickback / hip-abduction). Upper body present but lighter.
  · MAN → emphasize UPPER BODY, SUPER-emphasize DELTS + ARMS. More upper-body than lower each session. A shoulder move most days; at Stages 5–7 add dedicated delt/arm isolation (db-lateral-raise, machine-rear-delt-fly/db-rear-delt-fly, ez-bar-curl/db-curl/db-hammer-curl, cable-tricep-pushdown/db-tricep-extension/db-kickback). Lower body present but lighter (leg press + a hamstring/glute move).
- EQUIPMENT TRACK (Stage 4+): FULL → use the full-equipment moves as primary. MINIMAL → the member declined the gym; use the minimal-kit moves (kettlebell / push-up handles / ab wheel) as primary — the provided whitelist is already filtered to what they have.

ISOLATION gating (hard rule): isolation moves (curls, triceps extensions/pushdowns/kickbacks, lateral raises, rear-delt flies, glute kickbacks, hip abduction, leg extension, calf raise) are allowed ONLY at Stages 5–7. Stages 1–4 are COMPOUND-ONLY — emphasis there comes from move SELECTION and set count, not isolation.
FUNCTIONAL moves (walking-lunge as loaded carry, sled-push, db-farmer-carry, battle-ropes) unlock only at Stages 5–7. Battle ropes are men's-track only (Stages 5–6). At Stage 7, the men's track drops non-leg functional (no battle ropes) and alternates leg-primary functional (sled / lunge / carry) with traditional leg work.

Rules:
- You may ONLY use exercises from the provided whitelist, referenced by their exact id. Never invent an exercise or id. The whitelist is already filtered to this stage's equipment — every id in it is fair game for THIS block (subject to the stage/isolation gating above).
- Build exactly 4 weeks of 7 days each — everyone trains EVERY day. Days progress in intensity gently within the week; name each week's theme.
- EVERY workout is TOTAL-BODY (upper + lower + abs whenever the time budget allows). Never program push/pull/leg or body-part splits. Daily training is sustainable because volume per muscle per day stays modest: spread weekly volume across 7 light-to-moderate days; never train a muscle to failure two days in a row.
- NO SAME EXERCISE ON TWO CONSECUTIVE DAYS from Stage 3 up — alternate movements within their bucket (e.g. leg press → walking lunge → leg press). Stages 1–2 circuits are short enough that some moves may recur.
- Rough move counts by lifting time: 5 min ≈ 4 moves (timed circuit); 10 min ≈ 6 moves; 20 min ≈ 6 moves; 15 min lift ≈ 4-5; 25 min ≈ ~7; 35 min ≈ ~9; 45 min ≈ ~10 (plus the abs finisher; warm-up is separate).
- Every day ends with an abs finisher — this is Abs By AI. Stages 1–3 fold 1 ab/core move into the circuit; Stages 4 → 2 ab moves; Stages 5–6 → 2; Stage 7 → 3.
- STRICTLY avoid exercises that load reported injured areas; prefer joint-friendly picks (knee pain → hinge and glute work over deep lunges; lower-back pain → avoid loaded spinal flexion and heavy hinging; shoulder pain → avoid overhead pressing; wrist pain → avoid loaded straight-arm plank positions). Treat free-text health notes ("doctor said no jumping", "high blood pressure") as hard constraints that can also remove movements.
- warmup: HOME STAGES 1–3 ONLY — 1-2 quick light moves (warm-up category or easy bodyweight) so it fits the short session. At Stages 4–7 the app renders a zone-2 cardio block before the lifting and THAT IS the warm-up: return warmup as an EMPTY ARRAY []. Never program a separate warm-up on top of cardio, and never include cardio machines in any list.
- Their "beyond the look" health goals (heart health, energy, mental health, sleep, longevity, confidence) shape emphasis and MUST be woven into why_this_works — e.g. heart-health goals → frame the daily movement and the zone-2 cardio around lowering cardiovascular risk.
- cue: one short personalized coaching line. common_mistake: the single most likely error for THIS user.
- why_this_works: 3-5 sentences, warm but direct, referencing their photos (when provided), their health goals, and injuries. Address them as "you".
- rest_sec 30–180 (short rests on the timed circuit stages to fit the budget).

Exercise selection rules (safety-first — these OVERRIDE everything else):
- NO barbell or dumbbell DEADLIFTS, ever. The kettlebell deadlift (kb-deadlift) and kettlebell swing (kb-swing) are the ONLY loaded floor hinges. Hamstrings otherwise come from leg-curl (full) and glute-bridge / single-leg-glute-bridge / bb-hip-thrust (both tracks).
- NO flat or incline bench press, ever. Chest is FLY-DOMINANT (cable-fly, pec-deck, db-fly). "Pushing" appears only in later stages and only via SAFER pushes — machine-chest-press, db-floor-press, and the push-up family (pushup, incline-pushup, knee-pushup, deficit-pushup). Stages 3–4 use compound pushes (machine-chest-press / push-ups); Stages 5–7 go fly-dominant with a little pressing.
- SQUAT hierarchy: primary = leg-press. Backup 1 = safety-bar-squat. Backup 2 (tertiary) = bb-back-squat. The safety-bar and barbell back squats are allowed ONLY at Stages 6–7. Below Stage 6 the squat is leg-press / db-goblet-squat / kb-goblet-squat / bw-squat only.
- NEVER program cleans, snatches, jerks, or any Olympic lift — not in cues, notes, or why_this_works either.
- Rear delts: machine-rear-delt-fly is the default; db-rear-delt-fly as the alternate. Both only at Stages 5–7.`;

// v3 seven-stage ladder. mode = timed circuit vs sets×reps; equipFloor = the
// equipment tier a stage runs on (Stage 4+ minimal-track members drop to 'min');
// cardioMin = the zone-2 block the APP renders before lifting (not the model).
const STAGES = {
  1: { minutes: 5,  cardioMin: 0,  liftMin: 5,  mode: 'timed', equipFloor: 'none', functional: false, label: '5 min/day · home' },
  2: { minutes: 10, cardioMin: 0,  liftMin: 10, mode: 'timed', equipFloor: 'min',  functional: false, label: '10 min/day · home' },
  3: { minutes: 20, cardioMin: 0,  liftMin: 20, mode: 'timed', equipFloor: 'min',  functional: false, label: '20 min/day · home' },
  4: { minutes: 20, cardioMin: 5,  liftMin: 15, mode: 'reps',  equipFloor: 'full', functional: false, label: '20 min/day · 5 min cardio + lift · gym' },
  5: { minutes: 30, cardioMin: 5,  liftMin: 25, mode: 'reps',  equipFloor: 'full', functional: true,  label: '30 min/day · 5 min cardio + lift · gym' },
  6: { minutes: 45, cardioMin: 10, liftMin: 35, mode: 'reps',  equipFloor: 'full', functional: true,  label: '45 min/day · 10 min cardio + lift · gym' },
  7: { minutes: 60, cardioMin: 15, liftMin: 45, mode: 'reps',  equipFloor: 'full', functional: true,  label: '60 min/day · 15 min cardio + lift · gym' },
};

// Stated experience CAPS the starting stage; the before photo can only pull it
// lower (conservative wins). Advanced users still cap at 5 — everyone gets a
// ramp before the 45- and 60-min peaks.
const EXPERIENCE_START_STAGE = { beginner: 3, intermediate: 4, advanced: 5 };
const MAX_START_STAGE = 5;

function clampStage(s) {
  const n = parseInt(s, 10);
  return Number.isFinite(n) ? Math.min(7, Math.max(1, n)) : 1;
}

// Workouts are labelled by weekday (Day 1 = Monday … Day 7 = Sunday). A block
// built mid-week starts on TODAY's weekday rather than making the member wait
// for Monday: week 1 runs start_dow→Sunday, every later week is a full week.
// 1 = Monday … 7 = Sunday.
function todayDow() {
  const js = new Date().getDay(); // 0 = Sunday
  return js === 0 ? 7 : js;
}

// Back-compat: pre-v3 rows stored program.phase (1-6). Read either.
function programStage(program) {
  return clampStage(program?.stage ?? program?.phase ?? 1);
}

// The equipment tier a block actually runs on. Stages 1–3 are home (none/min);
// Stage 4+ is 'full' unless the member declined the gym (minimal track).
function equipForStage(stage, equipmentTrack) {
  const floor = STAGES[clampStage(stage)]?.equipFloor || 'none';
  if (floor === 'full' && equipmentTrack === 'minimal') return 'min';
  return floor;
}

// The equipment_track is decided entering Stage 4. Seed it from intake: a full
// gym / full home gym → 'full'; anything less → 'minimal' (re-nudged to upgrade
// each promotion). Below Stage 4 there is no track yet (home stages).
function trackForStage(stage, intake, prevTrack) {
  if (clampStage(stage) < 4) return null;
  if (prevTrack === 'full' || prevTrack === 'minimal') return prevTrack;
  return intake?.equipment === 'full' ? 'full' : 'minimal';
}

// Exercises removed from selection → their replacement, for rendering OLD stored
// programs. db-rdl / db-bench-press are still resolvable in the library but never
// re-selected (v3 §5); bb-* lifts predate the whitelist. Without this map an old
// id would fall through to a generic same-category pick.
const REMOVED_EXERCISE_SWAPS = {
  'bb-bench-press': 'machine-chest-press',
  'bb-deadlift': 'kb-deadlift',
  'db-rdl': 'kb-deadlift',
  'db-bench-press': 'machine-chest-press',
};

// Replace any hallucinated/out-of-tier exercise id with its library swap (if
// allowed) or a same-category fallback from the allowed list.
function makeExerciseFix(equipment) {
  const allowed = new Set(exercisesForEquipment(equipment).map((e) => e.id));
  const allowedList = exercisesForEquipment(equipment);
  return (id, prefCat) => {
    if (allowed.has(id)) return id;
    const legacy = REMOVED_EXERCISE_SWAPS[id];
    if (legacy && allowed.has(legacy)) return legacy;
    const lib = EXERCISE_BY_ID[id];
    if (lib && allowed.has(lib.swap)) return lib.swap;
    const cat = lib?.cat || prefCat;
    const sub = allowedList.find((e) => e.cat === cat) || allowedList[0];
    return sub.id;
  };
}

function sanitizeWeek(week, equipment, fix = makeExerciseFix(equipment)) {
  for (const day of week?.days || []) {
    for (const w of day.warmup || []) {
      const fixed = fix(w.exercise_id, 'warmup');
      if (fixed !== w.exercise_id) w.exercise_id = fixed;
    }
    for (const ex of [...(day.main || []), ...(day.abs_finisher || [])]) {
      const fixed = fix(ex.exercise_id, 'abs');
      if (fixed !== ex.exercise_id) ex.exercise_id = fixed;
    }
  }
  return week;
}

function sanitizeProgram(program, equipment) {
  const fix = makeExerciseFix(equipment);
  for (const week of program.weeks || []) sanitizeWeek(week, equipment, fix);
  return program;
}

// ============================================================
//  RELIABLE GENERATION — one short call PER WEEK, retried, with a
//  deterministic (no-AI) fallback so the user ALWAYS ends up with a full,
//  valid 4-week plan even if the model/API is unavailable.
// ============================================================
const WEEK_THEMES = { 1: 'Foundation', 2: 'Build', 3: 'Push', 4: 'Peak' };

function sexTrackLine(sexTrack) {
  return sexTrack === 'man'
    ? 'SEX TRACK: MAN — emphasize upper body, super-emphasize delts + arms (see the two-track rules).'
    : sexTrack === 'woman'
      ? 'SEX TRACK: WOMAN — emphasize lower body, super-emphasize glutes (see the two-track rules).'
      : 'SEX TRACK: unspecified — infer from the before photo; keep total-body balance.';
}

// Assessment-only prompt: read the photos, pick the stage, write the reveal +
// why-this-works. No workouts — this is the small, fast call the endpoints block
// on (the deterministic weeks are built from the stage it returns).
function buildAssessmentContent(intake, { photos, pinnedStage, cap, extraLines = [] }) {
  const content = [];
  if (photos) {
    const { beforeBase64, beforeMime, afterBase64, afterMime } = photos;
    if (beforeBase64 && beforeMime) {
      content.push({ type: 'image', source: { type: 'base64', media_type: beforeMime, data: beforeBase64 } });
      content.push({ type: 'text', text: 'BEFORE photo — the user\'s current body (shared with consent). Estimate their starting point: rough body-fat range, muscle base, apparent fitness level. Never judgmental.' });
    }
    if (afterBase64 && afterMime) {
      content.push({ type: 'image', source: { type: 'base64', media_type: afterMime, data: afterBase64 } });
      content.push({ type: 'text', text: 'AFTER photo — the AI-generated image of their goal physique. The training goal is the gap between the before photo and this one.' });
    }
  }
  const stageLine = pinnedStage
    ? `The stage is PINNED to ${pinnedStage} (${STAGES[clampStage(pinnedStage)].label}) — set assessment.starting_stage to ${pinnedStage}.`
    : `ASSESS the starting stage: set assessment.starting_stage in the range 1–${cap} (stated experience caps it; the BEFORE photo can only pull it LOWER — obese / severely deconditioned / elderly / a reported severe injury → Stage 1).`;
  content.push({
    type: 'text',
    text: `User intake:\n${JSON.stringify(intake, null, 2)}\n\n${stageLine}\n` +
      `Write assessment (starting_point, goal_summary, assigned_level, starting_stage) and why_this_works (3-5 warm, direct sentences, address them as "you", weaving in their photos when provided, health goals, and injuries). Do NOT write any workouts.\n` +
      extraLines.join('\n'),
  });
  return content;
}

async function generateAssessment(intake, opts) {
  const content = buildAssessmentContent(intake, opts);
  return callTrainerModel(TRAINER_SYSTEM_PROMPT, content, ASSESSMENT_ONLY_SCHEMA, { maxTokens: 1200, attempts: 2, perAttemptMs: 35000 });
}

// Prompt for ONE week at a pinned stage. Later weeks get the prior weeks so
// progression and the no-consecutive-repeat rule hold across boundaries.
function buildWeekUserContent(intake, opts) {
  const { stage, sexTrack, equipmentTrack, equip, weekNumber, priorWeeks = [], extraLines = [] } = opts;
  const st = STAGES[clampStage(stage)];
  const allowed = exercisesForEquipment(equip);
  const list = allowed.map((e) => `${e.id} | ${e.name} | ${e.cat} | ${e.muscles} | ${e.equip}`).join('\n');
  const equipLine = stage >= 4
    ? `EQUIPMENT TRACK: ${equipmentTrack === 'minimal' ? 'MINIMAL (build from the minimal-kit moves in the whitelist)' : 'FULL (full equipment)'}.`
    : 'EQUIPMENT: home stage — the whitelist is already filtered to what they have.';
  const priorSummary = priorWeeks.length
    ? `Prior weeks already built (exercise ids per day). Do NOT open week ${weekNumber} with the same main move that closed the previous week, keep alternating within each bucket, and progress load/volume slightly:\n${JSON.stringify(priorWeeks.map((w) => ({ week: w.week, days: (w.days || []).map((d) => ({ day: d.day, main: (d.main || []).map((m) => m.exercise_id) })) })))}`
    : '';
  const stageLine = `STAGE ${stage} — ${st.label}. Load method: ${st.mode === 'timed' ? 'TIMED circuit (reps = work interval like "30 sec", rest_sec = rest interval)' : 'SETS × REPS'}. ` +
    `${st.functional ? 'Functional moves UNLOCKED.' : 'NO functional moves.'} ${stage >= 5 ? 'Isolation moves ALLOWED.' : 'COMPOUND-ONLY (no isolation).'} ` +
    `${st.cardioMin ? `The app renders the ${st.cardioMin}-min cardio block itself — do not include it.` : 'No cardio block at this home stage.'}`;
  return [{
    type: 'text',
    text: `User intake:\n${JSON.stringify(intake, null, 2)}\n\n` +
      `${stageLine}\n${sexTrackLine(sexTrack)}\n${equipLine}\n` +
      `Generate ONLY WEEK ${weekNumber}: object "week" with "week":${weekNumber}, theme "${WEEK_THEMES[weekNumber] || 'Build'}", and 7 days${weekNumber > 1 ? ', progressing from the prior weeks below' : ''}. Every day is total-body and ends with an abs finisher.\n` +
      (priorSummary ? priorSummary + '\n' : '') +
      extraLines.join('\n') + (extraLines.length ? '\n' : '') +
      `\nExercise whitelist (id | name | category | muscles | tier) — use ONLY these ids:\n${list}`,
  }];
}

// Generate ONE week via the model (short, retried call) → { week }.
async function generateOneWeek(intake, opts) {
  const content = buildWeekUserContent(intake, opts);
  // One week is short — bound each call so a stalled request falls back to the
  // deterministic week quickly instead of holding on for minutes.
  return callTrainerModel(TRAINER_SYSTEM_PROMPT, content, WEEK_SCHEMA, { maxTokens: 6000, attempts: 2, perAttemptMs: 90000 });
}

// ── Deterministic (no-AI) builder — the never-fail backbone ──
// Rule-correct programming assembled straight from the whitelist + the stage /
// sex / equipment rules, so a full valid week exists even with zero API calls.
// Powers the locked-week teasers AND the fallback when the model can't deliver.
const DET_ROLES = {
  squat: ['leg-press', 'kb-goblet-squat', 'db-goblet-squat', 'bw-squat', 'chair-squat', 'wall-sit'],
  hinge: ['kb-deadlift', 'kb-swing', 'single-leg-glute-bridge', 'glute-bridge'],
  glute: ['bb-hip-thrust', 'single-leg-glute-bridge', 'glute-bridge', 'step-up'],
  gluteIso: ['cable-glute-kickback', 'hip-abduction'],
  lunge: ['walking-lunge', 'reverse-lunge', 'split-squat'],
  pushC: ['machine-chest-press', 'deficit-pushup', 'pushup', 'incline-pushup', 'knee-pushup'],
  pushFly: ['cable-fly', 'pec-deck', 'db-fly'],
  shoulder: ['db-shoulder-press', 'kb-press', 'pike-pushup'],
  shoulderIso: ['db-lateral-raise', 'machine-rear-delt-fly', 'db-rear-delt-fly'],
  pull: ['lat-pulldown', 'seated-cable-row', 'machine-row', 'kb-row', 'towel-row', 'table-row'],
  bicepsIso: ['ez-bar-curl', 'db-curl', 'db-hammer-curl'],
  tricepsIso: ['cable-tricep-pushdown', 'db-tricep-extension', 'db-kickback', 'chair-dip'],
  calf: ['calf-raise'],
  func: ['sled-push', 'walking-lunge', 'db-farmer-carry', 'battle-ropes'],
  abs: ['plank', 'dead-bug', 'bicycle-crunch', 'lying-leg-raise', 'hollow-hold', 'reverse-crunch', 'side-plank', 'hanging-knee-raise', 'ab-wheel-rollout', 'cable-crunch', 'mountain-climber', 'bird-dog'],
  warmup: ['march-in-place', 'arm-circles', 'leg-swings', 'cat-cow', 'jumping-jack', 'hip-circles'],
};

function detPick(role, poolSet, dayIdx, avoid) {
  const cands = (DET_ROLES[role] || []).filter((id) => poolSet.has(id));
  if (!cands.length) return null;
  for (let i = 0; i < cands.length; i++) {
    const id = cands[(dayIdx + i) % cands.length];
    if (!avoid.has(id)) return id;
  }
  return cands[dayIdx % cands.length];
}

// Movement slots per stage & sex (women lean glute, men lean upper/arms).
function detSlots(stage, sex) {
  const w = sex !== 'man';
  switch (clampStage(stage)) {
    case 1: return { main: ['squat', 'pull', 'pushC'], abs: ['abs'] };
    case 2: return { main: ['hinge', 'squat', 'glute', 'pushC', 'pull'], abs: ['abs'] };
    case 3: return w ? { main: ['squat', 'hinge', 'lunge', 'pushC', 'pull'], abs: ['abs'] }
                     : { main: ['squat', 'pushC', 'pull', 'shoulder', 'lunge'], abs: ['abs'] };
    case 4: return w ? { main: ['squat', 'glute', 'pushC', 'pull'], abs: ['abs', 'abs'] }
                     : { main: ['squat', 'pushC', 'pull', 'shoulder'], abs: ['abs', 'abs'] };
    case 5: return w ? { main: ['squat', 'glute', 'gluteIso', 'pushFly', 'pull', 'func'], abs: ['abs'] }
                     : { main: ['squat', 'pushC', 'pull', 'shoulderIso', 'bicepsIso', 'tricepsIso'], abs: ['abs'] };
    case 6: return w ? { main: ['squat', 'glute', 'gluteIso', 'calf', 'pushFly', 'pull', 'func'], abs: ['abs', 'abs'] }
                     : { main: ['squat', 'pushC', 'pushFly', 'pull', 'shoulder', 'bicepsIso', 'tricepsIso', 'func'], abs: ['abs', 'abs'] };
    default: return w ? { main: ['squat', 'glute', 'gluteIso', 'hinge', 'pushFly', 'pull', 'calf', 'func'], abs: ['abs', 'abs', 'abs'] }
                      : { main: ['squat', 'pushC', 'pull', 'shoulder', 'shoulderIso', 'bicepsIso', 'tricepsIso', 'func'], abs: ['abs', 'abs', 'abs'] };
  }
}

function detRx(stage, role) {
  const s = clampStage(stage);
  if (s <= 3) return { sets: 1, reps: s === 3 ? '40 sec' : '30 sec', rest_sec: s === 2 ? 20 : (s === 3 ? 20 : 30) };
  if (role === 'abs') return { sets: 3, reps: '15', rest_sec: 45 };
  if (role === 'func') return { sets: 3, reps: '40 sec', rest_sec: 60 };
  if (role === 'calf') return { sets: 3, reps: '20', rest_sec: 45 };
  if (/Iso$/.test(role)) return { sets: 3, reps: '12', rest_sec: 45 };
  return { sets: s >= 6 ? 4 : 3, reps: '12', rest_sec: 60 };
}

function detDay(dayNum, dayIdx, stage, sex, poolSet, avoid) {
  const slots = detSlots(stage, sex);
  const used = new Set();
  const mk = (role) => {
    const id = detPick(role, poolSet, dayIdx, new Set([...avoid, ...used]));
    if (!id) return null;
    used.add(id);
    const lib = EXERCISE_BY_ID[id] || {};
    const rx = detRx(stage, role);
    return { exercise_id: id, sets: rx.sets, reps: rx.reps, rest_sec: rx.rest_sec, cue: 'Move with control — full range beats speed.', common_mistake: lib.mistake || 'Rushing the reps — slow down and own each rep.' };
  };
  const main = slots.main.map(mk).filter(Boolean);
  const abs = slots.abs.map(mk).filter(Boolean);
  // Stages 4+ open with the app's zone-2 cardio block — that IS the warm-up, so
  // no separate warm-up section (the client hides it too).
  const warmId = STAGES[clampStage(stage)]?.cardioMin ? null : detPick('warmup', poolSet, dayIdx, new Set());
  const warmup = warmId ? [{ exercise_id: warmId, prescription: '45 sec' }] : [];
  const focus = `Total-body — ${sex === 'man' ? 'upper + arms' : 'lower + glutes'} + abs`;
  return { day: dayNum, focus, warmup, main, abs_finisher: abs, _used: [...used] };
}

function buildDeterministicWeek(ctx, weekNumber) {
  const poolSet = new Set(exercisesForEquipment(ctx.equip).map((e) => e.id));
  const days = [];
  let prev = new Set();
  for (let d = 1; d <= 7; d++) {
    const dayIdx = (weekNumber - 1) * 7 + (d - 1);
    const day = detDay(d, dayIdx, ctx.stage, ctx.sexTrack, poolSet, clampStage(ctx.stage) >= 3 ? prev : new Set());
    prev = new Set(day._used);
    delete day._used;
    days.push(day);
  }
  return { week: weekNumber, theme: WEEK_THEMES[weekNumber] || 'Build', days, ai: false, source: 'fallback' };
}

function detAssessment(intake, stage) {
  const level = ['beginner', 'intermediate', 'advanced'].includes(intake.experience) ? intake.experience : 'beginner';
  return {
    starting_point: 'Built from your intake. As you log workouts and add progress photos, your plan sharpens to exactly what your body responds to.',
    goal_summary: 'Steady, sustainable progress toward your after photo — a little every day, seven days a week.',
    assigned_level: level,
    starting_stage: clampStage(stage),
  };
}

function detWhy(intake, stage) {
  const goals = (intake.health_goals || []).length ? ' It also supports your goals beyond the look — the daily movement builds real health, not just the mirror.' : '';
  return `This is your Stage ${clampStage(stage)} plan: total-body training every day, finishing with abs — the Abs By AI way. Volume stays sustainable so you can show up seven days a week, and it climbs as you do.${goals} Log your workouts and it keeps adapting to you.`;
}

// Build the whole initial program. Only a small, fast ASSESSMENT call blocks the
// endpoint (reads the photos, picks the stage); all four weeks are seeded from
// the deterministic builder and returned instantly, then upgraded to AI in the
// background by the client. A total model outage still yields a full valid plan.
async function buildInitialProgram({ intake, photos, pinnedStage = null, sexTrack, prevTrack = null, prevSummary = null, skipAssessment = false }) {
  const cap = Math.min(MAX_START_STAGE, EXPERIENCE_START_STAGE[intake.experience] || 3);
  let a = null;
  if (!skipAssessment) {
    try {
      a = await generateAssessment(intake, { photos, pinnedStage, cap, extraLines: prevSummary ? [prevSummary] : [] });
    } catch (e) { console.warn('assessment failed — deterministic assessment:', e.message); }
  }

  const stage = pinnedStage ? clampStage(pinnedStage) : Math.min(clampStage(a?.assessment?.starting_stage ?? cap), cap);
  const track = trackForStage(stage, intake, prevTrack);
  const equip = equipForStage(stage, track);
  const ctx = { stage, sexTrack: sexTrack || intake.sex_track || null, equip };

  const assessment = a?.assessment || detAssessment(intake, stage);
  assessment.starting_stage = stage;
  const why = a?.why_this_works || detWhy(intake, stage);
  const weeks = [];
  for (let n = 1; n <= 4; n++) weeks.push(buildDeterministicWeek(ctx, n));
  return { why_this_works: why, assessment, stage, equipment_track: track, sex_track: ctx.sexTrack, start_dow: todayDow(), weeks };
}

// Regenerate ONE week of a stored program with the model, falling back to the
// deterministic week on failure. Mutates and returns the program.
async function regenerateWeek(program, intake, weekNumber) {
  const stage = programStage(program);
  const track = program.equipment_track || null;
  const equip = equipForStage(stage, track);
  const sexTrack = program.sex_track || intake.sex_track || null;
  const priorWeeks = (program.weeks || []).slice(0, weekNumber - 1);
  let week;
  try {
    const out = await generateOneWeek(intake, {
      stage, sexTrack, equipmentTrack: track, equip, weekNumber, priorWeeks, isFirst: false,
    });
    if (!out?.week?.days?.length) throw new Error('empty week');
    week = sanitizeWeek({ ...out.week, week: weekNumber, ai: true, source: 'ai' }, equip);
  } catch (e) {
    console.warn(`week ${weekNumber} generation failed — deterministic:`, e.message);
    week = buildDeterministicWeek({ stage, sexTrack, equip }, weekNumber);
  }
  const idx = (program.weeks || []).findIndex((w) => w.week === weekNumber);
  if (idx >= 0) program.weeks[idx] = week; else (program.weeks = program.weeks || []).push(week);
  return week;
}

// Free-preview shape: why-this-works + assessment + week/day structure at a
// glance + the FIRST 3 DAYS fully unlocked. Everything else is
// visible-but-locked (focus only).
function stripProgramForPreview(program) {
  return {
    why_this_works: program.why_this_works,
    assessment: program.assessment,
    stage: program.stage ?? program.phase,
    equipment_track: program.equipment_track ?? null,
    sex_track: program.sex_track ?? null,
    locked: true,
    weeks: (program.weeks || []).map((week) => ({
      week: week.week,
      theme: week.theme,
      days: (week.days || []).map((day) => {
        if (week.week === 1 && day.day <= 3) return { ...day, locked: false };
        return { day: day.day, focus: day.focus, locked: true, exercise_count: (day.main || []).length };
      }),
    })),
  };
}

const VALID_INTAKE = {
  goal: ['lose_fat', 'build_muscle', 'abs_visible', 'general_fitness', 'recomp'],
  body_type: ['slim', 'average', 'heavier', 'athletic'],
  equipment: ['none', 'min', 'full'],
  experience: ['beginner', 'intermediate', 'advanced'],
  sex_track: ['woman', 'man'],
  health_goals: ['heart_health', 'energy', 'mental_health', 'sleep', 'longevity', 'confidence', 'look_only'],
};

// Pre-v2 intakes stored a different experience scale.
const LEGACY_EXPERIENCE = { never: 'beginner', on_and_off: 'intermediate', consistent: 'advanced' };
// v2 equipment tiers → v3 (dumbbells are 'full' equipment now, not minimal).
const LEGACY_EQUIPMENT = { db: 'full', gym: 'full' };

function validateIntake(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const exp = LEGACY_EXPERIENCE[raw.experience] || raw.experience;
  const equip = LEGACY_EQUIPMENT[raw.equipment] || raw.equipment;
  const intake = {
    equipment: VALID_INTAKE.equipment.includes(equip) ? equip : 'none',
    experience: VALID_INTAKE.experience.includes(exp) ? exp : 'beginner',
    injuries: Array.isArray(raw.injuries) ? raw.injuries.slice(0, 6).map((s) => String(s).slice(0, 40)) : [],
    injury_notes: String(raw.injury_notes || '').slice(0, 300),
    health_goals: Array.isArray(raw.health_goals)
      ? raw.health_goals.filter((g) => VALID_INTAKE.health_goals.includes(g)).slice(0, 7)
      : [],
    health_notes: String(raw.health_notes || '').slice(0, 300),
    age_range: String(raw.age_range || raw.body?.age_range || '').slice(0, 20),
  };
  // Sex track drives the emphasis (glutes vs delts+arms). Optional — the model
  // infers from the before photo when it's missing.
  if (VALID_INTAKE.sex_track.includes(raw.sex_track)) intake.sex_track = raw.sex_track;
  // No-photo fallback answers (also present on old intakes — harmless to keep).
  if (VALID_INTAKE.goal.includes(raw.goal)) intake.goal = raw.goal;
  if (VALID_INTAKE.body_type.includes(raw.body_type)) intake.body_type = raw.body_type;
  return intake;
}

// One structured-output call to Claude, hardened for reliability:
//  • a per-attempt abort deadline so a stalled request is retried, not hung
//    forever behind a proxy that will eventually kill the connection;
//  • retry-with-backoff on transient failures (network resets, 429, 5xx);
//  • 4xx (bad request) fails fast — retrying won't help.
// The trainer now calls this once PER WEEK (short calls), so no single request
// runs long enough to trip the ~4-min timeout that broke the old 28-day call.
async function callTrainerModel(systemPrompt, userContent, schema = PROGRAM_SCHEMA, opts = {}) {
  const maxTokens = opts.maxTokens || 16000;
  const attempts = opts.attempts || 3;
  const perAttemptMs = opts.perAttemptMs || 150000; // 2.5 min per try
  let lastErr;
  for (let attempt = 1; attempt <= attempts; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), perAttemptMs);
    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-6',
          max_tokens: maxTokens,
          system: systemPrompt,
          output_config: { format: { type: 'json_schema', schema } },
          messages: [{ role: 'user', content: userContent }],
        }),
        signal: controller.signal,
      });
      const data = await response.json();
      if (response.ok) return JSON.parse(data?.content?.[0]?.text || '');
      const err = new Error(data?.error?.message || 'Claude API error');
      err.status = response.status;
      // Client errors (bad request/auth) are not transient — fail immediately.
      if (response.status < 500 && response.status !== 429) throw err;
      lastErr = err;
    } catch (e) {
      if (e.status && e.status < 500 && e.status !== 429) { clearTimeout(timer); throw e; }
      lastErr = e; // AbortError / network reset / 5xx / 429 — retryable
    } finally {
      clearTimeout(timer);
    }
    if (attempt < attempts) await new Promise((r) => setTimeout(r, 1200 * attempt));
  }
  throw lastErr || new Error('Claude API error');
}

// Generate a program from intake. Free for everyone (the sunk-cost hook) —
// members get the full block back; free users get the stripped preview.
// Logged-in users get the FULL program persisted server-side, so subscribing
// later unlocks it without regenerating.
app.post('/api/generate-program', aiLimiter, optionalAuth, async (req, res) => {
  try {
    const intake = validateIntake(req.body?.intake);
    if (!intake) return res.status(400).json({ error: 'Missing intake' });
    const { photoBase64, photoMime, afterPhotoBase64, afterPhotoMime, photoConsent } = req.body || {};
    const photos = photoConsent ? {
      beforeBase64: photoBase64, beforeMime: photoMime,
      afterBase64: afterPhotoBase64, afterMime: afterPhotoMime,
    } : null;

    // Sleep Coach cross-feature rule: bad night → longer warm-up, never a
    // shorter or lighter workout. Woven into the week-1 prompt.
    const extraLines = [];
    if (req.user) {
      const sleepLine = sleepContextForTrainer(await getTodaysSleep(req.user.id));
      if (sleepLine) extraLines.push(sleepLine);
      const weightLine = await getWeightContext(req.user.id);
      if (weightLine) extraLines.push(weightLine);
    }

    // Fast + reliable: AI week 1 (with the assessment) now; weeks 2-4 come back
    // as valid deterministic weeks that the client upgrades to AI one by one.
    // Even a total model outage yields a complete, usable plan.
    const program = await buildInitialProgram({
      intake, photos, pinnedStage: null, sexTrack: intake.sex_track,
      prevSummary: extraLines.length ? extraLines.join('\n') : null,
    });

    let programId = null;
    let member = false;
    if (req.user && db) {
      member = isActiveMembership(req.user);
      try {
        const { rows } = await db.query(
          `INSERT INTO programs (user_id, block_number, intake, program) VALUES ($1, 1, $2, $3) RETURNING id`,
          [req.user.id, JSON.stringify(intake), JSON.stringify(program)]
        );
        programId = rows[0].id;
        backfillProfile(req.user.id).catch(() => {}); // fill profile gaps from this intake
      } catch (e) { console.error('program save error:', e.message); }
    }

    res.json({
      programId,
      blockNumber: 1,
      locked: !member,
      // weeksPending tells the client which weeks still need AI upgrading.
      weeksPending: program.weeks.filter((w) => !w.ai).map((w) => w.week),
      program: member ? { ...program, locked: false } : stripProgramForPreview(program),
    });
  } catch (err) {
    console.error('generate-program error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Upgrade ONE week from its deterministic placeholder to a personalized AI week.
// The client calls this for each pending week after generate-program/checkin, so
// no single request is ever long. regenerateWeek never throws (it falls back to
// the deterministic week), so the member always gets a usable week back.
app.post('/api/program/week', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'Membership required', needsMembership: true });
    }
    const weekNumber = Math.min(4, Math.max(1, parseInt(req.body?.weekNumber, 10) || 0));
    if (!weekNumber) return res.status(400).json({ error: 'Missing weekNumber' });
    const { rows } = await db.query(
      'SELECT id, intake, program FROM programs WHERE id = $1 AND user_id = $2',
      [parseInt(req.body?.programId, 10) || 0, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Program not found' });
    const row = rows[0];
    const program = row.program;
    const intake = validateIntake(row.intake) || row.intake;
    const existing = (program.weeks || []).find((w) => w.week === weekNumber);
    if (existing?.ai) {
      return res.json({ programId: row.id, weekNumber, week: existing, alreadyAI: true, weeksPending: program.weeks.filter((w) => !w.ai).map((w) => w.week) });
    }
    const week = await regenerateWeek(program, intake, weekNumber);
    await db.query('UPDATE programs SET program = $1 WHERE id = $2 AND user_id = $3',
      [JSON.stringify(program), row.id, req.user.id]);
    res.json({ programId: row.id, weekNumber, week, weeksPending: program.weeks.filter((w) => !w.ai).map((w) => w.week) });
  } catch (err) {
    console.error('program week error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Latest program for the logged-in user (full for members, preview otherwise).
app.get('/api/program', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT id, block_number, intake, program, progress FROM programs WHERE user_id = $1 ORDER BY id DESC LIMIT 1',
      [req.user.id]
    );
    if (!rows.length) return res.json({ program: null });
    const row = rows[0];
    const userRow = await getUserRow(req.user.id);
    const member = isActiveMembership(userRow);
    res.json({
      programId: row.id,
      blockNumber: row.block_number,
      intake: row.intake,
      locked: !member,
      // Which weeks still need AI upgrading — lets the client resume on reload.
      weeksPending: member ? (row.program.weeks || []).filter((w) => !w.ai).map((w) => w.week) : [],
      program: member ? { ...row.program, locked: false } : stripProgramForPreview(row.program),
      progress: row.progress || {},
    });
  } catch (e) {
    console.error('get program error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Persist set check-offs and swaps. Client sends the full progress object
// (small: keys like "w1d1m0s2" → true, swaps like "swap_w1d1m0" → exerciseId).
app.post('/api/program/progress', requireAuth, async (req, res) => {
  const { programId, progress } = req.body || {};
  if (!programId || !progress || typeof progress !== 'object') {
    return res.status(400).json({ error: 'Missing programId or progress' });
  }
  try {
    await db.query(
      'UPDATE programs SET progress = $1 WHERE id = $2 AND user_id = $3',
      [JSON.stringify(progress), parseInt(programId, 10) || 0, req.user.id]
    );
    res.json({ ok: true });
  } catch (e) {
    console.error('progress save error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Week-4 check-in → regenerate the next block using completion data. Members only.
app.post('/api/program/checkin', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'Membership required', needsMembership: true });
    }
    const { programId, feedback } = req.body || {};
    const { rows } = await db.query(
      'SELECT id, block_number, intake, program, progress FROM programs WHERE id = $1 AND user_id = $2',
      [parseInt(programId, 10) || 0, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Program not found' });
    const prev = rows[0];

    const fb = {
      difficulty: ['too_easy', 'just_right', 'too_hard'].includes(feedback?.difficulty) ? feedback.difficulty : 'just_right',
      skipped: String(feedback?.skipped || '').slice(0, 300),
      notes: String(feedback?.notes || '').slice(0, 300),
    };
    const progressVals = Object.values(prev.progress?.done || prev.progress || {});
    const completedSets = progressVals.filter((v) => v === true).length;
    // v3 progression is workout-based, not set-based: how many of the block's
    // 28 daily workouts they actually logged (progress.dates keeps one per day).
    const BLOCK_WORKOUTS = 28;
    const completedDays = Math.min(BLOCK_WORKOUTS, Object.keys(prev.progress?.dates || {}).length);
    const loggedHalf = completedDays >= BLOCK_WORKOUTS / 2;

    // Stage ladder promotion: ≥50% of workouts logged → advance one stage.
    // <50% → hold (repeat this stage a month). "Too hard" is a manual hold too.
    // Cap at Stage 7 — the shared finish line.
    const intake = validateIntake(prev.intake) || prev.intake;
    const prevStage = programStage(prev.program);
    let nextStage;
    if (fb.difficulty === 'too_hard' || !loggedHalf) nextStage = prevStage;
    else nextStage = Math.min(7, prevStage + 1);

    // Sex track carries from the stored program / intake.
    const sexTrack = prev.program?.sex_track || intake.sex_track || null;
    const held = nextStage === prevStage;

    // Sleep Coach cross-feature rule: bad night → longer warm-up, never a
    // shorter or lighter workout. Plus the "you finished a block" context.
    const extraLines = [
      held
        ? `They are REPEATING Stage ${prevStage} (logged ${completedDays}/${BLOCK_WORKOUTS} workouts${fb.difficulty === 'too_hard' ? ' and said it was too hard' : ''}) — keep the same stage but refresh the movements and make it achievable.`
        : `They EARNED a promotion to Stage ${nextStage} (logged ${completedDays}/${BLOCK_WORKOUTS} workouts) — step up volume/complexity.`,
      `Check-in feedback: difficulty was "${fb.difficulty}"${fb.skipped ? `; they tended to skip: ${fb.skipped}` : ''}${fb.notes ? `; notes: ${fb.notes}` : ''}. Adjust: too_easy → harder/more volume; too_hard → dial back; swap in fresh moves to fight boredom; drop what they skipped.`,
      `Previous block (progress it, do not repeat verbatim): ${JSON.stringify((prev.program.weeks || []).map((w) => ({ week: w.week, main: (w.days || []).flatMap((d) => (d.main || []).map((m) => m.exercise_id)) })))}`,
    ];
    const sleepLine = sleepContextForTrainer(await getTodaysSleep(req.user.id));
    if (sleepLine) extraLines.push(sleepLine);
    const weightLine = await getWeightContext(req.user.id);
    if (weightLine) extraLines.push(weightLine);

    // Fast + reliable: AI week 1 of the new block now, deterministic weeks 2-4
    // that the client upgrades. Carries the equipment track forward.
    const program = await buildInitialProgram({
      intake, photos: null, pinnedStage: nextStage, sexTrack,
      prevTrack: prev.program?.equipment_track || null,
      prevSummary: extraLines.join('\n'),
    });

    const ins = await db.query(
      `INSERT INTO programs (user_id, block_number, intake, program) VALUES ($1, $2, $3, $4) RETURNING id`,
      [req.user.id, prev.block_number + 1, JSON.stringify(intake), JSON.stringify(program)]
    );
    res.json({
      programId: ins.rows[0].id,
      blockNumber: prev.block_number + 1,
      locked: false,
      promoted: !held,
      weeksPending: program.weeks.filter((w) => !w.ai).map((w) => w.week),
      // Entering a full-equipment stage on the minimal track → the UI shows the
      // "upgrade to a gym / full home gym" nudge (stronger each promotion).
      equipmentNudge: nextStage >= 4 && program.equipment_track === 'minimal',
      program: { ...program, locked: false },
    });
  } catch (err) {
    console.error('checkin error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Set the equipment track (full vs minimal) — the Stage-4 upgrade choice. Members
// only; regenerates the current block on the chosen track so moves match.
app.post('/api/program/equipment-track', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'Membership required', needsMembership: true });
    }
    const track = req.body?.track === 'full' ? 'full' : 'minimal';
    const { rows } = await db.query(
      'SELECT id, block_number, intake, program FROM programs WHERE id = $1 AND user_id = $2',
      [parseInt(req.body?.programId, 10) || 0, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Program not found' });
    const prev = rows[0];
    const intake = validateIntake(prev.intake) || prev.intake;
    const stage = programStage(prev.program);
    // Track only applies at Stage 4+. Below that there's nothing to switch.
    if (stage < 4) return res.status(400).json({ error: 'Equipment track applies from Stage 4' });
    if (prev.program?.equipment_track === track) {
      return res.json({ programId: prev.id, blockNumber: prev.block_number, unchanged: true, program: { ...prev.program, locked: false } });
    }

    const sexTrack = prev.program?.sex_track || intake.sex_track || null;

    // Same person, same stage — only the equipment changes. Rebuild week 1 (AI)
    // + deterministic weeks 2-4 on the new track; keep the existing assessment.
    const program = await buildInitialProgram({
      intake, photos: null, pinnedStage: stage, sexTrack, prevTrack: track, skipAssessment: true,
    });
    if (prev.program?.assessment) program.assessment = prev.program.assessment;
    if (prev.program?.why_this_works) program.why_this_works = prev.program.why_this_works;

    await db.query('UPDATE programs SET program = $1, progress = $2 WHERE id = $3 AND user_id = $4',
      [JSON.stringify(program), JSON.stringify({}), prev.id, req.user.id]);
    res.json({
      programId: prev.id, blockNumber: prev.block_number, locked: false,
      weeksPending: program.weeks.filter((w) => !w.ai).map((w) => w.week),
      program: { ...program, locked: false },
    });
  } catch (err) {
    console.error('equipment-track error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
//  AI NUTRITIONIST — meal-prep plans built from the photo gap
// ============================================================

const RECIPE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['name', 'emoji', 'description', 'prep_time_min', 'servings', 'ingredients', 'steps', 'per_serving'],
  properties: {
    name: { type: 'string', description: 'Appetizing recipe name, e.g. "Honey-Chipotle Chicken Bowls"' },
    emoji: { type: 'string', description: 'One food emoji for the card' },
    description: { type: 'string', description: '1-2 sentences selling the meal — why it tastes good AND fits their goal.' },
    prep_time_min: { type: 'integer', description: 'Total Sunday prep time in minutes, including cooking.' },
    servings: { type: 'integer', description: 'Always 10 — two meals a day, Monday through Friday.' },
    ingredients: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['item', 'quantity'],
        properties: {
          item: { type: 'string' },
          quantity: { type: 'string', description: 'Total quantity to buy for all 10 servings, e.g. "5 lbs", "3 cups dry"' },
        },
      },
    },
    steps: { type: 'array', items: { type: 'string' }, description: '4-8 numbered prep steps written for a home cook.' },
    per_serving: {
      type: 'object',
      additionalProperties: false,
      required: ['calories', 'protein_g', 'carbs_g', 'fat_g'],
      properties: {
        calories: { type: 'integer' },
        protein_g: { type: 'integer' },
        carbs_g: { type: 'integer' },
        fat_g: { type: 'integer' },
      },
    },
  },
};

const MEALPLAN_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['why_this_works', 'assessment', 'targets', 'prep_recipes', 'daily_structure', 'weekend_guidance'],
  properties: {
    why_this_works: {
      type: 'string',
      description: "Personalized paragraph (3-5 sentences, address them as 'you') referencing their photos, health goals, favorite foods, and medication situation — why THIS eating plan closes the gap to their after photo.",
    },
    assessment: {
      type: 'object',
      additionalProperties: false,
      required: ['starting_point', 'goal_summary'],
      properties: {
        starting_point: { type: 'string', description: '2-3 encouraging, never judgmental sentences: rough body-fat range from the before photo and what that means for nutrition. If no photo, base it on their answers.' },
        goal_summary: { type: 'string', description: '1-2 sentences on the gap between the before and after photos in nutrition terms: roughly how much fat to lose / muscle to support.' },
      },
    },
    targets: {
      type: 'object',
      additionalProperties: false,
      required: ['daily_calories', 'protein_g', 'calories_mode', 'target_explanation'],
      properties: {
        daily_calories: { type: 'integer', description: 'The daily calorie target, chosen inside the allowed range given in the prompt.' },
        protein_g: { type: 'integer', description: 'Daily protein target in grams, close to the computed guidance.' },
        calories_mode: { type: 'string', enum: ['ceiling', 'floor'], description: 'ceiling = "eat no more than" (normal deficit). floor = "eat at least" (GLP-1 / appetite-suppressed users).' },
        target_explanation: { type: 'string', description: 'One friendly sentence explaining the number, e.g. "Your maintenance is about 2,600 — 2,050 loses roughly 1 lb a week while keeping the muscle you\'re building."' },
      },
    },
    prep_recipes: {
      type: 'array',
      description: 'Exactly 3 meal-prep recipes that ALL hit the same per-serving macros (within ~5%), so the user can rotate weeks without changing the math. Built around their favorite foods, respecting allergies/diet/dislikes as hard constraints.',
      items: RECIPE_SCHEMA,
    },
    daily_structure: {
      type: 'object',
      additionalProperties: false,
      required: ['prep_meals_per_day', 'prep_calories', 'flexible_calories', 'flexible_protein_g', 'note', 'flexible_suggestions'],
      properties: {
        prep_meals_per_day: { type: 'integer', description: 'Always 2 (lunch + dinner from the prep), Monday-Friday.' },
        prep_calories: { type: 'integer', description: 'Calories covered by the two prep meals (2 × per-serving calories).' },
        flexible_calories: { type: 'integer', description: 'daily_calories minus prep_calories: what is left for breakfast and snacks.' },
        flexible_protein_g: { type: 'integer', description: 'Protein grams still needed outside the prep meals.' },
        note: { type: 'string', description: 'One sentence spelling out the daily math in plain words.' },
        flexible_suggestions: {
          type: 'array',
          description: '3-4 easy go-to breakfasts/snacks that fit the flexible budget, respecting allergies and diet style.',
          items: {
            type: 'object',
            additionalProperties: false,
            required: ['name', 'calories', 'protein_g'],
            properties: {
              name: { type: 'string' },
              calories: { type: 'integer' },
              protein_g: { type: 'integer' },
            },
          },
        },
      },
    },
    weekend_guidance: {
      type: 'object',
      additionalProperties: false,
      required: ['calories', 'tips'],
      properties: {
        calories: { type: 'integer', description: 'Weekend daily calorie target (usually same as weekday, can be slightly higher).' },
        tips: { type: 'array', items: { type: 'string' }, description: '2-4 realistic guardrails, e.g. "One restaurant meal fits if you keep it under ~1,200 — prioritize protein first."' },
      },
    },
  },
};

const NUTRITIONIST_SYSTEM_PROMPT = `You are an expert nutritionist for a fitness app called Abs By AI. Users have generated an AI image of their future physique — your meal plan is the nutrition path from their before photo to that after photo.

Photo assessment (when photos are provided):
- The BEFORE photo shows their starting point: estimate a rough body-fat range. Be encouraging and factual — NEVER judgmental about their current body.
- The AFTER photo is an AI-generated image of their goal physique: judge how much fat to lose and how much muscle the diet must support.
- If no photos were provided, base the assessment on their stated goal and answers.

The plan model (this is fixed — never propose a different structure):
- Every Sunday the user meal-preps ONE recipe into 10 portions. They eat 2 portions per day Monday-Friday (lunch + dinner). Breakfast and snacks are flexible within a calorie/protein budget you spell out. Weekends are flexible within a calorie target plus a few guardrails.
- You produce exactly 3 prep recipes that all hit the SAME per-serving macros (within ~5%), so the user rotates between them week to week without the math changing. Variety is what keeps this diet alive in week 3.
- Each recipe: 10 servings, a complete grocery-quantity ingredient list (totals for all 10 servings), and simple numbered prep steps. Match the recipe complexity to their stated cooking effort (minimal = ~5 ingredients + a sauce; love cooking = more interesting).
- Two prep portions should cover roughly 55-70% of daily calories, and the prep should be protein-dense: the two portions together should cover most of the protein target.

Calorie and protein targets:
- The prompt gives you server-computed maintenance calories, an ALLOWED calorie range, and protein guidance. Choose daily_calories INSIDE the allowed range — pick where in the range based on the photo gap (bigger fat-loss gap → lower in the range; lean user building muscle → top of the range). NEVER go outside the range.
- protein_g should stay within ±10% of the protein guidance.
- target_explanation must state maintenance and what the chosen number does, in plain words.

GLP-1 / appetite-suppressing medication (when the intake says yes):
- The medication already creates the deficit. Their real risk is under-eating and losing muscle, not overeating.
- Set calories_mode to "floor" and daily_calories toward the BOTTOM of the allowed range as an "eat at least" number.
- Make the prep recipes extra protein-dense with smaller, easier-to-finish portions.
- Say this plainly in why_this_works: the medication handles the deficit; their job is protein and training so what they lose is fat, not muscle.
- Otherwise calories_mode is "ceiling".

Hard constraints (these override everything else):
- Food allergies are absolute — the allergen must not appear in ANY recipe, suggestion, or tip, even as a garnish or optional item.
- Diet style (vegetarian, vegan, pescatarian, halal, kosher, dairy-free) is absolute.
- Disliked foods never appear. Favorite foods should visibly anchor the recipes — a plan built on foods they love is one they'll actually eat 10 times a week.
- Free-text medication or health notes are treated as hard constraints (e.g. "kidney issues" → moderate protein; "diabetic" → steady carbs, mention checking with their doctor).
- Never claim to treat, cure, or diagnose anything. For medical conditions, add a gentle "worth confirming with your doctor" where relevant.

Tone: warm, direct, zero judgment. Their "beyond the look" health goals (energy, heart health, sleep, digestion, blood sugar) shape food choices and MUST be woven into why_this_works.`;

// ── Server-side target math (deterministic — the model chooses within these) ──
const NUTRITION_ACTIVITY_MULT = { desk: 1.35, active: 1.5, very_active: 1.7 };
const CALORIE_FLOORS = { male: 1500, female: 1200, unspecified: 1350 };

function computeNutritionTargets(intake) {
  const kg = intake.weight_lb / 2.2046;
  const cm = intake.height_in * 2.54;
  const sexTerm = intake.sex === 'male' ? 5 : intake.sex === 'female' ? -161 : -78;
  const bmr = 10 * kg + 6.25 * cm - 5 * intake.age + sexTerm;
  const mult = NUTRITION_ACTIVITY_MULT[intake.activity] || 1.4;
  const maintenance = Math.round((bmr * mult) / 10) * 10;
  const floor = CALORIE_FLOORS[intake.sex] || CALORIE_FLOORS.unspecified;
  // Allowed range: never deeper than a 25% deficit or below the floor; up to a
  // small surplus for lean users whose after photo is mostly muscle.
  const minCalories = Math.max(floor, Math.round((maintenance * 0.75) / 10) * 10);
  const maxCalories = Math.round((maintenance + 300) / 10) * 10;
  // Protein: ~0.9 g per lb of estimated GOAL body weight (Devine ideal weight
  // +20% as the ceiling so heavy users aren't told to eat 280 g).
  const ibw = intake.sex === 'female' ? 100 + 5 * (intake.height_in - 60) : 106 + 6 * (intake.height_in - 60);
  const proteinRef = Math.min(intake.weight_lb, Math.max(ibw, 90) * 1.2);
  const proteinG = Math.min(220, Math.max(90, Math.round((proteinRef * 0.9) / 5) * 5));
  return { maintenance, minCalories, maxCalories, proteinG, floor };
}

const VALID_NUTRITION_INTAKE = {
  sex: ['male', 'female', 'unspecified'],
  activity: ['desk', 'active', 'very_active'],
  glp1: ['yes', 'no', 'prefer_not'],
  cooking: ['love', 'simple', 'minimal'],
  diet_style: ['none', 'vegetarian', 'vegan', 'pescatarian', 'halal', 'kosher', 'dairy_free'],
  allergies: ['dairy', 'gluten', 'nuts', 'shellfish', 'eggs', 'soy'],
  goal: ['lose_fat', 'build_muscle', 'abs_visible', 'general_fitness', 'recomp'],
  health_goals: ['heart_health', 'energy', 'digestion', 'blood_sugar', 'sleep', 'longevity', 'look_only'],
};

function validateNutritionIntake(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const num = (v, lo, hi) => {
    const n = parseFloat(v);
    return Number.isFinite(n) && n >= lo && n <= hi ? n : null;
  };
  const age = num(raw.age, 16, 90);
  const height_in = num(raw.height_in, 48, 90);
  const weight_lb = num(raw.weight_lb, 80, 500);
  if (age == null || height_in == null || weight_lb == null) return null;
  const intake = {
    sex: VALID_NUTRITION_INTAKE.sex.includes(raw.sex) ? raw.sex : 'unspecified',
    age, height_in, weight_lb,
    activity: VALID_NUTRITION_INTAKE.activity.includes(raw.activity) ? raw.activity : 'desk',
    glp1: VALID_NUTRITION_INTAKE.glp1.includes(raw.glp1) ? raw.glp1 : 'no',
    meds_notes: String(raw.meds_notes || '').slice(0, 300),
    health_goals: Array.isArray(raw.health_goals)
      ? raw.health_goals.filter((g) => VALID_NUTRITION_INTAKE.health_goals.includes(g)).slice(0, 7)
      : [],
    fav_foods: Array.isArray(raw.fav_foods) ? raw.fav_foods.slice(0, 12).map((s) => String(s).slice(0, 40)) : [],
    food_notes: String(raw.food_notes || '').slice(0, 300),
    allergies: Array.isArray(raw.allergies)
      ? raw.allergies.filter((a) => VALID_NUTRITION_INTAKE.allergies.includes(a)).slice(0, 6)
      : [],
    diet_style: VALID_NUTRITION_INTAKE.diet_style.includes(raw.diet_style) ? raw.diet_style : 'none',
    dislikes: String(raw.dislikes || '').slice(0, 300),
    cooking: VALID_NUTRITION_INTAKE.cooking.includes(raw.cooking) ? raw.cooking : 'simple',
  };
  if (VALID_NUTRITION_INTAKE.goal.includes(raw.goal)) intake.goal = raw.goal;
  return intake;
}

function buildNutritionistUserContent(intake, photos, targets) {
  const content = [];
  const { beforeBase64, beforeMime, afterBase64, afterMime } = photos || {};
  if (beforeBase64 && beforeMime) {
    content.push({ type: 'image', source: { type: 'base64', media_type: beforeMime, data: beforeBase64 } });
    content.push({ type: 'text', text: "BEFORE photo — the user's current body (shared with consent). Estimate a rough body-fat range. Never judgmental." });
  }
  if (afterBase64 && afterMime) {
    content.push({ type: 'image', source: { type: 'base64', media_type: afterMime, data: afterBase64 } });
    content.push({ type: 'text', text: 'AFTER photo — the AI-generated image of their goal physique. The nutrition goal is the gap between the before photo and this one.' });
  }
  content.push({
    type: 'text',
    text: `User intake:\n${JSON.stringify(intake, null, 2)}\n\n` +
      `Server-computed targets (Mifflin-St Jeor × activity):\n` +
      `- Maintenance: ~${targets.maintenance} calories/day\n` +
      `- ALLOWED daily_calories range: ${targets.minCalories}–${targets.maxCalories} (never outside this)\n` +
      `- Protein guidance: ~${targets.proteinG} g/day (stay within ±10%)\n` +
      (intake.glp1 === 'yes'
        ? `- This user takes a GLP-1: calories_mode MUST be "floor" — daily_calories is an "eat at least" number near the bottom of the range, and protein is the headline of the whole plan.\n`
        : '') +
      `\nBuild the full plan: 3 rotating prep recipes (10 servings each, same macros), the daily structure, and weekend guidance.`,
  });
  return content;
}

// Clamp the model's numbers back inside the server-computed rails and make the
// daily arithmetic self-consistent no matter what the model returned.
function sanitizeMealPlan(plan, targets, intake) {
  const t = plan.targets || (plan.targets = {});
  t.maintenance_calories = targets.maintenance;
  t.daily_calories = Math.min(targets.maxCalories, Math.max(targets.minCalories, parseInt(t.daily_calories, 10) || targets.minCalories));
  t.protein_g = Math.min(Math.round(targets.proteinG * 1.15), Math.max(Math.round(targets.proteinG * 0.85), parseInt(t.protein_g, 10) || targets.proteinG));
  t.calories_mode = intake.glp1 === 'yes' ? 'floor' : 'ceiling';
  plan.prep_recipes = (plan.prep_recipes || []).slice(0, 3);
  for (const r of plan.prep_recipes) r.servings = 10;
  const ds = plan.daily_structure || (plan.daily_structure = {});
  ds.prep_meals_per_day = 2;
  const perServing = plan.prep_recipes[0]?.per_serving?.calories || Math.round(t.daily_calories * 0.3);
  ds.prep_calories = perServing * 2;
  ds.flexible_calories = Math.max(0, t.daily_calories - ds.prep_calories);
  const perServingProtein = plan.prep_recipes[0]?.per_serving?.protein_g || Math.round(t.protein_g * 0.35);
  ds.flexible_protein_g = Math.max(0, t.protein_g - perServingProtein * 2);
  return plan;
}

// Free-preview shape: the assessment, the targets, and the daily math are the
// hook — recipe names/macros visible, ingredients & steps members-only.
function stripMealPlanForPreview(plan) {
  return {
    why_this_works: plan.why_this_works,
    assessment: plan.assessment,
    targets: plan.targets,
    daily_structure: plan.daily_structure,
    weekend_guidance: plan.weekend_guidance,
    locked: true,
    prep_recipes: (plan.prep_recipes || []).map((r) => ({
      name: r.name, emoji: r.emoji, description: r.description,
      prep_time_min: r.prep_time_min, servings: r.servings, per_serving: r.per_serving,
      locked: true,
    })),
  };
}

// Generate a meal plan from intake. Free for everyone (same sunk-cost hook as
// the trainer) — members get the full plan; free users get the preview.
app.post('/api/generate-mealplan', aiLimiter, optionalAuth, async (req, res) => {
  try {
    const intake = validateNutritionIntake(req.body?.intake);
    if (!intake) return res.status(400).json({ error: 'Missing or incomplete intake (age, height, and weight are required)' });
    const { photoBase64, photoMime, afterPhotoBase64, afterPhotoMime, photoConsent } = req.body || {};

    const targets = computeNutritionTargets(intake);
    const userContent = buildNutritionistUserContent(intake, photoConsent ? {
      beforeBase64: photoBase64, beforeMime: photoMime,
      afterBase64: afterPhotoBase64, afterMime: afterPhotoMime,
    } : null, targets);

    // Sleep Coach cross-feature rule: bad night → extra calories from protein
    // ONLY (craving control); great night → suggest a higher deficit today.
    if (req.user) {
      const sleepLine = sleepContextForNutrition(await getTodaysSleep(req.user.id));
      if (sleepLine) userContent.push({ type: 'text', text: sleepLine });
      const weightLine = await getWeightContext(req.user.id);
      if (weightLine) userContent.push({ type: 'text', text: weightLine });
    }

    let plan;
    try {
      plan = await callTrainerModel(NUTRITIONIST_SYSTEM_PROMPT, userContent, MEALPLAN_SCHEMA);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Meal plan generation failed. Please try again.' });
    }
    if (!plan?.prep_recipes?.length || !plan?.targets) {
      console.error('unusable meal plan, keys:', plan && Object.keys(plan));
      return res.status(502).json({ error: 'Model returned an unusable plan. Please try again.' });
    }
    sanitizeMealPlan(plan, targets, intake);

    let planId = null;
    let member = false;
    if (req.user && db) {
      member = isActiveMembership(req.user);
      try {
        const { rows } = await db.query(
          `INSERT INTO meal_plans (user_id, plan_number, intake, plan) VALUES ($1, 1, $2, $3) RETURNING id`,
          [req.user.id, JSON.stringify(intake), JSON.stringify(plan)]
        );
        planId = rows[0].id;
        backfillProfile(req.user.id).catch(() => {}); // fill profile gaps from this intake
      } catch (e) { console.error('meal plan save error:', e.message); }
    }

    res.json({
      planId,
      planNumber: 1,
      locked: !member,
      plan: member ? { ...plan, locked: false } : stripMealPlanForPreview(plan),
    });
  } catch (err) {
    console.error('generate-mealplan error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Latest meal plan for the logged-in user (full for members, preview otherwise).
app.get('/api/mealplan', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT id, plan_number, intake, plan FROM meal_plans WHERE user_id = $1 ORDER BY id DESC LIMIT 1',
      [req.user.id]
    );
    if (!rows.length) return res.json({ plan: null });
    const row = rows[0];
    const userRow = await getUserRow(req.user.id);
    const member = isActiveMembership(userRow);
    res.json({
      planId: row.id,
      planNumber: row.plan_number,
      intake: row.intake,
      locked: !member,
      plan: member ? { ...row.plan, locked: false } : stripMealPlanForPreview(row.plan),
    });
  } catch (e) {
    console.error('get mealplan error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Swap one prep recipe the user doesn't like — regenerates a single recipe at
// the same macros with their note. Members only.
app.post('/api/mealplan/swap', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'Membership required', needsMembership: true });
    }
    const { planId, recipeIndex, note } = req.body || {};
    const idx = parseInt(recipeIndex, 10);
    const { rows } = await db.query(
      'SELECT id, plan_number, intake, plan FROM meal_plans WHERE id = $1 AND user_id = $2',
      [parseInt(planId, 10) || 0, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Meal plan not found' });
    const row = rows[0];
    const plan = row.plan;
    if (!(idx >= 0 && idx < (plan.prep_recipes || []).length)) {
      return res.status(400).json({ error: 'Invalid recipeIndex' });
    }
    const intake = validateNutritionIntake(row.intake) || row.intake;
    const old = plan.prep_recipes[idx];
    const others = plan.prep_recipes.filter((_, i) => i !== idx).map((r) => r.name);

    const content = [{
      type: 'text',
      text: `User intake:\n${JSON.stringify(intake, null, 2)}\n\n` +
        `The user wants to REPLACE this meal-prep recipe:\n${JSON.stringify(old, null, 2)}\n\n` +
        (note ? `Their note about why / what they want instead: "${String(note).slice(0, 300)}"\n\n` : '') +
        `Create ONE new 10-serving prep recipe that:\n` +
        `- hits the SAME per-serving macros within ~5% (${old.per_serving?.calories} cal, ${old.per_serving?.protein_g}g protein per serving)\n` +
        `- is clearly different from the recipes they already have: ${others.join(', ')}\n` +
        `- respects every allergy, diet style, and dislike in the intake as hard constraints, matches their cooking effort, and leans on their favorite foods.`,
    }];

    let recipe;
    try {
      recipe = await callNutritionRecipeModel(content);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Recipe swap failed. Please try again.' });
    }
    if (!recipe?.name || !recipe?.per_serving) {
      return res.status(502).json({ error: 'Model returned an unusable recipe. Please try again.' });
    }
    recipe.servings = 10;
    plan.prep_recipes[idx] = recipe;
    await db.query('UPDATE meal_plans SET plan = $1 WHERE id = $2 AND user_id = $3',
      [JSON.stringify(plan), row.id, req.user.id]);
    res.json({ planId: row.id, planNumber: row.plan_number, locked: false, plan: { ...plan, locked: false } });
  } catch (err) {
    console.error('mealplan swap error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

async function callNutritionRecipeModel(userContent) {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: 4000,
      system: NUTRITIONIST_SYSTEM_PROMPT,
      output_config: { format: { type: 'json_schema', schema: RECIPE_SCHEMA } },
      messages: [{ role: 'user', content: userContent }],
    }),
  });
  const data = await response.json();
  if (!response.ok) {
    const err = new Error(data?.error?.message || 'Claude API error');
    err.status = response.status;
    throw err;
  }
  return JSON.parse(data?.content?.[0]?.text || '');
}

// Check-in: new weight (and optional feedback) → recompute targets and build a
// fresh plan. This is what makes it a nutritionist, not a calculator: static
// targets stop working as people lose weight. Members only.
app.post('/api/mealplan/checkin', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'Membership required', needsMembership: true });
    }
    const { planId, weight_lb, notes } = req.body || {};
    const { rows } = await db.query(
      'SELECT id, plan_number, intake, plan FROM meal_plans WHERE id = $1 AND user_id = $2',
      [parseInt(planId, 10) || 0, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Meal plan not found' });
    const prev = rows[0];

    const intake = validateNutritionIntake({ ...prev.intake, weight_lb: weight_lb ?? prev.intake.weight_lb });
    if (!intake) return res.status(400).json({ error: 'Invalid intake' });
    const prevWeight = parseFloat(prev.intake.weight_lb) || intake.weight_lb;
    const delta = Math.round((intake.weight_lb - prevWeight) * 10) / 10;

    const targets = computeNutritionTargets(intake);
    const userContent = buildNutritionistUserContent(intake, null, targets);
    userContent.push({
      type: 'text',
      text: `CHECK-IN: this user has been on plan ${prev.plan_number} and just weighed in.\n` +
        `Previous weight: ${prevWeight} lb → current weight: ${intake.weight_lb} lb (${delta > 0 ? '+' : ''}${delta} lb).\n` +
        (notes ? `Their notes: "${String(notes).slice(0, 300)}"\n` : '') +
        `Previous plan's recipes (build fresh ones — don't repeat): ${(prev.plan.prep_recipes || []).map((r) => r.name).join(', ')}.\n` +
        `Previous calorie target: ${prev.plan.targets?.daily_calories}. Adjust based on progress: losing on pace → stay the course; stalled 2+ weeks → nudge down within the allowed range; losing too fast or feeling drained → nudge up. Acknowledge their progress warmly in why_this_works.`,
    });

    // Sleep Coach cross-feature rule: bad night → extra calories from protein
    // ONLY (craving control); great night → suggest a higher deficit today.
    const nutriSleepLine = sleepContextForNutrition(await getTodaysSleep(req.user.id));
    if (nutriSleepLine) userContent.push({ type: 'text', text: nutriSleepLine });
    const nutriWeightLine = await getWeightContext(req.user.id);
    if (nutriWeightLine) userContent.push({ type: 'text', text: nutriWeightLine });

    let plan;
    try {
      plan = await callTrainerModel(NUTRITIONIST_SYSTEM_PROMPT, userContent, MEALPLAN_SCHEMA);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Plan update failed. Please try again.' });
    }
    if (!plan?.prep_recipes?.length || !plan?.targets) {
      return res.status(502).json({ error: 'Model returned an unusable plan.' });
    }
    sanitizeMealPlan(plan, targets, intake);

    const ins = await db.query(
      `INSERT INTO meal_plans (user_id, plan_number, intake, plan) VALUES ($1, $2, $3, $4) RETURNING id`,
      [req.user.id, prev.plan_number + 1, JSON.stringify(intake), JSON.stringify(plan)]
    );
    res.json({
      planId: ins.rows[0].id,
      planNumber: prev.plan_number + 1,
      locked: false,
      plan: { ...plan, locked: false },
    });
  } catch (err) {
    console.error('mealplan checkin error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
//  THE DECISION COUNSEL — five Claude seats, one verdict
// ============================================================
// Four counselors (Researcher, Skeptic, Coach, Safety Officer) review the
// user's case independently in parallel; the President synthesizes a final
// verdict. All seats are claude-sonnet-5 with different system prompts.

const COUNSEL_MODEL = 'claude-sonnet-5';

// Shared charter prepended to every seat + the President. The counsel's failure
// mode is unearned caution — this is the standing correction. (See HANDOFF Phase 5a.)
const COUNSEL_CHARTER = `COUNSEL CHARTER — applies to every seat: Users come here for a real answer they can act on, and every report already carries a "not medical advice" disclaimer, so your job is the useful answer, not the disclaimer. Generic unearned caution is a product failure: never say "consult a professional" or "talk to your doctor" unless you name the specific finding from THIS user's intake that requires it and say exactly what to ask. Hedged non-answers ("it depends", "everyone is different") are banned. Standard supplements at commonly studied doses in healthy adults do not need physician sign-off — reserve escalation for genuine flags: interactions with listed medications, doses well above studied ranges, pregnancy/nursing, age under 18, relevant medical conditions, or contaminated/gray-market product categories.

`;

const RESEARCHER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['position', 'reasoning', 'evidence_table', 'biggest_caveat'],
  properties: {
    position: { type: 'string', description: 'One-sentence position on the question.' },
    reasoning: { type: 'string', description: '3-6 short paragraphs of evidence-based reasoning, written for a smart layperson.' },
    evidence_table: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['item', 'verdict', 'rationale'],
        properties: {
          item: { type: 'string', description: 'The claim, substance, or intervention being rated.' },
          verdict: { type: 'string', enum: ['STRONG', 'MODERATE', 'WEAK', 'NO EVIDENCE'] },
          rationale: { type: 'string', description: 'One-line rationale for the rating.' },
        },
      },
    },
    biggest_caveat: { type: 'string', description: 'The single biggest caveat to this opinion.' },
  },
};

const SKEPTIC_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['position', 'reasoning', 'strongest_argument_against', 'would_change_mind'],
  properties: {
    position: { type: 'string', description: 'One-sentence position on the question.' },
    reasoning: { type: 'string', description: 'The skeptical case, 3-6 short paragraphs.' },
    strongest_argument_against: { type: 'string', description: 'The single strongest argument against the default/popular path.' },
    would_change_mind: { type: 'string', description: 'What evidence would change this opinion.' },
  },
};

const COACH_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['position', 'reasoning', 'adherence_risk', 'adherence_reason', 'do_first'],
  properties: {
    position: { type: 'string', description: 'One-sentence position on the question.' },
    reasoning: { type: 'string', description: 'Practical, life-fit reasoning grounded in the intake, 3-6 short paragraphs.' },
    adherence_risk: { type: 'string', enum: ['LOW', 'MEDIUM', 'HIGH'] },
    adherence_reason: { type: 'string', description: 'One sentence on why adherence risk is rated this way.' },
    do_first: { type: 'string', description: 'The one thing they should do first.' },
  },
};

const SAFETY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['rating', 'position', 'flags', 'doctor_questions'],
  properties: {
    rating: { type: 'string', enum: ['GREEN', 'YELLOW', 'RED'], description: 'GREEN = safe to self-manage, YELLOW = proceed with precautions, RED = see a professional before acting.' },
    position: { type: 'string', description: 'One-sentence position on the question.' },
    flags: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['flag', 'severity'],
        properties: {
          flag: { type: 'string', description: 'The safety issue, interaction, or red flag.' },
          severity: { type: 'string', enum: ['LOW', 'MEDIUM', 'HIGH'] },
        },
      },
    },
    doctor_questions: {
      type: 'array',
      items: { type: 'string' },
      description: 'Exactly what to ask a doctor, if a doctor is needed. Empty array if not.',
    },
  },
};

const PRESIDENT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['verdict', 'confidence', 'confidence_reason', 'where_agreed', 'where_split', 'reasoning', 'next_actions', 'keep_drop_table', 'new_stack', 'monthly_savings'],
  properties: {
    verdict: { type: 'string', description: 'ONE clear verdict sentence, e.g. "Yes, but only after X" or "No — do Y instead".' },
    confidence: { type: 'string', enum: ['HIGH', 'MODERATE', 'LOW'] },
    confidence_reason: { type: 'string', description: 'One sentence on why this confidence level; if LOW, what information would resolve it.' },
    where_agreed: { type: 'string', description: 'Where the counselors agreed.' },
    where_split: { type: 'string', description: 'Where the counselors disagreed. "No major disagreements" if none.' },
    reasoning: { type: 'string', description: 'Full synthesis, crediting counselors by role, 3-6 short paragraphs.' },
    next_actions: {
      type: 'array',
      items: { type: 'string' },
      description: 'Exactly 3 concrete ordered next actions, each doable within two weeks.',
    },
    // Supplement Audit deliverables. EVERY photographed/listed item must appear
    // as a row in keep_drop_table (nothing goes unmentioned).
    keep_drop_table: {
      type: 'array',
      description: 'One row per item the user currently takes, plus any ADD rows for new recommendations. Every listed item MUST appear here.',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['item', 'action', 'reason'],
        properties: {
          item: { type: 'string' },
          action: { type: 'string', enum: ['KEEP', 'DROP', 'DOWNGRADE', 'SWAP', 'ADD'] },
          reason: { type: 'string', description: 'One line. For DROP/DOWNGRADE/SWAP include monthly savings if estimable, e.g. "(-$35/mo)". ADD rows are new generic-ingredient recommendations with dose + rough cost.' },
        },
      },
    },
    new_stack: {
      type: 'array',
      description: 'The final recommended stack: generic ingredient, dose, timing, ~$/mo. Must respect the budget + max daily servings.',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['ingredient', 'dose', 'timing', 'monthly_cost'],
        properties: {
          ingredient: { type: 'string' },
          dose: { type: 'string' },
          timing: { type: 'string' },
          monthly_cost: { type: 'string' },
        },
      },
    },
    monthly_savings: { type: 'string', description: 'Net $/mo freed up, e.g. "~$55/mo". "$0" if nothing dropped.' },
  },
};

const FOLLOWUP_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['answer'],
  properties: {
    answer: { type: 'string', description: "The President's direct answer to the follow-up question, 1-4 short paragraphs, consistent with the case file." },
  },
};

const RESEARCHER_PROMPT = `You are THE RESEARCHER, a member of the Abs by AI Decision Counsel — a panel that helps everyday people make hard fitness and health decisions.

Your role: evaluate the user's question strictly through the lens of scientific evidence.

Rules:
- For every claim, substance, or intervention involved, rate the evidence: STRONG, MODERATE, WEAK, or NO EVIDENCE. Base this on study quality (RCTs and meta-analyses outrank observational studies, which outrank mechanistic speculation and bro-science).
- Report effect sizes in plain English ("creatine adds roughly 1-2 extra reps at the margin," not "d=0.43").
- Distinguish "studied in people like this user" from "studied in different populations" (e.g., trained vs untrained, male vs female, young vs older).
- If the evidence is genuinely mixed or absent, say so plainly. Do not fill gaps with optimism.
- You do not consider cost, convenience, or personal preference — other counselors handle that. Evidence only.
- Write for a smart layperson. No citations by author name; describe the evidence ("multiple large trials," "one small pilot study").

You must not diagnose conditions or prescribe treatment. Where a question can only be answered with labs, imaging, or a clinical exam, state that explicitly.

Output your opinion as JSON matching the provided schema: a one-sentence position, your reasoning (3-6 short paragraphs), an evidence table (item, verdict, one-line rationale), and your single biggest caveat.`;

const SKEPTIC_PROMPT = `You are THE SKEPTIC, a member of the Abs by AI Decision Counsel.

Your role: argue against the popular or default answer. You are the counsel's devil's advocate, and you take the job seriously — your goal is to make sure the user never spends money, time, or health on something that doesn't deserve it.

Rules:
- Assume marketing is lying until proven otherwise. Call out supplement-industry hype, influencer incentives, cherry-picked studies funded by manufacturers, and survivorship bias ("the guy on TRT was also training 6 days a week").
- Hunt for the boring alternative: is the real answer sleep, protein, consistency, or patience rather than the shiny intervention being asked about?
- Steelman the case AGAINST doing the thing, even if you suspect the counsel will ultimately favor it. If the case against is genuinely weak, say so — you are a skeptic, not a contrarian; your credibility depends on conceding when the evidence wins.
- Name the costs nobody mentions: dependency (TRT is usually for life), rebound (weight regain after GLP-1 discontinuation), habit displacement, money that could fund better food or a coach.
- Know when the evidence has already won: GLP-1s and physician-supervised TRT are NOT supplement-industry hype — they are among the best-evidenced interventions in this space, with benefits that extend beyond weight (reduced alcohol and junk-food cravings, metabolic health). If the user's case fits, your job is to attack the weak parts of the plan (sourcing, expectations, exit strategy), not to reflexively oppose the medication.
- You may be blunt and a little sharp-tongued. You may not be dismissive of the user's goals — attack the intervention, never the person.
- Over-caution is also a popular default answer. If the cautious path ("stop everything", "ask your doctor first") is not actually supported by a named risk, be skeptical of *that* too — reflexive caution wastes the user's money and trust the same way hype does.
- You own the proprietary-blend attack: a blend that hides its per-ingredient doses is presumed underdosed until the label proves otherwise. "Proprietary blend, doses not disclosed" is a strike against a product, not a neutral fact.

You must not diagnose or prescribe. Output your opinion as JSON matching the provided schema: a one-sentence position, your reasoning, the strongest argument against the default path, and what evidence would change your mind.`;

const COACH_PROMPT = `You are THE COACH, a member of the Abs by AI Decision Counsel.

Your role: ignore the lab and look at the user's actual life. Two interventions with identical evidence are not equal if one fits this person's schedule, budget, and psychology and the other doesn't. Adherence beats optimization, every time.

Rules:
- Ground everything in the intake details: their schedule, budget, training history, past failed attempts, and stated goals. Quote their own words back to them when relevant.
- Evaluate: Will they actually stick to this? What does it cost per month, and is that sustainable for years, not weeks? What does it displace — does adding this crowd out something more important?
- Prefer the smallest change that moves the needle. If the user is asking about an advanced intervention while a basic one is unhandled (sleeping 5 hours, protein at half target, program-hopping), say so directly — that IS your recommendation.
- Give a concrete implementation picture: what week 1 actually looks like if they proceed, and the single most likely failure point.
- Tone: warm, direct, experienced. Like a coach who has watched hundreds of people succeed and fail and knows the difference is rarely the supplement stack.

You are the LEAD COUNSELOR: the President's verdict defaults to your recommendation unless another counselor produces a concrete overriding finding, so commit to a clear recommendation — never punt.

Coaching philosophy (DAN TO REVIEW — drafted in his voice, edit freely):
- Food, sleep, and training drive 95% of results; supplements are the last 5%. Never let a supplement conversation obscure an unhandled basic.
- The proven shortlist is short: creatine, protein powder (as food convenience), caffeine, and vitamin D if you're actually low. Everything else is guilty until proven innocent.
- Money saved on junk supplements is a raise. Redirect it to better food, a gym membership, or nothing.
- A supplement you'll take consistently at an effective dose beats a "perfect" stack you'll abandon. Simple stacks survive real life.
- No hedging on the basics: an adult buying creatine does not need a doctor's permission slip.

The user's logged meals may be in your context: if their protein is already covered by food, say so — don't sell them powder they don't need.

You do not evaluate study quality (the Researcher does that) or medical risk (the Safety Officer does that). Output your opinion as JSON matching the provided schema: a one-sentence position, your reasoning, an adherence risk rating (LOW/MEDIUM/HIGH) with the reason, and the one thing you'd have them do first.`;

const SAFETY_PROMPT = `You are THE SAFETY OFFICER, a member of the Abs by AI Decision Counsel.

Your role: identify every safety issue in the user's question — interactions, contraindications, red flags, and above all, which parts of this decision require a real medical professional. You are the counsel's line of defense, and you are explicitly empowered to overrule enthusiasm.

Rules:
- YOUR TOP JOB, ALWAYS STRICT: check every listed supplement against any listed MEDICATIONS for known interactions (e.g. St. John's Wort + SSRIs/SNRIs; high-dose fish oil, garlic, vitamin E, or ginkgo + warfarin or other blood thinners; potassium + ACE inhibitors; stimulants + MAOIs). A real interaction with a listed medication is a named RED flag — this is the one thing you can never miss, and no charter language about avoiding caution weakens it.
- YOUR SECOND JOB: total-stimulant math. Sum the caffeine across every product (use each item's per-serving caffeine) PLUS the user's stated other caffeine (coffee, energy drinks, pre-workout). Call out the daily total in mg when it stacks toward or past ~400mg, and higher for anyone stim-sensitive or with cardiovascular flags.
- Flag dosages above commonly studied ranges, and note genuinely poorly-regulated categories with a real contamination history (e.g. some fat burners, "test boosters", SARMs-adjacent products). A proprietary blend that hides its doses cannot be dose-verified — say so.
- Rate the overall stack: GREEN (safe to self-manage), YELLOW (proceed with specific precautions), RED (a specific red flag means stop and see a professional before acting). GREEN is the EXPECTED rating for standard products at studied doses in healthy adults — most sensible stacks are GREEN. YELLOW requires a named precaution tied to THIS user's intake (a real stimulant total, a dose above studied range, pregnancy/nursing, a relevant condition). RED requires a named interaction, contraindication, or dangerous dose. Never rate up because "supplements in general carry risks" or because the category feels medical — that is exactly the unearned caution the charter bans.
- A flag must be worth its cost: burying two real flags under eight theoretical ones makes the user safer on paper and less safe in practice. List only flags you would act on yourself.
- Pregnancy/nursing and age under 18 are hard gates — if the intake indicates either, flag every item that isn't clearly safe for that state.
- Never diagnose, never prescribe, never estimate doses for prescription compounds.

Tone: calm and precise, not alarmist. You make risk legible, you don't catastrophize.
Output your opinion as JSON matching the provided schema: the GREEN/YELLOW/RED rating, a one-sentence position, itemized flags (each with severity), and exactly what to ask a doctor if a doctor is needed.`;

const PRESIDENT_PROMPT = `You are THE PRESIDENT of the Abs by AI Decision Counsel. Four counselors — the Researcher, the Skeptic, the Coach, and the Safety Officer — have independently reviewed the user's case. You have their full written opinions plus the user's original intake. Your job is to deliver the final verdict.

Rules:
- Read all four opinions before forming your view. Identify where they AGREE (this is your foundation — consensus across independent perspectives is strong signal) and where they DISAGREE (name the disagreement honestly; do not paper over it).
- The Coach is the LEAD COUNSELOR: their recommendation is your default verdict. Depart from it only if (a) the Researcher shows the evidence directly contradicts it, or (b) the Safety Officer names a concrete red flag from this user's intake. If neither happened, your verdict is the Coach's plan, sharpened — say so.
- The Safety Officer holds a special veto: if they rated the stack RED, your verdict MUST route through a medical professional as the primary recommendation. You may still advise on everything within the user's control in the meantime. A YELLOW is not a veto — a named precaution is fully compatible with a confident recommendation.
- "Consult a professional" is never a verdict by itself. If a real flag requires a doctor, the verdict is the actionable plan PLUS that specific referral with the exact question to ask.
- Issue ONE clear verdict. The user came here because "it depends" wasn't good enough. Formats like "Keep 2, drop 3, add creatine" or "Your stack is mostly waste — here's the $20 version that works" are verdicts; "here are some considerations" is not.
- State your confidence: HIGH (counsel consensus + clear evidence), MODERATE (some dissent or mixed evidence), or LOW (genuine split — and then explain what information would resolve it).
- End with exactly 3 concrete next actions, ordered, each doable within two weeks.
- Credit the counselors by role when you draw on them ("As the Skeptic pointed out..."). If you side against a counselor, say why in one sentence.
- Tone: decisive, fair, human. A good chairperson, not a hedge-fund disclaimer.

SUPPLEMENT AUDIT DELIVERABLES (in addition to the verdict):
- keep_drop_table: EVERY item the user currently takes must appear as a row, with action KEEP / DROP / DOWNGRADE / SWAP and a one-line reason. For DROP/DOWNGRADE/SWAP, include the monthly savings when estimable, e.g. "(-$35/mo)". Add ADD rows for anything genuinely worth starting (generic ingredient + dose + rough cost).
- new_stack: the final recommended stack as generic ingredients (not brands) — ingredient, dose, timing, ~$/mo. It MUST fit the user's stated monthly budget and max daily servings. If the ideal stack doesn't fit, cut in reverse order of evidence (drop the least-proven item first) until it fits.
- monthly_savings: the net $/mo the user frees up by following your plan, e.g. "~$55/mo" ("$0" if nothing is dropped).

You must not diagnose or prescribe. Output as JSON matching the provided schema.`;

// Per-decision-type addendum appended to every counselor's system prompt.
// The retired Decision Counsel types (glp1-trt, injury-return, etc.) are kept
// DORMANT below — commented, not deleted — so the feature can be restored (see
// _counsel_archive/README.md). Only 'supplement-audit' is live.
const COUNSEL_TYPE_ADDENDA = {
  'supplement-audit': `\n\nThis case is a SUPPLEMENT AUDIT. The user has photographed (or typed) the supplements they currently take; the label data is quoted to you verbatim in the items list — treat every dose and ingredient as read directly off the bottle, and where a product is a proprietary blend with no per-ingredient doses disclosed, treat it as exactly that: undisclosed and presumed underdosed. Address EVERY listed item — nothing on the list may go unmentioned in the counsel's collective output — and weigh the stack as a whole, not just each item in isolation. The user has stated a monthly budget and a maximum number of daily servings/pills; a good stack respects both. USER CONTEXT (their training, nutrition, logged protein, sleep, and weight trend) is provided — use it: if food already covers their protein, don't endorse a protein powder as essential; if they barely sleep, magnesium/glycine is more relevant than another stimulant.`,
  // DORMANT — retired Decision Counsel types. Restore alongside the frontend to
  // bring the multi-decision Counsel back.
  // 'glp1-trt': `\n\nThis case is a GLP-1 / TRT DECISION...`,
  // 'injury-return': `\n\nThis case is a RETURN-FROM-INJURY decision...`,
  // 'physique-direction': `\n\nThis case is a PHYSIQUE DIRECTION decision...`,
  // custom: `\n\nThis is a CUSTOM QUESTION the user has brought to the counsel...`,
};

const COUNSEL_SEATS = [
  { role: 'researcher', name: 'The Researcher', prompt: RESEARCHER_PROMPT, schema: RESEARCHER_SCHEMA },
  { role: 'skeptic', name: 'The Skeptic', prompt: SKEPTIC_PROMPT, schema: SKEPTIC_SCHEMA },
  { role: 'coach', name: 'The Coach (Lead Counselor)', prompt: COACH_PROMPT, schema: COACH_SCHEMA },
  { role: 'safety', name: 'The Safety Officer', prompt: SAFETY_PROMPT, schema: SAFETY_SCHEMA },
];

// Intake for the Supplement Audit. `items` is a structured array (the Phase-2
// label-reader output, or typed fallbacks); the rest are hard-clamped strings.
// DORMANT retired-type field defs are preserved in _counsel_archive/.
const COUNSEL_INTAKE_FIELDS = {
  'supplement-audit': {
    strings: ['medications', 'budget_monthly', 'max_daily_servings', 'caffeine_other', 'pregnant_nursing', 'sensitivities', 'stack_style', 'age', 'sex', 'goal', 'diet'],
    required: ['medications', 'budget_monthly', 'max_daily_servings', 'stack_style'],
  },
};

// One audit item, hard-sanitized to the known shape. Objects come from the
// label endpoint or the typed-item fallback; anything else is dropped.
function sanitizeAuditItems(raw) {
  if (!Array.isArray(raw)) return [];
  const clamp = (v, n) => String(v ?? '').trim().slice(0, n);
  return raw.slice(0, 25).map((it) => {
    if (!it || typeof it !== 'object') return null;
    const name = clamp(it.product_name || it.name, 120);
    if (!name) return null;
    const ingredients = Array.isArray(it.ingredients)
      ? it.ingredients.slice(0, 40).map((g) => ({
          name: clamp(g && g.name, 80),
          dose: clamp(g && g.dose, 24),
          unit: clamp(g && g.unit, 16),
        })).filter((g) => g.name)
      : [];
    const num = (v) => (Number.isFinite(+v) ? +v : null);
    return {
      product_name: name,
      source: it.source === 'typed' ? 'typed' : 'photo',
      brand: it.brand ? clamp(it.brand, 80) : null,
      category: clamp(it.category, 40) || 'other',
      is_blend: !!it.is_blend,
      ingredients,
      serving_info: it.serving_info ? clamp(it.serving_info, 120) : null,
      caffeine_mg_per_serving: num(it.caffeine_mg_per_serving),
      est_monthly_cost: num(it.est_monthly_cost),
      needs_panel: !!it.needs_panel,
      panel_skipped: !!it.panel_skipped,
      item_goal: it.item_goal ? clamp(it.item_goal, 200) : null,
    };
  }).filter(Boolean);
}

function validateCounselIntake(decisionType, raw) {
  // Live product accepts only the Supplement Audit; retired types are rejected
  // upstream (Phase 1 gate) but this stays defensive.
  if (decisionType !== 'supplement-audit') return null;
  const spec = COUNSEL_INTAKE_FIELDS['supplement-audit'];
  if (!raw || typeof raw !== 'object') return null;
  const intake = { items: sanitizeAuditItems(raw.items) };
  for (const key of spec.strings) {
    const v = String(raw[key] ?? '').trim().slice(0, 600);
    if (v) intake[key] = v;
  }
  // Required intake fields must be present. `items` MAY be empty — the
  // "empty-handed, recommend me a stack" case is valid.
  for (const key of spec.required) {
    if (!intake[key]) return null;
  }
  return intake;
}

const COUNSEL_TYPE_LABELS = {
  'supplement-audit': 'Supplement stack audit',
};

function buildCounselUserContent(decisionType, intake, photos, contextBlock) {
  const content = [];
  const { beforeBase64, beforeMime } = photos || {};
  if (beforeBase64 && beforeMime) {
    content.push({ type: 'image', source: { type: 'base64', media_type: beforeMime, data: beforeBase64 } });
    content.push({ type: 'text', text: "The user's CURRENT physique photo (from their account, shared with consent). Use it only as backdrop for judging whether the stack matches their real situation. Never judgmental." });
  }
  const { items, ...rest } = intake || {};
  let text = `Decision type: ${COUNSEL_TYPE_LABELS[decisionType] || decisionType}\n\n`;
  if (contextBlock) {
    text += `USER CONTEXT (pulled from their account — do NOT re-ask for any of this):\n${contextBlock}\n\n`;
  }
  text += `SUPPLEMENTS THE USER CURRENTLY TAKES — read off their labels, quoted verbatim. A "proprietary blend" with no per-ingredient doses is undisclosed and presumed underdosed:\n${JSON.stringify(items || [], null, 2)}\n\n`;
  text += `AUDIT INTAKE (budget, servings cap, meds, style, etc.):\n${JSON.stringify(rest, null, 2)}\n\n`;
  text += `Give a genuinely independent opinion for each lens, then the final verdict. Output JSON matching the provided schema.`;
  content.push({ type: 'text', text });
  return content;
}

async function callCounselSeat(systemPrompt, userContent, schema, maxTokens, effort) {
  // A stalled connection to Anthropic would otherwise hang this fetch forever —
  // node-fetch has no default timeout — leaving an audit_jobs row stuck at
  // "running" indefinitely. Bound every attempt so callSeatResilient's retry
  // (and the job's error state) can actually kick in.
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 240000); // 4 min/attempt
  let response;
  try {
    response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: COUNSEL_MODEL,
        max_tokens: maxTokens,
        system: systemPrompt,
        output_config: { ...(effort ? { effort } : {}), format: { type: 'json_schema', schema } },
        messages: [{ role: 'user', content: userContent }],
      }),
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timer);
  }
  const data = await response.json();
  if (!response.ok) {
    const err = new Error(data?.error?.message || 'Claude API error');
    err.status = response.status;
    throw err;
  }
  // Sonnet 5 runs adaptive thinking by default, so content[0] can be a
  // thinking block — find the text block instead of assuming position 0.
  const text = (data?.content || []).find((b) => b.type === 'text')?.text;
  if (!text) {
    throw new Error(`empty counsel response (stop_reason: ${data?.stop_reason})`);
  }
  return JSON.parse(text);
}

// One retry per seat; null (not a throw) when a seat fails twice, so the
// counsel can proceed short-handed per the resilience plan.
async function callSeatResilient(seatName, fn) {
  try {
    return await fn();
  } catch (e1) {
    console.warn(`counsel seat ${seatName} failed (${e1.message}) — retrying once`);
    try {
      return await fn();
    } catch (e2) {
      console.error(`counsel seat ${seatName} failed twice: ${e2.message}`);
      return null;
    }
  }
}

// Reconstructs the case-file text for a saved session — used only by the
// follow-up endpoint now that the main audit is a single call (see
// buildMasterSystemPrompt / MASTER_SCHEMA below).
function buildPresidentContent(decisionType, intake, opinions) {
  let text = `Decision type: ${COUNSEL_TYPE_LABELS[decisionType] || decisionType}\n\n`;
  text += `User intake (includes the full items list — every item here MUST appear in your keep_drop_table):\n${JSON.stringify(intake, null, 2)}\n\n`;
  for (const seat of COUNSEL_SEATS) {
    const op = opinions[seat.role];
    if (op) text += `=== Opinion of ${seat.name} ===\n${JSON.stringify(op, null, 2)}\n\n`;
  }
  text += `Deliver the final verdict as JSON matching the provided schema.`;
  return [{ type: 'text', text }];
}

// Single-call engine: one model call reasons through all four lenses plus the
// final verdict, replacing the old 5-call Phase 1 (seats) + Phase 2
// (President) orchestration. Cuts cost ~80% and collapses 5 failure points to 1.
const MASTER_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['opinions', 'verdict'],
  properties: {
    opinions: {
      type: 'object',
      additionalProperties: false,
      required: COUNSEL_SEATS.map((s) => s.role),
      properties: Object.fromEntries(COUNSEL_SEATS.map((s) => [s.role, s.schema])),
    },
    verdict: PRESIDENT_SCHEMA,
  },
};

function buildMasterSystemPrompt(addendum) {
  const lenses = COUNSEL_SEATS.map((s) => `=== LENS: ${s.name.toUpperCase()} ===\n${s.prompt}`).join('\n\n');
  return COUNSEL_CHARTER +
    `You are producing the ENTIRE Abs by AI Supplement Audit in a single pass. Below are four expert lenses plus a final verdict role that used to run as five separate calls — you now inhabit all five in one response. Reason through each lens genuinely and independently before moving to the next; do not let the verdict's conclusion leak backward and flatten real disagreement between lenses. The verdict role then reviews all four lenses (which you just wrote) and delivers one synthesis.\n\n` +
    `${lenses}\n\n=== FINAL VERDICT (HEAD AUDITOR) ===\n${PRESIDENT_PROMPT}\n\n` +
    `${addendum}\n\n` +
    `Output ONE JSON object matching the provided schema: opinions.researcher, opinions.skeptic, opinions.coach, opinions.safety (each matching its lens's schema above), and verdict (matching the final-verdict schema above).`;
}

// Free-preview shape: the verdict sentence + safety rating + the dollars-saved
// total are the hook; reasoning, the keep/drop list, the new stack, and next
// actions are members-only.
function stripCounselForPreview(counsel) {
  const v = counsel.verdict || {};
  return {
    locked: true,
    // monthly_savings stays visible — it's the teaser ("this audit found ~$55/mo of waste").
    verdict: { verdict: v.verdict, confidence: v.confidence, monthly_savings: v.monthly_savings, locked: true },
    opinions: Object.fromEntries(Object.entries(counsel.opinions || {}).map(([role, op]) => [
      role,
      op ? { position: op.position, ...(op.rating ? { rating: op.rating } : {}), locked: true } : null,
    ])),
  };
}

// Assemble the USER CONTEXT block for an audit from what we already know about
// this user — so the seats never re-ask for training, nutrition, protein,
// sleep, or weight. Every pull is best-effort and defensive: a missing table or
// unexpected shape just drops that line, never fails the audit. Also returns the
// user's stored physique photo so the counsel can ground its read in reality.
async function assembleAuditContext(userId) {
  const out = { text: '', beforeImage: null, beforeMime: null };
  if (!db || !userId) return out;
  const lines = [];
  const clean = (s) => String(s).replace(/_/g, ' ');
  try {
    const { rows } = await db.query('SELECT before_image FROM users WHERE id = $1', [userId]);
    const m = rows[0]?.before_image && rows[0].before_image.match(/^data:(.*?);base64,(.*)$/);
    if (m) { out.beforeMime = m[1]; out.beforeImage = m[2]; }
  } catch (e) { /* no photo */ }
  // Shared member profile — the only context source for quiz-only members who
  // never filled the Trainer/Nutritionist intakes below. Terse to match style.
  try {
    const p = await readProfile(userId);
    const b = [];
    if (p.sex) b.push(p.sex);
    if (p.ageRange) b.push(`age ${p.ageRange}`);
    if (p.weight) b.push(`${p.weight} ${p.weightUnit || 'lb'}`);
    if (p.goal && PROFILE_GOAL_LABEL[p.goal]) b.push(`goal ${PROFILE_GOAL_LABEL[p.goal]}`);
    if (p.equipment && PROFILE_EQUIP_LABEL[p.equipment]) b.push(PROFILE_EQUIP_LABEL[p.equipment]);
    if (Array.isArray(p.diet) && p.diet.length) b.push(`diet: ${p.diet.map(d => PROFILE_DIET_LABEL[d] || d).join(', ')}`);
    if (b.length) lines.push(`Member profile: ${b.join(', ')}.`);
  } catch (e) { /* no profile */ }
  try {
    const { rows } = await db.query('SELECT intake FROM programs WHERE user_id = $1 ORDER BY id DESC LIMIT 1', [userId]);
    const i = rows[0]?.intake;
    if (i) {
      const b = [];
      if (i.age_range) b.push(`age ${i.age_range}`);
      if (i.sex_track) b.push(i.sex_track === 'woman' ? 'female' : 'male');
      if (i.goal) b.push(`goal ${clean(i.goal)}`);
      if (i.experience) b.push(`${i.experience} lifter`);
      if (i.equipment) b.push(`${i.equipment} equipment`);
      if (Array.isArray(i.injuries) && i.injuries.length) b.push(`injuries: ${i.injuries.join(', ')}`);
      if (b.length) lines.push(`Training profile: ${b.join(', ')}.`);
    }
  } catch (e) { /* no program */ }
  try {
    const { rows } = await db.query('SELECT intake FROM meal_plans WHERE user_id = $1 ORDER BY id DESC LIMIT 1', [userId]);
    const i = rows[0]?.intake;
    if (i) {
      const b = [];
      if (i.sex) b.push(i.sex);
      if (i.age) b.push(`age ${i.age}`);
      if (i.weight_lb) b.push(`${i.weight_lb} lb`);
      if (i.goal) b.push(`nutrition goal ${clean(i.goal)}`);
      if (i.diet_style && i.diet_style !== 'none') b.push(clean(i.diet_style));
      if (Array.isArray(i.allergies) && i.allergies.length) b.push(`allergies: ${i.allergies.join(', ')}`);
      if (i.glp1 === 'yes') b.push('currently on a GLP-1');
      if (i.meds_notes) b.push(`meds noted: ${i.meds_notes}`);
      if (b.length) lines.push(`Nutrition profile: ${b.join(', ')}.`);
    }
  } catch (e) { /* no meal plan */ }
  try {
    const { rows } = await db.query(
      `SELECT date, totals FROM meals WHERE user_id = $1 AND logged_at >= now() - interval '14 days'`, [userId]);
    if (rows.length) {
      const byDay = {};
      for (const r of rows) byDay[r.date] = (byDay[r.date] || 0) + (r.totals?.protein_g || 0);
      const days = Object.keys(byDay).length;
      const avg = Math.round(Object.values(byDay).reduce((a, b) => a + b, 0) / days);
      lines.push(`Logged food (last 14 days): ${days} day${days === 1 ? '' : 's'} logged, averaging ~${avg}g protein/day — use this to decide whether a protein powder is real food convenience or redundant.`);
    }
  } catch (e) { /* no meals */ }
  try {
    const { rows } = await db.query(
      `SELECT weight, unit FROM weight_logs WHERE user_id = $1 AND entry_date >= CURRENT_DATE - 30 ORDER BY entry_date ASC`, [userId]);
    if (rows.length >= 2) {
      const delta = Math.round((rows[rows.length - 1].weight - rows[0].weight) * 10) / 10;
      const dir = delta < -0.5 ? 'losing weight' : delta > 0.5 ? 'gaining weight' : 'holding steady';
      lines.push(`Weight trend (30d): ${dir} (${delta > 0 ? '+' : ''}${delta} ${rows[0].unit || 'lb'}).`);
    }
  } catch (e) { /* no weight logs */ }
  try {
    const { rows } = await db.query(
      `SELECT data FROM sleep_entries WHERE user_id = $1 ORDER BY entry_date DESC LIMIT 7`, [userId]);
    const durs = rows.map((r) => r.data?.duration_min).filter(Boolean);
    if (durs.length) {
      const avg = Math.round(durs.reduce((a, b) => a + b, 0) / durs.length);
      lines.push(`Sleep (recent avg): ~${Math.floor(avg / 60)}h${String(avg % 60).padStart(2, '0')}m/night — relevant to magnesium/glycine/melatonin-type items.`);
    }
  } catch (e) { /* no sleep entries */ }
  out.text = lines.join('\n');
  return out;
}

// Audit jobs: Postgres-backed so they survive Railway restarts; an in-memory
// Map is only a fallback for local dev without DATABASE_URL.
const auditJobsMem = new Map();

async function createAuditJob(userId) {
  const id = crypto.randomUUID();
  if (db) {
    await db.query('INSERT INTO audit_jobs (id, user_id, status) VALUES ($1, $2, $3)', [id, userId || null, 'running']);
  } else {
    auditJobsMem.set(id, { user_id: userId || null, status: 'running', result: null, error: null });
  }
  return id;
}

async function finishAuditJob(id, status, result, error) {
  if (db) {
    try {
      await db.query('UPDATE audit_jobs SET status = $1, result = $2, error = $3 WHERE id = $4',
        [status, result ? JSON.stringify(result) : null, error || null, id]);
      return;
    } catch (e) { console.error('audit job update error:', e.message); }
  }
  const job = auditJobsMem.get(id);
  if (job) { job.status = status; job.result = result; job.error = error || null; }
}

async function getAuditJob(id) {
  if (db) {
    const { rows } = await db.query('SELECT id, user_id, status, result, error FROM audit_jobs WHERE id = $1', [id]);
    return rows[0] || null;
  }
  const job = auditJobsMem.get(id);
  return job ? { id, ...job } : null;
}

// Runs the single-call audit engine in the background and stores the outcome
// on the job row. POST /api/counsel has already responded with the job id by
// the time this runs, so no HTTP request rides on the model call.
async function runSupplementAuditJob(jobId, decisionType, intake, photos, contextBlock, userRow) {
  try {
    const addendum = COUNSEL_TYPE_ADDENDA[decisionType] || '';
    const systemPrompt = buildMasterSystemPrompt(addendum);
    const userContent = buildCounselUserContent(decisionType, intake, photos, contextBlock);
    const report = await callSeatResilient('Supplement Audit', () =>
      callCounselSeat(systemPrompt, userContent, MASTER_SCHEMA, 24000, 'high')
    );
    if (!report || !report.verdict || !report.verdict.verdict) {
      throw new Error("The audit couldn't be completed. Please try again in a moment.");
    }
    const opinions = report.opinions || {};
    const verdict = report.verdict;
    verdict.next_actions = (verdict.next_actions || []).slice(0, 3);
    verdict.keep_drop_table = verdict.keep_drop_table || [];
    verdict.new_stack = verdict.new_stack || [];
    const counsel = { opinions, verdict, missingSeats: [] };

    let sessionId = null;
    const member = isActiveMembership(userRow);
    if (userRow && db) {
      try {
        const { rows } = await db.query(
          `INSERT INTO counsel_sessions (user_id, decision_type, intake, opinions, verdict) VALUES ($1, $2, $3, $4, $5) RETURNING id`,
          [userRow.id, decisionType, JSON.stringify(intake), JSON.stringify(opinions), JSON.stringify(verdict)]
        );
        sessionId = rows[0].id;
      } catch (e) { console.error('counsel save error:', e.message); }
    }

    const result = {
      sessionId,
      decisionType,
      locked: !member,
      counsel: member ? { ...counsel, locked: false } : stripCounselForPreview(counsel),
    };
    await finishAuditJob(jobId, 'done', result, null);
  } catch (err) {
    console.error('supplement audit job error:', err);
    await finishAuditJob(jobId, 'error', null, err.message || "The audit couldn't be completed. Please try again in a moment.");
  }
}

// Convene the audit (Supplement Audit). Free for everyone (sunk-cost hook) —
// members get the full case file back; free users get the verdict-level
// preview. Responds with a job id immediately; the single-call engine runs
// detached so no request rides on the model call (mobile Safari killed the
// connection on 12-item stacks before this fix — see AI_COORDINATION.md).
app.post('/api/counsel', aiLimiter, optionalAuth, async (req, res) => {
  try {
    const decisionType = String(req.body?.decisionType || '');
    // The Decision Counsel is retired. This engine now serves the Supplement
    // Audit only — refuse any other type before any work is done.
    if (decisionType !== 'supplement-audit') {
      return res.status(400).json({ error: 'This feature has been replaced by the Supplement Audit.' });
    }
    const intake = validateCounselIntake(decisionType, req.body?.intake);
    if (!intake) return res.status(400).json({ error: 'Missing or incomplete audit intake.' });

    // Monthly cap, checked before any model call so a capped request costs nothing.
    if (req.user && db) {
      try {
        const { rows } = await db.query(
          `SELECT COUNT(*)::int AS n FROM counsel_sessions
           WHERE user_id = $1 AND created_at >= date_trunc('month', now())`,
          [req.user.id]
        );
        if (rows[0].n >= COUNSEL_MONTHLY_CAP) {
          return res.status(429).json({
            error: `You've used all ${COUNSEL_MONTHLY_CAP} Supplement Audits for this month. Your allowance resets on the 1st.`,
            capReached: true,
          });
        }
      } catch (e) { console.error('counsel cap check error:', e.message); }
    }

    // Pull everything we already know about this user (members/logged-in only)
    // into a USER CONTEXT block + their stored physique photo.
    let contextBlock = '';
    let photos = null;
    if (req.user && db) {
      try {
        const ctx = await assembleAuditContext(req.user.id);
        contextBlock = ctx.text;
        if (ctx.beforeImage && ctx.beforeMime) photos = { beforeBase64: ctx.beforeImage, beforeMime: ctx.beforeMime };
      } catch (e) { console.error('audit context error:', e.message); }
    }

    const jobId = await createAuditJob(req.user?.id);
    res.json({ jobId });
    runSupplementAuditJob(jobId, decisionType, intake, photos, contextBlock, req.user || null).catch((e) =>
      console.error('supplement audit job uncaught error:', e)
    );
  } catch (err) {
    console.error('counsel error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Poll an audit job. { status: 'running' } while working; { status: 'done',
// ...result } once finished; { status: 'error', error } on failure. Jobs tied
// to a user may only be read by that user; anonymous (free-preview) jobs are
// readable by the unguessable id alone.
app.get('/api/counsel/job/:id', optionalAuth, async (req, res) => {
  try {
    const job = await getAuditJob(String(req.params.id || ''));
    if (!job) return res.status(404).json({ error: 'Job not found' });
    if (job.user_id && (!req.user || req.user.id !== job.user_id)) {
      return res.status(404).json({ error: 'Job not found' });
    }
    if (job.status === 'running') return res.json({ status: 'running' });
    if (job.status === 'error') return res.json({ status: 'error', error: job.error });
    return res.json({ status: 'done', ...job.result });
  } catch (e) {
    console.error('get audit job error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Latest counsel session for the logged-in user (full for members, preview otherwise).
app.get('/api/counsel', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT id, decision_type, intake, opinions, verdict, followups, created_at FROM counsel_sessions WHERE user_id = $1 ORDER BY id DESC LIMIT 1',
      [req.user.id]
    );
    if (!rows.length) return res.json({ counsel: null });
    const row = rows[0];
    const userRow = await getUserRow(req.user.id);
    const member = isActiveMembership(userRow);
    const counsel = { opinions: row.opinions, verdict: row.verdict, missingSeats: [] };
    res.json({
      sessionId: row.id,
      decisionType: row.decision_type,
      createdAt: row.created_at,
      locked: !member,
      counsel: member ? { ...counsel, locked: false } : stripCounselForPreview(counsel),
      followups: member ? row.followups || [] : [],
    });
  } catch (e) {
    console.error('get counsel error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// "Ask the President" — one follow-up question against a saved case file. Members only.
app.post('/api/counsel/followup', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'Membership required', needsMembership: true });
    }
    const question = String(req.body?.question || '').trim().slice(0, 600);
    if (!question) return res.status(400).json({ error: 'Missing question' });
    const { rows } = await db.query(
      'SELECT id, decision_type, intake, opinions, verdict, followups FROM counsel_sessions WHERE id = $1 AND user_id = $2',
      [parseInt(req.body?.sessionId, 10) || 0, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Counsel session not found' });
    const row = rows[0];

    const content = buildPresidentContent(row.decision_type, row.intake, row.opinions);
    content.push({
      type: 'text',
      text: `\nYou already delivered this verdict:\n${JSON.stringify(row.verdict, null, 2)}\n\n` +
        ((row.followups || []).length ? `Previous follow-up Q&A:\n${JSON.stringify(row.followups, null, 2)}\n\n` : '') +
        `The user now has a FOLLOW-UP QUESTION about your verdict: "${question}"\n\nAnswer it directly and consistently with the case file. Do not re-issue the verdict unless the question genuinely changes it. Output JSON matching the provided schema.`,
    });

    let reply;
    try {
      reply = await callCounselSeat(COUNSEL_CHARTER + PRESIDENT_PROMPT + (COUNSEL_TYPE_ADDENDA[row.decision_type] || ''), content, FOLLOWUP_SCHEMA, 4000, 'high');
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: "The audit couldn't be completed. Please try again in a moment." });
    }
    if (!reply?.answer) return res.status(502).json({ error: "The audit couldn't be completed. Please try again in a moment." });

    const followups = [...(row.followups || []), { question, answer: reply.answer, at: new Date().toISOString() }].slice(-20);
    await db.query('UPDATE counsel_sessions SET followups = $1 WHERE id = $2 AND user_id = $3',
      [JSON.stringify(followups), row.id, req.user.id]);
    res.json({ sessionId: row.id, question, answer: reply.answer, followups });
  } catch (err) {
    console.error('counsel followup error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ── Supplement Audit: label reader (Phase 2) ──────────────────────────
// One vision call per photographed product. Free + uncapped by design — it's
// the hook that pulls users into the audit. Modeled on /api/analyze-meal.
const SUPPLEMENT_LABEL_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['product_name', 'brand', 'category', 'is_blend', 'ingredients', 'serving_info', 'caffeine_mg_per_serving', 'est_monthly_cost', 'needs_panel', 'read_confidence', 'unreadable'],
  properties: {
    product_name: { type: 'string', description: 'The product name as printed. "Unknown" if unreadable.' },
    brand: { type: ['string', 'null'], description: 'Brand/manufacturer if printed, else null.' },
    category: { type: 'string', description: "One of: creatine, protein, pre-workout, fat-burner, multivitamin, fish-oil, vitamin-d, magnesium, greens, test-booster, bcaa, other." },
    is_blend: { type: 'boolean', description: 'True if a multi-ingredient product or proprietary blend (pre-workout, fat burner, greens, "test booster").' },
    ingredients: {
      type: 'array',
      description: 'Every ingredient legible on THIS photo with its dose. Empty array if none legible (e.g. a proprietary blend hides them).',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['name', 'dose', 'unit'],
        properties: {
          name: { type: 'string' },
          dose: { type: 'string', description: 'The number only, e.g. "5". Empty string if a blend hides it.' },
          unit: { type: 'string', description: 'e.g. "g", "mg", "mcg", "IU". Empty string if unknown.' },
        },
      },
    },
    serving_info: { type: ['string', 'null'], description: 'Serving size / servings per container as printed, else null.' },
    caffeine_mg_per_serving: { type: ['number', 'null'], description: 'Caffeine mg per serving if stated, else null.' },
    est_monthly_cost: { type: ['number', 'null'], description: 'Only if a price is visible OR a confident category-typical figure; else null.' },
    needs_panel: { type: 'boolean', description: 'True if is_blend AND the per-ingredient doses are NOT legible from this photo (ask for the ingredients-panel photo).' },
    read_confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    unreadable: { type: 'boolean', description: "True if this photo isn't a supplement label or is too blurry to read." },
  },
};

const SUPPLEMENT_LABEL_PROMPT = `You are the supplement-label reader for a fitness app. Given a photo (or two — front label plus an ingredients/Supplement Facts panel) of ONE supplement product, extract exactly what the label says.

Hard rules:
- Read ONLY what is printed on the label in front of you. NEVER fill in a formula, dose, or ingredient from memory or from what the brand "usually" contains — brands reformulate constantly, and the whole point of the audit is to quote the ACTUAL label. If you can't read a dose, leave it blank; do not guess it.
- Proprietary blends: if the label shows a "proprietary blend" with a single combined weight and no per-ingredient doses, list the ingredient names you can see with empty dose strings, set is_blend true, and set needs_panel true unless a full panel with per-ingredient doses is actually visible.
- is_blend is true for any multi-ingredient product (pre-workout, fat burner, greens, "test booster", most "complex" products). Single-ingredient staples (plain creatine, a single-ingredient protein, fish oil, vitamin D, magnesium) are is_blend false.
- caffeine_mg_per_serving: only if the number is printed. Do not infer it.
- est_monthly_cost: null unless a price is visibly printed, or you are genuinely confident of a category-typical monthly cost.
- If the image is not a supplement label, or is too blurry/dark to read, set unreadable true and read_confidence "low".

Output JSON matching the provided schema.`;

app.post('/api/supplement/label', aiLimiter, optionalAuth, async (req, res) => {
  try {
    const { photoBase64, photoMime, panelBase64, panelMime } = req.body || {};
    const attemptId = String(req.body?.attemptId || '');
    const cached = getCachedAttempt(attemptId);
    if (cached) return res.status(cached.status).json(cached.body);

    if (!photoBase64 || !photoMime) {
      return res.status(400).json({ error: 'Missing photoBase64 or photoMime' });
    }

    const userContent = [
      { type: 'image', source: { type: 'base64', media_type: photoMime, data: photoBase64 } },
      { type: 'text', text: 'This is the FRONT label of one supplement product.' },
    ];
    if (panelBase64 && panelMime) {
      userContent.push({ type: 'image', source: { type: 'base64', media_type: panelMime, data: panelBase64 } });
      userContent.push({ type: 'text', text: 'This second image is the ingredients / Supplement Facts panel for the SAME product — read per-ingredient doses from it.' });
    }
    userContent.push({ type: 'text', text: 'Read this product. Output JSON matching the provided schema.' });

    let analysis;
    try {
      analysis = await callCounselSeat(SUPPLEMENT_LABEL_PROMPT, userContent, SUPPLEMENT_LABEL_SCHEMA, 1500);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Could not read the label. Please retake the photo.' });
    }
    // If a panel was supplied, the doses should now be legible — don't keep asking.
    if (panelBase64 && panelMime) analysis.needs_panel = false;

    const payload = { analysis };
    cacheAttempt(attemptId, 200, payload);
    res.json(payload);
  } catch (err) {
    console.error('supplement label error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ── Supplement Audit: "Recommend a Brand" (Phase 6) ───────────────────
// On-demand, members-only, uncapped. Keeps the main audit unbiased (generic
// ingredients); this names a specific product only when the user asks. Response
// shape is stable so a "where to buy" / affiliate layer can bolt on later.
const SUPPLEMENT_BRAND_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['brand_pick', 'product_name', 'why', 'price_note', 'runner_up'],
  properties: {
    brand_pick: { type: 'string', description: 'The recommended brand.' },
    product_name: { type: 'string', description: 'The specific product name for this ingredient + dose.' },
    why: { type: 'string', description: 'One or two sentences: why this pick — third-party testing, single-ingredient, value.' },
    price_note: { type: 'string', description: 'Rough price/value note. Always remind that prices change.' },
    runner_up: { type: 'string', description: 'A widely available alternative brand + product.' },
  },
};

const SUPPLEMENT_BRAND_PROMPT = `You are a no-nonsense supplement buyer for a fitness app. The user has been recommended a GENERIC ingredient at a specific dose and now wants a specific product to buy.

Rules:
- Recommend a widely available, reputable brand that is THIRD-PARTY TESTED (NSF Certified for Sport, Informed Sport/Choice, USP, or equivalent) for this exact ingredient at this dose.
- Strongly prefer SINGLE-INGREDIENT products over blends — the user wants this ingredient, not a proprietary mix.
- Give one runner-up that is also easy to find (a major retailer / Amazon-tier brand).
- Prices change and availability varies — always say so and tell the user to compare at purchase.
- No affiliate links, no coupon codes, no invented SKUs. If you are not confident a specific product exists, describe the category leader instead of inventing a name.

Output JSON matching the provided schema.`;

app.post('/api/supplement/brand', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'Membership required', needsMembership: true });
    }
    const ingredient = String(req.body?.ingredient || '').trim().slice(0, 120);
    const dose = String(req.body?.dose || '').trim().slice(0, 60);
    if (!ingredient) return res.status(400).json({ error: 'Missing ingredient' });

    const content = [{ type: 'text', text: `Recommend a specific product for:\nIngredient: ${ingredient}\nDose: ${dose || 'a standard effective dose'}\n\nOutput JSON matching the provided schema.` }];
    let pick;
    try {
      pick = await callCounselSeat(SUPPLEMENT_BRAND_PROMPT, content, SUPPLEMENT_BRAND_SCHEMA, 800);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Could not fetch a brand pick. Please try again.' });
    }
    res.json({ ingredient, dose, pick });
  } catch (err) {
    console.error('supplement brand error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
//  AI SLEEP COACH — the "Go Hard Anyway" briefing
// ============================================================
// Whatever the sleep data says, the verdict is GO HARD — the sleep only
// changes the justification and the tactics. Bad night → watch eating + stay
// tight; great night → push a higher deficit. Trend escalation touches the
// sleep fixes only, never the gym verdict.

const SLEEP_COACH_SYSTEM_PROMPT = `You are the AI Sleep Coach for a fitness app called Abs By AI. Sleep trackers tell people to "take it easy" after a bad night — you do the opposite. Sleep data tells the user HOW to attack the day, never WHETHER to.

THE IRON RULE (never break it):
- verdict is ALWAYS "GO HARD". Every briefing tells the user to go extra hard in the gym today. There is NO rest-day, "listen to your body", or "take it easy" verdict, ever. Do not hedge the gym verdict for any sleep score.

Persona: high-energy but evidence-grounded coach. Ground the justification in the real research framing: a single night of short sleep impairs perceived effort and mood far more than actual strength or power output, and hard morning training plus daylight exposure are among the strongest levers for the NEXT night's sleep.

Briefing structure (every day, same skeleton): acknowledge the sleep honestly → justify going extra hard anyway → tactical adjustments → tonight's fix.

BAD night (short, fragmented, low score, or feel 1-2):
- Justification: one bad night doesn't reduce strength; training hard today is the fastest fix for tonight's sleep.
- Tactics MUST include: "watch your eating today" (poor sleep spikes cravings and hunger hormones — name specific traps) and "stay tight" (form focus — reaction time is slightly down, so control every rep).
- sleep_quality: "bad".

GREAT night (long, solid, high score, or feel 4-5):
- This is the day to really push a HIGHER deficit: fully recovered, so push harder in the gym AND eat leaner today. Say that explicitly.
- sleep_quality: "great".

OK night: still go hard; pick the most useful tactical angle. sleep_quality: "ok".

TREND (when a multi-day history is provided): a clear downtrend gets honest escalation on the SLEEP FIXES in trend_note (e.g. "a 2-week average like this will stall fat loss — here's the protocol"), but the gym verdict stays GO HARD. If the trend is fine, trend_note is an empty string.

SAFETY VALVE (kept minimal): only if the data/notes suggest possible sleep-disorder red flags (loud snoring + gasping/choking awake + chronically unrefreshing sleep despite adequate hours), put a single calm sentence in red_flag saying it's worth mentioning to a doctor. Otherwise red_flag is an empty string. Never diagnose.

TONIGHT: 2-4 concrete, personalized fixes for tonight's sleep (timing anchors beat vague advice — compute a real target bedtime from their data when you can).

SCREENSHOT INPUT: when the user message contains a screenshot of a sleep tracker (Oura, Whoop, Apple Health, Fitbit, Garmin, etc.), read every number you can see and fill "parsed" with what you found (0 or "" for anything not visible). Base the briefing on those numbers. If the image is NOT a sleep-data screen, set parsed.duration_min to 0 and say in headline that you couldn't read sleep data from the image, but still deliver a usable go-hard briefing from whatever context you have.

MANUAL INPUT: normalize bedtime/wake time into parsed (compute duration_min from the times).

Voice: punchy, second person, zero fluff. Numbers over vibes. Never judgmental — the bad night is an opportunity, not a failure.`;

const SLEEP_BRIEFING_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['verdict', 'headline', 'sleep_quality', 'justification', 'tactics', 'tonight', 'trend_note', 'red_flag', 'parsed'],
  properties: {
    verdict: { type: 'string', description: 'Always exactly "GO HARD".' },
    headline: { type: 'string', description: 'One punchy sentence: the sleep acknowledged + the go-hard call. e.g. "5h 40m — rough. Perfect day to prove it doesn\'t own you."' },
    sleep_quality: { type: 'string', enum: ['bad', 'ok', 'great'], description: 'Your overall read of last night.' },
    justification: { type: 'string', description: '2-4 sentences: why going extra hard TODAY is the right call given this exact sleep, grounded in the research framing.' },
    tactics: { type: 'array', items: { type: 'string' }, description: '3-5 tactical adjustments for today. Bad night MUST include the watch-your-eating and stay-tight items. Great night MUST include pushing a higher deficit.' },
    tonight: { type: 'array', items: { type: 'string' }, description: "2-4 concrete fixes for tonight's sleep, personalized to their numbers." },
    trend_note: { type: 'string', description: 'Escalation on the sleep fixes when a multi-day downtrend shows; empty string otherwise.' },
    red_flag: { type: 'string', description: 'One "worth mentioning to a doctor" sentence ONLY for genuine sleep-disorder red flags; empty string otherwise.' },
    parsed: {
      type: 'object',
      additionalProperties: false,
      required: ['duration_min', 'bedtime', 'waketime', 'wakeups', 'feel_score', 'tracker_score', 'hrv', 'rhr', 'stages'],
      properties: {
        duration_min: { type: 'integer', description: 'Total sleep in minutes; 0 if unknown.' },
        bedtime: { type: 'string', description: 'e.g. "11:20 PM"; empty if unknown.' },
        waketime: { type: 'string', description: 'e.g. "6:45 AM"; empty if unknown.' },
        wakeups: { type: 'integer', description: 'Number of wake-ups; 0 if unknown.' },
        feel_score: { type: 'integer', description: 'User-reported feel 1-5; 0 if not given.' },
        tracker_score: { type: 'integer', description: 'Tracker sleep score (e.g. Oura 0-100); 0 if unknown.' },
        hrv: { type: 'integer', description: 'HRV in ms; 0 if unknown.' },
        rhr: { type: 'integer', description: 'Resting heart rate in bpm; 0 if unknown.' },
        stages: { type: 'string', description: 'e.g. "1h52m deep · 1h40m REM"; empty if unknown.' },
      },
    },
  },
};

// Non-member preview: the verdict, headline, honest read, and parsed numbers
// are free (that's the hook — "it read my ring"); the tactics, tonight
// protocol, and trend coaching are members-only. red_flag is safety info and
// is never paywalled.
function stripBriefingForPreview(briefing) {
  return {
    verdict: briefing.verdict,
    headline: briefing.headline,
    sleep_quality: briefing.sleep_quality,
    justification: briefing.justification,
    red_flag: briefing.red_flag || '',
    parsed: briefing.parsed,
    locked: true,
    tactics_count: (briefing.tactics || []).length,
    tonight_count: (briefing.tonight || []).length,
  };
}

// Today's normalized sleep entry for cross-feature prompts. Null when the user
// hasn't checked in today (or isn't logged in / no DB).
async function getTodaysSleep(userId) {
  if (!db || !userId) return null;
  try {
    const { rows } = await db.query(
      'SELECT data, briefing FROM sleep_entries WHERE user_id = $1 AND entry_date = CURRENT_DATE',
      [userId]
    );
    if (!rows.length) return null;
    const quality = rows[0].briefing?.sleep_quality || null;
    return { quality, data: rows[0].data || {}, briefing: rows[0].briefing || null };
  } catch (e) {
    console.warn('getTodaysSleep error:', e.message);
    return null;
  }
}

// One prompt line per feature, per Dan's locked cross-feature rules.
function sleepContextForTrainer(sleep) {
  if (!sleep?.quality) return '';
  if (sleep.quality === 'bad') {
    return `\nSLEEP CONTEXT (from today's sleep check-in): the user slept POORLY last night. Extend the warm-up by ~5 minutes with extra activation work, but the workout does NOT get shorter or lighter — same volume, same intensity. Cue extra form focus.`;
  }
  if (sleep.quality === 'great') {
    return `\nSLEEP CONTEXT (from today's sleep check-in): the user slept GREAT last night — fully recovered. This is a day they can push extra hard.`;
  }
  return '';
}
function sleepContextForNutrition(sleep) {
  if (!sleep?.quality) return '';
  if (sleep.quality === 'bad') {
    return `\nSLEEP CONTEXT (from today's sleep check-in): the user slept POORLY last night, which spikes cravings today. For TODAY's guidance: raise calories slightly via PROTEIN ONLY — zero added carbs (the protein blunts the cravings). Mention this explicitly.`;
  }
  if (sleep.quality === 'great') {
    return `\nSLEEP CONTEXT (from today's sleep check-in): the user slept GREAT last night — fully recovered. Suggest running a slightly higher calorie deficit today; mention it explicitly.`;
  }
  return '';
}

// pg returns DATE columns as JS Date objects; normalize to "YYYY-MM-DD".
function sleepDateStr(d) {
  return d instanceof Date ? d.toISOString().slice(0, 10) : String(d).slice(0, 10);
}

function formatSleepHistoryLine(row) {
  const d = row.data || {};
  const parts = [sleepDateStr(row.entry_date)];
  if (d.duration_min) parts.push(`${Math.floor(d.duration_min / 60)}h${String(d.duration_min % 60).padStart(2, '0')}m`);
  if (d.tracker_score) parts.push(`score ${d.tracker_score}`);
  if (d.feel_score) parts.push(`felt ${d.feel_score}/5`);
  if (d.wakeups) parts.push(`${d.wakeups} wake-up${d.wakeups === 1 ? '' : 's'}`);
  return parts.join(' · ');
}

// Morning check-in → Go Hard briefing. Manual form or tracker screenshot
// (one vision call extracts the numbers AND writes the briefing). Free preview
// for everyone; tactics/tonight/trend are members-only. Saved per-day (upsert)
// for logged-in users so re-submitting redoes the check-in.
app.post('/api/sleep/checkin', aiLimiter, optionalAuth, async (req, res) => {
  try {
    const { manual, screenshotBase64, screenshotMime, note } = req.body || {};
    const isScreenshot = !!(screenshotBase64 && screenshotMime);
    if (!isScreenshot && !manual) {
      return res.status(400).json({ error: 'Send either manual check-in fields or a tracker screenshot.' });
    }

    const userContent = [];
    if (isScreenshot) {
      userContent.push({ type: 'image', source: { type: 'base64', media_type: String(screenshotMime), data: String(screenshotBase64) } });
      userContent.push({ type: 'text', text: "Screenshot of the user's sleep tracker from last night. Read every number you can see, fill parsed, and write today's Go Hard briefing." });
    } else {
      const m = {
        bedtime: String(manual.bedtime || '').slice(0, 20),
        waketime: String(manual.waketime || '').slice(0, 20),
        wakeups: Math.max(0, Math.min(20, parseInt(manual.wakeups, 10) || 0)),
        feel_score: Math.max(1, Math.min(5, parseInt(manual.feel_score, 10) || 3)),
      };
      if (!m.bedtime || !m.waketime) {
        return res.status(400).json({ error: 'Bedtime and wake time are required.' });
      }
      userContent.push({
        type: 'text',
        text: `Manual morning check-in:\n- Went to bed: ${m.bedtime}\n- Woke up: ${m.waketime}\n- Wake-ups during the night: ${m.wakeups}\n- How they feel (1-5, 5 = fully rested): ${m.feel_score}\n\nNormalize these into parsed (compute duration_min from the times) and write today's Go Hard briefing.`,
      });
    }
    if (note) userContent.push({ type: 'text', text: `User note: "${String(note).slice(0, 300)}"` });

    // Trend context: the last 14 saved nights (excluding today).
    if (req.user && db) {
      try {
        const { rows } = await db.query(
          'SELECT entry_date, data FROM sleep_entries WHERE user_id = $1 AND entry_date < CURRENT_DATE ORDER BY entry_date DESC LIMIT 14',
          [req.user.id]
        );
        if (rows.length) {
          userContent.push({
            type: 'text',
            text: `Recent sleep history (most recent first) — use it for trend_note:\n${rows.map(formatSleepHistoryLine).join('\n')}`,
          });
        }
      } catch (e) { console.warn('sleep history fetch error:', e.message); }

      // Shared member profile as additive background (age/goal help the coach
      // pitch tonight's protocol to the person). The user's own inputs win.
      const pc = profileContextBlock(await readProfile(req.user.id));
      if (pc) userContent.push({ type: 'text', text: pc });
    }

    let briefing;
    try {
      briefing = await callTrainerModel(SLEEP_COACH_SYSTEM_PROMPT, userContent, SLEEP_BRIEFING_SCHEMA);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Briefing generation failed. Please try again.' });
    }
    if (!briefing?.headline || !Array.isArray(briefing.tactics)) {
      return res.status(502).json({ error: 'Model returned an unusable briefing. Please try again.' });
    }
    briefing.verdict = 'GO HARD'; // the iron rule, enforced server-side

    let member = false;
    let saved = false;
    if (req.user && db) {
      member = isActiveMembership(req.user);
      try {
        await db.query(
          `INSERT INTO sleep_entries (user_id, entry_date, source, data, briefing)
           VALUES ($1, CURRENT_DATE, $2, $3, $4)
           ON CONFLICT (user_id, entry_date)
           DO UPDATE SET source = EXCLUDED.source, data = EXCLUDED.data, briefing = EXCLUDED.briefing, created_at = now()`,
          [req.user.id, isScreenshot ? 'screenshot' : 'manual', JSON.stringify(briefing.parsed || {}), JSON.stringify(briefing)]
        );
        saved = true;
      } catch (e) { console.error('sleep entry save error:', e.message); }
    }

    res.json({
      saved,
      locked: !member,
      briefing: member ? { ...briefing, locked: false } : stripBriefingForPreview(briefing),
    });
  } catch (err) {
    console.error('sleep checkin error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Last 30 nights for the trend strip + restoring today's briefing.
app.get('/api/sleep/history', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT entry_date, source, data, briefing FROM sleep_entries WHERE user_id = $1 ORDER BY entry_date DESC LIMIT 30',
      [req.user.id]
    );
    const userRow = await getUserRow(req.user.id);
    const member = isActiveMembership(userRow);
    res.json({
      locked: !member,
      entries: rows.map((r) => ({
        date: sleepDateStr(r.entry_date),
        source: r.source,
        data: r.data,
        briefing: r.briefing
          ? (member ? { ...r.briefing, locked: false } : stripBriefingForPreview(r.briefing))
          : null,
      })),
    });
  } catch (e) {
    console.error('sleep history error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ============================================================
// WEIGHT & PROGRESS LOG — daily weight, trend math, weekly photo day
// ============================================================
// Trend weight = trailing-7-day rolling mean of raw weights (per handoff:
// simple mean, no exponential smoothing in v1). All math in the user's
// current unit; mixed-unit history converted at read time.
const LB_PER_KG = 2.20462;

function toUnit(weight, fromUnit, toUnitStr) {
  if (fromUnit === toUnitStr) return weight;
  return fromUnit === 'kg' ? weight * LB_PER_KG : weight / LB_PER_KG;
}

function dateStr(d) {
  return d instanceof Date ? d.toISOString().slice(0, 10) : String(d).slice(0, 10);
}

// rows: [{entry_date, weight, unit, flags}] ascending by date.
// Returns { entries: [{date, weight, trend, flags}], rate, consistency }.
function computeTrend(rows, unit) {
  const entries = rows.map((r) => ({
    date: dateStr(r.entry_date),
    weight: Math.round(toUnit(Number(r.weight), r.unit, unit) * 10) / 10,
    flags: r.flags || [],
  }));
  const byDate = new Map(entries.map((e) => [e.date, e.weight]));
  for (const e of entries) {
    // Mean of raw weights in the trailing 7-day calendar window.
    const end = new Date(e.date + 'T00:00:00Z');
    let sum = 0, n = 0;
    for (let i = 0; i < 7; i++) {
      const d = new Date(end); d.setUTCDate(d.getUTCDate() - i);
      const w = byDate.get(d.toISOString().slice(0, 10));
      if (w !== undefined) { sum += w; n++; }
    }
    e.trend = n ? Math.round((sum / n) * 10) / 10 : null;
  }

  // Rate of change: linear-regression slope of trend over the last 30 days,
  // expressed per week. Needs ≥7 logged days in the window, else null.
  let rate = null;
  const today = new Date();
  const cutoff = new Date(today); cutoff.setUTCDate(cutoff.getUTCDate() - 30);
  const win = entries.filter((e) => new Date(e.date + 'T00:00:00Z') >= cutoff && e.trend != null);
  if (win.length >= 7) {
    const xs = win.map((e) => new Date(e.date + 'T00:00:00Z').getTime() / 86400000);
    const ys = win.map((e) => e.trend);
    const mx = xs.reduce((a, b) => a + b, 0) / xs.length;
    const my = ys.reduce((a, b) => a + b, 0) / ys.length;
    let num = 0, den = 0;
    for (let i = 0; i < xs.length; i++) { num += (xs[i] - mx) * (ys[i] - my); den += (xs[i] - mx) ** 2; }
    if (den > 0) rate = Math.round((num / den) * 7 * 100) / 100; // per week
  }

  // Soft consistency: logged days in the last 14.
  const cut14 = new Date(today); cut14.setUTCDate(cut14.getUTCDate() - 13);
  const logged = entries.filter((e) => new Date(e.date + 'T00:00:00Z') >= cut14).length;

  return { entries, rate, consistency: { logged, window: 14 } };
}

const VALID_FLAGS = new Set(['high-sodium', 'poor-sleep', 'period', 'traveling']);

async function progressSummary(userId, unit) {
  const { rows } = await db.query(
    'SELECT entry_date, weight, unit, flags FROM weight_logs WHERE user_id = $1 ORDER BY entry_date ASC',
    [userId]
  );
  const effectiveUnit = unit || rows[rows.length - 1]?.unit || 'lb';
  const trend = computeTrend(rows, effectiveUnit);
  const { rows: photos } = await db.query(
    'SELECT id, entry_date, thumb_front, waist, waist_unit, (recap IS NOT NULL) AS has_recap FROM progress_entries WHERE user_id = $1 ORDER BY entry_date ASC',
    [userId]
  );
  const { rows: u } = await db.query('SELECT photo_day, weigh_reminder FROM users WHERE id = $1', [userId]);
  return {
    ...trend,
    unit: effectiveUnit,
    photoDay: u[0]?.photo_day ?? null,
    weighReminder: !!u[0]?.weigh_reminder,
    photoTimeline: photos.map((p) => ({
      id: p.id, date: dateStr(p.entry_date), thumb: p.thumb_front || null,
      waist: p.waist != null ? Number(p.waist) : null, waistUnit: p.waist_unit || 'in', hasRecap: !!p.has_recap,
    })),
  };
}

app.post('/api/progress/weight', requireAuth, async (req, res) => {
  const weight = Number(req.body?.weight);
  const unit = req.body?.unit === 'kg' ? 'kg' : 'lb';
  const date = DATE_RE.test(String(req.body?.date || '')) ? req.body.date : new Date().toISOString().slice(0, 10);
  const flags = Array.isArray(req.body?.flags) ? req.body.flags.filter((f) => VALID_FLAGS.has(f)) : [];
  if (!Number.isFinite(weight) || weight < 40 || weight > 1000) {
    return res.status(400).json({ error: 'Enter a valid weight.' });
  }
  try {
    await db.query(
      `INSERT INTO weight_logs (user_id, entry_date, weight, unit, flags) VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (user_id, entry_date) DO UPDATE SET weight = $3, unit = $4, flags = $5`,
      [req.user.id, date, weight, unit, JSON.stringify(flags)]
    );
    // Write-back: keep the shared profile's weight fresh from a today weigh-in
    // (factual; skip backdated entries so an old log can't clobber current weight).
    if (date === new Date().toISOString().slice(0, 10)) {
      writeProfileMerge(req.user.id, { weight, weightUnit: unit }, 'progress').catch(() => {});
    }
    res.json(await progressSummary(req.user.id, unit));
  } catch (e) {
    console.error('progress weight error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/progress/summary', requireAuth, async (req, res) => {
  try {
    const unit = req.query.unit === 'kg' ? 'kg' : req.query.unit === 'lb' ? 'lb' : null;
    res.json(await progressSummary(req.user.id, unit));
  } catch (e) {
    console.error('progress summary error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/progress/photo', requireAuth, async (req, res) => {
  const { photoFront, photoSide, photoBack, thumbFront, waist, waistUnit } = req.body || {};
  const date = DATE_RE.test(String(req.body?.date || '')) ? req.body.date : new Date().toISOString().slice(0, 10);
  if (!String(photoFront || '').startsWith('data:image/')) {
    return res.status(400).json({ error: 'A front photo is required.' });
  }
  const w = waist != null && waist !== '' ? Number(waist) : null;
  if (w != null && (!Number.isFinite(w) || w < 10 || w > 200)) {
    return res.status(400).json({ error: 'Enter a valid waist measurement.' });
  }
  try {
    await db.query(
      `INSERT INTO progress_entries (user_id, entry_date, photo_front, thumb_front, photo_side, photo_back, waist, waist_unit)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
       ON CONFLICT (user_id, entry_date) DO UPDATE SET photo_front = $3, thumb_front = $4, photo_side = $5, photo_back = $6, waist = $7, waist_unit = $8, recap = NULL`,
      [req.user.id, date, photoFront, String(thumbFront || '') || null,
       String(photoSide || '').startsWith('data:image/') ? photoSide : null,
       String(photoBack || '').startsWith('data:image/') ? photoBack : null,
       w, waistUnit === 'cm' ? 'cm' : 'in']
    );
    res.json(await progressSummary(req.user.id, null));
  } catch (e) {
    console.error('progress photo error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Full photos are heavy — fetched lazily per entry, never in list payloads.
app.get('/api/progress/photo/:id', requireAuth, async (req, res) => {
  try {
    const { rows } = await db.query(
      'SELECT id, entry_date, photo_front, photo_side, photo_back, waist, waist_unit, recap FROM progress_entries WHERE id = $1 AND user_id = $2',
      [parseInt(req.params.id, 10) || 0, req.user.id]
    );
    if (!rows.length) return res.status(404).json({ error: 'Not found' });
    const r = rows[0];
    res.json({
      id: r.id, date: dateStr(r.entry_date), photoFront: r.photo_front, photoSide: r.photo_side,
      photoBack: r.photo_back, waist: r.waist != null ? Number(r.waist) : null, waistUnit: r.waist_unit, recap: r.recap,
    });
  } catch (e) {
    console.error('progress photo fetch error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/progress/settings', requireAuth, async (req, res) => {
  const photoDay = req.body?.photoDay;
  const weighReminder = !!req.body?.weighReminder;
  const pd = Number.isInteger(photoDay) && photoDay >= 0 && photoDay <= 6 ? photoDay : null;
  try {
    await db.query('UPDATE users SET photo_day = $1, weigh_reminder = $2 WHERE id = $3', [pd, weighReminder, req.user.id]);
    res.json({ ok: true, photoDay: pd, weighReminder });
  } catch (e) {
    console.error('progress settings error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// ── AI weekly recap (members) ──
const PROGRESS_RECAP_SCHEMA = {
  type: 'object',
  properties: {
    headline: { type: 'string', description: 'One punchy sentence — the week in a line.' },
    week_story: { type: 'string', description: '2-3 short paragraphs interpreting the TREND (never the daily number), tying in waist, flags, sleep, and training adherence.' },
    scale_vs_waist: { type: 'string', description: 'One paragraph: what scale + waist together say. If weight stalled but waist dropped, call out recomposition as a win.' },
    adjustments: { type: 'array', items: { type: 'string' }, description: '0-3 concrete, encouraging adjustments. Empty if the plan is working.' },
    photo_note: { type: 'string', description: 'Pose/lighting-consistency coaching for next photo day (generic — no image analysis).' },
    encouragement: { type: 'string', description: 'Closing line in the go-hard coach voice.' },
  },
  required: ['headline', 'week_story', 'scale_vs_waist', 'adjustments', 'photo_note', 'encouragement'],
};

const PROGRESS_RECAP_SYSTEM_PROMPT = `You are the Abs by AI progress coach — the same evidence-grounded, go-hard voice as the AI Trainer. You are writing the user's WEEKLY PROGRESS RECAP on their photo day.

Iron rules:
- Interpret the 7-day TREND weight, never a single daily reading. If contextual flags (high sodium, poor sleep, period, traveling) explain a spike, say so explicitly and defuse it.
- If weight stalls but waist drops → that is recomposition. Call it a WIN, loudly.
- If both weight and waist have stalled 2+ weeks → give a concrete, specific adjustment referencing their program or meal plan. Stay encouraging.
- NEVER recommend under-eating, punishing cardio, or weighing more often.
- Numbers: quote the trend weight, rate of change, and waist delta exactly as given.
Output strict JSON matching the provided schema.`;

async function buildRecapContext(userId) {
  const summary = await progressSummary(userId, null);
  const lines = [];
  const last = summary.entries[summary.entries.length - 1];
  if (last) lines.push(`Current 7-day trend weight: ${last.trend} ${summary.unit} (latest raw: ${last.weight} ${summary.unit} on ${last.date}).`);
  if (summary.rate != null) lines.push(`Rate of change: ${summary.rate > 0 ? '+' : ''}${summary.rate} ${summary.unit}/week over the last 30 days.`);
  lines.push(`Consistency: logged ${summary.consistency.logged} of the last ${summary.consistency.window} days.`);
  const recent = summary.entries.slice(-30);
  lines.push(`Last ${recent.length} weigh-ins (date, raw, trend, flags): ${recent.map((e) => `${e.date} ${e.weight}/${e.trend}${e.flags.length ? ' [' + e.flags.join(',') + ']' : ''}`).join('; ')}`);
  const waists = summary.photoTimeline.filter((p) => p.waist != null).slice(-6);
  if (waists.length) lines.push(`Waist history: ${waists.map((p) => `${p.date}: ${p.waist} ${p.waistUnit}`).join('; ')}`);

  // Cross-feature context: training adherence + last week of sleep.
  try {
    const { rows } = await db.query('SELECT progress FROM programs WHERE user_id = $1 ORDER BY id DESC LIMIT 1', [userId]);
    if (rows.length) {
      const done = Object.values(rows[0].progress || {}).filter(Boolean).length;
      lines.push(`Training program: active, ${done} workouts checked off so far.`);
    }
  } catch (e) {}
  try {
    const { rows } = await db.query(
      'SELECT entry_date, data FROM sleep_entries WHERE user_id = $1 ORDER BY entry_date DESC LIMIT 7', [userId]
    );
    if (rows.length) lines.push(`Sleep, last ${rows.length} nights: ${rows.map(formatSleepHistoryLine).join(' | ')}`);
  } catch (e) {}
  return lines.join('\n');
}

app.post('/api/progress/recap', aiLimiter, requireAuth, async (req, res) => {
  try {
    const userRow = await getUserRow(req.user.id);
    if (!isActiveMembership(userRow)) {
      return res.status(402).json({ error: 'The weekly recap is a member feature.', needsMembership: true });
    }
    const { rows } = await db.query(
      'SELECT id, recap FROM progress_entries WHERE user_id = $1 ORDER BY entry_date DESC LIMIT 1',
      [req.user.id]
    );
    if (!rows.length) return res.status(400).json({ error: 'Log a progress photo first — the recap ties your week to photo day.' });
    if (rows[0].recap && !req.body?.force) return res.json({ recap: rows[0].recap });

    const context = await buildRecapContext(req.user.id);
    const recap = await callTrainerModel(
      PROGRESS_RECAP_SYSTEM_PROMPT,
      [{ type: 'text', text: `Here is the user's progress data:\n${context}\n\nWrite this week's recap.` }],
      PROGRESS_RECAP_SCHEMA
    );
    if (!recap?.headline) return res.status(502).json({ error: 'Recap generation failed. Please try again.' });
    await db.query('UPDATE progress_entries SET recap = $1 WHERE id = $2', [JSON.stringify(recap), rows[0].id]);
    res.json({ recap });
  } catch (e) {
    if (e.status) return res.status(e.status).json({ error: e.message });
    console.error('progress recap error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Cross-feature: one prompt line for Trainer/Nutritionist (same pattern as sleep).
async function getWeightContext(userId) {
  if (!db || !userId) return '';
  try {
    const s = await progressSummary(userId, null);
    const last = s.entries[s.entries.length - 1];
    if (!last?.trend) return '';
    let line = `\nWEIGHT CONTEXT (from the user's progress log): 7-day trend weight is ${last.trend} ${s.unit}`;
    if (s.rate != null) line += `, moving ${s.rate > 0 ? '+' : ''}${s.rate} ${s.unit}/week`;
    const waists = s.photoTimeline.filter((p) => p.waist != null);
    if (waists.length >= 2) {
      const delta = Math.round((waists[waists.length - 1].waist - waists[0].waist) * 10) / 10;
      line += `; waist ${delta <= 0 ? 'down' : 'up'} ${Math.abs(delta)} ${waists[waists.length - 1].waistUnit} since ${waists[0].date}`;
    }
    line += s.rate != null && s.rate < 0
      ? ' — the plan is working; do NOT cut calories further.'
      : '.';
    return line;
  } catch (e) {
    console.warn('getWeightContext error:', e.message);
    return '';
  }
}

// ============================================================
// DAILY COACH BRIEF — one card, one coach voice, every morning
// ============================================================
// Fuses today's sleep check-in, the next workout, meal-plan targets, and the
// weight trend into one short morning briefing on the member hub. Facts are
// deterministic (free for all logged-in users); the AI coach text is
// members-only. Cached per user-day; regenerated only when the underlying
// facts change (new sleep check-in, workout done, new weigh-in).

const COACH_BRIEF_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['headline', 'sleep_note', 'workout_note', 'nutrition_note', 'weight_note', 'focus'],
  properties: {
    headline: { type: 'string', description: "One energetic opening line for today, max ~14 words, built on the single most salient fact. Address the user as 'you'." },
    sleep_note: { type: 'string', description: 'One short sentence (max ~20 words) on last night and what it means for today. Empty string when there is no sleep data.' },
    workout_note: { type: 'string', description: "One short sentence firing them up for today's SPECIFIC workout (use its focus). Empty string when there is no program or the workout is already done." },
    nutrition_note: { type: 'string', description: "One short sentence on hitting today's calorie/protein targets, quoting the numbers. Empty string when there is no meal plan." },
    weight_note: { type: 'string', description: 'One short sentence interpreting the TREND weight (never a daily reading). Empty string when there is no weight data.' },
    focus: { type: 'string', description: 'THE one thing to nail today, chosen from the facts — one punchy sentence.' },
  },
};

const COACH_BRIEF_SYSTEM_PROMPT = `You are the Abs by AI head coach writing the user's DAILY MORNING BRIEF — the same warm, direct, evidence-grounded go-hard voice as the AI Trainer and Sleep Coach. One coach, one morning message.

Iron rules:
- Use ONLY the facts provided. Never invent data, numbers, or history. Quote numbers exactly as given.
- Bad sleep NEVER shrinks the workout: the rule is a longer warm-up and extra form focus — same volume, same intensity. Great sleep = green light to push.
- Weight: interpret the 7-day TREND only, never a single daily reading. A falling trend means the plan is working — say so and never suggest eating less.
- NEVER recommend under-eating, punishing cardio, or extra weigh-ins.
- If the workout is already done today, celebrate it in the headline or focus instead of prescribing it again.
- Each note is ONE short sentence. A section with no data gets an empty string — never apologize for missing data or tell them to go log things in more than one gentle nudge.
- focus: pick the single highest-leverage action for TODAY (usually the workout; protein if nutrition is the weak spot; the check-in if the block is complete).
Output strict JSON matching the provided schema.`;

// Server-side twin of the client's dayIsComplete(): first day whose main +
// abs-finisher sets aren't all checked off. progress = { done, swaps, dates }.
function firstIncompleteDay(program, progress) {
  const done = (progress && progress.done) || {};
  const startDow = parseInt(program.start_dow, 10);
  const skipEarly = Number.isFinite(startDow) && startDow >= 2 && startDow <= 7;
  for (const week of program.weeks || []) {
    for (const day of week.days || []) {
      // Week 1 of a mid-week block begins on the day it was generated.
      if (skipEarly && week.week === 1 && day.day < startDow) continue;
      const complete = [['m', day.main], ['a', day.abs_finisher]].every(([sec, list]) =>
        (list || []).every((ex, i) => {
          const sets = ex.sets || 1;
          for (let s = 0; s < sets; s++) {
            if (!done[`w${week.week}d${day.day}${sec}${i}s${s}`]) return false;
          }
          return true;
        })
      );
      if (!complete) {
        return {
          week: week.week, day: day.day, focus: day.focus || '', theme: week.theme || '',
          exercises: (day.main || []).length + (day.abs_finisher || []).length,
        };
      }
    }
  }
  return null; // whole block checked off
}

// Gather every fact the brief needs. Returns deterministic facts for the card,
// prompt lines for the model, and a fingerprint so the cache regenerates only
// when something actually changed.
async function buildBriefFacts(userId, dayStr) {
  const facts = { sleep: null, workout: null, nutrition: null, weight: null };
  const lines = [`Today is ${dayStr}.`];

  const sleep = await getTodaysSleep(userId);
  if (sleep?.quality) {
    facts.sleep = { quality: sleep.quality, headline: sleep.briefing?.headline || '' };
    lines.push(`SLEEP: last night was "${sleep.quality}"${sleep.briefing?.headline ? ` — sleep coach said: "${sleep.briefing.headline}"` : ''}.`);
  }

  try {
    const { rows } = await db.query(
      'SELECT block_number, program, progress FROM programs WHERE user_id = $1 ORDER BY id DESC LIMIT 1', [userId]
    );
    if (rows.length) {
      const { program, progress, block_number } = rows[0];
      const doneToday = !!(progress?.dates && progress.dates[dayStr]);
      const next = firstIncompleteDay(program, progress || {});
      const stageLabel = STAGES[programStage(program)]?.label || '';
      facts.workout = {
        blockNumber: block_number, doneToday, stageLabel,
        next: next ? { week: next.week, day: next.day, focus: next.focus, exercises: next.exercises } : null,
        blockComplete: !next,
      };
      if (doneToday) lines.push(`WORKOUT: already DONE today. ✓`);
      else if (next) lines.push(`WORKOUT: today is Block ${block_number}, Week ${next.week}, Day ${next.day} — "${next.focus}" (${next.exercises} exercises, ${stageLabel}).`);
      else lines.push(`WORKOUT: the 4-week block is fully checked off — their week-4 check-in builds the next block.`);
    }
  } catch (e) { console.warn('brief program fetch error:', e.message); }

  try {
    const { rows } = await db.query(
      'SELECT plan FROM meal_plans WHERE user_id = $1 ORDER BY id DESC LIMIT 1', [userId]
    );
    const t = rows[0]?.plan?.targets;
    if (t?.daily_calories) {
      let logged = null;
      try {
        const { rows: meals } = await db.query('SELECT totals FROM meals WHERE user_id = $1 AND date = $2', [userId, dayStr]);
        if (meals.length) {
          logged = {
            calories: Math.round(meals.reduce((s, m) => s + (Number(m.totals?.calories) || 0), 0)),
            protein_g: Math.round(meals.reduce((s, m) => s + (Number(m.totals?.protein_g) || 0), 0)),
            meals: meals.length,
          };
        }
      } catch (e) {}
      facts.nutrition = { calories: t.daily_calories, protein_g: t.protein_g, mode: t.calories_mode || 'ceiling', logged };
      lines.push(`NUTRITION: daily target ${t.daily_calories} cal (${t.calories_mode === 'floor' ? 'eat AT LEAST — GLP-1 floor mode' : 'ceiling'}) and ${t.protein_g}g protein.${logged ? ` Logged so far today: ${logged.calories} cal, ${logged.protein_g}g protein across ${logged.meals} meal(s).` : ''}`);
    }
  } catch (e) { console.warn('brief mealplan fetch error:', e.message); }

  try {
    const s = await progressSummary(userId, null);
    const last = s.entries[s.entries.length - 1];
    if (last?.trend != null) {
      facts.weight = { trend: last.trend, unit: s.unit, rate: s.rate, lastDate: last.date };
      lines.push(`WEIGHT: 7-day trend is ${last.trend} ${s.unit}${s.rate != null ? `, moving ${s.rate > 0 ? '+' : ''}${s.rate} ${s.unit}/week` : ''} (last weigh-in ${last.date}).`);
    }
  } catch (e) {}

  // Shared member profile as additive background (goal / age / diet / equipment
  // the brief's own facts don't carry). Folded into the fingerprint so a profile
  // change regenerates the cached brief.
  const profileBlock = profileContextBlock(await readProfile(userId));

  const fingerprint = crypto.createHash('sha1').update(JSON.stringify([
    dayStr,
    facts.sleep?.quality || null,
    facts.workout ? [facts.workout.doneToday, facts.workout.next?.week, facts.workout.next?.day, facts.workout.blockNumber] : null,
    facts.nutrition ? [facts.nutrition.calories, facts.nutrition.protein_g, facts.nutrition.logged?.meals || 0] : null,
    facts.weight ? [facts.weight.trend, facts.weight.lastDate] : null,
    profileBlock || null,
  ])).digest('hex');

  return { facts, lines, fingerprint, profileBlock };
}

app.get('/api/coach/brief', aiLimiter, requireAuth, async (req, res) => {
  try {
    const dayStr = DATE_RE.test(String(req.query.date || '')) ? req.query.date : new Date().toISOString().slice(0, 10);
    const userRow = await getUserRow(req.user.id);
    const member = isActiveMembership(userRow);
    const { facts, lines, fingerprint, profileBlock } = await buildBriefFacts(req.user.id, dayStr);
    const hasAnyData = !!(facts.sleep || facts.workout || facts.nutrition || facts.weight);

    // Non-members get the deterministic facts (the card still works) plus a
    // lock; members without any data yet get facts only — nothing to coach on.
    if (!member) return res.json({ locked: true, facts, brief: null });
    if (!hasAnyData) return res.json({ locked: false, facts, brief: null });

    let cached = null;
    try {
      const { rows } = await db.query(
        'SELECT fingerprint, brief FROM coach_briefs WHERE user_id = $1 AND brief_date = $2',
        [req.user.id, dayStr]
      );
      cached = rows[0] || null;
    } catch (e) { console.warn('brief cache read error:', e.message); }
    if (cached && cached.fingerprint === fingerprint) {
      return res.json({ locked: false, facts, brief: cached.brief });
    }

    let brief;
    try {
      brief = await callTrainerModel(
        COACH_BRIEF_SYSTEM_PROMPT,
        [{ type: 'text', text: `${profileBlock ? profileBlock + '\n\n' : ''}Here are today's facts for this user:\n${lines.join('\n')}\n\nWrite today's brief.` }],
        COACH_BRIEF_SCHEMA
      );
    } catch (e) {
      // The card must never die on a model hiccup: fall back to yesterday's
      // text (marked stale) or facts-only.
      console.warn('coach brief model error:', e.message);
      return res.json({ locked: false, facts, brief: cached ? cached.brief : null, stale: !!cached });
    }
    if (!brief?.headline) return res.json({ locked: false, facts, brief: cached ? cached.brief : null, stale: !!cached });

    try {
      await db.query(
        `INSERT INTO coach_briefs (user_id, brief_date, fingerprint, brief) VALUES ($1, $2, $3, $4)
         ON CONFLICT (user_id, brief_date) DO UPDATE SET fingerprint = $3, brief = $4, created_at = now()`,
        [req.user.id, dayStr, fingerprint, JSON.stringify(brief)]
      );
    } catch (e) { console.warn('brief cache write error:', e.message); }

    res.json({ locked: false, facts, brief });
  } catch (e) {
    console.error('coach brief error:', e.message);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Public client config (Stripe publishable key).
app.get('/api/config', (req, res) => {
  res.json({ stripePublishableKey: STRIPE_PUBLISHABLE_KEY || '' });
});

// Current credit balance for a device.
app.get('/api/credits', (req, res) => {
  res.json({ credits: getCredits(req.query.deviceId) });
});

// Create an embedded Stripe Checkout session for a credit pack.
app.post('/api/stripe/create-credits-checkout', async (req, res) => {
  try {
    const stripe = getStripe();
    if (!stripe) return res.status(503).json({ error: 'Payments are not configured yet.' });

    const { pack, deviceId } = req.body || {};
    const packDef = CREDIT_PACKS[pack];
    if (!packDef) return res.status(400).json({ error: 'Invalid pack' });
    if (!deviceId) return res.status(400).json({ error: 'Missing deviceId' });

    // redirect_on_completion:'never' keeps the buyer on the SPA after paying —
    // the client handles completion via Stripe's onComplete callback instead of
    // a full-page return_url redirect (which would lose the generated image).
    const session = await stripe.checkout.sessions.create({
      ui_mode: 'embedded',
      mode: 'payment',
      redirect_on_completion: 'never',
      line_items: [{
        quantity: 1,
        price_data: {
          currency: 'usd',
          unit_amount: packDef.priceInCents,
          product_data: {
            name: `${packDef.label} — ${packDef.credits} generations`,
            description: 'Abs By AI image generations',
          },
        },
      }],
      metadata: { kind: 'credits', pack, deviceId, credits: String(packDef.credits) },
    });

    res.json({ clientSecret: session.client_secret, sessionId: session.id });
  } catch (err) {
    console.error('create-credits-checkout error:', err.message);
    res.status(500).json({ error: 'Could not start checkout. Please try again.' });
  }
});

// Verify a checkout session on return from Stripe. Doubles as a fulfillment
// fallback in case the webhook hasn't landed yet.
app.get('/api/stripe/session-status', async (req, res) => {
  try {
    const stripe = getStripe();
    if (!stripe) return res.status(503).json({ error: 'Payments are not configured yet.' });
    const { session_id } = req.query;
    if (!session_id) return res.status(400).json({ error: 'Missing session_id' });

    const session = await stripe.checkout.sessions.retrieve(session_id);
    if (session.status === 'complete') {
      // Fallback fulfillment in case the webhook hasn't landed yet. All paths
      // are idempotent. Route by metadata: products / memberships / credit packs.
      if (session.metadata?.productType) {
        await fulfillProductOrder(session);
      } else if (session.metadata?.kind === 'membership') {
        await fulfillMembershipSession(session);
      } else {
        await fulfillCreditsSession(session);
      }
    }
    res.json({ status: session.status, payment_status: session.payment_status });
  } catch (err) {
    console.error('session-status error:', err.message);
    res.status(500).json({ error: 'Could not verify session.' });
  }
});

// Load persisted balances at startup.
loadCreditsStore().then(s => { creditsStore = s; console.log('Credits store loaded'); });
loadSubscribersStore().then(async s => {
  subscribersStore = s;
  console.log('Subscribers store loaded');
  // Backfill welcome-sequence fields onto any subscriber captured before this
  // feature existed (the 4 real signups). @example.com test rows are marked
  // excluded so they never get emailed. New signups init on capture instead.
  let backfilled = 0;
  for (const [email, entry] of Object.entries(subscribersStore.emails)) {
    if (ensureWelcomeFields(email, entry)) backfilled++;
  }
  if (backfilled) { persistSubscribersStore(); console.log(`Backfilled welcome fields for ${backfilled} subscriber(s)`); }
  // Heal addresses captured while MailerLite was unconfigured or unreachable.
  if (!MAILERLITE_API_KEY) return;
  let healed = 0;
  for (const [email, entry] of Object.entries(subscribersStore.emails)) {
    if (entry.synced) continue;
    if (await pushToMailerLite(email)) { entry.synced = true; healed++; }
  }
  if (healed) { persistSubscribersStore(); console.log(`Re-synced ${healed} subscriber(s) to MailerLite`); }
});

// ============================================================
// PRINTED PRODUCTS — Printify upsell (canvas / poster)
// ============================================================
// PRODUCT CONFIG — populated from the Printify catalog. Each variant carries
// its own blueprintId/printProviderId so the webhook can build the order
// without extra lookups. printifyCost / printifyShipping are in CENTS and
// hardcoded because Printify returns 0 on order creation (orders are
// "on-hold" until submitted to production); verify against fulfilled orders.
const PRODUCT_CONFIG = {
  canvas: {
    variants: {
      // Blueprint 937 (Matte Canvas Multi-Size), Jondo (105)
      '8x10_unframed':  { blueprintId: 937, printProviderId: 105, variantId: 95212,  price: 3400, printifyCost: 1399, printifyShipping: 899 },
      '11x14_unframed': { blueprintId: 937, printProviderId: 105, variantId: 82229,  price: 4200, printifyCost: 1699, printifyShipping: 899 },
      '16x20_unframed': { blueprintId: 937, printProviderId: 105, variantId: 82231,  price: 5400, printifyCost: 2199, printifyShipping: 1099 },
      // Blueprint 944 (Matte Canvas Framed), Jondo (105)
      '11x14_framed':   { blueprintId: 944, printProviderId: 105, variantId: 88291,  price: 7500,  printifyCost: 3199, printifyShipping: 1099 },
      '16x20_framed':   { blueprintId: 944, printProviderId: 105, variantId: 88293,  price: 8700,  printifyCost: 4099, printifyShipping: 1299 },
    },
  },
  poster: {
    variants: {
      // Blueprint 282 (Matte Vertical Posters), Sensaria (2)
      '9x11':  { blueprintId: 282, printProviderId: 2, variantId: 62103,  price: 1800, printifyCost:  599, printifyShipping: 499 },
      '11x14': { blueprintId: 282, printProviderId: 2, variantId: 43135,  price: 2700, printifyCost:  699, printifyShipping: 499 },
    },
  },
};

// Resolve a printed-product variant from its type/size/framed selection.
// This is the single source of truth for both pricing the Stripe session and
// building the Printify order, so the amount charged can never disagree with
// the amount fulfilled. Returns null for any combination not in the catalog.
function productVariant(productType, size, framed) {
  const key = productType === 'canvas' ? `${size}_${framed ? 'framed' : 'unframed'}` : size;
  return PRODUCT_CONFIG[productType]?.variants[key] || null;
}

// Parse a product's aspect ratio (width/height) from a size key like "11x14".
// Returns null for sizes without parseable dimensions.
function productAspectFromSize(size) {
  const m = /(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)/i.exec(size || '');
  if (!m) return null;
  const w = parseFloat(m[1]), h = parseFloat(m[2]);
  if (!w || !h) return null;
  return w / h;
}

// Compute a Printify front print-area placement that never crops the subject's
// head. Printify scales the artwork so its width fills the print area at
// scale 1, positions the image *center* at (x, y) as fractions of the print
// area, and crops whatever falls outside. Two cases:
//   • artwork WIDER than the product → scale up to fill the height instead,
//     so the overflow is on the (less important) left/right edges.
//   • artwork TALLER/narrower than the product → keep scale 1 and bias the
//     vertical position upward so the crop is taken from the bottom (feet),
//     keeping the head and abs in frame.
// Falls back to the original centered fill when dimensions are unknown.
function computePrintPlacement(imgW, imgH, prodAspect) {
  if (!imgW || !imgH || !prodAspect) return { scale: 1, x: 0.5, y: 0.5, angle: 0 };
  const aImg = imgW / imgH;
  if (aImg >= prodAspect) {
    return { scale: aImg / prodAspect, x: 0.5, y: 0.5, angle: 0 };
  }
  const renderedH = prodAspect / aImg;     // rendered height in print-area-height units (>1)
  const topMargin = 0.03;                   // small headroom so the head isn't flush to the edge
  const y = Math.min(1, topMargin + renderedH / 2);
  return { scale: 1, x: 0.5, y, angle: 0 };
}

// Upload the generated image to Printify and return its id + pixel dimensions.
app.post('/api/printify/upload-image', async (req, res) => {
  if (!PRINTIFY_API_KEY) {
    return res.status(503).json({ error: 'Printify not configured. Add PRINTIFY_API_KEY to environment variables.' });
  }
  try {
    const { imageBase64, fileName } = req.body || {};
    if (!imageBase64 || !fileName) {
      return res.status(400).json({ error: 'Missing imageBase64 or fileName' });
    }
    const response = await fetch('https://api.printify.com/v1/uploads/images.json', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${PRINTIFY_API_KEY}` },
      body: JSON.stringify({ file_name: fileName, contents: imageBase64 }),
    });
    const data = await response.json();
    if (!response.ok) {
      console.error('Printify upload error:', JSON.stringify(data));
      return res.status(response.status).json({ error: data?.message || 'Printify upload failed' });
    }
    // Printify returns the artwork's pixel dimensions — the client passes these
    // back into create-checkout so the webhook can compute a no-crop placement.
    res.json({ imageId: data.id, previewUrl: data.preview_url, width: data.width, height: data.height });
  } catch (err) {
    console.error('Printify upload error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Create an embedded Stripe Checkout session for a printed-product order.
app.post('/api/stripe/create-checkout', async (req, res) => {
  const stripe = getStripe();
  if (!stripe) return res.status(503).json({ error: 'Stripe not configured. Add STRIPE_SECRET_KEY to environment variables.' });
  try {
    // priceInCents is intentionally ignored — the price is looked up server-side
    // so the client can never dictate what it pays (see N1 in the July 17 audit).
    const { productType, size, framed, imageId, imgWidth, imgHeight, productLabel, returnUrl } = req.body || {};
    if (!productType || !size || !returnUrl) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    if (!imageId) {
      return res.status(400).json({ error: 'Missing imageId' });
    }
    const variant = productVariant(productType, size, !!framed);
    if (!variant) {
      return res.status(400).json({ error: 'Unknown product or size' });
    }
    const displayName = `${productLabel || productType} — ${size}${framed ? ' (Framed)' : ''}`;
    const session = await stripe.checkout.sessions.create({
      ui_mode: 'embedded',
      mode: 'payment',
      return_url: returnUrl,
      line_items: [{
        quantity: 1,
        price_data: {
          currency: 'usd',
          unit_amount: variant.price,
          product_data: {
            name: displayName,
            description: 'Your AI-generated future self, printed and shipped to you.',
          },
        },
      }],
      shipping_address_collection: {
        allowed_countries: [
          'US', 'CA', 'GB', 'AU', 'DE', 'FR', 'ES', 'IT', 'NL', 'SE', 'NO', 'DK',
          'FI', 'AT', 'BE', 'CH', 'IE', 'NZ', 'JP', 'SG', 'HK', 'MX', 'BR',
        ],
      },
      automatic_tax: { enabled: false },
      metadata: {
        // imagePreviewUrl is deliberately NOT stored — the printed artwork is
        // rebuilt from imageId server-side so it can only be an image uploaded
        // through our own Printify account, never an attacker-supplied URL.
        imageId: imageId || '',
        imgWidth: String(imgWidth || ''),
        imgHeight: String(imgHeight || ''),
        productType,
        size,
        framed: String(!!framed),
      },
    });
    res.json({ clientSecret: session.client_secret });
  } catch (err) {
    console.error('create-checkout error:', err.message);
    res.status(500).json({ error: err.message || 'Internal server error' });
  }
});

// Submit a paid printed-product order to Printify. Idempotent via the same
// `fulfilled` map used for credits, so the webhook + return-redirect paths
// never double-submit. Builds the order from the session metadata and the
// no-crop placement computed from the artwork + product aspect ratios.
async function fulfillProductOrder(session) {
  if (!session || session.payment_status !== 'paid') return false;
  const stripe = getStripe();
  // The webhook payload omits shipping_details for embedded checkout — re-fetch.
  const full = (stripe && session.id) ? await stripe.checkout.sessions.retrieve(session.id) : session;
  const sid = full.id;
  if (creditsStore.fulfilled[`order_${sid}`]) return false; // already submitted

  const meta = full.metadata || {};
  const { imageId, imagePreviewUrl, productType, size } = meta;
  const framedBool = meta.framed === 'true';
  const email = full.customer_details?.email;
  const shipping = full.shipping_details?.address;
  // Rebuild the artwork source from imageId (an image uploaded through our own
  // Printify account) rather than trusting any client-supplied URL. imagePreviewUrl
  // is only read as a fallback for sessions created before this fix, which still
  // carry it in their metadata.
  const imageSrc = (imageId ? `https://images-api.printify.com/${imageId}` : '') || imagePreviewUrl || '';

  if (!PRINTIFY_API_KEY || !PRINTIFY_SHOP_ID) {
    console.warn('Printify not configured — product order recorded but not submitted');
    return false;
  }
  if (!imageSrc || !productType || !size) {
    console.warn('Product order missing image/product/size — not submitted to Printify');
    return false;
  }

  const variantKey = productType === 'canvas' ? `${size}_${framedBool ? 'framed' : 'unframed'}` : size;
  const variant = productVariant(productType, size, framedBool);
  if (!variant || !variant.variantId) {
    console.warn(`Printify variant not configured for ${productType}/${variantKey} — order NOT submitted`);
    return false;
  }

  // Belt-and-braces price gate: the last line before money is spent with Printify.
  // Never fulfill an order that paid less than the catalog price (or a non-USD
  // amount we can't compare). This protects against any future create-checkout
  // regression as well as pre-fix attacker-priced sessions still in flight.
  if ((full.currency && full.currency !== 'usd') || (full.amount_total ?? 0) < variant.price) {
    console.error(`Print order ${sid} paid ${full.amount_total} ${full.currency} < required ${variant.price} — NOT submitted to Printify`);
    return false;
  }

  const prodAspect = productAspectFromSize(size);
  const placement = computePrintPlacement(parseInt(meta.imgWidth, 10), parseInt(meta.imgHeight, 10), prodAspect);
  console.log(`Print placement for ${productType}/${variantKey} (img ${meta.imgWidth}x${meta.imgHeight}, aspect ${prodAspect}):`, JSON.stringify(placement));

  const fullName = (full.shipping_details?.name || full.customer_details?.name || '').trim();
  const orderPayload = {
    external_id: sid,
    line_items: [{
      blueprint_id: variant.blueprintId,
      print_provider_id: variant.printProviderId,
      variant_id: variant.variantId,
      print_areas: { front: [{ src: imageSrc, ...placement }] },
      quantity: 1,
    }],
    shipping_method: 1,
    send_shipping_notification: true,
    address_to: {
      first_name: fullName.split(' ')[0] || '',
      last_name: fullName.split(' ').slice(1).join(' ') || '',
      email: email || '',
      phone: '',
      country: shipping?.country || 'US',
      region: shipping?.state || '',
      address1: shipping?.line1 || '',
      address2: shipping?.line2 || '',
      city: shipping?.city || '',
      zip: shipping?.postal_code || '',
    },
  };

  const printifyRes = await fetch(
    `https://api.printify.com/v1/shops/${PRINTIFY_SHOP_ID}/orders.json`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${PRINTIFY_API_KEY}` },
      body: JSON.stringify(orderPayload),
    }
  );
  const printifyData = await printifyRes.json();
  if (!printifyRes.ok) {
    console.error('Printify order creation failed:', JSON.stringify(printifyData));
    return false;
  }

  creditsStore.fulfilled[`order_${sid}`] = true;
  persistCreditsStore();
  console.log(`Printify order created: ${printifyData.id} (${productType} ${size}${framedBool ? ' framed' : ''}) for ${email}`);
  return true;
}

// ============================================================
// STATIC FILES & FALLBACK
// ============================================================
// Serve ONLY the curated public/ folder. This is an allowlist: the project root
// (server.js, db.js, *-data.json with customer PII, internal *.md handoffs) is
// NEVER exposed over HTTP. Do not revert to express.static('.').
app.use(express.static(path.join(__dirname, 'public')));

// Explicit route for the privacy page (linked as /privacy without .html).
app.get('/privacy', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'privacy.html'));
});

// Serve index.html for all non-API, non-dashboard routes (SPA fallback)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// ============================================================
// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Abs By AI backend running on port ${PORT}`);
});
initDb().catch(e => console.error('initDb error:', e.message));

// ── Keep-warm heartbeat ──────────────────────────────────────────────
// A user's first generation after an idle period can stall a few seconds while
// the server/runtime spins back up (a "cold start"). This self-ping every 4
// minutes keeps the process, outbound DNS/TLS, and the platform's instance warm
// so requests are served instantly. Hits the public Railway domain when known,
// otherwise localhost. Best-effort: failures are swallowed.
const KEEP_WARM_MS = 4 * 60 * 1000;
const KEEP_WARM_URL = process.env.RAILWAY_PUBLIC_DOMAIN
  ? `https://${process.env.RAILWAY_PUBLIC_DOMAIN}/health`
  : `http://127.0.0.1:${PORT}/health`;
setInterval(() => {
  fetch(KEEP_WARM_URL).catch(() => {});
}, KEEP_WARM_MS).unref?.();

// Trial-ending reminder sweep — hourly. Runs first pass shortly after boot so a
// due reminder isn't delayed a full hour on deploy.
const TRIAL_REMINDER_MS = 60 * 60 * 1000;
setTimeout(() => { trialReminderSweep(); }, 30 * 1000).unref?.();
setInterval(() => { trialReminderSweep(); }, TRIAL_REMINDER_MS).unref?.();

// Welcome-autoresponder sweep — hourly, first pass shortly after boot. No-op
// until WELCOME_ENABLED=true (set on Railway once mail.absbyai.com is verified).
const WELCOME_SWEEP_MS = 60 * 60 * 1000;
setTimeout(() => { welcomeSweep(); }, 45 * 1000).unref?.();
setInterval(() => { welcomeSweep(); }, WELCOME_SWEEP_MS).unref?.();

// Exposed for tests. Requiring this module also starts the server; tests point
// DATABASE_URL at pgmem:// and stub the stripe / node-fetch modules.
module.exports = { app, db, trialReminderSweep, welcomeSweep, fulfillMembershipSession };

