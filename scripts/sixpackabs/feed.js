'use strict';
/**
 * SixPackAbs.com feeds — what the sixpackabs.com homepage shows.
 *
 * sixpackabs.com (WordPress.com, theme `sixpackabs-child`) never talks to Google
 * or Meta. Its hourly WP-Cron job pulls these two documents from absbyai.com,
 * where the tokens already live:
 *
 *   GET /api/sixpackabs/channel.json    PUBLIC videos on the Abs by AI channel
 *   GET /api/sixpackabs/instagram.json  the 6 latest @danrosefit photo posts
 *
 * THE RULE THAT MATTERS: the YouTube OAuth token sees every upload — unlisted
 * ads, the website video, private drafts and scheduled posts are all in the
 * uploads playlist. Only `status.privacyStatus === 'public'` may leave this
 * module (and not an upcoming premiere, not a live stream, not a failed or
 * rejected upload). Putting an unlisted ad on the homepage would be the worst
 * outcome of the whole build; feed.test.js asserts the filter.
 *
 * Both documents are served from an in-memory cache refreshed hourly. An
 * upstream failure serves the last good copy with `stale: true` — never an error
 * while a cache exists.
 *
 * YOUTUBE PAGING DRIFTS: the uploads playlist pages by offset and reorders while
 * scheduled videos go live. On 2026-09-11 a 55-item listing returned one video
 * twice and silently skipped a public one ("Welcome to Abs by AI!"), which the
 * WordPress sync then drafted. So the playlist is listed at two page sizes (the
 * page boundaries differ), the ids are unioned and de-duplicated, and every video
 * that was public on the previous refresh is re-checked by id.
 *
 * Tests: node scripts/sixpackabs/feed.test.js
 */

const CHANNEL_ID = 'UC236gjadarHAhEhOMYNGJ9g';
const UPLOADS_PLAYLIST_ID = 'UU236gjadarHAhEhOMYNGJ9g';
const CHANNEL_URL = 'https://www.youtube.com/@absbyai';
const IG_USER_ID = '17841401601139982';
const IG_USERNAME = 'danrosefit';

const SHORT_MAX_SECONDS = 180;         // Short = public video of 180 s or less
const IG_IMAGE_COUNT = 6;
const REFRESH_MS = 60 * 60 * 1000;     // hourly
const RETRY_AFTER_FAILURE_MS = 5 * 60 * 1000;
const UPSTREAM_TIMEOUT_MS = 20 * 1000;

const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const YT_API = 'https://www.googleapis.com/youtube/v3';
const GRAPH_API = 'https://graph.facebook.com/v21.0';

// ISO 8601 duration ("PT12M48S", "P1DT2H") → whole seconds. Unparseable → 0.
function parseIsoDuration(iso) {
  const m = /^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$/.exec(String(iso || ''));
  if (!m) return 0;
  return (+m[1] || 0) * 86400 + (+m[2] || 0) * 3600 + (+m[3] || 0) * 60 + Math.round(+m[4] || 0);
}

// The public-only gate. Everything the homepage shows passes through here.
function isListable(v) {
  const status = (v && v.status) || {};
  const snippet = (v && v.snippet) || {};
  return status.privacyStatus === 'public'
    && snippet.liveBroadcastContent !== 'upcoming'
    && snippet.liveBroadcastContent !== 'live'
    && !['deleted', 'failed', 'rejected'].includes(status.uploadStatus)
    && parseIsoDuration(v.contentDetails && v.contentDetails.duration) > 0;
}

function videoType(seconds) {
  return seconds <= SHORT_MAX_SECONDS ? 'short' : 'long';
}

function firstThumb(thumbs, order) {
  for (const k of order) if (thumbs && thumbs[k] && thumbs[k].url) return thumbs[k].url;
  return null;
}

// One YouTube `videos` resource → the shape WordPress imports. `extra.portrait`
// is the verified vertical thumbnail (Shorts only), `extra.version` the maxres
// thumbnail's ETag so WordPress can tell when Dan swaps a thumbnail.
function toFeedVideo(v, extra = {}) {
  const s = v.snippet || {};
  const t = s.thumbnails || {};
  const durationSeconds = parseIsoDuration(v.contentDetails && v.contentDetails.duration);
  const maxres = firstThumb(t, ['maxres', 'standard', 'high', 'medium', 'default'])
    || `https://i.ytimg.com/vi/${v.id}/hqdefault.jpg`;
  return {
    id: v.id,
    title: s.title || '',
    description: s.description || '',
    publishedAt: s.publishedAt || null,
    durationSeconds,
    type: videoType(durationSeconds),
    embeddable: !v.status || v.status.embeddable !== false,
    thumbnails: {
      maxres,
      high: firstThumb(t, ['high', 'standard', 'medium', 'default']) || maxres,
      // maxresdefault is 16:9 with the vertical frame centred, so object-fit:cover
      // in a 9:16 box crops to exactly the video when no portrait exists.
      portrait: extra.portrait || maxres,
      version: extra.version || null,
    },
  };
}

// First line of an Instagram caption, hashtags dropped — alt text only; the grid
// itself shows no captions.
function altFromCaption(caption) {
  const line = String(caption || '').split('\n').map((l) => l.trim()).find(Boolean) || '';
  const clean = line.replace(/#[\w-]+/g, '').replace(/\s+/g, ' ').trim();
  if (!clean) return 'Dan Rose on Instagram';
  return clean.length > 120 ? `${clean.slice(0, 117).replace(/\s+\S*$/, '')}…` : clean;
}

// Graph `media` items → the newest photo posts. Reels (VIDEO) are skipped; a
// carousel contributes its first IMAGE child. `imageUrl` is a signed CDN URL
// that expires — WordPress must download it at sync time, never hotlink it.
function selectInstagramImages(items, limit = IG_IMAGE_COUNT) {
  const sorted = [...(items || [])].sort((a, b) => String(b.timestamp || '').localeCompare(String(a.timestamp || '')));
  const out = [];
  for (const m of sorted) {
    if (out.length >= limit) break;
    let imageUrl = null;
    if (m.media_type === 'IMAGE') {
      imageUrl = m.media_url;
    } else if (m.media_type === 'CAROUSEL_ALBUM') {
      const kids = (m.children && m.children.data) || [];
      const firstImage = kids.find((k) => k.media_type === 'IMAGE' && k.media_url);
      if (firstImage) imageUrl = firstImage.media_url;
      else if (m.media_url && !/\.mp4(\?|$)/i.test(m.media_url)) imageUrl = m.media_url;
    } else {
      continue;
    }
    if (!imageUrl || !m.permalink) continue;
    out.push({ id: String(m.id), permalink: m.permalink, imageUrl, timestamp: m.timestamp || null, alt: altFromCaption(m.caption) });
  }
  return out;
}

// Query strings carry the Graph access token — never let one reach a log line.
function redact(url) {
  return String(url).split('?')[0];
}

function createSixpackabsFeeds({ fetch, env = process.env, now = Date.now, log = console } = {}) {
  if (typeof fetch !== 'function') throw new Error('createSixpackabsFeeds needs a fetch implementation');

  async function request(url, opts = {}) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), UPSTREAM_TIMEOUT_MS);
    try {
      return await fetch(url, { ...opts, signal: controller.signal });
    } finally {
      clearTimeout(timer);
    }
  }

  async function getJson(url, opts) {
    const res = await request(url, opts);
    if (!res.ok) {
      let detail = '';
      try { detail = (await res.text()).slice(0, 200); } catch (e) { /* ignore */ }
      throw new Error(`${res.status} from ${redact(url)} ${detail}`.trim());
    }
    return res.json();
  }

  let ytToken = null;
  let ytTokenExpiry = 0;
  async function youtubeToken() {
    if (ytToken && now() < ytTokenExpiry) return ytToken;
    if (!env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET || !env.YOUTUBE_REFRESH_TOKEN) {
      throw new Error('YouTube credentials missing (GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN)');
    }
    const d = await getJson(TOKEN_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id: env.GOOGLE_CLIENT_ID,
        client_secret: env.GOOGLE_CLIENT_SECRET,
        refresh_token: env.YOUTUBE_REFRESH_TOKEN,
        grant_type: 'refresh_token',
      }).toString(),
    });
    if (!d.access_token) throw new Error('YouTube token refresh returned no access_token');
    ytToken = d.access_token;
    ytTokenExpiry = now() + (Math.max(120, Number(d.expires_in) || 3600) - 60) * 1000;
    return ytToken;
  }

  async function headEtag(url) {
    try {
      const res = await request(url, { method: 'HEAD' });
      if (!res.ok) return null;
      const etag = res.headers && res.headers.get ? res.headers.get('etag') : null;
      return etag ? String(etag).replace(/"/g, '') : null;
    } catch (e) {
      return null;
    }
  }

  // YouTube's vertical thumbnail exists for most Shorts but not all (it 404ed for
  // two on 2026-09-10). A found one never goes away, so only 200s are memoised.
  const portraitFound = new Map();
  async function portraitUrl(id) {
    if (portraitFound.has(id)) return portraitFound.get(id);
    const url = `https://i.ytimg.com/vi/${id}/oardefault.jpg`;
    try {
      const res = await request(url, { method: 'HEAD' });
      if (res.ok) { portraitFound.set(id, url); return url; }
    } catch (e) { /* fall back below */ }
    return null;
  }

  async function listUploads(headers, pageSize) {
    const ids = [];
    let pageToken = '';
    let pages = 0;
    do {
      const q = new URLSearchParams({ part: 'contentDetails', maxResults: String(pageSize), playlistId: UPLOADS_PLAYLIST_ID });
      if (pageToken) q.set('pageToken', pageToken);
      const page = await getJson(`${YT_API}/playlistItems?${q}`, { headers });
      for (const item of page.items || []) {
        const id = item.contentDetails && item.contentDetails.videoId;
        if (id) ids.push(id);
      }
      pageToken = page.nextPageToken || '';
      pages += 1;
    } while (pageToken && pages < 100);
    return ids;
  }

  let lastPublicIds = [];

  async function loadChannel() {
    const headers = { Authorization: `Bearer ${await youtubeToken()}` };

    // Two page sizes so a drifting page boundary can't hide the same video twice,
    // plus everything that was public last time (see the note at the top).
    const [byFifty, byTwenty] = await Promise.all([listUploads(headers, 50), listUploads(headers, 20)]);
    const ids = [...new Set([...byFifty, ...byTwenty, ...lastPublicIds])];

    const raw = [];
    for (let i = 0; i < ids.length; i += 50) {
      const q = new URLSearchParams({ part: 'snippet,contentDetails,status', id: ids.slice(i, i + 50).join(','), maxResults: '50' });
      const page = await getJson(`${YT_API}/videos?${q}`, { headers });
      raw.push(...(page.items || []));
    }

    const seenIds = new Set();
    const listable = raw.filter((v) => {
      if (!v || seenIds.has(v.id)) return false;
      seenIds.add(v.id);
      return isListable(v);
    });
    const videos = await Promise.all(listable.map(async (v) => {
      const secs = parseIsoDuration(v.contentDetails.duration);
      const [version, portrait] = await Promise.all([
        headEtag(`https://i.ytimg.com/vi/${v.id}/maxresdefault.jpg`),
        secs <= SHORT_MAX_SECONDS ? portraitUrl(v.id) : Promise.resolve(null),
      ]);
      return toFeedVideo(v, { version, portrait });
    }));
    videos.sort((a, b) => String(b.publishedAt || '').localeCompare(String(a.publishedAt || '')));
    lastPublicIds = videos.map((v) => v.id);

    const ch = await getJson(`${YT_API}/channels?${new URLSearchParams({ part: 'snippet,statistics', id: CHANNEL_ID })}`, { headers });
    const c = (ch.items || [])[0] || {};
    const stats = c.statistics || {};
    return {
      channel: {
        id: CHANNEL_ID,
        handle: (c.snippet && c.snippet.customUrl) || '@absbyai',
        url: CHANNEL_URL,
        subscriberCount: stats.hiddenSubscriberCount ? null : (Number(stats.subscriberCount) || null),
        videoCount: Number(stats.videoCount) || videos.length,
      },
      fetchedAt: new Date(now()).toISOString(),
      videos,
    };
  }

  async function loadInstagram() {
    if (!env.META_ADS_TOKEN) throw new Error('META_ADS_TOKEN not set');
    const q = new URLSearchParams({
      fields: 'id,media_type,media_url,permalink,timestamp,caption,children{media_type,media_url}',
      limit: '24',
      access_token: env.META_ADS_TOKEN,
    });
    const page = await getJson(`${GRAPH_API}/${IG_USER_ID}/media?${q}`);
    return {
      account: { id: IG_USER_ID, username: IG_USERNAME, url: `https://www.instagram.com/${IG_USERNAME}/` },
      fetchedAt: new Date(now()).toISOString(),
      images: selectInstagramImages(page.data || []),
    };
  }

  function cached(name, loader) {
    let good = null;
    let goodAt = 0;
    let inflight = null;
    let retryAt = 0;
    let lastError = null;

    async function get({ force = false } = {}) {
      const t = now();
      if (good && !force && t - goodAt < REFRESH_MS) return { ...good, stale: false };
      if (!force && t < retryAt) {
        if (good) return { ...good, stale: true };
        throw lastError || new Error(`${name} feed unavailable`);
      }
      if (!inflight) {
        inflight = (async () => {
          try {
            const d = await loader();
            good = d; goodAt = now(); retryAt = 0; lastError = null;
            return d;
          } catch (e) {
            lastError = e; retryAt = now() + RETRY_AFTER_FAILURE_MS;
            log.error(`sixpackabs ${name} feed refresh failed: ${e.message}`);
            throw e;
          } finally {
            inflight = null;
          }
        })();
      }
      try {
        return { ...(await inflight), stale: false };
      } catch (e) {
        if (good) return { ...good, stale: true };
        throw e;
      }
    }

    return { get };
  }

  const channel = cached('channel', loadChannel);
  const instagram = cached('instagram', loadInstagram);

  function route(feed) {
    return async (req, res) => {
      try {
        const body = await feed.get();
        res.set('Cache-Control', 'public, max-age=300');
        res.json(body);
      } catch (e) {
        res.set('Cache-Control', 'no-store');
        res.status(503).json({ error: 'feed_unavailable' });
      }
    };
  }

  return {
    channel,
    instagram,
    channelRoute: route(channel),
    instagramRoute: route(instagram),
    refreshAll: () => Promise.allSettled([channel.get({ force: true }), instagram.get({ force: true })]),
  };
}

module.exports = {
  createSixpackabsFeeds,
  parseIsoDuration,
  isListable,
  toFeedVideo,
  selectInstagramImages,
  altFromCaption,
  SHORT_MAX_SECONDS,
  REFRESH_MS,
};
