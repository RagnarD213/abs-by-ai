// Builds (and caches) the NEW full + condensed prompt for each male case from
// the real production assembly path (goalSystemPrompt() out of public/index.html
// -> prod /api/generate-prompt -> byte-identical condenseForKontext copy).
// Paced >=8s apart for prod's sitewide 10-AI-calls/min limiter.
const fs = require('fs');
const path = require('path');
const { CASES } = require('./cases');
const { generatePrompt, condense } = require('../prompts');

const OUT = path.join(__dirname, 'prompts');
fs.mkdirSync(OUT, { recursive: true });

const RUNG = {
  // expected rung fingerprint per case id — asserts the ladder actually landed
  // in the assembled prompt this harness is about to spend money on.
  'lean-male__dramatic':     'first serratus lines visible beside the ribs',
  'lean-male__max':          'deep shadowed separation between all six abdominal blocks',
  'moderate-male__dramatic': 'first serratus lines visible beside the ribs',
  'moderate-male__max':      'deep shadowed separation between all six abdominal blocks',
  'heavier-male__dramatic':  'top two abdominal blocks clearly separated',
  'heavier-male__max':       'first serratus lines visible beside the ribs',
};

(async () => {
  let fail = 0;
  const ck = (ok, msg) => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${msg}`); if (!ok) fail++; };

  for (const c of CASES) {
    const fullPath = path.join(OUT, `${c.id}.full.txt`);
    const condPath = path.join(OUT, `${c.id}.condensed.txt`);
    if (!fs.existsSync(fullPath)) {
      const p = await generatePrompt({ gender: c.gender, condition: c.condition, intensity: c.intensity });
      fs.writeFileSync(fullPath, p);
      fs.writeFileSync(condPath, condense(p));
      console.log(`built  ${c.id.padEnd(26)} full=${p.length} condensed=${condense(p).length}`);
      await new Promise((r) => setTimeout(r, 8000));
    } else console.log('cached', c.id);

    const f = fs.readFileSync(fullPath, 'utf8');
    const d = fs.readFileSync(condPath, 'utf8');
    ck(!f.includes('[[') && !d.includes('[['), `${c.id}: no marker leak`);
    ck(/natural, unretouched smartphone photograph/.test(f), `${c.id}: full not truncated`);
    ck(f.includes(RUNG[c.id]), `${c.id}: full carries assigned rung`);
    ck(d.includes(RUNG[c.id]), `${c.id}: condensed carries assigned rung`);
    ck(d.length <= 4000, `${c.id}: condensed <= 4000`);
  }
  console.log(fail ? `\n${fail} FAILURES` : '\nall prompt assertions passed');
  process.exitCode = fail ? 1 : 0;
})();
