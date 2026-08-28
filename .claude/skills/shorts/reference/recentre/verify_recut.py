#!/usr/bin/env python3
"""Prove the re-cut changed the framing and nothing else.

1. frame count, duration, fps, resolution and audio identical to the shipped file
2. audio bit-identical (the cut and the mix were not touched)
3. an old/new strip from the FINISHED files so the framing is judged by eye
"""
import subprocess, os, sys, json, cv2, numpy as np, hashlib
SP="/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/39032698-3f11-4a8d-9382-8b0b6599b994/scratchpad"
ROOT="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
FF=f"{ROOT}/Media/video_edit/bin/ffmpeg"; FP=f"{ROOT}/Media/video_edit/bin/ffprobe"
SF=f"{ROOT}/Short-form video content"
OUT={'v2':f"{ROOT}/YouTube Long Form Video Content/six-ways-ai-abs/out",
     'v3':f"{ROOT}/YouTube Long Form Video Content/v3-top10-tips/out",
     'v6':f"{ROOT}/YouTube Long Form Video Content/v6-3min-home-workout/out"}

def probe(p):
    j=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-select_streams','v:0',
        '-show_entries','stream=width,height,r_frame_rate,nb_read_frames','-show_entries','format=duration',
        '-of','json',p]).decode())
    s=j['streams'][0]
    return (s['width'],s['height'],s['r_frame_rate'],s['nb_read_frames'],round(float(j['format']['duration']),3))

def audio_md5(p):
    r=subprocess.run([FF,'-v','error','-i',p,'-map','0:a','-f','md5','-'],capture_output=True)
    return r.stdout.decode().strip()

def strip(old,new,name,k=6):
    d=float(subprocess.check_output([FP,'-v','error','-show_entries','format=duration','-of','csv=p=0',new]).decode())
    cols=[]
    for i in range(k):
        t=d*(i+0.5)/k; pair=[]
        for tag,p in (('OLD',old),('NEW',new)):
            o=f"{SP}/vf/{name}_{tag}_{i}.png"; os.makedirs(f"{SP}/vf",exist_ok=True)
            subprocess.run([FF,'-y','-v','error','-ss',f'{t:.2f}','-i',p,'-frames:v','1','-vf','scale=176:313',o],check=True)
            im=cv2.imread(o); cv2.line(im,(88,0),(88,313),(0,0,255),1)
            cv2.putText(im,tag,(3,13),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
            pair.append(im)
        cols.append(np.hstack(pair)); cols.append(np.zeros((313,10,3),np.uint8))
    body=np.hstack(cols)
    lab=np.zeros((20,body.shape[1],3),np.uint8)
    cv2.putText(lab,name,(4,14),cv2.FONT_HERSHEY_SIMPLEX,0.45,(255,255,255),1)
    return np.vstack([lab,body])

MAP=json.load(open(f"{SP}/recut_map.json"))   # delivered name -> (build, out basename)
rows=[]; ok=True
for name,(b,base) in MAP.items():
    old=f"{SF}/{name}.mp4"; new=f"{OUT[b]}/{base}.mp4"
    if not os.path.exists(new): print(f"MISSING {new}"); ok=False; continue
    po,pn=probe(old),probe(new)
    ao,an=audio_md5(old),audio_md5(new)
    same = po==pn and ao==an
    ok &= same
    print(f"{'PASS' if same else 'FAIL'} {name:38} {pn[3]}f {pn[4]}s {pn[0]}x{pn[1]} {pn[2]}  audio {'identical' if ao==an else 'CHANGED'}")
    if po!=pn: print(f"      shipped {po}\n      new     {pn}")
    rows.append(strip(old,new,name))
w=max(r.shape[1] for r in rows)
rows=[np.hstack([r,np.zeros((r.shape[0],w-r.shape[1],3),np.uint8)]) for r in rows]
cv2.imwrite(f"{SP}/verify_recut.png",np.vstack(rows))
print(f"\n{'ALL PARITY CHECKS PASS' if ok else 'PARITY FAILURES ABOVE'}  -> {SP}/verify_recut.png")
