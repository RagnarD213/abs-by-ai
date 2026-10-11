#!/usr/bin/env node
/**
 * Which public videos on the channel still need their pinned question comment?
 *
 * Dan, 2026-10-11: every published video carries one pinned comment from the channel that asks
 * the viewer an easy question, to start the discussion. The YouTube API cannot pin a comment
 * (and our token has no comment scope), so the post + pin is done in Chrome. This script only
 * finds the gaps; the procedure is Docs/PINNED_COMMENTS.md.
 *
 *   node scripts/youtube/pinned_comment_gap.js            human list
 *   node scripts/youtube/pinned_comment_gap.js --json     {gaps:[{id,title,published,comment,config}], done}
 *   node scripts/youtube/pinned_comment_gap.js --mark <id> "<comment text>"   record one as pinned
 *
 * A gap's `comment` comes from the "pinned_comment" field of the Blotato config whose "title"
 * equals the video title (scripts/blotato/configs/*.json). null means no config carries one:
 * write the question then (rules in Docs/PINNED_COMMENTS.md).
 * Ledger: scripts/youtube/pinned_comments.json. Exit 2 when the channel cannot be read.
 */
const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT = path.join(__dirname, '..', '..');
const LEDGER = path.join(__dirname, 'pinned_comments.json');
const CONFIGS = path.join(ROOT, 'scripts', 'blotato', 'configs');

function secrets() {
  const out = { ...process.env };
  try {
    for (const line of fs.readFileSync(path.join(os.homedir(), '.absbyai-secrets.env'), 'utf8').split('\n')) {
      const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
      if (m && !out[m[1]]) out[m[1]] = m[2].replace(/^"|"$/g, '');
    }
  } catch (_) {}
  return out;
}

const norm = (s) => String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

function configComments() {
  const byTitle = new Map();
  let files = [];
  try { files = fs.readdirSync(CONFIGS).filter((f) => f.endsWith('.json')); } catch (_) {}
  for (const f of files) {
    try {
      const c = JSON.parse(fs.readFileSync(path.join(CONFIGS, f), 'utf8'));
      if (c.title && c.pinned_comment) byTitle.set(norm(c.title), { comment: c.pinned_comment, config: `scripts/blotato/configs/${f}` });
    } catch (_) {}
  }
  return byTitle;
}

async function publicVideos() {
  const s = secrets();
  const tr = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    body: new URLSearchParams({
      client_id: s.GOOGLE_CLIENT_ID, client_secret: s.GOOGLE_CLIENT_SECRET,
      refresh_token: s.YOUTUBE_REFRESH_TOKEN, grant_type: 'refresh_token',
    }),
  });
  const token = await tr.json();
  if (!token.access_token) throw new Error(token.error_description || token.error || `token HTTP ${tr.status}`);
  const get = async (p, q) => {
    const u = new URL(`https://www.googleapis.com/youtube/v3/${p}`);
    u.search = new URLSearchParams(q);
    const r = await fetch(u, { headers: { Authorization: `Bearer ${token.access_token}` } });
    const j = await r.json();
    if (!r.ok) throw new Error(j.error?.message || `${p} HTTP ${r.status}`);
    return j;
  };
  const ch = await get('channels', { part: 'contentDetails', mine: 'true' });
  const uploads = ch.items[0].contentDetails.relatedPlaylists.uploads;
  const ids = new Set();
  let pageToken = '';
  do {
    const r = await get('playlistItems', { part: 'contentDetails', playlistId: uploads, maxResults: 50, ...(pageToken ? { pageToken } : {}) });
    r.items.forEach((i) => ids.add(i.contentDetails.videoId));
    pageToken = r.nextPageToken;
  } while (pageToken);
  const out = [];
  const list = [...ids];
  for (let i = 0; i < list.length; i += 50) {
    const r = await get('videos', { part: 'snippet,status', id: list.slice(i, i + 50).join(',') });
    for (const v of r.items) {
      // Public only: unlisted uploads are ads (never organic) and get no comment.
      if (v.status.privacyStatus === 'public') out.push({ id: v.id, title: v.snippet.title, published: v.snippet.publishedAt.slice(0, 10) });
    }
  }
  return out;
}

async function main() {
  const args = process.argv.slice(2);
  const ledger = JSON.parse(fs.readFileSync(LEDGER, 'utf8'));
  if (args[0] === '--mark') {
    const [, id, comment] = args;
    if (!id || !comment) throw new Error('usage: --mark <videoId> "<comment text>"');
    if (/[–—]/.test(comment)) throw new Error('comment contains an em or en dash');
    const v = (await publicVideos()).find((x) => x.id === id);
    if (!v) throw new Error(`${id} is not a public video on the channel`);
    ledger[id] = { title: v.title, comment, pinned: new Date().toISOString().slice(0, 10) };
    fs.writeFileSync(LEDGER, `${JSON.stringify(ledger, null, 1)}\n`);
    console.log(`recorded ${id}`);
    return;
  }
  const cfg = configComments();
  const vids = await publicVideos();
  const gaps = vids.filter((v) => !ledger[v.id]).map((v) => ({ ...v, ...(cfg.get(norm(v.title)) || { comment: null, config: null }) }));
  if (args.includes('--json')) {
    console.log(JSON.stringify({ gaps, done: vids.length - gaps.length }, null, 1));
    return;
  }
  console.log(`pinned comments: ${gaps.length} gaps (${vids.length - gaps.length} done)`);
  for (const g of gaps) console.log(`${g.id} | ${g.published} | ${g.title} | ${g.comment || 'NO QUESTION ON FILE'}`);
}

main().catch((e) => { console.error(e.message); process.exit(2); });
