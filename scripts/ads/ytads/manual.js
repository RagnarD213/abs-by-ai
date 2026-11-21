#!/usr/bin/env node
// Queue a one-off Google Ads edit that Dan asked for — and, since 2026-09-10, EXECUTE it
// at once through the Google Ads API (scripts/ads/api/client.js). The queue table stays
// the ledger; the hourly Ads Script only picks up rows still 'pending', so an edit run
// here is never sent twice. The system itself never edits an existing ad; this is the
// channel for Dan's edits.
//
//   node scripts/ads/ytads/manual.js list
//   node scripts/ads/ytads/manual.js headlines <adId> "<h1>" "<h2>" ... --note "why"
//   node scripts/ads/ytads/manual.js enable <adGroupAdResourceName> --note "why"
//   node scripts/ads/ytads/manual.js raw '<json mutation>' --note "why"
//   node scripts/ads/ytads/manual.js run [<id>]      execute pending row(s) now
//
// Flags on a new edit:
//   --dry-run   Google validates it (validateOnly) and nothing is queued or changed
//   --defer     queue only; the next LIVE hourly Ads Script run executes it (the old path,
//               and the fallback if the API is ever unavailable)
//
// Uses DATABASE_PUBLIC_URL (off-platform) or DATABASE_URL (on Railway). Customer id
// is the Abs by AI account, 342-717-0837.
const { Pool } = require('pg');
const ads = require('../api/client.js');
const CID = '3427170837';
const url = process.env.DATABASE_PUBLIC_URL || process.env.DATABASE_URL || readSecret('DATABASE_PUBLIC_URL');
if (!url) { console.error('need DATABASE_PUBLIC_URL or DATABASE_URL'); process.exit(2); }
const pool = new Pool({ connectionString: url, ssl: /railway\.internal/.test(url) ? false : { rejectUnauthorized: false } });

function readSecret(k) {
  try { const m = require('fs').readFileSync(require('os').homedir() + '/.absbyai-secrets.env', 'utf8').match(new RegExp('^' + k + '=(.*)$', 'm')); return m && m[1].replace(/^"|"$/g, ''); }
  catch (e) { return null; }
}
function optOf(argv, f) { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : null; }
function stripFlags(argv) {
  const out = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--note') { i++; continue; }
    if (argv[i] === '--dry-run' || argv[i] === '--defer') continue;
    out.push(argv[i]);
  }
  return out;
}

function build(argv) {
  const [kind, ...rest] = stripFlags(argv);
  if (kind === 'headlines') {
    const [adId, ...texts] = rest;
    if (!/^\d+$/.test(adId || '') || texts.length < 1 || texts.length > 5) throw new Error('headlines <adId> then 1–5 headline texts');
    const { LIMITS } = require('./lint.js'); const max = (LIMITS && LIMITS.headline) || 40;   // Demand Gen headline limit
    for (const t of texts) if (t.length > max) throw new Error(`headline over ${max} chars: "${t}"`);
    return { op: 'mutate', adId, reason: 'manual:headlines', headlines: texts,
             mutation: { adOperation: { update: { resourceName: `customers/${CID}/ads/${adId}`, demandGenVideoResponsiveAd: { headlines: texts.map(t => ({ text: t })) } },
                                        updateMask: 'demandGenVideoResponsiveAd.headlines' } } };
  }
  if (kind === 'enable' || kind === 'pause') {
    const [rn] = rest; if (!/^customers\/\d+\/adGroupAds\/\d+~\d+$/.test(rn || '')) throw new Error('enable|pause <customers/…/adGroupAds/<group>~<ad>>');
    return { op: 'mutate', adId: rn.split('~').pop(), resourceName: rn, reason: `manual:${kind}`,
             mutation: { adGroupAdOperation: { update: { resourceName: rn, status: kind === 'enable' ? 'ENABLED' : 'PAUSED' }, updateMask: 'status' } } };
  }
  if (kind === 'raw') { const m = JSON.parse(rest[0]); return { op: 'mutate', reason: 'manual:raw', mutation: m }; }
  throw new Error('usage: list | headlines | enable | pause | raw | run [id]');
}

// Claim the row (pending → 'api') so the hourly script can never pick it up as well,
// send it, and record the outcome exactly the way routes.js records a script-run edit.
async function execute(id) {
  const claim = await pool.query("UPDATE ytads_manual SET status = 'api' WHERE id = $1 AND status = 'pending' RETURNING note, command", [id]);
  if (!claim.rows.length) { console.log(`m${id}: not pending — skipped`); return false; }
  const { note, command: c } = claim.rows[0];
  let result;
  try {
    const r = await ads.mutate([c.mutation], { note, reason: c.reason || 'manual', log: false });
    result = { ok: true, channel: 'api', resourceName: r.results[0] || c.resourceName || null };
  } catch (e) {
    result = { ok: false, channel: 'api', error: e.message, google: e.body || null };
  }
  await pool.query("UPDATE ytads_manual SET status = $2, result = $3, done_at = now() WHERE id = $1", [id, result.ok ? 'done' : 'failed', JSON.stringify(result)]);
  await pool.query('INSERT INTO ytads_events (video_id, campaign_key, ad_id, event, detail) VALUES ($1, $2, $3, $4, $5)',
    [c.videoId || null, c.campaign || null, c.adId || null, result.ok ? 'manual' : 'error',
     JSON.stringify({ runId: null, channel: 'api', op: c.op, reason: c.reason || null, message: result.error || null, manualId: id, note: note || null, mutation: c.mutation || null, google: result.google || null })]);
  console.log(result.ok ? `m${id}: DONE via API → ${result.resourceName || ''}` : `m${id}: FAILED via API — ${result.error}`);
  return result.ok;
}

(async () => {
  await pool.query(`CREATE TABLE IF NOT EXISTS ytads_manual (
    id SERIAL PRIMARY KEY, at TIMESTAMPTZ NOT NULL DEFAULT now(), note TEXT, command JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', run_id INTEGER, result JSONB, done_at TIMESTAMPTZ)`);
  const argv = process.argv.slice(2);
  if (!argv.length || argv[0] === 'list') {
    const r = await pool.query('SELECT id, at, status, note, run_id, command->>\'reason\' AS reason, command->>\'adId\' AS ad_id, result->>\'error\' AS error, result->>\'channel\' AS channel FROM ytads_manual ORDER BY id');
    for (const row of r.rows) console.log(`${row.id}\t${row.at.toISOString().slice(0, 16)}\t${row.status}\t${row.channel === 'api' ? 'api' : 'run=' + (row.run_id || '-')}\t${row.reason}\tad=${row.ad_id || '-'}\t${row.note || ''}${row.error ? '\tERROR: ' + row.error : ''}`);
    if (!r.rows.length) console.log('(queue empty)');
  } else if (argv[0] === 'run') {
    const ids = argv[1] ? [Number(argv[1])] : (await pool.query("SELECT id FROM ytads_manual WHERE status = 'pending' ORDER BY id")).rows.map(r => r.id);
    if (!ids.length) console.log('(nothing pending)');
    for (const id of ids) await execute(id);
  } else {
    const command = build(argv);
    const note = optOf(argv, '--note');
    if (argv.includes('--dry-run')) {
      await ads.mutate([command.mutation], { dryRun: true, note, reason: command.reason });
      console.log(`VALID (Google validated, nothing queued or changed): ${command.reason} ${command.adId || ''}`);
    } else {
      const r = await pool.query('INSERT INTO ytads_manual (note, command) VALUES ($1, $2) RETURNING id', [note, JSON.stringify(command)]);
      const id = r.rows[0].id;
      console.log(`queued m${id}: ${command.reason} ${command.adId || ''} ${JSON.stringify(command.headlines || '')}`);
      if (!argv.includes('--defer')) { if (!(await execute(id))) process.exitCode = 1; }
      else console.log('deferred: the next live hourly Ads Script run executes it');
    }
  }
  await pool.end(); await ads.close();
})().catch(e => { console.error(e.message); process.exit(1); });
