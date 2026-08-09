// Round 8 — MODEL swap test for the male generation path.
//
// This is a MODEL question, not a prompt question. Three independent measured
// prompt attempts have now failed on male Gemini (denser ab language, the prose
// CALIBRATION RULE, the [[MARKER]]-scoped ab ladder, plus the magnitude restore
// of round 7). Every one of them was verified to reach the model on the wire and
// none changed its behaviour. So here the PROMPT IS HELD CONSTANT and the model
// varies.
//
// Prompt provenance — load-bearing, see verify-prompts.js:
//   Prompts are the EXACT byte-for-byte files from ../round5-prompt-ab/prompts/.
//   Those are the files that generated the already-Dan-labelled baseline Gemini
//   images being reused as the control arm, and the round-5 prompt era IS current
//   production (the ab ladder was reverted in feb94e0, the magnitude restore in
//   92c7e77). Reusing the bytes rather than re-calling /api/generate-prompt
//   removes prompt stochasticity as a confound entirely: every arm in every row
//   sees literally the same characters.
//
// Naming: this is "round 8" and not the handoff's "round7-male-model-swap"
// because bakeoff/ already holds round7-magnitude-restore and round7-male-magnitude.
const PHOTOS = {
  'lean-male':     { file: 'lean-male.jpg',     gender: 'male', condition: 'very_lean', desc: 'Lean athletic male (proof asset)' },
  'moderate-male': { file: 'moderate-male.jpg', gender: 'male', condition: 'moderate',  desc: 'Average male (proof asset) - the modal male user' },
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

// ── Arms ─────────────────────────────────────────────────────────────────────
// `baseline: true` means the image already exists on disk and is NEVER
// regenerated (it is Dan-labelled round-5 output). Cost of that arm is $0.
//
// `variant` is the prompt each model would actually receive if it took the
// GEMINI ANCHOR slot in production. Gemini's anchor role receives the FULL
// prompt; Seedream cannot (hard 4000-char API ceiling, and male full prompts run
// 4,027-6,472 chars), so it necessarily gets the condensed one. That asymmetry
// is a real property of the candidate and is recorded rather than hidden.
const ARMS = [
  {
    modelKey: 'gemini-2.5-flash-image', variant: 'full', baseline: true,
    label: 'Gemini 2.5 Flash Image (current production anchor)',
    // Reuse path in ../round5-prompt-ab/out — its files are suffixed by variant.
    reuseSuffix: 'full',
  },
  { modelKey: 'gemini-3.1-flash-image', variant: 'full',      label: 'Nano Banana 2 (gemini-3.1-flash-image, GA)' },
  { modelKey: 'gemini-3-pro-image',     variant: 'full',      label: 'Nano Banana Pro (gemini-3-pro-image, GA)' },
  { modelKey: 'seedream-4.5',           variant: 'condensed', label: 'Seedream 4.5 (already integrated as callSeedream)' },
];

const CHALLENGERS = ARMS.filter((a) => !a.baseline);

module.exports = { PHOTOS, INTENSITIES, CASES, ARMS, CHALLENGERS };
