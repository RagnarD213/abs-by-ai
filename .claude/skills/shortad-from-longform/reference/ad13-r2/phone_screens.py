"""Ad 13 round 3: the two phone lifts from Muhammad's master carried his bezel and his grid (a phone inside our phone
card, judge + reviewer 2026-10-02). Crop each to the SCREEN only and paint the rounded screen corners with the
screen's own background, so our media card is the only device."""
import subprocess, numpy as np
from PIL import Image, ImageDraw
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
B = "/Volumes/Extreme/_edit_work/kit9x16/av11-ad13/"
GEO = {"phone_04453": ("assets_sbl", 38, 38, 444, 926), "phone_05640": ("assets_sbl", 36, 36, 414, 860),
       "auto_06914": ("assets_auto", 27, 10, 457, 947), "auto_06945": ("assets_auto", 27, 10, 457, 947)}
for name in GEO:
    src = B + f"{GEO[name][0]}/{name}.mp4"
    fr = B + f"round3/chk/{name}_mid.png"
    subprocess.run([FF, "-v", "error", "-y", "-ss", "0.5", "-i", src, "-frames:v", "1", fr], check=True)
    # the screen's inner edge, measured on the bezel (dark band 21-33 px in, then the white screen): fixed per lift
    x0, y0, x1, y1 = GEO[name][1:]
    cw, ch = (x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2
    rgb = np.asarray(Image.open(fr).convert("RGB"))
    bg = tuple(int(v) for v in np.median(rgb[y1 - 40:y1 - 20, x0 + 6:x0 + 16].reshape(-1, 3), 0))
    r = int(round(0.12 * cw))
    m = Image.new("L", (cw, ch), 255); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=r, fill=0)
    mask = B + f"round3/chk/{name}_cornermask.png"
    Image.merge("RGBA", [Image.new("L", (cw, ch), c) for c in bg] + [m]).save(mask)
    out = B + f"assets_sbl/{name}_screen.mp4"
    subprocess.run([FF, "-v", "error", "-y", "-i", src, "-i", mask, "-filter_complex",
                    f"[0:v]crop={cw}:{ch}:{x0}:{y0}[s];[s][1:v]overlay=0:0", "-r", "30000/1001", "-c:v", "libx264", "-crf", "14",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
                    "-color_trc", "bt709", "-an", out], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", "0.5", "-i", out, "-frames:v", "1", B + f"round3/chk/{name}_screen.png"], check=True)
    print(name, "screen", (x0, y0, cw, ch), "bg", bg, "corner r", r)
