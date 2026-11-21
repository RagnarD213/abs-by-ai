#!/usr/bin/env node
/**
 * Pause, then remove, every non-removed ad for one video across the account (Dan, 2026-11-18: the Zepbound
 * engagement ads RO-28 yt:eLV6EluvyD0 were disapproved/limited for restricted drug terms; "Pause and delete all of the ads").
 *   node scripts/ads/api/remove-ads-for-video-20261118.js            list + dry run
 *   node scripts/ads/api/remove-ads-for-video-20261118.js --apply    pause, then remove, then read back
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const VIDEO = 'eLV6EluvyD0';

(async () => {
  const apply = process.argv.includes('--apply');
  const rows = await ads.search(`SELECT campaign.id, campaign.name, ad_group.name, ad_group_ad.resource_name, ad_group_ad.status,
    ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.policy_summary.approval_status FROM ad_group_ad
    WHERE ad_group_ad.status != 'REMOVED' AND ad_group_ad.ad.name LIKE '%${VIDEO}%'`);
  console.log(`${rows.length} ad(s):`);
  for (const r of rows) console.log(`  ${r.campaign.id} | ${r.adGroup.name} | ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary?.approvalStatus} | ${r.adGroupAd.ad.name}`);
  const note = 'pause then remove Zepbound ads (Dan, 2026-11-18)';
  const pause = rows.map(r => ({ adGroupAdOperation: { update: { resourceName: r.adGroupAd.resourceName, status: 'PAUSED' }, updateMask: 'status' } }));
  const remove = rows.map(r => ({ adGroupAdOperation: { remove: r.adGroupAd.resourceName } }));
  await ads.mutate(pause, { dryRun: true, note });
  await ads.mutate(remove, { dryRun: true, note });
  console.log('dry runs OK');
  if (!apply) { await ads.close(); return; }
  const dir = path.join(__dirname, 'dgen-ads');
  fs.writeFileSync(path.join(dir, `remove-${VIDEO}-20261118.before.json`), JSON.stringify(rows, null, 1));
  await ads.mutate(pause, { note });
  console.log('paused');
  await ads.mutate(remove, { note });
  console.log('removed');
  const ids = rows.map(r => r.adGroupAd.ad.id).join(',');
  const back = await ads.search(`SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status FROM ad_group_ad WHERE ad_group_ad.ad.id IN (${ids})`);
  fs.writeFileSync(path.join(dir, `remove-${VIDEO}-20261118.result.json`), JSON.stringify({ at: new Date().toISOString(), back }, null, 1));
  for (const b of back) console.log(`  ${b.adGroupAd.ad.id} ${b.adGroupAd.status}`);
  const left = await ads.search(`SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group_ad.status != 'REMOVED' AND ad_group_ad.ad.name LIKE '%${VIDEO}%'`);
  console.log(`remaining non-removed Zepbound ads: ${left.length}`);
  await ads.close();
})().catch(e => { console.error(e.message || e); process.exit(1); });
