"""DS-41 R2 review page (from DS-36 R2): the off-the-cuff Short only (Dan picked it), 1080p, plus the revision list with exact timestamps in this
film and short context clips around each change (VIDEO-RULES 2026-10-10). Text: review/notes.json.   python3 page_r2.py"""
from pathlib import Path
import json, subprocess, html, shutil
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True)
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
NAME = 'Kevin James Cheat SFC R2 - off the cuff'; O = W/'offcuff'; src = O/'review'
for suf in ('.mp4', ' - audio AB.mp4', '.srt'):
    a, b = src/f'{NAME}{suf}', Q/f'{NAME}{suf}'      # R2: real copies, refreshed on every run (the page mirrors to the M6; a stale or linked film would not)
    if a.exists() and (not b.exists() or b.is_symlink() or a.stat().st_size != b.stat().st_size or a.stat().st_mtime > b.stat().st_mtime):
        b.unlink(missing_ok=True); shutil.copy2(a, b)
notes = json.load(open(Q/'notes.json')); E = html.escape
edl = json.load(open(O/'edl.json')); END = edl['total_frames']/FPS; master = src/f'{NAME}.mp4'
def mmss(t): return f'{int(t//60)}:{t%60:04.1f}'
(Q/'context').mkdir(exist_ok=True); items = []
for i, ch in enumerate(notes['changes']):
    t = ch['t']; a0, b0 = max(0, t - 3.0), min(END, t + 3.0); clip = f'context/change{i+1}.mp4'
    subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', f'{a0:.3f}', '-i', str(master), '-t', f'{b0-a0:.3f}', '-vf', 'scale=540:960', '-c:v', 'libx264',
                    '-preset', 'fast', '-crf', '21', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(Q/clip)], check=True)
    items.append(f"<li><b>{mmss(t)}</b> (watch {mmss(a0)}-{mmss(b0)}): {E(ch['what'])} <button onclick=\"ctx({a0:.2f},{b0:.2f})\">Play</button> <a href=\"{clip}\">clip</a></li>")
subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', '6.0', '-i', str(master), '-frames:v', '1', '-vf', 'scale=540:960', '-q:v', '3', str(Q/'poster.jpg')], check=True)
li = lambda xs: ''.join(f'<li>{E(x)}</li>' for x in xs)
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kevin James Cheat R2</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--ok:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,Segoe UI,sans-serif}}
main{{max-width:900px;margin:0 auto;padding:16px 16px 80px}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:30px}}.badge{{color:var(--acc);font-weight:600}}
.film video{{width:100%;background:#000;border-radius:8px;display:block}}.len{{font-size:22px;font-weight:700;color:var(--ok);margin:4px 0}}
@media(min-width:760px){{main{{max-width:1100px;padding-right:348px}}.film{{position:fixed;right:16px;top:44px;width:300px}}.film video{{max-height:calc(100vh - 190px);object-fit:contain}}}}
@media(max-width:759px){{.film{{position:sticky;top:0;background:var(--bg);z-index:3;padding-bottom:6px}}.film video{{max-height:36vh;width:auto;max-width:100%;margin:0 auto}}}}
button{{margin-left:6px;background:var(--acc);color:#002;border:0;border-radius:6px;padding:4px 10px;font-weight:600;cursor:pointer}}
li{{margin:6px 0}}textarea{{width:100%;height:110px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}a{{color:var(--acc)}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 · DS-41 · off the cuff · locked reaction format (Bill Maher Codex R5)</p>
<h1>Kevin James Tried One Cheat Day A Week. It Wrecked His Diet.</h1><p>{E(notes['intro'])}</p>
<div class="film"><p class="len">{END:.1f} s</p><video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{E(NAME)}.mp4"></video>
<p><a href="{E(NAME)}.mp4">Full quality (1080x1920)</a> · <a href="{E(NAME)} - audio AB.mp4">Audio A/B</a> · <a href="{E(NAME)}.srt">Captions</a></p></div>
<h2>What changed in round 2 (times are in this film)</h2><ol>{''.join(items)}</ol>
<h2>What I decided (overrule anything)</h2><ul>{li(notes['decided'])}</ul>
<h2>Checks</h2><ul>{li(notes['checks'])}</ul>
<h2>Your reply</h2><textarea id="reply"></textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main><script>// R2 (side pane rule, 2026-11-14): ONE player, loaded at page load; a change's Play button plays its watch range in that player
let stopAt=null;const film=document.getElementById('film');film.addEventListener('timeupdate',()=>{{if(stopAt!==null&&film.currentTime>=stopAt){{film.pause();stopAt=null;}}}});
function ctx(a,b){{stopAt=null;film.currentTime=a;stopAt=b;film.play();}}</script></body></html>"""
(Q/'index.html').write_text(page); print('PAGE R2', round(END, 2), len(items))
