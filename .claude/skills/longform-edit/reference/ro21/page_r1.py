"""RO-21 round 1 review page (PRE-RENDER-APPROVAL "The review page"): decisions on top, the first minute, colour and voice
options, the key, the eight AI pictures, What I decided, then every graphic / picture card / clip in timeline order with a
"Play it moving, in context" button feeding ONE docked player. Serve with _shared/review_server.py (it injects the
silent-check / owner-handoff helper).   python3 page_r1.py"""
import json, html, os, shutil, re
B = '/Volumes/Expansion/_edit_work/RO-21'; R1 = f'{B}/round1'; OUT = f'{R1}/review'; E = html.escape
os.makedirs(f'{OUT}/media', exist_ok=True)
def cp(src, name):
    dst = f'{OUT}/media/{name}'
    if os.path.exists(src) and (not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src)): shutil.copy2(src, dst)
    return f'media/{name}' if os.path.exists(dst) else None
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
W = json.load(open(f'{R1}/film_words.json')); P = json.load(open(f'{R1}/plan_r1.json'))
FIX = [(r' ([.,%?!])', r'\1'), (r'(\d) \.(\d)', r'\1.\2'), (r'zap -bound|Zetbound|zet bound', 'Zepbound'), (r' -', '-'), (r'appsbyai \.com', 'AbsByAI.com'), (r'Shreddy', 'shredded'), (r'And yourself', 'And weigh yourself'), (r'never Do', 'never skip. Do')]
def said(a, b):
    s = ' '.join(w['w'] for w in W if a <= w['t0'] < b)
    for x, y in FIX: s = re.sub(x, y, s)
    return s
D = json.load(open(f'{R1}/page_copy.json'))
fm = cp(f'{R1}/fm/DRAFT - RO-21 round 1 - first minute - REVIEW 540p.mp4', 'first-minute-540p.mp4')
fm1080 = cp(f'{R1}/fm/DRAFT - RO-21 round 1 - first minute.mp4', 'first-minute-1080p.mp4')
def btn(src, label): return f"""<button onclick="play('{src}','{E(label)}')">&#9654; {E(label)}</button>""" if src else '<i>(rendering)</i>'
col = ''.join(f"""<div class=opt><img src="{cp(f'{R1}/colour/wide_{g}-00330.jpg', f'col_{g}_w.jpg')}"><img src="{cp(f'{R1}/colour/tight_{g}-00750.jpg', f'col_{g}_t.jpg')}">
  <b>{k}) {E(lab)}</b><br>{btn(cp(f'{R1}/colour/wide_{g}.mp4', f'col_{g}_w.mp4'), 'wide, moving')} {btn(cp(f'{R1}/colour/tight_{g}.mp4', f'col_{g}_t.mp4'), 'tight, moving')}</div>"""
              for k, g, lab in [('A', 'warm', 'Warm (recommended: your Celebrity Ozempic pick, same set and light)'), ('B', 'rich', 'Rich: warmer, more colour and snap'), ('C', 'natural', 'Natural: cooler, softer')])
vo = json.load(open(f'{B}/audio/opts/options.json'))['options']
names = {'B-balanced-bass': 'A) Your Celebrity Ozempic voice: Bill Maher voice plus the bass lift (recommended)', 'A-balanced': 'B) The same without the bass lift',
         'D-less-room': 'C) A light pass that takes some room echo off', 'E-untreated': 'D) The lav as recorded (rumble filter only)', 'F-chain-default': 'E) The automatic default (tone match plus a gate between words)'}
voice = ''.join(f"""<div class=vo><b>{E(names[k])}</b><br><audio controls muted preload="none" src="{cp(f'{B}/audio/opts/{k}.m4a', f'voice_{k}.m4a')}"></audio></div>"""
                for k in ['B-balanced-bass', 'A-balanced', 'D-less-room', 'E-untreated', 'F-chain-default'] if k in vo)
key = ''.join(btn(cp(f'{B}/key/CAL{n} {l}.mp4', f'key_cal{n}_{l}.mp4'), f'key test {n}, {l} backdrop') + ' ' for n in (1, 2) for l in ('pale', 'navy', 'pink'))
ai = f"""<img class=wide src="{cp(f'{B}/ai_images/ladder_contact.jpg', 'ladder_contact.jpg')}">""" + '<div class=row8>' + ''.join(
    f"""<a href="{cp(f'{B}/ai_images/L{l:02d}.png', f'L{l:02d}.png')}" target=_blank><img src="media/L{l:02d}.png"><br>{l}%</a>""" for l in (35, 30, 25, 20, 15, 12, 10, 8)) + '</div>'
real = f"""<img class=half src="{cp(f'{B}/broll/R08_photo.jpg', 'R08_photo.jpg')}">"""
KIND = {'ladder': 'Picture row (full screen)', 'fact': 'Picture card (full screen)', 'lt': 'Lower third', 'l3': 'Left-third card', 'broll': 'B-roll (full screen)', 'phone': 'App demo beside you'}
cards = ''
for p in P:
    c = cp(f'{R1}/review/context/{p["id"]}-context - REVIEW 540p.mp4', f'ctx_{p["id"]}.mp4'); st = cp(f'{R1}/review/context/{p["id"]}.jpg', f'ctx_{p["id"]}.jpg')
    copy = p.get('heading') or p.get('topic') or ''
    if p['kind'] == 'lt': copy = f"{p['topic']}: " + ' '.join(x for x, _ in p['parts'])
    if p['kind'] == 'l3': copy = p['heading'] + ': ' + ' / '.join(p['points'])
    if p['kind'] == 'fact': copy = f"{p['eyebrow'][0]}: " + ' '.join(x for x, _ in p['headline']) + (f" ({p['detail'][0]})" if p.get('detail') else '')
    if p['kind'] == 'broll': copy = ', '.join(p['src'] if isinstance(p['src'], list) else [p['src']])
    if p['kind'] == 'ladder': copy = 'The eight AI pictures' + (', ' + ' / '.join(b['s'] for b in p['band'][:1]) if p.get('band') else '')
    note = D.get('notes', {}).get(p['id'], p.get('why', ''))
    cards += f"""<div class=card>{f'<img src="{st}">' if st else '<div class=ph>rendering</div>'}<div><b>{p['id']}</b> {E(KIND.get(p['kind'], p['kind']))} · {mmss(p['a'])}-{mmss(p['b'])}</div>
<div class=cp>{E(copy)}</div>{f'<div class=nt>{E(note)}</div>' if note else ''}{btn(c, f"{p['id']} in context") if c else '<i>context clip rendering</i>'}
<details><summary>What you say</summary><p class=mute>before: {E(said(p['a'] - 4, p['a']))}</p><p><b>under it: {E(said(p['a'], p['b']))}</b></p><p class=mute>after: {E(said(p['b'], p['b'] + 4))}</p></details></div>"""
dec = ''.join(f'<li>{E(d)}</li>' for d in D['decisions']); did = ''.join(f'<li>{E(d)}</li>' for d in D['decided'])
reply = '\n'.join(f'{i + 1}. ' for i in range(len(D['decisions'])))
page = f"""<!doctype html><html><head><meta charset=utf-8><title>Body Fat % LFC R1</title><meta name=viewport content="width=device-width,initial-scale=1">
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,sans-serif;margin:0;padding:16px}}main{{max-width:1100px;margin:auto}}
h1{{font-size:26px}}h2{{color:var(--acc);font-size:20px;margin-top:34px;border-top:1px solid var(--line);padding-top:16px}}
button{{background:#18324d;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:6px 10px;margin:3px 2px;cursor:pointer}}
.card,.opt,.vo{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.card img,.opt img{{width:100%;border-radius:8px}}.cp{{margin:6px 0;font-weight:600}}.nt,.mute{{color:var(--mute);font-size:14px}}.ph{{height:160px;display:grid;place-items:center;color:var(--mute)}}
.opts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}.wide{{width:100%;border-radius:8px}}.half{{max-width:420px;width:100%;border-radius:8px}}
.row8{{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;text-align:center}}.row8 img{{width:100%;border-radius:6px}}.row8 a{{color:var(--ink);text-decoration:none}}
#dock{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px;margin:14px 0}}#dock video{{width:100%;border-radius:8px;background:#000}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:62vw}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
textarea{{width:100%;height:220px;background:#0b1828;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:10px;font:15px/1.5 monospace}}
a{{color:var(--acc)}}</style></head><body>
<div id=dock><div id=nowp class=mute>Player: press any Play button</div><video id=pv controls muted preload="none"></video></div><main>
<h1>What Every Body Fat Percentage Looks Like (On Me): round 1</h1>
<p>{E(D['intro'])}</p><p class=mute><b>Already locked (not asked):</b> {E(D['locked'])}</p>
<h2>Your decisions ({len(D['decisions'])})</h2><ol>{dec}</ol>
<h2>1. The first minute (draft)</h2><p>{btn(fm, 'First minute, 0:00-1:02')} {f'<a href="{fm1080}">1080p file</a>' if fm1080 else ''}</p><p class=mute>{E(D['fm_note'])}</p>
<h2>2. Colour (same two moments, three grades)</h2><div class=opts>{col}</div>
<h2>3. Voice (the same 26 seconds, level matched)</h2><div class=opts>{voice}</div><p class=mute>{E(D['voice_note'])}</p>
<h2>4. The eight AI pictures of you</h2>{ai}<p class=mute>{E(D['ai_note'])}</p>
<h2>5. "Me today" real photo (after the 8% card)</h2>{real}
<h2>The chroma key (house standard, measured)</h2><p>{key}</p><p class=mute>{E(D['key_note'])}</p>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Every graphic, picture card and clip, in order</h2><div class=grid>{cards}</div>
<h2>Your reply</h2><textarea id=rep>{E(reply)}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value)">Copy</button>
</main><script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></body></html>"""
open(f'{OUT}/index.html', 'w').write(page)
missing = [p['id'] for p in P if not os.path.exists(f'{R1}/review/context/{p["id"]}-context - REVIEW 540p.mp4')]
print('page written;', len(P), 'items;', 'context missing:', ', '.join(missing) or 'none')
