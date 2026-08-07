// Builds the RESTORED-MAGNITUDE prompt source by splicing the pre-retune male
// muscle blocks (commit 9cfe3d6, live during round 1 when Dan tagged
// lean-male__dramatic "just right") into today's index.html.
//
// Splicing exact bytes out of git rather than retyping the paragraphs — the
// blocks are 1-2k chars each and a transcription slip would silently become the
// experiment's independent variable.
//
// Deliberately NOT restored:
//   • the tan instruction — that removal WORKED (3 "too tan" on Gemini male in
//     round 1, zero since; today skin tone right on 6 of 6). It lives outside
//     these markers, so leaving the markers alone already preserves it.
//   • "Placed side by side with the input, the output must read as ..." — Phase 1
//     found GPT Image 1.5 renders that as a before/after diptych. Stripped from
//     the restored text; its intent is carried by the "must not be mistaken for
//     the original photo" sentence that remains.
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPO = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const PRE_RETUNE_REF = '9cfe3d6';

// Only the MALE magnitude blocks. Female directives are scoped by their own
// markers and are not touched.
const BLOCKS = ['MUSCLE_TABLE', 'MUSCLE_PRIMARY', 'MUSCLE_SECOND', 'MUSCLE_BULLET', 'MUSCLE_REMINDER'];

const DIPTYCH = /\s*Placed side by side with the input, the output must read as[^"]*?physique\./g;

function blockBody(html, name) {
  const s = `[[${name}_START]]`;
  const e = `[[${name}_END]]`;
  // First occurrence = the one inside SYSTEM_PROMPT. The later one is the
  // MUSCLE_BLOCKS lookup table in JS and must never be rewritten.
  const i = html.indexOf(s);
  const j = html.indexOf(e, i);
  if (i === -1 || j === -1) throw new Error(`block ${name} not found`);
  return { start: i + s.length, end: j, text: html.slice(i + s.length, j) };
}

function buildRestoredHtml() {
  const head = fs.readFileSync(path.join(REPO, 'public/index.html'), 'utf8');
  const old = execSync(`git -C "${REPO}" show ${PRE_RETUNE_REF}:public/index.html`, { maxBuffer: 1 << 28 }).toString();

  let out = head;
  const applied = [];
  // Replace back-to-front so earlier offsets stay valid.
  const targets = BLOCKS.map((n) => ({ name: n, cur: blockBody(out, n), pre: blockBody(old, n) }))
    .sort((a, b) => b.cur.start - a.cur.start);

  for (const t of targets) {
    let replacement = t.pre.text.replace(DIPTYCH, '');
    if (t.cur.text === replacement) { applied.push(`${t.name}: unchanged`); continue; }
    out = out.slice(0, t.cur.start) + replacement + out.slice(t.cur.end);
    applied.push(`${t.name}: restored (${t.cur.text.length} -> ${replacement.length} chars)`);
  }
  return { html: out, applied };
}

// --- assertions: prove the patch did what it claims, before spending money ---
function verify(html) {
  const fail = [];
  const ck = (cond, msg) => { if (!cond) fail.push(msg); };
  const table = blockBody(html, 'MUSCLE_TABLE').text;

  ck(/subtle ≈ \+5 lb, moderate ≈ \+8 lb, dramatic ≈ \+12 lb, max ≈ \+15 lb/.test(table),
    'anchor table not restored to +5/+8/+12/+15');
  ck(/visibly BIGGER/.test(blockBody(html, 'MUSCLE_PRIMARY').text),
    'MUSCLE_PRIMARY missing "visibly BIGGER"');
  ck(/noticeably thicker arms/.test(blockBody(html, 'MUSCLE_SECOND').text),
    'MUSCLE_SECOND missing restored magnitude verbs');

  // The contradiction guard: restoring "+15 lb / visibly BIGGER" while also
  // saying "no blown-up arms" is the retract-an-instruction pattern this
  // project has already proven unreliable. The male magnitude blocks must not
  // carry both.
  for (const b of ['MUSCLE_PRIMARY', 'MUSCLE_SECOND', 'MUSCLE_BULLET']) {
    ck(!/NEVER a bodybuilder|never a bodybuilder|blown-up arms|boulder shoulders/i.test(blockBody(html, b).text),
      `${b} still carries a no-bodybuilder prohibition that contradicts the restored magnitude`);
  }
  ck(!DIPTYCH.test(html), 'diptych sentence leaked back in');

  // Untouched-by-design checks.
  ck(/Do NOT add a tan|no tan|NEVER add a tan|not add a tan/i.test(html), 'no-tan rule missing (should be untouched)');
  ck((html.match(/\[\[MUSCLE_TABLE_START\]\]/g) || []).length === 2, 'MUSCLE_TABLE marker count changed');
  return fail;
}

module.exports = { buildRestoredHtml, verify, blockBody, PRE_RETUNE_REF };

if (require.main === module) {
  const { html, applied } = buildRestoredHtml();
  applied.forEach((a) => console.log('  ' + a));
  const fail = verify(html);
  console.log(fail.length ? '\nFAILURES:\n  ' + fail.join('\n  ') : '\nall patch assertions passed');
  process.exitCode = fail.length ? 1 : 0;
}
