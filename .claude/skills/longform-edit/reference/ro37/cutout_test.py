"""RO-37 cutout test (Dan, 2026-10-29: "Run the test"): can the portrait pool footage be cut out cleanly enough to stand Dan
on the moving Soft Blue field, no box? 20 s of one continuous take (C1895 86.26-106.26, 'Maybe you're just not feeling it...
Zero minutes breaks it'), three layouts: 0-8 s wide (Dan right, a side list left), 8-13 s the full-frame pool close-up,
13-20 s corner (his gym clip full screen, Dan small lower right). Mattes compared: BiRefNet per frame (Replicate, ~$0.002
a frame), the same with a 3-frame temporal median on the alpha, and Apple Vision's person mask (local)."""
import sys, os, io, json, subprocess, concurrent.futures as cf, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"; sys.path.insert(0, f"{P}/.claude/skills/background-removal/scripts"); sys.path.insert(0, f"{P}/.claude/skills/_shared")
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RO-37/round1/recipe")
import removebg as RB, softblue as SB, frames as F, build as B
T = "/Volumes/Expansion/_edit_work/RO-37/cutout_test"; FF = F.FF; FPS = F.FPS
SRC, S0, DUR = F.ROLLS["C1895"], 86.26, 20.0
N = round(DUR * FPS); WIDE = range(0, round(8 * FPS)); CORNER = range(round(13 * FPS), N)
NEED = list(WIDE) + list(CORNER)
os.makedirs(f"{T}/src", exist_ok=True); os.makedirs(f"{T}/bi", exist_ok=True); os.makedirs(f"{T}/vi", exist_ok=True)
# 1. graded source frames (colour F), 2160x3840
if not os.path.exists(f"{T}/src/{N-1:04d}.png"):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(S0), "-t", str(DUR), "-i", SRC, "-vf", f"{F.DEC},{F.GRADE},format=rgb24",
                    "-start_number", "0", f"{T}/src/%04d.png"], check=True)
# 2. BiRefNet alpha per needed frame (downscaled copy to the model, alpha back to full size)
tok = RB.token(); ver = RB.latest_version(tok)
def bir(i):
    out = f"{T}/bi/{i:04d}.png"
    if os.path.exists(out): return
    im = Image.open(f"{T}/src/{i:04d}.png").convert("RGB"); sm = im.resize((1152, 2048), Image.LANCZOS)
    buf = io.BytesIO(); sm.save(buf, "JPEG", quality=94)
    for k in range(3):
        try:
            url = RB.upload(tok, buf.getvalue(), f"f{i}.jpg"); png = urllib.request.urlopen(RB.predict(tok, ver, url)).read(); break
        except Exception as e:
            if k == 2: raise
    a = Image.open(io.BytesIO(png)).split()[-1].resize(im.size, Image.LANCZOS); a.save(out)
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(bir, NEED))
print("birefnet frames", len(NEED), flush=True)
# 3. Apple Vision mask (local)
todo = [f"{T}/src/{i:04d}.png" for i in NEED if not os.path.exists(f"{T}/vi/{i:04d}.mask.png")]
for k in range(0, len(todo), 60):
    subprocess.run([f"{P}/.claude/skills/shorts/reference/recentre/personmask", f"{T}/vi"] + todo[k:k+60], check=True, capture_output=True)
print("vision frames done", flush=True)
def alpha(kind, i):
    if kind == "vi":
        return np.asarray(Image.open(f"{T}/vi/{i:04d}.mask.png").convert("L").resize((2160, 3840), Image.BILINEAR), np.float32) / 255
    a = np.asarray(Image.open(f"{T}/bi/{i:04d}.png"), np.float32) / 255
    if kind == "bim":                                   # 3-frame temporal median, inside the same layout run only
        run = WIDE if i in WIDE else CORNER
        nb = [j for j in (i - 1, i + 1) if j in run]
        if len(nb) == 2: a = np.median(np.stack([a] + [np.asarray(Image.open(f"{T}/bi/{j:04d}.png"), np.float32) / 255 for j in nb]), 0)
    return a
# 4. composite
FONT = "/Volumes/Expansion/_edit_work/RO-37/round1/assets/Poppins-Bold.ttf"
def card(img):
    d = ImageDraw.Draw(img, "RGBA"); d.rounded_rectangle([96, 210, 860, 690], 30, fill=(22, 51, 81, 215), outline=(104, 197, 255, 180), width=2)
    f1, f2 = ImageFont.truetype(FONT, 54), ImageFont.truetype(FONT, 40)
    d.text((140, 250), "Bad Day?", font=f1, fill=(244, 250, 255)); d.line([140, 330, 320, 330], fill=(104, 197, 255), width=4)
    for k, s in enumerate(["Do 5 Minutes", "Do 10 Minutes", "Never Zero"]): d.text((140, 380 + k * 90), f"{k+1}.  {s}", font=f2, fill=(232, 242, 252))
def place(base, rgb, a, s, x_c, top, shadow=True):
    h, w = round(3840 * s), round(2160 * s)
    fg = Image.fromarray(rgb).resize((w, h), Image.LANCZOS); al = Image.fromarray((a * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
    hair = int(np.argmax(np.asarray(al).max(1) > 128)); y = top - hair; x = x_c - w // 2
    if shadow:
        sh = Image.new("L", base.size, 0); sh.paste(al.filter(ImageFilter.GaussianBlur(18)), (x + 10, y + 14)); dark = Image.new("RGB", base.size, (2, 8, 18))
        base.paste(dark, (0, 0), sh.point(lambda v: int(v * 0.55)))
    base.paste(fg, (x, y), al); return base
gtune = json.load(open("/Volumes/Expansion/_edit_work/RO-37/round1/broll/grade.json"))["B0621@3.0"]["vf"]
CLIP = f"{T}/clip_B0621.mp4"
if not os.path.exists(CLIP):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", "3.0", "-t", "7.5", "-i", __import__("broll_tune").path("B0621"),
                    "-vf", f"{F.DEC},{gtune},scale=1920:1080,format=rgb24", "-f", "rawvideo", f"{T}/clip.rgb"], check=True)
    os.rename(f"{T}/clip.rgb", CLIP)
clipraw = np.fromfile(CLIP, np.uint8).reshape(-1, 1080, 1920, 3)
def render(kind):
    out = f"{T}/test-{kind}.mp4"
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", "30000/1001", "-i", "-",
                          "-ss", str(S0), "-t", str(DUR), "-i", f"/Volumes/Expansion/_edit_work/RO-37/round1/lav_C1895.wav",
                          "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p",
                          "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-15", out], stdin=subprocess.PIPE)
    for i in range(N):
        rgb = np.asarray(Image.open(f"{T}/src/{i:04d}.png").convert("RGB"))
        if i in WIDE:
            base = SB.field(i / FPS, 1920, 1080).convert("RGB"); card(base)
            img = place(base, rgb, alpha(kind, i), 0.394, 1400, 44)
        elif i in CORNER:
            base = Image.fromarray(clipraw[min(i - CORNER[0], len(clipraw) - 1)])
            img = place(base, rgb, alpha(kind, i), 0.20, 1640, 560)
        else:
            y = F.t_y("C1895", S0, S0 + DUR); img = Image.fromarray(rgb[y:y + 1215]).resize((1920, 1080), Image.LANCZOS)
        p.stdin.write(img.tobytes())
    p.stdin.close(); p.wait()
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "21", "-c:a", "copy", "-movflags", "+faststart", out[:-4] + " - REVIEW 540p.mp4"], check=True)
    print("rendered", kind, flush=True)
for k in ("bi", "bim", "vi"): render(k)
print("CUTOUT_TEST_DONE")
