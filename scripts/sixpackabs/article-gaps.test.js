#!/usr/bin/env node
/* eslint-disable no-console */
//
// SIXPACKABS.COM ARTICLE GAPS — fixture tests (no network).
//
// Asserts: a public video with no article file and no skip is a gap; a video with
// a file or a skip is not; a TBD draft does not count as an article; each gap is
// logged once per process; a broken folder read never throws; the real folder
// reads cleanly.
//
// RUN: node scripts/sixpackabs/article-gaps.test.js
'use strict';

const assert = require('assert');
const path = require('path');
const { createArticleGapLogger, findArticleGaps, readArticleFolder } = require('./article-gaps');

const videos = [
  { id: 'HASFILE0001', title: 'Has a file', type: 'long', publishedAt: '2026-10-01T14:00:00Z' },
  { id: 'SKIPPED0001', title: 'Skipped on purpose', type: 'short', publishedAt: '2026-10-02T14:00:00Z' },
  { id: 'NEWVIDEO001', title: 'Brand new', type: 'short', publishedAt: '2026-10-10T14:00:00Z' },
];

const gaps = findArticleGaps(videos, new Set(['HASFILE0001']), new Set(['SKIPPED0001']));
assert.deepStrictEqual(gaps.map((v) => v.id), ['NEWVIDEO001']);
assert.deepStrictEqual(findArticleGaps(null, new Set(), new Set()), []);

const lines = [];
const log = { warn: (m) => lines.push(m), error: (m) => lines.push(`ERROR ${m}`) };
const logger = createArticleGapLogger({
  dir: '/nowhere',
  log,
  readFolder: () => ({ articleIds: new Set(['HASFILE0001']), skipIds: new Set(['SKIPPED0001']) }),
});
assert.strictEqual(logger.check({ videos }).length, 1);
assert.strictEqual(logger.check({ videos }).length, 1, 'still a gap on the next refresh');
assert.strictEqual(lines.length, 1, 'logged once per process');
assert.ok(/article gap: NEWVIDEO001 "Brand new" \(short\)/.test(lines[0]));
assert.deepStrictEqual(logger.check(undefined), [], 'a failed feed refresh is not a gap');

const broken = createArticleGapLogger({ dir: '/nowhere', log, readFolder: () => { throw new Error('gone'); } });
assert.deepStrictEqual(broken.check({ videos }), []);
assert.ok(lines[1].startsWith('ERROR sixpackabs article gap check failed'));

// The real folder: ids only, TBD drafts excluded, the skip list parses.
const real = readArticleFolder(path.join(__dirname, '..', '..', 'sixpackabs', 'articles'));
assert.ok(real.articleIds.size > 30);
assert.ok(![...real.articleIds].some((id) => id.startsWith('TBD-') || id === 'README'));
assert.ok(real.skipIds.has('D9v9POAKe_Q'));

console.log('article-gaps: all tests passed');
