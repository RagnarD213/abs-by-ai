'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const ads = require('../api/client.js');
const release = require('../../blotato/configs/ro28-got-abs.json');
const { createOp, TARGETS } = require('./instant.js');
const { testAdName } = require('./engine.js');
const { lintSet } = require('./lint.js');
const { ads: pausedByDan } = require('../api/dgen-ads/engagement-pause-others-20261118.before.json');

// Exact neutral copy read back from all seven prior RO-28 placements on Nov 18.
const COPY = {
  headlines: [
    'How I Keep The Weight Off At 40',
    'My Weight Maintenance Routine',
    'Weight Maintenance After Abs',
    'Why Lean Men Still Maintain',
    'What The Research Says On Health',
  ],
  longHeadlines: [
    "Here's why I still focus on weight maintenance at 40, even with abs, and the research.",
    'I explain my argument for staying on my maintenance routine and where the research ends.',
    'This video shows my view on weight maintenance and what the research actually covers.',
  ],
  descriptions: [
    'Daniel Rose explains why he keeps up his weight maintenance routine at 40 years old.',
    'Daniel Rose walks through the research and says where it applies and where it does not.',
    'See why Daniel Rose plans to stay on his maintenance routine for life. Try it free 7 days.',
  ],
};
const GROUPS = { tier1: '206274722584', tier2: '197884856303', us: '201123318425' };
const CAMPAIGN_IDS = [...new Set(Object.values(TARGETS).map(target => target.campaign))].join(',');
const PROTECTED = new Set(pausedByDan.map(r => r.adGroupAd.resourceName));
const namePrefix = `AT · ${release.title} · yt:`;
const firstReleaseDay = release.main.slice(0, 10);
const DESTINATION = 'https://absbyai.com/start';
const COPY_MASK = [
  'demand_gen_video_responsive_ad.headlines',
  'demand_gen_video_responsive_ad.long_headlines',
  'demand_gen_video_responsive_ad.descriptions',
  'final_urls',
].join(',');

function domain(url) {
  return new URL(url).hostname.replace(/^www\./, '');
}

async function readAccount() {
  const [groups, rows] = await Promise.all([
    ads.search(`SELECT campaign.id, campaign.status, ad_group.id, ad_group.status, ad_group.cpc_bid_micros,
      ad_group.target_cpa_micros FROM ad_group WHERE campaign.id IN (${CAMPAIGN_IDS}) AND ad_group.status != 'REMOVED'`),
    ads.search(`SELECT campaign.id, ad_group.id, ad_group_ad.resource_name, ad_group_ad.status, ad_group_ad.ad.id,
      ad_group_ad.ad.name, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.approval_status,
      ad_group_ad.policy_summary.review_status, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
      ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions,
      ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines,
      ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions, ad_group_ad.ad.demand_gen_video_responsive_ad.videos
      FROM ad_group_ad WHERE campaign.id IN (${CAMPAIGN_IDS}) AND ad_group_ad.status != 'REMOVED'`),
  ]);
  return { groups, rows };
}

function targetPlan(account, videoId) {
  return Object.entries(TARGETS).map(([key, { campaign, adGroup }]) => {
    const adGroupId = adGroup || GROUPS[key];
    const group = account.groups.find(r => r.adGroup.id === adGroupId && r.campaign.id === campaign);
    assert(group, `Missing ${key} campaign ${campaign} / ad group ${adGroupId}`);
    assert.equal(group.campaign.status, 'ENABLED', `${key} campaign status`);
    assert.equal(group.adGroup.status, 'ENABLED', `${key} ad group status`);
    const groupAds = account.rows.filter(r => r.adGroup.id === adGroupId).map(r => r.adGroupAd.ad);
    const domains = new Set(groupAds.flatMap(ad => (ad.finalUrls || []).map(domain)));
    assert.deepEqual([...domains], [domain(DESTINATION)], `${key} ad group destination domain`);
    const template = groupAds.filter(ad => !ad.name?.startsWith(namePrefix) && ad.finalUrls?.length &&
        ad.demandGenVideoResponsiveAd?.businessName?.text && ad.demandGenVideoResponsiveAd?.logoImages?.length)
      .sort((a, b) => Number(b.id) - Number(a.id))[0];
    assert(template, `Missing existing ${key} business name, logo and final URL`);
    const d = template.demandGenVideoResponsiveAd;
    return {
      key, campaign, adGroupId, domain: [...domains][0], templateAdId: template.id,
      name: testAdName(videoId, key, new Date(release.main), release.title),
      template: { businessName: d.businessName.text, finalUrls: [DESTINATION],
        logoImages: d.logoImages.map(x => x.asset), callToActions: (d.callToActions || []).map(x => x.asset) },
    };
  });
}

async function videoAssets(videoId) {
  const rows = await ads.search(`SELECT asset.resource_name FROM asset
    WHERE asset.type = 'YOUTUBE_VIDEO' AND asset.youtube_video_asset.youtube_video_id = '${videoId}'`);
  return rows.map(r => r.asset.resourceName).sort();
}

function readPlacements(account, plans, assets, corrections) {
  const placements = [];
  for (const r of account.rows.filter(r => r.adGroupAd.ad.name?.startsWith(namePrefix))) {
    const { ad, status, resourceName, policySummary } = r.adGroupAd;
    const plan = plans.find(p => p.name === ad.name && p.adGroupId === r.adGroup.id && p.campaign === r.campaign.id);
    assert(plan, `Unexpected RO-28 ad ${ad.id} in group ${r.adGroup.id}`);
    assert(!placements.some(x => x.key === plan.key), `Duplicate RO-28 placement for ${plan.key}`);
    assert.equal(status, 'ENABLED', `${plan.key} RO-28 status`);
    const [video] = ad.demandGenVideoResponsiveAd.videos;
    assert(ad.demandGenVideoResponsiveAd.videos.length === 1 && assets.includes(video.asset), `${plan.key} YouTube asset`);
    const inventory = video.adVideoAssetInfo?.adVideoAssetInventoryPreferences;
    assert(inventory?.inFeedPreference && !inventory.inStreamPreference && !inventory.shortsPreference, `${plan.key} in-feed inventory`);
    const sameCopy = Object.entries(COPY).every(([field, lines]) =>
      JSON.stringify((ad.demandGenVideoResponsiveAd[field] || []).map(x => x.text).sort()) === JSON.stringify([...lines].sort()));
    const sameUrl = ad.finalUrls?.length === 1 && ad.finalUrls[0] === DESTINATION;
    if (!sameCopy || !sameUrl) {
      assert(corrections && !PROTECTED.has(resourceName), `${plan.key} ad copy or final URL does not match`);
      const copy = Object.fromEntries(Object.entries(COPY).map(([field, lines]) => [field, lines.map(text => ({ text }))]));
      corrections.push({ adOperation: { update: {
        resourceName: ads.rn.ad(ad.id), demandGenVideoResponsiveAd: copy, finalUrls: [DESTINATION],
      }, updateMask: COPY_MASK } });
    }
    placements.push({ key: plan.key, campaign: plan.campaign, adGroupId: plan.adGroupId, adId: ad.id,
      resourceName, status, name: ad.name, finalUrls: ad.finalUrls, asset: video.asset, policySummary });
  }
  return placements.sort((a, b) => a.key.localeCompare(b.key));
}

function accountStatus(account) {
  const statuses = new Map(account.rows.map(r => [r.adGroupAd.resourceName, r.adGroupAd.status]));
  const tier2 = account.groups.find(r => r.adGroup.id === GROUPS.tier2).adGroup;
  return {
    enabled: [...statuses].filter(([, status]) => status === 'ENABLED').map(([id]) => id).sort(),
    protectedPaused: [...PROTECTED].filter(id => statuses.get(id) === 'PAUSED').length,
    protectedChanged: [...PROTECTED].filter(id => statuses.get(id) !== 'PAUSED').sort(),
    tier2: { targetCpaMicros: tier2.targetCpaMicros, cpcBidMicros: tier2.cpcBidMicros },
  };
}

// Railway can still be deploying when the early Short goes live. Restore the
// requested pause for fresh ads created by the normal worker in these groups.
// Dan's original list and ads outside the worker's naming pattern are excluded.
function pauseNewWorkerAds(account, plans) {
  return account.rows.flatMap(r => {
    const { status, resourceName, ad } = r.adGroupAd;
    if (status !== 'ENABLED' || PROTECTED.has(resourceName) || ad.name?.startsWith(namePrefix)) return [];
    const plan = plans.find(p => p.adGroupId === r.adGroup.id && p.campaign === r.campaign.id);
    const match = /^AT · .+ · yt:[\w-]{11} · ([\w-]+) · (\d{4}-\d{2}-\d{2})$/.exec(ad.name || '');
    if (!match || plan?.key !== match[1] || match[2] < firstReleaseDay) return [];
    return [{ adGroupAdOperation: { update: { resourceName, status: 'PAUSED' }, updateMask: 'status' } }];
  });
}

async function run(videoId, dryRun, journal) {
  assert(/^[\w-]{11}$/.test(videoId) && videoId !== 'eLV6EluvyD0', 'Invalid replacement YouTube ID');
  const lint = lintSet(COPY);
  assert(lint.ok, JSON.stringify(lint.failures));
  assert(!Object.values(COPY).flat().some(line => /\b(?:needles?|vials?|syringes?|pharmac\w*|pens?)\b/i.test(line)));
  assert.equal(PROTECTED.size, 45);
  const [account, assets] = await Promise.all([readAccount(), videoAssets(videoId)]);
  const plans = targetPlan(account, videoId);
  const before = accountStatus(account);
  // If an older worker reaches the same public upload first, finish its exact
  // placements in place so a deploy overlap cannot create a second set.
  const corrections = [];
  const existing = readPlacements(account, plans, assets, dryRun ? null : corrections);
  if (dryRun) assert.equal(existing.length, 0, 'Dry-run must exercise all seven creates');
  const issued = !dryRun && fs.existsSync(journal) ? JSON.parse(fs.readFileSync(journal, 'utf8')) : null;
  if (issued) {
    assert.equal(issued.videoId, videoId, 'YouTube ID changed after submission');
    const missingReadback = issued.ads.filter(name => !existing.some(x => x.resourceName === name));
    assert.equal(missingReadback.length, 0, `Awaiting readback of submitted ads: ${missingReadback.join(', ')}`);
  }
  const missing = plans.filter(p => !existing.some(x => x.key === p.key));
  const videoAsset = assets[0] || ads.rn.temp('assets', 1);
  const ops = [];
  if (missing.length && !assets.length) {
    ops.push({ assetOperation: { create: { resourceName: videoAsset, name: `yt ${videoId}`,
      youtubeVideoAsset: { youtubeVideoId: videoId } } } });
  }
  const firstAdOp = ops.length;
  for (const plan of missing) {
    ops.push(createOp({ ...plan, cid: ads.CID, set: COPY, videoAsset, isShort: false }));
  }
  const pauses = dryRun ? [] : pauseNewWorkerAds(account, plans);
  ops.push(...corrections, ...pauses);
  const meta = { note: `RO-28 Got Abs paid engagement: ${videoId}`, reason: 'ro28-release' };
  let mutation = null;
  if (ops.length) {
    await ads.mutate(ops, { ...meta, dryRun: true });
    if (!dryRun) {
      mutation = (await ads.mutate(ops, { ...meta, tries: 0 })).results;
      const newAds = mutation.slice(firstAdOp, firstAdOp + missing.length);
      fs.writeFileSync(journal + '.tmp', JSON.stringify({ videoId, ads: [...(issued?.ads || []), ...newAds] }) + '\n');
      fs.renameSync(journal + '.tmp', journal);
    }
  }
  const [fresh, freshAssets] = await Promise.all([readAccount(), videoAssets(videoId)]);
  const after = accountStatus(fresh);
  const placements = readPlacements(fresh, plans, freshAssets);
  if (dryRun) {
    assert.deepEqual(after, before, 'Live Google Ads status changed during dry-run');
    assert.deepEqual(freshAssets, assets, 'Dry-run video assets changed');
    assert.equal(placements.length, 0);
  }
  return {
    checkedAt: new Date().toISOString(), account: ads.CID, videoId, dryRun, validatedOps: ops.length,
    newAsset: !assets.length && missing.length > 0, placements, before, after, mutation,
    pausedNewWorkerAds: pauses.map(op => op.adGroupAdOperation.update.resourceName),
    plan: plans.map(({ key, campaign, adGroupId, domain, templateAdId, name, template }) =>
      ({ key, campaign, adGroupId, domain, templateAdId, name, finalUrls: template.finalUrls })),
    verified: placements.length === plans.length && after.protectedPaused === PROTECTED.size &&
      after.tier2.targetCpaMicros === '50000' && after.tier2.cpcBidMicros === '50000' &&
      JSON.stringify(after.enabled) === JSON.stringify(placements.map(x => x.resourceName).sort()),
  };
}

if (require.main === module) {
  const [mode, videoId, journal] = process.argv.slice(2);
  (async () => {
    assert(['--dry-run', '--apply'].includes(mode), 'Specify --dry-run or --apply');
    if (mode === '--apply') assert(journal, 'Supply the release job submission journal path');
    console.log(JSON.stringify(await run(videoId, mode === '--dry-run', journal)));
  })().catch(error => {
    console.error(error.message);
    process.exitCode = 1;
  }).finally(() => ads.close());
}
