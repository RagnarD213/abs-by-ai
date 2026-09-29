'use strict';
//
// YTADS SUNDAY PAUSE (Dan 2026-09-29). Every Sunday at 10 AM Central, in the two engagement
// campaigns geo tier 1 and geo tier 2 (NOT remarketing):
//   - every Short's ad is left exactly as it is (never enabled, never paused);
//   - every ENABLED long-form ad is PAUSED, except the ads for the newest public long-form;
//   - if every ad for the newest long-form in a campaign is paused, the best one is ENABLED
//     (the point is that the newest long-form runs);
//   - if the newest long-form has no approved ad in a campaign yet (in review or disapproved),
//     a second ad for it is created with tamer copy (" · r2 · " in the name), ENABLED.
// Dan re-enables the paused ads by hand on Tuesday. Every ad this pauses carries the Google Ads
// label "Sunday pause" (moved each week), so he can filter to exactly this week's pauses and
// never re-enable one he paused himself. Purpose: every new long-form gets the traffic for
// its first couple of days, so it gets an early read.
//
// This is the ONLY automation that pauses engagement ads. instant.js still only creates.
//
// Server: started from routes.js when YTADS_SUNDAY=1 (Railway abs-by-ai). Ticks every minute;
// runs once per Sunday, any time from 10:00 to 21:59 CT, so a server that was down at 10
// catches up the same day. A 'sunday:run' event per date makes it run once.
// CLI (read-only unless --apply; --apply pauses and labels but writes no tamer copy locally):
//   node scripts/ads/ytads/sunday.js --dry-run
//   node scripts/ads/ytads/sunday.js --apply

const engine = require('./engine.js');
const { fetchVideos } = require('./feed.js');
const { createOp } = require('./instant.js');

const CAMPAIGNS = { tier2: '24122099676', tier1: '24163535721' };
const TZ = 'America/Chicago';
const RUN_HOUR = 10, LAST_HOUR = 21;
const POLL_MS = 60 * 1000;
const LOCK_KEY = 71630929;
const LABEL = 'Sunday pause';
const APPROVED = new Set(['APPROVED', 'APPROVED_LIMITED']);

// Pure: Central-time parts of an instant.
function central(now) {
  const f = new Intl.DateTimeFormat('en-US', { timeZone: TZ, weekday: 'short', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hourCycle: 'h23' });
  const p = Object.fromEntries(f.formatToParts(now).map(x => [x.type, x.value]));
  return { weekday: p.weekday, hour: Number(p.hour), date: `${p.year}-${p.month}-${p.day}` };
}

// Pure: is a run due now? lastDates = Set of dates already run.
function due(now, lastDates) {
  const c = central(now);
  return c.weekday === 'Sun' && c.hour >= RUN_HOUR && c.hour <= LAST_HOUR && !lastDates.has(c.date);
}

// Pure: what to do.
// ads: [{ key, adGroupId, adId, name, status, approval, videoIds }]
// newestLong: { id, title } | null;  kindOf(videoId) → 'short' | 'long' | null (unknown)
function plan({ ads, newestLong, kindOf }) {
  const out = { pause: [], keep: [], enable: [], unknown: [], tame: [], warnings: [] };
  if (!newestLong) { out.warnings.push('no public long-form found in the channel feed: nothing paused'); return out; }
  for (const a of ads) {
    if (a.status !== 'ENABLED') continue;
    const kinds = a.videoIds.map(kindOf);
    if (!a.videoIds.length || kinds.some(k => k !== 'short' && k !== 'long')) { out.unknown.push(a); continue; }
    if (kinds.every(k => k === 'short')) continue;                    // Shorts are never touched
    if (a.videoIds.includes(newestLong.id)) { out.keep.push(a); continue; }
    out.pause.push(a);
  }
  for (const a of out.unknown) out.warnings.push(`${a.key}: ad ${a.adId} "${a.name}" left alone, could not tell Short or long-form`);
  for (const key of Object.keys(CAMPAIGNS)) {
    const mine = ads.filter(a => a.key === key && a.videoIds.includes(newestLong.id));
    if (!mine.length) { out.warnings.push(`${key}: no ad exists for the newest long-form ${newestLong.id} (instant.js should have made one)`); continue; }
    if (!mine.some(a => a.status === 'ENABLED')) {
      const best = [...mine].sort((x, y) => (APPROVED.has(y.approval) - APPROVED.has(x.approval)) || (Number(y.adId) - Number(x.adId)))[0];
      out.enable.push(best);
    }
    if (mine.some(a => APPROVED.has(a.approval))) continue;
    if (mine.some(a => / · r2 · /.test(a.name || ''))) continue;     // tamer copy already made
    out.tame.push({ key, from: [...mine].sort((x, y) => Number(y.adId) - Number(x.adId))[0] });
  }
  return out;
}

// Short or long-form, per video id. The feed knows recent videos; older ones are probed:
// youtube.com/shorts/<id> answers 200 for a Short and redirects for a long-form.
function classifier({ feed, fetchImpl = fetch }) {
  const cache = new Map(feed.map(v => [v.id, v.isShort ? 'short' : 'long']));
  return {
    async load(ids) {
      for (const id of ids) {
        if (cache.has(id)) continue;
        try {
          const r = await fetchImpl(`https://www.youtube.com/shorts/${id}`, { redirect: 'manual' });
          cache.set(id, r.status === 200 ? 'short' : (r.status >= 300 && r.status < 400 ? 'long' : null));
        } catch { cache.set(id, null); }
      }
    },
    kindOf: (id) => cache.get(id) ?? null,
  };
}

async function readAds(ads) {
  const assets = new Map();
  for (const r of await ads.search("SELECT asset.resource_name, asset.youtube_video_asset.youtube_video_id FROM asset WHERE asset.type = 'YOUTUBE_VIDEO'"))
    assets.set(r.asset.resourceName, r.asset.youtubeVideoAsset && r.asset.youtubeVideoAsset.youtubeVideoId);
  const keyOf = Object.fromEntries(Object.entries(CAMPAIGNS).map(([k, v]) => [v, k]));
  const rows = await ads.search(`SELECT campaign.id, ad_group.id, ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.status, ` +
    `ad_group_ad.policy_summary.approval_status, ad_group_ad.ad.final_urls, ad_group_ad.ad.demand_gen_video_responsive_ad.videos, ` +
    `ad_group_ad.ad.demand_gen_video_responsive_ad.business_name, ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ` +
    `ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions, ad_group_ad.ad.demand_gen_video_responsive_ad.headlines, ` +
    `ad_group_ad.ad.demand_gen_video_responsive_ad.long_headlines, ad_group_ad.ad.demand_gen_video_responsive_ad.descriptions ` +
    `FROM ad_group_ad WHERE campaign.id IN (${Object.values(CAMPAIGNS).join(',')}) AND ad_group_ad.status != 'REMOVED'`);
  return rows.map(r => {
    const ad = r.adGroupAd.ad, d = ad.demandGenVideoResponsiveAd || {};
    const videoAssets = (d.videos || []).map(v => v.asset);
    return {
      key: keyOf[String(r.campaign.id)], adGroupId: String(r.adGroup.id), adId: String(ad.id), name: ad.name || '',
      status: r.adGroupAd.status, approval: (r.adGroupAd.policySummary || {}).approvalStatus || null,
      videoAssets, videoIds: videoAssets.map(a => assets.get(a)).filter(Boolean),
      template: { businessName: d.businessName && d.businessName.text, finalUrls: ad.finalUrls || [],
                  logoImages: (d.logoImages || []).map(x => x.asset), callToActions: (d.callToActions || []).map(x => x.asset) },
      prior: { headlines: (d.headlines || []).map(x => x.text), longHeadlines: (d.longHeadlines || []).map(x => x.text), descriptions: (d.descriptions || []).map(x => x.text) },
    };
  });
}

// The "Sunday pause" label: moved off last week's ads, onto this week's.
async function relabel(ads, paused) {
  const cid = ads.CID;
  let label = (await ads.search(`SELECT label.resource_name FROM label WHERE label.name = '${LABEL}'`))[0];
  let labelRn = label && label.label.resourceName;
  if (!labelRn) labelRn = (await ads.mutate([{ labelOperation: { create: { name: LABEL, textLabel: { backgroundColor: '#E8710A', description: 'Paused by the Sunday routine; Dan re-enables on Tuesday' } } } }],
                                            { note: 'sunday: create label', reason: 'ytads-sunday' })).results[0];
  const old = await ads.search(`SELECT ad_group_ad_label.resource_name FROM ad_group_ad_label WHERE label.resource_name = '${labelRn}'`);
  const ops = old.map(r => ({ adGroupAdLabelOperation: { remove: r.adGroupAdLabel.resourceName } }))
    .concat(paused.map(a => ({ adGroupAdLabelOperation: { create: { adGroupAd: `customers/${cid}/adGroupAds/${a.adGroupId}~${a.adId}`, label: labelRn } } })));
  if (ops.length) await ads.mutate(ops, { note: `sunday: label ${paused.length} ad(s) "${LABEL}"`, reason: 'ytads-sunday' });
}

// One run. writeTameCopy(video, prior) → set | null (null: no copy, reported).
async function runOnce({ ads, now = new Date(), apply, writeTameCopy, fetchImpl, log = console.log }) {
  const feed = await fetchVideos();
  const newestLong = feed.filter(v => !v.isShort).sort((a, b) => new Date(b.published) - new Date(a.published))[0] || null;
  const all = await readAds(ads);
  const cls = classifier({ feed, fetchImpl });
  await cls.load([...new Set(all.flatMap(a => a.videoIds))]);
  const p = plan({ ads: all, newestLong, kindOf: cls.kindOf });
  const summary = {
    date: central(now).date, apply: !!apply, newestLong: newestLong && { id: newestLong.id, title: newestLong.title, published: newestLong.published },
    paused: p.pause.map(a => ({ key: a.key, adId: a.adId, name: a.name })), enabled: p.enable.map(a => ({ key: a.key, adId: a.adId, name: a.name })), kept: p.keep.map(a => ({ key: a.key, adId: a.adId, name: a.name, approval: a.approval })),
    tame: [], warnings: p.warnings,
  };
  log(`YTADS sunday ${summary.date}: newest long-form ${newestLong ? `${newestLong.id} "${newestLong.title}"` : 'NONE'}; pause ${p.pause.length}, keep ${p.keep.length}, enable ${p.enable.length}, tamer copy ${p.tame.length}${apply ? '' : ' (dry run)'}`);
  for (const a of p.pause) log(`  pause ${a.key} ${a.adId} ${a.name}`);
  for (const a of p.keep) log(`  keep  ${a.key} ${a.adId} ${a.approval} ${a.name}`);
  for (const a of p.enable) log(`  ENABLE ${a.key} ${a.adId} ${a.approval} ${a.name} (every ad for the newest long-form was paused)`);
  for (const t of p.tame) log(`  tame  ${t.key} from ${t.from.adId} (${t.from.approval})`);
  for (const w of p.warnings) log(`  WARN  ${w}`);
  if (!apply) return summary;

  if (p.pause.length) {
    await ads.mutate(p.pause.map(a => ({ adGroupAdOperation: { update: { resourceName: `customers/${ads.CID}/adGroupAds/${a.adGroupId}~${a.adId}`, status: 'PAUSED' }, updateMask: 'status' } })),
                     { note: `sunday: pause ${p.pause.length} long-form ad(s) except newest ${newestLong.id}`, reason: 'ytads-sunday' });
  }
  if (p.enable.length) {
    await ads.mutate(p.enable.map(a => ({ adGroupAdOperation: { update: { resourceName: `customers/${ads.CID}/adGroupAds/${a.adGroupId}~${a.adId}`, status: 'ENABLED' }, updateMask: 'status' } })),
                     { note: `sunday: enable the newest long-form ${newestLong.id}`, reason: 'ytads-sunday' });
  }
  try { await relabel(ads, p.pause); } catch (e) { summary.warnings.push(`label "${LABEL}" not applied: ${e.message}`); }

  for (const t of p.tame) {
    try {
      const set = writeTameCopy ? await writeTameCopy(newestLong, t.from.prior) : null;
      if (!set) { summary.warnings.push(`${t.key}: no tamer copy written for ${newestLong.id}`); continue; }
      const name = engine.testAdName(newestLong.id, t.key, now, newestLong.title, 2);
      const op = createOp({ cid: ads.CID, adGroupId: t.from.adGroupId, name, set, template: t.from.template, videoAsset: t.from.videoAssets[0], isShort: false });
      const r = await ads.mutate([op], { note: `sunday: tamer copy for ${newestLong.id} → ${t.key}`, reason: 'ytads-sunday' });
      summary.tame.push({ key: t.key, adId: String(r.results[0] || '').split('~').pop(), name, from: t.from.adId });
      log(`  created ${name}`);
    } catch (e) { summary.warnings.push(`${t.key}: tamer copy failed: ${e.message}`); }
  }
  return summary;
}

function start({ pool, db, writeTameCopy, ads = require('../api/client.js') }) {
  let busy = false;
  async function tick() {
    if (busy) return;
    const now = new Date();
    const c = central(now);
    if (c.weekday !== 'Sun' || c.hour < RUN_HOUR || c.hour > LAST_HOUR) return;
    busy = true;
    const lock = await pool.connect().catch(() => null);
    if (!lock) { busy = false; return; }
    let locked = false;
    try {
      locked = (await lock.query('SELECT pg_try_advisory_lock($1) AS ok', [LOCK_KEY])).rows[0].ok;
      if (!locked) return;
      const ran = (await pool.query("SELECT detail->>'date' AS d FROM ytads_events WHERE event = 'sunday:run' AND at > now() - interval '3 days'")).rows.map(r => r.d);
      if (!due(now, new Set(ran))) return;
      const summary = await runOnce({ ads, now, apply: true, writeTameCopy });
      await db.event(summary.newestLong && summary.newestLong.id, null, null, 'sunday:run', summary);
    } catch (e) {
      console.error('YTADS sunday:', e.message);
      await db.event(null, null, null, 'error', { op: 'sunday', error: e.message }).catch(() => {});
    } finally {
      if (locked) await lock.query('SELECT pg_advisory_unlock($1)', [LOCK_KEY]).catch(() => {});
      lock.release();
      busy = false;
    }
  }
  setInterval(tick, POLL_MS).unref?.();
  console.log('YTADS sunday: Sundays 10 AM CT, pause long-form ads except the newest (tier1 + tier2)');
  return { tick };
}

module.exports = { start, runOnce, plan, due, central, classifier, CAMPAIGNS, LABEL };

if (require.main === module) {
  const apply = process.argv.includes('--apply');
  runOnce({ ads: require('../api/client.js'), apply })
    .then(s => { console.log(JSON.stringify({ paused: s.paused.length, tame: s.tame, warnings: s.warnings }, null, 1)); process.exit(0); })
    .catch(e => { console.error(e.message); process.exit(1); });
}
