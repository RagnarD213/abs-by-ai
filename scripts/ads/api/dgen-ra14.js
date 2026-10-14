#!/usr/bin/env node
/**
 * Add RA-14 "The Cheat Code For Six Pack Abs" (9:16) to the TRIAL campaign 24316364155 in its own ad group.
 * Spec: Handoffs/handoff-20261014-ra14-cheat-code-setup.md. Config: dgen-ads/ra14.json.
 *   node scripts/ads/api/dgen-ra14.js            # plan + Google validateOnly dry run
 *   node scripts/ads/api/dgen-ra14.js --apply    # build, read back -> dgen-ads/ra14.result.json
 * One ad group ($40 target CPA, US + CA, English, RA-01's trial Audience), one ad per video, final URL on
 * absbyai.com/start like every ad in the campaign. Copy must pass ytads/lint.js except Dan's own lines.
 * Reads the campaign budget before and after and fails if it moved. Never touches campaign status or budget.
 * Idempotent by name: an existing ad group, asset or ad is reused.
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { lintLine, LIMITS } = require('../ytads/lint.js');
const { rn, GEO, LANG, CID } = ads;
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'dgen-ads', 'ra14.json'), 'utf8'));
const DAN_APPROVED = new Set(['How I Got Abs At 40', 'How AI Got Me Abs']);
const q = (s) => s.replace(/'/g, "\\'");

function checkCopy(copy) {
  const out = [];
  for (const [kind, arr] of [['headline', copy.headlines], ['longHeadline', copy.longHeadlines], ['description', copy.descriptions]])
    for (const t of arr) {
      if (t.length > LIMITS[kind]) out.push(`${kind} over ${LIMITS[kind]} (${t.length}): ${t}`);
      if (/—|–/.test(t)) out.push(`${kind} has a dash: ${t}`);
      if (!DAN_APPROVED.has(t)) { const r = lintLine(t, kind); if (!r.ok) out.push(`${kind} fails lint (${r.reasons.join('; ')}): ${t}`); }
    }
  return out;
}

async function budget() {
  const r = await ads.search(`SELECT campaign.status, campaign_budget.id, campaign_budget.amount_micros FROM campaign WHERE campaign.id = ${cfg.campaignId}`);
  return { status: r[0].campaign.status, budgetId: r[0].campaignBudget.id, perDay: Number(r[0].campaignBudget.amountMicros) / 1e6 };
}

async function main() {
  const apply = process.argv.includes('--apply');
  if (cfg.videos.some(v => !/^[\w-]{11}$/.test(v.youtubeId))) throw new Error('a video has no YouTube id yet (upload first)');
  const bad = checkCopy(cfg.copy);
  if (bad.length) throw new Error('COPY REFUSED:\n  - ' + bad.join('\n  - '));
  const before = await budget();
  const urls = await ads.search(`SELECT ad_group_ad.ad.final_urls FROM ad_group_ad WHERE campaign.id = ${cfg.campaignId} AND ad_group_ad.status != 'REMOVED'`);
  const hosts = new Set(urls.map(r => new URL(r.adGroupAd.ad.finalUrls[0]).host));
  if (hosts.size !== 1 || !hosts.has('absbyai.com')) throw new Error('campaign final URLs are not all absbyai.com: ' + [...hosts]);
  const aud = await ads.search(`SELECT ad_group_criterion.audience.audience FROM ad_group_criterion WHERE ad_group.id = ${cfg.audienceFromAdGroup} AND ad_group_criterion.type = 'AUDIENCE' AND ad_group_criterion.status != 'REMOVED'`);
  if (aud.length !== 1) throw new Error('could not read the RA-01 trial Audience');
  const audience = aud[0].adGroupCriterion.audience.audience;
  const groups = await ads.search(`SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.id = ${cfg.campaignId} AND ad_group.status != 'REMOVED' AND ad_group.name = '${q(cfg.label)}'`);
  const adNames = new Set((await ads.search(`SELECT ad_group_ad.ad.name FROM ad_group_ad WHERE campaign.id = ${cfg.campaignId} AND ad_group_ad.status != 'REMOVED'`)).map(r => r.adGroupAd.ad.name));

  let n = 0; const tmp = (k) => rn.temp(k, ++n); const ops = []; const plan = [];
  let group;
  if (groups.length) { group = rn.adGroup(groups[0].adGroup.id); plan.push(`reuse ad group ${groups[0].adGroup.id} "${cfg.label}"`); }
  else {
    group = tmp('adGroups');
    ops.push({ adGroupOperation: { create: { resourceName: group, name: cfg.label, status: 'ENABLED', campaign: rn.campaign(cfg.campaignId),
      optimizedTargetingEnabled: false, targetCpaMicros: String(cfg.targetCpa * 1e6) } } });
    for (const g of [GEO.US, GEO.CA]) ops.push({ adGroupCriterionOperation: { create: { adGroup: group, location: { geoTargetConstant: rn.geo(g) } } } });
    ops.push({ adGroupCriterionOperation: { create: { adGroup: group, language: { languageConstant: rn.language(LANG.EN) } } } });
    ops.push({ adGroupCriterionOperation: { create: { adGroup: group, audience: { audience } } } });
    plan.push(`create ad group "${cfg.label}" ($${cfg.targetCpa} target CPA, US+CA, English, audience ${audience.split('/').pop()})`);
  }
  for (const v of cfg.videos) {
    const adName = `${cfg.label} | ${v.version} | vsl`;
    if (adNames.has(adName)) { plan.push(`skip ad "${adName}" (exists)`); continue; }
    const a = await ads.search(`SELECT asset.id, asset.resource_name FROM asset WHERE asset.type = 'YOUTUBE_VIDEO' AND asset.youtube_video_asset.youtube_video_id = '${v.youtubeId}'`);
    let assetRn;
    if (a.length) { assetRn = a[0].asset.resourceName; plan.push(`reuse video asset ${a[0].asset.id}`); }
    else {
      assetRn = tmp('assets');
      ops.push({ assetOperation: { create: { resourceName: assetRn, name: `yt ${v.youtubeId} ${cfg.label} ${v.version}`, youtubeVideoAsset: { youtubeVideoId: v.youtubeId } } } });
      plan.push(`create video asset for ${v.youtubeId}`);
    }
    const finalUrl = `https://absbyai.com/start?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-trial-${cfg.key}&utm_content=${v.utm}-vsl`;
    ops.push({ adGroupAdOperation: { create: { adGroup: group, status: 'ENABLED', ad: { name: adName, finalUrls: [finalUrl],
      demandGenVideoResponsiveAd: {
        videos: [{ asset: assetRn }],
        headlines: cfg.copy.headlines.map(text => ({ text })), longHeadlines: cfg.copy.longHeadlines.map(text => ({ text })),
        descriptions: cfg.copy.descriptions.map(text => ({ text })),
        logoImages: [{ asset: `customers/${CID}/assets/${cfg.logoAsset}` }], businessName: { text: cfg.businessName },
        callToActions: [{ asset: `customers/${CID}/assets/${cfg.ctaAsset}` }],
      } } } } });
    plan.push(`create ad "${adName}" -> ${finalUrl}`);
  }
  console.log(`campaign ${cfg.campaignId} ${before.status}, budget ${before.budgetId} $${before.perDay}/day (left as is)`);
  console.log('PLAN\n  ' + plan.join('\n  '));
  if (!ops.length) { console.log('nothing to do'); await ads.close(); return; }
  const note = `dgen-ra14: RA-14 into trial ${cfg.campaignId}`;
  await ads.mutate(ops, { dryRun: true, note });
  console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
  if (!apply) { console.log('pass --apply to build'); await ads.close(); return; }
  const res = await ads.mutate(ops, { note });
  console.log('APPLIED\n  ' + res.results.join('\n  '));
  const after = await budget();
  const back = await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status,
      ad_group_ad.ad.final_urls, ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines,
      ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions,
      ad_group_ad.policy_summary.review_status, ad_group_ad.policy_summary.approval_status
      FROM ad_group_ad WHERE campaign.id = ${cfg.campaignId} AND ad_group.name = '${q(cfg.label)}' AND ad_group_ad.status != 'REMOVED'`);
  const crit = await ads.search(`SELECT ad_group_criterion.type, ad_group_criterion.audience.audience, ad_group_criterion.location.geo_target_constant,
      ad_group_criterion.language.language_constant FROM ad_group_criterion WHERE campaign.id = ${cfg.campaignId} AND ad_group.name = '${q(cfg.label)}' AND ad_group_criterion.status != 'REMOVED'`);
  fs.writeFileSync(path.join(__dirname, 'dgen-ads', 'ra14.result.json'), JSON.stringify({ at: new Date().toISOString(), budgetBefore: before, budgetAfter: after, results: res.results, readBack: back, criteria: crit }, null, 1));
  for (const r of back) console.log(`READ BACK ${r.adGroup.id} ${r.adGroup.name} ${r.adGroup.status} ($${Number(r.adGroup.targetCpaMicros) / 1e6}) | ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary.reviewStatus}/${r.adGroupAd.policySummary.approvalStatus} | ${r.adGroupAd.ad.finalUrls[0]}`);
  console.log(`criteria: ${crit.map(c => c.adGroupCriterion.type).join(', ')}`);
  console.log(`budget after $${after.perDay}/day, status ${after.status}`);
  if (after.perDay !== before.perDay || after.status !== before.status) throw new Error('campaign budget or status moved');
  await ads.close();
}
main().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
