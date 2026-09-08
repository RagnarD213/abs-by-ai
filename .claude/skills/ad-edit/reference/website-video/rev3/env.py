#!/usr/bin/env python3
"""5 ms RMS envelope of base.mov (lav mono)."""
import json, os, subprocess
import numpy as np
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; HERE=os.path.dirname(os.path.abspath(__file__))
SR=48000; HOP=0.005
raw=subprocess.run([FF,"-v","error","-i",f"{HERE}/base.mov","-map","0:a","-ac","1",
                    "-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.float32); h=int(HOP*SR); n=len(a)//h
db=20*np.log10(np.sqrt((a[:n*h].reshape(n,h)**2).mean(1)+1e-12))
json.dump({"hop":HOP,"db":[round(float(x),2) for x in db]},open(f"{HERE}/env.json","w"))
print(f"env.json {n} frames = {n*HOP:.1f}s   floor p05 {np.percentile(db,5):.1f}  p50 {np.percentile(db,50):.1f}  p95 {np.percentile(db,95):.1f}")
