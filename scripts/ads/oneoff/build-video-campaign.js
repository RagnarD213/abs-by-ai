// ======================================================================
// ONE-OFF Google Ads Script — build the Ad 1 + Ad 2 Demand Gen video
// campaign (2026-09-10). Install as a SECOND script (Tools -> Scripts),
// Preview / run it, then DELETE it. Never schedule it.
//
// MODE:
//   'REPORT' — reads only (custom segments, conversion actions, video
//              assets, a reference Demand Gen ad/ad group/campaign) and
//              dumps the exact operations it WOULD send. Zero writes.
//   'APPLY'  — sends the operations. Run in PREVIEW first: Google
//              validates every operation without saving anything.
// Both modes POST their findings to absbyai.com/api/ytads/dump (the
// editor's log panel is not a reliable read channel).
//
// Dan's spec (chat, 2026-09-10): one campaign, $20/day, target CPA $30 on
// Free Generation Started, built PAUSED for his review. Four ad groups =
// two ads x two landing pages (/start, homepage); every version of an ad
// sits in its ad group as its own ad. US + Canada, male + unknown gender,
// 25-54, custom segments per ad, optimized targeting OFF, no lookalikes.
// The canonical copy is scripts/ads/oneoff/build-video-campaign.js; the
// pasted copy differs only in the KEY line.
// ======================================================================

var SERVER = 'https://absbyai.com';
var KEY = 'PASTE_YTADS_KEY_HERE';   // = YTADS_KEY on Railway. Never commit a real key.
var MODE = 'REPORT';                // 'REPORT' or 'APPLY'

var CAMPAIGN_NAME = '[DAN] [DGEN] [CONVERSION] MU 25-54 | US+CA | ad 1 + ad 2 | start vs home';
var BUDGET_USD = 20;
var TARGET_CPA_USD = 30;
var CONVERSION_ACTION = 'Free Generation Started';
var BUSINESS_NAME_FALLBACK = 'Abs by AI';
var GEO = { 'United States': 'geoTargetConstants/2840', 'Canada': 'geoTargetConstants/2124' };
var LANGUAGE = 'languageConstants/1000'; // English
// Demographics (male + unknown, 25-54, unknown age included) live in the Audience built in step 2.

var LANDINGS = [
  { key: 'start', label: '/start', url: 'https://absbyai.com/start' },
  { key: 'home',  label: 'home',   url: 'https://absbyai.com/' },
];

var ADS = [
  { key: 'ad1', title: 'Ad 1 This Picture Got Me Abs',
    segments: ['custom | search | AI abs preview tool', 'custom | search | what would I look like', 'custom | search | competitor apps'],
    videos: [
      { id: 'lf46ytHacss', label: 'Muhammad 16:9', slug: 'muhammad-16x9' },
      { id: '1oEcwdp21Fg', label: 'Zeeshan 16:9',  slug: 'zeeshan-16x9' },
      { id: 'Iz0u8KHRbyE', label: 'Muhammad vertical', slug: 'muhammad-9x16' },
    ],
    headlines: ['This Picture Got Me Abs', 'AI Made A Picture Of Me With Abs', 'Upload A Photo, See Yourself With Abs', "Abs By AI - Here's How It Works", 'Abs At 40 - The Photo That Did It'],
    longHeadlines: ["Here's the AI picture of myself with abs that got me to change how I eat and train.", 'Upload one photo and AI shows you with abs. This video shows you how I used mine.', 'Daniel Rose explains how one AI photo of himself with abs changed his training at 40.'],
    descriptions: ['Daniel Rose shows the AI picture that got him started, and what he did next.', "Upload a photo and AI makes a picture of you with abs. Here's how it works.", 'This video shows how the Abs By AI picture works and what I did after seeing mine.'],
    // Dan's own headlines (screenshots, 2026-09-10 15:53 CT), after Google limited every
    // Ad 1 ad for CLICKBAIT within minutes. His rule: no claim that reads unbelievable
    // without context ("This picture got me abs"); "How I got abs at 40" / "How AI got me
    // abs" are the shapes to reuse. Long headlines and descriptions stay as first written.
    dan: { headlines: ['How I Got Abs At 40', 'See Yourself With Abs - Use AI', 'Abs by AI ®', "Abs By AI - Here's How It Works", 'How I Got Abs With AI Workouts'] } },
  { key: 'ad2', title: 'Ad 2 Stop Wasting Money On Nutritionists',
    segments: ['custom | search | AI fitness', 'custom | search | competitor apps', 'custom | search | get abs belly fat'],
    videos: [
      { id: 'Dtk5knWM7c8', label: 'Muhammad 16:9', slug: 'muhammad-16x9' },
      { id: '7XgHxn59Tsg', label: 'Muhammad vertical', slug: 'muhammad-9x16' },
    ],
    headlines: ['Stop Wasting Money On Nutritionists', 'AI Nutritionist Instead Of A Human One', 'How AI Replaced My Nutritionist', "Track Meals With AI - It's Simple", "AI Meal Plans - Here's How I Use Them"],
    longHeadlines: ["Here's why I stopped paying a nutritionist and use AI to plan and track my meals instead.", 'AI can plan your meals and track your macros. This video shows you how I use it.', 'Daniel Rose explains what a nutritionist costs and what AI does for him instead.'],
    descriptions: ['Daniel Rose shows how AI plans his meals and tracks his macros instead of a nutritionist.', "Most nutritionists charge hundreds a month. Here's how I use AI for the same job.", 'AI meal planning and macro tracking, explained by a guy who did it at 40 years old.'],
    // Dan's own headlines (screenshot, 2026-09-10 15:54 CT).
    dan: { headlines: ['Fire Your Nutritionist. Use AI Instead', 'How AI Replaces Nutritionists', 'How I Got Abs With AI', 'How I Got Abs At 40', 'How AI Got Me Abs'] } },
];

// Dan, 2026-09-10 16:01 CT: "Rewrite and resubmit anything that's still disapproved as clickbait.
// Just rewrite that one specific line only." Google's verdict is per ASSET (line), read from
// ad_group_ad_asset_view; only a line it disapproved is swapped, for the tamer line below.
// Every rewrite passed lint.js with { tame: true }.
var REWRITES = {
  "Daniel Rose shows the AI picture that got him started, and what he did next.": "Daniel Rose shows his AI abs picture and the training plan he followed at 40.",
  "Upload a photo and AI makes a picture of you with abs. Here's how it works.": "Upload a photo and AI makes a picture of you with abs. This video shows how it works.",
  "This video shows how the Abs By AI picture works and what I did after seeing mine.": "This video shows how the Abs By AI picture works and the plan that comes with it.",
  "Here's the AI picture of myself with abs that got me to change how I eat and train.": "Here's the AI picture of myself with abs, and how I changed the way I eat and train.",
  "Upload one photo and AI shows you with abs. This video shows you how I used mine.": "Upload one photo and AI shows you with abs. This video shows you how the app works.",
  "Daniel Rose explains how one AI photo of himself with abs changed his training at 40.": "Daniel Rose explains how he used an AI photo of himself with abs to plan training at 40.",
  "Daniel Rose shows how AI plans his meals and tracks his macros instead of a nutritionist.": "Daniel Rose shows how AI plans his meals and tracks his macros.",
  "Most nutritionists charge hundreds a month. Here's how I use AI for the same job.": "Here's how I use AI to plan meals and track macros instead of a nutritionist.",
  "AI meal planning and macro tracking, explained by a guy who did it at 40 years old.": "AI meal planning and macro tracking, explained step by step.",
  "Here's why I stopped paying a nutritionist and use AI to plan and track my meals instead.": "Here's how I use AI to plan and track my meals instead of paying a nutritionist.",
  "AI can plan your meals and track your macros. This video shows you how I use it.": "AI can plan your meals and track your macros. This video shows you how the app does it.",
  "Daniel Rose explains what a nutritionist costs and what AI does for him instead.": "Daniel Rose explains how AI handles his meal planning and macro tracking.",
};

function main() {
  var out = { tag: 'build-video-campaign:' + MODE, mode: MODE, at: new Date().toISOString(), errors: [] };
  try { out.preview = AdsApp.getExecutionInfo().isPreview(); } catch (e) { out.preview = 'unknown: ' + e; }
  try {
    var acct = AdsApp.currentAccount();
    out.account = { id: acct.getCustomerId(), name: acct.getName(), currency: acct.getCurrencyCode() };
    out.cid = acct.getCustomerId().replace(/-/g, '');
  } catch (e) { out.errors.push('account: ' + e); }

  out.read = readAll(out.cid);
  var plan = buildPlan(out.cid, out.read, out.errors);
  out.plan = plan;

  if (MODE === 'APPLY' && !plan.blocked.length) {
    out.applied = applyPlan(out.cid, plan, out.errors, out.preview === true);
  } else if (MODE === 'APPLY') {
    out.errors.push('APPLY refused: ' + plan.blocked.join(' | '));
  }

  if (out.applied) { var again = readAll(out.cid); out.after = {}; for (var k in again) if (/^built/.test(k)) out.after[k] = again[k]; }

  var ack = post('/api/ytads/dump', out);
  Logger.log('dump ack: ' + JSON.stringify(ack));
  Logger.log('errors: ' + JSON.stringify(out.errors));
  Logger.log('blocked: ' + JSON.stringify(plan.blocked));
  if (out.applied) Logger.log('applied: ' + JSON.stringify(out.applied).slice(0, 3000));
}

// ---------------------------------------------------------------- READ
function q(gaql, limit) {
  var rows = [], n = 0, it = AdsApp.search(gaql);
  while (it.hasNext() && (!limit || n < limit)) { var r = it.next(); n++; rows.push(JSON.parse(JSON.stringify(r))); }
  return rows;
}

function readAll(cid) {
  var r = {}, queries = {
    existing: "SELECT campaign.id, campaign.name, campaign.status FROM campaign WHERE campaign.name = '" + CAMPAIGN_NAME.replace(/'/g, "\\'") + "'",
    customAudiences: "SELECT custom_audience.id, custom_audience.name, custom_audience.status, custom_audience.type, custom_audience.resource_name FROM custom_audience",
    conversionActions: "SELECT conversion_action.id, conversion_action.name, conversion_action.category, conversion_action.origin, conversion_action.status, conversion_action.resource_name FROM conversion_action WHERE conversion_action.status != 'REMOVED'",
    videoAssets: "SELECT asset.resource_name, asset.youtube_video_asset.youtube_video_id, asset.youtube_video_asset.youtube_video_title FROM asset WHERE asset.type = 'YOUTUBE_VIDEO'",
    refCampaigns: "SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.advertising_channel_sub_type, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, campaign.maximize_conversions.target_cpa_micros, campaign.geo_target_type_setting.positive_geo_target_type, campaign.geo_target_type_setting.negative_geo_target_type FROM campaign WHERE campaign.advertising_channel_type = 'DEMAND_GEN' AND campaign.status != 'REMOVED'",
    refAdGroups: "SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status, ad_group.type, ad_group.optimized_targeting_enabled FROM ad_group WHERE campaign.advertising_channel_type = 'DEMAND_GEN' AND ad_group.status != 'REMOVED'",
    refCriteria: "SELECT campaign.name, ad_group.name, ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.status, ad_group_criterion.age_range.type, ad_group_criterion.gender.type, ad_group_criterion.custom_audience.custom_audience, ad_group_criterion.user_list.user_list FROM ad_group_criterion WHERE campaign.advertising_channel_type = 'DEMAND_GEN' AND ad_group_criterion.status != 'REMOVED'",
    refCampaignCriteria: "SELECT campaign.name, campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.language.language_constant FROM campaign_criterion WHERE campaign.advertising_channel_type = 'DEMAND_GEN' AND campaign_criterion.status != 'REMOVED'",
    refAds: "SELECT campaign.name, ad_group_ad.status, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name, ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions FROM ad_group_ad WHERE campaign.advertising_channel_type = 'DEMAND_GEN' AND ad_group_ad.status = 'ENABLED'",
    customerGoals: "SELECT customer_conversion_goal.category, customer_conversion_goal.origin, customer_conversion_goal.biddable FROM customer_conversion_goal",
    // Read-back of the built campaign (verification; empty until it exists).
    builtCampaign: "SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros, campaign_budget.amount_micros, campaign.geo_target_type_setting.positive_geo_target_type, campaign.geo_target_type_setting.negative_geo_target_type FROM campaign WHERE campaign.name = '" + CAMPAIGN_NAME.replace(/'/g, "\\'") + "'",
    builtCriteria: "SELECT campaign_criterion.type, campaign_criterion.negative, campaign_criterion.location.geo_target_constant, campaign_criterion.language.language_constant, campaign_criterion.device.type FROM campaign_criterion WHERE campaign.name = '" + CAMPAIGN_NAME.replace(/'/g, "\\'") + "' AND campaign_criterion.status != 'REMOVED'",
    builtGoals: "SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.name = '" + CAMPAIGN_NAME.replace(/'/g, "\\'") + "'",
    builtAdGroups: "SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.optimized_targeting_enabled, ad_group.audience_setting.use_audience_grouped FROM ad_group WHERE campaign.name = '" + CAMPAIGN_NAME.replace(/'/g, "\\'") + "' AND ad_group.status != 'REMOVED'",
    builtAdGroupCriteria: "SELECT ad_group.name, ad_group_criterion.type, ad_group_criterion.negative, ad_group_criterion.audience.audience, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.name = '" + CAMPAIGN_NAME.replace(/'/g, "\\'") + "' AND ad_group_criterion.status != 'REMOVED'",
    builtAudiences: "SELECT audience.id, audience.name, audience.status, audience.dimensions FROM audience",
    builtAds: "SELECT ad_group.name, ad_group_ad.status, ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.policy_topic_entries, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls, ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name FROM ad_group_ad WHERE campaign.name = '" + CAMPAIGN_NAME.replace(/'/g, "\\'") + "' AND ad_group_ad.status != 'REMOVED'",
  };
  for (var k in queries) {
    try { r[k] = q(queries[k], k === 'refAds' ? 8 : 0); }
    catch (e) { r[k] = null; r[k + 'Error'] = String(e); }
  }
  return r;
}

// ---------------------------------------------------------------- PLAN
// Three steps, learned from the dry runs of 2026-09-10:
//   step 1  budget + campaign + video assets + ad groups + ads, ONE atomic mutateAll
//           with temporary ids (Google validates all of it in preview);
//   step 2  campaign criteria (locations, language) and ad-group criteria
//           (demographics, custom segments) — these carry resource names derived
//           from their parent, which Google cannot derive from a temporary id
//           ("The field's contents don't match another field that represents the
//           same data"), so they go in a second batch against the saved ids;
//   step 3  campaign-specific conversion goals.
// Re-runnable: if the campaign already exists, step 1 is skipped and steps 2/3
// only add what is missing.
function buildPlan(cid, read, errors) {
  var plan = { blocked: [], step1: [], adCount: 0, notes: [] };
  if (!cid) { plan.blocked.push('no customer id'); return plan; }
  plan.existingCampaign = (read.existing && read.existing.length) ? read.existing[0].campaign : null;
  if (plan.existingCampaign) plan.notes.push('campaign already exists (' + plan.existingCampaign.id + ', ' + plan.existingCampaign.status + '): step 1 skipped, steps 2/3 fill in what is missing');

  var segByName = {};
  (read.customAudiences || []).forEach(function (row) { segByName[row.customAudience.name] = row.customAudience; });
  plan.segmentsFound = {};
  ADS.forEach(function (ad) { ad.segments.forEach(function (name) {
    if (segByName[name]) plan.segmentsFound[name] = segByName[name].resourceName || ('customers/' + cid + '/customAudiences/' + segByName[name].id);
    else plan.blocked.push('custom segment not found: ' + name);
  }); });

  var ca = (read.conversionActions || []).filter(function (row) { return row.conversionAction.name === CONVERSION_ACTION; })[0];
  if (!ca) plan.blocked.push('conversion action not found: ' + CONVERSION_ACTION);
  else plan.conversion = ca.conversionAction;

  var ref = (read.refAds || []).filter(function (row) { var d = row.adGroupAd.ad.demandGenVideoResponsiveAd; return d && d.logoImages && d.logoImages.length; })[0];
  if (!ref) plan.blocked.push('no reference Demand Gen ad with a logo found');
  else {
    var d = ref.adGroupAd.ad.demandGenVideoResponsiveAd;
    plan.businessName = d.businessName && d.businessName.text ? d.businessName.text : BUSINESS_NAME_FALLBACK;
    plan.logoImages = d.logoImages.map(function (x) { return x.asset; });
    plan.refAdName = ref.adGroupAd.ad.name;
  }

  var assetByVideo = {};
  (read.videoAssets || []).forEach(function (row) { assetByVideo[row.asset.youtubeVideoAsset.youtubeVideoId] = row.asset.resourceName; });

  var tmp = -1, ops = [];
  function t(kind) { return 'customers/' + cid + '/' + kind + '/' + (tmp--); }

  var budgetRn = t('campaignBudgets');
  ops.push({ campaignBudgetOperation: { create: { resourceName: budgetRn, name: CAMPAIGN_NAME + ' | budget', amountMicros: String(BUDGET_USD * 1000000), deliveryMethod: 'STANDARD', explicitlyShared: false } } });

  var campRn = t('campaigns');
  ops.push({ campaignOperation: { create: {
    resourceName: campRn, name: CAMPAIGN_NAME, status: 'PAUSED', advertisingChannelType: 'DEMAND_GEN',
    campaignBudget: budgetRn,
    // Demand Gen rejects maximizeConversions.targetCpaMicros ("not allowed for the given
    // context", dry run 2026-09-10); Dan's own DG campaigns are plain TARGET_CPA.
    targetCpa: { targetCpaMicros: String(TARGET_CPA_USD * 1000000) },
    geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE', negativeGeoTargetType: 'PRESENCE' },
    containsEuPoliticalAdvertising: 'DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING',
  } } });

  var videoRn = {};
  ADS.forEach(function (ad) { ad.videos.forEach(function (v) {
    if (videoRn[v.id]) return;
    if (assetByVideo[v.id]) { videoRn[v.id] = assetByVideo[v.id]; plan.notes.push('video asset exists: ' + v.id); return; }
    var rn = t('assets'); videoRn[v.id] = rn;
    ops.push({ assetOperation: { create: { resourceName: rn, youtubeVideoAsset: { youtubeVideoId: v.id }, name: 'yt ' + v.id + ' ' + ad.title + ' ' + v.label } } });
  }); });

  plan.adGroups = [];
  ADS.forEach(function (ad) { LANDINGS.forEach(function (lp) {
    var agRn = t('adGroups');
    var agName = ad.title + ' | ' + lp.label;
    // Targeting is NOT set here: API-made Demand Gen ad groups are always "audience
    // grouped", so step 2 attaches one named Audience per ad instead.
    ops.push({ adGroupOperation: { create: { resourceName: agRn, name: agName, campaign: campRn, status: 'ENABLED',
      optimizedTargetingEnabled: false } } });
    var adNames = [];
    ad.videos.forEach(function (v) {
      var url = lp.url + '?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-conv-' + ad.key + '&utm_content=' + v.slug + '-' + lp.key;
      var name = ad.title + ' | ' + v.label + ' | ' + lp.label;
      adNames.push(name);
      ops.push({ adGroupAdOperation: { create: { adGroup: agRn, status: 'ENABLED', ad: {
        name: name, finalUrls: [url],
        demandGenVideoResponsiveAd: {
          headlines: ad.headlines.map(function (x) { return { text: x }; }),
          longHeadlines: ad.longHeadlines.map(function (x) { return { text: x }; }),
          descriptions: ad.descriptions.map(function (x) { return { text: x }; }),
          businessName: { text: plan.businessName || BUSINESS_NAME_FALLBACK },
          videos: [{ asset: videoRn[v.id] }],
          logoImages: (plan.logoImages || []).map(function (rn) { return { asset: rn }; }),
        } } } } });
      plan.adCount++;
    });
    plan.adGroups.push({ name: agName, landing: lp.url, segments: ad.segments, ads: adNames, tmpRn: agRn });
  }); });

  plan.step1 = ops;
  plan.opCount = ops.length;
  return plan;
}

// ---------------------------------------------------------------- STEP 2
// Learned on the live run of 2026-09-10: a Demand Gen ad group created through the API
// is ALWAYS in "audience grouped" mode (audienceSetting.useAudienceGrouped:false is
// ignored), and in that mode Google refuses loose gender / age / custom-segment criteria
// ("Audience segment attachment is not allowed when use audience grouped bit is set to
// true"). Targeting therefore goes in as ONE named Audience per ad (age + gender +
// the ad's custom segments), attached to both of that ad's ad groups.
function audienceName(ad) {
  return ad.title + ' | MU 25-54 | ' + ad.segments.map(function (n) { return n.replace(/^custom \| search \| /, ''); }).join(' + ');
}

function audienceCreate(plan, ad) {
  return { audienceOperation: { create: {
    name: audienceName(ad),
    description: 'Built by scripts/ads/oneoff/build-video-campaign.js 2026-09-10 for ' + CAMPAIGN_NAME,
    dimensions: [
      { age: { ageRanges: [{ minAge: 25, maxAge: 34 }, { minAge: 35, maxAge: 44 }, { minAge: 45, maxAge: 54 }], includeUndetermined: true } },
      { gender: { genders: ['MALE'], includeUndetermined: true } },
      { audienceSegments: { segments: ad.segments.map(function (n) { return { customAudience: { customAudience: plan.segmentsFound[n] } }; }) } },
    ],
  } } };
}

function step2(cid, plan, campaignId, applied, errors) {
  var campRn = 'customers/' + cid + '/campaigns/' + campaignId;
  var rep = applied.step2Report = {};

  // What is there now.
  rep.campaignCriteria = q("SELECT campaign_criterion.type, campaign_criterion.negative, campaign_criterion.criterion_id, campaign_criterion.location.geo_target_constant, campaign_criterion.language.language_constant, campaign_criterion.device.type FROM campaign_criterion WHERE campaign.id = " + campaignId + " AND campaign_criterion.status != 'REMOVED'").map(function (r) { return r.campaignCriterion; });
  rep.adGroups = q("SELECT ad_group.id, ad_group.name, ad_group.resource_name, ad_group.audience_setting.use_audience_grouped, ad_group.optimized_targeting_enabled FROM ad_group WHERE campaign.id = " + campaignId + " AND ad_group.status != 'REMOVED'").map(function (r) { return r.adGroup; });
  rep.geoSetting = q("SELECT campaign.geo_target_type_setting.positive_geo_target_type, campaign.geo_target_type_setting.negative_geo_target_type FROM campaign WHERE campaign.id = " + campaignId).map(function (r) { return r.campaign.geoTargetTypeSetting; })[0];

  // 2a — locations + language. This campaign keeps them AT THE AD GROUP ("Location and
  // language: Set at ad group" in its settings page, 2026-09-10), which is why every
  // campaign-level location/language create came back "The error code is not in this
  // version". So: one LOCATION criterion per country and one LANGUAGE criterion per ad
  // group, each with its derived resource name, only where missing. The campaign's geo
  // setting is put back to PRESENCE (an earlier fallback had flipped it).
  var geoNow = rep.geoSetting && rep.geoSetting.positiveGeoTargetType;
  if (geoNow !== 'PRESENCE') {
    var fix = AdsApp.mutate({ campaignOperation: { update: { resourceName: campRn, geoTargetTypeSetting: { positiveGeoTargetType: 'PRESENCE', negativeGeoTargetType: 'PRESENCE' } }, updateMask: 'geo_target_type_setting.positive_geo_target_type,geo_target_type_setting.negative_geo_target_type' } }, { partialFailure: false });
    applied.step2aGeoFix = fix.isSuccessful() ? ('geo setting ' + geoNow + ' -> PRESENCE') : 'geo fix failed: ' + fix.getErrorMessages().join('; ');
  }
  var haveAg = {};
  q("SELECT ad_group.name, ad_group_criterion.type, ad_group_criterion.location.geo_target_constant, ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = " + campaignId + " AND ad_group_criterion.status != 'REMOVED' AND ad_group_criterion.type IN ('LOCATION', 'LANGUAGE')")
    .forEach(function (r) { var c = r.adGroupCriterion; if (c.location) haveAg[r.adGroup.name + '|loc:' + c.location.geoTargetConstant] = true; if (c.language) haveAg[r.adGroup.name + '|lang:' + c.language.languageConstant] = true; });
  var geoOps = [];
  rep.adGroups.forEach(function (ag) {
    var agId = ag.resourceName.split('/').pop();
    function critRn(constant) { return 'customers/' + cid + '/adGroupCriteria/' + agId + '~' + constant.split('/').pop(); }
    for (var g in GEO) if (!haveAg[ag.name + '|loc:' + GEO[g]]) geoOps.push({ adGroupCriterionOperation: { create: { resourceName: critRn(GEO[g]), adGroup: ag.resourceName, location: { geoTargetConstant: GEO[g] } } } });
    if (!haveAg[ag.name + '|lang:' + LANGUAGE]) geoOps.push({ adGroupCriterionOperation: { create: { resourceName: critRn(LANGUAGE), adGroup: ag.resourceName, language: { languageConstant: LANGUAGE } } } });
  });
  applied.step2a = runSingles(geoOps, 'step2a', errors);

  // 2b — one Audience per ad, reused if it already exists by name.
  var audByName = {};
  q("SELECT audience.id, audience.name, audience.resource_name, audience.status FROM audience").forEach(function (r) { audByName[r.audience.name] = r.audience.resourceName; });
  var audOps = [], audOpsAds = [];
  ADS.forEach(function (ad) { if (!audByName[audienceName(ad)]) { audOps.push(audienceCreate(plan, ad)); audOpsAds.push(ad); } });
  applied.step2b = runBatch(audOps, 'step2b', errors);
  if (applied.step2b.rows) applied.step2b.rows.forEach(function (row, i) { if (row.ok) audByName[audienceName(audOpsAds[i])] = row.rn; });
  rep.audiences = {}; ADS.forEach(function (ad) { rep.audiences[audienceName(ad)] = audByName[audienceName(ad)] || null; });
  if (applied.step2b.failed) return;

  // 2c — attach each ad's audience to its two ad groups (skip the ones already attached).
  var groups = {}; rep.adGroups.forEach(function (ag) { groups[ag.name] = ag.resourceName; });
  var attached = {};
  q("SELECT ad_group.name, ad_group_criterion.audience.audience FROM ad_group_criterion WHERE campaign.id = " + campaignId + " AND ad_group_criterion.type = 'AUDIENCE' AND ad_group_criterion.status != 'REMOVED'").forEach(function (r) { attached[r.adGroup.name + '|' + r.adGroupCriterion.audience.audience] = true; });
  var attOps = [];
  ADS.forEach(function (ad) { LANDINGS.forEach(function (lp) {
    var agName = ad.title + ' | ' + lp.label, agRn = groups[agName], audRn = audByName[audienceName(ad)];
    if (!agRn) { (rep.adGroupsMissing = rep.adGroupsMissing || []).push(agName); return; }
    if (!audRn || attached[agName + '|' + audRn]) return;
    var rn = 'customers/' + cid + '/adGroupCriteria/' + agRn.split('/').pop() + '~' + audRn.split('/').pop();
    attOps.push({ adGroupCriterionOperation: { create: { resourceName: rn, adGroup: agRn, audience: { audience: audRn } } } });
  }); });
  applied.step2c = runSingles(attOps, 'step2c', errors);
}

// ---------------------------------------------------------------- APPLY
function runBatch(ops, label, errors) {
  if (!ops.length) return { label: label, count: 0, failed: 0, skipped: 'nothing to do' };
  var results;
  try { results = AdsApp.mutateAll(ops, { partialFailure: false }); }
  catch (e) { errors.push(label + ' mutateAll threw: ' + e); return { label: label, failed: ops.length, threw: String(e) }; }
  var rows = results.map(function (r, i) { var ok = r.isSuccessful();
    return { i: i, op: Object.keys(ops[i])[0], ok: ok, rn: ok ? r.getResourceName() : null, err: ok ? null : r.getErrorMessages().join('; ') }; });
  var failed = rows.filter(function (x) { return !x.ok; });
  if (failed.length) errors.push(label + ': ' + failed.length + ' of ' + rows.length + ' operations failed');
  return { label: label, count: rows.length, failed: failed.length, rows: rows };
}

// One operation at a time, with partialFailure OFF: the default (on) is refused by
// campaign conversion goals ("This operation cannot be used with partial_failure").
// Criteria whose id is a Google constant (a country, a language, an audience) must
// also carry their EXACT derived resource name: the Ads Scripts wrapper stamps a
// temporary name on any create that lacks one, and Google then answers "The field's
// contents don't match another field that represents the same data. At
// ...create.resourceName" (measured 2026-09-10, both in mutateAll and single mutate).
function runSingles(ops, label, errors) {
  if (!ops.length) return { label: label, count: 0, failed: 0, skipped: 'nothing to do' };
  var rows = ops.map(function (op, i) {
    try { var r = AdsApp.mutate(op, { partialFailure: false }); var ok = r.isSuccessful();
      return { i: i, op: Object.keys(op)[0], ok: ok, rn: ok ? r.getResourceName() : null, err: ok ? null : r.getErrorMessages().join('; ') }; }
    catch (e) { return { i: i, op: Object.keys(op)[0], ok: false, rn: null, err: 'threw: ' + e }; }
  });
  var failed = rows.filter(function (x) { return !x.ok; });
  if (failed.length) errors.push(label + ': ' + failed.length + ' of ' + rows.length + ' operations failed');
  return { label: label, count: rows.length, failed: failed.length, rows: rows };
}

function applyPlan(cid, plan, errors, isPreview) {
  var applied = {};
  var campaignId = plan.existingCampaign ? String(plan.existingCampaign.id) : null;

  if (!campaignId) {
    applied.step1 = runBatch(plan.step1, 'step1', errors);
    if (applied.step1.failed) return applied;
    var m = /campaigns\/(\d+)/.exec(applied.step1.rows[1].rn || '');
    if (!m || Number(m[1]) < 0) { applied.step2 = applied.step3 = 'skipped: step 1 ran in preview, so the campaign has no saved id yet'; return applied; }
    campaignId = m[1];
  } else applied.step1 = 'skipped: campaign ' + campaignId + ' already exists';
  applied.campaignId = campaignId;

  try { step2(cid, plan, campaignId, applied, errors); } catch (e) { errors.push('step2 threw: ' + e); return applied; }
  if ((applied.step2c && applied.step2c.failed) || (applied.step2b && applied.step2b.failed)) return applied;

  // Step 3 — campaign-specific conversion goals: only Free Generation Started's
  // category/origin is biddable.
  var goals;
  try { goals = q("SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable, campaign_conversion_goal.resource_name FROM campaign_conversion_goal WHERE campaign.id = " + campaignId); }
  catch (e) { errors.push('step3 read: ' + e); return applied; }
  var want = plan.conversion.category + '/' + plan.conversion.origin;
  // The wanted goal is written biddable:true FIRST and explicitly, even though it reads
  // true already: switching a campaign to its own goals starts from an empty list, and
  // writing only the false ones fails with "The campaign is using campaign override goals
  // but has no goals configured" (preview 2026-09-10).
  var ops3 = [];
  goals.forEach(function (row) { var g = row.campaignConversionGoal; if ((g.category + '/' + g.origin) === want)
    ops3.push({ campaignConversionGoalOperation: { update: { resourceName: g.resourceName, biddable: true }, updateMask: 'biddable' } }); });
  goals.forEach(function (row) { var g = row.campaignConversionGoal; if ((g.category + '/' + g.origin) !== want && g.biddable)
    ops3.push({ campaignConversionGoalOperation: { update: { resourceName: g.resourceName, biddable: false }, updateMask: 'biddable' } }); });
  applied.step3Want = want;
  applied.step3 = runSingles(ops3, 'step3', errors);
  try { applied.goalsAfter = q("SELECT campaign_conversion_goal.category, campaign_conversion_goal.origin, campaign_conversion_goal.biddable FROM campaign_conversion_goal WHERE campaign.id = " + campaignId).map(function (row) { return row.campaignConversionGoal; }).filter(function (g) { return g.biddable; }); } catch (e) {}

  // Step 4 — Dan's headlines on EVERY ad of each ad (an update re-triggers policy review;
  // the ad keeps its id). Only the headlines field is touched.
  var ops4 = [], step4 = applied.step4Report = [];
  q("SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines FROM ad_group_ad WHERE campaign.id = " + campaignId + " AND ad_group_ad.status != 'REMOVED'")
    .forEach(function (row) {
      var a = row.adGroupAd;
      var ad = ADS.filter(function (x) { return x.dan && a.ad.name.indexOf(x.title + ' | ') === 0; })[0];
      if (!ad) return;
      var now = ((a.ad.demandGenVideoResponsiveAd || {}).headlines || []).map(function (h) { return h.text; });
      if (now.join('|') === ad.dan.headlines.join('|')) { step4.push({ ad: a.ad.name, skipped: "Dan's headlines already in place" }); return; }
      step4.push({ ad: a.ad.name, was: now, policy: (a.policySummary || {}).approvalStatus });
      ops4.push({ adOperation: { update: { resourceName: 'customers/' + cid + '/ads/' + a.ad.id, demandGenVideoResponsiveAd: {
        headlines: ad.dan.headlines.map(function (x) { return { text: x }; }) } },
        updateMask: 'demand_gen_video_responsive_ad.headlines' } });
    });
  applied.step4 = runSingles(ops4, 'step4', errors);

  // Step 5 — per-line policy: swap ONLY the lines Google disapproved (Clickbait) for their
  // rewrite, on every ad that carries them. Headlines are Dan's and are reported, not rewritten.
  var rep5 = applied.step5Report = [], ops5 = [], flagged = {};
  q("SELECT ad_group_ad.ad.id, ad_group_ad_asset_view.field_type, ad_group_ad_asset_view.policy_summary, asset.text_asset.text FROM ad_group_ad_asset_view WHERE campaign.id = " + campaignId + " AND ad_group_ad.status != 'REMOVED'")
    .forEach(function (row) {
      var v = row.adGroupAdAssetView, ps = v.policySummary || {}, topics = (ps.policyTopicEntries || []).map(function (t) { return t.topic; });
      if (ps.approvalStatus !== 'DISAPPROVED' && topics.indexOf('CLICKBAIT') < 0) return;
      var text = row.asset && row.asset.textAsset ? row.asset.textAsset.text : null;
      (flagged[row.adGroupAd.ad.id] = flagged[row.adGroupAd.ad.id] || []).push({ field: v.fieldType, text: text, status: ps.approvalStatus, topics: topics });
    });
  q("SELECT ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions FROM ad_group_ad WHERE campaign.id = " + campaignId + " AND ad_group_ad.status != 'REMOVED'")
    .forEach(function (row) {
      var a = row.adGroupAd, flags = flagged[a.ad.id]; if (!flags) return;
      var dg = a.ad.demandGenVideoResponsiveAd || {}, lists = { HEADLINE: 'headlines', LONG_HEADLINE: 'longHeadlines', DESCRIPTION: 'descriptions' };
      var upd = {}, mask = [], report = { ad: a.ad.name, swaps: [], untouched: [] };
      flags.forEach(function (f) {
        var key = lists[f.field], to = REWRITES[f.text];
        if (!key || !to) { report.untouched.push(f); return; }
        var list = (upd[key] || (dg[key] || []).map(function (x) { return { text: x.text }; }));
        var hit = false; list.forEach(function (x) { if (x.text === f.text) { x.text = to; hit = true; } });
        if (!hit) { report.untouched.push(f); return; }
        upd[key] = list; if (mask.indexOf(key) < 0) mask.push(key);
        report.swaps.push({ field: f.field, from: f.text, to: to });
      });
      rep5.push(report);
      if (!mask.length) return;
      var snake = { headlines: 'headlines', longHeadlines: 'long_headlines', descriptions: 'descriptions' };
      ops5.push({ adOperation: { update: { resourceName: 'customers/' + cid + '/ads/' + a.ad.id, demandGenVideoResponsiveAd: upd },
        updateMask: mask.map(function (k) { return 'demand_gen_video_responsive_ad.' + snake[k]; }).join(',') } });
    });
  applied.step5 = runSingles(ops5, 'step5', errors);
  return applied;
}

// ---------------------------------------------------------------- HTTP
function post(path, body) {
  var res = UrlFetchApp.fetch(SERVER + path, {
    method: 'post', contentType: 'application/json', headers: { 'X-YTADS-Key': KEY },
    payload: JSON.stringify(body), muteHttpExceptions: true,
  });
  try { return JSON.parse(res.getContentText()); } catch (e) { return { status: res.getResponseCode(), text: res.getContentText().slice(0, 300) }; }
}
