"""DS-40 R2 review page: R1 vs R2 green screen key on the same 9.3 s sample (colour B, voice E locked).
Everything shown is cut from the RENDERED files. Writes r2/review/index.html."""
from pathlib import Path
import json, subprocess, html, shutil
import numpy as np
from PIL import Image
W = Path('/Volumes/Extreme/_edit_work/ds40/r2'); Q = W/'review'; M = Q/'media'; R1 = W.parent/'r1'
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
NAME = 'Fat 90 Year Old SFC R2'
E = html.escape
M.mkdir(parents=True, exist_ok=True)
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
def frames(path, f0, n):
    p = subprocess.run([F, '-v', 'error', '-i', str(path), '-vf', f"select=between(n\\,{f0}\\,{f0 + n - 1}),scale=in_color_matrix=bt709:in_range=tv",
                        '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(p, np.uint8).reshape(-1, 1920, 1080, 3); assert len(a) == n, (path, f0, len(a)); return a

FILES = {
    'r1': {'navy': R1/'review/DS40 R1 sample - Warm Vivid colour, house voice.mp4', 'pale': R1/'review/colour/key check on pale backdrop.mp4', 'pink': W/'renders/r1 pink.mp4'},
    'r2': {'navy': W/'renders/r2 navy.mp4', 'pale': W/'renders/r2 pale.mp4', 'pink': W/'renders/r2 pink.mp4'},
}
SAMPLE = f'{NAME} - sample, Warm Vivid colour, house voice plus half bass.mp4'
shutil.copy(FILES['r2']['navy'], M/SAMPLE)
# side by side, R1 left, R2 right, R2 audio (voice E)
for bg in ['navy', 'pale', 'pink']:
    ff(['-i', FILES['r1'][bg], '-i', FILES['r2'][bg], '-filter_complex',
        '[0:v]scale=720:1280:flags=area[a];[1:v]scale=720:1280:flags=area[b];[a][b]hstack=2,format=yuv420p[v]',
        '-map', '[v]'] + (['-map', '1:a', '-c:a', 'aac', '-b:a', '192k'] if bg == 'navy' else ['-an']) +
       ['-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', M/f'R1 vs R2 - {bg}.mp4'])
# looping close-ups: 5 consecutive frames, R1 | R2, exact delivered pixels, nearest-neighbour zoom, 5 frames a second,
# played forward then back so the loop has no jump
LOOPS = [
    ('hair', 'pale', 100, (380, 470, 620, 630), 3, 'Hairline and curls, 0:03.34 to 0:03.47'),
    ('ear', 'pale', 60, (250, 780, 430, 940), 3, 'Ear and side of the face, 0:02.00 to 0:02.14'),
    ('shoulder', 'pale', 200, (60, 1080, 240, 1240), 3, 'Left shoulder and arm edge, 0:06.67 to 0:06.81'),
    ('hand', 'pale', 142, (0, 1620, 340, 1880), 2, 'Fastest hand movement (motion blur) and the old speck spot, 0:04.74 to 0:04.87'),
    ('watch', 'pink', 250, (885, 1745, 1005, 1865), 3, 'Watch glass seen edge-on, 0:08.34 to 0:08.47, over saturated pink'),
    ('watch0', 'pink', 0, (790, 1830, 890, 1920), 3, 'Watch glass at the very start, 0:00.00 to 0:00.13, over saturated pink'),
    ('watch236', 'pink', 234, (945, 1740, 1065, 1860), 3, 'Watch case edge, 0:07.81 to 0:07.94, over saturated pink'),
]
loop_html = []
for nm, bg, f0, (x0, y0, x1, y1), z, cap in LOOPS:
    a = frames(FILES['r1'][bg], f0, 5)[:, y0:y1, x0:x1]; b = frames(FILES['r2'][bg], f0, 5)[:, y0:y1, x0:x1]
    gap = np.full((5, y1 - y0, 4, 3), 255, np.uint8)
    seq = np.concatenate([a, gap, b], 2)
    seq = np.concatenate([seq, seq[-2:0:-1]], 0)        # ping-pong
    d = Q/'tmp_loop'; shutil.rmtree(d, ignore_errors=True); d.mkdir()
    for k, fr in enumerate(np.tile(seq, (4, 1, 1, 1))):
        im = Image.fromarray(fr); im.resize((im.width * z // 2 * 2, im.height * z // 2 * 2), Image.Resampling.NEAREST).save(d/f'{k:03d}.png')
    ff(['-framerate', 5, '-i', d/'%03d.png', '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', M/f'loop-{nm}.mp4'])
    shutil.rmtree(d)
    loop_html.append(f"<div class='edge'><h4>{E(cap)}</h4><video src='media/loop-{nm}.mp4' autoplay muted loop playsinline></video>"
                     f"<small>Left R1, right R2. Five consecutive frames, shown {z}x, played slowly forward and back.</small></div>")

def j(p): return json.load(open(W/'measure'/p))['summary']
m1, m2 = j('r1_metrics.json'), j('m_r2.json'); c1, c2 = j('mc_r1.json'), j('mc_r2.json')
true_see = lambda s: [f for f in s['seethru_frames'] if f <= 12 or f == 236 or 250 <= f <= 254]
notes = json.load(open(W/'notes_r2.json'))
rows = [
    ('Hair flicker, with Dan\'s movement taken out (camera\'s own grain = 1.00; lower is steadier)', f"{c1['mc_hair_ratio']:.2f}", f"{c2['mc_hair_ratio']:.2f}"),
    ('All edges flicker, with movement taken out (camera = 1.00)', f"{c1['mc_ratio']:.2f}", f"{c2['mc_ratio']:.2f}"),
    ('R1 reviewer\'s edge number (movement included, camera = 1.00)', f"{m1['flicker_ratio_mean']:.3f}", f"{m2['flicker_ratio_mean']:.3f}"),
    ('Dark outline on skin edges over a pale background (camera picture itself: 8%)', f"{m1['rim_fraction']*100:.1f}%", f"{m2['rim_fraction']*100:.1f}%"),
    ('Watch glass see-through, frames (0:00.0-0:00.4, 0:07.87, 0:08.34-0:08.44)', notes['watch_r1'], notes['watch_r2']),
    ('Floating specks, whole sample', f"{m1['speck_total']}", f"{m2['speck_total']}"),
]
table = ''.join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td class='win'>{E(c)}</td></tr>" for a, b, c in rows)
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
reply = '\n'.join(f'{i+1}. ' for i in range(len(notes['questions'])))
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(NAME)}</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1100px;padding:16px 16px 80px;margin-right:420px}}@media(max-width:1100px){{main{{margin-right:0}}#side{{position:static!important;width:auto!important}}}}
h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
#side{{position:fixed;right:16px;top:16px;width:380px}}#side video{{width:100%;background:#000;border-radius:8px;max-height:72vh}}
.edge{{background:var(--card);border-radius:8px;padding:10px;margin:12px 0}}.edge video,.sbs video{{width:100%;border-radius:4px;display:block;background:#000}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #2a3644;padding:6px;text-align:left;vertical-align:top}}td.win{{color:var(--rec);font-weight:600}}
button{{margin:6px 6px 6px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
textarea{{width:100%;height:110px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}small{{color:var(--mut)}}</style></head><body>
<aside id="side"><video id="film" controls playsinline preload="metadata" src="media/{E(SAMPLE)}"></video>
<p id="now" class="badge">Playing: the R2 sample (colour B, house voice plus half bass)</p>
<button onclick="ctx('media/{E(SAMPLE)}','the R2 sample')">R2 sample</button>
<button onclick="ctx('media/R1 vs R2 - navy.mp4','R1 left, R2 right, on the blue field')">R1 vs R2, blue</button>
<button onclick="ctx('media/R1 vs R2 - pale.mp4','R1 left, R2 right, pale key check')">R1 vs R2, pale</button>
<button onclick="ctx('media/R1 vs R2 - pink.mp4','R1 left, R2 right, pink key check')">R1 vs R2, pink</button></aside>
<main><p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 · DS-40 · green screen key polish</p>
<h1>Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right.</h1>
<p>{E(notes['intro'])}</p>
<h2>Your decision ({len(notes['questions'])})</h2><ol>{li(notes['questions'])}</ol>
<h2>What changed, measured on every frame</h2>
<table><tr><th></th><th>R1</th><th>R2</th></tr>{table}</table><p><small>{E(notes['numbers_note'])}</small></p>
<h2>R1 and R2 side by side</h2><p>{E(notes['sbs_desc'])}</p>
<div class="sbs edge"><h4>On the blue field, with sound (R2's voice)</h4><video controls playsinline preload="metadata" src="media/R1 vs R2 - navy.mp4"></video></div>
<div class="sbs edge"><h4>Pale key check (shows any grey outline)</h4><video controls playsinline muted preload="metadata" src="media/R1 vs R2 - pale.mp4"></video></div>
<div class="sbs edge"><h4>Saturated pink key check (shows anything see-through)</h4><video controls playsinline muted preload="metadata" src="media/R1 vs R2 - pink.mp4"></video></div>
<h2>Close-ups that loop</h2><p>{E(notes['loops_desc'])}</p>{''.join(loop_html)}
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src,label){{const v=document.getElementById('film');v.src=src;v.play();document.getElementById('now').textContent='Playing: '+(label||src);}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE written', Q/'index.html')
