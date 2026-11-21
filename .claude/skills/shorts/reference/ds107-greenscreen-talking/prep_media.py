"""DS-107 R1 media caches (decoded once, explicit BT.709 TV range -> RGB, rgb24 memmaps at each clip's NATIVE frame rate: the
assembly plays one native frame per film frame (DS-41: an fps filter doubled every fifth frame of a 24 fps clip and juddered), so
24/25 fps clips run 1.25x/1.2x for their 1-4 s.
Picture area under the title band: 1080 x 1610. Two 16:9 AI scenes need two people in shot, so they are square cards 1080 x 1080
at the top of the picture area (VIDEO-RULES 2026-10-01: fill, else square, else the whole clip; the reason is written here):
  A0063  stressed dad in a kitchen with two kids pulling at him (AI)   square x 420-1140 of 1280x720: dad and both kids
  A0072  family dinner, dad eating beside his wife (AI)                square x 840-1920 of 1920x1080: dad and his wife
Fill (window -> 1080 x 1610):
  A0182  man on the couch at night, snacking (AI)                      window 724x1080 at x 634
  A0242  man takes a drive-thru bag in his car (AI, 9:16)              rows 310-1920 (the car roof above goes)
  B0559  man lying awake in bed (stock, 2160x4096)                     2160x3219 at y 600
  B0042  chicken, rice and broccoli bowl (stock, 1440x2560)            1440x2147 at y 150
  B0448  Dan's jump rope, the correct boxer skip (real), the opener   window 724x1080 at x 560, his approved RO-28 grade (JR_B0448)
  B0542  the same skip, second cut (real; roll 101.8-105.9, no overlap with B0448 0.5-5.3 s)   window 724x1080 at x 598, same grade
Photos (real, 1080 x 1610): the standard deck-chair before picture (memory standard-before-picture), photo-251 from the 7-31 pool
shoot (the 'today' picture RO-31 used beside the same before)."""
import subprocess, numpy as np, sys
from pathlib import Path
from PIL import Image
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); F = str(R/'Media/video_edit/bin/ffmpeg')
LIB = '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library'
DEC = 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc'
JR = ("scale=in_color_matrix=bt709:in_range=tv,format=gbrp,curves=master='0/0 0.15/0.12 0.5/0.41 0.85/0.78 1/1',colorchannelmixer=rr=1.1181:rg=-0.1073:rb=-0.0108:"
      "gr=-0.0319:gg=1.0427:gb=-0.0108:br=-0.0319:bg=-0.1073:bb=1.1392,colorbalance=rm=-.01:gm=.02:bm=.05")
def dump(name, src, vf, wh, ss, t):
    out = W/f'src/{name}.npy'
    if out.exists() and '--force' not in sys.argv: print('have', out); return
    p = subprocess.Popen([F, '-nostdin', '-v', 'error', '-ss', str(ss), '-i', src, '-t', str(t), '-an', '-vf', vf + ',format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    fb = wh[0]*wh[1]*3; frames = []
    while True:
        b = p.stdout.read(fb)
        if len(b) < fb: break
        frames.append(np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], 3))
    p.wait(); a = np.stack(frames)
    mm = np.lib.format.open_memmap(out, 'w+', np.uint8, a.shape); mm[:] = a; mm.flush(); print(out, a.shape)
S = lambda x: x + ':flags=lanczos'
# (name, file, crop, out size, start s, seconds) -- start = the shot's src_t0 (framing.py), seconds = film length x speed + margin
dump('A0063', LIB + '/04 AI-Generated Clips/lifestyle/A0063_stressed-overweight-dad-kitchen-kids_16x9_6s.mp4', 'crop=720:720:420:0,' + DEC + S(',scale=1080:1080'), (1080, 1080), 0.0, 6.0)
dump('A0072', LIB + '/04 AI-Generated Clips/lifestyle/A0072_family-dinner-and-cooking-montage_16x9_10s.mp4', 'decimate=cycle=6,crop=1080:1080:840:0,' + DEC, (1080, 1080), 0.0, 4.0)   # R1 review: 25 fps content in a 29.97 file repeats every sixth frame; decimate keeps the 25 unique frames a second
dump('A0182', LIB + '/04 AI-Generated Clips/food-nutrition/A0182_man-couch-snacking-trail-mix-night_16x9_5s.mp4', 'crop=724:1080:634:0,' + DEC + S(',scale=1080:1610'), (1080, 1610), 0.0, 5.3)
dump('A0242', LIB + '/04 AI-Generated Clips/lifestyle/A0242_drive-thru-bag-guilty-glance_9x16_4s.mp4', 'crop=1080:1610:0:310,' + DEC, (1080, 1610), 0.0, 3.6)
dump('B0559', LIB + '/03 B-Roll - Real Footage/stock/other/B0559_man-awake-in-bed-at-night_2160x4096_54s.mp4', 'crop=2160:3219:0:600,' + DEC + S(',scale=1080:1610') + ",curves=master='0/0 0.06/0.13 0.25/0.40 0.6/0.78 1/1'", (1080, 1610), 39.0, 4.0)   # R1 review: median luma 20 and a face hidden by forearms; from 39 s his eyes are open, midtones lifted (night look kept)
dump('B0042', LIB + '/03 B-Roll - Real Footage/stock/food-nutrition/B0042_chicken-rice-broccoli-bowl-close-up_9x16_9s.mp4', 'crop=1440:2147:0:150,' + DEC + S(',scale=1080:1610'), (1080, 1610), 0.0, 8.7)
dump('B0542', LIB + '/03 B-Roll - Real Footage/dan-filmed/B0542_dan-jump-rope-fast-boxer-skip-poolside-second-cut_16x9_4s.mp4', 'crop=724:1080:598:0,' + JR + S(',scale=1080:1610'), (1080, 1610), 0.0, 4.2)
dump('B0448', LIB + '/03 B-Roll - Real Footage/dan-filmed/B0448_dan-jump-rope-high-knees-poolside_16x9_8s.mp4', 'crop=724:1080:560:0,' + JR + S(',scale=1080:1610'), (1080, 1610), 0.0, 8.0)
for name, path, box in [('before', R/'before-photo-candidates/B_deckchair_UPSCALED_3x_1080x1440.jpg', None), ('today', R/'photos/finalized social media photos/photo-251_FINAL_PRIMARY.jpg', None)]:
    out = W/f'src/{name}.npy'
    if out.exists() and '--force' not in sys.argv: continue
    im = Image.open(path).convert('RGB'); k = max(1080/im.width, 1610/im.height); im = im.resize((round(im.width*k), round(im.height*k)), Image.LANCZOS)
    x0 = (im.width - 1080)//2; y0 = 0 if name == 'today' else (im.height - 1610)//2
    np.save(out, np.asarray(im.crop((x0, y0, x0 + 1080, y0 + 1610)))[None]); im.crop((x0, y0, x0 + 1080, y0 + 1610)).save(W/f'src/{name}.jpg', quality=92); print(out)
for p in sorted((W/'src').glob('*.npy')):
    a = np.load(p, mmap_mode='r'); print(p.name, a.shape)
