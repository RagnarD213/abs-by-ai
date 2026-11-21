"""DS-36 R2 review page: the off-the-cuff Short only (Dan picked it), 1080p, plus the revision list with exact timestamps in this
film and short context clips around each change (VIDEO-RULES 2026-10-10). Text: review/notes.json.   python3 page_r2.py"""
from pathlib import Path
import json, subprocess, html
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True)
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
NAME = 'Fat Shaming SFC R2 - off the cuff'; O = W/'offcuff'; src = O/'review'
for suf in ('.mp4', ' - audio AB.mp4', '.srt'):
    if (src/f'{NAME}{suf}').exists() and not (Q/f'{NAME}{suf}').exists(): (Q/f'{NAME}{suf}').symlink_to(src/f'{NAME}{suf}')
notes = json.load(open(Q/'notes.json')); E = html.escape
edl = json.load(open(O/'edl.json')); END = edl['total_frames']/FPS; master = src/f'{NAME}.mp4'
def mmss(t): return f'{int(t//60)}:{t%60:04.1f}'
(Q/'context').mkdir(exist_ok=True); items = []
for i, ch in enumerate(notes['changes']):
    t = ch['t']; a0, b0 = max(0, t - 3.0), min(END, t + 3.0); clip = f'context/change{i+1}.mp4'
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a0:.3f}', '-i', str(master), '-t', f'{b0-a0:.3f}', '-vf', 'scale=540:960', '-c:v', 'libx264',
                    '-preset', 'fast', '-crf', '21', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(Q/clip)], check=True)
    items.append(f"<li><b>{mmss(t)}</b> (watch {mmss(a0)}-{mmss(b0)}): {E(ch['what'])} <button onclick=\"ctx('{clip}')\">Play</button></li>")
subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', '6.0', '-i', str(master), '-frames:v', '1', '-vf', 'scale=540:960', '-q:v', '3', str(Q/'poster.jpg')], check=True)
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fat Shaming R2</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--ok:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,Segoe UI,sans-serif}}
main{{max-width:900px;margin:0 auto;padding:16px 16px 80px}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:30px}}.badge{{color:var(--acc);font-weight:600}}
.film video{{width:100%;max-width:420px;max-height:80vh;background:#000;border-radius:8px;display:block}}.len{{font-size:22px;font-weight:700;color:var(--ok);margin:4px 0}}
button{{margin-left:6px;background:var(--acc);color:#002;border:0;border-radius:6px;padding:4px 10px;font-weight:600;cursor:pointer}}
#ctxbox{{position:sticky;top:8px;background:var(--card);padding:8px;border-radius:8px;display:none;z-index:2}}#ctxbox video{{max-height:60vh;max-width:100%}}
li{{margin:6px 0}}textarea{{width:100%;height:110px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 · DS-36 · off the cuff · locked reaction format (Bill Maher Codex R5)</p>
<h1>Bill Maher Says Fat Shaming Should Come Back. He's Right.</h1><p>{E(notes['intro'])}</p>
<div class="film"><p class="len">{END:.1f} s</p><video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{E(NAME)}.mp4"></video>
<p><a href="{E(NAME)}.mp4">Full quality (1080x1920)</a> · <a href="{E(NAME)} - audio AB.mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions</a></p></div>
<div id="ctxbox"><video id="ctx" controls playsinline preload="metadata"></video><br><button onclick="document.getElementById('ctxbox').style.display='none';document.getElementById('ctx').pause()">Close</button></div>
<h2>What changed in round 2 (times are in this film)</h2><ol>{''.join(items)}</ol>
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply"></textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>function ctx(src){{const b=document.getElementById('ctxbox'),v=document.getElementById('ctx');b.style.display='block';v.src=src;b.scrollIntoView({{block:'nearest'}});}}</script></body></html>"""
(Q/'index.html').write_text(page); print('PAGE R2', round(END, 2), len(items))
