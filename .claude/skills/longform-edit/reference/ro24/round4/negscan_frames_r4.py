"""RO-24 R4: grab the negative-events scan frames (every 10 s + the middle of every full-screen / AI item) and tile them
into labelled contact sheets for a human/Claude look. Writes round4/final/negscan/frames.json and sheet_XX.jpg."""
import json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
R4 = '/Volumes/Expansion/_edit_work/RO-24/round4'; OUT = f'{R4}/final/negscan'; V = f'{R4}/final/RO24_R4_MASTER.mp4'
FF = '/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
FPS = 30000 / 1001; N = json.load(open(f'{R4}/final/RO24_R4_MASTER.mp4.build.json'))['frames']; DUR = N / FPS
M = json.load(open(f'{R4}/film_manifest_r4.json'))
pts = [(float(t), f'{t//60:.0f}:{t%60:04.1f}') for t in range(0, int(DUR), 10)]
for m in M:
    if m['kind'] == 'opaque':
        t = (m['a'] + m['b']) / 2; pts.append((t, f"{m['id']} {t//60:.0f}:{t%60:04.1f}"))
B1a = [m for m in M if m['id'] == 'B1'][0]['a']
pts.append((B1a + 2.4024 + 1.4, 'B1-salmon(AI) %d:%04.1f' % ((B1a + 3.8) // 60, (B1a + 3.8) % 60)))
pts.sort()
os.makedirs(OUT, exist_ok=True)
rec = []
for k, (t, lab) in enumerate(pts):
    p = f'{OUT}/f{k:03d}.jpg'
    subprocess.run([FF, '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', V, '-frames:v', '1', '-vf', 'scale=640:360', '-q:v', '3', p], check=True)
    rec.append(dict(t=round(t, 3), label=lab, path=p))
json.dump(rec, open(f'{OUT}/frames.json', 'w'), indent=1)
try: font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 26)
except Exception: font = ImageFont.load_default()
per = 9
for s in range(0, len(rec), per):
    sheet = Image.new('RGB', (3 * 640, 3 * 360), 'black'); d = ImageDraw.Draw(sheet)
    for j, r in enumerate(rec[s:s + per]):
        x, y = (j % 3) * 640, (j // 3) * 360
        sheet.paste(Image.open(r['path']), (x, y)); d.rectangle([x, y, x + 330, y + 34], fill='black'); d.text((x + 6, y + 4), r['label'], fill='yellow', font=font)
    sheet.save(f'{OUT}/sheet_{s // per:02d}.jpg', quality=85)
print(len(rec), 'frames,', (len(rec) + per - 1) // per, 'sheets')
