#!/usr/bin/env python3
"""Contact sheet from EXACT -ss grabs (ad-edit lesson 94: `fps=1/N` + `%{pts}` labels lag the
content by ~N/2 s and produced three false alarms on rev 2's review).
  sheet.py <video> <out.jpg> [step_seconds=5]
"""
import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
V,OUT=sys.argv[1],sys.argv[2]; STEP=float(sys.argv[3]) if len(sys.argv)>3 else 5.0
dur=float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",V],capture_output=True,text=True).stdout)
ts=[i*STEP for i in range(int(dur//STEP)+1)]
W,H,COLS=384,216,6; rows=math.ceil(len(ts)/COLS)
try: fnt=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf",18)
except Exception: fnt=ImageFont.load_default()
sheet=Image.new("RGB",(W*COLS,H*rows),(0,0,0)); d=ImageDraw.Draw(sheet)
for i,t in enumerate(ts):
    raw=subprocess.run([FF,"-v","error","-ss",f"{t:.3f}","-i",V,"-frames:v","1","-vf",f"scale={W}:{H}",
                        "-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    if len(raw)<W*H*3: continue
    x,y=(i%COLS)*W,(i//COLS)*H
    sheet.paste(Image.frombytes("RGB",(W,H),raw[:W*H*3]),(x,y))
    lab=f"{int(t//60)}:{t%60:04.1f}"; d.rectangle([x+2,y+2,x+2+len(lab)*11,y+24],fill=(0,0,0))
    d.text((x+5,y+4),lab,font=fnt,fill=(255,230,0))
sheet.save(OUT,quality=88); print(f"{OUT}: {len(ts)} exact grabs every {STEP:.0f}s")
