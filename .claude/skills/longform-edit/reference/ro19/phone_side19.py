"""RO-19 round 3, P07: the approved app tour beside Dan (RO-06's closing scene, VIDEO-RULES 2026-10-10) on the trainer and nutritionist lines.
One fixed composition for both sentences (shots outro.0r4 + outro.0r5, one continuous take of roll C1512, the camera frame graded as the build grades it):
his picture sits DX px to the right (never animated), the approved iPhone shell on the left. DX = 270: across all 461 frames his arms reach from x 300 to
x 1620 in the camera frame (person mask, every 3rd frame), so both arms stay inside the frame (30 px spare on the right) and clear of the phone (54 px).
The strip the move uncovers is hidden behind the phone; the 40 px of it at the frame edge is the take's own left edge, mirrored.
Phone screens follow HIS WORDS here (trainer first, then nutritionist; RO-06 said them the other way round). Output frames at 29.97:
  0    home   the app's home screen, a visible tap on AI Trainer as he says "AI personal trainer"
  44   sheet  Push-Up, then (118) Reverse Lunge: the app's own exercise sheets, each demo playing at natural speed, AI-GENERATED on the video
  191  home   again, a visible tap on Macro Tracker as he says "AI nutritionist"
  226  macro  real recording B0038 from frame 30: the salmon plate, "Analyzing your meal", the itemised result (775 cal), a tap on Log Meal,
  336         then the same recording from frame 262 (4 s of the unchanged result screen skipped): the meal logged, today's total
Screens and captures are RO-06's (ro06/round6/phone/cap, appcap6.py); nothing here is new app footage.
usage: phone_side19.py [--stills]"""
import sys, os, json, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import softblue as B, frames as F, phone_demo as PD
W = "/Volumes/Extreme/_edit_work/ro19"; OUT = f"{W}/round3/phone"; CAP = "/Volumes/Extreme/_edit_work/ro06/round6/phone/cap"; FPS = 30000/1001; FF = B.FF
P = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"; os.makedirs(OUT, exist_ok=True)
B38 = glob.glob("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/screen-recordings/B0038*")[0]
DX = 270; OX = -50
T_S1, T_S2, T_H2, T_M, T_M2 = 44, 118, 191, 226, 336
REC0, REC2 = 30, 262                                     # recording frame shown at T_M, and at T_M2
TAP_MACRO = (216, 133); TAP_TRAINER = (216, 316)         # tiles on the 432 px wide home screen (hub_tiles.json x 432/390)
BLUE = (36, 128, 218); SHOTS = ("outro.0r4", "outro.0r5")
def dec(path, vf, n=None, ss=None):
    c = [FF, "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss else []) + ["-i", path] + (["-frames:v", str(n)] if n else []) + ["-vf", vf + ",format=rgb24", "-f", "rawvideo", "-"]
    return subprocess.run(c, capture_output=True, check=True).stdout
def screen_png(name): return Image.open(f"{CAP}/{name}.png").convert("RGB").resize((432, 935), Image.Resampling.LANCZOS).crop((0, 0, 432, 920))
def ring(im, xy, k, n=15):
    if not 0 <= k < n: return
    d = ImageDraw.Draw(im); rad = 12 + int(k/FPS*28*1.9); cx, cy = xy
    d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=BLUE, width=4); d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=BLUE)
DEMO_SS = {"pushup": 0.0, "reverse-lunge": 0.3}
class Screens:
    def __init__(self):
        self.home = screen_png("hub")
        raw = dec(B38, "scale=in_color_matrix=bt709:in_range=tv,crop=526:968:24:62,scale=432:795:flags=lanczos"); self.macro = np.frombuffer(raw, np.uint8).reshape(-1, 795, 432, 3)
        assert len(self.macro) > REC2 + (461 - T_M2) + 2, len(self.macro)            # never hold the recording's last frame
        a = self.macro[120].astype(int); m = (a[..., 2] > 180) & (a[..., 0] < 90) & (a[..., 1] < 130); ys, xs = np.nonzero(m)      # the blue Log Meal button on the result screen
        self.log_xy = (int(xs.mean()), int(ys.mean())); assert m.sum() > 4000, m.sum()
        self.sheet = {}
        for ex, n0 in (("pushup", T_S2 - T_S1), ("reverse-lunge", T_H2 - T_S2)):
            box = json.load(open(f"{CAP}/sheet_{ex}.json"))["video"]; k = 432/390
            x, y, w, h = [int(round(v*k)) for v in box]
            raw = dec(f"{P}/public/exercise-demos/{ex}.mp4", f"fps=30000/1001,scale={w}:{h}:flags=lanczos:in_color_matrix=bt709:in_range=tv", n=n0 + 4, ss=DEMO_SS[ex])
            self.sheet[ex] = (screen_png(f"sheet_{ex}"), (x, y, w, h), np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3))
    def macro_frame(self, r, k):
        fr_ = self.macro[r]; im = Image.new("RGB", (432, 920), tuple(int(v) for v in fr_[-4:].reshape(-1, 3).mean(0)))
        im.paste(Image.fromarray(fr_), (0, 0)); ring(im, self.log_xy, k - (T_M2 - 16)); return im
    def sheet_frame(self, ex, j):
        base, (x, y, w, h), V = self.sheet[ex]; im = base.copy(); assert j < len(V), (ex, j)
        m = Image.new("L", (w, h)); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 13, fill=255); im.paste(Image.fromarray(V[j]), (x, y), m)
        d = ImageDraw.Draw(im, "RGBA"); tw = int(B.text_w("AI-GENERATED", B.font(12))); d.rounded_rectangle((x + 9, y + 9, x + 9 + tw + 18, y + 31), 11, fill=(20, 22, 26, 165)); d.text((x + 18, y + 13), "AI-GENERATED", font=B.font(12), fill=(250, 250, 250, 255))
        return im
    def at(self, k):
        if k < T_S1: im = self.home.copy(); ring(im, TAP_TRAINER, k - (T_S1 - 16)); t0 = 0
        elif k < T_S2: im = self.sheet_frame("pushup", k - T_S1); t0 = T_S1
        elif k < T_H2: im = self.sheet_frame("reverse-lunge", k - T_S2); t0 = T_S2
        elif k < T_M: im = self.home.copy(); ring(im, TAP_MACRO, k - (T_M - 16)); t0 = T_H2
        elif k < T_M2: im = self.macro_frame(REC0 + k - T_M, k); t0 = T_M
        else: im = self.macro_frame(REC2 + k - T_M2, -99); t0 = 0
        if t0 and k - t0 < 7:                               # a new screen slides in from the right over 7 frames
            prev = self.at(t0 - 1); q = B.ease((k - t0 + 1)/FPS, 7/FPS); dx = int(round((1 - q)*432))
            c = prev.copy(); c.paste(im, (dx, 0)); return c
        return im
def presenter(n, src0):
    roll, lf = F.roll_of(src0); ts = lf/FPS; ss = max(0, ts - 1)
    p = subprocess.Popen([FF, "-v", "error", "-ss", f"{ss:.4f}", "-i", F.ROLLS[roll]["path"], "-ss", f"{max(0, ts-ss-0.4/FPS):.4f}", "-frames:v", str(n), "-vf", F.vf(roll, (1920, 1080, 0, 0)), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    for _ in range(n):
        b = p.stdout.read(1920*1080*3); assert len(b) == 1920*1080*3
        yield np.frombuffer(b, np.uint8).reshape(1080, 1920, 3)
    p.stdout.close(); p.wait()
def compose(a, scr, k):
    out = np.empty_like(a); out[:, DX:] = a[:, :1920 - DX]; out[:, :DX] = a[:, :DX][:, ::-1]
    im = Image.fromarray(out); q = B.ease((k + 1)/FPS, 10/FPS)                       # the phone fades in over the first 10 frames
    ph = PD.shell(im.copy(), scr, OX)
    return Image.blend(im, ph, q) if q < 1 else ph
if __name__ == "__main__":
    S = {s["id"]: s for s in json.load(open(f"{W}/shots.json"))}; a, b = S[SHOTS[0]], S[SHOTS[1]]
    assert a["src_f1"] == b["src_f0"] and a["out_f1"] == b["out_f0"], "the two shots are no longer one continuous take"
    n = b["out_f1"] - a["out_f0"]; src0 = a["src_f0"]; assert n == 461, n
    print("P07", n, "frames, source frame", src0, "film", round(a["out_f0"]/FPS, 3), "to", round(b["out_f1"]/FPS, 3), flush=True)
    SC = Screens(); print("Log Meal button at", SC.log_xy); stills = "--stills" in sys.argv
    want = (8, 34, 50, 100, 125, 180, 200, 218, 240, 290, 328, 340, 400, 455) if stills else range(n)
    e = None if stills else PD.writer(f"{OUT}/P07-side.mp4")
    for k, fr_ in enumerate(presenter(n, src0)):
        if k not in want: continue
        im = compose(fr_, SC.at(k), k)
        if stills: im.resize((960, 540)).save(f"{OUT}/P07-still-{k:03d}.jpg", quality=88)
        else: e.stdin.write(im.tobytes())
    if e: e.stdin.close(); e.wait(); print("P07 written", n, "frames")
