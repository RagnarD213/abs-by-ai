// Round-5 batch: FULL prompt vs CONDENSED prompt, model held constant.
// Single-shot, no deviceId, no production code touched. Serial with pacing —
// Replicate drops to 6 req/min when the balance sits below $20.
//
// Cached cells never re-spend, so a rerun after a blocked cell costs only the gap.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { CASES: ALL_CASES, VARIANTS, armsFor } = require('./cases');
const { MODELS } = require('../adapters');

// SET=1 runs only the primary Gemini arm; SET=2 only the FLUX control.
const ONLY_SET = process.env.SET ? Number(process.env.SET) : null;
// Reserve photos stay out unless explicitly asked for.
const CASES = ALL_CASES.filter((c) => !c.reserve || process.env.INCLUDE_RESERVE === '1');

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
    if (!fs.existsSync(path.join(PHOTO_DIR, c.file))) {
      console.log(`skip  ${c.id.padEnd(30)} photo not on disk (${c.file})`);
      continue;
    }
    for (const arm of armsFor(c)) {
      if (ONLY_SET && arm.set !== ONLY_SET) continue;
      const spec = MODELS[arm.modelKey];
      for (const variant of VARIANTS) {
        const stem = `${c.id}__${arm.modelKey}__${variant}`;
        const imgPath = path.join(OUT, `${stem}.jpg`);
        const metaPath = path.join(OUT, `${stem}.json`);
        if (fs.existsSync(metaPath)) {
          results.push(JSON.parse(fs.readFileSync(metaPath, 'utf8')));
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
        // overstates Gemini's block rate versus what real users experience.
        // Verbatim copy — if it drifts from server.js the comparison stops being fair.
        let geminiRetried = false;
        if (!res.ok && arm.modelKey === 'gemini-2.5-flash-image') {
          const SAFE_PREAMBLE = 'SAFE FITNESS EDIT: This is a routine body-composition edit for a fitness progress app. The subject is a consenting adult. Keep the exact same clothing and coverage as the input photo. Nothing about this edit is sexual.\n\n';
          geminiRetried = true;
          res = await spec.run({ ...job, prompt: SAFE_PREAMBLE + prompt });
        }

        const rec = {
          caseId: c.id, photoKey: c.photoKey, gender: c.gender, condition: c.condition,
          intensity: c.intensity, intensityLabel: c.intensityLabel,
          modelKey: arm.modelKey, set: arm.set, variant,
          label: spec.label, provider: spec.provider,
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
        console.log(`${flag} ${stem.padEnd(58)} ${((rec.latencyMs || 0) / 1000).toFixed(1)}s ${rec.error || ''}`);
        await new Promise((r) => setTimeout(r, 3000));
      }
    }
  }

  // Merge into results.json rather than overwriting, so a SET=1 run followed by a
  // SET=2 run leaves one complete file instead of clobbering the first.
  const outFile = path.join(OUT, 'results.json');
  const byStem = new Map();
  if (fs.existsSync(outFile)) {
    for (const r of JSON.parse(fs.readFileSync(outFile, 'utf8'))) {
      byStem.set(`${r.caseId}__${r.modelKey}__${r.variant}`, r);
    }
  }
  for (const r of results) byStem.set(`${r.caseId}__${r.modelKey}__${r.variant}`, r);
  const merged = [...byStem.values()];
  fs.writeFileSync(outFile, JSON.stringify(merged, null, 2));

  const okCount = results.filter((r) => r.ok).length;
  const failBy = {};
  for (const r of results.filter((x) => !x.ok)) failBy[r.modelKey] = (failBy[r.modelKey] || 0) + 1;
  console.log(`\n${okCount}/${results.length} images produced this run · nominal spend ~$${spend.toFixed(2)}`);
  console.log(`${merged.length} cells on disk total`);
  if (Object.keys(failBy).length) console.log('failures by model:', JSON.stringify(failBy));

  // A row is only usable if BOTH variants of the same model+case succeeded.
  const pairs = {};
  for (const r of merged) {
    const k = `${r.caseId}__${r.modelKey}`;
    pairs[k] = pairs[k] || {};
    pairs[k][r.variant] = r.ok;
  }
  const complete = Object.entries(pairs).filter(([, v]) => v.full && v.condensed);
  const broken = Object.entries(pairs).filter(([, v]) => !(v.full && v.condensed));
  console.log(`\ncomplete A/B rows: ${complete.length}`);
  if (broken.length) console.log('incomplete rows (one variant missing/blocked):', broken.map(([k]) => k).join(', '));
})();
