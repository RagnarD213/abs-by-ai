"""A2 selected-cover photograph revision. Preserve the R2 cyan design exactly.

Load only the frozen R2 helper definitions, without executing its assembly.
Input photo is the explicitly authorized AI-assisted correction of B0449.
"""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
import numpy as np

ROOT=Path(__file__).resolve().parents[4]
R=Path('/Volumes/Extreme/_edit_work/SL-12/setup/round3')
PREV=R.parent/'round2'
helper=ROOT/'scripts/covers/sl12-20261108/round2/build.py'
ns={'__file__':str(helper),'__name__':'sl12_r2_helpers'}
exec(compile(helper.read_text().split('\nrows=[]\n')[0],str(helper),'exec'),ns)
ns['R']=R
B=ns['B'];W,H=1080,1920

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

source=R/'A2-photo-edit-1.jpg'
photo=Image.open(source).convert('RGB')
# Keep the source's photographic correction, avoiding a second full contrast pass.
# The selected design's exact headline, framing and output geometry are reused.
photo=photo.resize((W,round(photo.height*W/photo.width)),Image.Resampling.LANCZOS)
rows=[]
for platform in ['instagram','youtube']:
    ig=platform=='instagram';mask=Image.new('L',(W,H));im=Image.new('RGBA',(W,H),(7,17,29,255))
    bottom=ns['headline'](Image.new('RGBA',(W,H)),Image.new('L',(W,H)),'cyan',ig)
    y=bottom+45
    im.alpha_composite(photo.convert('RGBA'),(0,y))
    ns['headline'](im,mask,'cyan',ig)
    ImageDraw.Draw(im).rectangle((22,22,W-23,H-23),outline=B.CYAN,width=4)
    row=ns['save'](im,mask,'A2',platform,{'photo_source':str(source),'photo_sha256':sha(source),
          'picture_top':y,'source_type':'AI-assisted correction of real B0449 screenshot at3.4s',
          'source_reference':str(R/'A2-base-photo.jpg'),'edits_requested':['even dumbbells','relaxed closed-mouth expression','eyes toward camera'],
          'approval':'Dan selected A2 design; exact photo revision awaits approval'})
    oldmask=Image.open(PREV/'covers/A2'/(platform+'.text-mask.png'))
    assert np.array_equal(np.asarray(mask),np.asarray(oldmask)),'Selected headline design changed'
    rows.append(row)

# B is retained exactly as last delivered. Only its YouTube file is approved.
import shutil
(R/'covers/BX2').mkdir(parents=True,exist_ok=True)
for name in ['instagram.png','instagram.jpg','youtube.png','youtube.jpg','profile.jpg']:
    a=PREV/'covers/BX2'/name;b=R/'covers/BX2'/name;shutil.copyfile(a,b);assert sha(a)==sha(b)
for platform in ['instagram','youtube']:
    p=R/'covers/BX2'/(platform+'.png')
    rows.append({'label':'BX2','platform':platform,'path':str(p),'sha256':sha(p),'jpeg':str(p.with_suffix('.jpg')),'jpeg_sha256':sha(p.with_suffix('.jpg')),
        'approval':'approved original' if platform=='youtube' else 'unchanged revised Instagram, awaits approval'})
(R/'manifest.json').write_text(json.dumps({'round':3,'date':'2026-11-09','status':'A2 chosen; revised photograph awaits exact-file approval','outputs':rows,'headline_masks_identical_to_R2':True,'B_both_layouts_identical_to_R2':True},indent=2)+'\n')
print('A2 paired layouts built; exact headline masks and both B files preserved.')
