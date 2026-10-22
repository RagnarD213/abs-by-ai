#!/usr/bin/env python3
"""RA-09 round 1 review page (PRE-RENDER-APPROVAL "The review page"; VIDEO-RULES 2026-10-08 round 1 shows every graphic and clip;
2026-10-14 a short ad shows the whole video; 2026-10-16 colour and voice options in round 1). Writes r1/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 9109 /Volumes/Expansion/_edit_work/RA-09/r1
"""
import html, json, os
from urllib.parse import quote
E = html.escape
PL = json.load(open("beats.json")); CU = json.load(open("r1/cuts.json"))
CK = json.load(open("r1/checks.json")) if os.path.exists("r1/checks.json") else {}
W = json.load(open("words_aligned.json"))["words"]
STATUS = json.load(open("r1/status.json")) if os.path.exists("r1/status.json") else {}
TOT = PL["total"]


def speech(a, b):
    return " ".join(w["w"] for w in W if a <= w["t"] < b)


ITEMS = [
 dict(id="H1", name="Hook: AI changing the world", kind="library AI clip A0014, full screen",
      copy="Chip: AI-GENERATED, placed by measuring the people in the frame.",
      src="A ripped middle-aged man flexes and laughs beside a humanoid robot whose eyes light up (made for Ad 3, used in Ads 3, 13 and 14). Source 0 to 2.37 s. Passed the motion check and two fresh independent reviews on exactly this window (Dan's three sense questions answered yes)."),
 dict(id="G1", name="An AI-generated picture", kind="the prospect's AI goal picture, Soft Blue photo scene",
      copy="Chip: AI-GENERATED under the photo.",
      src="The lake-dock man's real absbyai.com result (RA-04 round 5), the same picture and treatment you approved in First Step Abs round 2. Never your picture (your 10-17 rule)."),
 dict(id="W1", name="Real abs in real life", kind="your ab wheel B-roll (library B0427), full-height card",
      copy="No label: real moving footage of you.",
      src="The exact W1 you approved in First Step Abs: B0427 from 2.50 s, already rolling out, same brightening and colour so it sits with the pool footage."),
 dict(id="P1", name="Upload, then generate", kind="phone demo: the prospect's real generation",
      copy="The Generate tap and the scan over his before photo (AI-GENERATED under the phone: his before photo is AI-made), then his goal picture from \"with your dream body\", AI-GENERATED.",
      src="B0550, one real generation on absbyai.com, normal speed, in the approved iPhone shell. Same man before and after."),
 dict(id="A1", name="The analysis card", kind="the shared Soft Blue analysis card (HyperFrames)",
      copy="Rows land on \"exactly how much fat\", \"you need to lose\" and \"gain muscle\"; YOUR PERSONAL PLAN band on \"to make your dream body real\". No numbers printed.",
      src="_shared/hyperframes/analysis-card on the prospect's goal picture, as approved in First Step Abs."),
 dict(id="T1", name="Workout and nutrition plan", kind="approved app tour B0544 in the phone shell",
      copy="The AI Trainer's Push-Up demo on \"personalized workout\" (its own AI chip inside the app), then the Macro Tracker meal photo and breakdown on \"nutrition plan\".",
      src="B0544 (approved for reuse 2026-10-10), the same two parts as First Step Abs."),
 dict(id="L1", name="Key point", kind="Soft Blue lower third, under the captions on a wide shot",
      copy="KEY POINT / A Coach, Not Just A Picture",
      src="lower-third template, 24 px under the caption line, over your shorts (your 10-17 placement). It distils the ad's point rather than repeating \"AI always there to coach you\"."),
 dict(id="I1", name="Got injured?", kind="Fire Your Trainer's approved injury clip",
      copy="Chip: AI-GENERATED (as approved in Fire Your Trainer).",
      src="The exact card you finalized in Fire Your Trainer (library A0179: the man in a sling walks into the gym, then does the leg press with his phone). Unchanged pixels, all 62 frames."),
 dict(id="G2", name="Can't make it to the gym", kind="Fire Your Trainer's approved gym-closed clip",
      copy="Chip: AI-GENERATED (as approved).",
      src="The exact 14-frame card you approved in Fire Your Trainer: he opens his palms at the CLOSED sign. It plays on \"...gym one day?\", then you say \"AI will\" and the home workout follows."),
 dict(id="M1", name="A home workout", kind="Fire Your Trainer's approved home-workout clip",
      copy="Chip: AI-GENERATED (as approved).",
      src="The exact card you approved in Fire Your Trainer (library A0196): the same man curls a dumbbell in his living room, on \"swap out your gym workout for a home workout\"."),
 dict(id="C1", name="Closing button", kind="Soft Blue CTA button, under the captions on a wide shot",
      copy="Tap The Button Below / Get Started With AI",
      src="cta template, 24 px under the caption line over your shorts, to the end. Big line is new; First Step Abs used \"See Yourself With Abs\"."),
]
DECISIONS = [
 dict(short="Colour (A / B / C)", q="Colour, shown below on the same two moments beside the approved pool reference.",
      opts="A (recommended): the approved pool look exactly as in First Step Abs and The Cheat Code (your face measures the same on this roll). B: a third of a stop brighter. C: richer colour."),
 dict(short="Voice (V1 / V2 / V3)", q="Voice, three level-matched clips of the same 12.6 seconds below.",
      opts="V1 (recommended): +1.5 dB bass, as you finalized on First Step Abs (this roll's low end already sits at the reference). V2: the +3 dB house lift. V3: no lift."),
 dict(short="Opening shot (keep / swap)", q="The first 2.4 seconds: the robot-and-ripped-man clip under \"Do you think AI is changing the world?\".",
      opts="A (recommended): keep. B: open on your ab wheel clip instead. C: a new AI opener: pick one of the ideas listed under What I decided and I bring its start and end frames next round."),
 dict(short="Whole ad (approve / changes)", q="The whole 9:16 ad.",
      opts="A: approve it; I then build the 16:9 from the same edit and run the full delivery. B: changes (name them by time)."),
]
DECIDED = [
 "Length: every scripted line is kept and the talk plays 1.06x faster, the way you ruled on RA-05 (\"don't cut any of the lines, but just accelerate the video as necessary to get it under 60 seconds\"). Airtight it ran 61.7 s; now 58.6 s, under the 0:59 ceiling.",
 "Take: you read the script once. One stumble inside it (\"I'm not just talking about an...\", stopped and restarted) is cut; the clean restart is kept. Every other line was checked in isolated 8-second windows: clean.",
 "Four short pauses kept on purpose (after \"work around it.\", after \"one day?\" and around \"Tap\") so the approved Fire Your Trainer clips land on their words and no shot of you lasts a split second.",
 "Captions run over the bottom of the prospect's two photos, as you chose to keep on First Step Abs.",
 "Spoken versus script: you said \"and get six-pack abs\" (the script has \"get you\"); kept as filmed.",
 "The before/after picture is the AI prospect everywhere (your 10-17 rule); your real self appears only as moving footage (no label on moving footage).",
 "Graphics sit just under the captions on wide shots, on your shorts, never on your abs (your First Step Abs note). Only two graphics: the key point and the closing button; the clips carry the rest.",
 "Opening: I tried the first-5-seconds order. The best existing clip is A0014, a ripped man beside a robot that switches on: it says AI and abs before you speak. New AI opener ideas if you want one instead: (1) a man pulls a sheet off a mirror and his reflection is a ripped version of him; (2) a robot hands a man a printed plan, he flips it and abs appear on his own shirtless reflection; (3) a newspaper boy shouting \"AI changes everything\" hands a guy a phone showing his goal picture.",
 "No sound effects added; music bed as First Step Abs (Realizer, 32 dB under the voice).",
 "The 16:9 is built after you approve this 9:16, from the same edit (First Step Abs order), so a change here is not built twice.",
 "Claim lines: none flagged (your 10-14 rule: lines in the script are approved). On-screen text prints no numbers or comparisons.",
]


def btn(i):
    c = CU["items"][i]
    return f'<button class="ctx" data-src="{quote(c["clip"].replace("r1/", ""))}" data-poster="{quote(c["clip"].replace("r1/", "").replace(".mp4", ".jpg"))}">Play it moving, in context</button>'


cards = []
for it in ITEMS:
    c = CU["items"][it["id"]]; a, b = c["a"], c["b"]
    sp = (f'<details><summary>Speech before / during / after</summary><p><b>Before:</b> {E(speech(a - 3, a))}</p>'
          f'<p><b>During:</b> {E(speech(a, b))}</p><p><b>After:</b> {E(speech(b, b + 3))}</p></details>')
    chk = CK.get(it["id"]); chk = f'<p class="meta">Checked: {E(chk)}</p>' if chk else ""
    cards.append(f"""<section class="card"><h3>{it['id']} · {E(it['name'])}</h3>
<a href="{quote(c['still'].replace('r1/', ''))}" target="_blank"><img loading="lazy" src="{quote(c['still'].replace('r1/', ''))}" alt="{E(it['name'])}"></a>
{btn(it['id'])}
<table><tr><th>On screen</th><td>{a:.2f} to {b:.2f} s</td></tr><tr><th>What it is</th><td>{E(it['kind'])}</td></tr>
<tr><th>Copy</th><td>{E(it['copy'])}</td></tr><tr><th>Source</th><td>{E(it['src'])}</td></tr></table>
{chk}{sp}</section>""")

looks = ""
for w, lab in (("close", "Close shot (0:03)"), ("wide", "Wide shot (0:07)")):
    figs = "".join(f'<figure><a href="options/look-{k}-{w}.jpg" target="_blank"><img loading="lazy" src="options/look-{k}-{w}.jpg"></a><figcaption>{E(n)}</figcaption></figure>'
                   for k, n in (("A_approved", "A (recommended): approved look"), ("B_brighter", "B: brighter"), ("C_richer", "C: richer"),
                                ("ref-ra14-approved", "Reference: the approved pool look (The Cheat Code)")))
    looks += f'<h3>{E(lab)}</h3><div class="pair">{figs}</div>'
voices = "".join(f'<div class="aud"><b>{E(n)}</b><audio controls preload="none" src="options/voice-{k}.m4a"></audio></div>'
                 for k, n in (("V1_plus1.5dB", "V1 (recommended): +1.5 dB bass"), ("V2_plus3dB", "V2: +3 dB bass"), ("V3_no_lift", "V3: no bass lift")))

whole = CU["whole"]; WH = os.path.basename(whole["file"]); WR = WH.replace('.mp4', ' - REVIEW 540p.mp4')
dec = "".join(f"<li><b>{E(d['q'])}</b><br>{E(d['opts'])}</li>" for d in DECISIONS)
decided = "".join(f"<li>{E(x)}</li>" for x in DECIDED)
reply = "\n".join(f"{i+1}. {d['short']}: " for i, d in enumerate(DECISIONS)) + "\nAnything else to change: "
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Changing World AD R1</title><style>
:root{{--bg:#0d1420;--panel:#152033;--ink:#eef4fb;--mute:#9db0c7;--line:#27384f;--acc:#68c5ff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:24px 16px 80px}}@media(min-width:1500px){{main{{margin-right:460px}}}}
h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:21px;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:22px}}h3{{font-size:17px;margin:14px 0 10px}}
.sub{{color:var(--mute)}}ol,ul{{padding-left:22px}}li{{margin:6px 0}}a{{color:var(--acc)}}
.player{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}
@media(min-width:1500px){{.player{{position:fixed;right:18px;top:18px;width:420px}}}}
video{{width:100%;max-height:72vh;border-radius:10px;background:#000}}
.btns button,.ctx{{display:block;width:100%;text-align:left;background:#1d2c44;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:6px 0 0;font-size:14px;cursor:pointer}}
.btns button.on,.ctx.on{{border-color:var(--acc);color:var(--acc)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}@media(max-width:1000px){{.grid{{grid-template-columns:1fr}}}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}}.card img{{width:100%;border-radius:8px;display:block}}
table{{border-collapse:collapse;width:100%;font-size:14px;margin-top:10px}}th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:5px 10px 5px 0;width:30%}}td{{padding:5px 0;vertical-align:top}}
tr+tr th,tr+tr td{{border-top:1px solid var(--line)}}details{{font-size:13.5px;color:var(--mute);margin-top:8px}}summary{{cursor:pointer}}
.meta{{color:var(--mute);font-size:13px}}.pair{{display:flex;gap:10px;flex-wrap:wrap}}.pair figure{{margin:0;flex:1;min-width:140px}}.pair img{{width:100%;border-radius:8px}}figcaption{{font-size:12.5px;color:var(--mute);text-align:center}}
.aud{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px;margin:8px 0}}.aud audio{{width:100%;margin-top:6px}}
textarea{{width:100%;height:200px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
</style><body><main>
<h1>Do You Think AI Is Changing The World? · ad · round 1</h1>
<p class="sub">RA-09, vertical 9:16, the whole ad: {TOT:.1f} seconds, every scripted line. Built from parts you already approved (the pool look and framing, the prospect's generation and analysis card, the app tour, your ab wheel clip, and three Fire Your Trainer clips) plus one library hook clip. Spend: $0 (no new clips generated).</p>
<p class="sub"><b>Checks on the exact file:</b> {E(STATUS.get('checks', 'pending'))}</p>
<h2>Your decisions ({len(DECISIONS)})</h2><ol>{dec}</ol>
<h2>The whole ad</h2>
<div class="player"><video id="v" controls preload="none" poster="stills/whole.jpg" src="{quote(WR)}"></video>
<div class="btns"><button class="on" data-src="{quote(WR)}" data-poster="stills/whole.jpg">Whole ad (540p)</button>
<button data-src="{quote(WH)}" data-poster="stills/whole.jpg">Whole ad, full 1080x1920</button></div>
<p class="sub" style="font-size:13px">Built with colour A and voice V1. Every "Play it moving, in context" button below loads into this one player. The full file is also in Videos to Review for VLC.</p></div>
<h2>Colour options</h2>{looks}
<h2>Voice options (same passage, matched loudness)</h2>{voices}
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Every clip and graphic, in order, moving in context</h2>
<p class="sub">Each still is the settled moment on its real frame, with its caption. The button plays it with about 3 seconds of speech either side.</p>
<div class="grid">{''.join(cards)}</div>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
const v=document.getElementById('v');
function play(b){{v.poster=b.dataset.poster;v.src=b.dataset.src;v.play();document.querySelectorAll('.btns button,.ctx').forEach(x=>x.classList.toggle('on',x===b));
if(b.classList.contains('ctx')&&window.innerWidth<1500)v.scrollIntoView({{behavior:'smooth',block:'center'}})}}
document.querySelectorAll('.btns button,.ctx').forEach(b=>b.onclick=()=>play(b));
</script></body></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash on the page"
open("r1/index.html", "w").write(page)
json.dump({"decisions": DECISIONS, "decided": DECIDED, "items": ITEMS}, open("r1/notes_r1.json", "w"), indent=1)
print("r1/index.html", len(page), "bytes")
