"""scan.py S: frame-by-frame check of a rendered short: every large picture change against the planned cuts, near-identical
frames inside talking shots, and a strip of the five frames around every cut -> build/<S>/scan_cuts.jpg"""
import json, subprocess, sys, numpy as np
from PIL import Image, ImageDraw
import plans as P
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
for S in sys.argv[1:]:
    V=f"build/{S}/{P.NAME[S]}.mp4"; shots=json.load(open(f"build/{S}/shots.json")); N=shots[-1]["f1"]
    raw=subprocess.run([FF,"-v","error","-i",V,"-vf","scale=270:480","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,480,270,3)
    d=np.abs(fr[1:].astype(np.int16)-fr[:-1].astype(np.int16)).reshape(len(fr)-1,-1).mean(1)
    cuts=[s["f0"] for s in shots[1:]]; big=[int(i)+1 for i in np.where(d>12)[0]]
    print(S,"frames",len(fr),"plan",N,"| planned cuts",len(cuts),"| unplanned big changes:",[b for b in big if min(abs(b-c) for c in cuts)>1],"| planned cuts with no visible change:",[c for c in cuts if d[c-1]<4])
    for s in shots:
        if s["kind"]!="talk": continue
        z=np.where(d[s["f0"]:s["f1"]-1]<0.15)[0]
        if len(z): print("   near-identical frames in talk shot",s["idx"],[s["f0"]+int(q) for q in z][:8])
    rows=[]
    for c in cuts:
        row=Image.new("RGB",(270*5,480))
        for k,j in enumerate(range(c-2,c+3)): row.paste(Image.fromarray(fr[min(max(j,0),len(fr)-1)]),(k*270,0))
        ImageDraw.Draw(row).text((4,4),f"{S} cut f{c} {c/FPS:.2f}s",fill=(255,255,0)); rows.append(row)
    sh=Image.new("RGB",(1350*3,480*((len(rows)+2)//3)))
    for i,r in enumerate(rows): sh.paste(r,((i%3)*1350,(i//3)*480))
    sh.save(f"build/{S}/scan_cuts.jpg",quality=78)
