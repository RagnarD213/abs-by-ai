'use strict';
//
// YTADS ENGINE — the brain of the YouTube engagement-champion system.
//
// PURE. (snapshot, videos, events, headlines, now, config) → { commands, report, plan }.
// No I/O, no clock of its own, no randomness: every rule here is driven by
// engine.test.js. The executor (a Google Ads Script, later the Google Ads API)
// is deliberately dumb — it runs the commands and reports back.
//
// Design locked with Dan 2026-09-02:
//   Handoffs/handoff-20260902-google-ads-engagement-champion-automation.md
//   • every new public video (Shorts included) → one Demand Gen video ad in EACH of
//     the three existing campaigns, inside their normal budgets, published at once;
//   • a test runs until it has SPENT $5 (read from Google), then it is paused;
//   • each campaign keeps ONE champion — the lowest cost per conversion — a test
//     that beats the champion's trailing-30-day cost/conv takes the seat;
//   • day one: the best hand-made ad per campaign becomes champion #1, the rest are
//     paused (reversible: the id list is recorded before it is executed);
//   • the system never edits an ad that exists — it creates, pauses, enables, labels.
//
// GOOGLE IS THE LEDGER. Ad names carry the video id ("AUTO test yt:<id> · tier2 ·
// 2026-09-03"), labels carry the state (AUTO, AUTO:TEST, AUTO:CHAMPION, AUTO:RETIRED,
// AUTO:RETIRED-DAY1). "Has this video been tested in this campaign?" is answered by
// the snapshot, never by a file that can drift, so a re-run can never double-create.

// ============================================================
// CONFIG — Dan's decisions (not tunables)
// ============================================================

const TEST_SPEND_USD = 5.00;          // a test is judged once it has spent this much
const MIN_CONV = { tier2: 5, tier1: 2, rmktg: 1 };   // interpretation 2 in the handoff
const CHAMPION_WINDOW_DAYS = 30;      // the champion is judged on its trailing 30 days
const CAMPAIGN_KEYS = ['tier2', 'tier1', 'rmktg'];

const LABELS = {
  AUTO: 'AUTO', TEST: 'AUTO:TEST', CHAMPION: 'AUTO:CHAMPION',
  RETIRED: 'AUTO:RETIRED', RETIRED_DAY1: 'AUTO:RETIRED-DAY1',
};
const STATE_LABELS = [LABELS.TEST, LABELS.CHAMPION, LABELS.RETIRED, LABELS.RETIRED_DAY1];

// How the three campaigns are recognised in the snapshot. The tier-2 id is a
// verified account fact (8/31 handoff); the other two are matched on name until
// Phase 0 pins their ids in config.campaigns.
const DEFAULT_CAMPAIGN_MATCH = [
  { key: 'tier2', id: '24122099676' },
  { key: 'tier1', match: /tier\s*1/i },
  { key: 'rmktg', match: /RMKTG|remarket/i },
];

// ============================================================
// SMALL HELPERS
// ============================================================

const usd = (micros) => Math.round((Number(micros) || 0) / 10000) / 100;
const num = (v) => { const n = Number(v); return Number.isFinite(n) ? n : 0; };
const round2 = (n) => Math.round(n * 100) / 100;
const ymd = (d) => new Date(d).toISOString().slice(0, 10);
const videoIdOf = (name) => { const m = /yt:([A-Za-z0-9_-]{11})/.exec(name || ''); return m ? m[1] : null; };
const createdDateOf = (name) => { const m = /(\d{4}-\d{2}-\d{2})\s*$/.exec(name || ''); return m ? m[1] : null; };

const hasLabel = (ad, label) => (ad.labels || []).includes(label);
const isAuto = (ad) => hasLabel(ad, LABELS.AUTO) || STATE_LABELS.some(l => hasLabel(ad, l)) || /^AUTO /.test(ad.name || '');
function stateOf(ad) {
  for (const l of STATE_LABELS) if (hasLabel(ad, l)) return l;
  if (/^AUTO test /.test(ad.name || '')) return LABELS.TEST;      // label failed to apply; name still says what it is
  return null;
}
const isEnabled = (ad) => String(ad.status || '').toUpperCase() === 'ENABLED';
const costPerConv = (cost, conv) => (num(conv) > 0 ? round2(cost / conv) : null);
const stats = (block) => ({ cost: usd(block && block.costMicros), conv: round2(num(block && block.conversions)) });

function testAdName(videoId, key, now) {
  return `AUTO test yt:${videoId} · ${key} · ${ymd(now)}`;
}

// Resolve which snapshot campaign is which key. Unknown campaigns are ignored and
// reported; a key that matches no campaign is reported as missing.
function resolveCampaigns(snapshot, config) {
  const rules = (config && config.campaigns) || DEFAULT_CAMPAIGN_MATCH;
  const out = {}; const unmatched = [];
  for (const c of (snapshot.campaigns || [])) {
    const rule = rules.find(r => (r.id && String(r.id) === String(c.id)) || (r.match && r.match.test(c.name || '')));
    if (rule && !out[rule.key]) out[rule.key] = { key: rule.key, id: String(c.id), name: c.name, status: c.status, adGroups: c.adGroups || [] };
    else unmatched.push({ id: String(c.id), name: c.name });
  }
  const missing = CAMPAIGN_KEYS.filter(k => !out[k]);
  return { campaigns: out, unmatched, missing };
}

// ============================================================
// SKIP LIST
// ============================================================

function isSkipped(video, skiplist) {
  const ids = (skiplist && skiplist.videoIds) || [];
  if (ids.includes(video.id)) return 'skiplist:id';
  for (const p of ((skiplist && skiplist.titlePatterns) || [])) {
    let re; try { re = new RegExp(p, 'i'); } catch { continue; }
    if (re.test(video.title || '')) return `skiplist:title(${p})`;
  }
  return null;
}

// ============================================================
// CANDIDATES — which (video, campaign) pairs need an ad
// ============================================================

// Videos published on/after startDate, not skipped, that lack an AUTO ad in a
// campaign. A permanent skip event for that pair (lint failure, policy, three
// creation errors) also removes it. Returned per video so headlines can be
// written once and shared by the three campaigns.
function candidates({ snapshot, videos, events, config }) {
  const { campaigns } = resolveCampaigns(snapshot, config);
  const startDate = config.startDate;
  const out = []; const skipped = [];
  const adsByCampaign = groupAdsByCampaign(snapshot, campaigns);
  for (const v of (videos || [])) {
    if (!v.id || !v.published || ymd(v.published) < startDate) continue;
    const skip = isSkipped(v, config.skiplist);
    if (skip) { skipped.push({ videoId: v.id, title: v.title, reason: skip }); continue; }
    const needs = [];
    for (const key of CAMPAIGN_KEYS) {
      const c = campaigns[key]; if (!c) continue;
      const already = adsByCampaign[key].some(ad => isAuto(ad) && videoIdOf(ad.name) === v.id);
      if (already) continue;
      const perm = permanentSkip(events, v.id, key);
      if (perm) { skipped.push({ videoId: v.id, title: v.title, campaign: key, reason: perm }); continue; }
      needs.push(key);
    }
    if (needs.length) out.push({ video: v, campaigns: needs });
  }
  return { candidates: out, skipped };
}

const CREATE_ERROR_RETRIES = 3;

function permanentSkip(events, videoId, key) {
  const mine = (events || []).filter(e => e.video_id === videoId && (e.campaign_key === key || e.campaign_key == null));
  if (mine.some(e => e.event === 'skip' && e.detail && e.detail.permanent)) return 'skip:' + (mine.find(e => e.event === 'skip' && e.detail.permanent).detail.reason || 'permanent');
  if (mine.some(e => e.event === 'policy')) return 'policy:disapproved';
  const errs = mine.filter(e => e.event === 'error' && e.detail && e.detail.op === 'createAd' && e.campaign_key === key).length;
  if (errs >= CREATE_ERROR_RETRIES) return `create-error×${errs}`;
  return null;
}

function groupAdsByCampaign(snapshot, campaigns) {
  const byId = {}; for (const k of Object.keys(campaigns)) byId[campaigns[k].id] = k;
  const out = {}; for (const k of CAMPAIGN_KEYS) out[k] = [];
  for (const ad of (snapshot.ads || [])) {
    const k = byId[String(ad.campaignId)]; if (k) out[k].push(ad);
  }
  return out;
}

// ============================================================
// THE PLAN — one hourly cycle
// ============================================================

// headlinesByVideo: { [videoId]: {headlines, longHeadlines, descriptions} } — only
// videos with a passing set get an ad; the others are reported as waiting.
function plan({ snapshot, videos, events, headlinesByVideo, now, config, dryRun }) {
  now = now ? new Date(now) : new Date();
  const { campaigns, unmatched, missing } = resolveCampaigns(snapshot, config);
  const adsBy = groupAdsByCampaign(snapshot, campaigns);
  const commands = []; const warnings = []; const decisions = [];
  let seq = 0;
  const cmd = (c) => { c.id = `c${++seq}`; c.dryRun = !!dryRun; commands.push(c); return c; };

  if (missing.length) warnings.push(`campaign not found in snapshot: ${missing.join(', ')}`);
  if (unmatched.length) warnings.push(`ignored campaigns in snapshot: ${unmatched.map(u => u.name).join(' | ')}`);

  const perCampaign = {};

  for (const key of CAMPAIGN_KEYS) {
    const c = campaigns[key]; if (!c) continue;
    const ads = adsBy[key];
    const minConv = MIN_CONV[key];
    const summary = { key, id: c.id, name: c.name, champion: null, tests: [], verdicts: [], policy: [], dayOne: null, created: [] };
    perCampaign[key] = summary;

    // ── 6. Policy watch (first: a disapproved champion must not be compared against) ──
    for (const ad of ads) {
      if (!isAuto(ad)) continue;
      const approval = String((ad.policy && ad.policy.approvalStatus) || '').toUpperCase();
      if (approval === 'DISAPPROVED' && isEnabled(ad)) {
        cmd({ op: 'pauseAd', campaign: key, adId: ad.adId, resourceName: ad.resourceName, videoId: videoIdOf(ad.name),
              reason: 'policy:disapproved', topics: (ad.policy && ad.policy.topics) || [],
              labels: { add: [LABELS.RETIRED], remove: [LABELS.TEST, LABELS.CHAMPION] } });
        summary.policy.push({ adId: ad.adId, name: ad.name, topics: (ad.policy && ad.policy.topics) || [] });
        ad._paused = true;
      } else if (/LIMITED/i.test(approval) || /LIMITED/i.test(String(ad.policy && ad.policy.reviewStatus || ''))) {
        summary.policy.push({ adId: ad.adId, name: ad.name, limited: true, topics: (ad.policy && ad.policy.topics) || [] });
      }
    }

    // ── current champion ──
    let champion = ads.find(ad => stateOf(ad) === LABELS.CHAMPION && !ad._paused) || null;
    const champStats = (ch) => {
      if (!ch) return null;
      const d30 = stats(ch.d30), life = stats(ch.lifetime);
      return { adId: ch.adId, name: ch.name, videoId: videoIdOf(ch.name) || ch.videoId || null, status: ch.status,
               d30: { ...d30, costPerConv: costPerConv(d30.cost, d30.conv) },
               lifetime: { ...life, costPerConv: costPerConv(life.cost, life.conv) } };
    };

    // ── 7. Day-one pass (once per campaign) ──
    const dayOneDone = (events || []).some(e => e.event === 'dayone' && e.campaign_key === key && !(e.detail && e.detail.dryRun));
    const handMade = ads.filter(ad => !isAuto(ad) && isEnabled(ad));
    // testWins: called from the promote path — the winning TEST is the champion, so
    // every enabled hand-made ad is paused (interpretation 6). Otherwise the best
    // hand-made ad is picked, and with no qualifier nothing is paused.
    const runDayOne = (reason, testWins = false) => {
      const qualifiers = testWins ? [] : handMade
        .map(ad => ({ ad, life: stats(ad.lifetime) }))
        .filter(x => x.life.cost >= TEST_SPEND_USD && x.life.conv >= minConv)
        .map(x => ({ ...x, cpc: costPerConv(x.life.cost, x.life.conv) }))
        .sort((a, b) => a.cpc - b.cpc);
      const pick = qualifiers[0] ? qualifiers[0].ad : null;
      const toPause = testWins ? handMade : (pick ? handMade.filter(ad => ad !== pick) : []);
      const list = toPause.map(ad => ({ adId: ad.adId, resourceName: ad.resourceName, name: ad.name, lifetime: stats(ad.lifetime) }));
      summary.dayOne = { reason, champion: pick ? { adId: pick.adId, name: pick.name, lifetime: stats(pick.lifetime), costPerConv: qualifiers[0].cpc } : null,
                         paused: list, reversal: list.map(a => ({ op: 'enableAd', adId: a.adId, resourceName: a.resourceName })) };
      if (pick) {
        cmd({ op: 'label', campaign: key, adId: pick.adId, resourceName: pick.resourceName, reason: 'dayone:champion',
              labels: { add: [LABELS.AUTO, LABELS.CHAMPION], remove: [] } });
      }
      for (const ad of toPause) {
        cmd({ op: 'pauseAd', campaign: key, adId: ad.adId, resourceName: ad.resourceName, reason: 'dayone:retire',
              labels: { add: [LABELS.AUTO, LABELS.RETIRED_DAY1], remove: [] } });
      }
      return pick;
    };
    if (!champion && !dayOneDone) {
      const pick = runDayOne('no champion yet');
      if (pick) champion = { ...pick, labels: [...(pick.labels || []), LABELS.AUTO, LABELS.CHAMPION] };
      else summary.dayOne.deferred = `no hand-made ad has ≥$${TEST_SPEND_USD.toFixed(2)} spend and ≥${minConv} conversions; the first qualifying test becomes champion and the hand-made ads are paused then`;
    }

    // ── 5. Judge finished tests ──
    // Oldest first so several tests finishing in the same hour are compared in
    // creation order, each against the champion the previous one may have crowned.
    const tests = ads.filter(ad => stateOf(ad) === LABELS.TEST && !ad._paused)
      .sort((a, b) => String(createdDateOf(a.name) || '').localeCompare(String(createdDateOf(b.name) || '')));
    for (const t of tests) {
      const life = stats(t.lifetime);
      const created = createdDateOf(t.name);
      const daysWaiting = created ? Math.max(0, Math.floor((now - new Date(created + 'T00:00:00Z')) / 86400e3)) : null;
      const row = { adId: t.adId, name: t.name, videoId: videoIdOf(t.name), status: t.status, spend: life.cost, conv: life.conv,
                    costPerConv: costPerConv(life.cost, life.conv), created, daysWaiting,
                    policy: (t.policy && t.policy.approvalStatus) || null };
      if (!isEnabled(t)) { row.note = 'not enabled'; summary.tests.push(row); continue; }
      if (life.cost < TEST_SPEND_USD) { row.phase = 'running'; summary.tests.push(row); continue; }

      // Reached $5 — verdict.
      const champ = champStats(champion);
      let verdict, detail;
      if (life.conv < minConv) {
        verdict = 'no-read';
        detail = `${life.conv} conversions at $${life.cost.toFixed(2)} — under the ${minConv} needed in ${key}`;
      } else {
        const champCpc = champ && champ.d30.conv > 0 ? champ.d30.costPerConv : null;
        const testCpc = row.costPerConv;
        if (!champ) { verdict = 'win'; detail = `no champion in ${key} — $${testCpc} per conversion takes the seat`; }
        else if (champCpc === null) { verdict = 'win'; detail = `champion has 0 conversions in the last ${CHAMPION_WINDOW_DAYS} days — $${testCpc} per conversion takes the seat`; }
        else if (testCpc < champCpc) { verdict = 'win'; detail = `$${testCpc} per conversion beats the champion's $${champCpc} (${CHAMPION_WINDOW_DAYS}d)`; }
        else { verdict = 'lose'; detail = `$${testCpc} per conversion does not beat the champion's $${champCpc} (${CHAMPION_WINDOW_DAYS}d)`; }
      }
      row.phase = 'judged'; row.verdict = verdict; row.detail = detail;
      summary.verdicts.push({ ...row, champion: champ });
      summary.tests.push(row);

      if (verdict === 'win') {
        // Interpretation 6: the first qualifying test in a campaign that never had a
        // champion triggers the day-one pause of the hand-made ads at that moment.
        if (!champion && !dayOneDone && !(summary.dayOne && summary.dayOne.paused.length)) runDayOne('first qualifying test', true);
        cmd({ op: 'label', campaign: key, adId: t.adId, resourceName: t.resourceName, videoId: row.videoId, reason: 'promote',
              labels: { add: [LABELS.CHAMPION], remove: [LABELS.TEST] }, verdict: detail });
        if (champion) {
          cmd({ op: 'pauseAd', campaign: key, adId: champion.adId, resourceName: champion.resourceName, videoId: videoIdOf(champion.name),
                reason: 'dethroned', labels: { add: [LABELS.RETIRED], remove: [LABELS.CHAMPION] } });
        }
        champion = { ...t, labels: [...(t.labels || []).filter(l => l !== LABELS.TEST), LABELS.CHAMPION] };
      } else {
        cmd({ op: 'pauseAd', campaign: key, adId: t.adId, resourceName: t.resourceName, videoId: row.videoId,
              reason: `verdict:${verdict}`, labels: { add: [LABELS.RETIRED], remove: [LABELS.TEST] }, verdict: detail });
      }
    }
    summary.champion = champStats(champion);

    // Interpretation-6 pause deferred: with no champion and no day-one, the hand-made ads keep running.
  }

  // ── 2–4. New videos → new ads ──
  const { candidates: cands, skipped } = candidates({ snapshot, videos, events, config });
  const waitingHeadlines = [];
  for (const { video, campaigns: keys } of cands) {
    const set = headlinesByVideo && headlinesByVideo[video.id];
    if (!set) { waitingHeadlines.push({ videoId: video.id, title: video.title }); continue; }
    for (const key of keys) {
      const c = campaigns[key]; const summary = perCampaign[key];
      const groups = (c.adGroups || []).filter(g => String(g.status || '').toUpperCase() === 'ENABLED');
      if (groups.length !== 1) {
        warnings.push(`${key}: ${groups.length} enabled ad groups — cannot pick one, ask Dan (${groups.map(g => g.name).join(' | ') || 'none'})`);
        continue;
      }
      const template = pickTemplate(adsBy[key]);
      if (!template) { warnings.push(`${key}: no existing ad to copy business name / URL / logo from`); continue; }
      const name = testAdName(video.id, key, now);
      const created = cmd({
        op: 'createAd', campaign: key, campaignId: c.id, adGroupId: String(groups[0].id), videoId: video.id, videoTitle: video.title,
        name, labels: { add: [LABELS.AUTO, LABELS.TEST], remove: [] },
        headlines: set.headlines, longHeadlines: set.longHeadlines, descriptions: set.descriptions,
        businessName: template.businessName, finalUrls: template.finalUrls, logoImages: template.logoImages,
        callToActions: template.callToActions || [], templateAdId: template.adId,
      });
      summary.created.push({ commandId: created.id, videoId: video.id, title: video.title, name, headlines: set.headlines,
                             longHeadlines: set.longHeadlines, descriptions: set.descriptions });
    }
  }

  const report = {
    at: now.toISOString(), dryRun: !!dryRun,
    thresholds: { testSpendUsd: TEST_SPEND_USD, minConv: MIN_CONV, championWindowDays: CHAMPION_WINDOW_DAYS, startDate: config.startDate },
    campaigns: perCampaign, skipped, waitingHeadlines, warnings,
    counts: { commands: commands.length, createAd: commands.filter(c => c.op === 'createAd').length,
              pauseAd: commands.filter(c => c.op === 'pauseAd').length, label: commands.filter(c => c.op === 'label').length },
  };
  return { commands, report };
}

// The ad whose required fields a new test copies. The champion first (it is the
// proven one), else the most-spent enabled hand-made ad with content.
function pickTemplate(ads) {
  const withContent = ads.filter(ad => ad.content && ad.content.businessName && (ad.content.finalUrls || []).length && (ad.content.logoImages || []).length);
  if (!withContent.length) return null;
  const champ = withContent.find(ad => stateOf(ad) === LABELS.CHAMPION);
  const pick = champ || withContent.filter(isEnabled).sort((a, b) => num(b.lifetime && b.lifetime.costMicros) - num(a.lifetime && a.lifetime.costMicros))[0] || withContent[0];
  return { adId: pick.adId, businessName: pick.content.businessName, finalUrls: pick.content.finalUrls,
           logoImages: pick.content.logoImages, callToActions: pick.content.callToActions || [] };
}

module.exports = {
  plan, candidates, resolveCampaigns, isSkipped, isAuto, stateOf, videoIdOf, createdDateOf, testAdName, pickTemplate,
  TEST_SPEND_USD, MIN_CONV, CHAMPION_WINDOW_DAYS, CAMPAIGN_KEYS, LABELS, DEFAULT_CAMPAIGN_MATCH, CREATE_ERROR_RETRIES,
};
