#!/usr/bin/env node
// Verify the approved Ad 10 square uploads and reuse tags from the live 16:9.
const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert/strict');

async function main() {
  const s = { ...process.env };
  for (const line of fs.readFileSync(path.join(os.homedir(), '.absbyai-secrets.env'), 'utf8').split('\n')) {
    const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m && !s[m[1]]) s[m[1]] = m[2].replace(/^"|"$/g, '');
  }
  const response = await fetch('https://oauth2.googleapis.com/token', {method: 'POST', body: new URLSearchParams({
    client_id: s.GOOGLE_CLIENT_ID, client_secret: s.GOOGLE_CLIENT_SECRET,
    refresh_token: s.YOUTUBE_REFRESH_TOKEN, grant_type: 'refresh_token',
  })});
  const token = await response.json();
  if (!token.access_token) throw new Error(token.error_description || 'YouTube token refresh failed');
  const ids = process.argv.slice(2);
  const allIds = ['Sg3vcEY2P_8', ...ids];
  const r = await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet,status,processingDetails,contentDetails&id=${allIds.join(',')}`,
    {headers: {Authorization: `Bearer ${token.access_token}`}});
  const data = await r.json();
  if (!r.ok) throw new Error(data.error?.message || 'YouTube read failed');
  const source = data.items.find(v => v.id === 'Sg3vcEY2P_8');
  assert(source, '16:9 source missing');
  if (!ids.length) {
    console.log(JSON.stringify({tags: source.snippet.tags || [], categoryId: source.snippet.categoryId}));
    return;
  }
  assert.equal(data.items.length, allIds.length);
  for (const id of ids) {
    const v = data.items.find(item => item.id === id);
    assert.equal(v.snippet.channelId, 'UC236gjadarHAhEhOMYNGJ9g');
    assert.equal(v.processingDetails.processingStatus, 'succeeded');
    assert.equal(v.status.privacyStatus, 'unlisted');
    assert.equal(v.status.embeddable, true);
    assert.equal(v.status.madeForKids, false);
    assert.equal(v.status.selfDeclaredMadeForKids, false);
    assert.equal(v.snippet.categoryId, '26');
    assert.deepEqual(v.snippet.tags || [], source.snippet.tags || []);
    assert(!v.status.publishAt);
    assert(!/[\u2013\u2014]/.test(v.snippet.title + v.snippet.description));
    console.log(`${id}: succeeded, unlisted, embeddable, not made for kids, category 26, ${v.contentDetails.duration}`);
  }
  const out = path.join('Muhammad Ad Videos', 'my dad bod at 38 my dad bod at 40 - ad 10', 'youtube-square-readback.json');
  fs.writeFileSync(out, JSON.stringify(data, null, 2) + '\n');
  console.log(`saved: ${out}`);
}
main().catch(e => { console.error('FAILED: ' + e.message); process.exitCode = 1; });
