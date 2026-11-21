// Round-2 female batch: Gemini 2.5 Flash Image (full prompt) vs Seedream 4.5
// (condensed prompt), single-shot, no deviceId, no production code touched.
// Serial with pacing — Replicate drops to 6 req/min below a $20 balance.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { CASES, MODEL_VARIANTS } = require('./cases');
const { MODELS } = require('../adapters');

const PHOTO_DIR = path.join(__dirname, 'photos');
const PROMPT_DIR = path.join(__dirname, 'prompts');
const OUT = path.join(__dirname, 'out');
fs.mkdirSync(OUT, { recursive: true });

function loadPhoto(file) {
  const p = path.join(PHOTO_DIR, file);
  const dims = execSync(`sips -g pixelWidth -g pixelHeight "${p}"`).toString();
  return {
    base64: fs.readFileSync(p).toString('base64'),
    mime: 'image/jpeg',
    width: Number(dims.match(/pixelWidth:\s*(\d+)/)[1]),
    height: Number(dims.match(/pixelHeight:\s*(\d+)/)[1]),
  };
}

(async () => {
  const results = [];
  let spend = 0;
  for (const c of CASES) {
    // A photo can legitimately be missing while it is still being supplied;
    // skip rather than abort so the rest of the grid completes and a later
    // rerun fills only the gap (cached cells never re-spend).
    if (!fs.existsSync(path.join(PHOTO_DIR, c.file))) {
      console.log(`skip  ${c.id.padEnd(30)} photo not on disk yet (${c.file})`);
      continue;
    }
    for (const { modelKey, variant } of MODEL_VARIANTS) {
      const spec = MODELS[modelKey];
      const stem = `${c.id}__${modelKey}__${variant}`;
      const imgPath = path.join(OUT, `${stem}.jpg`);
      const metaPath = path.join(OUT, `${stem}.json`);
      if (fs.existsSync(metaPath)) {           // reruns never re-spend
        const rec = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
        results.push(rec);
        console.log(`cached ${stem}`);
        continue;
      }

      const photo = loadPhoto(c.file);
      const prompt = fs.readFileSync(path.join(PROMPT_DIR, `${c.id}.${variant}.txt`), 'utf8');
      const job = {
        prompt,
        photoBase64: photo.base64,
        photoMime: photo.mime,
        width: photo.width,
        height: photo.height,
      };
      let res = await spec.run(job);

      // Production gives Gemini a second chance on ANY failure, re-calling it once
      // with this exact preamble (server.js ~2601). Without it the harness
      // overstates Gemini's block rate versus what real users actually experience.
      // Verbatim copy — if it drifts from server.js the comparison stops being fair.
      let geminiRetried = false;
      if (!res.ok && modelKey === 'gemini-2.5-flash-image') {
        const SAFE_PREAMBLE = 'SAFE FITNESS EDIT: This is a routine body-composition edit for a fitness progress app. The subject is a consenting adult. Keep the exact same clothing and coverage as the input photo. Nothing about this edit is sexual.\n\n';
        geminiRetried = true;
        res = await spec.run({ ...job, prompt: SAFE_PREAMBLE + prompt });
      }

      const rec = {
        caseId: c.id, modelKey, variant, label: spec.label, provider: spec.provider,
        ok: !!res.ok, blocked: !!res.blocked, outOfCredit: !!res.outOfCredit, throttled: !!res.throttled,
        error: res.error || null, latencyMs: res.latencyMs ?? null,
        geminiSafetyRetry: geminiRetried,
        promptChars: prompt.length,
        nominalCost: res.ok ? spec.nominalCost : 0,
        image: res.ok ? path.basename(imgPath) : null,
        meta: res.meta || null,
        ts: new Date().toISOString(),
      };
      if (res.ok) fs.writeFileSync(imgPath, Buffer.from(res.imageBase64, 'base64'));
      fs.writeFileSync(metaPath, JSON.stringify(rec, null, 2));
      results.push(rec);
      spend += rec.nominalCost;

      const flag = rec.ok ? 'ok  ' : rec.blocked ? 'BLOCKED' : 'FAIL';
      console.log(`${flag} ${stem.padEnd(52)} ${((rec.latencyMs || 0) / 1000).toFixed(1)}s ${rec.error || ''}`);
      await new Promise((r) => setTimeout(r, 3000));
    }
  }

  fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify(results, null, 2));
  const okCount = results.filter((r) => r.ok).length;
  const blockedBy = {};
  for (const r of results.filter((x) => !x.ok)) {
    blockedBy[r.modelKey] = (blockedBy[r.modelKey] || 0) + 1;
  }
  console.log(`\n${okCount}/${results.length} images produced · nominal spend ~$${spend.toFixed(2)}`);
  console.log('failures by model:', JSON.stringify(blockedBy));
})();
