#!/usr/bin/env python3
"""Website video REV 2 -- punch/layout over the 4K tight.mov (3840x2160 -> 1920x1080), then overlays.
  python3 layout.py plan | pip | punch | mix

FRAMING (Dan, rev-1 review, 2026-09-02): "The opening shot is much too wide. I don't want to use
this wide shot ever ... crop between having my head and my belly button in the frame, and the top
of my head and my shorts visible, with the counter barely visible ... Many of these shots also
have a light in the shot. That's totally unacceptable."

Read off the 4K frame with a burned grid (pv/grid4k_lab.png), Dan centred at x~1980: head top
y~100, chin ~330, navel ~1290, shorts waistband ~1580, counter top ~1720, THE LIGHT ENTERS AT
x~3560. Three levels, all top-anchored at y=40 and centred on x=1980 so the eyeline never moves:

  WIDE   3058x1720 @ (451,40)  1.256x  top of head -> shorts, counter barely visible (the widest allowed)
  MID    2650x1490 @ (655,40)  1.45x   head -> hips
  TIGHT  2312x1300 @ (824,40)  1.66x   head -> belly button (Dan's stated tight frame)
  PIP    3058x1720 @ (0,40)    1.256x  the WIDE level with Dan pushed to x=65 % so the phone sits beside him

The base is the full 4K so even TIGHT is a downscale. No level may reach x>3500 or exceed WIDE:
asserted below, so the wide-shot defect cannot recur without failing the build (skill lesson 82).
PUNCH RULE unchanged (ad-edit lesson 21): boundaries land ON splices; holds >= 9 s; hardest
splices covered first inside a 3.5 s floor.
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

SW,SH=3840,2160
LIGHT_X=3530            # the studio light: leftmost bright pixel measured at x~3565 on two frames; WIDE ends at 3509
LEVELS={"WIDE":(451,40,3058,1720),"MID":(655,40,2650,1490),"TIGHT":(824,40,2312,1300),
        "PIP":(0,40,3058,1720)}
for _n,(_x,_y,_w,_h) in LEVELS.items():
    assert _w<=3058 and _h<=1720, f"{_n}: wider than the widest allowed level"
    assert _x>=0 and _y>=0 and _x+_w<=LIGHT_X and _y+_h<=SH, f"{_n}: crop reaches the light or leaves the frame"
    assert abs(_w/_h-16/9)<0.002, f"{_n}: not 16:9"
    assert _w%2==0 and _h%2==0
def _crop(n):
    x,y,w,h=LEVELS[n]; return f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,"
CROP={n:_crop(n) for n in LEVELS}
SHOTS=[]                # rev 1's tall app screenshots are gone (Dan: "if it looks lame, don't show it")
PANEL_BEATS=[B.BEATS[n] for n in sorted(B.PANEL)]
MIN_HOLD=9.0

def splices():
    tc=json.load(open(f"{HERE}/tight_cuts.json")); out,acc=[],0.0
    for a,b in tc["keeps"][:-1]:
        acc+=b-a; out.append(round(acc,3))
    return out

SOFT_FLOOR=3.5
def _hard_bare(forced=()):
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
        elif t-last>=MIN_HOLD and nxt-t>=5.0: bounds.append(round(t,3)); last=t
    bounds.append(round(DUR,3)); bounds=sorted(set(bounds))
    in_panel=lambda a,b: any(pa-0.01<=a and b<=pb+0.01 for pa,pb in PANEL_BEATS)
    # tighter than rev 1 on purpose: TIGHT half the time, MID and WIDE a quarter each; the hook
    # opens on MID (head -> hips, Muhammad's opening frame)
    plan,prev,alt,ai=[],None,["MID","TIGHT","WIDE","TIGHT"],0
    def nxt_level(prev):
        nonlocal ai
        lvl=alt[ai%len(alt)]; ai+=1
        if lvl==prev: lvl=alt[ai%len(alt)]; ai+=1      # never the same framing across a join
        return lvl
    for i in range(len(bounds)-1):
        a,b=bounds[i],bounds[i+1]
        if b-a<0.25:
            if plan: plan[-1]=(plan[-1][0],b,plan[-1][2]); continue
        if a<hook_end: lvl="MID"
        elif in_panel(a,b): lvl="PIP"
        else: lvl=nxt_level(prev)
        plan.append((a,b,lvl)); prev=lvl
    for a,b,lvl in plan: assert lvl in LEVELS, lvl
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

# ------------------------------------------------------------------ the phone PiP
# The REAL macro-tracker recording, measured off its contact sheet (1 frame / 3 s):
#   6-9 "Track your meals" + photo in place  9-15 typing the note  15-27 Analyze -> "Analyzing"
#   33-40 itemized result. Photo -> analyzing -> itemized numbers, each slice at its own rate.
MACRO_SRC=[(6.0,15.0),(15.0,27.0),(33.0,42.4)]
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
PIP_BOX=[150,130,583,950]      # must match gfx2.PIP_BOX (433x820)
def pip():
    """pre-render gfx/pip_macro.mov: the recording through the rounded mask, the hairline/shadow
    plate on top, alpha fades at both ends -- one alpha MOV for the whole MACRO beat, overlaid
    by mix() like any other graphic"""
    a,b=B.MACRO; D=round(b-a,3); sl=_macro_slices()
    inp,parts,cat=[],[],""
    for k,(ta,tb,si,rate) in enumerate(sl):
        need=round(tb-ta,3)
        inp+=["-ss",str(si),"-t",str(round(need*rate+0.4,3)),"-i",MACROFLOW]
        parts.append(f"[{k}:v]setpts=PTS/{rate},{AFCROP}scale={PIP_BOX[2]-PIP_BOX[0]}:{PIP_BOX[3]-PIP_BOX[1]}:flags=lanczos,"
                     f"fps={FPS},trim=duration={need},setpts=PTS-STARTPTS,setsar=1[r{k}]")
        cat+=f"[r{k}]"
    n=len(sl)
    inp+=["-loop","1","-framerate",FPS,"-t",str(D),"-i",f"{G}/pip_mask.png",
          "-loop","1","-framerate",FPS,"-t",str(D),"-i",f"{G}/pip_plate.png"]
    fc=(";".join(parts)+f";{cat}concat=n={n}:v=1:a=0,format=rgba[rec];"
        f"[{n}:v]format=gray[m];[rec][m]alphamerge=shortest=1[recm];"
        f"color=c=black@0.0:s=1920x1080:r={FPS}:d={D},format=rgba[bg];"
        f"[bg][recm]overlay={PIP_BOX[0]}:{PIP_BOX[1]}:format=rgb:shortest=1[o1];"
        f"[o1][{n+1}:v]overlay=0:0:format=rgb:shortest=1,"
        f"fade=t=in:st=0:d=0.45:alpha=1,fade=t=out:st={D-0.40:.3f}:d=0.40:alpha=1,format=argb[out]")
    subprocess.run([FF,"-nostdin","-y","-v","error"]+inp+["-filter_complex",fc,"-map","[out]",
        "-t",str(D),"-c:v","qtrle","-pix_fmt","argb",f"{G}/pip_macro.mov"],check=True)
    print("gfx/pip_macro.mov done")

# ------------------------------------------------------------------ overlays
GFX=[("name",B.NAME),("before",B.BEFORE),("today",B.TODAY),("num1",B.NUM1),("pip_macro",B.MACRO),
     ("flyblind",B.FLYBLIND),("num2",B.NUM2),("num3",B.NUM3),("trial",B.TRIAL),("cancel",B.CANCEL),
     ("price",B.PRICE),("solved",B.SOLVED),("cta",B.CTA)]

def mix():
    inp,fc,idx=["-i",f"{HERE}/punched.mov"],[],1
    cur="[0:v]"
    def over(src,a,b):
        nonlocal inp,fc,idx,cur
        inp+=["-i",src]
        fc.append(f"[{idx}:v]setpts=PTS+{a}/TB[g{idx}]")
        fc.append(f"{cur}[g{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]")
        cur=f"[s{idx}]"; idx+=1
    for name,beat in GFX:
        p=f"{G}/{name}.mov"
        assert os.path.exists(p), f"missing {name}.mov"
        over(p,beat[0],beat[1])
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
    if "pip"   in sys.argv: pip()
    if "punch" in sys.argv: punch()
    if "mix"   in sys.argv: mix()
