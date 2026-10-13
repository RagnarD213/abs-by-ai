#!/usr/bin/env python3
"""Round 2 (Dan, 2026-10-13): two new AI designs each for 200 Pounds At 38 (Dan made heavy, bleak scene) and
Make Time To Work Out (ripped Dan conjuring a clock). F and G, both layouts. Reuses the type layouts in build.py."""
from pathlib import Path
import sys,json
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent));import build as b
LAY={('ds-08','F'):b.copy_bottom,('ds-08','G'):b.copy_band,('ds-09','F'):b.copy_band,('ds-09','G'):b.copy_bottom}
rec=[]
for (k,v),fn in LAY.items():
 for pl in ['instagram','youtube']:
  im,gp=b.plate(k,v.lower(),False);tm=Image.new('L',(b.W,b.H));fn(im,tm,k,pl=='instagram')
  p=b.R/pl/f'{b.COPY[k][2]}_cover-{v}.png';im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'));rec.append(str(p))
  im.convert('RGB').resize((540,960),Image.Resampling.LANCZOS).save(b.R/'web'/f'{b.COPY[k][2]}_{v}_{pl}.jpg',quality=88)
(b.R/'round2.json').write_text(json.dumps(rec,indent=1));print('built',len(rec))
