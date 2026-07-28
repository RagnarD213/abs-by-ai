// Round-3 (female) grid: Gemini 2.5 Flash Image vs Seedream 4.5 on THREE
// distinct women — the identity/skin-tone coverage round 2 could not provide.
//
// Dan authorized both new photos on 2026-07-27. They are real, identifiable
// private individuals, so neither the sources nor the generated outputs are
// committed to the public repo (see .gitignore).
const PHOTOS = {
  'fem-dark-heavier': { file: 'fem-dark-heavier.jpg', condition: 'heavier',  desc: 'Woman, dark skin tone, heavier build - the case round 1 found hardest for every model, and where Seedream is claimed strongest' },
  'fem-moderate':     { file: 'fem-moderate.jpg',     condition: 'moderate', desc: 'Woman, average build, medium skin tone, indoor (proof asset) - the tier most women self-select' },
  'fem-pale':         { file: 'fem-pale.jpg',         condition: 'moderate', desc: 'Woman, average build, pale skin, outdoor beach daylight - real photo, hard lighting' },
  // EXCLUDED 2026-07-28: Dan identified this "before" as itself AI-generated, so
  // it tests the models on synthetic input rather than a real photo. Images stay
  // on disk but are kept out of the gallery; a real lean subject replaces her.
  'fem-lean':         { file: 'fem-lean.jpg',         condition: 'fit',      excluded: true, desc: 'Woman, already lean (AI-generated before - EXCLUDED)' },
};

// Production only offers two intensities: Subtle = `dramatic`, Ripped = `max`.
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
      gender: 'female',
      intensity: i.key, intensityLabel: i.label,
    });
  }
}

// Mirrors production's legs: Gemini gets the full prompt, the challenger the
// condensed one (Seedream hard-rejects >4000 chars).
const MODEL_VARIANTS = [
  { modelKey: 'gemini-2.5-flash-image', variant: 'full' },
  { modelKey: 'seedream-4.5',           variant: 'condensed' },
];

module.exports = { PHOTOS, INTENSITIES, CASES, MODEL_VARIANTS };
