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
    events: async () => (await pool.query('SELECT id, video_id, campaign_key, ad_id, event, detail, at FROM ytads_events ORDER BY at')).rows,
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

      const { commands, report } = engine.plan({ snapshot, videos, events, headlinesByVideo, now: new Date(), config: cfg, dryRun });
      report.warnings = [...warnings, ...report.warnings];
      report.videosSeen = videos.length;

      const snapshotStored = { ...snapshot, receivedAt: new Date().toISOString() };
      const run = await db.run(dryRun, isEnabled, snapshotStored, commands, report);

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
          if (!r.ok) { await db.event(c.videoId || null, c.campaign, c.adId || null, 'error', { ...base, name: c.name || null }); }
          if (c.op === 'createAd' && r.ok) {
            await db.event(c.videoId, c.campaign, r.adId || null, 'created', { name: c.name, resourceName: r.resourceName || null, videoTitle: c.videoTitle,
              headlines: c.headlines, longHeadlines: c.longHeadlines, descriptions: c.descriptions, labelErrors: r.labelErrors || null });
          } else if (c.op === 'pauseAd' && r.ok && /^verdict:/.test(c.reason || '')) {
            await db.event(c.videoId, c.campaign, c.adId, 'verdict', { verdict: c.reason.replace('verdict:', ''), detail: c.verdict || null });
          } else if (c.op === 'label' && r.ok && c.reason === 'promote') {
            await db.event(c.videoId, c.campaign, c.adId, 'promote', { detail: c.verdict || null });
          } else if (c.op === 'pauseAd' && r.ok && c.reason === 'policy:disapproved') {
            await db.event(c.videoId, c.campaign, c.adId, 'policy', { topics: c.topics || [] });
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
