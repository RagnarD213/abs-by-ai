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
//
// WHAT ACTUALLY HAPPENED, 2026-09-09. The REPORT pass ran here and is what the
// whole job was calibrated against. The APPLY pass could NOT be installed —
// pasting a script body of this size into the editor is blocked as code
// injection — so the changes went through two other channels instead:
//   * the ytads manual mutation queue (scripts/ads/ytads/manual.js) for the
//     budget, the negatives, the keywords, the /start ads and ad rotation:
//     36 of 44 operations landed on the first hourly run;
//   * the Ads UI for the two it cannot do — campaign conversion goals
//     ("This operation cannot be used with partial_failure", because the
//     hourly script calls AdsApp.mutate without {partialFailure:false}) and
//     the bidding-strategy switch ("The field mask updated a field with
//     subfields: 'target_spend'" — the mask wants leaf fields).
// The APPLY code below is kept, unrun, because it is the written record of
// what was done and because a future one-off can reuse it. If it is ever run,
// every step is idempotent and will report "alreadyDone".

var SERVER = 'https://absbyai.com';
var KEY = 'PASTE_YTADS_KEY_HERE';   // = YTADS_KEY on Railway. Never commit a real key.
var MODE = 'REPORT';                // 'REPORT' or 'APPLY'

var BRAND = 'Brand - Search - US';           // id 24086091285, budget $10.00/day
var NONBRAND = 'Search - US - Non-Brand - AI Abs Preview';  // id 24148587722, budget $5.00/day
var TIER2_ID = '24122099676';       // [DAN] [DGEN] ... geo tier 2 | ALL CONTENT
var TIER2_BUDGET = 5.00;            // Dan's instruction 2026-09-09: $15/day -> $5/day
var MAX_CPC = 2.00;                 // Maximize Clicks bid ceiling
var START_URL = 'https://absbyai.com/start';

// Brand phrase negatives. Measured, not guessed: in the 30 days to 2026-09-09 EVERY
// paid term in this campaign was a generic close variant of [abs by ai] — $155 of them,
// zero real brand searches. Each negative below is checked against the campaign's own
// brand keywords (abs by ai / absbyai / ab by ai / absby ai / absbyai.com): none of
// those queries contain any of these token sequences, so brand traffic is untouched.
var BRAND_NEGATIVES = [
  'ai abs',        // "ai abs" $37.86, "ai abs filter" $5.25
  'abs ai',        // "abs ai" $15.33, "abs ai generator" $28.79
  'ai ab',         // "ai ab" $8.16, "ai ab generator" $24.43
  'ab generator',  // "ab generator ai" $7.47
  'abs generator', // "ai abs generator"
  'abs creator',   // "abs creator ai" $10.37
  'give me abs',   // "give me abs ai" $5.93
  '6 pack',        // "ai 6 pack generator" $11.25
];
// Non-brand wrong-intent negatives. The handoff asked for a bare `fat`; measured, the
// only junk term is "ai to make me fat" ($6.57) and a bare `fat` would also block the
// belly-fat intent family Dan is deliberately building segments around. Tightened.
var NONBRAND_NEGATIVES = ['make me fat', 'get fat', 'gain weight'];

// Task 3d — broaden. The campaign is 75 keywords, almost all EXACT: 53 impressions a
// week is a match-type problem, not a topic problem. These are PHRASE versions of the
// ad group's own strongest exact keywords, plus two genuinely new terms.
var NEW_KEYWORDS = {
  'AI Abs Generator': ['abs generator ai', 'six pack ai generator', 'ai abs maker', 'abs generator app'],
  'Add Abs To Photo': ['add abs to picture', 'put abs on a photo', 'add muscles to photo'],
  'What Would I Look Like With Abs': ['see myself with abs', 'what would i look like ripped', 'what would i look like lean'],
  'AI Body Transformation Preview': ['ai body transformation', 'ai fitness transformation', 'body transformation simulator', 'body transformation ai'],
};

function main() {
  var out = { tag: 'search-repair:' + MODE, mode: MODE, at: new Date().toISOString(), errors: [] };
  try {
    var acct = AdsApp.currentAccount();
    out.account = { id: acct.getCustomerId(), name: acct.getName(), currency: acct.getCurrencyCode(), tz: acct.getTimeZone() };
  } catch (e) { out.errors.push('account: ' + e); }

  out.read = readAll();
  if (MODE === 'APPLY') {
    out.applied = applyAll(out.read);
    out.after = readAll(['campaigns', 'biddingDetail', 'goalConfig', 'campaignGoals',
                         'campaignNegatives', 'keywords', 'ads', 'adRotation']);
  }

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

function readAll(only) {
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
    if (only && only.indexOf(k) === -1) continue;
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
  step('task2:tier2-budget', function () { return setTier2Budget(read); });
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

// Tier 2 is a DEMAND GEN campaign and AdsApp.campaigns() does not return those, so the
// budget is changed on the CampaignBudget resource itself. Guarded: the budget must be
// referenced by exactly this one campaign and must not be explicitly shared, or nothing
// is written (a shared budget would move tier 1 and remarketing too, which is not authorised).
function setTier2Budget() {
  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
  var read = arguments[0] || {};
  var mine = null, users = [];
  (read.campaigns || []).forEach(function (r) {
    var c = r.campaign || {}, b = r.campaignBudget || {};
    if (String(c.id) === TIER2_ID) mine = { budgetId: String(b.id), micros: Number(b.amountMicros), shared: b.explicitlyShared, name: c.name };
  });
  if (!mine) throw new Error('tier-2 campaign ' + TIER2_ID + ' not present in the read');
  (read.campaigns || []).forEach(function (r) {
    if (String((r.campaignBudget || {}).id) === mine.budgetId) users.push((r.campaign || {}).name);
  });
  if (mine.shared === true || users.length > 1) {
    throw new Error('budget ' + mine.budgetId + ' is shared across ' + users.length + ' campaigns (' + users.join(' / ') + ') — NOT changed, per the handoff');
  }
  var want = Math.round(TIER2_BUDGET * 1e6);
  if (mine.micros === want) return { alreadyDone: true, dollars: mine.micros / 1e6 };
  var r = AdsApp.mutate({ campaignBudgetOperation: { update: {
    resourceName: 'customers/' + cid + '/campaignBudgets/' + mine.budgetId,
    amountMicros: want }, updateMask: 'amount_micros' } });
  if (!r.isSuccessful()) throw new Error(r.getErrorMessages().join('; '));
  return { campaign: mine.name, budgetId: mine.budgetId, soleUser: users[0],
           beforeDollars: mine.micros / 1e6, afterDollars: want / 1e6 };
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
    // getText() keeps the match-type decoration: [exact], "phrase", broad. Compare the
    // decorated form, so adding a PHRASE keyword next to an existing EXACT one is allowed.
    var have = {}, ks = g.keywords().get();
    while (ks.hasNext()) { have[String(ks.next().getText()).toLowerCase()] = true; }
    var added = [], skipped = [];
    want.forEach(function (t) {
      if (have['"' + t.toLowerCase() + '"']) { skipped.push(t + ' (phrase already present)'); return; }
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
  var goals = (read.customerGoals || []).slice().sort(function (a, b) {
    var A = a.customerConversionGoal || {}, B = b.customerConversionGoal || {};
    return (A.category === 'SUBMIT_LEAD_FORM' && A.origin === 'WEBSITE' ? -1 : 0) -
           (B.category === 'SUBMIT_LEAD_FORM' && B.origin === 'WEBSITE' ? -1 : 0);
  });
  // Only campaigns still on the ACCOUNT-DEFAULT goals need this. Measured 2026-09-09:
  // the non-brand campaign is already goal_config_level=CAMPAIGN with SUBMIT_LEAD_FORM
  // as its only biddable goal, so it is correct already and is left alone.
  var level = {};
  (read.goalConfig || []).forEach(function (r) {
    var n = (r.campaign || {}).name;
    if (n) level[n] = (r.conversionGoalCampaignConfig || {}).goalConfigLevel;
  });
  var ids = {};
  (read.campaigns || []).forEach(function (r) {
    var c = r.campaign || {};
    if (c.name !== BRAND && c.name !== NONBRAND) return;
    if (level[c.name] === 'CAMPAIGN') { out.push({ campaign: c.name, alreadyCampaignLevel: true, goals: goalsOf(read, c.name) }); return; }
    ids[c.name] = String(c.id);
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

function goalsOf(read, campaignName) {
  var o = [];
  (read.campaignGoals || []).forEach(function (r) {
    if (((r.campaign || {}).name) !== campaignName) return;
    var g = r.campaignConversionGoal || {};
    o.push(g.category + '/' + g.origin + '=' + (g.biddable === true));
  });
  return o;
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
