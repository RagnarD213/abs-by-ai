#!/usr/bin/env python3
"""RA-06 round 4 review page: both delivered films, only what is new (the 16:9 layouts, the two 9:16 label moves), each with exact
times, a watch range and a context clip, the two open choices, "What I decided", one reply box.
  python3 round4/page_r4.py [--media]      (run from anywhere) -> round4/page/index.html"""
import json, os, subprocess, html, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
os.chdir("/Volumes/Extreme/_edit_work/ra06")
DEL = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Claude Ad Videos/whats the best ab exercise - RA-06"
M16 = f"{DEL}/whats the best ab exercise | claude | 16x9 | RA-06.mp4"; M9 = f"{DEL}/whats the best ab exercise | claude | 9x16 | RA-06.mp4"
B = json.load(open("beats.json")); W = json.load(open("words_aligned.json"))["words"]; TOTAL = B["total"]
P = "round4/page"
def say(a, b): return " ".join(w["w"].strip() for w in W if a - 0.05 <= w["t"] < b - 0.05)
def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
ITEMS = [  # id, format, name, span, still at (fraction), copy
 ("open16", "16x9", "Opener: the three exercises", (0.0, 2.37), 0.5,
  "New 16:9 layout. Vacuum as one tall panel on the left, plank and toe touches stacked on the right; same footage, in-points and colour as "
  "the 9:16. The captions sit on the blue under the panels. Held 2 frames longer than the 9:16 so the first shot of you is not mid head-turn."),
 ("ai16", "16x9", "AI clips as full-height panels (OPEN CHOICE)", (5.97, 14.48), 0.3,
  "The body scan, copier, fired trainer (19.9 s) and robot goodbye (41.5 s) are vertical clips, so in 16:9 they play whole, full height, on "
  "the blue field with the AI-GENERATED label beside them. About a third of the ad. The reviewer thinks this leaves too much empty blue; "
  "the other option is the phone-beside-you layout used for the app screens."),
 ("lt16", "16x9", "Key point box beside you, not over your abs", (15.65, 19.95), 0.45,
  "\"Copy-Paste Plans Ignore Your Body\" is a narrow box in the bottom-left corner, so it does not cover your abs in the wide shot."),
 ("tour16", "16x9", "App screen beside you: workout list", (23.86, 27.56), 0.5,
  "Your approved RO-06 layout: you talking on the right, the app in a phone panel on the left. Close shot."),
 ("flow16", "16x9", "Generate flow: before, you, then the AI after (OPEN CHOICE)", (32.67, 37.10), 0.15,
  "The generating screen (his before photo) beside you, then you alone and closer for 0.9 s, then his AI result beside you. You sit "
  "between before and after so they never meet. You shift sideways with each of those two zooms (34.5 s and 35.4 s); the checks read "
  "them as deliberate cuts, but you may find it busy."),
 ("tour216", "16x9", "App screen beside you: meal analysis", (37.10, 41.47), 0.5,
  "Same layout, close shot, the 775-calorie meal analysis."),
 ("cta16", "16x9", "Button upper left", (41.47, 45.71), 0.75,
  "\"Tap The Button Below To / Start Training With AI\", upper left beside your shoulder. Your arms fill the bottom left in the last shot (measured)."),
 ("vac9", "9x16", "9:16 change: Stomach Vacuum label up 6 px", (0.0, 2.30), 0.5,
  "The only gate fixes in the 9:16 you approved. This label sat 1 px too close to the captions."),
 ("chip9", "9x16", "9:16 change: AI-GENERATED label lowered", (41.47, 43.58), 0.5,
  "It was overlapping the caption by 13 px; now under it, on the floor, clear of both figures and the button."),
 ("lt9", "9x16", "9:16, NOT changed: key point box over your abs", (15.65, 19.95), 0.45,
  "Unchanged from what you approved. The checks flag it covering your abs in the wide shot. Say the word and it moves (one graphic re-render)."),
]
DECIDED = [
 "Close shot in 16:9 tightened (1792 px wide of the 4K) so every close-to-wide switch is a clear zoom (the first build's step was too small and read as near jump cuts).",
 "App screens beside you instead of small phones on empty blue (flagged by the reviewer and the frame check).",
 "The 9:16 keeps your approved edit; only the two labels moved, proven frame by frame.",
 "Audio is your approved mix, bit for bit, in both formats (-14.2 LUFS).",
 "Both files: delivery gate 39 of 39, audio gate pass, frame-by-frame check 0 open defects, independent reviewer SHIP.",
]
os.makedirs(f"{P}/stills", exist_ok=True); os.makedirs(f"{P}/context", exist_ok=True)
if "--media" in sys.argv:
    for k, src, wh in (("16x9", M16, "960:540"), ("9x16", M9, "540:960")):
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", src, "-vf", f"scale={wh}", "-c:v", "libx264", "-crf", "22", "-preset", "fast",
                        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{P}/RA-06 R4 {k} - REVIEW 540p.mp4"], check=True)
    for iid, k, _n, (a, b), at, _c in ITEMS:
        src, wh = (M16, "960:540") if k == "16x9" else (M9, "540:960")
        mid = a + at * (b - a)
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", src, "-ss", f"{mid:.3f}", "-frames:v", "1", "-vf", f"scale={wh}", f"{P}/stills/{iid}.jpg"], check=True)
        s = max(0, a - 3); d = min(TOTAL, b + 3) - s
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", src, "-vf", f"scale={wh}", "-c:v", "libx264", "-crf", "23",
                        "-preset", "fast", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", f"{P}/context/{iid}-context.mp4"], check=True)
def card(it):
    iid, k, name, (a, b), _at, copy = it
    return f"""<div class="card {k}"><img loading="lazy" src="stills/{iid}.jpg" alt="{iid}">
<div class="meta"><div class="id">{html.escape(name)}</div><div class="t">{k} · {tc(a)} to {tc(b)} · watch {tc(max(0, a - 2))} to {tc(min(TOTAL, b + 2))}</div>
<div class="copy">{html.escape(copy)}</div>
<button onclick="play('context/{iid}-context.mp4','{html.escape(name)}')">Play it moving, in context</button>
<details><summary>What you say</summary><p>{html.escape(say(a, b))}</p></details></div></div>"""
did = "".join(f"<li>{html.escape(d)}</li>" for d in DECIDED)
g16 = "".join(card(i) for i in ITEMS if i[1] == "16x9"); g9 = "".join(card(i) for i in ITEMS if i[1] == "9x16")
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Best Ab Exercise AD R4</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 16px 120px}} @media(min-width:1500px){{main{{margin-right:420px}}}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:20px;margin:34px 0 10px;border-bottom:1px solid #24324a;padding-bottom:6px}}
.lock{{color:#9fb3cc;font-size:14px}} ul li{{margin:8px 0}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}} .grid.v{{grid-template-columns:repeat(3,1fr)}} @media(max-width:900px){{.grid,.grid.v{{grid-template-columns:1fr}}}}
.card{{background:#111b2e;border:1px solid #24324a;border-radius:12px;overflow:hidden}} .card img{{width:100%;display:block;background:#000}}
.meta{{padding:12px 14px}} .id{{font-weight:700}} .t{{color:#9fb3cc;font-size:14px}} .copy{{margin:8px 0;font-size:15px}}
button{{background:#1d6fb8;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer}} details{{margin-top:8px;font-size:14px;color:#c6d3e4}}
.top{{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start}} .top video.h{{width:640px;max-width:100%}} .top video.v{{width:300px;max-width:100%}} .top video{{border-radius:12px;background:#000}}
#dock{{position:fixed;right:18px;top:18px;width:380px;background:#0f1930;border:1px solid #2b3d5c;border-radius:12px;padding:10px;z-index:5}}
#dock video{{width:100%;max-height:70vh;border-radius:8px;background:#000}} #dock .lab{{font-size:13px;color:#9fb3cc;margin-bottom:6px}}
@media(max-width:1499px){{#dock{{position:sticky;top:0;right:auto;width:auto;max-width:420px;margin:0 auto}}}}
textarea{{width:100%;box-sizing:border-box;height:170px;background:#0f1930;color:#e8eef7;border:1px solid #2b3d5c;border-radius:8px;padding:10px;font:15px/1.4 Menlo,monospace}}
</style></head><body>
<div id="dock"><div class="lab" id="docklab">Context player: press a "Play it moving, in context" button</div><video id="dv" controls preload="none" playsinline></video></div>
<main>
<h1>What's The Best Ab Exercise? · AD (RA-06) · round 4</h1>
<div class="lock">You approved the 9:16 in round 3. This round builds the 16:9 from the same edit (same cut, audio, captions and clips) and runs every check on both. The 16:9 is new to you.</div>
<h2>Both films ({TOTAL:.1f} s)</h2>
<div class="top"><video class="h" controls preload="metadata" playsinline src="RA-06 R4 16x9 - REVIEW 540p.mp4"></video>
<video class="v" controls preload="metadata" playsinline src="RA-06 R4 9x16 - REVIEW 540p.mp4"></video></div>
<h2>New in the 16:9, in film order</h2>
<div class="grid">{g16}</div>
<h2>The 9:16 you approved: what moved and what did not</h2>
<div class="grid v">{g9}</div>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Your reply</h2>
<p class="lock">Two open choices: the AI clips as panels (5.97 s), and the sideways shift around the generate flow (34.5 s and 35.4 s). Approve, or write what to change (a time is enough).</p>
<textarea id="reply">Approved / changes: </textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('reply').value)">Copy my reply</button></p>
</main>
<script>function play(src,lab){{const v=document.getElementById('dv');v.src=src;document.getElementById('docklab').textContent=lab;v.play();}}</script>
</body></html>"""
open(f"{P}/index.html", "w").write(page); print("page ->", f"{P}/index.html", len(ITEMS), "items")
