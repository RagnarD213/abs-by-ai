// Female judge validation — measure the production judge (judge-v2, the exact
// config shipped in server.js: claude-sonnet-5, few-shot exemplars, default
// weights, order-swapped double pass) against Dan's 14 female blind labels from
// round2-female and round3-female.
//
// The male eval (judge-eval.js) is the pattern: for each case, pair Dan's pick
// against the other candidate and ask whether the judge prefers Dan's pick.
// Female specifics:
//   - Two rounds share a case id (fem-moderate) so cases are namespaced r2:/r3:.
//   - 12 rows have a "best". The 2 "neither" rows each have exactly ONE
//     candidate Dan marked acceptable — those are scored as acceptable-vs-
//     rejected pairings (flagged `proxy: true`) and reported both included and
//     excluded so neither reading is hidden.
//   - Every candidate here is one Gemini vs one Seedream image, mirroring the
//     production female ensemble exactly.
//
// Every Anthropic call is disk-cached via judge-lib (round1/judge-cache), so
// re-runs — including offline weight sweeps — are $0. Cache files hold only the
// judge's text output, never images, so round-3 privacy is preserved.
const fs = require('fs');
const path = require('path');
const { pmap, anthropic } = require('./judge-lib');
const { scoreCandidates, DEFAULT_WEIGHTS, SUBTLE_WEIGHTS, FEMALE_SUBTLE_EXEMPLAR } = require('./judge-v2');

const MODEL = process.env.JUDGE_MODEL || 'claude-sonnet-5';
const USE_FEWSHOT = process.env.NO_FEWSHOT !== '1';
// TIER_FIX=1 turns on the female-Subtle tier context (exemplar + tier note) for
// Subtle rows. The exemplar's own row is then excluded from the headline.
const TIER_FIX = process.env.TIER_FIX === '1';
const WEIGHTS = process.env.WEIGHTS ? { ...DEFAULT_WEIGHTS, ...JSON.parse(process.env.WEIGHTS) } : DEFAULT_WEIGHTS;
const OUT = process.env.EVAL_OUT || `judge-v2-female-${MODEL}${USE_FEWSHOT ? '' : '-nofewshot'}${TIER_FIX ? '-tierfix' : ''}.json`;

const ROUNDS = [
  { tag: 'r2', dir: path.join(__dirname, 'round2-female') },
  { tag: 'r3', dir: path.join(__dirname, 'round3-female') },
];

function buildFemaleCases() {
  const cases = [];
  for (const { tag, dir } of ROUNDS) {
    const labels = JSON.parse(fs.readFileSync(path.join(dir, 'out', 'labels.json'), 'utf8'));
    const key = JSON.parse(fs.readFileSync(path.join(dir, 'out', 'key.json'), 'utf8'));
    const { PHOTOS } = require(path.join(dir, 'cases.js'));
    const byCase = new Map();
    for (const [k, label] of Object.entries(labels)) {
      const [caseId, letter] = k.split(':');
      const meta = key[k];
      if (!meta) throw new Error(`No key entry for ${tag} ${k}`);
      const file = path.join(dir, 'out', `${caseId}__${meta.model}__${meta.variant}.jpg`);
      if (!fs.existsSync(file)) throw new Error(`Missing image: ${file}`);
      const photoKey = caseId.split('__')[0];
      const id = `${tag}:${caseId}`;
      if (!byCase.has(caseId)) {
        byCase.set(caseId, {
          caseId: id,
          intensity: caseId.split('__')[1],
          photoFile: path.join(dir, 'photos', PHOTOS[photoKey].file),
          condition: PHOTOS[photoKey].condition,
          candidates: [],
          best: null,
        });
      }
      const c = byCase.get(caseId);
      const cand = {
        letter, model: meta.model, variant: meta.variant, file,
        best: !!label.best, acceptable: !!label.acceptable,
        tags: label.tags || [], note: label.note || '',
      };
      c.candidates.push(cand);
      if (cand.best) c.best = cand;
    }
    for (const c of byCase.values()) {
      c.candidates.sort((a, b) => a.letter.localeCompare(b.letter));
      // "Neither" row: Dan picked no best, but exactly one candidate is
      // acceptable — that is still a stated preference, used as a proxy pick.
      if (!c.best) {
        const acc = c.candidates.filter((x) => x.acceptable);
        if (acc.length === 1) { c.best = acc[0]; c.proxy = true; }
      }
      cases.push(c);
    }
  }
  return cases;
}

(async () => {
  const cases = buildFemaleCases();
  // With the tier fix on, the female-Subtle exemplar's own row is training data,
  // not eval data — hold it out of the run entirely (male-eval protocol).
  const scored = cases.filter((c) => c.best && !(TIER_FIX && c.caseId === FEMALE_SUBTLE_EXEMPLAR.caseId));
  console.log(`Female judge eval — model=${MODEL} fewShot=${USE_FEWSHOT} tierFix=${TIER_FIX}`);
  console.log(`${cases.length} labelled rows; ${scored.length} scoreable (${scored.filter((c) => c.proxy).length} via acceptable-proxy on "neither" rows)${TIER_FIX ? `; exemplar row ${FEMALE_SUBTLE_EXEMPLAR.caseId} held out` : ''}`);

  const pairJobs = [];
  for (const c of scored) {
    for (const other of c.candidates) {
      if (other.letter === c.best.letter) continue;
      pairJobs.push({ c, other });
    }
  }
  console.log(`Pairwise: ${pairJobs.length} pairings × 2 orders = ${pairJobs.length * 2} calls\n`);

  let done = 0;
  const pairResults = await pmap(pairJobs, 3, async ({ c, other }) => {
    const femaleSubtle = TIER_FIX && c.intensity === 'dramatic';
    const res = await scoreCandidates({
      model: MODEL,
      photoFile: c.photoFile,
      candidates: [c.best, other],
      useFewShot: USE_FEWSHOT,
      weights: femaleSubtle ? SUBTLE_WEIGHTS : WEIGHTS,
      tag: `pair-female|${c.caseId}|${c.best.letter}v${other.letter}`,
      femaleSubtle,
    });
    done++;
    console.log(`  ${done}/${pairJobs.length} ${c.caseId}`);
    return {
      caseId: c.caseId,
      intensity: c.intensity,
      condition: c.condition,
      proxy: !!c.proxy,
      bestLetter: c.best.letter, bestModel: c.best.model, bestNote: c.best.note, bestTags: c.best.tags,
      otherLetter: other.letter, otherModel: other.model, otherTags: other.tags, otherNote: other.note,
      preferredBest: res ? res.winner.letter === c.best.letter : null,
      orderDisagreement: res ? res.orderDisagreement : null,
      margin: res ? res.margin : null,
      scores: res ? res.ranked.map((m) => ({
        letter: m.letter, model: m.model, score: m.score,
        identity: m.identity, photoreal: m.photoreal, skin_tone: m.skin_tone,
        definition: m.definition, bulk: m.bulk, change: m.change,
        overshoot: m.overshoot || 0, notes: m.notes,
      })) : null,
    };
  });

  const score = (rows) => {
    const wins = rows.reduce((s, r) => s + (r.preferredBest === null ? 0.5 : r.preferredBest ? 1 : 0), 0);
    const perCase = {};
    for (const r of rows) {
      const c = (perCase[r.caseId] ||= { wins: 0, total: 0 });
      c.wins += r.preferredBest === null ? 0.5 : r.preferredBest ? 1 : 0;
      c.total++;
    }
    const caseAgree = Object.values(perCase).filter((c) => c.wins > c.total / 2).length;
    return {
      pairings: rows.length,
      pairwise: rows.length ? +(wins / rows.length).toFixed(4) : null,
      pairwiseRaw: `${wins.toFixed(1)}/${rows.length}`,
      caseLevel: Object.keys(perCase).length ? +(caseAgree / Object.keys(perCase).length).toFixed(4) : null,
      caseLevelRaw: `${caseAgree}/${Object.keys(perCase).length}`,
      flips: rows.filter((r) => r.orderDisagreement).length,
      flipRate: rows.length ? +(rows.filter((r) => r.orderDisagreement).length / rows.length).toFixed(4) : null,
    };
  };

  const summary = {
    model: MODEL, fewShot: USE_FEWSHOT, weights: WEIGHTS,
    all: score(pairResults),
    bestOnly: score(pairResults.filter((r) => !r.proxy)),
    subtle: score(pairResults.filter((r) => r.intensity === 'dramatic')),
    ripped: score(pairResults.filter((r) => r.intensity === 'max')),
  };

  fs.writeFileSync(path.join(__dirname, OUT), JSON.stringify({ summary, pairResults }, null, 2));

  const show = (name, s) => console.log(
    `${name.padEnd(28)} pairwise ${(s.pairwise * 100).toFixed(1)}% (${s.pairwiseRaw})   case-level ${(s.caseLevel * 100).toFixed(1)}% (${s.caseLevelRaw})   flips ${s.flips}/${s.pairings} (${(s.flipRate * 100).toFixed(1)}%)`);
  console.log('\n══════════ FEMALE JUDGE EVAL ══════════');
  show('ALL 14 rows (incl. proxy)', summary.all);
  show('12 true-best rows', summary.bestOnly);
  show('Subtle (dramatic) rows', summary.subtle);
  show('Ripped (max) rows', summary.ripped);
  console.log('\nMale baseline (held-out): pairwise 80.5%, case-level 100%, flips 13.8%');
  console.log('\nPer-pairing detail:');
  for (const r of pairResults) {
    const s = Object.fromEntries((r.scores || []).map((x) => [x.letter, x]));
    const fmt = (l, m) => s[l] ? `${m.split('-')[0]} ${s[l].score.toFixed(1)} (def ${s[l].definition} bulk ${s[l].bulk} chg ${s[l].change}${s[l].overshoot ? ` OVER ${s[l].overshoot}` : ''})` : '?';
    console.log(`  ${r.caseId.padEnd(28)} ${r.intensity === 'dramatic' ? 'Subtle' : 'Ripped'}  Dan=${r.bestModel.split('-')[0]}${r.proxy ? '(proxy)' : ''}  ${r.preferredBest ? 'HIT ' : 'MISS'}${r.orderDisagreement ? ' [flip]' : ''}  ${fmt(r.bestLetter, r.bestModel)} vs ${fmt(r.otherLetter, r.otherModel)}`);
  }
  console.log(`\nSaved → bakeoff/${OUT}`);
})();
