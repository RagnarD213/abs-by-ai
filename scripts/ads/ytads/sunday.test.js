#!/usr/bin/env node
/* eslint-disable no-console */
//
// YTADS SUNDAY PAUSE tests (Dan 2026-09-29).
// RUN: node scripts/ads/ytads/sunday.test.js
'use strict';

const S = require('./sunday.js');

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; console.log(`  ok   ${name}`); }
  else { fail++; console.log(`  FAIL ${name}${extra !== undefined ? `\n       ${JSON.stringify(extra)}` : ''}`); }
}

console.log('due: Sundays 10:00-21:59 Central, once per date');
// 2026-10-04 is a Sunday. CDT = UTC-5.
check('Sun 9:59 CT not due', !S.due(new Date('2026-10-04T14:59:00Z'), new Set()));
check('Sun 10:00 CT due', S.due(new Date('2026-10-04T15:00:00Z'), new Set()));
check('Sun 21:30 CT due (catch-up)', S.due(new Date('2026-10-05T02:30:00Z'), new Set()));
check('Sun 22:00 CT not due', !S.due(new Date('2026-10-05T03:00:00Z'), new Set()));
check('already ran that date', !S.due(new Date('2026-10-04T16:00:00Z'), new Set(['2026-10-04'])));
check('Monday not due', !S.due(new Date('2026-10-05T15:00:00Z'), new Set()));
check('after DST ends (CST, UTC-6): Sun 10:00 CT due', S.due(new Date('2026-11-08T16:00:00Z'), new Set()));
check('after DST ends: Sun 9:00 CT not due', !S.due(new Date('2026-11-08T15:00:00Z'), new Set()));

console.log('plan');
const kinds = { S1: 'short', S2: 'short', L_OLD: 'long', L_OLDER: 'long', L_NEW: 'long' };
const kindOf = (id) => kinds[id] ?? null;
const ad = (key, adId, vid, status = 'ENABLED', approval = 'APPROVED', name = `AT · x · yt:${vid} · ${key} · 2026-09-01`) =>
  ({ key, adGroupId: 'g' + key, adId, name, status, approval, videoIds: vid ? [vid] : [], videoAssets: ['a' + vid], template: {}, prior: {} });
const newest = { id: 'L_NEW', title: 'New' };

let p = S.plan({ newestLong: newest, kindOf, ads: [
  ad('tier1', '1', 'S1'), ad('tier1', '2', 'L_OLD'), ad('tier1', '3', 'L_NEW'), ad('tier1', '4', 'S2', 'PAUSED'),
  ad('tier2', '5', 'L_OLDER'), ad('tier2', '6', 'L_OLD', 'PAUSED'), ad('tier2', '7', 'L_NEW'),
] });
check('old long-forms paused (enabled only)', p.pause.map(a => a.adId).join() === '2,5', p.pause.map(a => a.adId));
check('Shorts never touched', !p.pause.some(a => ['1', '4'].includes(a.adId)) && !p.enable.some(a => ['1', '4'].includes(a.adId)));
check('newest kept', p.keep.map(a => a.adId).join() === '3,7');
check('approved newest: no tamer copy', p.tame.length === 0);
check('already-paused long-form not re-paused', !p.pause.some(a => a.adId === '6'));

p = S.plan({ newestLong: newest, kindOf, ads: [ad('tier1', '3', 'L_NEW', 'ENABLED', 'UNDER_REVIEW'), ad('tier2', '7', 'L_NEW', 'ENABLED', 'DISAPPROVED'), ad('tier2', '8', 'L_OLD')] });
check('unapproved newest → tamer copy in both campaigns', p.tame.map(t => t.key).sort().join() === 'tier1,tier2', p.tame);
check('old long-forms still paused when newest is unapproved', p.pause.map(a => a.adId).join() === '8');

p = S.plan({ newestLong: newest, kindOf, ads: [ad('tier1', '3', 'L_NEW', 'ENABLED', 'UNDER_REVIEW'),
  ad('tier1', '9', 'L_NEW', 'ENABLED', 'UNDER_REVIEW', 'AT · x · yt:L_NEW · r2 · tier1 · 2026-10-04')] });
check('tamer copy made once (r2 exists)', !p.tame.some(t => t.key === 'tier1'));

p = S.plan({ newestLong: newest, kindOf, ads: [ad('tier1', '3', 'L_NEW', 'PAUSED'), ad('tier1', '10', 'L_NEW', 'PAUSED', 'DISAPPROVED')] });
check('newest all paused → enable the approved one', p.enable.map(a => a.adId).join() === '3', p.enable);

p = S.plan({ newestLong: newest, kindOf, ads: [ad('tier1', '11', 'MYSTERY'), ad('tier1', '12', null)] });
check('unknown video type → left alone', p.pause.length === 0 && p.unknown.length === 2);
check('missing newest ad → warning', p.warnings.some(w => /tier2: no ad exists/.test(w)));

p = S.plan({ newestLong: null, kindOf, ads: [ad('tier1', '2', 'L_OLD')] });
check('no newest long-form → nothing paused', p.pause.length === 0 && p.warnings.length === 1);

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
