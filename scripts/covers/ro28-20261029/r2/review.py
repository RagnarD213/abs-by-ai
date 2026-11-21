from pathlib import Path
import shutil,json
HERE=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI/social media graphics/youtube/thumbnails/Why Zepbound Improves Your Health Even If Youre Ripped/_build-2026-10-29/r2')
OUT=HERE.parents[1]
qc=json.loads((HERE/'qc.json').read_text())
assert len(qc)==3 and all(r['pass'] for r in qc)
old=OUT/'index-round1.html'
if not old.exists():shutil.copy2(OUT/'index.html',old)
labels={'A1':('1: Confident Half-Smile','Yellow headline stack, pharmacy scene on the right.'),'A2':('2: Playful Surprise','A more animated expression, navy and cyan headline on the right.'),'A3':('3: Broad Smile','A yellow headline banner over the pharmacy scene.')}
cards=''
for r in qc:
 title,note=labels[r['choice']]
 cards+=f'<article><h2>{title}</h2><a href="{r["file"]}" target="_blank"><img src="{r["file"]}" alt="{title}"></a><p>{note}</p><a href="{r["file"]}" target="_blank">Open Full Size</a></article>'
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Why Ripped Men Should Take Zepbound: Three Thumbnail Designs</title><style>body{margin:0;background:#0c1520;color:#eef3f8;font:17px/1.5 system-ui}main{max-width:1480px;margin:auto;padding:24px}h1{font-size:30px;max-width:1150px}h2{font-size:23px;margin:0 0 12px}a{color:#65dce9}header{margin-bottom:28px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}article{background:#152333;border:1px solid #314354;border-radius:12px;padding:18px}img{display:block;width:100%;height:auto}p{color:#d4e0ea}footer{margin:28px 0 60px}@media(max-width:850px){.grid{grid-template-columns:1fr}main{padding:14px}h1{font-size:26px}}</style><main><header><h1>Why Ripped Men Should Take Zepbound</h1><p>Three new designs based on your preferred pharmacy concept A.</p><p>Your requested changes: a small recognizable Zepbound vial, stronger expressions, more defined abs, and the new headline.</p><p><b>Choose 1, 2 or 3.</b> These revised thumbnails are awaiting your review. Nothing installed or scheduled.</p></header><div class="grid">'''+cards+'''</div><footer><p><a href="REVIEW-three-revised-thumbnails.jpg" target="_blank">Compare All Three On One Sheet</a></p><p><a href="index-round1.html" target="_blank">Previous Five Choices</a></p><p>Vial appearance reference: <a href="https://www.lilly.com/news/media/zepbound" target="_blank">Lilly's official product image</a>.</p></footer></main></html>'''
(OUT/'index.html').write_text(html)
(OUT/'index-r2.html').write_text(html)
print('Three revised designs published to review files')
