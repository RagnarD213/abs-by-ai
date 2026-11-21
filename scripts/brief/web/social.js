'use strict';
// Transport batches are bounded; the persistent inventory has no entry cap.
function validateMaster(rows) {
  if (!Array.isArray(rows) || rows.length > 100) throw new Error('Invalid import batch');
  const text = (s, max) => { if (typeof s !== 'string' || s.length > max || /[\u0000-\u0008]/.test(s)) throw new Error('Invalid inventory text'); return s; };
  const url = s => { if (!s) return null; const u = new URL(text(s,2000)); if (u.protocol !== 'https:' || u.username || u.password) throw new Error('Invalid inventory URL'); return u.href; };
  const instant = s => { if (typeof s !== 'string' || !/(Z|[+-]\d\d:\d\d)$/.test(s) || !Number.isFinite(Date.parse(s))) throw new Error('Invalid inventory time'); return s; };
  return rows.map(r => {
    if (!/^[a-f0-9]{64}$/.test(r.id) || !['youtube','tiktok','facebook','instagram'].includes(r.platform) || !['photo','short','longform','unknown'].includes(r.kind) ||
        !r.approval || !['approved','pending','scheduled_observed'].includes(r.approval.status) || !Array.isArray(r.media) || r.media.length > 20 || !Array.isArray(r.provenance) || !r.provenance.length || r.provenance.length > 1000) throw new Error('Invalid inventory record');
    const approval = {status:r.approval.status,reference:text(r.approval.reference,500),quote:text(r.approval.quote,2000)};
    if (approval.status === 'approved' && (!approval.quote.trim() || !approval.reference.trim())) throw new Error('Approval needs provenance');
    return {id:r.id,platform:r.platform,account:text(r.account,100),scheduledAt:instant(r.scheduledAt),title:text(r.title,220),caption:text(r.caption,10000),
      cover:url(r.cover),media:r.media.map(url),kind:r.kind,approval,
      provenance:r.provenance.map(p=>({source:text(p.source,100),sourceId:text(p.sourceId,200),checkedAt:instant(p.checkedAt)}))};
  });
}
function mediaURL(value) {
  try {
    const u = new URL(value);
    if (u.protocol !== 'https:' || u.username || u.password || u.port || u.hash) return null;
    if (u.hostname === 'i9.ytimg.com' && /^\/vi\/[A-Za-z0-9_-]{11}\/[A-Za-z0-9_-]+\.jpg$/.test(u.pathname) && [...u.searchParams.keys()].every(k=>['sqp','rs'].includes(k))) return u.href;
    if (u.search) return null;
    if (u.hostname === 'database.blotato.io' && /^\/storage\/v1\/object\/public\/public_media\/[a-f0-9-]+\/[a-f0-9-]+\.(png|jpe?g|mp4|webm)$/i.test(u.pathname)) return u.href;
    if (u.hostname === 'i.ytimg.com' && /^\/vi\/[A-Za-z0-9_-]{11}\/[A-Za-z0-9_-]+\.jpg$/.test(u.pathname)) return u.href;
    return null;
  } catch { return null; }
}
module.exports = {validateMaster,mediaURL};
