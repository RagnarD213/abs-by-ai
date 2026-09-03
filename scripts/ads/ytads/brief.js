'use strict';
//
// YTADS BRIEF — turns the latest run + recent events into the block the morning
// brief renders ("YouTube engagement ads"). Shared by /api/ytads/state and
// scripts/ads/ads-digest.js so the two surfaces can never disagree.

const { CHAMPION_WINDOW_DAYS, TEST_SPEND_USD, MIN_CONV } = require('./engine.js');
const GOOGLE_CONVERSION_INFLATION = 1.96;   // measured 2026-08-26 (1,553 conversions vs 792 real subscribers); same constant as ads-digest.js
const STALE_HOURS = 3;                       // hourly script; two missed runs is a problem worth a line

const round2 = (n) => Math.round((Number(n) || 0) * 100) / 100;

function buildBrief({ run, events, enabled, now = new Date() }) {
  if (!run) return { ok: false, reason: 'the Google Ads Script has never synced — ytads_runs is empty.' };
  const ageHours = round2((now - new Date(run.at)) / 3600e3);
  const report = run.report || {};
  const since = new Date(now - 24 * 3600e3);
  const recent = (events || []).filter(e => new Date(e.at) >= since);
  const ev = (name) => recent.filter(e => e.event === name);

  const campaigns = {};
  for (const [key, c] of Object.entries(report.campaigns || {})) {
    const ch = c.champion;
    campaigns[key] = {
      name: c.name,
      champion: ch ? {
        adId: ch.adId, name: ch.name, videoId: ch.videoId,
        spend30d: ch.d30.cost, conv30d: ch.d30.conv, costPerConv30d: ch.d30.costPerConv,
        approxCostPerSubscriber30d: ch.d30.costPerConv === null ? null : round2(ch.d30.costPerConv * GOOGLE_CONVERSION_INFLATION),
      } : null,
      testsRunning: (c.tests || []).filter(t => t.phase === 'running').map(t => ({
        adId: t.adId, videoId: t.videoId, spend: t.spend, of: TEST_SPEND_USD, conv: t.conv, daysWaiting: t.daysWaiting, policy: t.policy,
      })),
      verdicts: c.verdicts || [],
      policy: c.policy || [],
      dayOne: c.dayOne || null,
      created: c.created || [],
    };
  }

  return {
    ok: true,
    enabled: !!enabled,
    dryRun: !!run.dry_run,
    lastRunAt: new Date(run.at).toISOString(),
    ageHours,
    stale: ageHours > STALE_HOURS,
    resultsPosted: !!run.results_at,
    thresholds: { testSpendUsd: TEST_SPEND_USD, minConv: MIN_CONV, championWindowDays: CHAMPION_WINDOW_DAYS, conversionInflation: GOOGLE_CONVERSION_INFLATION },
    campaigns,
    warnings: report.warnings || [],
    skipped: report.skipped || [],
    waitingHeadlines: report.waitingHeadlines || [],
    counts: report.counts || {},
    // The review surface: everything that went live since yesterday, WITH its headlines.
    events24h: {
      created:  ev('created').map(e => ({ at: e.at, campaign: e.campaign_key, videoId: e.video_id, adId: e.ad_id, ...(e.detail || {}) })),
      verdicts: ev('verdict').map(e => ({ at: e.at, campaign: e.campaign_key, videoId: e.video_id, adId: e.ad_id, ...(e.detail || {}) })),
      promotes: ev('promote').map(e => ({ at: e.at, campaign: e.campaign_key, videoId: e.video_id, adId: e.ad_id, ...(e.detail || {}) })),
      skips:    ev('skip').map(e => ({ at: e.at, campaign: e.campaign_key, videoId: e.video_id, ...(e.detail || {}) })),
      errors:   ev('error').map(e => ({ at: e.at, campaign: e.campaign_key, videoId: e.video_id, adId: e.ad_id, ...(e.detail || {}) })),
      policy:   ev('policy').map(e => ({ at: e.at, campaign: e.campaign_key, videoId: e.video_id, adId: e.ad_id, ...(e.detail || {}) })),
      dayOne:   ev('dayone').map(e => ({ at: e.at, campaign: e.campaign_key, ...(e.detail || {}) })),
    },
    lastResults: run.results || null,
  };
}

module.exports = { buildBrief, GOOGLE_CONVERSION_INFLATION, STALE_HOURS };
