'use strict';
//
// YTADS LINT — the hard compliance gate on every auto-written headline.
//
// Built from memory `ad-suspension-prevention` (the 2026-08-09 suspension of account
// 342-717-0837) and the 8/11 copy fixes. A line that fails here is NEVER used; the
// generator regenerates, and if it still fails the ad is not created and the morning
// brief shows the failing text. Conservative beats clever: this account carries prior
// suspensions on Dan's identity, so boring copy is the margin.
//
// The rule: sell the VIDEO and the visualization, never the viewer's body.
//
// Exports: lintLine(text, kind) → { ok, reasons:[] }
//          lintSet({headlines, longHeadlines, descriptions}) → { ok, failures:[{kind,text,reasons}] }
//          LIMITS, RULES (for the prompt and the tests)

const LIMITS = { headline: 40, longHeadline: 90, description: 90 };

// Each rule: id, test(text) → true when it FAILS, and a human reason.
const RULES = [
  // ── physical-result promises ────────────────────────────────────────────
  { id: 'result-promise',
    re: /\b(get|gets|got|build|builds|reveal|reveals|unlock|earn|achieve|finally have|have)\s+(real\s+|visible\s+|actual\s+|your\s+)?(abs|a six[- ]?pack|six[- ]?pack abs|a sixpack|sixpack abs|a flat stomach|a lean body|ripped|shredded|defined abs)\b/i,
    reason: 'promises a physical result ("get abs" / "six pack")' },
  { id: 'make-real',
    re: /\bmake\s+(them|it|those|these|your abs|the abs|your body|my abs)\s+(real|happen|permanent|show)\b/i,
    reason: '"make them real" result promise' },
  { id: 'result-verbs',
    re: /\b(lose|losing|lost|burn|burns|burning|melt|melts|melting|shred|shreds|shredded|shredding|torch|torching|drop|dropping)\b\s*(\d+|the|your|belly|body|stubborn|fat|weight|pounds|lbs|kg|inches)?/i,
    reason: 'weight-loss / fat-burn result verb' },
  { id: 'transform',
    re: /\btransform(s|ed|ing|ation)?\s+(your|the|my|his|her)?\s*(body|physique|life|self)?\b/i,
    reason: '"transform your body" language' },
  { id: 'real-results',
    re: /\b(real|guaranteed|proven|actual|visible)\s+results?\b/i,
    reason: '"real results" claim' },
  { id: 'body-superlative',
    re: /\b(ripped|shredded|jacked|lean|toned|sculpted|chiseled|defined)\s+(body|physique|abs|core|stomach|you)\b/i,
    reason: 'superlative about the viewer\'s body' },
  // ── timeframes ──────────────────────────────────────────────────────────
  { id: 'timeframe',
    re: /\b(in|within|under|just)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten|twelve|thirty|sixty|ninety|a|an)\s*(-|\s)?(day|days|week|weeks|month|months|minute workout)s?\b|\b(\d+)[- ](day|week|month)\s+(challenge|plan|program|shred|transformation)\b|\bby (summer|christmas|new year)/i,
    reason: 'result timeframe ("in 30 days")' },
  // ── before / after ──────────────────────────────────────────────────────
  { id: 'before-after',
    re: /\bbefore\s*(&|and|\/|→|-)\s*after\b|\bbefore\/after\b|\bafter photo|\bbefore photo|\bmy transformation\b/i,
    reason: 'before/after language' },
  // ── disease / drug / medication names ───────────────────────────────────
  { id: 'medical',
    re: /\b(zepbound|ozempic|wegovy|mounjaro|tirzepatide|semaglutide|glp[- ]?1|retatrutide|testosterone|trt|steroids?|sarms?|clenbuterol|phentermine|metformin|insulin|diabetes|diabetic|obesity|obese|hypertension|depression|anxiety|adhd|cancer|disease|prescription|medication|meds|drug|drugs|dose|dosage|inject(ion|ing|ed)?|shot)\b/i,
    reason: 'names a drug, medication, injection or condition' },
  // ── guarantees / marks ──────────────────────────────────────────────────
  { id: 'guarantee', re: /\bguarantee[sd]?\b|\bpromise[sd]?\b|\bno[- ]fail\b|\bfoolproof\b/i, reason: '"guaranteed"' },
  { id: 'marks', re: /[®™©]/, reason: 'contains ® / ™ / ©' },
  // ── negative self-image ─────────────────────────────────────────────────
  { id: 'negative-self',
    re: /\b(out of shape|fat|overweight|chubby|flabby|embarrass(ing|ed|ment)|humiliat(ing|ed|ion)|ugly|gross|disgusting|dad bod|beer belly|belly fat|love handles|skinny[- ]fat|lazy|ashamed|shame|hate your|hate my|hiding your|hide your)\b/i,
    reason: 'negative self-image phrasing' },
  // ── formatting ──────────────────────────────────────────────────────────
  { id: 'exclamation', re: /!/, reason: 'exclamation mark' },
  { id: 'all-caps', test: (t) => { const words = t.match(/[A-Za-z]{3,}/g) || []; return words.some(w => w === w.toUpperCase() && !ALLOWED_CAPS.has(w)); },
    reason: 'all-caps word' },
  { id: 'quotes', re: /["“”]/, reason: 'quotation marks' },
  { id: 'urls', re: /https?:\/\/|www\.|\.com\b/i, reason: 'URL in copy' },
  { id: 'emoji', re: /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u, reason: 'emoji' },
  { id: 'empty', test: (t) => !t.trim(), reason: 'empty' },
];

// Brand and acronym words allowed in caps.
const ALLOWED_CAPS = new Set(['AI', 'GLP', 'USA', 'UK', 'DIY', 'TV', 'PDF', 'FAQ', 'HIIT', 'IQ', 'OK']);

function lintLine(text, kind = 'headline') {
  const t = String(text == null ? '' : text).replace(/\s+/g, ' ').trim();
  const reasons = [];
  const limit = LIMITS[kind] || LIMITS.headline;
  if (t.length > limit) reasons.push(`over ${limit} characters (${t.length})`);
  for (const r of RULES) {
    const failed = r.re ? r.re.test(t) : r.test(t);
    if (failed) reasons.push(r.reason);
  }
  return { ok: reasons.length === 0, reasons, text: t };
}

function lintSet(set) {
  const failures = [];
  const groups = [['headline', set.headlines], ['longHeadline', set.longHeadlines], ['description', set.descriptions]];
  for (const [kind, arr] of groups) {
    for (const text of (arr || [])) {
      const r = lintLine(text, kind);
      if (!r.ok) failures.push({ kind, text: r.text, reasons: r.reasons });
    }
  }
  return { ok: failures.length === 0, failures };
}

// Filter a set down to its passing lines. Used after the generator has had its
// retries: a failing line is dropped, never used.
function passingOnly(set) {
  const keep = (arr, kind) => (arr || []).map(t => lintLine(t, kind)).filter(r => r.ok).map(r => r.text);
  return {
    headlines: keep(set.headlines, 'headline'),
    longHeadlines: keep(set.longHeadlines, 'longHeadline'),
    descriptions: keep(set.descriptions, 'description'),
  };
}

// Plain-English rules for the generator prompt — kept next to the regexes so
// the two cannot drift apart.
const RULES_TEXT = [
  'Sell the VIDEO (what the viewer will see) and the AI visualization — never the viewer\'s body or a result.',
  'No physical-result promises: no "get abs", "get a six pack", "lose", "burn", "shred", "transform your body", "real results".',
  'No timeframes: no "in 30 days", "in 2 weeks", "by summer".',
  'No before/after language, no "transformation".',
  'No disease, drug, medication, injection or condition names of any kind (no Zepbound, Ozempic, GLP-1, testosterone, diabetes, depression). A video about a medication gets a headline about its TOPIC without naming the drug.',
  'No "guaranteed", "proven", "promise". No ® ™ © symbols.',
  'No superlatives about the viewer\'s body (ripped, shredded, toned, lean body).',
  'No negative self-image phrasing (out of shape, fat, belly fat, embarrassing, dad bod).',
  'No exclamation marks, no ALL-CAPS words (AI is fine), no quotation marks, no URLs, no emoji.',
  `Headlines ≤ ${LIMITS.headline} characters. Long headlines and descriptions ≤ ${LIMITS.longHeadline} characters.`,
];

module.exports = { lintLine, lintSet, passingOnly, LIMITS, RULES, RULES_TEXT };
