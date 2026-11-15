"""DS-107 R2 review page (later-round format, VIDEO-RULES 2026-10-10): the film on top, the revision list with exact timestamps and short
watch ranges, the opener at 25 % (in the film) beside the 21 % alternate, one decision, a reply box. Players never autoplay (review_server.py
injects review_player.js).   python3 page_r2.py"""
from pathlib import Path
import json, subprocess, html
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True)
F = str(R/'Media/video_edit/bin/ffmpeg'); NAME = 'Metabolism Not The Reason SFC R2'; src = W/'main'/'review'; E = html.escape
for f in (f'{NAME}.mp4', f'{NAME}.srt', 'opener-25pct.mp4', 'opener-21pct.mp4'):
    p = Q/f
    if p.is_symlink() or p.exists(): p.unlink()
    p.symlink_to(src/f)
(Q/'context').mkdir(exist_ok=True)
subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', '46.0', '-i', str(src/f'{NAME}.mp4'), '-t', '8.0', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', str(Q/'context'/'b7-46-54.mp4')], check=True)
subprocess.run([F, '-nostdin', '-v', 'error', '-y', '-ss', '1.0', '-i', str(src/f'{NAME}.mp4'), '-frames:v', '1', '-vf', 'scale=540:960', '-q:v', '3', str(Q/'poster.jpg')], check=True)
rev = json.load(open(Q/'review.json')) if (Q/'review.json').exists() else {}
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Metabolism SFC R2</title>
<style>:root{{--bg:#0f141b;--fg:#e8eef5;--mut:#9fb0c3;--acc:#5cc8ff;--card:#18212c;--rec:#3ddc97}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,sans-serif}}
main{{max-width:1100px;padding:16px 16px 80px;margin:0 auto}}h2{{border-bottom:1px solid #2a3644;padding-bottom:4px;margin-top:28px}}.badge{{color:var(--acc);font-weight:600}}
.top{{display:grid;grid-template-columns:minmax(0,400px) 1fr;gap:20px;align-items:start}}@media(max-width:760px){{.top{{grid-template-columns:1fr}}}}
video{{width:100%;background:#000;border-radius:8px;max-height:78vh}}.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}@media(max-width:560px){{.two{{grid-template-columns:1fr}}}}
.card{{background:var(--card);border-radius:8px;padding:10px}}small{{color:var(--mut)}}textarea{{width:100%;height:110px;background:#0b1016;color:var(--fg);border:1px solid #2a3644;border-radius:6px}}
button{{background:var(--acc);color:#002;border:0;border-radius:6px;padding:6px 10px;font-weight:600;cursor:pointer}}a{{color:var(--acc)}}li{{margin:6px 0}}</style></head><body><main>
<p class="badge">CONTENT · Dedicated Short (SFC) · Round 2 · DS-107 · edited on the M2</p>
<h1>Your Metabolism Is Not The Reason You're Fat</h1>
<div class="top"><div><p style="font-size:20px;font-weight:700;color:var(--rec);margin:0">63.9 s</p>
<video controls playsinline preload="metadata" muted poster="poster.jpg" src="{E(NAME)}.mp4"></video>
<p><a href="{E(NAME)}.mp4">Full quality (1080x1920)</a> · <a href="{E(NAME)}.srt">Captions</a></p></div>
<div><h3>What changed (2 spots; watch only these)</h3><ol>
<li><b>0:00 to 0:04.4, the jump rope opener now plays 25 % faster</b> (your words: "accelerate this by 25%"). Picture only: your voice, captions and the rest of the Short are exactly as you approved them. It starts a little earlier in the clip (1.6 s instead of 2.0 s) so every step stays the correct one-foot-at-a-time skip. Watch 0:00 to 0:06.</li>
<li><b>0:48.3 to 0:52.0, the second jump rope clip starts 0.2 s later inside the clip.</b> The faster opener now uses more of the same recording, so this keeps the two shots from showing the same moment twice. Watch 0:46 to 0:54.</li></ol>
<p>Locked from round 1: Balanced voice, colour A (house warm look), everything else in the film (checked frame by frame; the sound is bit-identical).</p>
<h3>Your decision (1)</h3><ol><li>Opener speed: <b>25 % faster (in the film, my pick: your first number)</b> or 21 % faster (you also said 21 %; the alternate is below)? Then approve, or tell me what to change.</li></ol>
<p><small>{E(rev.get('line', ''))}</small></p></div></div>
<h2>Opener: 25 % vs 21 % (same 6 seconds)</h2><div class="two">
<div class="card"><b>25 % faster (in the film)</b><video controls playsinline preload="none" muted src="opener-25pct.mp4"></video></div>
<div class="card"><b>21 % faster (alternate)</b><video controls playsinline preload="none" muted src="opener-21pct.mp4"></video></div></div>
<h2>The second jump rope clip in context (0:46 to 0:54)</h2><div class="card" style="max-width:400px"><video controls playsinline preload="none" muted src="context/b7-46-54.mp4"></video></div>
<h2>Checks</h2><ul>{''.join(f'<li>{E(x)}</li>' for x in rev.get('checks', []))}</ul>
<h2>Your reply</h2><textarea id="reply">Opener: 25 %
Approved / changes:
</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy reply</button>
</main></body></html>"""
(Q/'index.html').write_text(page); print('PAGE R2')
