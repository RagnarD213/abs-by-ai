"""DS-30 R1 review page (DS-107 page adapted): the finished Short on top, the round-1 decisions (colour, voice), "What I decided",
every graphic and clip in timeline order (a still on its real frame + "Play it in context" with ~2.5 s either side), checks and a
reply box. Players never autoplay: review_server.py injects the shared silent-checks / owner-handoff helper (review_player.js).
Text: review/notes.json.   python3 page.py"""
from pathlib import Path
import json, subprocess, html, shutil
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
NAME = 'Self-Driving Car SFC R1'; src = W/'review'; Q = W/'page'; Q.mkdir(exist_ok=True)
notes = json.load(open(W/'notes.json'))
def mmss(t): return f'{int(t//60)}:{t%60:04.1f}'
E = html.escape
for f in (f'{NAME} - complete Short.mp4', f'{NAME} - audio AB.mp4', f'{NAME}.srt'):
    shutil.copy2(src/f, Q/f)
(Q/'opt').mkdir(exist_ok=True)
opts = json.load(open(W/'options/options.json'))
for v in opts['voices']: shutil.copy2(W/'options'/v['clip'], Q/'opt'/v['clip'])
for c in opts['colours']:
    for f in list(c['stills'].values()) + [c['sample']]: shutil.copy2(W/'options'/f, Q/'opt'/f)
edl = json.load(open(W/'edl.json')); shots = json.load(open(W/'shots.json')); man = json.load(open(W/'graphics-manifest.json'))
END = edl['total_frames']/FPS; master = src/f'{NAME} - complete Short.mp4'
(Q/'context').mkdir(exist_ok=True)
items = []
def add(id_, title, a, b, still, kind):
    a0 = max(0, a - 2.5); b0 = min(END, b + 2.5); clip = f'context/{id_}.mp4'; img = f'context/{id_}.jpg'
    ff(['-ss', f'{a0:.3f}', '-i', master, '-t', f'{b0 - a0:.3f}', '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 21,
        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', Q/clip])
    ff(['-ss', f'{still:.3f}', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/img])
    items.append(dict(id=id_, title=title, a=a, b=b, clip=clip, img=img, kind=kind, range=f'{mmss(a0)}-{mmss(b0)}'))
for s in shots:
    if s['kind'] == 'broll': add(s['id'], notes['clips'][s['k']], s['a'], s['b'], (s['a'] + s['b'])/2, 'clip')
for m in man:
    add(m['id'], 'Graphic: ' + m['words'], m['a'], m['b'], m['b'] - 0.4, 'graphic')
items.sort(key=lambda x: x['a'])
ff(['-ss', '4.0', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/'poster.jpg'])
cards = ''.join(f"""<div class="it"><img loading="lazy" src="{it['img']}"><b>{E(it['id'])} · {E(it['title'])}</b><small>{mmss(it['a'])}-{mmss(it['b'])} · context {it['range']}</small>
<button onclick="ctx('{it['clip']}')">Play it in context</button></div>""" for it in items)
looks = ''.join(f"""<div class="it"><div class="two"><img loading="lazy" src="opt/{E(c['stills']['tight'])}"><img loading="lazy" src="opt/{E(c['stills']['wide'])}"></div>
<b>{E(c['id'])}: {E(c['name'])}{' (recommended, in the film)' if c['recommended'] else ''}</b><button onclick="ctx('opt/{E(c['sample'])}')">Play a moving sample</button></div>""" for c in opts['colours'])
voices = ''.join(f"""<div class="it"><b>{E(v['id'])}: {E(v['name'])}{' (recommended, in the film)' if v['recommended'] else ''}</b>
<video controls playsinline preload="none" muted src="opt/{E(v['clip'])}"></video></div>""" for v in opts['voices'])
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
qs = ''.join(f'<li>{E(x)}</li>' for x in notes['questions'])
FULL = f'{NAME} - complete Short.mp4'
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Self-Driving Car SFC R1</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1180px;padding:16px 16px 80px;margin:0 auto}}h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
.top{{display:grid;grid-template-columns:minmax(0,420px) 1fr;gap:20px;align-items:start}}@media(max-width:760px){{.top{{grid-template-columns:1fr}}}}
.film video{{width:100%;background:#000;border-radius:8px;max-height:80vh}}.q{{background:var(--card);padding:12px 12px 12px 30px;border-radius:8px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr 1fr}}}}
.it{{background:var(--card);border-radius:8px;padding:8px;display:flex;flex-direction:column;gap:4px}}.it img{{width:100%;border-radius:6px}}.it video{{width:100%;border-radius:6px}}.two{{display:flex;gap:4px}}.two img{{width:50%}}small{{color:var(--mut)}}
.len{{font-size:20px;font-weight:700;color:var(--rec);margin:0}}button{{margin:4px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
#ctxbox{{position:fixed;right:12px;bottom:12px;width:300px;background:var(--card);padding:8px;border-radius:8px;display:none;z-index:2;box-shadow:0 4px 24px #000a}}#ctxbox video{{width:100%}}
textarea{{width:100%;height:140px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 1 · DS-30 · 9/23 shoot, roll C1720 · edited on the M2</p>
<h1>Make Time For Exercise With A Self-Driving Car</h1>
<div class="top"><div class="film"><p class="len">{END:.1f} s</p><video id="film" controls playsinline preload="metadata" muted poster="poster.jpg" src="{E(FULL)}"></video>
<p><a href="{E(FULL)}">Full quality (1080x1920)</a> · <a href="{E(NAME)} - audio AB.mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions</a></p></div>
<div><p>{E(notes['intro'])}</p><h3>Your decisions ({len(notes['questions'])})</h3><ol class="q">{qs}</ol><p><small>{E(notes['locked'])}</small></p></div></div>
<h2>1. Colour on you (same two moments, only your grade changes)</h2><div class="grid">{looks}</div>
<h2>2. Voice (the same 10 s, level matched; press play)</h2><div class="grid">{voices}</div><p><small>{E(notes['listen'])}</small></p>
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Every graphic and clip, in order</h2><div class="grid">{cards}</div>
<div id="ctxbox"><video id="ctx" controls playsinline preload="none" muted></video><br><button onclick="document.getElementById('ctxbox').style.display='none';document.getElementById('ctx').pause()">Close</button></div>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply">{E(notes['reply'])}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src){{const b=document.getElementById('ctxbox'),v=document.getElementById('ctx');b.style.display='block';v.src=src;}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE', round(END, 2), len(items), 'items')
