// Round-7: CURRENT-PRODUCTION prompt (old) vs MAGNITUDE-RESTORED prompt (new),
// model held constant per row — the round-4/5/6 shape.
//
// The restore is commit 9ee1320: male muscle anchors back to +5/+8/+12/+15 lb
// and the "visibly BIGGER" verbs back, keeping 14b4790's no-tan rule and
// no-bodybuilder ceiling. See AI_COORDINATION.md, "WE CAUSED THE MALE GEMINI
// REGRESSION OURSELVES", for why this is the lever.
//
// Scope is MALE only, by design: the restore leaves female prompts
// byte-identical to HEAD (asserted, all 16 female combos), so female rows
// would compare a prompt against itself.
//
//   set 1 (primary)   — Gemini, full prompt. The leg the restore targets:
//                       Dan rejected BOTH candidates in 6 of 6 male Gemini
//                       rows in round 6, every one tagged "not enough change".
//   set 2 (control)   — FLUX Kontext, condensed prompt. The magnitude sentence
//                       lands in the directive paragraph so it survives
//                       condenseForKontext; this set shows whether the restore
//                       pushes FLUX (which already over-changes men 8/12)
//                       further into "too muscular". Production sends the
//                       condensed prompt to FLUX, so the restore ships to both
//                       legs or neither.
//
// OLD arm images come from ../round5-prompt-ab/out — Dan's labelled round-5
// set, generated under the prompt that is live in production today (the
// ab-ladder was reverted in feb94e0, so round 5 == current production).
// Only the NEW arm is generated. No deviceId on any call, ever.
const PHOTOS = {
  'lean-male':     { file: 'lean-male.jpg',     gender: 'male', condition: 'very_lean', desc: 'Lean athletic male (proof asset)' },
  'moderate-male': { file: 'moderate-male.jpg', gender: 'male', condition: 'moderate',  desc: 'Average male (proof asset)' },
  'heavier-male':  { file: 'heavier-male.jpg',  gender: 'male', condition: 'heavier',   desc: 'Heavier male (proof asset)' },
};

const INTENSITIES = [
  { key: 'dramatic', label: 'Subtle' },
  { key: 'max',      label: 'Ripped' },
];

const CASES = [];
for (const [pkey, p] of Object.entries(PHOTOS)) {
  for (const i of INTENSITIES) {
    CASES.push({ id: `${pkey}__${i.key}`, photoKey: pkey, ...p, intensity: i.key, intensityLabel: i.label });
  }
}

// modelKey -> which prompt variant that leg receives in production.
const ARMS = [
  { modelKey: 'gemini-2.5-flash-image', variant: 'full',      set: 1 },
  { modelKey: 'flux-kontext-pro',       variant: 'condensed', set: 2 },
];

module.exports = { PHOTOS, INTENSITIES, CASES, ARMS };
