// SL-04 plan: the shot list is planned in plan_shots.py (output-time, frame-quantised) and
// written to shots/manifest.json. This module only exposes it plus the titles.
const path = require('path');
const fs = require('fs');
const { SEGMENTS } = require('./segments.js');

// Benefit-first; the headline names the thing for someone who never saw the long-form.
const META = {
  A: { eyebrow: 'TRAIN YOUR SHOULDERS', title: 'MAKE YOUR WAIST\nLOOK SMALLER' },
  C: { eyebrow: 'SIDE LATERAL RAISES', title: 'RAISE YOUR ELBOWS,\nNOT YOUR HANDS' },
  K: { eyebrow: 'BICEP CURL MISTAKE', title: 'STOP SWINGING\nYOUR CURLS' },
  H: { eyebrow: '2 WAYS TO DO THEM', title: 'HOW TO DO\nBICEP CURLS' },
  F: { eyebrow: '2-MINUTE HOME ARM WORKOUT', title: 'DO THIS BEFORE YOU\nTAKE YOUR SHIRT OFF' },
};

function loadShots() {
  return JSON.parse(fs.readFileSync(path.join(__dirname, 'shots', 'manifest.json'), 'utf8'));
}
module.exports = { META, loadShots, SEGMENTS, TALK_X: 0.5 };
