const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const fetch = require('node-fetch');
const fs = require('fs');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
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
      const timeStr = startTime
        ? new Date(startTime).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
        : 'All day';

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

app.post('/api/push/subscribe', async (req, res) => {
  if (!GITHUB_TOKEN) return res.status(503).json({ error: 'storage not configured' });
  const sub = req.body;
  if (!sub || !sub.endpoint) return res.status(400).json({ error: 'invalid subscription' });
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
        model: 'claude-sonnet-4-6',
        max_tokens: 2048,
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
// ENDPOINT 3: Generate image (Gemini)
// ============================================================
app.post('/api/generate-image', aiLimiter, async (req, res) => {
  try {
    const { prompt, photoBase64, photoMime } = req.body;

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

    res.json({ imageBase64 });
  } catch (err) {
    console.error('Image generation error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

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

