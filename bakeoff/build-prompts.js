// Builds (and caches) the real production prompt for each of the 12 cases.
// Paced ≥8s apart because prod's aiLimiter allows 10 AI calls/min sitewide.
const fs = require('fs');
const path = require('path');
const { CASES } = require('./cases');
const { generatePrompt, condense } = require('./prompts');

const OUT = path.join(__dirname, 'prompts');
fs.mkdirSync(OUT, { recursive: true });

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
        console.log('built', c.id, p.length, 'chars');
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
  console.log('done');
})();
