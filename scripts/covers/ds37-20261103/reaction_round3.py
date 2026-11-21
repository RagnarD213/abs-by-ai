#!/usr/bin/env python3
"""Dan's B revision: C's complete original-video view, tighter headroom, more body."""
import json, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import reaction_round2 as S

OUT=S.BASE/'round3'
OUT.mkdir(exist_ok=True)
BRIEF="Let's go with B but I want to change it where you're using the image of Dr. Mike in C. That way you show less space above my head and a little bit more of my body"

def dan(height,pf,pad=0):
 path=S.SRC/'dan-O0430.png';im=Image.open(path).convert('RGBA');face=S.face_box(path)
 scale=.64 if pf=='instagram' else 1.0
 alpha=np.array(im.getchannel('A'));ys,xs=np.where(alpha>200);hair=int(ys.min())
 layer=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 x=round(S.W/2-(face[0]+face[2])/2*scale);y=round(pad+24-hair*scale)
 yy,xx=np.mgrid[:height,:S.W];glow=np.exp(-(((xx-S.W*.5)/(S.W*.6))**2+((yy-height*.35)/(height*.8))**2))
 rgb=(np.array([8,17,25])+np.array([21,37,47])*glow[...,None]).astype('uint8')
 bg=Image.fromarray(rgb).convert('RGBA');bg.alpha_composite(layer,(x,y))
 f=[face[0]*scale+x,face[1]*scale+y,face[2]*scale+x,face[3]*scale+y]
 assert f[1]>20 and f[3]<height-20
 return bg.convert('RGB'),f,dict(scale=scale,source_hair_row=hair,rendered_hair_row=y+hair*scale,profile_headroom=y+hair*scale-pad,source_bottom_visible=(height-y)/scale)

def build(pf):
 lo,hi=(240,1680) if pf=='instagram' else (0,S.H)
 band=290;mike_h=540;top_h=hi-lo-band-mike_h;by=lo+top_h;my=by+band
 upper,df,framing=dan(top_h+lo,pf,pad=lo)
 mp=S.SRC/'mike-668.00s.png';original=Image.open(mp).convert('RGB');mike=original.resize((S.W,mike_h),Image.Resampling.LANCZOS)
 mf=[v*.5625 for v in S.face_box(mp)]
 im=Image.new('RGB',(S.W,S.H),'#111D29');im.paste(upper,(0,0));im.paste(mike,(0,my))
 # Continue desk colours below the profile crop with a quiet fade, never stretched faces.
 if hi<S.H:
  edge=np.array(mike)[-1].astype(float);amount=np.linspace(0,1,S.H-hi)[:,None,None]
  tail=(edge[None,:,:]*(1-amount)+np.array([8,17,25])*amount).astype('uint8');im.paste(Image.fromarray(tail),(0,hi))
 d=ImageDraw.Draw(im);d.rectangle((0,by,S.W,my),fill='#090A0C');d.rectangle((0,by,S.W,by+9),fill='#FFD60A');d.rectangle((0,my-9,S.W,my),fill='#FFD60A')
 boxes=[S.text(im,line,by+40+i*128,S.DESIGNS['B'],['#FFD60A','#FFFDF6'][i]) for i,line in enumerate(S.COPY)]
 faces=[df,[mf[0],mf[1]+my,mf[2],mf[3]+my]]
 for b in boxes:
  assert 25<=b[0]<b[2]<=S.W-25 and lo+20<=b[1]<b[3]<=hi-20
  for f in faces:assert b[2]<f[0]-20 or b[0]>f[2]+20 or b[3]<f[1]-20 or b[1]>f[3]+20
 for f in faces:assert f[1]>=lo+20 and f[3]<=hi-20
 p=OUT/f'B-revised-{pf}.jpg';im.save(p,quality=94,subsampling=0)
 assert im.size==(1080,1920) and im.mode=='RGB' and p.stat().st_size<2_000_000
 detected=S.detector(p);assert len(detected)==2,detected
 shutil.copy2(p,S.PUBLIC/f'r3-B-{pf}.jpg')
 if pf=='instagram':im.crop((0,240,1080,1680)).resize((540,720),Image.Resampling.LANCZOS).save(S.PUBLIC/'r3-B-grid.jpg',quality=94)
 # Compare actual decoded lower panel against C's exact original-video image.
 image_lower=Image.open(p).crop((0,my,1080,my+540));delta=float(np.abs(np.array(image_lower,dtype=float)-np.array(mike,dtype=float)).mean())
 assert delta<4,delta
 return dict(platform=pf,path=str(p.relative_to(S.ROOT)),sha256=S.sha(p),bytes=p.stat().st_size,text_boxes=boxes,head_boxes=faces,detected_faces=detected,dan_source=str(S.SRC/'dan-O0430.png'),mike_source=str(mp),mike_source_sha256=S.sha(mp),mike_source_full_frame_preserved=True,mike_panel_mean_jpeg_delta=delta,framing=framing,passed=True)

def review():
 if not (S.PUBLIC/'round2.html').exists():shutil.copy2(S.PUBLIC/'index.html',S.PUBLIC/'round2.html')
 sheet=Image.new('RGB',(1020,1040),'#101823');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(str(S.SUP/'Arial Bold.ttf'),26)
 for x,pf,title in [(15,'instagram','Instagram'),(525,'youtube','YouTube Shorts')]:
  d.text((x+8,15),'B Revised / '+title,font=font,fill='white');im=Image.open(S.PUBLIC/f'r3-B-{pf}.jpg');im.thumbnail((480,950));sheet.paste(im,(x,65))
 sheet.save(S.PUBLIC/'B-revised-review.jpg',quality=95)
 html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dr Mike Cover B Revised</title><style>body{margin:0;background:#101823;color:#f6f8fa;font:18px/1.5 -apple-system,Arial}main{max-width:1150px;margin:auto;padding:26px 20px}h1{font-size:32px}a{color:#86dcff}img{display:block;width:100%}.pair{display:grid;grid-template-columns:1fr 1fr .75fr;gap:18px}figure{margin:0}figcaption{margin-bottom:10px;color:#cad7e4;font-size:16px}@media(max-width:700px){.pair{grid-template-columns:1fr 1fr}.grid{grid-column:1/3;max-width:250px}}</style></head><body><main><h1>B Revised</h1><p>B’s layout with C’s full original Dr. Mike video image below. Your framing has less room above your hair and shows more of your body. The headline is unchanged.</p><p>Please approve these final layouts in this chat before they are installed. Nothing is uploaded or scheduled.</p><div class="pair">'''
 for pf,title in [('instagram','Instagram'),('youtube','YouTube Shorts'),('grid','Instagram Profile Crop')]:html+=f'<figure class="{"grid" if pf=="grid" else ""}"><figcaption>{title}</figcaption><a href="r3-B-{pf}.jpg"><img src="r3-B-{pf}.jpg" alt="Revised B {title}"></a></figure>'
 html+='</div><p><a href="B-revised-review.jpg">Open Both Layouts Together</a></p></main></body></html>'
 (S.PUBLIC/'index.html').write_text(html)

if __name__=='__main__':
 rows=[build(p) for p in ['instagram','youtube']]
 (OUT/'manifest.json').write_text(json.dumps({'date':'2026-11-04','status':'revised-pick-awaiting-exact-file-approval','dan_words':BRIEF,'selected_base':'round2 B','borrowed_image':'round2 C, full source video','outputs':rows,'no_film_change':True,'no_generation':True},indent=2))
 review();print('Two revised layouts built and checked; waiting for exact-file approval.')
