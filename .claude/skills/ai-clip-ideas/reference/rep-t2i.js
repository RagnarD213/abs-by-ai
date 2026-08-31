#!/usr/bin/env node
// Text-to-image via Replicate nano-banana-pro (start frames; Google direct is 503).
const fs = require('fs'); const path = require('path');
const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];
if (args.env && fs.existsSync(args.env)) for (const line of fs.readFileSync(args.env, 'utf8').split('\n')) { const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m && !process.env[m[1]]) process.env[m[1]] = m[2]; }
const TOKEN = process.env.REPLICATE_API_TOKEN;
const model = args.model || 'google/nano-banana-pro';
const prompt = fs.readFileSync(args['prompt-file'], 'utf8');
const input = { prompt, resolution: args.resolution || '2K', aspect_ratio: args.aspect || '16:9', output_format: 'jpg', safety_filter_level: 'block_only_high' };
(async () => {
  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN}` };
  const t0 = Date.now();
  const submit = await fetch(`https://api.replicate.com/v1/models/${model}/predictions`, { method: 'POST', headers: { ...headers, Prefer: 'wait' }, body: JSON.stringify({ input }) });
  let pred = await submit.json().catch(() => null);
  if (!submit.ok || !pred) { console.error(`submit failed: ${submit.status} ${pred && (pred.detail || pred.title) || ''}`); process.exit(1); }
  while (pred.status === 'starting' || pred.status === 'processing') { await new Promise(r => setTimeout(r, 2500)); pred = await (await fetch(pred.urls.get, { headers })).json(); }
  if (pred.status !== 'succeeded' || !pred.output) { console.error(`failed: ${String(pred.error || pred.status).slice(0, 300)}`); process.exit(1); }
  const url = Array.isArray(pred.output) ? pred.output[0] : pred.output;
  const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
  fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
  fs.writeFileSync(args.out, buf);
  console.log(JSON.stringify({ ok: true, out: args.out, bytes: buf.length, ms: Date.now() - t0 }));
})();
