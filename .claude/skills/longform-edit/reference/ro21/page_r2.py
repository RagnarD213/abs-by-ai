"""RO-21 round 2 review page (small: only Dan's four changes). The first minute plays in its OWN inline player at the top
(Dan, R1: "The first minute isn't showing on the review page"), then B10's new START/END frames under the line they play
under, and G10 / B01 / P12 in context through the docked player. Rich grade, voice A. Serve with _shared/review_server.py
(it injects the silent-check / owner-handoff helper).   python3 page_r2.py"""
import json, html, os, shutil
B = '/Volumes/Expansion/_edit_work/RO-21'; R2 = f'{B}/round2'; OUT = f'{R2}/review'; E = html.escape
os.makedirs(f'{OUT}/media', exist_ok=True)
def cp(src, name):
    dst = f'{OUT}/media/{name}'
    if os.path.exists(src) and (not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src)): shutil.copy2(src, dst)
    return f'media/{name}' if os.path.exists(dst) else None
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
D = json.load(open(f'{R2}/page_copy.json'))
fm = cp(f'{R2}/fm/DRAFT - RO-21 round 2 - first minute.mp4', 'first-minute.mp4')
def btn(src, label): return f"""<button onclick="play('{src}','{E(label)}')">&#9654; {E(label)}</button>""" if src else '<i>(rendering)</i>'
ctx = lambda i: cp(f'{OUT}/context/{i}-context - REVIEW 540p.mp4', f'ctx_{i}.mp4')
post = lambda i: cp(f'{OUT}/context/{i}.jpg', f'ctx_{i}.jpg')
s, e = cp(D['b10']['start'], 'B10_start.png'), cp(D['b10']['end'], 'B10_end.png')
ev = cp(D['b10']['evidence'], 'B10_framecheck.jpg') if D['b10'].get('evidence') else None
man = cp(f'{R2}/ai/G10_man.png', 'G10_man.png')
items = ''.join(f"""<div class=card><img src="{post(i)}"><div><b>{i}</b> {E(D['items'][i]['what'])} · {E(D['items'][i]['when'])}</div>
<div class=cp>{E(D['items'][i]['copy'])}</div><div class=nt>{E(D['items'][i]['note'])}</div>{btn(ctx(i), f'{i} in context')}</div>""" for i in ('B01', 'P12', 'G10'))
dec = ''.join(f'<li>{E(d)}</li>' for d in D['decisions']); did = ''.join(f'<li>{E(d)}</li>' for d in D['decided'])
reply = '\n'.join(f'{k + 1}. ' for k in range(len(D['decisions'])))
page = f"""<!doctype html><html><head><meta charset=utf-8><title>Body Fat % LFC R2</title><meta name=viewport content="width=device-width,initial-scale=1">
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,sans-serif;margin:0;padding:16px}}main{{max-width:1100px;margin:auto}}
h1{{font-size:26px}}h2{{color:var(--acc);font-size:20px;margin-top:34px;border-top:1px solid var(--line);padding-top:16px}}
button{{background:#18324d;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:6px 10px;margin:3px 2px;cursor:pointer}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.card img{{width:100%;border-radius:8px}}.cp{{margin:6px 0;font-weight:600}}.nt,.mute{{color:var(--mute);font-size:14px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.pair img,.wide{{width:100%;border-radius:8px}}.line{{font-size:19px;font-weight:600;margin:8px 0}}
video.inline{{width:100%;border-radius:10px;background:#000}}
#dock{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px;margin:14px 0}}#dock video{{width:100%;border-radius:8px;background:#000}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:62vw}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
@media(max-width:700px){{.pair{{grid-template-columns:1fr}}}}
textarea{{width:100%;height:150px;background:#0b1828;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:10px;font:15px/1.5 monospace}}
a{{color:var(--acc)}}</style></head><body><main>
<h1>What Every Body Fat Percentage Looks Like (On Me): round 2</h1>
<p>{E(D['intro'])}</p>
<h2>The first minute, as it is now</h2><video class=inline id=fmv controls muted preload=metadata src="{fm}"></video><p class=mute>{E(D['fm_note'])}</p>
<h2>Your decisions ({len(D['decisions'])})</h2><ol>{dec}</ol>
<h2>1. New AI clip B10: you asleep, Nest at 63 (frames only, no motion yet)</h2>
<p class=line>"{E(D['b10']['line'])}" <span class=mute>({E(D['b10']['when'])})</span></p>
<div class=pair><div><b>START</b><br><a href="{s}" target=_blank><img src="{s}"></a></div><div><b>END</b><br><a href="{e}" target=_blank><img src="{e}"></a></div></div>
<p class=nt>{E(D['b10']['note'])}</p>{f'<details><summary>Frame check evidence</summary><img class=wide src="{ev}"></details>' if ev else ''}
<h2>2-4. The other three changes, in context</h2>
<p class=mute>G10 background still:</p><a href="{man}" target=_blank><img class=wide style="max-width:520px" src="{man}"></a>
<div class=grid style="margin-top:12px">{items}</div>
<div id=dock><div id=nowp class=mute>Player: press any Play button</div><video id=pv controls muted preload="none"></video></div>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Your reply</h2><textarea id=rep>{E(reply)}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value)">Copy</button>
</main><script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></body></html>"""
open(f'{OUT}/index.html', 'w').write(page)
print('page written; first minute', 'ok' if fm else 'MISSING', '; context', [i for i in ('B01', 'P12', 'G10') if not ctx(i)] or 'all present')
