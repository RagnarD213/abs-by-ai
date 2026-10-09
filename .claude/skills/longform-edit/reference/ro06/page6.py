"""RO-06 round 6 review page: the FULL FILM on top, What changed (Dan's four revisions), What I decided, each revision with before and after stills and
'Play it in place', the mic repair as a before / after clip, the lines he did not speak to (one each, to overrule), the checks, one reply box.
Text comes from round6/page_text.json (written by the editor after the checks ran). Writes round6/index.html. usage: page6.py"""
import json, os, html, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import build as Bd
W = "/Volumes/Extreme/_edit_work/ro06"; O = f"{W}/round6"; NAME = "RO-06 round 6 - full film"; OLD = f"{W}/round5/RO-06 round 5 - full film.mp4"
M = f"{O}/{NAME}.mp4"; e = html.escape; os.makedirs(f"{O}/stills", exist_ok=True)
FPS = Bd.FPS; TOTAL = json.load(open(M + ".build.json"))["frames"]/FPS
def mmss(t): return f"{int(t//60)}:{t % 60:04.1f}"
def grab(t, name, src=M):
    p = subprocess.run([Bd.FF, "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv,format=rgb24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    Image.frombytes("RGB", (1920, 1080), p).save(f"{O}/stills/{name}.jpg", quality=90); return name
S = json.load(open(f"{O}/page_text.json")); grab(8.0, "poster")
css = open(f"{W}/recipe/page.py").read().split('css = """')[1].split('"""')[0]
css += (".three{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.three img,.three video{width:100%;border-radius:6px;display:block}"
        ".three div{font-size:13px;color:#9fb2cc;text-align:center}.ai{background:#14223a;border:1px solid #26354d;border-radius:10px;padding:12px 14px;margin:14px 0}ul li,ol li{margin:5px 0}"
        "table.ck{border-collapse:collapse;width:100%}table.ck td{border-bottom:1px solid #26354d;padding:6px 8px;vertical-align:top;font-size:14px}.ok{color:#7fd69a}.no{color:#ff9a8a}")
V = f"{NAME} - REVIEW 540p.mp4"
h = [f"<!doctype html><meta charset='utf-8'><title>RO-06 round 6</title><style>{css}</style>",
     f"<div id='dock'><div class='muted' id='docklabel'>The full film. Press any 'Play it in place' button.</div><video id='player' controls preload='none' poster='stills/poster.jpg' src='{V}'></video></div><main>",
     "<h1>How To Work Out At Home On A Budget: round 6, your four revisions</h1>",
     f"<div class='sub'>Long-form content, 16:9, {mmss(TOTAL)}. Nothing is uploaded or scheduled.</div>",
     "<h2>The full film</h2>", f"<video class='big' controls preload='none' poster='stills/poster.jpg' src='{V}'></video>",
     f"<p class='muted'>Also in the project folder for VLC: <b>Videos to Review / Work Out At Home LFC R6 - full film.mp4</b>. <a href='{NAME}.mp4'>Full 1080p file</a> &nbsp; <a href='RO-06 audio AB (reference then ours).mp4'>Audio A/B against the reference voice</a> &nbsp; <a href='RO06.srt'>Subtitles file</a> &nbsp; <a href='RO06.chapters.txt'>Chapters</a></p>",
     "<h2>What changed</h2><ul>"] + [f"<li>{e(c)}</li>" for c in S["CHANGED"]] + ["</ul>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in S["DECIDED"]] + ["</ol>"]
h.append("<h2>Your four revisions</h2>")
for it in S["ITEMS"]:
    st = []
    for j, (src, t, cap) in enumerate(it["stills"]): st.append((grab(t, f"{it['id']}-{j}", OLD if src == "old" else M), f"{cap} ({mmss(t)})"))
    media = "".join(f"<div><img loading='lazy' src='stills/{s}.jpg'>{e(c)}</div>" for s, c in st)
    media += "".join(f"<div><video controls preload='none' src='{e(v)}'></video>{e(c)}</div>" for v, c in it.get("videos", []))
    n = len(st) + len(it.get("videos", []))
    h.append(f"<div class='ai'><span class='id'>{it['n']}</span> &nbsp; {e(it['when'])} &nbsp; <span class='muted'>You said: {e(it['said'])}</span>"
             f"<div class='three' style='margin-top:8px;grid-template-columns:repeat({min(n, 4)},1fr)'>{media}</div><div class='copy'><b>What I did:</b> {e(it['what'])}</div>"
             f"<button onclick=\"seek({max(0, it['t0']-3.0):.1f})\">Play it in place, from 3 seconds before</button></div>")
h += ["<h2>What you did not mention (stays as built; change any line in the reply)</h2><ul>"] + [f"<li>{e(c)}</li>" for c in S["UNSPOKEN"]] + ["</ul>"]
h.append("<h2>The checks, as they came out</h2><table class='ck'>" + "".join(f"<tr><td class='{'ok' if ok else 'no'}'>{'PASS' if ok else 'NOT PASSED'}</td><td><b>{e(n)}</b></td><td>{e(t)}</td></tr>" for ok, n, t in S["CHECKS"]) + "</table>")
if S.get("OPEN"): h += ["<h2>Things I want you to know before you approve</h2><ul>"] + [f"<li>{e(c)}</li>" for c in S["OPEN"]] + ["</ul>"]
h += ["<h2>Your reply</h2><p class='muted'>Change any line, add notes, then copy and paste it to me.</p>",
      f"<textarea id='reply'>{e(S['REPLY'])}</textarea><br><button onclick=\"navigator.clipboard.writeText(document.getElementById('reply').value);this.textContent='Copied'\">Copy</button>",
      "<script>function seek(t){var v=document.getElementById('player');var go=function(){v.currentTime=t;v.play();};if(v.readyState>=1){go();}else{v.addEventListener('loadedmetadata',go,{once:true});v.load();}}</script></main>"]
txt = "\n".join(h); open(f"{O}/index.html", "w").write(txt); print("page written; em dashes:", txt.count(chr(8212)) + txt.count(chr(8211)))
