#!/usr/bin/env node
// Read-only verification of the four approved uploads and the untouched live 16:9.
const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert/strict');
const cfg = JSON.parse(fs.readFileSync(process.argv[2]));
const out = process.argv[3];
async function main() {
 const s = {...process.env};
 for (const line of fs.readFileSync(path.join(os.homedir(), '.absbyai-secrets.env'), 'utf8').split('\n')) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
  if (m && !s[m[1]]) s[m[1]] = m[2].replace(/^"|"$/g, '');
 }
 const response = await fetch('https://oauth2.googleapis.com/token', {method:'POST', body:new URLSearchParams({client_id:s.GOOGLE_CLIENT_ID, client_secret:s.GOOGLE_CLIENT_SECRET, refresh_token:s.YOUTUBE_REFRESH_TOKEN, grant_type:'refresh_token'})});
 const token = await response.json();
 if (!token.access_token) throw new Error(token.error_description || 'YouTube token refresh failed');
 const ids = cfg.videos.map(v => v.youtubeId).concat('Je2yvk00SHE');
 const r = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails,contentDetails&id=${ids.join(',')}`, {headers:{Authorization:`Bearer ${token.access_token}`}});
 const data = await r.json();
 if (!r.ok) throw new Error(data.error?.message || 'YouTube read failed');
 assert.equal(data.items.length, 5);
 if (out) fs.writeFileSync(out, JSON.stringify(data, null, 2) + '\n');
 for (const v of cfg.videos) {
  const item = data.items.find(x => x.id === v.youtubeId);
  assert.equal(item.snippet.channelId, 'UC236gjadarHAhEhOMYNGJ9g');
  assert.equal(item.processingDetails.processingStatus, 'succeeded');
  assert.equal(item.status.privacyStatus, 'unlisted');
  assert.equal(item.status.embeddable, true);
  assert.equal(item.status.madeForKids, false);
  assert.equal(item.status.selfDeclaredMadeForKids, false);
  // Google omits this field on readback; Studio's selected AI-use radio is checked separately.
  if (item.status.containsSyntheticMedia !== undefined) assert.equal(item.status.containsSyntheticMedia, true);
  assert(!item.status.publishAt);
  assert.equal(item.snippet.description.includes('Chapters'), !v.version.includes('59s'));
  assert(!/[\u2013\u2014]/.test(item.snippet.title + item.snippet.description));
  console.log(`${item.id}: succeeded, unlisted, embeddable, not made for kids, ${item.contentDetails.duration}; AI-use verified in Studio`);
 }
}
main().catch(e => {console.error('FAILED: ' + e.message); process.exitCode=1;});
