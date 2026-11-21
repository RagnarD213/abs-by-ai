#!/usr/bin/env node
/**
 * Rewrite the long headlines and descriptions of the six ads in the Demand Gen trial campaign 24316364155 to Dan's
 * "sell the click" style (skill /ad-copy, calibration of 2026-10-02). Headlines are not touched. Every format of an
 * ad gets the same copy. Lines marked DAN are his own, word for word, from Performance Max 24308574894.
 *
 *   node scripts/ads/api/dgen-trial-longcopy-20261002.js            # plan + Google dry run
 *   node scripts/ads/api/dgen-trial-longcopy-20261002.js --apply    # write, read back; old copy saved beside the result
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const CAMPAIGN = 24316364155;

const DAN = {
  why: "Here's why I stopped paying a personal trainer and use an AI trainer instead.",
  despise: 'Trainers despise this AI fitness app. See why men are replacing their trainer with AI.',
  app: 'AI fitness app shows you how to lose stomach fat and get abs. Try it free for 7 days!',
  genius: 'AI genius discovers how to use AI to lose his stubborn belly fat. Video reveals full story',
  struggled: 'I struggled with belly fat until I discovered how to use an AI trainer to get abs.',
  appD: 'This AI app shows you how to lose your belly fat. Try it free for 7 days.',
  plans: 'AI plans workouts and meals around your schedule, equipment and starting point.',
};
const COPY = {
  'Ad 3 Stop Paying Human Trainers': {
    long: [DAN.why, DAN.despise, 'I fired my personal trainer and got abs at 40 with AI. Video reveals full story'],
    desc: ["Most personal trainers charge $70 to $200 an hour. Here's how I use AI for the same job.", DAN.struggled, DAN.appD] },
  'Ad 13 The Cost Of Getting Abs': {
    long: ['I added up what trainers, nutritionists and supplements cost me. See what AI does instead', DAN.despise, DAN.app],
    desc: ['Stop paying trainers and nutritionists to lose your belly fat. See how I use AI instead.', DAN.struggled,
      'See what getting abs was supposed to cost me, and how AI does the same job for less.'] },
  'Ad 10 Busy Dad Fitness': {
    long: ['Busy dad discovers how to use AI to lose his stubborn belly fat. Video reveals full story',
      'No time for the gym? See how this busy dad used AI to lose his dad bod and get abs at 40.', DAN.app],
    desc: ['I had a dad bod at 38 and abs at 40. See how I used AI to lose my stubborn belly fat.',
      'This AI app shows busy dads how to lose their belly fat. Try it free for 7 days.', DAN.plans] },
  "Ad 6 You're Not Too Old": {
    long: ["Think you're too old to get abs? See how I lost my stubborn belly fat and got abs at 40.", DAN.genius,
      'AI fitness app shows men 40+ how to lose stomach fat and get abs. Try it free for 7 days!'],
    desc: ["You're not too old to get abs. I got mine at 40 with an AI trainer. See how I did it.", DAN.struggled,
      'This AI app shows men 40+ how to lose their belly fat. Try it free for 7 days.'] },
  'Ad 4 Stop Wasting Money On Supplements': {
    long: ["Here's how AI fixed my supplements. Find which supplements are a waste of money with AI",
      'Take a photo of your supplements and AI tells you which ones are a waste of your money.',
      'Supplement companies despise this AI app. See why men are cutting their supplement bill.'],
    desc: ['Many supplements are a waste of money. AI can identify which supplements you should cut.',
      'I was wasting money on supplements until AI audited my stack. See what it told me to cut.',
      'This AI app audits your supplements from one photo. Try it free for 7 days.'] },
  'RA-01 AI Got Me Abs': {
    long: [DAN.genius, 'See how I used AI to lose my stubborn stomach fat and get six pack abs at 40.', DAN.app],
    desc: [DAN.struggled, 'AI built my workouts, planned my meals and tracked my macros. See how I got abs at 40.', DAN.appD] },
};

(async () => {
  const apply = process.argv.includes('--apply');
  for (const [k, c] of Object.entries(COPY)) for (const t of [...c.long, ...c.desc]) {
    if (t.length > 90) throw new Error(`${k}: over 90 characters (${t.length}): ${t}`);
    if (/—|–|\btrick\b/i.test(t)) throw new Error(`${k}: banned character or word: ${t}`);
  }
  const rows = await ads.search(`SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines,
    ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions FROM ad_group_ad WHERE campaign.id = ${CAMPAIGN} AND ad_group_ad.status != 'REMOVED'`);
  const ops = [];
  for (const r of rows) {
    const c = COPY[r.adGroup.name]; if (!c) throw new Error('no copy for ad group ' + r.adGroup.name);
    ops.push({ adOperation: { update: { resourceName: ads.rn.ad(r.adGroupAd.ad.id),
      demandGenVideoResponsiveAd: { longHeadlines: c.long.map(text => ({ text })), descriptions: c.desc.map(text => ({ text })) } },
      updateMask: 'demand_gen_video_responsive_ad.long_headlines,demand_gen_video_responsive_ad.descriptions' } });
  }
  const note = 'trial campaign long headlines + descriptions rewritten to sell the click (Dan, 2026-10-02)';
  await ads.mutate(ops, { dryRun: true, note });
  console.log(`dry run OK: ${ops.length} ads`);
  if (apply) {
    const dir = path.join(__dirname, 'dgen-ads');
    fs.writeFileSync(path.join(dir, 'trial-longcopy-20261002.before.json'), JSON.stringify(rows, null, 1));
    await ads.mutate(ops, { note });
    const back = await ads.search(`SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status,
      ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions
      FROM ad_group_ad WHERE campaign.id = ${CAMPAIGN} AND ad_group_ad.status != 'REMOVED'`);
    fs.writeFileSync(path.join(dir, 'trial-longcopy-20261002.result.json'), JSON.stringify({ at: new Date().toISOString(), back }, null, 1));
    let bad = 0;
    for (const r of back) { const c = COPY[r.adGroup.name], d = r.adGroupAd.ad.demandGenVideoResponsiveAd;
      const ok = JSON.stringify(d.longHeadlines.map(x => x.text)) === JSON.stringify(c.long) && JSON.stringify(d.descriptions.map(x => x.text)) === JSON.stringify(c.desc);
      if (!ok) bad++;
      console.log(`${ok ? 'OK ' : 'MISMATCH'} ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary.reviewStatus}/${r.adGroupAd.policySummary.approvalStatus} headlines ${d.headlines.length} | ${r.adGroupAd.ad.name}`); }
    console.log(bad ? `${bad} MISMATCH` : `APPLIED and read back: ${back.length} ads match`);
  }
  await ads.close();
})().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
