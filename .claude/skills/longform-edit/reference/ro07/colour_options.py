"""RO-07 round 1b: the colour options MOVING (Dan rejected the first minute's colour, option C). The same 16 s of the cut
(camera frame, then the punch-in, lower third included) in each option: one clip per option, a 2x2 grid that plays all four
at once, and one back-to-back file for VLC. Picture only."""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro07/recipe")
import frames as F, build as Bd
from PIL import Image, ImageDraw, ImageFont
W = "/Volumes/Extreme/_edit_work/ro07"; O = f"{W}/round1b/colour"; os.makedirs(O, exist_ok=True); FF = Bd.FF
A0, A1 = 5.41, 21.29
NAMES = {"C": "C: what you saw in the first minute", "B": "B: brighter", "D": "D: bright and natural", "E": "E: bright, more contrast"}
font = ImageFont.truetype(os.path.expanduser("~/Library/Fonts/Manrope.ttf"), 44) if os.path.exists(os.path.expanduser("~/Library/Fonts/Manrope.ttf")) else ImageFont.load_default()
for k, name in NAMES.items():
    out = f"{O}/{k}.mp4"
    if not os.path.exists(out):
        F.LOOK = k; Bd._SEGS = None; Bd.render_range(A0, A1, out, audio=False)
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(im); w = d.textlength(name, font=font)
    d.rounded_rectangle((40, 36, 40 + w + 48, 36 + 76), 16, fill=(8, 14, 24, 215)); d.text((64, 46), name, font=font, fill=(255, 255, 255, 255)); im.save(f"{O}/{k}.label.png")
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", out, "-i", f"{O}/{k}.label.png", "-filter_complex", "[0][1]overlay=0:0,format=yuv420p", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", f"{O}/option-{k}.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", f"{O}/option-{k}.mp4", "-vf", "scale=1280:720", "-c:v", "libx264", "-crf", "21", "-movflags", "+faststart", f"{O}/option-{k} - REVIEW 720p.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", "11", "-i", f"{O}/option-{k}.mp4", "-frames:v", "1", "-vf", "scale=960:540", "-q:v", "3", f"{O}/option-{k}.jpg"], check=True)
    print("option", k, flush=True)
ins = sum([["-i", f"{O}/option-{k}.mp4"] for k in "CBDE"], [])
subprocess.run([FF, "-nostdin", "-v", "error", "-y"] + ins + ["-filter_complex", "[0]scale=960:540[a];[1]scale=960:540[b];[2]scale=960:540[c];[3]scale=960:540[d];[a][b]hstack[x];[c][d]hstack[y];[x][y]vstack,format=yuv420p",
                "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", f"{O}/grid-all-four.mp4"], check=True)
open(f"{O}/cat.txt", "w").write("".join(f"file '{O}/option-{k}.mp4'\n" for k in "CBDE"))
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{O}/cat.txt", "-c", "copy", "-movflags", "+faststart", f"{O}/all-four-back-to-back.mp4"], check=True)
print("COLOUR OPTIONS DONE", flush=True)
