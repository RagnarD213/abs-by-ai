#!/usr/bin/env python3
"""REV 6 item 2 -- the pale spray-tan patch on Dan's cheek (VIEWER'S LEFT, his right, beside the mouth).

Measured on rev 5 at 14.0 s (handoff): a flat MULTIPLICATIVE lift, x1.145 / 1.148 / 1.161 over the surrounding cheek,
~38 px square at 1080p, centroid (985,288). The fix is a feathered GAIN on the patch, deliberately UNDER-corrected
(GAIN=0.90 against the measured 0.87), never a blur, clone or desaturation -- texture and colour ratios survive.

The region is anchored to FACE LANDMARKS (mediapipe FaceLandmarker, 478 points, CPU delegate -- Metal crashes on this
Mac), never to a brightness search (the handoff's brightest-blob search locked onto the doorframe). The patch is the
set of mesh indices that fall inside the hand-confirmed 14.0 s box; every other frame takes the convex hull of those
same indices, so the mask rides the face through every turn. The pass runs on nocap.mov (the mixed picture BEFORE
audio/captions); it only touches frames where Dan is on camera (AI inserts and full-frame cards are skipped) and
asserts the region never enters the phone box.

  python3 tanpass.py track                       -> tanpass_track.json (per-frame patch hull + anchors, keys to the cut)
  python3 tanpass.py proof                       -> pv/tan_proof.jpg  (native crops: before | after | mask, extreme frames)
  GAIN=0.90 python3 tanpass.py render nocap_A.mov
  GAIN=1.00 python3 tanpass.py render nocap_B.mov  (identical pipeline, correction off -- removes the encode confound)
  python3 tanpass.py gate nocap.mov nocap_A.mov  -> patch-vs-surround ratio on N frames: mean + variance must drop
"""
import hashlib, json, os, subprocess, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import beats as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
HERE=os.path.dirname(os.path.abspath(__file__)); PV=f"{HERE}/pv"
SRC=os.environ.get("TAN_IN", f"{HERE}/nocap.mov")
TRACK=f"{HERE}/tanpass_track.json"
MODEL=os.environ.get("FACE_MODEL", "/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/f6290172-b341-4d83-8d42-ab0bc897ab24/scratchpad/face_landmarker.task")
W,H=1920,1080; FPS=30000/1001
GAIN=float(os.environ.get("GAIN","0.90"))
PIP_BOX=[150,130,583,950]
# the hand-confirmed box at 14.0 s (rev-5 master == nocap.mov picture there; the NAME lower third is long gone)
BOX=(950,255,1014,342); T_BOX=14.0
# face crop handed to the detector (full-res, never a downscale): Dan's head across every level incl. PIP (pushed right)
CX0,CY0,CW,CH=600,0,1100,700
DILATE=8; FEATHER=9          # px: hull grown by DILATE, then a Gaussian of sigma FEATHER -> no visible edge
EDGE_FADE=6                  # frames: the correction ramps in/out at the ends of every detected run
GAP_FILL=8                   # frames: a detection gap this short is interpolated, longer = correction off
_sig=hashlib.md5(json.dumps(json.load(open(f"{HERE}/tight_cuts.json"))["keeps"]).encode()).hexdigest()[:12]

def on_camera_spans():
    """frames where Dan is visible: everything except the OPAQUE middle of AI inserts and full-frame cards"""
    cov=sorted((a,b) for n,(a,b) in B.BEATS.items() if n not in B.OVERLAY and n not in B.PANEL)
    merged=[]
    for a,b in cov:                      # A->B, C1->C2, D1->D2->D3 are straight cuts: one opaque span each
        if merged and a-merged[-1][1]<0.05: merged[-1]=(merged[-1][0],max(merged[-1][1],b))
        else: merged.append((a,b))
    return merged
FADE_HOLD=0.5      # s: inside an insert's alpha fade Dan's LAST landmarks are held and the strength ramps with the fade
def dur(): return float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",SRC],capture_output=True,text=True).stdout)

def frames(video, x0=0,y0=0,w=W,h=H):
    p=subprocess.Popen([FF,"-v","error","-i",video,"-vf",f"crop={w}:{h}:{x0}:{y0}","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE,bufsize=w*h*3*4)
    k=0
    while True:
        buf=p.stdout.read(w*h*3)
        if len(buf)<w*h*3: break
        yield k, np.frombuffer(buf,np.uint8).reshape(h,w,3); k+=1
    p.wait()

def landmarker():
    import mediapipe as mp
    from mediapipe.tasks.python import vision, BaseOptions
    bo=BaseOptions(model_asset_path=MODEL, delegate=BaseOptions.Delegate.CPU)
    return mp, vision, vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=bo,num_faces=1,running_mode=vision.RunningMode.IMAGE))

ANCH=[1,234,454,61,291,33,263,10,152]     # nose tip, cheek edges, mouth corners, eye outers, forehead, chin
LIPS=[61,146,91,181,84,17,314,405,321,375,291,409,270,269,267,0,37,39,40,185]   # outer lip ring -> carved out of the mask and the surround ring
MOUTH=set(LIPS)|{78,95,88,178,87,14,317,402,318,324,308,415,310,311,312,13,82,81,80,191,62,76,77,96,89,90,180,179,86,15,16,85,316,315,403,319,325,307,306,292,408,304,303,302,11,72,73,74,41,42,38,12}   # inner ring + corners: never part of the patch
def track():
    mp,vision,lm=landmarker()
    total=dur(); N=int(round(total*FPS)); spans=on_camera_spans()
    def covered(t): return any(a<=t<=b for a,b in spans)      # True = under an opaque insert/card -> skip
    # 1. the patch indices: the mesh points inside the confirmed box on the 14.0 s frame
    raw=subprocess.run([FF,"-v","error","-ss",f"{T_BOX:.3f}","-i",SRC,"-frames:v","1","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    im=np.frombuffer(raw[:W*H*3],np.uint8).reshape(H,W,3)
    res=lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(im[CY0:CY0+CH,CX0:CX0+CW])))
    pts=np.array([(p.x*CW+CX0,p.y*CH+CY0) for p in res.face_landmarks[0]])
    x0,y0,x1,y1=BOX
    inside=[i for i,(x,y) in enumerate(pts) if x0<=x<=x1 and y0<=y<=y1 and i not in MOUTH]
    assert 6<=len(inside)<=40, f"patch indices {len(inside)} -- box/landmarks disagree"
    print(f"patch = {len(inside)} mesh points inside the 14.0 s box: {inside}")
    # 2. every frame
    rows=[None]*N; det=0
    for k,fr in frames(SRC,CX0,CY0,CW,CH):
        t=k/FPS
        if covered(t): continue
        r=lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=np.ascontiguousarray(fr)))
        if not r.face_landmarks: continue
        P=[(round(p.x*CW+CX0,1),round(p.y*CH+CY0,1)) for p in r.face_landmarks[0]]
        rows[k]={"p":[P[i] for i in inside],"a":[P[i] for i in ANCH],"l":[P[i] for i in LIPS]}; det+=1
        if k%1500==0: print(f"  frame {k}/{N}  {t:.0f}s  detected so far {det}",flush=True)
    st=os.stat(SRC); src_sig=f"{st.st_size}:{int(st.st_mtime)}"
    json.dump({"src":os.path.basename(SRC),"src_sig":src_sig,"keeps_sig":_sig,"box":BOX,"t_box":T_BOX,"idx":inside,"anch":ANCH,"lips":LIPS,"n":N,"rows":rows},open(TRACK,"w"))
    oncam=sum(1 for k in range(N) if not covered(k/FPS))
    print(f"{N} frames, {oncam} with Dan on camera, {det} with a face detected ({det/oncam*100:.1f} %) -> {TRACK}")

def load_track():
    T=json.load(open(TRACK)); assert T["keeps_sig"]==_sig, "tanpass_track.json is stale for this cut -- run track"
    st=os.stat(SRC); assert T.get("src_sig")==f"{st.st_size}:{int(st.st_mtime)}", "tanpass_track.json was measured on a different picture -- run track on this nocap.mov"
    rows=T["rows"]; N=T["n"]
    # interpolate gaps <= GAP_FILL, then a 5-frame median on every coordinate (jitter), then the per-run edge fade
    P=np.full((N,len(T["idx"]),2),np.nan); A=np.full((N,len(T["anch"]),2),np.nan); Lp=np.full((N,len(T["lips"]),2),np.nan)
    for k,r in enumerate(rows):
        if r: P[k]=r["p"]; A[k]=r["a"]; Lp[k]=r["l"]
    ok=~np.isnan(P[:,0,0])
    def fill(X):
        X=X.copy(); k=0
        while k<N:
            if not np.isnan(X[k,0,0]): k+=1; continue
            j=k
            while j<N and np.isnan(X[j,0,0]): j+=1
            if 0<k and j<N and j-k<=GAP_FILL:
                for m in range(k,j):
                    w=(m-k+1)/(j-k+1); X[m]=(1-w)*X[k-1]+w*X[j]
            k=j
        return X
    P,A,Lp=fill(P),fill(A),fill(Lp); valid=~np.isnan(P[:,0,0])
    def med5(X):
        Y=X.copy()
        for k in range(N):
            if not valid[k]: continue
            lo=max(0,k-2); hi=min(N,k+3); win=[X[m] for m in range(lo,hi) if valid[m]]
            Y[k]=np.median(np.stack(win),axis=0)
        return Y
    P,A,Lp=med5(P),med5(A),med5(Lp)
    # frames under an insert/card (fades included) are never corrected from their own detection -- a blended frame
    # can hand the detector the AI man's face (rev-6 proof sheet, frame 3715: yaw 151, strength 1.0 on the wrong face)
    spans=on_camera_spans(); nf=int(round(FADE_HOLD*FPS))
    edges=[(int(round(a*FPS)),int(round(b*FPS))) for a,b in spans]
    for ka,kb in edges: valid[ka:kb+1]=False
    # sanity: a detection whose yaw or face width is wild is a wrong face -> invalid
    fw=A[:,2,0]-A[:,1,0]; med_fw=np.nanmedian(fw[valid]) if valid.any() else 1
    with np.errstate(invalid="ignore"):
        wild=valid&((fw<0.6*med_fw)|(fw>1.5*med_fw))
    valid[wild]=False
    # strength: 0 where invalid, ramps over EDGE_FADE frames at each end of a detection run (dropouts) -- except at an
    # insert boundary, where the FADE_HOLD below takes over
    S=np.zeros(N); k=0
    bnd=set(x for ka,kb in edges for x in (ka-1,kb+1))
    while k<N:
        if not valid[k]: k+=1; continue
        j=k
        while j<N and valid[j]: j+=1
        for m in range(k,j):
            e_in=1.0 if k in bnd or k==0 else min(m-k+1,EDGE_FADE)/EDGE_FADE
            e_out=1.0 if (j-1) in bnd or j==N else min(j-m,EDGE_FADE)/EDGE_FADE
            S[m]=min(e_in,e_out)
        k=j
    # FADE_HOLD: into an insert, hold the last valid landmarks and ramp the strength down over the fade; out of one,
    # hold the first valid landmarks after it and ramp up. Residual = (1-alpha)*(1-strength)*lift -> peaks at 1/4 mid-fade.
    for ka,kb in edges:
        if ka-1>=0 and valid[ka-1]:
            for m in range(ka,min(ka+nf,kb+1,N)):
                P[m]=P[ka-1]; A[m]=A[ka-1]; Lp[m]=Lp[ka-1]; valid[m]=True; S[m]=S[ka-1]*(1-(m-ka+1)/nf)
        if kb+1<N and valid[kb+1]:
            for m in range(max(kb-nf+1,ka),kb+1):
                if valid[m] and S[m]>0: continue
                P[m]=P[kb+1]; A[m]=A[kb+1]; Lp[m]=Lp[kb+1]; valid[m]=True; S[m]=S[kb+1]*(1-(kb-m+1)/nf)
    # yaw proxy: his right cheek (viewer's left, where the patch is) width vs the other side: (nose - cheek234) / (cheek454 - nose)
    nose,c234,c454=A[:,0,0],A[:,1,0],A[:,2,0]
    with np.errstate(invalid="ignore",divide="ignore"):
        r=(nose-c234)/np.maximum(1,(c454-nose))
    vis=np.clip((r-0.55)/0.35,0,1); vis[~valid]=0          # full correction while the cheek faces camera, off once it turns away
    S=S*vis
    return T,P,A,Lp,valid,S,r

def mask_for(pts, lips):
    """feathered 0..1 mask of the patch hull (dilated), lips carved out"""
    m=np.zeros((H,W),np.uint8)
    hull=cv2.convexHull(np.round(pts).astype(np.int32))
    cv2.fillConvexPoly(m,hull,255)
    m=cv2.dilate(m,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*DILATE+1,2*DILATE+1)))
    lp=cv2.convexHull(np.round(lips).astype(np.int32)); cv2.fillConvexPoly(m,lp,0)
    m=cv2.GaussianBlur(m,(0,0),FEATHER)
    return m.astype(np.float32)/255.0

def hull_bbox(pts):
    x,y=pts[:,0],pts[:,1]; return (x.min()-DILATE-3*FEATHER, y.min()-DILATE-3*FEATHER, x.max()+DILATE+3*FEATHER, y.max()+DILATE+3*FEATHER)

def apply(fr, m, g):
    """multiplicative gain g inside the mask: out = fr * (1 - (1-g)*m)"""
    if g>=0.999: return fr
    gm=1.0-(1.0-g)*m
    ys,xs=np.nonzero(m>0.002)
    if len(ys)==0: return fr
    y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    out=fr.copy()
    out[y0:y1,x0:x1]=np.clip(fr[y0:y1,x0:x1].astype(np.float32)*gm[y0:y1,x0:x1,None]+0.5,0,255).astype(np.uint8)
    return out

def frames_yuv(video):
    """yuv420p planes, NO colour conversion: an rgb24 round trip through swscale darkened every channel by ~1.4 levels
    across the whole picture (measured B - mix at three instants), enough to tip the hair gate's border rows. The gain
    is applied in YUV instead: Y' = 16 + (Y-16)*g, U' = 128 + (U-128)*g -- exact for a multiplicative gain."""
    n=W*H*3//2
    p=subprocess.Popen([FF,"-v","error","-i",video,"-f","rawvideo","-pix_fmt","yuv420p","-"],stdout=subprocess.PIPE,bufsize=n*4)
    k=0
    while True:
        buf=p.stdout.read(n)
        if len(buf)<n: break
        a=np.frombuffer(buf,np.uint8); yield k,(a[:W*H].reshape(H,W),a[W*H:W*H+W*H//4].reshape(H//2,W//2),a[W*H+W*H//4:].reshape(H//2,W//2)); k+=1
    p.wait()
def apply_yuv(planes, m, g):
    Y,U,V=planes
    ys,xs=np.nonzero(m>0.002)
    if len(ys)==0 or g>=0.999: return planes
    y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    gm=1.0-(1.0-g)*m[y0:y1,x0:x1]
    Yo=Y.copy(); Yo[y0:y1,x0:x1]=np.clip(16+(Y[y0:y1,x0:x1].astype(np.float32)-16)*gm+0.5,16,235).astype(np.uint8)
    cy0,cy1,cx0,cx1=y0//2,(y1+1)//2,x0//2,(x1+1)//2
    mc=cv2.resize(m,(W//2,H//2),interpolation=cv2.INTER_AREA)[cy0:cy1,cx0:cx1]; gc=1.0-(1.0-g)*mc
    Uo=U.copy(); Uo[cy0:cy1,cx0:cx1]=np.clip(128+(U[cy0:cy1,cx0:cx1].astype(np.float32)-128)*gc+0.5,16,240).astype(np.uint8)
    Vo=V.copy(); Vo[cy0:cy1,cx0:cx1]=np.clip(128+(V[cy0:cy1,cx0:cx1].astype(np.float32)-128)*gc+0.5,16,240).astype(np.uint8)
    return (Yo,Uo,Vo)
def _color_args(video):
    p=subprocess.run([FFP,"-v","error","-select_streams","v:0","-show_entries","stream=color_space,color_primaries,color_transfer,color_range","-of","csv=p=0",video],capture_output=True,text=True).stdout.strip().split(",")
    out=[]
    for flag,val in zip(("-colorspace","-color_primaries","-color_trc","-color_range"),p):
        if val and val!="unknown": out+=[flag,val]
    return out
def render(out):
    T,P,A,Lp,valid,S,r=load_track(); N=T["n"]
    pip_hits=[]; panel=[B.BEATS[n] for n in B.PANEL]
    enc=subprocess.Popen([FF,"-nostdin","-y","-v","error","-f","rawvideo","-pix_fmt","yuv420p","-s",f"{W}x{H}","-r","30000/1001","-i","-",
        "-i",SRC,"-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","16","-pix_fmt","yuv420p","-r","30000/1001"]+_color_args(SRC)+["-c:a","copy",out],stdin=subprocess.PIPE)
    n_corr=0
    for k,planes in frames_yuv(SRC):
        g=1.0-(1.0-GAIN)*S[k] if valid[k] else 1.0
        if g<0.999:
            bb=hull_bbox(P[k]); t=k/FPS
            if any(a<=t<=b for a,b in panel):
                assert bb[0]>PIP_BOX[2]+10, f"patch region {bb} enters the phone box at {t:.2f}s"
            assert bb[0]>PIP_BOX[2], (t,bb)
            planes=apply_yuv(planes,mask_for(P[k],Lp[k]),g); n_corr+=1
        enc.stdin.write(b"".join(np.ascontiguousarray(pl).tobytes() for pl in planes))
        if k%1500==0: print(f"  frame {k}/{N}  corrected {n_corr}",flush=True)
    enc.stdin.close(); enc.wait(); assert enc.returncode==0
    print(f"{out}: {N} frames, {n_corr} corrected at GAIN {GAIN} (S>0), {int((S>0).sum())} frames with correction strength > 0")

def ring_ratio(fr, pts, lips):
    """median luma of the patch core vs a 10-25 px ring of skin around it (lips excluded)"""
    core=np.zeros((H,W),np.uint8); hull=cv2.convexHull(np.round(pts).astype(np.int32)); cv2.fillConvexPoly(core,hull,255)
    core=cv2.erode(core,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7)))
    k1=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*(DILATE+10)+1,)*2); k2=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*(DILATE+25)+1,)*2)
    base=np.zeros((H,W),np.uint8); cv2.fillConvexPoly(base,hull,255)
    ring=cv2.dilate(base,k2)-cv2.dilate(base,k1)
    lp=cv2.convexHull(np.round(lips).astype(np.int32)); cv2.fillConvexPoly(ring,lp,0)
    f=fr.astype(np.float32); Y=0.299*f[...,0]+0.587*f[...,1]+0.114*f[...,2]
    skin=(f[...,0]>f[...,1]+10)&(f[...,1]>f[...,2])&(f[...,0]>60)
    c=Y[(core>0)&skin]; rg=Y[(ring>0)&skin]
    if len(c)<50 or len(rg)<200: return None
    return float(np.median(c)/np.median(rg))

def gate(before, after):
    T,P,A,Lp,valid,S,r=load_track(); N=T["n"]
    ks=[k for k in range(0,N,15) if valid[k] and S[k]>0.99]
    want=set(ks); rb={}; ra={}
    for vid,store in ((before,rb),(after,ra)):
        for k,fr in frames(vid):
            if k in want:
                v=ring_ratio(fr,P[k],Lp[k])
                if v is not None: store[k]=v
    keys=sorted(set(rb)&set(ra)); b=np.array([rb[k] for k in keys]); a=np.array([ra[k] for k in keys])
    print(f"patch/surround luma ratio on {len(keys)} frames (every 0.5 s where the correction is at full strength)")
    print(f"  before: mean {b.mean():.3f}  sd {b.std():.4f}  min {b.min():.3f}  max {b.max():.3f}")
    print(f"  after : mean {a.mean():.3f}  sd {a.std():.4f}  min {a.min():.3f}  max {a.max():.3f}")
    print(f"  per-frame change: mean {(a-b).mean():+.3f}  sd of the change {np.std(a-b):.4f}  (a constant shift = no flicker)")
    ok_mean=abs(a.mean()-1.0)<abs(b.mean()-1.0); ok_sd=np.std(a-b)<0.02
    print(("PASS" if ok_mean and ok_sd else "FAIL")+f": mean ratio closer to 1.0 {ok_mean}, change is constant across frames {ok_sd}")
    return ok_mean and ok_sd

def proof():
    T,P,A,Lp,valid,S,r=load_track(); N=T["n"]
    # pick: the box frame, the most-turned-toward, the most-turned-away still corrected, and 5 spread across the video
    cand=[k for k in range(N) if valid[k] and S[k]>0.5]
    picks=[int(round(T_BOX*FPS))]+[max(cand,key=lambda k:r[k]), min(cand,key=lambda k:r[k])]+[cand[int(i*(len(cand)-1)/5)] for i in range(1,5)]
    picks+=[int(round((B.AI_C1[0]+0.15)*FPS)), int(round((B.AI_C1[0]+0.4)*FPS)), int(round((B.AI_C2[1]+0.2)*FPS))]   # inside the fades
    picks=sorted(set(picks)); want=set(picks); tiles={}
    for k,fr in frames(SRC):
        if k in want:
            m=mask_for(P[k],Lp[k]); g=1.0-(1.0-GAIN)*S[k]
            aft=apply(fr,m,g); cx,cy=P[k].mean(axis=0); x0=int(cx-160); y0=int(cy-120)
            crop=lambda im: Image.fromarray(np.ascontiguousarray(im[y0:y0+240,x0:x0+320])).resize((640,480),Image.NEAREST)
            ov=fr.copy().astype(np.float32); ov[...,1]=np.clip(ov[...,1]+120*m,0,255); ov=ov.astype(np.uint8)
            tiles[k]=(crop(fr),crop(aft),crop(ov),f"frame {k}  t {k/FPS:.2f}s  yaw {r[k]:.2f}  strength {S[k]:.2f}  gain {g:.3f}")
        if len(tiles)==len(want): break
    fnt=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf",20)
    sheet=Image.new("RGB",(3*640+40,len(picks)*(480+34)+10),(20,20,20)); d=ImageDraw.Draw(sheet)
    for i,k in enumerate(picks):
        b,a,o,lab=tiles[k]; y=10+i*(514)
        d.text((10,y),lab+"    before | after | mask",fill=(255,255,0),font=fnt)
        sheet.paste(b,(10,y+28)); sheet.paste(a,(660,y+28)); sheet.paste(o,(1310,y+28))
    os.makedirs(PV,exist_ok=True); sheet.save(f"{PV}/tan_proof.jpg",quality=90); print(f"{PV}/tan_proof.jpg  frames {picks}")

if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="track": track()
    elif cmd=="render": render(sys.argv[2])
    elif cmd=="gate": print(gate(sys.argv[2],sys.argv[3]))
    elif cmd=="proof": proof()
