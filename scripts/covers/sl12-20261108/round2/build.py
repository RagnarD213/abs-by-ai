"""Four unique real lifting screenshots, plus the B X2 Instagram repair.

Photographic adjustments only. Reuses the DS77 real-frame touch-up and SL08
font/measurement helpers. No image generation, fabricated physique or new pose.
"""
from pathlib import Path
import sys,json,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[4]
R=Path('/Volumes/Extreme/_edit_work/SL-12/setup/round2')
sys.path.insert(0,str(ROOT/'scripts/covers/sl08-20261025'))
import build as B
spec=importlib.util.spec_from_file_location('real_touchup',ROOT/'scripts/covers/ds77-20261105/real_build.py')
T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
W,H=1080,1920
COPY=['Lift Weights On','Weight Loss Medication']
CROPS={'A1':(1100,330,2750,2160),'A2':(590,0,1330,1080),
       'A3':(1480,250,2800,2160),'A4':(500,0,1420,1080)}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def headline(im,mask,style,ig):
    top=262 if ig else 90
    if style=='yellow':
        f=B.common(COPY,B.DIN,190,965);step=round(f.size*1.10)
        bottom=top+step*2+30
        B.box(im,mask,(0,top-20,W,bottom),B.YEL)
        for n,line in enumerate(COPY):B.text(im,mask,(54,top+n*step),line,f,B.INK if n==0 else (180,25,25))
        return bottom
    if style=='ivory':
        f=B.common(COPY,B.FUTURA,145,950);step=round(f.size*1.2)
        bottom=top+step*2+40
        B.box(im,mask,(24,top-20,W-24,bottom),(242,237,222),18)
        for n,line in enumerate(COPY):B.text(im,mask,(540,top+n*step),line,f,B.INK,anchor='ma')
        ImageDraw.Draw(im).rectangle((420,bottom-16,660,bottom-8),fill=(180,30,28))
        return bottom
    f=B.common(COPY,B.IMPACT,180,960,4);step=round(f.size*1.16)
    for n,line in enumerate(COPY):B.text(im,mask,(58,top+n*step),line,f,B.WHITE if n==0 else B.CYAN,4)
    ImageDraw.Draw(im).rectangle((58,top-18,270,top-10),fill=B.CYAN)
    return top+2*step+35

def picture(crop,w=1080):
    return crop.resize((w,round(crop.height*w/crop.width)),Image.Resampling.LANCZOS)

def audit(im,mask,key,platform):
    _,faces=B.person_mask(im)
    assert faces,(key,platform,'face detection missing')
    a=np.asarray(mask)>0;guards=[]
    for f in faces:
        x0,y0,x1,y1=map(int,f);hh=y1-y0
        g=[max(0,x0-18),max(0,y0-round(hh*.5)),min(W,x1+18),min(H,y1+18)]
        guards.append(g)
        assert a[g[1]:g[3],g[0]:g[2]].sum()==0,(key,platform,'text on face/hair',g)
    bounds=mask.getbbox();assert bounds
    assert bounds[1]>=(240 if platform=='instagram' else 40) and bounds[3]<=(1630 if platform=='instagram' else 1850),(key,platform,bounds)
    return {'text_bounds':bounds,'faces':faces,'hair_guards':guards,'text_face_hair_pixels':0}

def save(im,mask,key,platform,info):
    dest=R/'covers'/key;dest.mkdir(parents=True,exist_ok=True)
    p=dest/(platform+'.png');im.convert('RGB').save(p)
    im.convert('RGB').save(p.with_suffix('.jpg'),quality=94)
    assert p.with_suffix('.jpg').stat().st_size<2_000_000
    mask.save(dest/(platform+'.text-mask.png'))
    if platform=='instagram':im.convert('RGB').crop((0,240,W,1680)).save(dest/'profile.jpg',quality=94)
    return {'label':key,'platform':platform,'path':str(p),'sha256':sha(p),'jpeg':str(p.with_suffix('.jpg')),'jpeg_sha256':sha(p.with_suffix('.jpg')),**audit(im,mask,key,platform),**info}

rows=[]
for entry in json.loads((R/'selected-sources.json').read_text()):
    key=entry['label'];original=Image.open(entry['original']).convert('RGB')
    # Same real pixels/geometry: exposure, restrained S-curve, saturation and clarity.
    rgb=np.asarray(original).astype(np.uint16)*257
    retouched=Image.fromarray(T.to8(T.touchup(rgb)))
    retouched.save(R/'sources'/(key+'-touched-up.png'))
    crop=retouched.crop(CROPS[key]);photo=picture(crop)
    for platform in ['instagram','youtube']:
        ig=platform=='instagram';mask=Image.new('L',(W,H));im=Image.new('RGBA',(W,H),(7,17,29,255))
        if entry['style']=='bottom':
            # Hair at the top of the source has room inside the Instagram crop.
            y=270 if ig else 120;im.alpha_composite(photo.convert('RGBA'),(0,y))
            B.ramp(im,1100 if ig else 1260,1290 if ig else 1460,255,top_dark=False)
            lines=['Lift Weights On','Weight Loss','Medication']
            f=B.common(lines,B.AVENIR,180,1000,4);step=round(f.size*.98);limit=1610 if ig else 1810
            last=limit-f.getbbox(lines[-1],anchor='ma',stroke_width=4)[3]
            for n,line in enumerate(lines):B.text(im,mask,(540,last-(2-n)*step),line,f,B.WHITE if n<2 else B.CYAN,4,anchor='ma')
        else:
            bottom=headline(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),entry['style'],ig)
            # All exercise-critical hands/weights remain within the recorded crop.
            y=bottom+45;im.alpha_composite(photo.convert('RGBA'),(0,y))
            headline(im,mask,entry['style'],ig)
            if entry['style']=='cyan':ImageDraw.Draw(im).rectangle((22,22,W-23,H-23),outline=B.CYAN,width=4)
        rows.append(save(im,mask,key,platform,{'exercise':entry['exercise'],'source_clip':entry['id'],'source_time':entry['t'],
             'original':entry['original'],'original_sha256':entry['sha256'],'source_crop':CROPS[key],'picture_top':y,'source_type':'Real video screenshot with photographic touch-ups','ai_generation':False}))

# B: preserve the approved YouTube file byte for byte. Fit its entire food scene
# inside the Instagram profile instead of pushing the lower food plates off-frame.
old=R.parent/'layouts/B/youtube/g3.png';assert sha(old)=='4ef67084203de366469d926a82f3908446c2227e3f40cd327ad298edc33da722'
src=Image.open(R.parent/'assets/B-g3.jpg').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
scene=src.crop((0,450,W,H));scene=scene.resize((810,round(scene.height*.75)),Image.Resampling.LANCZOS)
im=Image.new('RGBA',(W,H),(8,19,33,255));im.alpha_composite(scene.convert('RGBA'),(135,560))
ImageDraw.Draw(im).rounded_rectangle((22,22,W-23,H-23),radius=18,outline=B.WHITE,width=4)
mask=Image.new('L',(W,H));lines=['How Much Protein','Do You Need?'];f=B.common(lines,B.IMPACT,165,950,4);step=round(f.size*1.12)
for n,line in enumerate(lines):B.text(im,mask,(58,262+n*step),line,f,B.WHITE if n==0 else B.CYAN,4)
ImageDraw.Draw(im).rectangle((58,242,280,250),fill=B.CYAN)
rows.append(save(im,mask,'BX2','instagram',{'source':str(R.parent/'assets/B-g3.jpg'),'scene_crop':[0,450,W,H],'scene_rect':[135,560,945,560+scene.height],
    'reason_for_containment':'Keep the complete food spread and Dan inside the Instagram profile crop, without stretching or generating anything','approval':'awaiting exact revised Instagram approval'}))
out=R/'covers/BX2';import shutil
for ext in ['png','jpg']:shutil.copyfile(old.with_suffix('.'+ext),out/('youtube.'+ext))
rows.append({'label':'BX2','platform':'youtube','path':str(out/'youtube.png'),'sha256':sha(out/'youtube.png'),'jpeg':str(out/'youtube.jpg'),'jpeg_sha256':sha(out/'youtube.jpg'),'approval':'Dan approved November8, preserved exact file'})
(R/'manifest.json').write_text(json.dumps({'round':2,'date':'2026-11-08','status':'awaiting A pick and revised B Instagram approval','outputs':rows},indent=2)+'\n')
sheet=Image.new('RGB',(4*300,2*560),'#101722');dr=ImageDraw.Draw(sheet)
for i,k in enumerate(['A1','A2','A3','A4']):
    for j,platform in enumerate(['instagram','youtube']):
        im=Image.open(R/'covers'/k/(platform+'.png'));im.thumbnail((280,500));x=i*300;y=j*560;sheet.paste(im,(x+10,y+40));dr.text((x+10,y+8),k+' '+platform,fill='white')
sheet.save(R/'four-real-choices.jpg',quality=95)
print('Built ten paired cover layouts; B YouTube bytes unchanged.')
