"""RO-06 round 5: the two app demos in the Soft Blue phone card (full screen: the closing roll C1581 is shot too close for a
phone beside Dan). Writes round5/phone/P01-softblue.mp4 and P02-softblue.mp4 (1920x1080, 29.97, BT.709), used as plan clips.

P01 = Dan's approved self-generation demo (Ad 14 R3 g17, simulated/composited provenance kept): the SAME screen content,
steps and timing, lifted out of the old olive card and placed in the approved WV-01 iPhone shell on the Soft Blue field;
then the SAME settled pool result with its AI-GENERATED chip exactly as approved (embedded in the picture). The before
picture carries "Real picture of me. Not AI-generated." for the whole phone phase, as the approved Ad 14 finish did.
P02 = the real app recording B0034 (workout list, tap "How to do it", the exercise sheet with its demo video) in the same
shell, WV-01's approved workout-app format: upright phone, visible tap, AI-GENERATED chip on the AI exercise demo.
usage: phone_demo.py [P01] [P02] [--stills]"""
import sys, os, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import softblue as B
W = "/Volumes/Extreme/_edit_work/ro06"; OUT = f"{W}/round5/phone"; FPS = 30000/1001; FF = B.FF; U = 2.0
DEMO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/simulated-dan-sunglasses-to-pool-ad14-v1.mp4"
B34 = "/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/screen-recordings/B0034_app-monday-workout-goblet-squat-video-sheet_780x1476_23s.mp4"
SQUAT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/public/exercise-demos/db-goblet-squat.mp4"   # the app's own demo file for this sheet
CARD = (241, 57, 1723, 1023)                 # where the approved demo's card sat
DISP = (741, 68, 434, 941)                   # the demo phone's display (measured: union of the white UI frames), corner radius about 52
PHOTO = (647, 94, 673, 904)                  # the settled pool result inside the demo frame (measured)
def decode(path, vf):
    raw = subprocess.run([FF, "-v", "error", "-i", path, "-vf", vf + ",format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return raw
def shell(im, content, ox, fill_below=None):
    """The approved WV-01 iPhone shell (wv01-edit/round4/recipe/graphics.py iphone(), same geometry as gfx.iphone), with the
    status area taking the app's own top colour so a dark screen does not sit under a white strip."""
    sh = Image.new("RGBA", im.size); ImageDraw.Draw(sh).rounded_rectangle((91+ox, 34, 573+ox, 1062), 68, fill=(0, 0, 0, 120))
    im = Image.alpha_composite(im.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(14))).convert("RGB")
    def rr(box, fill, r, outline=None, width=1): ImageDraw.Draw(im).rounded_rectangle((box[0]+ox, box[1], box[2]+ox, box[3]), r, fill=fill, outline=outline, width=width)
    rr((90, 28, 562, 1052), (95, 107, 119), 66, (166, 179, 190), 2); rr((95, 33, 557, 1047), (5, 8, 12), 62)
    p = ImageOps.contain(content, (432, 920), Image.Resampling.LANCZOS); a = np.asarray(p)
    top = tuple(int(v) for v in np.median(np.concatenate([a[:6, :10], a[:6, -10:]], 1).reshape(-1, 3), 0))   # the page colour at the top corners, not a picture scrolled under the bar
    bot = fill_below or tuple(int(v) for v in np.median(a[-6:].reshape(-1, 3), 0))
    scr = Image.new("RGB", (448, 1000), top); d = ImageDraw.Draw(scr)
    d.rectangle((0, 65 + p.height, 448, 1000), fill=bot)
    if p.width < 448:                                                 # side slivers take each row's own edge colour
        x0 = (448 - p.width)//2; scr.paste(p.crop((0, 0, 1, p.height)).resize((x0, p.height)), (0, 65)); scr.paste(p.crop((p.width-1, 0, p.width, p.height)).resize((448 - x0 - p.width, p.height)), (x0 + p.width, 65))
    scr.paste(p, ((448 - p.width)//2, 65))
    ink = (25, 32, 40) if sum(top) > 380 else (240, 243, 246)
    d.text((30, 14), "9:41", font=B.font(17), fill=ink)
    for i in range(4): d.rounded_rectangle((352+i*6, 30-i*3, 355+i*6, 35), 1, fill=ink)
    d.rounded_rectangle((391, 22, 418, 34), 3, outline=ink, width=2); d.rectangle((419, 26, 422, 30), fill=ink); d.rectangle((394, 25, 413, 31), fill=ink)
    d.rounded_rectangle((146, 15, 302, 51), 18, fill=(0, 0, 0)); d.ellipse((276, 26, 288, 38), fill=(18, 26, 36)); d.ellipse((280, 29, 284, 33), fill=(34, 60, 82))
    d.rounded_rectangle((153, 984, 295, 989), 3, fill=(24, 28, 32) if sum(bot) > 380 else (235, 238, 242))
    m = Image.new("L", (448, 1000)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 447, 999), 54, fill=255); im.paste(scr, (102+ox, 40), m)
    rr((86, 202, 90, 258), (69, 81, 94), 2); rr((86, 283, 90, 354), (69, 81, 94), 2); rr((562, 253, 566, 352), (86, 96, 110), 2)
    return im
def stage(t):
    im = B.field(t); B.glass(im, CARD, t, U, 22); return im
def square_corners(a, r=56):
    """The demo display has rounded corners with the old bezel outside them: every row inside the corner radius takes its
    own first pixel inside the arc, so the lifted screen is a clean rectangle (flat UI colour there on every frame)."""
    a = a.copy(); h, w = a.shape[:2]
    for dy in range(r):
        inset = int(math.ceil(r - math.sqrt(r*r - (r - dy)**2))) + 3
        for y in (dy, h - 1 - dy):
            a[y, :inset] = a[y, inset]; a[y, w - inset:] = a[y, w - inset - 1]
    return a
def writer(path):
    return subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-framerate", "30000/1001", "-i", "-",
                             "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p", "-c:v", "libx264", "-crf", "12", "-preset", "medium",
                             "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", path], stdin=subprocess.PIPE)
def p01_frame(F, k):
    """k = output frame. Demo frames 0..107 are the phone phase, 110.. the settled result (108, 109 were its slide in)."""
    t = k/FPS; im = stage(t)
    if k < 108:
        x, y, w, h = DISP; scr = Image.fromarray(square_corners(F[k][y:y+h, x:x+w]))
        im = shell(im, scr, 334)                                   # left of centre: the label needs the room on the right, inside the card
        B.disclosure(im, "Real picture of me. Not AI-generated.", (928, 505), 1.6, anchor="lt")
        return im
    x, y, w, h = PHOTO; ph = Image.fromarray(F[min(max(k, 110), len(F)-1)][y:y+h, x:x+w])
    q = B.ease((k - 108)/FPS, .22); dx = int(round((1 - q)*520))
    m = Image.new("L", (w, h)); ImageDraw.Draw(m).rounded_rectangle((0, 0, w-1, h-1), 46, fill=255)
    ImageDraw.Draw(im).rounded_rectangle((x - 4 + dx, y - 4, x + w + 3 + dx, y + h + 3), 50, fill=(92, 152, 198))
    im.paste(ph, (x + dx, y), m)
    if dx:                                                           # the card edge clips a picture still sliding in
        st = stage(t); mk = Image.new("L", im.size, 0); ImageDraw.Draw(mk).rounded_rectangle(CARD, 44, fill=255); im = Image.composite(im, st, mk)
    return im
_SQ = None
def squat(i):
    """The demo the sheet plays, at natural speed. In the recording the sheet's player sits paused on its first frame for the whole take (watch judge: 'the
    exercise picture never plays'), so the app's own demo file is laid into the player's rectangle, as in the approved WV-01 workout-app composition."""
    global _SQ
    if _SQ is None:
        raw = decode(SQUAT, "fps=30000/1001,scale=388:218:in_color_matrix=bt709:in_range=tv"); _SQ = np.frombuffer(raw, np.uint8).reshape(-1, 218, 388, 3)
    return Image.fromarray(_SQ[min(i, len(_SQ) - 1)])
def p02_frame(G, k, k0=75):
    """k = output frame; recording frame k0 + k. The sheet opens on recording frame 115; the tap ring runs the 16 frames before."""
    t = k/FPS; im = stage(t); f = min(k0 + k, 302); c = Image.fromarray(G[f]).resize((432, 817), Image.Resampling.LANCZOS); d = ImageDraw.Draw(c)
    if 99 <= f < 115:
        rad = 12 + int((f - 99)/FPS*28*1.9); cx, cy = 81, 214
        d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=(36, 128, 218), width=4); d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=(36, 128, 218))
    if f >= 115:                                                     # the exercise demo in the sheet is AI-made footage of Dan
        m = Image.new("L", (388, 218)); ImageDraw.Draw(m).rounded_rectangle((0, 0, 387, 217), 13, fill=255); c.paste(squat(f - 115), (22, 261), m)
        d.rounded_rectangle((231, 450, 402, 472), 5, fill=(6, 17, 30)); d.text((241, 453), "AI-GENERATED", font=B.font(15), fill=(248, 250, 252))
    im = shell(im, c, 234)
    x = 900; y = 372
    if t > .05:
        a = B.ease(t, .55); B.rr(im, (x, y + 8, x + 8 + 70*a, y + 16), B.CYAN, 3); B.text(im, (x, y + 30), "YOUR CUSTOM WORKOUT PLAN", 30, B.CYAN)
    for i, ln in enumerate(["Built Around", "The Equipment", "You HAVE."]):
        tt = t - .18 - i*.22
        if tt > 0: B.text(im, (x - 4, y + 98 + i*76*1.22 + (1 - B.ease(tt, .55))*26), ln, 76)
    return im
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); which = [a for a in sys.argv[1:] if not a.startswith("--")] or ["P01", "P02"]; stills = "--stills" in sys.argv
    if "P01" in which:
        F = np.frombuffer(decode(DEMO, "scale=in_color_matrix=bt709:in_range=tv"), np.uint8).reshape(-1, 1080, 1920, 3); N = 340
        if stills:
            for k in (10, 60, 100, 108, 109, 111, 200): p01_frame(F, k).save(f"{OUT}/P01-still-{k:03d}.png")
        else:
            e = writer(f"{OUT}/P01-softblue.mp4")
            for k in range(N): e.stdin.write(p01_frame(F, k).tobytes())
            e.stdin.close(); e.wait(); print("P01", N, "frames")
    if "P02" in which:
        G = np.frombuffer(decode(B34, "fps=30000/1001,scale=in_color_matrix=bt709:in_range=tv"), np.uint8).reshape(-1, 1476, 780, 3); N = 228
        if stills:
            for k in (5, 30, 38, 41, 120): p02_frame(G, k).save(f"{OUT}/P02-still-{k:03d}.png")
        else:
            e = writer(f"{OUT}/P02-softblue.mp4")
            for k in range(N): e.stdin.write(p02_frame(G, k).tobytes())
            e.stdin.close(); e.wait(); print("P02", N, "frames")
