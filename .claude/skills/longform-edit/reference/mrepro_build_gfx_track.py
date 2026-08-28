#!/usr/bin/env python3
"""Build ONE flattened qtrle alpha track (0..418.051) carrying every overlay
graphic (pills, chips, bars, stack, price, cta, subscribe, ffwd, ai label),
with a 0.25s fade-out on each. Then concat -c copy."""
import os, sys, subprocess, json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import beats, orglib as G
from PIL import Image

BASE='/Volumes/Extreme/_edit_work/abwheel/mrepro'
OUT=f'{BASE}/gfxtrack'
os.makedirs(OUT,exist_ok=True)
FPS=30000/1001; FPSS='30000/1001'
TOTAL=418.051

def comp_frame_fn(g):
    c=g['comp']
    if c=='pill2':
        fn,_=G.pill_two_line(g['line1'],g.get('line2'),style=g.get('style','olive'),
                             y0=64 if g.get('style')=='white' else 78,
                             size1=g.get('size1',56 if g.get('style')=='olive' else 74),
                             size2=g.get('size2',46))
        return fn
    if c=='pillw':
        fn,_=G.pill_two_line(g['line1'],None,style='white',y0=64,size1=74)
        return fn
    if c=='numchip':
        fn,_=G.num_chip(g['num'],g['text'])
        return fn
    if c=='thin':
        fn,_=G.thin_bar(g['text'])
        return fn
    if c=='stack':
        fn,_=G.stack_panel(g['items'],per_item=0.35 if g.get('fast') else 0.9)
        return fn
    if c=='price':
        fn,_=G.price_pill(g['pre'],g['amount'])
        return fn
    if c=='cta':
        fn,_=G.cta_pill(g['text'],y0=940)
        return fn
    if c=='subscribe':
        return G.subscribe_anim(y0=960)
    if c=='ai_label':
        return G.ai_label()
    raise ValueError(c)

events=[]
for g in beats.GRAPHICS:
    events.append((g['t0'],g['t1'],comp_frame_fn(g),g['comp']))
for (a,b) in beats.FFWD:
    events.append((a,b,G.ffwd_glyph(),'ffwd'))
events.sort(key=lambda e:e[0])
# assert no overlap (ffwd + pill CAN overlap: pillw over set1 + ffwd!). Handle by
# merging overlapping events into one composite frame fn.
merged=[]
for e in events:
    if merged and e[0]<merged[-1][1]-1e-6:
        a0,b0,f0,n0=merged[-1]
        a1,b1,f1,n1=e
        A,B=min(a0,a1),max(b0,b1)
        def mk(f0,f1,a0,a1,A):
            def fn(t):
                im=Image.new('RGBA',(1920,1080),(0,0,0,0))
                if t+A>=a0: im.alpha_composite(f0(t+A-a0))
                if t+A>=a1: im.alpha_composite(f1(t+A-a1))
                return im
            return fn
        merged[-1]=(A,B,mk(f0,f1,a0,a1,A),n0+'+'+n1)
    else:
        merged.append(e)
print(len(merged),"track events")

# transparent filler PNG
filler=f'{OUT}/_blank.png'
Image.new('RGBA',(1920,1080),(0,0,0,0)).save(filler)

concat=open(f'{OUT}/concat.txt','w')
prevf=0
def gap(nf,idx):
    of=f'{OUT}/gap{idx:03d}.mov'
    if not os.path.exists(of):
        subprocess.run(["ffmpeg","-nostdin","-v","error","-loop","1","-framerate",FPSS,
                        "-i",filler,"-frames:v",str(nf),"-c:v","qtrle","-y",of],check=True)
    return of

idx=0
for (a,b,fn,name) in merged:
    fa=int(round(a*FPS)); fb=int(round(b*FPS))
    if fa>prevf:
        concat.write(f"file '{gap(fa-prevf,idx)}'\n"); idx+=1
    of=f'{OUT}/g{idx:03d}_{name[:12].replace("+","_")}.mov'
    if not (os.path.exists(of) and os.path.getsize(of)>1000):
        dur=(fb-fa)/FPS
        FADE=0.25
        def wrapped(t,fn=fn,dur=dur):
            im=fn(t)
            if t>dur-FADE:
                k=max(0.0,(dur-t)/FADE)
                im.putalpha(im.getchannel('A').point(lambda v:int(v*k)))
            return im
        G.encode_seq(wrapped,dur,of)
    # verify frames
    r=subprocess.run(["ffprobe","-v","error","-count_frames","-select_streams","v",
                      "-show_entries","stream=nb_read_frames","-of","csv=p=0",of],capture_output=True,text=True)
    nf=int(r.stdout.strip())
    want=fb-fa
    if nf!=want:
        print("frame mismatch",of,nf,want); sys.exit(1)
    concat.write(f"file '{of}'\n")
    idx+=1
    prevf=fb
    print("done",name,round(a,1),round(b,1))
total_f=int(round(TOTAL*FPS))
if prevf<total_f:
    concat.write(f"file '{gap(total_f-prevf,idx)}'\n")
concat.close()
subprocess.run(["ffmpeg","-nostdin","-v","error","-f","concat","-safe","0","-i",f"{OUT}/concat.txt",
                "-c","copy","-video_track_timescale","30000","-y",f"{BASE}/gfx_track.mov"],check=True)
r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{BASE}/gfx_track.mov"],capture_output=True,text=True)
print("gfx_track duration",r.stdout.strip())
