// Builds (and caches) the real production prompt for each round-2 female case.
// Paced >=8s apart because prod's aiLimiter allows 10 AI calls/min sitewide.
const fs = require('fs');
const path = require('path');
const { CASES } = require('./cases');
const { generatePrompt, condense } = require('../prompts');

const OUT = path.join(__dirname, 'prompts');
fs.mkdirSync(OUT, { recursive: true });

const MAX_SEEDREAM_CHARS = 4000; // hard 422 above this

(async () => {
  for (const c of CASES) {
    const full = path.join(OUT, `${c.id}.full.txt`);
    const cond = path.join(OUT, `${c.id}.condensed.txt`);
    if (fs.existsSync(full) && fs.existsSync(cond)) { console.log('cached', c.id); continue; }
    let attempt = 0;
    for (;;) {
      try {
        const p = await generatePrompt({ gender: c.gender, condition: c.condition, intensity: c.intensity });
        fs.writeFileSync(full, p);
        fs.writeFileSync(cond, condense(p));
        console.log('built', c.id, `full=${p.length}`, `condensed=${condense(p).length}`);
        break;
      } catch (e) {
        attempt++;
        console.log('retry', c.id, e.message);
        if (attempt >= 3) throw e;
        await new Promise((r) => setTimeout(r, 20000));
      }
    }
    await new Promise((r) => setTimeout(r, 8000));
  }

  // Plan step 4 asks us to assert programmatically that condenseForKontext's
  // output fits Seedream's 4000-char ceiling for the LONGEST female prompt.
  let worst = 0, worstId = null;
  for (const c of CASES) {
    const n = fs.readFileSync(path.join(OUT, `${c.id}.condensed.txt`), 'utf8').length;
    if (n > worst) { worst = n; worstId = c.id; }
  }
  console.log(`\nlongest condensed female prompt: ${worst} chars (${worstId}) — limit ${MAX_SEEDREAM_CHARS}`);
  if (worst > MAX_SEEDREAM_CHARS) {
    console.log('*** FAIL: condensed prompt exceeds Seedream limit — a trim is required in server.js');
    process.exitCode = 1;
  } else {
    console.log('*** PASS: condenseForKontext output fits Seedream unchanged; no extra trim needed');
  }
})();
