// Round-5 grid: condensed-vs-full PROMPT A/B, re-run after the tan-block removal
// + muscle-anchor halving (14b4790) and the female Subtle retune (d948f93) removed
// exactly the language the condensed variant was already dropping.
//
// What is being compared is the PROMPT VARIANT with the MODEL HELD CONSTANT, so
// every gallery row is a clean paired vote (full vs condensed on one model, one
// photo, one tier) with no model-identity confound.
//
// Why the arms are asymmetric — a structural fact, measured, not assumed:
// every assembled full prompt runs 4.9-5.5k chars, and Seedream hard-rejects
// anything over 4000 with a 422. So the FEMALE challenger leg *cannot* receive
// the full prompt at all; it is condensed-only by construction. The male
// challenger (FLUX Kontext) has no such ceiling but is already sent condensed by
// design choice. That leaves the GEMINI leg as the only place where the full
// prompt is actually in use and where "replace full with condensed" is a
// shippable change -- so Gemini is the primary arm, on every case.
const PHOTOS = {
  // Male — the three body types the handoff asks for. Committed proof assets
  // plus round-1 normalised copies.
  'lean-male':        { file: 'lean-male.jpg',        gender: 'male',   condition: 'very_lean', desc: 'Lean athletic male (proof asset) - little fat left to lose; the case where added-muscle language matters most' },
  'moderate-male':    { file: 'moderate-male.jpg',    gender: 'male',   condition: 'moderate',  desc: 'Average male (proof asset) - the modal male user' },
  'heavier-male':     { file: 'heavier-male.jpg',     gender: 'male',   condition: 'heavier',   desc: 'Heavier male (proof asset) - the Gemini ceiling case' },

  // Female — moderate / lean / heavier, matching the handoff's coverage ask.
  // Real private individuals; see .gitignore.
  'fem-moderate':     { file: 'fem-moderate.jpg',     gender: 'female', condition: 'moderate',  desc: 'Woman, average build, medium skin tone, indoor - the tier most women self-select' },
  'fem-lean-real':    { file: 'fem-lean-real.jpg',    gender: 'female', condition: 'fit',       desc: 'Woman, already lean, pale skin, studio daylight - little fat left to lose' },
  'fem-dark-heavier': { file: 'fem-dark-heavier.jpg', gender: 'female', condition: 'heavier',   desc: 'Woman, dark skin tone, heavier build - hardest case for every model' },

  // Held in reserve: a second moderate woman under hard outdoor light. Not in the
  // headline grid (fem-moderate already covers the tier); available as a drop-in
  // if a Gemini cell blocks non-deterministically and a row is lost.
  'fem-pale':         { file: 'fem-pale.jpg',         gender: 'female', condition: 'moderate',  reserve: true, desc: 'Woman, average build, pale skin, outdoor beach daylight - hard lighting (reserve)' },
};

// Production only offers two intensities: Subtle = `dramatic`, Ripped = `max`.
// Subtle is the freshly retuned tier for women, so both tiers are in scope.
const INTENSITIES = [
  { key: 'dramatic', label: 'Subtle' },
  { key: 'max',      label: 'Ripped' },
];

const CASES = [];
for (const [pkey, p] of Object.entries(PHOTOS)) {
  for (const i of INTENSITIES) {
    CASES.push({
      id: `${pkey}__${i.key}`,
      photoKey: pkey, ...p,
      intensity: i.key, intensityLabel: i.label,
    });
  }
}

// Which model each case's A/B runs on.
//   set 1 (primary)  - Gemini, every case. The leg whose prompt would change.
//   set 2 (control)  - FLUX Kontext, male cases only. Tests whether a condensed
//                      advantage is model-specific. Seedream cannot take the full
//                      prompt (>4000 chars = 422), so there is no female control.
const VARIANTS = ['full', 'condensed'];

function armsFor(c) {
  const arms = [{ modelKey: 'gemini-2.5-flash-image', set: 1 }];
  if (c.gender === 'male') arms.push({ modelKey: 'flux-kontext-pro', set: 2 });
  return arms;
}

// The model that would actually serve this case's challenger leg in production.
// Recorded for the write-up; not run with the full prompt (see header).
const CHALLENGER = { male: 'flux-kontext-pro', female: 'seedream-4.5' };

const MAX_SEEDREAM_CHARS = 4000;

module.exports = { PHOTOS, INTENSITIES, CASES, VARIANTS, armsFor, CHALLENGER, MAX_SEEDREAM_CHARS };
