// Name the finished shorts in POSTING ORDER and copy them to the delivery folder.
//
// Prefix `zep-` - the existing prefixes in Short-form video content/ are `short` (V4),
// `v2-`, `v3-`, `v6-` and `abwheel-`, and nothing collides.
const fs = require('fs');
const path = require('path');
const { SEGMENTS } = require('./segments.js');

// Posting order. B first: it is the most self-contained beat in the video and the only one
// that works with no setup at all. Then relatable (E), stat hook (J), the thesis that sells
// the product (A), the quirky honesty hook (M), the single-product payoff (C), the
// contrarian recommendation (H), and the long philosophical one last (D).
const ORDER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];

const OUT = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content';
// Rev 2 renamed two shorts (J and M carry Dan's new titles), so clear the old delivery
// first - otherwise the folder keeps a stale supp-short3/supp-short5 alongside the new ones.
for (const f of fs.readdirSync(OUT)) if (/^zep-short\d+_/.test(f)) fs.unlinkSync(path.join(OUT, f));
const rows = [];
ORDER.forEach((id, i) => {
  const seg = SEGMENTS.find((s) => s.id === id);
  if (!seg) throw new Error(`unknown segment ${id}`);
  const src = path.join(__dirname, 'out', `${id.toLowerCase()}_${seg.slug}.mp4`);
  if (!fs.existsSync(src)) throw new Error(`missing render: ${src}`);
  const name = `zep-short${i + 1}_${seg.slug}.mp4`;
  const dst = path.join(OUT, name);
  fs.copyFileSync(src, dst);
  rows.push({ n: i + 1, id, name, title: seg.title, bytes: fs.statSync(dst).size });
});
if (new Set(ORDER).size !== SEGMENTS.length) throw new Error('ORDER does not cover every segment');
for (const r of rows) console.log(`  ${r.n}. ${r.name.padEnd(52)} ${(r.bytes / 1e6).toFixed(1)} MB  ${r.title}`);
fs.writeFileSync(path.join(__dirname, 'work', 'delivered.json'), JSON.stringify(rows, null, 1));
