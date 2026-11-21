"""DS-107 R1 review page: the finished Short on top, then the round-1 decisions (look on Dan, voice), the key check, "What I decided",
every graphic, clip and photo in timeline order (a still on its real frame + "Play it in context" with ~2.5 s either side), checks and
a reply box. Players never autoplay: review_server.py injects the shared silent-checks / owner-handoff helper (review_player.js).
Text: review/notes.json.   python3 page.py"""
from pathlib import Path
import json, subprocess, html
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True)
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
NAME = 'Metabolism Not The Reason SFC R1'; O = W/'main'; src = O/'review'
notes = json.load(open(Q/'notes.json'))
def mmss(t): return f'{int(t//60)}:{t%60:04.1f}'
E = html.escape
for suf in ('.mp4', ' - audio AB.mp4', '.srt'):
    p = Q/f'{NAME}{suf}'
    if (src/f'{NAME}{suf}').exists():
        if p.is_symlink() or p.exists(): p.unlink()
        p.symlink_to(src/f'{NAME}{suf}')
edl = json.load(open(O/'edl.json')); shots = json.load(open(O/'shots.json')); man = json.load(open(O/'graphics-manifest.json'))
END = edl['total_frames']/FPS; master = src/f'{NAME}.mp4'
(Q/'context').mkdir(exist_ok=True)
items = []
def add(id_, title, a, b, still, kind):
    a0 = max(0, a - 2.5); b0 = min(END, b + 2.5); clip = f'context/{id_}.mp4'; img = f'context/{id_}.jpg'
    ff(['-ss', f'{a0:.3f}', '-i', master, '-t', f'{b0 - a0:.3f}', '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 21,
        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', Q/clip])
    ff(['-ss', f'{still:.3f}', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/img])
    items.append(dict(id=id_, title=title, a=a, b=b, clip=clip, img=img, kind=kind, range=f'{mmss(a0)}-{mmss(b0)}'))
for s in shots:
    if s['kind'] in ('broll', 'still'):
        add(s['id'], notes['clips'][s.get('clip') or s.get('photo')], s['a'], s['b'], (s['a'] + s['b'])/2, 'clip')
for m in man:
    add(m['id'], 'Graphic: ' + m['words'], m['a'], m['b'], min(m['b'] - 0.3, m['a'] + (8.0 if m['id'] == 'K1' else 1.6)), 'graphic')
add('band', 'Title band (on screen the whole Short): METABOLISM MYTH / Your Metabolism Is Not / The Reason You\'re Fat', 0.0, 2.0, 1.0, 'graphic')
items.sort(key=lambda x: x['a'])
ff(['-ss', '2.0', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/'poster.jpg'])
cards = ''.join(f"""<div class="it"><img loading="lazy" src="{it['img']}"><b>{E(it['id'])} · {E(it['title'])}</b><small>{mmss(it['a'])}-{mmss(it['b'])} · context {it['range']}</small>
<button onclick="ctx('{it['clip']}')">Play it in context</button></div>""" for it in items)
looks = ''.join(f"""<div class="it"><img loading="lazy" src="{E(l['img'])}"><b>{E(l['label'])}</b><small>{E(l['note'])}</small></div>""" for l in notes['looks'])
voices = ''.join(f"""<div class="it"><b>{E(v['label'])}</b><audio controls preload="none" muted src="{E(v['src'])}"></audio><small>{E(v['note'])}</small></div>""" for v in notes['voices'])
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
qs = ''.join(f'<li>{E(x)}</li>' for x in notes['questions'])
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Metabolism SFC R1</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1180px;padding:16px 16px 80px;margin:0 auto}}h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
.top{{display:grid;grid-template-columns:minmax(0,420px) 1fr;gap:20px;align-items:start}}@media(max-width:760px){{.top{{grid-template-columns:1fr}}}}
.film video{{width:100%;background:#000;border-radius:8px;max-height:80vh}}.q{{background:var(--card);padding:12px 12px 12px 30px;border-radius:8px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr 1fr}}}}
.it{{background:var(--card);border-radius:8px;padding:8px;display:flex;flex-direction:column;gap:4px}}.it img{{width:100%;border-radius:6px}}small{{color:var(--mut)}}audio{{width:100%}}
.len{{font-size:20px;font-weight:700;color:var(--rec);margin:0}}button{{margin:4px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
#ctxbox{{position:fixed;right:12px;bottom:12px;width:300px;background:var(--card);padding:8px;border-radius:8px;display:none;z-index:2;box-shadow:0 4px 24px #000a}}#ctxbox video{{width:100%}}
textarea{{width:100%;height:140px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 1 · DS-107 · 11/13 green screen, roll C1908 · edited on the M2</p>
<h1>Your Metabolism Is Not The Reason You're Fat</h1>
<div class="top"><div class="film"><p class="len">{END:.1f} s</p><video id="film" controls playsinline preload="metadata" muted poster="poster.jpg" src="{E(NAME)}.mp4"></video>
<p><a href="{E(NAME)}.mp4">Full quality (1080x1920)</a> · <a href="{E(NAME)} - audio AB.mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions</a></p></div>
<div><p>{E(notes['intro'])}</p><h3>Your decisions ({len(notes['questions'])})</h3><ol class="q">{qs}</ol><p><small>{E(notes['locked'])}</small></p></div></div>
<h2>1. Colour on you (same two moments, only your grade changes)</h2><div class="grid">{looks}</div>
<h2>2. Voice (the same 30 s, level matched; press play)</h2><div class="grid">{voices}</div><p><small>{E(notes['listen'])}</small></p>
<h2>Green-screen key check</h2><div class="grid">{''.join(f'<div class="it"><img loading="lazy" src="{E(k["img"])}"><small>{E(k["note"])}</small></div>' for k in notes['key'])}</div>
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Every graphic, clip and photo, in order</h2><div class="grid">{cards}</div>
<div id="ctxbox"><video id="ctx" controls playsinline preload="none" muted></video><br><button onclick="document.getElementById('ctxbox').style.display='none';document.getElementById('ctx').pause()">Close</button></div>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply">{E(notes['reply'])}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src){{const b=document.getElementById('ctxbox'),v=document.getElementById('ctx');b.style.display='block';v.src=src;}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE', round(END, 2), len(items), 'items')
