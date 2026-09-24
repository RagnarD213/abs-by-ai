#!/usr/bin/env node
/* eslint-disable no-console */
//
// BRAND GUARD — keeps the Brand - Search - US campaign on brand searches only.
//
// Google's exact and phrase match serve "close variants", and on 2026-09-24 that meant the
// brand campaign had spent $142.94 in 30 days with not one search containing "abs by ai"
// ("ai six pack", "abs editor", "ai ab generator"). Negative keywords catch the patterns seen
// so far; this job catches the next one. Each run it reads the campaign's recent search terms
// and adds an EXACT negative, on that ad group, for every term that fails its group's rule:
//   Brand - Abs By AI : the term must contain "abs by ai" (spaces/punctuation ignored).
//   Brand - Dan Rose  : the term must contain Dan's name AND something unmistakably his
//                       (Abs By AI, SixPackAbs, Six Pack Shortcuts, abs, fitness, danrosefit,
//                       Social Response Marketing, his YouTube-marketing book). The bare name is
//                       never enough: there is a chef, a developer and a Facebook VP of that name.
// An exact negative only blocks that literal search, so a wrong call costs one search and is
// undone by deleting the negative. Terms already excluded are skipped.
//
// RUN:  node scripts/ads/brand-guard.js [--dry-run] [--days N]
//   Railway cron service `brand-guard` (daily). Exits 0 with a one-line summary.
//
'use strict';

const CAMPAIGN = '24086091285';
const RULES = {
  'Brand - Abs By AI': (n) => /absbyai|abbyai/.test(n),
  'Brand - Dan Rose': (n) => /dan(iel)?rose/.test(n)
    && /absbyai|sixpack|6pack|abs|fitness|fit|socialresponse|youtube|15steps/.test(n.replace(/dan(iel)?rose/g, '|')),
};
const norm = (t) => String(t).toLowerCase().replace(/[^a-z0-9]/g, '');

// true = the term belongs in that ad group; unknown ad groups are left alone.
function allowed(adGroupName, term) {
  const rule = RULES[adGroupName];
  return rule ? rule(norm(term)) : true;
}

async function main() {
  const ads = require('./api/client.js');
  const dryRun = process.argv.includes('--dry-run');
  const di = process.argv.indexOf('--days');
  const days = di > 0 ? Number(process.argv[di + 1]) : 14;
  const since = new Date(Date.now() - days * 864e5).toISOString().slice(0, 10);
  const today = new Date().toISOString().slice(0, 10);
  const rows = await ads.search(`SELECT ad_group.resource_name, ad_group.name, search_term_view.search_term, search_term_view.status, metrics.impressions
    FROM search_term_view WHERE campaign.id = ${CAMPAIGN} AND segments.date BETWEEN '${since}' AND '${today}'`);
  const seen = new Set();
  const ops = [];
  const blocked = [];
  for (const r of rows) {
    const term = r.searchTermView.searchTerm;
    const key = `${r.adGroup.resourceName}|${term}`;
    if (seen.has(key)) continue;
    seen.add(key);
    if (/EXCLUDED/.test(r.searchTermView.status || '')) continue;
    if (allowed(r.adGroup.name, term)) continue;
    blocked.push(`${r.adGroup.name}: "${term}"`);
    ops.push({ adGroupCriterionOperation: { create: { adGroup: r.adGroup.resourceName, negative: true, keyword: { text: term, matchType: 'EXACT' } } } });
  }
  if (ops.length) {
    const res = await ads.mutate(ops, { dryRun, partialFailure: true, note: `brand-guard: ${ops.length} off-brand search terms`, reason: 'brand-guard' });
    if (!res.ok) throw new Error(JSON.stringify(res).slice(0, 500));
  }
  console.log(`brand-guard${dryRun ? ' (dry run)' : ''}: ${seen.size} terms checked over ${days} days, ${blocked.length} negated`);
  for (const b of blocked) console.log('  - ' + b);
}

module.exports = { allowed, norm };
if (require.main === module) main().catch((e) => { console.error('brand-guard failed:', e.message || e); process.exit(1); });
