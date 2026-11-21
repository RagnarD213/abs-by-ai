"""One still per background segment (its middle frame, or --at film seconds), through the real assembler code path, then a
contact sheet. Cheap: one plate frame per still.   stills_r4.py OUTDIR [--only BG01,BG03] [--at 10.5,60.2]"""
import json, subprocess, sys, pathlib
from PIL import Image, ImageDraw
R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round4'); FPS = 30000 / 1001
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
plan = json.load(open(R3 / 'bg_plan.json'))['segments']
if '--at' in sys.argv:
    frames = [(f'at{t}', int(round(float(t) * FPS))) for t in sys.argv[sys.argv.index('--at') + 1].split(',')]
else:
    frames = [(s['id'], int(round((s['t0'] + s['t1']) / 2 * FPS))) for s in plan if (not only or s['id'] in only)]
tiles = []
for name, f in frames:
    o = out / f'{name}.mp4'
    r = subprocess.run(['python3', str(R3 / 'recipe/assemble_r4.py'), str(o), '--g0', str(f), '--g1', str(f + 1), '--stills', str(f)], capture_output=True, text=True)
    jpg = out / f'{name}-{f:05d}.jpg'
    if not jpg.exists(): print(name, 'FAILED', r.stderr[-800:]); continue
    tiles.append((name, jpg)); print(name, f, 'ok', flush=True)
W = Image.new('RGB', (1920, 360 * ((len(tiles) + 2) // 3)), (0, 0, 0))
for i, (n, j) in enumerate(tiles):
    im = Image.open(j).resize((640, 360)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 120, 26), fill=(0, 0, 0)); d.text((6, 6), n, fill=(255, 255, 0))
    W.paste(im, ((i % 3) * 640, (i // 3) * 360))
W.save(out / 'sheet.jpg', quality=90); print('SHEET', out / 'sheet.jpg')
