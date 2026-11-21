'use strict';
//
// YTADS FEED — the channel's public uploads, from YouTube's RSS feed.
// No API key, lists Shorts, only PUBLIC videos (so a scheduled Short appears the
// hour it goes live, and a private/unlisted one never does). Verified live
// 2026-09-02 and 2026-09-03 (13 entries, Shorts included).
//
// BACKUP (Dan 2026-11-03): YouTube's RSS feed went down (HTTP 404/500 for hours on 2026-11-03),
// so no new video got engagement ads; the Short "How Fast To Roll Out With The Ab Wheel" went
// public with none. When the RSS feed fails, fetchVideos() reads the server's own public-video
// list instead (/api/sixpackabs/channel.json: YouTube Data API through the channel's OAuth
// token, PUBLIC videos only, cached and refreshed every 5 minutes, so it costs no extra quota).
// Same row shape; Short = 180 s or less there.

const CHANNEL_ID = 'UC236gjadarHAhEhOMYNGJ9g';
const FEED_URL = `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`;

const decode = (s) => String(s || '')
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&apos;/g, "'").replace(/&amp;/g, '&');

// Pure: XML string → [{ id, title, description, published, url, isShort }]
function parseFeed(xml) {
  const out = [];
  const entries = String(xml || '').split('<entry>').slice(1);
  for (const raw of entries) {
    const pick = (tag) => { const m = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`).exec(raw); return m ? decode(m[1].trim()) : ''; };
    const id = pick('yt:videoId');
    if (!id) continue;
    const link = /<link rel="alternate" href="([^"]+)"/.exec(raw);
    out.push({
      id, title: pick('title'), description: pick('media:description'),
      published: pick('published'), url: link ? decode(link[1]) : `https://www.youtube.com/watch?v=${id}`,
      isShort: !!(link && /\/shorts\//.test(link[1])),
    });
  }
  return out;
}

// In the web server, ask itself (no public round trip); from a laptop CLI, ask the live site.
const BACKUP_URL = process.env.PORT
  ? `http://127.0.0.1:${process.env.PORT}/api/sixpackabs/channel.json`
  : 'https://absbyai.com/api/sixpackabs/channel.json';

// Pure: channel.json → the same rows parseFeed gives, newest first.
function parseBackup(json) {
  return ((json && json.videos) || []).filter(v => v && v.id && v.publishedAt).map(v => ({
    id: v.id, title: v.title || '', description: v.description || '', published: v.publishedAt,
    url: v.type === 'short' ? `https://www.youtube.com/shorts/${v.id}` : `https://www.youtube.com/watch?v=${v.id}`,
    isShort: v.type === 'short',
  })).sort((a, b) => Date.parse(b.published) - Date.parse(a.published));
}

async function get(fetchImpl, url, timeoutMs, headers) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetchImpl(url, { signal: ctrl.signal, headers });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res;
  } finally { clearTimeout(timer); }
}

let lastSource = null;   // log only when the source changes, not every minute
async function fetchVideos({ fetchImpl = fetch, timeoutMs = 10000, backupUrl = BACKUP_URL, log = console } = {}) {
  let rssError;
  try {
    const videos = parseFeed(await (await get(fetchImpl, FEED_URL, timeoutMs, { 'User-Agent': 'absbyai-ytads/1.0' })).text());
    if (lastSource === 'backup') log.log('YTADS feed: RSS feed is back');
    lastSource = 'rss';
    return videos;
  } catch (e) { rssError = e; }
  try {
    const videos = parseBackup(await (await get(fetchImpl, backupUrl, timeoutMs * 3)).json());
    if (!videos.length) throw new Error('no videos');
    if (lastSource !== 'backup') log.log(`YTADS feed: RSS failed (${rssError.message}), using the YouTube API backup`);
    lastSource = 'backup';
    return videos;
  } catch (e) {
    throw new Error(`feed ${rssError.message}; backup ${e.message}`);
  }
}

module.exports = { parseFeed, parseBackup, fetchVideos, FEED_URL, BACKUP_URL, CHANNEL_ID };
