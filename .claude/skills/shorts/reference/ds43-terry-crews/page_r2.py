"""DS-43 R2 review page: the off-the-cuff film, the revision list with timestamps in the new film and short watch ranges (VIDEO-RULES later-round
rule), context clips, decisions, checks, reply box. Players never autoplay: the review server injects the shared owner-handoff helper."""
from pathlib import Path
import json, subprocess, html
W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True); O = W/'offcuff'; S = O/'review'
F = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'; NAME = 'Terry Crews Fasting SFC R2 - off the cuff'
E = html.escape
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
for suf in ('.mp4', ' - REVIEW 540p.mp4', ' - audio AB.mp4', '.srt'):
    if (S/f'{NAME}{suf}').exists() and not (Q/f'{NAME}{suf}').exists(): (Q/f'{NAME}{suf}').symlink_to(S/f'{NAME}{suf}')
(Q/'context').mkdir(exist_ok=True)
REV = [('Your laptop is visible while you watch', '0:04.3-0:15.7', 3.0, 9.0, 8.0,
        "The real lid of your laptop now sits at the bottom of the frame through the whole watching section, in front of your hands, so you read as watching your screen. You stay the same size. The small corner shot in the first 4 seconds already showed the laptop."),
       ('Shirtless, jacked Terry right after the intro', '0:15.7-0:23.8', 14.7, 9.8, 17.0,
        "The Brooklyn Nine-Nine footage is gone. Above your reply, silent and horizontal: Terry shirtless in the gym ring, walking up to the lens, then abs and chest beside a heavy bag. The panel title now reads 'Terry Crews' because this footage isn't Business Insider's."),
       ('More flexing behind you on the physique line', '0:23.8-0:33.4', 22.8, 11.6, 28.8,
        "The panel stays up through 'not just a great actor, but he's got a great physique and he's maintained that...' with close chest, a flexed back on the pull-up bar, boxing gloves, a shirtless profile, pec pops landing on 'great physique', front on, and a double-biceps skyscraper shot from his Old Spice ads.")]
cards = ''
for i, (t, rng, a, d, st, txt) in enumerate(REV):
    ff(['-ss', a, '-i', S/f'{NAME}.mp4', '-t', d, '-vf', 'scale=540:960', '-c:v', 'libx264', '-preset', 'fast', '-crf', 21, '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', Q/f'context/rev{i}.mp4'])
    ff(['-ss', st, '-i', S/f'{NAME}.mp4', '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/f'context/rev{i}.jpg'])
    cards += f"""<div class="it"><img src="context/rev{i}.jpg"><b>{i + 1}. {E(t)}</b><small>{rng} in the new film</small><p>{E(txt)}</p><button onclick="ctx('context/rev{i}.mp4')">Play this change</button></div>"""
ff(['-ss', 20.0, '-i', S/f'{NAME}.mp4', '-frames:v', 1, '-vf', 'scale=540:960', '-q:v', 3, Q/'poster.jpg'])
n = json.load(open(Q/'notes.json')); li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Terry Crews Fasting R2</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1080px;padding:16px 16px 80px;margin:0 auto}}h1{{margin:.2em 0}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:32px}}.badge{{color:var(--acc);font-weight:600}}
.film video{{width:min(420px,100%);background:#000;border-radius:8px;max-height:80vh}}.q{{font-size:20px;font-weight:700;background:var(--card);padding:12px;border-radius:8px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}}}
.it{{background:var(--card);border-radius:8px;padding:8px;display:flex;flex-direction:column;gap:4px}}.it img{{width:100%;border-radius:6px}}.it p{{margin:2px 0;color:var(--mut)}}small{{color:var(--acc);font-weight:600}}
button{{margin:4px 0;background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}#ctxbox{{position:sticky;top:8px;background:var(--card);padding:8px;border-radius:8px;display:none;z-index:2}}#ctxbox video{{max-height:60vh;max-width:100%}}
textarea{{width:100%;height:120px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 · DS-43 · off the cuff · 77.3 s</p>
<h1>Terry Crews Doesn't Eat Until 2 PM. He's Right.</h1><p>{E(n['intro'])}</p>
<p class="q">Your one call: is round 2 approved? If yes, I'll write the setup handoff (covers, then scheduling).</p>
<div class="film"><video controls playsinline preload="metadata" poster="poster.jpg" src="{E(NAME)} - REVIEW 540p.mp4"></video>
<p><a href="{E(NAME)}.mp4">Full quality (1080x1920)</a> · <a href="{E(NAME)} - audio AB.mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions</a></p></div>
<h2>What changed (you only need to watch 0:03 to 0:34)</h2>
<div id="ctxbox"><video id="ctx" controls playsinline preload="metadata"></video><br><button onclick="document.getElementById('ctxbox').style.display='none';document.getElementById('ctx').pause()">Close</button></div>
<div class="grid">{cards}</div>
<h2>What I decided (overrule anything)</h2><ul>{li(n['decided'])}</ul>
<h2>Checks</h2><ul>{li(n['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply"></textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src){{const b=document.getElementById('ctxbox'),v=document.getElementById('ctx');b.style.display='block';v.src=src;b.scrollIntoView({{block:'nearest'}});}}</script></body></html>"""
(Q/'index.html').write_text(page); print('PAGE ok')
