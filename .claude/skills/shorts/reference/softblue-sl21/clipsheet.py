"""clipsheet.py: one contact sheet per Short of every cutaway's used range: 6 whole frames per clip with the 9:16 fill window drawn at fx 0.5."""
import subprocess, sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, "recipe"); import lib
CL = "clips/"
ROWS = {"A": [("Cd08", 0, 8), ("Cd09", 0, 4.6), ("Cd10", 0, 7.4), ("Cd11a", 0, 3.4), ("Cd11b", 0, 3.4), ("Cd13", 0, 3.4)],
        "D": [("Cd18", 0, 6), ("Cd19a", 1.0, 4.3), ("Cd19b", 0, 3.3), ("Cd20", 0.5, 4.4), ("Cd21", 2.0, 5.6), ("Cd23", 0, 5)],
        "E": [("Cd24", 0, 5.6), ("Cd25", 1.0, 5.0), ("Cd26", 0, 3.6), ("B0642", 0, 8.5), ("B0642", 8.5, 17)]}
for S, rows in ROWS.items():
    sheet = Image.new("RGB", (6 * 320, len(rows) * 180))
    for r, (cid, a, b) in enumerate(rows):
        for k in range(6):
            t = a + (b - a) * k / 5
            raw = subprocess.run([lib.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", CL + cid + ".mp4", "-frames:v", "1", "-vf", "scale=320:180:in_color_matrix=bt709,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
            if len(raw) < 320 * 180 * 3: continue
            im = Image.frombytes("RGB", (320, 180), raw); d = ImageDraw.Draw(im); ww = 180 * 1080 / 1610
            d.rectangle((160 - ww / 2, 0, 160 + ww / 2, 179), outline=(255, 255, 0)); d.rectangle((0, 0, 110, 12), fill=(0, 0, 0)); d.text((2, 0), f"{cid} {t:.1f}s", fill=(255, 255, 0))
            sheet.paste(im, (k * 320, r * 180))
    sheet.save(f"sheets/clips_{S}.jpg", quality=85); print(S, "ok")
