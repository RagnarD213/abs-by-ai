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
// GOOGLE IS THE LEDGER. Ad names carry the video id ("AT · <title> · yt:<id> · tier2 ·
// 2026-09-03"), labels carry the state (AUTO, AUTO:TEST, AUTO:CHAMPION, AUTO:RETIRED,
// AUTO:RETIRED-DAY1). "Has this video been tested in this campaign?" is answered by
// the snapshot, never by a file that can drift, so a re-run can never double-create.

// ============================================================
// CONFIG — Dan's decisions (not tunables)
// ============================================================

const TEST_SPEND_USD = 5.00;          // a test is judged once it has spent this much
const MIN_CONV = { tier2: 5, tier1: 2, rmktg: 1 };   // interpretation 2 in the handoff
const CHAMPION_WINDOW_DAYS = 30;      // the champion is judged on its trailing 30 days
// Retry rule (Dan 2026-09-10) — see plan() step 6b.
const RETRY_WAIT_DAYS = 2;            // a LIMITED ad still at $0 after this many days has failed review (measured 2026-09-10: no limited ad in the account has ever spent); DISAPPROVED fails at once
const THUMB_SETTLE_MINUTES = 50;      // after the thumbnail swap, wait this long before attempt 3 so Google reviews the new image
const CAMPAIGN_KEYS = ['tier2', 'tier1', 'rmktg'];

const LABELS = {
  AUTO: 'AUTO', TEST: 'AUTO:TEST', CHAMPION: 'AUTO:CHAMPION',
  RETIRED: 'AUTO:RETIRED', RETIRED_DAY1: 'AUTO:RETIRED-DAY1',
  SUPERSEDED: 'AUTO:SUPERSEDED',   // failed review and replaced by a retry attempt; removed if the whole chain fails
};
const STATE_LABELS = [LABELS.TEST, LABELS.CHAMPION, LABELS.RETIRED, LABELS.RETIRED_DAY1, LABELS.SUPERSEDED];

// How the three campaigns are recognised in the snapshot. All three ids were PINNED
// from the first Ads Script snapshot (run 1, 2026-09-08 20:54 UTC). Name matching is
// gone on purpose: the remarketing campaign's name also contains "geo tier 1", and a
// new campaign someone creates in the account must be ignored (it is reported as
// `unmatched`), never silently adopted. To add a campaign, add its id here and its
// key to CAMPAIGN_KEYS / MIN_CONV.
const DEFAULT_CAMPAIGN_MATCH = [
  { key: 'tier2', id: '24122099676' },  // [DAN] [DGEN] [ENGAGEMENT] MU 18-54 | in-feed & shorts | geo tier 2 | ALL CONTENT — $10/day, ad group 197884856303
  { key: 'tier1', id: '24163535721' },  // [DAN] [DGEN] [ENGAGEMENT] MU 18-54 | in-feed & shorts | geo tier 1 | ALL CONTENT — $15/day, ad group 206274722584
  { key: 'rmktg', id: '24169507109' },  // [DAN] [DGEN] [ENGAGEMENT] [RMKTG] FMU 18-54 | … | geo tier 1 | … | youtube viewers — $5/day, ad group 203082125721
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
const titleOf = (name) => { const m = /^(?:AT|AUTO test) · (.+?) · yt:/.exec(name || ''); return m ? m[1] : null; };
const attemptOf = (name) => { const m = / · r([23]) · /.exec(name || ''); return m ? Number(m[1]) : 1; };   // retry attempt, from the name
const approvalOf = (ad) => String((ad.policy && ad.policy.approvalStatus) || '').toUpperCase();
const videoOfAd = (ad) => videoIdOf(ad.name) || ad.videoId || null;   // hand-made ads carry the video only in the snapshot
const daysSince = (iso, now) => (iso ? Math.max(0, Math.floor((now - new Date(iso)) / 86400e3)) : null);

const hasLabel = (ad, label) => (ad.labels || []).includes(label);
// Name prefixes: "AT · " (Dan's rule 2026-09-09) and the earlier "AUTO test " (ads created 2026-09-08, left as they are).
const AUTO_NAME = /^(AT · |AUTO )/;
const TEST_NAME = /^(AT · |AUTO test )/;
const isAuto = (ad) => hasLabel(ad, LABELS.AUTO) || STATE_LABELS.some(l => hasLabel(ad, l)) || AUTO_NAME.test(ad.name || '');
function stateOf(ad) {
  for (const l of STATE_LABELS) if (hasLabel(ad, l)) return l;
  if (TEST_NAME.test(ad.name || '')) return LABELS.TEST;      // label failed to apply; name still says what it is
  return null;
}
const isEnabled = (ad) => String(ad.status || '').toUpperCase() === 'ENABLED';
const costPerConv = (cost, conv) => (num(conv) > 0 ? round2(cost / conv) : null);
const stats = (block) => ({ cost: usd(block && block.costMicros), conv: round2(num(block && block.conversions)) });

// Google's review of one ad, as the retry rule reads it: 'failed' | 'pending' | 'ok'.
// Disapproved fails at once. Limited fails only while it has spent nothing for
// RETRY_WAIT_DAYS (a limited ad that spends is running — Dan's answer 2026-09-10);
// `forced` (a retry:force event) skips the wait. Anything else in review is pending.
function policyVerdict(ad, ageDays, forced) {
  const a = approvalOf(ad);
  if (a === 'DISAPPROVED') return 'failed';
  if (/LIMITED/.test(a)) {
    if (stats(ad.lifetime).cost > 0) return 'ok';
    return forced || (ageDays !== null && ageDays >= RETRY_WAIT_DAYS) ? 'failed' : 'pending';
  }
  return a === 'APPROVED' ? 'ok' : 'pending';
}

// Ad names are for Dan's eyes in Ads Manager as much as for the ledger: "AT" (Dan's
// prefix, 2026-09-09), the video title, then the machine-readable tail. Parsers key on
// "yt:<id>", the trailing date and the prefix — never on the title (Dan's rule
// 2026-09-08: every automated ad must be identifiable by its video title).
const TITLE_MAX = 70;
function cleanTitle(title) {
  const t = String(title || '').replace(/[·|\u0000-\u001f]/g, ' ').replace(/\s+/g, ' ').trim();
  return t.length > TITLE_MAX ? t.slice(0, TITLE_MAX - 1).trimEnd() + '…' : t;
}
// attempt 2/3 = a retry (" · r2 · " after the id); attempt 1 names are unchanged.
function testAdName(videoId, key, now, title, attempt = 1) {
  const t = cleanTitle(title);
  const r = attempt > 1 ? ` · r${attempt}` : '';
  return t ? `AT · ${t} · yt:${videoId}${r} · ${key} · ${ymd(now)}`
           : `AT · yt:${videoId}${r} · ${key} · ${ymd(now)}`;
}
// An AUTO ad created before titles went into names (format "AUTO test yt:…"). Kept for
// reporting only — such an ad cannot be renamed (see plan()).
const lacksTitle = (ad) => /^AUTO test yt:/.test(ad.name || '');

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
  // Removed ads drop out of the snapshot, so without this the video would look untested and start over.
  if (mine.some(e => e.event === 'retry:failed' && e.campaign_key === key)) return 'retry:failed';
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
// retryCopyByVideo: { [videoId]: set } — the tamer copy for a resubmission (retrycopy events).
function plan({ snapshot, videos, events, headlinesByVideo, retryCopyByVideo, now, config, dryRun }) {
  now = now ? new Date(now) : new Date();
  const { campaigns, unmatched, missing } = resolveCampaigns(snapshot, config);
  const adsBy = groupAdsByCampaign(snapshot, campaigns);
  const commands = []; const warnings = []; const decisions = [];
  let seq = 0;
  const cmd = (c) => { c.id = `c${++seq}`; c.dryRun = !!dryRun; commands.push(c); return c; };

  if (missing.length) warnings.push(`campaign not found in snapshot: ${missing.join(', ')}`);
  if (unmatched.length) warnings.push(`ignored campaigns in snapshot: ${unmatched.map(u => u.name).join(' | ')}`);

  const perCampaign = {};

  // Retry-rule state, rebuilt from the events every hour.
  const retry = { waitingCopy: [], seen: [], thumbnails: [], restore: [], failed: [], actions: [] };
  const seen = {}, forced = new Set(), thumb = {}, retryCopyFailed = new Set(), inPlay = new Set();
  for (const e of (events || [])) {
    if (e.event === 'limited:seen' && e.ad_id && !seen[e.ad_id]) seen[e.ad_id] = e.at;
    else if (e.event === 'retry:force' && e.ad_id) forced.add(String(e.ad_id));
    else if (e.event === 'retrycopy:failed' && e.video_id) retryCopyFailed.add(e.video_id);
    else if (e.event === 'retrycopy' && e.video_id) retryCopyFailed.delete(e.video_id);
    else if (/^thumb:/.test(e.event) && e.video_id) {
      const t = thumb[e.video_id] = thumb[e.video_id] || {};
      if (e.event === 'thumb:swapped') { t.swappedAt = e.at; t.failed = null; }
      else if (e.event === 'thumb:restored') t.restoredAt = e.at;
      else if (e.event === 'thumb:failed' && !(e.detail && e.detail.transient)) t.failed = (e.detail && e.detail.reason) || 'unknown reason';
    }
  }
  const adAge = (ad) => { const d = createdDateOf(ad.name); return d ? daysSince(d + 'T00:00:00Z', now) : (seen[ad.adId] ? daysSince(seen[ad.adId], now) : null); };
  const assetTitles = {}; for (const a of Object.values(snapshot.assets || {})) if (a && a.videoId) assetTitles[a.videoId] = a.title;
  const titleFor = (vid, vads) => ((videos || []).find(v => v.id === vid) || {}).title || vads.map(a => titleOf(a.name)).find(Boolean) || assetTitles[vid] || vid;

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

    // ── 6b. Retry rule (Dan 2026-09-10) ──
    // A disapproved ad, or a limited one still at $0 after RETRY_WAIT_DAYS, is resubmitted:
    // attempt 2 = a new ad with tamer copy; attempt 3 = a clean, text-free thumbnail on the
    // video (done by routes.js between runs), then a fresh ad. If attempt 3 fails too, every
    // ad in the chain is removed and the original thumbnail goes back. An attempt that passes
    // review simply runs on as an ordinary test. Hand-made ads are included (Dan's answer);
    // ones he paused himself are not (only enabled, day-one-retired or disapproved ones).
    {
      const groupsEnabled = (c.adGroups || []).filter(g => String(g.status || '').toUpperCase() === 'ENABLED');
      const verdictOf = (ad) => policyVerdict(ad, adAge(ad), forced.has(String(ad.adId)));
      const createRetry = (attempt, vid, title, set) => {
        if (!set) { warnings.push(`retry: no copy for attempt ${attempt} of "${title}" (yt:${vid}) in ${key}`); return null; }
        if (groupsEnabled.length !== 1) { warnings.push(`${key}: ${groupsEnabled.length} enabled ad groups — retry of yt:${vid} held, ask Dan`); return null; }
        const template = pickTemplate(ads);
        if (!template) { warnings.push(`${key}: no existing ad to copy business name / URL / logo from (retry of yt:${vid})`); return null; }
        const name = testAdName(vid, key, now, title, attempt);
        const made = cmd({
          op: 'createAd', campaign: key, campaignId: c.id, adGroupId: String(groupsEnabled[0].id), videoId: vid, videoTitle: title,
          name, attempt, reason: `retry:${attempt}`, labels: { add: [LABELS.AUTO, LABELS.TEST], remove: [] },
          headlines: set.headlines, longHeadlines: set.longHeadlines, descriptions: set.descriptions,
          businessName: template.businessName, finalUrls: template.finalUrls, logoImages: template.logoImages,
          callToActions: template.callToActions || [], templateAdId: template.adId,
        });
        summary.created.push({ commandId: made.id, videoId: vid, title, name, attempt, headlines: set.headlines });
        return made;
      };
      const supersede = (list) => {
        for (const ad of list) {
          const labels = { add: [LABELS.AUTO, LABELS.SUPERSEDED], remove: [LABELS.TEST, LABELS.CHAMPION] };
          if (isEnabled(ad) && !ad._paused) cmd({ op: 'pauseAd', campaign: key, adId: ad.adId, resourceName: ad.resourceName, videoId: videoOfAd(ad), reason: 'retry:superseded', labels });
          else if (!hasLabel(ad, LABELS.SUPERSEDED)) cmd({ op: 'label', campaign: key, adId: ad.adId, resourceName: ad.resourceName, videoId: videoOfAd(ad), reason: 'retry:superseded', labels });
          ad._paused = true;
        }
      };
      const byVideo = {};
      for (const ad of ads) { const v = videoOfAd(ad); if (v) (byVideo[v] = byVideo[v] || []).push(ad); }
      for (const [vid, vads] of Object.entries(byVideo)) {
        if ((events || []).some(e => e.event === 'retry:failed' && e.video_id === vid && e.campaign_key === key)) continue;
        const a1 = vads.filter(ad => attemptOf(ad.name) === 1), a2 = vads.filter(ad => attemptOf(ad.name) === 2), a3 = vads.filter(ad => attemptOf(ad.name) === 3);
        // A limited hand-made ad carries no creation date: the first hour we see it limited starts its clock.
        for (const ad of a1) if (/LIMITED/.test(approvalOf(ad)) && !createdDateOf(ad.name) && !seen[ad.adId]) retry.seen.push({ adId: ad.adId, campaign: key, videoId: vid });
        const chain1 = a1.filter(ad => hasLabel(ad, LABELS.SUPERSEDED) ||
          (verdictOf(ad) === 'failed' && (isEnabled(ad) || hasLabel(ad, LABELS.RETIRED_DAY1) || approvalOf(ad) === 'DISAPPROVED')));
        const title = titleFor(vid, vads);
        if (!a2.length && !a3.length) {
          // Nothing failed, or the video still runs here on another ad → leave it.
          if (!chain1.length || a1.some(ad => isEnabled(ad) && !ad._paused && verdictOf(ad) !== 'failed')) continue;
          const set = retryCopyByVideo && retryCopyByVideo[vid];
          if (!set) {
            if (retryCopyFailed.has(vid)) warnings.push(`retry: the tamer copy for "${title}" (yt:${vid}) failed the lint — attempt 2 in ${key} is on hold`);
            else if (!retry.waitingCopy.some(w => w.videoId === vid)) retry.waitingCopy.push({ videoId: vid, title, prior: copyOf(chain1[0]), topics: topicsOf(chain1) });
            continue;
          }
          const made = createRetry(2, vid, title, set); if (!made) continue;
          supersede(chain1);
          retry.actions.push({ videoId: vid, title, campaign: key, step: 'attempt2', commandId: made.id, replaces: chain1.map(a => a.adId) });
        } else if (!a3.length) {
          const r2 = newest(a2);
          if (verdictOf(r2) !== 'failed') continue;   // approved → an ordinary test from here on; in review → wait
          inPlay.add(vid);
          const th = thumb[vid] || {};
          if (!th.swappedAt) {
            if (th.failed) warnings.push(`retry: no clean thumbnail could be made for "${title}" (yt:${vid}) — ${th.failed}; attempt 3 in ${key} is on hold`);
            else if (!retry.thumbnails.some(t => t.videoId === vid)) retry.thumbnails.push({ videoId: vid, title });
            continue;
          }
          if ((now - new Date(th.swappedAt)) / 60000 < THUMB_SETTLE_MINUTES) continue;   // let YouTube serve the new thumbnail before Google reviews the ad
          const made = createRetry(3, vid, title, copyOf(r2) || (retryCopyByVideo && retryCopyByVideo[vid])); if (!made) continue;
          supersede([r2]);
          retry.actions.push({ videoId: vid, title, campaign: key, step: 'attempt3', commandId: made.id, replaces: [r2.adId] });
        } else {
          const r3 = newest(a3);
          if (verdictOf(r3) !== 'failed') { inPlay.add(vid); continue; }
          const doomed = [...chain1, ...a2, ...a3];
          for (const ad of doomed) {
            cmd({ op: 'mutate', campaign: key, adId: ad.adId, videoId: vid, reason: 'retry:remove', note: `retry chain failed — removing ${ad.name}`,
                  mutation: { adGroupAdOperation: { remove: ad.resourceName } } });
          }
          retry.failed.push({ videoId: vid, title, campaign: key, removed: doomed.map(ad => ({ adId: ad.adId, name: ad.name })) });
        }
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

  // Retry rule, last step: the clean thumbnail stays only while some attempt 3 is still
  // in play or passed; once every one failed, the original goes back (Dan 2026-09-10).
  for (const [vid, th] of Object.entries(thumb)) {
    if (!th.swappedAt || th.restoredAt || inPlay.has(vid)) continue;
    const failedNow = retry.failed.find(f => f.videoId === vid);
    const failedBefore = (events || []).find(e => e.event === 'retry:failed' && e.video_id === vid && new Date(e.at) >= new Date(th.swappedAt));
    if (failedNow || failedBefore) retry.restore.push({ videoId: vid, title: (failedNow && failedNow.title) || (failedBefore && failedBefore.detail && failedBefore.detail.title) || vid });
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
      const name = testAdName(video.id, key, now, video.title);
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

  // NOTE (measured 2026-09-08 23:38 UTC): Ad.name is IMMUTABLE — Google answers
  // "Field 'name' cannot be modified by 'UPDATE' operation". Legacy-named AUTO ads
  // therefore cannot be renamed; the nine from the first live run were removed by hand
  // (manual queue) and recreated by the next run under titled names. Never emit renames.

  const report = {
    at: now.toISOString(), dryRun: !!dryRun,
    thresholds: { testSpendUsd: TEST_SPEND_USD, minConv: MIN_CONV, championWindowDays: CHAMPION_WINDOW_DAYS, startDate: config.startDate },
    campaigns: perCampaign, skipped, waitingHeadlines, warnings, retry,
    counts: { commands: commands.length, createAd: commands.filter(c => c.op === 'createAd').length,
              pauseAd: commands.filter(c => c.op === 'pauseAd').length, label: commands.filter(c => c.op === 'label').length,
              manual: commands.filter(c => c.op === 'mutate').length },
  };
  return { commands, report };
}

const newest = (list) => list.slice().sort((a, b) => String(createdDateOf(b.name) || '').localeCompare(String(createdDateOf(a.name) || '')) || Number(b.adId) - Number(a.adId))[0];
const copyOf = (ad) => (ad && ad.content && (ad.content.headlines || []).length
  ? { headlines: ad.content.headlines, longHeadlines: ad.content.longHeadlines || [], descriptions: ad.content.descriptions || [] } : null);
const topicsOf = (list) => [...new Set(list.flatMap(ad => (ad.policy && ad.policy.topics) || []))];

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
  plan, candidates, resolveCampaigns, isSkipped, isAuto, stateOf, videoIdOf, createdDateOf, titleOf, attemptOf, policyVerdict, testAdName, cleanTitle, lacksTitle, pickTemplate,
  TEST_SPEND_USD, MIN_CONV, CHAMPION_WINDOW_DAYS, RETRY_WAIT_DAYS, THUMB_SETTLE_MINUTES, CAMPAIGN_KEYS, LABELS, DEFAULT_CAMPAIGN_MATCH, CREATE_ERROR_RETRIES,
};
