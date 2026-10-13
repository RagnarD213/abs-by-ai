#!/usr/bin/env python3
"""RA-14 round 2 review page (PRE-RENDER-APPROVAL "The review page"): header and decisions, the opening in one docked player,
the AI opener frames with labelled context rows, what I decided, framing pairs, colour candidates beside approved videos,
the unchanged round 1 items as a record, one reply box. Writes round2/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 8815 /Volumes/Extreme/_edit_work/ra14/round2
"""
import html, json
from urllib.parse import quote
E = html.escape
B = json.load(open("beats.json")); M = json.load(open("round2/stills/r2_meta.json")); N = json.load(open("round2/stills/colour_numbers.json"))
R1 = json.load(open("round1/notes_r1.json"))
T = "RA-14 round 2 - opening - "
VID = [("Brighter, golden skin (recommended colour), opener placeholder", T + "brighter gold colour - opener placeholder.mp4"),
       ("RA-01 level colour (runner-up), opener placeholder", T + "RA-01 level colour - opener placeholder.mp4"),
       ("If you approve no opener: camera opening", T + "brighter gold colour - camera opening.mp4"),
       ("Voice with more bass", T + "brighter gold colour - opener placeholder - more bass.mp4")]
LINE = "Guys have figured out the cheat code for getting six pack abs."
IDEAS = [
 dict(id="O1", name="Character creator", rec=True,
      see="A video game character screen. An ordinary guy stands on the turntable, soft around the middle. A slider marked BODY: ABS sits above his head with a pointer on it.",
      action="One shot, 3.6 seconds. The pointer drags the slider from 0% to 100% over about 2.2 seconds and his body leans out as it moves. It holds on 100% for the last second. I draw the slider, the pointer and the numbers over the clip myself, so they stay sharp; the model only changes his body.",
      cost="About $1 a take. I would plan up to two takes: about $2.",
      sense=["Yes. The pointer moves the slider and the body follows it, the way a game slider works. Nothing changes without a cause.",
             "Yes. A stranger sees a game slider marked ABS go from 0% to 100% and a man get abs.",
             "Yes. A setting that simply hands you abs is a cheat. It reads in one viewing."]),
 dict(id="O2", name="8-bit power-up", rec=False,
      see="An old pixel side-scroller. A little pixel dude with a round tummy runs toward a glowing six-pack power-up. The counter in the corner reads ABS x0.",
      action="One shot, 3.6 seconds. He runs for about 1.2 seconds, touches the power-up, the screen flashes white for 3 frames, and he is flexing with pixel abs while the counter flips to ABS x6. I draw the counter myself.",
      cost="I would build this one in code from a few more Codex sprite frames, which costs nothing. If that looks stiff, a video model take is about $1.",
      sense=["Yes. He touches the power-up and changes, like every game power-up.",
             "Yes. Run, grab, abs. The counter says it in two words.",
             "Mostly. A power-up is a shortcut more than a cheat code, so it is a little less exact than the slider. It is the most charming of the three."]),
 dict(id="O3", name="Arcade combo", rec=False,
      see="A guy at an arcade machine with two friends watching. START: hands on the buttons, the machine dim. END: he has stepped back and lifted his shirt to find abs, the machine is lit up like a jackpot and his friends are losing it.",
      action="Two shots with a cut between them (a time jump is a cut, never a morph). Shot 1, about 1.6 seconds: he slams the buttons and the machine comes alive. Cut. Shot 2, about 2.0 seconds: shirt already lifted, he looks down, the friends react. I can put CHEAT CODE ACCEPTED on the machine's screen in code.",
      cost="Two clips at about $1 a take, two takes each: about $4.",
      sense=["Only as a joke. Pressing buttons does not give a man abs, and the clip never pretends it does: the machine pays out, he checks, they are there.",
             "Partly. A stranger sees friends, a jackpot and a man surprised by his own abs. Without the words CHEAT CODE on the machine it would not say cheat code.",
             "Yes, and it is the funniest. It is also the most to fit into 3.6 seconds and the hardest for the model: three faces, hands and a shirt."]),
]
SENSEQ = ["Does everything obey cause and effect?", "With the sound off, would a stranger say what it shows?", "Does it show the line, and does the joke land in one viewing?"]
DECISIONS = [
 dict(short="Opener (Character creator / 8-bit power-up / Arcade combo / none)", q="The opener. Which idea do I animate for the first 3.6 seconds?",
      opts="A (recommended): Character creator. It reads fastest and is the safest to get right. B: 8-bit power-up. C: Arcade combo. D: none, the ad opens on you by the pool. You can approve more than one and choose after seeing them move: all three together come to about $6 to $8 of this ad's $10."),
 dict(short="Framing (A little wider / Wider / Widest)", q="Framing. Both shots wider, as you asked. Which pair?",
      opts="A (recommended): Wider, 14% and 18% wider than round 1. B: A little wider, 7% and 9%. C: Widest, 21% and 24%."),
 dict(short="Colour (Brighter golden skin / RA-01 level / Brighter cooler background)", q="Colour. Three new candidates, round 1 beside them.",
      opts="A (recommended): Brighter, golden skin. B: RA-01 level, the deepest tan. C: Brighter, cooler background. A and B are on the player, moving."),
 dict(short="Analysis card (Soft Blue redraw / keep RA-01 card)", q=R1["decisions"][0]["q"] + " (Asked in round 1, not answered yet.)", opts=R1["decisions"][0]["opts"]),
 dict(short="Voice (as on RA-01 / more bass)", q="Voice: as approved on RA-01, or with the bass lift? (Asked in round 1, not answered yet.)",
      opts="A (recommended): as approved on RA-01. On this roll it already measures as full in the low end as the reference voice. B: the same with 3 dB more bass, which is your 10-12 standard lift for new voices (last button on the player)."),
 dict(short="Recap list (keep / none)", q=R1["decisions"][2]["q"] + " (Asked in round 1, not answered yet.)", opts=R1["decisions"][2]["opts"]),
]
DECIDED = [
 "The AI picture at 5 seconds is out. You stay on camera for \"I'm not talking about an AI picture.\" The goal picture still appears once, later, as the result of the step one demo. Say if you want it out there too.",
 "With that picture gone, the pause I tightened between \"It's AI.\" and \"I'm not talking\" showed as a jump: your head shifts and your mouth snaps open. So the shot size changes right on it. The opening now goes: opener clip, close for \"It's AI.\", wide for \"I'm not talking about an AI picture.\", close for \"real abs in real life\" (the wider close still shows your abs to the waistband), wide for \"Here's how it works.\" The handoff had planned close, wide, close; I changed it because of the jump.",
 "Step one now starts on the close shot, exactly on the change of take instead of 3 frames after it. The new close is about the size of round 1's wide, so the Step 1 label still sits clear of your face. You will see every label again, moving, next round.",
 "The crop now lands exactly on your head at every cut. In round 1 it landed 5 to 20 pixels off because your head was measured 5 times a second; I added a measurement on the first frame of every shot.",
 "Colour, what was actually wrong: not the white balance (the clouds measure neutral, so the camera was set right). You were a stop and a half darker than mid grey in front of a bright sky, and round 1 left you there. Face brightness was 64; the approved RA-01 and Ad 1 sit at 77 to 78.",
 "I looked at every colour candidate at full size beside frames from RA-01's master and the approved Ad 1 vertical before choosing. Simply brightening the picture turned your skin pink, so each candidate holds your skin on the golden hue of the approved videos with a correction that touches skin tones only. I also tried a stronger gold and threw it out: it went yellow in the shadows of your face.",
 "Wider is also sharper. The close shot was a 2.14x enlargement of the 4K picture in round 1; in the recommended pair it is 1.88x.",
 "The opening sample shows the Character creator frames where the opener goes, with a yellow PLACEHOLDER banner. They are still frames with a cut between them. No motion exists.",
 "On the opener frames, every letter is drawn by me in code (the slider, the percentages, the ABS counter). The pictures came from Codex with no lettering. AI-GENERATED sits low on the left, on no face.",
 "Each opener shows men whole, with ordinary faces, and nobody touching a stomach. In the arcade END frame his hands hold the shirt only.",
 "Spend on AI generation so far: $0 of this ad's $10. The six frames were made on your Codex subscription.",
 "Not in this round, still to do before the full ad: check four more tightened pauses inside shots (11.4, 19.7, 31.1 and 41.4 / 42.6 s), lift the captions above the recap card, build the phone demos moving, fix the music tail, then the 16:9.",
]
PAIRWHY = {"F0": "What you called too tight. Shown for comparison only.",
           "F1": "7% and 9% wider. The close shot ends at your waistband. A small change: side by side with round 1 it is easy to miss.",
           "F2": "14% and 18% wider. The close shot shows your abs to just below the waistband; the wide shot shows most of your shorts. A clear step back from round 1, and the punch-in still feels like one.",
           "F3": "21% and 24% wider. The wide shot reaches the bottom of your shorts. Its close shot is exactly round 1's wide, so cutting in to it has less force."}
LOOKS = [
 dict(key="R1_round1", name="Round 1 (what you saw)", rec=False,
      txt="Dim. Your skin reads dark red-brown, the trees are heavy and the picture is flat for a pool."),
 dict(key="C1_approved_level", name="RA-01 level", rec=False,
      txt="Lifted to the brightness of the approved RA-01, and cleaner. The deepest tan and the hardest abs shadows of the three. Wrong with it: still reads as a dull day, and your face stays a little dark."),
 dict(key="C2_brighter_gold", name="Brighter, golden skin", rec=True,
      txt="About one stop brighter than round 1, so it reads as a day by the pool. Skin on the golden hue of the approved videos. Wrong with it: the lightest stones in the wall are close to white (nothing is clipped), and the abs shadows are a little softer than at RA-01 level."),
 dict(key="C3_brighter_cool", name="Brighter, cooler background", rec=False,
      txt="The same brightness with a cooler balance: the whitest wall and the bluest pool. Wrong with it: your skin is slightly less rich, and the whole picture feels a little colder."),
]
UNCHANGED = [("L1", "Step 1 label", "now on the close shot (see What I decided)"), ("P1", "Generating your picture", "unchanged"), ("L2", "Step 2 label", "unchanged"),
             ("A1", "The analysis card", "waiting on decision 4"), ("L3", "Step 3 label", "unchanged"), ("T1", "The app solving it", "unchanged"),
             ("R1", "The recap list", "waiting on decision 6"), ("C1", "The button", "unchanged")]

img = lambda p, alt: f'<a href="{p}" target="_blank"><img loading="lazy" src="{p}" alt="{E(alt)}"></a>'
row = lambda k, v: f'<tr><th>{E(k)}</th><td>{v}</td></tr>'
AFTER = 'A hard cut to you, close, saying "It' + chr(39) + 's AI."'
ideas = []
for d in IDEAS:
    tag = ' <span class="rec">recommended</span>' if d["rec"] else ""
    sense = "".join(f"<li><b>{E(q)}</b> {E(a)}</li>" for q, a in zip(SENSEQ, d["sense"]))
    ideas.append(f"""<section class="idea"><h3>{d['id']} · {E(d['name'])}{tag}</h3>
<div class="pair"><figure>{img(f"stills/{d['id']}-start.jpg", d['name'] + ' start')}<figcaption>START</figcaption></figure>
<figure>{img(f"stills/{d['id']}-end.jpg", d['name'] + ' end')}<figcaption>END</figcaption></figure></div>
<table>{row('When it appears', '0:00.0 to 0:03.6, the first thing on screen.')}
{row('The line it plays under', f'<b>"{E(LINE)}"</b>')}
{row('What comes right after', AFTER)}
{row('What you see', E(d['see']))}{row('Action and length', E(d['action']))}{row('Cost to animate', E(d['cost']))}
{row('If you say no', 'The camera scene: you by the pool, wide, saying the line (third button on the player).')}</table>
<ul class="sense">{sense}</ul>
<p class="meta">Clean frames for the model (nothing drawn on them): <a href="frames/{d['id']}-start.png" target="_blank">start</a>, <a href="frames/{d['id']}-end.png" target="_blank">end</a></p></section>""")
pairs = []
for p in M["pairs"]:
    c, w = p["close"], p["wide"]; rec = ' <span class="rec">recommended</span>' if p["id"] == "F2" else ""
    pairs.append(f"""<section class="card"><h3>{E(p['name'])}{rec}</h3><div class="pair">
<figure>{img(f"stills/{p['id']}-close.jpg", p['name'] + ' close')}<figcaption>Close · {c['crop'][0]}x{c['crop'][1]} · enlarged {c['enlarge']}x</figcaption></figure>
<figure>{img(f"stills/{p['id']}-wide.jpg", p['name'] + ' wide')}<figcaption>Wide · {w['crop'][0]}x{w['crop'][1]} · enlarged {w['enlarge']}x</figcaption></figure></div>
<p>{E(PAIRWHY[p['id']])}</p><p class="meta">Wide is {p['spread']:.2f}x the close. Hair rule unchanged: the top of the frame sits 4% of its height above your highest point in the shot.</p></section>""")
looks = []
for l in LOOKS:
    n = N[l["key"]]; rec = ' <span class="rec">recommended</span>' if l["rec"] else ""
    looks.append(f"""<section class="card"><h3>{E(l['name'])}{rec}</h3><div class="pair">
<figure>{img(f"stills/K-{l['key']}-close.jpg", l['name'] + ' close')}<figcaption>Close</figcaption></figure>
<figure>{img(f"stills/K-{l['key']}-wide.jpg", l['name'] + ' wide')}<figcaption>Wide</figcaption></figure></div>
<p>{E(l['txt'])}</p><p class="meta">Face brightness {n['face']['luma']:.0f} (approved videos 77 to 78) · skin hue {n['face']['hue']:.0f} (approved 53 to 55) · clipped white {n['clipped_pct']:.1f}%</p></section>""")
refs = "".join(f'<figure>{img(f"stills/{f}.jpg", c)}<figcaption>{E(c)}</figcaption></figure>' for f, c in
               (("ref-ra01-a", "RA-01 master (approved 09-18)"), ("ref-ra01-b", "RA-01 master, its goal picture card"), ("ref-ad1-a", "Ad 1 vertical (approved)"), ("ref-ad1-b", "Ad 1 vertical (approved)")))
dec = "".join(f"<li><b>{E(d['q'])}</b><br>{E(d['opts'])}</li>" for d in DECISIONS)
decided = "".join(f"<li>{E(x)}</li>" for x in DECIDED)
unch = "".join(f"<li><b>{i} · {E(n)}</b>: {E(s)}</li>" for i, n, s in UNCHANGED)
reply = "\n".join(f"{i+1}. {d['short']}: " for i, d in enumerate(DECISIONS)) + "\nAnything else to change: "
btn = "".join(f'<button class="{"on" if i == 0 else ""}" data-src="{quote(f)}">{E(n)}</button>' for i, (n, f) in enumerate(VID))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cheat Code Six Pack AD R2</title><style>
:root{{--bg:#0d1420;--panel:#152033;--ink:#eef4fb;--mute:#9db0c7;--line:#27384f;--acc:#68c5ff;--rec:#7be0a0}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:24px 16px 80px}}@media(min-width:1500px){{main{{margin-right:460px}}}}
h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:21px;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:22px}}h3{{font-size:17px;margin:0 0 10px}}
.sub{{color:var(--mute)}}ol,ul{{padding-left:22px}}li{{margin:6px 0}}a{{color:var(--acc)}}
.player{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}
@media(min-width:1500px){{.player{{position:fixed;right:18px;top:18px;width:420px}}}}
video{{width:100%;max-height:70vh;border-radius:10px;background:#000}}
.btns button{{display:block;width:100%;text-align:left;background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:6px 0 0;font-size:14px;cursor:pointer}}
.btns button.on{{border-color:var(--acc);color:var(--acc)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}}
@media(max-width:1000px){{.grid,.grid4{{grid-template-columns:1fr}}}}
.card,.idea{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}.card p,.idea p{{margin:8px 0;font-size:14.5px}}
.pair{{display:flex;gap:8px}}figure{{margin:0;flex:1}}figure img{{width:100%;border-radius:8px;display:block}}figcaption{{font-size:12.5px;color:var(--mute);text-align:center;margin-top:4px}}
table{{border-collapse:collapse;width:100%;font-size:14px;margin-top:10px}}th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:5px 10px 5px 0;width:34%}}td{{padding:5px 0;vertical-align:top}}
tr+tr th,tr+tr td{{border-top:1px solid var(--line)}}
.sense{{font-size:13.5px;color:var(--mute);padding-left:18px}}.sense b{{color:var(--ink);font-weight:600}}
.meta{{color:var(--mute);font-size:13px}}.rec{{color:var(--rec);font-size:12.5px;font-weight:700;border:1px solid var(--rec);border-radius:20px;padding:1px 8px;margin-left:6px;white-space:nowrap}}
.refs{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:14px}}
textarea{{width:100%;height:230px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
</style></head><body><main>
<h1>The Cheat Code For Six Pack Abs · ad · round 2</h1>
<p class="sub">RA-14, vertical 9:16 first. This round has four things: start and end frames for the three opener ideas you picked, wider framing, colour options, and the opening re-cut without the AI picture. No motion is made until you approve frames, and nothing is rendered in full. The ad still runs {B['total']:.1f} seconds with no line cut.</p>
<h2>Carried over from round 1 (not questions)</h2><ul>
<li>The cut, the takes and the length: as shown in round 1.</li><li>Captions, the Soft Blue Light graphics, the two phone demos and the button: as shown in round 1. You asked for no changes; they are listed at the bottom.</li>
<li>Music and voice treatment: as in round 1 (the voice question is decision 5).</li></ul>
<h2>Your decisions ({len(DECISIONS)})</h2><ol>{dec}</ol>
<h2>The opening, re-cut without the AI picture</h2>
<div class="player"><video id="v" controls preload="none" poster="stills/poster.jpg" src="{quote(VID[0][1])}"></video>
<div class="btns">{btn}</div>
<p class="sub" style="font-size:13px">The first 10.6 seconds, up to "Step one", in the recommended framing. The yellow banner marks the opener placeholder: two still frames, no motion yet.</p></div>
<p>Play it on the panel (on a narrow window it sits just above). First button: the recommended colour and framing with the Character creator frames standing in for the opener. Second: the same in the runner-up colour. Third: what plays if you approve no opener. Fourth: the bass version of the voice.</p>
<h2>The opener: start and end frames for your three ideas</h2>
<p class="sub">All three play under the same line and are followed by the same cut. Frames only. Budget for this ad: $10 in total, spent $0.</p>
<div class="grid">{''.join(ideas)}</div>
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Framing: three wider pairs</h2>
<p class="sub">The same two moments in every pair: the close shot on "real abs in real life", the wide shot on "I'm not talking about an AI picture". All are wider than the written framing standard, which is your call for this roll. Click a still for full size.</p>
<div class="grid4">{''.join(pairs)}</div>
<h2>Colour: three candidates beside the approved videos</h2>
<p class="sub">The same two moments, in the recommended framing, no captions. Approved videos underneath for comparison.</p>
<div class="grid4">{''.join(looks)}</div>
<div class="refs">{refs}</div>
<h2>Shown in round 1, not changed this round (a record, not questions)</h2><ul>{unch}</ul>
<p class="sub">Round 1 page, with each of these as a still: <a href="http://127.0.0.1:8814/" target="_blank">http://127.0.0.1:8814/</a></p>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
document.querySelectorAll('.btns button').forEach(b=>b.onclick=()=>{{const v=document.getElementById('v');const t=v.currentTime;v.src=b.dataset.src;v.currentTime=t;v.play();document.querySelectorAll('.btns button').forEach(x=>x.classList.toggle('on',x===b))}});
</script></body></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash on the page"
open("round2/index.html", "w").write(page)
json.dump({"decisions": DECISIONS, "decided": DECIDED, "ideas": IDEAS, "looks": LOOKS, "videos": VID}, open("round2/notes_r2.json", "w"), indent=1)
print("round2/index.html", len(page), "bytes")
