"""RO-20 round 4 page (2026-10-18): the three full films, what is new by timestamp in each (later-round format, VIDEO-RULES 2026-10-10),
gates and the independent reviews. Writes round3/index.html (the round 3b page is kept as round3/index-r3b.html; same port 8868).
Media: round3/r4/ (540p review copies and short join clips). Serve: _shared/review_server.py 8868 /Volumes/Extreme/_edit_work/ro20/round3"""
import os, html, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
W = "/Volumes/Extreme/_edit_work/ro20"; O = f"{W}/round3"; e = html.escape; FPS = 30000/1001
css = open(f"{W}/recipe/page2_20.py").read().split('css = """')[1].split('"""')[0]
S = json.load(open(f"{W}/round4/page_state.json"))          # written by the delivery step: per video name, new parts, gate rows, review verdict
def mmss(t): return f"{int(t//60)}:{t % 60:05.2f}"
def vid(p, cap):
    if not os.path.exists(f"{O}/{p}"): return "<p class='muted'>(not built yet)</p>"
    return f"<video class='big' controls preload='none' src='{e(p)}' style='width:100%;max-width:960px;border-radius:8px;background:#000'></video><p class='muted'>{cap}</p>"
h = [f"<!doctype html><meta charset='utf-8'><title>Invest In Your Health LFC R4</title><style>{css}</style><main style='margin-right:28px'>",
     "<h1>Invest In Your Health, round 4: the three full films</h1>",
     "<div class='sub'>Everything you approved on the round 3b page is built in. Below: each film, then only what is new in it, with the time to jump to. "
     "The full 1080p files are in the <b>Videos to Review</b> folder for VLC.</div>",
     f"<h2>Your decisions ({len(S['decisions'])})</h2>"] + [f"<div class='dec'><b>{i}. {e(d['q'])}</b> {e(d['why'])}<div class='opt'>Options: {' &nbsp;|&nbsp; '.join(e(o) for o in d['opts'])}</div></div>" for i, d in enumerate(S["decisions"], 1)] + [
     "<p>Otherwise, watch the new parts listed under each film and reply with notes, or say the three are finalized.</p>"]
for v in S["videos"]:
    h += [f"<h2>Video {v['n']}: {e(v['title'])} ({e(v['length'])})</h2>", vid(v["review"], f"Full film, 540p for the page. VLC file: {e(v['vlc'])}"),
          "<h3>New in this round (everything else is the cut you approved)</h3><table><tr><th>Where</th><th>What</th><th>Watch</th></tr>"]
    for c in v["changes"]:
        h.append(f"<tr><td>{e(c['at'])}</td><td>{e(c['what'])}</td><td>{e(c['watch'])}" + (f"<br><a href='{e(c['clip'])}'>clip</a>" if c.get("clip") else "") + "</td></tr>")
    h += ["</table>", f"<p class='muted'>Checks: {e(v['gate'])}</p>", f"<p class='muted'>Independent review: {e(v['review_verdict'])}</p>",
          f"<p class='muted'>Chapters for the description:</p><pre>{e(v['chapters'])}</pre>"]
h += ["<h2>What I decided (overrule anything)</h2><ol>"] + [f"<li>{e(d)}</li>" for d in S["decided"]] + ["</ol>",
      "<p class='muted'>The round 3b page: <a href='index-r3b.html'>index-r3b.html</a>.</p></main>"]
open(f"{O}/index.html", "w").write("\n".join(h)); print("wrote", f"{O}/index.html")
