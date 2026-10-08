'use strict';
// A brief is structured text, never executable HTML or a raw source dump.
const STATUS = new Set(['ok', 'missing', 'stale', 'error', 'partial', 'unverified', 'not_checked', 'not_applicable']);
const CHECK = new Set(['verified', 'missing', 'unverified', 'not_applicable', 'broken', 'duplicate', 'mismatch']);
function text(value, limit = 500) {
  if (typeof value !== 'string' || value.length > limit || /[\u0000-\u0008]/.test(value)) throw new Error('Invalid text');
  return value;
}
function date(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d\d-\d\d$/.test(value) || new Date(value).toISOString().slice(0, 10) !== value) throw new Error('Invalid date');
  return value;
}
function instant(value) {
  if (typeof value !== 'string' || !/(?:Z|[+-]\d\d:\d\d)$/.test(value) || !Number.isFinite(Date.parse(value))) throw new Error('Invalid timestamp');
  return value;
}
function status(value, allowed = STATUS) { if (!allowed.has(value)) throw new Error('Invalid status'); return value; }
function count(value) { if (value === null) return null; if (!Number.isFinite(value) || value < 0) throw new Error('Invalid count'); return value; }
function list(value, max) { if (!Array.isArray(value) || value.length > max) throw new Error('Invalid list'); return value; }
function link(value) {
  if (!value) return null;
  const url = new URL(text(value, 2000));
  if (url.protocol !== 'https:' || url.username || url.password) throw new Error('Invalid link');
  return url.href;
}
function validate(input, now = Date.now()) {
  if (!input || input.schemaVersion !== 1 || typeof input.routineEnabled !== 'boolean' || input.timezone !== 'America/Chicago') throw new Error('Invalid edition');
  const generatedAt = instant(input.generatedAt), forDate = date(input.forDate);
  if (Date.parse(generatedAt) > now + 300000 || !['manual', 'retrospective', 'daily'].includes(input.editionType)) throw new Error('Invalid edition time/type');
  let routine = null;
  if (input.routine != null) {
    const r = input.routine, clock = /^(?:[01]\d|2[0-3]):[0-5]\d$/;
    if (r.kind !== 'cloud' || !clock.test(r.startTime) || !clock.test(r.readyBy) || r.startTime >= r.readyBy || r.localCron !== false || r.notifications !== false) throw new Error('Invalid external schedule');
    routine = {kind:'cloud', startTime:r.startTime, readyBy:r.readyBy, startsOn:date(r.startsOn), confirmedAt:instant(r.confirmedAt), localCron:false, notifications:false};
    if (Date.parse(routine.confirmedAt) > now + 300000) throw new Error('Unconfirmed future schedule');
  }
  if (input.routineEnabled && !routine) throw new Error('Enabled routine requires external schedule evidence');
  const f = input.focus;
  if (!f || !['current', 'missing', 'stale'].includes(f.status)) throw new Error('Invalid focus');
  const focus = {status: f.status, task: text(f.task, 250), why: text(f.why, 650), source: text(f.source, 100),
    statedAt: f.statedAt ? instant(f.statedAt) : null, applicableDate: f.applicableDate ? date(f.applicableDate) : null};
  if (focus.status === 'current' && (!focus.statedAt || focus.applicableDate !== forDate || Date.parse(focus.statedAt) > Date.parse(generatedAt) + 300000 || Date.parse(generatedAt) - Date.parse(focus.statedAt) > 36 * 3600000)) throw new Error('Focus is not fresh/applicable');
  const cards = values => list(values, 3).map(row => ({title: text(row.title, 160), detail: text(row.detail, 500), source: text(row.source, 120), url: link(row.url)}));
  const result = {schemaVersion: 1, generatedAt, forDate, timezone: 'America/Chicago', editionType: input.editionType, routineEnabled: input.routineEnabled, routine,
    focus, yesterday: cards(input.yesterday || []), opportunities: cards(input.opportunities || []), useful: cards(input.useful || []),
    sources: list(input.sources || [], 25).map(row => ({name: text(row.name, 80), status: status(row.status), sourceAt: row.sourceAt ? instant(row.sourceAt) : null})),
    stats: null, socialReleaseQueue: null, imageAvailable: input.imageAvailable === true, image: null};
  if (input.image != null) {
    const i = input.image;
    if (!result.imageAvailable || typeof i.sha256 !== 'string' || i.sha256.length !== 64 || !/^[a-f0-9]{64}$/.test(i.sha256) ||
        !['image/png','image/jpeg'].includes(i.mime) || !Number.isInteger(i.sizeBytes) || i.sizeBytes <= 4 || i.sizeBytes > 8*1024*1024) throw new Error('Invalid image provenance');
    result.image = {forDate:date(i.forDate), sha256:i.sha256, mime:i.mime, sizeBytes:i.sizeBytes, publishedAt:instant(i.publishedAt)};
    if (result.image.forDate > forDate || Date.parse(result.image.publishedAt) > now + 300000) throw new Error('Invalid image provenance time');
  }
  if (input.stats) {
    const s = input.stats;
    if (s.currency !== 'USD' || s.timezone !== 'America/Chicago') throw new Error('Unverified measurement currency/timezone');
    result.stats = {day: date(s.day), weekFrom: date(s.weekFrom), weekThrough: date(s.weekThrough), currency: 'USD', timezone: 'America/Chicago',
      campaigns: list(s.campaigns, 30).map(c => ({name: text(c.name, 300), daySpend: count(c.daySpend), last7dSpend: count(c.last7dSpend)})),
      sites: list(s.sites, 2).map(site => {
        if (!['absbyai.com', 'sixpackabs.com'].includes(site.name)) throw new Error('Unknown site');
        return {name: site.name, visitors: count(site.visitors), previousVisitors: count(site.previousVisitors), emailLeads: count(site.emailLeads),
          freeGenerations: count(site.freeGenerations), trials: count(site.trials), paid: count(site.paid)};
      }), note: text(s.note, 700)};
    if (date(s.weekThrough) !== s.day || date(s.weekFrom) > s.day) throw new Error('Invalid measurement window');
  }
  if (input.socialReleaseQueue) {
    const q = input.socialReleaseQueue, from = instant(q.windowFrom), to = instant(q.windowTo);
    // Seven local calendar days may contain 169 hours when DST ends.
    if (Date.parse(to) <= Date.parse(from) || Date.parse(to) - Date.parse(from) > 169 * 3600000) throw new Error('Invalid queue window');
    result.socialReleaseQueue = {status: status(q.status), checkedAt: q.checkedAt ? instant(q.checkedAt) : null, windowFrom: from, windowTo: to,
      sourceCoverage: {blotato: status(q.sourceCoverage.blotato), youtubeStudio: status(q.sourceCoverage.youtubeStudio)},
      coverageNote: text(q.coverageNote || '',500),
      publicCoverage: Object.fromEntries(['youtube','tiktok','facebook','instagram'].map(p=>[p,status(q.publicCoverage?.[p] || 'unverified')])),
      released: list(q.released || [],200).map(r=>({id:text(r.id,100),platform:text(r.platform,80),title:text(r.title,220),reviewUrl:link(r.reviewUrl),status:status(r.status,CHECK),reason:text(r.reason,500)})),
      rows: list(q.rows, 500).map(row => {
        const at = instant(row.scheduledAt);
        if (Date.parse(at) < Date.parse(from) || Date.parse(at) >= Date.parse(to)) throw new Error('Queue item outside window');
        return {id: text(row.id, 100), platform: text(row.platform, 80), account: text(row.account, 100), scheduledAt: at,
          title: text(row.title, 220), caption: text(row.caption || '', 1000), reviewUrl: link(row.reviewUrl), coverReviewUrl: link(row.coverReviewUrl), mediaUrl:link(row.mediaUrl),
          mediaSource: ['verified_upload_source','native_private'].includes(row.mediaSource) ? row.mediaSource : 'scheduled',
          coverFrameAt: row.coverFrameAt === 0 ? 0 : null,
          preflight: Object.fromEntries(['cover', 'description', 'links', 'duplicates', 'assetMatch','cadence','crop'].map(key => [key, status(row.preflight[key] || 'unverified', CHECK)])),
          notes: list(row.notes || [], 8).map(note => text(note, 250))};
      }).sort((a, b) => Date.parse(a.scheduledAt) - Date.parse(b.scheduledAt))};
  }
  const words = [focus.task, focus.why, ...[result.yesterday, result.opportunities, result.useful].flat().flatMap(c => [c.title, c.detail])].join(' ').split(/\s+/).length;
  if (words > 550) throw new Error('Main brief exceeds reading budget');
  return result;
}
module.exports = {validate};
