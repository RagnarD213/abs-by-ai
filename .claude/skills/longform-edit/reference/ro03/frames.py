"""RO-02 graded frames. Source is 1920x1080 (8/14 poolside, tripod). Two fixed compositions per shot, hair-anchored:
F (far, about x1.50) and N (near, about x1.86), each placed from the shot's own measurements (measure.json): centred on his head,
top edge a fixed pad above the highest his hair gets in that shot. Colour: the approved poolside grade (grade.py cube)
after a per-shot exposure trim (gamma) that brings raw torso-skin luma into the range the grade was approved on."""
import json, os, sys, subprocess, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edl as E, grade as GR
W = E.W; FPS = E.FPS
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SCALE = {"F": 1.45, "N": 1.80}; PAD0 = {"F": 50, "N": 40}       # round 1 windows: they fix each shot's BOTTOM edge (Dan approved the bottoms)
PAD = {"F": 25, "N": 20}                                        # round 2 (Dan, 10-04): half the headroom. Source px above the shot's highest hair
PAD_SHOT = {}                                                   # (shot id, framing) -> pad, for a shot whose hair would drop under ~20 px out
LOOK = os.environ.get("RO02_LOOK", "A")                         # A = C1630 calibration, strength 1.0; B = C1631, 0.8
LOOKS = {"A": ("C1630", 1.0), "B": ("C1631", 0.8)}
BAND = (0.38, 0.50)                                             # raw torso-skin luma on the approved sample's rolls: 0.37-0.52, median 0.43
S = json.load(open(f"{W}/shots.json")); M = json.load(open(f"{W}/measure.json")); SK = json.load(open(f"{W}/skin.json"))
def _rows(sh, table):
    a, b = sh["src_f0"]/FPS, sh["src_f1"]/FPS
    r = [x for x in table[sh["piece"]] if a-0.3 <= x[0] <= b+0.3]
    return r or table[sh["piece"]]
CARD_CX = 1336/1920            # under a left card his head sits at the centre of the space right of it (x752..1920)
def crop(sh, framing, card=False):
    r = np.array(_rows(sh, M)); tops = np.sort(r[:, 1]); med = np.median(tops)
    good = tops[tops >= med-36] if (tops < med-36).mean() < 0.15 else tops       # a few far-low outliers = mask touching the chimney
    top = float(good.min()); hx = float(np.median(r[:, 2])); x0b, x1b = float(np.percentile(r[:, 3], 2)), float(np.percentile(r[:, 4], 98))
    h0 = int(round(1080/SCALE[framing]/2))*2; y0 = int(round(min(max(top-PAD0[framing], 0), 1080-h0)/2))*2; bottom = y0+h0
    y = int(round(max(top-PAD_SHOT.get((sh["id"], framing), PAD[framing]), 0)/2))*2          # new top; the bottom edge stays where round 1 had it
    h = int(round((bottom-y)/2))*2; w = int(round(h*16/9/2))*2
    x = hx-w/2
    if x1b-x0b <= w-40:                                         # keep hands and elbows inside when the body span fits
        x = min(x, x0b-20); x = max(x, x1b+20-w)
    if card: x = hx-CARD_CX*w                                   # slide the window left inside the 1080p frame: same size, same y, same grade
    x = int(round(min(max(x, 0), 1920-w)/2))*2
    return w, h, x, y
SETS = ("set1", "set2", "set3")                                # one filmed hold, shown three times: one exposure trim for all of it
def gamma(sh):
    v = float(np.median([x[1] for x in (SK["set1"] if sh["piece"] in SETS else _rows(sh, SK))]))
    tgt = min(max(v, BAND[0]), BAND[1])
    g = np.log(tgt)/np.log(v)
    return round(float(min(max(g, 0.75), 1.15))/0.025)*0.025
def lut(sh):
    g = gamma(sh); roll, s = LOOKS[LOOK]; p = f"{W}/look/cubes/{LOOK}_g{g:.3f}.cube"
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True); GR.cube(roll, s, p, n=49, pre_gamma=g)
    return p
def vf(sh, framing, look=True, card=False):
    w, h, x, y = crop(sh, framing, card)
    s = f"crop={w}:{h}:{x}:{y},scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le"
    if look: s += f",lut3d=file='{lut(sh)}':interp=tetrahedral"
    return s+",format=rgb24"
def shot_at(t):
    f = int(round(t*FPS)); return next(s for s in S if s["out_f0"] <= f < s["out_f1"])
def frame_src(sh, ts, framing, look=True, card=False):
    p = subprocess.run([FF, "-v", "error", "-ss", f"{max(0, ts-1):.4f}", "-i", E.src(sh["roll"]), "-ss", f"{min(1, ts):.4f}", "-frames:v", "1",
                        "-vf", vf(sh, framing, look, card), "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (1920, 1080), p)
def frame_at(t, framing, look=True):
    sh = shot_at(t); return frame_src(sh, (sh["src_f0"]+int(round(t*FPS))-sh["out_f0"])/FPS, framing, look)
if __name__ == "__main__":
    for sh in S: print(f"{sh['id']:12s} {sh['roll']} F{crop(sh,'F')} N{crop(sh,'N')} gamma {gamma(sh):.3f}")
