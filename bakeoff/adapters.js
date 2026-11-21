// Model adapters for the bake-off. Every adapter returns the same shape:
//   { ok, imageBase64, imageMime, latencyMs, blocked, error, meta }
// Nothing here touches production code — the harness calls each provider directly.
// Minimal .env loader (secrets pulled from Railway into a 0600 scratchpad file).
for (const line of require('fs').readFileSync(__dirname + '/.env', 'utf8').split('\n')) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
  if (m) process.env[m[1]] = m[2];
}

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const REPLICATE_API_TOKEN = process.env.REPLICATE_API_TOKEN;

const TIMEOUT_MS = 150000; // GPT Image high-fidelity + 4MP models can be slow

function withTimeout(ms) {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), ms);
  return { signal: c.signal, done: () => clearTimeout(t) };
}

// ── Gemini family (gemini-2.5-flash-image, gemini-3-pro-image-preview) ──
// Mirrors server.js callGemini: same parts layout, same safetySettings.
async function geminiAdapter(modelId, { prompt, photoBase64, photoMime }) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${modelId}:generateContent?key=${encodeURIComponent(GEMINI_API_KEY)}`;
  const { signal, done } = withTimeout(TIMEOUT_MS);
  const t0 = Date.now();
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal,
      body: JSON.stringify({
        contents: [{
          role: 'user',
          parts: [
            { text: prompt },
            { inline_data: { mime_type: photoMime, data: photoBase64 } },
          ],
        }],
        generationConfig: { responseModalities: ['TEXT', 'IMAGE'] },
        safetySettings: [
          { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_ONLY_HIGH' },
          { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_ONLY_HIGH' },
          { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
          { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' },
        ],
      }),
    });
    const data = await response.json();
    const latencyMs = Date.now() - t0;
    if (!response.ok) {
      return { ok: false, latencyMs, error: `HTTP ${response.status}: ${data?.error?.message || ''}`.slice(0, 300) };
    }
    const parts = data?.candidates?.[0]?.content?.parts || [];
    const imgPart = parts.find((p) => p.inline_data || p.inlineData);
    if (!imgPart) {
      const fr = data?.candidates?.[0]?.finishReason || data?.promptFeedback?.blockReason || 'no-image';
      return { ok: false, latencyMs, blocked: /SAFETY|PROHIBITED|BLOCK|IMAGE_SAFETY/i.test(String(fr)), error: `no image (${fr})` };
    }
    const inline = imgPart.inline_data || imgPart.inlineData;
    return { ok: true, latencyMs, imageBase64: inline.data, imageMime: inline.mime_type || inline.mimeType || 'image/png' };
  } catch (e) {
    return { ok: false, latencyMs: Date.now() - t0, error: e.name === 'AbortError' ? 'timeout' : e.message };
  } finally { done(); }
}

// ── Replicate (shared submit → poll → download) ──
async function replicateRun(modelSlug, input) {
  const { signal, done } = withTimeout(TIMEOUT_MS);
  const t0 = Date.now();
  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${REPLICATE_API_TOKEN}` };
  try {
    const submit = await fetch(`https://api.replicate.com/v1/models/${modelSlug}/predictions`, {
      method: 'POST', headers: { ...headers, Prefer: 'wait' }, body: JSON.stringify({ input }), signal,
    });
    let pred = await submit.json().catch(() => null);
    if (!submit.ok || !pred) {
      const msg = `${submit.status} ${pred?.detail || pred?.title || ''}`.trim();
      return {
        ok: false, latencyMs: Date.now() - t0,
        error: msg.slice(0, 300),
        outOfCredit: submit.status === 402,
        throttled: submit.status === 429,
      };
    }
    while (pred.status === 'starting' || pred.status === 'processing') {
      await new Promise((r) => setTimeout(r, 2000));
      const poll = await fetch(pred.urls?.get, { headers, signal });
      pred = await poll.json().catch(() => null);
      if (!pred) return { ok: false, latencyMs: Date.now() - t0, error: 'poll failed' };
    }
    if (pred.status !== 'succeeded' || !pred.output) {
      const err = String(pred.error || pred.status);
      return {
        ok: false, latencyMs: Date.now() - t0, error: err.slice(0, 300),
        blocked: /sensitive|moderat|E005|safety|flagged|content polic/i.test(err),
      };
    }
    const imgUrl = Array.isArray(pred.output) ? pred.output[0] : pred.output;
    const imgRes = await fetch(imgUrl, { signal });
    if (!imgRes.ok) return { ok: false, latencyMs: Date.now() - t0, error: `download ${imgRes.status}` };
    const buf = Buffer.from(await imgRes.arrayBuffer());
    const mime = imgRes.headers.get('content-type') || 'image/jpeg';
    return {
      ok: true, latencyMs: Date.now() - t0, imageBase64: buf.toString('base64'), imageMime: mime,
      meta: { predictTime: pred.metrics?.predict_time ?? null, predictionId: pred.id },
    };
  } catch (e) {
    return { ok: false, latencyMs: Date.now() - t0, error: e.name === 'AbortError' ? 'timeout' : e.message };
  } finally { done(); }
}

const dataUrl = (b64, mime) => `data:${mime};base64,${b64}`;
const portraitRatio = (w, h) => (h >= w ? '2:3' : '3:2'); // gpt-image-1.5 has no match_input_image

// GPT Image 1.5 reads the production prompt's "Placed side by side with the input"
// line literally and renders a before/after diptych. Its prompting guide calls for
// an explicit statement of the output artifact, so the adapter appends one.
const GPT_SINGLE_IMAGE_CLAUSE = `

OUTPUT FORMAT: Return exactly ONE photograph showing only the AFTER version of this person, filling the entire frame. Do NOT produce a before-and-after comparison, split panel, side-by-side, collage, grid, border, caption, or any text. Reproduce the input photo's framing, crop, background and lighting as closely as possible — this is a single edited photograph, not a composite.`;

// ── Roster ──
// nominalCost = published per-image price, used only for a running estimate;
// real spend is confirmed on the Replicate billing page.
const MODELS = {
  'gemini-2.5-flash-image': {
    label: 'Gemini 2.5 Flash Image', provider: 'google', nominalCost: 0.039, promptVariant: 'full',
    run: (job) => geminiAdapter('gemini-2.5-flash-image', job),
  },
  'nano-banana-pro': {
    label: 'Nano Banana Pro (gemini-3-pro-image-preview)', provider: 'google', nominalCost: 0.134, promptVariant: 'full',
    run: (job) => geminiAdapter('gemini-3-pro-image-preview', job),
  },
  // Added 2026-08-09 (round 8). Both are GA on generativelanguage.googleapis.com
  // and were confirmed live in the model list + a real smoke-test call, not
  // assumed. `gemini-3-pro-image` is the GA endpoint for the same Nano Banana Pro
  // model the `-preview` alias above points at — prefer the GA one for anything
  // that could ship. Prices are per-image from ai.google.dev/gemini-api/docs/pricing
  // at the DEFAULT (1K) output resolution these calls request.
  'gemini-3.1-flash-image': {
    label: 'Nano Banana 2 (gemini-3.1-flash-image)', provider: 'google', nominalCost: 0.067, promptVariant: 'full',
    run: (job) => geminiAdapter('gemini-3.1-flash-image', job),
  },
  'gemini-3-pro-image': {
    label: 'Nano Banana Pro (gemini-3-pro-image, GA)', provider: 'google', nominalCost: 0.134, promptVariant: 'full',
    run: (job) => geminiAdapter('gemini-3-pro-image', job),
  },
  'gpt-image-1.5': {
    label: 'GPT Image 1.5 (high fidelity)', provider: 'replicate', nominalCost: 0.19, promptVariant: 'condensed',
    run: (job) => replicateRun('openai/gpt-image-1.5', {
      prompt: job.prompt + GPT_SINGLE_IMAGE_CLAUSE,
      input_images: [dataUrl(job.photoBase64, job.photoMime)],
      input_fidelity: 'high',          // required: low drifts faces
      quality: 'high',
      aspect_ratio: portraitRatio(job.width, job.height),
      moderation: job.gptModeration || 'auto',
      output_format: 'jpeg',
    }),
  },
  'flux-kontext-pro': {
    label: 'FLUX Kontext Pro', provider: 'replicate', nominalCost: 0.04, promptVariant: 'condensed',
    run: (job) => replicateRun('black-forest-labs/flux-kontext-pro', {
      prompt: job.prompt,
      input_image: dataUrl(job.photoBase64, job.photoMime),
      aspect_ratio: 'match_input_image',
      output_format: 'jpg',
    }),
  },
  'flux-2-pro': {
    label: 'FLUX 2 Pro (edit)', provider: 'replicate', nominalCost: 0.03, promptVariant: 'condensed',
    run: (job) => replicateRun('black-forest-labs/flux-2-pro', {
      prompt: job.prompt,
      input_images: [dataUrl(job.photoBase64, job.photoMime)],
      aspect_ratio: 'match_input_image',
      resolution: 'match_input_image',
      output_format: 'jpg',
      output_quality: 95,
      safety_tolerance: 2,
    }),
  },
  'seedream-4.5': {
    label: 'Seedream 4.5 (edit)', provider: 'replicate', nominalCost: 0.04, promptVariant: 'condensed',
    // Seedream hard-rejects prompts over 4000 chars (422), so the full production
    // prompt has to be trimmed to fit. Recorded as a real constraint of this model.
    run: (job) => replicateRun('bytedance/seedream-4.5', {
      prompt: job.prompt.length > 4000 ? job.prompt.slice(0, 4000) : job.prompt,
      image_input: [dataUrl(job.photoBase64, job.photoMime)],
      size: '2K',
      aspect_ratio: 'match_input_image',
      sequential_image_generation: 'disabled',
    }),
  },
};

module.exports = { MODELS, geminiAdapter, replicateRun };
