"""SL-09 R2: full-rate cut finder over each short's source range of Zeeshan's master + a contact sheet per range (one tile per shot: in / mid / out)."""
import json, subprocess, sys, numpy as np
from PIL import Image, ImageDraw
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
R={"A":(680.5,739.5),"H":(926.5,986.0),"I":(988.0,1066.5),"J":(1065.5,1114.0),"K":(194.0,238.5)}
res={}
for S,(a0,a1) in R.items():
    raw=subprocess.run([FF,"-v","error","-ss",f"{a0:.3f}","-i","master.mp4","-t",f"{a1-a0:.3f}","-vf","scale=160:90:in_color_matrix=bt709","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,90,160).astype(np.float32); d=np.abs(np.diff(fr,axis=0)).mean((1,2)); med=np.median(d)+0.3
    cuts=[]
    for i in range(1,len(d)-1):
        if d[i]>6*med and d[i]>4 and d[i]>=d[i-1] and d[i]>=d[i+1]: cuts.append(round(a0+(i+1)/FPS,3))
    # soft changes (animated zooms / dissolves): sustained diff over 3x median for >=4 frames
    soft=[]; run=0
    for i in range(len(d)):
        run=run+1 if d[i]>3*med else 0
        if run==4: soft.append(round(a0+(i-2)/FPS,3))
    res[S]=dict(a=a0,b=a1,cuts=cuts,soft=soft,diff=[round(float(x),2) for x in d])
    print(S,len(cuts),"cuts",cuts,"soft",soft,flush=True)
    bounds=[a0]+cuts+[a1]; tiles=[]
    for k in range(len(bounds)-1):
        s,e=bounds[k],bounds[k+1]
        for lab,t in (("in",s+0.05),("mid",(s+e)/2),("out",e-0.08)):
            b=subprocess.run([FF,"-v","error","-ss",f"{t:.3f}","-i","master.mp4","-frames:v","1","-vf","scale=384:216:in_color_matrix=bt709","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
            im=Image.frombytes("RGB",(384,216),b); dd=ImageDraw.Draw(im); dd.rectangle((0,0,170,14),fill=(0,0,0)); dd.text((2,1),f"#{k} {lab} {t:.2f}",fill=(255,255,0)); tiles.append(im)
    cols=6; rows=(len(tiles)+cols-1)//cols; sh=Image.new("RGB",(384*cols,216*rows))
    for k,im in enumerate(tiles): sh.paste(im,((k%cols)*384,(k//cols)*216))
    sh.save(f"scan_{S}.jpg",quality=80)
json.dump(res,open("src_cuts.json","w"))
