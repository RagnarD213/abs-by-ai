// Round-8 batch: generate the CHALLENGER arms only.
//
// The baseline arm (gemini-2.5-flash-image) is NEVER generated here — its images
// already exist and are already Dan-labelled in ../round5-prompt-ab/out. That arm
// costs $0. See cases.js.
//
// No deviceId is sent on any call — these hit the providers directly, never
// /api/generate-image, so no user credits are spent and no data-file commit
// triggers a Railway redeploy.
//
// MODEL=<key> runs one arm. DRY=1 prints the plan and the cost estimate without
// calling anything.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { CASES, CHALLENGERS } = require('./cases');
const { MODELS } = require('../adapters');

const ONLY_MODEL = process.env.MODEL || null;
const DRY = !!process.env.DRY;
const PHOTO_DIR = path.join(__dirname, '..', 'round5-prompt-ab', 'photos');
const PROMPT_DIR = path.join(__dirname, '..', 'round5-prompt-ab', 'prompts');
const OUT = path.join(__dirname, 'out');
fs.mkdirSync(OUT, { recursive: true });

// Production's Gemini safety-retry preamble, verbatim from server.js. Applied to
// any Google-family candidate, because a model taking the ANCHOR slot inherits
// the anchor's retry behaviour. Whether a candidate NEEDS this retry is itself a
// measurement — bar (b) is "no increase in moderation blocks vs Gemini".
const SAFE_PREAMBLE = 'SAFE FITNESS EDIT: This is a routine body-composition edit for a fitness progress app. The subject is a consenting adult. Keep the exact same clothing and coverage as the input photo. Nothing about this edit is sexual.\n\n';

function loadPhoto(file) {
  const p = path.join(PHOTO_DIR, file);
  const dims = execSync(`sips -g pixelWidth -g pixelHeight "${p}"`).toString();
  return {
    base64: fs.readFileSync(p).toString('base64'), mime: 'image/jpeg',
    width: Number(dims.match(/pixelWidth:\s*(\d+)/)[1]),
    height: Number(dims.match(/pixelHeight:\s*(\d+)/)[1]),
  };
}

// ── The round-6/7 caching bug, fixed ────────────────────────────────────────
// The old check was `if (fs.existsSync(metaPath))`. A FAILED cell writes a
// {ok:false} record, so after a provider outage a re-run reported "cached" for
// every failure and generated nothing — this silently cost a whole re-run during
// the 2026-08-07 Gemini credit outage. A cell now counts as cached only if the
// record parses, ok is true, AND the image is actually on disk. Anything else is
// deleted and regenerated.
function isCached(metaPath, imgPath) {
  if (!fs.existsSync(metaPath)) return false;
  let rec;
  try { rec = JSON.parse(fs.readFileSync(metaPath, 'utf8')); }
  catch { fs.rmSync(metaPath, { force: true }); return false; }
  if (rec.ok !== true || !fs.existsSync(imgPath)) {
    fs.rmSync(metaPath, { force: true });
    fs.rmSync(imgPath, { force: true });
    return false;
  }
  return true;
}

(async () => {
  const arms = CHALLENGERS.filter((a) => !ONLY_MODEL || a.modelKey === ONLY_MODEL);
  if (!arms.length) throw new Error(`no challenger arm matches MODEL=${ONLY_MODEL}`);

  // Cost estimate up front, always printed before anything is called.
  let planned = 0, est = 0;
  for (const c of CASES) {
    for (const arm of arms) {
      const stem = `${c.id}__${arm.modelKey}`;
      if (isCached(path.join(OUT, `${stem}.json`), path.join(OUT, `${stem}.jpg`))) continue;
      planned++; est += MODELS[arm.modelKey].nominalCost;
    }
  }
  console.log(`plan: ${planned} images to generate across ${arms.length} arm(s) · nominal estimate ~$${est.toFixed(2)}`);
  console.log(`baseline arm (gemini-2.5-flash-image): reused from round-5, $0.00\n`);
  if (DRY) return;

  let spend = 0, ok = 0, total = 0;
  const blocks = {};
  for (const c of CASES) {
    for (const arm of arms) {
      total++;
      const spec = MODELS[arm.modelKey];
      const stem = `${c.id}__${arm.modelKey}`;
      const imgPath = path.join(OUT, `${stem}.jpg`);
      const metaPath = path.join(OUT, `${stem}.json`);
      if (isCached(metaPath, imgPath)) { console.log('cached', stem); ok++; continue; }

      const photo = loadPhoto(c.file);
      const prompt = fs.readFileSync(path.join(PROMPT_DIR, `${c.id}.${arm.variant}.txt`), 'utf8');
      const job = { prompt, photoBase64: photo.base64, photoMime: photo.mime, width: photo.width, height: photo.height };

      let res = await spec.run(job);
      let safetyRetry = false;
      const firstBlocked = !!res.blocked;
      if (!res.ok && spec.provider === 'google') {
        safetyRetry = true;
        await new Promise((r) => setTimeout(r, 2000));
        res = await spec.run({ ...job, prompt: SAFE_PREAMBLE + prompt });
      }

      const rec = {
        caseId: c.id, photoKey: c.photoKey, gender: c.gender, condition: c.condition,
        intensity: c.intensity, intensityLabel: c.intensityLabel,
        modelKey: arm.modelKey, modelLabel: arm.label, variant: arm.variant, arm: 'challenger',
        ok: !!res.ok, blocked: !!res.blocked, firstAttemptBlocked: firstBlocked,
        error: res.error || null, latencyMs: res.latencyMs ?? null, safetyRetry,
        promptChars: prompt.length, nominalCost: res.ok ? spec.nominalCost : 0,
        image: res.ok ? path.basename(imgPath) : null, ts: new Date().toISOString(),
      };
      if (res.ok) { fs.writeFileSync(imgPath, Buffer.from(res.imageBase64, 'base64')); ok++; }
      fs.writeFileSync(metaPath, JSON.stringify(rec, null, 2));
      spend += rec.nominalCost;
      const b = (blocks[arm.modelKey] = blocks[arm.modelKey] || { blocked: 0, retried: 0, n: 0, ms: [] });
      b.n++; if (rec.blocked) b.blocked++; if (safetyRetry) b.retried++;
      if (rec.latencyMs) b.ms.push(rec.latencyMs);

      console.log(`${res.ok ? 'ok  ' : res.blocked ? 'BLOCKED' : 'FAIL'} ${stem.padEnd(46)} ${((rec.latencyMs || 0) / 1000).toFixed(1)}s${safetyRetry ? ' [safety-retry]' : ''} ${rec.error || ''}`);
      await new Promise((r) => setTimeout(r, 3000));
    }
  }

  console.log(`\n${ok}/${total} challenger cells ok · nominal spend this run ~$${spend.toFixed(2)}`);
  // Bars (b) and (c) are measured here, not eyeballed later.
  for (const [k, b] of Object.entries(blocks)) {
    const med = b.ms.length ? [...b.ms].sort((x, y) => x - y)[Math.floor(b.ms.length / 2)] / 1000 : 0;
    console.log(`  ${k.padEnd(26)} blocks ${b.blocked}/${b.n} · safety-retries ${b.retried}/${b.n} · median ${med.toFixed(1)}s`);
  }
})();
