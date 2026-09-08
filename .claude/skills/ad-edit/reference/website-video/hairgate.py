#!/usr/bin/env python3
"""The delivered-frame HAIR gate (ad-edit lesson 107 c): measured on the finished 1080p master, independent of the plan.

Two tests, and the second does not depend on finding anything:
  A  hairdet.detect on the delivered picture every 0.25 s wherever Dan is on camera: the head region is cropped from the
     1080p frame, resized to 4K scale through that segment's crop and fed to the SAME detector as the plan, with the
     door panel's static per-column luma (hairtrack.json hdr_col) mapped through the crop. Reports the hair top in px
     below the top edge. FAIL if any valid sample is < HAIR_MIN px; per segment the minimum must be within
     [SEG_MIN, SEG_MAX] (the crop IS anchored to his tallest instant, not loose); the median over the video <= MEDIAN_MAX.
  B  EVERY FRAME: the top TOP_ROWS rows of the head band must NOT be hair-coloured -- the fraction of pixels darker than
     (door panel column luma - 5) must stay under DARK_MAX. Hair against the edge reads 0.5+; the door panel reads ~0.03.
     A gate built from the plan's own detector inherits its bias (rev 3 passed 21-95 px of 'headroom' to the wrong
     point); this test would have failed rev 3 on frame one.
Proof frames: the six tightest and three loosest valid samples at native 1080p, pv/hair_tight*.png / pv/hair_loose*.png
and the sheet pv/hairgate_sheet.jpg -- the executor LOOKS at them.
  WORK=<dir> python3 hairgate.py <master.mp4>      (imports that dir's layout.py/beats.py for the segments and cards)
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import hairdet as HD
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
HAIR_MIN=20; SEG_MIN=30; SEG_MAX=70; MEDIAN_MAX=75; TOP_ROWS=12; DARK_MAX=0.20
def _frames(video,fps,vf):
    p=subprocess.Popen([FF,"-v","error","-i",video,"-vf",(f"fps={fps},"+vf if fps else vf),"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
    return p
def run(video, segs, cards, hdr_col, dan_cx=1980, fps=4, pv=None, tag=""):
    """segs: [(a,b,level,(x0,y0,w,h))] in 4K crop units; cards: [(a,b)] beats where Dan is replaced. Returns (fails, info)."""
    fails=[]; info={}
    hdr=np.array(hdr_col,dtype=float)
    # for the top-rows test the door's vertical grooves must never count as hair when the delivered frame's scaling puts a
    # groove edge one column off the base profile: take the MINIMUM of the profile over +-3 columns (a lower threshold
    # around every groove). Hair is 20-30 luma against a 36-37 panel, so this costs the hair test nothing.
    hdr_lo=np.array([hdr[max(0,i-3):i+4].min() for i in range(len(hdr))])
    def seg_at(t): return next((s for s in segs if s[0]<=t<s[1]),None)
    def on_cam(t): return not any(a-0.6<=t<=b+0.6 for a,b in cards)
    # ---- A: the detector on the delivered frames
    W,H=1920,1080; p=_frames(video,fps,f"scale={W}:{H}"); samples=[]; k=0
    while True:
        buf=p.stdout.read(W*H*3)
        if len(buf)<W*H*3: break
        t=k/fps; k+=1; s=seg_at(t)
        if s is None or not on_cam(t): continue
        a,b,lvl,(x0,y0,cw,ch)=s; kk=ch/1080.0                      # 4K px per delivered px
        cx=(dan_cx-x0)/kk                                            # Dan's centre in delivered px
        rx0=int(max(0,cx-420/kk)); rx1=int(min(W,cx+420/kk)); ry1=int(min(H,720/kk))
        fr=np.frombuffer(buf,np.uint8).reshape(H,W,3)[0:ry1, rx0:rx1]
        im=np.asarray(Image.fromarray(fr).resize((int(round((rx1-rx0)*kk)),int(round(ry1*kk))),Image.BILINEAR)).astype(int)
        d=HD.detect(im, cx_guess=dan_cx, X0=x0+rx0*kk, hdr_col=hdr)
        samples.append((t, (d["hair"]/kk if d["valid"] else None), lvl, d))
    p.wait()
    valid=[(t,h,l) for t,h,l,_ in samples if h is not None]
    hs=np.array([h for _,h,_ in valid]) if valid else np.array([0.0])
    info["n"]=len(samples); info["valid"]=len(valid)
    print(f"  hair top on the delivered frames{tag}: {len(samples)} samples with Dan on camera, {len(valid)} valid, {len(samples)-len(valid)} discarded (climb outside {HD.CLIMB})")
    print(f"  hair top below the top edge (px @1080p): min {hs.min():.0f}  p5 {np.percentile(hs,5):.0f}  median {np.median(hs):.0f}  p95 {np.percentile(hs,95):.0f}  max {hs.max():.0f}")
    for lvl in sorted({s[2] for s in segs}):
        v=[h for _,h,l in valid if l==lvl]
        if v: print(f"    {lvl:5s} n={len(v):3d}  min {min(v):5.1f}  median {np.median(v):5.1f}  max {max(v):5.1f}")
    segmin=[]
    for a,b,l,_ in segs:
        v=[h for t,h,_ in valid if a<=t<b]
        segmin.append((round(a,2),l,(round(min(v)) if v else None)))
    nosample=[s for s in segmin if s[2] is None and not all(any(ca-0.6<=t<=cb+0.6 for ca,cb in cards) for t in np.arange(s[0],s[0]+0.01,1))]
    loose=[s for s in segmin if s[2] is not None and s[2]>SEG_MAX]; tight=[s for s in segmin if s[2] is not None and s[2]<SEG_MIN]
    print(f"  per-segment minimum: {[s[2] for s in segmin]}")
    def check(ok,msg):
        print(("  PASS  " if ok else "  FAIL  ")+msg)
        if not ok: fails.append(msg)
    check(len(valid)>=0.6*max(1,len(samples)),f"detector agreement on the delivered frames: >= 60 % of samples valid ({len(valid)}/{len(samples)})")
    check(hs.min()>=HAIR_MIN,f"HAIR NEVER CUT: hair top >= {HAIR_MIN} px below the top edge on every valid frame (min {hs.min():.0f} px)")
    check(not tight,f"no segment anchors the hair closer than {SEG_MIN} px (min over the segment): {tight[:5]}")
    check(not loose,f"every segment brings the hair within {SEG_MAX} px of the top edge (crop anchored, not loose): {loose[:5]}")
    check(np.median(hs)<=MEDIAN_MAX,f"median hair top over the video <= {MEDIAN_MAX} px (got {np.median(hs):.0f})")
    # ---- B: every frame, the top rows of the head band must not be hair-coloured
    p=_frames(video,None,f"crop=1920:{TOP_ROWS}:0:0"); FD=1001/30000; k=0; worst=(0.0,None); bad=[]; nfr=0
    while True:
        buf=p.stdout.read(1920*TOP_ROWS*3)
        if len(buf)<1920*TOP_ROWS*3: break
        t=k*FD; k+=1; s=seg_at(t)
        if s is None or not on_cam(t): continue
        a,b,lvl,(x0,y0,cw,ch)=s; kk=ch/1080.0; cx=(dan_cx-x0)/kk; half=int(80/kk)
        lo,hi=int(max(0,cx-half)),int(min(1920,cx+half))
        fr=np.frombuffer(buf,np.uint8).reshape(TOP_ROWS,1920,3)[:,lo:hi].astype(float)
        Y=0.299*fr[...,0]+0.587*fr[...,1]+0.114*fr[...,2]
        cols4k=x0+np.arange(lo,hi)*kk; thr=np.interp(cols4k,np.arange(len(hdr_lo)),hdr_lo)-5.0
        frac=float((Y<thr[None,:]).mean()); nfr+=1
        if frac>worst[0]: worst=(frac,round(t,2))
        if frac>=DARK_MAX: bad.append((round(t,2),round(frac,2)))
    p.wait()
    info["top_rows_worst"]=worst; info["top_rows_bad"]=len(bad)
    print(f"  top {TOP_ROWS} rows of the head band on EVERY frame ({nfr} frames): worst hair-dark fraction {worst[0]:.3f} at {worst[1]}s; {len(bad)} frame(s) at or above {DARK_MAX}")
    check(not bad,f"INDEPENDENT TEST: no frame has hair-coloured pixels in the top {TOP_ROWS} rows of the head band (>= {DARK_MAX}): {bad[:6]}")
    # ---- proof frames
    if pv and valid:
        os.makedirs(pv,exist_ok=True)
        try: fnt=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf",22)
        except Exception: fnt=ImageFont.load_default()
        picks=[("tight",x) for x in sorted(valid,key=lambda v:v[1])[:6]]+[("loose",x) for x in sorted(valid,key=lambda v:-v[1])[:3]]
        TW,TH=640,360; sheet=Image.new("RGB",(TW*3,(TH+26)*3),(0,0,0)); d=ImageDraw.Draw(sheet)
        for n,(kind,(t,h,l)) in enumerate(picks):
            raw=subprocess.run([FF,"-v","error","-ss",f"{t:.3f}","-i",video,"-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
            if len(raw)<1920*1080*3: continue
            full=Image.frombytes("RGB",(1920,1080),raw[:1920*1080*3])
            s=seg_at(t); x0,y0,cw,ch=s[3]; kk=ch/1080.0; cx=int((dan_cx-x0)/kk)
            crop=full.crop((max(0,cx-320),0,max(0,cx-320)+TW,TH)); cd=ImageDraw.Draw(crop)   # NATIVE 1080p pixels, no scaling
            cd.line([(0,int(h)),(TW,int(h))],fill=(0,255,0),width=2)
            for gy in range(0,TH,50): cd.line([(0,gy),(14,gy)],fill=(255,0,0),width=1); cd.text((16,gy-8),str(gy),fill=(255,255,0),font=fnt)
            crop.save(f"{pv}/hair_{kind}{n%6+1 if kind=='tight' else n-5}.png")
            X=(n%3)*TW; Yy=(n//3)*(TH+26); sheet.paste(crop,(X,Yy+26))
            d.text((X+4,Yy+2),f"{kind}  {t:.2f}s  {l}  hair top {h:.0f} px below the edge (native 1080p crop)",fill=(255,255,0),font=fnt)
        sheet.save(f"{pv}/hairgate_sheet.jpg",quality=90); print(f"  proof frames: {pv}/hairgate_sheet.jpg (+ hair_tight1-6.png, hair_loose1-3.png), native 1080p")
    return fails, info
if __name__=="__main__":
    WORK=os.environ.get("WORK",HERE); sys.path.insert(0,WORK)
    import importlib; B=importlib.import_module("beats"); L=importlib.import_module("layout")
    V=sys.argv[1] if len(sys.argv)>1 else f"{WORK}/website_video_16x9.mp4"
    HT=json.load(open(f"{HERE}/hairtrack.json"))
    segs=[(a,b,l,c) for (a,b,l),c in zip(L.PUNCH,L.CROPS)]
    cards=[B.BEATS[n] for n in B.BEATS if n not in B.OVERLAY and n not in B.PANEL]
    print(f"hairgate  {os.path.basename(V)}  segments {len(segs)}  cards {len(cards)}")
    fails,info=run(V,segs,cards,HT["hdr_col"],getattr(L,"DAN_CX",1980),pv=os.environ.get("PV"))
    print("\n"+("HAIR GATE PASSED" if not fails else f"HAIR GATE FAILED -- {len(fails)} check(s)"))
    sys.exit(1 if fails else 0)
