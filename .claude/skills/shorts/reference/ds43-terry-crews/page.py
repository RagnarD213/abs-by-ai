"""DS-43 R1 review page: the scripted and the off-the-cuff Shorts side by side (lengths shown, one question: which ships), then
round 1's full asset review (VIDEO-RULES 2026-10-08): every graphic, cutaway and clip in timeline order, three per row, each
with a still on its real frame and a "Play it in context" clip; What I decided; checks; reply box.
Players never autoplay: the review server injects the shared silent-checks / owner-handoff helper (review_player.js).
Text: review/notes.json.   python3 page.py"""
from pathlib import Path
import json, subprocess, html, shutil
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True)
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
NAMES = {'scripted': 'Terry Crews Fasting SFC R1 - scripted', 'offcuff': 'Terry Crews Fasting SFC R1 - off the cuff'}
LABEL = {'scripted': 'Scripted (teleprompter)', 'offcuff': 'Off the cuff'}
notes = json.load(open(Q/'notes.json'))
def mmss(t): return f'{int(t//60)}:{t%60:04.1f}'
E = html.escape
V = {}
for v, name in NAMES.items():
    O = W/v; src = O/'review'
    for suf in ('.mp4', ' - REVIEW 540p.mp4', ' - audio AB.mp4', '.srt'):
        if (src/f'{name}{suf}').exists() and not (Q/f'{name}{suf}').exists(): (Q/f'{name}{suf}').symlink_to(src/f'{name}{suf}')
    edl = json.load(open(O/'edl.json')); shots = json.load(open(O/'shots.json')); man = json.load(open(O/'graphics-manifest.json'))
    END = edl['total_frames']/FPS; master = src/f'{name}.mp4'
    (Q/'context').mkdir(exist_ok=True)
    items = []
    def add(id_, title, a, b, still, kind):
        a0 = max(0, a - 2.5); b0 = min(END, b + 2.5); clip = f'context/{v}-{id_}.mp4'; img = f'context/{v}-{id_}.jpg'
        ff(['-ss', f'{a0:.3f}', '-i', master, '-t', f'{b0 - a0:.3f}', '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 21,
            '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', Q/clip])
        ff(['-ss', f'{still:.3f}', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/img])
        items.append(dict(id=id_, title=title, a=a, b=b, clip=clip, img=img, kind=kind, range=f'{mmss(a0)}-{mmss(b0)}'))
    sh = {s['id']: s for s in shots}
    add('open', 'Opening: Terry\'s clip full screen, you watching lower left', 0, sh['S0']['b'], 2.0, 'format')
    add('panel', 'Titled panel "Terry Crews | Business Insider", you watching', sh['PW']['a'], sh['PW']['b'], sh['PW']['a'] + 6.0, 'format')
    add('resp', 'Your reply starts; the clip keeps playing silently behind you', sh['PR']['a'], sh['PR']['b'], sh['PR']['a'] + 2.0, 'format')
    for s in shots:
        if s['kind'] == 'broll':
            add(s['id'], {'A0210': 'AI clip (library A0210): AI you waits until 2 PM, then eats', 'B0317': 'Stock clip (library B0317): a restaurant table of steak, bread and wine', 'A0086': 'AI clip (library A0086): a man eats a steak dinner'}[s['clip']],
                s['a'], s['b'], (s['a'] + s['b'])/2, 'clip')
        if s['kind'] == 'still':
            add(s['id'], 'Cutaway: Terry shirtless (a frame of his own clip, slow push-in)', s['a'], s['b'], (s['a'] + s['b'])/2, 'clip')
    for m in man:
        add(m['id'], 'Graphic: ' + m['words'], m['a'], m['b'], min(m['b'] - 0.3, m['a'] + 1.6), 'graphic')
    items.sort(key=lambda x: x['a'])
    ff(['-ss', '6.0', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/f'poster-{v}.jpg'])
    V[v] = dict(name=name, END=END, items=items)
films = ''.join(f"""<div class="film"><h3>{E(LABEL[v])}</h3><p class="len">{d['END']:.1f} s</p>
<video id="film-{v}" controls playsinline preload="metadata" poster="poster-{v}.jpg" src="{E(d['name'])} - REVIEW 540p.mp4"></video>
<p><a href="{E(d['name'])}.mp4">Full quality (1080x1920)</a> · <a href="{E(d['name'])} - audio AB.mp4">Audio A/B</a> · <a href="{E(d['name'])}.srt">Captions</a></p></div>""" for v, d in V.items())
def cards(v): return ''.join(f"""<div class="it"><img loading="lazy" src="{it['img']}"><b>{E(it['title'])}</b><small>{mmss(it['a'])}-{mmss(it['b'])} · context {it['range']}</small>
<button onclick="ctx('{it['clip']}')">Play it in context</button></div>""" for it in V[v]['items'])
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Terry Crews Fasting R1</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1180px;padding:16px 16px 80px;margin:0 auto}}h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
.films{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.film video{{width:100%;background:#000;border-radius:8px;max-height:78vh}}@media(max-width:700px){{.films{{grid-template-columns:1fr}}}}
.q{{font-size:20px;font-weight:700;background:var(--card);padding:12px;border-radius:8px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr 1fr}}}}
.it{{background:var(--card);border-radius:8px;padding:8px;display:flex;flex-direction:column;gap:4px}}.it img{{width:100%;border-radius:6px}}small{{color:var(--mut)}}
.len{{font-size:20px;font-weight:700;color:var(--rec);margin:0}}button{{margin:4px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
#ctxbox{{position:sticky;top:8px;background:var(--card);padding:8px;border-radius:8px;display:none;z-index:2}}#ctxbox video{{max-height:60vh;max-width:100%}}
textarea{{width:100%;height:120px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 1 · DS-43 · locked reaction format (Bill Maher Codex R5)</p>
<h1>Terry Crews Doesn't Eat Until 2 PM. He's Right.</h1><p>{E(notes['intro'])}</p>
<p class="q">Your one call: which version ships, scripted or off the cuff?</p>
<div class="films">{films}</div>
<div id="ctxbox"><video id="ctx" controls playsinline preload="metadata"></video><br><button onclick="document.getElementById('ctxbox').style.display='none';document.getElementById('ctx').pause()">Close</button></div>
<h2>Scripted: every graphic, clip and cutaway</h2><div class="grid">{cards('scripted')}</div>
<h2>Off the cuff: every graphic, clip and cutaway</h2><div class="grid">{cards('offcuff')}</div>
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply"></textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src){{const b=document.getElementById('ctxbox'),v=document.getElementById('ctx');b.style.display='block';v.src=src;b.scrollIntoView({{block:'nearest'}});}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE', {v: (round(d['END'], 2), len(d['items'])) for v, d in V.items()})
