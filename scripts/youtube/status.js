#!/usr/bin/env node
/** Read processing/privacy status for one or more YouTube video IDs. */
const fs = require('fs');
const os = require('os');
const path = require('path');

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

async function main() {
  const ids = process.argv.slice(2);
  if (!ids.length) throw new Error('usage: status.js <videoId> [videoId ...]');
  const s = secrets();
  const tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    body: new URLSearchParams({
      client_id: s.GOOGLE_CLIENT_ID,
      client_secret: s.GOOGLE_CLIENT_SECRET,
      refresh_token: s.YOUTUBE_REFRESH_TOKEN,
      grant_type: 'refresh_token',
    }),
  });
  const token = await tokenResponse.json();
  if (!token.access_token) throw new Error(token.error_description || token.error || `token HTTP ${tokenResponse.status}`);
  const url = new URL('https://www.googleapis.com/youtube/v3/videos');
  url.search = new URLSearchParams({ part: 'snippet,status,processingDetails', id: ids.join(',') });
  const response = await fetch(url, { headers: { Authorization: `Bearer ${token.access_token}` } });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error?.message || `videos.list HTTP ${response.status}`);
  const found = new Map((data.items || []).map((item) => [item.id, item]));
  for (const id of ids) {
    const item = found.get(id);
    if (!item) { console.log(`${id}\tNOT_FOUND`); continue; }
    console.log([
      id,
      item.processingDetails?.processingStatus || 'unknown',
      item.status?.privacyStatus || 'unknown',
      `embeddable=${item.status?.embeddable}`,
      item.snippet?.title || '',
    ].join('\t'));
  }
}

main().catch((error) => { console.error(`ERROR: ${error.message}`); process.exit(1); });
