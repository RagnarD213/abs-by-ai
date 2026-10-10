"""Round 6, P03 (Dan, 15:49): Dan on camera with the app in a phone frame beside him, left third.
One fixed composition for the whole sentence (shot cta.0r1, roll C1581, the camera frame as shot and graded as the build grades it): his picture sits
DX px to the right (never animated; GRAPHICS-STANDARDS "Lists and phones alongside Dan"), the approved iPhone shell (phone_demo.shell) on the left.
The strip the move uncovers is hidden behind the phone; the 40 px of it that shows at the frame edge is the take's own foliage, mirrored.
Phone screens, in order (frames at 29.97):
  home   the app's own home screen (appcap6.py, local copy of the app), a visible tap on Macro Tracker
  macro  real recording B0038 from frame 30: the salmon plate, "Analyzing your meal", the itemised result (775 cal)
  home   again, a visible tap on AI Trainer (as he says "we're also going to use AI to design a custom workout plan")
  sheet  the app's own Push-Up sheet, then Reverse Lunge, each with its demo file playing at natural speed in the player's rectangle,
         AI-GENERATED on the video where the app puts it
usage: phone_side.py [--stills]"""
import sys, os, json, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
import softblue as B, frames as F, phone_demo as PD
W = "/Volumes/Extreme/_edit_work/ro06"; OUT = f"{W}/round6/phone"; CAP = f"{OUT}/cap"; FPS = 30000/1001; FF = B.FF
P = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
B38 = glob.glob("/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/screen-recordings/B0038*")[0]
DX = 290; OX = -50                                       # his picture moves right by DX; the shell's left edge lands at 90 + OX = 40
T_MACRO, T_HOME2, T_SHEET1, T_SHEET2 = 57, 159, 180, 242  # output frames where each screen takes over
TAP1 = (216, 133); TAP2 = (216, 316)                     # Macro Tracker and AI Trainer tiles on the 432 px wide screen (hub_tiles.json x 432/390)
BLUE = (36, 128, 218)
def fr(t): return int(round(t*FPS))
def dec(path, vf, n=None, ss=None):
    c = [FF, "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss else []) + ["-i", path] + (["-frames:v", str(n)] if n else []) + ["-vf", vf + ",format=rgb24", "-f", "rawvideo", "-"]
    return subprocess.run(c, capture_output=True, check=True).stdout
def screen_png(name): return Image.open(f"{CAP}/{name}.png").convert("RGB").resize((432, 935), Image.Resampling.LANCZOS).crop((0, 0, 432, 920))
def ring(im, xy, k, n=15):
    """The visible tap: a filled dot and a ring that grows over n frames."""
    if not 0 <= k < n: return
    d = ImageDraw.Draw(im); rad = 12 + int(k/FPS*28*1.9); cx, cy = xy
    d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=BLUE, width=4); d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=BLUE)
class Screens:
    def __init__(self):
        self.home = screen_png("hub")
        raw = dec(B38, "scale=in_color_matrix=bt709:in_range=tv,crop=526:968:24:62,scale=432:795:flags=lanczos"); self.macro = np.frombuffer(raw, np.uint8).reshape(-1, 795, 432, 3)
        self.sheet = {}
        for ex, n0 in (("pushup", T_SHEET2 - T_SHEET1), ("reverse-lunge", 400)):
            box = json.load(open(f"{CAP}/sheet_{ex}.json"))["video"]; k = 432/390
            x, y, w, h = [int(round(v*k)) for v in box]
            raw = dec(f"{P}/public/exercise-demos/{ex}.mp4", f"fps=30000/1001,scale={w}:{h}:flags=lanczos:in_color_matrix=bt709:in_range=tv", n=n0 + 4, ss=DEMO_SS[ex])
            self.sheet[ex] = (screen_png(f"sheet_{ex}"), (x, y, w, h), np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3))
    def macro_frame(self, j):
        im = Image.new("RGB", (432, 920), tuple(int(v) for v in self.macro[min(30 + j, len(self.macro) - 1)][-4:].reshape(-1, 3).mean(0)))
        im.paste(Image.fromarray(self.macro[min(30 + j, len(self.macro) - 1)]), (0, 0)); return im
    def sheet_frame(self, ex, j):
        base, (x, y, w, h), V = self.sheet[ex]; im = base.copy()
        m = Image.new("L", (w, h)); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 13, fill=255); im.paste(Image.fromarray(V[min(j, len(V) - 1)]), (x, y), m)
        d = ImageDraw.Draw(im, "RGBA"); tw = int(B.text_w("AI-GENERATED", B.font(12))); d.rounded_rectangle((x + 9, y + 9, x + 9 + tw + 18, y + 31), 11, fill=(20, 22, 26, 165)); d.text((x + 18, y + 13), "AI-GENERATED", font=B.font(12), fill=(250, 250, 250, 255))
        return im
    def at(self, k):
        """(screen for output frame k, the screen it is sliding in over or None, slide progress)."""
        if k < T_MACRO: im = self.home.copy(); ring(im, TAP1, k - (T_MACRO - 16)); cur = (im, T_MACRO*0)
        elif k < T_HOME2: cur = (self.macro_frame(k - T_MACRO), T_MACRO)
        elif k < T_SHEET1: im = self.home.copy(); ring(im, TAP2, k - (T_SHEET1 - 16)); cur = (im, T_HOME2)
        elif k < T_SHEET2: cur = (self.sheet_frame("pushup", k - T_SHEET1), T_SHEET1)
        else: cur = (self.sheet_frame("reverse-lunge", k - T_SHEET2), T_SHEET2)
        im, t0 = cur
        if t0 and k - t0 < 7:                               # a new screen slides in from the right over 7 frames
            prev = self.at(t0 - 1); q = B.ease((k - t0 + 1)/FPS, 7/FPS); dx = int(round((1 - q)*432))
            c = prev.copy(); c.paste(im, (dx, 0)); return c
        return im
DEMO_SS = {"pushup": 0.0, "reverse-lunge": 0.3}   # second sheet was Reverse Crunch: its demo pauses at the top of the rep (the review read an 8 frame hold in 1.7 s). Reverse Lunge never stops moving
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
    if q < 1:
        return Image.blend(im, ph, q)
    return ph
if __name__ == "__main__":
    R = json.load(open(f"{W}/plan_resolved.json")); it = next(r for r in R if r["id"] == "P03"); f0, f1 = fr(it["t0"]), fr(it["t1"]); n = f1 - f0
    S = json.load(open(f"{W}/shots.json")); sh = next(s for s in S if s["out_f0"] <= f0 < s["out_f1"]); assert sh["out_f0"] == f0 and sh["out_f1"] == f1, (sh, f0, f1)
    src0 = sh["src_f0"]; print("P03", n, "frames, shot", sh["id"], "source frame", src0, flush=True)
    SC = Screens(); stills = "--stills" in sys.argv
    if "--screens" in sys.argv:                            # the reusable asset (Dan, 2026-10-10: "save that for future reuse"): the phone screen alone, 432x920, same timing
        e = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "432x920", "-framerate", "30000/1001", "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p",
                              "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", f"{OUT}/app-tour-screens-432x920.mp4"], stdin=subprocess.PIPE)
        for k in range(n): e.stdin.write(SC.at(k).tobytes())
        e.stdin.close(); e.wait(); print("screens written", n); sys.exit(0); want = (8, 30, 50, 60, 100, 150, 170, 183, 210, 250, 290) if stills else range(n)
    e = None if stills else PD.writer(f"{OUT}/P03-side.mp4")
    for k, a in enumerate(presenter(n, src0)):
        if k not in want: continue
        im = compose(a, SC.at(k), k)
        if stills: im.save(f"{OUT}/P03-still-{k:03d}.jpg", quality=90)
        else: e.stdin.write(im.tobytes())
    if e: e.stdin.close(); e.wait(); print("P03 written", n, "frames")
