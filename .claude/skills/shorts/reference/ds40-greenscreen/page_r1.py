"""DS-40 R1 review page: green screen key, colour and voice only (Dan asked for a 10 s sample before anything else).
Builds stills and close-ups from the RENDERED sample files, then writes review/index.html. Notes: review/notes.json."""
from pathlib import Path
import json, subprocess, html, shutil
from PIL import Image
W = Path('/Volumes/Extreme/_edit_work/ds40/r1'); Q = W/'review'
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
NAME = 'Fat 90 Year Old SFC R1'
E = html.escape
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
def still(src, t, out):
    ff(['-ss', t, '-i', src, '-frames:v', 1, '-vf', 'scale=in_color_matrix=bt709:in_range=tv,format=rgb24', out])
notes = json.load(open(Q/'notes.json'))
LOOKS = [('B_warmvivid', 'B: Warm Vivid'), ('A_natural', 'A: Natural'), ('C_bold', 'C: Bold Contrast')]
MOM = [('2.0', 'moment 1 (0:02)'), ('6.6', 'moment 2 (0:06.6)')]
(Q/'stills').mkdir(exist_ok=True); (Q/'edges').mkdir(exist_ok=True)
for k, _ in LOOKS:
    for t, _ in MOM:
        p = Q/f'stills/{k}-{t}.png'; still(Q/f'colour/sample {k}.mp4', t, p)
        Image.open(p).resize((540, 960)).save(Q/f'stills/{k}-{t}.jpg', quality=90)
# approved references from the same camera / the house target
for nm, src in [('ref-ro25', W/'colref/ro25_20.png'), ('ref-muhammad', W/'colref/muh_8.png')]:
    Image.open(src).convert('RGB').resize((960, 540)).save(Q/f'stills/{nm}.jpg', quality=90)
# edge close-ups at 2x from the delivered pixels (blue sample and pale key check)
pale = Q/'colour/key check on pale backdrop.mp4'; blue = Q/'colour/sample B_warmvivid.mp4'
CROPS = notes['edge_crops']   # name -> [t, x0, y0, x1, y1, caption]
edge_html = []
for nm, (t, x0, y0, x1, y1, cap) in CROPS.items():
    for tag, src in [('blue', blue), ('pale', pale)]:
        p = Q/f'edges/{nm}-{tag}.png'; still(src, t, p)
        im = Image.open(p).crop((x0, y0, x1, y1)); im = im.resize((im.width * 2, im.height * 2), Image.Resampling.NEAREST)
        im.save(Q/f'edges/{nm}-{tag}.jpg', quality=94); p.unlink()
    edge_html.append(f"<div class='edge'><h4>{E(cap)}</h4><div class='two'><img loading='lazy' src='edges/{nm}-blue.jpg'><img loading='lazy' src='edges/{nm}-pale.jpg'></div>"
                     f"<small>Shown at 2x, exact output pixels at {E(str(t))} s. Left: over the blue field. Right: over a pale backdrop (key check only).</small></div>")
sample = 'DS40 R1 sample - Warm Vivid colour, house voice.mp4'
cols = ''.join(f"""<div class="opt{' rec' if i == 0 else ''}"><h3>{E(lab)}{' · RECOMMENDED, in the sample' if i == 0 else ''}</h3>
<div class="three">{''.join(f'<figure><img loading="lazy" src="stills/{k}-{t}.jpg"><figcaption>{E(mlab)}</figcaption></figure>' for t, mlab in MOM)}</div>
<p>{E(notes['colour_desc'][k])}</p><button onclick="ctx('colour/sample {k}.mp4','{E(lab)} moving, with sound')">Play {E(lab)} moving</button>
<small> Skin measured: {E(notes['colour_nums'][k])}</small></div>""" for i, (k, lab) in enumerate(LOOKS))
voices = ''.join(f"""<div class="opt{' rec' if v['key'] == notes['voice_pick'] else ''}"><h3>{E(v['name'])}{' · RECOMMENDED, in the sample' if v['key'] == notes['voice_pick'] else ''}</h3>
<audio controls preload="none" src="voice/{v['key']}.m4a"></audio><p>{E(v['desc'])}</p><small>{E(v['listen'])}</small></div>""" for v in notes['voices'])
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
reply = '\n'.join(f'{i+1}. ' for i in range(len(notes['questions'])))
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(NAME)}</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1100px;padding:16px 16px 80px;margin-right:420px}}@media(max-width:1100px){{main{{margin-right:0}}#side{{position:static!important;width:auto!important}}}}
h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
#side{{position:fixed;right:16px;top:16px;width:380px}}#side video{{width:100%;background:#000;border-radius:8px;max-height:72vh}}
.opt{{background:var(--card);border-radius:8px;padding:10px;margin:12px 0;border:2px solid transparent}}.opt.rec{{border-color:var(--rec)}}.opt h3{{margin:.2em 0}}.rec h3{{color:var(--rec)}}
.three{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;max-width:620px}}.three img,.refs img{{width:100%;border-radius:6px;display:block}}figure{{margin:0}}figcaption{{color:var(--mut);font-size:13px}}
.refs{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.edge{{background:var(--card);border-radius:8px;padding:10px;margin:12px 0}}.two{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.two img{{width:100%;border-radius:4px}}
audio{{width:100%}}button{{margin:6px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}
textarea{{width:100%;height:120px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}small{{color:var(--mut)}}</style></head><body>
<aside id="side"><video id="film" controls playsinline preload="metadata" src="{E(sample)}"></video>
<p id="now" class="badge">Playing: the 9 second sample (recommended colour and voice)</p>
<button onclick="ctx('{E(sample)}','the sample (recommended)')">Recommended sample</button>
<button onclick="ctx('colour/key check on pale backdrop.mp4','key check on a pale backdrop')">Key check on pale</button>
<p><a href="voice/audio AB - reference then house voice.mp4">Audio A/B: Muhammad's reference voice, then ours</a></p></aside>
<main><p class="badge">CONTENT · Dedicated Short (SFC) · Round 1 · DS-40 · first green screen video</p>
<h1>Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right.</h1>
<p>{E(notes['intro'])}</p>
<h2>Your decisions ({len(notes['questions'])})</h2><ol>{li(notes['questions'])}</ol>
<h2>The sample</h2><p>{E(notes['sample_desc'])}</p>
<h2>1. Chroma key: close-ups of the hardest edges</h2><p>{E(notes['key_intro'])}</p>{''.join(edge_html)}
<h2>2. Colour options</h2><p>{E(notes['colour_intro'])}</p>{cols}
<h3>Approved references</h3><div class="refs"><figure><img src="stills/ref-ro25.jpg"><figcaption>I'm 41. I Wasted My Life (approved, same camera, 10/15 studio set)</figcaption></figure>
<figure><img src="stills/ref-muhammad.jpg"><figcaption>Muhammad, This Picture Got Me Abs (house colour target)</figcaption></figure></div>
<h2>3. Voice options (same 30 seconds, level matched)</h2><p>{E(notes['voice_intro'])}</p>{voices}
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src,label){{const v=document.getElementById('film');v.src=src;v.play();document.getElementById('now').textContent='Playing: '+(label||src);}}</script></body></html>"""
(Q/'index.html').write_text(page)
print('PAGE written', Q/'index.html')
