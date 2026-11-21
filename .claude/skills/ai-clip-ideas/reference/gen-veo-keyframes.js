#!/usr/bin/env node
// Keyframe-locked video generation via Replicate Veo.
// Usage:
//   node gen-veo-keyframes.js --start start.jpg --end end.jpg --prompt-file motion.txt --out clip.mp4 \
//     [--model google/veo-3.1-fast] [--duration 8] [--aspect 16:9] [--env ~/.absbyai-secrets.env]
// Notes:
//   - The Gemini-direct API does NOT support last_frame; Replicate does. Use this for any start+end pair.
//   - generate_audio is false on purpose: ad clips ride under Dan's own mix.
const fs = require('fs'); const path = require('path');
const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];
const envFile = args.env || process.env.HOME + '/.absbyai-secrets.env';
if (fs.existsSync(envFile)) for (const l of fs.readFileSync(envFile, 'utf8').split('\n')) { const m = l.match(/^([A-Z0-9_]+)=(.*)$/); if (m && !process.env[m[1]]) process.env[m[1]] = m[2]; }
const TOKEN = process.env.REPLICATE_API_TOKEN;
if (!TOKEN || !args.start || !args.end || !args['prompt-file'] || !args.out) { console.error('need REPLICATE_API_TOKEN + --start --end --prompt-file --out'); process.exit(1); }
const uri = f => 'data:image/jpeg;base64,' + fs.readFileSync(f).toString('base64');
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const model = args.model || 'google/veo-3.1-fast';
  const input = {
    prompt: fs.readFileSync(args['prompt-file'], 'utf8'),
    image: uri(args.start), last_frame: uri(args.end),
    duration: +(args.duration || 8), resolution: '1080p',
    aspect_ratio: args.aspect || '16:9', generate_audio: false,
  };
  const r = await fetch(`https://api.replicate.com/v1/models/${model}/predictions`, {
    method: 'POST', headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ input }),
  });
  const p = await r.json();
  if (r.status >= 400) { console.error(`HTTP ${r.status}: ${JSON.stringify(p).slice(0, 400)}`); process.exit(1); }
  console.log('submitted', p.id);
  for (;;) {
    await sleep(10000);
    const q = await (await fetch(`https://api.replicate.com/v1/predictions/${p.id}`, { headers: { Authorization: `Bearer ${TOKEN}` } })).json();
    if (q.status === 'succeeded') {
      const url = Array.isArray(q.output) ? q.output[0] : q.output;
      fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
      fs.writeFileSync(args.out, Buffer.from(await (await fetch(url)).arrayBuffer()));
      console.log(JSON.stringify({ ok: true, out: args.out, mb: (fs.statSync(args.out).size / 1048576).toFixed(1) }));
      process.exit(0);
    }
    if (q.status === 'failed' || q.status === 'canceled') { console.error(q.status, JSON.stringify(q.error).slice(0, 400)); process.exit(1); }
    console.log(q.status);
  }
})();
