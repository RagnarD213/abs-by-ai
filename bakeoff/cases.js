// Round-1 test grid: 6 photos × 2 intensities (Subtle = `dramatic`, Ripped = `max`).
const PHOTOS = {
  'lean-male':         { file: 'lean-male.jpg',         gender: 'male',   condition: 'very_lean', desc: 'Lean athletic male (proof asset) — the hard case: little fat left to lose' },
  'moderate-male':     { file: 'moderate-male.jpg',     gender: 'male',   condition: 'moderate',  desc: 'Average male (proof asset)' },
  'heavier-male':      { file: 'heavier-male.jpg',      gender: 'male',   condition: 'heavier',   desc: 'Heavier male (proof asset) — the Gemini ceiling case' },
  'heavier-female':    { file: 'heavier-female.jpg',    gender: 'female', condition: 'heavier',   desc: 'Heavier female (proof asset) — moderation + ceiling case' },
  'dan-real':          { file: 'dan-real.jpg',          gender: 'male',   condition: 'fit',       desc: 'Real phone photo, fit male, outdoor daylight' },
  'heavier-male-dark': { file: 'heavier-male-dark.jpg', gender: 'male',   condition: 'heavier',   desc: 'Heavier male, dark skin tone, studio — skin-tone fidelity test' },
};

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

module.exports = { PHOTOS, INTENSITIES, CASES };
