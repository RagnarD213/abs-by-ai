#!/usr/bin/env python3
from pathlib import Path
import shutil,json
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'Short-form video content/covers/review/ds52-zepbound-free-20261102';R=BASE/'r2';P=BASE/'blind-review';D=P/'designs-r2';D.mkdir(exist_ok=True)
old=P/'original-eight.html'
if not old.exists():shutil.copy2(P/'index.html',old)
shutil.copy2(R/'four-designs.jpg',D/'four-designs.jpg');shutil.copy2(R/'profile-crops.jpg',D/'profile-crops.jpg')
m=json.loads((R/'manifest.json').read_text())
for row in m['outputs']:
 p=ROOT/row['path'];shutil.copy2(p.with_suffix('.jpg'),D/f"Design-{row['design']}-{row['platform']}.jpg")
for n in range(1,5):shutil.copy2(R/f'Design-{n}-profile.jpg',D/f'Design-{n}-profile.jpg')
labels={1:'Cobalt Signal',2:'Editorial Split',3:'Savings Receipt',4:'Red Contrast'}
notes={1:'Electric blue, oversized lime type and a larger portrait.',2:'Warm paper, serif headline, offset portrait and a large red payoff.',3:'Deep green, a framed portrait and a receipt-inspired headline.',4:'Sharp red-and-black contrast, angled architecture and a large portrait.'}
css='''*{box-sizing:border-box}body{margin:0;background:#101722;color:#f6f7fa;font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1260px;margin:auto;padding:32px 22px}h1{font-size:35px;line-height:1.15;margin:0 0 14px}p{max-width:880px;color:#c5d0df}a{color:#8ed4ff}.note{padding:16px 22px;background:#1d2c40;border-left:4px solid #b3ef41;margin:22px 0}section{background:#182333;padding:24px;border-radius:12px;border:1px solid #344357;margin:26px 0}h2{margin:0;font-size:25px}.pair{display:grid;grid-template-columns:1fr 1fr .74fr;gap:20px;align-items:start}figure{margin:0;min-width:0}figcaption{font-size:14px;color:#becadc;margin:8px 0}img{width:100%;height:auto;display:block;border-radius:5px}nav{display:flex;gap:12px;margin:24px 0}nav a{background:#263a53;padding:8px 18px;border-radius:7px;text-decoration:none}small{color:#b4c0d0}@media(max-width:700px){main{padding:24px 12px}section{padding:16px}.pair{grid-template-columns:1fr 1fr;gap:12px}.profile{grid-column:1/3;max-width:240px}h1{font-size:28px}}'''
h=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Zepbound Free: Four Revised Designs</title><style>{css}</style></head><body><main><h1>Same X3 Image. Four New Designs.</h1><p>Why Zepbound Is Actually Free</p><div class="note">Your chosen image is unchanged. These are four different layouts using that same face, pose, pen and cash. No new image generation. My recommendation: <strong>1</strong> for the strongest feed impact, or <strong>3</strong> for the clearest money-saving theme.</div><p>Each option shows Instagram, YouTube Shorts and the actual Instagram profile crop. Choose a design number in this chat. Nothing has been installed, uploaded or scheduled. Your approved R3 film remains unchanged.</p><nav>']
for n in range(1,5):h.append(f'<a href="#design-{n}">{n}</a>')
h.append('</nav><a href="designs-r2/four-designs.jpg"><img src="designs-r2/four-designs.jpg" alt="Four revised designs in both platform layouts"></a>')
for n in range(1,5):
 h.append(f'<section id="design-{n}"><h2>{n}. {labels[n]}</h2><p>{notes[n]}</p><div class="pair">')
 for p,label in [('instagram','Instagram'),('youtube','YouTube Shorts'),('profile','Instagram Profile Crop')]:
  h.append(f'<figure class="{"profile" if p=="profile" else ""}"><figcaption>{label}</figcaption><a href="designs-r2/Design-{n}-{p}.jpg"><img loading="lazy" src="designs-r2/Design-{n}-{p}.jpg" alt="Design {n}: {label}"></a></figure>')
 h.append('</div></section>')
h.append('<p><a href="original-eight.html">Earlier eight options</a></p><p>After your exact revised-design pick, backups and platform setup continue in this same chat.</p></main></body></html>')
(P/'index.html').write_text(''.join(h));print('Updated existing review page; first-round options archived intact.')
