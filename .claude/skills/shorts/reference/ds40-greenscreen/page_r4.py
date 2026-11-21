"""DS-40 R4 review page: the intro clip, version A (box upper left) and B (lower left, larger, laptop)."""
from pathlib import Path
import json, subprocess, html, shutil
import numpy as np
from PIL import Image
W = Path('/Volumes/Expansion/_edit_work/ds40/r4'); Q = W/'review'; M = Q/'media'
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
NAME = 'Fat 90 Year Old SFC R4'
E = html.escape
M.mkdir(parents=True, exist_ok=True)
FILES = {v: f'{NAME} - intro {v}.mp4' for v in 'AB'}
for v in 'AB':
    shutil.copy(W/f'renders/DS40 R4 intro {v}.mp4', M/FILES[v])
    shutil.copy(W/f'renders/DS40 R4 intro {v} pink.mp4', M/f'{NAME} - intro {v} pink key check.mp4')
TIMES = [1.0, 4.0, 11.5, 18.8]
sel = '+'.join(f"eq(n\\,{int(round(t * 30000 / 1001))})" for t in TIMES)
for v in 'AB':
    p = subprocess.run([F, '-v', 'error', '-i', str(M/FILES[v]), '-vf', f'select={sel},scale=in_color_matrix=bt709:in_range=tv',
                        '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    for i, fr in enumerate(np.frombuffer(p, np.uint8).reshape(-1, 1920, 1080, 3)):
        Image.fromarray(fr).resize((360, 640), Image.Resampling.LANCZOS).save(M/f'{v}{i}.jpg', quality=90)
notes = json.load(open(W/'notes_r4.json'))
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
reply = '\n'.join(f'{i+1}. ' for i in range(len(notes['questions'])))
stills = ''.join(f"<div><h4>{E(notes['label'][v])}</h4><div class='four'>" +
                 ''.join(f"<figure><img src='media/{v}{i}.jpg'><figcaption>0:{t:04.1f}</figcaption></figure>" for i, t in enumerate(TIMES)) +
                 "</div></div>" for v in 'AB')
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(NAME)}</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:16px 16px 80px}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.pair video{{width:100%;max-height:78vh;background:#000;border-radius:8px}}
.four{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}}.four img{{width:100%;border-radius:6px;display:block}}figure{{margin:0}}figcaption,small{{color:var(--mut);font-size:13px}}
button{{margin:6px 6px 6px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
textarea{{width:100%;height:110px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 4 · DS-40 · the intro clip, two ways</p>
<h1>Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right.</h1>
<p>{E(notes['intro'])}</p>
<h2>Your decision</h2><ol>{li(notes['questions'])}</ol>
<h2>A and B side by side</h2>
<div class="pair" id="pp"><div><h4>{E(notes['label']['A'])}</h4><video playsinline preload="metadata" src="media/{E(FILES['A'])}"></video></div>
<div><h4>{E(notes['label']['B'])}</h4><video playsinline preload="metadata" muted src="media/{E(FILES['B'])}"></video></div></div>
<button onclick="pair()">Play or pause both (sound from A)</button><button onclick="step(-1)">Back one frame</button><button onclick="step(1)">Forward one frame</button>
<p><small>Each one alone, with sound: <a style="color:var(--acc)" href="media/{E(FILES['A'])}">A</a> · <a style="color:var(--acc)" href="media/{E(FILES['B'])}">B</a>.
Key checks over pink: <a style="color:var(--acc)" href="media/{E(NAME)} - intro A pink key check.mp4">A</a> · <a style="color:var(--acc)" href="media/{E(NAME)} - intro B pink key check.mp4">B</a></small></p>
<h2>Stills</h2>{stills}
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>
function vids(){{return [...document.querySelectorAll('#pp video')];}}
function pair(){{const v=vids();if(!v[0].paused){{v.forEach(x=>x.pause());return;}}const t=v[0].currentTime>=v[0].duration-0.05?0:v[0].currentTime;v.forEach(x=>{{x.currentTime=t;x.play();}});}}
function step(d){{const v=vids();v.forEach(x=>x.pause());const t=Math.max(0,v[0].currentTime+d*1001/30000);v.forEach(x=>x.currentTime=t);}}
</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE written', Q/'index.html')
