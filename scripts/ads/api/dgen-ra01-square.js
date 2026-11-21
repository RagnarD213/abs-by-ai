#!/usr/bin/env node
/**
 * Add the approved RA-01 1:1 square as one more ad in the existing RA-01 ad group of the TRIAL campaign (24316364155).
 *   node scripts/ads/api/dgen-ra01-square.js            # plan + Google validateOnly dry run
 *   node scripts/ads/api/dgen-ra01-square.js --apply    # create the ad, read it back
 * The copy is cloned from the live 16:9 twin (Dan's own lines), and refused unless it still equals the readback
 * recorded in dgen-ads/ra01-square.json. Reuses the ad group; never creates a campaign, group or audience.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { rn, CID } = ads;
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'dgen-ads', 'ra01-square.json'), 'utf8'));

async function main() {
  const apply = process.argv.includes('--apply');
  const grp = await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, campaign.id, campaign.status FROM ad_group WHERE ad_group.id = ${cfg.adGroupId}`);
  if (!grp.length || String(grp[0].campaign.id) !== cfg.campaignId) throw new Error('RA-01 ad group is not in the trial campaign');
  const rows = await ads.search(`SELECT ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls,
      ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
      ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
      ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
      ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions
      FROM ad_group_ad WHERE ad_group.id = ${cfg.adGroupId} AND ad_group_ad.status != 'REMOVED'`);
  const twin = rows.find(r => r.adGroupAd.ad.id === cfg.twinAdId);
  if (!twin) throw new Error('twin ad ' + cfg.twinAdId + ' not found');
  const d = twin.adGroupAd.ad.demandGenVideoResponsiveAd;
  const t = (a) => (a || []).map(x => x.text);
  for (const k of ['headlines', 'longHeadlines', 'descriptions'])
    if (JSON.stringify(t(d[k])) !== JSON.stringify(cfg.copyReadBackFromLive[k])) throw new Error(`live ${k} differ from the recorded readback; re-read and update the config`);

  const adName = `${cfg.label} | ${cfg.video.version} | vsl`;
  if (rows.some(r => r.adGroupAd.ad.name === adName)) { console.log(`ad "${adName}" already exists, nothing to do`); await ads.close(); return; }
  const assets = await ads.search(`SELECT asset.id, asset.resource_name FROM asset WHERE asset.type = 'YOUTUBE_VIDEO' AND asset.youtube_video_asset.youtube_video_id = '${cfg.video.youtubeId}'`);
  const ops = []; const plan = []; let assetRn;
  if (assets.length) { assetRn = assets[0].asset.resourceName; plan.push(`reuse video asset ${assets[0].asset.id}`); }
  else {
    assetRn = rn.temp('assets', 1);
    ops.push({ assetOperation: { create: { resourceName: assetRn, name: `yt ${cfg.video.youtubeId} ${cfg.label} ${cfg.video.version}`, youtubeVideoAsset: { youtubeVideoId: cfg.video.youtubeId } } } });
    plan.push(`create video asset for ${cfg.video.youtubeId}`);
  }
  const finalUrl = `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-ra01&utm_content=${cfg.video.utm}-vsl`;
  const texts = (arr) => (arr || []).map(x => ({ text: x.text }));
  ops.push({ adGroupAdOperation: { create: { adGroup: rn.adGroup(cfg.adGroupId), status: 'ENABLED', ad: { name: adName, finalUrls: [finalUrl],
    demandGenVideoResponsiveAd: { videos: [{ asset: assetRn }], headlines: texts(d.headlines), longHeadlines: texts(d.longHeadlines), descriptions: texts(d.descriptions),
      logoImages: d.logoImages.map(x => ({ asset: x.asset })), businessName: { text: d.businessName.text }, callToActions: d.callToActions.map(x => ({ asset: x.asset })) } } } } });
  plan.push(`REUSE ad group ${cfg.adGroupId} (${grp[0].adGroup.name}, ${grp[0].adGroup.status}); create ad "${adName}" -> ${finalUrl}`);
  console.log('PLAN\n  ' + plan.join('\n  '));
  const note = 'dgen-ra01-square: approved RA-01 1:1 into trial ad group';
  await ads.mutate(ops, { dryRun: true, note });
  console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
  if (!apply) { console.log('pass --apply to build'); await ads.close(); return; }
  const res = await ads.mutate(ops, { note });
  console.log('APPLIED\n  ' + res.results.join('\n  '));
  const back = await ads.search(`SELECT ad_group.id, ad_group.name, ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls,
      ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
      ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status
      FROM ad_group_ad WHERE ad_group.id = ${cfg.adGroupId} AND ad_group_ad.ad.name = '${adName}'`);
  fs.writeFileSync(path.join(__dirname, 'dgen-ads', 'ra01-square.result.json'), JSON.stringify({ at: new Date().toISOString(), results: res.results, readBack: back }, null, 1));
  const ad = back[0].adGroupAd.ad, dd = ad.demandGenVideoResponsiveAd;
  console.log(`READ BACK ad ${ad.id} ${back[0].adGroupAd.status} ${back[0].adGroupAd.policySummary.reviewStatus}/${back[0].adGroupAd.policySummary.approvalStatus} | ${ad.name} | ${ad.finalUrls[0]}`);
  for (const k of ['headlines', 'longHeadlines', 'descriptions'])
    console.log(`  ${k} identical to live twin: ${JSON.stringify(t(dd[k])) === JSON.stringify(cfg.copyReadBackFromLive[k])}`);
  await ads.close();
}
main().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
