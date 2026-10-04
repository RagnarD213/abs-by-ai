#!/usr/bin/env node
// Read video status and preserve the evidence without exposing credentials.
const fs = require('fs');
const os = require('os');
const s = { ...process.env };
for (const l of fs.readFileSync(os.homedir() + '/.absbyai-secrets.env', 'utf8').split('\n')) {
  const m = l.match(/^([A-Z0-9_]+)=(.*)$/);
  if (m && !s[m[1]]) s[m[1]] = m[2].replace(/^"|"$/g, '');
}
async function main() {
  const t = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', body: new URLSearchParams({
    client_id: s.GOOGLE_CLIENT_ID, client_secret: s.GOOGLE_CLIENT_SECRET,
    refresh_token: s.YOUTUBE_REFRESH_TOKEN, grant_type: 'refresh_token',
  }) }).then(r => r.json());
  if (!t.access_token) throw new Error('YouTube authentication failed');
  const get = async (url) => {
    const j = await fetch('https://www.googleapis.com/youtube/v3/' + url, { headers: { Authorization: 'Bearer ' + t.access_token } }).then(r => r.json());
    if (j.error) throw new Error(j.error.message);
    return j;
  };
  if (process.argv[2] === '--recent') {
    const c = await get('channels?part=contentDetails&mine=true');
    if (c.items[0].id !== 'UC236gjadarHAhEhOMYNGJ9g') throw new Error('Wrong channel');
    const j = await get('playlistItems?part=snippet&maxResults=50&playlistId=' + c.items[0].contentDetails.relatedPlaylists.uploads);
    for (const x of j.items) console.log(JSON.stringify({ id: x.snippet.resourceId.videoId, title: x.snippet.title, at: x.snippet.publishedAt }));
    return;
  }
  const j = await get('videos?part=snippet,status,contentDetails,processingDetails&id=' + process.argv[2]);
  if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(j, null, 2) + '\n');
  for (const v of j.items) console.log(JSON.stringify({ id:v.id, title:v.snippet.title, duration:v.contentDetails.duration,
    status:v.status, processingStatus:v.processingDetails && v.processingDetails.processingStatus }));
}
main().catch(e => { console.error(e.message); process.exit(1); });
