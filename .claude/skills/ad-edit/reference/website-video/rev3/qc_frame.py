#!/usr/bin/env python3
"""Website video QC -- the two checks rev 2 did not have (ad-edit lessons 97 and 99), measured on the
DELIVERED pixels, never on the plan. Rev 2 passed 14/14 and Dan rejected it on both of these.

 10 CAPTION CLEARANCE. For every caption cue that overlaps a lower-third beat: render the cue alone
    over a green frame and take its ink bbox (fill + outline + shadow); take the lower third's alpha
    bbox from the graphic's own MOV at three points across the cue; wherever the two overlap
    horizontally, assert a >= 20 px vertical gap. Every cue during the phone PiP keeps its ink out of
    the phone box. (Rev 2: MarginV 300 inked at 727-806 over lower thirds at 757-905 -- 49 px of
    overlap on every lower-third beat; QC only compared captions against full-frame cards.)
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
    pip=B.BEATS[sorted(B.PANEL)[0]] if B.PANEL else None
    gaps=[]; coll=[]; pipbad=[]; checked=0
    for e in ev:
        f=e.split(",",9); ca,cb=_secs(f[1]),_secs(f[2]); txt=f[9]
        hits=[(n,ab) for n,ab in lowers.items() if not (cb<=ab[0]+0.02 or ca>=ab[1]-0.02)]
        inpip=pip and not (cb<=pip[0]+0.02 or ca>=pip[1]-0.02)
        if not hits and not inpip: continue
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
    if gaps:
        gs=sorted(g[0] for g in gaps)
        print(f"  caption vs lower third: {len(gaps)} cue/graphic pairs over {checked} cues   gap min {gs[0]} px  median {gs[len(gs)//2]} px  max {gs[-1]} px")
        worst=min(gaps,key=lambda g:g[0])
        print(f"  tightest: {worst[1]}s {worst[2]} gap {worst[0]} px  caption ink y {worst[4][1]}-{worst[4][3]}  graphic y {worst[5][1]}-{worst[5][3]}  {worst[3][:50]!r}")
    check(not coll,f"every caption clears its lower third by >= {MIN_GAP} px (measured ink vs alpha): {coll[:5]}")
    check(not pipbad,f"no caption ink inside or within {MIN_GAP} px of the phone box {L.PIP_BOX}: {pipbad[:3]}")

# ------------------------------------------------------------------ 11 headroom on the delivered frames
def _grab(t,w=960,h=540):
    raw=subprocess.run([FF,"-v","error","-ss",f"{t:.3f}","-i",V,"-frames:v","1","-vf",f"scale={w}:{h}",
                        "-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    return Image.frombytes("RGB",(w,h),raw[:w*h*3]) if len(raw)>=w*h*3 else None
def headroom():
    crops=L.CROPS if hasattr(L,"CROPS") else [L.LEVELS[l] for _,_,l in L.PUNCH]
    segs=[(a,b,l,c) for (a,b,l),c in zip(L.PUNCH,crops)]
    cards=[B.BEATS[n] for n in B.BEATS if n not in B.OVERLAY and n not in B.PANEL]   # Dan replaced
    FPS=4; w,h=960,540; hair4k=40
    p=subprocess.Popen([FF,"-v","error","-i",V,"-vf",f"fps={FPS},scale={w}:{h}","-f","rawvideo","-pix_fmt","rgb24","-"],
                       stdout=subprocess.PIPE)
    samples=[]; k=0
    while True:
        buf=p.stdout.read(w*h*3)
        if len(buf)<w*h*3: break
        t=k/FPS; k+=1
        seg=next(((a,b,l,c) for a,b,l,c in segs if a<=t<b),None)
        if seg is None or any(s-0.6<=t<=e+0.6 for s,e in cards): continue
        a,b,l,(cx0,cy0,cw,ch)=seg
        cx=int(round((L.DAN_CX-cx0)/cw*w)) if hasattr(L,"DAN_CX") else int(round((1980-cx0)/cw*w))
        fr=np.frombuffer(buf,np.uint8).reshape(h,w,3).astype(int)
        band=fr[:, cx-45:cx+45]; r,g,bb=band[...,0],band[...,1],band[...,2]
        skin=((r>g+15)&(g>bb)&(r>120)).mean(1)
        hit=np.where(skin[:220]>=0.30)[0]
        ht=None if len(hit)==0 else int(hit[0])*(1080/h)-hair4k*1080/ch      # 1080p px below the top edge
        samples.append((t,ht,l))
    p.wait()
    # validity: misses read LOW (large headroom); keep a sample when it sits within 40 px of the
    # minimum over +-1.5 s
    valid=[]; rejected=0; nodet=0
    for i,(t,ht,l) in enumerate(samples):
        if ht is None: nodet+=1; continue
        loc=[h2 for t2,h2,_ in samples[max(0,i-6):i+7] if h2 is not None]
        if ht-min(loc)<=40: valid.append((t,ht,l))
        else: rejected+=1
    hs=np.array([v[1] for v in valid])
    print(f"  headroom on the delivered frames: {len(samples)} samples with Dan on camera, {len(valid)} valid, "
          f"{rejected} look-down misses rejected, {nodet} without a detection")
    print(f"  head top below the top edge (px @1080p): min {hs.min():.0f}  p5 {np.percentile(hs,5):.0f}  median {np.median(hs):.0f}  "
          f"p95 {np.percentile(hs,95):.0f}  max {hs.max():.0f}")
    for lvl in ("WIDE","MID","TIGHT","PIP"):
        v=[x[1] for x in valid if x[2]==lvl]
        if v: print(f"    {lvl:5s} n={len(v):3d}  min {min(v):5.1f}  median {np.median(v):5.1f}  max {max(v):5.1f}")
    segmin=[]
    for a,b,l,_ in segs:
        v=[x[1] for x in valid if a<=x[0]<b]
        if v: segmin.append((round(a,2),l,round(min(v))))
    loose=[s for s in segmin if s[2]>HEAD_SEG_MIN]
    print(f"  per-segment minimum headroom: {[s[2] for s in segmin]}")
    check(rejected<=0.30*len(samples),f"detector agreement: <= 30 % of samples rejected as misses ({rejected}/{len(samples)})")
    check(hs.min()>=HEAD_MIN,f"head never cut or cramped: head top >= {HEAD_MIN} px below the top edge on every valid frame (min {hs.min():.0f})")
    check(not loose,f"every punch segment brings the head within {HEAD_SEG_MIN} px of the top edge (crop anchored to the head): {loose[:5]}")
    check(np.median(hs)<=HEAD_MEDIAN,f"median headroom over the video <= {HEAD_MEDIAN} px (got {np.median(hs):.0f})")
    check(hs.max()<=HEAD_MAX,f"no valid frame carries more than {HEAD_MAX} px of headroom (max {hs.max():.0f})")
    # proof frames: the three with the most headroom and the three tightest
    try: fnt=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf",20)
    except Exception: fnt=ImageFont.load_default()
    picks=[("worst",x) for x in sorted(valid,key=lambda v:-v[1])[:3]]+[("tight",x) for x in sorted(valid,key=lambda v:v[1])[:3]]
    sheet=Image.new("RGB",(960*3,(540+26)*2),(0,0,0)); d=ImageDraw.Draw(sheet)
    for n,(kind,(t,ht,l)) in enumerate(picks):
        im=_grab(t)
        if im is None: continue
        x=(n%3)*960; y=(n//3)*566
        sheet.paste(im,(x,y+26)); yy=y+26+int(ht/2)
        d.line([(x,yy),(x+960,yy)],fill=(255,0,0),width=2)
        d.text((x+4,y+3),f"{kind} #{n%3+1}  {t:.2f}s  {l}  head top {ht:.0f} px below the edge",font=fnt,fill=(255,255,0))
        im2=im.copy(); ImageDraw.Draw(im2).line([(0,int(ht/2)),(960,int(ht/2))],fill=(255,0,0),width=2)
        im2.save(f"{PV}/headroom_{kind}{n%3+1}.png")
    sheet.save(f"{PV}/headroom_sheet.jpg",quality=90)
    print(f"  proof frames: {PV}/headroom_sheet.jpg (+ headroom_worst1-3.png, headroom_tight1-3.png)")

if __name__=="__main__":
    print(f"qc_frame  {os.path.basename(V)}  ({WORK})")
    print("10 caption clearance"); caption_clearance()
    print("11 headroom"); headroom()
    print("\n"+("QC_FRAME PASSED" if not fails else f"QC_FRAME FAILED -- {len(fails)} check(s)"))
    sys.exit(1 if fails else 0)
