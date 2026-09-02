#!/usr/bin/env node
/* eslint-disable no-console */
//
// IG AUTO-BOOST — rules tests.
//
// The rules decide where real money goes every hour with nobody watching, so each
// one is pinned here against the numbers Dan set on 2026-09-02. A rule that
// drifts (a cap that stops holding, a test promoted on 3 visits, a champion
// killed on lag) fails this file before it reaches the cron.
//
// RUN: node scripts/ads/auto-boost.test.js

'use strict';

const {
  metricsFrom, capState, findCandidates, testPhase, verdict, championHealth, pairDecision, CONFIG,
} = require('./auto-boost.js');

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; console.log(`  ok   ${name}`); }
  else { fail++; console.log(`  FAIL ${name}${extra ? `\n       ${extra}` : ''}`); }
}

console.log('\n1. METRICS OUT OF AN INSIGHTS ROW');
{
  const m = metricsFrom({ spend: '4.73', impressions: '1200', instagram_profile_visits: '19',
                          actions: [{ action_type: 'post_engagement', value: '40' }, { action_type: 'follow', value: '3' }] });
  check('spend is a rounded number', m.spend === 4.73);
  check('visits read from the top-level field', m.visits === 19);
  check('follows found via the candidate list, and the type is named', m.follows === 3 && m.followsType === 'follow');
  const none = metricsFrom({ spend: '2.00', actions: [{ action_type: 'link_click', value: '5' }] });
  check('no follow-type action → 0 follows, null type', none.follows === 0 && none.followsType === null);
  check('empty row does not crash', metricsFrom({}).spend === 0 && metricsFrom(undefined).visits === 0);
  const zeroLike = metricsFrom({ actions: [{ action_type: 'like', value: '0' }] });
  check('a zero-valued candidate does not count as "readable"', zeroLike.followsType === null);
}

console.log('\n2. MONTHLY CAPS — $300 tests / $500 total, including money already committed');
{
  check('fresh month: open', capState({ testsMtd: 0, totalMtd: 0, committedTests: 0 }).capReached === false);
  check('$295 tests spent: the next $5 still fits', capState({ testsMtd: 295, totalMtd: 400, committedTests: 0 }).capReached === false);
  check('$296 tests spent: the next $5 would breach → closed', capState({ testsMtd: 296, totalMtd: 400, committedTests: 0 }).capReached === true);
  const c = capState({ testsMtd: 280, totalMtd: 380, committedTests: 20 });
  check('committed but unspent test budgets count against the cap', c.capReached === true && /tests/.test(c.reason), c.reason);
  const t = capState({ testsMtd: 100, totalMtd: 496, committedTests: 0 });
  check('total cap closes even when tests are under theirs', t.capReached === true && /total/.test(t.reason), t.reason);
  check('the caps are Dan\'s numbers', CONFIG.CAP_TESTS_MTD === 300 && CONFIG.CAP_TOTAL_MTD === 500 && CONFIG.TEST_BUDGET_CENTS === 500);
}

console.log('\n3. CANDIDATE DISCOVERY — new posts only, never twice, never the first-run pair');
{
  const media = [
    { id: 'new1', timestamp: '2026-09-03T22:00:00+0000', media_type: 'IMAGE' },
    { id: 'new0', timestamp: '2026-09-02T22:00:26+0000', media_type: 'IMAGE' },
    { id: 'old',  timestamp: '2026-09-01T22:00:42+0000', media_type: 'VIDEO' },
    { id: CONFIG.FIRST_RUN_PAIR[0], timestamp: '2026-09-05T00:00:00+0000', media_type: 'VIDEO' },
    { id: 'tested', timestamp: '2026-09-03T10:00:00+0000', media_type: 'VIDEO' },
    { id: 'skipped', timestamp: '2026-09-03T11:00:00+0000', media_type: 'CAROUSEL_ALBUM' },
  ];
  const c = findCandidates({ media, testedIds: ['tested'], skippedIds: ['skipped'] });
  check('posts before the system start date are ignored', !c.find(m => m.id === 'old'));
  check('posts already carrying a TEST:: ad set are ignored', !c.find(m => m.id === 'tested'));
  check('posts Meta refused (skip event) are ignored', !c.find(m => m.id === 'skipped'));
  check('the first-run pair never gets a test even if re-dated', !c.find(m => m.id === CONFIG.FIRST_RUN_PAIR[0]));
  check('the two genuinely new posts survive, oldest first', c.length === 2 && c[0].id === 'new0' && c[1].id === 'new1', JSON.stringify(c.map(m => m.id)));
  check('the start date is the go-live day', CONFIG.SYSTEM_START === '2026-09-02');
  check('empty media list is fine', findCandidates({ media: [] }).length === 0);
}

console.log('\n4. TEST WINDOW — judge at $4.50 spent or 5 days, whichever first');
{
  const now = new Date('2026-09-05T12:00:00Z');
  check('$1.20 with 3 days left: running', testPhase({ spend: 1.2, endTime: '2026-09-08T12:00:00Z' }, now) === 'running');
  check('$4.50 spent: ready', testPhase({ spend: 4.5, endTime: '2026-09-08T12:00:00Z' }, now) === 'ready');
  check('end_time passed at $0.00: ready (and will be judged, not ignored)', testPhase({ spend: 0, endTime: '2026-09-05T11:59:00Z' }, now) === 'ready');
  check('$0 with time left is NOT judged as a loser', testPhase({ spend: 0, endTime: '2026-09-07T00:00:00Z' }, now) === 'running');
}

console.log('\n5. VERDICT — beat the champion\'s cost/visit with at least 10 visits; ties keep the champion');
{
  const champ = { costPerVisit: 0.40, hasActive: true };
  check('WIN: $0.25/visit on 20 visits beats $0.40', verdict({ spend: 5, visits: 20, visitsReadable: true }, champ).result === 'win');
  check('LOSE: $0.50/visit on 10 visits does not beat $0.40', verdict({ spend: 5, visits: 10, visitsReadable: true }, champ).result === 'lose');
  check('LOSE: an exact tie keeps the champion', verdict({ spend: 4, visits: 10, visitsReadable: true }, champ).result === 'lose');
  const few = verdict({ spend: 5, visits: 9, visitsReadable: true }, champ);
  check('LOSE: 9 visits at a great price is not enough evidence', few.result === 'lose' && /needs 10/.test(few.reason), few.reason);
  check('WIN by default when the champion slot is empty', verdict({ spend: 5, visits: 12, visitsReadable: true }, { costPerVisit: null, hasActive: false }).result === 'win');
  check('WIN by default when the champion has no visits in its window', verdict({ spend: 5, visits: 12, visitsReadable: true }, { costPerVisit: null, hasActive: true }).result === 'win');
  const blind = verdict({ spend: 5, visits: 0, visitsReadable: false }, champ);
  check('UNMEASURED, not lose, when the visit metric has never been observed on the account', blind.result === 'unmeasured', blind.reason);
  check('...but 0 visits IS a loss once the metric is known to work', verdict({ spend: 5, visits: 0, visitsReadable: true }, champ).result === 'lose');
  check('the promotion floor is 10 visits', CONFIG.PROMOTE_MIN_VISITS === 10);
}

console.log('\n6. CHAMPION HEALTH — pause > $5/follow after $35, flag < $3/follow, never auto-scale');
{
  check('$35 / 5 follows = $7/follow → pause', championHealth({ spend: 35, visits: 100, follows: 5, followsReadable: true }).action === 'pause');
  check('$35 / 0 follows → pause (infinite cost)', championHealth({ spend: 35, visits: 100, follows: 0, followsReadable: true }).action === 'pause');
  check('$34.99 / 0 follows → still under the judging floor, ok', championHealth({ spend: 34.99, visits: 90, follows: 0, followsReadable: true }).action === 'ok');
  check('$40 / 10 follows = $4/follow → ok', championHealth({ spend: 40, visits: 100, follows: 10, followsReadable: true }).action === 'ok');
  const s = championHealth({ spend: 45, visits: 200, follows: 20, followsReadable: true });
  check('$45 / 20 follows = $2.25/follow → scale candidate, reported only', s.action === 'scale_candidate' && /reported only/.test(s.reason), s.reason);
  const u = championHealth({ spend: 60, visits: 150, follows: 0, followsReadable: false });
  check('follows not readable → UNJUDGED, no pause, even at $60 with 0 follows', u.action === 'unjudged' && u.costPerVisit === 0.4, JSON.stringify(u));
  check('exactly $5.00/follow is not over the line', championHealth({ spend: 50, visits: 100, follows: 10, followsReadable: true }).action === 'ok');
  check('the lines are Dan\'s numbers', CONFIG.CHAMPION_KILL_CPF === 5 && CONFIG.CHAMPION_SCALE_CPF === 3 && CONFIG.CHAMPION_MIN_SPEND === 35);
}

console.log('\n7. FIRST-RUN PAIR — both run to $10 each, then the cheaper visit stays');
{
  const [A, B] = CONFIG.FIRST_RUN_PAIR;
  const open = pairDecision([{ id: 'a', mediaId: A, spend: 12, visits: 30, active: true }, { id: 'b', mediaId: B, spend: 8, visits: 30, active: true }]);
  check('one side under $10 → not resolved', open.resolved === false, open.reason);
  const done = pairDecision([{ id: 'a', mediaId: A, spend: 12, visits: 30, active: true }, { id: 'b', mediaId: B, spend: 11, visits: 20, active: true }]);
  check('both past $10 → resolved, keep the cheaper visit', done.resolved === true && done.keep.id === 'a' && done.retire.id === 'b', done.reason);
  const one = pairDecision([{ id: 'a', mediaId: A, spend: 12, visits: 30, active: true }, { id: 'b', mediaId: B, spend: 11, visits: 20, active: false }]);
  check('already one active → nothing to do', one.resolved === false);
  const stranger = pairDecision([{ id: 'x', mediaId: '999', spend: 50, visits: 30, active: true }, { id: 'a', mediaId: A, spend: 12, visits: 30, active: true }]);
  check('a promoted champion outside the pair is never part of the pair rule', stranger.resolved === false);
  const noVisits = pairDecision([{ id: 'a', mediaId: A, spend: 12, visits: 0, active: true }, { id: 'b', mediaId: B, spend: 11, visits: 0, active: true }]);
  check('no visits on either → cannot rank, stays open', noVisits.resolved === false);
}

console.log('\n8. NOTHING CRASHES ON DEGENERATE INPUT');
{
  check('verdict with no champion object', verdict({ spend: 5, visits: 15, visitsReadable: true }, null).result === 'win');
  check('pairDecision on empty list', pairDecision([]).resolved === false);
  check('capState with undefined committed', capState({ testsMtd: 0, totalMtd: 0 }).capReached === false);
}

console.log(`\n${fail === 0 ? 'PASS' : 'FAIL'} — ${pass} passed, ${fail} failed\n`);
process.exit(fail === 0 ? 0 : 1);
