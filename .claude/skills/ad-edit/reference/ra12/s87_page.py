#!/usr/bin/env python3
"""RA-14 round 3 review page (PRE-RENDER-APPROVAL "The review page"): header + decisions, the finished first 30 seconds in the one
docked player, the O2 opener moving, "What I decided", then every graphic and clip in timeline order three per row, each with
"Play it moving, in context". One reply box. Writes round1/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 8816 /Volumes/Expansion/_edit_work/ra12/round3
"""
import html, json, os
from urllib.parse import quote
E = html.escape
PL = json.load(open("beats.json")); CU = json.load(open("round1/cuts.json")); CK = json.load(open("round1/checks.json"))
W = json.load(open("words_aligned.json"))["words"]
FPS = 30000 / 1001


def speech(a, b):
    return " ".join(w["w"] for w in W if a <= w["t"] < b)


ITEMS = [
 dict(id="W1", name="Not a workout", kind="library AI clip A0151, in a card", status="new for this ad",
      copy="Chip: AI-GENERATED under the card.", src="A0151, a heavyset man doing slow crunches on a mat (used once before, RO-02). Full height; sides trimmed to 1400 px because filling the screen cuts him in half."),
 dict(id="D1", name="Not a diet", kind="library AI clip A0069, in a card", status="new for this ad",
      copy="Chip: AI-GENERATED under the card.", src="A0069, a man pushes away a plate of pizza toward a salad (0.55-1.47 s only: the file cuts to a push-up shot at 1.9 s)."),
 dict(id="G1", name="It's a picture", kind="your AI goal picture, Soft Blue photo scene", status="new for this ad",
      copy="Chip: AI-GENERATED under the photo.", src="dan by pool.png, the same goal picture the phone demo generates later."),
 dict(id="K1", name="Look at it every day", kind="your goal picture as a phone wallpaper (built in code)", status="new for this ad",
      copy="Chip: AI-GENERATED under the phone.", src="dan by pool.png filling the screen of the approved iPhone shell, slow 4 % push. Replaced library clip A0074, whose photo tilted its head by itself."),
 dict(id="Q1", name="When everyone else quits", kind="library AI clip A0172, in a card", status="new for this ad",
      copy="Chip: AI-GENERATED under the card.", src="A0172, a worn-out beginner flat on a gym floor beside a tiny pink dumbbell (0.40-1.87 s, before he gets up). Also covers the join between your two takes."),
 dict(id="P1", name="Generating your picture", kind="phone demo", status="approved in RA-14; retimed to these words",
      copy="Options, the tap, \"Refining\" and \"Rendering your goal image\" over your photo (chip: Real picture of me. Not AI-generated.), then your goal picture, AI-GENERATED, on \"with ripped six-pack abs\".",
      src="The approved self-generation demo (Ad 14 R3), same person before and after, in the approved iPhone shell, normal speed."),
 dict(id="C1", name="First button", kind="Soft Blue CTA button", status="new copy",
      copy="Tap The Button Below / Generate Yours", src="cta template, on \"Tap the button below to generate yours.\""),
 dict(id="A1", name="The analysis card", kind="the shared Soft Blue analysis card", status="your RA-14 standard; new timing",
      copy="Your goal picture with the scan, then BODY FAT, FAT TO LOSE, MUSCLE TO GAIN landing on \"how much fat\", \"to lose\", \"gain muscle\", and a YOUR PERSONAL PLAN band on \"to make your dream body real\". No numbers.",
      src="_shared/hyperframes/analysis-card"),
 dict(id="T1", name="Workout and nutrition plan", kind="phone demo", status="approved in RA-14; reordered to these words",
      copy="The tap on AI Trainer and its Push-Up demo on \"personalized workout\", then the meal photo analysed to 775 calories on \"and nutrition plan\".",
      src="App tour B0544 (approved for reuse 10-10), approved iPhone shell, normal speed."),
 dict(id="L1", name="Key point", kind="Soft Blue lower third", status="new, the only lower third",
      copy="KEY POINT / See Your Goal Before You Start", src="lower-third template, on \"Workouts and diets fail without a goal. So take the first step.\""),
 dict(id="C2", name="Closing button", kind="Soft Blue CTA button", status="new copy",
      copy="Tap The Button Below / See Yourself With Abs", src="cta template, to the last frame"),
]
IDEAS = [
 ("Missing box lid", "A man stares at a pile of jigsaw pieces with no picture to follow, turns the box over, and the lid shows a ripped man by a pool: now he knows what he is building. The picture-first idea in one look."),
 ("Mirror double take", "A regular guy brushing his teeth glances at the mirror; the reflection is him with abs. He looks down at himself, back at the mirror, grins."),
 ("Blindfold archery", "A man in gym clothes fires arrows blindfolded; they go everywhere. He lifts the blindfold: his goal picture is pinned on the bullseye. Next arrow, dead centre."),
 ("Roundabout", "A man drives round and round a roundabout with no destination. His phone lights up with his goal picture as the destination, and he takes the exit."),
 ("Flat-pack chaos", "A man builds furniture with no picture on the instructions and ends up with a lopsided mess; cut to the box photo, which is a ripped man posing."),
 ("Dartboard in the dark", "Lights off, a guy throws darts at nothing; lights on, his goal picture is the dartboard and he walks up to it."),
]
DECISIONS = [
 dict(short="Whole ad (approve / changes)", q="The whole 9:16 ad (46 seconds, top of the page). Every graphic and clip is below with its own in-context button.",
      opts="A (recommended): approve it, then I build the 16:9 from the same edit and run the full delivery. B: changes (name them by ID or time)."),
 dict(short="Buttons and key point (keep / move)", q="The two buttons and the KEY POINT lower third sit across your lower chest and abs (0:22.9, 0:39.3, 0:42.7 to the end). That is the standard Soft Blue spot you approved on RA-14 two days ago, but the independent judge flagged it: the closing button that says \"See Yourself With Abs\" covers your abs.",
      opts="A (recommended): keep the RA-14 spot. It stays clear of YouTube's own buttons along the bottom of a Short. B: a compact button at chest height beside you (the RA-01 style), built next round."),
 dict(short="Opener (keep / AI ideas)", q="The first 4 seconds are a fast montage from clips we already own: you, the crunches clip on \"isn't a workout\", the pizza clip on \"it's not a diet\", your goal picture on \"It's a picture.\" Or I make an AI opener (ideas below).",
      opts="A (recommended): keep the montage. B: pick the ideas you want as START and END frames (no cost to make frames; motion about $1 each of this ad's $10)."),
]
DECIDED = json.load(open("round1/decided.json"))


def btn(i):
    c = CU["items"][i]
    return f'<button class="ctx" data-src="{quote(c["clip"].replace("round1/", ""))}" data-poster="{quote(c["clip"].replace("round1/", "").replace(".mp4", ".jpg"))}">Play it moving, in context</button>'


cards = []
for it in ITEMS:
    c = CU["items"][it["id"]]
    a, b = c["a"], c["b"]
    sp = (f'<details><summary>Speech before / during / after</summary><p><b>Before:</b> {E(speech(a - 3, a))}</p>'
          f'<p><b>During:</b> {E(speech(a, b))}</p><p><b>After:</b> {E(speech(b, b + 3))}</p></details>')
    chk = CK.get(it["id"])
    chk = f'<p class="meta">Checked: {E(chk)}</p>' if chk else ""
    cards.append(f"""<section class="card"><h3>{it['id']} · {E(it['name'])}</h3>
<a href="{quote(c['still'].replace('round1/', ''))}" target="_blank"><img loading="lazy" src="{quote(c['still'].replace('round1/', ''))}" alt="{E(it['name'])}"></a>
{btn(it['id'])}
<table><tr><th>On screen</th><td>{a:.2f} to {b:.2f} s</td></tr><tr><th>What it is</th><td>{E(it['kind'])}</td></tr>
<tr><th>Status</th><td>{E(it['status'])}</td></tr><tr><th>Copy</th><td>{E(it['copy'])}</td></tr><tr><th>Source</th><td>{E(it['src'])}</td></tr></table>
{chk}{sp}</section>""")

whole = CU["whole"]
dec = "".join(f"<li><b>{E(d['q'])}</b><br>{E(d['opts'])}</li>" for d in DECISIONS)
decided = "".join(f"<li>{E(x)}</li>" for x in DECIDED)
ideas = "".join(f"<li><b>{E(n)}</b>: {E(t)}</li>" for n, t in IDEAS)
reply = "\n".join(f"{i+1}. {d['short']}: " for i, d in enumerate(DECISIONS)) + "\nAnything else to change: "
WH = os.path.basename(whole["file"]); WR = WH.replace('.mp4', ' - REVIEW 540p.mp4')
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>First Step Abs AD R1</title><style>
:root{{--bg:#0d1420;--panel:#152033;--ink:#eef4fb;--mute:#9db0c7;--line:#27384f;--acc:#68c5ff;--rec:#7be0a0}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:24px 16px 80px}}@media(min-width:1500px){{main{{margin-right:460px}}}}
h1{{font-size:28px;margin:0 0 6px}}h2{{font-size:21px;margin:34px 0 10px;border-top:1px solid var(--line);padding-top:22px}}h3{{font-size:17px;margin:0 0 10px}}
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
.meta{{color:var(--mute);font-size:13px}}.pair{{display:flex;gap:10px}}.pair figure{{margin:0;flex:1}}.pair img{{width:100%;border-radius:8px}}figcaption{{font-size:12.5px;color:var(--mute);text-align:center}}
textarea{{width:100%;height:200px;background:#0a101a;color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:12px;font:15px/1.5 ui-monospace,Menlo,monospace}}
.copy{{background:var(--acc);color:#04121f;border:0;border-radius:8px;padding:10px 16px;font-weight:700;margin-top:8px;cursor:pointer}}
</style><body><main>
<h1>The First Step To Getting Abs Isn't A Workout · ad · round 1</h1>
<p class="sub">RA-12, vertical 9:16 first, from roll C1667 (the same pool roll as RA-14, minutes apart). Reused from RA-14 as you approved it on this roll: the wider crop, the brighter golden-skin colour, the voice with the bass lift, the analysis card, the phone demo and the app tour. The ad runs {PL['total']:.1f} seconds with every scripted line; nothing is a placeholder. Spend: about 2 cents of transcription, $0 of AI generation.</p>
<h2>Your decisions ({len(DECISIONS)})</h2><ol>{dec}</ol>
<h2>The whole ad, finished</h2>
<div class="player"><video id="v" controls preload="none" poster="stills/whole.jpg" src="{quote(WR)}"></video>
<div class="btns"><button class="on" data-src="{quote(WR)}" data-poster="stills/whole.jpg">Whole ad (540p)</button>
<button data-src="{quote(WH)}" data-poster="stills/whole.jpg">Whole ad, full 1080x1920</button></div>
<p class="sub" style="font-size:13px">Every "Play it moving, in context" button below loads into this one player. The full file is also in Videos to Review for VLC.</p></div>
<h2>AI opener ideas (only if you want one instead of the montage)</h2>
<p class="sub">Each would play under "The first step to getting six pack abs isn't a workout. And it's not a diet." and hand over to your goal picture on "It's a picture." If you pick none, the montage stays.</p><ol>{ideas}</ol>
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Every graphic and clip, in order, moving in context</h2>
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
open("round1/index.html", "w").write(page)
json.dump({"decisions": DECISIONS, "decided": DECIDED, "items": ITEMS, "ideas": IDEAS}, open("round1/notes_r1.json", "w"), indent=1)
print("round1/index.html", len(page), "bytes")
