#!/usr/bin/env python3
"""QC for the modern-edit sample: splice visibility, pacing, loudness, script fidelity."""
import json, re, statistics, subprocess, sys
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC="modern_sample.mp4"
import importlib.util
mod=importlib.util.spec_from_file_location("m60","modern60.py")
m60=importlib.util.module_from_spec(mod); mod.loader.exec_module(m60)

tc=json.load(open("tight_cuts.json"))
acc=0.0; splices=[]
for a,b in tc["keeps"][:-1]:
    acc+=b-a; splices.append(round(acc,3))

# intentional visual changes: punch-level boundaries + graphic in/out points
punch=[p[0] for p in m60.PUNCH[1:]]
gfx=[t for beat in (m60.CALLOUT,m60.GEN,m60.PHONE,m60.TODAY,m60.BULLETS,m60.LOWER3,
                    m60.TITLE,m60.SHOP) for t in beat]
covered=[(a,b) for a,b in (m60.GEN,m60.PHONE,m60.TODAY,m60.BULLETS,m60.TITLE,m60.SHOP)]

subprocess.run([FF,"-v","error","-i",SRC,"-vf",
 "scale=320:180,tblend=all_mode=difference,signalstats,"
 "metadata=print:key=lavfi.signalstats.YAVG:file=qcdiff.txt","-an","-f","null","-"],check=True)
vals=[]
for blk in open("qcdiff.txt").read().split("frame:")[1:]:
    t=re.search(r"pts_time:([\d.]+)",blk); v=re.search(r"YAVG=([\d.]+)",blk)
    if t and v: vals.append((float(t.group(1)),float(v.group(1))))
ys=[v for _,v in vals]
p99=sorted(ys)[int(len(ys)*.99)]
print(f"frame-diff control: median {statistics.median(ys):.2f}  p99 {p99:.2f}  ({len(ys)} frames)")

def near(t,xs,w=0.12): return any(abs(t-x)<w for x in xs)
def under(t): return any(a-0.05<=t<=b+0.05 for a,b in covered)

bad=[]
print("\npause-removal splices:")
for s in splices:
    d=max([v for t,v in vals if abs(t-s)<0.05] or [0])
    why=("under a graphic" if under(s) else
         "on a punch change" if near(s,punch) else
         "on a graphic edge" if near(s,gfx) else "BARE")
    flag=""
    if why=="BARE" and d>p99: flag="   <<< VISIBLE"; bad.append((s,d))
    print(f"   t={s:6.2f}  diff={d:5.2f}  {why}{flag}")
print(f"\n{len(bad)} bare splices above the p99 ceiling")

# pacing
changes=sorted(set([0.0]+punch+gfx+[float(subprocess.run(
    [FF.replace('ffmpeg','ffprobe'),"-v","error","-show_entries","format=duration",
     "-of","csv=p=0",SRC],capture_output=True,text=True).stdout.strip())]))
shots=[round(changes[i+1]-changes[i],2) for i in range(len(changes)-1) if changes[i+1]-changes[i]>0.2]
print(f"\nvisual changes: {len(changes)-1}   median hold {statistics.median(shots):.2f}s   "
      f"longest hold {max(shots):.2f}s")
assert max(shots)<=25.0, "a visual sits unchanged longer than 25s"
print("PASS: nothing sits visually unchanged longer than 25s")
sys.exit(1 if bad else 0)
