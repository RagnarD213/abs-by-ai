#!/usr/bin/env node
/**
 * Build the two Demand Gen REMARKETING campaigns (Dan, 2026-10-01).
 * Spec: Handoffs/handoff-20261001-remarketing-campaigns-conversion-and-subscriber.md
 *
 *   node scripts/ads/api/dgen-rmktg-campaigns.js [a|b]            # plan + Google dry run
 *   node scripts/ads/api/dgen-rmktg-campaigns.js [a|b] --apply    # build PAUSED, set the goal, read back
 *
 * A = conversion remarketing: the cold trial campaign's ads to /start, Trial Signup only, $40 target.
 * B = subscriber remarketing: tier 1's enabled ads, YouTube channel subscriptions only, $3 target.
 * Each has two ad groups: Website visitors (7 + 30 + 365 day lists) and YouTube viewers (7 + 30 day lists).
 * Every ad is cloned from its live twin in the source campaign, so no copy is written here.
 * Idempotent by name: an existing audience, campaign, ad group or ad is reused, never duplicated. Re-run with
 * --apply after a new format is added to the source campaign and it is copied into both groups.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { rn, dg, CID } = ads;

const UL = (id) => `customers/${CID}/userLists/${id}`;
const LISTS = {
  site: ['9452848282', '9453529251', '9452257061'],   // website visitors 7 / 30 / 365 day
  yt: ['9453532227', '9452269226'],                   // watched any video 7 / 30 day
};
const MEMBERS = ['9480144404', '9441311426', '9469016618'];   // member hub 540 day, All Converters, Purchasers
const SUBSCRIBERS = '9452604668';                            // youtube | subscribed to channel | 540 day
const GROUPS = [
  { key: 'site', name: 'Website visitors | 7 + 30 + 365 day' },
  { key: 'yt', name: 'YouTube viewers | watched any video 7 + 30 day' },
];
const MALE_UNKNOWN = { gender: { genders: ['MALE'], includeUndetermined: true } };

const CAMPAIGNS = {
  a: {
    name: '[DAN] [DGEN] [TRIAL] [RMKTG] VSL page | 6 ads | US+CA | site visitors + youtube viewers',
    source: 24316364155, budget: 10, targetCpa: 40, freqCap: 4,
    geoType: { positiveGeoTargetType: 'PRESENCE', negativeGeoTargetType: 'PRESENCE' },
    goal: { category: 'SIGNUP', origin: 'WEBSITE' },            // Trial Signup 7704441545 is the only SIGNUP action
    audName: (g) => `RMKTG trial | MU 25-54 | ${g.key === 'site' ? 'site visitors 7+30+365 day' : 'youtube viewers 7+30 day'} | excl members`,
    demo: [{ age: { ageRanges: [{ minAge: 25, maxAge: 54 }], includeUndetermined: true } }, MALE_UNKNOWN],
    exclude: MEMBERS,
    adName: (src, g) => `${src.name} | rmktg-${g.key}`,
    finalUrl: (src, g) => {
      const u = src.finalUrls[0];
      const ad = /utm_campaign=dgen-trial-([^&]+)/.exec(u)[1], video = /utm_content=([^&]+)/.exec(u)[1];
      return `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-rmktg-${g.key}&utm_content=${ad}-${video}`;
    },
  },
  b: {
    name: '[DAN] [DGEN] [ENGAGEMENT] [RMKTG] geo tier 1 | ALL CONTENT | site visitors + youtube viewers',
    source: 24163535721, budget: 10, targetCpa: 3,
    geoType: { positiveGeoTargetType: 'PRESENCE_OR_INTEREST' },   // as tier 1
    goal: { category: 'ENGAGEMENT', origin: 'YOUTUBE_HOSTED' }, // YouTube channel subscriptions 7717762965
    channels: { channelConfig: 'SELECTED_CHANNELS', selectedChannels: { youtubeInFeed: true, youtubeShorts: true } },
    audName: (g) => `RMKTG subs | MU 18-65+ | ${g.key === 'site' ? 'site visitors 7+30+365 day' : 'youtube viewers 7+30 day'} | excl members + subscribers`,
    demo: [MALE_UNKNOWN],
    exclude: [...MEMBERS, SUBSCRIBERS],
    adName: (src, g) => /tier1/.test(src.name) ? src.name.replace('tier1', `rmktg-${g.key}`) : `${src.name} · rmktg-${g.key}`,
    finalUrl: (src) => src.finalUrls[0],
  },
};

const q = (s) => s.replace(/'/g, "\\'");
const texts = (arr) => (arr || []).map(x => ({ text: x.text }));

async function build(which, apply, flags) {
  const C = CAMPAIGNS[which];
  console.log(`\n================ CAMPAIGN ${which.toUpperCase()}: ${C.name}`);

  const srcAds = await ads.search(`SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls,
      ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
      ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
      ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name,
      ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions
      FROM ad_group_ad WHERE campaign.id = ${C.source} AND ad_group_ad.status = 'ENABLED' AND ad_group.status = 'ENABLED' ORDER BY ad_group_ad.ad.id`);
  // Geo and language: copied from wherever the source keeps them (campaign level for UI-built, ad group for API-built).
  const campGeo = await ads.search(`SELECT campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.language.language_constant FROM campaign_criterion WHERE campaign.id = ${C.source} AND campaign_criterion.type IN ('LOCATION','LANGUAGE')`);
  const groupGeo = await ads.search(`SELECT ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = ${C.source} AND ad_group_criterion.type IN ('LOCATION','LANGUAGE') AND ad_group_criterion.status != 'REMOVED' AND ad_group.status = 'ENABLED'`);
  const geo = new Map();
  for (const c of [...campGeo.map(r => r.campaignCriterion), ...groupGeo.map(r => r.adGroupCriterion)]) {
    const v = c.location ? { location: { geoTargetConstant: c.location.geoTargetConstant } } : { language: { languageConstant: c.language.languageConstant } };
    if (c.negative) { if (flags.noNegativeGeo) continue; v.negative = true; }
    geo.set(JSON.stringify(v), v);
  }
  const geoCriteria = [...geo.values()];
  const count = (f) => geoCriteria.filter(f).length;
  const geoNote = `${count(v => v.location && !v.negative)} countries targeted, ${count(v => v.location && v.negative)} excluded, ${count(v => v.language)} language`;

  // Audiences first (their own step: an Audience cannot be created and attached in the same atomic batch).
  const audId = {};
  for (const g of GROUPS) {
    const name = C.audName(g);
    const found = await ads.search(`SELECT audience.id FROM audience WHERE audience.name = '${q(name)}' AND audience.status = 'ENABLED'`);
    if (found.length) { audId[g.key] = found[0].audience.id; console.log(`reuse audience ${audId[g.key]} "${name}"`); continue; }
    const op = { audienceOperation: { create: { name, description: 'Remarketing handoff 2026-10-01',
      dimensions: [...C.demo, { audienceSegments: { segments: LISTS[g.key].map(id => ({ userList: { userList: UL(id) } })) } }],
      exclusionDimension: { exclusions: C.exclude.map(id => ({ userList: { userList: UL(id) } })) } } } };
    await ads.mutate([op], { dryRun: true, note: `rmktg ${which}: audience ${g.key}` });
    if (!apply) { console.log(`audience "${name}" VALID (dry run)`); audId[g.key] = null; continue; }
    const r = await ads.mutate([op], { note: `rmktg ${which}: audience ${g.key}` });
    audId[g.key] = r.results[0].split('/').pop();
    console.log(`created audience ${audId[g.key]} "${name}"`);
  }

  const existing = await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(C.name)}' AND campaign.status != 'REMOVED'`);
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
    ops.push({ campaignBudgetOperation: { create: { resourceName: budget, name: C.name, amountMicros: String(C.budget * 1e6), deliveryMethod: 'STANDARD', explicitlyShared: false } } });
    const create = { resourceName: camp, name: C.name, status: 'PAUSED', advertisingChannelType: 'DEMAND_GEN', campaignBudget: budget,
      ...dg.targetCpa(C.targetCpa), geoTargetTypeSetting: C.geoType,
      containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING' };
    if (C.freqCap && !flags.noCap) create.frequencyCaps = [{ key: { level: 'CAMPAIGN', eventType: 'IMPRESSION', timeUnit: 'DAY', timeLength: 1 }, cap: C.freqCap }];
    ops.push({ campaignOperation: { create } });
    plan.push(`create campaign PAUSED, $${C.budget}/day, target CPA $${C.targetCpa}${create.frequencyCaps ? `, cap ${C.freqCap} impressions per user per day` : ''}`);
  }

  for (const g of GROUPS) {
    let group = groupByName[g.name] ? rn.adGroup(groupByName[g.name]) : null;
    if (group) plan.push(`reuse ad group ${groupByName[g.name]} "${g.name}"`);
    else {
      group = tmp('adGroups');
      const create = { resourceName: group, name: g.name, status: 'ENABLED', campaign: camp, optimizedTargetingEnabled: false, targetCpaMicros: String(C.targetCpa * 1e6) };
      if (C.channels) create.demandGenAdGroupSettings = { channelControls: C.channels };
      ops.push({ adGroupOperation: { create } });
      for (const v of geoCriteria) ops.push({ adGroupCriterionOperation: { create: { adGroup: group, ...v } } });
      // Dry run before the audience exists: validate against a live audience of the same shape.
      ops.push({ adGroupCriterionOperation: { create: { adGroup: group, audience: { audience: rn.audience(audId[g.key] || '357211400') } } } });
      plan.push(`create ad group "${g.name}" ($${C.targetCpa} target, ${geoNote}, audience ${audId[g.key] || '(new)'}${C.channels ? ', in-feed + Shorts only' : ''})`);
    }
    for (const r of srcAds) {
      const src = r.adGroupAd.ad; const d = src.demandGenVideoResponsiveAd;
      const adName = C.adName(src, g);
      if (adNames.has(adName)) { plan.push(`skip ad "${adName}" (exists)`); continue; }
      const finalUrl = C.finalUrl(src, g);
      const ad = { videos: d.videos.map(v => ({ asset: v.asset })), headlines: texts(d.headlines), longHeadlines: texts(d.longHeadlines),
        descriptions: texts(d.descriptions), logoImages: (d.logoImages || []).map(x => ({ asset: x.asset })), businessName: { text: d.businessName.text } };
      if ((d.callToActions || []).length) ad.callToActions = d.callToActions.map(x => ({ asset: x.asset }));
      ops.push({ adGroupAdOperation: { create: { adGroup: group, status: 'ENABLED', ad: { name: adName, finalUrls: [finalUrl], demandGenVideoResponsiveAd: ad } } } });
      plan.push(`create ad "${adName}" (twin ${src.id} ${r.adGroupAd.policySummary.approvalStatus}) → ${finalUrl}`);
    }
  }

  console.log('PLAN\n  ' + plan.join('\n  '));
  const note = `dgen-rmktg-campaigns ${which}`;
  if (ops.length) {
    await ads.mutate(ops, { dryRun: true, note });
    console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
    if (!apply) return;
    const res = await ads.mutate(ops, { note });
    console.log(`APPLIED ${res.results.length} operations`);
    if (!campaignId) campaignId = (await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(C.name)}' AND campaign.status != 'REMOVED'`))[0].campaign.id;
  } else if (!apply) { console.log('\nnothing to create'); return; }

  // Campaign-specific goal: the one wanted goal only. The account default goals are untouched.
  const goalQ = `SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = ${campaignId}`;
  const goals = (await ads.search(goalQ)).map(r => r.campaignConversionGoal);
  const isWanted = (g) => g.category === C.goal.category && g.origin === C.goal.origin;
  if (!goals.some(isWanted)) throw new Error(`the campaign has no ${C.goal.category} / ${C.goal.origin} goal row`);
  const unwanted = goals.filter(g => !isWanted(g) && g.biddable);
  if (unwanted.length || !goals.find(isWanted).biddable)
    await ads.mutate(dg.conversionGoals(campaignId, [C.goal], unwanted), { note: note + ' | goals' });

  const back = {
    campaign: await ads.search(`SELECT campaign.id, campaign.name, campaign.status, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, campaign.frequency_caps, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type FROM campaign WHERE campaign.id = ${campaignId}`),
    goals: await ads.search(goalQ),
    goalLevel: await ads.search(`SELECT conversion_goal_campaign_config.goal_config_level FROM conversion_goal_campaign_config WHERE campaign.id = ${campaignId}`),
    groups: await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, ad_group.optimized_targeting_enabled, ad_group.demand_gen_ad_group_settings.channel_controls.channel_config, ad_group.demand_gen_ad_group_settings.channel_controls.channel_strategy, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_in_feed, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_shorts, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.youtube_in_stream, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.discover, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.gmail, ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels.display FROM ad_group WHERE campaign.id = ${campaignId} AND ad_group.status != 'REMOVED'`),
    ads: await ads.search(`SELECT ad_group.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status FROM ad_group_ad WHERE campaign.id = ${campaignId} AND ad_group_ad.status != 'REMOVED'`),
    criteria: await ads.search(`SELECT ad_group.id, ad_group.name, ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.audience.audience, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = ${campaignId} AND ad_group_criterion.type IN ('AUDIENCE','LOCATION','LANGUAGE') AND ad_group_criterion.status != 'REMOVED'`),
    audiences: await ads.search(`SELECT audience.id, audience.name, audience.dimensions, audience.exclusion_dimension FROM audience WHERE audience.id IN (${Object.values(audId).join(',')})`),
  };
  const c = back.campaign[0];
  console.log(`\nREAD BACK campaign ${c.campaign.id} ${c.campaign.status} ${c.campaign.biddingStrategyType} $${c.campaign.targetCpa.targetCpaMicros / 1e6} | budget $${c.campaignBudget.amountMicros / 1e6}/day | geo ${c.campaign.geoTargetTypeSetting.positiveGeoTargetType} | caps ${JSON.stringify(c.campaign.frequencyCaps || [])}`);
  console.log('goal level ' + back.goalLevel.map(r => r.conversionGoalCampaignConfig.goalConfigLevel).join() + ' | biddable: ' + back.goals.filter(r => r.campaignConversionGoal.biddable).map(r => `${r.campaignConversionGoal.category}/${r.campaignConversionGoal.origin}`).join(', '));
  for (const r of back.groups) {
    const cr = back.criteria.filter(x => x.adGroup.id === r.adGroup.id).map(x => x.adGroupCriterion);
    console.log(`  group ${r.adGroup.id} ${r.adGroup.status} "${r.adGroup.name}" $${Number(r.adGroup.targetCpaMicros || 0) / 1e6} | optimized targeting ${!!r.adGroup.optimizedTargetingEnabled} | channels ${JSON.stringify(r.adGroup.demandGenAdGroupSettings || {})} | countries +${cr.filter(x => x.type === 'LOCATION' && !x.negative).length} -${cr.filter(x => x.type === 'LOCATION' && x.negative).length} | languages ${cr.filter(x => x.type === 'LANGUAGE').length} | audience ${cr.filter(x => x.type === 'AUDIENCE').map(x => x.audience.audience.split('/').pop()).join()} | ads ${back.ads.filter(x => x.adGroup.id === r.adGroup.id).length}`);
  }
  for (const r of back.audiences) {
    const seg = (r.audience.dimensions.find(d => d.audienceSegments) || { audienceSegments: { segments: [] } }).audienceSegments.segments.map(s => s.userList.userList.split('/').pop());
    const ex = ((r.audience.exclusionDimension || {}).exclusions || []).map(s => s.userList.userList.split('/').pop());
    console.log(`  audience ${r.audience.id} "${r.audience.name}" | lists ${seg.join(', ')} | excludes ${ex.join(', ')}`);
  }
  for (const r of back.ads)
    console.log(`  ${r.adGroup.id} | ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary.reviewStatus}/${r.adGroupAd.policySummary.approvalStatus} | ${r.adGroupAd.ad.name} | ${r.adGroupAd.ad.finalUrls[0]}`);
  const out = path.join(__dirname, 'dgen-ads', `rmktg-campaign-${which}.result.json`);
  fs.writeFileSync(out, JSON.stringify({ at: new Date().toISOString(), campaignId, audiences: audId, ...back }, null, 1));
  console.log(`result saved: ${path.relative(process.cwd(), out)}`);
}

async function main() {
  const argv = process.argv.slice(2);
  const apply = argv.includes('--apply');
  const flags = { noCap: argv.includes('--no-frequency-cap'), noNegativeGeo: argv.includes('--no-negative-geo') };
  const which = argv.filter(a => a === 'a' || a === 'b');
  for (const w of which.length ? which : ['a', 'b']) await build(w, apply, flags);
  if (!apply) console.log('\npass --apply to build');
  await ads.close();
}

main().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
