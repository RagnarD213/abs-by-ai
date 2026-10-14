#!/usr/bin/env python3
"""RA-14 round 3 review page (PRE-RENDER-APPROVAL "The review page"): header + decisions, the finished first 30 seconds in the one
docked player, the O2 opener moving, "What I decided", then every graphic and clip in timeline order three per row, each with
"Play it moving, in context". One reply box. Writes round3/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 8816 /Volumes/Extreme/_edit_work/ra14/round3
"""
import html, json, os
from urllib.parse import quote
E = html.escape
PL = json.load(open("beats_r3.json")); CU = json.load(open("round3/cuts.json")); CK = json.load(open("round3/checks.json"))
W = json.load(open("words_aligned.json"))["words"]
FPS = 30000 / 1001


def speech(a, b):
    return " ".join(w["w"] for w in W if a <= w["t"] < b)


ITEMS = [
 dict(id="O2", name="Opener: 8-bit power-up", kind="AI clip, built in code from your approved frames", status="new: moving for the first time",
      copy="Counter ABS x0 to ABS x6 (drawn in code). Chip: AI-GENERATED, low left.",
      src="Your approved START and END frames, plus one Codex sprite sheet for the second run pose and the hop (round3/opener/raw/o2_runsheet.png)."),
 dict(id="L1", name="Step 1 label", kind="Soft Blue lower third", status="shown in round 1; now on the new framing, moving",
      copy="STEP 1 / Generate Your Goal Picture", src="lower-third template"),
 dict(id="P1", name="Generating your picture", kind="phone demo", status="shown in round 1 as stills; now moving",
      copy="Options screen, tap, \"Mapping muscle groups\" and \"Rendering your goal image\" over your photo (chip: Real picture of me. Not AI-generated.), then your goal picture full card, AI-GENERATED.",
      src="The approved self-generation demo (Ad 14 R3), in the approved iPhone shell, at normal speed."),
 dict(id="L2", name="Step 2 label", kind="Soft Blue lower third", status="shown in round 1; now moving",
      copy="STEP 2 / AI Builds Your Custom Plan", src="lower-third template"),
 dict(id="A1", name="The analysis card, Soft Blue (new standard)", kind="new shared HyperFrames template", status="new: your round 2 instruction",
      copy="Your goal picture with a scan line, then BODY FAT, FAT TO LOSE, MUSCLE TO GAIN bars and a YOUR WORKOUT PLAN band. No numbers. Chip: AI-GENERATED, under the picture.",
      src="_shared/hyperframes/analysis-card (every video from now on)"),
 dict(id="L3", name="Step 3 label", kind="Soft Blue lower third", status="shown in round 1; now moving",
      copy="STEP 3 / AI Coaches You Every Day", src="lower-third template"),
 dict(id="T1", name="The app solving it", kind="phone demo", status="shown in round 1 as stills; now moving",
      copy="A meal photo analysed to 775 calories, then the AI Trainer's Push-Up demo (the app's own AI-GENERATED chip).",
      src="App tour B0544 (approved for reuse 10-10), in the approved iPhone shell, at normal speed."),
 dict(id="R1", name="The recap list", kind="Soft Blue list card, bottom of frame", status="decision 3 (asked twice before)",
      copy="The Cheat Code / 1. A Goal You Can See / 2. A Plan Built Just For You / 3. A Coach That's Always There",
      src="side-list template. Captions move up above the card while it is on screen."),
 dict(id="C1", name="The button", kind="Soft Blue CTA button", status="shown in round 1; now moving",
      copy="Tap The Button Below / Get Started", src="cta template"),
]
DECISIONS = [
 dict(short="Opener (approve / redo)", q="The 8-bit power-up opener, now moving (top of the page and the first 3.6 seconds of the player).",
      opts="A (recommended): approve as it is. B: changes (say what). C: try one video model take from your two frames instead of my code version, about $1 of this ad's $10."),
 dict(short="Analysis card (approve / changes)", q="The new Soft Blue analysis card (A1), which becomes the standard card for every video.",
      opts="A (recommended): approve it as the standard. B: changes (say what: layout, timing, colours, the bars, the band)."),
 dict(short="Recap list (keep / none)", q="The recap list card (R1) on \"That's the cheat code. A goal you can see, a plan built just for you, and a coach that's always there.\" I have asked this in rounds 1 and 2 without an answer; it is the one item I cannot lock without you.",
      opts="A (recommended): keep it, each line landing as you say it, captions lifted above it. B: no card, you on camera with captions only."),
]
DECIDED = json.load(open("round3/decided.json"))


def btn(i):
    c = CU["items"][i]
    return f'<button class="ctx" data-src="{quote(c["clip"].replace("round3/", ""))}" data-poster="{quote(c["clip"].replace("round3/", "").replace(".mp4", ".jpg"))}">Play it moving, in context</button>'


cards = []
for it in ITEMS:
    c = CU["items"][it["id"]]
    a, b = c["a"], c["b"]
    sp = (f'<details><summary>Speech before / during / after</summary><p><b>Before:</b> {E(speech(a - 3, a))}</p>'
          f'<p><b>During:</b> {E(speech(a, b))}</p><p><b>After:</b> {E(speech(b, b + 3))}</p></details>')
    chk = CK.get(it["id"])
    chk = f'<p class="meta">Checked: {E(chk)}</p>' if chk else ""
    cards.append(f"""<section class="card"><h3>{it['id']} · {E(it['name'])}</h3>
<a href="{quote(c['still'].replace('round3/', ''))}" target="_blank"><img loading="lazy" src="{quote(c['still'].replace('round3/', ''))}" alt="{E(it['name'])}"></a>
{btn(it['id'])}
<table><tr><th>On screen</th><td>{a:.2f} to {b:.2f} s</td></tr><tr><th>What it is</th><td>{E(it['kind'])}</td></tr>
<tr><th>Status</th><td>{E(it['status'])}</td></tr><tr><th>Copy</th><td>{E(it['copy'])}</td></tr><tr><th>Source</th><td>{E(it['src'])}</td></tr></table>
{chk}{sp}</section>""")

LINE = "Guys have figured out the cheat code for getting six pack abs."
o2 = CU["items"]["O2"]
first = CU["first30"]
dec = "".join(f"<li><b>{E(d['q'])}</b><br>{E(d['opts'])}</li>" for d in DECISIONS)
decided = "".join(f"<li>{E(x)}</li>" for x in DECIDED)
reply = "\n".join(f"{i+1}. {d['short']}: " for i, d in enumerate(DECISIONS)) + "\nAnything else to change: "
F30 = os.path.basename(first["file"])
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cheat Code Six Pack AD R3</title><style>
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
</style></head><body><main>
<h1>The Cheat Code For Six Pack Abs · ad · round 3</h1>
<p class="sub">RA-14, vertical 9:16 first. Locked from round 2: the 8-bit power-up opener (frames), the wider framing, the brighter golden-skin colour, the bass-lift voice, the Soft Blue analysis card as the standard. This round: the opener moving, the new analysis card, every graphic and clip moving in context, and the finished first {first['dur']:.1f} seconds. The ad runs {PL['total']:.1f} seconds; no line is cut. Spend on AI generation: $0 of $10.</p>
<h2>Your decisions ({len(DECISIONS)})</h2><ol>{dec}</ol>
<h2>The finished first {first['dur']:.1f} seconds</h2>
<div class="player"><video id="v" controls preload="none" poster="stills/first30.jpg" src="{quote(F30.replace('.mp4', ' - REVIEW 540p.mp4'))}"></video>
<div class="btns"><button class="on" data-src="{quote(F30.replace('.mp4', ' - REVIEW 540p.mp4'))}" data-poster="stills/first30.jpg">First {first['dur']:.0f} seconds (540p)</button>
<button data-src="{quote(F30)}" data-poster="stills/first30.jpg">First {first['dur']:.0f} seconds, full 1080x1920</button>
<button data-src="{quote(o2['clip'].replace('round3/', ''))}" data-poster="stills/O2.jpg">The opener in context</button></div>
<p class="sub" style="font-size:13px">Every "Play it moving, in context" button below loads into this one player.</p></div>
<p>From the opener to "Step three": the opener, your approved crop and colour, captions, Step 1 and the demo, Step 2 and the new analysis card, the voice with the bass lift and the music. Nothing in it is a placeholder.</p>
<h2>The opener, moving</h2>
<div class="pair"><figure><a href="opener/O2_sheet.jpg" target="_blank"><img src="opener/O2_sheet.jpg" alt="O2 every 6th frame"></a><figcaption>Every 6th frame</figcaption></figure></div>
<table><tr><th>When it appears</th><td>0:00.0 to 0:03.6, the first thing on screen</td></tr>
<tr><th>The line it plays under</th><td><b>"{E(LINE)}"</b></td></tr>
<tr><th>What comes right after</th><td>A hard cut to you, close, saying "It's AI."</td></tr>
<tr><th>What you see</th><td>Your approved start frame. He runs right at an even speed, hops and punches the six-pack power-up (it bumps), the screen flashes white for 3 frames as you say "cheat code", he flickers small and big like a game power-up, then flexes with pixel abs while the counter climbs to ABS x6 on "abs".</td></tr>
<tr><th>How it was made</th><td>In code, $0. Frame 0 is your approved start frame; the flexing man is lifted from your approved end frame; one Codex sprite sheet gave the second run pose and the hop. The counter is drawn by me.</td></tr>
<tr><th>Checked</th><td>{E(CK.get('O2_review', ''))}</td></tr></table>
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>Every graphic and clip, in order, moving in context</h2>
<p class="sub">Each still is the settled moment on its real frame, with its caption. The button plays it with about 3 seconds of speech either side.</p>
<div class="grid">{''.join(cards)}</div>
<h2>The analysis card in the other two shapes (a record)</h2>
<div class="pair"><figure><a href="stills/A1-16x9.jpg" target="_blank"><img src="stills/A1-16x9.jpg" alt="A1 16:9"></a><figcaption>16:9 (the horizontal version of this ad uses this)</figcaption></figure>
<figure style="flex:.6"><a href="stills/A1-1x1.jpg" target="_blank"><img src="stills/A1-1x1.jpg" alt="A1 1:1"></a><figcaption>1:1 square</figcaption></figure></div>
<p class="sub">Round 2 page: <a href="http://127.0.0.1:8815/" target="_blank">http://127.0.0.1:8815/</a></p>
<h2>Your reply</h2>
<textarea id="r">{E(reply)}</textarea><br><button class="copy" onclick="navigator.clipboard.writeText(document.getElementById('r').value);this.textContent='Copied'">Copy reply</button>
</main><script>
const v=document.getElementById('v');
function play(b){{v.poster=b.dataset.poster;v.src=b.dataset.src;v.play();document.querySelectorAll('.btns button,.ctx').forEach(x=>x.classList.toggle('on',x===b));
if(b.classList.contains('ctx')&&window.innerWidth<1500)v.scrollIntoView({{behavior:'smooth',block:'center'}})}}
document.querySelectorAll('.btns button,.ctx').forEach(b=>b.onclick=()=>play(b));
</script></body></html>"""
assert chr(8212) not in page and chr(8211) not in page, "dash on the page"
open("round3/index.html", "w").write(page)
json.dump({"decisions": DECISIONS, "decided": DECIDED, "items": ITEMS}, open("round3/notes_r3.json", "w"), indent=1)
print("round3/index.html", len(page), "bytes")
