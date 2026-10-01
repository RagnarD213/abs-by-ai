// SL-05 plan: the shot list is planned in plan_shots.py and written to shots/manifest.json.
// This module exposes it plus the titles (round-1 draft copy, Dan edits on the review page).
const path = require('path');
const fs = require('fs');
const { SEGMENTS } = require('./segments.js');

// Benefit-first; eyebrow + headline, the headline measured to fit 2 lines of Impact 98.
const META = {
  S1: { eyebrow: 'STOP DOING DEADLIFTS', title: 'MORE INJURIES THAN\nEVERY OTHER LIFT' },
  S2: { eyebrow: 'BUILD MORE MUSCLE', title: 'SAFER LIFTS WIN\nLONG TERM' },
  S3: { eyebrow: 'WANT AN AESTHETIC BODY?', title: 'DEADLIFTS BUILD A\nPOWERLIFTER BODY' },
  S4: { eyebrow: 'SKIP THE DEADLIFT', title: '2 BACK EXERCISES\nTO DO INSTEAD' },
  S5: { eyebrow: 'SKIP THE DEADLIFT', title: 'TRAIN LEGS WITHOUT\nDEADLIFTS' },
};

function loadShots() {
  return JSON.parse(fs.readFileSync(path.join(__dirname, 'shots', 'manifest.json'), 'utf8'));
}
module.exports = { META, loadShots, SEGMENTS, TALK_X: 0.5 };
