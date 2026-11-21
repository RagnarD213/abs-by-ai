"""DS-44 R1 review page (round 1: every graphic, clip and the B-roll shown on its real frame and playable in context with
3-5 s around it; colour and voice options; What I decided; decisions; checks; reply box). Text: review/notes.json."""
from pathlib import Path
import json, subprocess, html, shutil
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = 'Hormozi Fat Guy SFC R2'
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
master = Q/f'{NAME} - complete Short.mp4'; phone = f'{NAME} - REVIEW 540p.mp4'
notes = json.load(open(Q/'notes.json')); man = json.load(open(W/'graphics-manifest.json'))
END = json.load(open(W/'edl.json'))['total_frames']/FPS
(Q/'context').mkdir(exist_ok=True); (Q/'options').mkdir(exist_ok=True)
for f in (W/'options').glob('*'):
    if not f.name.startswith('._'): shutil.copy(f, Q/'options'/f.name)
SH = json.load(open(W/'shots.json'))
# R2: only what changed (Dan 2026-10-10: later rounds list each change with timestamps in the new film)
items = [dict(id='R2-1', a=0.0, b=15.42, title='Opening: you lower left at the standard size, laptop showing (Bill Maher option B)', still=6.0),
         dict(id='R2-2', a=15.42, b=15.95, title='The move: the clip shrinks into the frame at the top, you grow in front of it', still=15.7),
         dict(id='R2-3', a=15.95, b=25.09, title='The interview keeps playing silently behind your head, your hair over the frame edge', still=20.0),
         dict(id='R2-4', a=27.53, b=32.03, title='Interview frame continues (after the caller cutaway); THE REAL PROBLEM moved under your chin', still=31.0)]
items.sort(key=lambda x: x['a'])
def mmss(t): return f'{int(t//60)}:{t%60:04.1f}'
for it in items:
    a0 = max(0, it['a'] - 3.5); b0 = min(END, it['b'] + 3.5)
    it['clip'] = f"context/{it['id']}.mp4"; it['img'] = f"context/{it['id']}.jpg"
    ff(['-ss', f'{a0:.3f}', '-i', master, '-t', f'{b0 - a0:.3f}', '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 21, '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', Q/it['clip']])
    ff(['-ss', f"{it['still']:.3f}", '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/it['img']])
    it['range'] = f"{mmss(a0)}-{mmss(b0)}"
ff(['-ss', '1.0', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/'poster.jpg'])
E = html.escape
cards = ''.join(f"""<div class="it"><img loading="lazy" src="{it['img']}"><b>{E(it['id'])}: {E(it['title'])}</b><small>{mmss(it['a'])}-{mmss(it['b'])} in the Short</small>
<button onclick="ctx('{it['clip']}','{E(it['id'])} in context ({it['range']})')">Play it moving, in context</button></div>""" for it in items)
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
reply = '\n'.join(f'{i+1}. ' for i in range(len(notes['questions'])))
voices = ''.join(f"""<div class="opt{' rec' if k == 'house_bass15' else ''}"><b>{E(v)}</b><audio controls preload="none" src="options/voice-{k}.m4a"></audio></div>"""
                 for k, v in notes['voices'].items())
colours = ''.join(f"""<div class="opt{' rec' if k == 'B_warmvivid' else ''}"><img src="options/colour-{k}.jpg"><b>{E(v)}</b></div>""" for k, v in notes['colours'].items())
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Hormozi Fat Guy SFC R2</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1180px;padding:16px 16px 80px;margin-right:420px}}@media(max-width:1100px){{main{{margin-right:0}}#side{{position:static!important;width:auto!important}}}}
h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
#side{{position:fixed;right:16px;top:16px;width:380px}}#side video{{width:100%;background:#000;border-radius:8px;max-height:72vh}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}@media(max-width:700px){{.grid{{grid-template-columns:1fr 1fr}}}}
.it,.opt{{background:var(--card);border-radius:8px;padding:8px;border:2px solid transparent;display:flex;flex-direction:column;gap:4px}}.it img,.opt img{{width:100%;border-radius:6px}}
.opt.rec{{border-color:var(--rec)}}audio{{width:100%}}small{{color:var(--mut)}}
button{{margin:4px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
textarea{{width:100%;height:140px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}</style></head><body>
<aside id="side"><video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{E(phone)}"></video>
<p><a href="{E(master.name)}">Full-quality Short (1080x1920)</a> · <a href="{E(NAME)} - audio AB.mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions file</a></p>
<p id="now" class="badge">Playing: the complete Short</p><button onclick="ctx('{E(phone)}','the complete Short')">Back to the complete Short</button></aside>
<main><p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 · DS-44</p><h1>Alex Hormozi Asks A Fat Guy Why He Isn't 200 Pounds Heavier. He's Right.</h1>
<p>{E(notes['intro'])}</p>
<h2>The complete Short ({END:.1f} s)</h2><p>Plays in the panel on the right (on a phone: above). Full quality: <a href="{E(master.name)}">1080x1920 master</a>. Also in your <b>Videos to Review</b> folder for VLC.</p>
<h2>Your decisions ({len(notes['questions'])})</h2><ol>{li(notes['questions'])}</ol>
<h2>What changed in round 2 (watch these)</h2><div class="grid">{cards}</div>
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src,label){{const v=document.getElementById('film');v.src=src;v.play();document.getElementById('now').textContent='Playing: '+(label||src);}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE', len(items), 'items')
