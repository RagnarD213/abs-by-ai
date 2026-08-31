#!/usr/bin/env node
/**
 * Google-direct image generation/editing for the content skills (photo-edit,
 * imagesandclips, make-ad, bake-offs). NOT used by the product — `server.js`
 * has its own generation path and must not import this.
 *
 * Why this exists (measured 2026-08-10, see COSTS.md):
 *   • Replicate charges a small markup over Google for nano-banana-pro and has
 *     NO batch tier. Google direct has one, at a flat 50% discount.
 *   • Drafting at 2K instead of 4K is 44% cheaper per image ($0.134 vs $0.24)
 *     and 1K costs the SAME as 2K, so 2K is the correct draft tier.
 *
 * Usage:
 *   node gemini-image.js generate --prompt-file p.txt --out o.jpg \
 *        [--image in.jpg] [--tier draft|final] [--model M] [--env keys.env]
 *
 *   node gemini-image.js batch-submit  --spec jobs.json [--tier draft|final] [--model M]
 *   node gemini-image.js batch-status  --job <batches/xyz>
 *   node gemini-image.js batch-collect --job <batches/xyz> --out-dir out/
 *
 * jobs.json is [{ "key": "row1", "promptFile": "p1.txt", "image": "a.jpg" }, ...]
 * (`image` optional — omit for text-to-image).
 *
 * Tiers:
 *   draft → imageSize 2K   ($0.134/img, halves again under batch)
 *   final → imageSize 4K   ($0.24/img)
 *
 * MODEL CHOICE IS NOT A COST DIAL FOR RETOUCHING. Measured 2026-08-10 on
 * public/img/proof/male-before.webp: gemini-3.1-flash-image (Nano Banana 2,
 * ~half price) CHANGED THE SUBJECT'S SHORTS from black to grey and shifted the
 * framing — it re-renders rather than retouches, the same failure the
 * photo-edit skill records for Seedream and FLUX. gemini-3-pro-image held
 * garment, background, framing and identity exactly. Use Pro for any edit of an
 * existing photo. Nano Banana 2 is fine for NEW images (ad stills, character
 * sheets) where there is no original to preserve.
 */
const fs = require('fs');
const path = require('path');

const argv = process.argv.slice(2);
const cmd = argv[0];
const args = {};
for (let i = 1; i < argv.length; i += 2) args[argv[i].replace(/^--/, '')] = argv[i + 1];

if (args.env && fs.existsSync(args.env)) {
  for (const line of fs.readFileSync(args.env, 'utf8').split('\n')) {
    const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  }
}
const KEY = process.env.GEMINI_API_KEY;
if (!KEY) { console.error('GEMINI_API_KEY not set (pass --env or export it)'); process.exit(1); }

const BASE = 'https://generativelanguage.googleapis.com/v1beta';
const TIER_SIZE = { draft: '2K', final: '4K' };
const PRICE = { '1K': 0.134, '2K': 0.134, '4K': 0.24 };

const tier = args.tier || 'final';
if (!TIER_SIZE[tier]) { console.error(`--tier must be draft or final (got ${tier})`); process.exit(1); }
const imageSize = args.resolution || TIER_SIZE[tier];
const model = args.model || 'gemini-3-pro-image';

const mimeOf = (p) => (/\.png$/i.test(p) ? 'image/png' : /\.webp$/i.test(p) ? 'image/webp' : 'image/jpeg');

/** Build one GenerateContentRequest. Shared by the sync and batch paths so the
 *  two can never drift — a batch result must be the same image a live call
 *  would have produced. */
function buildRequest(promptFile, imageFile) {
  const parts = [{ text: fs.readFileSync(promptFile, 'utf8') }];
  if (imageFile) {
    parts.push({ inline_data: { mime_type: mimeOf(imageFile), data: fs.readFileSync(imageFile).toString('base64') } });
  }
  return {
    contents: [{ parts }],
    generationConfig: { responseModalities: ['TEXT', 'IMAGE'], imageConfig: args.aspect ? { imageSize, aspectRatio: args.aspect } : { imageSize } },
  };
}

async function api(url, opts = {}) {
  const res = await fetch(url, opts);
  const text = await res.text();
  let json = null;
  try { json = JSON.parse(text); } catch (_) { /* non-JSON (e.g. file download) */ }
  if (!res.ok) {
    const msg = (json && json.error && json.error.message) || text.slice(0, 300);
    throw new Error(`HTTP ${res.status}: ${msg}`);
  }
  return json !== null ? json : text;
}

/** Pull the first inline image out of a candidate, tolerating both the
 *  camelCase and snake_case spellings the API uses in different responses. */
function firstImage(candidate) {
  const parts = ((candidate || {}).content || {}).parts || [];
  for (const p of parts) {
    const d = p.inlineData || p.inline_data;
    if (d && d.data) return Buffer.from(d.data, 'base64');
  }
  return null;
}

function writeOut(file, buf) {
  fs.mkdirSync(path.dirname(path.resolve(file)), { recursive: true });
  fs.writeFileSync(file, buf);
}

async function generate() {
  if (!args['prompt-file'] || !args.out) { console.error('need --prompt-file and --out'); process.exit(1); }
  const t0 = Date.now();
  const body = buildRequest(args['prompt-file'], args.image);
  const d = await api(`${BASE}/models/${model}:generateContent?key=${KEY}`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  });
  const cand = (d.candidates || [])[0];
  const buf = firstImage(cand);
  if (!buf) {
    console.error(`no image returned (finishReason=${cand && cand.finishReason})`);
    process.exit(1);
  }
  writeOut(args.out, buf);
  console.log(JSON.stringify({
    ok: true, out: args.out, bytes: buf.length, ms: Date.now() - t0,
    model, tier, imageSize, estCostUsd: PRICE[imageSize],
  }));
}

async function batchSubmit() {
  if (!args.spec) { console.error('need --spec jobs.json'); process.exit(1); }
  const jobs = JSON.parse(fs.readFileSync(args.spec, 'utf8'));
  if (!Array.isArray(jobs) || !jobs.length) { console.error('spec must be a non-empty array'); process.exit(1); }

  const requests = jobs.map((j) => {
    if (!j.key) throw new Error('every job needs a unique "key"');
    return { request: buildRequest(j.promptFile, j.image), metadata: { key: j.key } };
  });

  // Inline batches are capped by request size. Fail loudly and early rather
  // than letting the API reject a batch that took minutes to base64-encode.
  const bytes = Buffer.byteLength(JSON.stringify(requests));
  if (bytes > 18 * 1024 * 1024) {
    console.error(`inline batch is ${(bytes / 1e6).toFixed(1)}MB, over the ~20MB ceiling. Split the spec into smaller batches.`);
    process.exit(1);
  }

  const d = await api(`${BASE}/models/${model}:batchGenerateContent?key=${KEY}`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ batch: { display_name: args.name || `batch-${Date.now()}`, input_config: { requests: { requests } } } }),
  });
  const full = PRICE[imageSize] * jobs.length;
  console.log(JSON.stringify({
    ok: true, job: d.name, state: (d.metadata && d.metadata.state) || d.state,
    count: jobs.length, model, tier, imageSize,
    estCostUsd: +(full / 2).toFixed(3), estCostIfInteractiveUsd: +full.toFixed(3),
    payloadMB: +(bytes / 1e6).toFixed(2),
  }));
}

async function batchStatus() {
  if (!args.job) { console.error('need --job'); process.exit(1); }
  const d = await api(`${BASE}/${args.job}?key=${KEY}`);
  console.log(JSON.stringify({ job: d.name, state: (d.metadata && d.metadata.state) || d.state, done: !!d.done }));
}

async function batchCollect() {
  if (!args.job || !args['out-dir']) { console.error('need --job and --out-dir'); process.exit(1); }
  const d = await api(`${BASE}/${args.job}?key=${KEY}`);
  const state = (d.metadata && d.metadata.state) || d.state;
  if (!d.done) { console.log(JSON.stringify({ ok: false, state, note: 'not finished yet' })); return; }

  const dest = d.response || d.metadata || {};
  let entries = ((dest.inlinedResponses || {}).inlinedResponses) || dest.inlined_responses || null;

  // File-backed results (larger batches) come back as a downloadable JSONL.
  if (!entries && (dest.responsesFile || dest.responses_file)) {
    const fileName = dest.responsesFile || dest.responses_file;
    const raw = await api(`${BASE.replace('/v1beta', '')}/download/v1beta/${fileName}:download?alt=media&key=${KEY}`);
    entries = String(raw).split('\n').filter(Boolean).map((l) => JSON.parse(l));
  }
  if (!entries) { console.log(JSON.stringify({ ok: false, state, note: 'no results found on the job object' })); return; }

  const out = [];
  entries.forEach((e, i) => {
    const key = (e.metadata && e.metadata.key) || e.key || `item-${i}`;
    const cand = (((e.response || e).candidates) || [])[0];
    const buf = firstImage(cand);
    if (!buf) { out.push({ key, ok: false, reason: (e.error && e.error.message) || (cand && cand.finishReason) || 'no image' }); return; }
    const file = path.join(args['out-dir'], `${key}.jpg`);
    writeOut(file, buf);
    out.push({ key, ok: true, out: file, bytes: buf.length });
  });
  console.log(JSON.stringify({ ok: true, state, results: out }, null, 2));
}

const commands = { generate, 'batch-submit': batchSubmit, 'batch-status': batchStatus, 'batch-collect': batchCollect };
if (!commands[cmd]) {
  console.error('usage: gemini-image.js <generate|batch-submit|batch-status|batch-collect> [flags]');
  process.exit(1);
}
commands[cmd]().catch((e) => { console.error(String(e.message || e)); process.exit(1); });
