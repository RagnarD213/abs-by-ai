from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,html
r=Path(__file__).resolve().parents[3]/'Short-form video content/covers/review/sl05-covers-20261001'
p=r.parents[4]; f='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
font=lambda s:ImageFont.truetype(f,s)
kinds=['A: Pool','B: Studio, red gym','C: Studio, blue gym','D: Video screenshot','E: Designer choice']
records=json.loads((r/'manifest.json').read_text())['outputs']
for platform in ['instagram','youtube']:
 im=Image.new('RGB',(1550,2940),(18,23,31));d=ImageDraw.Draw(im)
 d.text((30,20),'SL-05 STOP DEADLIFTING: FIVE OPTIONS PER SHORT',font=font(39),fill='white')
 d.text((30,72),('Instagram: profile grid safe' if platform=='instagram' else 'YouTube: taller photo layout')+' | Pick one letter for shorts 1, 2, 3, 4 and 5',font=font(27),fill=(185,198,209))
 for row,n in enumerate([1,2,3,4,5]):
  y=130+row*560;d.text((30,y),f'SHORT {n}',font=font(29),fill='white')
  for col,v in enumerate('ABCDE'):
   x=30+col*300
   d.text((x,y+41),kinds[col],font=font(22),fill=(213,228,238))
   file=next(Path(a['path']) for a in records if a['short']==n and a['variant']==v and a['platform']==platform)
   im.paste(Image.open(file).resize((270,480),Image.Resampling.LANCZOS),(x,y+78))
 im.save(r/f'REVIEW_sl05_five-options_{platform}.jpg',quality=96)
# One paired review per short with both platform versions and literal Instagram grid crops.
for n in [1,2,3,4,5]:
 im=Image.new('RGB',(2870,1090),(18,23,31));d=ImageDraw.Draw(im)
 d.text((24,14),f'SHORT {n}: INSTAGRAM + YOUTUBE PER OPTION',font=font(36),fill='white')
 for i,v in enumerate('ABCDE'):
  x=24+i*568;d.text((x,66),kinds[i],font=font(25),fill='white')
  for j,platform in enumerate(['instagram','youtube']):
   file=next(Path(a['path']) for a in records if a['short']==n and a['variant']==v and a['platform']==platform)
   xx=x+j*278;d.text((xx,107),'Instagram' if j==0 else 'YouTube',font=font(21),fill=(180,195,211));im.paste(Image.open(file).resize((270,480),Image.Resampling.LANCZOS),(xx,140))
   if j==0:im.paste(Image.open(file).crop((0,240,1080,1680)).resize((270,360),Image.Resampling.LANCZOS),(xx,686));d.text((xx,646),'Instagram grid crop',font=font(20),fill=(180,195,211))
 im.save(r/f'REVIEW_short{n}_paired.jpg',quality=95)
# Accessible local gallery: review images, with each original export linked.
page=['<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SL-05 cover choices</title><style>body{margin:0;background:#111820;color:#f3f7fb;font:16px Arial;padding:24px}h1{font-size:28px}nav{display:flex;gap:20px;flex-wrap:wrap;margin:20px 0}a{color:#8ce5ff}section{margin:48px 0}section>img{width:100%;max-width:1800px}div.options{display:grid;grid-template-columns:repeat(5,minmax(230px,1fr));gap:14px;overflow:auto}article h3{font-size:18px}div.pair{display:flex;gap:8px}div.pair img{width:100%;max-width:270px}div.pair a{width:50%}small{color:#bcc9d3}</style></head><body><h1>SL-05 Stop Deadlifting: five cover options per short</h1><p>A: pool. B: studio, red gym. C: studio, blue home gym. D: enhanced video screenshot. E: clean editorial.</p><h2>What I decided (overrule anything)</h2><p>Approved short copy throughout. Real studio portraits on red barbell and blue safer-machine scene plates, without repainting you. Enhanced authentic parent-video screenshots preserve the black tank top, glasses and gesture; short 4 shows the lat demonstration. Pool and editorial choices emphasize abs. Final exports wait for your picks.</p><p>Each option includes Instagram and YouTube versions. Click a cover to view the full file. Reply with five picks, for example: 1A, 2B, 3C, 4D, 5E. Final exports wait for your picks. Nothing uploaded or scheduled.</p><nav>'+''.join(f'<a href="#short{n}">Short {n}</a>' for n in [1,2,3,4,5])+'<a href="REVIEW_sl05_five-options_instagram.jpg">Instagram review sheet</a><a href="REVIEW_sl05_five-options_youtube.jpg">YouTube review sheet</a></nav>']
for n in [1,2,3,4,5]:
 page.append(f'<section id="short{n}"><h2>Short {n}</h2><div class="options">')
 for i,v in enumerate('ABCDE'):
  page.append(f'<article><h3>{html.escape(kinds[i])}</h3><small>Instagram | YouTube</small><div class="pair">')
  for platform in ['instagram','youtube']:
   file=next(Path(a['path']) for a in records if a['short']==n and a['variant']==v and a['platform']==platform);url=file.relative_to(r).as_posix();page.append(f'<a href="{url}" target="_blank"><img src="{url}" alt="Short {n} option {v}, {platform}"></a>')
  page.append('</div></article>')
 page.append(f'</div><p><a href="REVIEW_short{n}_paired.jpg">Paired review and Instagram grid crops</a></p></section>')
page.append('</body></html>')
(r/'index.html').write_text(''.join(page))
print('Created two full review sheets, five paired sheets and gallery.')
