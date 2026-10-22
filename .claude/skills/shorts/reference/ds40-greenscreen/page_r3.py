"""DS-40 R3 review page: the opening (clip full screen, Dan small in the corner, then large). Writes r3/review/index.html."""
from pathlib import Path
import json, subprocess, html, shutil
import numpy as np
from PIL import Image
W = Path('/Volumes/Expansion/_edit_work/ds40/r3'); Q = W/'review'; M = Q/'media'
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
NAME = 'Fat 90 Year Old SFC R3'
E = html.escape
M.mkdir(parents=True, exist_ok=True)
OPEN = f'{NAME} - opening.mp4'; PINK = f'{NAME} - opening, pink key check.mp4'
shutil.copy(W/'renders/DS40 R3 opening.mp4', M/OPEN); shutil.copy(W/'renders/DS40 R3 opening pink.mp4', M/PINK)
# stills from the delivered file
STILLS = [(0.5, 'Opens on the clip, full screen; you small in the corner'), (10.0, 'Mid-clip: your live reaction'),
          (19.3, 'Last frame of the clip'), (19.55, 'The move: the clip shrinks, you grow'), (20.0, 'Settled: you full size'),
          (24.0, 'Speaking: "Bill Maher is right..."')]
p = subprocess.run([F, '-v', 'error', '-i', str(M/OPEN), '-vf', 'scale=in_color_matrix=bt709:in_range=tv', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                   capture_output=True, check=True).stdout
fr = np.frombuffer(p, np.uint8).reshape(-1, 1920, 1080, 3)
cells = []
for i, (t, cap) in enumerate(STILLS):
    k = min(len(fr) - 1, int(round(t * 30000 / 1001)))
    Image.fromarray(fr[k]).resize((360, 640), Image.Resampling.LANCZOS).save(M/f'still{i}.jpg', quality=90)
    cells.append(f"<figure><img src='media/still{i}.jpg'><figcaption>0:{t:05.2f} · {E(cap)}</figcaption></figure>")
notes = json.load(open(W/'notes_r3.json'))
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
reply = '\n'.join(f'{i+1}. ' for i in range(len(notes['questions'])))
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(NAME)}</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1100px;padding:16px 16px 80px;margin-right:420px}}@media(max-width:1100px){{main{{margin-right:0}}#side{{position:static!important;width:auto!important}}}}
h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
#side{{position:fixed;right:16px;top:16px;width:380px}}#side video{{width:100%;background:#000;border-radius:8px;max-height:72vh}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}.three img{{width:100%;border-radius:6px;display:block}}figure{{margin:0}}figcaption{{color:var(--mut);font-size:13px}}
button{{margin:6px 6px 6px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
textarea{{width:100%;height:110px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}small{{color:var(--mut)}}</style></head><body>
<aside id="side"><video id="film" controls playsinline preload="metadata" src="media/{E(OPEN)}"></video>
<p id="now" class="badge">Playing: the opening ({E(notes['duration'])})</p>
<button onclick="ctx('media/{E(OPEN)}','the opening')">The opening</button>
<button onclick="ctx('media/{E(PINK)}','pink key check')">Key check on pink</button></aside>
<main><p class="badge">CONTENT · Dedicated Short (SFC) · Round 3 · DS-40 · the opening</p>
<h1>Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right.</h1>
<p>{E(notes['intro'])}</p>
<h2>Your decisions ({len(notes['questions'])})</h2><ol>{li(notes['questions'])}</ol>
<h2>The opening, frame by frame</h2><div class="three">{''.join(cells)}</div>
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src,label){{const v=document.getElementById('film');v.src=src;v.play();document.getElementById('now').textContent='Playing: '+(label||src);}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE written', Q/'index.html')
