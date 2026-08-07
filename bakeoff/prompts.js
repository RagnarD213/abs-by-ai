// Extracts the REAL production prompt-assembly logic out of public/index.html and
// drives prod /api/generate-prompt, exactly as the browser client does.
// No production code is modified; this only reads the file.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const REPO = '/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const HTML = fs.readFileSync(path.join(REPO, 'public/index.html'), 'utf8');

// Slice from `const SYSTEM_PROMPT = ` through the end of goalSystemPrompt().
const start = HTML.indexOf('const SYSTEM_PROMPT = `');
if (start === -1) throw new Error('SYSTEM_PROMPT not found');
const gsMarker = HTML.indexOf('function goalSystemPrompt() {', start);
if (gsMarker === -1) throw new Error('goalSystemPrompt not found');
const gsEnd = HTML.indexOf('\n}', gsMarker) + 2;
const source = HTML.slice(start, gsEnd);

function buildSystemPrompt({ gender, condition, intensity }) {
  const sandbox = {
    state: {
      gender,
      condition,
      intensity,
      effectiveIntensity: intensity,
      description: '',
    },
    module: {},
  };
  vm.createContext(sandbox);
  vm.runInContext(source + '\n;__out = goalSystemPrompt();', sandbox);
  const out = sandbox.__out;
  if (!out || out.includes('[[')) throw new Error('marker leak or empty prompt');
  return out;
}

function makeUserJson({ gender, condition, intensity }) {
  return JSON.stringify({
    user_description: '',
    subject_gender: gender,
    subject_current_condition: condition,
    intensity,
    has_reference_photo: false,
  });
}

// Prod call — identical shape to callGeminiText() in the client.
async function generatePrompt(caseSpec) {
  const res = await fetch('https://absbyai.com/api/generate-prompt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      systemPrompt: buildSystemPrompt(caseSpec),
      userJson: makeUserJson(caseSpec),
    }),
  });
  const data = await res.json();
  if (!res.ok || !data?.prompt) throw new Error(`generate-prompt failed ${res.status}: ${data?.error || ''}`);
  return data.prompt.trim();
}

// Production's condensed variant for Kontext (server.js condenseForKontext).
function condense(fullPrompt) {
  const firstPara = String(fullPrompt).split(/\n\s*\n/)[0] || String(fullPrompt);
  return firstPara.slice(0, 1800)
    + '\n\nKeep the exact same face, identity, hairstyle, expression, clothing, pose, camera framing, background, and lighting as the input photo — only the body composition changes. No veins, no comically oversized muscles. The result must look like a natural, unretouched smartphone photograph of the same person.';
}

module.exports = { buildSystemPrompt, makeUserJson, generatePrompt, condense };
