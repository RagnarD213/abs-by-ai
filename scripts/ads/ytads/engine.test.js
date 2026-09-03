#!/usr/bin/env node
/* eslint-disable no-console */
//
// YTADS ENGINE + LINT tests. Every rule in the handoff pinned to Dan's numbers.
// RUN: node scripts/ads/ytads/engine.test.js
'use strict';

const E = require('./engine.js');
const L = require('./lint.js');
const { parseFeed } = require('./feed.js');

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; console.log(`  ok   ${name}`); }
  else { fail++; console.log(`  FAIL ${name}${extra !== undefined ? `\n       ${typeof extra === 'string' ? extra : JSON.stringify(extra)}` : ''}`); }
}

const NOW = '2026-09-04T15:10:00Z';
const CFG = { startDate: '2026-09-03', skiplist: { videoIds: ['skipME12345'], titlePatterns: ['ab wheel beats crunches'] } };
const M = (usd) => Math.round(usd * 1e6);

// ── fixture builders ─────────────────────────────────────────
const content = { businessName: 'Abs by AI', finalUrls: ['https://absbyai.com/'], logoImages: ['customers/1/assets/logo1'], callToActions: ['customers/1/assets/cta1'] };
let adSeq = 100;
function ad({ campaign, name, labels = [], status = 'ENABLED', life = [0, 0], d30, policy, withContent = true, adGroupId = '9' }) {
  const id = String(++adSeq);
  return {
    campaignId: campaign, adGroupId, adId: id, resourceName: `customers/1/adGroupAds/${adGroupId}~${id}`, name, status, labels,
    policy: policy || { approvalStatus: 'APPROVED', reviewStatus: 'REVIEWED', topics: [] },
    lifetime: { costMicros: M(life[0]), conversions: life[1] },
    d30: { costMicros: M((d30 || life)[0]), conversions: (d30 || life)[1] },
    content: withContent ? content : null,
  };
}
const CAMPS = [
  { id: '24122099676', name: '[DAN] [DGEN] [ENGAGEMENT] geo tier 2', status: 'ENABLED', adGroups: [{ id: '9', name: 'g', status: 'ENABLED' }] },
  { id: '2', name: '[DAN] [DGEN] [ENGAGEMENT] MU 18-54 | in-feed & shorts | geo tier 1 | ALL CONTENT', status: 'ENABLED', adGroups: [{ id: '19', name: 'g', status: 'ENABLED' }] },
  { id: '3', name: '[DAN] [DGEN] [ENGAGEMENT] [RMKTG] FMU 18-54 | in-feed & shorts | geo tier 1 | ALL CONTENT | youtube viewers', status: 'ENABLED', adGroups: [{ id: '29', name: 'g', status: 'ENABLED' }] },
];
const T2 = '24122099676', T1 = '2', RM = '3';
const snap = (ads, campaigns = CAMPS) => ({ campaigns, ads });
const video = (id, published, title = 'A video') => ({ id, title, published, description: '' });
const HL = { headlines: ['Why I love the ab wheel', 'One move for the whole core', 'The rollout, done slowly'], longHeadlines: ['Dan shows the ab wheel rollout he does every week'], descriptions: ['Watch the full form breakdown'] };
const run = (o) => E.plan({ snapshot: o.snapshot, videos: o.videos || [], events: o.events || [], headlinesByVideo: o.headlines || {}, now: NOW, config: o.config || CFG, dryRun: !!o.dryRun });
const ops = (r, op) => r.commands.filter(c => c.op === op);

// ============================================================
console.log('\n1. NEW-VIDEO DISCOVERY');
{
  const s = snap([ad({ campaign: T2, name: 'dan 1', life: [20, 60] }), ad({ campaign: T1, name: 'dan 2', life: [20, 8] }), ad({ campaign: RM, name: 'dan 3', life: [9, 0] })]);
  const r = run({ snapshot: s, videos: [video('newVid00001', '2026-09-03T22:00:00Z'), video('oldVid00001', '2026-08-29T22:00:00Z')], headlines: { newVid00001: HL, oldVid00001: HL } });
  const creates = ops(r, 'createAd');
  check('one createAd per campaign for the new video', creates.length === 3 && new Set(creates.map(c => c.campaign)).size === 3, creates.map(c => c.campaign));
  check('a video from before START_DATE is not a candidate', !creates.some(c => c.videoId === 'oldVid00001'));
  check('ad name carries the video id, campaign and date', creates[0].name === 'AUTO test yt:newVid00001 · tier2 · 2026-09-04', creates[0].name);
  check('labels AUTO + AUTO:TEST', creates[0].labels.add.join() === 'AUTO,AUTO:TEST');
  check('business name / url / logo / CTA copied from the existing ad', creates[0].businessName === 'Abs by AI' && creates[0].finalUrls[0] === 'https://absbyai.com/' && creates[0].logoImages.length === 1 && creates[0].callToActions[0] === 'customers/1/assets/cta1');
  check('ad group id is the campaign\'s single enabled group', creates.find(c => c.campaign === 'tier1').adGroupId === '19');
  check('headlines are the passed set', creates[0].headlines.length === 3);
  check('the created ads are in the report with their headlines', r.report.campaigns.tier2.created[0].headlines[0] === HL.headlines[0]);
}
{
  const s = snap([ad({ campaign: T2, name: 'dan 1', life: [20, 60] })]);
  const r = run({ snapshot: s, videos: [video('newVid00001', '2026-09-03T22:00:00Z')] });
  check('no headlines yet → no createAd, reported as waiting', ops(r, 'createAd').length === 0 && r.report.waitingHeadlines[0].videoId === 'newVid00001');
}

console.log('\n2. SKIP LIST + ONE-AD-PER-(VIDEO,CAMPAIGN)');
{
  const s = snap([ad({ campaign: T2, name: 'dan 1', life: [20, 60] }), ad({ campaign: T2, name: 'AUTO test yt:newVid00001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [1, 2] })]);
  const vids = [video('newVid00001', '2026-09-03T22:00:00Z'), video('skipME12345', '2026-09-03T23:00:00Z'), video('abwhl000001', '2026-09-03T23:30:00Z', 'Ab Wheel Beats Crunches - Here Is Why')];
  const r = run({ snapshot: s, videos: vids, headlines: { newVid00001: HL, skipME12345: HL, abwhl000001: HL } });
  check('an existing AUTO ad for the video in that campaign → no second ad', ops(r, 'createAd').filter(c => c.videoId === 'newVid00001').length === 0);
  check('skiplist by id never gets an ad', !ops(r, 'createAd').some(c => c.videoId === 'skipME12345'));
  check('skiplist by title pattern never gets an ad (ab-wheel short 1)', !ops(r, 'createAd').some(c => c.videoId === 'abwhl000001'));
  check('skips are reported with the reason', r.report.skipped.some(x => x.videoId === 'abwhl000001' && /title/.test(x.reason)));
  check('the AUTO:TEST ad is listed as running', r.report.campaigns.tier2.tests[0].phase === 'running' && r.report.campaigns.tier2.tests[0].spend === 1);
}
{
  // A permanent skip event (lint failure) and three create errors both stop retries.
  const s = snap([ad({ campaign: T2, name: 'dan 1', life: [20, 60] }), ad({ campaign: T1, name: 'dan 2', life: [20, 8] })]);
  const events = [
    { video_id: 'lintFail001', campaign_key: null, event: 'skip', detail: { permanent: true, reason: 'lint' } },
    ...[1, 2, 3].map(() => ({ video_id: 'errVid00001', campaign_key: 'tier2', event: 'error', detail: { op: 'createAd', message: 'x' } })),
    { video_id: 'errVid00001', campaign_key: 'tier1', event: 'error', detail: { op: 'createAd', message: 'x' } },
  ];
  const r = run({ snapshot: s, videos: [video('lintFail001', '2026-09-03T22:00:00Z'), video('errVid00001', '2026-09-03T22:00:00Z')], events, headlines: { lintFail001: HL, errVid00001: HL } });
  check('permanent lint skip → no ad anywhere', !ops(r, 'createAd').some(c => c.videoId === 'lintFail001'));
  check('three createAd errors in tier2 → give up there, still try tier1', ops(r, 'createAd').filter(c => c.videoId === 'errVid00001').map(c => c.campaign).join() === 'tier1');
}

console.log('\n3. $5 PAUSE + MIN_CONV NO-READ');
{
  const champ = ad({ campaign: T2, name: 'dan champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [40, 200], d30: [10, 40] });   // $0.25/conv
  const running = ad({ campaign: T2, name: 'AUTO test yt:runVid00001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [4.99, 30] });
  const noRead = ad({ campaign: T2, name: 'AUTO test yt:noRead00001 · tier2 · 2026-09-02', labels: ['AUTO', 'AUTO:TEST'], life: [5.10, 3] });
  const r = run({ snapshot: snap([champ, running, noRead]) });
  check('$4.99 spent → keeps running', !r.commands.some(c => c.adId === running.adId));
  check('$5.10 with 3 conv (< 5 in tier2) → paused as no-read', ops(r, 'pauseAd').some(c => c.adId === noRead.adId && c.reason === 'verdict:no-read'));
  check('no-read gets AUTO:RETIRED and loses AUTO:TEST', ops(r, 'pauseAd')[0].labels.add.join() === 'AUTO:RETIRED' && ops(r, 'pauseAd')[0].labels.remove.includes('AUTO:TEST'));
  check('champion untouched', !r.commands.some(c => c.adId === champ.adId));
  check('days waiting computed from the name date', r.report.campaigns.tier2.tests.find(t => t.adId === noRead.adId).daysWaiting === 2);
}
{
  const champ = ad({ campaign: RM, name: 'dan rm champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [30, 2], d30: [10, 1] });
  const t = ad({ campaign: RM, name: 'AUTO test yt:rmVid000001 · rmktg · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [5.00, 0] });
  const r = run({ snapshot: snap([champ, t]) });
  check('zero conversions at $5 → paused (no-read), even in remarketing (min 1)', ops(r, 'pauseAd').some(c => c.adId === t.adId && c.reason === 'verdict:no-read'));
}

console.log('\n4. WIN / LOSE AGAINST THE CHAMPION\'S TRAILING 30 DAYS');
{
  const champ = ad({ campaign: T2, name: 'dan champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [100, 2000], d30: [10, 20] }); // lifetime $0.05, 30d $0.50
  const winner = ad({ campaign: T2, name: 'AUTO test yt:winVid00001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [5.20, 20] }); // $0.26
  const r = run({ snapshot: snap([champ, winner]) });
  const promote = ops(r, 'label').find(c => c.reason === 'promote');
  check('test at $0.26 beats champion\'s 30d $0.50 (not its lifetime $0.05) → promote', !!promote && promote.adId === winner.adId, r.commands);
  check('promotion relabels TEST → CHAMPION', promote && promote.labels.add.join() === 'AUTO:CHAMPION' && promote.labels.remove.join() === 'AUTO:TEST');
  const dethrone = ops(r, 'pauseAd').find(c => c.reason === 'dethroned');
  check('old champion paused and relabelled RETIRED', dethrone && dethrone.adId === champ.adId && dethrone.labels.add.join() === 'AUTO:RETIRED' && dethrone.labels.remove.join() === 'AUTO:CHAMPION');
  check('report names the new champion', r.report.campaigns.tier2.champion.adId === winner.adId);
  check('verdict detail carries both numbers', /\$0\.26.*\$0\.5/.test(r.report.campaigns.tier2.verdicts[0].detail), r.report.campaigns.tier2.verdicts[0].detail);
}
{
  const champ = ad({ campaign: T2, name: 'dan champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [100, 2000], d30: [10, 100] }); // 30d $0.10
  const loser = ad({ campaign: T2, name: 'AUTO test yt:loseVid0001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [5.00, 20] }); // $0.25
  const tie = ad({ campaign: T2, name: 'AUTO test yt:tieVid00001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [5.00, 50] }); // $0.10
  const r = run({ snapshot: snap([champ, loser, tie]) });
  check('$0.25 vs champion $0.10 → paused as lose', ops(r, 'pauseAd').some(c => c.adId === loser.adId && c.reason === 'verdict:lose'));
  check('a tie keeps the champion', ops(r, 'pauseAd').some(c => c.adId === tie.adId && c.reason === 'verdict:lose') && !r.commands.some(c => c.adId === champ.adId));
}
{
  // Champion with zero conversions in the trailing 30 days: any test clearing MIN_CONV wins.
  const champ = ad({ campaign: T1, name: 'dan champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [60, 20], d30: [15, 0] });
  const t = ad({ campaign: T1, name: 'AUTO test yt:t1Vid000001 · tier1 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [5.00, 2] }); // exactly MIN_CONV
  const r = run({ snapshot: snap([champ, t]) });
  check('champion with 0 conv in 30d is beaten by a 2-conversion test in tier1', ops(r, 'label').some(c => c.reason === 'promote' && c.adId === t.adId));
  check('…and the old champion is paused', ops(r, 'pauseAd').some(c => c.adId === champ.adId && c.reason === 'dethroned'));
}
{
  // Two tests finish in the same hour: the earlier one wins, then the later, better one beats it.
  const champ = ad({ campaign: T2, name: 'dan champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [100, 2000], d30: [10, 10] }); // $1.00
  const a = ad({ campaign: T2, name: 'AUTO test yt:aVid0000001 · tier2 · 2026-09-01', labels: ['AUTO', 'AUTO:TEST'], life: [5, 10] }); // $0.50
  const b = ad({ campaign: T2, name: 'AUTO test yt:bVid0000001 · tier2 · 2026-09-02', labels: ['AUTO', 'AUTO:TEST'], life: [5, 25] }); // $0.20
  const r = run({ snapshot: snap([champ, b, a]) });
  const promotes = ops(r, 'label').filter(c => c.reason === 'promote').map(c => c.adId);
  check('both promoted in order, the better second', promotes.join() === [a.adId, b.adId].join(), promotes);
  check('a is dethroned by b in the same run; final champion is b', ops(r, 'pauseAd').some(c => c.adId === a.adId && c.reason === 'dethroned') && r.report.campaigns.tier2.champion.adId === b.adId);
}

console.log('\n5. DAY-ONE PASS');
{
  const dan = [
    ad({ campaign: T2, name: 'dan A', life: [30, 100] }),   // $0.30
    ad({ campaign: T2, name: 'dan B', life: [20, 200] }),   // $0.10 ← champion
    ad({ campaign: T2, name: 'dan C', life: [4.99, 100] }), // under $5, not eligible, still paused
    ad({ campaign: T2, name: 'dan D', life: [50, 3] }),     // under MIN_CONV
    ad({ campaign: T2, name: 'dan E (paused)', status: 'PAUSED', life: [50, 300] }), // paused: ignored entirely
  ];
  const r = run({ snapshot: snap(dan) });
  const champLabel = ops(r, 'label').find(c => c.reason === 'dayone:champion');
  check('lowest lifetime cost/conv hand-made ad becomes champion', champLabel && champLabel.adId === dan[1].adId);
  check('champion gets AUTO + AUTO:CHAMPION and keeps its name', champLabel.labels.add.join() === 'AUTO,AUTO:CHAMPION' && !r.commands.some(c => c.op === 'createAd'));
  const retired = ops(r, 'pauseAd').filter(c => c.reason === 'dayone:retire').map(c => c.adId);
  check('every other ENABLED hand-made ad is paused with AUTO:RETIRED-DAY1', retired.length === 3 && retired.includes(dan[0].adId) && retired.includes(dan[2].adId) && retired.includes(dan[3].adId) && ops(r, 'pauseAd')[0].labels.add.join() === 'AUTO,AUTO:RETIRED-DAY1');
  check('an already-PAUSED hand-made ad is not touched', !r.commands.some(c => c.adId === dan[4].adId));
  check('the report carries the full pause list and a reversal', r.report.campaigns.tier2.dayOne.paused.length === 3 && r.report.campaigns.tier2.dayOne.reversal[0].op === 'enableAd');
  check('champion reported', r.report.campaigns.tier2.champion.adId === dan[1].adId);
}
{
  // No qualifier (remarketing: 0 conversions) → nothing paused, deferred and said so.
  const r = run({ snapshot: snap([ad({ campaign: RM, name: 'rm A', life: [6, 0] }), ad({ campaign: RM, name: 'rm B', life: [3, 0] })]) });
  check('day-one with no qualifier pauses nothing', r.commands.length === 0);
  check('…and reports the deferral', /first qualifying test/.test(r.report.campaigns.rmktg.dayOne.deferred));
}
{
  // Day-one already executed (event) but the champion later got paused: hand-made ads are NEVER touched again.
  const events = [{ video_id: null, campaign_key: 'tier2', event: 'dayone', detail: { paused: [] } }];
  const r = run({ snapshot: snap([ad({ campaign: T2, name: 'dan new hand-made', life: [30, 100] })]), events });
  check('after day one, a hand-made ENABLED ad is never paused or labelled', r.commands.length === 0);
}
{
  // A dry-run day-one event does not count as executed.
  const events = [{ video_id: null, campaign_key: 'tier2', event: 'dayone', detail: { dryRun: true, paused: [] } }];
  const r = run({ snapshot: snap([ad({ campaign: T2, name: 'dan A', life: [30, 100] }), ad({ campaign: T2, name: 'dan B', life: [20, 200] })]), events });
  check('a dry-run day-one record does not block the real one', ops(r, 'pauseAd').length === 1);
}
{
  // Interpretation 6: first qualifying test in a champion-less campaign crowns itself AND pauses the hand-made ads then.
  const hand = ad({ campaign: RM, name: 'rm A', life: [6, 0] });
  const t = ad({ campaign: RM, name: 'AUTO test yt:rmWin000001 · rmktg · 2026-09-01', labels: ['AUTO', 'AUTO:TEST'], life: [5, 1] });
  const r = run({ snapshot: snap([hand, t]) });
  check('test promoted with no champion present', ops(r, 'label').some(c => c.reason === 'promote' && c.adId === t.adId));
  check('the hand-made ad is paused at that moment (RETIRED-DAY1)', ops(r, 'pauseAd').some(c => c.adId === hand.adId && c.reason === 'dayone:retire'));
  check('no dethrone command (there was nobody to dethrone)', !ops(r, 'pauseAd').some(c => c.reason === 'dethroned'));
}

console.log('\n6. POLICY');
{
  const champ = ad({ campaign: T2, name: 'dan champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [40, 200], d30: [10, 40] });
  const bad = ad({ campaign: T2, name: 'AUTO test yt:badVid00001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [0, 0], policy: { approvalStatus: 'DISAPPROVED', reviewStatus: 'REVIEWED', topics: ['HEALTH_CLAIMS'] } });
  const limited = ad({ campaign: T2, name: 'AUTO test yt:limVid00001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [1, 3], policy: { approvalStatus: 'APPROVED_LIMITED', reviewStatus: 'REVIEWED', topics: ['BODY_IMAGE'] } });
  const danBad = ad({ campaign: T2, name: 'dan disapproved', life: [1, 0], policy: { approvalStatus: 'DISAPPROVED', reviewStatus: 'REVIEWED', topics: [] } });
  const events = [{ video_id: null, campaign_key: 'tier2', event: 'dayone', detail: {} }];
  const r = run({ snapshot: snap([champ, bad, limited, danBad]), events, videos: [video('badVid00001', '2026-09-03T00:00:00Z')], headlines: { badVid00001: HL } });
  const p = ops(r, 'pauseAd').find(c => c.adId === bad.adId);
  check('DISAPPROVED AUTO ad → paused, RETIRED, topic carried', p && p.reason === 'policy:disapproved' && p.topics[0] === 'HEALTH_CLAIMS');
  check('the disapproved video is not re-created in that campaign (its ad is still in the ledger)', !ops(r, 'createAd').some(c => c.videoId === 'badVid00001' && c.campaign === 'tier2'));
  check('Eligible (Limited) is reported, not acted on', !r.commands.some(c => c.adId === limited.adId) && r.report.campaigns.tier2.policy.some(x => x.adId === limited.adId && x.limited));
  check('a disapproved NON-AUTO ad is Dan\'s business, not ours', !r.commands.some(c => c.adId === danBad.adId));
}
{
  // A DISAPPROVED champion is paused and no longer used as the bar.
  const champ = ad({ campaign: T2, name: 'dan champ', labels: ['AUTO', 'AUTO:CHAMPION'], life: [40, 200], d30: [10, 40], policy: { approvalStatus: 'DISAPPROVED', reviewStatus: 'REVIEWED', topics: [] } });
  const t = ad({ campaign: T2, name: 'AUTO test yt:tVid0000001 · tier2 · 2026-09-03', labels: ['AUTO', 'AUTO:TEST'], life: [5, 5] });
  const events = [{ video_id: null, campaign_key: 'tier2', event: 'dayone', detail: {} }];
  const r = run({ snapshot: snap([champ, t]), events });
  check('disapproved champion paused', ops(r, 'pauseAd').some(c => c.adId === champ.adId && c.reason === 'policy:disapproved'));
  check('a qualifying test then takes the empty seat', ops(r, 'label').some(c => c.reason === 'promote' && c.adId === t.adId));
}

console.log('\n7. DRY RUN, MISSING CAMPAIGNS, AMBIGUOUS AD GROUP');
{
  const r = run({ snapshot: snap([ad({ campaign: T2, name: 'dan A', life: [30, 100] }), ad({ campaign: T2, name: 'dan B', life: [20, 200] })]), dryRun: true });
  check('every command carries dryRun:true', r.commands.length === 2 && r.commands.every(c => c.dryRun === true));
  check('report says dry run', r.report.dryRun === true);
}
{
  const camps = [CAMPS[0], { id: '2', name: 'tier 1', status: 'ENABLED', adGroups: [{ id: '19', status: 'ENABLED' }, { id: '20', status: 'ENABLED' }] }];
  const r = run({ snapshot: snap([ad({ campaign: T2, name: 'dan A', life: [30, 100] }), ad({ campaign: T1, name: 'dan B', life: [30, 100] })], camps), videos: [video('v0000000001', '2026-09-03T00:00:00Z')], headlines: { v0000000001: HL } });
  check('missing campaign is a warning, not a crash', r.report.warnings.some(w => /rmktg/.test(w)));
  check('two enabled ad groups → no ad created there, warning asks Dan', !ops(r, 'createAd').some(c => c.campaign === 'tier1') && r.report.warnings.some(w => /tier1: 2 enabled ad groups/.test(w)));
  check('the unambiguous campaign still gets its ad', ops(r, 'createAd').some(c => c.campaign === 'tier2'));
}
{
  const r = run({ snapshot: snap([ad({ campaign: T2, name: 'dan A', life: [30, 100], withContent: false })]), videos: [video('v0000000001', '2026-09-03T00:00:00Z')], headlines: { v0000000001: HL } });
  check('no ad with copyable fields → no createAd, warning', ops(r, 'createAd').length === 0 && r.report.warnings.some(w => /copy business name/.test(w)));
}
{
  // Label failed to apply at creation: the name still says it is a test.
  const t = ad({ campaign: T2, name: 'AUTO test yt:unlab000001 · tier2 · 2026-09-03', labels: [], life: [5, 10] });
  const events = [{ video_id: null, campaign_key: 'tier2', event: 'dayone', detail: {} }];
  const r = run({ snapshot: snap([t]), events, videos: [video('unlab000001', '2026-09-03T00:00:00Z')], headlines: { unlab000001: HL } });
  check('an unlabelled "AUTO test" ad is still recognised (no duplicate, judged)', ops(r, 'createAd').length === 0 && ops(r, 'label').some(c => c.reason === 'promote'));
}

console.log('\n8. LINT — must-fail fixtures (the 8/11 headlines) and must-pass');
for (const bad of ['Get Real Abs Using AI Tools', 'Get Sixpack Abs Using AI Tools', 'Make them real', 'Lose 10 lbs in 30 days', 'Before and after with AI', 'My Zepbound results', 'Guaranteed six pack', 'Abs by AI®', 'Stop being out of shape', 'Amazing results!', 'SEE YOUR ABS NOW', 'Transform your body', 'Burn belly fat fast', 'Real results from AI', 'Your GLP-1 questions answered', 'a headline that is far too long to fit inside forty chars']) {
  check(`fails: "${bad}"`, !L.lintLine(bad).ok);
}
check('"Make them real" fails on the result-promise rule', L.lintLine('Make them real').reasons.length > 0);
for (const good of ['See what you would look like with abs', 'Why I love the ab wheel', 'A photo replaces your food scale', 'The 3 supplements I actually take', 'One minute, four ab muscles', 'My honest update at six months', 'The AI trick that ended my snacking', 'What I eat before jiu jitsu']) {
  check(`passes: "${good}"`, L.lintLine(good).ok, L.lintLine(good).reasons);
}
check('long headline limit is 90', L.lintLine('x'.repeat(90), 'longHeadline').ok && !L.lintLine('x'.repeat(91), 'longHeadline').ok);
check('lintSet reports per-line failures', L.lintSet({ headlines: ['ok line', 'Get abs now'], longHeadlines: [], descriptions: ['fine'] }).failures.length === 1);
check('passingOnly drops the failing line', L.passingOnly({ headlines: ['ok line', 'Get abs now'], longHeadlines: [], descriptions: [] }).headlines.join() === 'ok line');

console.log('\n9. FEED PARSER');
{
  const xml = `<feed><entry><yt:videoId>abc12345678</yt:videoId><title>T &amp; U</title><link rel="alternate" href="https://www.youtube.com/shorts/abc12345678"/><published>2026-09-03T22:00:17+00:00</published><media:group><media:description>Desc &quot;x&quot;</media:description></media:group></entry></feed>`;
  const v = parseFeed(xml);
  check('parses id, title, short flag, published, description', v.length === 1 && v[0].id === 'abc12345678' && v[0].title === 'T & U' && v[0].isShort && v[0].published.startsWith('2026-09-03') && v[0].description === 'Desc "x"');
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
