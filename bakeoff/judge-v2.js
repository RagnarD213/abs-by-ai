// Phase 3 — the rebuilt judge.
//
// Design changes vs the production judge:
//   1. Per-candidate 1–5 rubric scores instead of a bare winner. Scores compose
//      across N candidates and the tie-break lives in OUR code, not the model's.
//   2. The aesthetic target is Dan's, not "more muscular": shredded/defined at
//      low body fat, NO added tan, natural not airbrushed, athletic NOT
//      bodybuilder. Muscularity beyond athletic is an explicit DEMERIT.
//   3. Position-bias control: every comparison runs twice with the order
//      swapped; the scores are averaged and an order disagreement IS the
//      "close margin" signal.
//   4. Few-shot vision exemplars built from Dan's own labelled best/rejected
//      pairs, with his one-line reasons. Exemplar cases are held out of the
//      headline eval.
const path = require('path');
const { imageBlock, anthropic, parseJson } = require('./judge-lib');

// ── few-shot exemplars (3 cases, held out of the headline eval) ──────────────
// Each: BEFORE photo, Dan's best pick, one candidate he rejected, his reason.
const EXEMPLAR_CASE_IDS = ['dan-real__dramatic', 'moderate-male__max', 'heavier-female__max'];

const EXEMPLARS = [
  {
    caseId: 'dan-real__dramatic',
    photo: 'dan-real.jpg',
    good: 'dan-real__dramatic__seedream-4.5__condensed.jpg',
    bad: 'dan-real__dramatic__gpt-image-1.5__condensed.jpg',
    goodWhy: 'CHOSEN: the most ab definition of any candidate while staying natural — skin tone identical to the BEFORE, no bronzing, no oil sheen, and the frame is still an ordinary fit guy rather than a bodybuilder.',
    badWhy: 'REJECTED: too muscular — chest, delts and arms are inflated well past athletic — and the whole image reads fake/rendered rather than like a real photo of this man.',
  },
  {
    caseId: 'moderate-male__max',
    photo: 'moderate-male.jpg',
    good: 'moderate-male__max__gpt-image-1.5__condensed.jpg',
    bad: 'moderate-male__max__seedream-4.5__condensed.jpg',
    goodWhy: 'CHOSEN: exactly right — clearly leaner with a real six-pack, skin tone unchanged from the BEFORE, and the added muscle stays in athletic proportion.',
    badWhy: 'REJECTED: three faults at once — not enough actual change from the BEFORE, skin has been warmed/bronzed, and what muscle was added is overblown.',
  },
  {
    caseId: 'heavier-female__max',
    photo: 'heavier-female.jpg',
    good: 'heavier-female__max__gpt-image-1.5__condensed.jpg',
    bad: 'heavier-female__max__flux-2-pro__full.jpg',
    goodWhy: 'CHOSEN: the most ab definition available without becoming excessively muscular or tan; still unmistakably her, still feminine.',
    badWhy: 'REJECTED: muscled far past what was asked for, and the skin has been given a tan the BEFORE photo does not have.',
  },
];

const IMG = path.join(__dirname, 'round1', 'images');
const PHOTO = path.join(__dirname, 'round1', 'photos');
const EXEMPLAR_EDGE = 768; // exemplars calibrate; they don't need full res

// ── the judging spec ─────────────────────────────────────────────────────────
const SYSTEM = `You are the quality judge for an AI fitness-transformation product. Users upload a photo of themselves and the product returns an edited photo of how they could look after getting in shape. Your job is to pick the candidate edit the product owner would ship.

The product owner has labelled hundreds of candidates. His taste is specific and it is NOT "the most dramatic transformation wins". The target physique is a lean, shredded, natural athlete — sometimes called a "Kino" build:

- VERY LOW body fat with a sharply cut, clearly separated six-pack, visible obliques, a tight waist and a V-taper. Ab definition is the single most valuable quality.
- Muscle volume stays ATHLETIC. Added size beyond a lean athlete — inflated chest, capped/boulder delts, blown-up arms, flared lats, bodybuilder or comic-book mass — is a DEMERIT, not a win. His most common complaint by far is "too muscular".
- SKIN TONE MUST MATCH THE BEFORE PHOTO EXACTLY. Any added tan, bronzing, warming, darkening or golden cast is a serious fault, even when it makes the abs pop. His second most common complaint is "too tan".
- The result must look like a REAL UNRETOUCHED PHOTOGRAPH of that same person: natural skin texture, natural lighting, dry skin. Airbrushed/plastic/CGI/rendered looks, and oiled or wet-looking skin, are faults. His third most common complaint is "looks fake".
- It must still be CLEARLY CHANGED from the BEFORE. A result that could be mistaken for the original is a failure ("not enough change"). But magnitude is subordinate to the aesthetic above: overshooting into bodybuilder mass is worse than undershooting slightly.

Score each candidate independently on these dimensions. Use the FULL 1–5 range; do not cluster everything at 3–4.

identity  — "good" (clearly the same person, same face), "borderline" (mostly them but the face is subtly off), "broken" (a different person, or distorted/artifact-ridden).

photoreal (1–5) — 5 = indistinguishable from a real unretouched photo; 3 = slightly processed but plausible; 1 = obviously AI-generated, plastic, airbrushed, rendered or uncanny. Oiled/wet/sweaty skin caps this at 3.

skin_tone (1–5) — 5 = skin colour and warmth are identical to the BEFORE; 4 = a barely perceptible shift; 3 = noticeably warmer or more bronzed; 1 = obviously tanned, golden or darkened versus the BEFORE. Judge the skin ONLY, ignoring how lighting affects muscle shadow.

definition (1–5) — 5 = sharply cut, deeply separated six-pack with visible obliques and a tight waist; 3 = some visible ab outline; 1 = soft midsection, no ab separation.

bulk (1–5) — how much muscle VOLUME the body carries relative to the BEFORE. 1 = same frame as the BEFORE, no added size; 2 = slightly fuller, natural; 3 = lean athlete / fitness model — THIS IS THE TARGET; 4 = noticeably bigger than a lean athlete, heading toward bodybuilder; 5 = bodybuilder or comic-book mass. Higher is NOT better. 4 and 5 are faults.

change (1–5) — how clearly different from the BEFORE. 5 = unmistakably transformed; 3 = clearly different on a close look; 1 = could be mistaken for the BEFORE photo.

Reply with ONLY a JSON object, no other text:
{"candidates":[{"id":"A","identity":"good|borderline|broken","photoreal":1-5,"skin_tone":1-5,"definition":1-5,"bulk":1-5,"change":1-5,"note":"one short clause"}, ...]}
Include one entry per candidate shown, keyed by the letter label given.`;

// ── few-shot block (stable prefix → prompt-cached) ───────────────────────────
function exemplarBlocks() {
  const blocks = [{
    type: 'text',
    text: 'Before you judge, here are worked examples of the product owner\'s actual choices. Each shows a BEFORE photo, the candidate he chose, and a candidate he rejected, with his reason. Calibrate your scores so that his chosen images score highest.',
  }];
  for (const [i, ex] of EXEMPLARS.entries()) {
    blocks.push({ type: 'text', text: `EXAMPLE ${i + 1} — BEFORE photo:` });
    blocks.push(imageBlock(path.join(PHOTO, ex.photo), EXEMPLAR_EDGE));
    blocks.push({ type: 'text', text: `EXAMPLE ${i + 1} — the candidate he CHOSE:` });
    blocks.push(imageBlock(path.join(IMG, ex.good), EXEMPLAR_EDGE));
    blocks.push({ type: 'text', text: ex.goodWhy });
    blocks.push({ type: 'text', text: `EXAMPLE ${i + 1} — a candidate he REJECTED:` });
    blocks.push(imageBlock(path.join(IMG, ex.bad), EXEMPLAR_EDGE));
    blocks.push({ type: 'text', text: ex.badWhy });
  }
  const last = blocks[blocks.length - 1];
  last.cache_control = { type: 'ephemeral' }; // caches system + all exemplars
  return blocks;
}
let EXEMPLAR_BLOCKS = null;

const LETTERS = 'ABCDEFGHIJKL'.split('');

// One scoring call over N candidates in a fixed order. Returns per-letter rubric.
async function scoreOnce({ model, photoFile, candFiles, useFewShot, tag }) {
  const content = [];
  if (useFewShot) {
    EXEMPLAR_BLOCKS = EXEMPLAR_BLOCKS || exemplarBlocks();
    content.push(...EXEMPLAR_BLOCKS);
  }
  content.push({ type: 'text', text: 'Now judge this case.\n\nBEFORE photo (the real person):' });
  content.push(imageBlock(photoFile));
  candFiles.forEach((f, i) => {
    content.push({ type: 'text', text: `Candidate ${LETTERS[i]}:` });
    content.push(imageBlock(f));
  });
  content.push({ type: 'text', text: `Score all ${candFiles.length} candidate(s) (${candFiles.map((_, i) => LETTERS[i]).join(', ')}) on the rubric. JSON only.` });

  const { text } = await anthropic({
    model,
    maxTokens: 8000,
    system: SYSTEM,
    content,
    cacheKey: `judge-v2|v4|${model}|${useFewShot ? 'fs' : 'nofs'}|${tag}|${photoFile}|${candFiles.join('|')}`,
  });
  const raw = parseJson(text);
  if (!raw || !Array.isArray(raw.candidates)) return null;
  const out = {};
  const clamp = (x) => (Number.isFinite(+x) ? Math.min(5, Math.max(1, Math.round(+x))) : 3);
  for (const c of raw.candidates) {
    const letter = String(c?.id || '').trim().toUpperCase();
    if (!LETTERS.includes(letter)) continue;
    out[letter] = {
      identity: ['good', 'borderline', 'broken'].includes(c.identity) ? c.identity : 'borderline',
      photoreal: clamp(c.photoreal),
      skin_tone: clamp(c.skin_tone),
      definition: clamp(c.definition),
      bulk: clamp(c.bulk),
      change: clamp(c.change),
      note: typeof c.note === 'string' ? c.note.slice(0, 160) : '',
    };
  }
  return out;
}

// Score a set of candidates with the position-bias swap: run forward, run
// reversed, average each candidate's dimension scores across the two runs.
// `orderDisagreement` is true when the two runs pick different winners.
async function scoreCandidates({ model, photoFile, candidates, useFewShot = true, weights = DEFAULT_WEIGHTS, tag = '' }) {
  const files = candidates.map((c) => c.file);
  const rev = [...files].reverse();
  const [fwd, bwd] = await Promise.all([
    scoreOnce({ model, photoFile, candFiles: files, useFewShot, tag: `${tag}|fwd` }),
    scoreOnce({ model, photoFile, candFiles: rev, useFewShot, tag: `${tag}|rev` }),
  ]);
  if (!fwd && !bwd) return null;

  const n = candidates.length;
  const merged = candidates.map((cand, i) => {
    const a = fwd ? fwd[LETTERS[i]] : null;              // forward position i
    const b = bwd ? bwd[LETTERS[n - 1 - i]] : null;      // reversed position
    const runs = [a, b].filter(Boolean);
    if (!runs.length) return null;
    const avg = (k) => runs.reduce((s, r) => s + r[k], 0) / runs.length;
    const identity = runs.some((r) => r.identity === 'broken') ? 'broken'
      : runs.every((r) => r.identity === 'good') ? 'good' : 'borderline';
    return {
      ...cand,
      identity,
      photoreal: avg('photoreal'),
      skin_tone: avg('skin_tone'),
      definition: avg('definition'),
      bulk: avg('bulk'),
      change: avg('change'),
      notes: runs.map((r) => r.note).filter(Boolean),
      runs: { fwd: a, bwd: b },
    };
  });
  if (merged.some((m) => !m)) return null;

  for (const m of merged) m.score = composite(m, weights);

  const rank = (list) => [...list].sort((x, y) => y.score - x.score);
  const winnerOf = (src) => {
    if (!src) return null;
    const scored = candidates.map((cand, i) => {
      const r = src[LETTERS[i]] !== undefined ? src[LETTERS[i]] : null;
      return r ? { letter: cand.letter, score: composite(r, weights) } : null;
    }).filter(Boolean);
    return scored.length ? rank(scored)[0].letter : null;
  };
  // per-run winners for the position-bias signal (reversed run needs remapping)
  const bwdRemap = bwd ? Object.fromEntries(candidates.map((c, i) => [LETTERS[i], bwd[LETTERS[n - 1 - i]]])) : null;
  const wFwd = winnerOf(fwd);
  const wBwd = winnerOf(bwdRemap);

  const ranked = rank(merged);
  const alive = ranked.filter((m) => m.identity !== 'broken');
  const pool = alive.length ? alive : ranked;
  return {
    ranked: pool,
    winner: pool[0],
    orderDisagreement: !!(wFwd && wBwd && wFwd !== wBwd),
    margin: pool.length > 1 ? +(pool[0].score - pool[1].score).toFixed(3) : null,
  };
}

// ── composite: maximize definition subject to the fault penalties ────────────
const DEFAULT_WEIGHTS = {
  definition: 2.0,
  skin: 1.0,
  photoreal: 1.0,
  change: 0.6,
  bulkPenalty: 2.5,   // per point of bulk above the athletic target (3)
  underPenalty: 1.5,  // per point of change below 3 ("not enough change")
  borderlineId: 2.0,
};

function composite(m, w = DEFAULT_WEIGHTS) {
  let s = w.definition * m.definition
    + w.skin * m.skin_tone
    + w.photoreal * m.photoreal
    + w.change * m.change
    - w.bulkPenalty * Math.max(0, m.bulk - 3)
    - w.underPenalty * Math.max(0, 3 - m.change);
  if (m.identity === 'borderline') s -= w.borderlineId;
  if (m.identity === 'broken') s -= 100;
  return +s.toFixed(3);
}

module.exports = { scoreCandidates, scoreOnce, composite, DEFAULT_WEIGHTS, EXEMPLAR_CASE_IDS, SYSTEM };
