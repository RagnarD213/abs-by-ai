"""RA-R2A in 1:1 (1080x1080). Same photo, scene, copy and type as the approved 16:9 and 9:16.
Reuses the round 1 functions without running its builder, and the existing Codex-generated ra01-C plate
(no new image generation). Writes only to round2-square/."""
from pathlib import Path
import ast,copy,json,sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
P=ROOT/'social media graphics/youtube/thumbnails/_trial-campaign-20261001'
OUT=P/'round2-square'; OUT.mkdir(exist_ok=True)
source=ROOT/'scripts/covers/trial-campaign-20261001/build.py'
tree=ast.parse(source.read_text());tree.body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.Assign)) and not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['ROOT','records'] for t in n.targets))]
ns={'ROOT':ROOT,'__file__':str(source)};exec(compile(tree,str(source),'exec'),ns)
ADS={a['id']:a for a in ns['ADS']}
a=copy.deepcopy(ADS['ra01']);slot='C';i=2
a['photos'][i]='studio-blue-53';a['waist'][i]=.80
size=(1080,1080)
variant=sys.argv[1] if len(sys.argv)>1 else 'scene'
if variant=='generic':
    im=ns['backdrop'](a,slot,size)
else:
    im=ns['gradient'](size,(9,11,14),(24,27,31))
    scene=Image.open(P/'generated/ra01-C.png').convert('RGBA')
    sw=1130;scene=scene.resize((sw,int(scene.height*sw/scene.width)),Image.Resampling.LANCZOS)
    alpha=Image.new('L',scene.size,255);fade=ImageDraw.Draw(alpha)
    for yy in range(100):fade.line((0,yy,sw,yy),fill=int(255*yy/99))
    scene.putalpha(alpha)
    im.alpha_composite(scene,(0,1080-scene.height+20))
layer,person,info=ns['place_person'](a,slot,size)
im.alpha_composite(layer);tm,ti=ns['type_block'](a,slot,im,person);info.update(ti)
assert info['text_person_overlap']==0
path=OUT/f'RA-R2A-1x1-{variant}.jpg'
im.convert('RGB').save(path,quality=94,subsampling=0)
print(path,info['font_size'],info['text_bbox'],info['output_box'],path.stat().st_size)
