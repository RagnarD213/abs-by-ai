#!/usr/bin/env node
/**
 * Build the Performance Max TRIAL campaign that spends the $450 Performance Max credit: one campaign, one asset
 * group, /start only, Trial Signup as the only goal. Spec: Handoffs/handoff-20261001-pmax-campaign-build.md (Dan).
 *
 *   node scripts/ads/api/pmax-trial-campaign.js images            # upload the 20 finalized images (AI label set)
 *   node scripts/ads/api/pmax-trial-campaign.js                   # plan + Google dry run
 *   node scripts/ads/api/pmax-trial-campaign.js --apply           # build PAUSED, set the goal, read back
 *   node scripts/ads/api/pmax-trial-campaign.js --skip gender,members   # leave out a control Google refuses
 *
 * Text is Dan's own, taken verbatim from the live cold trial campaign 24316364155; the script refuses a line that
 * is not live there unless it is listed in NEW_LINES. Idempotent by campaign name. Enabling is a separate call.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { rn, dg, GEO, LANG, CID } = ads;

const NAME = '[DAN] [PMAX] [TRIAL] VSL page | 6 ads | US+CA | site visitors 30 day';
const GROUP = 'VSL page | 6 ads | 20 images';
const BUDGET = 15;
const END = '2026-11-01 23:59:59';          // 30 days after the 2026-10-02 start; the credit expires 2026-11-30
const URL = 'https://absbyai.com/start?utm_source=google&utm_medium=pmax&utm_campaign=pmax-trial';
const WANTED_GOAL = { category: 'SIGNUP', origin: 'WEBSITE' };   // Trial Signup 7704441545
const SOURCE_CAMPAIGN = 24316364155;
const NEGATIVES_FROM = 24148587722;         // Non-Brand Search
const VISITORS_30 = '9453529251';           // website | visited absbyai.com | 30 day (membership 30, read 2026-10-02)
const MEMBERS = ['9480144404', '9441311426', '9469016618'];
const LOGO = '400941168572';
const IMAGE_DIR = path.join(__dirname, '..', '..', '..', 'output', 'campaign-images-20261001', 'Finalized Images');
const IMAGE_IDS = path.join(__dirname, 'dgen-ads', 'pmax-images.result.json');
const RESULT = path.join(__dirname, 'dgen-ads', 'pmax-campaign.result.json');

// Five videos (the Performance Max limit): five of the six ads, all three shapes. RA-01 is left out (lowest
// click-through of the six in 24316364155 on 2026-10-02).
const VIDEOS = [
  ['423865478571', 'Ad 13 16:9'], ['419938098517', 'Ad 4 16:9'], ['421668364056', 'Ad 6 16:9'],
  ['424707539263', 'Ad 10 9:16'], ['422079967995', 'Ad 3 1:1'],
];
const HEADLINES = [
  'How I Got Abs At 40', 'How AI Got Me Abs', 'Fire Your Personal Trainer', 'Human Trainers Hate Him',
  'Trainers Hate This AI App', 'How Busy Dads Get Abs', 'How 40+ Dads Can Get Abs', 'How Men 40+ Lose Belly Fat',
  'How To Get Abs After 40', 'Supplement Corps Hate Him', 'How AI Fixed My Supplements', 'How I Lost Belly Fat With AI',
  'A Personalized AI Fitness Plan', 'How AI Got Me Abs At 40', "A Busy Dad's Fitness System",
];
const LONG_HEADLINES = [
  'Daniel Rose shows how he used AI to turn a goal image into a workout and nutrition plan.',
  "Here's why I stopped paying a personal trainer and use an AI trainer instead.",
  'A busy dad explains the workout, meal and adjustment plan he uses with AI.',
  'Daniel Rose explains how he rebuilt his fitness at 40 with a plan he could follow.',
  'Daniel Rose explains why he stopped taking supplement advice from influencers.',
];
const DESCRIPTIONS = [
  'Daniel Rose shows how AI turned his goal image into a personalized fitness plan.',
  'Daniel Rose shows how an AI trainer builds his plan and adjusts it at every workout.',
  'AI plans workouts and meals around your schedule, equipment and starting point.',
  'Daniel Rose shows the workout and nutrition system he follows as a 40-year-old dad.',
  'Daniel Rose shows how AI reads the label on every supplement in his stack.',
];
const NEW_LINES = [];   // lines not in the trial campaign (written with /ad-copy); listed in the report
const EXTRA_NEGATIVES = [['free', 'BROAD'], ['generator', 'BROAD'], ['abs editor', 'PHRASE'], ['abs creator', 'PHRASE'],
  ['six pack ai', 'PHRASE'], ['ai six pack', 'PHRASE'], ['give me abs ai', 'PHRASE']];
const AUTOMATION_OFF = ['TEXT_ASSET_AUTOMATION', 'FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION', 'GENERATE_ENHANCED_YOUTUBE_VIDEOS',
  'GENERATE_IMAGE_ENHANCEMENT', 'GENERATE_IMAGE_EXTRACTION'];

const q = (s) => s.replace(/'/g, "\\'");
const arg = (f) => { const i = process.argv.indexOf(f); return i >= 0 ? process.argv[i + 1] : null; };
const skip = new Set((arg('--skip') || '').split(',').filter(Boolean));
const redact = (ops) => ops.map(o => (o.assetOperation && o.assetOperation.create && o.assetOperation.create.imageAsset)
  ? { assetOperation: { create: { ...o.assetOperation.create, imageAsset: { data: '<omitted>' } } } } : o);

function fieldOf(w, h) {
  const r = w / h;
  if (Math.abs(r - 1.91) < 0.02) return 'MARKETING_IMAGE';
  if (Math.abs(r - 1) < 0.01) return 'SQUARE_MARKETING_IMAGE';
  if (Math.abs(r - 0.8) < 0.01) return 'PORTRAIT_MARKETING_IMAGE';
  throw new Error(`unsupported image shape ${w}x${h}`);
}

// Upload the finalized images as assets, each marked as made with AI. Assets are inert until linked.
async function uploadImages() {
  const files = [];
  for (const dir of fs.readdirSync(IMAGE_DIR)) {
    const d = path.join(IMAGE_DIR, dir);
    if (!fs.statSync(d).isDirectory()) continue;
    for (const f of fs.readdirSync(d).filter(x => /\.jpe?g$/i.test(x)).sort()) files.push(path.join(d, f));
  }
  const have = fs.existsSync(IMAGE_IDS) ? JSON.parse(fs.readFileSync(IMAGE_IDS, 'utf8')).images : [];
  const todo = files.filter(f => !have.some(h => h.file === path.basename(f)));
  const ops = todo.map(f => ({ assetOperation: { create: { name: `pmax-20261002 ${path.basename(f, '.jpg')}`, type: 'IMAGE',
    imageAsset: { data: fs.readFileSync(f).toString('base64') },
    syntheticContentInfo: { advertiserAttestation: { status: 'IS_SYNTHETIC', source: 'ADVERTISER_ATTESTED' } } } } }));
  if (ops.length) {
    const dry = process.argv.includes('--dry-run');
    const res = await ads.mutate(ops, { dryRun: dry, log: false });
    await ads.ledger(dry ? 'api:validate' : 'api:mutate', { reason: 'pmax-trial-campaign', note: 'upload finalized campaign images with the AI label', cid: CID, ops: redact(ops), response: res.response });
    if (dry) { console.log(`dry run OK: ${ops.length} image(s)`); return; }
    todo.forEach((f, i) => have.push({ file: path.basename(f), asset: res.results[i] }));
  }
  const ids = have.map(h => h.asset.split('/').pop()).join(',');
  const back = await ads.search(`SELECT asset.id, asset.name, asset.image_asset.full_size.width_pixels, asset.image_asset.full_size.height_pixels,
    asset.synthetic_content_info.advertiser_attestation.status, asset.synthetic_content_info.advertiser_attestation.source FROM asset WHERE asset.id IN (${ids})`);
  const images = have.map(h => {
    const a = back.find(r => r.asset.resourceName === h.asset).asset;
    const w = Number(a.imageAsset.fullSize.widthPixels), ht = Number(a.imageAsset.fullSize.heightPixels);
    return { file: h.file, asset: h.asset, name: a.name, width: w, height: ht, field: fieldOf(w, ht),
      aiLabel: (a.syntheticContentInfo && a.syntheticContentInfo.advertiserAttestation) || null };
  });
  fs.writeFileSync(IMAGE_IDS, JSON.stringify({ at: new Date().toISOString(), images }, null, 1));
  for (const i of images) console.log(`${i.asset.split('/').pop()} ${i.field.padEnd(24)} ${i.width}x${i.height} AI label ${i.aiLabel ? i.aiLabel.status : 'NOT SET'} | ${i.file}`);
}

async function readBack(campaignId) {
  const s = (g) => ads.search(g).catch(e => [{ error: e.message }]);
  return {
    campaign: await s(`SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros,
      campaign.start_date_time, campaign.end_date_time, campaign.asset_automation_settings, campaign.brand_guidelines_enabled, campaign.geo_target_type_setting.positive_geo_target_type,
      campaign.geo_target_type_setting.negative_geo_target_type, campaign.primary_status, campaign.primary_status_reasons, campaign_budget.amount_micros, campaign_budget.explicitly_shared FROM campaign WHERE campaign.id = ${campaignId}`),
    goals: await s(`SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = ${campaignId}`),
    goalLevel: await s(`SELECT conversion_goal_campaign_config.goal_config_level FROM conversion_goal_campaign_config WHERE campaign.id = ${campaignId}`),
    criteria: await s(`SELECT campaign_criterion.criterion_id, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.language.language_constant,
      campaign_criterion.age_range.type, campaign_criterion.gender.type, campaign_criterion.user_list.user_list, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type,
      campaign_criterion.brand_list.shared_set FROM campaign_criterion WHERE campaign.id = ${campaignId}`),
    assetGroup: await s(`SELECT asset_group.id, asset_group.name, asset_group.status, asset_group.final_urls, asset_group.ad_strength, asset_group.primary_status, asset_group.primary_status_reasons FROM asset_group WHERE campaign.id = ${campaignId}`),
    assets: await s(`SELECT asset_group_asset.field_type, asset_group_asset.status, asset_group_asset.policy_summary.approval_status, asset_group_asset.policy_summary.review_status, asset.id, asset.name, asset.type,
      asset.text_asset.text, asset.youtube_video_asset.youtube_video_id, asset.call_to_action_asset.call_to_action, asset.image_asset.full_size.width_pixels, asset.image_asset.full_size.height_pixels,
      asset.synthetic_content_info.advertiser_attestation.status FROM asset_group_asset WHERE campaign.id = ${campaignId} AND asset_group_asset.status != 'REMOVED'`),
    signals: await s(`SELECT asset_group_signal.resource_name, asset_group_signal.audience.audience, asset_group_signal.search_theme.text FROM asset_group_signal WHERE campaign.id = ${campaignId}`),
    audiences: await s(`SELECT audience.id, audience.name, audience.dimensions, audience.exclusion_dimension FROM audience WHERE audience.name = '${q(NAME)}'`),
    campaignAssets: await s(`SELECT campaign.id, campaign_asset.field_type, campaign_asset.status, asset.id, asset.name FROM campaign_asset WHERE campaign.id = ${campaignId}`),
  };
}

async function main() {
  if (process.argv[2] === 'images') { await uploadImages(); await ads.close(); return; }
  const apply = process.argv.includes('--apply');
  const images = JSON.parse(fs.readFileSync(IMAGE_IDS, 'utf8')).images;

  // Dan's lines must be live in the cold trial campaign, word for word.
  const src = await ads.search(`SELECT ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines,
    ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions, ad_group_ad.ad.demand_gen_video_responsive_ad.videos FROM ad_group_ad WHERE campaign.id = ${SOURCE_CAMPAIGN} AND ad_group_ad.status = 'ENABLED'`);
  const live = { h: new Set(), l: new Set(), d: new Set(), v: new Set() };
  for (const r of src) { const d = r.adGroupAd.ad.demandGenVideoResponsiveAd;
    d.headlines.forEach(x => live.h.add(x.text)); d.longHeadlines.forEach(x => live.l.add(x.text)); d.descriptions.forEach(x => live.d.add(x.text)); d.videos.forEach(x => live.v.add(x.asset.split('/').pop())); }
  const check = (list, set, max, what) => list.forEach(t => {
    if (t.length > max) throw new Error(`${what} over ${max} characters: ${t}`);
    if (!set.has(t) && !NEW_LINES.includes(t)) throw new Error(`${what} is not live in ${SOURCE_CAMPAIGN}: ${t}`); });
  check(HEADLINES, live.h, 30, 'headline'); check(LONG_HEADLINES, live.l, 90, 'long headline'); check(DESCRIPTIONS, live.d, 90, 'description');
  VIDEOS.forEach(([id, label]) => { if (!live.v.has(id)) throw new Error(`video ${label} (${id}) is not live in ${SOURCE_CAMPAIGN}`); });

  const negs = (await ads.search(`SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type FROM campaign_criterion
    WHERE campaign.id = ${NEGATIVES_FROM} AND campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'`)).map(r => [r.campaignCriterion.keyword.text, r.campaignCriterion.keyword.matchType]);
  for (const n of EXTRA_NEGATIVES) if (!negs.some(x => x[0] === n[0])) negs.push(n);
  const banned = negs.filter(([t]) => /abs by ai|dan rose/i.test(t));
  if (banned.length) throw new Error('brand term among the negatives: ' + banned.map(x => x[0]).join(', '));

  // Google counts headlines and descriptions toward the asset group's minimums only when the text assets already
  // exist, so they are made in their own request first (text assets are inert until linked, and Google dedupes them).
  const allText = [...HEADLINES, ...LONG_HEADLINES, ...DESCRIPTIONS, 'Abs by AI'];
  const made = await ads.mutate(allText.map(t => ({ assetOperation: { create: { textAsset: { text: t } } } })), { note: 'pmax-trial-campaign: text assets' });
  const textAsset = Object.fromEntries(allText.map((t, i) => [t, made.results[i]]));

  const existing = await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(NAME)}' AND campaign.status != 'REMOVED'`);
  let campaignId = existing.length ? existing[0].campaign.id : null;
  const note = 'pmax-trial-campaign: one asset group to /start, Trial Signup only';

  if (!campaignId) {
    let n = 0; const tmp = (kind) => rn.temp(kind, ++n);
    const ops = []; const plan = [];
    const budget = tmp('campaignBudgets'), camp = tmp('campaigns'), group = tmp('assetGroups'), aud = tmp('audiences');
    ops.push({ campaignBudgetOperation: { create: { resourceName: budget, name: NAME, amountMicros: String(BUDGET * 1e6), deliveryMethod: 'STANDARD', explicitlyShared: false } } });
    ops.push({ campaignOperation: { create: { resourceName: camp, name: NAME, status: 'PAUSED', advertisingChannelType: 'PERFORMANCE_MAX', campaignBudget: budget,
      maximizeConversions: {}, endDateTime: END, brandGuidelinesEnabled: false,
      geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE', negativeGeoTargetType: 'PRESENCE' },
      assetAutomationSettings: AUTOMATION_OFF.filter(t => !skip.has(t)).map(t => ({ assetAutomationType: t, assetAutomationStatus: 'OPTED_OUT' })),
      containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING' } } });
    plan.push(`campaign "${NAME}" PAUSED, $${BUDGET}/day, Maximize conversions (no target), ends ${END}, presence only, automation off: ${AUTOMATION_OFF.filter(t => !skip.has(t)).join(', ')}`);

    const crit = (c) => ops.push({ campaignCriterionOperation: { create: { campaign: camp, ...c } } });
    crit({ location: { geoTargetConstant: rn.geo(GEO.US) } }); crit({ location: { geoTargetConstant: rn.geo(GEO.CA) } });
    crit({ language: { languageConstant: rn.language(LANG.EN) } });
    if (!skip.has('age')) { crit({ negative: true, ageRange: { type: 'AGE_RANGE_18_24' } }); crit({ negative: true, ageRange: { type: 'AGE_RANGE_65_UP' } }); }
    if (!skip.has('gender')) crit({ negative: true, gender: { type: 'FEMALE' } });
    if (!skip.has('members')) MEMBERS.forEach(id => crit({ negative: true, userList: { userList: `customers/${CID}/userLists/${id}` } }));
    if (!skip.has('negatives')) negs.forEach(([text, matchType]) => crit({ negative: true, keyword: { text, matchType } }));
    plan.push(`US + Canada, English${skip.has('age') ? '' : ', exclude 18-24 and 65+'}${skip.has('gender') ? '' : ', exclude female'}${skip.has('members') ? '' : ', exclude 3 member lists'}, ${skip.has('negatives') ? 0 : negs.length} negative keywords`);

    ops.push({ assetGroupOperation: { create: { resourceName: group, name: GROUP, campaign: camp, status: 'ENABLED', finalUrls: [URL] } } });
    const link = (asset, fieldType) => ops.push({ assetGroupAssetOperation: { create: { assetGroup: group, asset, fieldType } } });
    const text = (t, fieldType) => link(textAsset[t], fieldType);
    HEADLINES.forEach(t => text(t, 'HEADLINE')); LONG_HEADLINES.forEach(t => text(t, 'LONG_HEADLINE')); DESCRIPTIONS.forEach(t => text(t, 'DESCRIPTION'));
    text('Abs by AI', 'BUSINESS_NAME');
    link(`customers/${CID}/assets/${LOGO}`, 'LOGO');
    // Performance Max refuses the trial campaign's "Start now" (UNSUPPORTED_CALL_TO_ACTION); "Sign up" is the nearest it offers.
    const cta = tmp('assets'); ops.push({ assetOperation: { create: { resourceName: cta, callToActionAsset: { callToAction: 'SIGN_UP' } } } });
    link(cta, 'CALL_TO_ACTION_SELECTION');
    VIDEOS.forEach(([id]) => link(`customers/${CID}/assets/${id}`, 'YOUTUBE_VIDEO'));
    images.forEach(i => link(i.asset, i.field));
    plan.push(`asset group "${GROUP}" → ${URL}: ${HEADLINES.length} headlines, ${LONG_HEADLINES.length} long headlines, ${DESCRIPTIONS.length} descriptions, ${VIDEOS.length} videos, ${images.length} images, logo, Sign up`);

    ops.push({ audienceOperation: { create: { resourceName: aud, name: NAME, description: 'Performance Max signal: website visitors, 30 day. Nothing else.',
      dimensions: [{ audienceSegments: { segments: [{ userList: { userList: `customers/${CID}/userLists/${VISITORS_30}` } }] } }] } } });
    ops.push({ assetGroupSignalOperation: { create: { assetGroup: group, audience: { audience: aud } } } });
    plan.push(`audience signal: user list ${VISITORS_30} only`);

    console.log('PLAN\n  ' + plan.join('\n  '));
    await ads.mutate(ops, { dryRun: true, note });
    console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
    if (!apply) { console.log('pass --apply to build'); await ads.close(); return; }
    const res = await ads.mutate(ops, { note });
    console.log(`APPLIED ${res.results.length} operations`);
    campaignId = (await ads.search(`SELECT campaign.id FROM campaign WHERE campaign.name = '${q(NAME)}' AND campaign.status != 'REMOVED'`))[0].campaign.id;
  } else console.log(`campaign ${campaignId} exists, nothing created`);

  // Campaign-specific goal: Trial Signup (SIGNUP / WEBSITE) only. The account default goals are untouched.
  const goals = (await ads.search(`SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = ${campaignId}`)).map(r => r.campaignConversionGoal);
  const isWanted = (g) => g.category === WANTED_GOAL.category && g.origin === WANTED_GOAL.origin;
  if (!goals.some(isWanted)) throw new Error('the campaign has no SIGNUP / WEBSITE goal row');
  const unwanted = goals.filter(g => !isWanted(g) && g.biddable);
  if (apply && (unwanted.length || !goals.find(isWanted).biddable))
    await ads.mutate(dg.conversionGoals(campaignId, [WANTED_GOAL], unwanted), { note: note + ' | goals' });

  const back = await readBack(campaignId);
  fs.writeFileSync(RESULT, JSON.stringify({ at: new Date().toISOString(), campaignId, skipped: [...skip], ...back }, null, 1));
  const c = back.campaign[0];
  console.log(`\nREAD BACK campaign ${c.campaign.id} ${c.campaign.status} ${c.campaign.advertisingChannelType} ${c.campaign.biddingStrategyType} | $${c.campaignBudget.amountMicros / 1e6}/day | ends ${c.campaign.endDateTime} | geo ${c.campaign.geoTargetTypeSetting.positiveGeoTargetType}`);
  console.log('automation: ' + (c.campaign.assetAutomationSettings || []).map(x => `${x.assetAutomationType}=${x.assetAutomationStatus}`).join(', '));
  console.log('goal level ' + back.goalLevel.map(r => r.conversionGoalCampaignConfig.goalConfigLevel).join() + ' | biddable: ' + back.goals.filter(r => r.campaignConversionGoal.biddable).map(r => `${r.campaignConversionGoal.category}/${r.campaignConversionGoal.origin}`).join(', '));
  const by = {}; back.criteria.forEach(r => { const k = (r.campaignCriterion.negative ? 'NEG ' : '') + r.campaignCriterion.type; by[k] = (by[k] || 0) + 1; });
  console.log('criteria: ' + JSON.stringify(by));
  const fa = {}; back.assets.forEach(r => { fa[r.assetGroupAsset.fieldType] = (fa[r.assetGroupAsset.fieldType] || 0) + 1; });
  console.log('assets: ' + JSON.stringify(fa));
  console.log('signals: ' + JSON.stringify(back.signals.map(r => r.assetGroupSignal)));
  console.log(`\nresult saved: ${path.relative(process.cwd(), RESULT)}`);
  await ads.close();
}

main().catch(async (e) => { console.error('FAILED:', e.message); if (process.env.ADS_DEBUG && e.body) console.error(JSON.stringify(e.body, null, 1).slice(0, 6000)); await ads.close(); process.exit(1); });
