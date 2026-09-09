#!/usr/bin/env node
/**
 * Upload a video file to the Abs By AI YouTube channel (resumable upload).
 *
 * WHY THIS EXISTS
 * ---------------
 * Until 2026-09-09 nothing in this repo could put a video on YouTube: the Chrome
 * extension's file_upload is capped at 10 MB (our masters are 0.4-1.3 GB) and the
 * stored GOOGLE_REFRESH_TOKEN was calendar.readonly only. That blocked the website
 * conversion video, the two finished long-forms (02 + 03) and every Short re-upload.
 * This script closes that gap with a proper resumable upload against the YouTube
 * Data API, using a YOUTUBE_REFRESH_TOKEN minted for the "Abs by AI" brand channel.
 *
 * ONE-TIME SETUP (already done, recorded here so it can be redone)
 *   1. Google Cloud project 768453214640 must have the YouTube Data API v3 enabled.
 *   2. Consent through the OAuth Playground redirect (the only redirect URI this
 *      client has registered) with scopes youtube.upload + youtube.readonly, picking
 *      the "Abs by AI" BRAND account at the account chooser — not the personal one,
 *      or the video lands on the wrong channel.
 *   3. Store the refresh token as YOUTUBE_REFRESH_TOKEN in ~/.absbyai-secrets.env.
 *
 * USAGE
 *   node scripts/youtube/upload.js --file "path/to/video.mp4" \
 *     --title "Title" [--description-file notes.md] [--privacy unlisted] \
 *     [--tags "a,b,c"] [--made-for-kids false] [--dry-run]
 *
 * Prints the video id and watch/embed URLs on success. Safe to re-run only if the
 * previous attempt failed — YouTube does not dedupe, a second run makes a second video.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const SECRETS = path.join(os.homedir(), '.absbyai-secrets.env');
const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const UPLOAD_URL = 'https://www.googleapis.com/upload/youtube/v3/videos';
// 8 MB chunks: small enough that a dropped connection costs little, large enough
// that a 450 MB master is ~56 requests rather than thousands.
const CHUNK = 8 * 1024 * 1024;

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
  const o = { privacy: 'unlisted', madeForKids: false, dryRun: false };
  for (let i = 0; i < a.length; i++) {
    const k = a[i];
    if (k === '--file') o.file = a[++i];
    else if (k === '--title') o.title = a[++i];
    else if (k === '--description') o.description = a[++i];
    else if (k === '--description-file') o.descriptionFile = a[++i];
    else if (k === '--privacy') o.privacy = a[++i];
    else if (k === '--tags') o.tags = a[++i].split(',').map((s) => s.trim()).filter(Boolean);
    else if (k === '--category') o.category = a[++i];
    else if (k === '--made-for-kids') o.madeForKids = a[++i] === 'true';
    else if (k === '--dry-run') o.dryRun = true;
  }
  return o;
}

async function accessToken(s) {
  if (!s.YOUTUBE_REFRESH_TOKEN) throw new Error('YOUTUBE_REFRESH_TOKEN missing from ~/.absbyai-secrets.env');
  const body = new URLSearchParams({
    client_id: s.GOOGLE_CLIENT_ID,
    client_secret: s.GOOGLE_CLIENT_SECRET,
    refresh_token: s.YOUTUBE_REFRESH_TOKEN,
    grant_type: 'refresh_token',
  });
  const r = await fetch(TOKEN_URL, { method: 'POST', body });
  const d = await r.json();
  if (!d.access_token) throw new Error('token refresh failed: ' + JSON.stringify(d));
  return d.access_token;
}

// Confirms the token points at the channel we think it does, so a mis-picked
// brand account fails loudly BEFORE 450 MB goes up to the wrong place.
async function whoami(token) {
  const r = await fetch('https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true', {
    headers: { Authorization: `Bearer ${token}` },
  });
  const d = await r.json();
  if (d.error) throw new Error('channels.list failed: ' + (d.error.message || JSON.stringify(d.error)));
  const c = (d.items || [])[0];
  if (!c) throw new Error('This token controls no channel — the brand account was not selected at consent.');
  return { id: c.id, title: c.snippet.title };
}

async function main() {
  const o = args();
  const s = loadSecrets();
  if (!o.file) throw new Error('--file is required');
  if (!fs.existsSync(o.file)) throw new Error('file not found: ' + o.file);
  if (!o.title) throw new Error('--title is required');
  if (!['unlisted', 'private', 'public'].includes(o.privacy)) throw new Error('--privacy must be unlisted|private|public');

  const size = fs.statSync(o.file).size;
  const description = o.descriptionFile ? fs.readFileSync(o.descriptionFile, 'utf8') : (o.description || '');

  const token = await accessToken(s);
  const ch = await whoami(token);
  console.log(`channel: ${ch.title} (${ch.id})`);
  console.log(`file:    ${path.basename(o.file)} — ${(size / 1048576).toFixed(1)} MB`);
  console.log(`title:   ${o.title}`);
  console.log(`privacy: ${o.privacy}`);
  if (o.dryRun) { console.log('DRY RUN — nothing uploaded.'); return; }

  const metadata = {
    snippet: {
      title: o.title,
      description,
      ...(o.tags ? { tags: o.tags } : {}),
      ...(o.category ? { categoryId: o.category } : {}),
    },
    status: {
      privacyStatus: o.privacy,
      selfDeclaredMadeForKids: !!o.madeForKids,
      embeddable: true,
    },
  };

  // 1. Open the resumable session.
  const init = await fetch(`${UPLOAD_URL}?uploadType=resumable&part=snippet,status`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=UTF-8',
      'X-Upload-Content-Length': String(size),
      'X-Upload-Content-Type': 'video/mp4',
    },
    body: JSON.stringify(metadata),
  });
  if (!init.ok) throw new Error(`resumable init failed ${init.status}: ${await init.text()}`);
  const session = init.headers.get('location');
  if (!session) throw new Error('no upload session URL returned');

  // 2. Push the bytes. 308 = "keep going", and its Range header is the source of
  //    truth for how much the server actually kept — never assume our own offset.
  const fd = fs.openSync(o.file, 'r');
  let offset = 0;
  let videoId = null;
  const started = Date.now();
  try {
    while (offset < size) {
      const end = Math.min(offset + CHUNK, size);
      const len = end - offset;
      const buf = Buffer.allocUnsafe(len);
      fs.readSync(fd, buf, 0, len, offset);

      let res;
      for (let attempt = 1; attempt <= 5; attempt++) {
        try {
          res = await fetch(session, {
            method: 'PUT',
            headers: {
              'Content-Length': String(len),
              'Content-Range': `bytes ${offset}-${end - 1}/${size}`,
            },
            body: buf,
          });
          break;
        } catch (e) {
          if (attempt === 5) throw e;
          await new Promise((r) => setTimeout(r, 1500 * attempt));
        }
      }

      if (res.status === 308) {
        const range = res.headers.get('range');
        offset = range ? parseInt(range.split('-')[1], 10) + 1 : end;
        const pct = ((offset / size) * 100).toFixed(1);
        const mbps = (offset / 1048576) / ((Date.now() - started) / 1000);
        process.stdout.write(`\r  ${pct}%  ${(offset / 1048576).toFixed(0)}/${(size / 1048576).toFixed(0)} MB  ${mbps.toFixed(1)} MB/s   `);
      } else if (res.ok) {
        const done = await res.json();
        videoId = done.id;
        offset = size;
        process.stdout.write('\r  100%                                  \n');
      } else {
        throw new Error(`chunk failed ${res.status}: ${await res.text()}`);
      }
    }
  } finally {
    fs.closeSync(fd);
  }

  if (!videoId) throw new Error('upload finished without returning a video id');
  console.log(`\nvideo id:  ${videoId}`);
  console.log(`watch:     https://www.youtube.com/watch?v=${videoId}`);
  console.log(`embed:     https://www.youtube-nocookie.com/embed/${videoId}`);
  console.log(`studio:    https://studio.youtube.com/video/${videoId}/edit`);
}

main().catch((e) => { console.error('\nERROR:', e.message); process.exit(1); });
