#!/usr/bin/env python3
"""RA-05 round 3 review page: the WHOLE 9:16 on top (VIDEO-RULES 2026-10-14, short ads nearly approved), then the two items that
were never seen moving (the couch clip, the vertical body scan) as stills on their real frames and moving in context, "What I
decided", three decisions, one reply box.
  python3 page_r3.py --media    cuts the review files from draft_9x16.mp4, then writes the page
  python3 page_r3.py            page only
Writes round3/review/ (served by _shared/review_server.py). Round 2's page (round2/review/) is never touched."""
import html, json, os, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000 / 1001
B = json.load(open("beats.json")); W = json.load(open("words_aligned.json"))["words"]
R = "review"; [os.makedirs(f"{R}/{d}", exist_ok=True) for d in ("stills", "context")]
SRC = "draft_9x16.mp4"; TOTAL = B["total"]; by = {c["name"]: c for c in B["cards"]}
TITLE = "How AI Real Abs AD R3 - whole 9x16"
N = json.load(open("page_notes_r3.json"))
def say(a, b): return " ".join(w["w"].strip() for w in W if a - 0.05 <= w["t"] < b - 0.05)
def tc(t): return f"{int(t // 60)}:{t % 60:04.1f}"
dv = "scale=in_color_matrix=bt709:in_range=tv"
enc = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-color_range", "tv", "-c:a", "aac", "-movflags", "+faststart"]
if "--media" in sys.argv:
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", SRC, "-c", "copy", "-movflags", "+faststart", f"{R}/{TITLE}.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", SRC, "-vf", "scale=540:960", "-crf", "22", "-preset", "fast", "-b:a", "128k"]
                   + enc + [f"{R}/{TITLE} - REVIEW 540p.mp4"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", "5.0", "-i", SRC, "-frames:v", "1", "-vf", f"{dv},scale=540:960",
                    f"{R}/stills/whole.jpg"], check=True)
    for it in N["items"]:
        c = by[it["key"]]; a, b = c["beat"]
        for k, t in enumerate(it["stills"]):
            subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{a + t:.3f}", "-i", SRC, "-frames:v", "1", "-vf", dv,
                            f"{R}/stills/{it['id']}-{k}.png"], check=True)
            subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", f"{R}/stills/{it['id']}-{k}.png", "-vf", "scale=432:768",
                            f"{R}/stills/{it['id']}-{k}.jpg"], check=True)
        s = max(0, a - 3); d = min(TOTAL, b + 3) - s
        subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", SRC, "-crf", "18", "-preset", "medium",
                        "-b:a", "192k"] + enc + [f"{R}/context/{it['id']}-context.mp4"], check=True)
def item(it):
    c = by[it["key"]]; a, b = c["beat"]
    figs = "".join(f'<figure><a href="stills/{it["id"]}-{k}.png"><img src="stills/{it["id"]}-{k}.jpg" alt=""></a>'
                   f'<figcaption>{tc(a + t)} · {html.escape(cap)}</figcaption></figure>' for k, (t, cap) in enumerate(zip(it["stills"], it["captions"])))
    rows = [("When it appears", f"{tc(a)} to {tc(b)} ({b - a:.1f} s)"), ("You say just before", html.escape(say(a - 3, a))),
            ("It plays under", f"<b>{html.escape(say(a, b))}</b>"), ("Right after", html.escape(say(b, b + 2.5)))] + [(k, v) for k, v in it["rows"]]
    rws = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    sense = "".join(f"<li>{x}</li>" for x in it.get("sense", []))
    return f"""<h2>{html.escape(it['title'])}</h2>
<div class="top"><video controls preload="metadata" playsinline poster="stills/{it['id']}-0.jpg" src="context/{it['id']}-context.mp4"></video>
<div class="pair">{figs}</div></div><table class="ctx">{rws}</table>{'<p><b>Checked before you saw it:</b></p><ol>' + sense + '</ol>' if sense else ''}"""
dec = "".join(f"<li><b>{html.escape(d['q'])}</b><br>{d['body']}</li>" for d in N["decisions"])
did = "".join(f"<li>{d}</li>" for d in N["decided"])
reply = "\n".join(f"{n + 1}. {d['short']}: " for n, d in enumerate(N["decisions"])) + "\nOther notes: "
page = f"""<!doctype html><html><head><meta charset="utf-8"><title>How AI Real Abs AD R3</title><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#0b1220;color:#e8eef7;font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:24px 24px 120px}}
h1{{font-size:26px;margin:0 0 6px}} h2{{font-size:20px;margin:34px 0 10px;border-bottom:1px solid #24324a;padding-bottom:6px}}
.lock{{color:#9fb3cc;font-size:14px;margin:6px 0}} ol li,ul li{{margin:8px 0}} a{{color:#68c5ff}}
.top{{display:flex;gap:22px;flex-wrap:wrap;align-items:flex-start}} .top video{{width:320px;border-radius:12px;background:#000}}
.pair{{display:flex;gap:14px;flex-wrap:wrap}} .pair figure{{margin:0;width:216px}} .pair img{{width:100%;border-radius:10px}} figcaption{{font-size:13px;color:#9fb3cc}}
table.ctx{{border-collapse:collapse;margin:12px 0;max-width:980px}} .ctx th{{text-align:left;vertical-align:top;color:#9fb3cc;font-weight:600;padding:5px 14px 5px 0;white-space:nowrap}} .ctx td{{padding:5px 0}}
textarea{{width:100%;height:150px;background:#0f1930;color:#e8eef7;border:1px solid #2b3d5c;border-radius:8px;padding:10px;font:15px/1.4 Menlo,monospace}}
button{{background:#1d6fb8;color:#fff;border:0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer}}
@media(max-width:700px){{main{{padding:16px}} .top video{{width:100%}} .pair figure{{width:46%}}}}
</style></head><body><main>
<h1>How AI Can Get You REAL Six Pack Abs · AD (RA-05) · round 3</h1>
<div class="lock">{N['intro']}</div>
<div class="lock"><b>Locked from your answers:</b> {N['locked']}</div>
<h2>Your decisions ({len(N['decisions'])})</h2><ol>{dec}</ol>
<h2>The whole ad, 9:16 ({TOTAL:.1f} s)</h2>
<div class="top"><video controls preload="metadata" playsinline poster="stills/whole.jpg" src="{TITLE} - REVIEW 540p.mp4"></video>
<div><p><a href="{TITLE}.mp4">Full quality 1080 x 1920 file</a> (also in <i>Videos to Review</i>)</p><p>{N['whole']}</p></div></div>
{''.join(item(i) for i in N['items'])}
<h2>What I decided (overrule anything)</h2><ul>{did}</ul>
<h2>Your reply</h2><textarea id="rep">{html.escape(reply)}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('rep').value);this.textContent='Copied'">Copy</button>
</main></body></html>"""
assert "—" not in page and "–" not in page, "no em or en dashes"
open(f"{R}/index.html", "w").write(page); print("page written")
