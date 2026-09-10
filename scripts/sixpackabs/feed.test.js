#!/usr/bin/env node
/* eslint-disable no-console */
//
// SIXPACKABS.COM FEEDS — fixture tests (no network).
//
// Drives scripts/sixpackabs/feed.js with a fake fetch and asserts:
//   (a) only PUBLIC videos come out — private, unlisted, an upcoming premiere, a
//       live stream and a rejected upload never do, and the three real unlisted
//       ids (lf46ytHacss, CwEGFxpIM-E, rimBWjT9-oo) never appear in the JSON;
//   (b) 180 s is a Short, 181 s is long-form; newest first; the uploads playlist
//       is paged;
//   (c) a Short's portrait thumbnail is used when YouTube has one and falls back
//       to maxres when it 404s; the maxres ETag rides along as `version`;
//   (d) Instagram keeps IMAGE + CAROUSEL_ALBUM only (reels skipped), 6 max,
//       a carousel contributes its first IMAGE child;
//   (e) the cache: a second read inside the hour makes no upstream call; an
//       upstream failure serves the last good copy with stale:true; a cold
//       failure is a 503, never a 500; the Graph token never reaches a log line.
//
// RUN: node scripts/sixpackabs/feed.test.js
'use strict';

const assert = require('assert');
const {
  createSixpackabsFeeds, parseIsoDuration, isListable, selectInstagramImages, altFromCaption,
} = require('./feed');

const UNLISTED_REAL = ['lf46ytHacss', 'CwEGFxpIM-E', 'rimBWjT9-oo'];

function video(id, { privacy = 'public', duration = 'PT10M', published = '2026-09-01T14:00:00Z', live = 'none', upload = 'processed', title } = {}) {
  return {
    id,
    snippet: {
      title: title || `Title ${id}`,
      description: `First line for ${id}.\n\nSecond paragraph https://absbyai.com/?utm_source=youtube #abs`,
      publishedAt: published,
      liveBroadcastContent: live,
      thumbnails: {
        default: { url: `https://i.ytimg.com/vi/${id}/default.jpg` },
        high: { url: `https://i.ytimg.com/vi/${id}/hqdefault.jpg` },
        maxres: { url: `https://i.ytimg.com/vi/${id}/maxresdefault.jpg` },
      },
    },
    contentDetails: { duration },
    status: { privacyStatus: privacy, uploadStatus: upload, embeddable: true },
  };
}

const VIDEOS = [
  video('pubLong1', { duration: 'PT12M48S', published: '2026-09-06T14:00:00Z' }),
  video('pub180', { duration: 'PT3M', published: '2026-09-05T22:00:00Z' }),
  video('pub181', { duration: 'PT3M1S', published: '2026-09-04T22:00:00Z' }),
  video('pubShortNoOar', { duration: 'PT45S', published: '2026-09-08T22:00:00Z' }),
  video('pubShortOar', { duration: 'PT1M3S', published: '2026-09-09T22:00:00Z' }),
  video('lf46ytHacss', { privacy: 'unlisted', duration: 'PT1M30S' }),
  video('CwEGFxpIM-E', { privacy: 'unlisted', duration: 'PT3M51S' }),
  video('rimBWjT9-oo', { privacy: 'unlisted', duration: 'PT58S' }),
  video('privDraft', { privacy: 'private', duration: 'PT7M' }),
  video('schedPriv', { privacy: 'private', duration: 'PT7M', published: '2026-09-13T14:00:00Z' }),
  video('premiere1', { live: 'upcoming', duration: 'P0D' }),
  video('liveNow', { live: 'live', duration: 'P0D' }),
  video('rejected1', { upload: 'rejected', duration: 'PT2M' }),
];
const PLAYLIST_PAGE1 = { items: VIDEOS.slice(0, 7).map((v) => ({ contentDetails: { videoId: v.id } })), nextPageToken: 'P2' };
const PLAYLIST_PAGE2 = { items: VIDEOS.slice(7).map((v) => ({ contentDetails: { videoId: v.id } })) };
const CHANNEL = { items: [{ snippet: { customUrl: '@absbyai' }, statistics: { subscriberCount: '3030', videoCount: '18', hiddenSubscriberCount: false } }] };

const IG_TOKEN = 'EAAG-secret-graph-token';
const IG = {
  data: [
    { id: '1', media_type: 'VIDEO', media_url: 'https://cdn.example/1.mp4', permalink: 'https://www.instagram.com/reel/1/', timestamp: '2026-09-10T12:00:00+0000', caption: 'A reel' },
    { id: '2', media_type: 'IMAGE', media_url: 'https://cdn.example/2.jpg?sig=x', permalink: 'https://www.instagram.com/p/2/', timestamp: '2026-09-09T12:00:00+0000', caption: 'Train your abs every single day.\n\nMore #abs' },
    { id: '3', media_type: 'CAROUSEL_ALBUM', media_url: 'https://cdn.example/3-cover.mp4', permalink: 'https://www.instagram.com/p/3/', timestamp: '2026-09-08T12:00:00+0000',
      children: { data: [{ media_type: 'VIDEO', media_url: 'https://cdn.example/3a.mp4' }, { media_type: 'IMAGE', media_url: 'https://cdn.example/3b.jpg' }] } },
    { id: '4', media_type: 'IMAGE', media_url: 'https://cdn.example/4.jpg', permalink: 'https://www.instagram.com/p/4/', timestamp: '2026-09-07T12:00:00+0000' },
    { id: '5', media_type: 'VIDEO', media_url: 'https://cdn.example/5.mp4', permalink: 'https://www.instagram.com/reel/5/', timestamp: '2026-09-06T12:00:00+0000' },
    { id: '6', media_type: 'IMAGE', media_url: 'https://cdn.example/6.jpg', permalink: 'https://www.instagram.com/p/6/', timestamp: '2026-09-05T12:00:00+0000' },
    { id: '7', media_type: 'IMAGE', media_url: 'https://cdn.example/7.jpg', permalink: 'https://www.instagram.com/p/7/', timestamp: '2026-09-04T12:00:00+0000' },
    { id: '8', media_type: 'IMAGE', media_url: 'https://cdn.example/8.jpg', permalink: 'https://www.instagram.com/p/8/', timestamp: '2026-09-03T12:00:00+0000' },
    { id: '9', media_type: 'IMAGE', media_url: 'https://cdn.example/9.jpg', permalink: 'https://www.instagram.com/p/9/', timestamp: '2026-09-02T12:00:00+0000' },
  ],
};

function resp(status, body, headers = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => body,
    text: async () => JSON.stringify(body),
    headers: { get: (k) => (k.toLowerCase() in headers ? headers[k.toLowerCase()] : null) },
  };
}

function makeFetch(state = {}) {
  const calls = [];
  const fn = async (url, opts = {}) => {
    calls.push({ url: String(url), method: opts.method || 'GET' });
    const u = new URL(url);
    if (state.down) return resp(500, { error: { message: 'upstream down' } });
    if (u.href === 'https://oauth2.googleapis.com/token') return resp(200, { access_token: 'ya29.test', expires_in: 3600 });
    if (u.pathname === '/youtube/v3/playlistItems') return resp(200, u.searchParams.get('pageToken') === 'P2' ? PLAYLIST_PAGE2 : PLAYLIST_PAGE1);
    if (u.pathname === '/youtube/v3/videos') {
      const ids = u.searchParams.get('id').split(',');
      return resp(200, { items: VIDEOS.filter((v) => ids.includes(v.id)) });
    }
    if (u.pathname === '/youtube/v3/channels') return resp(200, CHANNEL);
    if (u.host === 'i.ytimg.com') {
      if (u.pathname.endsWith('/oardefault.jpg')) return resp(u.pathname.includes('pubShortNoOar') ? 404 : 200, null);
      if (u.pathname.endsWith('/maxresdefault.jpg')) return resp(200, null, { etag: '"1788703208"' });
    }
    if (u.host === 'graph.facebook.com') return resp(200, IG);
    return resp(404, {});
  };
  fn.calls = calls;
  return fn;
}

function fakeRes() {
  return {
    headers: {}, statusCode: 200, body: undefined,
    set(k, v) { this.headers[k] = v; return this; },
    status(c) { this.statusCode = c; return this; },
    json(b) { this.body = b; return this; },
  };
}

const ENV = { GOOGLE_CLIENT_ID: 'cid', GOOGLE_CLIENT_SECRET: 'csec', YOUTUBE_REFRESH_TOKEN: 'rt', META_ADS_TOKEN: IG_TOKEN };

let passed = 0;
async function check(name, fn) {
  await fn();
  passed += 1;
  console.log(`  ok  ${name}`);
}

(async () => {
  console.log('sixpackabs feed tests');

  await check('parseIsoDuration', () => {
    assert.strictEqual(parseIsoDuration('PT12M48S'), 768);
    assert.strictEqual(parseIsoDuration('PT3M'), 180);
    assert.strictEqual(parseIsoDuration('PT3M1S'), 181);
    assert.strictEqual(parseIsoDuration('PT1H2M3S'), 3723);
    assert.strictEqual(parseIsoDuration('P1DT1S'), 86401);
    assert.strictEqual(parseIsoDuration('P0D'), 0);
    assert.strictEqual(parseIsoDuration('garbage'), 0);
    assert.strictEqual(parseIsoDuration(undefined), 0);
  });

  await check('isListable gates on public / not upcoming / not live / not rejected', () => {
    const byId = Object.fromEntries(VIDEOS.map((v) => [v.id, isListable(v)]));
    assert.deepStrictEqual(Object.keys(byId).filter((k) => byId[k]).sort(),
      ['pub180', 'pub181', 'pubLong1', 'pubShortNoOar', 'pubShortOar']);
  });

  const fetch = makeFetch();
  const logs = [];
  const log = { error: (m) => logs.push(m) };
  let clock = Date.parse('2026-09-10T23:00:00Z');
  const feeds = createSixpackabsFeeds({ fetch, env: ENV, now: () => clock, log });

  const res = fakeRes();
  await feeds.channelRoute({}, res);
  const body = res.body;

  await check('channel.json: only public videos, unlisted/private never serialised', () => {
    assert.strictEqual(res.statusCode, 200);
    assert.strictEqual(body.stale, false);
    assert.deepStrictEqual(body.videos.map((v) => v.id), ['pubShortOar', 'pubShortNoOar', 'pubLong1', 'pub180', 'pub181']);
    const json = JSON.stringify(body);
    for (const id of [...UNLISTED_REAL, 'privDraft', 'schedPriv', 'premiere1', 'liveNow', 'rejected1']) {
      assert.ok(!json.includes(id), `${id} leaked into channel.json`);
    }
  });

  await check('channel.json: 180 s = short, 181 s = long; paged playlist read', () => {
    const t = Object.fromEntries(body.videos.map((v) => [v.id, v.type]));
    assert.strictEqual(t.pub180, 'short');
    assert.strictEqual(t.pub181, 'long');
    assert.strictEqual(t.pubLong1, 'long');
    assert.strictEqual(t.pubShortNoOar, 'short');
    assert.strictEqual(fetch.calls.filter((c) => c.url.includes('/playlistItems')).length, 2);
  });

  await check('channel.json: portrait thumbnail verified, falls back to maxres; etag as version', () => {
    const v = Object.fromEntries(body.videos.map((x) => [x.id, x]));
    assert.strictEqual(v.pubShortOar.thumbnails.portrait, 'https://i.ytimg.com/vi/pubShortOar/oardefault.jpg');
    assert.strictEqual(v.pubShortNoOar.thumbnails.portrait, 'https://i.ytimg.com/vi/pubShortNoOar/maxresdefault.jpg');
    assert.strictEqual(v.pubLong1.thumbnails.portrait, v.pubLong1.thumbnails.maxres);
    assert.strictEqual(v.pubLong1.thumbnails.version, '1788703208');
    assert.strictEqual(v.pubLong1.durationSeconds, 768);
    assert.ok(v.pubLong1.description.startsWith('First line for pubLong1.'));
    assert.strictEqual(body.channel.subscriberCount, 3030);
    assert.strictEqual(body.channel.handle, '@absbyai');
    assert.strictEqual(res.headers['Cache-Control'], 'public, max-age=300');
  });

  await check('cache: second read inside the hour makes no upstream call', async () => {
    const before = fetch.calls.length;
    const r2 = fakeRes();
    await feeds.channelRoute({}, r2);
    assert.strictEqual(fetch.calls.length, before);
    assert.strictEqual(r2.body.videos.length, 5);
  });

  await check('cache: upstream failure after a good fetch serves last good copy, stale:true', async () => {
    const downFetch = makeFetch({ down: true });
    const f2 = createSixpackabsFeeds({ fetch: (u, o) => (downFetch.down ? downFetch(u, o) : fetch(u, o)), env: ENV, now: () => clock, log });
    await f2.channel.get();
    downFetch.down = true;
    clock += 61 * 60 * 1000;
    const r = fakeRes();
    await f2.channelRoute({}, r);
    assert.strictEqual(r.statusCode, 200);
    assert.strictEqual(r.body.stale, true);
    assert.strictEqual(r.body.videos.length, 5);
    clock -= 61 * 60 * 1000;
  });

  await check('cache: cold failure is a 503 (never 500), with no-store', async () => {
    const f3 = createSixpackabsFeeds({ fetch: makeFetch({ down: true }), env: ENV, now: () => clock, log });
    const r = fakeRes();
    await f3.channelRoute({}, r);
    assert.strictEqual(r.statusCode, 503);
    assert.deepStrictEqual(r.body, { error: 'feed_unavailable' });
    assert.strictEqual(r.headers['Cache-Control'], 'no-store');
  });

  await check('instagram.json: images + carousels only, 6 max, carousel uses first IMAGE child', async () => {
    const r = fakeRes();
    await feeds.instagramRoute({}, r);
    assert.strictEqual(r.statusCode, 200);
    assert.deepStrictEqual(r.body.images.map((i) => i.id), ['2', '3', '4', '6', '7', '8']);
    assert.strictEqual(r.body.images[1].imageUrl, 'https://cdn.example/3b.jpg');
    assert.strictEqual(r.body.images[0].alt, 'Train your abs every single day.');
    assert.strictEqual(r.body.account.username, 'danrosefit');
    assert.ok(!JSON.stringify(r.body).includes('reel/'), 'a reel leaked into instagram.json');
  });

  await check('instagram: the Graph token never reaches a log line or the response', async () => {
    const f4 = createSixpackabsFeeds({ fetch: makeFetch({ down: true }), env: ENV, now: () => clock, log });
    const r = fakeRes();
    await f4.instagramRoute({}, r);
    assert.strictEqual(r.statusCode, 503);
    assert.ok(logs.length > 0, 'expected a logged failure');
    for (const line of logs) assert.ok(!line.includes(IG_TOKEN), `token leaked into log: ${line}`);
    assert.ok(!JSON.stringify(r.body).includes(IG_TOKEN));
  });

  await check('selectInstagramImages / altFromCaption edge cases', () => {
    assert.deepStrictEqual(selectInstagramImages([]), []);
    assert.deepStrictEqual(selectInstagramImages([{ id: 'x', media_type: 'IMAGE', permalink: 'p' }]), []);
    assert.strictEqual(altFromCaption(''), 'Dan Rose on Instagram');
    assert.strictEqual(altFromCaption('#abs #fitness'), 'Dan Rose on Instagram');
    assert.ok(altFromCaption('x '.repeat(100)).length <= 121);
  });

  console.log(`\n${passed} checks passed`);
})().catch((e) => {
  console.error('\nFAIL:', e && e.stack ? e.stack : e);
  process.exit(1);
});
