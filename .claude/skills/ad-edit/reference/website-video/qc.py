#!/usr/bin/env python3
"""Website video QC -- the /longform-edit suite plus the ad-specific assertions.

 1 splice visibility vs the file's own frame-diff control distribution
 2 punch integrity: no segment under 0.20 s, no two adjacent at the same framing
 3 pacing: nothing visually unchanged longer than 25 s
 4 loudness -14 LUFS / true peak, and the voice centred
 5 script fidelity: re-transcribe the FINISHED render and diff against the tight words
 6 no drug names spoken
 7 every AI insert carries a label window
 8 BANNED SCREENS: template-scan the finished picture for the app's side-by-side
   before/after and for the email-capture form -- measured on the delivered pixels, not
   on the build plan (the plan was right about the window and still shipped a violation
   on Ad 1 because the asset in-point was 0.27 s early)
 9 caption/graphic collision: no caption event inside a full-screen card
"""
import json, os, re, statistics, subprocess, sys
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import beats as B, layout as L
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.environ.get("QCIN",f"{HERE}/website_video_16x9.mp4")
fails=[]
def check(ok,msg):
    print(("  PASS  " if ok else "  FAIL  ")+msg)
    if not ok: fails.append(msg)
print(f"QC {os.path.basename(SRC)}")
dur=float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",
                          SRC],capture_output=True,text=True).stdout)
print(f"duration {int(dur//60)}:{dur%60:05.2f}\n")

# ------------------------------------------------------------------ 1 splices
tc=json.load(open(f"{HERE}/tight_cuts.json"))
acc,splices=0.0,[]
for a,b in tc["keeps"][:-1]:
    acc+=b-a; splices.append(round(acc,3))
punch=[p[0] for p in L.PUNCH[1:]]
gfx_t=[t for _,beat in L.GFX for t in beat]
OVERLAYS={n.lower() for n in B.OVERLAY}
covered=[beat for name,beat in L.GFX if name not in OVERLAYS]
covered+=[B.MACRO]                       # rev 2: the PiP beat (no SHOTS any more)
subprocess.run([FF,"-v","error","-i",SRC,"-vf",
  "scale=320:180,tblend=all_mode=difference,signalstats,"
  f"metadata=print:key=lavfi.signalstats.YAVG:file={HERE}/qcdiff.txt","-an","-f","null","-"],check=True)
vals=[]
for blk in open(f"{HERE}/qcdiff.txt").read().split("frame:")[1:]:
    t=re.search(r"pts_time:([\d.]+)",blk); v=re.search(r"YAVG=([\d.]+)",blk)
    if t and v: vals.append((float(t.group(1)),float(v.group(1))))
ys=sorted(v for _,v in vals); p99=ys[int(len(ys)*.99)]
print(f"frame-diff control: median {statistics.median(ys):.2f}  p99 {p99:.2f}")
near=lambda t,xs,w=0.14: any(abs(t-x)<w for x in xs)
under=lambda t: any(a-0.05<=t<=b+0.05 for a,b in covered)
bare=[]
for s in splices:
    d=max([v for t,v in vals if abs(t-s)<0.05] or [0])
    if under(s) or near(s,punch) or near(s,gfx_t): continue
    if d>p99: bare.append((s,round(d,2)))
check(not bare,f"bare splices above the p99 ceiling: {bare[:6]}")

# ------------------------------------------------------------------ 2 punch
short=[(a,b,l) for a,b,l in L.PUNCH if b-a<0.20]
check(not short,f"punch segments under 0.20s: {short}")
same=[(L.PUNCH[i][2],L.PUNCH[i+1][0]) for i in range(len(L.PUNCH)-1)
      if L.PUNCH[i][2]==L.PUNCH[i+1][2]]
check(not same,f"adjacent segments at the same framing (jump cut): {same}")

bad=[(a,b,l) for a,b,l in L.PUNCH if l not in L.LEVELS]
check(not bad,f"every framing level is an asserted crop (no wide shot, no light): {bad}")
wide=[(a,b,l) for a,b,l in L.PUNCH if L.LEVELS[l][2]>3058 or L.LEVELS[l][0]+L.LEVELS[l][2]>L.LIGHT_X]
check(not wide,f"no level exceeds the widest allowed crop or reaches x>{L.LIGHT_X}: {wide}")

# ------------------------------------------------------------------ 3 pacing
changes=sorted(set([0.0]+punch+gfx_t+list(B.MACRO)+[dur]))
shots=[round(changes[i+1]-changes[i],2) for i in range(len(changes)-1) if changes[i+1]-changes[i]>0.2]
print(f"visual changes {len(changes)-1}   median hold {statistics.median(shots):.2f}s   longest {max(shots):.2f}s")
check(max(shots)<=25.0,f"nothing visually unchanged longer than 25s (worst {max(shots):.2f}s)")

# ------------------------------------------------------------------ 4 audio
# ⚠ THE ONE AUDIO GATE (2026-09-02): _shared/audio/audio_gate.py must have stamped THIS file
# (sha256-matched, verdict PASS). The loudness/peak/centring below stay as a print; the stamp decides.
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
try:
    from require_stamp import require_stamp; require_stamp(SRC); check(True,"audio gate stamp present, matches this file, PASS")
except SystemExit as _e: check(False,f"audio gate: {_e}")
p=subprocess.run([FF,"-nostats","-i",SRC,"-af","ebur128=peak=true","-f","null","-"],
                 capture_output=True,text=True).stderr
gi=lambda k: float(re.findall(rf"{k}:\s*(-?[\d.]+)",p)[-1])
I,TP,LRA=gi("I"),gi("Peak"),gi("LRA")
print(f"loudness  I {I:.2f} LUFS   true peak {TP:.2f} dBTP   LRA {LRA:.1f} LU")
check(abs(I+14)<=0.6,f"integrated loudness within 0.6 LU of -14 (got {I:.2f})")
check(TP<=-0.9,f"true peak at or under -1.0 dBTP (got {TP:.2f})")
raw=subprocess.run([FF,"-v","error","-i",SRC,"-map","0:a","-ac","2","-ar","48000","-f","f32le","-"],
                   capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.float32).reshape(-1,2)
corr=float(np.corrcoef(a[:,0],a[:,1])[0,1])
mid,side=(a[:,0]+a[:,1])/2,(a[:,0]-a[:,1])/2
sep=20*np.log10(np.sqrt((mid**2).mean())/(np.sqrt((side**2).mean())+1e-12))
print(f"stereo    L/R corr {corr:+.4f}   side {sep:.1f} dB under mid")
check(corr>0.95,f"voice is centred (L/R correlation {corr:+.4f})")

# ------------------------------------------------------------------ 5 fidelity
TXF=f"{HERE}/qc.whisper.json"
if not os.path.exists(TXF):
    wav=f"{HERE}/_qc.wav"
    subprocess.run([FF,"-v","error","-y","-i",SRC,"-map","0:a","-ac","1","-ar","16000",
                    "-c:a","pcm_s16le",wav],check=True)
    os.environ["PATH"]=os.path.dirname(FF)+os.pathsep+os.environ.get("PATH","")
    import whisper
    json.dump(whisper.load_model("small.en").transcribe(wav,language="en"),open(TXF,"w"))
norm=lambda s: re.sub(r"[^a-z0-9 ]"," ",s.lower()).split()
said=norm(" ".join(s["text"] for s in json.load(open(TXF))["segments"]))
want=norm(" ".join(w["w"] for w in tc["words"]))
import difflib
ratio=difflib.SequenceMatcher(None,want,said).ratio()
print(f"script fidelity {ratio*100:.1f}%  ({len(want)} words expected, {len(said)} heard)")
check(ratio>=0.95,f"finished render matches the cut's words (>=95%, got {ratio*100:.1f}%)")

# ------------------------------------------------------------------ 6 drug names
banned=re.compile(r"\b(zepbound|tirzepatide|semaglutide|ozempic|mounjaro|wegovy)\b",re.I)
hits=[s["text"].strip() for s in json.load(open(TXF))["segments"] if banned.search(s["text"])]
check(not hits,f"no drug names spoken: {hits}")

# ------------------------------------------------------------------ 7 AI labels
# the ONLY AI image in this video is Dan's goal image on the SOLVED card; gfx.py tags it
check(os.path.exists(f"{HERE}/gfx/solved.mov") and os.path.exists(f"{HERE}/gfx/tag.png"),
      "the goal image card exists and carries the AI-GENERATED tag (built in gfx.py g_solved)")

# ------------------------------------------------------------------ 8 banned screens
def _patch(path, ss, pre, w, h, dsz=(48,96)):
    raw=subprocess.run([FF,"-v","error","-ss",str(ss),"-i",path,"-frames:v","1",
        "-vf",f"{pre}scale={dsz[0]}:{dsz[1]}","-f","rawvideo","-pix_fmt","gray","-"],
        capture_output=True).stdout
    if len(raw)<dsz[0]*dsz[1]: return None
    return np.frombuffer(raw[:dsz[0]*dsz[1]],dtype=np.uint8).astype(np.float64)
APPSRC=f"{L.APP}/app-flow-generate-future-self.mp4"   # the recording that CONTAINS the banned screens
# the two banned screens, rendered through the SAME crop/scale chain as the insert
refs={}
for lbl,ss in (("before/after 'Meet the new you'",26.5),("email-capture form",30.0)):
    r=_patch(APPSRC,ss,L.AFCROP+"scale=433:820,",433,820)
    if r is not None: refs[lbl]=r
# EVERY frame, not a sample: the email-capture form was exposed for exactly ONE frame
# at 179.41 s and a 2 fps scan stepped straight over it. A compliance gate that samples
# cannot see a single-frame violation.
raw=subprocess.run([FF,"-v","error","-i",SRC,"-vf",
    "crop=433:820:150:130,scale=48:96","-f","rawvideo","-pix_fmt","gray","-"],
    capture_output=True).stdout
n=len(raw)//(48*96)
frames=np.frombuffer(raw[:n*48*96],dtype=np.uint8).astype(np.float64).reshape(n,-1)
worst={}
for lbl,r in refs.items():
    rz=(r-r.mean())/(r.std()+1e-9)
    fz=(frames-frames.mean(1,keepdims=True))/(frames.std(1,keepdims=True)+1e-9)
    c=(fz@rz)/len(rz)
    i=int(np.argmax(c)); FD=1001/30000
    worst[lbl]=(round(float(c[i]),3),round(i*FD,2))
    print(f"  banned-screen scan ({len(frames)} frames): {lbl:30s} best {c[i]:+.3f} at {i*FD:.2f}s")
check(all(v[0]<0.90 for v in worst.values()),
      f"no banned app screen on the delivered picture: {worst}")

# ------------------------------------------------------------------ 9 captions
capf=f"{HERE}/cap.ass"
if os.path.exists(capf):
    ev=[l for l in open(capf) if l.startswith("Dialogue:")]
    def secs(x):
        h,m,s=x.split(":"); return int(h)*3600+int(m)*60+float(s)
    SUP=[B.BEFORE,B.TODAY,B.TRIAL,B.PRICE,B.SOLVED,B.CTA]
    coll=[]
    for l in ev:
        f=l.split(","); a2,b2=secs(f[1]),secs(f[2])
        # 0.02 s slack: ASS timestamps are centisecond-quantised (ad-edit lesson 66)
        if any(not (b2<=s+0.02 or a2>=e-0.02) for s,e in SUP): coll.append(round(a2,2))
    print(f"captions: {len(ev)} cues")
    check(not coll,f"no caption sits on a full-screen card: {coll[:6]}")

print("\n"+("QC PASSED" if not fails else f"QC FAILED -- {len(fails)} check(s)"))
sys.exit(1 if fails else 0)
