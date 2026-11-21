"""RO-29 round 3 review page: the full film, only what changed, with jump buttons."""
import html
O = "/Volumes/Expansion/_edit_work/RO-29/round3/review"; V = "RO-29 round 3 - full film - REVIEW 540p.mp4"
def mm(t): return f"{int(t//60)}:{t%60:04.1f}"
ch = [(1.0, "0:03 The pitcher no longer shakes", "It shimmered through the end of the phone clip. It now holds perfectly still there and in the bartender shot right after it. Everything else in both clips is the same."),
      (207.5, "3:30 New: the divorce papers", "On \"If your wife stresses you out all the time, divorce her\": the ripped husband hands his average-looking wife the DIVORCE PAPERS, she takes them and her jaw drops. Then it goes straight into the \"I quit\" clip."),
      (219.0, "3:41 The wife is slimmer", "She is now slightly overweight, not obese. The husband is the same. His mouth stays mostly shut (no paid lip sync, you did not ask for it): he does open it briefly a couple of times, and it reads as a groan."),
      (268.0, "4:30 He eats through the fight", "No more chicken or scale. He takes a bite and chews calmly with his meal prep in hand, unbothered, while she rants right behind him. She starts to turn and storm off as the clip ends.")]
rows = "".join(f"<li><button onclick='go({w})'>{mm(w)}</button> <b>{html.escape(t)}</b><br>{html.escape(d)}</li>" for w, t, d in ch)
dec = ["<b>Same two people in the divorce clip and the couch clip,</b> so the gag reads as one couple. She is the same ordinary-looking wife in both.",
       "<b>The eating clip ends as she starts to storm off.</b> The take has her leaving fully, but he opens wide for a pained-looking bite right after, so I cut before that.",
       "<b>I read \"certain m-frames\" as start and end frames</b> for a new AI clip.",
       "<b>No lip sync.</b> You did not answer that question, so I did not spend it. Say \"lip sync OK\" and I will add it (about $0.50)."]
chk = ["Each new clip went through the picture check, the motion check and a fresh reviewer. The papers and couch takes passed. The eating take failed on that wide bite, so I moved the cut: the second half passed review and I checked the first half (the calm bite) myself.",
       "A fresh judge went through every frame strip of this exact film (202 images, 95 joins): no defects. It noted one thing to eyeball: at 5:18 your hands go from flat on the table to raised across a cut; the punch-in hides it.",
       "Audio is untouched from round 2 and its checks match: loudness -14.2, true peak -2.0. Voice tone row red because of the bass lift you picked.",
       "<b>Still nobody has listened to it.</b> Listen at 4:51 and from 3:39 to 3:57, as flagged last round.",
       "Hair room: closest 38 px. Other red delivery rows are the same as round 2 and explained there: B-roll share 39% against a 40% minimum, and three false alarms checked by hand.",
       "The full independent reviewer did not re-watch this round; only these four spots changed."]
page = f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Cortisol Belly, round 3</title><style>
:root{{--bg:#0e1622;--card:#16212f;--tx:#e8eef6;--mu:#9fb0c3;--ac:#5fb4ff}}
body{{margin:0;background:var(--bg);color:var(--tx);font:16px/1.5 -apple-system,Segoe UI,sans-serif}}main{{max-width:980px;margin:0 auto;padding:16px}}
section{{background:var(--card);border-radius:12px;padding:16px 18px;margin:14px 0}}h1{{font-size:24px;margin:8px 0}}h2{{font-size:19px;margin:4px 0 10px}}
video{{width:100%;border-radius:8px;background:#000}}button{{background:var(--ac);color:#04121f;border:0;border-radius:6px;padding:3px 9px;font-weight:600;cursor:pointer}}
li{{margin:8px 0}}.t{{color:var(--mu)}}textarea{{width:100%;min-height:130px;background:#0b121c;color:var(--tx);border:1px solid #2a3a4f;border-radius:8px;padding:8px;font:15px/1.4 inherit;box-sizing:border-box}}
</style></head><body><main>
<h1>Cortisol Belly Is Real, But TikTok Has It Wrong (RO-29), round 3</h1>
<p>Only four spots changed since round 2. Each button jumps a few seconds before the change.</p>
<section><h2>The full film (5:29)</h2><video id=v controls preload=metadata src="{html.escape(V)}"></video>
<p class=t>Full quality for VLC: Videos to Review / Cortisol Belly LFC R3 - full film.mp4</p></section>
<section><h2>What changed ({len(ch)})</h2><ol>{rows}</ol></section>
<section><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>'+x+'</li>' for x in dec)}</ul></section>
<section><h2>Checks</h2><ul>{''.join('<li>'+x+'</li>' for x in chk)}</ul></section>
<section><h2>One reply</h2><textarea id=r>Approve as final, or list changes (time + what):

</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section>
</main><script>function go(t){{const v=document.getElementById('v');v.currentTime=t;v.play()}}</script></body></html>"""
open(f"{O}/index.html", "w").write(page); print("page ok", len(ch))
