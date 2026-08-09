// FREE pre-flight (zero API calls, zero spend). Proves three things before a
// single image is generated:
//
//  1. The prompt files this round reuses are byte-identical to the ones that
//     produced the Dan-labelled baseline images. If this ever drifts, the
//     "control" arm stops being a control.
//  2. Today's production prompt assembly is still the ROUND-5 ERA — i.e. the ab
//     ladder (feb94e0) and the magnitude restore (92c7e77) are genuinely both
//     reverted in public/index.html. If either were live, the baseline images
//     would no longer represent what production ships and the whole comparison
//     would be invalid.
//  3. Seedream's hard 4000-char API ceiling is satisfied by the condensed prompt.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { CASES } = require('./cases');
const { buildSystemPrompt } = require('../prompts');

const R5 = path.join(__dirname, '..', 'round5-prompt-ab');
const PROMPTS = path.join(R5, 'prompts');
const BASELINE_OUT = path.join(R5, 'out');

let fail = 0;
const ck = (ok, msg) => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${msg}`); if (!ok) fail++; };
const sha = (s) => crypto.createHash('sha256').update(s).digest('hex').slice(0, 12);

// ── 1. Prompt files + baseline images are present and paired ────────────────
for (const c of CASES) {
  const full = path.join(PROMPTS, `${c.id}.full.txt`);
  const cond = path.join(PROMPTS, `${c.id}.condensed.txt`);
  ck(fs.existsSync(full), `${c.id}: round-5 full prompt on disk`);
  ck(fs.existsSync(cond), `${c.id}: round-5 condensed prompt on disk`);

  const baselineImg = path.join(BASELINE_OUT, `${c.id}__gemini-2.5-flash-image__full.jpg`);
  const baselineMeta = path.join(BASELINE_OUT, `${c.id}__gemini-2.5-flash-image__full.json`);
  ck(fs.existsSync(baselineImg), `${c.id}: baseline Gemini image exists (free control arm)`);

  // The baseline cell must record the SAME prompt length as the file we reuse —
  // this is the actual link proving the control was generated from these bytes.
  if (fs.existsSync(baselineMeta) && fs.existsSync(full)) {
    const meta = JSON.parse(fs.readFileSync(baselineMeta, 'utf8'));
    const len = fs.readFileSync(full, 'utf8').length;
    ck(meta.ok === true, `${c.id}: baseline cell recorded ok:true`);
    ck(meta.promptChars === len,
      `${c.id}: baseline promptChars ${meta.promptChars} == reused file ${len} (sha ${sha(fs.readFileSync(full, 'utf8'))})`);
  }

  const d = fs.readFileSync(cond, 'utf8');
  ck(d.length <= 4000, `${c.id}: condensed ${d.length} <= 4000 (Seedream hard ceiling)`);
  ck(!d.includes('[[') && !fs.readFileSync(full, 'utf8').includes('[['), `${c.id}: no marker leak`);
}

// ── 2. Today's assembly is still the round-5 era ────────────────────────────
// Deterministic: buildSystemPrompt() runs the real goalSystemPrompt() out of
// public/index.html in a VM. No network, no model, no spend.
// Applies to EVERY male combo:
const ERA_ALL = [
  { needle: 'visibly BIGGER',   want: false, why: 'magnitude restore language must be gone' },
  { needle: 'AB-DEFINITION',    want: false, why: 'ab ladder (feb94e0) must be gone' },
  { needle: 'AB_TABLE',         want: false, why: 'ab ladder markers must be gone' },
  { needle: 'Do NOT add a tan', want: true,  why: 'no-tan rule from 14b4790 is still live (it worked, it stays)' },
];
// Applies only to combos that carry the [[MUSCLE_*]] mass blocks. HEAVIER males
// carry none — muscleAxisPlan() strips them — so the restrained-anchor sentence
// is legitimately absent there. Asserting it everywhere would be asserting a
// falsehood about how the assembler works.
const ERA_MASS = [
  { needle: 'These numbers are deliberately small', want: true, why: 'restrained anchors = round-5 era, restore reverted' },
  { needle: 'If in doubt, add LESS',                want: true, why: 'restrained anchors = round-5 era, restore reverted' },
];
const carriesMass = (c) => c.condition !== 'heavier';

for (const c of CASES) {
  const sys = buildSystemPrompt({ gender: c.gender, condition: c.condition, intensity: c.intensity });
  for (const e of ERA_ALL) {
    ck(sys.includes(e.needle) === e.want, `${c.id}: system prompt ${e.want ? 'HAS' : 'lacks'} "${e.needle}" — ${e.why}`);
  }
  for (const e of ERA_MASS) {
    const want = carriesMass(c) ? e.want : false;
    ck(sys.includes(e.needle) === want,
      `${c.id}: system prompt ${want ? 'HAS' : 'lacks'} "${e.needle}" — ${carriesMass(c) ? e.why : 'heavier males carry no [[MUSCLE_*]] blocks'}`);
  }
}

console.log(fail ? `\n${fail} FAILURES — do not spend` : '\nall pre-flight assertions passed — safe to spend');
process.exitCode = fail ? 1 : 0;
