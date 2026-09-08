#!/usr/bin/env node
// Queue a one-off Google Ads edit that Dan asked for, to be executed by the next LIVE
// hourly run of the Ads Script (which passes `mutation` straight to AdsApp.mutate).
// The system itself never edits an existing ad; this is the channel for Dan's edits.
//
//   node scripts/ads/ytads/manual.js list
//   node scripts/ads/ytads/manual.js headlines <adId> "<h1>" "<h2>" ... --note "why"
//   node scripts/ads/ytads/manual.js enable <adGroupAdResourceName> --note "why"
//   node scripts/ads/ytads/manual.js raw '<json mutation>' --note "why"
//
// Uses DATABASE_PUBLIC_URL (off-platform) or DATABASE_URL (on Railway). Customer id
// is the Abs by AI account, 342-717-0837.
const { Pool } = require('pg');
const CID = '3427170837';
const url = process.env.DATABASE_PUBLIC_URL || process.env.DATABASE_URL;
if (!url) { console.error('need DATABASE_PUBLIC_URL or DATABASE_URL'); process.exit(2); }
const pool = new Pool({ connectionString: url, ssl: /railway\.internal/.test(url) ? false : { rejectUnauthorized: false } });

function noteOf(argv) { const i = argv.indexOf('--note'); return i >= 0 ? argv[i + 1] : null; }
function stripNote(argv) { const i = argv.indexOf('--note'); return i >= 0 ? [...argv.slice(0, i), ...argv.slice(i + 2)] : argv; }

function build(argv) {
  const [kind, ...rest] = stripNote(argv);
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
  throw new Error('usage: list | headlines | enable | pause | raw');
}

(async () => {
  await pool.query(`CREATE TABLE IF NOT EXISTS ytads_manual (
    id SERIAL PRIMARY KEY, at TIMESTAMPTZ NOT NULL DEFAULT now(), note TEXT, command JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending', run_id INTEGER, result JSONB, done_at TIMESTAMPTZ)`);
  const argv = process.argv.slice(2);
  if (!argv.length || argv[0] === 'list') {
    const r = await pool.query('SELECT id, at, status, note, run_id, command->>\'reason\' AS reason, command->>\'adId\' AS ad_id, result->>\'error\' AS error FROM ytads_manual ORDER BY id');
    for (const row of r.rows) console.log(`${row.id}\t${row.at.toISOString().slice(0, 16)}\t${row.status}\trun=${row.run_id || '-'}\t${row.reason}\tad=${row.ad_id || '-'}\t${row.note || ''}${row.error ? '\tERROR: ' + row.error : ''}`);
    if (!r.rows.length) console.log('(queue empty)');
  } else {
    const command = build(argv);
    const r = await pool.query('INSERT INTO ytads_manual (note, command) VALUES ($1, $2) RETURNING id', [noteOf(argv), JSON.stringify(command)]);
    console.log(`queued m${r.rows[0].id}: ${command.reason} ${command.adId || ''} ${JSON.stringify(command.headlines || '')}`);
  }
  await pool.end();
})().catch(e => { console.error(e.message); process.exit(1); });
