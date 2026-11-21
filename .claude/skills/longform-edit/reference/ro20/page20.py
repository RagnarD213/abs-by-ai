"""RO-20 round 1 review page (standard layout: decisions, first minute, AI frames, look and sound, What I decided, every item three
per row, one docked player, one reply box). Copy lives in round1/page_copy.json so it can be edited without touching this file.
Writes round1/index.html. Serve with _shared/review_server.py PORT round1."""
import json, os, html, shutil, glob
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round1"
C = json.load(open(f"{O}/page_copy.json"))
rows = json.load(open(f"{O}/stills.json")); S = json.load(open(f"{W}/shots.json")); TOTAL = S[-1]["out_f1"]/(30000/1001)
ctx = {f.split("-context")[0] for f in os.listdir(f"{O}/context") if f.endswith("REVIEW 540p.mp4") and not f.startswith("._")} if os.path.isdir(f"{O}/context") else set()
def mmss(t): return f"{int(t//60)}:{int(t%60):02d}"
e = html.escape
os.makedirs(f"{O}/frames", exist_ok=True); os.makedirs(f"{O}/look", exist_ok=True); os.makedirs(f"{O}/audio", exist_ok=True)
for a in C["ai"]:
    for se in ("start", "end"):
        Image.open(f"{W}/aiframes/{a['id']}-{se}.png").convert("RGB").resize((1280, 720), Image.LANCZOS).save(f"{O}/frames/{a['id']}-{se}.jpg", quality=90)
LOOKS = C["looks"]                                    # [[key, label], ...] in display order; key 'raw' = camera original
for m in ("m1", "m2"):
    for k, _ in LOOKS:
        for z in ("W", "T"):
            src = f"{W}/look/opt/{m}_{z}_{k}.png"
            if os.path.exists(src): Image.open(src).convert("RGB").resize((960, 540), Image.LANCZOS).save(f"{O}/look/{m}_{z}_{k}.jpg", quality=90)
for name, src in C["refs"]: Image.open(src).convert("RGB").resize((960, 540), Image.LANCZOS).save(f"{O}/look/ref_{name}.jpg", quality=90)
for k, _ in C["voices"]: shutil.copy(f"{W}/audio/opts/{k}.mp3", f"{O}/audio/{k}.mp3")
css = """body{font:15px/1.45 -apple-system,Helvetica,Arial;margin:0;background:#0d1626;color:#e8eef7}main{max-width:1180px;margin:0 420px 60px 28px}
h1{font-size:24px;margin:22px 0 6px}h2{font-size:19px;margin:34px 0 10px;border-top:1px solid #26354d;padding-top:18px}h3{font-size:15px;margin:22px 0 8px;color:#8fd0ff}.sub{color:#9fb2cc}
.dec{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:10px 0}.dec b{color:#8fd0ff}.opt{color:#cfe2f7;margin:4px 0 0 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#14223a;border:1px solid #26354d;border-radius:10px;overflow:hidden}
.card img{width:100%;display:block}.card .b{padding:9px 11px;font-size:13px}.id{font-weight:700;color:#8fd0ff}.copy{color:#fff;margin:4px 0}.muted{color:#9fb2cc}
details{margin-top:5px}summary{cursor:pointer;color:#9fb2cc}button{background:#2b6cb0;color:#fff;border:0;border-radius:6px;padding:6px 10px;margin-top:6px;cursor:pointer}a.btn{display:inline-block;background:#2b6cb0;color:#fff;border-radius:6px;padding:6px 10px;margin-top:6px;text-decoration:none}
#dock{position:fixed;right:14px;top:14px;width:384px;background:#14223a;border:1px solid #26354d;border-radius:10px;padding:10px}#dock video{width:100%;border-radius:6px;background:#000}
.look{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.look img{width:100%;border-radius:6px}.look div{font-size:12px;color:#9fb2cc;text-align:center}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 2px}.pair img{width:100%;border-radius:6px}.pair div{font-size:12px;color:#9fb2cc;text-align:center}
.aud{display:grid;grid-template-columns:230px 1fr;gap:6px 12px;align-items:center}audio{width:100%;height:34px}
textarea{width:100%;height:330px;background:#0b1320;color:#e8eef7;border:1px solid #26354d;border-radius:8px;padding:10px;font:13px/1.4 Menlo,monospace}
video.big{width:100%;border-radius:10px;background:#000}ol li{margin:5px 0}a{color:#8fd0ff}table{border-collapse:collapse}td{padding:2px 14px 2px 0;vertical-align:top}
@media(max-width:1300px){main{margin-right:28px}#dock{position:static;width:auto;margin:14px 28px}}"""
h = [f"<!doctype html><meta charset='utf-8'><title>RO-20 round 1</title><style>{css}</style>",
     "<div id='dock'><div class='muted' id='docklabel'>Play any item moving, in context: press its button</div><video id='player' controls preload='none'></video></div><main>",
     f"<h1>{e(C['title'])}</h1>", f"<div class='sub'>{e(C['sub']).replace('{TOTAL}', mmss(TOTAL))}</div>", f"<p><b>Already locked and reused:</b> {e(C['locked'])}</p>",
     f"<h2>Your decisions ({len(C['decisions'])})</h2>"]
for i, d in enumerate(C["decisions"], 1):
    h.append(f"<div class='dec'><b>{i}. {e(d['t'])}.</b> {e(d['why'])}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in d['opts'])}</div></div>")
fm = "first-minute/DRAFT - RO-20 round 1 - first minute"
h += ["<h2>The first minute, finished</h2>", f"<video class='big' controls preload='none' poster='{fm}.jpg' src='{fm} - REVIEW 540p.mp4'></video>",
      f"<p class='muted'>{e(C['fm_note'])} <a href='{fm}.mp4'>Full 1080p file</a> &nbsp; <a href='first-minute/AB_reference-vs-ours.mp4'>Audio A/B against the reference voice</a><br>Also in the project folder for VLC: <b>{e(C['vlc'])}</b></p>",
      "<h2>New AI clips: start and end frames</h2>"]
for a in C["ai"]:
    h.append(f"<div class='dec'><b>{a['id']}. {e(a['name'])}.</b> {e(a['act'])} Slot: {a['dur']:.1f} s. Estimated cost: {e(a['cost'])}."
             f"<div class='pair'><div><img loading='lazy' src='frames/{a['id']}-start.jpg'>START</div><div><img loading='lazy' src='frames/{a['id']}-end.jpg'>END</div></div></div>")
h += [f"<h2>Colour: what I compared</h2><div class='muted'>{e(C['look_note'])}</div>"]
for m, z, title in (("m1", "W", "The camera frame"), ("m2", "T", "The closer size (1.3x)")):
    h += [f"<h3>{title}</h3><div class='look'>"] + [f"<div><img loading='lazy' src='look/{m}_{z}_{k}.jpg'>{e(lab)}</div>" for k, lab in LOOKS if os.path.exists(f"{O}/look/{m}_{z}_{k}.jpg")]
    h += [f"<div><img loading='lazy' src='look/ref_{name}.jpg'>{e(name)}</div>" for name, _ in C["refs"][(0 if z == 'W' else 1):(1 if z == 'W' else 3)]] + ["</div>"]
h += [f"<h2>Sound: what I compared</h2><div class='muted'>{e(C['voice_note'])}</div><div class='aud'>"]
for k, lab in C["voices"]: h.append(f"<div>{e(lab)}</div><audio controls preload='none' src='audio/{k}.mp3'></audio>")
h += ["</div>", "<h2>Chapters (the film is long, so it gets chapters)</h2><table>"] + [f"<tr><td>{e(t)}</td><td>{e(n)}</td></tr>" for t, n in C["chapters"]] + ["</table>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in C["decided"]] + ["</ol>"]
h += [f"<h2>Every graphic and clip, in order ({len(rows)})</h2><p class='muted'>{e(C['items_note'])}</p><div class='grid'>"]
KIND = {"lt": "lower third", "fact": "fact card", "l3": "side list", "clip": "clip", "scene": "full screen"}
for r in rows:
    c = r["copy"]; lines = []
    if "topic" in c: lines.append(f"{e(c['topic'])}: {e(c['point'])}")
    if r["kind"] == "clip": lines.append(e(r.get("note") or ""))
    if c.get("label"): lines.append("Label on screen: " + e(c["label"]))
    if r.get("pending"): lines.append("<b>PLACEHOLDER: start frame shown. Motion is generated only after you approve the frames.</b>")
    btn = f"<a class='btn' href='context/{r['id']}-context - REVIEW 540p.mp4' onclick=\"return play(this,'{r['id']}')\">Play it moving, in context</a>" if r["id"] in ctx else ""
    h.append(f"<div class='card' id='{r['id']}'><img loading='lazy' src='stills/{r['id']}.jpg'><div class='b'><span class='id'>{r['id']}</span> <span class='muted'>{KIND.get(r['kind'], r['kind'])} &middot; {mmss(r['t0'])} to {mmss(r['t1'])}</span>"
             f"<div class='copy'>{'<br>'.join(lines)}</div>{btn}<details><summary>What you are saying</summary><span class='muted'>Before:</span> {e(r['before'])}<br><span class='muted'>During:</span> {e(r['during'])}<br><span class='muted'>After:</span> {e(r['after'])}</details></div></div>")
reply = "RO-20 round 1\n" + "\n".join(f"{i}. {d['t']}: {d['rec']}" for i, d in enumerate(C["decisions"], 1)) + "\nGraphics or clips to change (ID and what):\nFirst minute, anything to change:\nAnything else:\n"
h += ["</div><h2>Your reply</h2><p class='muted'>My recommendations are filled in. Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(reply)}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function play(a,id){var v=document.getElementById('player');v.src=a.getAttribute('href');document.getElementById('docklabel').textContent=id+' in context';v.play();return false;}</script></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page:", len(rows), "items,", len(ctx), "context clips,", "em dashes:", txt.count(chr(8212)))
