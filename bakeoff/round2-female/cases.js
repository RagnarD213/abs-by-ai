// Round-2 (female) grid: Gemini 2.5 Flash Image vs Seedream 4.5 on FEMALE photos.
//
// Only ONE distinct female identity exists in the proof assets — round-1's
// `heavier-female.jpg` is byte-for-byte the same subject as
// public/img/proof/female-before.webp, and female-after.webp is the same woman
// leaner. So the grid varies the two things we CAN vary honestly: the starting
// body state (heavier vs fit) and the declared start condition a real user would
// pick for that body (heavier vs moderate). Coverage gap is flagged to Dan.
const PHOTOS = {
  'fem-heavier':  { file: 'fem-before.jpg', condition: 'heavier',  desc: 'Female, softer build (proof asset) — declared HEAVIER (triggers the FEMALE HEAVIER REALISM RULE)' },
  'fem-moderate': { file: 'fem-before.jpg', condition: 'moderate', desc: 'Female, same photo — declared MODERATE (the tier most women self-select)' },
  'fem-fit':      { file: 'fem-after.jpg',  condition: 'fit',      desc: 'Female, already fit (proof asset) — the hard case: little fat left to lose' },
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
