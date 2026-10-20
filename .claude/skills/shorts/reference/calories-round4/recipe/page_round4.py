from pathlib import Path
import sys,json,html,shutil,hashlib
P=Path(__file__).parent;W=P.parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=W/'review';F=W/'frames'
sys.path.insert(0,str(R/'.claude/skills/_shared/framecheck'))
from gate import require_pass
for S in 'AD':require_pass(str(F/f'{S}01-start.png'),str(F/f'{S}01-end.png'))
base=(W.parent/'round3/review/index.html').read_text();style=base.split('<style>',1)[1].split('</style>',1)[0]
aside='<aside'+base.split('<aside',1)[1].split('</aside>',1)[0]+'</aside>'
rows=[];items=[];e=html.escape
for S,title,dur,line,after,change,action in [
 ('A','Why I fast until 2 pm every day.',6.2368333333,"I don't eat anything until 2 in the afternoon. Then I break my fast with a big salad and I eat dinner in the evening.","And here's why I love this.",'START: dawn with the sun rising outside, clock at 8:00 am. END: full mid-afternoon sunlight, clock at 2:00 pm.','During eventual Flow motion the hands will advance clockwise from 8 to 2, with six full minute-hand turns and a half-turn of the hour hand. Dan works without eating, then reaches on “Then I break my fast” at about 2.86 seconds and takes the salad bite.'),
 ('D','Snack on Protein, Not Carbs',2.3004666667,'Snack on protein, not on carbs.','Protein keeps you full for hours and carb snacks do the opposite.','Both lean top Dan and heavier bottom Dan are shirtless in START and END.','Arms, hands, sardine tin, fork, chip, bowls and crackers stay fixed. Both heads lean naturally forward to bite the food. Same split screen and physiques.')]:
 gid=S+'01';item={'id':gid,'title':title,'scope':'R4 revised start/end frames only; motion not generated','start_sha256':hashlib.sha256((F/f'{gid}-start.png').read_bytes()).hexdigest(),'end_sha256':hashlib.sha256((F/f'{gid}-end.png').read_bytes()).hexdigest()};items.append(item)
 for q in ['start','end']:shutil.copy2(F/f'{gid}-{q}.png',O/'frames'/f'{gid}-{q}-full.png')
 pair=''.join(f'<article><a href="frames/{gid}-{q}-full.png"><img src="frames/{gid}-{q}-composed.jpg" alt="{q.capitalize()} frame for {e(title)}"></a><p><b>{q.upper()}</b> · <a href="frames/{gid}-{q}-full.png">Full-size Image</a></p></article>' for q in ['start','end'])
 rows.append(f'''<section id="{gid}"><h2>{e(title)}</h2><p><b>{e(change)}</b></p><div class="pair">{pair}</div><p><button onclick='play({json.dumps(gid+'-frame-context.mp4')},{json.dumps(title+': Still Placeholders With Narration')})'>Hear The Opening With These Frames</button> <a href="{gid}-frame-context.mp4">Open Narrated Preview</a></p><p><b>Review:</b> 0:00 to {dur:.2f}. Both are still placeholders, not generated motion.</p><p><b>During:</b> {e(line)}</p><p><b>Next line:</b> {e(after)}</p><p><b>Intended motion:</b> {e(action)}</p><p class="note">Measured frame gate and fresh independent review passed on these exact images. Frame approval is required before Flow motion.</p><label>Frame decision <select class="decision" data-id="{gid}"><option value="pending">Pending</option><option value="approved">Approve Frames</option><option value="changes-requested">Changes Requested</option></select></label></section>''')
text='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Calories Not Losing Weight SFL R4</title><style>STYLE</style><link rel="stylesheet" href="panel.css"></head><body>ASIDE<main><h1>Calories Not Losing Weight SFL R4</h1><div class="notice">CONTENT (SFL). Two revised opening frame pairs for approval. The existing narration, timing and title treatment are preserved. No new Flow motion, covers or publishing.</div><h2>Your Decisions (2)</h2><p>Approve these revised image pairs or name what you want changed. The preview buttons play your actual opening narration over clearly labelled still placeholders.</p>ROWS<h2>Preserved</h2><p>All five selected Shorts remain. The approved sound, grade, titles, captions and timing stay as recorded. R2 and R3 files and review services were not modified. This R4 page shows only the two requested changes.</p><h2>Reply</h2><textarea id="reply">Calories Shorts R4 frame decisions:
Why I fast until 2 pm every day.: Frames approved / Changes:
Snack on Protein, Not Carbs: Frames approved / Changes:
</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy Reply</button> <button onclick="saveDecisions()">Save Decisions As JSON</button></p><p class="note">Still frames made on the Codex subscription. No paid image generation. Awaiting Dan's review of these revised images before motion.</p></main><script>const ITEMS=ITEMSJSON;</script><script src="panel.js"></script></body></html>'''
text=text.replace('STYLE',style).replace('ASIDE',aside).replace('ROWS',''.join(rows)).replace('ITEMSJSON',json.dumps(items))
# Narrated still player: exact PCM prefixes, no placeholder rendered film.
config=json.loads((W/'records/narrated-still-config.json').read_text())
text=text.replace('<video id="player" controls preload="metadata" playsinline src="A01-frame-context.mp4" poster="frames/A01-start-composed.jpg"></video>','<img id="placeholder-frame" src="frames/A01-context-00.jpg" alt="Fasting start still placeholder"><audio id="player" controls preload="metadata" src="A01-narration.wav"></audio>')
text=text.replace('A01-frame-context.mp4','A01-narration.wav').replace('D01-frame-context.mp4','D01-narration.wav').replace('Open Narrated Preview','Open Audio Only')
text=text.replace('</style>', ' aside #placeholder-frame{width:100%;max-height:48vh;object-fit:contain;display:block}aside audio{width:100%;height:36px;margin-top:8px}@media(max-width:620px){aside #placeholder-frame{grid-column:1;grid-row:1 / 7;max-height:36vh}aside audio{grid-column:2} } </style>')
preloads=''.join('<link rel="preload" as="image" href="'+slide['src']+'">' for c in config.values() for slide in c['slides'])
text=text.replace('</head>',preloads+'</head>')
(O/'index.html').write_text(text)
for p in ['panel.css','panel.js']:shutil.copy2(P/p,O/p)
js=(O/'panel.js').read_text().replace('/\\.m4a$/i', '/\\.(m4a|wav)$/i')
js += '\nconst FRAME_CONFIG = ' + json.dumps(config) + """;
const frameImage = document.getElementById('placeholder-frame');
function syncStill() {
 const id = (preview.currentSrc || preview.src).split('/').pop().split('-')[0];
 const cfg = FRAME_CONFIG[id]; if (!cfg) return;
 const t = preview.currentTime || 0;
 const slide = cfg.slides.filter(s => s.at <= t + 0.0001).pop() || cfg.slides[0];
 if (!frameImage.src.endsWith(slide.src)) frameImage.src = slide.src;
 frameImage.alt = id + ' still placeholder at ' + t.toFixed(2) + ' seconds; motion not generated';
}
['loadedmetadata','timeupdate','seeked','play','pause'].forEach(n => preview.addEventListener(n,syncStill));
function animateStill() { syncStill(); if (!preview.paused) requestAnimationFrame(animateStill); }
preview.addEventListener('play', () => requestAnimationFrame(animateStill));
syncStill();
"""
(O/'panel.js').write_text(js)
(W/'records/review-items.json').write_text(json.dumps(items,indent=2))
print('R4 page written; no old panel operated')
