// ======================================================================
// ABS BY AI — YouTube engagement champion: the HANDS (Google Ads Script)
// ======================================================================
// Installed in Google Ads account 342-717-0837 (Tools → Scripts), scheduled HOURLY.
// This script is deliberately dumb. Every hour it:
//   1. reads every ad in the three Demand Gen campaigns (GAQL) into a snapshot,
//   2. POSTs it to absbyai.com, which decides everything and returns commands,
//   3. executes the commands (create / pause / label) and POSTs the results back.
// The rules live on the server (scripts/ads/ytads/engine.js) where they are unit-tested.
// Change nothing here to change a rule.
//
// If the server answers dryRun:true (YTADS_ENABLED is not 1) every command is logged
// and NOTHING is written to Google Ads. One switch, on the server.
//
// The canonical copy of this file is scripts/ads/ytads/ads-script.js in the repo;
// the pasted copy in Google Ads must match it apart from the KEY line.

var SERVER = 'https://absbyai.com';
var KEY = 'PASTE_YTADS_KEY_HERE';   // = YTADS_KEY on Railway. Never commit a real key.
var SNAPSHOT_VERSION = 1;

function main() {
  var cid = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
  var snapshot = readSnapshot(cid);
  Logger.log('Snapshot: ' + snapshot.campaigns.length + ' campaigns, ' + snapshot.ads.length + ' ads, ' + Object.keys(snapshot.assets).length + ' video assets');

  var plan = post('/api/ytads/sync', snapshot);
  if (!plan || !plan.commands) { Logger.log('No plan from server: ' + JSON.stringify(plan)); return; }
  Logger.log('Run ' + plan.runId + (plan.dryRun ? ' DRY RUN' : ' LIVE') + ': ' + plan.commands.length + ' command(s). ' + JSON.stringify(plan.summary));

  var results = [];
  if (plan.dryRun) {
    for (var i = 0; i < plan.commands.length; i++) {
      Logger.log('DRY ' + describe(plan.commands[i]));
      results.push({ id: plan.commands[i].id, op: plan.commands[i].op, skipped: true, dryRun: true });
    }
  } else {
    var labels = ensureLabels(cid, plan.labels || []);
    for (var j = 0; j < plan.commands.length; j++) {
      var c = plan.commands[j];
      var r;
      try { r = execute(cid, c, labels, snapshot); }
      catch (e) { r = { id: c.id, op: c.op, ok: false, error: String(e && e.message || e) }; }
      Logger.log((r.ok ? 'OK   ' : 'FAIL ') + describe(c) + (r.error ? ' — ' + r.error : '') + (r.resourceName ? ' → ' + r.resourceName : ''));
      results.push(r);
    }
  }
  var ack = post('/api/ytads/results', { runId: plan.runId, results: results });
  Logger.log('Results posted: ' + JSON.stringify(ack));
}

// ----------------------------------------------------------------------
// READ
// ----------------------------------------------------------------------

function readSnapshot(cid) {
  var tz = AdsApp.currentAccount().getTimeZone();
  var today = Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd');
  var DG = "campaign.advertising_channel_type = 'DEMAND_GEN'";

  var campaigns = {};
  var q1 = AdsApp.search("SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros FROM campaign WHERE " + DG + " AND campaign.status != 'REMOVED'");
  while (q1.hasNext()) {
    var r1 = q1.next();
    campaigns[r1.campaign.id] = { id: String(r1.campaign.id), name: r1.campaign.name, status: r1.campaign.status,
      budgetMicros: r1.campaignBudget ? Number(r1.campaignBudget.amountMicros) : null, adGroups: [] };
  }
  var q2 = AdsApp.search("SELECT ad_group.id, ad_group.name, ad_group.status, campaign.id FROM ad_group WHERE " + DG + " AND ad_group.status != 'REMOVED'");
  while (q2.hasNext()) {
    var r2 = q2.next();
    if (campaigns[r2.campaign.id]) campaigns[r2.campaign.id].adGroups.push({ id: String(r2.adGroup.id), name: r2.adGroup.name, status: r2.adGroup.status });
  }

  // Labels: resource name → name (ad_group_ad.labels returns resource names).
  var labelNames = {};
  var q3 = AdsApp.search("SELECT label.id, label.name, label.resource_name FROM label WHERE label.status = 'ENABLED'");
  while (q3.hasNext()) { var r3 = q3.next(); labelNames[r3.label.resourceName] = r3.label.name; }

  // YouTube video assets: resource name → video id (so the brief can name the video).
  var assets = {};
  var q4 = AdsApp.search("SELECT asset.resource_name, asset.youtube_video_asset.youtube_video_id, asset.youtube_video_asset.youtube_video_title FROM asset WHERE asset.type = 'YOUTUBE_VIDEO'");
  while (q4.hasNext()) {
    var r4 = q4.next();
    assets[r4.asset.resourceName] = { videoId: r4.asset.youtubeVideoAsset.youtubeVideoId, title: r4.asset.youtubeVideoAsset.youtubeVideoTitle || null };
  }

  var fields = "campaign.id, ad_group.id, ad_group_ad.resource_name, ad_group_ad.status, ad_group_ad.labels, " +
    "ad_group_ad.policy_summary.approval_status, ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.policy_topic_entries, " +
    "ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.type, ad_group_ad.ad.final_urls, " +
    "ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, " +
    "ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions, ad_group_ad.ad.demand_gen_video_responsive_ad.business_name, " +
    "ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, " +
    "ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions, metrics.cost_micros, metrics.conversions";
  var base = " FROM ad_group_ad WHERE " + DG + " AND ad_group_ad.status != 'REMOVED'";

  var ads = {};
  var q5 = AdsApp.search("SELECT " + fields + base + " AND segments.date BETWEEN '2020-01-01' AND '" + today + "'");
  while (q5.hasNext()) {
    var row = q5.next();
    var a = row.adGroupAd, ad = a.ad, dg = ad.demandGenVideoResponsiveAd || {};
    var texts = function (arr) { var o = []; (arr || []).forEach(function (x) { if (x && x.text) o.push(x.text); }); return o; };
    var assetsOf = function (arr) { var o = []; (arr || []).forEach(function (x) { if (x && x.asset) o.push(x.asset); }); return o; };
    var labs = []; (a.labels || []).forEach(function (rn) { labs.push(labelNames[rn] || rn); });
    var topics = []; ((a.policySummary && a.policySummary.policyTopicEntries) || []).forEach(function (t) { topics.push((t.topic || '?') + ':' + (t.type || '?')); });
    var videoRns = assetsOf(dg.videos);
    ads[a.resourceName] = {
      campaignId: String(row.campaign.id), adGroupId: String(row.adGroup.id), adId: String(ad.id), resourceName: a.resourceName,
      name: ad.name || '', type: ad.type, status: a.status, labels: labs,
      policy: { approvalStatus: a.policySummary ? a.policySummary.approvalStatus : null, reviewStatus: a.policySummary ? a.policySummary.reviewStatus : null, topics: topics },
      lifetime: { costMicros: Number(row.metrics.costMicros || 0), conversions: Number(row.metrics.conversions || 0) },
      d30: { costMicros: 0, conversions: 0 },
      videoId: videoRns.length && assets[videoRns[0]] ? assets[videoRns[0]].videoId : null,
      content: {
        headlines: texts(dg.headlines), longHeadlines: texts(dg.longHeadlines), descriptions: texts(dg.descriptions),
        businessName: dg.businessName ? dg.businessName.text : null, finalUrls: ad.finalUrls || [],
        videos: videoRns, logoImages: assetsOf(dg.logoImages), callToActions: assetsOf(dg.callToActions),
      },
    };
  }
  var q6 = AdsApp.search("SELECT ad_group_ad.resource_name, metrics.cost_micros, metrics.conversions" + base + " AND segments.date DURING LAST_30_DAYS");
  while (q6.hasNext()) {
    var r6 = q6.next();
    var hit = ads[r6.adGroupAd.resourceName];
    if (hit) hit.d30 = { costMicros: Number(r6.metrics.costMicros || 0), conversions: Number(r6.metrics.conversions || 0) };
  }
  // Ads with no spend ever come back from neither metrics query; list them too.
  var q7 = AdsApp.search("SELECT " + fields + base);
  while (q7.hasNext()) {
    var r7 = q7.next();
    if (ads[r7.adGroupAd.resourceName]) continue;
    var a7 = r7.adGroupAd, ad7 = a7.ad, dg7 = ad7.demandGenVideoResponsiveAd || {};
    var t7 = function (arr) { var o = []; (arr || []).forEach(function (x) { if (x && x.text) o.push(x.text); }); return o; };
    var as7 = function (arr) { var o = []; (arr || []).forEach(function (x) { if (x && x.asset) o.push(x.asset); }); return o; };
    var labs7 = []; (a7.labels || []).forEach(function (rn) { labs7.push(labelNames[rn] || rn); });
    var topics7 = []; ((a7.policySummary && a7.policySummary.policyTopicEntries) || []).forEach(function (t) { topics7.push((t.topic || '?') + ':' + (t.type || '?')); });
    var v7 = as7(dg7.videos);
    ads[a7.resourceName] = {
      campaignId: String(r7.campaign.id), adGroupId: String(r7.adGroup.id), adId: String(ad7.id), resourceName: a7.resourceName,
      name: ad7.name || '', type: ad7.type, status: a7.status, labels: labs7,
      policy: { approvalStatus: a7.policySummary ? a7.policySummary.approvalStatus : null, reviewStatus: a7.policySummary ? a7.policySummary.reviewStatus : null, topics: topics7 },
      lifetime: { costMicros: 0, conversions: 0 }, d30: { costMicros: 0, conversions: 0 },
      videoId: v7.length && assets[v7[0]] ? assets[v7[0]].videoId : null,
      content: { headlines: t7(dg7.headlines), longHeadlines: t7(dg7.longHeadlines), descriptions: t7(dg7.descriptions),
        businessName: dg7.businessName ? dg7.businessName.text : null, finalUrls: ad7.finalUrls || [],
        videos: v7, logoImages: as7(dg7.logoImages), callToActions: as7(dg7.callToActions) },
    };
  }

  var campaignList = [], adList = [];
  for (var k in campaigns) campaignList.push(campaigns[k]);
  for (var rn in ads) adList.push(ads[rn]);
  return { version: SNAPSHOT_VERSION, customerId: cid, at: new Date().toISOString(), today: today, timeZone: tz,
           campaigns: campaignList, ads: adList, assets: assets, labels: labelNames };
}

// ----------------------------------------------------------------------
// WRITE
// ----------------------------------------------------------------------

function ensureLabels(cid, names) {
  var byName = {};
  var q = AdsApp.search("SELECT label.id, label.name, label.resource_name FROM label WHERE label.status = 'ENABLED'");
  while (q.hasNext()) { var r = q.next(); byName[r.label.name] = { id: String(r.label.id), resourceName: r.label.resourceName }; }
  for (var i = 0; i < names.length; i++) {
    if (byName[names[i]]) continue;
    var res = AdsApp.mutate({ labelOperation: { create: { name: names[i] } } });
    if (res.isSuccessful()) {
      var rn = res.getResourceName();
      byName[names[i]] = { id: rn.split('/').pop(), resourceName: rn };
      Logger.log('Created label ' + names[i]);
    } else {
      Logger.log('Label create failed ' + names[i] + ': ' + res.getErrorMessages().join('; '));
    }
  }
  return byName;
}

function execute(cid, c, labels, snapshot) {
  var out = { id: c.id, op: c.op, ok: false };
  if (c.op === 'createAd') {
    var videoAsset = findVideoAsset(snapshot, c.videoId) || createVideoAsset(c.videoId);
    if (!videoAsset) { out.error = 'could not create YouTube video asset for ' + c.videoId; return out; }
    var dg = {
      headlines: c.headlines.map(function (t) { return { text: t }; }),
      longHeadlines: c.longHeadlines.map(function (t) { return { text: t }; }),
      descriptions: c.descriptions.map(function (t) { return { text: t }; }),
      businessName: { text: c.businessName },
      videos: [{ asset: videoAsset }],
      logoImages: c.logoImages.map(function (rn) { return { asset: rn }; }),
    };
    if (c.callToActions && c.callToActions.length) dg.callToActions = c.callToActions.map(function (rn) { return { asset: rn }; });
    var op = { adGroupAdOperation: { create: {
      adGroup: 'customers/' + cid + '/adGroups/' + c.adGroupId, status: 'ENABLED',
      ad: { name: c.name, finalUrls: c.finalUrls, demandGenVideoResponsiveAd: dg },
    } } };
    var res = AdsApp.mutate(op);
    if (!res.isSuccessful()) { out.error = res.getErrorMessages().join('; '); return out; }
    out.ok = true; out.resourceName = res.getResourceName();
    out.adId = out.resourceName.split('~').pop();
    out.labelErrors = applyLabels(cid, out.resourceName, c.labels, labels);
    return out;
  }
  if (c.op === 'pauseAd' || c.op === 'enableAd') {
    var st = c.op === 'pauseAd' ? 'PAUSED' : 'ENABLED';
    var r2 = AdsApp.mutate({ adGroupAdOperation: { update: { resourceName: c.resourceName, status: st }, updateMask: 'status' } });
    if (!r2.isSuccessful()) { out.error = r2.getErrorMessages().join('; '); return out; }
    out.ok = true; out.resourceName = c.resourceName;
    out.labelErrors = applyLabels(cid, c.resourceName, c.labels, labels);
    return out;
  }
  if (c.op === 'label') {
    var errs = applyLabels(cid, c.resourceName, c.labels, labels);
    out.ok = errs.length === 0; if (errs.length) out.error = errs.join('; ');
    out.resourceName = c.resourceName;
    return out;
  }
  out.error = 'unknown op ' + c.op;
  return out;
}

// Adds then removes; an "already applied" / "not applied" is not a failure.
function applyLabels(cid, adRn, spec, labels) {
  var errs = [];
  if (!spec) return errs;
  var parts = adRn.split('/').pop().split('~');   // adGroupId~adId
  (spec.add || []).forEach(function (name) {
    var l = labels[name]; if (!l) { errs.push('no label ' + name); return; }
    var r = AdsApp.mutate({ adGroupAdLabelOperation: { create: { adGroupAd: adRn, label: l.resourceName } } });
    if (!r.isSuccessful()) { var m = r.getErrorMessages().join('; '); if (!/already|exist|duplicate/i.test(m)) errs.push('add ' + name + ': ' + m); }
  });
  (spec.remove || []).forEach(function (name) {
    var l = labels[name]; if (!l) return;
    var r = AdsApp.mutate({ adGroupAdLabelOperation: { remove: 'customers/' + cid + '/adGroupAdLabels/' + parts[0] + '~' + parts[1] + '~' + l.id } });
    if (!r.isSuccessful()) { var m2 = r.getErrorMessages().join('; '); if (!/not found|does not exist|NOT_FOUND/i.test(m2)) errs.push('remove ' + name + ': ' + m2); }
  });
  return errs;
}

function findVideoAsset(snapshot, videoId) {
  for (var rn in snapshot.assets) if (snapshot.assets[rn].videoId === videoId) return rn;
  return null;
}

function createVideoAsset(videoId) {
  var r = AdsApp.mutate({ assetOperation: { create: { youtubeVideoAsset: { youtubeVideoId: videoId }, name: 'yt ' + videoId } } });
  if (r.isSuccessful()) return r.getResourceName();
  Logger.log('Video asset create failed for ' + videoId + ': ' + r.getErrorMessages().join('; '));
  return null;
}

// ----------------------------------------------------------------------
// HTTP
// ----------------------------------------------------------------------

function post(path, body) {
  var res = UrlFetchApp.fetch(SERVER + path, {
    method: 'post', contentType: 'application/json', headers: { 'X-YTADS-Key': KEY },
    payload: JSON.stringify(body), muteHttpExceptions: true,
  });
  var code = res.getResponseCode(), text = res.getContentText();
  if (code !== 200) { Logger.log('POST ' + path + ' → ' + code + ': ' + text.slice(0, 500)); return null; }
  try { return JSON.parse(text); } catch (e) { Logger.log('Bad JSON from ' + path + ': ' + text.slice(0, 200)); return null; }
}

function describe(c) {
  var s = c.op + ' [' + c.campaign + '] ' + (c.reason || '') + ' ' + (c.name || c.resourceName || c.adId || '');
  if (c.op === 'createAd') s += ' | ' + (c.headlines || []).join(' / ');
  return s;
}
