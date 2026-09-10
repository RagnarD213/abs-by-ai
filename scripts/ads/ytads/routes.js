'use strict';
//
// YTADS ROUTES — the server half of the YouTube engagement-champion system.
//
//   POST /api/ytads/sync     ← the Google Ads Script posts the account snapshot every
//                              hour; we read the channel feed, write headlines for new
//                              videos, run the engine, record the run, return commands.
//   POST /api/ytads/results  ← the script reports what each command did (ids created,
//                              Google's errors verbatim); we turn them into events.
//   GET  /api/ytads/state    ← the brief block (dashboard-gated, see DASH_APIS).
//
// Auth for the first two: header `X-YTADS-Key` must equal YTADS_KEY (Railway). Fails
// closed — with the key unset the routes 503. The switch: YTADS_ENABLED=1 makes the
// commands real; anything else returns every command with dryRun:true and the script
// executes nothing (it logs). One switch, same shape as the Meta auto-boost.
//
// What is stored: `ytads_runs` (one row per sync: snapshot, commands, report, results)
// and `ytads_events` (headlines, created, verdict, promote, skip, error, policy,
// dayone). Google remains the ledger for "which video has an ad where".

const crypto = require('crypto');
const engine = require('./engine.js');
const { fetchVideos } = require('./feed.js');
const { generateHeadlines } = require('./headlines.js');
const { buildBrief } = require('./brief.js');
const thumbs = require('./thumbs.js');

const START_DATE_DEFAULT = '2026-09-03';   // go-live day; videos published before it are history
const HEADLINE_TIME_BUDGET_MS = 20000;     // the script is waiting on this request; the rest is generated after we respond
const RUNS_TO_KEEP = 300;

function loadSkiplist() {
  try { return JSON.parse(require('fs').readFileSync(require('path').join(__dirname, 'skiplist.json'), 'utf8')); } catch { return { videoIds: [], titlePatterns: [] }; }
}

function safeEq(a, b) {
  const ab = Buffer.from(String(a)), bb = Buffer.from(String(b));
  return ab.length === bb.length && crypto.timingSafeEqual(ab, bb);
}

module.exports = function mountYtads(app, { pool }) {
  const enabled = () => process.env.YTADS_ENABLED === '1';
  const config = () => ({ startDate: process.env.YTADS_START_DATE || START_DATE_DEFAULT, skiplist: loadSkiplist() });

  let schemaReady = null;
  function ensureSchema() {
    if (!pool) return Promise.reject(new Error('no DATABASE_URL'));
    if (!schemaReady) {
      schemaReady = pool.query(`
        CREATE TABLE IF NOT EXISTS ytads_events (
          id           SERIAL PRIMARY KEY,
          video_id     TEXT,
          campaign_key TEXT,
          ad_id        TEXT,
          event        TEXT NOT NULL,
          detail       JSONB,
          at           TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        CREATE INDEX IF NOT EXISTS ytads_events_video_idx ON ytads_events (video_id);
        CREATE INDEX IF NOT EXISTS ytads_events_at_idx ON ytads_events (at);
        CREATE TABLE IF NOT EXISTS ytads_manual (
          id         SERIAL PRIMARY KEY,
          at         TIMESTAMPTZ NOT NULL DEFAULT now(),
          note       TEXT,
          command    JSONB NOT NULL,
          status     TEXT NOT NULL DEFAULT 'pending',
          run_id     INTEGER,
          result     JSONB,
          done_at    TIMESTAMPTZ
        );
        CREATE TABLE IF NOT EXISTS ytads_runs (
          id         SERIAL PRIMARY KEY,
          at         TIMESTAMPTZ NOT NULL DEFAULT now(),
          dry_run    BOOLEAN NOT NULL,
          enabled    BOOLEAN NOT NULL,
          snapshot   JSONB,
          commands   JSONB NOT NULL,
          report     JSONB NOT NULL,
          results    JSONB,
          results_at TIMESTAMPTZ
        );
      `).catch(e => { schemaReady = null; throw e; });
    }
    return schemaReady;
  }

  const db = {
    // The saved original thumbnails (base64) are left out: the engine never needs them.
    events: async () => (await pool.query("SELECT id, video_id, campaign_key, ad_id, event, CASE WHEN event = 'thumb:original' THEN '{}'::jsonb ELSE detail END AS detail, at FROM ytads_events ORDER BY at")).rows,
    event: (videoId, key, adId, event, detail) =>
      pool.query('INSERT INTO ytads_events (video_id, campaign_key, ad_id, event, detail) VALUES ($1, $2, $3, $4, $5)',
                 [videoId || null, key || null, adId == null ? null : String(adId), event, JSON.stringify(detail || {})]),
    run: async (dryRun, isEnabled, snapshot, commands, report) => {
      const r = await pool.query('INSERT INTO ytads_runs (dry_run, enabled, snapshot, commands, report) VALUES ($1, $2, $3, $4, $5) RETURNING id, at',
                                 [dryRun, isEnabled, JSON.stringify(snapshot), JSON.stringify(commands), JSON.stringify(report)]);
      await pool.query(`DELETE FROM ytads_runs WHERE id NOT IN (SELECT id FROM ytads_runs ORDER BY at DESC LIMIT ${RUNS_TO_KEEP})`);
      return r.rows[0];
    },
    latestRun: async () => (await pool.query('SELECT id, at, dry_run, enabled, commands, report, results, results_at FROM ytads_runs ORDER BY at DESC LIMIT 1')).rows[0] || null,
    getRun: async (id) => (await pool.query('SELECT id, at, dry_run, enabled, commands, report, results, results_at FROM ytads_runs WHERE id = $1', [id])).rows[0] || null,
    saveResults: (id, results) => pool.query('UPDATE ytads_runs SET results = $2, results_at = now() WHERE id = $1', [id, JSON.stringify(results)]),
    // Dan-requested one-off edits (copy changes, re-enables, renames). Enqueued with
    // scripts/ads/ytads/manual.js; the next sync appends them to the plan as
    // commands "m<id>", and the results call marks them done or failed.
    manualPending: async () => (await pool.query("SELECT id, note, command FROM ytads_manual WHERE status = 'pending' ORDER BY id")).rows,
    manualClaim: (ids, runId) => ids.length ? pool.query("UPDATE ytads_manual SET status = 'sent', run_id = $2 WHERE id = ANY($1::int[])", [ids, runId]) : Promise.resolve(),
    manualDone: (id, ok, result) => pool.query("UPDATE ytads_manual SET status = $2, result = $3, done_at = now() WHERE id = $1", [id, ok ? 'done' : 'failed', JSON.stringify(result || {})]),
  };

  function scriptAuth(req, res, next) {
    const key = process.env.YTADS_KEY || '';
    if (!key) return res.status(503).json({ error: 'YTADS_KEY not configured' });
    const given = req.headers['x-ytads-key'] || '';
    if (!given || !safeEq(given, key)) return res.status(401).json({ error: 'Unauthorized' });
    if (!pool) return res.status(503).json({ error: 'no database' });
    next();
  }

  // Headlines for a video, written once and shared by the three campaigns.
  async function writeHeadlinesFor(video) {
    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) { await db.event(video.id, null, null, 'skip', { reason: 'no ANTHROPIC_API_KEY', title: video.title, permanent: false }); return null; }
    const r = await generateHeadlines({ video, apiKey });
    if (r.ok) {
      await db.event(video.id, null, null, 'headlines', { title: video.title, set: r.set, attempts: r.attempts, partial: !!r.partial, failures: r.failures });
      return r.set;
    }
    await db.event(video.id, null, null, 'skip', { permanent: true, reason: 'lint', title: video.title, error: r.error, failures: r.failures, attempts: r.attempts });
    return null;
  }

  // Retry rule (Dan 2026-09-10): tamer copy for a video whose ad failed Google's review —
  // written once per video and shared by the campaigns (`retrycopy` event).
  const copyInFlight = new Set();
  async function writeRetryCopyFor(w, videos) {
    if (copyInFlight.has(w.videoId)) return null;
    copyInFlight.add(w.videoId);
    try {
      const apiKey = process.env.ANTHROPIC_API_KEY;
      if (!apiKey) return null;
      const video = (videos || []).find(v => v.id === w.videoId) || { id: w.videoId, title: w.title, description: '' };
      const r = await generateHeadlines({ video, apiKey, tame: { prior: w.prior, topics: w.topics } });
      if (r.ok) { await db.event(w.videoId, null, null, 'retrycopy', { title: w.title, set: r.set, attempts: r.attempts, topics: w.topics, failures: r.failures }); return r.set; }
      await db.event(w.videoId, null, null, 'retrycopy:failed', { title: w.title, error: r.error, failures: r.failures });
      return null;
    } finally { copyInFlight.delete(w.videoId); }
  }

  // Attempt 3's thumbnail swap on the public video, and the restore once attempt 3 has
  // failed everywhere. Run after the sync has answered (they take a minute); the next
  // hourly run reads the thumb:* events. The original is saved once, before any swap.
  const thumbBusy = new Set();
  const thumbEvents = async (videoId) => (await pool.query("SELECT event, detail, at FROM ytads_events WHERE video_id = $1 AND event LIKE 'thumb:%' ORDER BY at", [videoId])).rows;
  async function thumbJobs({ thumbnails = [], restore = [] }) {
    for (const t of thumbnails) {
      if (thumbBusy.has(t.videoId)) continue;
      thumbBusy.add(t.videoId);
      try {
        const evs = await thumbEvents(t.videoId);
        if (evs.some(e => e.event === 'thumb:swapped')) continue;
        if (!evs.some(e => e.event === 'thumb:original')) {
          const cur = await thumbs.fetchCurrent(t.videoId);
          await db.event(t.videoId, null, null, 'thumb:original', { title: t.title, url: cur.url, bytes: cur.buf.length, b64: cur.buf.toString('base64') });
        }
        const made = await thumbs.makeCleanThumbnail({ videoId: t.videoId, apiKey: process.env.ANTHROPIC_API_KEY });
        if (!made.ok) { await db.event(t.videoId, null, null, 'thumb:failed', { title: t.title, reason: made.reason, transient: false }); continue; }
        await thumbs.setThumbnail(t.videoId, made.jpeg);
        await db.event(t.videoId, null, null, 'thumb:swapped', { title: t.title, frame: made.frame, crop: made.crop, bytes: made.jpeg.length, check: made.check, why: made.why });
        console.log(`YTADS clean thumbnail set on ${t.videoId} (${made.frame})`);
      } catch (e) {
        console.error(`ytads thumbnail ${t.videoId}:`, e.message);
        await db.event(t.videoId, null, null, 'thumb:failed', { title: t.title, reason: e.message, transient: true }).catch(() => {});
      } finally { thumbBusy.delete(t.videoId); }
    }
    for (const r of restore) {
      if (thumbBusy.has(r.videoId)) continue;
      thumbBusy.add(r.videoId);
      try {
        const evs = await thumbEvents(r.videoId);
        const swapped = evs.filter(e => e.event === 'thumb:swapped').pop();
        if (!swapped || evs.some(e => e.event === 'thumb:restored' && new Date(e.at) >= new Date(swapped.at))) continue;
        const orig = evs.find(e => e.event === 'thumb:original');
        if (!orig || !orig.detail || !orig.detail.b64) throw new Error('the original thumbnail was never saved');
        await thumbs.setThumbnail(r.videoId, Buffer.from(orig.detail.b64, 'base64'));
        await db.event(r.videoId, null, null, 'thumb:restored', { title: r.title, from: orig.detail.url });
        console.log(`YTADS original thumbnail restored on ${r.videoId}`);
      } catch (e) {
        console.error(`ytads thumbnail restore ${r.videoId}:`, e.message);
        await db.event(r.videoId, null, null, 'thumb:failed', { title: r.title, reason: 'restore: ' + e.message, transient: true, restore: true }).catch(() => {});
      } finally { thumbBusy.delete(r.videoId); }
    }
  }

  app.post('/api/ytads/sync', scriptAuth, async (req, res) => {
    const t0 = Date.now();
    try {
      await ensureSchema();
      const snapshot = req.body || {};
      if (!Array.isArray(snapshot.ads) || !Array.isArray(snapshot.campaigns)) return res.status(400).json({ error: 'snapshot needs campaigns[] and ads[]' });
      const cfg = config();
      const isEnabled = enabled();
      const dryRun = !isEnabled;
      const warnings = [];

      let videos = [];
      try { videos = await fetchVideos(); }
      catch (e) { warnings.push(`YouTube feed unreadable this hour: ${e.message}`); }

      let events = await db.events();
      const headlinesByVideo = {};
      for (const e of events) if (e.event === 'headlines' && e.detail && e.detail.set) headlinesByVideo[e.video_id] = e.detail.set;

      // Headlines for candidates that have none — within a time budget; the rest after we answer.
      const { candidates } = engine.candidates({ snapshot, videos, events, config: cfg });
      const needing = candidates.map(c => c.video).filter(v => !headlinesByVideo[v.id] && !events.some(e => e.video_id === v.id && (e.event === 'headlines' || (e.event === 'skip' && e.detail && e.detail.permanent))));
      const deferred = [];
      for (const v of needing) {
        if (Date.now() - t0 > HEADLINE_TIME_BUDGET_MS) { deferred.push(v); continue; }
        try { const set = await writeHeadlinesFor(v); if (set) headlinesByVideo[v.id] = set; }
        catch (e) { warnings.push(`headlines for ${v.id} failed: ${e.message}`); }
      }
      if (deferred.length) {
        warnings.push(`headlines for ${deferred.length} video(s) are being written after this run; their ads are created next hour`);
        setImmediate(async () => { for (const v of deferred) { try { await writeHeadlinesFor(v); } catch (e) { console.error('ytads deferred headlines:', e.message); } } });
      }
      events = await db.events();

      const retryCopy = () => { const m = {}; for (const e of events) if (e.event === 'retrycopy' && e.detail && e.detail.set) m[e.video_id] = e.detail.set; return m; };
      const planNow = () => engine.plan({ snapshot, videos, events, headlinesByVideo, retryCopyByVideo: retryCopy(), now: new Date(), config: cfg, dryRun });
      let { commands, report } = planNow();

      // Retry rule: tamer copy for videos whose ad failed review — same time budget; the rest after we answer.
      if (report.retry.waitingCopy.length) {
        let wrote = 0; const later = [];
        for (const w of report.retry.waitingCopy) {
          if (Date.now() - t0 > HEADLINE_TIME_BUDGET_MS) { later.push(w); continue; }
          try { if (await writeRetryCopyFor(w, videos)) wrote++; } catch (e) { warnings.push(`tamer copy for ${w.videoId} failed: ${e.message}`); }
        }
        if (later.length) {
          warnings.push(`tamer copy for ${later.length} video(s) is being written after this run; their resubmissions are created next hour`);
          setImmediate(async () => { for (const w of later) { try { await writeRetryCopyFor(w, videos); } catch (e) { console.error('ytads deferred retry copy:', e.message); } } });
        }
        if (wrote) { events = await db.events(); ({ commands, report } = planNow()); }
      }
      for (const s of report.retry.seen) await db.event(s.videoId, s.campaign, s.adId, 'limited:seen', {});
      report.warnings = [...warnings, ...report.warnings];
      report.videosSeen = videos.length;

      // Dan's one-off edits ride along with the hourly plan (live runs only; a dry run
      // would report them skipped and they must stay pending until a live run).
      const manual = dryRun ? [] : await db.manualPending();
      for (const m of manual) commands.push({ ...m.command, id: `m${m.id}`, manualId: m.id, reason: m.command.reason || 'manual', note: m.note || null, dryRun: false });
      if (manual.length) report.counts.manual = manual.length;

      const snapshotStored = { ...snapshot, receivedAt: new Date().toISOString() };
      const run = await db.run(dryRun, isEnabled, snapshotStored, commands, report);
      await db.manualClaim(manual.map(m => m.id), run.id);

      // A chain given up on is recorded BEFORE the script removes its ads (removed ads leave the snapshot).
      if (!dryRun) for (const f of report.retry.failed) await db.event(f.videoId, f.campaign, null, 'retry:failed', { runId: run.id, title: f.title, removed: f.removed });
      if (!dryRun && (report.retry.thumbnails.length || report.retry.restore.length)) {
        setImmediate(() => thumbJobs(report.retry).catch(e => console.error('ytads thumbs:', e.message)));
      }

      // Day-one pause list is written BEFORE the script executes it — reversibility.
      for (const [key, c] of Object.entries(report.campaigns)) {
        if (c.dayOne && (c.dayOne.champion || c.dayOne.paused.length)) {
          await db.event(null, key, c.dayOne.champion ? c.dayOne.champion.adId : null, 'dayone',
                         { dryRun, runId: run.id, reason: c.dayOne.reason, champion: c.dayOne.champion, paused: c.dayOne.paused, reversal: c.dayOne.reversal });
        }
      }

      console.log(`YTADS sync run ${run.id}: ${dryRun ? 'DRY RUN' : 'LIVE'}, ${commands.length} command(s), ${videos.length} videos in feed, ${Date.now() - t0}ms`);
      res.json({
        runId: run.id, dryRun, enabled: isEnabled, startDate: cfg.startDate,
        labels: Object.values(engine.LABELS),
        commands,
        summary: { counts: report.counts, warnings: report.warnings },
      });
    } catch (e) {
      console.error('ytads sync error:', e.stack || e.message);
      res.status(500).json({ error: e.message });
    }
  });

  app.post('/api/ytads/results', scriptAuth, async (req, res) => {
    try {
      await ensureSchema();
      const { runId, results } = req.body || {};
      if (!runId || !Array.isArray(results)) return res.status(400).json({ error: 'need runId and results[]' });
      const run = await db.getRun(runId);
      if (!run) return res.status(404).json({ error: 'unknown run' });
      const byId = {}; for (const c of (run.commands || [])) byId[c.id] = c;
      const executed = results.filter(r => !r.skipped);
      await db.saveResults(runId, { at: new Date().toISOString(), dryRun: !!run.dry_run, results });

      if (!run.dry_run) {
        const dayOneOutcome = {};
        for (const r of results) {
          const c = byId[r.id]; if (!c) continue;
          const base = { runId, op: c.op, reason: c.reason || null, message: r.error || null };
          if (c.manualId) {
            await db.manualDone(c.manualId, !!r.ok, r);
            await db.event(c.videoId || null, c.campaign || null, c.adId || null, r.ok ? 'manual' : 'error', { ...base, manualId: c.manualId, note: c.note || null, mutation: c.mutation || null });
            continue;
          }
          if (!r.ok) { await db.event(c.videoId || null, c.campaign, c.adId || null, 'error', { ...base, name: c.name || null }); }
          if (c.op === 'createAd' && r.ok) {
            await db.event(c.videoId, c.campaign, r.adId || null, 'created', { name: c.name, attempt: c.attempt || 1, resourceName: r.resourceName || null, videoTitle: c.videoTitle,
              headlines: c.headlines, longHeadlines: c.longHeadlines, descriptions: c.descriptions, labelErrors: r.labelErrors || null });
          } else if (c.op === 'pauseAd' && r.ok && /^verdict:/.test(c.reason || '')) {
            await db.event(c.videoId, c.campaign, c.adId, 'verdict', { verdict: c.reason.replace('verdict:', ''), detail: c.verdict || null });
          } else if (c.op === 'label' && r.ok && c.reason === 'promote') {
            await db.event(c.videoId, c.campaign, c.adId, 'promote', { detail: c.verdict || null });
          } else if (c.op === 'pauseAd' && r.ok && c.reason === 'policy:disapproved') {
            await db.event(c.videoId, c.campaign, c.adId, 'policy', { topics: c.topics || [] });
          } else if (c.op === 'mutate' && r.ok && c.reason === 'retry:remove') {
            await db.event(c.videoId, c.campaign, c.adId, 'retry:removed', { note: c.note || null });
          } else if (/^dayone:/.test(c.reason || '')) {
            (dayOneOutcome[c.campaign] = dayOneOutcome[c.campaign] || []).push({ adId: c.adId, op: c.op, ok: !!r.ok, error: r.error || null });
          }
        }
        for (const [key, list] of Object.entries(dayOneOutcome)) await db.event(null, key, null, 'dayone:executed', { runId, outcomes: list });
      }
      console.log(`YTADS results run ${runId}: ${executed.filter(r => r.ok).length} ok, ${executed.filter(r => !r.ok).length} failed${run.dry_run ? ' (dry run)' : ''}`);
      res.json({ ok: true, recorded: results.length });
    } catch (e) {
      console.error('ytads results error:', e.stack || e.message);
      res.status(500).json({ error: e.message });
    }
  });

  // A read channel for ONE-OFF Ads Scripts. The Google Ads UI freezes for minutes at a
  // time, so a one-off script posts what it read (and what it changed) here instead of
  // relying on the editor's log panel; we read it back from Postgres. Same script key.
  app.post('/api/ytads/dump', scriptAuth, async (req, res) => {
    try {
      await ensureSchema();
      const body = req.body || {};
      const tag = String(body.tag || 'oneoff').slice(0, 60);
      const r = await pool.query(
        'INSERT INTO ytads_events (video_id, campaign_key, ad_id, event, detail) VALUES (NULL, $1, NULL, $2, $3) RETURNING id',
        [tag, 'dump', JSON.stringify(body)]);
      console.log(`YTADS dump ${tag}: event ${r.rows[0].id}`);
      res.json({ ok: true, eventId: r.rows[0].id });
    } catch (e) {
      console.error('ytads dump error:', e.stack || e.message);
      res.status(500).json({ error: e.message });
    }
  });

  // Dashboard-gated (listed in DASH_APIS). The brief block + the raw latest run.
  app.get('/api/ytads/state', async (req, res) => {
    try {
      if (!pool) return res.json({ ok: false, reason: 'no database' });
      await ensureSchema();
      const run = await db.latestRun();
      const since = new Date(Date.now() - 48 * 3600e3).toISOString();
      const events = (await pool.query('SELECT video_id, campaign_key, ad_id, event, detail, at FROM ytads_events WHERE at >= $1 ORDER BY at', [since])).rows;
      const brief = buildBrief({ run, events, enabled: enabled() });
      res.json({ ...brief, run: run ? { id: run.id, at: run.at, commands: run.commands, results: run.results } : null });
    } catch (e) {
      res.status(500).json({ ok: false, reason: e.message });
    }
  });
};
