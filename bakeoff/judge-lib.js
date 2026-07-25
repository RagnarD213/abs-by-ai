// Shared plumbing for the Phase-3 judge evaluation.
//
// Loads Dan's ground-truth labels + the blind key, resolves each labeled letter
// to its image file, and provides a cached Anthropic vision call. Test-only —
// nothing here is imported by the server.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');

const ROUND1 = path.join(__dirname, 'round1');
const IMAGES = path.join(ROUND1, 'images');
const PHOTOS = path.join(ROUND1, 'photos');
const CACHE = path.join(ROUND1, 'judge-cache');
const SCALED = path.join(ROUND1, 'scaled');

for (const d of [CACHE, SCALED]) if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });

// bakeoff/.env → process.env (same convention as the rest of the harness)
for (const line of fs.readFileSync(path.join(__dirname, '.env'), 'utf8').split('\n')) {
  const m = line.match(/^([A-Z_]+)=(.*)$/);
  if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
}

const { PHOTOS: PHOTO_SPECS } = require('./cases');

const labels = JSON.parse(fs.readFileSync(path.join(ROUND1, 'labels.json'), 'utf8'));
const key = JSON.parse(fs.readFileSync(path.join(ROUND1, 'key.json'), 'utf8'));

// ── cases ────────────────────────────────────────────────────────────────────
// Group the labeled letters into cases, decode each letter → model/variant →
// image file, and record which letter Dan marked best.
function buildCases() {
  const byCase = new Map();
  for (const [k, label] of Object.entries(labels)) {
    const [caseId, letter] = k.split(':');
    const meta = key[k];
    if (!meta) throw new Error(`No key entry for ${k}`);
    const file = path.join(IMAGES, `${caseId}__${meta.model}__${meta.variant}.jpg`);
    if (!fs.existsSync(file)) throw new Error(`Missing image for ${k}: ${file}`);
    if (!byCase.has(caseId)) {
      const photoKey = caseId.split('__')[0];
      byCase.set(caseId, {
        caseId,
        photoKey,
        intensity: caseId.split('__')[1],
        photoFile: path.join(PHOTOS, PHOTO_SPECS[photoKey].file),
        gender: PHOTO_SPECS[photoKey].gender,
        condition: PHOTO_SPECS[photoKey].condition,
        candidates: [],
        best: null,
      });
    }
    const c = byCase.get(caseId);
    const cand = {
      letter, caseId, model: meta.model, variant: meta.variant, file,
      best: !!label.best, acceptable: !!label.acceptable,
      tags: label.tags || [], note: label.note || '',
    };
    c.candidates.push(cand);
    if (cand.best) c.best = cand;
  }
  for (const c of byCase.values()) c.candidates.sort((a, b) => a.letter.localeCompare(b.letter));
  return [...byCase.values()];
}

// ── images ───────────────────────────────────────────────────────────────────
// Anthropic downscales anything over 1568px on the long edge server-side, so
// pre-scaling to 1568 is lossless in token terms and keeps uploads small.
const MAX_EDGE = 1568;
function scaledPath(file, maxEdge = MAX_EDGE) {
  const out = path.join(SCALED, crypto.createHash('sha1').update(`${file}|${maxEdge}`).digest('hex').slice(0, 16) + '.jpg');
  if (!fs.existsSync(out)) {
    execFileSync('sips', ['-Z', String(maxEdge), '-s', 'format', 'jpeg', file, '--out', out], { stdio: 'ignore' });
  }
  return out;
}

const b64cache = new Map();
function imageBlock(file, maxEdge = MAX_EDGE) {
  const k = `${file}|${maxEdge}`;
  if (!b64cache.has(k)) {
    b64cache.set(k, fs.readFileSync(scaledPath(file, maxEdge)).toString('base64'));
  }
  return { type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: b64cache.get(k) } };
}

// ── Anthropic call (disk-cached, so reruns of an unchanged judge are free) ────
async function anthropic({ model, maxTokens, content, cacheKey, system }) {
  const hash = crypto.createHash('sha256').update(cacheKey).digest('hex').slice(0, 32);
  const cacheFile = path.join(CACHE, `${hash}.json`);
  if (fs.existsSync(cacheFile)) return JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
  // CACHE_ONLY=1 scores whatever is already on disk without spending anything —
  // used to salvage a partial run (e.g. the account ran out of credit).
  if (process.env.CACHE_ONLY === '1') return { text: '', usage: null, __miss: true };

  const body = { model, max_tokens: maxTokens, messages: [{ role: 'user', content }] };
  if (system) body.system = system;
  // NOTE: never pass temperature/top_p/top_k — Claude 5 family hard-400s.

  let lastErr = null;
  for (let attempt = 0; attempt < 4; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 180000);
    try {
      const res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': process.env.ANTHROPIC_API_KEY,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });
      const data = await res.json();
      if (!res.ok) {
        lastErr = `${res.status} ${data?.error?.message || ''}`;
        if (res.status === 429 || res.status >= 500) {
          await new Promise((r) => setTimeout(r, 3000 * (attempt + 1)));
          continue;
        }
        throw new Error(lastErr);
      }
      const text = (data.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('\n');
      const out = { text, usage: data.usage };
      fs.writeFileSync(cacheFile, JSON.stringify(out));
      return out;
    } catch (e) {
      lastErr = e.message;
      if (attempt === 3) throw e;
      await new Promise((r) => setTimeout(r, 3000 * (attempt + 1)));
    } finally {
      clearTimeout(timer);
    }
  }
  throw new Error(lastErr);
}

function parseJson(text) {
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) return null;
  try { return JSON.parse(m[0]); } catch { return null; }
}

// Bounded-concurrency map.
async function pmap(items, limit, fn) {
  const out = new Array(items.length);
  let i = 0;
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (i < items.length) {
      const idx = i++;
      out[idx] = await fn(items[idx], idx);
    }
  }));
  return out;
}

module.exports = { buildCases, imageBlock, anthropic, parseJson, pmap, labels, key, ROUND1 };
