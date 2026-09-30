'use strict';
// Only shared-client search is used. No campaign mutation, ledger, or generation.
const fs = require('fs');
const OUTCOMES = ['free_generations', 'email_leads', 'trials', 'paid'];

function validMap(mapping = {}) {
  const used = new Set();
  for (const [name, ids] of Object.entries(mapping)) {
    if (!OUTCOMES.includes(name) || !Array.isArray(ids) || !ids.length) throw new Error('Invalid mapping');
    for (const id of ids) {
      if (!/^\d+$/.test(String(id)) || used.has(String(id))) throw new Error('Invalid or overlapping action IDs');
      used.add(String(id));
    }
  }
  return mapping;
}

function buildStats(spendRows, actionRows, mapping, day, weekFrom) {
  validMap(mapping);
  const campaigns = new Map();
  function get(row) {
    const id = String(row.campaign.id);
    if (!campaigns.has(id)) campaigns.set(id, {
      id, name: row.campaign.name, status: row.campaign.status,
      yesterday: {spend: 0, clicks: 0, impressions: 0},
      last7d: {spend: 0, clicks: 0, impressions: 0}, observedActions: [],
    });
    return campaigns.get(id);
  }
  const actionCounts = new Map();
  for (const row of spendRows) {
    if (!row.campaign?.id || !row.segments?.date || !row.metrics) throw new Error('Invalid campaign row');
    const c = get(row), date = row.segments.date;
    const values = {spend: Number(row.metrics.costMicros || 0) / 1e6,
      clicks: Number(row.metrics.clicks || 0), impressions: Number(row.metrics.impressions || 0)};
    if (Object.values(values).some(v => !Number.isFinite(v) || v < 0)) throw new Error('Invalid campaign metrics');
    for (const period of (date === day ? ['yesterday', 'last7d'] : ['last7d'])) {
      if (date < weekFrom || date > day) continue;
      for (const key of Object.keys(values)) c[period][key] += values[key];
    }
  }
  for (const row of actionRows) {
    if (!row.campaign?.id || !row.segments?.conversionAction || !row.segments?.date) throw new Error('Invalid action row');
    const c = get(row), id = String(row.segments.conversionAction).split('/').pop();
    const count = Number(row.metrics?.allConversions);
    if (!Number.isFinite(count) || count < 0) throw new Error('Invalid conversion count');
    const key = `${c.id}:${id}`;
    if (!actionCounts.has(key)) actionCounts.set(key, {id, name: row.segments.conversionActionName || null, yesterday: 0, last7d: 0});
    const action = actionCounts.get(key), date = row.segments.date;
    if (date >= weekFrom && date <= day) action.last7d += count;
    if (date === day) action.yesterday += count;
  }
  for (const c of campaigns.values()) {
    c.observedActions = [...actionCounts].filter(([key]) => key.startsWith(c.id + ':')).map(([, action]) => action);
    for (const period of ['yesterday', 'last7d']) {
      c[period].spend = Math.round(c[period].spend * 100) / 100;
      for (const outcome of OUTCOMES) {
        const ids = mapping[outcome];
        c[period][outcome] = ids ? {
          status: 'mapped', actionIds: ids.map(String),
          value: c.observedActions.filter(a => ids.map(String).includes(a.id)).reduce((sum, a) => sum + a[period], 0),
        } : {status: 'unmapped', value: null};
      }
    }
  }
  return [...campaigns.values()];
}

async function collect(config, day, weekFrom, search) {
  validMap(config.conversion_actions);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(day) || !/^\d{4}-\d{2}-\d{2}$/.test(weekFrom)) throw new Error('Invalid dates');
  const cid = String(config.customer_id || '3427170837').replace(/-/g, '');
  if (!/^\d{10}$/.test(cid)) throw new Error('Invalid customer ID');
  const options = {cid};
  const account = await search('SELECT customer.id, customer.time_zone, customer.currency_code FROM customer LIMIT 1', options);
  if (account[0]?.customer?.timeZone !== 'America/Chicago') throw new Error('Account timezone not verified as America/Chicago');
  const currency = account[0]?.customer?.currencyCode;
  if (!/^[A-Z]{3}$/.test(currency || '')) throw new Error('Account currency unavailable');
  const actions = await search("SELECT conversion_action.id, conversion_action.name, conversion_action.status FROM conversion_action WHERE conversion_action.status != 'REMOVED'", options);
  const known = new Set(actions.map(r => String(r.conversionAction.id)));
  for (const ids of Object.values(config.conversion_actions || {})) {
    if (ids.some(id => !known.has(String(id)))) throw new Error('Mapped action unavailable');
  }
  const dateFilter = `segments.date BETWEEN '${weekFrom}' AND '${day}'`;
  const spend = await search(`SELECT campaign.id, campaign.name, campaign.status, segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions FROM campaign WHERE ${dateFilter}`, options);
  const counts = await search(`SELECT campaign.id, campaign.name, campaign.status, segments.date, segments.conversion_action, segments.conversion_action_name, metrics.all_conversions FROM campaign WHERE ${dateFilter}`, options);
  return {status: Object.keys(config.conversion_actions || {}).length === OUTCOMES.length ? 'ok' : 'partial',
    customerId: cid, timezone: 'America/Chicago', currency, day, weekFrom,
    definition: 'Google-attributed conversion-action counts; may be fractional. Not backend customer totals.',
    unmapped: OUTCOMES.filter(name => !config.conversion_actions?.[name]),
    availableActions: actions.map(r => ({id: String(r.conversionAction.id), name: r.conversionAction.name})),
    campaigns: buildStats(spend, counts, config.conversion_actions || {}, day, weekFrom)};
}

module.exports = {buildStats, collect, validMap};
if (require.main === module) {
  const [day, weekFrom] = process.argv.slice(2);
  const config = JSON.parse(fs.readFileSync(0, 'utf8'));
  // The required module's CLI is guarded; importing it does not run mutate.
  collect(config, day, weekFrom, require('../ads/api/client.js').search)
    .then(result => process.stdout.write(JSON.stringify(result)))
    .catch(() => { process.stdout.write(JSON.stringify({status: 'error', reason: 'Google Ads read failed; credentials, action mapping, timezone, or query requires verification'})); process.exitCode = 1; });
}
