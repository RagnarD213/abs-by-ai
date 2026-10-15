"""RA-04 round 3: measure one Veo take before anyone looks at it.  usage: check_take04.py <AI1-1|AI1-2|AI1-3> <tag>
Writes round3/check/<tag>/: sheet.jpg (every 6th frame), first.jpg / last.jpg (first and last second, every 3rd frame),
selfchange.jpg (changes away from the man, window by window), and report.json with:
  * cut scan: frame-to-frame difference spikes (a baked cut or dissolve, RA-15 lesson / ad-edit lesson 111)
  * how close frame 0 and the last frame are to Dan's approved START and END (Veo should land on both)
  * self-change blobs: things that change away from the man (appear, vanish, drift), per 12-frame window
  * pose per sampled frame (posecheck.py): bone lengths against the START frame, knee angle, leg line against the rails (AI1-3)
  * AI1-3 only, rigid.py of frame 0 against each sampled frame: the sled parts (plate hub, platform corner) move together along
    the 45 degree rails, the near shoe moves with them (feet stay on the platform), the upright and lower rail stay still.
All coordinates are the approved frames' (941x1672); video frames are scaled to that size first."""
import sys, os, json, subprocess, glob
import cv2, numpy as np
W = "/Volumes/Extreme/_edit_work/ra04"; FC = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck"
PAIRS = {"AI1-1": ("S1_a", "F2_a"), "AI1-2": ("F2_a", "F3b_a"), "AI1-3": ("F4h", "F5p"), "AI1-12": ("S1_a", "F3b_a")}
RAIL = "533,1021,721,833"
PARTS = ["hub:780,615,870,675", "platform:505,480,565,535"]; SHOE = "shoe:575,545,650,600"
STILL = ["upright:885,620,925,720", "lowrail:600,960,680,1040", "pillar:590,390,650,470"]
cid, tag = sys.argv[1], sys.argv[2]
src = f"{W}/round3/motion/{tag}.mp4"; out = f"{W}/round3/check/{tag}"; os.makedirs(f"{out}/f", exist_ok=True)
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); F = []
while True:
    ok, f = cap.read()
    if not ok: break
    F.append(cv2.resize(f, (941, 1672), interpolation=cv2.INTER_AREA))
N = len(F); R = {"take": tag, "shot": cid, "frames": N, "fps": round(fps, 3), "seconds": round(N/fps, 3)}
def lab(img, s):
    im = img.copy(); cv2.rectangle(im, (0, 0), (300, 60), (0, 0, 0), -1); cv2.putText(im, s, (8, 44), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3); return im
def grid(idx, cols, w):
    tiles = [cv2.resize(lab(F[i], f"{i} {i/fps:.2f}s"), (w, int(w*1672/941))) for i in idx]
    while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
    return np.vstack([np.hstack(tiles[r*cols:(r+1)*cols]) for r in range(len(tiles)//cols)])
cv2.imwrite(f"{out}/sheet.jpg", grid(list(range(0, N, 6)) + [N-1], 9, 240), [cv2.IMWRITE_JPEG_QUALITY, 85])
sec = int(round(fps))
cv2.imwrite(f"{out}/first.jpg", grid(list(range(0, sec+1, 3)), 9, 300), [cv2.IMWRITE_JPEG_QUALITY, 88])
cv2.imwrite(f"{out}/last.jpg", grid(list(range(N-1-sec, N, 3)), 9, 300), [cv2.IMWRITE_JPEG_QUALITY, 88])
# cut / dissolve scan
g = [cv2.GaussianBlur(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (0, 0), 2).astype(np.float32) for f in F]
d = np.array([float(np.abs(g[i] - g[i-1]).mean()) for i in range(1, N)]); med = float(np.median(d))
R["cut_scan"] = {"median_diff": round(med, 2), "max_diff": round(float(d.max()), 2), "max_at_frame": int(d.argmax()) + 1,
                 "spikes": [(int(i)+1, round(float(d[i]), 2)) for i in np.nonzero(d > max(4*med, med + 6))[0]]}
# start / end match
s_img, e_img = (cv2.imread(f"{W}/round2/frames/{p}.png") for p in PAIRS[cid])
R["start_match_levels"] = round(float(np.abs(F[0].astype(np.float32) - s_img).mean()), 2)
R["end_match_levels"] = round(float(np.abs(F[-1].astype(np.float32) - e_img).mean()), 2)
# self-change away from the man, every 12-frame window (a5_cut.py's test: neighbourhood range, man = biggest change, grown 40 px)
k7 = np.ones((7, 7), np.uint8); heat = np.zeros((1672, 941), np.float32); blobs = []
for a in range(0, N-12, 12):
    A = cv2.GaussianBlur(F[a], (0, 0), 1.5).astype(np.float32); B = cv2.GaussianBlur(F[a+12], (0, 0), 1.5).astype(np.float32)
    dd = np.maximum(np.maximum(A - cv2.dilate(B, k7), cv2.erode(B, k7) - A), 0).max(2)
    raw = (np.abs(A - B).max(2) > 14).astype(np.uint8); n, l, st, _ = cv2.connectedComponentsWithStats(raw)
    man = np.zeros_like(raw)
    if n > 1:
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); man = cv2.dilate((l == big).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (81, 81)))
    m = ((dd > 12) & (man == 0)).astype(np.uint8); n2, l2, s2, _ = cv2.connectedComponentsWithStats(m)
    for j in range(1, n2):
        if s2[j, cv2.CC_STAT_AREA] >= 150: blobs.append(dict(frames=[a, a+12], area=int(s2[j, 4]), box=[int(v) for v in s2[j, :4]]))
    heat = np.maximum(heat, np.where(man > 0, 0, dd))
vis = cv2.cvtColor(np.clip(heat*8, 0, 255).astype(np.uint8), cv2.COLOR_GRAY2BGR); vis = cv2.addWeighted(vis, 0.8, F[0], 0.25, 0)
cv2.imwrite(f"{out}/selfchange.jpg", cv2.resize(vis, (470, 836)))
R["selfchange_blobs"] = sorted(blobs, key=lambda b: -b["area"])[:12]
# pose + rigid on sampled frames
samp = sorted(set(list(range(0, N, 6)) + [N-1])); pose = []; rig = []
for i in samp:
    p = f"{out}/f/{i:03d}.png"; cv2.imwrite(p, F[i])
    args = ["python3", f"{FC}/posecheck.py", p, "--json", f"{out}/f/{i:03d}.pose.json"] + (["--rail", RAIL] if cid == "AI1-3" else [])
    subprocess.run(args, capture_output=True)
    try: q = json.load(open(f"{out}/f/{i:03d}.pose.json"))
    except Exception: q = {"ok": False}
    pose.append(dict(frame=i, **{k: q.get(k) for k in ("ok", "torso_len", "thigh_len", "shin_len", "knee_angle", "hip_angle", "leg_vs_rail_deg")}))
    if cid == "AI1-3" and i > 0:
        a = ["python3", f"{FC}/rigid.py", f"{out}/f/000.png", p, "--guide", RAIL]
        for b in PARTS: a += ["--part", b]
        a += ["--part", SHOE]
        for b in STILL: a += ["--still", b]
        r = subprocess.run(a, capture_output=True, text=True).stdout
        try: rig.append(dict(frame=i, **json.loads(r[r.index("{"):])))
        except Exception: rig.append(dict(frame=i, raw=r[-400:]))
R["pose"] = pose
ok = [p for p in pose if p["ok"] and p["thigh_len"]]
if ok:
    t0 = ok[0]
    R["bone_change_max_pct"] = {b: round(100*max(abs(p[b]/t0[b] - 1) for p in ok if p[b]), 1) for b in ("torso_len", "thigh_len", "shin_len")}
if rig: R["rigid"] = rig
json.dump(R, open(f"{out}/report.json", "w"), indent=1)
print(json.dumps({k: R[k] for k in R if k not in ("pose", "rigid", "selfchange_blobs")}), "| blobs:", len(blobs))
