"""DS-40 R6 review page: the four graphics moving in their real context, the edit plan, and the whole Short as a draft."""
from pathlib import Path
import json, subprocess, html, shutil
import numpy as np
from PIL import Image
W = Path('/Volumes/Expansion/_edit_work/ds40/r6'); Q = W / 'review'; M = Q / 'media'
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
NAME = 'Fat 90 Year Old SFC R6'
E = html.escape
FPS = 30000 / 1001
M.mkdir(parents=True, exist_ok=True)
P = json.load(open(W / 'plan.json')); N = json.load(open(W / 'notes_r6.json'))
DRAFT = W / 'renders/DS40 R6 draft.mp4'
FULL = f'{NAME} - full Short draft.mp4'
shutil.copy(DRAFT, M / FULL)
shutil.copy(W / 'renders/DS40 R6 pink.mp4', M / f'{NAME} - key check over pink.mp4')


def clip(name, a, b):
    out = M / f'{NAME} - {name}.mp4'
    subprocess.run([F, '-v', 'error', '-y', '-ss', f'{a:.3f}', '-i', str(DRAFT), '-t', f'{b - a:.3f}', '-c:v', 'libx264', '-crf', '16',
                    '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(out)], check=True)
    return out.name


def stills(tag, times):
    sel = '+'.join(f"eq(n\\,{int(round(t * FPS))})" for t in times)
    p = subprocess.run([F, '-v', 'error', '-i', str(DRAFT), '-vf', f'select={sel},scale=in_color_matrix=bt709:in_range=tv',
                        '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    names = []
    for i, fr in enumerate(np.frombuffer(p, np.uint8).reshape(-1, 1920, 1080, 3)):
        n = f'{tag}{i}.jpg'; Image.fromarray(fr).resize((432, 768), Image.Resampling.LANCZOS).save(M / n, quality=90); names.append(n)
    return names


ts = lambda t: f'{int(t // 60)}:{t % 60:04.1f}'
sec = []
for g in N['graphics']:
    c = clip(g['clip_name'], *g['context'])
    st = stills(g['id'], g['stills'])
    figs = ''.join(f"<figure><img src='media/{E(n)}'><figcaption>{ts(t)}</figcaption></figure>" for n, t in zip(st, g['stills']))
    sec.append(f"""<section class="g"><h3>{E(g['title'])} <small>{ts(g['t0'])} to {ts(g['t1'])}</small></h3>
<p>{E(g['what'])}</p><div class="row"><div class="vid"><video controls playsinline preload="metadata" src="media/{E(c)}"></video>
<small>In context, {ts(g['context'][0])} to {ts(g['context'][1])}, with sound</small></div><div class="st">{figs}</div></div></section>""")
card_st = stills('K', [(s['f0'] + s['f1']) / 2 / FPS for s in P['card']])
cards = ''.join(f"<figure><img src='media/{E(n)}'><figcaption>{ts(s['f0'] / FPS)} to {ts(s['f1'] / FPS)}: {E(s['what'])}</figcaption></figure>"
                for n, s in zip(card_st, P['card']))
mv = clip('the move into the layout', 16.5, 25.0)
li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
reply = '\n'.join(f'{i + 1}. ' for i in range(len(N['questions'])))
plan_rows = ''.join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in N['plan'])
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(NAME)}</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1150px;margin:0 auto;padding:16px 16px 80px}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
video{{width:100%;max-height:80vh;background:#000;border-radius:8px}}.top{{display:grid;grid-template-columns:minmax(0,380px) 1fr;gap:20px;align-items:start}}
.row{{display:grid;grid-template-columns:minmax(0,300px) 1fr;gap:14px;align-items:start}}.st,.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}}
img{{width:100%;border-radius:6px;display:block}}figure{{margin:0}}figcaption,small{{color:var(--mut);font-size:13px}}section.g{{background:var(--card);border-radius:10px;padding:10px 14px;margin:14px 0}}
table{{border-collapse:collapse;width:100%}}td{{border-bottom:1px solid #2a3644;padding:6px 8px;vertical-align:top}}td:first-child{{white-space:nowrap;color:var(--acc)}}
button{{margin:6px 6px 6px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}a{{color:var(--acc)}}
textarea{{width:100%;height:120px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}
@media (max-width:700px){{.top,.row{{grid-template-columns:1fr}}}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 6 · DS-40 · the four graphics and the edit plan, shown inside a full draft</p>
<h1>Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right.</h1>
<div class="top"><div><video controls playsinline preload="metadata" src="media/{E(FULL)}"></video><small>The whole Short as it stands ({P['dur_s']:.1f} s). Also in Videos to Review for VLC.</small></div>
<div><p>{N['intro']}</p><h2>Your decisions</h2><ol>{li(N['questions'])}</ol></div></div>
<h2>The four graphics, each moving in its place</h2>{''.join(sec)}
<h2>The edit plan</h2><table>{plan_rows}</table>
<h3>The move into the layout</h3><div class="row"><div class="vid"><video controls playsinline preload="metadata" src="media/{E(mv)}"></video></div>
<p>{E(N['move'])}</p></div>
<h3>Silent Bill Maher footage in the card</h3><p>{E(N['card'])}</p><div class="cards">{cards}</div>
<h2>What I decided (overrule anything)</h2><ul>{li(N['decided'])}</ul>
<h2>Checks</h2><ul>{li(N['checks'])}</ul>
<p><small>Key check over saturated pink (shows any see-through spot): <a href="media/{E(NAME)} - key check over pink.mp4">open</a></small></p>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main></body></html>"""
(Q / 'index.html').write_text(page)
print('PAGE written', Q / 'index.html')
