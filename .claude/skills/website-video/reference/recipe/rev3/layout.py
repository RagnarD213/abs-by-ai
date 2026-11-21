#!/usr/bin/env python3
"""Website video REV 3 -- punch/layout over the 4K tight.mov (3840x2160 -> 1920x1080), then overlays.
  python3 layout.py plan | pip | punch | mix

FRAMING. Rev 1 (Dan): never the wide kitchen shot, never the light. Rev 2 (Dan): "too much space
above my head in all the shots ... crop in closer and also lower throughout ... just a little bit of
space above my head, and then more on the bottom, with the shorts and the counter visible."

Rev 2's three levels were top-anchored at a FIXED y=40, read off one grid frame where his head top
sat at y~100. headtrack.py measured the real head top across the cut at 296-340 px (4K), so every
shot carried 168-232 px of headroom at 1080p, worst on TIGHT. REV 3 ANCHORS EVERY CROP TO THE
MEASURED HEAD (ad-edit lesson 97): per punch segment, y0 = (that segment's minimum head top) -
3 % of the crop height, so the head top lands ~32 px below the top edge in every level and the
bottom edge goes as low as the zoom allows. Widths/zooms are unchanged and x stays centred on 1980:

  WIDE   3058x1720  1.256x  head -> shorts + plenty of counter (the widest allowed level)
  MID    2650x1490  1.45x   head -> shorts line / counter edge
  TIGHT  2312x1300  1.66x   head -> just above the shorts
  PIP    3058x1720  1.256x  WIDE at x=0: Dan at 65 % so the phone sits beside him

Asserted at import: no level wider than WIDE, none reaching the light (x>3530), y0 in 0..500, the
crop inside the frame. qc_frame.py re-measures the headroom on the DELIVERED frames (15-60 px).
PUNCH RULE unchanged (lesson 21): boundaries land ON splices; holds >= 9 s; hardest splices covered
first inside a 3.5 s floor.
"""
import hashlib, json, os, subprocess, sys
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
DAN_CX=1980             # Dan's centre in the 4K frame (headtrack.py)
HEADROOM_FRAC=0.03      # head top sits 3 % of the crop height below the top edge = ~32 px at 1080p, every level
Y_MAX=500               # sanity: his head is never lower than ~460 in the 4K frame
# x, w, h -- y is per punch segment (crop_for)
LEVELS={"WIDE":(451,3058,1720),"MID":(655,2650,1490),"TIGHT":(824,2312,1300),"PIP":(0,3058,1720)}
for _n,(_x,_w,_h) in LEVELS.items():
    assert _w<=3058 and _h<=1720, f"{_n}: wider than the widest allowed level"
    assert _x>=0 and _x+_w<=LIGHT_X, f"{_n}: crop reaches the light or leaves the frame"
    assert abs(_w/_h-16/9)<0.002, f"{_n}: not 16:9"
    assert _w%2==0 and _h%2==0

# ---- the head track, keyed to THIS tight cut (headtrack.py samples base.mov and maps through the keeps)
_HT=json.load(open(f"{HERE}/headtrack.json"))
_sig=hashlib.md5(json.dumps(json.load(open(f"{HERE}/tight_cuts.json"))["keeps"]).encode()).hexdigest()[:12]
assert _HT.get("keeps_sig")==_sig, "headtrack.json is stale for this tight cut -- run headtrack.py"
HEAD=[(t,ht) for t,ht,_ in _HT["samples"] if t is not None and ht is not None]
# headtrack_refine.py adds delivered-scale samples (the QC detector on punched.mov, mapped back to 4K);
# the per-segment minimum runs over BOTH tracks so the crop anchors to the tallest instant either saw
if _HT.get("refine",{}).get("keeps_sig")==_sig:
    HEAD+=[(t,ht) for t,ht,_ in _HT["refine"]["samples"] if t is not None and ht is not None]
    REFINED=True
else: REFINED=False
def head_top_min(a,b):
    """the tallest he stands inside [a,b): detector misses only ever read LOW, so the minimum is safe"""
    seg=[ht for t,ht in HEAD if a<=t<b] or [ht for t,ht in HEAD if a-1.0<=t<b+1.0]
    assert seg, f"no head samples in {a:.2f}-{b:.2f}"
    return min(seg)
def crop_for(lvl,a,b):
    x,w,h=LEVELS[lvl]; hm=head_top_min(a,b)
    y=hm-int(round(HEADROOM_FRAC*h)); y=max(0,min(y,SH-h)); y-=y%2
    assert 0<=y<=Y_MAX and y+h<=SH and x+w<=LIGHT_X, (lvl,a,b,y)
    return (x,y,w,h)
def crop_filter(c):
    x,y,w,h=c; return f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,"
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
    # TIGHT half the time, MID and WIDE a quarter each; the hook opens on MID
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
CROPS=[crop_for(l,a,b) for a,b,l in PUNCH]          # (x,y,w,h) per punch segment, head-anchored

def punch():
    parts,cat=[],""
    for i,((a,b,lvl),c) in enumerate(zip(PUNCH,CROPS)):
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,{crop_filter(c)}setsar=1[v{i}]")
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
        print(f"{len(PUNCH)} punch segments over {DUR:.2f}s   head track refined from delivered frames: {REFINED}")
        from collections import Counter
        print(Counter(l for _,_,l in PUNCH))
        print("   start     end     len   level   crop y0  head_top(min/med)  headroom@1080p(min)  bottom(4K)")
        for (a,b,l),(x,y,w,h) in zip(PUNCH,CROPS):
            seg=[ht for t,ht in HEAD if a<=t<b]; hm=min(seg) if seg else head_top_min(a,b)
            med=sorted(seg)[len(seg)//2] if seg else hm
            print(f"  {a:7.2f} -> {b:7.2f}  {b-a:6.2f}  {l:5s}   {y:4d}      {hm:4d}/{med:4d}         {(hm-y)*1080/h:5.1f} px          {y+h}")
        print("\nmacro slices:", _macro_slices())
    if "pip"   in sys.argv: pip()
    if "punch" in sys.argv: punch()
    if "mix"   in sys.argv: mix()
