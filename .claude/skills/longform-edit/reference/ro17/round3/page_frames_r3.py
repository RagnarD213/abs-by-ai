"""RO-17 round 3 frames page: the new One can and done pair (needs Dan's yes before motion) and the two candy swaps (a look,
no answer needed). One section, standard header + "What I decided" + one reply box. Refuses a pair without gate + reviewer PASS."""
import os, sys, shutil, json, html
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/framecheck")
from gate import require_pass
W = "/Volumes/Extreme/_edit_work/RO-17/round3"; AF = f"{W}/aiframes"; OUT = f"{W}/frames_page"
os.makedirs(f"{OUT}/frames", exist_ok=True)
PAIRS = [
    dict(id="A10", name="One can and done", ask=True,
         when="6:47.6 to 6:51.7, in the snack swaps section (sardines)",
         before="You can eat half a bag of trail mix and not even notice you did it.",
         under="Nobody has ever binged on sardines. You eat one can and then you're done.",
         after="And here's what surprised me the most. After about three weeks of snacking like this...",
         see="NEW MAN, as you asked: ripped, lean, in a tank top. START: the last sardine on his fork, the empty tin in his other "
             "hand. END: the empty tin with the same fork in it set on the sofa back, hands behind his head, content.",
         motion="6 s take (about $0.90), about 4 s of it used.",
         fallback="Your camera shot plays under the line."),
    dict(id="A3", name="The calorie scale (opener)", ask=False,
         when="0:00 to 0:04, the first shot of the video",
         before="(the video opens on it)",
         under="You can get fat eating healthy foods. I'll show you why this happens and",
         after="how to prevent it in today's video.",
         see="Your note applied: the colourful candy in the trail mix is now white yogurt-covered raisins, in the cup and on the pan. "
             "Every other pixel is the frame you approved.",
         motion="4 s take (about $0.60).", fallback="n/a: approved, motion authorized"),
    dict(id="A2", name="Couch snacking", ask=False,
         when="1:16.0 to 1:21.3, trail mix section",
         before="You're not eating one small handful of trail mix and then putting the bag away. I know I wasn't.",
         under="What really happens is you're watching TV or you're working at your desk and you keep reaching into the bag.",
         after="One cup of trail mix is about 700 calories...",
         see="Your note applied: white yogurt-covered raisins instead of the candy, in the bag and the piece at his mouth. "
             "Every other pixel is the frame you approved.",
         motion="6 s take (about $0.90).", fallback="n/a: approved, motion authorized"),
]
DECIDED = [
    "A3 and A2: only the trail mix was edited; I pasted your approved round 2 pixels back over everything else, so nothing "
    "else in those frames moved. A second pass removed a few shiny red candies that survived the first edit on the pan.",
    "One can and done: a fresh man, same sofa, room and night light. Fork kept full size and the tin kept empty in both "
    "frames (the two faults caught in round 2).",
    "Every pair here passed the frame gate and a fresh independent reviewer before this page.",
    "Clip C13 (you drinking from the bottle) is cut; you stay on camera for \"Just drink water\". The cut there goes wide to "
    "close, no jump.",
    "Motion is already generating for the five clips you approved as they are (hiker, nut jar, grapes vs raisins, nothing left "
    "for dinner, boardroom), and A3 and A2 next. Each take gets the motion check and an independent review before you see it "
    "in the full film.",
]
rows = []
for p in PAIRS:
    s, e = f"{AF}/{p['id']}-start.png", f"{AF}/{p['id']}-end.png"
    if not p["ask"]:
        try: require_pass(s, e)
        except BaseException: print("held back (not passed yet):", p["id"]); continue
    require_pass(s, e)
    for k, f in (("start", s), ("end", e)): shutil.copy(f, f"{OUT}/frames/{p['id']}-{k}.png")
    tag = '<span class="ask">Needs your yes before motion</span>' if p["ask"] else '<span class="ok">For a look: no answer needed</span>'
    rows.append(f"""<section><h2>{html.escape(p['name'])} <small>{p['id']}</small> {tag}</h2>
<div class="pair"><figure><img src="frames/{p['id']}-start.png"><figcaption>START</figcaption></figure>
<figure><img src="frames/{p['id']}-end.png"><figcaption>END</figcaption></figure></div>
<table><tr><th>When</th><td>{html.escape(p['when'])}</td></tr>
<tr><th>Just before</th><td>{html.escape(p['before'])}</td></tr>
<tr><th>Line it plays under</th><td><b>{html.escape(p['under'])}</b></td></tr>
<tr><th>Right after</th><td>{html.escape(p['after'])}</td></tr>
<tr><th>What you see</th><td>{html.escape(p['see'])}</td></tr>
<tr><th>Motion and cost</th><td>{html.escape(p['motion'])}</td></tr>
<tr><th>If you say no</th><td>{html.escape(p['fallback'])}</td></tr></table></section>""")
reply = "1. One can and done (ripped guy in a tank top): approve / changes: \n2. Candy swaps on the calorie scale and couch snacking: (optional)"
page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>3 Healthy Foods LFC R3 frames</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Segoe UI,sans-serif;margin:0;padding:24px 16px;max-width:1500px;margin:auto}}
h1{{font-size:24px;margin:0 0 6px}}h2{{font-size:20px;margin:0 0 10px}}small{{color:var(--mute);font-weight:400}}
.box,section{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;margin:16px 0}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}@media(max-width:800px){{.pair{{grid-template-columns:1fr}}}}
img{{width:100%;border-radius:8px;display:block}}figure{{margin:0}}figcaption{{color:var(--mute);font-size:13px;margin-top:4px}}
table{{border-collapse:collapse;margin-top:10px;width:100%}}th{{text-align:left;color:var(--mute);font-weight:500;width:170px;vertical-align:top;padding:4px 10px 4px 0}}td{{padding:4px 0}}
.ask{{background:#ffcf6b;color:#1b1300;border-radius:20px;padding:2px 10px;font-size:13px;margin-left:8px}}
.ok{{background:#2b6a4c;color:#e6fff1;border-radius:20px;padding:2px 10px;font-size:13px;margin-left:8px}}
textarea{{width:100%;min-height:90px;background:#0b1828;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:10px;font:inherit;box-sizing:border-box}}
button{{background:var(--acc);border:0;border-radius:8px;padding:8px 16px;font-weight:600;margin-top:8px;cursor:pointer}}</style></head><body>
<h1>3 Healthy Foods That Made Me Fat: round 3 frames</h1>
<p>Long-form content. Everything else you approved in round 2 stays as it was (look, voice, graphics, stock, photos, first minute).</p>
<div class="box"><h2>Your decisions (1)</h2><ol><li><b>One can and done, new man:</b> approve the pair below, or tell me what to change. Recommended: approve.</li></ol></div>
<div class="box"><h2>What I decided (overrule anything)</h2><ul>{''.join(f'<li>{html.escape(d)}</li>' for d in DECIDED)}</ul></div>
{''.join(rows)}
<div class="box"><h2>Reply</h2><textarea id="r">{html.escape(reply)}</textarea><br><button onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy</button></div>
</body></html>"""
open(f"{OUT}/index.html", "w").write(page)
print(f"{OUT}/index.html")
