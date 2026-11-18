"""frames f0-1 | f0 at every picture cut of the exact draft (native frames, scaled to 180x320), one sheet per Short."""
import json, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, "recipe"); import plans as P, batch as Bt
for S in sys.argv[1:]:
    d = Bt.D(S); V = f"{d}/{P.NAME[S]}.mp4"; sh = json.load(open(f"{d}/shots.json"))
    cuts = [x["f0"] for x in sh[1:]]; want = sorted(set(n for c in cuts for n in (c - 1, c)))
    sel = "+".join(f"eq(n\\,{n})" for n in want)
    raw = subprocess.run([Bt.lib.FF, "-v", "error", "-i", V, "-vf", f"select='{sel}',scale=180:320,format=rgb24", "-vsync", "0", "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = {n: Image.frombytes("RGB", (180, 320), raw[k * 180 * 320 * 3:(k + 1) * 180 * 320 * 3]) for k, n in enumerate(want)}
    cols = 6; rows = (len(cuts) + cols - 1) // cols; s = Image.new("RGB", (cols * 370, rows * 330), (30, 30, 30))
    for k, c in enumerate(cuts):
        x, y = (k % cols) * 370, (k // cols) * 330; s.paste(fr[c - 1], (x, y)); s.paste(fr[c], (x + 182, y))
        ImageDraw.Draw(s).text((x + 2, y + 2), f"{c / Bt.FPS:.2f}", fill=(255, 255, 0))
    s.save(f"{d}/joins_sheet.jpg", quality=85); print(S, len(cuts), "cuts")
