#!/usr/bin/env node
/**
 * Build the Demand Gen TRIAL campaign: six ads to the /start sales page, optimized for Trial Signup only.
 * Spec: Handoffs/handoff-20261001-vsl-trial-campaign-six-ads.md (Dan, 2026-10-01).
 *
 *   node scripts/ads/api/dgen-trial-campaign.js            # plan + Google dry run
 *   node scripts/ads/api/dgen-trial-campaign.js --apply    # build PAUSED, set the goal, read back
 *
 * Every ad is cloned from its live, already approved twin in campaign 24243839443 (same video asset, headlines,
 * descriptions, logo, call to action and Audience), so nothing new is written and no copy is re-linted here.
 * Idempotent by name: an existing campaign, ad group or ad is reused, never duplicated. To add a new format of an
 * ad later, add its YouTube id to ADS once its twin exists in the old campaign, or use /ad-setup.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { rn, dg, GEO, LANG, CID } = ads;

const NAME = '[DAN] [DGEN] [TRIAL] VSL page | 6 ads | MU 25-54 | US+CA';
const BUDGET = 50, TARGET_CPA = 40, FREQ_CAP = 4;
const URL = 'https://absbyai.com/start';
const WANTED_GOAL = { category: 'SIGNUP', origin: 'WEBSITE' };   // Trial Signup 7704441545 is the only SIGNUP action
const SOURCE_CAMPAIGN = 24243839443;

// label = ad group name; source = that ad's /start ad group in the old campaign.
const ADS = [
  { key: 'ad13', label: 'Ad 13 The Cost Of Getting Abs', source: '197465035822', videos: ['-SuKGXGcbIg'] },
  { key: 'ra01', label: 'RA-01 AI Got Me Abs', source: '195593120770', videos: ['OUw788sF1KY', 'rfCsWNxuNV0'] },
  { key: 'ad10', label: 'Ad 10 Busy Dad Fitness', source: '206979993984', videos: ['Sg3vcEY2P_8', '4nDWFmdjzQQ', 'CR4WAVmSuXY'] },
  { key: 'ad4', label: 'Ad 4 Stop Wasting Money On Supplements', source: '202812319169', videos: ['R08TPEtkjuQ'] },
  { key: 'ad3', label: 'Ad 3 Stop Paying Human Trainers', source: '199782847163', videos: ['86jbUhqBTUQ', 'xlC-tigurnA', '-wTErCSi640', 'DXRkrfvcJEM'] },
  { key: 'ad6', label: "Ad 6 You're Not Too Old", source: '199737961146', videos: ['Je2yvk00SHE'] },
];

const q = (s) => s.replace(/'/g, "\\'");

async function main() {
  const apply = process.argv.includes('--apply');
  const noCap = process.argv.includes('--no-frequency-cap');

  const srcIds = ADS.map(a => a.source).join(',');
  const srcAds = await ads.search(`SELECT ad_group.id, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.id, ad_group_ad.ad.name,
      ad_group_ad.ad.final_urls, ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
      ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
      ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
      ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions
      FROM ad_group_ad WHERE campaign.id = ${SOURCE_CAMPAIGN} AND ad_group.id IN (${srcIds}) AND ad_group_ad.status != 'REMOVED'`);
  const srcAud = await ads.search(`SELECT ad_group.id, ad_group_criterion.audience.audience FROM ad_group_criterion
      WHERE ad_group.id IN (${srcIds}) AND ad_group_criterion.type = 'AUDIENCE' AND ad_group_criterion.status != 'REMOVED'`);
  const audBy = Object.fromEntries(srcAud.map(r => [r.adGroup.id, r.adGroupCriterion.audience.audience]));
  const assets = await ads.search(`SELECT asset.resource_name, asset.youtube_video_asset.youtube_video_id FROM asset WHERE asset.type = 'YOUTUBE_VIDEO'`);
  const ytOf = Object.fromEntries(assets.map(r => [r.asset.resourceName, r.asset.youtubeVideoAsset.youtubeVideoId]));

  const existing = await ads.search(`SELECT campaign.id, campaign.status FROM campaign WHERE campaign.name = '${q(NAME)}' AND campaign.status != 'REMOVED'`);
  let campaignId = existing.length ? existing[0].campaign.id : null;
  const groupByName = {}; const adNames = new Set();
  if (campaignId) {
    (await ads.search(`SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.id = ${campaignId} AND ad_group.status != 'REMOVED'`)).forEach(r => { groupByName[r.adGroup.name] = r.adGroup.id; });
    (await ads.search(`SELECT ad_group_ad.ad.name FROM ad_group_ad WHERE campaign.id = ${campaignId} AND ad_group_ad.status != 'REMOVED'`)).forEach(r => adNames.add(r.adGroupAd.ad.name));
  }

  let n = 0; const tmp = (kind) => rn.temp(kind, ++n);
  const ops = []; const plan = [];
  let camp;
  if (campaignId) { camp = rn.campaign(campaignId); plan.push(`reuse campaign ${campaignId}`); }
  else {
    const budget = tmp('campaignBudgets'); camp = tmp('campaigns');
    ops.push({ campaignBudgetOperation: { create: { resourceName: budget, name: NAME, amountMicros: String(BUDGET * 1e6), deliveryMethod: 'STANDARD', explicitlyShared: false } } });
    const create = { resourceName: camp, name: NAME, status: 'PAUSED', advertisingChannelType: 'DEMAND_GEN', campaignBudget: budget,
      ...dg.targetCpa(TARGET_CPA),
      geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE', negativeGeoTargetType: 'PRESENCE' },
      containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING' };
    if (!noCap) create.frequencyCaps = [{ key: { level: 'CAMPAIGN', eventType: 'IMPRESSION', timeUnit: 'DAY', timeLength: 1 }, cap: FREQ_CAP }];
    ops.push({ campaignOperation: { create } });
    plan.push(`create campaign "${NAME}" PAUSED, $${BUDGET}/day, target CPA $${TARGET_CPA}${noCap ? '' : `, cap ${FREQ_CAP} impressions per user per day`}`);
  }

  for (const a of ADS) {
    let group = groupByName[a.label] ? rn.adGroup(groupByName[a.label]) : null;
    if (group) plan.push(`reuse ad group ${groupByName[a.label]} "${a.label}"`);
    else {
      if (!audBy[a.source]) throw new Error(`${a.label}: source ad group ${a.source} has no Audience`);
      group = tmp('adGroups');
      ops.push({ adGroupOperation: { create: { resourceName: group, name: a.label, status: 'ENABLED', campaign: camp,
        optimizedTargetingEnabled: false, targetCpaMicros: String(TARGET_CPA * 1e6) } } });
      for (const g of [GEO.US, GEO.CA]) ops.push({ adGroupCriterionOperation: { create: { adGroup: group, location: { geoTargetConstant: rn.geo(g) } } } });
      ops.push({ adGroupCriterionOperation: { create: { adGroup: group, language: { languageConstant: rn.language(LANG.EN) } } } });
      ops.push({ adGroupCriterionOperation: { create: { adGroup: group, audience: { audience: audBy[a.source] } } } });
      plan.push(`create ad group "${a.label}" ($${TARGET_CPA} target CPA, US+CA, English, audience ${audBy[a.source].split('/').pop()})`);
    }
    for (const yt of a.videos) {
      const twins = srcAds.filter(r => r.adGroup.id === a.source && (r.adGroupAd.ad.demandGenVideoResponsiveAd.videos || []).some(v => ytOf[v.asset] === yt));
      const twin = twins.find(r => r.adGroupAd.status === 'ENABLED') || twins[0];
      if (!twin) throw new Error(`${a.label}: no live ad carries video ${yt} in source ad group ${a.source}`);
      const src = twin.adGroupAd.ad; const d = src.demandGenVideoResponsiveAd;
      const version = src.name.split(' | ')[1];
      const utm = (/utm_content=([^&]+)/.exec(src.finalUrls[0]) || [])[1].replace(/-start$/, '');
      const adName = `${a.label} | ${version} | vsl`;
      if (adNames.has(adName)) { plan.push(`skip ad "${adName}" (exists)`); continue; }
      const finalUrl = `${URL}?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-${a.key}&utm_content=${utm}-vsl`;
      const texts = (arr) => (arr || []).map(x => ({ text: x.text }));
      ops.push({ adGroupAdOperation: { create: { adGroup: group, status: 'ENABLED', ad: { name: adName, finalUrls: [finalUrl],
        demandGenVideoResponsiveAd: {
          videos: d.videos.filter(v => ytOf[v.asset] === yt).map(v => ({ asset: v.asset })),
          headlines: texts(d.headlines), longHeadlines: texts(d.longHeadlines), descriptions: texts(d.descriptions),
          logoImages: (d.logoImages || []).map(x => ({ asset: x.asset })),
          businessName: { text: d.businessName.text },
          callToActions: (d.callToActions || []).map(x => ({ asset: x.asset })),
        } } } } });
      plan.push(`create ad "${adName}" (${yt}, twin ${src.id} ${twin.adGroupAd.policySummary.approvalStatus}) → ${finalUrl}`);
    }
  }

  console.log('PLAN\n  ' + plan.join('\n  '));
  const note = 'dgen-trial-campaign: six ads to /start, Trial Signup only';
  if (ops.length) {
    await ads.mutate(ops, { dryRun: true, note });
    console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
    if (!apply) { console.log('pass --apply to build'); await ads.close(); return; }
    const res = await ads.mutate(ops, { note });
    console.log(`APPLIED ${res.results.length} operations`);
    if (!campaignId) campaignId = (await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(NAME)}' AND campaign.status != 'REMOVED'`))[0].campaign.id;
  } else if (!apply) { console.log('\nnothing to create'); await ads.close(); return; }

  // Campaign-specific goal: Trial Signup (SIGNUP / WEBSITE) only. The account default goals are untouched.
  const goals = (await ads.search(`SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = ${campaignId}`)).map(r => r.campaignConversionGoal);
  const isWanted = (g) => g.category === WANTED_GOAL.category && g.origin === WANTED_GOAL.origin;
  if (!goals.some(isWanted)) throw new Error('the campaign has no SIGNUP / WEBSITE goal row');
  const unwanted = goals.filter(g => !isWanted(g) && g.biddable);
  if (unwanted.length || !goals.find(isWanted).biddable)
    await ads.mutate(dg.conversionGoals(campaignId, [WANTED_GOAL], unwanted), { note: note + ' | goals' });

  const back = {
    campaign: await ads.search(`SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, campaign.frequency_caps, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id = ${campaignId}`),
    goals: await ads.search(`SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = ${campaignId}`),
    goalLevel: await ads.search(`SELECT conversion_goal_campaign_config.goal_config_level FROM conversion_goal_campaign_config WHERE campaign.id = ${campaignId}`),
    ads: await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = ${campaignId} AND ad_group_ad.status != 'REMOVED'`),
    criteria: await ads.search(`SELECT ad_group.name, ad_group_criterion.type, ad_group_criterion.audience.audience, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = ${campaignId} AND ad_group_criterion.type IN ('AUDIENCE','LOCATION','LANGUAGE') AND ad_group_criterion.status != 'REMOVED'`),
  };
  const c = back.campaign[0];
  console.log(`\nREAD BACK campaign ${c.campaign.id} ${c.campaign.status} ${c.campaign.biddingStrategyType} $${c.campaign.targetCpa.targetCpaMicros / 1e6} | budget $${c.campaignBudget.amountMicros / 1e6}/day | geo ${c.campaign.geoTargetTypeSetting.positiveGeoTargetType} | caps ${JSON.stringify(c.campaign.frequencyCaps || [])}`);
  console.log('goal level ' + back.goalLevel.map(r => r.conversionGoalCampaignConfig.goalConfigLevel).join() + ' | biddable: ' + back.goals.filter(r => r.campaignConversionGoal.biddable).map(r => `${r.campaignConversionGoal.category}/${r.campaignConversionGoal.origin}`).join(', '));
  for (const r of back.ads)
    console.log(`  ${r.adGroup.id} ${r.adGroup.name} ($${Number(r.adGroup.targetCpaMicros || 0) / 1e6}) | ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary.reviewStatus}/${r.adGroupAd.policySummary.approvalStatus} | ${r.adGroupAd.ad.name} | ${r.adGroupAd.ad.finalUrls[0]}`);
  const out = path.join(__dirname, 'dgen-ads', 'trial-campaign.result.json');
  fs.writeFileSync(out, JSON.stringify({ at: new Date().toISOString(), campaignId, ...back }, null, 1));
  console.log(`\nresult saved: ${path.relative(process.cwd(), out)}`);
  await ads.close();
}

main().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
