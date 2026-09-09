// ======================================================================
// ONE-OFF Google Ads Script — Search repair + /start A/B  (2026-09-09)
// ======================================================================
// Executes Handoffs/handoff-20260909-google-ads-account-fixes.md inside
// account 342-717-0837. Install as a SECOND script (Tools -> Scripts),
// run it, then DELETE it. It must never be scheduled.
//
// MODE decides what it does:
//   'REPORT' — reads only. Makes no change of any kind. Safe to preview.
//   'APPLY'  — makes the changes, each one idempotent and each recorded
//              with its before value.
// Both modes POST what they found to absbyai.com/api/ytads/dump, because
// the Google Ads UI freezes for minutes at a time and the editor's log
// panel is not a reliable read channel.
//
// The canonical copy is scripts/ads/oneoff/search-repair.js in the repo;
// the pasted copy in Google Ads differs only in the KEY line.

var SERVER = 'https://absbyai.com';
var KEY = 'PASTE_YTADS_KEY_HERE';   // = YTADS_KEY on Railway. Never commit a real key.
var MODE = 'REPORT';                // 'REPORT' or 'APPLY'

var BRAND = 'Brand - Search - US';
var NONBRAND = 'Search - US - Non-Brand - AI Abs Preview';
var TIER2_ID = '24122099676';       // [DAN] [DGEN] ... geo tier 2 | ALL CONTENT
var TIER2_BUDGET = 5.00;            // Dan's instruction 2026-09-09: $15/day -> $5/day
var MAX_CPC = 2.00;                 // Maximize Clicks bid ceiling
var START_URL = 'https://absbyai.com/start';

// Phrase negatives for the brand campaign: stop close variants harvesting generics.
var BRAND_NEGATIVES = ['abs ai', 'ai abs', 'ai ab generator', 'ai abs generator'];
// Wrong-intent negatives for the non-brand campaign. Deliberately short.
var NONBRAND_NEGATIVES = ['fat', 'gain weight'];
// Broadening keywords, phrase match, per ad group name.
var NEW_KEYWORDS = {
  'AI Abs Generator': ['abs generator app', 'six pack photo editor'],
  'AI Body Transformation Preview': ['body transformation ai', 'ai fitness transformation'],
  'What Would I Look Like With Abs': ['what would i look like with abs', 'see myself with abs'],
};

function main() {
  var out = { tag: 'search-repair:' + MODE, mode: MODE, at: new Date().toISOString(), errors: [] };
  try {
    var acct = AdsApp.currentAccount();
    out.account = { id: acct.getCustomerId(), name: acct.getName(), currency: acct.getCurrencyCode(), tz: acct.getTimeZone() };
  } catch (e) { out.errors.push('account: ' + e); }

  out.read = readAll();
  if (MODE === 'APPLY') out.applied = applyAll(out.read);

  var ack = post('/api/ytads/dump', out);
  Logger.log('dump ack: ' + JSON.stringify(ack));
  Logger.log(summarise(out));
}

// ----------------------------------------------------------------------
// READ — every query is optional; a failure is recorded, never fatal.
// ----------------------------------------------------------------------

function q(gaql, limit) {
  var rows = [], n = 0;
  var it = AdsApp.search(gaql);
  while (it.hasNext() && (!limit || n < limit)) {
    var r = it.next(); n++;
    try { rows.push(JSON.parse(JSON.stringify(r))); }
    catch (e) { rows.push({ unserialisable: String(e) }); }
  }
  return rows;
}

function readAll() {
  var r = {}, queries = {
    campaigns: "SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, " +
      "campaign.bidding_strategy_type, campaign.bidding_strategy, campaign.campaign_budget, " +
      "campaign_budget.id, campaign_budget.name, campaign_budget.amount_micros, campaign_budget.explicitly_shared, " +
      "campaign_budget.delivery_method, campaign.tracking_url_template " +
      "FROM campaign WHERE campaign.status != 'REMOVED'",
    biddingDetail: "SELECT campaign.id, campaign.name, campaign.bidding_strategy_type, " +
      "campaign.target_cpa.target_cpa_micros, campaign.target_spend.cpc_bid_ceiling_micros, " +
      "campaign.maximize_conversions.target_cpa_micros " +
      "FROM campaign WHERE campaign.status != 'REMOVED'",
    conversionActions: "SELECT conversion_action.id, conversion_action.name, conversion_action.category, " +
      "conversion_action.origin, conversion_action.status, conversion_action.type, " +
      "conversion_action.include_in_conversions_metric, conversion_action.counting_type " +
      "FROM conversion_action WHERE conversion_action.status != 'REMOVED'",
    conversionActionsPrimary: "SELECT conversion_action.id, conversion_action.name, conversion_action.primary_for_goal " +
      "FROM conversion_action WHERE conversion_action.status != 'REMOVED'",
    customerGoals: "SELECT customer_conversion_goal.category, customer_conversion_goal.origin, customer_conversion_goal.biddable " +
      "FROM customer_conversion_goal",
    campaignGoals: "SELECT campaign.id, campaign.name, campaign_conversion_goal.category, campaign_conversion_goal.origin, " +
      "campaign_conversion_goal.biddable FROM campaign_conversion_goal",
    goalConfig: "SELECT campaign.id, campaign.name, conversion_goal_campaign_config.goal_config_level, " +
      "conversion_goal_campaign_config.custom_conversion_goal FROM conversion_goal_campaign_config",
    adGroups: "SELECT campaign.id, campaign.name, ad_group.id, ad_group.name, ad_group.status, ad_group.type, " +
      "ad_group.cpc_bid_micros FROM ad_group WHERE campaign.advertising_channel_type = 'SEARCH' AND ad_group.status != 'REMOVED'",
    adRotation: "SELECT campaign.id, ad_group.id, ad_group.name, ad_group.ad_rotation_mode " +
      "FROM ad_group WHERE campaign.advertising_channel_type = 'SEARCH' AND ad_group.status != 'REMOVED'",
    ads: "SELECT campaign.id, campaign.name, ad_group.id, ad_group.name, ad_group_ad.resource_name, ad_group_ad.status, " +
      "ad_group_ad.ad.id, ad_group_ad.ad.type, ad_group_ad.ad.name, ad_group_ad.ad.final_urls, " +
      "ad_group_ad.ad.final_url_suffix, ad_group_ad.ad.tracking_url_template, " +
      "ad_group_ad.ad.responsive_search_ad.headlines, ad_group_ad.ad.responsive_search_ad.descriptions, " +
      "ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2, " +
      "ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status " +
      "FROM ad_group_ad WHERE campaign.advertising_channel_type = 'SEARCH' AND ad_group_ad.status != 'REMOVED'",
    keywords: "SELECT campaign.id, campaign.name, ad_group.id, ad_group.name, ad_group_criterion.criterion_id, " +
      "ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, " +
      "ad_group_criterion.negative, ad_group_criterion.effective_cpc_bid_micros " +
      "FROM ad_group_criterion WHERE campaign.advertising_channel_type = 'SEARCH' " +
      "AND ad_group_criterion.type = 'KEYWORD' AND ad_group_criterion.status != 'REMOVED'",
    campaignNegatives: "SELECT campaign.id, campaign.name, campaign_criterion.criterion_id, campaign_criterion.type, " +
      "campaign_criterion.negative, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type " +
      "FROM campaign_criterion WHERE campaign_criterion.type = 'KEYWORD' AND campaign_criterion.status != 'REMOVED'",
    dailyCost: "SELECT campaign.id, campaign.name, segments.date, metrics.cost_micros, metrics.clicks, " +
      "metrics.impressions, metrics.conversions FROM campaign " +
      "WHERE campaign.advertising_channel_type = 'SEARCH' AND segments.date DURING LAST_14_DAYS",
    searchTerms: "SELECT campaign.name, ad_group.name, search_term_view.search_term, search_term_view.status, " +
      "segments.keyword.info.text, segments.keyword.info.match_type, metrics.clicks, metrics.impressions, " +
      "metrics.cost_micros, metrics.conversions FROM search_term_view WHERE segments.date DURING LAST_30_DAYS " +
      "ORDER BY metrics.cost_micros DESC LIMIT 300",
    changeHistory: "SELECT change_event.change_date_time, change_event.change_resource_type, change_event.change_resource_name, " +
      "change_event.changed_fields, change_event.user_email, change_event.client_type, " +
      "change_event.resource_change_operation, change_event.old_resource, change_event.new_resource, campaign.name " +
      "FROM change_event WHERE change_event.change_date_time DURING LAST_14_DAYS " +
      "ORDER BY change_event.change_date_time DESC LIMIT 500",
  };
  for (var k in queries) {
    try { r[k] = q(queries[k]); }
    catch (e) { r[k] = null; r[k + '_error'] = String(e && e.message || e); }
  }
  return r;
}

// ----------------------------------------------------------------------
// APPLY
// ----------------------------------------------------------------------

function applyAll(read) {
  var log = [];
  function step(name, fn) {
    try { var v = fn(); log.push({ step: name, ok: true, detail: v }); }
    catch (e) { log.push({ step: name, ok: false, error: String(e && e.message || e) }); }
    return log[log.length - 1];
  }

  // Goals first: the handoff's ordering — everything else is downstream of the signal.
  step('task1:conversion-goals', function () { return setCampaignGoals(read); });
  step('task2:tier2-budget', function () { return setTier2Budget(); });
  step('task3c:bidding', function () { return setBidding(); });
  step('task3a:brand-negatives', function () { return addCampaignNegatives(BRAND, BRAND_NEGATIVES); });
  step('task3b:nonbrand-negatives', function () { return addCampaignNegatives(NONBRAND, NONBRAND_NEGATIVES); });
  step('task3d:keywords', function () { return addKeywords(); });
  step('task4:start-ads', function () { return duplicateAdsToStart(read); });
  step('task4b:ad-rotation', function () { return setAdRotation(); });
  return log;
}

function campaignByName(name) {
  var it = AdsApp.campaigns().withCondition("campaign.name = '" + name + "'").get();
  if (!it.hasNext()) throw new Error('campaign not found: ' + name);
  return it.next();
}

function setTier2Budget() {
  var it = AdsApp.campaigns().withCondition('campaign.id = ' + TIER2_ID).get();
  if (!it.hasNext()) throw new Error('tier-2 campaign ' + TIER2_ID + ' not found');
  var c = it.next(), b = c.getBudget();
  var before = b.getAmount(), shared = b.isExplicitlyShared();
  var users = 0, cs = b.campaigns().get(); while (cs.hasNext()) { cs.next(); users++; }
  if (shared || users > 1) throw new Error('budget is shared across ' + users + ' campaigns (explicitlyShared=' + shared + ') — NOT changed, per the handoff');
  if (Math.abs(before - TIER2_BUDGET) < 0.005) return { alreadyDone: true, amount: before };
  b.setAmount(TIER2_BUDGET);
  return { campaign: c.getName(), before: before, after: TIER2_BUDGET, budgetId: b.getId(), shared: shared, users: users };
}

function setBidding() {
  var res = [];
  [BRAND, NONBRAND].forEach(function (name) {
    var c = campaignByName(name), bid = c.bidding();
    var before = { type: bid.getStrategyType(), targetCpa: safe(function () { return bid.getTargetCpa(); }), ceiling: safe(function () { return bid.getCpcBidCeiling(); }) };
    if (before.type === 'TARGET_SPEND') { res.push({ campaign: name, alreadyDone: true, before: before }); return; }
    bid.setStrategy('TARGET_SPEND', bid.argsBuilder().withCpcBidCeiling(MAX_CPC));
    res.push({ campaign: name, before: before, after: { type: 'TARGET_SPEND', ceiling: MAX_CPC } });
  });
  return res;
}

function safe(fn) { try { return fn(); } catch (e) { return null; } }

function addCampaignNegatives(campaignName, texts) {
  var c = campaignByName(campaignName);
  var have = {}, it = c.negativeKeywords().get();
  while (it.hasNext()) { have[String(it.next().getText()).toLowerCase()] = true; }
  var added = [], skipped = [];
  texts.forEach(function (t) {
    var phrase = '"' + t + '"';
    if (have[phrase.toLowerCase()] || have[t.toLowerCase()]) { skipped.push(t); return; }
    c.createNegativeKeyword(phrase);
    added.push(phrase);
  });
  return { campaign: campaignName, added: added, skippedAlreadyPresent: skipped, hadBefore: Object.keys(have) };
}

function addKeywords() {
  var c = campaignByName(NONBRAND), out = [];
  var groups = c.adGroups().get();
  while (groups.hasNext()) {
    var g = groups.next(), want = NEW_KEYWORDS[g.getName()];
    if (!want) { out.push({ adGroup: g.getName(), skipped: 'no keywords configured for this ad group' }); continue; }
    var have = {}, ks = g.keywords().get();
    while (ks.hasNext()) { have[String(ks.next().getText()).toLowerCase().replace(/^[\["]|[\]"]$/g, '')] = true; }
    var added = [], skipped = [];
    want.forEach(function (t) {
      if (have[t.toLowerCase()]) { skipped.push(t); return; }
      var op = g.newKeywordBuilder().withText('"' + t + '"').build();
      if (!op.isSuccessful()) { skipped.push(t + ' FAILED: ' + op.getErrors().join('; ')); return; }
      added.push('"' + t + '"');
    });
    out.push({ adGroup: g.getName(), added: added, skipped: skipped });
  }
  return out;
}

function duplicateAdsToStart(read) {
  var out = [];
  var byGroup = {};
  (read.ads || []).forEach(function (row) {
    var a = row.adGroupAd || {}, ad = a.ad || {};
    if (ad.type !== 'RESPONSIVE_SEARCH_AD') return;
    var gid = String((row.adGroup || {}).id);
    (byGroup[gid] = byGroup[gid] || []).push({ row: row, ad: ad, status: a.status,
      finalUrl: (ad.finalUrls || [])[0] || '', groupName: (row.adGroup || {}).name });
  });

  for (var gid in byGroup) {
    var ads = byGroup[gid];
    var already = ads.filter(function (x) { return /\/start/.test(x.finalUrl); });
    var source = ads.filter(function (x) { return x.status === 'ENABLED' && !/\/start/.test(x.finalUrl); })[0];
    var groupName = ads[0].groupName;
    if (already.length) { out.push({ adGroup: groupName, skipped: 'a /start ad already exists', adIds: already.map(function (x) { return String(x.ad.id); }) }); continue; }
    if (!source) { out.push({ adGroup: groupName, skipped: 'no enabled non-/start RSA to copy' }); continue; }

    var it = AdsApp.adGroups().withCondition('ad_group.id = ' + gid).get();
    if (!it.hasNext()) { out.push({ adGroup: groupName, error: 'ad group ' + gid + ' not found' }); continue; }
    var group = it.next();
    var rsa = source.ad.responsiveSearchAd || {};
    var heads = (rsa.headlines || []).map(assetOf);
    var descs = (rsa.descriptions || []).map(assetOf);
    if (heads.length < 3 || descs.length < 2) { out.push({ adGroup: groupName, error: 'source ad has ' + heads.length + ' headlines / ' + descs.length + ' descriptions — refusing to build a partial copy' }); continue; }

    var b = group.newAd().responsiveSearchAdBuilder()
      .withHeadlines(heads).withDescriptions(descs).withFinalUrl(START_URL);
    if (rsa.path1) b = b.withPath1(rsa.path1);
    if (rsa.path2) b = b.withPath2(rsa.path2);
    if (source.ad.trackingUrlTemplate) b = b.withTrackingTemplate(source.ad.trackingUrlTemplate);
    if (source.ad.finalUrlSuffix) b = b.withFinalUrlSuffix(source.ad.finalUrlSuffix);
    var op = b.build();
    if (!op.isSuccessful()) { out.push({ adGroup: groupName, error: op.getErrors().join('; ') }); continue; }
    out.push({ adGroup: groupName, createdFrom: String(source.ad.id), sourceFinalUrl: source.finalUrl,
      newFinalUrl: START_URL, headlines: heads, descriptions: descs, path1: rsa.path1 || null, path2: rsa.path2 || null,
      newAdId: safe(function () { return String(op.getResult().getId()); }) });
  }
  return out;
}

function assetOf(a) {
  if (!a) return '';
  if (!a.pinnedField || a.pinnedField === 'UNSPECIFIED' || a.pinnedField === 'UNKNOWN') return a.text;
  return { text: a.text, pinning: a.pinnedField };
}

function setAdRotation() {
  var out = [], cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
  [BRAND, NONBRAND].forEach(function (name) {
    var c = campaignByName(name), groups = c.adGroups().get();
    while (groups.hasNext()) {
      var g = groups.next(), rn = 'customers/' + cid + '/adGroups/' + g.getId();
      try {
        var r = AdsApp.mutate({ adGroupOperation: { update: { resourceName: rn, adRotationMode: 'ROTATE_FOREVER' }, updateMask: 'ad_rotation_mode' } });
        out.push({ adGroup: g.getName(), ok: r.isSuccessful(), error: r.isSuccessful() ? null : r.getErrorMessages().join('; ') });
      } catch (e) { out.push({ adGroup: g.getName(), ok: false, error: String(e && e.message || e) }); }
    }
  });
  return out;
}

// Campaign-specific conversion goals: only (SUBMIT_LEAD_FORM, WEBSITE) biddable.
// Mutating any CampaignConversionGoal flips goal_config_level to CAMPAIGN by itself.
function setCampaignGoals(read) {
  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, ''), out = [];
  var want = [{ category: 'SUBMIT_LEAD_FORM', origin: 'WEBSITE', biddable: true }];
  var goals = read.customerGoals || [];
  var ids = {};
  (read.campaigns || []).forEach(function (r) {
    var c = r.campaign || {};
    if (c.name === BRAND || c.name === NONBRAND) ids[c.name] = String(c.id);
  });

  for (var name in ids) {
    var campaignId = ids[name], ops = [], plan = [];
    goals.forEach(function (g) {
      var cg = g.customerConversionGoal || {};
      var target = (cg.category === 'SUBMIT_LEAD_FORM' && cg.origin === 'WEBSITE');
      plan.push({ category: cg.category, origin: cg.origin, wasBiddableAtAccount: !!cg.biddable, setTo: target });
      ops.push({ campaignConversionGoalOperation: { update: {
        resourceName: 'customers/' + cid + '/campaignConversionGoals/' + campaignId + '~' + cg.category + '~' + cg.origin,
        biddable: target }, updateMask: 'biddable' } });
    });
    // Make sure the one we want is set even if it is absent from the account list.
    var haveTarget = plan.some(function (p) { return p.category === 'SUBMIT_LEAD_FORM' && p.origin === 'WEBSITE'; });
    if (!haveTarget) {
      plan.push({ category: 'SUBMIT_LEAD_FORM', origin: 'WEBSITE', wasBiddableAtAccount: false, setTo: true, addedByUs: true });
      ops.push({ campaignConversionGoalOperation: { update: {
        resourceName: 'customers/' + cid + '/campaignConversionGoals/' + campaignId + '~SUBMIT_LEAD_FORM~WEBSITE',
        biddable: true }, updateMask: 'biddable' } });
    }
    var results = [];
    ops.forEach(function (op, i) {
      try { var r = AdsApp.mutate(op); results.push({ goal: plan[i], ok: r.isSuccessful(), error: r.isSuccessful() ? null : r.getErrorMessages().join('; ') }); }
      catch (e) { results.push({ goal: plan[i], ok: false, error: String(e && e.message || e) }); }
    });
    out.push({ campaign: name, campaignId: campaignId, want: want, results: results });
  }
  return out;
}

// ----------------------------------------------------------------------

function summarise(out) {
  var r = out.read || {}, s = ['MODE ' + out.mode];
  ['campaigns', 'adGroups', 'ads', 'keywords', 'campaignNegatives', 'customerGoals', 'campaignGoals', 'searchTerms', 'changeHistory'].forEach(function (k) {
    s.push(k + '=' + (r[k] ? r[k].length : 'ERR ' + (r[k + '_error'] || '')));
  });
  (out.applied || []).forEach(function (a) { s.push(a.step + (a.ok ? ' OK' : ' FAIL ' + a.error)); });
  return s.join(' | ');
}

function post(path, body) {
  var res = UrlFetchApp.fetch(SERVER + path, { method: 'post', contentType: 'application/json',
    headers: { 'X-YTADS-Key': KEY }, payload: JSON.stringify(body), muteHttpExceptions: true });
  var code = res.getResponseCode(), text = res.getContentText();
  if (code !== 200) { Logger.log('POST ' + path + ' -> ' + code + ' ' + text.slice(0, 300)); return null; }
  try { return JSON.parse(text); } catch (e) { return null; }
}
