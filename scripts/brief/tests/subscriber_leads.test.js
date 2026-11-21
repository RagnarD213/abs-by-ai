'use strict';
const assert = require('node:assert/strict');
const {build, collect, QUERY} = require('../subscriber_leads');
const window = {yesterday: {from: '2026-09-29T05:00:00Z', toExclusive: '2026-09-30T05:00:00Z'},
  sameWeekdayLastWeek: {from: '2026-09-22T05:00:00Z', toExclusive: '2026-09-23T05:00:00Z'}};
const sample = build([{site: 'sixpackabs.com', yesterday: '2', previous: '1'}, {site: 'unattributed', yesterday: '3', previous: '0'}]);
assert.equal(sample.windows.yesterday.sites['sixpackabs.com'].value, 2);
assert.equal(sample.windows.yesterday.sites['absbyai.com'].value, 0);
assert.equal(sample.windows.yesterday.unattributed, 3);
assert.equal(build([]).windows.yesterday.sites['sixpackabs.com'].value, 0);
assert.throws(() => build([{site: 'unattributed', yesterday: null, previous: '0'}]));
assert.throws(() => build([{site: 'other', yesterday: '1', previous: '0'}]));
assert.throws(() => build([{site: 'absbyai.com', yesterday: 'bad', previous: '0'}]));
assert.match(QUERY, /CASE source WHEN 'analysis'/);
assert.match(QUERY, /WHEN 'sixpackabs'/);
assert.match(QUERY, /subscribed_at >= \$1 AND subscribed_at < \$2/);
assert(!/SELECT\s+email/i.test(QUERY));

(async () => {
  const calls = [];
  const client = {connect: async () => calls.push('connect'), end: async () => calls.push('end'),
    query: async (sql, args) => { calls.push(sql); if (sql === QUERY) { assert.equal(args.length, 4); return {rows: []}; } }};
  await collect(client, window);
  assert.equal(calls[1], 'BEGIN READ ONLY');
  assert.equal(calls[calls.length - 2], 'ROLLBACK');
  assert.equal(calls[calls.length - 1], 'end');
  const failed = [];
  const broken = {connect: async () => {}, end: async () => failed.push('end'), query: async sql => {
    failed.push(sql); if (sql === QUERY) throw new Error('Fixture connection error'); }};
  await assert.rejects(() => collect(broken, window));
  assert(failed.includes('ROLLBACK'));
  assert.equal(failed[failed.length - 1], 'end');
  console.log('subscriber_leads: verified-source counts, zero/unknown validation, bound windows and read-only rollback passed');
})().catch(error => {console.error(error); process.exitCode = 1;});
