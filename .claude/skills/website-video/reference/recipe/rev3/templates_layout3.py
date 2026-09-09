#!/usr/bin/env python3
"""Ad 3 -- pass 1 punch/layout over tight.mov, pass 2 the overlays.
  python3 layout3.py plan | punch | mix

PUNCH RULE (lesson 21): every pause cut needs cover and a punch change is the cheapest
cover, so punch boundaries land ON the splices the tight pass left -- never at arbitrary
times, where the layout change would be its own visible event. The hook is protected:
no splice and no punch change inside the opening line.
"""
import json, os, subprocess, sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import beats3 as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
HERE=os.path.dirname(os.path.abspath(__file__))
G=f"{HERE}/gfx"; FPS="30000/1001"; SRC=f"{HERE}/tight.mov"; DUR=B.DUR
L="/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library"
AI=f"{L}/04 AI-Generated Clips"; APP=f"{L}/02 App Screen Recordings and Screenshots"
ARCH=f"{L}/08 SixPackAbs Archive - CHECK BEFORE USING"
DEMO="/Users/danielrose/Documents/Claude/Projects/Abs By AI/public/exercise-demos"
APPFLOW=f"{APP}/app-flow-generate-future-self.mp4"
AFCROP="crop=1320:2500:0:175,"

PANEL_W=980; VID_W=1920-PANEL_W
CROP={"A":"",
      "B":"crop=1574:886:198:54,scale=1920:1080:flags=lanczos,",
      "C":"crop=1730:973:104:40,scale=1920:1080:flags=lanczos,",
      "P1":f"crop={VID_W}:1080:450:0,pad=1920:1080:{PANEL_W}:0:black,",
      "P2":f"crop=800:919:530:80,scale={VID_W}:1080:flags=lanczos,pad=1920:1080:{PANEL_W}:0:black,"}
PANEL_BEATS=[B.COSTCARD,B.TAILOR,B.PLANBUL,B.ADAPTS,B.ADAPTMID]
MIN_HOLD=7.0

def splices():
    tc=json.load(open(f"{HERE}/tight_cuts.json")); out,acc=[],0.0
    for a,b in tc["keeps"][:-1]:
        acc+=b-a; out.append(round(acc,3))
    return out

def punch_plan():
    sp=splices(); hook_end=B.LOWER3A[0]
    forced=sorted({t for beat in PANEL_BEATS for t in beat}|{hook_end})
    bounds,last=[0.0],0.0
    for t in sorted(set(sp)|set(forced)):
        if t<=hook_end or t>=DUR-0.4: continue
        if t in forced or t-last>=MIN_HOLD: bounds.append(round(t,3)); last=t
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
GFX=[("lower3a",B.LOWER3A),("whycard",B.WHYCARD),("num1",B.NUM1),("costcard",B.COSTCARD),
     ("num3",B.NUM3),("brocard",B.BROCARD),("num4",B.NUM4),("adaptmid",B.ADAPTMID),
     ("toolate",B.TOOLATE),("before",B.BEFORE),("goalimg",B.GOALIMG),("today",B.TODAY),
     ("cta1",B.CTA1),("howcard",B.HOWCARD),("tailor",B.TAILOR),("planbul",B.PLANBUL),
     ("gymq",B.GYMQ),("adapts",B.ADAPTS),("notprice",B.NOTPRICE),("cta2",B.CTA2)]

# video panel inserts: (beat, src, src_in, hole_w, hole_h, plate, tag, src_len_or_None)
ROBOT8=f"{AI}/ai-trainer-vs-robot-cutdown-8s.mp4"
ROBOT35=f"{AI}/ai-trainer-vs-robot-story-35s.mp4"
SPA=f"{ARCH}/dan-sixpackabs-8s-dan-solo.mp4"
def _rate(beat, src_len): return round(src_len/(beat[1]-beat[0]),4)
VID=[(B.ROBOTCUT,  ROBOT8, 0.0, 574,1020,"plate_vert","small", 8.16),
     (B.SPACLIP,   SPA,    0.0,1264,1000,"plate_wide",None,     8.00),
     (B.ROBOTSTORY,ROBOT35,0.0, 574,1020,"plate_vert","small",35.29)]

# tall app screenshots, panned vertically inside the phone panel (reads as scrolling)
SHOTS=[(B.ASSESS, f"{APP}/app_trainer_assessment.png", 540,1020,"plate_shot", 690),
       (B.WORKOUT,f"{APP}/app_trainer_workout.png",    540,1020,"plate_shot", 690)]

# the exercise demo videos the script literally promises
DEMOCLIPS=["lat-pulldown","db-curl"]

# Measured off the recording, frame by frame:
#   0.0-3.0   the photo CROP screen            -- banned (lesson 15)
#   3.0-9.0   generation screen, photo in place
#   9.0-25.3  generating / progress ("Done! 100%" at 25.0)
#   25.4-27.6 "Meet the new you." BEFORE|AFTER -- BANNED, Dan's #1 compliance rule
#   27.9-33.9 the after ALONE + an email-capture form (must be covered, lesson 10)
APPFLOW_LEN=33.96
APPGEN_SRC=[(3.20,9.00),(13.00,25.20),(27.90,APPFLOW_LEN)]

def _appgen_slices():
    """upload -> generate -> see yourself, synced to the phrases. Each slice carries its
    own rate: the after-alone window is only 6.06 s of source and the beat wants ~7 s,
    so it retimes rather than running off the end of the file into nothing."""
    a,b=B.APPGEN
    m1=B.at("Then you have AI generate", after=a-0.5)
    m2=B.at("And once you see how great", after=a-0.5)
    out=[]
    for (sa,sb),(ta,tb) in zip(APPGEN_SRC,[(a,m1),(m1,m2),(m2,b)]):
        avail=sb-sa; need=tb-ta
        rate=round(min(avail/need,1.35),4) if need>0 else 1.0
        out.append((round(ta,3),round(tb,3),sa,rate))
    return out

def mix():
    inp,fc,idx=["-i",f"{HERE}/punched.mov"],[],1
    cur="[0:v]"
    def over(src,a,b,x=0,y=0,loop=False,pre="",ss=None,tlen=None,lead=0.0):
        """`lead` starts the STREAM early while the enable window still opens at `a`.

        Without it a video layer's first frame lands one frame after the beat starts, so
        for exactly one frame the plate's transparent hole shows the punched talking-head
        footage behind it -- a visible flash at every panel entrance. The watch pass's
        consecutive-frame strips are what exposed this; no metric sees a single frame."""
        nonlocal inp,fc,idx,cur
        # -framerate is NOT optional. A looped image input defaults to 25 fps while the
        # timeline runs at 29.97, and at the output frames where the two grids drift
        # apart the overlay drops the still for ONE frame -- the plate vanishes and
        # whatever it was covering is exposed. That is how the app's email-capture form
        # reached the picture at 179.40 s with the disclosure correctly built and
        # correctly enabled. Proven by A/B: 25 fps exposes one frame, 30000/1001 exposes
        # none. Invisible to any sampled scan; only consecutive frames show it.
        if loop: inp+=["-loop","1","-framerate",FPS,"-t",str(round(b-a+0.45,3))]
        if ss is not None: inp+=["-ss",str(ss),"-t",str(round(tlen if tlen else b-a+0.25,3))]
        inp+=["-i",src]
        pts="setpts=PTS-STARTPTS" if ss is not None or not loop else "setpts=PTS"
        fc.append(f"[{idx}:v]{pre}{pts}+{a-lead}/TB[g{idx}]")
        fc.append(f"{cur}[g{idx}]overlay={x}:{y}:enable='between(t,{a},{b})'[s{idx}]")
        cur=f"[s{idx}]"; idx+=1
    LEAD=0.09
    def panel(src,a,b,w,h,plate,tag,pre="",ss=None,tlen=None,loop=False,top_plate=None):
        x=(1920-w)//2; y=(1080-h)//2
        over(f"{G}/{plate}.png",a,b,loop=True,lead=LEAD)
        over(src,a,b,x=x,y=y,ss=ss,tlen=tlen,loop=loop,pre=pre,
             lead=(LEAD if ss is not None else 0.0))
        over(f"{G}/{top_plate or plate}.png",a,b,loop=True,lead=LEAD)
        if tag=="small": over(f"{G}/tag.png",a+0.10,b,x=x+26,y=y+26,loop=True)
        elif tag=="big": over(f"{G}/tag_big.png",a+0.10,b,x=40,y=40,loop=True)

    for name,beat in GFX:
        p=f"{G}/{name}.mov"
        if not os.path.exists(p): print(f"  ! missing {name}.mov -- skipped"); continue
        over(p,beat[0],beat[1])

    for (beat,src,si,w,h,plate,tag,slen) in VID:
        a,b=beat
        if not os.path.exists(src): print(f"  ! missing {os.path.basename(src)}"); continue
        r=_rate(beat,slen-si)
        # a retimed insert needs its own source length (lesson 42): setpts=PTS/r demands
        # r x the beat length off the source, and defaulting to the beat length ships a
        # fraction of the intended footage.
        panel(src,a,b,w,h,plate,tag,ss=si,tlen=round((b-a)*r+0.3,3),
              pre=f"setpts=PTS/{r},scale={w}:{h}:force_original_aspect_ratio=decrease,"
                  f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,")

    for (beat,png,w,h,plate,_x) in SHOTS:
        a,b=beat; d=round(b-a,3)
        # a still is never left static (lesson 1): pan the tall screenshot top->bottom,
        # which reads as scrolling the app. Pure translation, so no zoompan jitter.
        panel(png,a,b,w,h,plate,None,loop=True,
              pre=f"scale={w}:-1:flags=lanczos,crop={w}:{h}:0:'(ih-oh)*clip(t/{d},0,1)',setsar=1,")

    a,b=B.DEMOS; n=len(DEMOCLIPS); step=(b-a)/n
    for i,e in enumerate(DEMOCLIPS):
        da,db=round(a+i*step,3),round(a+(i+1)*step,3)
        panel(f"{DEMO}/{e}.mp4",da,db,1088,812,"plate_demo","small",ss=0.6,
              tlen=round(db-da+0.25,3),
              pre="scale=1088:812:force_original_aspect_ratio=increase,crop=1088:812,setsar=1,")

    _sl=_appgen_slices()
    for i,(ta,tb,si,rate) in enumerate(_sl):
        # the AFTER-alone slice (the last one) uses the plate with the disclosure BAKED
        # IN -- it covers the email-capture form, which must never appear in an ad
        # (Dan, ad-1 rev-2), and baking it removes the one-frame race a separate overlay
        # had at the slice boundary.
        last = (i == len(_sl)-1)
        if last:
            # crop=1320:1560:0:175 keeps the headline and the after image and cuts the
            # frame ABOVE the email-capture form, which starts at source y~1797. The
            # form is then absent from the pixels rather than covered by an overlay that
            # can drop a frame; the plate's baked disclosure sits over the black pad.
            pre=(f"setpts=PTS/{rate},crop=1320:1560:0:175,scale=520:-2:flags=lanczos,"
                 f"pad=520:1020:0:0:black,setsar=1,")
        else:
            pre=f"setpts=PTS/{rate},{AFCROP}scale=520:1020:flags=lanczos,setsar=1,"
        panel(APPFLOW,ta,tb,520,1020,"plate_app",None,ss=si,
              tlen=round((tb-ta)*rate+0.25,3),
              top_plate=("plate_app_cover" if last else None), pre=pre)

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
        for a,b,l in PUNCH: print(f"  {a:7.2f} -> {b:7.2f}  {l}")
        print("\nappgen slices:", _appgen_slices())
    if "punch" in sys.argv: punch()
    if "mix"   in sys.argv: mix()
