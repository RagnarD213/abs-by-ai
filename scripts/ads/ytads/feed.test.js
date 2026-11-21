'use strict';
// node scripts/ads/ytads/feed.test.js — the RSS feed, and the API backup when RSS is down (Dan 2026-11-03).
const assert = require('assert');
const { fetchVideos, parseBackup } = require('./feed.js');

const rss = '<feed><entry><yt:videoId>AAA</yt:videoId><title>Long</title><link rel="alternate" href="https://www.youtube.com/watch?v=AAA"/><published>2026-11-03T15:00:00+00:00</published></entry></feed>';
const backup = { videos: [
  { id: 'OLD', title: 'Old long', publishedAt: '2026-11-01T15:00:00Z', type: 'long' },
  { id: 'SHT', title: 'New short', publishedAt: '2026-11-03T23:00:30Z', type: 'short' },
  { id: 'BAD', title: 'no date' },
] };
const res = (status, body) => ({ ok: status === 200, status, text: async () => body, json: async () => body });
const quiet = { log() {} };

(async () => {
  // RSS works: RSS is used, the backup is never asked.
  let asked = [];
  let v = await fetchVideos({ log: quiet, fetchImpl: async (u) => { asked.push(u); return res(200, rss); } });
  assert.deepStrictEqual(v.map(x => x.id), ['AAA']);
  assert.strictEqual(asked.length, 1);

  // RSS 404: the backup is used, same shape, newest first, Shorts flagged, undated rows dropped.
  v = await fetchVideos({ log: quiet, backupUrl: 'B', fetchImpl: async (u) => u === 'B' ? res(200, backup) : res(404, '') });
  assert.deepStrictEqual(v.map(x => x.id), ['SHT', 'OLD']);
  assert.strictEqual(v[0].isShort, true);
  assert.strictEqual(v[0].published, '2026-11-03T23:00:30Z');
  assert.strictEqual(v[1].isShort, false);

  // Both down: one error naming both.
  await assert.rejects(fetchVideos({ log: quiet, backupUrl: 'B', fetchImpl: async () => res(500, '') }), /feed HTTP 500; backup HTTP 500/);
  // Backup answers but empty: still an error (never "no videos" by accident).
  await assert.rejects(fetchVideos({ log: quiet, backupUrl: 'B', fetchImpl: async (u) => u === 'B' ? res(200, { videos: [] }) : res(404, '') }), /backup no videos/);

  assert.deepStrictEqual(parseBackup(null), []);
  console.log('feed.test.js: ok');
})().catch(e => { console.error(e); process.exit(1); });
