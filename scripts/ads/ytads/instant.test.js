'use strict';
// node scripts/ads/ytads/instant.test.js — every new video must reach all four targets (Dan 2026-10-18).
const assert = require('assert');
const { missing, keyFor, createOp, TARGETS } = require('./instant.js');

assert.deepStrictEqual(Object.keys(TARGETS), ['tier2', 'tier1', 'rmktg-site', 'rmktg-yt']);
assert.strictEqual(keyFor('24316408288', '200887799219'), 'rmktg-site');
assert.strictEqual(keyFor('24316408288', '209156230708'), 'rmktg-yt');
assert.strictEqual(keyFor('24163535721', '206274722584'), 'tier1');
assert.strictEqual(keyFor('24169507109', '203082125721'), null, 'old paused remarketing campaign is not a target');

const now = new Date('2026-10-25T15:00:00Z');
const v = { id: 'tnzIUH6RW7g', title: "I'm 41. I'm Top 1%.", published: '2026-10-25T14:00:45Z' };
const got = missing({ videos: [v], existing: new Set(['tier2:tnzIUH6RW7g', 'tier1:tnzIUH6RW7g']), now, startDate: '2026-09-03', skiplist: [] });
assert.deepStrictEqual(got[0].keys, ['rmktg-site', 'rmktg-yt']);

const op = createOp({ cid: '1', adGroupId: '2', name: 'n', set: { headlines: ['h'], longHeadlines: ['l'], descriptions: ['d'] },
  template: { businessName: 'b', finalUrls: ['u'], logoImages: ['a'], callToActions: [] }, videoAsset: 'x', isShort: false, status: 'PAUSED' });
assert.strictEqual(op.adGroupAdOperation.create.status, 'PAUSED');
console.log('instant.test.js: ok');
