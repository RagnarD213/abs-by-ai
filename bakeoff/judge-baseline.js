// Step 1 — baseline the CURRENT production judge against Dan's labels.
//
// The judge call below is copied byte-for-byte from server.js `judgeCandidates`
// (~line 2325): same model (claude-sonnet-5), same max_tokens, same prompt text,
// same JSON contract, no temperature. The only difference is where the images
// come from.
//
// Scoring: production's judge is pairwise, so for each case we run it on
// {Dan's best, every other candidate} in BOTH orders (position-bias control).
// A pairing is "won" if Dan's best is preferred in both orders; an order
// disagreement counts as half.
const fs = require('fs');
const path = require('path');
const { buildCases, imageBlock, anthropic, parseJson, pmap, ROUND1 } = require('./judge-lib');

// ── verbatim production prompt text (server.js ~2349) ────────────────────────
const PROD_PROMPT = 'Candidates A and B are AI fitness-transformation edits of the BEFORE photo. Judge them.\n\nFor each candidate assess:\n- identity: "good" (clearly the same person — same face, recognizably them), "borderline" (mostly the same person but something about the face is slightly off), or "broken" (looks like a different person, or the face/body is distorted or artifact-ridden)\n- photoreal: true if it reads as a real unretouched photograph, false if it looks AI-generated, painted, or uncanny\n\nThen pick the winner: the candidate showing the MORE dramatic, more impressive body transformation versus the BEFORE (leaner, more muscular, more defined) among those with acceptable identity and photorealism. Set margin to "clear" only if one candidate is decisively better overall; use "close" when they are near-equal or the call is debatable.\n\nReply with ONLY this JSON, no other text:\n{"a":{"identity":"good|borderline|broken","photoreal":true},"b":{"identity":"good|borderline|broken","photoreal":true},"winner":"a|b","margin":"clear|close"}';

const MODEL = 'claude-sonnet-5';

async function prodJudge(photoFile, candAFile, candBFile) {
  const content = [
    { type: 'text', text: 'BEFORE photo (the real person):' },
    imageBlock(photoFile),
    { type: 'text', text: 'Candidate A:' },
    imageBlock(candAFile),
    { type: 'text', text: 'Candidate B:' },
    imageBlock(candBFile),
    { type: 'text', text: PROD_PROMPT },
  ];
  const { text } = await anthropic({
    model: MODEL,
    maxTokens: 300,
    content,
    cacheKey: `prod-judge|${MODEL}|${photoFile}|${candAFile}|${candBFile}`,
  });
  const raw = parseJson(text);
  if (!raw) return null;
  const norm = (x) => ({
    identity: ['good', 'borderline', 'broken'].includes(x?.identity) ? x.identity : 'borderline',
    photoreal: x?.photoreal !== false,
  });
  return {
    a: norm(raw.a),
    b: norm(raw.b),
    winner: raw.winner === 'b' ? 'b' : 'a',
    margin: raw.margin === 'clear' ? 'clear' : 'close',
  };
}

(async () => {
  const cases = buildCases().filter((c) => c.best);
  const skipped = buildCases().filter((c) => !c.best).map((c) => c.caseId);

  // Build the pairing list: Dan's best vs every other candidate, both orders.
  const jobs = [];
  for (const c of cases) {
    for (const other of c.candidates) {
      if (other.letter === c.best.letter) continue;
      jobs.push({ c, other, order: 'best-first' });
      jobs.push({ c, other, order: 'best-second' });
    }
  }
  console.log(`Baseline: ${cases.length} cases, ${jobs.length / 2} pairings, ${jobs.length} judge calls (both orders).`);
  console.log(`Cases with no Dan-best (excluded): ${skipped.join(', ') || 'none'}`);

  let done = 0;
  const results = await pmap(jobs, 4, async (job) => {
    const { c, other, order } = job;
    const bestFirst = order === 'best-first';
    const A = bestFirst ? c.best : other;
    const B = bestFirst ? other : c.best;
    const v = await prodJudge(c.photoFile, A.file, B.file);
    done++;
    if (done % 20 === 0) console.log(`  ${done}/${jobs.length}`);
    const bestKey = bestFirst ? 'a' : 'b';
    return {
      caseId: c.caseId, order,
      bestLetter: c.best.letter, bestModel: c.best.model, bestVariant: c.best.variant,
      otherLetter: other.letter, otherModel: other.model, otherVariant: other.variant,
      otherTags: other.tags,
      verdict: v,
      preferredBest: v ? v.winner === bestKey : null,
      margin: v ? v.margin : null,
    };
  });

  // ── score ──────────────────────────────────────────────────────────────────
  const byPairing = new Map();
  for (const r of results) {
    const k = `${r.caseId}:${r.otherLetter}`;
    if (!byPairing.has(k)) byPairing.set(k, { ...r, orders: {} });
    byPairing.get(k).orders[r.order] = r.preferredBest;
  }

  let pairScore = 0, pairTotal = 0, flips = 0;
  const perCase = {};
  const lossExamples = [];
  for (const [k, p] of byPairing) {
    const a = p.orders['best-first'];
    const b = p.orders['best-second'];
    let score;
    if (a === null || b === null) score = 0.5;          // judge failed → no credit either way
    else if (a && b) score = 1;                          // best wins regardless of position
    else if (!a && !b) score = 0;                        // other wins regardless of position
    else { score = 0.5; flips++; }                       // position-dependent = coin flip
    pairScore += score; pairTotal++;
    const c = (perCase[p.caseId] ||= { wins: 0, total: 0, losses: [] });
    c.wins += score; c.total++;
    if (score < 1) {
      c.losses.push({ other: p.otherLetter, model: p.otherModel, variant: p.otherVariant, tags: p.otherTags, score });
      lossExamples.push({ caseId: p.caseId, bestModel: p.bestModel, otherModel: p.otherModel, otherTags: p.otherTags, score });
    }
  }

  let caseAgree = 0;
  for (const [caseId, c] of Object.entries(perCase)) {
    c.rate = c.wins / c.total;
    c.majority = c.wins > c.total / 2;
    c.sweep = c.wins === c.total;
    if (c.majority) caseAgree++;
  }

  // How often does the loss go to a candidate Dan tagged "too muscular"/"too tan"/"looks fake"?
  const rejectTagCounts = {};
  for (const l of lossExamples) for (const t of l.otherTags) rejectTagCounts[t] = (rejectTagCounts[t] || 0) + 1;

  const summary = {
    judge: 'production (server.js judgeCandidates, verbatim)',
    model: MODEL,
    casesEvaluated: cases.length,
    casesExcludedNoBest: skipped,
    pairings: pairTotal,
    judgeCalls: jobs.length,
    pairingAgreement: +(pairScore / pairTotal).toFixed(4),
    caseAgreement: +(caseAgree / cases.length).toFixed(4),
    caseAgreementCount: `${caseAgree}/${cases.length}`,
    positionFlips: flips,
    positionFlipRate: +(flips / pairTotal).toFixed(4),
    lossesToTagCounts: rejectTagCounts,
    perCase,
  };

  fs.writeFileSync(path.join(ROUND1, 'judge-baseline.json'), JSON.stringify({ summary, results }, null, 2));

  console.log('\n══════════ BASELINE — current production judge ══════════');
  console.log(`Pairing-level agreement with Dan : ${(summary.pairingAgreement * 100).toFixed(1)}%  (${pairScore.toFixed(1)}/${pairTotal})`);
  console.log(`Case-level agreement (majority)  : ${(summary.caseAgreement * 100).toFixed(1)}%  (${summary.caseAgreementCount})`);
  console.log(`Position flips (order changed the answer): ${flips}/${pairTotal} (${(summary.positionFlipRate * 100).toFixed(1)}%)`);
  console.log('\nPer case:');
  for (const [caseId, c] of Object.entries(perCase)) {
    console.log(`  ${caseId.padEnd(30)} ${c.wins.toFixed(1)}/${c.total}  ${c.majority ? 'AGREE' : 'DISAGREE'}${c.sweep ? ' (sweep)' : ''}`);
  }
  console.log('\nWhen the judge preferred something over Dan\'s pick, that candidate was tagged:');
  for (const [t, n] of Object.entries(rejectTagCounts).sort((a, b) => b[1] - a[1])) console.log(`  ${t.padEnd(20)} ${n}`);
  console.log('\nSaved → bakeoff/round1/judge-baseline.json');
})();
