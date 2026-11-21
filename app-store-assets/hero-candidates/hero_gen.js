// Reproduces the Abs by AI client's real prompt assembly, then drives the live
// production endpoints exactly as the app does:
//   goalSystemPrompt() -> /api/generate-prompt -> /api/generate-image
// No hand-written prompts: the SYSTEM_PROMPT is lifted verbatim from public/index.html.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const OUT = __dirname;
const html = fs.readFileSync(path.join(ROOT, 'public/index.html'), 'utf8');

function extractTemplate(varName) {
  const start = html.indexOf(`const ${varName} = \``);
  if (start === -1) throw new Error(`${varName} not found`);
  const from = start + `const ${varName} = \``.length;
  const end = html.indexOf('`;', from);
  if (end === -1) throw new Error(`${varName} terminator not found`);
  return html.slice(from, end);
}

const SYSTEM_PROMPT = extractTemplate('SYSTEM_PROMPT');

// The GOAL_SYSTEM_PROMPT .replace() pair, lifted from index.html:3023.
const CAL_FIND = `CALIBRATION RULE — only for "heavier" starting condition
If subject_current_condition is "heavier" AND intensity is "dramatic" or "max": DOWNGRADE the body-fat target by one step (use "moderate" anchors), and add to the directive: "This is a believable mid-journey transformation — the subject should look noticeably leaner and fitter, but not yet at peak condition."
All other starting conditions (moderate, fit, very_lean): honor the requested intensity at full strength. Do NOT downgrade fit or lean subjects.`;
const CAL_REPL = `CALIBRATION RULE — DISABLED FOR THIS PROMPT
Always honor the user's requested intensity at FULL strength regardless of starting condition. Do NOT downgrade. This is the "Goal Vision" — show exactly what the user asked for. (EXCEPTION: a heavier FEMALE subject still follows the FEMALE HEAVIER REALISM RULE above — a realistic edit cannot render a peak physique on a heavier female body, so a believable strong transformation is used instead.)`;

if (!SYSTEM_PROMPT.includes(CAL_FIND)) throw new Error('CALIBRATION RULE block not found — client changed, abort');
const GOAL_SYSTEM_PROMPT = SYSTEM_PROMPT.replace(CAL_FIND, CAL_REPL);

const MUSCLE_BLOCKS = {
  table:     ['[[MUSCLE_TABLE_START]]', '[[MUSCLE_TABLE_END]]'],
  primary:   ['[[MUSCLE_PRIMARY_START]]', '[[MUSCLE_PRIMARY_END]]'],
  secondary: ['[[MUSCLE_SECOND_START]]', '[[MUSCLE_SECOND_END]]'],
  bullet:    ['[[MUSCLE_BULLET_START]]', '[[MUSCLE_BULLET_END]]'],
  reminder:  ['[[MUSCLE_REMINDER_START]]', '[[MUSCLE_REMINDER_END]]'],
};
function applyMuscleAxis(prompt, keep) {
  let out = prompt;
  for (const [name, [open, close]] of Object.entries(MUSCLE_BLOCKS)) {
    const i = out.indexOf(open), j = out.indexOf(close);
    if (i === -1 || j === -1) continue;
    out = keep[name]
      ? out.slice(0, i) + out.slice(i + open.length, j) + out.slice(j + close.length)
      : out.slice(0, i) + out.slice(j + close.length);
  }
  return out;
}
function muscleAxisPlan(gender, cond, intens) {
  const male = gender === 'male';
  const lean = male && (cond === 'fit' || cond === 'very_lean');
  const moderateStrong = male && cond === 'moderate' && (intens === 'dramatic' || intens === 'max');
  return { table: lean || moderateStrong, primary: lean, secondary: moderateStrong, bullet: lean, reminder: lean };
}

const BASE = 'https://absbyai.com';
async function post(pathname, body, timeoutMs = 300000) {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), timeoutMs);
  try {
    const r = await fetch(BASE + pathname, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body), signal: ctl.signal,
    });
    const j = await r.json().catch(() => null);
    if (!r.ok) throw new Error(`${pathname} HTTP ${r.status}: ${JSON.stringify(j).slice(0, 300)}`);
    return j;
  } finally { clearTimeout(t); }
}

async function main() {
  const gender = 'male', cond = process.env.COND || 'heavier', intens = 'max';
  const runs = Number(process.argv[2] || 4);
  const photoPath = process.argv[3] || path.join(OUT, 'male2-before.jpg');

  const sys = applyMuscleAxis(GOAL_SYSTEM_PROMPT, muscleAxisPlan(gender, cond, intens));
  for (const [, [open, close]] of Object.entries(MUSCLE_BLOCKS)) {
    if (sys.includes(open) || sys.includes(close)) throw new Error('marker leaked into sent prompt');
  }
  const userJson = JSON.stringify({
    user_description: '', subject_gender: gender,
    subject_current_condition: cond, intensity: intens, has_reference_photo: false,
  });
  console.log(`system prompt: ${sys.length} chars (no markers) | ${gender}/${cond}/${intens}`);

  const photoBase64 = fs.readFileSync(photoPath).toString('base64');
  const results = [];

  for (let i = 1; i <= runs; i++) {
    try {
      const p = await post('/api/generate-prompt', { systemPrompt: sys, userJson });
      const prompt = p.prompt || p.text || p.result;
      if (!prompt) throw new Error('no prompt returned: ' + JSON.stringify(p).slice(0, 200));
      if (i === 1) fs.writeFileSync(path.join(OUT, `hero-prompt-${cond}.txt`), prompt);

      const g = await post('/api/generate-image', {
        prompt, photoBase64, photoMime: 'image/jpeg', intensity: intens,
        sex: gender, startCondition: cond,
        distinctId: 'claude-hero', deviceId: 'claude-hero-' + crypto.randomBytes(4).toString('hex'),
        attemptId: crypto.randomUUID(),
      });
      const tel = g.telemetry || {};
      const saved = [];
      if (g.imageBase64) {
        const f = `hero-${cond}-run${i}-${tel.served_model || 'out'}.jpg`;
        fs.writeFileSync(path.join(OUT, f), Buffer.from(g.imageBase64, 'base64')); saved.push(f);
      }
      (g.candidates || []).forEach((c, k) => {
        const f = `hero-${cond}-run${i}-cand-${c.model || k}.jpg`;
        fs.writeFileSync(path.join(OUT, f), Buffer.from(c.imageBase64, 'base64')); saved.push(f);
      });
      results.push({ run: i, models_run: tel.models_run, served: tel.served_model,
        judge: tel.judge_winner, margin: tel.judge_margin, chooser: !!g.chooser,
        firstTry: tel.verifierPassedFirstTry, rungs: tel.retryRungsUsed, weak: tel.weakChange, saved });
      console.log(`run ${i}: models=${tel.models_run} served=${tel.served_model} judge=${tel.judge_winner}/${tel.judge_margin} chooser=${!!g.chooser} firstTry=${tel.verifierPassedFirstTry} -> ${saved.join(', ')}`);
    } catch (e) {
      console.log(`run ${i}: FAILED ${e.message}`);
      results.push({ run: i, error: e.message });
    }
  }
  fs.writeFileSync(path.join(OUT, `hero-results-${cond}.json`), JSON.stringify(results, null, 2));
  console.log('\ndone ->', path.join(OUT, `hero-results-${cond}.json`));
}
main().catch((e) => { console.error('FATAL', e); process.exit(1); });
