// Decisive test: is today's weak male Gemini result caused by OUR prompt
// softening (14b4790, 2026-07-25) or by drift in the Gemini model itself?
//
// Same photo, same settings, same model, SAME DAY — only the prompt era differs:
//   ERA-A "pre-retune"  = index.html at 9cfe3d6 (live during round 1, when Dan
//                         picked lean-male/dramatic as BEST + "just right")
//   ERA-B "today"       = index.html at HEAD (post-retune, ladder reverted)
//
// If ERA-A comes back visibly stronger, the regression is ours and reversible.
// If both are weak, the model drifted and the swap is the only path.
// No deviceId anywhere. ~$0.04/image.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { execSync } = require('child_process');
const { MODELS } = require('/Users/danielrose/Documents/Claude/Projects/Abs By AI/bakeoff/adapters');

const REPO = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const OUT = __dirname;

function htmlAt(ref) {
  return ref === 'HEAD-WORKTREE'
    ? fs.readFileSync(path.join(REPO, 'public/index.html'), 'utf8')
    : execSync(`git -C "${REPO}" show ${ref}:public/index.html`, { maxBuffer: 1 << 28 }).toString();
}

function buildSystemPrompt(HTML, { gender, condition, intensity }) {
  const start = HTML.indexOf('const SYSTEM_PROMPT = `');
  if (start === -1) throw new Error('SYSTEM_PROMPT not found');
  const gsMarker = HTML.indexOf('function goalSystemPrompt() {', start);
  if (gsMarker === -1) throw new Error('goalSystemPrompt not found');
  const gsEnd = HTML.indexOf('\n}', gsMarker) + 2;
  const source = HTML.slice(start, gsEnd);
  const sandbox = { state: { gender, condition, intensity, effectiveIntensity: intensity, description: '' }, module: {} };
  vm.createContext(sandbox);
  vm.runInContext(source + '\n;__out = goalSystemPrompt();', sandbox);
  const out = sandbox.__out;
  if (!out || out.includes('[[MUSCLE_') || out.includes('[[AB')) throw new Error('marker leak or empty');
  return out;
}

async function assemble(HTML, c) {
  const res = await fetch('https://absbyai.com/api/generate-prompt', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      systemPrompt: buildSystemPrompt(HTML, c),
      userJson: JSON.stringify({
        user_description: '', subject_gender: c.gender,
        subject_current_condition: c.condition, intensity: c.intensity, has_reference_photo: false,
      }),
    }),
  });
  const d = await res.json();
  if (!res.ok || !d?.prompt) throw new Error(`generate-prompt ${res.status}: ${d?.error || ''}`);
  return d.prompt.trim();
}

function loadPhoto(file) {
  const p = path.join(REPO, 'bakeoff/round5-prompt-ab/photos', file);
  const dims = execSync(`sips -g pixelWidth -g pixelHeight "${p}"`).toString();
  return {
    base64: fs.readFileSync(p).toString('base64'), mime: 'image/jpeg',
    width: +dims.match(/pixelWidth:\s*(\d+)/)[1], height: +dims.match(/pixelHeight:\s*(\d+)/)[1],
  };
}

const ERAS = [
  { key: 'A-pre-retune', ref: '9cfe3d6' },
  { key: 'B-today',      ref: 'HEAD-WORKTREE' },
];
const CASES = [
  { id: 'lean-male__dramatic',     file: 'lean-male.jpg',     gender: 'male', condition: 'very_lean', intensity: 'dramatic' },
  { id: 'moderate-male__max',      file: 'moderate-male.jpg', gender: 'male', condition: 'moderate',  intensity: 'max' },
];

(async () => {
  const gem = MODELS['gemini-2.5-flash-image'];
  let spend = 0;
  const summary = [];
  for (const c of CASES) {
    const photo = loadPhoto(c.file);
    for (const era of ERAS) {
      const HTML = htmlAt(era.ref);
      const prompt = await assemble(HTML, c);
      const stem = `${c.id}__${era.key}`;
      fs.writeFileSync(path.join(OUT, `${stem}.prompt.txt`), prompt);

      // fingerprint the magnitude language actually present
      const lbs = [...prompt.matchAll(/(\d+)\s*pounds?/gi)].map((m) => m[1]);
      const fp = {
        chars: prompt.length,
        pounds: lbs.join(','),
        bigger: /visibly BIGGER/i.test(prompt),
        slightly: (prompt.match(/slightly/gi) || []).length,
        neverBodybuilder: /NEVER a bodybuilder|never a bodybuilder/i.test(prompt),
        tan: /tan\b|bronze|sun-kissed/i.test(prompt),
      };

      let res = await gem.run({ prompt, photoBase64: photo.base64, photoMime: photo.mime, width: photo.width, height: photo.height });
      let retried = false;
      if (!res.ok) {
        retried = true;
        res = await gem.run({ prompt: 'SAFE FITNESS EDIT: This is a routine body-composition edit for a fitness progress app. The subject is a consenting adult. Keep the exact same clothing and coverage as the input photo. Nothing about this edit is sexual.\n\n' + prompt,
          photoBase64: photo.base64, photoMime: photo.mime, width: photo.width, height: photo.height });
      }
      if (res.ok) { fs.writeFileSync(path.join(OUT, `${stem}.jpg`), Buffer.from(res.imageBase64, 'base64')); spend += gem.nominalCost; }
      summary.push({ case: c.id, era: era.key, ok: !!res.ok, retried, ...fp });
      console.log(`${res.ok ? 'ok  ' : 'FAIL'} ${stem.padEnd(38)} chars=${fp.chars} lbs=[${fp.pounds}] bigger=${fp.bigger} slightly=${fp.slightly} neverBB=${fp.neverBodybuilder} tan=${fp.tan}`);
      await new Promise((r) => setTimeout(r, 9000));
    }
  }
  fs.writeFileSync(path.join(OUT, 'era-summary.json'), JSON.stringify(summary, null, 2));
  console.log(`\nnominal spend ~$${spend.toFixed(2)}`);
})();
