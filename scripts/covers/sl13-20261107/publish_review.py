from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,hashlib,html,shutil,socket
w=Path(__file__).parent;root=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');blind=root/'.claude/skills/_shared/blind-image/blind.py'
rows=json.loads((w/'layout-manifest-private.json').read_text());assert len(rows)==42 and not any(r['face_hair_text_pixels'] for r in rows)
public=root/'Short-form video content/covers/review/sl13-20261107';public.mkdir(parents=True,exist_ok=True)
titles={'A':'Eat Protein First To Keep Muscle While Losing Fat','B':'Eat Less Without Counting Every Calorie','C':'Keep Your Steps Up While You Diet'}
entries=[]
for k in 'ABC':
 sd=w/'blind-sets'/k;sd.mkdir(parents=True,exist_ok=True)
 ig=[r for r in rows if r['short']==k and r['platform']=='instagram']
 if not (sd/'.blind-key.json').exists():
  for r in ig:
   args=['python3',str(blind),'add',str(sd),'--source',r['origin'],'--file',r['path'],'--note',r['id']]
   if r['style']=='real':args+=['--not-comparison']
   subprocess.run(args,check=True,capture_output=True)
  args=['python3',str(blind),'build',str(sd),'--kind','cover','--video','Calories Dont Matter Shorts','--shot',titles[k]]
  if k=='C':args+=['--comparison-unavailable',str(w/'google/google-refusals.txt')]
  subprocess.run(args,check=True,capture_output=True)
 key=json.loads((sd/'.blind-key.json').read_text())
 for label,info in key['labels'].items():
  r=next(r for r in ig if hashlib.sha256(Path(r['path']).read_bytes()).hexdigest().startswith(info['sha']))
  for platform in ['instagram','youtube']:
   native=next(x for x in rows if x['short']==k and x['id']==r['id'] and x['platform']==platform)
   d=public/k/platform;d.mkdir(parents=True,exist_ok=True)
   image=Image.open(native['path']).convert('RGB');image.resize((940,1672),Image.Resampling.LANCZOS).save(d/(label+'.jpg'),quality=93)
   # Review copies have common resolution and stripped metadata. Originals remain immutable for installation.
  entries.append({'short':k,'label':label,'instagram':f'{k}/instagram/{label}.jpg','youtube':f'{k}/youtube/{label}.jpg'})
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#0b1320;color:#f2f6fc;font:16px/1.5 system-ui,sans-serif}header,main{max-width:1180px;margin:auto;padding:22px 16px}h1{font-size:30px;line-height:1.15;margin:12px 0}h2{font-size:24px;line-height:1.2;margin:12px 0 20px}p{color:#b9c7da;max-width:780px}nav{display:flex;flex-wrap:wrap;gap:10px;position:sticky;top:0;background:#0b1320f2;padding:14px 16px;z-index:10;border-bottom:1px solid #2d3c50}a{color:#82d6ff}nav a{border:1px solid #3e566f;border-radius:8px;padding:7px 12px;text-decoration:none}.grid{display:grid;grid-template-columns:1fr;gap:22px}article{padding:14px;border:1px solid #334158;border-radius:14px;background:#111e30}h3{margin:0 0 10px;color:#8cdeff;font-size:25px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}figure{margin:0;min-width:0}figcaption{font-size:13px;font-weight:700;padding:6px 0 10px}img{display:block;width:100%;height:auto;border-radius:5px}.ig{position:relative}.ig:after{content:"";position:absolute;left:0;right:0;top:12.5%;bottom:12.5%;border-top:1px dashed #fff9;border-bottom:1px dashed #fff9;pointer-events:none}section{scroll-margin-top:90px;margin-bottom:55px}.count{color:#86a3c6;font-size:14px}.legend{background:#15263b;border-left:3px solid #3fc1ff;padding:12px 16px;border-radius:5px}.badge{color:#7fe0cb;font-size:13px;letter-spacing:.08em;font-weight:700}.footer{border-top:1px solid #334158;margin-top:36px;padding-top:20px}@media(min-width:820px){.grid{grid-template-columns:1fr 1fr}header{padding-top:34px}h1{font-size:40px}}'''
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Calories Dont Matter: Cover Choices</title><style>'+css+'</style><header><div class="badge">COVER REVIEW · AWAITING YOUR PICKS</div><h1>Calories Don’t Matter Shorts</h1><p>Choose one design for each Short. Every option shows the Instagram layout first, then the YouTube Shorts layout. Click either image for a larger view.</p><p class="legend">The dashed lines show the Instagram profile-grid crop. Check the face, the action, the headline and how the image reads at phone size. Reply with three picks, for example: <strong>Protein X2, Eat Less X4, Steps X1.</strong></p></header><nav><a href="#A">Protein</a><a href="#B">Eat Less</a><a href="#C">Steps</a></nav><main>']
for k in 'ABC':
 subset=[e for e in entries if e['short']==k]
 parts.append(f'<section id="{k}"><div class="count">{len(subset)} choices</div><h2>{html.escape(titles[k])}</h2><div class="grid">')
 for e in subset:
  parts.append(f'<article id="{k}-{e["label"]}"><h3>{e["label"]}</h3><div class="pair">')
  for platform,name in [('instagram','Instagram'),('youtube','YouTube Shorts')]:
   url=e[platform];parts.append(f'<figure><figcaption>{name}</figcaption><a class="{"ig" if platform=="instagram" else ""}" style="display:block" href="{url}" target="_blank" rel="noopener"><img src="{url}" loading="lazy" width="940" height="1672" alt="{html.escape(titles[k])}, {e["label"]}, {name}"></a></figure>')
  parts.append('</div></article>')
 if k=='C':parts.append('</div><p class="count">Three additional comparison images were unavailable because the image service returned repeated errors. The five main designs are complete.</p></section>')
 else:parts.append('</div></section>')
parts.append('<div class="footer"><p>The three R2 films are approved. These covers are awaiting your selection. Descriptions and backup checks are prepared separately. No covers have been installed and no Shorts have been scheduled.</p></div></main></html>')
(public/'index.html').write_text(''.join(parts))
(w/'neutral-review-manifest.json').write_text(json.dumps(entries,indent=2))
# Compact paired sheets are also available as a local fallback.
for k in 'ABC':
 sub=[e for e in entries if e['short']==k];cw,ch=480,485;cols=2
 s=Image.new('RGB',(cols*cw,((len(sub)+1)//2)*ch),'#111e30');d=ImageDraw.Draw(s);f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',21)
 for i,e in enumerate(sub):
  x=(i%cols)*cw;y=(i//cols)*ch;d.text((x+10,y+3),e['label']+'  Instagram | YouTube',font=f,fill='#8cdeff')
  for j,plat in enumerate(['instagram','youtube']):
   im=Image.open(public/e[plat]);im.thumbnail((235,418));s.paste(im,(x+j*240,y+38))
 s.save(public/f'{k}-choices.jpg',quality=94)
print('Review built:',public,'21 choices / 42 layouts')
