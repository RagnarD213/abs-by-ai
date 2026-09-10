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
  { id: '24163535721', name: '[DAN] [DGEN] [ENGAGEMENT] MU 18-54 | in-feed & shorts | geo tier 1 | ALL CONTENT', status: 'ENABLED', adGroups: [{ id: '19', name: 'g', status: 'ENABLED' }] },
  { id: '24169507109', name: '[DAN] [DGEN] [ENGAGEMENT] [RMKTG] FMU 18-54 | in-feed & shorts | geo tier 1 | ALL CONTENT | youtube viewers', status: 'ENABLED', adGroups: [{ id: '29', name: 'g', status: 'ENABLED' }] },
];
const T2 = '24122099676', T1 = '24163535721', RM = '24169507109';  // the real ids, pinned 2026-09-08
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
  check('ad name carries the video title, id, campaign and date', creates[0].name === 'AT · A video · yt:newVid00001 · tier2 · 2026-09-04', creates[0].name);
  check('the new name still parses: video id, date, state', E.videoIdOf(creates[0].name) === 'newVid00001' && E.createdDateOf(creates[0].name) === '2026-09-04' && E.stateOf({ name: creates[0].name, labels: [] }) === 'AUTO:TEST');
  check('titles are cleaned: separators removed, long titles cut to 70 with an ellipsis',
        E.cleanTitle('Bad · title | here') === 'Bad title here' && E.cleanTitle('x'.repeat(100)).length === 70 && E.cleanTitle('x'.repeat(100)).endsWith('…'));
  {
    const legacy = ad({ campaign: T2, name: 'AUTO test yt:legacyVid01 · tier2 · 2026-09-08', labels: ['AUTO', 'AUTO:TEST'], life: [1, 2] });
    const r2 = run({ snapshot: snap([ad({ campaign: T2, name: 'dan 1', life: [20, 60] }), legacy]),
                     videos: [video('legacyVid01', '2026-09-03T22:00:00Z', 'Hire A Maid Instead Of A Personal Trainer')], headlines: { legacyVid01: HL } });
    check('a legacy-named AUTO ad is never renamed (Ad.name is immutable) and still counts as the video\'s test', !r2.commands.some(c => c.op === 'renameAd') && !ops(r2, 'createAd').some(c => c.videoId === 'legacyVid01'), r2.commands.map(c => c.op));
    check('lacksTitle recognises the legacy format only', E.lacksTitle(legacy) && !E.lacksTitle({ name: 'AT · T · yt:x · tier2 · 2026-09-09' }));
    check('both name prefixes are recognised as ours: AT (new) and AUTO test (2026-09-08 ads)', E.isAuto({ name: 'AT · T · yt:abcdefghijk · tier2 · 2026-09-09', labels: [] }) && E.isAuto({ name: 'AUTO test · T · yt:abcdefghijk · tier2 · 2026-09-08', labels: [] }) && E.stateOf({ name: 'AT · T · yt:abcdefghijk · tier2 · 2026-09-09', labels: [] }) === 'AUTO:TEST' && !E.isAuto({ name: 'ATTENTION my ad', labels: [] }));
  }
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

console.log('\n6b. RETRY RULE (Dan 2026-09-10)');
{
  const LIM = { approvalStatus: 'APPROVED_LIMITED', reviewStatus: 'REVIEWED', topics: ['YOUTUBE_AD_REQUIREMENTS_EXAGERRATED_OR_INACCURATE_CLAIMS:LIMITED'] };
  const DIS = { approvalStatus: 'DISAPPROVED', reviewStatus: 'REVIEWED', topics: ['CLICKBAIT:PROHIBITED'] };
  const APP = { approvalStatus: 'APPROVED', reviewStatus: 'REVIEWED', topics: [] };
  const REV = { approvalStatus: 'UNKNOWN', reviewStatus: 'REVIEW_IN_PROGRESS', topics: [] };
  const DAYONE = E.CAMPAIGN_KEYS.map(k => ({ video_id: null, campaign_key: k, event: 'dayone', detail: {} }));
  const COPY = { headlines: ['Ab routine order at home', 'Where ab exercises fit', 'My ab training order'], longHeadlines: ['Daniel Rose shows the order he trains his abs in.'], descriptions: ['A short video on the order of an ab routine.'] };
  const V = 'stuckVid001';
  const t1 = (o = {}) => ad({ campaign: T2, name: `AT · Stop Doing Ab Exercises · yt:${V} · tier2 · ${o.date || '2026-09-02'}`, labels: ['AUTO', 'AUTO:TEST'], life: o.life || [0, 0], policy: o.policy || LIM, status: o.status || 'ENABLED' });
  const tr = (n, o = {}) => ad({ campaign: o.campaign || T2, name: `AT · Stop Doing Ab Exercises · yt:${V} · r${n} · ${o.key || 'tier2'} · ${o.date || '2026-09-02'}`, labels: ['AUTO', 'AUTO:TEST'], life: o.life || [0, 0], policy: o.policy || LIM });
  const R = (ads, o = {}) => E.plan({ snapshot: snap(ads), videos: [], events: [...DAYONE, ...(o.events || [])], headlinesByVideo: {}, retryCopyByVideo: o.copy || {}, now: NOW, config: CFG, dryRun: false });
  const evt = (event, extra = {}) => ({ video_id: V, campaign_key: null, ad_id: null, event, detail: {}, at: '2026-09-03T00:00:00Z', ...extra });

  // ── attempt 2: tamer copy ──
  let a = t1(); let r = R([a]);
  check('limited + $0 after 2 days, no tamer copy yet → asks for copy (with the policy topic), creates nothing',
        r.report.retry.waitingCopy.some(w => w.videoId === V && w.topics.length === 1) && r.commands.length === 0, r.commands);
  a = t1(); r = R([a], { copy: { [V]: COPY } });
  const c2 = ops(r, 'createAd')[0];
  check('with copy → attempt 2 ad: r2 in the name, the tamer copy, TEST labels',
        c2 && c2.name === `AT · Stop Doing Ab Exercises · yt:${V} · r2 · tier2 · 2026-09-04` && c2.attempt === 2 && c2.headlines === COPY.headlines && c2.labels.add.join() === 'AUTO,AUTO:TEST', c2);
  check('the failed original is paused and labelled SUPERSEDED', ops(r, 'pauseAd').some(c => c.adId === a.adId && c.reason === 'retry:superseded' && c.labels.add.includes('AUTO:SUPERSEDED')));
  check('the r2 name still parses: a TEST for this video, attempt 2, dated', E.attemptOf(c2.name) === 2 && E.videoIdOf(c2.name) === V && E.stateOf({ name: c2.name, labels: [] }) === 'AUTO:TEST' && E.createdDateOf(c2.name) === '2026-09-04');
  check('limited + $0 after only 1 day → waits', R([t1({ date: '2026-09-03' })], { copy: { [V]: COPY } }).commands.length === 0);
  a = t1({ date: '2026-09-03' });
  check('a retry:force event skips the wait (Dan\'s one-off resubmits)', ops(R([a], { copy: { [V]: COPY }, events: [evt('retry:force', { ad_id: a.adId })] }), 'createAd').length === 1);
  check('limited but spending → it is running, no retry', R([t1({ life: [0.4, 0] })], { copy: { [V]: COPY } }).commands.length === 0);
  a = t1({ date: '2026-09-04', policy: DIS });
  r = R([a], { copy: { [V]: COPY } });
  check('disapproved → attempt 2 at once, and the original is paused exactly once', ops(r, 'createAd').some(c => c.attempt === 2) && ops(r, 'pauseAd').filter(c => c.adId === a.adId).length === 1, r.commands.map(c => c.op + ':' + c.reason));
  check('tamer copy that failed the lint → attempt 2 held with a warning', R([t1()], { events: [evt('retrycopy:failed')] }).report.warnings.some(w => /attempt 2 in tier2 is on hold/.test(w)));

  // ── hand-made ads (Dan: retry them too) ──
  const hand = (o = {}) => Object.assign(ad({ campaign: o.campaign || RM, name: 'late night eating', labels: o.labels || [], life: [0, 0], policy: LIM, status: o.status || 'ENABLED' }), { videoId: 'handVid0001' });
  let h = hand(); r = R([h], { copy: { handVid0001: COPY } });
  check('a limited hand-made ad (no date in its name) starts its clock with limited:seen and waits', r.report.retry.seen.some(s => s.adId === h.adId) && r.commands.length === 0);
  h = hand(); r = R([h], { copy: { handVid0001: COPY }, events: [{ video_id: 'handVid0001', campaign_key: 'rmktg', ad_id: h.adId, event: 'limited:seen', detail: {}, at: '2026-09-01T00:00:00Z' }] });
  check('…and is resubmitted once it has been limited at $0 for 2 days', ops(r, 'createAd').some(c => c.campaign === 'rmktg' && c.videoId === 'handVid0001' && c.attempt === 2) && ops(r, 'pauseAd').some(c => c.adId === h.adId));
  h = hand({ campaign: T2, labels: ['AUTO', 'AUTO:RETIRED-DAY1'], status: 'PAUSED' });
  r = R([h], { copy: { handVid0001: COPY }, events: [{ video_id: 'handVid0001', campaign_key: 'tier2', ad_id: h.adId, event: 'retry:force', detail: {}, at: NOW }] });
  check('a day-one-retired hand-made ad is resubmitted and only relabelled (it is already paused)', ops(r, 'createAd').length === 1 && ops(r, 'label').some(c => c.adId === h.adId && c.reason === 'retry:superseded') && !ops(r, 'pauseAd').some(c => c.adId === h.adId));
  check('a hand-made ad Dan paused himself is left alone', R([hand({ status: 'PAUSED' })], { copy: { handVid0001: COPY } }).commands.length === 0);

  // ── attempt 3: clean thumbnail, then a fresh ad ──
  const supL = () => { const x = t1({ status: 'PAUSED' }); x.labels = ['AUTO', 'AUTO:SUPERSEDED']; return x; };
  check('attempt 2 approved → nothing more (it runs on as an ordinary test)', R([supL(), tr(2, { policy: APP })]).commands.length === 0);
  check('attempt 2 still in review → wait', R([supL(), tr(2, { policy: REV })]).commands.length === 0);
  r = R([supL(), tr(2)]);
  check('attempt 2 failed → the thumbnail swap is requested, no ad yet', r.report.retry.thumbnails.some(t => t.videoId === V) && r.commands.length === 0);
  check('thumbnail swapped 30 min ago → wait for YouTube to serve it', R([supL(), tr(2)], { events: [evt('thumb:swapped', { at: '2026-09-04T14:40:00Z' })] }).commands.length === 0);
  const r2 = tr(2); r2.content = { ...r2.content, ...COPY };
  r = R([supL(), r2], { events: [evt('thumb:swapped', { at: '2026-09-04T13:00:00Z' })] });
  const c3 = ops(r, 'createAd')[0];
  check('thumbnail swapped over an hour ago → attempt 3 with attempt 2\'s copy; attempt 2 superseded',
        c3 && c3.attempt === 3 && / · r3 · tier2 · /.test(c3.name) && c3.headlines === COPY.headlines && ops(r, 'pauseAd').some(c => c.adId === r2.adId && c.reason === 'retry:superseded'), r.commands);
  check('no clean frame could be made → attempt 3 held with a warning', R([supL(), tr(2)], { events: [evt('thumb:failed', { detail: { reason: 'no frame without text' } })] }).report.warnings.some(w => /attempt 3 in tier2 is on hold/.test(w)));
  check('a transient thumbnail failure is retried, not held', R([supL(), tr(2)], { events: [evt('thumb:failed', { detail: { reason: 'network', transient: true } })] }).report.retry.thumbnails.length === 1);

  // ── give up: remove the chain, restore the thumbnail ──
  const o1 = supL(), o2 = tr(2), o3 = tr(3);
  o2.labels = ['AUTO', 'AUTO:SUPERSEDED']; o2.status = 'PAUSED';
  r = R([o1, o2, o3], { events: [evt('thumb:swapped')] });
  const removes = r.commands.filter(c => c.op === 'mutate' && c.reason === 'retry:remove');
  check('attempt 3 failed → every ad in the chain is removed (original, r2, r3)', removes.length === 3 && [o1, o2, o3].every(x => removes.some(c => c.mutation.adGroupAdOperation.remove === x.resourceName)), removes);
  check('…the chain is reported failed and the original thumbnail restore is requested', r.report.retry.failed.some(f => f.videoId === V && f.campaign === 'tier2') && r.report.retry.restore.some(x => x.videoId === V));
  r = R([o1, o2, o3, tr(3, { campaign: T1, key: 'tier1', policy: APP })], { events: [evt('thumb:swapped')] });
  check('attempt 3 passed in another campaign → that ad keeps running and the clean thumbnail stays', r.report.retry.failed.length === 1 && r.report.retry.restore.length === 0);
  const gone = [evt('retry:failed', { campaign_key: 'tier2' })];
  check('after a chain failed, the video is never started over in that campaign',
        E.candidates({ snapshot: snap([]), videos: [video(V, '2026-09-03T00:00:00Z')], events: gone, config: CFG }).candidates.every(x => !x.campaigns.includes('tier2')));
  check('…and its leftover ads are not processed again', R([o1, o2, o3], { events: gone }).commands.length === 0);
  check('policyVerdict: limited+$0 pending → failed at 2 days; spending = ok; disapproved = failed at once',
        E.policyVerdict({ policy: LIM, lifetime: {} }, 1) === 'pending' && E.policyVerdict({ policy: LIM, lifetime: {} }, 2) === 'failed' &&
        E.policyVerdict({ policy: LIM, lifetime: { costMicros: 10000 } }, 9) === 'ok' && E.policyVerdict({ policy: DIS, lifetime: {} }, 0) === 'failed');
}
check('lint: "trick" fails every ad (Dan 2026-09-10)', !L.lintLine('The AI trick for late night snacking').ok && !L.lintLine('Two tricks I use').ok);
check('lint: tame mode rejects hooks, questions and claim numbers that normal mode allows',
      L.lintLine('Stop doing crunches first').ok && !L.lintLine('Stop doing crunches first', 'headline', { tame: true }).ok &&
      !L.lintLine('Why do abs hide?', 'headline', { tame: true }).ok && !L.lintLine('Supplements are 3% of it', 'headline', { tame: true }).ok &&
      L.lintLine('My ab training order', 'headline', { tame: true }).ok);
{
  // Attempt 3's thumbnail framing is computed by rule from the located head (thumbs.js cropFromHead).
  const T = require('./thumbs.js');
  const HEAD = { top: 0.2, bottom: 0.45, left: 0.3, right: 0.7 };   // on a 1080×1920 Short frame: head 480 px tall
  const b = T.cropFromHead(HEAD, [{ top: 0.55, bottom: 0.6, left: 0.1, right: 0.9 }], 1080, 1920);
  check('thumbnail crop: room above the hair and below the chin, and it stops above the caption',
        b && b.top <= 0.2 * 1920 - 0.08 * 480 && b.top + b.height >= 0.45 * 1920 + 0.1 * 480 && b.top + b.height <= 0.55 * 1920, b);
  check('thumbnail crop: a caption across the face → no crop', T.cropFromHead(HEAD, [{ top: 0.3, bottom: 0.35, left: 0, right: 1 }], 1080, 1920) === null);
  check('thumbnail crop: head touching the top of the frame → no crop (the hair would be cut)', T.cropFromHead({ top: 0.0, bottom: 0.3, left: 0.3, right: 0.7 }, [], 1080, 1920) === null);
  const GOOD = { dan: true, text: false, face: true, cut: false, expression: 'good' };
  check('thumbnail check: Dan, no text, whole face, nothing cut AND a calm expression',
        T.passes(GOOD) && !T.passes({ ...GOOD, expression: 'bad' }) && !T.passes({ ...GOOD, cut: true }) && !T.passes({ ...GOOD, text: true }));
  check('thumbnail check: a B-roll stranger never becomes the thumbnail (measured 2026-09-10)', !T.passes({ ...GOOD, dan: false }) && !T.passes({ ...GOOD, dan: undefined }));
}
check('titleOf reads both prefixes, null for the legacy untitled format',
      E.titleOf('AT · A b · yt:abcdefghijk · tier2 · 2026-09-09') === 'A b' && E.titleOf('AUTO test · T · yt:abcdefghijk · rmktg · 2026-09-08') === 'T' && E.titleOf('AUTO test yt:abcdefghijk · tier2 · 2026-09-08') === null);
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
  const camps = [CAMPS[0], { id: '24163535721', name: 'tier 1', status: 'ENABLED', adGroups: [{ id: '19', status: 'ENABLED' }, { id: '20', status: 'ENABLED' }] }];
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
for (const good of ['See what you would look like with abs', 'Why I love the ab wheel', 'A photo replaces your food scale', 'The 3 supplements I actually take', 'One minute, four ab muscles', 'My honest update at six months', 'What I eat before jiu jitsu']) {   // "The AI trick that ended my snacking" left this list 2026-09-10 (Dan's no-"trick" rule)
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
