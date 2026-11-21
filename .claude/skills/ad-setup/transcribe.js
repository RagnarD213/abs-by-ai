#!/usr/bin/env node
/**
 * /ad-setup step 3 — timestamped transcript of a finished ad, for the YouTube chapters.
 * Runs Whisper on Replicate (vaibhavs10/incredibly-fast-whisper, ~5 s, well under a cent per ad) instead of local
 * Whisper, so it never counts against the two-concurrent-video-builds cap and never slows another session's render.
 *
 *   node .claude/skills/ad-setup/transcribe.js "<master.mp4>" [more.mp4 …]
 *
 * Writes <master>.transcript.json next to each file and prints "m:ss.s text" lines.
 * Token: REPLICATE_API_TOKEN in bakeoff/.env (the repo's usual place for it).
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '../../..');
const FFMPEG = path.join(ROOT, 'Media/video_edit/bin/ffmpeg');
const tok = fs.readFileSync(path.join(ROOT, 'bakeoff/.env'), 'utf8').match(/REPLICATE_API_TOKEN=(\S+)/)[1].replace(/"/g, '');
const H = { Authorization: `Bearer ${tok}`, 'Content-Type': 'application/json' };

async function one(file, version) {
  const mp3 = path.join(os.tmpdir(), `adsetup-${process.pid}-${path.basename(file).replace(/\W+/g, '_')}.mp3`);
  execFileSync(FFMPEG, ['-v', 'error', '-y', '-i', file, '-vn', '-ac', '1', '-ar', '16000', '-b:a', '32k', mp3]);
  const audio = 'data:audio/mpeg;base64,' + fs.readFileSync(mp3).toString('base64');
  fs.unlinkSync(mp3);
  let p = await (await fetch('https://api.replicate.com/v1/predictions', { method: 'POST', headers: H,
    body: JSON.stringify({ version, input: { audio, timestamp: 'chunk', language: 'english', task: 'transcribe', batch_size: 24 } }) })).json();
  while (!['succeeded', 'failed', 'canceled'].includes(p.status)) {
    await new Promise(r => setTimeout(r, 3000));
    p = await (await fetch(p.urls.get, { headers: H })).json();
  }
  if (p.status !== 'succeeded') throw new Error(`${file}: ${p.status} ${p.error || ''}`);
  const out = file.replace(/\.[^.]+$/, '') + '.transcript.json';
  fs.writeFileSync(out, JSON.stringify(p.output));
  const lines = p.output.chunks.map(c => { const s = c.timestamp[0]; return `${Math.floor(s / 60)}:${(s % 60).toFixed(1).padStart(4, '0')} ${c.text.trim()}`; });
  return `===== ${path.basename(file)}\n${lines.join('\n')}`;
}

(async () => {
  const files = process.argv.slice(2);
  if (!files.length) { console.error('usage: transcribe.js <video> [video …]'); process.exit(2); }
  const m = await (await fetch('https://api.replicate.com/v1/models/vaibhavs10/incredibly-fast-whisper', { headers: H })).json();
  for (const r of await Promise.all(files.map(f => one(f, m.latest_version.id)))) console.log(r);
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
