#!/usr/bin/env node
/**
 * Dan, 2026-11-18: pause every ad in the five engagement campaigns so the re-edited "Got Abs? You need to see this."
 * ads become the only ones, and set the geo tier 2 ad group's bid to $0.05 (ad group target CPA, with the ad group
 * CPC placeholder kept equal).
 *   node scripts/ads/api/engagement-pause-others-20261118.js [--apply]
 * Pass --keep <ad id,...> to leave specific ads (the new Got Abs ads) enabled. Old state saved beside the result.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const CAMPAIGNS = [24163535721, 24122099676, 24422704023, 24316408288, 24437265255];
const TIER2_AD_GROUP = '197884856303';
(async () => {
  const apply = process.argv.includes('--apply');
  const ki = process.argv.indexOf('--keep');
  const keep = new Set(ki > 0 ? process.argv[ki + 1].split(',') : []);
  const rows = await ads.search(`SELECT campaign.id, ad_group.id, ad_group.name, ad_group_ad.resource_name, ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name
    FROM ad_group_ad WHERE campaign.id IN (${CAMPAIGNS.join(',')}) AND ad_group_ad.status = 'ENABLED'`);
  const hit = rows.filter(r => !keep.has(String(r.adGroupAd.ad.id)) && !/Got Abs/i.test(r.adGroupAd.ad.name || ''));
  console.log(`${rows.length} enabled ads; pausing ${hit.length}, keeping ${rows.length - hit.length}`);
  const byCamp = {};
  for (const r of hit) byCamp[r.campaign.id] = (byCamp[r.campaign.id] || 0) + 1;
  console.log('per campaign:', JSON.stringify(byCamp));
  const ops = hit.map(r => ({ adGroupAdOperation: { update: { resourceName: r.adGroupAd.resourceName, status: 'PAUSED' }, updateMask: 'status' } }));
  const bid = [{ adGroupOperation: { update: { resourceName: ads.rn.adGroup(TIER2_AD_GROUP), targetCpaMicros: '50000', cpcBidMicros: '50000' }, updateMask: 'target_cpa_micros,cpc_bid_micros' } }];
  const note = 'engagement: pause all but Got Abs ads; tier 2 bid $0.05 (Dan, 2026-11-18)';
  if (ops.length) await ads.mutate(ops, { dryRun: true, note });
  await ads.mutate(bid, { dryRun: true, note });
  console.log('dry runs OK');
  if (!apply) { await ads.close(); return; }
  const dir = path.join(__dirname, 'dgen-ads');
  const before = await ads.search(`SELECT ad_group.id, ad_group.cpc_bid_micros, ad_group.target_cpa_micros FROM ad_group WHERE ad_group.id = ${TIER2_AD_GROUP}`);
  fs.writeFileSync(path.join(dir, 'engagement-pause-others-20261118.before.json'), JSON.stringify({ ads: hit, tier2: before }, null, 1));
  if (ops.length) await ads.mutate(ops, { note });
  await ads.mutate(bid, { note });
  const left = await ads.search(`SELECT campaign.id, ad_group_ad.ad.id, ad_group_ad.ad.name FROM ad_group_ad WHERE campaign.id IN (${CAMPAIGNS.join(',')}) AND ad_group_ad.status = 'ENABLED'`);
  const t2 = await ads.search(`SELECT ad_group.id, ad_group.cpc_bid_micros, ad_group.target_cpa_micros FROM ad_group WHERE ad_group.id = ${TIER2_AD_GROUP}`);
  fs.writeFileSync(path.join(dir, 'engagement-pause-others-20261118.result.json'), JSON.stringify({ at: new Date().toISOString(), enabledLeft: left, tier2: t2 }, null, 1));
  console.log(`enabled ads left: ${left.length}`);
  console.log('tier 2 ad group:', JSON.stringify(t2.map(x => x.adGroup)));
  await ads.close();
})().catch(e => { console.error(e.message || e); process.exit(1); });
