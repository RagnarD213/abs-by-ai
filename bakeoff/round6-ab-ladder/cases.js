// Round-6: OLD prompt vs NEW prompt (ab-visibility anchor ladder, commit
// 4e4f4d1), model held constant per row — the round4-female-retune shape.
//
// Scope is MALE only, by design: the ladder leaves female prompts
// byte-identical to the pre-ladder assembly (asserted, 32 combos), so female
// rows would compare a prompt against itself.
//
//   set 1 (primary)   — Gemini, full prompt. The leg the ladder targets:
//                       Gemini under-changed 19/24 male candidates in round 5.
//   set 2 (secondary) — FLUX Kontext, condensed prompt. The rung sentence
//                       lands in the directive paragraph so it survives
//                       condenseForKontext; this set shows whether it pushes
//                       FLUX (which already over-changes 8/12) further over.
//
// OLD arm images come from ../round5-prompt-ab/out (Dan's labelled round-5
// set); only the NEW arm is generated. No deviceId on any call, ever.
const PHOTOS = {
  'lean-male':     { file: 'lean-male.jpg',     gender: 'male', condition: 'very_lean', desc: 'Lean athletic male (proof asset) - round 5: BOTH candidates rejected at both tiers' },
  'moderate-male': { file: 'moderate-male.jpg', gender: 'male', condition: 'moderate',  desc: 'Average male (proof asset) - the modal male user' },
  'heavier-male':  { file: 'heavier-male.jpg',  gender: 'male', condition: 'heavier',   desc: 'Heavier male (proof asset) - now capped one ab rung lower (AB2/AB3)' },
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
