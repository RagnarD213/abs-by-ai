#!/usr/bin/env node
// Four approved Ad 4 formats into its existing trial group. Only create operations.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const ads = require('./client.js');
const dir = path.join(__dirname, 'dgen-ads');
const cfg = JSON.parse(fs.readFileSync(path.join(dir, 'ad4-formats.json')));
const fields = `ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros,
 ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls,
 ad_group_ad.ad.demand_gen_video_responsive_ad.videos,
 ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
 ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines,
 ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
 ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images,
 ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
 ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions`;
const campaignQuery = `SELECT campaign.id, campaign.status, campaign.target_cpa.target_cpa_micros,
 campaign_budget.id, campaign_budget.amount_micros FROM campaign
 WHERE campaign.id IN (24316364155,24305381214,24316408288,24243839443,24308574894)`;
const criteriaQuery = `SELECT ad_group_criterion.resource_name, ad_group_criterion.status,
 ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.audience.audience
 FROM ad_group_criterion WHERE ad_group.id = ${cfg.adGroupId}`;
async function main() {
 const apply = process.argv.includes('--apply');
 assert.equal(cfg.campaignId, '24316364155');
 assert.equal(cfg.adGroupId, '204553317030');
 assert.equal(cfg.twinAdId, '826635661909');
 assert.equal(cfg.videos.length, 4);
 const group = await ads.search(`SELECT campaign.id FROM ad_group WHERE ad_group.id = ${cfg.adGroupId}`);
 assert.equal(group[0].campaign.id, cfg.campaignId);
 const before = await ads.search(`SELECT ${fields} FROM ad_group_ad WHERE campaign.id = ${cfg.campaignId} AND ad_group_ad.status != 'REMOVED'`);
 const twin = before.find(r => r.adGroupAd.ad.id === cfg.twinAdId);
 assert(twin, 'Live 16:9 twin must exist');
 const d = twin.adGroupAd.ad.demandGenVideoResponsiveAd;
 for (const k of ['headlines', 'longHeadlines', 'descriptions'])
  assert.deepEqual(d[k].map(x => x.text), cfg.copyReadBackFromLive[k], `Live ${k} changed`);
 const campaignsBefore = await ads.search(campaignQuery);
 const criteriaBefore = await ads.search(criteriaQuery);
 fs.writeFileSync(path.join(dir, 'ad4-formats.protected-before.json'), JSON.stringify({before,campaignsBefore,criteriaBefore},null,2)+'\n');
 let n = 0;
 const ops = [];
 for (const v of cfg.videos) {
  const name = `${cfg.label} | ${v.version} | vsl`;
  const finalUrl = `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ad4&utm_content=${v.utm}-vsl`;
  const found = before.find(r => r.adGroupAd.ad.name === name);
  if (found) { assert.deepEqual(found.adGroupAd.ad.finalUrls, [finalUrl]); console.log('Already exists: ' + name); continue; }
  const assets = await ads.search(`SELECT asset.resource_name FROM asset WHERE asset.type = 'YOUTUBE_VIDEO' AND asset.youtube_video_asset.youtube_video_id = '${v.youtubeId}'`);
  let asset;
  if (assets.length) asset = assets[0].asset.resourceName;
  else {
   asset = ads.rn.temp('assets', ++n);
   ops.push({assetOperation: {create: {resourceName: asset, name: `yt ${v.youtubeId} Ad 4 ${v.version}`, youtubeVideoAsset: {youtubeVideoId: v.youtubeId}}}});
  }
  const text = a => a.map(x => ({text: x.text}));
  ops.push({adGroupAdOperation: {create: {adGroup: ads.rn.adGroup(cfg.adGroupId), status: 'ENABLED', ad: {name, finalUrls: [finalUrl], demandGenVideoResponsiveAd: {
   videos: [{asset}], headlines: text(d.headlines), longHeadlines: text(d.longHeadlines), descriptions: text(d.descriptions),
   logoImages: d.logoImages.map(x => ({asset: x.asset})), businessName: {text: d.businessName.text}, callToActions: d.callToActions.map(x => ({asset: x.asset}))
  }}}}});
  console.log(`Create ${name} -> ${v.youtubeId} -> ${finalUrl}`);
 }
 assert(ops.every(op => (op.assetOperation || op.adGroupAdOperation)?.create), 'Only asset/ad creation is allowed');
 if (ops.length) {
  const note = 'Approved Ad 4 formats in existing trial group, budget and live 16:9 preserved';
  await ads.mutate(ops, {dryRun: true, note});
  console.log(`validateOnly passed: ${ops.length} operations`);
  if (!apply) return;
  const result = await ads.mutate(ops, {note});
  fs.writeFileSync(path.join(dir, 'ad4-formats.mutation.json'), JSON.stringify(result, null, 2) + '\n');
 }
 if (!apply) return;
 const after = await ads.search(`SELECT ${fields}, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = ${cfg.campaignId} AND ad_group_ad.status != 'REMOVED'`);
 const campaignsAfter = await ads.search(campaignQuery);
 const criteriaAfter = await ads.search(criteriaQuery);
 assert.deepEqual(campaignsAfter, campaignsBefore, 'Campaign budgets/status/bids must remain unchanged');
 assert.deepEqual(criteriaAfter, criteriaBefore, 'Audience/criteria must remain unchanged');
 for (const old of before) {
  const current = JSON.parse(JSON.stringify(after.find(r => r.adGroupAd.ad.id === old.adGroupAd.ad.id)));
  delete current.adGroupAd.policySummary;
  assert.deepEqual(current, old, `Existing ad ${old.adGroupAd.ad.id} changed`);
 }
 const created = after.filter(r => cfg.videos.some(v => r.adGroupAd.ad.name === `${cfg.label} | ${v.version} | vsl`));
 assert.equal(created.length, 4);
 const assets = await ads.search(`SELECT asset.id, asset.resource_name, asset.youtube_video_asset.youtube_video_id FROM asset WHERE asset.type = 'YOUTUBE_VIDEO' AND asset.youtube_video_asset.youtube_video_id IN (${cfg.videos.map(v => `'${v.youtubeId}'`).join(',')})`);
 for (const r of created) {
  assert.equal(r.adGroupAd.status, 'ENABLED');
  for (const k of ['headlines','longHeadlines','descriptions']) assert.deepEqual(r.adGroupAd.ad.demandGenVideoResponsiveAd[k].map(x => x.text), cfg.copyReadBackFromLive[k]);
  for (const k of ['logoImages','businessName','callToActions']) assert.deepEqual(r.adGroupAd.ad.demandGenVideoResponsiveAd[k],d[k], `Live ${k} must be cloned exactly`);
  console.log(`Read back ${r.adGroupAd.ad.id}: ${r.adGroupAd.status} ${JSON.stringify(r.adGroupAd.policySummary)}`);
 }
 fs.writeFileSync(path.join(dir, 'ad4-formats.result.json'), JSON.stringify({at: new Date().toISOString(), campaignId: cfg.campaignId, adGroupId: cfg.adGroupId, campaignsBefore, campaignsAfter, criteriaBefore, criteriaAfter, created, assets, existingAdsUnchanged: true}, null, 2) + '\n');
}
main().catch(e => {console.error('FAILED: ' + e.message); process.exitCode = 1;}).finally(() => ads.close());
