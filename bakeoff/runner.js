const fs = require('fs');
const path = require('path');
const { MODELS } = require('./adapters');

const PHOTO_DIR = path.join(__dirname, 'photos');
const PROMPT_DIR = path.join(__dirname, 'prompts');

function loadPhoto(file) {
  const buf = fs.readFileSync(path.join(PHOTO_DIR, file));
  const dims = require('child_process')
    .execSync(`sips -g pixelWidth -g pixelHeight "${path.join(PHOTO_DIR, file)}"`)
    .toString();
  const width = Number(dims.match(/pixelWidth:\s*(\d+)/)[1]);
  const height = Number(dims.match(/pixelHeight:\s*(\d+)/)[1]);
  return { base64: buf.toString('base64'), mime: 'image/jpeg', width, height };
}

function loadPrompt(caseId, variant) {
  return fs.readFileSync(path.join(PROMPT_DIR, `${caseId}.${variant}.txt`), 'utf8');
}

// One (case × model × prompt-variant) cell. Writes the image to outDir and
// returns a result record. Existing images are reused so a rerun never re-spends.
async function runCell({ caseObj, modelKey, variant, outDir, gptModeration }) {
  const spec = MODELS[modelKey];
  const stem = `${caseObj.id}__${modelKey}__${variant}`;
  const imgPath = path.join(outDir, `${stem}.jpg`);
  const metaPath = path.join(outDir, `${stem}.json`);
  if (fs.existsSync(metaPath)) return JSON.parse(fs.readFileSync(metaPath, 'utf8'));

  const photo = loadPhoto(caseObj.file);
  const prompt = loadPrompt(caseObj.id, variant);
  const res = await spec.run({
    prompt,
    photoBase64: photo.base64,
    photoMime: photo.mime,
    width: photo.width,
    height: photo.height,
    gptModeration,
  });

  const rec = {
    caseId: caseObj.id, modelKey, variant,
    label: spec.label, provider: spec.provider,
    ok: !!res.ok, blocked: !!res.blocked, outOfCredit: !!res.outOfCredit, throttled: !!res.throttled,
    error: res.error || null, latencyMs: res.latencyMs ?? null,
    nominalCost: res.ok ? spec.nominalCost : 0,
    image: res.ok ? path.basename(imgPath) : null,
    meta: res.meta || null,
    ts: new Date().toISOString(),
  };
  if (res.ok) fs.writeFileSync(imgPath, Buffer.from(res.imageBase64, 'base64'));
  fs.writeFileSync(metaPath, JSON.stringify(rec, null, 2));
  return rec;
}

module.exports = { runCell, loadPhoto, loadPrompt };
