#!/usr/bin/env node
/**
 * Add a finished ad to the Demand Gen conversion campaign (24243839443) — the Google Ads half of /ad-setup.
 *
 * One ad = one Audience + one ad group per landing page (/start and home) + one ad per video version in each
 * ad group. This is the exact shape Ads 1, 2 and 5 were built in (Docs/DGEN_CONVERSION_CAMPAIGN.md); built as a
 * reusable script on 2026-09-11 for Ads 3 + 4.
 *
 *   node scripts/ads/api/dgen-add-ad.js scripts/ads/api/dgen-ads/ad3.json            # plan + Google dry run
 *   node scripts/ads/api/dgen-add-ad.js scripts/ads/api/dgen-ads/ad3.json --apply    # build, then read back
 *
 * Idempotent: an ad group, audience, video asset or ad that already exists BY NAME is reused, not duplicated —
 * so adding a new version (a vertical) later is the same command with one more entry in `videos`.
 *
 * Config (JSON; anything left out takes DEFAULTS below):
 *   { "adNumber": 3, "label": "Ad 3 Stop Paying Human Trainers",
 *     "videos": [{ "youtubeId": "…", "version": "Muhammad 16:9", "utm": "muhammad-16x9" }],
 *     "audience": { "label": "AI fitness + competitor apps + get abs belly fat", "segments": ["1013657228", …] },
 *     "copy": { "headlines": [5 × ≤40], "longHeadlines": [≤5 × ≤90], "descriptions": [≤5 × ≤90] } }
 *
 * Copy gate: every line must pass scripts/ads/ytads/lint.js, except the lines Dan wrote or approved himself
 * (DAN_APPROVED below — his "How I Got Abs At 40" shape trips the lint's result-promise rule, and he wants it).
 */
const fs = require('fs');
const path = require('path');
const ads = require('./client.js');
const { lintLine, LIMITS } = require('../ytads/lint.js');
const { rn, GEO, LANG, CID } = ads;

const DEFAULTS = {
  campaignId: '24243839443',
  targetCpa: 30,                       // every ad group carries $30 (Dan set it per ad group in the UI, 2026-09-11)
  logoAsset: '400941168572',
  ctaAsset: '401407635767',
  businessName: 'Abs by AI',
  landings: [['/start', 'https://absbyai.com/start', 'start'], ['home', 'https://absbyai.com/', 'home']],
  ages: [25, 54],
  geos: [GEO.US, GEO.CA],
  language: LANG.EN,
};

// Lines Dan wrote or approved verbatim (live ad copy, headline-style.md). Exempt from lint, never from length.
const DAN_APPROVED = new Set([
  'How I Got Abs At 40', 'How AI Got Me Abs', 'How I Got Abs With AI',
  'Fire Your Nutritionist. Use AI Instead', 'Fire Your Personal Trainer',
  'How AI Fixed My Supplements', 'Audit Supplements With AI', 'The Truth About Supplements',
  "Here's how AI fixed my supplements. Find which supplements are a waste of money with AI",
  'Many supplements are a waste of money. AI can identify which supplements you should cut.',
]);

// Lines Google has already refused in this account — never reuse them.
const GOOGLE_REFUSED = new Set([
  'This Picture Got Me Abs', 'Abs At 40 - The Photo That Did It', 'Why My Diets Kept Failing',
]);

function checkCopy(copy) {
  const out = [];
  const kinds = [['headline', copy.headlines, 1, 5], ['longHeadline', copy.longHeadlines, 1, 5], ['description', copy.descriptions, 1, 5]];
  for (const [kind, arr, min, max] of kinds) {
    if (!Array.isArray(arr) || arr.length < min || arr.length > max) { out.push(`${kind}: need ${min}–${max} lines, got ${arr ? arr.length : 0}`); continue; }
    for (const t of arr) {
      if (t.length > LIMITS[kind]) out.push(`${kind} over ${LIMITS[kind]} chars (${t.length}): ${t}`);
      if (GOOGLE_REFUSED.has(t)) out.push(`${kind} already refused by Google in this account: ${t}`);
      if (DAN_APPROVED.has(t)) continue;
      const r = lintLine(t, kind);
      if (!r.ok) out.push(`${kind} fails lint (${r.reasons.join('; ')}): ${t}`);
    }
  }
  return out;
}

const q = (s) => s.replace(/'/g, "\\'");

async function main() {
  const argv = process.argv.slice(2);
  const cfgPath = argv.find(a => !a.startsWith('--'));
  const apply = argv.includes('--apply');
  if (!cfgPath) { console.error('usage: dgen-add-ad.js <config.json> [--apply]'); process.exit(2); }
  const c = { ...DEFAULTS, ...JSON.parse(fs.readFileSync(cfgPath, 'utf8')) };
  for (const k of ['adNumber', 'label', 'videos', 'audience', 'copy'])
    if (c[k] == null) throw new Error(`config is missing "${k}"`);

  const problems = checkCopy(c.copy);
  if (problems.length) { console.error('COPY REFUSED:\n  - ' + problems.join('\n  - ')); process.exit(1); }

  // What already exists (by name) — reuse, never duplicate.
  const camp = Number(c.campaignId);
  const groups = await ads.search(`SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.id = ${camp} AND ad_group.status != 'REMOVED'`);
  const groupByName = Object.fromEntries(groups.map(r => [r.adGroup.name, r.adGroup.id]));
  const adRows = await ads.search(`SELECT ad_group.id, ad_group_ad.ad.name FROM ad_group_ad WHERE campaign.id = ${camp} AND ad_group_ad.status != 'REMOVED'`);
  const adNames = new Set(adRows.map(r => r.adGroupAd.ad.name));
  const assets = await ads.search(`SELECT asset.id, asset.youtube_video_asset.youtube_video_id FROM asset WHERE asset.type = 'YOUTUBE_VIDEO'`);
  const assetByYt = Object.fromEntries(assets.map(r => [r.asset.youtubeVideoAsset.youtubeVideoId, r.asset.id]));
  const audName = `${c.label} | MU ${c.ages[0]}-${c.ages[1]} | ${c.audience.label}`;
  const auds = await ads.search(`SELECT audience.id, audience.name FROM audience WHERE audience.name = '${q(audName)}'`);

  let n = 0; const tmp = (kind) => rn.temp(kind, ++n);
  const ops = []; const plan = [];

  const videoAsset = {};
  for (const v of c.videos) {
    if (assetByYt[v.youtubeId]) { videoAsset[v.youtubeId] = rn.asset ? rn.asset(assetByYt[v.youtubeId]) : `customers/${CID}/assets/${assetByYt[v.youtubeId]}`; plan.push(`reuse video asset ${assetByYt[v.youtubeId]} (${v.youtubeId})`); continue; }
    const r = tmp('assets'); videoAsset[v.youtubeId] = r;
    ops.push({ assetOperation: { create: { resourceName: r, name: `yt ${v.youtubeId} ${c.label} ${v.version}`, youtubeVideoAsset: { youtubeVideoId: v.youtubeId } } } });
    plan.push(`create video asset for ${v.youtubeId} (${v.version})`);
  }

  let audience;
  if (auds.length) { audience = rn.audience(auds[0].audience.id); plan.push(`reuse audience ${auds[0].audience.id} "${audName}"`); }
  else {
    audience = tmp('audiences');
    ops.push({ audienceOperation: { create: { resourceName: audience, name: audName,
      description: `Built ${new Date().toISOString().slice(0, 10)} by dgen-add-ad.js for campaign ${c.campaignId}`,
      dimensions: [
        { age: { ageRanges: [{ minAge: c.ages[0], maxAge: c.ages[1] }], includeUndetermined: true } },
        { gender: { genders: ['MALE'], includeUndetermined: true } },
        { audienceSegments: { segments: c.audience.segments.map(id => ({ customAudience: { customAudience: `customers/${CID}/customAudiences/${id}` } })) } },
      ] } } });
    plan.push(`create audience "${audName}" (segments ${c.audience.segments.join(', ')})`);
  }

  for (const [landingLabel, url, utmTag] of c.landings) {
    const gName = `${c.label} | ${landingLabel}`;
    let group = groupByName[gName] ? rn.adGroup(groupByName[gName]) : null;
    if (group) plan.push(`reuse ad group ${groupByName[gName]} "${gName}"`);
    else {
      group = tmp('adGroups');
      ops.push({ adGroupOperation: { create: { resourceName: group, name: gName, status: 'ENABLED', campaign: rn.campaign(c.campaignId),
        optimizedTargetingEnabled: false, targetCpaMicros: String(Math.round(c.targetCpa * 1e6)) } } });
      for (const g of c.geos) ops.push({ adGroupCriterionOperation: { create: { adGroup: group, location: { geoTargetConstant: rn.geo(g) } } } });
      ops.push({ adGroupCriterionOperation: { create: { adGroup: group, language: { languageConstant: rn.language(c.language) } } } });
      ops.push({ adGroupCriterionOperation: { create: { adGroup: group, audience: { audience } } } });
      plan.push(`create ad group "${gName}" ($${c.targetCpa} target CPA, US+CA, English, the audience)`);
    }
    for (const v of c.videos) {
      const adName = `${c.label} | ${v.version} | ${landingLabel}`;
      if (adNames.has(adName)) { plan.push(`skip ad "${adName}" (exists)`); continue; }
      const finalUrl = `${url}?utm_source=google&utm_medium=video_ad&utm_campaign=dgen-conv-ad${c.adNumber}&utm_content=${v.utm}-${utmTag}`;
      ops.push({ adGroupAdOperation: { create: { adGroup: group, status: 'ENABLED', ad: { name: adName, finalUrls: [finalUrl],
        demandGenVideoResponsiveAd: {
          videos: [{ asset: videoAsset[v.youtubeId] }],
          headlines: c.copy.headlines.map(text => ({ text })),
          longHeadlines: c.copy.longHeadlines.map(text => ({ text })),
          descriptions: c.copy.descriptions.map(text => ({ text })),
          logoImages: [{ asset: `customers/${CID}/assets/${c.logoAsset}` }],
          businessName: { text: c.businessName },
          callToActions: [{ asset: `customers/${CID}/assets/${c.ctaAsset}` }],
        } } } } });
      plan.push(`create ad "${adName}" → ${finalUrl}`);
    }
  }

  console.log('PLAN\n  ' + plan.join('\n  '));
  if (!ops.length) { console.log('\nnothing to do — everything already exists'); await ads.close(); return; }
  const note = `dgen-add-ad: ${c.label} (${c.videos.map(v => v.youtubeId).join(', ')}) into ${c.campaignId}`;
  await ads.mutate(ops, { dryRun: true, note });
  console.log(`\nGoogle dry run OK (${ops.length} operations validated, nothing changed)`);
  if (!apply) { console.log('pass --apply to build'); await ads.close(); return; }

  const res = await ads.mutate(ops, { note });
  console.log(`\nAPPLIED ${res.results.length} operations`);
  // Read back from the account, not the response.
  const back = await ads.search(`SELECT ad_group.id, ad_group.name, ad_group.target_cpa_micros, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status,
      ad_group_ad.ad.final_urls, ad_group_ad.policy_summary.review_status FROM ad_group_ad
      WHERE campaign.id = ${camp} AND ad_group.name LIKE '${q(c.label)} |%' AND ad_group_ad.status != 'REMOVED'`);
  for (const r of back)
    console.log(`  ${r.adGroup.id} ${r.adGroup.name} ($${Number(r.adGroup.targetCpaMicros || 0) / 1e6}) | ad ${r.adGroupAd.ad.id} ${r.adGroupAd.status} ${r.adGroupAd.policySummary.reviewStatus} | ${r.adGroupAd.ad.name}`);
  const out = cfgPath.replace(/\.json$/, '.result.json');
  fs.writeFileSync(out, JSON.stringify({ at: new Date().toISOString(), results: res.results, readBack: back }, null, 1));
  console.log(`\nresult saved: ${path.relative(process.cwd(), out)}`);
  await ads.close();
}

main().catch(async (e) => { console.error('FAILED:', e.message); await ads.close(); process.exit(1); });
