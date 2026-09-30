'use strict';
const assert = require('node:assert/strict');
const {buildStats, collect, validMap} = require('../ads_stats');
const row = (date, cost) => ({campaign: {id: '7', name: 'Fixture', status: 'ENABLED'}, segments: {date}, metrics: {costMicros: cost, clicks: 3, impressions: 20}});
const action = (id, count, date = '2026-09-29') => ({campaign: {id: '7', name: 'Fixture'}, segments: {date, conversionAction: 'customers/123/conversionActions/' + id, conversionActionName: 'Fixture ' + id}, metrics: {allConversions: count}});
const rows = buildStats([row('2026-09-29', '10000000'), row('2026-09-28', '5000000')], [action('11', 2), action('22', 0.5)], {trials: ['11']}, '2026-09-29', '2026-09-23');
assert.equal(rows[0].yesterday.spend, 10);
assert.equal(rows[0].last7d.spend, 15);
assert.equal(rows[0].yesterday.trials.value, 2);
assert.equal(rows[0].yesterday.paid.value, null);
assert.equal(rows[0].yesterday.free_generations.status, 'unmapped');
assert.equal(rows[0].observedActions[1].yesterday, 0.5);
assert.throws(() => validMap({trials: ['11'], paid: ['11']}));
assert.throws(() => validMap({paid: []}));
assert.throws(() => validMap({unknown: ['11']}));
assert.throws(() => buildStats([row('2026-09-29', 'not-a-number')], [], {}, '2026-09-29', '2026-09-23'));
const zero = buildStats([row('2026-09-29', '0')], [], {paid: ['22']}, '2026-09-29', '2026-09-23');
assert.equal(zero[0].yesterday.paid.value, 0);

(async () => {
  const queries = [];
  const search = async q => {
    queries.push(q);
    if (q.includes('FROM customer')) return [{customer: {timeZone: 'America/Chicago', currencyCode: 'USD'}}];
    if (q.includes('FROM conversion_action')) return [{conversionAction: {id: '11', name: 'Trial'}}];
    if (q.includes('segments.conversion_action')) return [action('11', 2)];
    return [row('2026-09-29', '1000000')];
  };
  const result = await collect({conversion_actions: {trials: ['11']}}, '2026-09-29', '2026-09-23', search);
  assert.equal(result.status, 'partial');
  assert.equal(result.currency, 'USD');
  assert.equal(queries.length, 4);
  assert(queries.every(q => /^SELECT /.test(q)));
  await assert.rejects(() => collect({conversion_actions: {paid: ['404']}}, '2026-09-29', '2026-09-23', search));
  await assert.rejects(() => collect({}, '2026-09-29', '2026-09-23', async () => [{customer: {timeZone: 'UTC'}}]));
  await assert.rejects(() => collect({}, '2026-09-29', '2026-09-23', async () => [{customer: {timeZone: 'America/Chicago'}}]));
  console.log('ads_stats: aggregation, unknown/zero outcomes, mapping validation, read-only queries and timezone checks passed');
})().catch(error => {console.error(error); process.exitCode = 1;});
