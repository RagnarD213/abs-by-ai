#!/usr/bin/env python3
"""Website video -- EDL concat across TWO rolls + S-Log3 grade + LAV mono -> base.mov.

Source is 3840x2160 S-Log3 / S-Gamut3.Cine (first shoot in this format; every prior roll
was S-Cinetone). Grade = a numpy-built 33^3 .cube (make_lut.py: Sony S-Log3 transfer ->
linear, S-Gamut3.Cine->Rec709 matrix, soft shoulder, BT.709 OETF) at 1.45x linear
exposure, then saturation 0.88 -- picked by eye against the approved Ad 3 skin.

Audio: the rolls carry FOUR mono LPCM streams. a:1 is the close lav (SNR 40 dB); a:0 is
the far mic, 7.2 ms late and POLARITY INVERTED (chan_analyse.py). Lav only.

Output is 2560x1440 so the punch pass (1.00 / 1.15 / 1.30) never upscales: even the 1.30
crop of 1440p is 1969 px wide -> 1920 is a downscale.
"""
import json, os, subprocess
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
HERE=os.path.dirname(os.path.abspath(__file__))
GRADE=open(f"{HERE}/grade.txt").read().strip()
R=json.load(open(f"{HERE}/edl.json"))["ranges"]
srcs=[]; 
for r in R:
    if r["source"] not in srcs: srcs.append(r["source"])
inp=[]
for s in srcs: inp+=["-i",s]
parts=[]
for k in range(len(srcs)):
    n=sum(1 for r in R if r["source"]==srcs[k])
    parts.append(f"[{k}:a:1]asplit={n}"+"".join(f"[m{k}_{i}]" for i in range(n)))
cnt={k:0 for k in range(len(srcs))}; cat=""
for i,r in enumerate(R):
    k=srcs.index(r["source"]); j=cnt[k]; cnt[k]+=1; a,b=r["start"],r["end"]
    parts.append(f"[{k}:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,setsar=1[v{i}]")
    parts.append(f"[m{k}_{j}]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]")
    cat+=f"[v{i}][a{i}]"
fc=";".join(parts)+f";{cat}concat=n={len(R)}:v=1:a=1[vc][ac];[vc]{GRADE}[vout]"
subprocess.run([FF,"-nostdin","-y","-v","error"]+inp+["-filter_complex",fc,
  "-map","[vout]","-map","[ac]","-c:v","libx264","-preset","medium","-crf","15",
  "-pix_fmt","yuv420p","-r","30000/1001","-c:a","pcm_s16le",f"{HERE}/base.mov"],check=True)
print("base.mov written")
