#!/usr/bin/env node
// RA-07: word-timestamped transcript of the take span on Replicate (the same model /ad-setup's transcribe.js uses), so the
// transcript never takes one of the machine's two build slots. Usage: node replicate_words.js span.mp3 OFFSET out.json
const fs = require('fs'), path = require('path');
const ROOT = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const tok = fs.readFileSync(path.join(ROOT, 'bakeoff/.env'), 'utf8').match(/REPLICATE_API_TOKEN=(\S+)/)[1].replace(/"/g, '');
const H = { Authorization: `Bearer ${tok}`, 'Content-Type': 'application/json' };
(async () => {
  const [file, off, out] = [process.argv[2], parseFloat(process.argv[3]), process.argv[4]];
  const m = await (await fetch('https://api.replicate.com/v1/models/vaibhavs10/incredibly-fast-whisper', { headers: H })).json();
  const version = m.latest_version.id;
  const audio = 'data:audio/mpeg;base64,' + fs.readFileSync(file).toString('base64');
  let p = await (await fetch('https://api.replicate.com/v1/predictions', { method: 'POST', headers: H,
    body: JSON.stringify({ version, input: { audio, timestamp: 'word', language: 'english', task: 'transcribe', batch_size: 24 } }) })).json();
  while (!['succeeded', 'failed', 'canceled'].includes(p.status)) { await new Promise(r => setTimeout(r, 3000)); p = await (await fetch(p.urls.get, { headers: H })).json(); }
  if (p.status !== 'succeeded') throw new Error(`${p.status} ${p.error || ''}`);
  fs.writeFileSync(out.replace(/\.json$/, '.raw.json'), JSON.stringify(p.output));
  const words = p.output.chunks.filter(c => c.timestamp && c.timestamp[0] != null).map(c => ({ word: ' ' + c.text.trim(), start: +(c.timestamp[0] + off).toFixed(3), end: +(((c.timestamp[1] ?? c.timestamp[0] + 0.2)) + off).toFixed(3) }));
  fs.writeFileSync(out, JSON.stringify({ source: 'replicate vaibhavs10/incredibly-fast-whisper (large-v3), word timestamps', predict_time: p.metrics && p.metrics.predict_time, segments: [{ start: words[0].start, end: words[words.length - 1].end, words }] }, null, 1));
  console.log(words.length, 'words', words[0].start, '..', words[words.length - 1].end, 'predict', p.metrics && p.metrics.predict_time);
  console.log(p.output.text);
})().catch(e => { console.error(e); process.exit(1); });
