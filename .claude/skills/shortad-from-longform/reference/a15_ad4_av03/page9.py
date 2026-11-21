#!/usr/bin/env python3
"""THE ONE REVIEW PAGE for Ad 4's four formats (PRE-RENDER-APPROVAL.md "The review page"; handoff-20261001-ad4-other-formats:
Dan reviews the ad once, on one page). The four finished files on top, "Your decisions", "What I decided", the colour
proof against Muhammad's own frames, then every re-laid shot in timeline order, three per row, each with its 9:16 and 1:1
still and a "Play it moving, in context" button per format feeding ONE docked player (it seeks inside the review copy, so
nothing extra is rendered), the checks, and one reply box.

  python3 page9.py [--media]      -> review/index.html     serve: _shared/review_server.py 8814 review
page_extra.json carries {"decisions", "decided", "checks", "reply"}.
"""
import html, json, os, subprocess, sys
import numpy as np
from PIL import Image
sys.path.insert(0, '.')
import beats as B
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = B.FPS; E = html.escape
OUT = 'review'; os.makedirs(f'{OUT}/stills', exist_ok=True); os.makedirs(f'{OUT}/colour', exist_ok=True)
X = json.load(open('page_extra.json'))
FILES = [('v', 'ad4_9x16.mp4', '9:16 full length', 'stop wasting money on supplements | claude | 9x16 | ad 4'),
         ('vc', 'cut/ad4_9x16_59s.mp4', '9:16, 59 seconds or under', 'stop wasting money on supplements | claude | 9x16 59s | ad 4'),
         ('s', 'ad4_1x1.mp4', '1:1 full length', 'stop wasting money on supplements | claude | 1x1 | ad 4'),
         ('sc', 'cut_sq/ad4_1x1_59s.mp4', '1:1, 59 seconds or under', 'stop wasting money on supplements | claude | 1x1 59s | ad 4')]
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def dur(p):
    return float(subprocess.run([FF.replace('ffmpeg', 'ffprobe'), '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip())
# id, n0, n1, still frame, what it is, 9:16 verdict, 1:1 verdict, note
I = [
 ('C01', 85, 262, 150, 'AI robot clip, shot 1', 'fill', 'whole', 'Portrait clip. In the square its action runs top to bottom (head, arm, bottles, trash can), so the whole clip is shown in a card; a square crop loses the trash can.'),
 ('C02', 262, 437, 380, 'AI robot clip, shot 2', 'fill', 'fill', 'The robot holding the bottle up fills both frames.'),
 ('C03', 437, 639, 560, 'Your real supplement stack (pan)', 'square', 'fill', 'The stack runs the whole width of the counter, so the vertical shows the centre square, as wide as the phone allows. It fills the square.'),
 ('C04', 928, 1267, 1200, 'Text screen 1', 'window', 'window', 'You above, his two points below, at his wording and pace.'),
 ('C05', 1307, 1477, 1400, 'Influencer with the shaker', 'whole', 'whole', 'His shaker is at the far left and his face right of centre. A card three quarters of the clip wide holds both; a full-screen crop or a square cuts the shaker in half.'),
 ('C06', 1754, 1827, 1790, 'Library', 'fill', 'fill', 'Nothing needed at the sides.'),
 ('C07', 2016, 2304, 2290, 'Text screen 2', 'window', 'window', ''),
 ('C08', 2488, 2713, 2700, 'Text screen 3', 'window', 'window', ''),
 ('C09', 3086, 3167, 3140, 'The tub label ("Proprietary Blends")', 'fill', 'fill', 'Vertical: pushed in on the tub so Muhammad\'s yellow PROPRIETARY BLENDS highlight sits above the caption line, not under it.'),
 ('C10', 3775, 3864, 3820, 'Pill bottles', 'fill', 'fill', ''),
 ('C11', 4186, 4219, 4210, 'Before: deck chair', 'fill', 'whole', 'The standard before picture. No label (before pictures carry none). Square: the whole photo, because a square crop loses your belly, which is the point of the picture.'),
 ('C12', 4219, 4251, 4240, 'Before: standing', 'whole', 'fill', 'The recentred version you approved as a before picture (the original cuts your hair and cheek at the photo edge). Vertical: the whole photo in a card, because a full-screen crop cuts the girl\'s face in half.'),
 ('C13', 4251, 4289, 4275, 'Before: on the ride', 'square', 'fill', 'A vertical crop would cut the girl beside you in half, so the vertical shows a square.'),
 ('C14', 4524, 4595, 4570, 'AI goal image', 'fill', 'whole', 'AI-GENERATED sits beside your head, measured clear of your face and abs. Square: the whole image at full height, so the caption sits on the shorts.'),
 ('C15', 4723, 4741, 4735, 'After picture 1', 'fill', 'whole', 'Label measured beside your head, same size and spot on all four. Square: each after picture whole at full height, so the caption line is on your shorts, not your abs.'),
 ('C16', 4741, 4759, 4752, 'After picture 2', 'fill', 'whole', ''),
 ('C17', 4759, 4777, 4770, 'After picture 3', 'fill', 'whole', 'Decision 5: a portrait from the pool shoot in place of his landscape park photo.'),
 ('C18', 4777, 4792, 4787, 'After picture 4', 'fill', 'whole', 'Decision 5: a studio portrait in place of his landscape flag photo.'),
 ('C19', 5145, 5238, 5215, 'App: generating', 'phone', 'phone', 'The phone is as large as fits.'),
 ('C20', 5351, 5435, 5420, 'App: download screen', 'phone', 'phone', 'Email form out of frame, as you approved on his cut.'),
 ('C21', 5435, 5534, 5510, 'Title card: YOU LOCK IN', 'graphic', 'graphic', ''),
 ('C22', 5534, 5704, 5660, 'App: supplement audit', 'phone', 'phone', ''),
 ('C23', 5704, 5912, 5890, 'Text screen 4', 'window', 'window', ''),
 ('C24', 6041, 6206, 6150, 'Audit results beside you', 'window', 'window', 'Vertical: you above (head and shoulders), his caption bar under your chin, the phone below as large as fits. Square: his own layout, the phone beside you.'),
 ('C25', 6282, 6391, 6350, 'Safety flags beside you', 'window', 'window', ''),
 ('C26', 6514, 6634, 6580, 'Supermarket', 'fill', 'fill', ''),
 ('C27', 6634, 6773, 6710, 'Meal prep (overhead)', 'square', 'fill', 'The containers spread across the table (your overhead salad table example), so the vertical shows the centre square.'),
 ('C28', 6836, 6909, 6880, 'AI goal image (second time)', 'fill', 'whole', ''),
]
SH = dict(fill='FILLS THE FRAME', square='CENTRE SQUARE', whole='SHOWN WHOLE (REASON BELOW)', phone='PHONE, AS LARGE AS FITS', window='YOU + TEXT', graphic='GRAPHIC')
def run(c): subprocess.run(c, check=True)
def frame(vid, n, out, w):
    run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{max(0, n/FPS - 1.0):.3f}', '-i', vid, '-vf', f"select='gte(t\\,{min(1.0, n/FPS):.4f})',scale={w}:-2", '-frames:v', '1', '-q:v', '3', out])
if '--media' in sys.argv:
    for key, src, _, name in FILES:
        rv = f'{OUT}/{name} REVIEW 540p.mp4'.replace(' | ', ' - ')
        if not os.path.exists(rv) or os.path.getmtime(rv) < os.path.getmtime(src):
            run([FF, '-nostdin', '-v', 'error', '-y', '-i', src, '-vf', 'scale=540:-2', '-c:v', 'h264_videotoolbox', '-b:v', '2600k', '-pix_fmt', 'yuv420p',
                 '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'copy', '-movflags', '+faststart', rv])
        frame(src, 60, f'{OUT}/stills/poster_{key}.jpg', 540)
    for id_, n0, n1, sn, *_ in I:
        frame('ad4_9x16.mp4', sn, f'{OUT}/stills/{id_}_v.jpg', 405); frame('ad4_1x1.mp4', sn, f'{OUT}/stills/{id_}_s.jpg', 405)
    # colour proof: Muhammad's frame (read as BT.709, the way a player shows it) beside ours, the same instant, his frame cropped to our window
    C = json.load(open('crop.json'))['frames']
    for k, n in enumerate((700, 3300, 5000)):
        x0, y0, w, h = C[str(n)]
        def raw(v, W, H):
            b = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', v, '-vf', f"select='eq(n\\,{n})',scale=in_color_matrix=bt709:in_range=tv", '-fps_mode', 'passthrough', '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
            return Image.fromarray(np.frombuffer(b, np.uint8).reshape(H, W, 3))
        his = raw('reference.mp4', 1920, 1080).crop((int(x0), int(y0), int(x0+w), int(y0+h))).resize((405, 720), Image.LANCZOS)
        ours = raw('ad4_9x16.mp4', 1080, 1920).resize((405, 720), Image.LANCZOS)
        sh = Image.new('RGB', (820, 720), (7, 18, 33)); sh.paste(his, (0, 0)); sh.paste(ours, (415, 0)); sh.save(f'{OUT}/colour/c{k}.jpg', quality=92)
    print('media ok')
revs = {key: f'{name} REVIEW 540p.mp4'.replace(' | ', ' - ') for key, _, _, name in FILES}
players = ''.join(f"""<article><h3>{E(lab)}</h3><video controls preload="none" playsinline poster="stills/poster_{key}.jpg" src="{E(revs[key])}"></video>
<div class="copy">{mmss(dur(src))} · <a href="masters/{E(name)}.mp4">full-quality file</a></div></article>""" for key, src, lab, name in FILES)
cards = []
for id_, n0, n1, sn, what, v9, v1, note in I:
    t0, t1 = n0/FPS, n1/FPS
    cards.append(f"""<article id="{id_}"><h3>{id_} <span class="tag">{E(what)}</span> <span class="small">{mmss(t0)} to {mmss(t1)}</span></h3>
<div class="pair"><a href="stills/{id_}_v.jpg"><img loading="lazy" src="stills/{id_}_v.jpg"></a><a href="stills/{id_}_s.jpg"><img loading="lazy" src="stills/{id_}_s.jpg"></a></div>
<button onclick="play('v',{max(0, t0-3):.2f},'{id_} 9:16')">Play 9:16 in context</button> <button onclick="play('s',{max(0, t0-3):.2f},'{id_} 1:1')">Play 1:1 in context</button>
<div class="copy"><span class="shape {v9}">9:16 {SH[v9]}</span> <span class="shape {v1}">1:1 {SH[v1]}</span>{('<br><i>' + E(note) + '</i>') if note else ''}</div></article>""")
li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ad 4 - vertical, square and both 59s cuts - round 1</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px;margin-top:40px}}p,li{{color:#bdd0e4}}a{{color:#8fd0ff}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}.four{{grid-template-columns:repeat(4,minmax(0,1fr))}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black;display:block}}
.pair{{display:grid;grid-template-columns:9fr 16fr;gap:8px;align-items:start}}h3{{margin:0 0 8px;font-size:16px}}.tag{{font-weight:500;color:#9fd3ff}}.small{{font-size:13px;color:#8ea6bf;font-weight:400}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.shape{{display:inline-block;font-weight:800;font-size:11px;letter-spacing:.5px;padding:3px 8px;border-radius:7px;background:#1d5f8f;color:white;margin:2px 2px 2px 0}}.shape.fill{{background:#167a52}}.shape.whole,.shape.square{{background:#8a5a12}}.shape.window,.shape.graphic{{background:#44506a}}
#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b;margin-bottom:16px;text-align:center}}#dock video{{max-height:42vh;width:auto;max-width:100%;margin:auto}}
@media(min-width:1500px){{body{{padding-right:min(30vw,520px)}}#dock{{position:fixed;top:16px;right:16px;width:calc(min(30vw,520px) - 40px);max-height:calc(100vh - 32px);box-sizing:border-box;margin:0;box-shadow:0 8px 40px #000a}}#dock video{{max-height:calc(100vh - 120px)}}}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:7px 10px;cursor:pointer;font-size:13px;margin-top:8px}}textarea{{width:100%;min-height:210px;background:#04101d;color:#edf5ff;border:1px solid #29425b;border-radius:10px;font:15px ui-monospace,monospace;padding:12px;box-sizing:border-box}}
@media(max-width:900px){{.grid,.four{{grid-template-columns:1fr}}}}</style>
<main><h1>Ad 4 "Stop Wasting Money On Supplements": vertical, square and both 59-second cuts</h1>
<p>{X['intro']}</p><p class="small"><b>Already locked, not reopened:</b> {X['locked']}</p>
<div id="dock"><div class="small" id="dockt">Press a "Play in context" button on any shot: it plays here, starting 3 seconds before the shot. Click the timeline to scrub.</div><video id="dv" controls preload="none" playsinline style="display:none"></video></div>
<h2>Your decisions ({len(X['decisions'])})</h2><ol>{li(X['decisions'])}</ol>
<h2>The four files</h2><div class="grid four">{players}</div>
<p class="small">{X.get('files_note', '')}</p>
<h2>What I decided (overrule anything)</h2><ol>{li(X['decided'])}</ol>
<h2>Colour: Muhammad's frame (left) and ours (right), the same instant</h2><div class="grid">{''.join(f'<article><a href="colour/c{k}.jpg"><img loading="lazy" src="colour/c{k}.jpg"></a><div class="copy">{c}</div></article>' for k, c in enumerate(X['colour']))}</div>
<h2>Every re-laid shot, in order (9:16 left, 1:1 right)</h2><div class="grid">{''.join(cards)}</div>
<h2>Checks</h2><ul>{li(X['checks'])}</ul>
<h2>Your reply</h2><textarea id="rep">{E(X['reply'])}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value);this.textContent='Copied'">Copy</button>
</main><script>
const SRC={{v:{json.dumps(revs['v'])},s:{json.dumps(revs['s'])}}};const dv=document.getElementById('dv');let cur=null;
function play(k,t,label){{document.getElementById('dockt').textContent=label+' (from 3 s before)';dv.style.display='block';
 const go=()=>{{dv.currentTime=t;dv.play()}};
 if(cur!==k){{cur=k;dv.src=SRC[k];dv.addEventListener('loadedmetadata',go,{{once:true}});dv.load()}}else go()}}
</script></html>"""
open(f'{OUT}/index.html', 'w').write(page)
assert '-' not in page and '–' not in page, 'an em or en dash is in the page'
print(f'{OUT}/index.html written, {len(I)} shots')
