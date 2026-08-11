#!/usr/bin/env node
// Generic Replicate image-edit runner for the photo-edit skill.
// Usage:
//   node replicate-edit.js --image <input.jpg> --prompt-file <prompt.txt> --out <output.jpg> \
//     [--model google/nano-banana-pro] [--resolution 4K] [--env <path-to-keys.env>]
// Token: REPLICATE_API_TOKEN from the environment, or from the --env file (KEY=value lines).
const fs = require('fs');
const path = require('path');

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];

if (args.env && fs.existsSync(args.env)) {
  for (const line of fs.readFileSync(args.env, 'utf8').split('\n')) {
    const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
}
const TOKEN = process.env.REPLICATE_API_TOKEN;
if (!TOKEN) { console.error('REPLICATE_API_TOKEN not set (pass --env or export it)'); process.exit(1); }
if (!args.image || !args['prompt-file'] || !args.out) { console.error('need --image, --prompt-file, --out'); process.exit(1); }

const model = args.model || 'google/nano-banana-pro';
const prompt = fs.readFileSync(args['prompt-file'], 'utf8');
const mime = args.image.match(/\.png$/i) ? 'image/png' : 'image/jpeg';
const dataUri = `data:${mime};base64,` + fs.readFileSync(args.image).toString('base64');

// Per-model input shapes (verified against live schemas 2026-08-04).
function buildInput() {
  if (model.includes('nano-banana')) return { prompt, image_input: [dataUri], resolution: args.resolution || '4K', aspect_ratio: 'match_input_image', output_format: 'jpg', safety_filter_level: 'block_only_high' };
  if (model.includes('seedream')) return { prompt: prompt.slice(0, 4000), image_input: [dataUri], size: args.resolution || '4K', aspect_ratio: 'match_input_image', sequential_image_generation: 'disabled' };
  if (model.includes('flux-kontext')) return { prompt, input_image: dataUri, aspect_ratio: 'match_input_image', output_format: 'jpg' };
  return { prompt, image_input: [dataUri] };
}

(async () => {
  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${TOKEN}` };
  const t0 = Date.now();
  const submit = await fetch(`https://api.replicate.com/v1/models/${model}/predictions`, {
    method: 'POST', headers: { ...headers, Prefer: 'wait' }, body: JSON.stringify({ input: buildInput() }),
  });
  let pred = await submit.json().catch(() => null);
  if (!submit.ok || !pred) { console.error(`submit failed: ${submit.status} ${pred && (pred.detail || pred.title) || ''}`); process.exit(1); }
  while (pred.status === 'starting' || pred.status === 'processing') {
    await new Promise((r) => setTimeout(r, 2500));
    pred = await (await fetch(pred.urls.get, { headers })).json();
  }
  if (pred.status !== 'succeeded' || !pred.output) { console.error(`failed: ${String(pred.error || pred.status).slice(0, 300)}`); process.exit(1); }
  const url = Array.isArray(pred.output) ? pred.output[0] : pred.output;
  const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
  fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
  fs.writeFileSync(args.out, buf);
  console.log(JSON.stringify({ ok: true, out: args.out, bytes: buf.length, ms: Date.now() - t0 }));
})();
