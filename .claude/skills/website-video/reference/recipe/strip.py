#!/usr/bin/env python3
"""Frame strip of a clip span: python3 strip.py <clip> <t0> <t1> <step> <out.jpg> [cols]"""
import subprocess, sys, tempfile, shutil, os
from PIL import Image, ImageDraw
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
clip,t0,t1,step,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
cols=int(sys.argv[6]) if len(sys.argv)>6 else 5
tmp=tempfile.mkdtemp(prefix="strip_"); ts=[]; t=t0
while t<=t1+1e-6: ts.append(round(t,3)); t+=step
ims=[]
for i,t in enumerate(ts):
    p=f"{tmp}/{i:03d}.png"
    subprocess.run([FF,"-nostdin","-y","-v","error","-ss",str(t),"-i",clip,"-frames:v","1","-vf","scale=480:-2",p],check=True)
    im=Image.open(p).convert("RGB"); d=ImageDraw.Draw(im)
    d.rectangle([0,0,150,26],fill=(0,0,0)); d.text((6,6),f"{t:.2f}s",fill=(255,255,80))
    ims.append(im)
w,h=ims[0].size; rows=(len(ims)+cols-1)//cols
sheet=Image.new("RGB",(cols*w,rows*h),(20,20,20))
for i,im in enumerate(ims): sheet.paste(im,((i%cols)*w,(i//cols)*h))
sheet.save(out,quality=92); shutil.rmtree(tmp)
print(f"{out}  {len(ims)} frames  {t0}->{t1} step {step}  {sheet.size}")
