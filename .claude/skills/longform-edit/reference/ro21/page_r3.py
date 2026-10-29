"""RO-21 round 3 review page: the full film. First minute and the whole film each in their OWN inline player at the top
(Dan R1), then the revision list with exact timestamps and watch ranges (Dan 2026-10-10: later rounds list each change so he
does not rewatch everything), what I decided, the checks, reply box. Serve with _shared/review_server.py.  python3 page_r3.py"""
import json, html, os, shutil
B = '/Volumes/Expansion/_edit_work/RO-21'; R3 = f'{B}/round3'; OUT = f'{R3}/review'; E = html.escape
os.makedirs(f'{OUT}/media', exist_ok=True)
def cp(src, name):
    dst = f'{OUT}/media/{name}'
    if os.path.exists(src) and (not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src)): shutil.copy2(src, dst)
    return f'media/{name}' if os.path.exists(dst) else None
D = json.load(open(f'{R3}/page_copy.json'))
fm = cp(f'{R3}/final/first-minute-540p.mp4', 'first-minute.mp4'); full = cp(f'{R3}/final/RO-21 round 3 - full film - REVIEW 540p.mp4', 'full-film-540p.mp4')
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
rows = ''.join(f"""<tr><td><b>{mmss(c['t'])}</b></td><td>{E(c['what'])}</td><td><button onclick="seek({max(0, c['t'] - 3):.1f},{c['t'] + c.get('len', 8):.1f})">&#9654; {mmss(max(0, c['t'] - 3))}-{mmss(c['t'] + c.get('len', 8))}</button></td></tr>"""
               for c in D['changes'])
did = ''.join(f'<li>{E(d)}</li>' for d in D['decided']); chk = ''.join(f'<li>{E(d)}</li>' for d in D['checks'])
page = f"""<!doctype html><html><head><meta charset=utf-8><title>Body Fat % LFC R3</title><meta name=viewport content="width=device-width,initial-scale=1">
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,sans-serif;margin:0;padding:16px}}main{{max-width:1100px;margin:auto}}
h1{{font-size:26px}}h2{{color:var(--acc);font-size:20px;margin-top:30px;border-top:1px solid var(--line);padding-top:14px}}
button{{background:#18324d;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:5px 9px;cursor:pointer;white-space:nowrap}}
video.inline{{width:100%;border-radius:10px;background:#000}}table{{width:100%;border-collapse:collapse}}td{{border-bottom:1px solid var(--line);padding:8px 6px;vertical-align:top}}
.mute{{color:var(--mute);font-size:14px}}textarea{{width:100%;height:140px;background:#0b1828;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:10px;font:15px/1.5 monospace}}
a{{color:var(--acc)}}</style></head><body><main>
<h1>What Every Body Fat Percentage Looks Like (On Me): round 3, the full film</h1><p>{E(D['intro'])}</p>
<h2>The first minute</h2><video class=inline controls muted preload=metadata src="{fm}"></video>
<h2>The whole film (7:27)</h2><video class=inline id=full controls muted preload=metadata src="{full}"></video>
<p class=mute>{E(D['files_note'])}</p>
<h2>What changed in this round ({len(D['changes'])}), with watch ranges</h2><p class=mute>Each button plays that stretch in the whole-film player above.</p><table>{rows}</table>
<h2>One question</h2><p>{E(D.get('question',''))}</p>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Checks on this exact file</h2><ul>{chk}</ul>
<h2>Your reply</h2><textarea id=rep>Approved / notes:\n</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value)">Copy</button>
</main><script>let stopAt=null;const v=document.getElementById('full');function seek(a,b){{v.currentTime=a;stopAt=b;v.play();v.scrollIntoView({{behavior:'smooth',block:'center'}});}}
v.addEventListener('timeupdate',()=>{{if(stopAt!==null&&v.currentTime>=stopAt){{v.pause();stopAt=null;}}}});</script></body></html>"""
open(f'{OUT}/index.html', 'w').write(page); print('page written', 'fm' if fm else 'NO FM', 'full' if full else 'NO FULL')
