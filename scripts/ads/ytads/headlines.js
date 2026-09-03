'use strict';
//
// YTADS HEADLINES — Claude writes the ad copy for one new video, in Dan's existing
// style, and lint.js is the hard gate. Regenerates up to MAX_ATTEMPTS times, feeding
// the failures back; whatever still fails is DROPPED, never used. If fewer than the
// minimum lines survive, the caller records a permanent skip and the brief shows the
// failing text — the ad is not created. Conservative beats clever.
//
// Copy shape (Demand Gen video responsive ad): up to 5 headlines (≤40), up to 5 long
// headlines (≤90), up to 5 descriptions (≤90). We ask for 5 / 3 / 3 and require at
// least 3 / 1 / 1 after lint.
//
// Model: Opus 5 through the same raw /v1/messages fetch server.js uses everywhere
// (project convention). A few hundred tokens per video, a handful of videos a week.

const fs = require('fs');
const path = require('path');
const { lintSet, passingOnly, RULES_TEXT, LIMITS } = require('./lint.js');

const MODEL = 'claude-opus-5';
const MAX_ATTEMPTS = 3;
const MIN_LINES = { headlines: 3, longHeadlines: 1, descriptions: 1 };
const STYLE_FILE = path.join(__dirname, 'headline-style.md');

function loadStyle() {
  try { return fs.readFileSync(STYLE_FILE, 'utf8'); } catch { return '(no style file yet)'; }
}

function buildPrompt({ video, style, failures }) {
  const desc = String(video.description || '').split('\n').filter(l => !/^https?:\/\//.test(l.trim()) && !/^#/.test(l.trim())).join('\n').slice(0, 1200);
  let user = `Write Google Ads Demand Gen copy for this YouTube ${video.isShort ? 'Short' : 'video'} from the Abs by AI channel. The ad's only goal is to get the viewer to WATCH the video and subscribe; it must describe what the video shows.

VIDEO TITLE: ${video.title}
VIDEO DESCRIPTION:
${desc || '(none)'}

Return ONLY a JSON object, no prose, shaped exactly:
{"headlines": [5 strings, each ≤ ${LIMITS.headline} characters],
 "longHeadlines": [3 strings, each ≤ ${LIMITS.longHeadline} characters],
 "descriptions": [3 strings, each ≤ ${LIMITS.description} characters]}`;
  if (failures && failures.length) {
    user += `\n\nYour previous attempt had lines that FAILED the compliance lint. Do not repeat them or anything like them:\n` +
      failures.map(f => `- [${f.kind}] "${f.text}" → ${f.reasons.join('; ')}`).join('\n');
  }
  const system = `You write short, plain, compliant ad copy for Abs by AI, a fitness channel run by Dan (a 40-year-old with visible abs who shows exactly what he does). Match the style rules below exactly — they were extracted from Dan's own live ads. Sentence case, no hype, no exclamation marks, about the video.

STYLE RULES (from Dan's existing ads):
${style}

COMPLIANCE RULES (hard gate — a line that breaks one is thrown away):
${RULES_TEXT.map(r => '- ' + r).join('\n')}`;
  return { system, user };
}

function parseJson(text) {
  const m = /\{[\s\S]*\}/.exec(String(text || ''));
  if (!m) throw new Error('no JSON object in model output');
  const obj = JSON.parse(m[0]);
  const arr = (a) => Array.isArray(a) ? a.map(s => String(s)).filter(Boolean) : [];
  return { headlines: arr(obj.headlines), longHeadlines: arr(obj.longHeadlines), descriptions: arr(obj.descriptions) };
}

async function callClaude({ system, user, apiKey, fetchImpl = fetch }) {
  const res = await fetchImpl('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-beta': 'server-side-fallback-2026-07-01',
    },
    body: JSON.stringify({
      model: MODEL, max_tokens: 2000,
      output_config: { effort: 'medium' },
      fallbacks: 'default',
      system,
      messages: [{ role: 'user', content: user }],
    }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(`Anthropic ${res.status}: ${(data.error && data.error.message) || JSON.stringify(data).slice(0, 200)}`);
  if (data.stop_reason === 'refusal') throw new Error('model refused');
  return (data.content || []).filter(b => b.type === 'text').map(b => b.text).join('');
}

// → { ok, set, attempts, failures:[...all failing lines seen...], error? }
async function generateHeadlines({ video, apiKey, fetchImpl, style = loadStyle(), generate }) {
  const gen = generate || (async (p) => parseJson(await callClaude({ ...p, apiKey, fetchImpl })));
  const allFailures = [];
  let last = null; let lastFailures = [];
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    let set;
    try { set = await gen(buildPrompt({ video, style, failures: lastFailures })); }
    catch (e) { allFailures.push({ kind: 'error', text: '', reasons: [e.message] }); continue; }
    last = set;
    const lint = lintSet(set);
    if (lint.ok && enough(set)) return { ok: true, set: passingOnly(set), attempts: attempt, failures: allFailures };
    lastFailures = lint.failures;
    allFailures.push(...lint.failures);
    if (!lint.ok) continue;
  }
  // Out of attempts: keep what passes, if it is enough.
  const kept = last ? passingOnly(last) : { headlines: [], longHeadlines: [], descriptions: [] };
  if (enough(kept)) return { ok: true, set: kept, attempts: MAX_ATTEMPTS, failures: allFailures, partial: true };
  return { ok: false, set: kept, attempts: MAX_ATTEMPTS, failures: allFailures,
           error: `only ${kept.headlines.length}/${kept.longHeadlines.length}/${kept.descriptions.length} lines passed lint (need ${MIN_LINES.headlines}/${MIN_LINES.longHeadlines}/${MIN_LINES.descriptions})` };
}

function enough(set) {
  return set.headlines.length >= MIN_LINES.headlines && set.longHeadlines.length >= MIN_LINES.longHeadlines && set.descriptions.length >= MIN_LINES.descriptions;
}

module.exports = { generateHeadlines, buildPrompt, parseJson, callClaude, loadStyle, MODEL, MAX_ATTEMPTS, MIN_LINES, STYLE_FILE };
