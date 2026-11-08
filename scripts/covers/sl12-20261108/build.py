"""SL12 setup covers, using the checked SL08 house compositing helpers.

Original people stay untouched in the real-photo choices. Two platform layouts
are built before neutral shuffling. Never run this over a picked/approved set.
"""
from pathlib import Path
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[3]
WORK = Path('/Volumes/Extreme/_edit_work/SL-12/setup')
sys.path.insert(0, str(ROOT/'scripts/covers/sl08-20261025'))
import build as B

W,H=1080,1920
COPY={'A':['Lift Weights On','Weight Loss Medication'],
      'B':['How Much Protein','Do You Need?']}
TRIPLE={'A':['Lift Weights On','Weight Loss','Medication'],
        'B':['How Much','Protein','Do You Need?']}
B.STUDIO={'A':'studio-blue-247','B':'studio-white-23'}
STYLES={'c1':'yellow','c2':'frame','c3':'bottom','c4':'ivory',
        'c5':'real','g1':'red','g2':'yellow','g3':'frame'}

def upper(im,mask,k,ig,style):
    top=(270 if style in ('real','ivory') else 256) if ig else 90
    if style=='yellow':
        f=B.common(COPY[k],B.DIN,190,960);step=int(f.size*1.08)
        bottom=top+2*step+44
        B.box(im,mask,(0,top-16,W,bottom),B.YEL)
        for n,t in enumerate(COPY[k]):
            B.text(im,mask,(54,top+n*step),t,f,B.INK if n==0 else (186,24,24))
        return bottom
    if style in ('real','ivory'):
        f=B.common(COPY[k],B.FUTURA,145,950,0);step=int(f.size*1.16)
        bottom=top+2*step+50
        color=(241,237,225) if style=='ivory' else (8,24,43)
        B.box(im,mask,(22,top-25,W-22,bottom),color,20)
        for n,t in enumerate(COPY[k]):
            B.text(im,mask,(540,top+n*step),t,f,
                   B.INK if style=='ivory' else B.WHITE,anchor='ma')
        ImageDraw.Draw(im).rectangle((400,bottom-16,680,bottom-9),fill=(190,40,30) if style=='ivory' else B.YEL)
        return bottom
    f=B.common(COPY[k],B.IMPACT,175,950,4);step=int(f.size*1.13)
    for n,t in enumerate(COPY[k]):
        B.text(im,mask,(58,top+n*step),t,f,
               B.WHITE if n==0 else (B.RED if style=='red' else B.CYAN),4)
    ImageDraw.Draw(im).rectangle((58,top-23,280,top-15),fill=B.RED if style=='red' else B.CYAN)
    return top+2*step+20

def build():
    only=set(sys.argv[1:])
    manifest=WORK/'layout-manifest-private.json'
    records=[r for r in json.loads(manifest.read_text()) if r['short']+':'+r['id'] not in only] if only else []
    for k in 'AB':
        for ident,style in STYLES.items():
            if only and k+':'+ident not in only:continue
            file=WORK/'assets'/f'{k}-{ident}{".jpg" if ident.startswith("g") else ".png"}'
            if not file.exists():raise FileNotFoundError(file)
            for platform in ['instagram','youtube']:
                ig=platform=='instagram';mask=Image.new('L',(W,H))
                im=ImageOps.fit(Image.open(file).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS).convert('RGBA')
                info={}
                if style=='bottom':
                    pm,faces=B.person_mask(im)
                    ys=np.where(pm.any(axis=1))[0]
                    if not len(ys):raise ValueError('No measured subject: '+str(file))
                    # Move actual photo upward, keeping its own background behind.
                    shift=max(0,int(ys.min())-(270 if ig else 100))
                    picture=im.copy()
                    im.alpha_composite(picture,(0,-shift))
                    B.ramp(im,1060 if ig else 1210,1260 if ig else 1450,255,top_dark=False)
                    # B's longer three-line title must start below the lower abs.
                    # Keep the last line above the Reels caption area.
                    cap=(145 if ig else 180) if k=='B' else 205
                    f=B.common(TRIPLE[k],B.AVENIR,cap,1000,4);step=int(f.size*.98)
                    limit=1610 if ig else 1810
                    last=limit-f.getbbox(TRIPLE[k][-1],stroke_width=4,anchor='ma')[3]
                    for n,t in enumerate(TRIPLE[k]):
                        B.text(im,mask,(540,last-(2-n)*step),t,f,B.WHITE if n<2 else B.CYAN,4,anchor='ma')
                    info['picture_shift']=-shift
                else:
                    bottom=upper(Image.new('RGBA',(W,H)),Image.new('L',(W,H)),k,ig,style)
                    if style=='real':
                        B.ramp(im,0,1000,190)
                        info.update(B.studio(im,k,bottom+100))
                        info['real_photo_source']=info.pop('source')
                        info['real_photo_source_sha256']=info.pop('source_sha256')
                        info['source_pixels_preserved']=True
                    else:
                        im,shift=B.drop_below(im,bottom+90)
                        info['picture_shift']=shift
                        if style in ('frame','red'):B.ramp(im,0,900,175)
                    upper(im,mask,k,ig,style)
                    if style=='frame':
                        ImageDraw.Draw(im).rounded_rectangle((22,22,W-23,H-23),radius=18,outline=B.WHITE,width=4)
                out=WORK/'layouts'/k/platform;out.mkdir(parents=True,exist_ok=True)
                p=out/(ident+'.png');im.convert('RGB').save(p);mask.save(out/(ident+'.text-mask.png'))
                if not ig:im.convert('RGB').save(p.with_suffix('.jpg'),quality=92)
                pm,faces=B.person_mask(im)
                guards=[]
                for face in faces:
                    x0,y0,x1,y1=map(int,face);fh=y1-y0
                    guards.append([max(0,x0-30),max(0,y0-int(fh*.6)-25),min(W,x1+30),min(H,y1+25)])
                ink=np.array(mask)>0
                overlap=sum(int(ink[g[1]:g[3],g[0]:g[2]].sum()) for g in guards)
                bounds=mask.getbbox()
                if k=='B' and ident=='c3' and ig:assert bounds[1]>=1190,('B bottom title too high',bounds)
                assert bounds and bounds[0]>=0 and bounds[2]<=W
                assert bounds[1]>=(240 if ig else 40) and bounds[3]<= (1630 if ig else 1850),(k,ident,platform,bounds)
                assert overlap==0,(k,ident,platform,'face/hair overlap',overlap)
                assert faces,(k,ident,platform,'No face detection; inspect and resolve')
                records.append(dict(short=k,id=ident,platform=platform,path=str(p),sha256=B.sha(p),
                     source=str(file),source_sha256=B.sha(file),style=style,copy=TRIPLE[k] if style=='bottom' else COPY[k],
                     text_bounds=bounds,faces=faces,hair_guards=guards,face_hair_text_pixels=overlap,**info))
    (WORK/'layout-manifest-private.json').write_text(json.dumps(records,indent=2)+'\n')
    for k in 'AB':
        ids=list(STYLES);sheet=Image.new('RGB',(8*270,1000),'#171e28');dr=ImageDraw.Draw(sheet)
        for i,ident in enumerate(ids):
            for j,plat in enumerate(['instagram','youtube']):
                p=WORK/'layouts'/k/plat/(ident+'.png');im=Image.open(p);im.thumbnail((270,480));sheet.paste(im,(i*270,j*500));dr.text((i*270+4,j*500+482),ident+' '+plat,fill='white')
        sheet.save(WORK/(k+'-layout-audit.jpg'))
    print('Built and measured',len(records),'layouts')

if __name__=='__main__':build()
