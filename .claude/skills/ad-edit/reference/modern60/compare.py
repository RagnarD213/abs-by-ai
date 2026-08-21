#!/usr/bin/env python3
"""Side-by-side A/B: the Upwork trial edit (left) vs this pipeline sample (right).

Same footage, same minute. Audio is OURS -- the two mixes cannot be judged on top of
each other, and the trial edit plays on its own from its original file.
"""
import importlib.util, subprocess
from PIL import Image, ImageDraw
SKILL="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec=importlib.util.spec_from_file_location("ml",f"{SKILL}/motionlib.py")
ml=importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
FF=ml.FF
VW,VH=940,528
LX,RX,VY=10,970,300

bg=Image.new("RGBA",(1920,1080),(15,17,21,255))
d=ImageDraw.Draw(bg)
fT=ml.font(54,"ExtraBold"); fS=ml.font(30,"Medium"); fF=ml.font(28,"Medium")
d.text((LX+VW//2,150),"UPWORK TRIAL EDIT",font=fT,fill=(232,234,238),anchor="mm")
d.text((RX+VW//2,150),"ABS BY AI PIPELINE",font=fT,fill=(232,234,238),anchor="mm")
d.text((LX+VW//2,205),"61.5s  ·  Premiere  ·  no captions",font=fS,fill=(128,138,152),anchor="mm")
d.text((RX+VW//2,205),"65.8s  ·  motionlib  ·  no captions",font=fS,fill=(226,34,34),anchor="mm")
d.rounded_rectangle([RX-4,VY-4,RX+VW+4,VY+VH+4],radius=6,outline=(226,34,34),width=3)
d.text((960,900),"Audio is the pipeline mix. Same source footage, same first minute.",
       font=fF,fill=(128,138,152),anchor="mm")
d.text((960,948),"Play the trial edit from its own file to A/B the sound.",
       font=fF,fill=(96,104,116),anchor="mm")
bg.convert("RGB").save("cmp_bg.png")

fc=(f"[1:v]scale={VW}:{VH}:flags=lanczos,tpad=stop_mode=clone:stop_duration=8,setsar=1[L];"
    f"[2:v]scale={VW}:{VH}:flags=lanczos,setsar=1[R];"
    f"[0:v][L]overlay={LX}:{VY}[a];[a][R]overlay={RX}:{VY}:shortest=1[vout]")
subprocess.run([FF,"-nostdin","-y","-v","error","-loop","1","-i","cmp_bg.png",
    "-i","reference/muhammad_a.mp4","-i","modern_sample.mp4",
    "-filter_complex",fc,"-map","[vout]","-map","2:a",
    "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
    "-r","30000/1001","-c:a","aac","-b:a","192k","-movflags","+faststart",
    "compare_trial_vs_pipeline.mp4"],check=True)
print("compare_trial_vs_pipeline.mp4 done")
