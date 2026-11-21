#!/usr/bin/env python3
"""Website video REV 4 -- punch/layout over the 4K tight.mov (3840x2160 -> 1920x1080), then overlays.
  python3 layout.py plan | punch | mix

FRAMING (Dan, rev 3 review 2026-09-08): "My hair is cut off in the opening scene here and throughout the video ...
Never cut off my hair or below my shorts line ... use a little bit closer crops. Avoid that super wide crop."

Rev 3 anchored every crop to the HAIRLINE (skin at r>120, minus a 40-px guess) and cut the hair in 23 of 26 holds
(ad-edit lesson 107). REV 4 ANCHORS EVERY CROP TO THE MEASURED TOP OF HIS HAIR: hairtrack.py runs hairdet.detect on
the 4K base at 8/s (validated by eye on pv/hairtrack_proof.jpg at native scale), hairtrack_refine.py adds samples
measured on the delivered-scale picture, and per punch segment
    y0 = (that segment's minimum hair top over BOTH tracks) - 4 % of the crop height
so the hair sits ~43 px below the top edge at his tallest instant in every level. Two levels, both from Dan's own
rev-1 definition of the frames he likes; the WIDE level is deleted (max crop width asserted):

  NEAR  2076x1168  1.85x  hair -> belly button ("between my head and my belly button")
  FAR   2630x1480  1.46x  hair -> shorts line + a sliver of counter ("shorts visible, counter barely")
  PIP   2630x1480  1.46x  FAR geometry at x0=270: Dan at 65 % so the phone PiP sits beside him

Asserted at import: exactly NEAR/FAR/PIP, none wider than 2630, none reaching the light (x>3530), y0 in 0..500, the
crop inside the frame. hairgate.py re-measures the hair on the DELIVERED frames (never < 20 px, per segment 30-70)
and, independently, that the top 12 rows of the head band are never hair-coloured on ANY frame.
PUNCH RULE (lesson 21): boundaries land ON splices; holds >= 9 s; hardest splices covered first inside a 3.5 s floor;
NEAR/FAR alternate strictly across every visible join; the hook opens on FAR; the AI inserts and the two phone PiPs are
forced boundaries, and a segment hidden under an AI insert does not advance the alternation, so the framing changes
across every insert.
"""
import hashlib, json, os, subprocess, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import beats as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
HERE=os.path.dirname(os.path.abspath(__file__))
G=f"{HERE}/gfx"; FPS="30000/1001"; SRC=f"{HERE}/tight.mov"; DUR=B.DUR
L="/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
APP=f"{L}/02 App Screen Recordings and Screenshots"
AFCROP="crop=1320:2500:0:175,"                              # qc.py's banned-screen templates use this chain

SW,SH=3840,2160
LIGHT_X=3530            # the studio light: leftmost bright pixel measured at x~3565 on two frames
DAN_CX=1980             # Dan's centre in the 4K frame
HEADROOM_FRAC=0.04      # the hair top sits 4 % of the crop height below the top edge = ~43 px at 1080p, every level
Y_MAX=500               # sanity: his hair is never lower than ~400 in the 4K frame
WIDEST_W=2630           # REV 4: the FAR level is the widest crop that may ever appear (rev 3's WIDE was 3058)
# x, w, h -- y is per punch segment (crop_for)
LEVELS={"NEAR":(942,2076,1168),"FAR":(665,2630,1480),"PIP":(270,2630,1480)}
assert set(LEVELS)=={"NEAR","FAR","PIP"}, "exactly NEAR, FAR and PIP -- there is no WIDE level"
for _n,(_x,_w,_h) in LEVELS.items():
    assert _w<=WIDEST_W and _h<=1480, f"{_n}: wider than the widest allowed level"
    assert _x>=0 and _x+_w<=LIGHT_X, f"{_n}: crop reaches the light or leaves the frame"
    assert abs(_w/_h-16/9)<0.002, f"{_n}: not 16:9"
    assert _w%2==0 and _h%2==0

# ---- the HAIR track, keyed to THIS tight cut (hairtrack.py samples base.mov and maps through the keeps)
_HT=json.load(open(f"{HERE}/hairtrack.json"))
_sig=hashlib.md5(json.dumps(json.load(open(f"{HERE}/tight_cuts.json"))["keeps"]).encode()).hexdigest()[:12]
assert _HT.get("keeps_sig")==_sig, "hairtrack.json is stale for this tight cut -- run hairtrack.py"
assert _HT.get("detector")=="hairdet.py", "hairtrack.json was not written by the hair detector"
HAIR=[(t,h) for t,h,*_ in _HT["samples"] if t is not None and h is not None]
HDR_COL=_HT["hdr_col"]
if _HT.get("refine",{}).get("keeps_sig")==_sig:
    HAIR+=[(t,h) for t,h,*_ in _HT["refine"]["samples"] if t is not None and h is not None]
    REFINED=True
else: REFINED=False
def hair_top_min(a,b):
    """the tallest he stands inside [a,b): invalid samples are discarded (never used), so the minimum is safe"""
    seg=[h for t,h in HAIR if a<=t<b] or [h for t,h in HAIR if a-1.0<=t<b+1.0]
    assert seg, f"no valid hair samples in {a:.2f}-{b:.2f}"
    return min(seg)
def crop_for(lvl,a,b):
    x,w,h=LEVELS[lvl]; hm=hair_top_min(a,b)
    y=hm-int(round(HEADROOM_FRAC*h)); y=max(0,min(y,SH-h)); y-=y%2
    assert 0<=y<=Y_MAX and y+h<=SH and x+w<=LIGHT_X and w<=WIDEST_W, (lvl,a,b,y)
    return (x,y,w,h)
def crop_filter(c):
    x,y,w,h=c; return f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos,"
PANEL_BEATS=[B.BEATS[n] for n in sorted(B.PANEL)]
AI_BEATS=[B.BEATS[n] for n in sorted(B.AI)]
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
def _inside(a,b,beats): return any(pa-0.01<=a and b<=pb+0.01 for pa,pb in beats)
def punch_plan():
    sp=splices(); hook_end=B.NAME[0]
    forced=sorted({t for beat in PANEL_BEATS+AI_BEATS for t in beat}|{hook_end})
    hard=set(_hard_bare(forced))
    bounds,last=[0.0],0.0
    for t in sorted(set(sp)|set(forced)):
        if t<=hook_end or t>=DUR-0.4: continue
        nxt=min([f for f in forced if f>t],default=DUR)
        if t in forced: bounds.append(round(t,3)); last=t
        elif t in hard and t-last>=SOFT_FLOOR and nxt-t>=SOFT_FLOOR: bounds.append(round(t,3)); last=t
        elif t-last>=MIN_HOLD and nxt-t>=5.0: bounds.append(round(t,3)); last=t
    bounds.append(round(DUR,3)); bounds=sorted(set(bounds))
    plan,prev_vis,alt,ai=[],None,["FAR","NEAR"],0
    def nxt_level(prev):
        nonlocal ai
        lvl=alt[ai%2]; ai+=1
        if lvl==prev: lvl=alt[ai%2]; ai+=1      # never the same framing across a visible join
        return lvl
    for i in range(len(bounds)-1):
        a,b=bounds[i],bounds[i+1]
        if b-a<0.25:
            if plan: plan[-1]=(plan[-1][0],b,plan[-1][2]); continue
        if a<hook_end: lvl="FAR"; prev_vis=lvl
        elif _inside(a,b,PANEL_BEATS): lvl="PIP"; prev_vis=lvl
        elif _inside(a,b,AI_BEATS): lvl=prev_vis or "FAR"          # hidden under a full-frame insert: no advance
        else: lvl=nxt_level(prev_vis); prev_vis=lvl
        plan.append((a,b,lvl))
    for a,b,lvl in plan: assert lvl in LEVELS, lvl
    return plan
PUNCH=punch_plan()
CROPS=[crop_for(l,a,b) for a,b,l in PUNCH]          # (x,y,w,h) per punch segment, hair-anchored
COVERED=[_inside(a,b,AI_BEATS) or _inside(a,b,[B.BEATS[n] for n in B.BEATS if n not in B.OVERLAY and n not in B.PANEL]) for a,b,_ in PUNCH]
assert max(c[2] for c in CROPS)<=WIDEST_W, "a crop wider than the FAR level exists"

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

# ------------------------------------------------------------------ overlays
PIP_BOX=[150,130,583,950]      # must match gfx2.PIP_BOX (433x820); both PiPs (macro + hub) use it
GFX=[("name",B.NAME),("before",B.BEFORE),("today",B.TODAY),("num1",B.NUM1),("pip_macro",B.MACRO),
     ("flyblind",B.FLYBLIND),("pip_num2",B.NUM2),("num3",B.NUM3),("pip_hub",B.HUB),("trial",B.TRIAL),("cancel",B.CANCEL),
     ("price",B.PRICE),("cta",B.CTA)]   # REV 5: the goal-image card ("solved") is removed. REV 6: num2 lower third -> pip_num2 (the Trainer PiP)
# the AI inserts: pre-rendered by build_inserts.py (clip trimmed to the beat, scaled, AI-GENERATED tag burned upper-left
# at 1.5x), overlaid full-frame with ALPHA fades of 0.5 s at the outer edges of each run -- a straight cut between two
# consecutive clips (A->B, C1->C2, D1->D2->D3), never a dip to Dan in between
AI_FADE=0.5
def ai_inserts():
    out=[]
    beats=sorted((B.BEATS[n],n) for n in B.AI)
    for (a,b),n in beats:
        fi=not any(abs(pb-a)<0.02 for (pa,pb),_ in beats if pb!=b)
        fo=not any(abs(pa-b)<0.02 for (pa,pb),_ in beats if pa!=a)
        out.append((n.lower(),(a,b),fi,fo))
    return out
AIV=ai_inserts()
def pip_marks():
    """state-change times of the two PiPs on the tight timeline (for the watch pass)"""
    out=[]
    for n in ("pip_macro","pip_num2","pip_hub"):
        p=f"{G}/{n}.json"
        if os.path.exists(p): out+=json.load(open(p)).get("marks",[])
    return out

def _mix_pass(items, src, out, final, audio_from=None):
    """one overlay pass. Intermediates are RAWVIDEO in .nut -- lossless, so staging costs no picture quality."""
    inp,fc,idx=["-i",src],[],1
    cur="[0:v]"
    for kind,name,(a,b),fi,fo in items:
        p=f"{G}/{name}.mov"; assert os.path.exists(p), f"missing {name}.mov"
        inp+=["-i",p]
        if kind=="gfx":
            fc.append(f"[{idx}:v]setpts=PTS+{a}/TB[g{idx}]")
        else:
            D=b-a; f=[f"format=yuva420p"]
            if fi: f.append(f"fade=t=in:st=0:d={AI_FADE}:alpha=1")
            if fo: f.append(f"fade=t=out:st={D-AI_FADE:.3f}:d={AI_FADE}:alpha=1")
            fc.append(f"[{idx}:v]{','.join(f)},setpts=PTS+{a}/TB[g{idx}]")
        fc.append(f"{cur}[g{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]")
        cur=f"[s{idx}]"; idx+=1
    fc[-1]=fc[-1].rsplit("[s",1)[0]+"[vout]"
    nin=len(inp)//2                       # count the inputs BEFORE -threads doubles the tokens
    dt=os.environ.get("MIX_DEC_THREADS")
    if dt: inp=[x for pair in ([["-threads",dt,"-i",p] for p in inp[1::2]]) for x in pair]
    tail=["-t",os.environ["MIX_T"]] if os.environ.get("MIX_T") else []
    if final:
        amap=["-map",f"{nin}:a"] if audio_from else ["-map","0:a"]
        if audio_from: inp+=["-i",audio_from]
        enc=["-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","-r",FPS]+amap+["-c:a","copy"]
    else:
        enc=["-c:v","rawvideo","-pix_fmt","yuv420p","-r",FPS,"-an"]
    subprocess.run([FF,"-nostdin","-y","-v","error"]+inp+
      ["-filter_complex",";".join(fc),"-map","[vout]"]+enc+tail+[out],check=True)
    print(os.path.basename(out),"done")

def mix():
    """REV 5: MIX_STAGES splits the overlay chain into N sequential ffmpeg passes.

    21 inputs in ONE graph livelocks ffmpeg's threaded scheduler on a loaded machine: 336 threads, every one of them
    parked in tq_receive (`sample <pid>` shows 0 busy), the process burning 23 % CPU on park/wake, and 0.4 s of picture
    per 75 s -- against an encode floor of 0.63x real time and a total decode cost of 2 s for every overlay MOV. Three
    passes of ~7 inputs each stay under it. The intermediates are RAWVIDEO, so staging is lossless."""
    items=[("gfx",n,beat,None,None) for n,beat in GFX]+[("ai",n,beat,fi,fo) for n,beat,fi,fo in AIV]
    items.sort(key=lambda it: it[2][0])
    out=os.environ.get("MIX_OUT",f"{HERE}/nocap.mov")
    N=int(os.environ.get("MIX_STAGES","1"))
    if N<=1:
        return _mix_pass(items,f"{HERE}/punched.mov",out,True)
    k=-(-len(items)//N); groups=[items[i:i+k] for i in range(0,len(items),k)]
    src=f"{HERE}/punched.mov"; tmps=[]
    for i,grp in enumerate(groups):
        last=(i==len(groups)-1)
        dst=out if last else f"{HERE}/_mixstage{i}.nut"
        print(f"  stage {i+1}/{len(groups)}: {len(grp)} overlays -> {os.path.basename(dst)}", flush=True)
        _mix_pass(grp,src,dst,last,audio_from=(f"{HERE}/punched.mov" if last else None))
        if not last: tmps.append(dst)
        src=dst
    for p in tmps: os.remove(p)

if __name__=="__main__":
    if not sys.argv[1:] or "plan" in sys.argv:
        print(f"{len(PUNCH)} punch segments over {DUR:.2f}s   hair track refined from delivered frames: {REFINED}   hair samples {len(HAIR)}")
        from collections import Counter
        print(Counter(l for (_,_,l),cv in zip(PUNCH,COVERED) if not cv), " (visible segments)")
        print("   start     end     len   level   crop y0  hair_top(min/med)  hair below edge@1080p  bottom(4K)")
        for (a,b,l),(x,y,w,h),cv in zip(PUNCH,CROPS,COVERED):
            seg=[ht for t,ht in HAIR if a<=t<b]; hm=min(seg) if seg else hair_top_min(a,b)
            med=sorted(seg)[len(seg)//2] if seg else hm
            print(f"  {a:7.2f} -> {b:7.2f}  {b-a:6.2f}  {l:5s}   {y:4d}      {hm:4d}/{med:4d}          {(hm-y)*1080/h:5.1f} px          {y+h}   {'(covered)' if cv else ''}")
        print("\nAI inserts (name, beat, fade in, fade out):"); [print("  ",x) for x in AIV]
    if "punch" in sys.argv: punch()
    if "mix"   in sys.argv: mix()
