// Builds (and caches) BOTH prompt variants for each round-5 case from the real
// production assembly path: goalSystemPrompt() out of public/index.html, driven
// through prod /api/generate-prompt, then condensed by the byte-identical copy of
// server.js's condenseForKontext.
//
// Paced >=8s apart because prod's aiLimiter allows 10 AI calls/min sitewide.
const fs = require('fs');
const path = require('path');
const { CASES, MAX_SEEDREAM_CHARS } = require('./cases');
const { generatePrompt, condense } = require('../prompts');

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
        const cd = condense(p);
        fs.writeFileSync(full, p);
        fs.writeFileSync(cond, cd);
        console.log(`built  ${c.id.padEnd(28)} full=${p.length} condensed=${cd.length}`);
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

  // ── Assertions that shape the experiment's design ────────────────────────────
  let fullWorst = 0, fullWorstId = null, condWorst = 0, condWorstId = null;
  let truncated = [];
  for (const c of CASES) {
    const f = fs.readFileSync(path.join(OUT, `${c.id}.full.txt`), 'utf8');
    const d = fs.readFileSync(path.join(OUT, `${c.id}.condensed.txt`), 'utf8');
    if (f.length > fullWorst) { fullWorst = f.length; fullWorstId = c.id; }
    if (d.length > condWorst) { condWorst = d.length; condWorstId = c.id; }
    // A full prompt cut off mid-sentence would mean /api/generate-prompt hit its
    // max_tokens ceiling again (the 8a7c4a4 bug); the CLOSING block is the tell.
    if (!/\S/.test(f.slice(-3)) || f.length < 2000) truncated.push(c.id);
    if (f.includes('[[')) truncated.push(`${c.id} (marker leak)`);
  }

  console.log(`\nlongest full prompt:      ${fullWorst} chars (${fullWorstId})`);
  console.log(`longest condensed prompt: ${condWorst} chars (${condWorstId}) — Seedream limit ${MAX_SEEDREAM_CHARS}`);

  let fail = 0;
  const ck = (ok, msg) => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${msg}`); if (!ok) fail++; };

  ck(condWorst <= MAX_SEEDREAM_CHARS,
     `condensed fits Seedream unchanged (${condWorst} <= ${MAX_SEEDREAM_CHARS})`);
  // The load-bearing design fact: full is structurally un-sendable to Seedream,
  // so the female challenger leg can never be part of a full-vs-condensed A/B.
  ck(fullWorst > MAX_SEEDREAM_CHARS,
     `full EXCEEDS Seedream's ceiling (${fullWorst} > ${MAX_SEEDREAM_CHARS}) — female challenger is condensed-only by construction`);
  ck(truncated.length === 0, `no truncated prompts or marker leaks${truncated.length ? ': ' + truncated.join(', ') : ''}`);

  console.log(fail ? `\n${fail} assertion(s) FAILED` : '\nall prompt assertions passed');
  process.exitCode = fail ? 1 : 0;
})();
