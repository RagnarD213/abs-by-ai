"""DS-31 R1 review page: full Short on top, AI idea frames, What I decided, every graphic and clip in order (3 per row)
with a shared side player for 'play it moving, in context', one reply box. Notes text lives in review/notes.json."""
from pathlib import Path
import json, subprocess, html, shutil, os
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = 'AI Homework SFC R1'
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
master = Q/f'{NAME} - complete Short.mp4'; phone = f'{NAME} - phone review.mp4'
shots = json.load(open(W/'shots.json')); graphics = json.load(open(W/'graphics-sheet.json'))['graphics']; words = json.load(open(W/'words_out.json'))
notes = json.load(open(Q/'notes.json'))
(Q/'context').mkdir(exist_ok=True); (Q/'stills').mkdir(exist_ok=True); (Q/'frames').mkdir(exist_ok=True)
END = json.load(open(W/'edl.json'))['total_frames']/FPS
def said(a, b): return ' '.join(w['w'] for w in words if a - 0.05 <= w['t0'] < b - 0.05)
def mmss(t): return f'{int(t//60)}:{t%60:05.2f}'
items = []
for s in shots:
    if s['kind'] == 'broll':
        items.append(dict(id=s['id'], kind='Clip', a=s['a'], b=s['b'], title=s['f'].replace('.mp4', ''), what=s['line'],
                          src=('our own B-roll, library ' + s['f'][:5]) if s['f'].startswith('B0') else f"Pexels {s['f'][2:-4]} (free)"))
for g in graphics:
    items.append(dict(id=g['id'], kind='Graphic', a=g['t0'], b=g['t1'], title=g['title'], what=' | '.join(g['labels']), src='Soft Blue card (Meal Prep ribbon style)'))
items.sort(key=lambda x: x['a'])
for it in items:
    st = Q/'stills'/f"{it['id']}.jpg"; cx = Q/'context'/f"{it['id']}-context - REVIEW 540p.mp4"
    t = it['b'] - 0.4 if it['kind'] == 'Graphic' else (it['a'] + it['b'])/2
    ff(['-ss', f'{t:.3f}', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, st])
    a = max(0, it['a'] - 3); b = min(END, it['b'] + 3)
    ff(['-ss', f'{a:.3f}', '-i', master, '-t', f'{b - a:.3f}', '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 22, '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', cx])
    it['before'] = said(max(0, it['a'] - 3), it['a']); it['during'] = said(it['a'], it['b']); it['after'] = said(it['b'], min(END, it['b'] + 3))
for a in notes['ai']:
    for k in ('start', 'end'):
        shutil.copy(W/'aiframes'/f"{a['id']}-{k}.png", Q/'frames'/f"{a['id']}-{k}.png")
E = html.escape
cards = ''.join(f"""<div class="card"><img loading="lazy" src="stills/{it['id']}.jpg"><div class="meta"><b>{it['id']} · {it['kind']}</b> {mmss(it['a'])} to {mmss(it['b'])}<br>
<span class="t">{E(it['title'])}</span><br>{E(it['what'])}<br><small>{E(it['src'])}</small>
<button onclick="ctx('context/{it['id']}-context - REVIEW 540p.mp4')">Play it moving, in context</button>
<details><summary>Speech before / during / after</summary><p><i>{E(it['before'])}</i></p><p><b>{E(it['during'])}</b></p><p><i>{E(it['after'])}</i></p></details></div></div>""" for it in items)
ai = ''.join(f"""<div class="pair"><h3>{E(a['id'])}: {E(a['name'])}</h3><div class="two"><figure><img src="frames/{a['id']}-start.png"><figcaption>START</figcaption></figure><figure><img src="frames/{a['id']}-end.png"><figcaption>END</figcaption></figure></div>
<table>{''.join(f'<tr><th>{E(k)}</th><td>{E(v)}</td></tr>' for k, v in a['rows'])}</table></div>""" for a in notes['ai'])
decided = ''.join(f'<li>{E(x)}</li>' for x in notes['decided'])
qs = ''.join(f'<li>{E(x)}</li>' for x in notes['questions'])
reply = '\n'.join(f'{i+1}. ' for i in range(len(notes['questions'])))
checks = ''.join(f'<li>{E(x)}</li>' for x in notes['checks'])
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Homework SFC R1</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1180px;padding:16px 16px 80px;margin-right:420px}}@media(max-width:1100px){{main{{margin-right:0}}#side{{position:static!important;width:auto!important}}}}
h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
#side{{position:fixed;right:16px;top:16px;width:380px}}#side video{{width:100%;background:#000;border-radius:8px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:var(--card);border-radius:8px;overflow:hidden}}.card img{{width:100%;display:block}}.meta{{padding:8px 10px;font-size:13px}}.t{{color:var(--acc);font-weight:600}}
button{{margin:6px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
.pair{{background:var(--card);border-radius:8px;padding:10px;margin:12px 0}}.two{{display:flex;gap:10px}}.two figure{{margin:0;flex:1}}.two img{{width:100%;border-radius:6px}}figcaption{{text-align:center;color:var(--mut)}}
th{{text-align:left;color:var(--mut);padding-right:10px;vertical-align:top;white-space:nowrap}}textarea{{width:100%;height:140px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}
a{{color:var(--acc)}}small{{color:var(--mut)}}</style></head><body>
<aside id="side"><video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{E(phone)}"></video>
<p><a href="{E(master.name)}">Full-quality Short (1080x1920)</a> · <a href="{E(NAME)} - audio AB (reference then ours).mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions file</a></p>
<p id="now" class="badge">Playing: the complete Short</p><button onclick="ctx('{E(phone)}','the complete Short')">Back to the complete Short</button></aside>
<main><p class="badge">CONTENT · Dedicated Short (SFC) · Round 1 · DS-31</p><h1>AI Homework</h1>
<p>{E(notes['intro'])}</p><p><b>Already locked (reused from Meal Prep, same studio set and roll):</b> {E(notes['locked'])}</p>
<h2>Your decisions ({len(notes['questions'])})</h2><ol>{qs}</ol>
<h2>The complete Short ({END:.1f} s)</h2><p>It plays in the panel on the right. Phone copy there; full quality: <a href="{E(master.name)}">1080x1920 master</a>. Also in your <b>Videos to Review</b> folder for VLC.</p>
<h2>AI clip ideas (frames only, no motion made yet)</h2><p>{E(notes['ai_intro'])}</p>{ai}
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Every clip and graphic, in order</h2><div class="grid">{cards}</div>
<h2>Checks</h2><ul>{checks}</ul>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src,label){{const v=document.getElementById('film');v.src=src;v.play();document.getElementById('now').textContent='Playing: '+(label||src.replace('context/','').split(' - REVIEW')[0]);}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE', len(items), 'items', len(notes['ai']), 'AI pairs')
