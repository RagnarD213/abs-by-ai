#!/usr/bin/env python3
"""Hard gate for the 9:16 build. Every check is measured off the FINISHED FILE, never the
build plan -- a build plan cannot tell you a filter silently truncated a segment."""
import json, os, re, subprocess, sys, wave
import numpy as np
sys.path.insert(0,'.')
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP=FF.replace('ffmpeg','ffprobe')
V=sys.argv[1] if len(sys.argv)>1 else 'ad1_vertical_9x16.mp4'
TARGET=float(sys.argv[2]) if len(sys.argv)>2 else 232.768
R=[]
def chk(ok,name,detail): R.append((ok,name,detail))

p=subprocess.run([FP,'-v','error','-select_streams','v','-show_entries',
   'stream=width,height,r_frame_rate','-show_entries','format=duration','-of','csv=p=0',V],
   capture_output=True,text=True).stdout.split()
w,h,fr=p[0].split(',')[:3]; dur=float(p[1])
chk((w,h)==('1080','1920'), '1  frame size is 1080x1920', f'{w}x{h}')
chk(fr=='30000/1001', '2  frame rate is 29.97', fr)
chk(abs(dur-TARGET)<0.10, '3  duration matches the reference cut', f'{dur:.3f}s vs {TARGET}s')

r=subprocess.run([FF,'-hide_banner','-nostats','-i',V,'-af','loudnorm=print_format=summary',
   '-f','null','-'],capture_output=True,text=True).stderr
g=lambda k: float(re.search(rf'{k}:\s+(-?[\d.]+)',r).group(1))
I,TP=g('Input Integrated'),g('Input True Peak')
chk(abs(I+14)<=0.8, '4  loudness -14 LUFS', f'{I} LUFS')
chk(TP<=-1.0,       '5  true peak at or under -1.0 dBTP', f'{TP} dBTP')

subprocess.run([FF,'-v','error','-y','-i',V,'-map','0:a','-ar','16000','-ac','2','_qc.wav'],check=True)
a=np.frombuffer(wave.open('_qc.wav').readframes(10**9),dtype='<i2').astype(np.float32).reshape(-1,2)
L,Rr=a[:,0],a[:,1]
c=float(np.corrcoef(L,Rr)[0,1])
chk(c>0.98, '6  voice is centred (single mic, no comb)', f'L/R corr {c:.4f}')

vals=subprocess.run([FF,'-v','info','-i',V,'-vf',
   "select='gt(scene,0.12)',metadata=print:file=-",'-an','-f','null','-'],
   capture_output=True,text=True).stdout
ts=sorted(set(round(float(x),2) for x in re.findall(r'pts_time:([\d.]+)',vals)))
gaps=[b-a2 for a2,b in zip([0.0]+ts, ts+[dur])]
chk(len(ts)/(dur/60)>=9.0, '7  visual change rate >= 9/min', f'{len(ts)/(dur/60):.1f}/min ({len(ts)} changes)')
chk(max(gaps)<=16.0,      '8  no stretch over 16s without a visual change', f'longest {max(gaps):.1f}s')

import beats as BT
tl,_=BT.timeline()
ins=sum(b['t1']-b['t0'] for b in tl if b['kind']!='talk')
chk(ins/TARGET>=0.55, '9  insert/graphic coverage >= 55%', f'{100*ins/TARGET:.0f}%')

from assets import MEDIA
BAD=[(k,v) for k,v in MEDIA.items() if v[0]=='vid' and 'clip_109' in v[1] and v[2]>=25.0]
longest={}
for b in tl:
    if b.get('media') in MEDIA and 'clip_109' in MEDIA[b['media']][1]:
        longest[b['media']]=max(longest.get(b['media'],0), MEDIA[b['media']][2]+(b['t1']-b['t0']))
over=[k for k,v in longest.items() if v>25.0]
chk(not BAD and not over,
    '10 app recording never reaches the banned before/after or email screens (>25.0s)',
    f'max in-point+len {max(longest.values()) if longest else 0:.1f}s')

sup=set()
for b in tl:
    if b['kind'] in BT.NO_CAPS: sup.add((b['t0'],b['t1']))
cap_ok=os.path.exists('captions.mov')
chk(cap_ok, '11 burned captions present', 'captions.mov')

print(f'\nQC  {V}')
for ok,n,d in R: print(f'  {"PASS" if ok else "FAIL"}  {n:58s} {d}')
bad=[x for x in R if not x[0]]
print(f'\n{len(R)-len(bad)}/{len(R)} pass')
sys.exit(1 if bad else 0)
