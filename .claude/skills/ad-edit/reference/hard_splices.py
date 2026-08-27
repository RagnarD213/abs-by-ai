#!/usr/bin/env python3
"""Which pause-removal splices are VISIBLY discontinuous, measured before the punch pass.

QC fails a splice whose frame difference exceeds the finished file's own p99 control.
Waiting for QC to say so costs a full re-render, and covering EVERY uncovered splice with
a punch change shreds the pacing (37 uncovered here, only 4 actually visible). So measure
the tight cut directly and force a punch boundary only where the join really jumps.

  hard_splices.py <tight.mov> <tight_cuts.json> <out.json>
"""
import json, re, subprocess, sys
import statistics
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"
tight, tcf, out = sys.argv[1], sys.argv[2], sys.argv[3]
tmp="/tmp/_hsdiff.txt"
subprocess.run([FF,"-v","error","-i",tight,"-vf",
  "scale=320:180,tblend=all_mode=difference,signalstats,"
  f"metadata=print:key=lavfi.signalstats.YAVG:file={tmp}","-an","-f","null","-"],check=True)
vals=[]
for blk in open(tmp).read().split("frame:")[1:]:
    t=re.search(r"pts_time:([\d.]+)",blk); v=re.search(r"YAVG=([\d.]+)",blk)
    if t and v: vals.append((float(t.group(1)),float(v.group(1))))
ys=sorted(v for _,v in vals); p99=ys[int(len(ys)*.99)]
tc=json.load(open(tcf)); acc=0.0; sp=[]
for a,b in tc["keeps"][:-1]:
    acc+=b-a; sp.append(round(acc,3))
hard=[]
for s in sp:
    d=max([v for t,v in vals if abs(t-s)<0.05] or [0])
    if d>p99: hard.append([s,round(d,2)])
print(f"control median {statistics.median(ys):.2f}  p99 {p99:.2f}")
print(f"{len(hard)} of {len(sp)} splices exceed the ceiling on the tight cut")
print("  ",[h[0] for h in hard][:20])
json.dump({"p99":p99,"hard":[h[0] for h in hard],"detail":hard},open(out,"w"),indent=1)
