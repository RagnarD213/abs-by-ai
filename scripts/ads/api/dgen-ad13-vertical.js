#!/usr/bin/env node
// Add only the two approved Ad 13 vertical formats to its existing trial group.
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const dir = path.join(__dirname, 'dgen-ads');
const cfg = JSON.parse(fs.readFileSync(path.join(dir, 'ad13-vertical.json'), 'utf8'));
const fields = `ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls,
 ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
 ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
 ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
 ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions`;
const readGroup = () => ads.search(`SELECT ${fields} FROM ad_group_ad WHERE ad_group.id = ${cfg.adGroupId} AND ad_group_ad.status != 'REMOVED'`);
const texts = a => (a || []).map(x => ({ text: x.text }));
async function protectedState() {
 return {
  campaigns: await ads.search(`SELECT campaign.id, campaign.status, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, campaign_budget.id, campaign_budget.amount_micros FROM campaign WHERE campaign.id IN (24316364155,24305381214,24316408288,24243839443,24308574894)`),
  group: await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, ad_group.optimized_targeting_enabled FROM ad_group WHERE ad_group.id = ${cfg.adGroupId}`),
  criteria: await ads.search(`SELECT ad_group_criterion.resource_name, ad_group_criterion.type, ad_group_criterion.status, ad_group_criterion.negative, ad_group_criterion.audience.audience, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE ad_group.id = ${cfg.adGroupId} AND ad_group_criterion.status != 'REMOVED'`),
  twin: (await readGroup()).find(r => r.adGroupAd.ad.id === cfg.twinAdId),
 };
}
async function main() {
 const apply = process.argv.includes('--apply');
 if (cfg.campaignId !== '24316364155' || cfg.adGroupId !== '204553316830' || cfg.twinAdId !== '826635661894') throw new Error('Unexpected target');
 const g = await ads.search(`SELECT ad_group.id, campaign.id, campaign.status FROM ad_group WHERE ad_group.id = ${cfg.adGroupId}`);
 if (!g.length || g[0].campaign.id !== cfg.campaignId) throw new Error('Wrong campaign');
 const before = await protectedState();
 const beforeFile = path.join(dir, 'ad13-vertical.protected-before.json');
 if (!fs.existsSync(beforeFile)) fs.writeFileSync(beforeFile, JSON.stringify(before,null,2)+'\n');
 const rows = await readGroup();
 const twin = rows.find(r => r.adGroupAd.ad.id === cfg.twinAdId);
 if (!twin) throw new Error('Live 16:9 ad missing');
 const d = twin.adGroupAd.ad.demandGenVideoResponsiveAd;
 for (const k of ['headlines','longHeadlines','descriptions'])
  if (JSON.stringify(d[k].map(x=>x.text)) !== JSON.stringify(cfg.copyReadBackFromLive[k])) throw new Error('Live copy changed: '+k);
 const ops = []; let n = 0;
 for (const v of cfg.videos) {
  const name = `${cfg.label} | ${v.version} | vsl`;
  const exists = rows.find(r=>r.adGroupAd.ad.name===name);
  if (exists) { console.log('Already exists: '+exists.adGroupAd.ad.id+' '+name); continue; }
  const found = await ads.search(`SELECT asset.id, asset.resource_name FROM asset WHERE asset.type = 'YOUTUBE_VIDEO' AND asset.youtube_video_asset.youtube_video_id = '${v.youtubeId}'`);
  let asset = found.length ? found[0].asset.resourceName : ads.rn.temp('assets',++n);
  if (!found.length) ops.push({assetOperation:{create:{resourceName:asset,name:`yt ${v.youtubeId} Ad 13 ${v.version}`,youtubeVideoAsset:{youtubeVideoId:v.youtubeId}}}});
  const url = new URL(twin.adGroupAd.ad.finalUrls[0]);
  url.searchParams.set('utm_content',v.utm+'-vsl');
  const ad = {videos:[{asset}],headlines:texts(d.headlines),longHeadlines:texts(d.longHeadlines),descriptions:texts(d.descriptions),
   logoImages:d.logoImages.map(x=>({asset:x.asset})),businessName:{text:d.businessName.text},callToActions:d.callToActions.map(x=>({asset:x.asset}))};
  ops.push({adGroupAdOperation:{create:{adGroup:ads.rn.adGroup(cfg.adGroupId),status:'ENABLED',ad:{name,finalUrls:[url.toString()],demandGenVideoResponsiveAd:ad}}}});
  console.log('Create '+name+' -> '+url.toString());
 }
 const opsFile = path.join(dir,'ad13-vertical.operations.json');
 fs.writeFileSync(opsFile,JSON.stringify(ops,null,2)+'\n');
 if (ops.some(x=>!x.assetOperation&&!x.adGroupAdOperation)) throw new Error('Unexpected operation');
 if (ops.length) {
  await ads.mutate(ops,{dryRun:true,note:'Ad 13 approved vertical formats, existing trial group'});
  console.log('Google validateOnly passed: '+ops.length+' operations');
  if (!apply) return;
  await ads.mutate(ops,{note:'Ad 13 approved vertical formats, existing trial group'});
 }
 if (!apply) return;
 const back = await ads.search(`SELECT ad_group.id, ${fields}, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE ad_group.id = ${cfg.adGroupId} AND ad_group_ad.status != 'REMOVED'`);
 const after = await protectedState();
 const unchanged = JSON.stringify(before)===JSON.stringify(after);
 const baselineUnchanged = JSON.stringify(JSON.parse(fs.readFileSync(beforeFile,'utf8')))===JSON.stringify(after);
 fs.writeFileSync(path.join(dir,'ad13-vertical.result.json'),JSON.stringify({at:new Date().toISOString(),readBack:back,protectedState:after,protectedUnchanged:unchanged,baselineUnchanged},null,2)+'\n');
 if (!unchanged || !baselineUnchanged) throw new Error('Protected settings changed; inspect readback');
 for(const r of back) {
  const a=r.adGroupAd; console.log(a.ad.id+' '+a.status+' '+a.policySummary.reviewStatus+'/'+a.policySummary.approvalStatus+' '+a.ad.name);
  for(const k of ['headlines','longHeadlines','descriptions']) if(JSON.stringify(a.ad.demandGenVideoResponsiveAd[k].map(x=>x.text))!==JSON.stringify(cfg.copyReadBackFromLive[k]))throw new Error('Readback copy differs');
 }
 console.log('Budget, campaigns, bids, audiences and live 16:9 are unchanged');
}
main().catch(e=>{console.error('FAILED: '+e.message);process.exitCode=1;}).finally(()=>ads.close());
