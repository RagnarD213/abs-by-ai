'use strict';
//
// YTADS FEED — the channel's public uploads, from YouTube's RSS feed.
// No API key, lists Shorts, only PUBLIC videos (so a scheduled Short appears the
// hour it goes live, and a private/unlisted one never does). Verified live
// 2026-09-02 and 2026-09-03 (13 entries, Shorts included).

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

async function fetchVideos({ fetchImpl = fetch, timeoutMs = 10000 } = {}) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetchImpl(FEED_URL, { signal: ctrl.signal, headers: { 'User-Agent': 'absbyai-ytads/1.0' } });
    if (!res.ok) throw new Error(`feed HTTP ${res.status}`);
    return parseFeed(await res.text());
  } finally { clearTimeout(timer); }
}

module.exports = { parseFeed, fetchVideos, FEED_URL, CHANNEL_ID };
