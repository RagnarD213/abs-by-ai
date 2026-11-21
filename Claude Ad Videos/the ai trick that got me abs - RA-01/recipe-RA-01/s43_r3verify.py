#!/usr/bin/env python3
"""ROUND 3 proof pass: s43_r3verify.py <9x16|16x9> <master.mp4> [--out r3/verify_<k>.json]

Measures, on the DELIVERED frames, exactly the three picture things plan section 13 rules on:

  D4  the face box inside 8-92 % of the frame width on EVERY frame of every talking hold
  D5  (16:9) his head centre across every NEAR<->FAR join, and the per-hold medians
  D6  (16:9) the CTA pill clear of him on every frame of both beats, and clear of the caption ink

The face box is mediapipe FaceDetection (model_selection=1), the same detector the round-2 review
used; where it fails the face-mesh hull is used and the frame is flagged. Every talking frame is
decoded -- no sampling.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
import mediapipe as mp

KEY, SRC = sys.argv[1], sys.argv[2]
OUT = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else f"r3/verify_{KEY}.json"
B = json.load(open("beats.json"))
TL = json.load(open(f"timeline_{KEY}.json"))
W, H = (1080, 1920) if KEY == "9x16" else (1920, 1080)
SC = 0.5                                   # measure at half size; fractions are scale-free
FD = 1001/30000

dan = [it for it in TL["items"] if it["kind"] == "dan"]
f0, f1 = dan[0]["f0"], dan[-1]["f1"]

raw = subprocess.run([L.FF, "-nostdin", "-v", "error", "-i", SRC,
                      "-vf", f"select='between(n\\,{f0}\\,{f1-1})',scale={int(W*SC)}:{int(H*SC)}",
                      "-vsync", "0", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True, check=True).stdout
w2, h2 = int(W*SC), int(H*SC)
frames = np.frombuffer(raw, np.uint8).reshape(-1, h2, w2, 3)
print(f"{KEY}: decoded {len(frames)} talking frames ({f0}..{f1-1})")

fd = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                                     refine_landmarks=False, min_detection_confidence=0.5)


def face(a):
    r = fd.process(np.ascontiguousarray(a))
    if r.detections:
        b = r.detections[0].location_data.relative_bounding_box
        return b.xmin, b.xmin + b.width, "detect"
    r = fm.process(np.ascontiguousarray(a))
    if r.multi_face_landmarks:
        xs = [p.x for p in r.multi_face_landmarks[0].landmark]
        return min(xs), max(xs), "mesh"
    return None, None, "miss"


rows, misses = [], 0
for it in dan:
    for n in range(it["f0"], it["f1"]):
        x0, x1, how = face(frames[n-f0])
        if x0 is None:
            misses += 1
            rows.append(dict(hold=it["a"], lvl=it["punch"]["level"] if "punch" in it else None,
                             n=n, t=round(n*FD, 3), how=how)); continue
        rows.append(dict(hold=it["a"], n=n, t=round(n*FD, 3), how=how,
                         x0=round(x0*100, 2), x1=round(x1*100, 2), cx=round((x0+x1)/2*100, 2)))
fd.close(); fm.close()

lvl = {p["beat"]: p["level"] for p in TL["punch"]}
crop = {p["beat"]: p["crop"] for p in TL["punch"]}
holds = []
for it in dan:
    rs = [r for r in rows if r["hold"] == it["a"] and "x0" in r]
    bad = [r for r in rs if r["x0"] < 8.0 or r["x1"] > 92.0]
    holds.append(dict(name=it["name"], beat=round(it["a"], 3), level=lvl[it["a"]],
                      crop=crop[it["a"]], frames=len(rs),
                      x0_min=round(min(r["x0"] for r in rs), 2),
                      x1_max=round(max(r["x1"] for r in rs), 2),
                      cx_med=round(float(np.median([r["cx"] for r in rs])), 2),
                      cx_first=rs[0]["cx"], cx_last=rs[-1]["cx"],
                      out_of_band=[(r["t"], r["x0"], r["x1"]) for r in bad]))
    h = holds[-1]
    print(f"  {h['name']} {h['level']:<4} {h['beat']:7.3f} crop {h['crop']}  face x "
          f"{h['x0_min']:5.1f}..{h['x1_max']:5.1f} %  cx med {h['cx_med']:5.1f} %  "
          f"out-of-8..92: {len(h['out_of_band'])}")

joins = []
for i in range(len(dan)-1):
    a, b = dan[i], dan[i+1]
    visible = b["f0"] - a["f1"] == 0
    if lvl[a["a"]] == lvl[b["a"]]: continue
    ha, hb = holds[i], holds[i+1]
    joins.append(dict(a=ha["name"], b=hb["name"], la=ha["level"], lb=hb["level"],
                      visible=visible, t=round(b["a"], 3),
                      cx_last_a=ha["cx_last"], cx_first_b=hb["cx_first"],
                      d_frame=round(abs(ha["cx_last"]-hb["cx_first"]), 2),
                      d_median=round(abs(ha["cx_med"]-hb["cx_med"]), 2),
                      crop_centre_a=crop[a["a"]][2] + crop[a["a"]][0]/2,
                      crop_centre_b=crop[b["a"]][2] + crop[b["a"]][0]/2))
    j = joins[-1]
    print(f"  join {j['a']}({j['la']})->{j['b']}({j['lb']}) {'VISIBLE' if visible else 'card'} "
          f"t={j['t']}  head centre {j['cx_last_a']:.1f}% -> {j['cx_first_b']:.1f}% "
          f"(d {j['d_frame']:.1f} %, medians d {j['d_median']:.1f} %)  crop centres "
          f"{j['crop_centre_a']:.0f} / {j['crop_centre_b']:.0f}")

rep = dict(key=KEY, source=os.path.abspath(SRC), frames=len(frames), misses=misses,
           holds=holds, joins=joins,
           worst_face=dict(x0_min=min(h["x0_min"] for h in holds),
                           x1_max=max(h["x1_max"] for h in holds),
                           out_of_band=sum(len(h["out_of_band"]) for h in holds)),
           visible_join_max_d=max([j["d_frame"] for j in joins if j["visible"]] or [0]),
           visible_join_max_median_d=max([j["d_median"] for j in joins if j["visible"]] or [0]))
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
json.dump(rep, open(OUT, "w"), indent=1)
print(f"{KEY}: face box {rep['worst_face']['x0_min']:.1f}..{rep['worst_face']['x1_max']:.1f} %, "
      f"{rep['worst_face']['out_of_band']} frames outside 8-92 %, {misses} detector misses")
print(f"{KEY}: visible NEAR<->FAR joins: max head-centre step {rep['visible_join_max_d']:.1f} % "
      f"(per-hold medians {rep['visible_join_max_median_d']:.1f} %)")
print("->", OUT)
