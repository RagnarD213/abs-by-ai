// Phase 3 — evaluate the rebuilt judge against Dan's labels.
//
// Two metrics, both scored against Dan's "best" pick:
//   PAIRWISE  — production-relevant. The judge sees {Dan's best, one other}, in
//               both orders. Directly comparable to the production-judge
//               baseline in judge-baseline.json.
//   N-WAY     — the harness metric. The judge sees every candidate at once and
//               must rank Dan's best first.
//
// Three cases supply the few-shot exemplars and are excluded from the headline
// numbers; the HELD-OUT block is the honest result.
//
// Every Anthropic call is disk-cached, so re-running with different composite
// weights costs nothing.
const fs = require('fs');
const path = require('path');
const { buildCases, pmap, ROUND1 } = require('./judge-lib');
const { scoreCandidates, DEFAULT_WEIGHTS, EXEMPLAR_CASE_IDS } = require('./judge-v2');

const MODEL = process.env.JUDGE_MODEL || 'claude-sonnet-5';
const USE_FEWSHOT = process.env.NO_FEWSHOT !== '1';
const OUT = process.env.EVAL_OUT || `judge-v2-${MODEL}${USE_FEWSHOT ? '' : '-nofewshot'}.json`;

const WEIGHTS = process.env.WEIGHTS ? { ...DEFAULT_WEIGHTS, ...JSON.parse(process.env.WEIGHTS) } : DEFAULT_WEIGHTS;

(async () => {
  // HELD_OUT_ONLY=1 skips the three exemplar cases. The held-out number is the
  // one that decides anything, so a costlier judge model can be compared on it
  // alone rather than paying for cases whose result we already know.
  const heldOutOnly = process.env.HELD_OUT_ONLY === '1';
  const cases = buildCases().filter((c) => c.best && (!heldOutOnly || !EXEMPLAR_CASE_IDS.includes(c.caseId)));
  const noBest = buildCases().filter((c) => !c.best).map((c) => c.caseId);

  console.log(`Judge v2 eval — model=${MODEL} fewShot=${USE_FEWSHOT}`);
  console.log(`${cases.length} labelled cases; exemplar cases excluded from headline: ${EXEMPLAR_CASE_IDS.join(', ')}`);
  console.log(`No-best cases (excluded entirely): ${noBest.join(', ')}`);

  // ── pairwise ───────────────────────────────────────────────────────────────
  const pairJobs = [];
  for (const c of cases) {
    for (const other of c.candidates) {
      if (other.letter === c.best.letter) continue;
      pairJobs.push({ c, other });
    }
  }
  console.log(`\nPairwise: ${pairJobs.length} pairings × 2 orders = ${pairJobs.length * 2} calls`);

  let done = 0;
  const pairResults = await pmap(pairJobs, 3, async ({ c, other }) => {
    const res = await scoreCandidates({
      model: MODEL,
      photoFile: c.photoFile,
      candidates: [c.best, other],
      useFewShot: USE_FEWSHOT,
      weights: WEIGHTS,
      tag: `pair|${c.caseId}|${c.best.letter}v${other.letter}`,
    });
    done++;
    if (done % 10 === 0) console.log(`  ${done}/${pairJobs.length}`);
    return {
      caseId: c.caseId,
      bestLetter: c.best.letter, bestModel: c.best.model, bestVariant: c.best.variant,
      otherLetter: other.letter, otherModel: other.model, otherVariant: other.variant,
      otherTags: other.tags,
      preferredBest: res ? res.winner.letter === c.best.letter : null,
      orderDisagreement: res ? res.orderDisagreement : null,
      margin: res ? res.margin : null,
      scores: res ? res.ranked.map((m) => ({
        letter: m.letter, model: m.model, variant: m.variant, score: m.score,
        identity: m.identity, photoreal: m.photoreal, skin_tone: m.skin_tone,
        definition: m.definition, bulk: m.bulk, change: m.change, notes: m.notes,
      })) : null,
    };
  });

  // ── N-way ──────────────────────────────────────────────────────────────────
  console.log(`\nN-way: ${cases.length} cases × 2 orders = ${cases.length * 2} calls`);
  const nwayResults = await pmap(cases, 3, async (c) => {
    const res = await scoreCandidates({
      model: MODEL,
      photoFile: c.photoFile,
      candidates: c.candidates,
      useFewShot: USE_FEWSHOT,
      weights: WEIGHTS,
      tag: `nway|${c.caseId}`,
    });
    return {
      caseId: c.caseId,
      danBest: c.best.letter,
      danBestModel: `${c.best.model}/${c.best.variant}`,
      judgeTop1: res ? res.winner.letter : null,
      judgeTop1Model: res ? `${res.winner.model}/${res.winner.variant}` : null,
      correct: res ? res.winner.letter === c.best.letter : null,
      danBestRank: res ? res.ranked.findIndex((m) => m.letter === c.best.letter) + 1 : null,
      n: c.candidates.length,
      orderDisagreement: res ? res.orderDisagreement : null,
      ranked: res ? res.ranked.map((m) => ({
        letter: m.letter, model: `${m.model}/${m.variant}`, score: m.score,
        identity: m.identity, photoreal: m.photoreal, skin_tone: m.skin_tone,
        definition: m.definition, bulk: m.bulk, change: m.change,
        danAcceptable: m.acceptable, danTags: m.tags,
      })) : null,
    };
  });

  // ── scoring ────────────────────────────────────────────────────────────────
  const score = (caseIds) => {
    const pw = pairResults.filter((r) => caseIds.includes(r.caseId));
    const nw = nwayResults.filter((r) => caseIds.includes(r.caseId));
    const pairWins = pw.reduce((s, r) => s + (r.preferredBest === null ? 0.5 : r.preferredBest ? 1 : 0), 0);
    const perCase = {};
    for (const r of pw) {
      const c = (perCase[r.caseId] ||= { wins: 0, total: 0 });
      c.wins += r.preferredBest === null ? 0.5 : r.preferredBest ? 1 : 0;
      c.total++;
    }
    let caseAgree = 0;
    for (const c of Object.values(perCase)) if (c.wins > c.total / 2) caseAgree++;
    const nwayCorrect = nw.filter((r) => r.correct).length;
    const top2 = nw.filter((r) => r.danBestRank && r.danBestRank <= 2).length;
    return {
      cases: caseIds.length,
      pairings: pw.length,
      pairingAgreement: +(pairWins / pw.length).toFixed(4),
      pairingRaw: `${pairWins.toFixed(1)}/${pw.length}`,
      caseAgreement: +(caseAgree / Object.keys(perCase).length).toFixed(4),
      caseAgreementRaw: `${caseAgree}/${Object.keys(perCase).length}`,
      nwayTop1: +(nwayCorrect / nw.length).toFixed(4),
      nwayTop1Raw: `${nwayCorrect}/${nw.length}`,
      nwayTop2: +(top2 / nw.length).toFixed(4),
      nwayTop2Raw: `${top2}/${nw.length}`,
      perCase,
    };
  };

  const allIds = cases.map((c) => c.caseId);
  const heldOutIds = allIds.filter((id) => !EXEMPLAR_CASE_IDS.includes(id));
  const summary = {
    model: MODEL, fewShot: USE_FEWSHOT, weights: WEIGHTS,
    exemplarCases: EXEMPLAR_CASE_IDS,
    heldOut: score(heldOutIds),
    all: score(allIds),
    positionFlips: pairResults.filter((r) => r.orderDisagreement).length,
    positionFlipRate: +(pairResults.filter((r) => r.orderDisagreement).length / pairResults.length).toFixed(4),
  };

  fs.writeFileSync(path.join(ROUND1, OUT), JSON.stringify({ summary, pairResults, nwayResults }, null, 2));

  const show = (name, s) => {
    console.log(`\n── ${name} (${s.cases} cases) ──`);
    console.log(`  Pairwise agreement : ${(s.pairingAgreement * 100).toFixed(1)}%  (${s.pairingRaw})`);
    console.log(`  Case-level (major.): ${(s.caseAgreement * 100).toFixed(1)}%  (${s.caseAgreementRaw})`);
    console.log(`  N-way top-1        : ${(s.nwayTop1 * 100).toFixed(1)}%  (${s.nwayTop1Raw})`);
    console.log(`  N-way top-2        : ${(s.nwayTop2 * 100).toFixed(1)}%  (${s.nwayTop2Raw})`);
  };
  console.log('\n══════════ JUDGE v2 ══════════');
  show('HELD OUT (headline)', summary.heldOut);
  show('ALL LABELLED CASES', summary.all);
  console.log(`\nPosition flips (order changed the winner): ${summary.positionFlips}/${pairResults.length} (${(summary.positionFlipRate * 100).toFixed(1)}%)`);
  console.log('\nPer-case N-way:');
  for (const r of nwayResults) {
    const held = EXEMPLAR_CASE_IDS.includes(r.caseId) ? ' [exemplar]' : '';
    console.log(`  ${r.caseId.padEnd(30)} n=${String(r.n).padStart(2)}  Dan=${r.danBest} (${r.danBestModel})  judge=${r.judgeTop1} (${r.judgeTop1Model})  rank=${r.danBestRank}  ${r.correct ? 'HIT' : 'miss'}${held}`);
  }
  console.log(`\nSaved → bakeoff/round1/${OUT}`);
})();
