#!/usr/bin/env node
//
// SUBSCRIBER LIST DIGEST — one fingerprint of the marketing list, computed the
// same way on both sides of the 2026-09-11 move off subscribers-data.json.
//
// Why it exists: the list moved from a JSON file in a PUBLIC repo into Postgres,
// and the file could only be deleted once production was PROVEN to hold the same
// data. Counting rows is not proof — it misses a dropped welcome step or a
// mangled timestamp, which would silently re-send five marketing emails to
// people who already finished the sequence. So:
//
//   node scripts/subscribers/digest.js subscribers-data.json
//   curl -s -H "X-Dash-Key: $DASH_SECRET" https://absbyai.com/api/subscribers/status
//
// and the two `digest` values must be identical. The digest covers addresses
// but never reveals them, so it is safe to paste into a terminal, a commit
// message or a chat log.
//
// Normalisation rules (must stay in lockstep with server.js):
//   • keys sorted at every level — Postgres JSONB does not preserve key order
//   • null and absent are the same thing (a NULL column reads back as absent)
//   • timestamps compared as ISO-8601 UTC, since pg returns Date objects
'use strict';

const crypto = require('crypto');

const TS_KEYS = new Set(['subscribedAt', 'welcomeNextAt', 'unsubscribedAt']);

function toIso(v) {
  if (v === undefined || v === null || v === '') return null;
  const d = v instanceof Date ? v : new Date(v);
  return isNaN(d.getTime()) ? null : d.toISOString();
}

// Stable stringify: objects get their keys sorted recursively, arrays keep order.
function canon(value) {
  if (Array.isArray(value)) return value.map(canon);
  if (value && typeof value === 'object' && !(value instanceof Date)) {
    const out = {};
    for (const k of Object.keys(value).sort()) {
      if (value[k] === undefined || value[k] === null) continue;
      out[k] = canon(value[k]);
    }
    return out;
  }
  return value;
}

function canonEntry(entry) {
  const e = entry || {};
  const out = {};
  for (const k of Object.keys(e).sort()) {
    const v = TS_KEYS.has(k) ? toIso(e[k]) : e[k];
    if (v === undefined || v === null) continue; // absent === null, both sides
    out[k] = canon(v);
  }
  return out;
}

// `emails` is the { [address]: entry } map, from the file or from the DB.
function subscribersDigest(emails) {
  const canonical = {};
  for (const email of Object.keys(emails || {}).sort()) {
    canonical[email] = canonEntry(emails[email]);
  }
  return crypto.createHash('sha256').update(JSON.stringify(canonical)).digest('hex');
}

module.exports = { subscribersDigest, canonEntry, toIso };

if (require.main === module) {
  const file = process.argv[2] || 'subscribers-data.json';
  const parsed = JSON.parse(require('fs').readFileSync(file, 'utf8'));
  const emails = parsed.emails || parsed;
  console.log(JSON.stringify({
    file,
    count: Object.keys(emails).length,
    digest: subscribersDigest(emails),
  }, null, 2));
}
