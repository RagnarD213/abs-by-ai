#!/usr/bin/env python3
"""Website video -- pause removal over base.mov, CALMER than the ad setting.

Silence is measured from the 5 ms RMS envelope of the REAL audio, never from Whisper's
word times (ad-edit lesson 20). This is the trust video that plays right before the
buy, so it keeps a little more breath than the ads: only pauses >= 0.30 s are touched,
each is shortened to ~0.24 s (0.10 tail + 0.14 head), never removed outright.
Outputs tight.mov + tight_cuts.json (the source->tight map every later pass uses).
"""
import json, os, subprocess
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=f"{HERE}/base.mov"
FD=1001/30000
TAILPAD=0.60; SIL_DB=-40.0; MINSIL=0.30
KEEP_TAIL=0.12; KEEP_HEAD=0.18; MIN_REMOVE=0.08
HOOK_SAFE=3.0           # no splice inside the opening line
frames=lambda t: round(t/FD)
snapf=lambda t: round(frames(t)*FD,6)

edl=json.load(open(f"{HERE}/edl.json"))["ranges"]
rw,off=[],0.0
for rg in edl:
    wh=json.load(open(f"{HERE}/tx/{rg['roll']}.whisper.json"))
    ws=[w for s in wh["segments"] for w in s.get("words",[])]
    for w in ws:
        if rg["start"]-0.05 <= w["start"] <= rg["end"]:
            rw.append({"t":round(off+w["start"]-rg["start"],3),
                       "e":round(off+min(w["end"],rg["end"])-rg["start"],3),"w":w["word"]})
    off+=rg["end"]-rg["start"]
BASE_DUR=off
SPAN_END=round(min(rw[-1]["e"]+TAILPAD,off),3)

env=json.load(open(f"{HERE}/env.json")); HOP=env["hop"]; DB=env["db"]
runs,cur=[],None
for i in range(min(int(SPAN_END/HOP),len(DB))):
    if DB[i]<SIL_DB: cur=(cur[0],i) if cur else (i,i)
    else:
        if cur: runs.append(cur); cur=None
if cur: runs.append(cur)
sil=[(a*HOP,(b+1)*HOP) for a,b in runs if (b-a+1)*HOP>=MINSIL]

# range joins on the base timeline: a splice there is already a cut, keep those pauses tighter
joins=[]; acc=0.0
for rg in edl[:-1]:
    acc+=rg["end"]-rg["start"]; joins.append(round(acc,3))

cuts=[]
for s0,s1 in sil:
    pv=max((w for w in rw if w["e"]<=s0+0.12),key=lambda w:w["e"],default=None)
    nx=min((w for w in rw if w["t"]>=s1-0.02),key=lambda w:w["t"],default=None)
    ci,co=snapf(s0+KEEP_TAIL),snapf(s1-KEEP_HEAD)
    if co-ci<MIN_REMOVE: continue
    if ci<=HOOK_SAFE: continue
    cuts.append({"in":ci,"out":co,"rm":round(co-ci,3),
                 "a":pv["w"].strip() if pv else "?","b":nx["w"].strip() if nx else "?",
                 "join":any(ci-0.3<=j<=co+0.3 for j in joins)})
keeps,prev=[],0.0
for c in cuts:
    keeps.append([round(prev,6),c["in"]]); prev=c["out"]
keeps.append([round(prev,6),snapf(SPAN_END)])
keeps=[k for k in keeps if k[1]-k[0]>0.05]
dur=sum(b-a for a,b in keeps)
print(f"base {BASE_DUR:.2f}s  span {SPAN_END:.2f}s -> tight {dur:.2f}s ({int(dur//60)}:{dur%60:04.1f})")
print(f"{len(cuts)} cuts, {sum(c['rm'] for c in cuts):.1f}s removed")
print(f"density {len(rw)/dur*60:.0f} wpm")

def to_tight(t):
    acc=0.0
    for a,b in keeps:
        if t<a: return round(acc,3)
        if t<=b: return round(acc+t-a,3)
        acc+=b-a
    return round(acc,3)
json.dump({"keeps":keeps,"cuts":cuts,"dur":round(dur,3),"span_end":SPAN_END,
           "joins_base":joins,"joins_tight":[to_tight(j) for j in joins],
           "words":[{"t":to_tight(w["t"]),"e":to_tight(w["e"]),"w":w["w"]} for w in rw]},
          open(f"{HERE}/tight_cuts.json","w"),indent=1)
print("tight_cuts.json written")

if os.environ.get("RENDER","1")=="1":
    parts=[f"[0:a]asplit={len(keeps)}"+"".join(f"[m{i}]" for i in range(len(keeps)))]
    cat=""
    for i,(a,b) in enumerate(keeps):
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,setsar=1[v{i}]")
        parts.append(f"[m{i}]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}]")
        cat+=f"[v{i}][a{i}]"
    fc=";".join(parts)+f";{cat}concat=n={len(keeps)}:v=1:a=1[vout][ac]"
    subprocess.run([FF,"-nostdin","-y","-v","error","-i",BASE,"-filter_complex",fc,
        "-map","[vout]","-map","[ac]","-c:v","libx264","-preset","medium","-crf","15",
        "-pix_fmt","yuv420p","-r","30000/1001","-c:a","pcm_s16le",f"{HERE}/tight.mov"],check=True)
    print("tight.mov written")
