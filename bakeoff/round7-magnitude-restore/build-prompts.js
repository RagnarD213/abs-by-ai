// Builds (and caches) the NEW full + condensed prompt for each male case from
// the real production assembly path (goalSystemPrompt() out of public/index.html
// -> prod /api/generate-prompt -> byte-identical condenseForKontext copy).
// Paced >=8s apart for prod's sitewide 10-AI-calls/min limiter.
//
// Asserts the magnitude restore actually landed in the prompt this harness is
// about to spend money on — in the FULL prompt (Gemini's leg) and in the
// CONDENSED one (FLUX's leg), because production sends the restore to both.
const fs = require('fs');
const path = require('path');
const { CASES } = require('./cases');
const { generatePrompt, condense } = require('../prompts');

const OUT = path.join(__dirname, 'prompts');
fs.mkdirSync(OUT, { recursive: true });

// Magnitude fingerprint per case. Heavier males are the PLACEBO control: they
// carry no [[MUSCLE_*]] markers, so their prompt is unchanged by the restore
// and must NOT contain a mass ask. A hit there would mean the marker scoping
// leaked (the failure mode this project has recorded four times).
const MAG = /\b(bigger|larger|thicker|wider|fuller|more muscular)\b/i;
const MASS_ASK = /(pounds of lean muscle|lb of lean muscle|added roughly)/i;

(async () => {
  let fail = 0;
  const ck = (ok, msg) => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${msg}`); if (!ok) fail++; };

  for (const c of CASES) {
    const placebo = c.condition === 'heavier';
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
    ck(d.length <= 4000, `${c.id}: condensed <= 4000`);
    // The half of 14b4790 that WORKED must survive the restore.
    // NB: the retune's own PROHIBITION text contains the words "tan"/"bronzing"
    // — this is the documented false-positive trap. Strip every prohibition
    // form first, then assert nothing tan-flavoured survives.
    const tanStripped = f
      .replace(/(do not|don't|never|no|avoid)[^.]{0,160}?\b(tan|bronz\w*|sun-kissed|golden cast)\b[^.]*\./gi, '')
      .replace(/^[-•*\s]*any tan[^.\n]*/gim, "");
    ck(!/\b(tan|bronz\w*|sun-kissed)\b/i.test(tanStripped), `${c.id}: no positive tan instruction`);
    if (placebo) {
      ck(!MASS_ASK.test(f), `${c.id}: PLACEBO (heavier) carries no mass ask — scoping held`);
    } else {
      ck(MAG.test(f), `${c.id}: full carries magnitude language`);
      ck(MAG.test(d), `${c.id}: condensed carries magnitude language`);
    }
  }
  console.log(fail ? `\n${fail} FAILURES` : '\nall prompt assertions passed');
  process.exitCode = fail ? 1 : 0;
})();
