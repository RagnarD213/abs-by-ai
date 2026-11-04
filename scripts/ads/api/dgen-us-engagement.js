#!/usr/bin/env node
/**
 * Build the US-only YouTube engagement (subscriber) campaign (Dan, 2026-11-03).
 * Why: supplements can only be sold in the US, so US subscribers now matter most. Inside tier 1
 * Google spent 60-70% on Ireland and under 4% on the US, so the US gets its own campaign and
 * budget, and the US comes out of tier 1 (`--tier1` step below).
 *
 *   node scripts/ads/api/dgen-us-engagement.js            # plan + Google dry run
 *   node scripts/ads/api/dgen-us-engagement.js --apply    # build ENABLED, set the goal, read back
 *   node scripts/ads/api/dgen-us-engagement.js --tier1 [--apply]   # tier 1: drop US, exclude US, budget $20
 *
 * A copy of tier 1 `24163535721`: same audience (men + unknown, all ages), English, in-feed + Shorts only,
 * optimized targeting off, Maximize Conversions with the ad group's $7 target, goal YouTube channel
 * subscriptions only, and a clone of every live tier 1 ad (name `tier1` → `us`, video inventory
 * preferences kept). Location: United States only, PRESENCE (people physically in the US).
 * Idempotent by name: an existing campaign, ad group or ad is reused, never duplicated.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { rn, dg, CID } = ads;

const SOURCE = '24163535721';
const US = 2840;
const NAME = '[DAN] [DGEN] [ENGAGEMENT] MU 18-65+ | in-feed & shorts | US ONLY | ALL CONTENT';
const GROUP = '[DAN] [DGEN] [ENGAGEMENT] MU 18-65+, UA | US ONLY | ALL CONTENT';
const BUDGET = 10, TIER1_BUDGET = 20;
const GOAL = { category: 'ENGAGEMENT', origin: 'YOUTUBE_HOSTED' };   // YouTube channel subscriptions
const q = (s) => s.replace(/'/g, "\\'");
const texts = (arr) => (arr || []).map(x => ({ text: x.text }));

async function build(apply) {
  const [srcGroup] = await ads.search(`SELECT ad_group.id, ad_group.target_cpa_micros FROM ad_group WHERE campaign.id = ${SOURCE} AND ad_group.status = 'ENABLED'`);
  const targetCpaMicros = srcGroup.adGroup.targetCpaMicros;
  const [aud] = await ads.search(`SELECT ad_group_criterion.audience.audience FROM ad_group_criterion WHERE ad_group.id = ${srcGroup.adGroup.id} AND ad_group_criterion.type = 'AUDIENCE' AND ad_group_criterion.status = 'ENABLED'`);
  const audience = aud.adGroupCriterion.audience.audience;
  const langs = (await ads.search(`SELECT campaign_criterion.language.language_constant FROM campaign_criterion WHERE campaign.id = ${SOURCE} AND campaign_criterion.type = 'LANGUAGE'`)).map(r => r.campaignCriterion.language.languageConstant);
  const srcAds = await ads.search(`SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls,
      ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
      ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
      ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
      ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions
      FROM ad_group_ad WHERE campaign.id = ${SOURCE} AND ad_group_ad.status = 'ENABLED' AND ad_group.status = 'ENABLED' ORDER BY ad_group_ad.ad.id`);

  const existing = await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(NAME)}' AND campaign.status != 'REMOVED'`);
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
    ops.push({ campaignOperation: { create: { resourceName: camp, name: NAME, status: 'ENABLED', advertisingChannelType: 'DEMAND_GEN', campaignBudget: budget,
      maximizeConversions: {}, geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE' },
      containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING' } } });
    plan.push(`create campaign ENABLED, $${BUDGET}/day, Maximize Conversions, location PRESENCE`);
  }
  let group = groupByName[GROUP] ? rn.adGroup(groupByName[GROUP]) : null;
  if (group) plan.push(`reuse ad group ${groupByName[GROUP]}`);
  else {
    group = tmp('adGroups');
    ops.push({ adGroupOperation: { create: { resourceName: group, name: GROUP, status: 'ENABLED', campaign: camp, optimizedTargetingEnabled: false, targetCpaMicros,
      demandGenAdGroupSettings: { channelControls: { channelConfig: 'SELECTED_CHANNELS', selectedChannels: { youtubeInFeed: true, youtubeShorts: true } } } } } });
    ops.push({ adGroupCriterionOperation: { create: { adGroup: group, location: { geoTargetConstant: rn.geo(US) } } } });
    for (const l of langs) ops.push({ adGroupCriterionOperation: { create: { adGroup: group, language: { languageConstant: l } } } });
    ops.push({ adGroupCriterionOperation: { create: { adGroup: group, audience: { audience } } } });
    plan.push(`create ad group "${GROUP}" ($${targetCpaMicros / 1e6} target, US only, ${langs.length} language, audience ${audience.split('/').pop()}, in-feed + Shorts)`);
  }
  for (const r of srcAds) {
    const src = r.adGroupAd.ad; const d = src.demandGenVideoResponsiveAd;
    const adName = /tier1/.test(src.name) ? src.name.replace('tier1', 'us') : `${src.name} · us`;
    if (adNames.has(adName)) { plan.push(`skip "${adName}" (exists)`); continue; }
    const ad = { videos: d.videos.map(v => v.adVideoAssetInfo ? { asset: v.asset, adVideoAssetInfo: v.adVideoAssetInfo } : { asset: v.asset }),
      headlines: texts(d.headlines), longHeadlines: texts(d.longHeadlines), descriptions: texts(d.descriptions),
      logoImages: (d.logoImages || []).map(x => ({ asset: x.asset })), businessName: { text: d.businessName.text } };
    if ((d.callToActions || []).length) ad.callToActions = d.callToActions.map(x => ({ asset: x.asset }));
    ops.push({ adGroupAdOperation: { create: { adGroup: group, status: 'ENABLED', ad: { name: adName, finalUrls: src.finalUrls, demandGenVideoResponsiveAd: ad } } } });
    plan.push(`create ad "${adName}" (twin ${src.id} ${r.adGroupAd.policySummary.approvalStatus})`);
  }

  console.log('PLAN\n  ' + plan.join('\n  '));
  if (ops.length) {
    await ads.mutate(ops, { dryRun: true, note: 'dgen-us-engagement' });
    console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
    if (!apply) return;
    const res = await ads.mutate(ops, { note: 'dgen-us-engagement (Dan 2026-11-03)' });
    console.log(`APPLIED ${res.results.length} operations`);
    if (!campaignId) campaignId = (await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(NAME)}' AND campaign.status != 'REMOVED'`))[0].campaign.id;
  } else if (!apply) { console.log('\nnothing to create'); return; }

  const goalQ = `SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = ${campaignId}`;
  const goals = (await ads.search(goalQ)).map(r => r.campaignConversionGoal);
  const isWanted = (g) => g.category === GOAL.category && g.origin === GOAL.origin;
  if (!goals.some(isWanted)) throw new Error('the campaign has no ENGAGEMENT / YOUTUBE_HOSTED goal row');
  const unwanted = goals.filter(g => !isWanted(g) && g.biddable);
  if (unwanted.length || !goals.find(isWanted).biddable) await ads.mutate(dg.conversionGoals(campaignId, [GOAL], unwanted), { note: 'dgen-us-engagement | goals' });

  const back = {
    campaign: await ads.search(`SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id = ${campaignId}`),
    goals: (await ads.search(goalQ)).filter(r => r.campaignConversionGoal.biddable),
    groups: await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, ad_group.optimized_targeting_enabled, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_in_feed, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_shorts FROM ad_group WHERE campaign.id = ${campaignId} AND ad_group.status != 'REMOVED'`),
    criteria: await ads.search(`SELECT ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.audience.audience, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = ${campaignId} AND ad_group_criterion.type IN ('AUDIENCE','LOCATION','LANGUAGE') AND ad_group_criterion.status != 'REMOVED'`),
    ads: await ads.search(`SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = ${campaignId} AND ad_group_ad.status != 'REMOVED'`),
  };
  const c = back.campaign[0];
  console.log(`\nREAD BACK campaign ${c.campaign.id} ${c.campaign.status} ${c.campaign.biddingStrategyType} | $${c.campaignBudget.amountMicros / 1e6}/day | geo ${c.campaign.geoTargetTypeSetting.positiveGeoTargetType}`);
  console.log('biddable goals: ' + back.goals.map(r => `${r.campaignConversionGoal.category}/${r.campaignConversionGoal.origin}`).join(', '));
  for (const r of back.groups) console.log(`  group ${r.adGroup.id} ${r.adGroup.status} "${r.adGroup.name}" $${r.adGroup.targetCpaMicros / 1e6} | optimized ${!!r.adGroup.optimizedTargetingEnabled} | ${JSON.stringify(r.adGroup.demandGenAdGroupSettings)}`);
  for (const r of back.criteria) { const x = r.adGroupCriterion; console.log(`  criterion ${x.type}${x.negative ? ' (excluded)' : ''} ${(x.location && x.location.geoTargetConstant) || (x.language && x.language.languageConstant) || (x.audience && x.audience.audience)}`); }
  for (const r of back.ads) console.log(`  ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary.reviewStatus}/${r.adGroupAd.policySummary.approvalStatus} | ${r.adGroupAd.ad.name}`);
  const out = path.join(__dirname, 'dgen-ads', 'us-engagement-campaign.result.json');
  fs.writeFileSync(out, JSON.stringify({ at: new Date().toISOString(), campaignId, ...back }, null, 1));
  console.log(`result saved: ${path.relative(process.cwd(), out)}`);
}

// Tier 1: remove the US as a target, add it as an exclusion (tier 1 uses presence-or-interest, so a
// US resident "interested in" the UK could otherwise still be shown tier 1 ads), budget $20/day.
async function tier1(apply) {
  const rows = await ads.search(`SELECT campaign_criterion.resource_name, campaign_criterion.negative FROM campaign_criterion WHERE campaign.id = ${SOURCE} AND campaign_criterion.location.geo_target_constant = 'geoTargetConstants/${US}'`);
  const [b] = await ads.search(`SELECT campaign_budget.resource_name, campaign_budget.amount_micros FROM campaign WHERE campaign.id = ${SOURCE}`);
  const ops = [];
  for (const r of rows) if (!r.campaignCriterion.negative) ops.push({ campaignCriterionOperation: { remove: r.campaignCriterion.resourceName } });
  if (!rows.some(r => r.campaignCriterion.negative))
    ops.push({ campaignCriterionOperation: { create: { campaign: rn.campaign(SOURCE), negative: true, location: { geoTargetConstant: rn.geo(US) } } } });
  if (Number(b.campaignBudget.amountMicros) !== TIER1_BUDGET * 1e6)
    ops.push({ campaignBudgetOperation: { update: { resourceName: b.campaignBudget.resourceName, amountMicros: String(TIER1_BUDGET * 1e6) }, updateMask: 'amount_micros' } });
  console.log(`tier 1: US rows ${JSON.stringify(rows.map(r => r.campaignCriterion.negative))}, budget $${b.campaignBudget.amountMicros / 1e6}/day → ${ops.length} operations`);
  if (!ops.length) return;
  await ads.mutate(ops, { dryRun: true, note: 'tier1 drop US' });
  console.log('Google dry run OK');
  if (!apply) return;
  await ads.mutate(ops, { note: 'tier1: US moved to its own campaign (Dan 2026-11-03)' });
  const after = await ads.search(`SELECT campaign_criterion.negative FROM campaign_criterion WHERE campaign.id = ${SOURCE} AND campaign_criterion.location.geo_target_constant = 'geoTargetConstants/${US}'`);
  const [b2] = await ads.search(`SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = ${SOURCE}`);
  const pos = (await ads.search(`SELECT campaign_criterion.location.geo_target_constant FROM campaign_criterion WHERE campaign.id = ${SOURCE} AND campaign_criterion.type = 'LOCATION' AND campaign_criterion.negative = FALSE`)).map(r => r.campaignCriterion.location.geoTargetConstant.split('/').pop());
  console.log(`READ BACK tier 1: US ${after.map(r => r.campaignCriterion.negative ? 'EXCLUDED' : 'TARGETED').join()} | targeted ${pos.join(', ')} | budget $${b2.campaignBudget.amountMicros / 1e6}/day`);
}

async function main() {
  const argv = process.argv.slice(2);
  const apply = argv.includes('--apply');
  if (argv.includes('--tier1')) await tier1(apply); else await build(apply);
  if (!apply) console.log('\npass --apply to make the change');
  await ads.close();
}

main().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
