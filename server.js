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
const COUNSEL_MONTHLY_CAP = 10; // full Decision Counsel sessions per account per calendar month

const CREDIT_PACKS = {
  starter: { credits: 5,  priceInCents: 499,  label: 'Starter Pack' },
  power:   { credits: 20, priceInCents: 1499, label: 'Power Pack' },
};
// Membership plans (Stripe subscriptions). Keys must match data-plan
// attributes in index.html. Annual ≈ $5/mo is the anti-churn lever.
const MEMBERSHIP_PLANS = {
  monthly: { priceInCents: 999,  interval: 'month', label: 'Monthly Membership' },
  annual:  { priceInCents: 5999, interval: 'year',  label: 'Annual Membership' },
};
// Free (non-member) allowance of meal-photo analyses — the freemium taste.
const FREE_MEAL_ANALYSES = 3;
const { EXERCISE_BY_ID, exercisesForEquipment } = require('./exercises');
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
  const [todos, checks] = await Promise.all([loadTodos(), loadTaskChecks()]);
  res.json({ todos, task_checks: { checked: checks.checked, log: checks.log } });
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

Reply with only the single code word, nothing else.`,
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

    const code = data?.content?.[0]?.text?.trim().toUpperCase() || 'OK';

    res.json({ code });
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

const MEAL_SYSTEM_PROMPT = `You are the meal-analysis engine for a fitness app. Given a photo of food, itemize everything edible and estimate nutrition per item.

Rules:
- One entry per distinct food item. Include cooking fats, oils, dressings, and sauces as their own line items when they are plausibly present, even if not directly visible (e.g. "cooking oil" for pan-fried food, "dressing" for a glossy salad).
- estimated_grams is the edible portion as served. Use visual references (plate ~27cm, fork, hands) to judge scale. Do not default to "standard serving" sizes when the photo shows more or less.
- calories, protein_g, carbs_g, fat_g are for the estimated portion, not per 100g. Keep calories consistent with energy math: 4 kcal/g protein and carbs, 9 kcal/g fat, 7 kcal/g alcohol.
- For alcoholic drinks, set alcohol_g to the grams of pure ethanol in the portion — most of their calories come from alcohol, not macros. Set alcohol_g to 0 for everything else.
- If the photo shows a nutrition label, read it verbatim and set source to "label" with a single item.
- List every assumption that materially moves the numbers (e.g. "assumed whole milk", "assumed cooked in 1 tbsp oil").
- clarifying_questions: at most 2, only questions whose answer would change calories by >10%. Each needs 2-4 short tap-friendly options, most likely option first. If confidence is high, return an empty array.
- If the image contains no food or drink, set is_food to false and return an empty items array.`;

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
    const { photoBase64, photoMime, note, recentMeals, deviceId } = req.body;

    if (!photoBase64 || !photoMime) {
      return res.status(400).json({ error: 'Missing photoBase64 or photoMime' });
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
          return res.status(402).json({
            error: 'You\'ve used your free meal analyses. Buy credits or become a member for unlimited tracking.',
            needsMembership: true,
            needsCredits: true,
          });
        }
      }
    }

    const userContent = [
      {
        type: 'image',
        source: { type: 'base64', media_type: photoMime, data: photoBase64 },
      },
    ];

    let textParts = ['Analyze this meal.'];
    if (note && typeof note === 'string') {
      textParts.push(`User note about the meal: "${note.slice(0, 300)}"`);
    }
    if (Array.isArray(recentMeals) && recentMeals.length) {
      const names = recentMeals.slice(0, 15).map((m) => String(m).slice(0, 80));
      textParts.push(`The user's recently logged meals: ${names.join('; ')}. If this photo clearly shows one of these exact meals again, set matches_recent to its name.`);
    }
    userContent.push({ type: 'text', text: textParts.join('\n') });

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 2000,
        system: MEAL_SYSTEM_PROMPT,
        output_config: { format: { type: 'json_schema', schema: MEAL_SCHEMA } },
        messages: [{ role: 'user', content: userContent }],
      }),
    });

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

    res.json({
      isFood: true,
      mealName: analysis.meal_name,
      source: analysis.source,
      context: analysis.context,
      confidence: analysis.confidence,
      matchesRecent: analysis.matches_recent,
      items: adjustedItems,
      totals: sumTotals(adjustedItems),
      raw: { items: checkedItems, totals: sumTotals(checkedItems), calibrationFactor: factor },
      clarifyingQuestions: (analysis.clarifying_questions || []).slice(0, 2),
      needsClarification: analysis.confidence !== 'high' && (analysis.clarifying_questions || []).length > 0,
      ...(creditsRemaining !== undefined ? { creditsRemaining, usedCredit: true } : {}),
    });
  } catch (err) {
    console.error('Meal analysis error:', err);
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
// ENDPOINT 3: Generate image (Gemini)
// ============================================================
app.post('/api/generate-image', aiLimiter, (req, res, next) => optionalAuth(req, res, next), async (req, res) => {
  try {
    const { prompt, photoBase64, photoMime, deviceId } = req.body;

    if (!prompt || !photoBase64 || !photoMime) {
      return res.status(400).json({
        error: 'Missing prompt, photoBase64, or photoMime',
      });
    }

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key=${encodeURIComponent(GEMINI_API_KEY)}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [
              { text: prompt },
              {
                inline_data: {
                  mime_type: photoMime,
                  data: photoBase64,
                },
              },
            ],
          },
        ],
        generationConfig: {
          responseModalities: ['TEXT', 'IMAGE'],
        },
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: data?.error?.message || 'Image generation error',
      });
    }

    const parts = data?.candidates?.[0]?.content?.parts || [];
    const imgPart = parts.find((p) => p.inline_data || p.inlineData);

    if (!imgPart) {
      const textBlock = parts.find((p) => p.text)?.text;
      return res.status(400).json({
        error:
          textBlock ||
          'Image generation was blocked â this is usually caused by a photo that is too suggestive or explicit. For best results, use a simple shirtless photo (men) or sports bra / swimsuit photo (women) with neutral pose and lighting.',
      });
    }

    const imageBase64 = (imgPart.inline_data || imgPart.inlineData).data;

    // Credit gating: if the device has credits left, consume one and return the
    // image unlocked. If it's out of credits, still return the image but flag it
    // `locked` so the client blurs it behind the paywall (generate-and-lock).
    // Requests without a deviceId (e.g. legacy clients) are left unlocked.
    // Members generate without consuming credits.
    let locked = false;
    if (deviceId && !isActiveMembership(req.user)) {
      const balance = getCredits(deviceId);
      if (balance > 0) {
        creditsStore.balances[deviceId] = balance - 1;
        persistCreditsStore(); // fire-and-forget; in-memory copy is source of truth
      } else {
        locked = true;
      }
    }

    res.json({ imageBase64, locked });
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
let creditsStore = { balances: {}, fulfilled: {}, mealCounts: {} };

async function loadCreditsStore() {
  const empty = { balances: {}, fulfilled: {}, mealCounts: {} };
  if (!GITHUB_TOKEN) return empty;
  try {
    const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${CREDITS_FILE}`, {
      headers: { 'Authorization': `Bearer ${GITHUB_TOKEN}`, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return empty;
    const data = await res.json();
    const parsed = JSON.parse(Buffer.from(data.content, 'base64').toString('utf8'));
    return { balances: parsed.balances || {}, fulfilled: parsed.fulfilled || {}, mealCounts: parsed.mealCounts || {} };
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

  const existing = subscribersStore.emails[email];
  if (existing?.synced) return res.json({ ok: true }); // already captured + synced

  const synced = await pushToMailerLite(email);
  subscribersStore.emails[email] = {
    subscribedAt: existing?.subscribedAt || new Date().toISOString(),
    deviceId: existing?.deviceId || deviceId,
    synced,
  };
  persistSubscribersStore(); // fire-and-forget; in-memory copy is source of truth
  console.log(`Subscriber ${existing ? 'retried' : 'added'}: ${email} (MailerLite sync: ${synced})`);
  res.json({ ok: true });
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
  const status = userRow.membership_status;
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
    if (isActiveMembership(row)) return res.status(400).json({ error: 'You already have an active membership.' });

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

    const session = await stripe.checkout.sessions.create({
      ui_mode: 'embedded',
      mode: 'subscription',
      redirect_on_completion: 'never',
      customer_email: req.user.email,
      line_items: [{
        quantity: 1,
        price_data: {
          currency: 'usd',
          unit_amount: planDef.priceInCents,
          recurring: { interval: planDef.interval },
          product_data: {
            name: `Abs By AI ${planDef.label}`,
            description: 'AI trainer, unlimited transformations & meal tracking. 7-day money-back guarantee.',
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
  try {
    if (stripe && typeof subId === 'string') {
      const sub = await stripe.subscriptions.retrieve(subId);
      if (sub.current_period_end) periodEnd = new Date(sub.current_period_end * 1000).toISOString();
    }
  } catch (e) { console.warn('subscription retrieve failed:', e.message); }

  await db.query(
    `UPDATE users SET stripe_customer_id = $1, stripe_subscription_id = $2,
       membership_status = 'active', membership_plan = $3, membership_period_end = $4
     WHERE id = $5`,
    [session.customer || null, subId, meta.plan || 'monthly', periodEnd, parseInt(meta.userId, 10)]
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

const PROGRAM_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['why_this_works', 'assessment', 'weeks'],
  properties: {
    why_this_works: {
      type: 'string',
      description: "Personalized paragraph referencing the user's photos (starting point → goal), health goals, and injuries — why THIS program works for THEM.",
    },
    assessment: {
      type: 'object',
      additionalProperties: false,
      required: ['starting_point', 'goal_summary', 'assigned_level', 'starting_phase'],
      properties: {
        starting_point: { type: 'string', description: "2-3 encouraging, never judgmental sentences on what the before photo shows: rough body-fat range, muscle base, apparent fitness level. If no photo was provided, base it on their answers." },
        goal_summary: { type: 'string', description: "1-2 sentences on the gap between the before and after photos: how much muscle to gain and fat to lose. If no photos, base it on their stated goal." },
        assigned_level: { type: 'string', enum: ['beginner', 'intermediate', 'advanced'], description: 'The MORE CONSERVATIVE of the photo assessment and their stated experience.' },
        starting_phase: { type: 'integer', description: 'Phase 1-6 from the phase ladder, matching assigned_level.' },
      },
    },
    weeks: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['week', 'theme', 'days'],
        properties: {
          week: { type: 'integer' },
          theme: { type: 'string', description: 'Short label, e.g. "Foundation", "Build", "Push", "Peak".' },
          days: {
            type: 'array',
            items: {
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
            },
          },
        },
      },
    },
  },
};

const TRAINER_SYSTEM_PROMPT = `You are an expert personal trainer designing a 4-week program for a fitness app called Abs By AI. Users have generated an AI image of their future physique — your program is the path from their before photo to that after photo.

Photo assessment (when photos are provided):
- The BEFORE photo shows their starting point: estimate a rough body-fat range, muscle base, and apparent fitness level.
- The AFTER photo is an AI-generated image of their goal physique: judge how much muscle to gain and fat to lose.
- Derive the training goal from the GAP between the two photos. Be encouraging and factual — NEVER judgmental about their current body.
- assessment.assigned_level: combine the photo assessment with their stated experience — the MORE CONSERVATIVE of the two wins (photo looks fit but they say beginner → beginner).
- If no photos were provided, base the assessment on their answers (goal + body type).

The phase ladder (assessment.starting_phase — everyone eventually ends at Phase 6):
| Phase | Minutes/day | Where | Who starts here |
| 1 | 10 | home, bodyweight | complete beginner |
| 2 | 20 | home (dumbbells if available) | beginner, month 2 |
| 3 | 30 | gym | beginner month 3 · intermediate month 1 |
| 4 | 35-40 | gym | intermediate month 2 |
| 5 | 45 | gym | intermediate month 3 · advanced month 1 |
| 6 | 45 + 15 min zone-2 cardio warm-up | gym | advanced after 1 comfortable month — final phase |
- starting_phase matches assigned_level: beginner → 1, intermediate → 3, advanced → 5 (never higher; go lower if the photo suggests it).
- Home-only users (no gym) run the same phases with their equipment tier — a "gym" phase becomes its full home version.
- This block is ONE phase: build all 4 weeks to that phase's daily time budget. The block prompt may pin the phase for you — if it does, use that phase.

Rules:
- You may ONLY use exercises from the provided whitelist, referenced by their exact id. Never invent an exercise or id.
- Build exactly 4 weeks of 7 days each — everyone trains EVERY day. Days progress in intensity gently within the week; name each week's theme.
- EVERY workout is TOTAL-BODY. Never program push/pull/leg or body-part splits. Daily training is sustainable because volume per muscle per day stays modest: spread the weekly volume across 7 light-to-moderate days, and no muscle is trained to failure two days in a row.
- Daily time budgets: 10 min ≈ 2-3 compound moves + a short abs finisher; 20 min ≈ 3-4 moves; 30 min ≈ 4-5; 35-40 min ≈ 5-6; 45 min ≈ 6-7 (plus warm-up and abs finisher).
- Under 30 min/day: COMPOUND moves only (squat pattern, push-up/press, row, hinge, carry, core). Isolation exercises (curls, lateral raises, flies, kickbacks, leg extension) are allowed ONLY at 30+ min/day.
- Every day ends with an abs finisher of 2-3 exercises — this is Abs By AI. At Phase 1 keep it to 1-2 short ab moves.
- STRICTLY avoid exercises that load reported injured areas; prefer joint-friendly picks (e.g. knee pain → hinge and glute work over deep lunges; lower-back pain → avoid loaded spinal flexion and heavy hinging; shoulder pain → avoid overhead pressing; wrist pain → avoid loaded straight-arm plank positions). Treat free-text health notes (e.g. "doctor said no jumping", "high blood pressure") as hard constraints.
- Match assigned_level: beginners get simpler movements, fewer sets, and reps in the 8-15 range; experienced lifters get more volume and harder variations.
- warmup: 2-4 light moves. Use warm-up category exercises or easy bodyweight moves. (At Phase 6 the app adds a separate 15-min zone-2 cardio block before your warm-up — do not include cardio machines in the exercise list.)
- Their "beyond the look" health goals (heart health, energy, mental health, sleep, longevity, confidence) shape emphasis and MUST be woven into why_this_works — e.g. heart-health goals → frame the daily movement and future zone-2 cardio around lowering cardiovascular risk.
- cue: one short personalized coaching line. common_mistake: the single most likely error for THIS user.
- why_this_works: 3-5 sentences, warm but direct, referencing their photos (when provided), their health goals, and injuries. Address them as "you".
- Reps for timed holds use e.g. "30 sec". rest_sec between 30 and 180 (short rests at low phases to fit the time budget).

Exercise selection rules (safety-first — these override everything else):
- NEVER program barbell bench press, barbell deadlifts, barbell back squats, cleans, snatches, jerks, or ANY powerlifting/Olympic lift — they are not in the whitelist and must not appear even in cues, notes, or why_this_works.
- Squat pattern: gym users → leg-press (advanced) or db-goblet-squat; beginners → db-goblet-squat or bw-squat.
- Hamstrings: leg-curl (machine) is the DEFAULT for gym users. db-rdl (Dumbbell Hip Hinge) only when there is no machine access (home/dumbbell users), and NEVER in workouts under 15 minutes per day.
- Rear delts: machine-rear-delt-fly is the default for gym users; db-rear-delt-fly when no machine.
- Chest: dumbbell/machine presses and flies only (db-fly, cable-fly, pec-deck, machine-chest-press, db-bench-press, db-floor-press, and the push-up family).`;

// Phase ladder: daily time budget per phase. Phase 6 adds a 15-min zone-2
// cardio warm-up block (rendered by the app, not the model).
const PHASES = {
  1: { minutes: 10, label: '10 min/day · home' },
  2: { minutes: 20, label: '20 min/day · home' },
  3: { minutes: 30, label: '30 min/day · gym' },
  4: { minutes: 40, label: '35–40 min/day · gym' },
  5: { minutes: 45, label: '45 min/day · gym' },
  6: { minutes: 45, label: '45 min/day + 15 min zone-2 cardio · gym', zone2: true },
};
const EXPERIENCE_START_PHASE = { beginner: 1, intermediate: 3, advanced: 5 };

function clampPhase(p) {
  const n = parseInt(p, 10);
  return Number.isFinite(n) ? Math.min(6, Math.max(1, n)) : 1;
}

function buildTrainerUserContent(intake, photos, pinnedPhase) {
  const allowed = exercisesForEquipment(intake.equipment);
  const list = allowed.map((e) => `${e.id} | ${e.name} | ${e.cat} | ${e.muscles}`).join('\n');
  const content = [];
  const { beforeBase64, beforeMime, afterBase64, afterMime } = photos || {};
  if (beforeBase64 && beforeMime) {
    content.push({ type: 'image', source: { type: 'base64', media_type: beforeMime, data: beforeBase64 } });
    content.push({ type: 'text', text: 'BEFORE photo — the user\'s current body (shared with consent). Estimate their starting point: rough body-fat range, muscle base, apparent fitness level. Never judgmental.' });
  }
  if (afterBase64 && afterMime) {
    content.push({ type: 'image', source: { type: 'base64', media_type: afterMime, data: afterBase64 } });
    content.push({ type: 'text', text: 'AFTER photo — the AI-generated image of their goal physique. The training goal is the gap between the before photo and this one.' });
  }
  content.push({
    type: 'text',
    text: `User intake:\n${JSON.stringify(intake, null, 2)}\n\n` +
      (pinnedPhase
        ? `This block is pinned to Phase ${pinnedPhase} (${PHASES[pinnedPhase].label}). Build every day to that time budget and set assessment.starting_phase to ${pinnedPhase}.\n\n`
        : `Their stated experience caps the starting phase at Phase ${EXPERIENCE_START_PHASE[intake.experience] || 1}. Go lower if the before photo suggests it — never higher.\n\n`) +
      `Exercise whitelist (id | name | category | muscles) — use ONLY these ids:\n${list}`,
  });
  return content;
}

// Exercises removed from the library (v2 safety pass) → their replacement.
// Old stored programs may still reference them; without this map they would
// fall through to a generic same-category pick.
const REMOVED_EXERCISE_SWAPS = {
  'bb-bench-press': 'db-bench-press',
  'bb-deadlift': 'db-rdl',
  'bb-back-squat': 'db-goblet-squat',
};

// Replace any hallucinated/out-of-tier exercise id with its library swap (if
// allowed) or a same-category fallback from the allowed list.
function sanitizeProgram(program, equipment) {
  const allowed = new Set(exercisesForEquipment(equipment).map((e) => e.id));
  const allowedList = exercisesForEquipment(equipment);
  const fix = (id, prefCat) => {
    if (allowed.has(id)) return id;
    const legacy = REMOVED_EXERCISE_SWAPS[id];
    if (legacy && allowed.has(legacy)) return legacy;
    const lib = EXERCISE_BY_ID[id];
    if (lib && allowed.has(lib.swap)) return lib.swap;
    const cat = lib?.cat || prefCat;
    const sub = allowedList.find((e) => e.cat === cat) || allowedList[0];
    return sub.id;
  };
  let replaced = 0;
  for (const week of program.weeks || []) {
    for (const day of week.days || []) {
      for (const w of day.warmup || []) {
        const fixed = fix(w.exercise_id, 'warmup');
        if (fixed !== w.exercise_id) { w.exercise_id = fixed; replaced++; }
      }
      for (const ex of [...(day.main || []), ...(day.abs_finisher || [])]) {
        const fixed = fix(ex.exercise_id, 'abs');
        if (fixed !== ex.exercise_id) { ex.exercise_id = fixed; replaced++; }
      }
    }
  }
  if (replaced) console.warn(`sanitizeProgram: replaced ${replaced} out-of-whitelist exercise id(s)`);
  return program;
}

// Free-preview shape: why-this-works + assessment + week/day structure at a
// glance + the FIRST 3 DAYS fully unlocked. Everything else is
// visible-but-locked (focus only).
function stripProgramForPreview(program) {
  return {
    why_this_works: program.why_this_works,
    assessment: program.assessment,
    phase: program.phase,
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
  equipment: ['none', 'db', 'gym'],
  experience: ['beginner', 'intermediate', 'advanced'],
  health_goals: ['heart_health', 'energy', 'mental_health', 'sleep', 'longevity', 'confidence', 'look_only'],
};

// Pre-v2 intakes stored a different experience scale.
const LEGACY_EXPERIENCE = { never: 'beginner', on_and_off: 'intermediate', consistent: 'advanced' };

function validateIntake(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const exp = LEGACY_EXPERIENCE[raw.experience] || raw.experience;
  const intake = {
    equipment: VALID_INTAKE.equipment.includes(raw.equipment) ? raw.equipment : 'none',
    experience: VALID_INTAKE.experience.includes(exp) ? exp : 'beginner',
    injuries: Array.isArray(raw.injuries) ? raw.injuries.slice(0, 6).map((s) => String(s).slice(0, 40)) : [],
    injury_notes: String(raw.injury_notes || '').slice(0, 300),
    health_goals: Array.isArray(raw.health_goals)
      ? raw.health_goals.filter((g) => VALID_INTAKE.health_goals.includes(g)).slice(0, 7)
      : [],
    health_notes: String(raw.health_notes || '').slice(0, 300),
    age_range: String(raw.age_range || raw.body?.age_range || '').slice(0, 20),
  };
  // No-photo fallback answers (also present on old intakes — harmless to keep).
  if (VALID_INTAKE.goal.includes(raw.goal)) intake.goal = raw.goal;
  if (VALID_INTAKE.body_type.includes(raw.body_type)) intake.body_type = raw.body_type;
  return intake;
}

async function callTrainerModel(systemPrompt, userContent, schema = PROGRAM_SCHEMA) {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      // Sonnet-class reasoning: program design rewards reasoning quality, and
      // it must read the before photo. Same structured-output pattern as
      // /api/analyze-meal.
      model: 'claude-sonnet-4-6',
      max_tokens: 16000,
      system: systemPrompt,
      output_config: { format: { type: 'json_schema', schema } },
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

// Generate a program from intake. Free for everyone (the sunk-cost hook) —
// members get the full block back; free users get the stripped preview.
// Logged-in users get the FULL program persisted server-side, so subscribing
// later unlocks it without regenerating.
app.post('/api/generate-program', aiLimiter, optionalAuth, async (req, res) => {
  try {
    const intake = validateIntake(req.body?.intake);
    if (!intake) return res.status(400).json({ error: 'Missing intake' });
    const { photoBase64, photoMime, afterPhotoBase64, afterPhotoMime, photoConsent } = req.body || {};

    const userContent = buildTrainerUserContent(intake, photoConsent ? {
      beforeBase64: photoBase64, beforeMime: photoMime,
      afterBase64: afterPhotoBase64, afterMime: afterPhotoMime,
    } : null);

    // Sleep Coach cross-feature rule: bad night → longer warm-up, never a
    // shorter or lighter workout.
    if (req.user) {
      const sleepLine = sleepContextForTrainer(await getTodaysSleep(req.user.id));
      if (sleepLine) userContent.push({ type: 'text', text: sleepLine });
      const weightLine = await getWeightContext(req.user.id);
      if (weightLine) userContent.push({ type: 'text', text: weightLine });
    }

    let program;
    try {
      program = await callTrainerModel(TRAINER_SYSTEM_PROMPT, userContent);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Program generation failed. Please try again.' });
    }
    if (!program?.weeks?.length) {
      return res.status(502).json({ error: 'Model returned an unusable program. Please try again.' });
    }
    sanitizeProgram(program, intake.equipment);

    // Pin the ladder phase: the stated experience caps it; the model's
    // photo-based assessment can only lower it (conservative wins).
    const expPhase = EXPERIENCE_START_PHASE[intake.experience] || 1;
    program.phase = Math.min(clampPhase(program.assessment?.starting_phase ?? expPhase), expPhase);
    if (program.assessment) program.assessment.starting_phase = program.phase;

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
      } catch (e) { console.error('program save error:', e.message); }
    }

    res.json({
      programId,
      blockNumber: 1,
      locked: !member,
      program: member ? { ...program, locked: false } : stripProgramForPreview(program),
    });
  } catch (err) {
    console.error('generate-program error:', err);
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

    // Phase ladder promotion: finishing a block normally moves up a phase.
    // "Too hard" holds; "too hard" with almost nothing completed demotes.
    const intake = validateIntake(prev.intake) || prev.intake;
    const prevPhase = clampPhase(prev.program?.phase ?? EXPERIENCE_START_PHASE[intake.experience] ?? 1);
    let nextPhase = Math.min(6, prevPhase + 1);
    if (fb.difficulty === 'too_hard') nextPhase = completedSets < 20 ? Math.max(1, prevPhase - 1) : prevPhase;

    const userContent = buildTrainerUserContent(intake, null, nextPhase);
    userContent.push({
      type: 'text',
      text: `This user just FINISHED a 4-week block (block ${prev.block_number}, Phase ${prevPhase}) — design block ${prev.block_number + 1} at Phase ${nextPhase} (${PHASES[nextPhase].label}) that progresses from it.\n` +
        `Previous block (for reference, do not repeat verbatim — progress it):\n${JSON.stringify(prev.program.weeks?.map((w) => ({ week: w.week, days: w.days?.map((d) => ({ day: d.day, focus: d.focus, main: d.main?.map((m) => m.exercise_id) })) })))}\n` +
        `Completion: ${completedSets} sets checked off across the block.\n` +
        `Check-in feedback: difficulty was "${fb.difficulty}"${fb.skipped ? `; they tended to skip: ${fb.skipped}` : ''}${fb.notes ? `; notes: ${fb.notes}` : ''}.\n` +
        `Adjust accordingly: too_easy → harder variations/more volume; too_hard → dial back; swap in fresh exercises to fight boredom; drop or replace what they skipped. why_this_works should acknowledge that they completed a block and what changes this time.`,
    });

    // Sleep Coach cross-feature rule: bad night → longer warm-up, never a
    // shorter or lighter workout.
    const trainerSleepLine = sleepContextForTrainer(await getTodaysSleep(req.user.id));
    if (trainerSleepLine) userContent.push({ type: 'text', text: trainerSleepLine });
    const trainerWeightLine = await getWeightContext(req.user.id);
    if (trainerWeightLine) userContent.push({ type: 'text', text: trainerWeightLine });

    let program;
    try {
      program = await callTrainerModel(TRAINER_SYSTEM_PROMPT, userContent);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'Program generation failed. Please try again.' });
    }
    if (!program?.weeks?.length) return res.status(502).json({ error: 'Model returned an unusable program.' });
    sanitizeProgram(program, intake.equipment);
    program.phase = nextPhase;
    if (program.assessment) program.assessment.starting_phase = nextPhase;

    const ins = await db.query(
      `INSERT INTO programs (user_id, block_number, intake, program) VALUES ($1, $2, $3, $4) RETURNING id`,
      [req.user.id, prev.block_number + 1, JSON.stringify(intake), JSON.stringify(program)]
    );
    res.json({
      programId: ins.rows[0].id,
      blockNumber: prev.block_number + 1,
      locked: false,
      program: { ...program, locked: false },
    });
  } catch (err) {
    console.error('checkin error:', err);
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
  required: ['verdict', 'confidence', 'confidence_reason', 'where_agreed', 'where_split', 'reasoning', 'next_actions'],
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

You must not diagnose or prescribe. Output your opinion as JSON matching the provided schema: a one-sentence position, your reasoning, the strongest argument against the default path, and what evidence would change your mind.`;

const COACH_PROMPT = `You are THE COACH, a member of the Abs by AI Decision Counsel.

Your role: ignore the lab and look at the user's actual life. Two interventions with identical evidence are not equal if one fits this person's schedule, budget, and psychology and the other doesn't. Adherence beats optimization, every time.

Rules:
- Ground everything in the intake details: their schedule, budget, training history, past failed attempts, and stated goals. Quote their own words back to them when relevant.
- Evaluate: Will they actually stick to this? What does it cost per month, and is that sustainable for years, not weeks? What does it displace — does adding this crowd out something more important?
- Prefer the smallest change that moves the needle. If the user is asking about an advanced intervention while a basic one is unhandled (sleeping 5 hours, protein at half target, program-hopping), say so directly — that IS your recommendation.
- Give a concrete implementation picture: what week 1 actually looks like if they proceed, and the single most likely failure point.
- Tone: warm, direct, experienced. Like a coach who has watched hundreds of people succeed and fail and knows the difference is rarely the supplement stack.

You do not evaluate study quality (the Researcher does that) or medical risk (the Safety Officer does that). Output your opinion as JSON matching the provided schema: a one-sentence position, your reasoning, an adherence risk rating (LOW/MEDIUM/HIGH) with the reason, and the one thing you'd have them do first.`;

const SAFETY_PROMPT = `You are THE SAFETY OFFICER, a member of the Abs by AI Decision Counsel.

Your role: identify every safety issue in the user's question — interactions, contraindications, red flags, and above all, which parts of this decision require a real medical professional. You are the counsel's line of defense, and you are explicitly empowered to overrule enthusiasm.

Rules:
- For supplement audits: check every listed item against the others AND against any listed medications for known interactions (e.g., stimulant stacking, blood-thinning combinations, absorption conflicts, liver load). Flag dosages above commonly studied ranges. Note which supplements are poorly regulated categories with contamination history.
- For hormonal/pharmaceutical questions (TRT, GLP-1s, etc.): these are prescription medications, so a physician is already in the loop by definition — "requires a doctor" is NOT a danger signal in itself and does not justify a RED on its own. Modern, properly supervised GLP-1 and TRT treatment is safe and effective for the right candidate, and the benefits (appetite regulation, reduced alcohol and junk-food cravings, metabolic health, restored energy and libido) are real and well-documented. Your job is to help the user pursue it WELL: what labs to ask for, what questions to bring, what monitoring proper treatment requires. Reserve flags for genuine red flags: gray-market or compounded sourcing without oversight, doses from forums, online clinics that prescribe without labs, eating-disorder history, contraindicated conditions, or already-lean users chasing purely cosmetic loss.
- For injury/return-to-training questions: distinguish general reconditioning principles (which you may discuss) from clearance decisions (which belong to their physician or physical therapist). List the red-flag symptoms that mean stop and seek care.
- Rate the overall decision: GREEN (safe to self-manage), YELLOW (proceed with specific precautions), RED (a specific red flag means stop and see a professional before acting). For prescription interventions, YELLOW is the natural default — "pursue this through your doctor with proper labs and monitoring" IS the specific precaution. Use RED only when you can name a concrete red flag from the intake, not because the category feels medical. You are a safety officer, not a gatekeeper — when the case looks like a good candidate, say so plainly.
- Never diagnose, never prescribe, never estimate doses for prescription compounds.

Tone: calm and precise, not alarmist. You make risk legible, you don't catastrophize.
Output your opinion as JSON matching the provided schema: the GREEN/YELLOW/RED rating, a one-sentence position, itemized flags (each with severity), and exactly what to ask a doctor if a doctor is needed.`;

const PRESIDENT_PROMPT = `You are THE PRESIDENT of the Abs by AI Decision Counsel. Four counselors — the Researcher, the Skeptic, the Coach, and the Safety Officer — have independently reviewed the user's case. You have their full written opinions plus the user's original intake. Your job is to deliver the final verdict.

Rules:
- Read all four opinions before forming your view. Identify where they AGREE (this is your foundation — consensus across independent perspectives is strong signal) and where they DISAGREE (name the disagreement honestly; do not paper over it).
- The Safety Officer holds a special veto: if they rated the decision RED, your verdict MUST route through a medical professional as the primary recommendation. You may still advise on everything within the user's control in the meantime. A YELLOW is not a veto — "pursue it with proper medical supervision" is fully compatible with a confident "Yes".
- Do not be reflexively conservative about well-evidenced prescription interventions (GLP-1s, TRT). If the case is a good candidate, say "Yes — pursue this with your doctor" plainly; the report carries a not-medical-advice disclaimer, so you do not need to hedge the verdict itself.
- Issue ONE clear verdict. The user came here because "it depends" wasn't good enough. Formats like "Yes, but only after X" or "No — do Y instead" are verdicts; "here are some considerations" is not.
- State your confidence: HIGH (counsel consensus + strong evidence), MODERATE (some dissent or mixed evidence), or LOW (genuine split — and then explain what information would resolve it).
- End with exactly 3 concrete next actions, ordered, each doable within two weeks.
- Credit the counselors by role when you draw on them ("As the Skeptic pointed out..."). If you side against a counselor, say why in one sentence.
- Tone: decisive, fair, human. A good chairperson, not a hedge-fund disclaimer.

You must not diagnose or prescribe. Output as JSON matching the provided schema: verdict (one sentence), confidence with reason, where the counsel agreed, where it split, full reasoning, and the 3 next actions.`;

// Per-decision-type addendum appended to every counselor's system prompt.
const COUNSEL_TYPE_ADDENDA = {
  'supplement-audit': `\n\nThis case is a SUPPLEMENT AUDIT. The user has listed their current (or planned) supplement stack with doses, plus any medications. Address every listed item — nothing on the list should go unmentioned in the counsel's collective output — and weigh the stack as a whole, not just each item in isolation.`,
  'glp1-trt': `\n\nThis case is a GLP-1 / TRT DECISION. The question before the counsel is: "Is this intervention worth pursuing with a physician, and how should this user pursue it well?" — NOT "should the user self-start a drug" (they can't; it's prescription-only, so a doctor is in the loop by definition). A clear "Yes — this looks like a strong candidate case; here's how to pursue it" is a normal, reachable outcome and should be given when the case supports it. These interventions are well-evidenced and their benefits often go beyond the scale (appetite regulation, reduced alcohol and junk-food consumption, metabolic health, energy). Weigh benefits as rigorously as risks. Never prescribe or estimate doses; the counsel prepares the user for the physician conversation.`,
  'injury-return': `\n\nThis case is a RETURN-FROM-INJURY decision. The user wants to know whether and how to get back to training. General reconditioning principles are fair game; clearance decisions belong to their physician or physical therapist. Be specific about what a safe ramp actually looks like.`,
  'physique-direction': `\n\nThis case is a PHYSIQUE DIRECTION decision. The user is choosing what to pursue next with their body (bulk, cut, recomp, maintain — and what that implies for training and eating). If photos are provided, ground your assessment in what you can actually see. Be honest about realistic timelines.`,
  custom: `\n\nThis is a CUSTOM QUESTION the user has brought to the counsel. Answer the question they actually asked. If the question is outside fitness/health/nutrition territory, say so and answer the nearest in-scope version of it.`,
};

const COUNSEL_SEATS = [
  { role: 'researcher', name: 'The Researcher', prompt: RESEARCHER_PROMPT, schema: RESEARCHER_SCHEMA },
  { role: 'skeptic', name: 'The Skeptic', prompt: SKEPTIC_PROMPT, schema: SKEPTIC_SCHEMA },
  { role: 'coach', name: 'The Coach', prompt: COACH_PROMPT, schema: COACH_SCHEMA },
  { role: 'safety', name: 'The Safety Officer', prompt: SAFETY_PROMPT, schema: SAFETY_SCHEMA },
];

// Fields accepted per decision type. Everything is treated as free-ish text
// and clamped hard — the model reads it, so length limits are the defense.
const COUNSEL_INTAKE_FIELDS = {
  'supplement-audit': { arrays: ['supplements', 'medications'], strings: ['age', 'sex', 'goal', 'budget_monthly', 'notes'] },
  'glp1-trt': { arrays: [], strings: ['subject', 'age', 'sex', 'height_in', 'weight_lb', 'weight_history', 'training_history', 'tried', 'symptoms_motivation', 'budget_monthly', 'doctor_access', 'notes'] },
  'injury-return': { arrays: [], strings: ['injury', 'when', 'treatment', 'current_pain', 'clearance', 'goal', 'notes'] },
  'physique-direction': { arrays: ['inspirations'], strings: ['age', 'sex', 'height_in', 'weight_lb', 'timeline', 'lifestyle', 'goal', 'notes'] },
  custom: { arrays: [], strings: ['question', 'age', 'sex', 'goal', 'notes'] },
};

function validateCounselIntake(decisionType, raw) {
  const fields = COUNSEL_INTAKE_FIELDS[decisionType];
  if (!fields || !raw || typeof raw !== 'object') return null;
  const intake = {};
  let filled = 0;
  for (const key of fields.strings) {
    const v = String(raw[key] ?? '').trim().slice(0, 600);
    if (v) { intake[key] = v; filled++; }
  }
  for (const key of fields.arrays) {
    const arr = Array.isArray(raw[key])
      ? raw[key].slice(0, 20).map((s) => String(s).trim().slice(0, 150)).filter(Boolean)
      : [];
    if (arr.length) { intake[key] = arr; filled++; }
  }
  if (decisionType === 'custom' && !intake.question) return null;
  if (decisionType === 'supplement-audit' && !(intake.supplements || []).length) return null;
  return filled ? intake : null;
}

const COUNSEL_TYPE_LABELS = {
  'supplement-audit': 'Supplement stack audit',
  'glp1-trt': 'GLP-1 / TRT decision',
  'injury-return': 'Returning from injury',
  'physique-direction': 'Physique direction',
  custom: 'Custom question',
};

function buildCounselUserContent(decisionType, intake, photos) {
  const content = [];
  const { beforeBase64, beforeMime, afterBase64, afterMime } = photos || {};
  if (beforeBase64 && beforeMime) {
    content.push({ type: 'image', source: { type: 'base64', media_type: beforeMime, data: beforeBase64 } });
    content.push({ type: 'text', text: "CURRENT photo — the user's body today (shared with consent). Ground your assessment in what you can see. Never judgmental." });
  }
  if (afterBase64 && afterMime) {
    content.push({ type: 'image', source: { type: 'base64', media_type: afterMime, data: afterBase64 } });
    content.push({ type: 'text', text: 'GOAL photo — an AI-generated image of the physique the user is aiming for.' });
  }
  content.push({
    type: 'text',
    text: `Decision type: ${COUNSEL_TYPE_LABELS[decisionType]}\n\nUser intake:\n${JSON.stringify(intake, null, 2)}\n\nGive your independent opinion as your seat on the counsel. Output JSON matching the provided schema.`,
  });
  return content;
}

async function callCounselSeat(systemPrompt, userContent, schema, maxTokens) {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
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
      output_config: { format: { type: 'json_schema', schema } },
      messages: [{ role: 'user', content: userContent }],
    }),
  });
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

function buildPresidentContent(decisionType, intake, opinions, missingSeats) {
  let text = `Decision type: ${COUNSEL_TYPE_LABELS[decisionType]}\n\nUser intake:\n${JSON.stringify(intake, null, 2)}\n\n`;
  for (const seat of COUNSEL_SEATS) {
    const op = opinions[seat.role];
    text += op
      ? `=== Opinion of ${seat.name} ===\n${JSON.stringify(op, null, 2)}\n\n`
      : `=== ${seat.name} ===\n(This counselor's seat was empty for this session — their opinion is unavailable.)\n\n`;
  }
  if (missingSeats.length) {
    text += `NOTE: ${missingSeats.join(', ')} could not deliver an opinion this session. Acknowledge the absence briefly in your reasoning and weigh the remaining opinions accordingly.\n\n`;
  }
  text += `Deliver the final verdict as JSON matching the provided schema.`;
  return [{ type: 'text', text }];
}

// Free-preview shape: the verdict sentence + safety rating are the hook;
// reasoning, evidence, and next actions are members-only.
function stripCounselForPreview(counsel) {
  const v = counsel.verdict || {};
  return {
    locked: true,
    verdict: { verdict: v.verdict, confidence: v.confidence, locked: true },
    opinions: Object.fromEntries(Object.entries(counsel.opinions || {}).map(([role, op]) => [
      role,
      op ? { position: op.position, ...(op.rating ? { rating: op.rating } : {}), locked: true } : null,
    ])),
  };
}

// Convene the counsel. Free for everyone (sunk-cost hook) — members get the
// full case file back; free users get the verdict-level preview.
app.post('/api/counsel', aiLimiter, optionalAuth, async (req, res) => {
  try {
    const decisionType = String(req.body?.decisionType || '');
    const intake = validateCounselIntake(decisionType, req.body?.intake);
    if (!intake) return res.status(400).json({ error: 'Missing or incomplete intake for this decision type' });

    // Monthly cap: 10 counsel sessions per account per calendar month (each
    // run is 5 model calls — this keeps membership economics sane). Checked
    // before convening the seats so a capped request costs nothing.
    if (req.user && db) {
      try {
        const { rows } = await db.query(
          `SELECT COUNT(*)::int AS n FROM counsel_sessions
           WHERE user_id = $1 AND created_at >= date_trunc('month', now())`,
          [req.user.id]
        );
        if (rows[0].n >= COUNSEL_MONTHLY_CAP) {
          return res.status(429).json({
            error: `You've used all ${COUNSEL_MONTHLY_CAP} Decision Counsel sessions for this month. Your allowance resets on the 1st.`,
            capReached: true,
          });
        }
      } catch (e) { console.error('counsel cap check error:', e.message); }
    }

    const { photoBase64, photoMime, afterPhotoBase64, afterPhotoMime, photoConsent } = req.body || {};
    const photos = (decisionType === 'physique-direction' && photoConsent) ? {
      beforeBase64: photoBase64, beforeMime: photoMime,
      afterBase64: afterPhotoBase64, afterMime: afterPhotoMime,
    } : null;

    const addendum = COUNSEL_TYPE_ADDENDA[decisionType];
    const userContent = buildCounselUserContent(decisionType, intake, photos);

    // Phase 1: four independent opinions in parallel, each with one retry.
    const results = await Promise.all(COUNSEL_SEATS.map((seat) =>
      callSeatResilient(seat.name, () => callCounselSeat(seat.prompt + addendum, userContent, seat.schema, 8000))
    ));
    const opinions = {};
    const missingSeats = [];
    COUNSEL_SEATS.forEach((seat, i) => {
      const op = results[i];
      if (op && op.position) opinions[seat.role] = op;
      else { opinions[seat.role] = null; missingSeats.push(seat.name); }
    });
    if (missingSeats.length > 1) {
      return res.status(502).json({ error: 'The counsel could not convene. Please try again in a moment.' });
    }

    // Phase 2: the President synthesizes. This seat is required.
    const verdict = await callSeatResilient('The President', () =>
      callCounselSeat(PRESIDENT_PROMPT + addendum, buildPresidentContent(decisionType, intake, opinions, missingSeats), PRESIDENT_SCHEMA, 10000)
    );
    if (!verdict || !verdict.verdict) {
      return res.status(502).json({ error: 'The President could not reach a verdict. Please try again.' });
    }
    verdict.next_actions = (verdict.next_actions || []).slice(0, 3);

    const counsel = { opinions, verdict, missingSeats };

    let sessionId = null;
    let member = false;
    if (req.user && db) {
      member = isActiveMembership(req.user);
      try {
        const { rows } = await db.query(
          `INSERT INTO counsel_sessions (user_id, decision_type, intake, opinions, verdict) VALUES ($1, $2, $3, $4, $5) RETURNING id`,
          [req.user.id, decisionType, JSON.stringify(intake), JSON.stringify(opinions), JSON.stringify(verdict)]
        );
        sessionId = rows[0].id;
      } catch (e) { console.error('counsel save error:', e.message); }
    }

    res.json({
      sessionId,
      decisionType,
      locked: !member,
      counsel: member ? { ...counsel, locked: false } : stripCounselForPreview(counsel),
    });
  } catch (err) {
    console.error('counsel error:', err);
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

    const content = buildPresidentContent(row.decision_type, row.intake, row.opinions, []);
    content.push({
      type: 'text',
      text: `\nYou already delivered this verdict:\n${JSON.stringify(row.verdict, null, 2)}\n\n` +
        ((row.followups || []).length ? `Previous follow-up Q&A:\n${JSON.stringify(row.followups, null, 2)}\n\n` : '') +
        `The user now has a FOLLOW-UP QUESTION about your verdict: "${question}"\n\nAnswer it directly and consistently with the case file. Do not re-issue the verdict unless the question genuinely changes it. Output JSON matching the provided schema.`,
    });

    let reply;
    try {
      reply = await callCounselSeat(PRESIDENT_PROMPT + (COUNSEL_TYPE_ADDENDA[row.decision_type] || ''), content, FOLLOWUP_SCHEMA, 4000);
    } catch (e) {
      if (e.status) return res.status(e.status).json({ error: e.message });
      return res.status(502).json({ error: 'The President is unavailable. Please try again.' });
    }
    if (!reply?.answer) return res.status(502).json({ error: 'The President could not answer. Please try again.' });

    const followups = [...(row.followups || []), { question, answer: reply.answer, at: new Date().toISOString() }].slice(-20);
    await db.query('UPDATE counsel_sessions SET followups = $1 WHERE id = $2 AND user_id = $3',
      [JSON.stringify(followups), row.id, req.user.id]);
    res.json({ sessionId: row.id, question, answer: reply.answer, followups });
  } catch (err) {
    console.error('counsel followup error:', err);
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
    const { productType, size, framed, priceInCents, imageId, imagePreviewUrl, imgWidth, imgHeight, productLabel, returnUrl } = req.body || {};
    if (!productType || !size || !priceInCents || !returnUrl) {
      return res.status(400).json({ error: 'Missing required fields' });
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
          unit_amount: priceInCents,
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
        imageId: imageId || '',
        imagePreviewUrl: imagePreviewUrl || '',
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
  const imageSrc = imagePreviewUrl || (imageId ? `https://images-api.printify.com/${imageId}` : '');

  if (!PRINTIFY_API_KEY || !PRINTIFY_SHOP_ID) {
    console.warn('Printify not configured — product order recorded but not submitted');
    return false;
  }
  if (!imageSrc || !productType || !size) {
    console.warn('Product order missing image/product/size — not submitted to Printify');
    return false;
  }

  const variantKey = productType === 'canvas' ? `${size}_${framedBool ? 'framed' : 'unframed'}` : size;
  const variant = PRODUCT_CONFIG[productType]?.variants[variantKey];
  if (!variant || !variant.variantId) {
    console.warn(`Printify variant not configured for ${productType}/${variantKey} — order NOT submitted`);
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
app.use(express.static('.'));

// Serve index.html for all non-API, non-dashboard routes (SPA fallback)
app.get('*', (req, res) => {
  res.sendFile(__dirname + '/index.html');
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

