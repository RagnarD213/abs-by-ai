from pathlib import Path
import json
from build import OUT,PLAN
P=OUT/'review'
css='''*{box-sizing:border-box}body{margin:0;background:#102334;color:#f3f7fa;font:17px/1.55 system-ui}main{max-width:1240px;margin:auto;padding:30px 20px}h1{font-size:34px;margin:0}p{color:#c6d6e0}a{color:#92daff}nav{display:flex;gap:12px;margin:22px 0}nav a{padding:9px 20px;background:#274658;border-radius:8px;text-decoration:none}section{background:#18364a;border:1px solid #35566a;border-radius:14px;padding:22px;margin:24px 0}.pair{display:grid;grid-template-columns:1fr 1fr .7fr;gap:20px;align-items:start}figure{margin:0;min-width:0}figcaption{font-size:14px;margin-bottom:8px}img{width:100%;height:auto;display:block;border-radius:6px}.overview{max-width:1100px}h2{margin-top:0}@media(max-width:700px){main{padding:20px 12px}.pair{grid-template-columns:1fr 1fr;gap:12px}.grid{grid-column:1/3;max-width:230px}h1{font-size:28px}}'''
h=[f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Home Workouts: Four Real Photo Covers</title><style>{css}</style></head><body><main><h1>Home Workouts: Four Real Photo Designs</h1><p>Round 2. Four different exercise photos from your real pool shoot, each with a different design. Every choice has an Instagram layout, a YouTube Shorts layout and an Instagram profile-grid crop.</p><p>The approved film is unchanged. Choose 1, 2, 3 or 4 in this chat to continue setup.</p><nav>']
for k in PLAN['designs']:h.append(f'<a href="#R2-{k}">{k}</a>')
h.append('</nav><a href="four-cover-choices.jpg"><img class="overview" src="four-cover-choices.jpg" alt="All four real photo cover choices, Instagram and YouTube paired"></a>')
for k,spec in PLAN['designs'].items():
    h.append(f'<section id="R2-{k}"><h2>{k}: {spec["action"]}</h2><div class="pair">')
    for pf,title in [('instagram','Instagram'),('youtube','YouTube Shorts'),('grid','Instagram Profile Crop')]:
        h.append(f'<figure class="{"grid" if pf=="grid" else ""}"><figcaption>{title}</figcaption><a href="R2-{k}-{pf}.jpg"><img loading="lazy" src="R2-{k}-{pf}.jpg" alt="Design {k}: {title}"></a></figure>')
    h.append('</div></section>')
h.append('<p>Reply with your chosen number. Your full-film approval is already recorded.</p></main></body></html>')
(P/'index.html').write_text(''.join(h));print('Four-choice review prepared')

# Keep the owned durable URL on its registered directory; archive the old HTML first.
import shutil
LIVE=OUT.parent/'blind-review'
if not (LIVE/'index-round1-preserved.html').exists():shutil.copy2(LIVE/'index.html',LIVE/'index-round1-preserved.html')
for f in P.iterdir():
    if f.is_file() and not f.name.startswith('._') and 'text-mask' not in f.name and 'person-mask' not in f.name:
        shutil.copy2(f,LIVE/f.name)
print('Updated owned live root, preserving initial choices')
