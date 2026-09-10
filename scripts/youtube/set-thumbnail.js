#!/usr/bin/env node
/**
 * Set a custom thumbnail on an existing Abs By AI YouTube video, then read it back.
 *
 * WHY THIS EXISTS
 * ---------------
 * upload.js can set a thumbnail only as part of a fresh upload. Swapping the thumbnail
 * on a video that is already up used to mean Studio's clipboard-paste trick in Chrome.
 * thumbnails.set needs only the youtube.upload scope, which YOUTUBE_REFRESH_TOKEN has,
 * so this does it by API and then proves it took: videos.list -> the highest thumbnail
 * URL -> downloaded to --out so the caller can compare it against the file it sent.
 *
 * USAGE
 *   node scripts/youtube/set-thumbnail.js --video <id> --file thumb.jpg [--out readback.jpg]
 *   node scripts/youtube/set-thumbnail.js --video <id> --read-only --out readback.jpg
 *
 * JPEG/PNG, max 2 MB. The i.ytimg.com URL does not change when the image does, so the
 * read-back retries until the served bytes differ from what was served before the set.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const SECRETS = path.join(os.homedir(), '.absbyai-secrets.env');

function loadSecrets() {
  const out = { ...process.env };
  try {
    for (const line of fs.readFileSync(SECRETS, 'utf8').split('\n')) {
      const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
      if (m && !out[m[1]]) out[m[1]] = m[2].replace(/^"|"$/g, '');
    }
  } catch (e) { /* env-only is fine */ }
  return out;
}

function args() {
  const a = process.argv.slice(2);
  const o = {};
  for (let i = 0; i < a.length; i++) {
    if (a[i] === '--video') o.video = a[++i];
    else if (a[i] === '--file') o.file = a[++i];
    else if (a[i] === '--out') o.out = a[++i];
    else if (a[i] === '--read-only') o.readOnly = true;
  }
  if (!o.video || (!o.file && !o.readOnly)) {
    console.error('usage: set-thumbnail.js --video <id> --file thumb.jpg [--out readback.jpg] | --video <id> --read-only --out f.jpg');
    process.exit(2);
  }
  return o;
}

async function accessToken(s) {
  if (!s.YOUTUBE_REFRESH_TOKEN) throw new Error('YOUTUBE_REFRESH_TOKEN missing from ~/.absbyai-secrets.env');
  const r = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    body: new URLSearchParams({
      client_id: s.GOOGLE_CLIENT_ID,
      client_secret: s.GOOGLE_CLIENT_SECRET,
      refresh_token: s.YOUTUBE_REFRESH_TOKEN,
      grant_type: 'refresh_token',
    }),
  });
  const d = await r.json();
  if (!d.access_token) throw new Error('token refresh failed: ' + JSON.stringify(d));
  return d.access_token;
}

async function thumbUrl(token, id) {
  const r = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const d = await r.json();
  const v = (d.items || [])[0];
  if (!v) throw new Error(`videos.list returned no video for ${id}: ${JSON.stringify(d.error || d)}`);
  // Right after a set, videos.list can already name a maxres URL that still 404s for a
  // while (seen 2026-09-10), so keep every size and let fetchBytes take the first that serves.
  const t = v.snippet.thumbnails;
  const sizes = ['maxres', 'standard', 'high'].filter((k) => t[k]).map((k) => ({ key: k, ...t[k] }));
  return { title: v.snippet.title, sizes };
}

async function fetchBytes(info) {
  for (const s of info.sizes) {
    // Cache-busted first: the bare maxres URL can keep serving the OLD image from a CDN edge long
    // after the set took (2 of 3 videos on 2026-09-10, while ?cb= and every smaller size were new).
    // Bare second: right after a set, a query-string URL can 404 while the bare one serves.
    // All sizes 404 for a minute or two while YouTube processes a freshly set thumbnail.
    for (const u of [`${s.url}?cb=${Date.now()}`, s.url]) {
      const r = await fetch(u, { cache: 'no-store' });
      if (r.ok) { info.url = s.url; info.key = s.key; info.w = s.width; info.h = s.height; return Buffer.from(await r.arrayBuffer()); }
    }
  }
  throw new Error(`no thumbnail size serves yet: ${info.sizes.map((s) => s.url).join(', ')}`);
}

async function main() {
  const o = args();
  const token = await accessToken(loadSecrets());
  const before = await thumbUrl(token, o.video);
  const old = await fetchBytes(before).catch(() => Buffer.alloc(0));

  if (!o.readOnly) {
    const size = fs.statSync(o.file).size;
    if (size > 2 * 1024 * 1024) throw new Error(`${o.file} is ${size} bytes; YouTube caps thumbnails at 2 MB`);
    const type = /\.png$/i.test(o.file) ? 'image/png' : 'image/jpeg';
    const r = await fetch(`https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${o.video}&uploadType=media`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': type },
      body: fs.readFileSync(o.file),
    });
    if (!r.ok) throw new Error(`thumbnails.set failed (${r.status}): ${await r.text()}`);
    console.log(`set:       ${o.video} <- ${path.basename(o.file)}`);
  }

  // Read back. After a set, wait until the served image changes (CDN lag is usually seconds).
  let now = await thumbUrl(token, o.video);
  let bytes = await fetchBytes(now);
  for (let i = 0; !o.readOnly && bytes.equals(old) && i < 12; i++) {
    await new Promise((res) => setTimeout(res, 5000));
    now = await thumbUrl(token, o.video);
    bytes = await fetchBytes(now);
  }
  const changed = !bytes.equals(old);
  console.log(`video:     ${now.title}`);
  console.log(`read back: ${now.url} (${now.key} ${now.w}x${now.h}, ${bytes.length} bytes)${o.readOnly ? '' : changed ? ' — changed' : ' — UNCHANGED after 60 s'}`);
  if (o.out) { fs.writeFileSync(o.out, bytes); console.log(`saved:     ${o.out}`); }
  if (!o.readOnly && !changed) process.exit(3);
}

main().catch((e) => { console.error('ERROR:', e.message); process.exit(1); });
