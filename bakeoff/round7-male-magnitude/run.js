// Round 7: does restoring the male muscle magnitude fix Gemini's under-change?
//
//   arm "current"  = today's production prompt (post-revert HEAD)
//   arm "restored" = today's prompt with the pre-retune male magnitude blocks
//                    spliced back in (see patch.js)
//
// BOTH arms are generated TODAY, on the same model, rather than reusing the
// round-5/6 images. Gemini is stochastic and may itself have drifted, so
// regenerating both arms removes date and model-version as confounds — worth
// the extra ~$0.23.
//
// Gemini only. No deviceId, ever. A failed cell is NOT treated as cached
// (the round-6 bug: a re-run after an outage silently generated nothing).
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execSync } = require('child_process');
const { MODELS } = require('../adapters');
const { buildRestoredHtml, verify } = require('./patch');

const REPO = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const PHOTO_DIR = path.join(REPO, 'bakeoff/round5-prompt-ab/photos');
const OUT = path.join(__dirname, 'out');
fs.mkdirSync(OUT, { recursive: true });

const CASES = [
  { id: 'lean-male__dramatic',     file: 'lean-male.jpg',     condition: 'very_lean', intensity: 'dramatic', label: 'Subtle', desc: 'Lean athletic male — the case Dan tagged "just right" in round 1 and rejected in round 6' },
  { id: 'lean-male__max',          file: 'lean-male.jpg',     condition: 'very_lean', intensity: 'max',      label: 'Ripped', desc: 'Lean athletic male' },
  { id: 'moderate-male__dramatic', file: 'moderate-male.jpg', condition: 'moderate',  intensity: 'dramatic', label: 'Subtle', desc: 'Average male — the modal user' },
  { id: 'moderate-male__max',      file: 'moderate-male.jpg', condition: 'moderate',  intensity: 'max',      label: 'Ripped', desc: 'Average male — today\'s prompt carries NO pounds figure at all on this path' },
  { id: 'heavier-male__dramatic',  file: 'heavier-male.jpg',  condition: 'heavier',   intensity: 'dramatic', label: 'Subtle', desc: 'Heavier male' },
  { id: 'heavier-male__max',       file: 'heavier-male.jpg',  condition: 'heavier',   intensity: 'max',      label: 'Ripped', desc: 'Heavier male' },
];

function buildSystemPrompt(HTML, c) {
  const start = HTML.indexOf('const SYSTEM_PROMPT = `');
  const gsMarker = HTML.indexOf('function goalSystemPrompt() {', start);
  const gsEnd = HTML.indexOf('\n}', gsMarker) + 2;
  const source = HTML.slice(start, gsEnd);
  const sandbox = { state: { gender: 'male', condition: c.condition, intensity: c.intensity, effectiveIntensity: c.intensity, description: '' }, module: {} };
  vm.createContext(sandbox);
  vm.runInContext(source + '\n;__out = goalSystemPrompt();', sandbox);
  const out = sandbox.__out;
  if (!out) throw new Error('empty prompt');
  if (/\[\[[A-Z_]+\]\]|\[\[MUSCLE_/.test(out)) throw new Error(`marker leak in ${c.id}`);
  return out;
}

async function assemble(HTML, c) {
  const res = await fetch('https://absbyai.com/api/generate-prompt', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      systemPrompt: buildSystemPrompt(HTML, c),
      userJson: JSON.stringify({ user_description: '', subject_gender: 'male', subject_current_condition: c.condition, intensity: c.intensity, has_reference_photo: false }),
    }),
  });
  const d = await res.json();
  if (!res.ok || !d?.prompt) throw new Error(`generate-prompt ${res.status}: ${d?.error || ''}`);
  return d.prompt.trim();
}

function loadPhoto(file) {
  const p = path.join(PHOTO_DIR, file);
  const dims = execSync(`sips -g pixelWidth -g pixelHeight "${p}"`).toString();
  return { base64: fs.readFileSync(p).toString('base64'), mime: 'image/jpeg',
    width: +dims.match(/pixelWidth:\s*(\d+)/)[1], height: +dims.match(/pixelHeight:\s*(\d+)/)[1] };
}

const SAFE = 'SAFE FITNESS EDIT: This is a routine body-composition edit for a fitness progress app. The subject is a consenting adult. Keep the exact same clothing and coverage as the input photo. Nothing about this edit is sexual.\n\n';

(async () => {
  const restored = buildRestoredHtml();
  const vfail = verify(restored.html);
  if (vfail.length) { console.error('PATCH VERIFY FAILED:\n  ' + vfail.join('\n  ')); process.exit(1); }
  const ARMS = [
    { key: 'current',  html: fs.readFileSync(path.join(REPO, 'public/index.html'), 'utf8') },
    { key: 'restored', html: restored.html },
  ];

  const gem = MODELS['gemini-2.5-flash-image'];
  let spend = 0, ok = 0, total = 0;

  // Build + assert every prompt BEFORE generating anything.
  const prompts = {};
  for (const c of CASES) {
    for (const arm of ARMS) {
      const f = path.join(__dirname, 'prompts', `${c.id}.${arm.key}.txt`);
      fs.mkdirSync(path.dirname(f), { recursive: true });
      if (!fs.existsSync(f)) {
        fs.writeFileSync(f, await assemble(arm.html, c));
        await new Promise((r) => setTimeout(r, 8000));
      }
      prompts[`${c.id}.${arm.key}`] = fs.readFileSync(f, 'utf8');
    }
    const cur = prompts[`${c.id}.current`], res = prompts[`${c.id}.restored`];
    const lbs = (s) => [...s.matchAll(/(\d+)\s*pounds?/gi)].map((m) => +m[1]);
    const slight = (s) => (s.match(/slightly/gi) || []).length;
    console.log(`${c.id.padEnd(26)} current: lbs=[${lbs(cur)}] slightly=${slight(cur)} | restored: lbs=[${lbs(res)}] slightly=${slight(res)}`);
    if (cur === res) throw new Error(`${c.id}: arms are IDENTICAL — the patch did not reach the assembled prompt`);
  }

  for (const c of CASES) {
    const photo = loadPhoto(c.file);
    for (const arm of ARMS) {
      total++;
      const stem = `${c.id}__${arm.key}`;
      const imgPath = path.join(OUT, `${stem}.jpg`);
      const metaPath = path.join(OUT, `${stem}.json`);
      if (fs.existsSync(metaPath)) {
        const prev = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
        if (prev.ok) { console.log('cached', stem); ok++; continue; }
        fs.unlinkSync(metaPath); // round-6 lesson: never treat a failure as cached
      }
      const prompt = prompts[`${c.id}.${arm.key}`];
      let res = await gem.run({ prompt, photoBase64: photo.base64, photoMime: photo.mime, width: photo.width, height: photo.height });
      let retried = false;
      if (!res.ok) { retried = true; res = await gem.run({ prompt: SAFE + prompt, photoBase64: photo.base64, photoMime: photo.mime, width: photo.width, height: photo.height }); }
      if (res.ok) { fs.writeFileSync(imgPath, Buffer.from(res.imageBase64, 'base64')); ok++; spend += gem.nominalCost; }
      fs.writeFileSync(metaPath, JSON.stringify({
        caseId: c.id, arm: arm.key, condition: c.condition, intensity: c.intensity, intensityLabel: c.label,
        desc: c.desc, ok: !!res.ok, blocked: !!res.blocked, error: res.error || null,
        latencyMs: res.latencyMs ?? null, safetyRetry: retried, promptChars: prompt.length,
        image: res.ok ? path.basename(imgPath) : null, ts: new Date().toISOString(),
      }, null, 2));
      console.log(`${res.ok ? 'ok  ' : 'FAIL'} ${stem.padEnd(38)} ${((res.latencyMs || 0) / 1000).toFixed(1)}s ${res.error || ''}`);
      await new Promise((r) => setTimeout(r, 3000));
    }
  }
  console.log(`\n${ok}/${total} cells ok · nominal spend this run ~$${spend.toFixed(2)}`);
})();
