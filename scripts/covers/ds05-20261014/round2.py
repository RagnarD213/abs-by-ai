#!/usr/bin/env python3
"""Round 2 (Dan, 2026-10-16): two new AI designs of one concept. Ripped Dan walking a beach road in swim trunks with a fit
woman in a bikini, while a fat millionaire in his convertible looks on, miserable and envious.
F: yellow band on top (couple walking toward camera). G: headline at the bottom (over the rich man's shoulder).
Builds both layouts, appends to manifest.json, and adds a round 2 section to the top of index.html."""
from pathlib import Path
import json,sys,importlib.util
from PIL import Image
spec=importlib.util.spec_from_file_location('ds05build',Path(__file__).resolve().parent/'build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);b=m.b
LAY={'F':b.copy_band,'G':b.copy_bottom}
DESC={'F':'AI you and her walking toward the camera on a beach road; the rich guy watches from his convertible (yellow band on top)',
 'G':'Same idea from over the rich guy\'s shoulder: his envious face up front, you two walking past (headline at the bottom)'}
k='ds-05';slug=b.COPY[k][2];mp=b.R/'manifest.json';man=json.loads(mp.read_text())
man['outputs']=[r for r in man['outputs'] if r['variant'] not in LAY]
for v,fn in LAY.items():
 for pl in ['instagram','youtube']:
  im,gp=b.plate(k,v.lower(),False);tm=Image.new('L',(b.W,b.H));fn(im,tm,k,pl=='instagram')
  p=b.R/pl/f'{slug}_cover-{v}.png';im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
  im.convert('RGB').resize((540,960),Image.Resampling.LANCZOS).save(b.R/'web'/f'{slug}_{v}_{pl}.jpg',quality=88)
  man['outputs'].append(dict(short=k,variant=v,platform=pl,path=str(p),sha256=b.sha(p),kind='Round 2 AI design: '+DESC[v],copy={'badge':b.COPY[k][0],'headline':b.COPY[k][1]},plate=str(gp)))
mp.write_text(json.dumps(man,indent=1)+'\n')
idx=b.R/'index.html';h=idx.read_text();mark='<!--round2-->'
if mark in h:h=h[:h.index(mark)]+h[h.index('<!--/round2-->')+len('<!--/round2-->'):]
cards=''.join(f'<div class="c"><b>{v}: New design {i+1}</b><small>{DESC[v]}</small><div class="pair">'+''.join(f'<figure><a href="web/{slug}_{v}_{pl}.jpg" target="_blank"><img src="web/{slug}_{v}_{pl}.jpg"></a><figcaption>{"Instagram" if pl=="instagram" else "YouTube"}</figcaption></figure>' for pl in ['instagram','youtube'])+'</div></div>' for i,v in enumerate(LAY))
sec=f'{mark}<h2 style="color:#40dcff">Round 2: your beach idea, two designs (F and G)</h2><p>Ripped you in swim trunks walking a beach road with a fit woman in a swimsuit, while the fat millionaire sits in his car looking miserable and envious. Pick any letter from A to G, or two for a YouTube A/B test.</p><div class="row" style="grid-template-columns:repeat(2,minmax(0,420px))">{cards}</div><h2 style="color:#fff">Round 1 (still available)</h2><!--/round2-->'
i=h.index('<h2 style="color:#fff">What I decided');idx.write_text(h[:i]+sec+h[i:]);print('built F, G')
