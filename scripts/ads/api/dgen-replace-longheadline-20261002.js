#!/usr/bin/env node
/**
 * Replace the clickbait-disapproved long headline family ("AI genius / Busy dad discovers how to use AI to lose his
 * stubborn belly fat. Video reveals full story") with Dan's line, on every non-removed ad in the account that carries
 * it (Dan, 2026-10-02). Only that one long headline slot changes; the other long headlines, headlines and descriptions
 * are re-sent unchanged. Old state saved beside the result.
 *   node scripts/ads/api/dgen-replace-longheadline-20261002.js [--apply]
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const OLD = new Set([
  'AI genius discovers how to use AI to lose his stubborn belly fat. Video reveals full story',
  'Busy dad discovers how to use AI to lose his stubborn belly fat. Video reveals full story',
]);
const NEW = 'Korean AI prodigy discovers how to use AI to lose belly fat. Video reveals full story.';

(async () => {
  const apply = process.argv.includes('--apply');
  if (NEW.length > 90 || /—|–/.test(NEW)) throw new Error('bad new line: ' + NEW.length);
  const rows = await ads.search(`SELECT campaign.id, campaign.name, campaign.status, ad_group.name, ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name,
    ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED'`);
  const hit = rows.filter(r => ((r.adGroupAd.ad.demandGenVideoResponsiveAd || {}).longHeadlines || []).some(h => OLD.has(h.text)));
  console.log(`${hit.length} ad(s) carry the line (new line is ${NEW.length} characters)`);
  const ops = hit.map(r => {
    const longs = r.adGroupAd.ad.demandGenVideoResponsiveAd.longHeadlines.map(h => ({ text: OLD.has(h.text) ? NEW : h.text }));
    console.log(`  ${r.campaign.id} ${r.campaign.status} | ${r.adGroup.name} | ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status}`);
    return { adOperation: { update: { resourceName: ads.rn.ad(r.adGroupAd.ad.id), demandGenVideoResponsiveAd: { longHeadlines: longs } },
      updateMask: 'demand_gen_video_responsive_ad.long_headlines' } };
  });
  const note = 'replace clickbait-disapproved long headline (Dan, 2026-10-02)';
  await ads.mutate(ops, { dryRun: true, note });
  console.log(`dry run OK: ${ops.length} ads`);
  if (!apply) { await ads.close(); return; }
  const dir = path.join(__dirname, 'dgen-ads');
  fs.writeFileSync(path.join(dir, 'longheadline-replace-20261002.before.json'), JSON.stringify(hit, null, 1));
  await ads.mutate(ops, { note });
  const ids = hit.map(r => r.adGroupAd.ad.id).join(',');
  const back = await ads.search(`SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status,
    ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines FROM ad_group_ad WHERE ad_group_ad.ad.id IN (${ids})`);
  fs.writeFileSync(path.join(dir, 'longheadline-replace-20261002.result.json'), JSON.stringify({ at: new Date().toISOString(), back }, null, 1));
  for (const b of back) {
    const l = b.adGroupAd.ad.demandGenVideoResponsiveAd.longHeadlines.map(h => h.text);
    console.log(`  ad ${b.adGroupAd.ad.id} ${b.adGroupAd.status} ${b.adGroupAd.policySummary.reviewStatus}/${b.adGroupAd.policySummary.approvalStatus} | new line present: ${l.includes(NEW)} | old gone: ${!l.some(t => OLD.has(t))} | ${l.length} long headlines`);
  }
  await ads.close();
})().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
