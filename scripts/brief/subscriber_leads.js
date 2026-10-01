'use strict';
// Aggregate-only intake. Do not import db.js or server.js: they initialize/write.
const fs = require('fs');
const path = require('path');
const {createRequire} = require('module');
const SITES = ['absbyai.com', 'sixpackabs.com'];
const QUERY = `SELECT
  CASE source WHEN 'analysis' THEN 'absbyai.com'
              WHEN 'sixpackabs' THEN 'sixpackabs.com' ELSE 'unattributed' END AS site,
  count(*) FILTER (WHERE subscribed_at >= $1 AND subscribed_at < $2) AS yesterday,
  count(*) FILTER (WHERE subscribed_at >= $3 AND subscribed_at < $4) AS previous
FROM subscribers
WHERE ((subscribed_at >= $1 AND subscribed_at < $2)
    OR (subscribed_at >= $3 AND subscribed_at < $4))
  AND lower(email) NOT LIKE '%@example.com'
  AND NOT coalesce(excluded, false)
  AND NOT coalesce(deleted_account, false)
GROUP BY 1`;

function build(rows) {
  const windows = {};
  for (const [window, field] of [['yesterday', 'yesterday'], ['sameWeekdayLastWeek', 'previous']]) {
    const counts = Object.fromEntries([...SITES, 'unattributed'].map(site => [site, 0]));
    for (const row of rows) {
      const count = Number(row[field]);
      if (!(row.site in counts) || !Number.isSafeInteger(count) || count < 0 || row[field] == null) throw new Error('Invalid aggregate');
      counts[row.site] += count;
    }
    windows[window] = {sites: Object.fromEntries(SITES.map(site => [site, {
      status: 'verified_database', value: counts[site],
      definition: 'First persisted newsletter address captures with an explicit site-source tag. Not form attempts or all account/checkout emails.',
    }])), unattributed: counts.unattributed};
  }
  return {status: 'ok', metric: 'first_captured_newsletter_addresses', windows,
    evidence: ['db.js:202', 'server.js:4549', 'public/index.html:5567', 'sixpackabs/theme/sixpackabs-child/assets/js/site.js:197'],
    limitations: ['Unknown sources stay unattributed', 'Deleted, excluded and example.com rows are omitted', 'Historical deletions and asynchronous persistence can reduce counts']};
}

async function collect(client, window) {
  let began = false;
  try {
    await client.connect();
    await client.query('BEGIN READ ONLY');
    began = true;
    await client.query("SET LOCAL statement_timeout = '10s'");
    const params = [window.yesterday.from, window.yesterday.toExclusive,
      window.sameWeekdayLastWeek.from, window.sameWeekdayLastWeek.toExclusive];
    if (params.some(value => !Number.isFinite(Date.parse(value)))) throw new Error('Invalid dates');
    const result = await client.query(QUERY, params);
    if (!Array.isArray(result.rows)) throw new Error('Invalid result');
    return build(result.rows);
  } finally {
    try { if (began) await client.query('ROLLBACK'); }
    finally { await client.end(); }
  }
}

module.exports = {build, collect, QUERY};
if (require.main === module) {
  (async () => {
    const connectionString = process.env.DATABASE_PUBLIC_URL || process.env.DATABASE_URL;
    if (!connectionString) return {status: 'missing', reason: 'Existing database read credential unavailable'};
    const projectRoot = process.argv[2];
    const {Client} = createRequire(path.join(projectRoot, 'package.json'))('pg');
    const window = JSON.parse(fs.readFileSync(0, 'utf8'));
    const client = new Client({connectionString, connectionTimeoutMillis: 10000,
      // Matches the existing backend's Railway connection configuration.
      ssl: /localhost|127\.0\.0\.1|railway\.internal/.test(connectionString) ? false : {rejectUnauthorized: false}});
    return collect(client, window);
  })().then(result => process.stdout.write(JSON.stringify(result))).catch(() => {
    process.stdout.write(JSON.stringify({status: 'error', reason: 'Read-only subscriber aggregate unavailable; no zero inferred'}));
    process.exitCode = 1;
  });
}
