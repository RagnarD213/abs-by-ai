#!/usr/bin/env node
/**
 * Split the engagement REMARKETING campaign by country (Dan, 2026-11-07), as was done for tier 1 on 2026-11-03.
 *
 *   node scripts/ads/api/dgen-us-rmktg.js                  # plan + Google dry run
 *   node scripts/ads/api/dgen-us-rmktg.js --apply          # build the US copy ENABLED, set the goal, read back
 *   node scripts/ads/api/dgen-us-rmktg.js --source [--apply]   # source: drop US, exclude US, budget $10
 *
 * A copy of remarketing campaign `24316408288` for the United States only, $5/day: same target CPA bidding,
 * goal (YouTube channel subscriptions only), both ad groups with their names, targets, channels, optimized
 * targeting, language, excluded countries and audiences (site visitors / YouTube viewers, members + purchasers +
 * subscribers excluded), and every ad with its status (ENABLED stays ENABLED, PAUSED stays PAUSED).
 * Location: United States only, PRESENCE, as the US engagement campaign `24422704023`.
 * Idempotent by name: an existing campaign, ad group or ad is reused, never duplicated.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { rn, dg } = ads;

const SOURCE = '24316408288';
const US = 2840;
const NAME = '[ENGAGEMENT] [DGEN] [RMKTG] US ONLY | ALL CONTENT | site visitors + youtube viewers';
const BUDGET = 5, SOURCE_BUDGET = 10;
const GOAL = { category: 'ENGAGEMENT', origin: 'YOUTUBE_HOSTED' };   // YouTube channel subscriptions
const q = (s) => s.replace(/'/g, "\\'");
const texts = (arr) => (arr || []).map(x => ({ text: x.text }));
const usName = (name, key) => /rmktg-(site|yt)/.test(name) ? name.replace(/rmktg-(site|yt)/, 'us-rmktg-$1')
  : /tier1/.test(name) ? name.replace('tier1', `us-rmktg-${key}`) : `${name} · us-rmktg-${key}`;

async function build(apply) {
  const [src] = await ads.search(`SELECT campaign.target_cpa.target_cpa_micros, campaign.bidding_strategy_type FROM campaign WHERE campaign.id = ${SOURCE}`);
  if (src.campaign.biddingStrategyType !== 'TARGET_CPA') throw new Error(`source bidding is ${src.campaign.biddingStrategyType}, expected TARGET_CPA`);
  const campaignCpa = Number(src.campaign.targetCpa.targetCpaMicros) / 1e6;
  const srcGroups = await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, ad_group.optimized_targeting_enabled, ad_group.demand_gen_ad_group_settings.channel_controls.channel_config, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_in_feed, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_in_stream, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_shorts, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.discover, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.gmail, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.display FROM ad_group WHERE campaign.id = ${SOURCE} AND ad_group.status != 'REMOVED' ORDER BY ad_group.id`);
  const srcCrit = await ads.search(`SELECT ad_group.id, ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant, ad_group_criterion.audience.audience FROM ad_group_criterion WHERE campaign.id = ${SOURCE} AND ad_group_criterion.type IN ('LOCATION','LANGUAGE','AUDIENCE') AND ad_group_criterion.status != 'REMOVED'`);
  const srcAds = await ads.search(`SELECT ad_group.id, ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls,
      ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
      ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
      ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
      ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions
      FROM ad_group_ad WHERE campaign.id = ${SOURCE} AND ad_group_ad.status IN ('ENABLED','PAUSED') ORDER BY ad_group_ad.ad.id`);

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
      ...dg.targetCpa(campaignCpa), geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE' },
      containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING' } } });
    plan.push(`create campaign ENABLED "${NAME}", $${BUDGET}/day, target CPA $${campaignCpa}, location PRESENCE`);
  }

  for (const r of srcGroups) {
    const g = r.adGroup;
    let group = groupByName[g.name] ? rn.adGroup(groupByName[g.name]) : null;
    if (group) plan.push(`reuse ad group ${groupByName[g.name]} "${g.name}"`);
    else {
      group = tmp('adGroups');
      const create = { resourceName: group, name: g.name, status: g.status, campaign: camp, optimizedTargetingEnabled: !!g.optimizedTargetingEnabled, targetCpaMicros: g.targetCpaMicros };
      if (g.demandGenAdGroupSettings) create.demandGenAdGroupSettings = g.demandGenAdGroupSettings;
      ops.push({ adGroupOperation: { create } });
      const crit = srcCrit.filter(x => x.adGroup.id === g.id).map(x => x.adGroupCriterion);
      ops.push({ adGroupCriterionOperation: { create: { adGroup: group, location: { geoTargetConstant: rn.geo(US) } } } });
      let excluded = 0;
      for (const c of crit) {
        if (c.type === 'LOCATION' && c.negative && !c.location.geoTargetConstant.endsWith(`/${US}`)) {
          ops.push({ adGroupCriterionOperation: { create: { adGroup: group, negative: true, location: { geoTargetConstant: c.location.geoTargetConstant } } } }); excluded++;
        } else if (c.type === 'LANGUAGE') ops.push({ adGroupCriterionOperation: { create: { adGroup: group, language: { languageConstant: c.language.languageConstant } } } });
        else if (c.type === 'AUDIENCE') ops.push({ adGroupCriterionOperation: { create: { adGroup: group, audience: { audience: c.audience.audience } } } });
      }
      const aud = crit.filter(c => c.type === 'AUDIENCE').map(c => c.audience.audience.split('/').pop()).join();
      plan.push(`create ad group "${g.name}" ${g.status} ($${g.targetCpaMicros / 1e6} target, US only, ${excluded} excluded countries, audience ${aud}, ${JSON.stringify(g.demandGenAdGroupSettings)})`);
    }
    for (const a of srcAds.filter(x => x.adGroup.id === g.id)) {
      const s = a.adGroupAd.ad; const d = s.demandGenVideoResponsiveAd;
      const adName = usName(s.name, /^Website/.test(g.name) ? 'site' : 'yt');
      if (adNames.has(adName)) { plan.push(`skip ad "${adName}" (exists)`); continue; }
      const ad = { videos: d.videos.map(v => v.adVideoAssetInfo ? { asset: v.asset, adVideoAssetInfo: v.adVideoAssetInfo } : { asset: v.asset }),
        headlines: texts(d.headlines), longHeadlines: texts(d.longHeadlines), descriptions: texts(d.descriptions),
        logoImages: (d.logoImages || []).map(x => ({ asset: x.asset })), businessName: { text: d.businessName.text } };
      if ((d.callToActions || []).length) ad.callToActions = d.callToActions.map(x => ({ asset: x.asset }));
      ops.push({ adGroupAdOperation: { create: { adGroup: group, status: a.adGroupAd.status, ad: { name: adName, finalUrls: s.finalUrls, demandGenVideoResponsiveAd: ad } } } });
      plan.push(`  ad ${a.adGroupAd.status} "${adName}" (twin ${s.id} ${a.adGroupAd.policySummary.approvalStatus})`);
    }
  }

  console.log('PLAN\n  ' + plan.join('\n  '));
  if (ops.length) {
    await ads.mutate(ops, { dryRun: true, note: 'dgen-us-rmktg' });
    console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
    if (!apply) return;
    const res = await ads.mutate(ops, { note: 'dgen-us-rmktg: US remarketing copy (Dan 2026-11-07)' });
    console.log(`APPLIED ${res.results.length} operations`);
    if (!campaignId) campaignId = (await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(NAME)}' AND campaign.status != 'REMOVED'`))[0].campaign.id;
  } else if (!apply) { console.log('\nnothing to create'); return; }

  const goalQ = `SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = ${campaignId}`;
  const goals = (await ads.search(goalQ)).map(r => r.campaignConversionGoal);
  const isWanted = (g) => g.category === GOAL.category && g.origin === GOAL.origin;
  if (!goals.some(isWanted)) throw new Error('the campaign has no ENGAGEMENT / YOUTUBE_HOSTED goal row');
  const unwanted = goals.filter(g => !isWanted(g) && g.biddable);
  if (unwanted.length || !goals.find(isWanted).biddable) await ads.mutate(dg.conversionGoals(campaignId, [GOAL], unwanted), { note: 'dgen-us-rmktg | goals' });

  const back = {
    campaign: await ads.search(`SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id = ${campaignId}`),
    goals: (await ads.search(goalQ)).filter(r => r.campaignConversionGoal.biddable),
    groups: await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, ad_group.optimized_targeting_enabled, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_in_feed, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_shorts FROM ad_group WHERE campaign.id = ${campaignId} AND ad_group.status != 'REMOVED'`),
    criteria: await ads.search(`SELECT ad_group.id, ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.audience.audience, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = ${campaignId} AND ad_group_criterion.type IN ('AUDIENCE','LOCATION','LANGUAGE') AND ad_group_criterion.status != 'REMOVED'`),
    ads: await ads.search(`SELECT ad_group.id, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = ${campaignId} AND ad_group_ad.status != 'REMOVED'`),
  };
  const c = back.campaign[0];
  console.log(`\nREAD BACK campaign ${c.campaign.id} ${c.campaign.status} ${c.campaign.biddingStrategyType} $${c.campaign.targetCpa.targetCpaMicros / 1e6} | $${c.campaignBudget.amountMicros / 1e6}/day | geo ${c.campaign.geoTargetTypeSetting.positiveGeoTargetType}`);
  console.log('biddable goals: ' + back.goals.map(r => `${r.campaignConversionGoal.category}/${r.campaignConversionGoal.origin}`).join(', '));
  for (const r of back.groups) {
    const cr = back.criteria.filter(x => x.adGroup.id === r.adGroup.id).map(x => x.adGroupCriterion);
    const pos = cr.filter(x => x.type === 'LOCATION' && !x.negative).map(x => x.location.geoTargetConstant.split('/').pop());
    console.log(`  group ${r.adGroup.id} ${r.adGroup.status} "${r.adGroup.name}" $${r.adGroup.targetCpaMicros / 1e6} | optimized ${!!r.adGroup.optimizedTargetingEnabled} | ${JSON.stringify(r.adGroup.demandGenAdGroupSettings)} | targeted ${pos.join()} | excluded ${cr.filter(x => x.type === 'LOCATION' && x.negative).length} | languages ${cr.filter(x => x.type === 'LANGUAGE').length} | audience ${cr.filter(x => x.type === 'AUDIENCE').map(x => x.audience.audience.split('/').pop()).join()} | ads ${back.ads.filter(x => x.adGroup.id === r.adGroup.id).length}`);
  }
  for (const r of back.ads) console.log(`  ${r.adGroup.id} | ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary.reviewStatus}/${r.adGroupAd.policySummary.approvalStatus} | ${r.adGroupAd.ad.name}`);
  const out = path.join(__dirname, 'dgen-ads', 'us-rmktg-campaign.result.json');
  fs.writeFileSync(out, JSON.stringify({ at: new Date().toISOString(), campaignId, ...back }, null, 1));
  console.log(`result saved: ${path.relative(process.cwd(), out)}`);
}

// Source remarketing campaign: remove the US target from each ad group, add the US as an excluded location (the
// campaign uses presence-or-interest, so a US resident "interested in" Canada could otherwise still see it), $10/day.
async function source(apply) {
  const rows = await ads.search(`SELECT ad_group.id, ad_group_criterion.resource_name, ad_group_criterion.negative FROM ad_group_criterion WHERE campaign.id = ${SOURCE} AND ad_group.status != 'REMOVED' AND ad_group_criterion.status != 'REMOVED' AND ad_group_criterion.location.geo_target_constant = 'geoTargetConstants/${US}'`);
  const groups = (await ads.search(`SELECT ad_group.id FROM ad_group WHERE campaign.id = ${SOURCE} AND ad_group.status != 'REMOVED'`)).map(r => r.adGroup.id);
  const [b] = await ads.search(`SELECT campaign_budget.resource_name, campaign_budget.amount_micros FROM campaign WHERE campaign.id = ${SOURCE}`);
  const ops = [];
  for (const r of rows) if (!r.adGroupCriterion.negative) ops.push({ adGroupCriterionOperation: { remove: r.adGroupCriterion.resourceName } });
  for (const g of groups) if (!rows.some(r => r.adGroup.id === g && r.adGroupCriterion.negative))
    ops.push({ adGroupCriterionOperation: { create: { adGroup: rn.adGroup(g), negative: true, location: { geoTargetConstant: rn.geo(US) } } } });
  if (Number(b.campaignBudget.amountMicros) !== SOURCE_BUDGET * 1e6)
    ops.push({ campaignBudgetOperation: { update: { resourceName: b.campaignBudget.resourceName, amountMicros: String(SOURCE_BUDGET * 1e6) }, updateMask: 'amount_micros' } });
  console.log(`source: US rows ${JSON.stringify(rows.map(r => `${r.adGroup.id}:${r.adGroupCriterion.negative ? 'excluded' : 'targeted'}`))}, budget $${b.campaignBudget.amountMicros / 1e6}/day → ${ops.length} operations`);
  if (!ops.length) return;
  await ads.mutate(ops, { dryRun: true, note: 'rmktg drop US' });
  console.log('Google dry run OK');
  if (!apply) return;
  await ads.mutate(ops, { note: 'rmktg tier 1: US moved to its own remarketing campaign (Dan 2026-11-07)' });
  const [b2] = await ads.search(`SELECT campaign_budget.amount_micros FROM campaign WHERE campaign.id = ${SOURCE}`);
  console.log(`READ BACK source budget $${b2.campaignBudget.amountMicros / 1e6}/day`);
  for (const g of groups) {
    const loc = (await ads.search(`SELECT ad_group_criterion.negative, ad_group_criterion.location.geo_target_constant FROM ad_group_criterion WHERE ad_group.id = ${g} AND ad_group_criterion.type = 'LOCATION' AND ad_group_criterion.status != 'REMOVED'`)).map(r => r.adGroupCriterion);
    const us = loc.filter(x => x.location.geoTargetConstant.endsWith(`/${US}`)).map(x => x.negative ? 'EXCLUDED' : 'TARGETED');
    console.log(`  group ${g}: targeted ${loc.filter(x => !x.negative).map(x => x.location.geoTargetConstant.split('/').pop()).join(', ')} | excluded ${loc.filter(x => x.negative).length} | US ${us.join()}`);
  }
}

async function main() {
  const argv = process.argv.slice(2);
  const apply = argv.includes('--apply');
  if (argv.includes('--source')) await source(apply); else await build(apply);
  if (!apply) console.log('\npass --apply to make the change');
  await ads.close();
}

main().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
