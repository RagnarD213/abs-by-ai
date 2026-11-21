#!/usr/bin/env python3
"""Website video -- pass 1 punch/layout over tight.mov (2560x1440 -> 1920x1080), pass 2 overlays.
  python3 layout.py plan | punch | mix

PUNCH RULE (ad-edit lesson 21): a punch change is the cheapest cover for a pause splice, so
punch boundaries land ON splices. TRUST brief: holds are LONG (>= 9 s), only three levels,
crop anchored on Dan's face, no framing change inside the opening line. The base is 1440p
so no level ever upscales.
"""
import json, os, subprocess, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import beats as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
HERE=os.path.dirname(os.path.abspath(__file__))
G=f"{HERE}/gfx"; FPS="30000/1001"; SRC=f"{HERE}/tight.mov"; DUR=B.DUR
L="/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
APP=f"{L}/02 App Screen Recordings and Screenshots"
MACROFLOW=f"{APP}/app-flow-macro-tracker-itemized.mp4"     # 1320x2868, 46.4 s
AFCROP="crop=1320:2500:0:175,"                              # strips the iOS status bar + Safari bar

# Dan's face sits at x~0.50 of frame, head top ~0.055. Crops are top-anchored (y=0) and
# centred on x=0.50 so the eyeline never moves between levels.
SW,SH=2560,1440
def _crop(k):
    w=int(round(SW/k/2)*2); h=int(round(w*9/16/2)*2); x=(SW-w)//2
    return f"crop={w}:{h}:{x}:0,scale=1920:1080:flags=lanczos,"
PANEL_W=980; VID_W=1920-PANEL_W    # 940 px video column on the RIGHT (x 980..1920)
CROP={"A":"scale=1920:1080:flags=lanczos,",
      "B":_crop(1.15),
      "C":_crop(1.30),
      # panel levels: Dan in the right column. P1 = 1.00 crop of the column, P2 = a tighter one
      "P1":f"scale=1920:1080:flags=lanczos,crop={VID_W}:1080:490:0,pad=1920:1080:{PANEL_W}:0:black,",
      "P2":f"scale=1920:1080:flags=lanczos,crop=800:919:560:0,scale={VID_W}:1080:flags=lanczos,pad=1920:1080:{PANEL_W}:0:black,"}
PANEL_BEATS=[B.BEATS[n] for n in sorted(B.PANEL)]
MIN_HOLD=9.0

def splices():
    tc=json.load(open(f"{HERE}/tight_cuts.json")); out,acc=[],0.0
    for a,b in tc["keeps"][:-1]:
        acc+=b-a; out.append(round(acc,3))
    return out

# Splices that MEASURABLY jump on the tight cut (hard_splices.py, ad-edit lesson 64) and are
# not under a full-frame card get a punch change as cover, even below MIN_HOLD -- but never
# closer than SOFT_FLOOR to another bound, so the pacing stays calm.
SOFT_FLOOR=3.5
def _hard_bare(forced=()):
    """bare hard splices, greedily thinned HARDEST-FIRST so that when two sit inside one
    SOFT_FLOOR window the more visible one gets the cover (51.08 s: 2.62 vs 50.35 s: 1.2)"""
    p=f"{HERE}/hard_splices.json"
    if not os.path.exists(p): return []
    det=json.load(open(p))["detail"]
    cov=[B.BEATS[n] for n in B.BEATS if n not in B.OVERLAY]
    cand=[(t,d) for t,d in det if not any(a-0.05<=t<=b+0.05 for a,b in cov)]
    acc=list(forced)+[0.0,DUR]; keep=[]
    for t,d in sorted(cand,key=lambda x:-x[1]):
        if all(abs(t-x)>=SOFT_FLOOR for x in acc): keep.append(t); acc.append(t)
    return sorted(keep)
def punch_plan():
    sp=splices(); hook_end=B.NAME[0]
    forced=sorted({t for beat in PANEL_BEATS for t in beat}|{hook_end})
    hard=set(_hard_bare(forced))
    bounds,last=[0.0],0.0
    for t in sorted(set(sp)|set(forced)):
        if t<=hook_end or t>=DUR-0.4: continue
        nxt=min([f for f in forced if f>t],default=DUR)
        if t in forced: bounds.append(round(t,3)); last=t
        elif t in hard and t-last>=SOFT_FLOOR and nxt-t>=SOFT_FLOOR: bounds.append(round(t,3)); last=t
        # a free splice is only used if the NEXT forced bound is far enough away that the
        # new hold is itself a real hold (no 2 s framing stubs before a panel edge)
        elif t-last>=MIN_HOLD and nxt-t>=5.0: bounds.append(round(t,3)); last=t
    bounds.append(round(DUR,3)); bounds=sorted(set(bounds))
    in_panel=lambda a,b: any(pa-0.01<=a and b<=pb+0.01 for pa,pb in PANEL_BEATS)
    plan,prev,alt,ai=[],None,["B","A","C","A"],0
    for i in range(len(bounds)-1):
        a,b=bounds[i],bounds[i+1]
        if b-a<0.25:
            if plan: plan[-1]=(plan[-1][0],b,plan[-1][2]); continue
        if a<hook_end: lvl="A"
        elif in_panel(a,b): lvl="P1" if prev!="P1" else "P2"
        else:
            lvl=alt[ai%len(alt)]; ai+=1
            if lvl==prev: ai+=1; lvl=alt[ai%len(alt)]
        plan.append((a,b,lvl)); prev=lvl
    return plan
PUNCH=punch_plan()

def punch():
    parts,cat=[],""
    for i,(a,b,lvl) in enumerate(PUNCH):
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,{CROP[lvl]}setsar=1[v{i}]")
        cat+=f"[v{i}]"
    fc=";".join(parts)+f";{cat}concat=n={len(PUNCH)}:v=1:a=0[vout]"
    subprocess.run([FF,"-nostdin","-y","-v","error","-i",SRC,"-filter_complex",fc,
      "-map","[vout]","-map","0:a","-c:v","libx264","-preset","medium","-crf","16",
      "-pix_fmt","yuv420p","-r",FPS,"-c:a","copy",f"{HERE}/punched.mov"],check=True)
    print("punched.mov done")

# ------------------------------------------------------------------ overlays
GFX=[("name",B.NAME),("pool",B.POOL),("before",B.BEFORE),("today",B.TODAY),("num1",B.NUM1),
     ("flyblind",B.FLYBLIND),("num2",B.NUM2),("tellai",B.TELLAI),("num3",B.NUM3),("mealbul",B.MEALBUL),
     ("trial",B.TRIAL),("trylist",B.TRYLIST),("cancel",B.CANCEL),("price",B.PRICE),("solved",B.SOLVED),("cta",B.CTA)]

# tall app screenshots, panned slowly inside the left phone panel (reads as scrolling)
SHOTS=[(B.ASSESS,   f"{APP}/app_trainer_assessment.png", 540,1020,"plate_shot"),
       (B.WORKOUT,  f"{APP}/app_trainer_workout.png",    540,1020,"plate_shot"),
       (B.MEALPLAN, f"{APP}/09_app_nutrition_plan.png",  540,1020,"plate_shot"),
       (B.SLEEP,    f"{APP}/11_app_daily_brief.png",     540,1020,"plate_shot")]

# The REAL macro-tracker recording, measured off the contact sheet (1 frame / 3 s):
#   0-3     phone camera        6-9   "Track your meals" + photo in place   9-15  typing the note
#   15-27   Analyze -> "Analyzing your meal"   27-33 clarifying questions   33-40 itemized result
#   40-46   "logged"
# The beat wants photo -> analyze -> itemized numbers; each slice carries its own rate.
MACRO_SRC=[(6.0,15.0),(15.0,27.0),(33.0,42.4)]   # photo+note -> analyzing -> itemized result
def _macro_slices():
    a,b=B.MACRO
    m1=B.at("our AI instantly", after=a-0.5)
    m2=B.at("tells you the calories", after=a-0.5)
    out=[]
    for (sa,sb),(ta,tb) in zip(MACRO_SRC,[(a,m1),(m1,m2),(m2,b)]):
        avail=sb-sa; need=tb-ta
        rate=round(min(max(avail/need,0.85),1.6),4) if need>0 else 1.0
        out.append((round(ta,3),round(tb,3),sa,rate))
    return out

def mix():
    inp,fc,idx=["-i",f"{HERE}/punched.mov"],[],1
    cur="[0:v]"
    def over(src,a,b,x=0,y=0,loop=False,pre="",ss=None,tlen=None,lead=0.0):
        nonlocal inp,fc,idx,cur
        # -framerate is NOT optional on a looped still (lesson 50): 25 fps vs 29.97 drops a
        # frame where the grids drift and exposes whatever the plate was covering.
        if loop: inp+=["-loop","1","-framerate",FPS,"-t",str(round(b-a+0.45,3))]
        if ss is not None: inp+=["-ss",str(ss),"-t",str(round(tlen if tlen else b-a+0.25,3))]
        inp+=["-i",src]
        pts="setpts=PTS-STARTPTS" if ss is not None or not loop else "setpts=PTS"
        fc.append(f"[{idx}:v]{pre}{pts}+{a-lead}/TB[g{idx}]")
        fc.append(f"{cur}[g{idx}]overlay={x}:{y}:enable='between(t,{a},{b})'[s{idx}]")
        cur=f"[s{idx}]"; idx+=1
    LEAD=0.09
    def panel(src,a,b,w,h,plate,tag,pre="",ss=None,tlen=None,loop=False):
        x=(PANEL_W-w)//2; y=(1080-h)//2
        over(f"{G}/{plate}.png",a,b,loop=True,lead=LEAD)
        over(src,a,b,x=x,y=y,ss=ss,tlen=tlen,loop=loop,pre=pre,lead=(LEAD if ss is not None else 0.0))
        over(f"{G}/{plate}.png",a,b,loop=True,lead=LEAD)
        if tag: over(f"{G}/tag.png",a+0.10,b,x=x+26,y=y+26,loop=True)

    for name,beat in GFX:
        p=f"{G}/{name}.mov"
        if not os.path.exists(p): print(f"  ! missing {name}.mov -- skipped"); continue
        over(p,beat[0],beat[1])

    for (beat,png,w,h,plate) in SHOTS:
        a,b=beat; d=round(b-a,3)
        # a still is never left static (lesson 1): pan the tall screenshot top->bottom,
        # a pure translation -- no zoompan jitter. Stop at 45% of the drop so the text
        # that matters (the assessment / targets) stays readable rather than racing by.
        panel(png,a,b,w,h,plate,False,loop=True,
              pre=f"scale={w}:-1:flags=lanczos,crop={w}:{h}:0:'(ih-oh)*0.45*clip(t/{d},0,1)',setsar=1,")

    for (ta,tb,si,rate) in _macro_slices():
        panel(MACROFLOW,ta,tb,520,1020,"plate_app",False,ss=si,
              tlen=round((tb-ta)*rate+0.25,3),
              pre=f"setpts=PTS/{rate},{AFCROP}scale=520:1020:flags=lanczos,setsar=1,")

    fc[-1]=fc[-1].rsplit("[s",1)[0]+"[vout]"
    subprocess.run([FF,"-nostdin","-y","-v","error"]+inp+
      ["-filter_complex",";".join(fc),"-map","[vout]","-map","0:a","-c:v","libx264",
       "-preset","medium","-crf","17","-pix_fmt","yuv420p","-r",FPS,"-c:a","copy",
       f"{HERE}/nocap.mov"],check=True)
    print("nocap.mov done")

if __name__=="__main__":
    if not sys.argv[1:] or "plan" in sys.argv:
        print(f"{len(PUNCH)} punch segments over {DUR:.2f}s")
        from collections import Counter
        print(Counter(l for _,_,l in PUNCH))
        for a,b,l in PUNCH: print(f"  {a:7.2f} -> {b:7.2f}  {b-a:6.2f}  {l}")
        print("\nmacro slices:", _macro_slices())
    if "punch" in sys.argv: punch()
    if "mix"   in sys.argv: mix()
