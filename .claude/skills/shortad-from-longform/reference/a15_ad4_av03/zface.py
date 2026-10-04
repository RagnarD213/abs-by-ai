#!/usr/bin/env python3
"""FACE centre x on the base at every measure.json sample (mediapipe FaceMesh, the delivery gate's own instrument).
The person-mask 'head' value is the median column of the mask's top 18 %: raised hands and a turned head drag it (the
gate read one hold +6.5 % off centre where the mask head said +3 %). Writes measure_face.json {n: face_x in source px}."""
import json, subprocess, numpy as np, mediapipe as mp
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
M = [m for m in json.load(open('measure.json')) if m.get('ok')]; ns = sorted(m['n'] for m in M)
open('rc/sel_face.txt', 'w').write("select='" + '+'.join(f'eq(n,{n})' for n in ns) + "',scale=960:540")
p = subprocess.Popen([FF, '-nostdin', '-v', 'error', '-i', 'base.mp4', '-filter_script:v', 'rc/sel_face.txt', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=10**8)
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=False, min_detection_confidence=0.4)
out = {}
for n in ns:
    b = p.stdout.read(960*540*3)
    if len(b) < 960*540*3: break
    r = fm.process(np.frombuffer(b, np.uint8).reshape(540, 960, 3))
    if r.multi_face_landmarks:
        xs = np.array([l.x for l in r.multi_face_landmarks[0].landmark]); out[n] = round(float((xs.min() + xs.max())/2*1920), 1)
json.dump(out, open('measure_face.json', 'w'))
d = np.array([out[m['n']] - m['head'] for m in M if m['n'] in out])
print(f'{len(out)}/{len(ns)} faces; face - mask head (source px): median {np.median(d):+.1f}, p5 {np.percentile(d,5):+.1f}, p95 {np.percentile(d,95):+.1f}, |d|>20: {(np.abs(d)>20).sum()}, |d|>30: {(np.abs(d)>30).sum()}')
