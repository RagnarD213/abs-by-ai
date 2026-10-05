#!/usr/bin/env node
// Add only the four approved Ad 4 formats to existing conversion remarketing groups.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert/strict');
const ads = require('./client.js');
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'dgen-ads/ad4-formats.json')));
const campaignId = '24305381214';
const groups = [{id:'206411886211',key:'site'}, {id:'201604959278',key:'yt'}];
const sourceIds = ['826899511366','826899511387','826899464146','826899511576'];
const prefix = path.join(__dirname, 'dgen-ads/ad4-remarketing-20261005');
const fields = `campaign.id, ad_group.id, ad_group_ad.status,
 ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls,
 ad_group_ad.ad.demand_gen_video_responsive_ad.videos,
 ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
 ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines,
 ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
 ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images,
 ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
 ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions`;
const queries = {
 campaigns: `SELECT campaign.id,campaign.name,campaign.status,campaign.advertising_channel_type,
  campaign.target_cpa.target_cpa_micros,campaign_budget.id,campaign_budget.amount_micros
  FROM campaign WHERE campaign.status != 'REMOVED' ORDER BY campaign.id`,
 groups: `SELECT campaign.id,ad_group.id,ad_group.name,ad_group.status,ad_group.target_cpa_micros,
  ad_group.optimized_targeting_enabled FROM ad_group WHERE ad_group.status != 'REMOVED' ORDER BY ad_group.id`,
 criteria: `SELECT ad_group_criterion.resource_name,ad_group_criterion.status,ad_group_criterion.type,
  ad_group_criterion.negative,ad_group_criterion.audience.audience,
  ad_group_criterion.location.geo_target_constant,ad_group_criterion.language.language_constant
  FROM ad_group_criterion WHERE ad_group_criterion.status != 'REMOVED'`,
 goals: `SELECT campaign.id,campaign_conversion_goal.category,campaign_conversion_goal.origin,
  campaign_conversion_goal.biddable FROM campaign_conversion_goal ORDER BY campaign.id`,
 audiences: `SELECT audience.id,audience.name,audience.dimensions,audience.exclusion_dimension
  FROM audience WHERE audience.status = 'ENABLED' ORDER BY audience.id`,
 existingAds: `SELECT ${fields} FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED' ORDER BY ad_group_ad.ad.id`
};
const save = (suffix, value) => fs.writeFileSync(prefix+suffix, JSON.stringify(value,null,2)+'\n');
const hash = value => crypto.createHash('sha256').update(JSON.stringify(value)).digest('hex');
async function snapshot() {
 const result = await Promise.allSettled(Object.entries(queries).map(async ([key,query]) => [key,await ads.search(query)]));
 for (const r of result) if (r.status === 'rejected') throw r.reason;
 return Object.fromEntries(result.map(r => [r.value[0],r.value[1].sort((a,b)=>JSON.stringify(a).localeCompare(JSON.stringify(b)))]));
}
async function main() {
 const apply = process.argv.includes('--apply');
 const before = await snapshot();
 const campaign = before.campaigns.find(r => r.campaign.id===campaignId);
 assert.equal(campaign.campaign.status,'ENABLED');
 assert.equal(campaign.campaign.advertisingChannelType,'DEMAND_GEN');
 const goals = before.goals.filter(r=>r.campaign.id===campaignId && r.campaignConversionGoal.biddable);
 assert.equal(goals.length,1);
 assert.equal(goals[0].campaignConversionGoal.category,'SIGNUP');
 assert.equal(goals[0].campaignConversionGoal.origin,'WEBSITE');
 for (const g of groups) {
  const row=before.groups.find(r=>r.adGroup.id===g.id);
  assert.equal(row.campaign.id,campaignId);
  assert.equal(row.adGroup.status,'ENABLED');
 }
 const source = before.existingAds.filter(r=>sourceIds.includes(r.adGroupAd.ad.id));
 assert.equal(source.length,4);
 const names=[];const ops=[];
 for (const v of cfg.videos) {
  const row=source.find(r=>r.adGroupAd.ad.name===`${cfg.label} | ${v.version} | vsl`);
  assert(row,'Approved source format must exist');
  assert.equal(row.campaign.id,cfg.campaignId);
  assert.equal(row.adGroup.id,cfg.adGroupId);
  assert.equal(row.adGroupAd.status,'ENABLED');
  const src=row.adGroupAd.ad;
  for (const g of groups) {
   const name=src.name+` | rmktg-${g.key}`;names.push(name);
   const url=`https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-rmktg-${g.key}&utm_content=ad4-${v.utm}-vsl`;
   const found=before.existingAds.find(r=>r.campaign.id===campaignId && r.adGroup.id===g.id && r.adGroupAd.ad.name===name);
   if (found) {
    assert.equal(found.adGroupAd.status,'ENABLED');
    assert.deepEqual(found.adGroupAd.ad.finalUrls,[url]);
    assert.deepEqual(found.adGroupAd.ad.demandGenVideoResponsiveAd,src.demandGenVideoResponsiveAd);
    console.log('Already exists: '+name);continue;
   }
   ops.push({adGroupAdOperation:{create:{adGroup:ads.rn.adGroup(g.id),status:'ENABLED',ad:{
    name,finalUrls:[url],demandGenVideoResponsiveAd:src.demandGenVideoResponsiveAd
   }}}});
   console.log(`Create ${v.version} in ${g.key} group ${g.id}`);
  }
 }
 assert(ops.every(op=>op.adGroupAdOperation?.create && groups.some(g=>op.adGroupAdOperation.create.adGroup===ads.rn.adGroup(g.id))));
 const protectedBefore = Object.fromEntries(Object.entries(before).map(([key,value])=>[key,{count:value.length,sha256:hash(value)}]));
 save('.before.json',{at:new Date().toISOString(),campaign:campaign,source,groups:before.groups.filter(r=>r.campaign.id===campaignId),protectedBefore});
 save('.operations.json',ops);
 if (ops.length) {
  const note='Dan approved four Ad 4 formats in live conversion remarketing only; budgets and engagement preserved';
  await ads.mutate(ops,{dryRun:true,note});
  console.log(`validateOnly passed: ${ops.length} ad create operations`);
  if (!apply) return;
  save('.mutation.json',await ads.mutate(ops,{note}));
 }
 if (!apply) return;
 const after=await snapshot();
 for (const key of Object.keys(before).filter(k=>k!=='existingAds')) assert.deepEqual(after[key],before[key],`Protected ${key} must remain unchanged`);
 const oldIds=new Set(before.existingAds.map(r=>r.adGroupAd.ad.id));
 assert.deepEqual(after.existingAds.filter(r=>oldIds.has(r.adGroupAd.ad.id)),before.existingAds,'Every pre-existing account ad must remain unchanged');
 const created=after.existingAds.filter(r=>r.campaign.id===campaignId && names.includes(r.adGroupAd.ad.name));
 assert.equal(created.length,8);
 for (const row of created) {
  const src=source.find(r=>row.adGroupAd.ad.name.startsWith(r.adGroupAd.ad.name+' | rmktg-'));
  assert.deepEqual(row.adGroupAd.ad.demandGenVideoResponsiveAd,src.adGroupAd.ad.demandGenVideoResponsiveAd);
  assert.equal(row.adGroupAd.status,'ENABLED');
 }
 const policies=await ads.search(`SELECT ad_group.id,ad_group_ad.ad.id,ad_group_ad.policy_summary.review_status,
  ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id=${campaignId} AND ad_group_ad.status!='REMOVED'`);
 for (const row of created) row.adGroupAd.policySummary=policies.find(r=>r.adGroupAd.ad.id===row.adGroupAd.ad.id).adGroupAd.policySummary;
 save('.result.json',{at:new Date().toISOString(),campaignId,campaignBefore:campaign,campaignAfter:after.campaigns.find(r=>r.campaign.id===campaignId),
  created,protectedBefore,protectedSettingsUnchanged:true,allExistingAccountAdsUnchanged:true,engagementCampaignsUntouched:true});
 for (const row of created) console.log(`${row.adGroup.id} | ${row.adGroupAd.ad.id} | ENABLED | ${JSON.stringify(row.adGroupAd.policySummary)}`);
}
main().catch(e=>{console.error('FAILED: '+e.message);process.exitCode=1;}).finally(()=>ads.close());
