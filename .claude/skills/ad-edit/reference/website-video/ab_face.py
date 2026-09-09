#!/usr/bin/env python3
"""AB_tan_face.mp4 -- the face region only, version A (tan-corrected) beside version B (as-is), at four timestamps
where the blotch is visible and the correction is at full strength, ~3 s each, labelled. Built from the two DELIVERED
masters so Dan judges exactly what ships. python3 ab_face.py <A.mp4> <B.mp4> <out.mp4>"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; HERE=os.path.dirname(os.path.abspath(__file__))
A,Bv,OUT=sys.argv[1:4]; FPS=30000/1001
T=json.load(open(f"{HERE}/tanpass_track.json"))
import tanpass as TP
_,P,_,_,valid,S,r=TP.load_track()
# four windows: the 14.0 s frame Dan pointed at, then three spread across the talking head where S==1 for 3 s straight
def full_run(k0,n=int(3*FPS)): return all(valid[k0:k0+n]) and all(S[k0:k0+n]>0.99)
cands=[k for k in range(0,T["n"]-100,15) if full_run(k)]
picks=[int(round(13.0*FPS))]
for frac in (0.3,0.55,0.8):
    tgt=int(frac*T["n"]); picks.append(min(cands,key=lambda k:abs(k-tgt)))
parts=[]
for i,k in enumerate(picks):
    t=k/FPS; cx,cy=P[k:k+int(3*FPS)].reshape(-1,2).mean(axis=0)
    x0=int(max(0,min(1920-560,cx-280))); y0=int(max(0,min(1080-420,cy-210)))
    for src,lab,tag in ((A,"A  tan-corrected","a"),(Bv,"B  as-is","b")):
        parts.append((src,t,x0,y0,lab,f"{i}{tag}"))
fc=[]; inputs=[]
for j,(src,t,x0,y0,lab,tag) in enumerate(parts):
    inputs+=["-ss",f"{t:.3f}","-t","3","-i",src]
    fc.append(f"[{j}:v]crop=560:420:{x0}:{y0},scale=960:720:flags=lanczos,drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial\\ Bold.ttf:text='{lab}   {int(t//60)}\\:{t%60:05.2f}':fontcolor=white:fontsize=34:box=1:boxcolor=black@0.6:boxborderw=10:x=20:y=20,setsar=1[v{j}]")
rows=[]
for i in range(len(picks)):
    fc.append(f"[v{2*i}][v{2*i+1}]hstack=inputs=2[r{i}]"); rows.append(f"[r{i}]")
fc.append("".join(rows)+f"concat=n={len(picks)}:v=1:a=0[out]")
subprocess.run([FF,"-nostdin","-y","-v","error"]+inputs+["-filter_complex",";".join(fc),"-map","[out]","-r","30000/1001",
    "-c:v","libx264","-preset","medium","-crf","16","-pix_fmt","yuv420p","-movflags","+faststart",OUT],check=True)
print(OUT, "windows at", [round(k/FPS,2) for k in picks])
