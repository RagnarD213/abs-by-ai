const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const ROOT = process.cwd();
const OUT = __dirname;
const SOURCE = path.join(ROOT, 'output/thumbnails/channel-refresh-20260916/revision-2/frames/v6-B.jpg');
const W = 1280;
const H = 720;

const svg = (body) => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}">
  <defs>
    <linearGradient id="leftFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#03172d" stop-opacity="0.90"/>
      <stop offset="0.58" stop-color="#03172d" stop-opacity="0.64"/>
      <stop offset="1" stop-color="#03172d" stop-opacity="0"/>
    </linearGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="3" dy="5" stdDeviation="4" flood-color="#000000" flood-opacity="0.82"/>
    </filter>
  </defs>
  ${body}
</svg>`);

function textNode(text, x, y, size, fill, anchor = 'start') {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Arial Black, Arial, sans-serif" font-size="${size}" font-weight="900" letter-spacing="-2" fill="${fill}" filter="url(#shadow)">${text}</text>`;
}

async function write(name, overlay, details) {
  const base = await sharp(SOURCE)
    .resize(W, H)
    .modulate({ brightness: 1.04, saturation: 1.03 })
    .png()
    .toBuffer();
  const output = path.join(OUT, `${name}.jpg`);
  await sharp(base)
    .composite([{ input: svg(overlay) }])
    .jpeg({ quality: 96, chromaSubsampling: '4:4:4' })
    .toFile(output);
  return { name, output, ...details };
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });

  const results = [];
  results.push(await write('V8-A-3-sets-thats-it', `
    <rect x="24" y="22" width="490" height="245" rx="22" fill="#041426" fill-opacity="0.95" stroke="#1788ff" stroke-width="2"/>
    ${textNode('3 SETS.', 52, 132, 104, '#ffe500')}
    ${textNode("THAT'S IT.", 52, 234, 92, '#ffffff')}
  `, {
    headline: "3 SETS. THAT'S IT.",
    concept: 'Direct promise with a compact navy panel and yellow emphasis'
  }));

  results.push(await write('V8-B2-ab-wheel-workout', `
    <path d="M34 32 H840 L812 157 H34 Z" fill="#0865ef" stroke="#58c7ff" stroke-width="2"/>
    ${textNode('AB WHEEL WORKOUT', 62, 123, 62, '#ffffff')}
    <rect x="48" y="171" width="516" height="70" rx="12" fill="#ffd400"/>
    ${textNode('3-SET FOLLOW-ALONG', 69, 223, 43, '#071324')}
  `, {
    headline: 'AB WHEEL WORKOUT / 3-SET FOLLOW-ALONG',
    concept: 'Exercise name in three separate words, fully contained in blue, with no shaded overlay'
  }));

  results.push(await write('V8-C-do-this-with-me', `
    <rect x="0" y="0" width="1280" height="250" fill="url(#leftFade)" opacity="0.74"/>
    ${textNode('DO THIS', 45, 130, 95, '#ffffff')}
    ${textNode('WITH ME', 485, 130, 95, '#18e1ef')}
    <circle cx="1118" cy="114" r="82" fill="#ed1111" stroke="#ffffff" stroke-width="7" filter="url(#shadow)"/>
    ${textNode('3', 1118, 105, 70, '#ffffff', 'middle')}
    ${textNode('SETS', 1118, 156, 40, '#ffffff', 'middle')}
  `, {
    headline: 'DO THIS WITH ME / 3 SETS',
    concept: 'Follow-along invitation with a high-visibility three-set badge'
  }));

  const manifest = {
    videoId: 'b_bS9NdmL-g',
    title: 'Ab Wheel Workout: 3 Sets For Stronger Abs (Do It With Me)',
    source: SOURCE,
    sourceTreatment: 'Same source frame and photographic finishing as the installed thumbnail; only graphic overlays changed',
    width: W,
    height: H,
    realPhotoDisclosure: 'Omitted under the standing thumbnail exception',
    absByAiUrl: 'Omitted under the standing thumbnail exception',
    generatedConceptReferences: [
      '/Users/danielrose/.codex/generated_images/01a0c594-b623-7892-acd7-3003ea88c14e/exec-7df72f26-301b-487a-beb7-10981cac6f6e.png',
      '/Users/danielrose/.codex/generated_images/01a0c594-b623-7892-acd7-3003ea88c14e/exec-eabebf73-c926-4da9-b91a-9c671ca7bf23.png',
      '/Users/danielrose/.codex/generated_images/01a0c594-b623-7892-acd7-3003ea88c14e/exec-574453f2-e2c4-4bcd-a728-e877d603b6d0.png'
    ],
    results
  };
  fs.writeFileSync(path.join(OUT, 'manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);
  console.log(JSON.stringify(manifest, null, 2));
})();
