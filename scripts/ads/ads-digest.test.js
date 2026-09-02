#!/usr/bin/env node
/* eslint-disable no-console */
//
// ADS DIGEST — detection tests.
//
// WHY THIS FILE EXISTS. Neither ad platform is readable yet (no ads_read token on
// Meta, no Google Ads developer token), so the detection rules have never seen a
// real number and will not until Dan grants a credential. Shipping untested
// judgement logic into a page Dan reads every morning is how a digest starts
// crying wolf — and the first time it does, he stops reading it.
//
// So the fixtures below are built from the REAL measured figures in the
// 2026-08-26 paid audit and the 2026-08-31 pull (AI_COORDINATION.md). Each case
// asserts the rule fires on a failure that actually happened to this account, or
// stays silent on the noise that actually surrounds it.
//
// RUN: node scripts/ads/ads-digest.test.js

'use strict';

const {
  summarise, detectAnomalies, detectWinners, addDays, metaResultFrom,
  GOOGLE_CONVERSION_INFLATION,
} = require('./ads-digest.js');

const DAY = '2026-08-31';
const FROM = addDays(DAY, -7);   // 2026-08-24
const TO   = addDays(DAY, -1);   // 2026-08-30

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; console.log(`  ok   ${name}`); }
  else { fail++; console.log(`  FAIL ${name}${extra ? `\n       ${extra}` : ''}`); }
}

// Build a Row with a per-day spend/results series.
function row(id, name, series, opts = {}) {
  const days = {};
  for (const [date, spend, results] of series) {
    days[date] = { spend, results, impressions: Math.round(spend * 400) };
  }
  return { id, name, days, resultLabel: opts.resultLabel || 'ThruPlay', status: opts.status || 'ACTIVE' };
}
const flat = (from, to, spend, results) => {
  const out = [];
  for (let d = from; d <= to; d = addDays(d, 1)) out.push([d, spend, results]);
  return out;
};

// ============================================================
console.log('\n1. STOPPED SPENDING — the 2026-08-31 miss');
// IG GEO spent $29.19 over the window then went to zero when the campaign was
// toggled OFF, and nobody noticed for days. This is the case the whole digest
// exists for, and the one a spike-only detector cannot see.
{
  const r = summarise(
    row('c1', '[DAN] [ENGAGEMENT] IG GEO', [...flat(FROM, TO, 4.17, 6800), [DAY, 0, 0]], { status: 'PAUSED' }),
    DAY, FROM, TO
  );
  const a = detectAnomalies('meta', [r], null);
  check('fires on a campaign that went to $0', a.some(x => x.kind === 'spend_stopped'));
  check('marked high severity', a[0] && a[0].severity === 'high');
  check('names the paused status', a[0] && /PAUSED/.test(a[0].detail), a[0] && a[0].detail);
  check('reports the real baseline', a[0] && /\$4\.17\/day/.test(a[0].detail), a[0] && a[0].detail);
}

console.log('\n2. ...but NOT on a campaign that was always tiny');
// The other Meta campaign sat at $0.00 the whole window. It never started, so
// "it stopped" is a false statement — and a digest that says it every morning
// forever is exactly the wallpaper the morning brief was rewritten to kill.
{
  const r = summarise(row('c2', '[DAN] [ENGAGEMENT]', flat(FROM, DAY, 0, 0)), DAY, FROM, TO);
  check('silent on a never-started campaign', detectAnomalies('meta', [r], null).length === 0);
}
{
  // A $2/day campaign dropping to $0.10 is below SPEND_STOP_MIN_BASE — noise.
  const r = summarise(row('c3', 'tiny test campaign', [...flat(FROM, TO, 2.00, 3), [DAY, 0.10, 0]]), DAY, FROM, TO);
  check('silent below the $3/day baseline floor', detectAnomalies('meta', [r], null).length === 0);
}

console.log('\n3. SPEND SPIKE — ratio AND dollars, so small accounts stay quiet');
{
  // Tier 2 Demand Gen: $136.75 / 9 days ≈ $15/day, then a $60 day.
  const r = summarise(row('g1', 'DGEN geo tier 2', [...flat(FROM, TO, 15.19, 172), [DAY, 60.00, 180]],
                          { resultLabel: 'conversion' }), DAY, FROM, TO);
  const a = detectAnomalies('google', [r], null);
  check('fires on 4x its normal day', a.some(x => x.kind === 'spend_spike'), JSON.stringify(a));
}
{
  // $1.50/day → $4.00. That is 2.7x but only $2.50 — must not print.
  const r = summarise(row('g2', 'small campaign', [...flat(FROM, TO, 1.50, 2), [DAY, 4.00, 5]]), DAY, FROM, TO);
  const a = detectAnomalies('google', [r], null);
  check('silent on a 2.7x spike worth only $2.50', !a.some(x => x.kind === 'spend_spike'), JSON.stringify(a));
}

console.log('\n4. BOUGHT NOTHING — the $63 search campaign, zero conversions, twice');
{
  const r = summarise(row('g3', 'Search - US - Non-Brand', flat(FROM, DAY, 7.90, 0),
                          { resultLabel: 'conversion' }), DAY, FROM, TO);
  const a = detectAnomalies('google', [r], null);
  check('fires on real spend with zero results', a.some(x => x.kind === 'zero_results'), JSON.stringify(a));
  check('quotes the cumulative spend, not one day',
        a[0] && /\$63\.20/.test(a[0].headline), a[0] && a[0].headline);
}
{
  // $1/day for 8 days = $8. Under the floor — a new campaign in its first days
  // must not be accused of failing.
  const r = summarise(row('g4', 'brand new campaign', flat(FROM, DAY, 1.00, 0)), DAY, FROM, TO);
  check('silent under the $15 window floor',
        !detectAnomalies('google', [r], null).some(x => x.kind === 'zero_results'));
}

console.log('\n5. COST PER RESULT DEGRADING');
{
  // Tier 1: 26 conversions on $59.02 ≈ $2.27 each. A day at $4.00 each is +76%.
  const r = summarise(row('g5', 'DGEN geo tier 1', [...flat(FROM, TO, 6.56, 2.9), [DAY, 12.00, 3]],
                          { resultLabel: 'conversion' }), DAY, FROM, TO);
  const a = detectAnomalies('google', [r], null);
  check('fires when cost/result rises past 1.5x', a.some(x => x.kind === 'cpa_degraded'), JSON.stringify(a));
  check('compares against its OWN average, not a global one',
        a.some(x => x.kind === 'cpa_degraded' && /its own 7-day average/i.test(x.detail)));
}
{
  // Same degradation but on 2 baseline results — not enough to mean anything.
  const r = summarise(row('g6', 'thin campaign', [...flat(FROM, TO, 6.00, 0.28), [DAY, 12.00, 1]]), DAY, FROM, TO);
  check('silent without enough baseline results',
        !detectAnomalies('google', [r], null).some(x => x.kind === 'cpa_degraded'));
}

console.log('\n6. WINNING ADS');
{
  // Five ads. One buys results at roughly half the blended rate on real volume.
  const ads = [
    row('a1', 'v-sit twist',        flat(FROM, DAY, 2.00, 20)),
    row('a2', 'top 10 ab tips',     flat(FROM, DAY, 2.00, 22)),
    row('a3', 'toe touch',          flat(FROM, DAY, 2.00, 18)),
    row('a4', 'spiderman plank',    flat(FROM, DAY, 2.00, 19)),
    row('a5', '1-minute ab workout', flat(FROM, DAY, 2.00, 48)), // ~half the cost per result
  ].map(r => summarise(r, DAY, FROM, TO));

  const w = detectWinners('meta', ads, null);
  check('finds the outperformer', w.length >= 1 && w[0].name === '1-minute ab workout', JSON.stringify(w.map(x => x.name)));
  check('quotes both its rate and the account rate',
        w[0] && w[0].costPerResult < w[0].accountCostPerResult);
  check('caps at 3 winners', w.length <= 3);
}
{
  // All five identical — nothing is winning, and saying otherwise is noise.
  const ads = [1, 2, 3, 4, 5].map(i =>
    summarise(row(`b${i}`, `ad ${i}`, flat(FROM, DAY, 2.00, 20)), DAY, FROM, TO));
  check('silent when every ad performs the same', detectWinners('meta', ads, null).length === 0);
}
{
  // A great rate on 3 results is luck, not a winner.
  const ads = [
    summarise(row('c1', 'lucky ad',  flat(FROM, DAY, 0.20, 0.4)), DAY, FROM, TO),
    ...[1, 2, 3].map(i => summarise(row(`c${i + 1}`, `ad ${i}`, flat(FROM, DAY, 5.00, 20)), DAY, FROM, TO)),
  ];
  check('silent below the volume floor',
        !detectWinners('meta', ads, null).some(w => w.name === 'lucky ad'));
}

console.log('\n7. META RESULT SELECTION');
{
  check('prefers a purchase over a video view', metaResultFrom({
    actions: [{ action_type: 'video_view', value: '900' },
              { action_type: 'offsite_conversion.fb_pixel_purchase', value: '2' }],
  }).label === 'purchase');

  check('falls back to ThruPlay when that is all there is', metaResultFrom({
    video_thruplay_watched_actions: [{ action_type: 'video_view', value: '47953' }],
  }).results === 47953);

  check('never returns NaN on an empty insight', metaResultFrom({}).results === 0);
}

console.log('\n8. THE ~2x GOOGLE CONVERSION INFLATION');
{
  // The measurement itself: 1,553 reported vs 792 earned subscribers.
  check('constant matches the measured ratio',
        Math.abs(GOOGLE_CONVERSION_INFLATION - 1553 / 792) < 0.01,
        `got ${GOOGLE_CONVERSION_INFLATION}, measured ${(1553 / 792).toFixed(3)}`);
  // And what it does to the number that matters: $136.75 / 1,553 reads $0.09 a
  // "conversion", but the real cost per subscriber was $0.17.
  const est = 1553 / GOOGLE_CONVERSION_INFLATION;
  check('deflating 1,553 conversions lands on ~792 subscribers', Math.abs(est - 792) < 5, `got ${est.toFixed(0)}`);
  check('and turns $0.09/conv into ~$0.17/subscriber',
        Math.abs(136.75 / est - 0.17) < 0.01, `got ${(136.75 / est).toFixed(3)}`);
}

console.log('\n9. NO CRASHES ON DEGENERATE INPUT');
{
  check('empty row list', detectAnomalies('meta', [], null).length === 0);
  check('row with no days at all',
        Array.isArray(detectAnomalies('meta', [summarise(row('x', 'x', []), DAY, FROM, TO)], null)));
  check('winners on an empty list', detectWinners('meta', [], null).length === 0);
}

console.log(`\n${fail === 0 ? 'PASS' : 'FAIL'} — ${pass} passed, ${fail} failed\n`);
process.exit(fail === 0 ? 0 : 1);
