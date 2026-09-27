'use strict';
//
// YTADS INSTANT: a new public video gets an ENABLED ad in each of the three engagement
// campaigns within about a minute of going live (Dan 2026-09-27). Replaces the hourly
// Ads Script, which is disabled. This path NEVER pauses, enables or removes an existing
// ad: Dan does all pausing by hand. It only creates.
//
// Runs inside the web server: every POLL_MS it reads the channel's RSS feed (cheap, no
// quota). Only when a recent video is not yet known to have all three ads does it call
// the Google Ads API (scripts/ads/api/client.js), so API use stays a few calls a day.
// A Postgres advisory lock keeps two containers (a deploy overlap) from double-creating.
// Switch: YTADS_INSTANT=1 on Railway service abs-by-ai.

const engine = require('./engine.js');
const { fetchVideos } = require('./feed.js');

// The three engagement campaigns (ids measured 2026-09-27). Each has exactly one enabled ad group.
const CAMPAIGNS = { tier2: '24122099676', tier1: '24163535721', rmktg: '24169507109' };
const POLL_MS = 60 * 1000;
const LOOKBACK_HOURS = 72;          // only videos this new are ever considered; older ones are history
const RETRY_AFTER_MS = 5 * 60 * 1000;
const MAX_FAILURES = 12;            // per video, then it is left alone and reported
const LOCK_KEY = 71630927;          // pg advisory lock id for this job

const IN_FEED_ONLY = { inFeedPreference: true, inStreamPreference: false, shortsPreference: false };

// Pure: which (video, campaign) pairs still need an ad.
// videos: feed rows; existing: Set of `${key}:${videoId}` that already have an ad in any status.
function missing({ videos, existing, now, startDate, skiplist }) {
  const out = [];
  const floor = Math.max(new Date(startDate).getTime(), now.getTime() - LOOKBACK_HOURS * 3600e3);
  for (const v of videos) {
    const t = new Date(v.published).getTime();
    if (!(t >= floor)) continue;
    if (engine.isSkipped(v, skiplist)) continue;
    const keys = Object.keys(CAMPAIGNS).filter(k => !existing.has(`${k}:${v.id}`));
    if (keys.length) out.push({ video: v, keys });
  }
  return out;
}

// Pure: the create operation for one campaign.
function createOp({ cid, adGroupId, name, set, template, videoAsset, isShort }) {
  const video = { asset: videoAsset };
  // Dan 2026-09-13: long-form runs in-feed only; Shorts keep the default (no preference).
  if (!isShort) video.adVideoAssetInfo = { adVideoAssetInventoryPreferences: IN_FEED_ONLY };
  const dg = {
    headlines: set.headlines.map(text => ({ text })),
    longHeadlines: set.longHeadlines.map(text => ({ text })),
    descriptions: set.descriptions.map(text => ({ text })),
    businessName: { text: template.businessName },
    videos: [video],
    logoImages: template.logoImages.map(asset => ({ asset })),
  };
  if (template.callToActions.length) dg.callToActions = template.callToActions.map(asset => ({ asset }));
  return { adGroupAdOperation: { create: {
    adGroup: `customers/${cid}/adGroups/${adGroupId}`, status: 'ENABLED',
    ad: { name, finalUrls: template.finalUrls, demandGenVideoResponsiveAd: dg },
  } } };
}

function start({ pool, db, writeHeadlinesFor, config, ads = require('../api/client.js') }) {
  const done = new Set();           // `${key}:${videoId}` confirmed to have an ad
  const failures = new Map();       // videoId → { n, last }
  let busy = false;
  const campaignIds = Object.values(CAMPAIGNS).join(',');

  async function existingAds(videoIds) {
    const like = videoIds.map(id => `ad_group_ad.ad.name LIKE '%yt:${id}%'`);
    const found = new Set();
    // GAQL has no OR; one query per video (only ever a handful).
    for (let i = 0; i < videoIds.length; i++) {
      const rows = await ads.search(`SELECT campaign.id, ad_group_ad.ad.name FROM ad_group_ad WHERE campaign.id IN (${campaignIds}) AND ${like[i]}`);
      for (const r of rows) {
        const key = Object.keys(CAMPAIGNS).find(k => CAMPAIGNS[k] === String(r.campaign.id));
        if (key) found.add(`${key}:${videoIds[i]}`);
      }
    }
    return found;
  }

  async function templateFor(key) {
    const rows = await ads.search(`SELECT ad_group.id, ad_group.status, ad_group_ad.ad.id, ad_group_ad.ad.final_urls, ` +
      `ad_group_ad.ad.demand_gen_video_responsive_ad.business_name, ad_group_ad.ad.demand_gen_video_responsive_ad.logo_images, ` +
      `ad_group_ad.ad.demand_gen_video_responsive_ad.call_to_actions FROM ad_group_ad WHERE campaign.id = ${CAMPAIGNS[key]} ` +
      `AND ad_group_ad.status != 'REMOVED' AND ad_group.status = 'ENABLED' AND ad_group_ad.ad.type = 'DEMAND_GEN_VIDEO_RESPONSIVE_AD'`);
    const usable = rows.map(r => ({ adGroupId: String(r.adGroup.id), ad: r.adGroupAd.ad }))
      .filter(x => { const d = x.ad.demandGenVideoResponsiveAd || {}; return d.businessName && (d.logoImages || []).length && (x.ad.finalUrls || []).length; })
      .sort((a, b) => Number(b.ad.id) - Number(a.ad.id));
    const groups = [...new Set(usable.map(x => x.adGroupId))];
    if (!usable.length) throw new Error(`${key}: no existing ad to copy business name / URL / logo from`);
    if (groups.length !== 1) throw new Error(`${key}: ${groups.length} enabled ad groups, cannot pick one`);
    const d = usable[0].ad.demandGenVideoResponsiveAd;
    return { adGroupId: groups[0], templateAdId: usable[0].ad.id, businessName: d.businessName.text, finalUrls: usable[0].ad.finalUrls,
             logoImages: d.logoImages.map(x => x.asset), callToActions: (d.callToActions || []).map(x => x.asset) };
  }

  async function videoAssetFor(videoId) {
    const rows = await ads.search(`SELECT asset.resource_name FROM asset WHERE asset.type = 'YOUTUBE_VIDEO' AND asset.youtube_video_asset.youtube_video_id = '${videoId}'`);
    if (rows.length) return rows[0].asset.resourceName;
    const r = await ads.mutate([{ assetOperation: { create: { youtubeVideoAsset: { youtubeVideoId: videoId }, name: 'yt ' + videoId } } }],
                               { note: `instant: video asset for ${videoId}`, reason: 'ytads-instant' });
    return r.results[0];
  }

  async function headlinesFor(video) {
    const rows = (await pool.query("SELECT event, detail FROM ytads_events WHERE video_id = $1 AND event IN ('headlines','skip') ORDER BY at", [video.id])).rows;
    const last = rows.filter(r => r.event === 'headlines' && r.detail && r.detail.set).pop();
    if (last) return last.detail.set;
    if (rows.some(r => r.event === 'skip' && r.detail && r.detail.permanent)) return null;
    return writeHeadlinesFor(video);
  }

  async function tick() {
    if (busy) return;
    busy = true;
    const lock = await pool.connect().catch(() => null);
    if (!lock) { busy = false; return; }
    let locked = false;
    try {
      locked = (await lock.query('SELECT pg_try_advisory_lock($1) AS ok', [LOCK_KEY])).rows[0].ok;
      if (!locked) return;
      const cfg = config();
      const now = new Date();
      const videos = await fetchVideos();
      let todo = missing({ videos, existing: done, now, startDate: cfg.startDate, skiplist: cfg.skiplist })
        .filter(({ video }) => { const f = failures.get(video.id); return !f || (f.n < MAX_FAILURES && now - f.last >= RETRY_AFTER_MS); });
      if (!todo.length) return;
      // Ask Google once what already exists (any status, removed included: never recreate).
      const have = await existingAds(todo.map(t => t.video.id));
      for (const k of have) done.add(k);
      todo = missing({ videos: todo.map(t => t.video), existing: done, now, startDate: cfg.startDate, skiplist: cfg.skiplist });
      for (const { video, keys } of todo) {
        try {
          const set = await headlinesFor(video);
          if (!set) { for (const k of keys) done.add(`${k}:${video.id}`); console.log(`YTADS instant: ${video.id} has no usable headlines (lint skip), no ad`); continue; }
          const asset = await videoAssetFor(video.id);
          for (const key of keys) {
            const tpl = await templateFor(key);
            const name = engine.testAdName(video.id, key, now, video.title);
            const op = createOp({ cid: ads.CID, adGroupId: tpl.adGroupId, name, set, template: tpl, videoAsset: asset, isShort: !!video.isShort });
            const r = await ads.mutate([op], { note: `instant: new video ${video.id} → ${key}`, reason: 'ytads-instant' });
            const adId = String(r.results[0] || '').split('~').pop();
            done.add(`${key}:${video.id}`);
            await db.event(video.id, key, adId, 'created', { name, attempt: 1, via: 'instant', status: 'ENABLED', inFeedOnly: !video.isShort,
              templateAdId: tpl.templateAdId, headlines: set.headlines, longHeadlines: set.longHeadlines, descriptions: set.descriptions });
            console.log(`YTADS instant: created ${name} (${adId})`);
          }
          failures.delete(video.id);
        } catch (e) {
          const f = failures.get(video.id) || { n: 0, last: 0 };
          f.n++; f.last = Date.now(); failures.set(video.id, f);
          console.error(`YTADS instant: ${video.id} failed (${f.n}/${MAX_FAILURES}):`, e.message);
          await db.event(video.id, null, null, 'error', { op: 'instantCreate', title: video.title, attempt: f.n, error: e.message }).catch(() => {});
        }
      }
    } catch (e) {
      console.error('YTADS instant tick:', e.message);
    } finally {
      if (locked) await lock.query('SELECT pg_advisory_unlock($1)', [LOCK_KEY]).catch(() => {});
      lock.release();
      busy = false;
    }
  }

  setTimeout(tick, 20 * 1000).unref?.();
  setInterval(tick, POLL_MS).unref?.();
  console.log('YTADS instant: watching the channel feed every minute (create only, never pause)');
  return { tick };
}

module.exports = { start, missing, createOp, CAMPAIGNS, LOOKBACK_HOURS };
