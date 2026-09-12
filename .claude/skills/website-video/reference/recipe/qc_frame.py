#!/usr/bin/env python3
# ⚠ SUPERSEDED BY `.claude/skills/_shared/deliver/gate.py` (2026-09-11, Phase 1 of
#   Handoffs/handoff-20260911-video-quality-engine.md). Its rows are folded into the shared gate,
#   with every bound moved to `_shared/deliver/formats.py` beside the file and the date it was
#   measured on. DO NOT add a check here -- add it there, or it lands in one of six pipelines and
#   the other five keep the bug.
#   ⚠ STILL ON DISK ON PURPOSE: three sessions were mid-build against these scripts when the shared
#   gate landed (ad1-sq, ad2-sq, ad3-vert, ad4-vert, ad5-vert). It is deleted once those deliver,
#   and it still carries rows the shared gate has not absorbed yet -- framing is Phase 2, the watch
#   pass Phase 3. RUN BOTH until those land.
"""Website video QC -- the two checks rev 2 did not have (ad-edit lessons 97 and 99), measured on the
DELIVERED pixels, never on the plan. Rev 2 passed 14/14 and Dan rejected it on both of these.

 10 CAPTION CLEARANCE. For every caption cue that overlaps a lower-third beat: render the cue alone
    over a green frame and take its ink bbox (fill + outline + shadow); take the lower third's alpha
    bbox from the graphic's own MOV at three points across the cue; wherever the two overlap
    horizontally, assert a >= 20 px vertical gap. Every cue during the phone PiP keeps its ink out of
    the phone box. (Rev 2: MarginV 300 inked at 727-806 over lower thirds at 757-905 -- 49 px of
    overlap on every lower-third beat; QC only compared captions against full-frame cards.)
 11 HAIR (REV 4, replaces the rev-3 headroom check that measured to the hairline -- lesson 107): hairgate.py.
 13 AI TAG: the 1.5x AI-GENERATED chip measured present at (40,40) on every AI insert.
 (rev 3's headroom text follows for the record)
 11 HEADROOM. headtrack.py's detector run on the delivered 1080p master every 0.25 s wherever Dan is
    on camera. Never cut or cramped: >= 15 px on every valid frame. Never excessive: in EVERY punch
    segment he reaches within 45 px of the top edge (the crop is anchored to his tallest instant in
    that segment), the median over the whole video is <= 60 px, and no valid frame exceeds 100 px
    (a sanity ceiling: an anchor that failed reads 150+; his own posture spread inside a hold reaches ~95).
    The spread above the minimum is his own posture inside a fixed crop (measured: up to ~50 px of
    4K in a 10 s hold) -- a crop that followed it would cut his head when he stands tall. Misses (he
    looks down and the forehead fails the skin test) only ever read LOW, so a sample is valid when it
    is within 40 px of the minimum over +-1.5 s. (Rev 2: 159-261 px, median 201.) The worst and the
    tightest frames are written to pv/headroom_*.png for the watch strips.

  WORK=<dir> python3 qc_frame.py [master.mp4] [cap.ass]      exit 1 on any FAIL
"""
import os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
WORK=os.environ.get("WORK",os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,WORK)
import json
import beats as B, layout as L
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
V=sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith("-") else os.environ.get("QCIN",f"{WORK}/website_video_16x9.mp4")
CAP=sys.argv[2] if len(sys.argv)>2 else f"{WORK}/cap.ass"
G=f"{WORK}/gfx"; PV=f"{WORK}/pv"; os.makedirs(PV,exist_ok=True)
W,H=1920,1080
MIN_GAP=20; HEAD_MIN,HEAD_SEG_MIN,HEAD_MEDIAN,HEAD_MAX=15,45,60,100
# HEAD_MAX is a sanity ceiling against an anchor that FAILED (rev 2 read 159-261), not a framing target:
# measured on rev 3, his posture inside a 14 s TIGHT hold spans up to ~75 px of 4K below his tallest
# instant = 33 + 62 = 95 px at 1080p with the anchor exactly on design. The anchor is asserted per segment.
fails=[]
def check(ok,msg):
    print(("  PASS  " if ok else "  FAIL  ")+msg)
    if not ok: fails.append(msg)

# ------------------------------------------------------------------ 10 caption clearance
def _secs(x):
    h,m,s=x.split(":"); return int(h)*3600+int(m)*60+float(s)
def _events():
    head,ev=[],[]
    for l in open(CAP):
        l=l.rstrip("\n")
        if l.startswith("Dialogue:"): ev.append(l)
        elif not ev: head.append(l)
    return head,ev
def ink_bbox(head,ev):
    """render this one cue over pure green at t=1 s and return the bbox of everything that is not green"""
    f=ev.split(",",9); f[1],f[2]="0:00:00.00","0:00:02.00"
    tmp=f"{PV}/_cue.ass"; open(tmp,"w").write("\n".join(head)+"\n"+",".join(f)+"\n")
    raw=subprocess.run([FF,"-v","error","-f","lavfi","-i",f"color=c=0x00FF00:s={W}x{H}:r=30:d=2",
        "-vf",f"ass={tmp}","-ss","1","-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    if len(raw)<W*H*3: return None
    a=np.frombuffer(raw[:W*H*3],np.uint8).reshape(H,W,3).astype(int)
    ink=~((a[...,0]<60)&(a[...,1]>190)&(a[...,2]<60))
    ys,xs=np.where(ink)
    return None if len(ys)==0 else (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
def alpha_bbox(mov,dt):
    raw=subprocess.run([FF,"-v","error","-ss",f"{max(0.0,dt):.3f}","-i",mov,"-frames:v","1","-f","rawvideo",
                        "-pix_fmt","rgba","-"],capture_output=True).stdout
    if len(raw)<W*H*4: return None
    al=np.frombuffer(raw[:W*H*4],np.uint8).reshape(H,W,4)[...,3]
    ys,xs=np.where(al>8)
    return None if len(ys)==0 else (int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max()))
def _union(bbs):
    bbs=[b for b in bbs if b]
    return None if not bbs else (min(b[0] for b in bbs),min(b[1] for b in bbs),max(b[2] for b in bbs),max(b[3] for b in bbs))
def vgap(c,g):
    """vertical clearance between a caption bbox and a graphic bbox; None = no horizontal overlap;
    negative = they overlap"""
    if c[2]<g[0] or c[0]>g[2]: return None
    if c[3]<g[1]: return g[1]-c[3]
    if c[1]>g[3]: return c[1]-g[3]
    return -(min(c[3],g[3])-max(c[1],g[1]))

def caption_clearance():
    head,ev=_events()
    lowers={n:B.BEATS[n] for n in B.OVERLAY}
    pips=[B.BEATS[n] for n in sorted(B.PANEL)]                       # REV 4: both phone PiPs (macro + hub)
    ais=[B.BEATS[n] for n in sorted(B.AI)]
    tagim=Image.open(f"{G}/tag15.png"); TAG=(40,40,40+tagim.size[0],40+tagim.size[1])
    gaps=[]; coll=[]; pipbad=[]; tagbad=[]; checked=0
    for e in ev:
        f=e.split(",",9); ca,cb=_secs(f[1]),_secs(f[2]); txt=f[9]
        hits=[(n,ab) for n,ab in lowers.items() if not (cb<=ab[0]+0.02 or ca>=ab[1]-0.02)]
        inpip=any(not (cb<=p[0]+0.02 or ca>=p[1]-0.02) for p in pips)
        inai=any(not (cb<=p[0]+0.02 or ca>=p[1]-0.02) for p in ais)
        if not hits and not inpip and not inai: continue
        ink=ink_bbox(head,e)
        if ink is None: continue
        checked+=1
        for n,(a,b) in hits:
            lo,hi=max(ca,a),min(cb,b)
            ts=[lo+0.03,(lo+hi)/2,hi-0.03] if hi-lo>0.1 else [(lo+hi)/2]
            g=_union([alpha_bbox(f"{G}/{n.lower()}.mov",min(t-a,(b-a)-0.04)) for t in ts])
            if g is None: continue
            gp=vgap(ink,g)
            if gp is None: continue
            gaps.append((gp,round(ca,2),n,txt,ink,g))
            if gp<MIN_GAP: coll.append((round(ca,2),n,gp,txt[:40]))
        if inpip:
            px0,py0,px1,py1=L.PIP_BOX
            if not (ink[0]>=px1+MIN_GAP or ink[2]<=px0-MIN_GAP or ink[3]<py0 or ink[1]>py1):
                pipbad.append((round(ca,2),ink,txt[:40]))
        if inai:
            gp=vgap(ink,TAG)
            if gp is not None and gp<MIN_GAP: tagbad.append((round(ca,2),gp,txt[:40]))
    if gaps:
        gs=sorted(g[0] for g in gaps)
        print(f"  caption vs lower third: {len(gaps)} cue/graphic pairs over {checked} cues   gap min {gs[0]} px  median {gs[len(gs)//2]} px  max {gs[-1]} px")
        worst=min(gaps,key=lambda g:g[0])
        print(f"  tightest: {worst[1]}s {worst[2]} gap {worst[0]} px  caption ink y {worst[4][1]}-{worst[4][3]}  graphic y {worst[5][1]}-{worst[5][3]}  {worst[3][:50]!r}")
    check(not coll,f"every caption clears its lower third by >= {MIN_GAP} px (measured ink vs alpha): {coll[:5]}")
    check(not pipbad,f"no caption ink inside or within {MIN_GAP} px of the phone box {L.PIP_BOX} (both PiPs): {pipbad[:3]}")
    check(not tagbad,f"no caption ink within {MIN_GAP} px of the AI-GENERATED tag {TAG} on the AI inserts: {tagbad[:3]}")

# ------------------------------------------------------------------ 11 HAIR on the delivered frames (hairgate.py)
def hair():
    import hairgate as HG
    HT=json.load(open(f"{WORK}/hairtrack.json"))
    segs=[(a,b,l,c) for (a,b,l),c in zip(L.PUNCH,L.CROPS)]
    cards=[B.BEATS[n] for n in B.BEATS if n not in B.OVERLAY and n not in B.PANEL]   # Dan replaced: cards + AI inserts
    f,info=HG.run(V,segs,cards,HT["hdr_col"],L.DAN_CX,pv=PV)
    fails.extend(f)

# ------------------------------------------------------------------ 13 the AI tag, measured on the delivered pixels
def ai_tags():
    tag=Image.open(f"{G}/tag15.png").convert("RGBA"); tw,th=tag.size; tw-=tw%2; th-=th%2     # ffmpeg crops to even sizes
    ref=np.asarray(Image.alpha_composite(Image.new("RGBA",tag.size,(80,80,80,255)),tag).convert("L"),dtype=float)[:th,:tw]
    bad=[]; scores=[]
    for n,(a,b),_,_ in L.AIV:
        for t in (a+0.9,(a+b)/2,b-0.9):
            raw=subprocess.run([FF,"-v","error","-ss",f"{t:.3f}","-i",V,"-frames:v","1","-vf",f"crop={tw}:{th}:40:40","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
            if len(raw)<tw*th: bad.append((n,round(t,2),"no frame")); continue
            got=np.frombuffer(raw[:tw*th],np.uint8).reshape(th,tw).astype(float)
            c=float(np.corrcoef(ref.ravel(),got.ravel())[0,1]); scores.append(round(c,3))
            if c<0.85: bad.append((n,round(t,2),round(c,3)))
    print(f"  tag correlation over {len(scores)} frames: min {min(scores) if scores else None}  median {sorted(scores)[len(scores)//2] if scores else None}")
    check(not bad,f"the AI-GENERATED tag reads at (40,40) on every AI insert, start/middle/end (corr >= 0.85): {bad[:4]}")

if __name__=="__main__":
    print(f"qc_frame  {os.path.basename(V)}  ({WORK})")
    print("10 caption clearance"); caption_clearance()
    print("11 hair"); hair()
    print("13 AI tags"); ai_tags()
    print("\n"+("QC_FRAME PASSED" if not fails else f"QC_FRAME FAILED -- {len(fails)} check(s)"))
    sys.exit(1 if fails else 0)
