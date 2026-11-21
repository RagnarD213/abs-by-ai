#!/usr/bin/env node
// Supplement Audit eval harness.
//
// Runs a folder of structured-intake cases through /api/counsel and prints the
// verdict, safety rating, keep/drop table, new stack, and dollars saved next to
// a human-readable "expect" note. Nothing is auto-scored EXCEPT the safety
// canaries: a case tagged "mustBeRed" that comes back GREEN/YELLOW (or
// "mustBeGreen" that comes back RED) prints a loud FAIL — those are ship gates.
//
// Cases POST structured `items` directly, so no photos and no label-reading
// step are involved (that step is bypassed by design).
//
// Run:
//   node eval/counsel-eval.js eval/counsel-cases                 # against prod
//   BACKEND_URL=http://localhost:3000 node eval/counsel-eval.js eval/counsel-cases
//
// To see the FULL audit (keep/drop table, new stack, reasoning) rather than the
// free preview, pass a MEMBER token:
//   EVAL_AUTH_TOKEN=<member-session-token> node eval/counsel-eval.js eval/counsel-cases
// The safety RATING is visible even anonymously, so the RED canaries (4, 5) can
// be checked without a token; keep/drop detail needs one.

const fs = require('fs');
const path = require('path');

const BACKEND_URL = process.env.BACKEND_URL || 'https://absbyai.com';
const dir = process.argv[2];
if (!dir) { console.error('Usage: node eval/counsel-eval.js <folder-of-case-json>'); process.exit(1); }

async function runCase(caseObj) {
  const res = await fetch(`${BACKEND_URL}/api/counsel`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(process.env.EVAL_AUTH_TOKEN ? { Authorization: `Bearer ${process.env.EVAL_AUTH_TOKEN}` } : {}),
    },
    body: JSON.stringify({ decisionType: caseObj.decisionType || 'supplement-audit', intake: caseObj.intake }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

function line(ch = '─', n = 72) { return ch.repeat(n); }

(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort();
  if (!files.length) { console.error(`No .json cases found in ${dir}`); process.exit(1); }
  console.log(`\nSupplement Audit eval → ${BACKEND_URL}`);
  console.log(process.env.EVAL_AUTH_TOKEN ? '(authenticated — full audit visible)\n' : '(anonymous — preview only; safety rating still visible)\n');

  let gateFails = 0;
  for (const f of files) {
    const caseObj = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8'));
    console.log(line('═'));
    console.log(`CASE: ${f}`);
    if (caseObj.expect) console.log(`EXPECT: ${caseObj.expect}`);
    console.log(line());
    let data;
    try {
      process.stdout.write('  running (5 model calls)... ');
      data = await runCase(caseObj);
      console.log('done');
    } catch (e) {
      console.log(`ERROR: ${e.message}\n`);
      continue;
    }
    const c = data.counsel || {};
    const v = c.verdict || {};
    const safety = c.opinions?.safety || {};
    const rating = safety.rating || '(hidden)';

    console.log(`  VERDICT:        ${v.verdict || '(locked)'}`);
    console.log(`  CONFIDENCE:     ${v.confidence || '(locked)'}`);
    console.log(`  SAFETY RATING:  ${rating}`);
    console.log(`  MONTHLY SAVED:  ${v.monthly_savings || '(none)'}`);
    if (Array.isArray(safety.flags) && safety.flags.length) {
      console.log('  SAFETY FLAGS:');
      for (const fl of safety.flags) console.log(`     [${fl.severity}] ${fl.flag}`);
    }
    if (Array.isArray(v.keep_drop_table) && v.keep_drop_table.length) {
      console.log('  KEEP / DROP:');
      for (const r of v.keep_drop_table) console.log(`     ${(r.action || '').padEnd(9)} ${r.item} — ${r.reason}`);
    } else if (data.locked) {
      console.log('  KEEP / DROP:    (members-only — pass EVAL_AUTH_TOKEN to see it)');
    }
    if (Array.isArray(v.new_stack) && v.new_stack.length) {
      console.log('  NEW STACK:');
      for (const s of v.new_stack) console.log(`     ${s.ingredient} — ${s.dose} — ${s.timing} — ${s.monthly_cost}`);
    }

    // Safety-canary gates.
    if (caseObj.mustBeRed && rating !== 'RED') {
      console.log(`\n  ❌ GATE FAIL: expected SAFETY RED, got ${rating}. The recalibration went too far — fix before shipping.`);
      gateFails++;
    }
    if (caseObj.mustBeGreen && rating === 'RED') {
      console.log(`\n  ❌ GATE FAIL: expected GREEN/YELLOW (anti-caution canary), got RED.`);
      gateFails++;
    }
    console.log('');
  }
  console.log(line('═'));
  console.log(gateFails ? `\n❌ ${gateFails} safety-canary gate(s) FAILED — do not ship.\n` : `\n✅ All safety-canary gates passed.\n`);
  process.exit(gateFails ? 1 : 0);
})();
