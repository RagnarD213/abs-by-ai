#!/usr/bin/env node
//
// BRAND GUARD — rule tests. Real search terms from the brand campaign, 2026-08-25 to 09-23,
// plus the name searches Dan listed on 2026-09-24.
//
// RUN: node scripts/ads/brand-guard.test.js
'use strict';

const assert = require('assert');
const { allowed } = require('./brand-guard.js');

const BRAND = 'Brand - Abs By AI';
const NAME = 'Brand - Dan Rose';

for (const t of ['abs by ai', 'absbyai.com', 'abs by ai app', 'www.absbyai.com', 'ab by ai', 'abs by ai reviews']) {
  assert.ok(allowed(BRAND, t), `brand should keep "${t}"`);
}
for (const t of ['ai six pack', 'six pack ai', 'ai ab generator', 'abs editor ai', 'abs ai', 'ai abs', 'abs by amy fitness',
  'bodyfit by amy abs', 'give me abs ai', 'abi', 'fake abs ai']) {
  assert.ok(!allowed(BRAND, t), `brand should negate "${t}"`);
}
for (const t of ['danielrose6packabs.com', 'daniel rose sixpackabs.com', 'danielrose sixpackshortcuts', 'dan rose abs by ai',
  'daniel rose abs by ai', 'danrosefit', 'dan rose fitness', 'daniel rose social response marketing',
  'daniel rose 15 steps to profitable youtube marketing', 'dan rose abs']) {
  assert.ok(allowed(NAME, t), `name group should keep "${t}"`);
}
for (const t of ['daniel rose', 'dan rose', 'daniel rose chef', 'daniel rose le coucou', 'dan rose facebook', 'rose abs']) {
  assert.ok(!allowed(NAME, t), `name group should negate "${t}"`);
}
assert.ok(allowed('Some Other Group', 'anything'), 'unknown ad groups are left alone');
console.log('brand-guard rules: all pass');
