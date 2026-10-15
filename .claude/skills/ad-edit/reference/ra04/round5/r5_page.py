#!/usr/bin/env python3
"""RA-04 round 5 review page -> <delivery>/review-r5/ (index.html + 540p copies + the A/B + the two stills).
usage: python3 round5/r5_page.py"""
import os, shutil, subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
D = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/top 3 tips for getting abs - RA-04"
OUT = f"{D}/review-r5"; os.makedirs(OUT, exist_ok=True)
for a in ("9x16", "16x9"):
    shutil.copy(f"{D}/top 3 tips for getting abs | REVIEW 540p {a} | RA-04.mp4", f"{OUT}/ra04_r5_{a}.mp4")
shutil.copy(f"{D}/top 3 tips for getting abs | AB audio ref-vs-ours 9x16 | RA-04.mp4", f"{OUT}/ra04_r5_audio_ab.mp4")
from PIL import Image
for src, dst in (("round5/before_white_man_45.png", "before.jpg"), ("round5/after_white_man.jpg", "after.jpg")):
    im = Image.open(src).convert("RGB"); im.thumbnail((640, 800)); im.save(f"{OUT}/{dst}", quality=88)
for a, t, name in (("16x9", 4.0, "frame16_gen.jpg"), ("16x9", 8.0, "frame16_lock.jpg")):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", f"{D}/top 3 tips for getting abs | claude | {a} | RA-04.mp4",
                    "-frames:v", "1", "-vf", "scale=960:-2", f"{OUT}/{name}"], check=True)
ROWS = [("1", "0:01 to 0:11", "0:03.2 to 0:06.8: a white man's real generation in the app replaces you on camera. His before photo goes through "
         "the live absbyai.com generator (the scan running down him), then a hard cut to his AI picture on the app's result screen. The TIP 1 "
         "strip stays up, so the phone sits above it."),
        ("6.5", "0:06.8 to 0:09.9", "The lock-screen phone now shows his AI picture instead of yours (same phone, same glare, his picture held still on the screen)."),
        ("54", "0:54 to the end", "The ending is 0.97 s shorter: it now stops 0.41 s after \"app.\" on your held smile (0:57.9, was 0:58.9)."),
        (None, "everything else", "Unchanged from round 4: the Asian demo man's app cards (0:12.2 to 0:17.9) and analysis card (0:25 to 0:31), every "
         "other shot, graphic and caption, the voice and the music.")]
rows = "".join(f'<tr><td>{f"<a class=t data-t={t}>{w}</a>" if t else w}</td><td>{x}</td></tr>' for t, w, x in ROWS)
DECIDED = ["<b>His before photo is AI-generated</b> (Codex): Pexels had no ordinary heavier white man standing facing the camera. It carries "
           "the AI-GENERATED label for the whole card. I gave it extra sky above his head before generating, because the app trims photos to "
           "4:5 and the first result cut his hair at the top edge.",
           "<b>His AI picture is a real generation</b> in the live app (Male, Heavier, Ripped), same man before and after. The app's own "
           "before/after screen was hidden on the page before generating, so it never appears.",
           "The 16:9 phone is smaller than the other app cards (644 px tall), because it has to end above the TIP 1 strip and the captions lifted over it.",
           "The ending stops on your held smile, not on black or a fade."]
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Top 3 Tips AD R5</title>
<style>
:root{{--bg:#f6f8fb;--fg:#14202e;--mute:#5b6b7d;--card:#fff;--line:#dde4ec;--accent:#2b6cdf}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0e141b;--fg:#e8eef5;--mute:#9aabbd;--card:#16202b;--line:#26323f;--accent:#6aa5ff}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,system-ui,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px 60px}}h1{{font-size:24px;margin:0 0 4px}}h2{{font-size:18px;margin:28px 0 10px}}
.sub{{color:var(--mute);margin:0 0 18px}}.row{{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;max-width:100%;box-sizing:border-box}}
video,img{{display:block;border-radius:8px;background:#000;max-width:100%}}.v916{{width:300px}}.v169{{width:640px}}.still{{width:260px}}.f16{{width:480px}}
table{{border-collapse:collapse;width:100%}}td,th{{border-top:1px solid var(--line);padding:8px 6px;text-align:left;vertical-align:top}}
th{{color:var(--mute);font-weight:600;font-size:13px}}a.t{{color:var(--accent);cursor:pointer;text-decoration:none;font-variant-numeric:tabular-nums;white-space:nowrap}}
ol li{{margin:6px 0}}.cap{{color:var(--mute);font-size:13px;margin-top:6px}}
</style></head><body><main>
<h1>Top 3 Tips AD R5</h1>
<p class="sub">RA-04 "Top 3 Tips For Getting Abs" (AD). Full 9:16 and 16:9, 0:57.9. Every gate passed, independent review. Click a time to jump both players there.</p>
<h2>The new man (veto either one)</h2>
<div class="row">
<div class="card"><img class="still" src="before.jpg" alt="before photo"><div class="cap">Before photo (AI-generated, labelled)</div></div>
<div class="card"><img class="still" src="after.jpg" alt="AI result"><div class="cap">His AI picture from the real generation</div></div>
</div>
<h2>Both films</h2>
<div class="row">
<div class="card"><div>9:16</div><video id="v9" class="v916" src="ra04_r5_9x16.mp4" controls preload="metadata"></video></div>
<div class="card"><div>16:9</div><video id="v16" class="v169" src="ra04_r5_16x9.mp4" controls preload="metadata"></video></div>
</div>
<h2>What changed since round 4 (watch these)</h2>
<table><tr><th>Watch</th><th>What</th></tr>{rows}</table>
<h2>What I decided (overrule anything)</h2>
<ol>{"".join(f"<li>{d}</li>" for d in DECIDED)}</ol>
<div class="row"><div class="card"><img class="f16" src="frame16_gen.jpg" alt="16:9 at 0:04"><div class="cap">16:9 at 0:04</div></div>
<div class="card"><img class="f16" src="frame16_lock.jpg" alt="16:9 at 0:08"><div class="cap">16:9 at 0:08</div></div></div>
<h2>Audio A/B</h2>
<div class="card" style="display:inline-block"><div>Muhammad's reference, then ours</div><video src="ra04_r5_audio_ab.mp4" controls preload="metadata" style="width:480px"></video></div>
</main>
<script>
document.querySelectorAll('a.t').forEach(a=>a.addEventListener('click',()=>{{const t=+a.dataset.t;for(const id of['v9','v16']){{const v=document.getElementById(id);try{{v.currentTime=t;}}catch(e){{}}}}}}));
</script></body></html>"""
assert chr(0x2014) not in html and chr(0x2013) not in html
open(f"{OUT}/index.html", "w").write(html)
print("PAGE", OUT)
