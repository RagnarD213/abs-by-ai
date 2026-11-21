"""DS-31 R2 review page: what changed (with timestamps), the colour options at the top (recommendation already in the
film), the A1 opener in context, the complete Short in a side player, What I decided, decisions, checks, reply box.
Later round: only what changed is shown (VIDEO-RULES, round 1 shows everything, later rounds lighter). Notes text: review/notes.json."""
from pathlib import Path
import json, subprocess, html, shutil
from PIL import Image
R = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; C = W/'col'
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001; NAME = 'AI Homework SFC R2'
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
master = Q/f'{NAME} - complete Short.mp4'; phone = f'{NAME} - phone review.mp4'
notes = json.load(open(Q/'notes.json')); opts = json.load(open(C/'options.json')); pick = json.load(open(C/'pick.json'))['option']
END = json.load(open(W/'edl.json'))['total_frames']/FPS
O = Q/'colour'; O.mkdir(exist_ok=True); (Q/'context').mkdir(exist_ok=True)
for k in opts:
    for fk in ('tight', 'wide', 'closing'):
        Image.open(C/f'{k}-{fk}.png').convert('RGB').resize((540, 960)).save(O/f'{k}-{fk}.jpg', quality=90)
    shutil.copy(C/f'{k}-sample.mp4', O/f'{k}-sample.mp4'); shutil.copy(C/f'broll-{k}.jpg', O/f'broll-{k}.jpg')
a1ctx = Q/'context/A1-context - REVIEW 540p.mp4'
ff(['-i', master, '-t', '6.0', '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 21, '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', a1ctx])
ff(['-ss', '1.4', '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/'context/A1-still.jpg'])
E = html.escape
def nums(k):
    f = opts[k]['frames']
    return (f"<table class='n'><tr><th></th><th>tight</th><th>wide</th><th>closing</th></tr>"
            + ''.join(f"<tr><th>{lab}</th>" + ''.join(f"<td>{fmt(f[x][key])}</td>" for x in ('tight', 'wide', 'closing')) + '</tr>'
                      for lab, key, fmt in [('Median brightness', 'luma', lambda v: f'{v:.3f}'), ('Median saturation', 'sat', lambda v: f'{v:.2f}'),
                                            ('Backdrop saturation', 'backdrop_sat', lambda v: f'{v:.2f}'), ('Skin hue', 'skin_hue', lambda v: f'{v:.0f}°'),
                                            ('Skin saturation', 'skin_sat', lambda v: f'{v:.2f}')])
            + f"<tr><th>Light tubes hue</th><td>n/a</td><td>{f['wide']['tube_hue']:.0f}°</td><td>{f['closing']['tube_hue']:.0f}°</td></tr></table>")
cols = ''.join(f"""<div class="opt{' rec' if k == pick else ''}"><h3>{k}: {E(o['name'])}{' · RECOMMENDED, in the film' if k == pick else ''}</h3>
<div class="three">{''.join(f'<img loading="lazy" src="colour/{k}-{fk}.jpg" alt="{k} {fk}">' for fk in ('tight', 'wide', 'closing'))}</div>
<p>{E(notes['colour_desc'][k])}</p>
<button onclick="ctx('colour/{k}-sample.mp4','colour {k} moving sample (0:25.7-0:31.9)')">Play {k} moving, with sound</button>
<details><summary>Measured numbers</summary>{nums(k)}</details>
<details><summary>Next to the B-roll</summary><img class="wide" loading="lazy" src="colour/broll-{k}.jpg"><small>Your two camera frames in {k}, then every B-roll clip as graded in the film.</small></details></div>""" for k, o in opts.items())
changes = ''.join(f'<li>{E(x)}</li>' for x in notes['changes'])
decided = ''.join(f'<li>{E(x)}</li>' for x in notes['decided'])
qs = ''.join(f'<li>{E(x)}</li>' for x in notes['questions'])
reply = '\n'.join(f'{i+1}. ' for i in range(len(notes['questions'])))
checks = ''.join(f'<li>{E(x)}</li>' for x in notes['checks'])
a1rows = ''.join(f'<tr><th>{E(k)}</th><td>{E(v)}</td></tr>' for k, v in notes['a1_rows'])
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Homework SFC R2</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1180px;padding:16px 16px 80px;margin-right:420px}}@media(max-width:1100px){{main{{margin-right:0}}#side{{position:static!important;width:auto!important}}}}
h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
#side{{position:fixed;right:16px;top:16px;width:380px}}#side video{{width:100%;background:#000;border-radius:8px;max-height:70vh}}
.opt{{background:var(--card);border-radius:8px;padding:10px;margin:12px 0;border:2px solid transparent}}.opt.rec{{border-color:var(--rec)}}.opt h3{{margin:.2em 0}}.rec h3{{color:var(--rec)}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}.three img{{width:100%;border-radius:6px;display:block}}img.wide{{width:100%;border-radius:6px;margin-top:6px}}
table.n td,table.n th{{padding:2px 8px;text-align:right}}table.n th:first-child{{text-align:left;color:var(--mut)}}
.a1{{display:flex;gap:12px;flex-wrap:wrap}}.a1 img{{width:240px;border-radius:6px}}th{{text-align:left;color:var(--mut);padding-right:10px;vertical-align:top}}
button{{margin:6px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
textarea{{width:100%;height:120px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}small{{color:var(--mut)}}</style></head><body>
<aside id="side"><video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{E(phone)}"></video>
<p><a href="{E(master.name)}">Full-quality Short (1080x1920)</a> · <a href="{E(NAME)} - audio AB (reference then ours).mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions file</a></p>
<p id="now" class="badge">Playing: the complete Short</p><button onclick="ctx('{E(phone)}','the complete Short')">Back to the complete Short</button></aside>
<main><p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 · DS-31</p><h1>AI Homework</h1>
<p>{E(notes['intro'])}</p>
<h2>What changed since Round 1 (watch these)</h2><ul>{changes}</ul>
<h2>Your decisions ({len(notes['questions'])})</h2><ol>{qs}</ol>
<h2>Colour options</h2><p>{E(notes['colour_intro'])}</p>{cols}
<h2>A1: Homework tower, moving (0:00-0:02.8)</h2><div class="a1"><img src="context/A1-still.jpg"><div><table>{a1rows}</table>
<button onclick="ctx('context/A1-context - REVIEW 540p.mp4','A1 opener in context (0:00-0:06)')">Play it moving, in context</button></div></div>
<h2>The complete Short ({END:.1f} s)</h2><p>Plays in the panel on the right, already in colour {pick}. Full quality: <a href="{E(master.name)}">1080x1920 master</a>. Also in your <b>Videos to Review</b> folder for VLC.</p>
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Checks</h2><ul>{checks}</ul>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src,label){{const v=document.getElementById('film');v.src=src;v.play();document.getElementById('now').textContent='Playing: '+(label||src);}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE R2', len(opts), 'colour options, pick', pick)
