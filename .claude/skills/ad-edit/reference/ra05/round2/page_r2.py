#!/usr/bin/env python3
"""RA-05 round 2 review page (PRE-RENDER-APPROVAL.md layout, VIDEO-RULES 2026-09-30): header with what is locked and the
decisions, the finished first 30 seconds, the couch START/END frames with full context, "What I decided", then every
graphic and clip in the first 30 s in timeline order (three per row, one docked context player), one reply box.

  python3 page_r2.py --media    cuts the first 30 s, the context clips and the stills from draft_9x16.mp4, then writes the page
  python3 page_r2.py            page only
Writes round2/review/ (served by _shared/review_server.py)."""
import html, json, os, shutil, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000 / 1001
B = json.load(open("beats.json")); W = json.load(open("words_aligned.json"))["words"]
R = "review"; os.makedirs(f"{R}/stills", exist_ok=True); os.makedirs(f"{R}/context", exist_ok=True); os.makedirs(f"{R}/frames", exist_ok=True)
SRC = "draft_9x16.mp4"; TOTAL = B["total"]
by = {c["name"]: c for c in B["cards"]}; lt = {l["id"]: l for l in B["lt"]}
END30 = next(p["beat"][0] for p in B["punch"] if p["beat"][0] > 30.0)          # "AI is a transformative...": 31.70 s
F30 = int(round(END30 * FPS))
TITLE = "RA-05 round 2 - first 30 seconds"
N = json.load(open("page_notes_r2.json"))


def say(a, b): return " ".join(w["w"].strip() for w in W if a - 0.05 <= w["t"] < b - 0.05)
def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def span(k):
    if k in by: return by[k]["beat"]
    if k in lt: return [lt[k]["a"], lt[k]["b"]]
    raise KeyError(k)


items = [dict(i, a=span(i["key"])[0], b=span(i["key"])[1]) for i in N["items"]]
couch = by["couch"]

if "--media" in sys.argv:
    dv = "scale=in_color_matrix=bt709:in_range=tv"
    enc = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-color_range", "tv", "-c:a", "aac", "-movflags", "+faststart"]
    d30 = F30 / FPS
    af = f"afade=t=out:st={d30 - 0.3:.3f}:d=0.3"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", SRC, "-frames:v", str(F30), "-t", f"{d30:.4f}", "-af", af, "-crf", "17",
                    "-preset", "slow", "-b:a", "256k"] + enc + [f"{R}/DRAFT - {TITLE}.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", f"{R}/DRAFT - {TITLE}.mp4", "-vf", "scale=540:960", "-crf", "22",
                    "-preset", "fast", "-b:a", "128k"] + enc + [f"{R}/DRAFT - {TITLE} - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", "2.6", "-i", SRC, "-frames:v", "1", "-vf", f"{dv},scale=540:960",
                    f"{R}/stills/first30.jpg"], check=True)
    for it in items:
        mid = it["a"] + it.get("at", 0.6) * (it["b"] - it["a"])
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{mid:.3f}", "-i", SRC, "-frames:v", "1", "-vf", f"{dv},scale=540:960",
                        f"{R}/stills/{it['id']}.jpg"], check=True)
        s = max(0, it["a"] - 3); d = min(TOTAL, it["b"] + 3) - s
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-vf", "scale=540:960", "-crf", "23",
                        "-preset", "fast", "-b:a", "128k"] + enc + [f"{R}/context/{it['id']}-context - REVIEW 540p.mp4"], check=True)
    from PIL import Image
    for tag in ("START", "END"):
        Image.open(f"frames/couch_{tag}.png").convert("RGB").save(f"{R}/frames/couch-{tag.lower()}.png")
        Image.open(f"frames/couch_{tag}.png").convert("RGB").resize((480, 820), Image.LANCZOS).save(f"{R}/frames/couch-{tag.lower()}.jpg", quality=90)
    for k, src in (("voice_106x_rubberband", "listen/o_rb.mp3"), ("voice_normal_speed", "listen/o_control.mp3")):
        shutil.copy(src, f"{R}/{k}.mp3")


def card(it):
    sp = (f"<b>Before:</b> {html.escape(say(it['a'] - 3, it['a']))}<br><b>During:</b> {html.escape(say(it['a'], it['b']))}"
          f"<br><b>After:</b> {html.escape(say(it['b'], it['b'] + 3))}")
    tag = f'<span class="tag {it["status"]}">{html.escape(it["status_txt"])}</span>'
    return f"""<div class="card"><img loading="lazy" src="stills/{it['id']}.jpg" alt="{it['id']}">
<div class="meta"><div class="id">{it['id']} · {html.escape(it['name'])} {tag}</div><div class="t">{tc(it['a'])} to {tc(it['b'])} ({it['b'] - it['a']:.1f} s)</div>
<div class="copy">{it['copy']}</div><div class="src">{html.escape(it['source'])}</div>
<button onclick="play('context/{it['id']}-context - REVIEW 540p.mp4','{it['id']} · {html.escape(it['name'])}')">Play it moving, in context</button>
<details><summary>What he says</summary><p>{sp}</p></details></div></div>"""


ca, cb, cc = couch["beat"][0], couch["beat"][1], couch["cut_at"]
rows = [("When it appears", f"{tc(ca)} to {tc(cb)} ({cb - ca:.1f} s), right after the app opening"),
        ("You say just before", say(ca - 3, ca)),
        ("It plays under", f"<b>{html.escape(say(ca, cb))}</b>"),
        ("Right after", f"you on camera: {html.escape(say(cb, cb + 2.5))}"),
        ("What you see", N["couch_see"]),
        ("The cut", f"START shot {ca:.1f} to {cc:.1f} s (under \"{html.escape(say(ca, cc))}\"), a straight CUT to the END shot {cc:.1f} to {cb:.1f} s (under \"{html.escape(say(cc, cb))}\"). Two shots, never a morph."),
        ("If you say no", N["couch_no"]),
        ("Motion and cost", N["couch_cost"])]
crow = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
sense = "".join(f"<li>{x}</li>" for x in N["couch_sense"])
dec = "".join(f"<li><b>{html.escape(d['q'])}</b><br>{d['body']}</li>" for d in N["decisions"])
did = "".join(f"<li>{d}</li>" for d in N["decided"])
reply = "\n".join(f"{n + 1}. {d['short']}: " for n, d in enumerate(N["decisions"])) + "\nOther notes: "
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>How AI Real Abs AD R2</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 24px 120px}} @media(min-width:1500px){{main{{margin-right:400px}}}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:20px;margin:34px 0 10px;border-bottom:1px solid #24324a;padding-bottom:6px}}
.lock{{color:#9fb3cc;font-size:14px;margin:6px 0}} ol li,ul li{{margin:8px 0}} a{{color:#68c5ff}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}} @media(max-width:900px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:#111b2e;border:1px solid #24324a;border-radius:12px;overflow:hidden}} .card img{{width:100%;display:block}}
.meta{{padding:12px 14px}} .id{{font-weight:700}} .t{{color:#9fb3cc;font-size:14px}} .copy{{margin:8px 0;font-size:15px}} .src{{color:#9fb3cc;font-size:13px;margin-bottom:8px}}
.tag{{font-size:12px;font-weight:600;border-radius:6px;padding:1px 7px;margin-left:4px}} .tag.new{{background:#d9a400;color:#111}} .tag.same{{background:#24324a;color:#c6d3e4}}
button{{background:#1d6fb8;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer}} details{{margin-top:8px;font-size:14px;color:#c6d3e4}}
.top{{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start}} .top video{{width:300px;border-radius:12px;background:#000}}
#dock{{position:fixed;right:18px;top:18px;width:350px;background:#0f1930;border:1px solid #2b3d5c;border-radius:12px;padding:10px;z-index:5}}
#dock video{{width:100%;border-radius:8px;background:#000}} #dock .lab{{font-size:13px;color:#9fb3cc;margin-bottom:6px}}
@media(max-width:1499px){{#dock{{position:sticky;top:0;right:auto;width:auto;max-width:360px;margin:0 auto}}}}
textarea{{width:100%;height:170px;background:#0f1930;color:#e8eef7;border:1px solid #2b3d5c;border-radius:8px;padding:10px;font:15px/1.4 Menlo,monospace}}
.pair{{display:flex;gap:16px;flex-wrap:wrap}} .pair figure{{margin:0;width:300px}} .pair img{{width:100%;border-radius:10px}} figcaption{{font-size:13px;color:#9fb3cc}}
table.ctx{{border-collapse:collapse;margin:12px 0;max-width:900px}} .ctx th{{text-align:left;vertical-align:top;color:#9fb3cc;font-weight:600;padding:5px 14px 5px 0;white-space:nowrap}} .ctx td{{padding:5px 0}}
audio{{width:300px;vertical-align:middle}}
</style></head><body>
<div id="dock"><div class="lab" id="docklab">Context player: press a "Play it moving, in context" button</div><video id="dv" controls preload="none" playsinline></video></div>
<main>
<h1>How AI Can Get You REAL Six Pack Abs · AD (RA-05) · round 2</h1>
<div class="lock">{N['intro']}</div>
<div class="lock"><b>Locked from your answers, applied without asking again:</b> {N['locked']}</div>
<h2>Your decisions ({len(N['decisions'])})</h2><ol>{dec}</ol>
<h2>The first 30 seconds, finished ({F30 / FPS:.1f} s, to the end of "...the picture you generated.")</h2>
<div class="top"><video controls preload="none" playsinline poster="stills/first30.jpg" src="DRAFT - {TITLE} - REVIEW 540p.mp4"></video>
<div><p><a href="DRAFT - {TITLE}.mp4">Full quality 1080 x 1920 file</a></p>
<p>{N['first30']}</p>
<p><b>The voice at 1.06x, 15 seconds:</b> <audio controls preload="none" src="voice_106x_rubberband.mp3"></audio><br>
<b>The same lines at normal speed:</b> <audio controls preload="none" src="voice_normal_speed.mp3"></audio></p></div></div>
<h2>New AI clip: "Steps out of the phone" (the guy on the couch), START and END frames</h2>
<div class="pair"><figure><a href="frames/couch-start.png"><img src="frames/couch-start.jpg" alt="START"></a><figcaption><b>START</b> (click for full size)</figcaption></figure>
<figure><a href="frames/couch-end.png"><img src="frames/couch-end.jpg" alt="END"></a><figcaption><b>END</b>, a separate shot joined by a cut (click for full size)</figcaption></figure></div>
<table class="ctx">{crow}</table>
<p><b>The three sense questions, answered for the frames:</b></p><ol>{sense}</ol>
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Every graphic and clip in the first 30 seconds, in order</h2>
<p class="lock">Yellow = new or changed this round. Grey = as in round 1, only retimed by the speed-up. After the 30 seconds, the call-to-action button, Step lower thirds and the physique poses are unchanged from round 1 and are not repeated here.</p>
<div class="grid">{''.join(card(i) for i in items)}</div>
<h2>Your reply</h2><textarea id="rep">{html.escape(reply)}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value);this.textContent='Copied'">Copy</button>
</main><script>
function play(src,lab){{const v=document.getElementById('dv');v.src=encodeURI(src);document.getElementById('docklab').textContent=lab;v.play();}}
</script></body></html>"""
assert "—" not in page, "no em dashes"
open(f"{R}/index.html", "w").write(page); print("page written", len(items), "items; first 30 s =", round(F30 / FPS, 3), "s")
