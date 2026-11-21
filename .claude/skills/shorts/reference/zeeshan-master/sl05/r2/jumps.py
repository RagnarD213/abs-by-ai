#!/usr/bin/env python3
"""jumps.py: inherited same-framing jump cuts inside every piece (the full-rate cut finder missed them: whole-frame
diff 3-7, under its threshold). Face-band diff (rows 0-60% , central 50%) at 480x270: a single-frame spike >= 3x the
median of the 12 frames around it and >= 2.0. Prints source time + exact frame."""
import json, subprocess, math, numpy as np
B='/Volumes/Extreme/_edit_work/sl05/build'; FPS=30000/1001
FF='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
cfg=json.loads(subprocess.check_output(['node','-e',"const c=require('./config.js');const {SEGMENTS}=require('./segments.js');console.log(JSON.stringify({c,S:SEGMENTS}))"],cwd=B))
for s in cfg['S']:
    for p in s['pieces']:
        a=p['start']; n=int((p['end']-a)*FPS)
        raw=subprocess.run([FF,'-v','error','-ss',f'{a:.4f}','-i',cfg['c']['SRC'],'-frames:v',str(n),'-vf','scale=480:270:in_color_matrix=bt709:in_range=tv,format=gray','-f','rawvideo','-'],capture_output=True).stdout
        fr=np.frombuffer(raw,np.uint8).reshape(-1,270,480).astype(float)[:, :162, 120:360]
        d=np.abs(fr[1:]-fr[:-1]).mean((1,2)); first=math.ceil(a*FPS)
        for k in range(len(d)):
            nb=np.r_[d[max(0,k-6):k],d[k+1:k+7]]
            if d[k]>=2.0 and d[k]>=3*np.median(nb) and d[k] >= 1.6*nb.max():
                f=first+k+1; print(f"{s['id']} src {f/FPS:8.3f} frame {f} diff {d[k]:5.1f} nb med {np.median(nb):4.1f} out {f/FPS-a:6.2f}+piece")
