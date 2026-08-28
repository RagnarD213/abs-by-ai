#!/usr/bin/env python3
"""Render the graded, framed, frame-locked base conform.
Pieces = intersection of EDL segments and framing-schedule pieces.
Cumulative frame counts; concat; no audio (his mix goes under later)."""
import json, subprocess, os, sys

BASE='/Volumes/Extreme/_edit_work/abwheel'
SHOOT=("/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, "
       "indoor talking content, outdoor workout content | jeff chagrin | dan rose")
OUT=f'{BASE}/mrepro/base_pieces'
os.makedirs(OUT,exist_ok=True)
FPS=30000/1001
FPSS='30000/1001'

segs=json.load(open(f'{BASE}/mrepro/edl_final.json'))
sched=json.load(open(f'{BASE}/mrepro/schedule.json'))
grades=json.load(open(f'{BASE}/mrepro/grade_fit.json'))

def curve_str(roll):
    g=grades[roll]
    def pts(ch):
        p=g[str(ch)] if str(ch) in g else g[ch]
        s='0/0 '+ ' '.join(f"{a}/{b}" for a,b in p) + ' 1/1'
        return s
    return f"curves=r='{pts(0)}':g='{pts(1)}':b='{pts(2)}'"

# build piece list
cuts=sorted(set([s['cut_in'] for s in segs]+[s['cut_out'] for s in segs]
              +[p['t0'] for p in sched]+[p['t1'] for p in sched]))
cuts=[c for c in cuts if 0<=c<=418.051]
pieces=[]
for a,b in zip(cuts,cuts[1:]):
    if b-a<1/FPS/2: continue
    seg=[s for s in segs if s['cut_in']-1e-6<=a<s['cut_out']][0]
    sp=[p for p in sched if p['t0']-1e-6<=a<p['t1']]
    sp=sp[0] if sp else {'t0':a,'t1':b,'s0':1.0,'s1':1.0,'dx0':0,'dx1':0,'dy0':0,'dy1':0}
    pieces.append((a,b,seg,sp))

# cumulative frame counts
Ns=[]
prev=0
for (a,b,seg,sp) in pieces:
    fb=round(b*FPS); Ns.append(int(fb-prev)); prev=fb
print(len(pieces),"pieces, total frames",prev)

concat=open(f'{OUT}/concat.txt','w')
for i,((a,b,seg,sp),N) in enumerate(zip(pieces,Ns)):
    if N<=0: continue
    of=f'{OUT}/p{i:03d}.mp4'
    concat.write(f"file 'p{i:03d}.mp4'\n")
    if os.path.exists(of) and os.path.getsize(of)>1000: continue
    src=f"{SHOOT}/{seg['roll']}.MP4"
    sin=seg['src_in']+(a-seg['cut_in'])*seg['speed']
    dur_src=(b-a)*seg['speed']
    # framing ramp local to this piece
    T=max(b-a,1e-3)
    fr=(a-sp['t0'])/max(sp['t1']-sp['t0'],1e-3); to=(b-sp['t0'])/max(sp['t1']-sp['t0'],1e-3)
    s0=sp['s0']+(sp['s1']-sp['s0'])*fr; s1=sp['s0']+(sp['s1']-sp['s0'])*to
    dx0=sp['dx0']+(sp['dx1']-sp['dx0'])*fr; dx1=sp['dx0']+(sp['dx1']-sp['dx0'])*to
    dy0=sp['dy0']+(sp['dy1']-sp['dy0'])*fr; dy1=sp['dy0']+(sp['dy1']-sp['dy0'])*to
    s0=max(1.0,s0); s1=max(1.0,s1)
    # animated zoom: per-frame upscale by s(t), then fixed 1920x1080 crop with
    # animated x/y. dx/dy are in 160x90 track units -> *12 source px -> *s upscaled.
    sE=f"({s0}+({s1}-{s0})*t/{T})"
    dxE=f"({dx0}+({dx1}-{dx0})*t/{T})*12*(iw/1920)"
    dyE=f"({dy0}+({dy1}-{dy0})*t/{T})*12*(ih/1080)"
    cx=f"min(max((iw-1920)/2+{dxE},0),iw-1920)"
    cy=f"min(max((ih-1080)/2+{dyE},0),ih-1080)"
    vf=[]
    if abs(seg['speed']-1.0)>1e-6:
        vf.append(f"setpts=(PTS-STARTPTS)/{seg['speed']}")
    else:
        vf.append("setpts=PTS-STARTPTS")
    vf.append(f"fps={FPSS}")
    vf.append(curve_str(seg['roll']))
    if abs(s0-1.0)<1e-4 and abs(s1-1.0)<1e-4:
        pass  # wide: no zoom
    else:
        vf.append(f"scale=w='floor(1920*{sE}/2)*2':h=-2:eval=frame:flags=lanczos")
        vf.append(f"crop=1920:1080:'{cx}':'{cy}'")
    vf.append("format=yuv420p")
    cmd=["ffmpeg","-nostdin","-v","error","-ss",f"{sin:.4f}","-t",f"{dur_src+0.6:.4f}",
         "-i",src,"-vf",",".join(vf),"-r",FPSS,"-frames:v",str(N),
         "-an","-c:v","libx264","-crf","17","-preset","medium","-y",of]
    r=subprocess.run(cmd,capture_output=True)
    if r.returncode!=0:
        print("FAIL",i,r.stderr.decode()[-400:]); sys.exit(1)
    if i%20==0: print("piece",i,"/",len(pieces))
concat.close()
subprocess.run(["ffmpeg","-nostdin","-v","error","-f","concat","-safe","0","-i",f"{OUT}/concat.txt",
                "-c","copy","-y",f"{BASE}/mrepro/base.mp4"],check=True)
r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{BASE}/mrepro/base.mp4"],capture_output=True,text=True)
print("base.mp4 duration",r.stdout.strip())
