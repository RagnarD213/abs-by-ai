#!/usr/bin/env python3
"""Round 3 (Dan, 2026-10-16): Dan picked F; only the woman's outfit changes, no cover-up. F2 = one-piece swimsuit
(Codex edit of the F plate). F1 = black bikini: Codex's filter refused it four times, and on Replicate Nano Banana Pro and
Seedream 4 refused it too; FLUX Kontext Pro edited the F2 plate (Dan asked for Replicate by name, 2026-10-16).
Builds F1 and F2 in both layouts with F's yellow band, appends to manifest.json."""
from pathlib import Path
import json,importlib.util
from PIL import Image
spec=importlib.util.spec_from_file_location('ds05build',Path(__file__).resolve().parent/'build.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);b=m.b
k='ds-05';slug=b.COPY[k][2];mp=b.R/'manifest.json';man=json.loads(mp.read_text())
KIND={'F1':'F with a black bikini, no cover-up (FLUX Kontext Pro edit)','F2':'F with a one-piece swimsuit, no cover-up'}
man['outputs']=[r for r in man['outputs'] if r['variant'] not in KIND]
for v in KIND:
 for pl in ['instagram','youtube']:
  im,gp=b.plate(k,v.lower(),False);tm=Image.new('L',(b.W,b.H));b.copy_band(im,tm,k,pl=='instagram')
  p=b.R/pl/f'{slug}_cover-{v}.png';im.convert('RGB').save(p);tm.save(p.with_name(p.stem+'.text-mask.png'))
  man['outputs'].append(dict(short=k,variant=v,platform=pl,path=str(p),sha256=b.sha(p),kind=KIND[v],copy={'badge':b.COPY[k][0],'headline':b.COPY[k][1]},plate=str(gp)))
mp.write_text(json.dumps(man,indent=1)+'\n');print('built F1, F2')
