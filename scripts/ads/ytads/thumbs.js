'use strict';
//
// YTADS THUMBS — attempt 3 of the retry rule (Dan 2026-09-10). A Demand Gen video ad has no
// thumbnail of its own: it shows the YouTube video's thumbnail. So attempt 3 puts a clean,
// text-free frame of Dan on the PUBLIC video (Dan's choice over an unlisted copy), and if
// that attempt fails too, the original thumbnail goes back.
//
//   fetchCurrent(videoId)          → { url, buf }  the thumbnail YouTube serves now (saved before any swap)
//   makeCleanThumbnail({videoId})  → { ok, jpeg, frame, crop, check } | { ok:false, reason }
//   setThumbnail(videoId, buf)     → thumbnails.set on the Abs by AI channel
//
// Frames: YouTube's own full-size frames — oar1..3 + oardefault (1080×1920, Shorts) or
// maxres1..3 (1280×720). Claude only LOCATES things on each frame — Dan's head (top of hair
// to chin), every text/caption area, and whether the expression is calm. The crop is then
// computed here by rule (room above the hair and below the chin, centred on the head,
// clear of every text area — our Shorts carry burned captions), so the framing is the
// same every time. Measured 2026-09-10: letting the model draw the crop box cut Dan off
// at the glasses and at the chin, and picked a mid-shout frame. A second Claude look must
// then confirm: no text, whole face, head not cut, expression not bad.
//
// Credentials: GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN — the same
// client and token scripts/youtube/upload.js uses (scope youtube.upload covers
// thumbnails.set; verified 2026-09-10).

const sharp = require('sharp');

const MODEL = 'claude-opus-5';
const YT = 'https://i.ytimg.com/vi/';
const OUT_W = 1280, OUT_H = 720;
// A frame of Dan from his own Short "Hire A Maid Instead Of A Personal Trainer" — a YouTube
// auto-frame, which thumbnails.set does not touch. Both Claude passes compare against it:
// measured 2026-09-10, a frame of a B-roll stranger passed every other check.
const REFERENCE_URL = `${YT}LvOMn7IpuCI/oar2.jpg`;

async function fetchImage(url, fetchImpl = fetch) {
  const r = await fetchImpl(url);
  if (!r.ok) return null;
  const buf = Buffer.from(await r.arrayBuffer());
  return buf.length > 2000 ? buf : null;   // YouTube's grey placeholder is ~1 KB
}

async function fetchCurrent(videoId, fetchImpl = fetch) {
  for (const f of ['maxresdefault', 'sddefault', 'hqdefault']) {
    const url = `${YT}${videoId}/${f}.jpg`;
    const buf = await fetchImage(url, fetchImpl);
    if (buf) return { url, buf };
  }
  throw new Error(`no current thumbnail readable for ${videoId}`);
}

async function accessToken(fetchImpl = fetch) {
  const { GOOGLE_CLIENT_ID: id, GOOGLE_CLIENT_SECRET: secret, YOUTUBE_REFRESH_TOKEN: rt } = process.env;
  if (!id || !secret || !rt) throw new Error('YouTube credentials missing (GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET / YOUTUBE_REFRESH_TOKEN)');
  const r = await fetchImpl('https://oauth2.googleapis.com/token', {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: id, client_secret: secret, refresh_token: rt, grant_type: 'refresh_token' }),
  });
  const j = await r.json();
  if (!j.access_token) throw new Error('YouTube token refresh failed: ' + (j.error_description || j.error || r.status));
  return j.access_token;
}

async function setThumbnail(videoId, buf, fetchImpl = fetch) {
  const token = await accessToken(fetchImpl);
  const r = await fetchImpl(`https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${videoId}&uploadType=media`, {
    method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'image/jpeg' }, body: buf,
  });
  if (!r.ok) throw new Error(`thumbnails.set ${r.status}: ${(await r.text()).slice(0, 300)}`);
  return r.json();
}

async function claude({ content, apiKey, fetchImpl = fetch }) {
  const res = await fetchImpl('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-api-key': apiKey, 'anthropic-version': '2023-06-01', 'anthropic-beta': 'server-side-fallback-2026-07-01' },
    body: JSON.stringify({ model: MODEL, max_tokens: 2000, output_config: { effort: 'medium' }, fallbacks: 'default', messages: [{ role: 'user', content }] }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(`Anthropic ${res.status}: ${(data.error && data.error.message) || JSON.stringify(data).slice(0, 200)}`);
  const text = (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('');
  const m = /\{[\s\S]*\}/.exec(text);
  if (!m) throw new Error('no JSON in model output');
  return JSON.parse(m[0]);
}

const jpegBlock = (buf) => ({ type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: buf.toString('base64') } });

// One definition for both passes. Talking-head Shorts catch Dan mid-word in almost every
// frame and YouTube serves only 3–4 of them, so normal speech must count as good —
// measured 2026-09-10: a vaguer wording flip-flopped on the same frame between runs.
const EXPRESSION_RULE = '"good" when his eyes are open and his mouth is closed, smiling, or open only as it is in normal speech; "bad" ONLY for eyes closed or half-closed, a grimace or squint, or a mouth open wide (shouting, yawning, a big laugh, tongue showing).';

const LOCATE_PROMPT = `The first image is a REFERENCE photo of Dan. The numbered images are frames from a YouTube video of his. We need a calm, clean thumbnail of Dan with no text in it. Do not choose a crop — only report what is where.
Some frames may show other people (B-roll). Report "head" ONLY when the man in the frame is Dan — the same person as in the reference; for anyone else set "head" to null and "who" to "other".
For EACH numbered frame report:
- "who": "dan", "other" or "none".
- "head": the box around Dan's WHOLE head — top = the top of his hair, bottom = the lowest point of his chin (below the mouth, where the jaw meets the neck), left/right = the outer edges of his ears — in PIXELS of that frame's image exactly as shown to you (its size is given above it). null if his whole head is not inside the frame.
- "text": every area holding text, captions, subtitles, numbers, logos, watermarks or graphic overlays, as boxes {"top","bottom","left","right"} in the same pixels. [] if there is none.
- "expression": ${EXPRESSION_RULE}
- "mouth": "closed" or "open".
Be precise: a caption line directly under his chin must be its own text box.
Return ONLY JSON: {"frames":[{"frame":0,"who":"dan","head":{"top":230,"bottom":520,"left":190,"right":450},"text":[{"top":690,"bottom":760,"left":60,"right":580}],"expression":"good","mouth":"closed"}]}`;

// Pixel boxes on the preview → fractions of the frame. The head gets a safety margin
// (the chin is the point the model most often places too high — measured 2026-09-10).
const toFrac = (b, f) => (b ? { top: b.top / f.ph, bottom: b.bottom / f.ph, left: b.left / f.pw, right: b.right / f.pw } : null);
const padHead = (h, extraBelow = 0) => {
  const hh = h.bottom - h.top, hw = h.right - h.left;
  return { top: h.top - 0.04 * hh, bottom: h.bottom + (0.08 + extraBelow) * hh, left: h.left - 0.05 * hw, right: h.right + 0.05 * hw };
};

const CHECK_PROMPT = `The first image is a REFERENCE photo of Dan; the second is a CANDIDATE thumbnail. Answer about the candidate:
- "dan": is the man in the candidate the same person as in the reference?
- "text": is there ANY text — letters, words, numbers, captions, subtitles, logos, watermarks, UI or graphic overlays — even small or partial at an edge?
- "face": is a man's WHOLE face visible — both eyes, nose, mouth and the whole chin?
- "cut": does the image edge touch or cut his hair or his chin (no space above the hair or below the chin)?
- "expression": ${EXPRESSION_RULE}
Return ONLY JSON: {"dan":true|false,"text":true|false,"face":true|false,"cut":true|false,"expression":"good"|"bad","note":"..."}`;
const passes = (check) => !!check && check.dan === true && check.text === false && check.face === true && check.cut === false && check.expression !== 'bad';

// The crop, by rule, from the located head and text boxes (fractions) on a W×H frame.
// Room above the hair (30% of head height, at least 8%) and below the chin (70%, at least
// 10%) — pulled in to stay clear of any caption above or below — centred on the head,
// shaped between 3:4 and 16:9. Null when no such box exists (e.g. a caption over the face).
function cropFromHead(head, texts, W, H) {
  if (!head) return null;
  const hy0 = head.top * H, hy1 = head.bottom * H, hx0 = head.left * W, hx1 = head.right * W;
  const hh = hy1 - hy0, hw = hx1 - hx0;
  if (!(hh > 60 && hw > 40)) return null;
  const boxes = (texts || []).map(t => ({ y0: t.top * H, y1: t.bottom * H, x0: t.left * W, x1: t.right * W }));
  let top = hy0 - 0.3 * hh, bottom = hy1 + 0.7 * hh;
  for (const t of boxes) {
    if (t.x1 < hx0 - hw || t.x0 > hx1 + hw) continue;                        // far off to the side
    if (t.y0 >= hy1 - 2 && t.y0 < bottom) bottom = Math.max(hy1 + 0.1 * hh, t.y0 - 0.02 * H);
    if (t.y1 <= hy0 + 2 && t.y1 > top) top = Math.min(hy0 - 0.08 * hh, t.y1 + 0.02 * H);
  }
  top = Math.max(0, top); bottom = Math.min(H, bottom);
  if (hy0 - top < 0.08 * hh || bottom - hy1 < 0.1 * hh) return null;         // no room above the hair / below the chin
  let h = bottom - top;
  let w = Math.max(h * 16 / 9, hw * 1.6);
  w = Math.min(W, w);
  if (w / h < 3 / 4) { h = w * 4 / 3; bottom = top + h; if (bottom - hy1 < 0.1 * hh) return null; }
  const left = Math.max(0, Math.min(W - w, (hx0 + hx1) / 2 - w / 2));
  const box = { left: Math.round(left), top: Math.round(top), width: Math.round(w), height: Math.round(h) };
  const hits = boxes.some(t => t.x0 < box.left + box.width && t.x1 > box.left && t.y0 < box.top + box.height && t.y1 > box.top);
  return hits ? null : box;
}

// 1280×720 JPEG from a crop: a 16:9 crop fills the frame; a taller one is centred on a
// plain background the colour of its own left/right edges (no blur — Dan's thumbnail style).
async function render(buf, box) {
  if (box.width / box.height >= 16 / 9 - 0.01) return sharp(buf).extract(box).resize(OUT_W, OUT_H).jpeg({ quality: 90 }).toBuffer();
  const part = await sharp(buf).extract(box).resize({ height: OUT_H }).toBuffer();
  const pm = await sharp(part).metadata();
  const edge = async (left) => (await sharp(part).extract({ left, top: 0, width: 8, height: pm.height }).stats()).channels.slice(0, 3).map(c => c.mean);
  const [l, r] = [await edge(0), await edge(pm.width - 8)];
  const bg = { r: Math.round((l[0] + r[0]) / 2), g: Math.round((l[1] + r[1]) / 2), b: Math.round((l[2] + r[2]) / 2) };
  return sharp({ create: { width: OUT_W, height: OUT_H, channels: 3, background: bg } })
    .composite([{ input: part, left: Math.round((OUT_W - pm.width) / 2), top: 0 }]).jpeg({ quality: 90 }).toBuffer();
}

async function candidateFrames(videoId, fetchImpl) {
  const list = [];
  for (const f of ['oar1', 'oar2', 'oar3', 'oardefault']) { const buf = await fetchImage(`${YT}${videoId}/${f}.jpg`, fetchImpl); if (buf) list.push({ url: `${YT}${videoId}/${f}.jpg`, buf }); }
  if (!list.length) for (const f of ['maxres1', 'maxres2', 'maxres3']) { const buf = await fetchImage(`${YT}${videoId}/${f}.jpg`, fetchImpl); if (buf) list.push({ url: `${YT}${videoId}/${f}.jpg`, buf }); }
  for (const fr of list) { const m = await sharp(fr.buf).metadata(); fr.w = m.width; fr.h = m.height; }
  return list;
}

async function makeCleanThumbnail({ videoId, apiKey, fetchImpl = fetch }) {
  if (!apiKey) return { ok: false, reason: 'no ANTHROPIC_API_KEY' };
  const frames = await candidateFrames(videoId, fetchImpl);
  if (!frames.length) return { ok: false, reason: 'YouTube serves no full-size frames for this video' };
  const refBuf = await fetchImage(REFERENCE_URL, fetchImpl);
  if (!refBuf) throw new Error('the reference frame of Dan is unreadable: ' + REFERENCE_URL);   // thrown → transient, retried next hour
  const ref = await sharp(refBuf).resize({ width: 480, withoutEnlargement: true }).jpeg({ quality: 85 }).toBuffer();
  const content = [{ type: 'text', text: 'REFERENCE — this is Dan:' }, jpegBlock(ref)];
  for (let i = 0; i < frames.length; i++) {
    const small = await sharp(frames[i].buf).resize({ width: 640, withoutEnlargement: true }).jpeg({ quality: 85 }).toBuffer();
    const sm = await sharp(small).metadata(); frames[i].pw = sm.width; frames[i].ph = sm.height;
    content.push({ type: 'text', text: `Frame ${i} — ${sm.width}×${sm.height} px as shown` }, jpegBlock(small));
  }
  content.push({ type: 'text', text: LOCATE_PROMPT });
  const tried = [];
  // Two looks at the frames: the model's reading is not deterministic, and a second look
  // is cheaper than holding attempt 3 for a video that has a usable frame.
  for (let pass = 1; pass <= 2; pass++) {
    const found = await tryFrames({ frames, content, ref, apiKey, fetchImpl, pass, tried });
    if (found) return found;
  }
  return { ok: false, reason: `no frame gave a clean thumbnail (Dan, whole head with room around it, no text, calm expression): ${tried.join(' | ').slice(0, 400) || 'Dan\'s whole head is in none of the frames'}` };
}

// Frame order: a good expression with the mouth closed first, then any good expression,
// then the biggest head.
const frameRank = (f) => (f.expression === 'good' ? 0 : 2) + (f.mouth === 'closed' ? 0 : 1);

// One look: locate Dan on every frame, then crop, render and check the frames in order.
// Returns the first thumbnail that passes, or null (reasons appended to `tried`).
async function tryFrames({ frames, content, ref, apiKey, fetchImpl, pass, tried }) {
  const located = ((await claude({ content, apiKey, fetchImpl })).frames || [])
    .map(f => { const fr = frames[Number(f.frame)]; return fr && f.head && f.who === 'dan' ? { ...f, fr, head: toFrac(f.head, fr), text: (f.text || []).map(t => toFrac(t, fr)) } : null; })
    .filter(Boolean)
    .sort((a, b) => frameRank(a) - frameRank(b) || (b.head.bottom - b.head.top) - (a.head.bottom - a.head.top));
  for (const f of located) {
    const tag = f.fr.url.split('/').pop();
    if (f.expression === 'bad') { tried.push(`pass ${pass} ${tag}: expression`); continue; }
    // One retry with more room under the chin when the check says the face is cut.
    let note = 'no text-free crop with room around the head';
    for (const extraBelow of [0, 0.25]) {
      const crop = cropFromHead(padHead(f.head, extraBelow), f.text, f.fr.w, f.fr.h);
      if (!crop) break;
      const jpeg = await render(f.fr.buf, crop);
      const check = await claude({ content: [jpegBlock(ref), jpegBlock(jpeg), { type: 'text', text: CHECK_PROMPT }], apiKey, fetchImpl });
      if (passes(check)) return { ok: true, jpeg, frame: f.fr.url, crop, check };
      note = (check && check.note) || 'check failed';
      if (!check || check.dan !== true || check.text !== false || check.expression === 'bad' || !(check.cut || !check.face)) break;   // only a cut face is worth the retry
    }
    tried.push(`pass ${pass} ${tag}: ${note}`);
  }
  return null;
}

module.exports = { fetchCurrent, makeCleanThumbnail, setThumbnail, cropFromHead, render, passes, LOCATE_PROMPT, CHECK_PROMPT, REFERENCE_URL };
