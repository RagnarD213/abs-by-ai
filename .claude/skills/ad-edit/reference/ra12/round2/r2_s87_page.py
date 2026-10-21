#!/usr/bin/env python3
"""RA-14 round 3 review page (PRE-RENDER-APPROVAL "The review page"): header + decisions, the finished first 30 seconds in the one
docked player, the O2 opener moving, "What I decided", then every graphic and clip in timeline order three per row, each with
"Play it moving, in context". One reply box. Writes round2/index.html.
Serve: python3 .claude/skills/_shared/review_server.py 8816 /Volumes/Expansion/_edit_work/ra12/round3
"""
import html, json, os
from urllib.parse import quote
E = html.escape
PL = json.load(open("beats_r2.json")); CU = json.load(open("round2/cuts.json")); CK = json.load(open("round2/checks.json"))
W = json.load(open("words_aligned.json"))["words"]
FPS = 30000 / 1001


def speech(a, b):
    return " ".join(w["w"] for w in W if a <= w["t"] < b)


def mmss(t): return f"0:{t:05.2f}"

ITEMS = [
 dict(id="W1", name="Not a workout", kind="your own ab wheel B-roll (library B0427), full-height card", status="CHANGED (was an AI man doing crunches)",
      copy="No label: real moving footage of you.", src="B0427, your kneeling ab wheel rollout by the pool in low golden sun, from 2.50 s (already rolling out). Picked over B0030 and B0436 because the side light shows the most definition. Graded brighter and a little less yellow to sit with the talking shots. Full height; sides trimmed because the rollout spans most of the frame width."),
 dict(id="D1", name="Not a diet", kind="you holding your salad (salad shoot roll C1546), full screen", status="CHANGED (was an AI man pushing away pizza)",
      copy="No label: real moving footage of you.", src="C1546 at 73.80 s: you hold a container of your daily salad up beside your face in the kitchen. Full screen; graded warmer and brighter to sit with the pool footage."),
 dict(id="G1", name="It's a picture", kind="the prospect's AI goal picture, Soft Blue photo scene", status="CHANGED (was your pool picture)",
      copy="Chip: AI-GENERATED under the photo.", src="The lake-dock man's real absbyai.com result from RA-04 round 5, the same picture the phone generates at 0:17."),
 dict(id="K1", name="Look at it every day", kind="library clip A0180: the prospect's goal picture on a phone lock screen", status="CHANGED (was your picture as a wallpaper)",
      copy="Chip: AI-GENERATED under the phone.", src="A0180 (made for RA-04 round 5, passed the motion check and review there), 0.50 s on."),
 dict(id="P1", name="Generating the picture", kind="phone demo: the prospect's real generation", status="CHANGED (was your sunglasses-to-pool demo)",
      copy="The Generate button, the tap and the scan over his before photo (AI-GENERATED under the phone, because his before photo is AI-made), then his goal picture, AI-GENERATED, from \"with ripped six-pack abs\".",
      src="B0550, one real generation on absbyai.com (RA-04 round 5), normal speed, in the approved iPhone shell. Same man before and after."),
 dict(id="C1", name="First button", kind="Soft Blue CTA button", status="MOVED under the captions",
      copy="Tap The Button Below / Generate Yours (unchanged)", src="cta template, now 24 px under the caption line, over your shorts. Wide shot."),
 dict(id="A1", name="The analysis card", kind="the shared Soft Blue analysis card", status="CHANGED picture only",
      copy="Same bars and plan band, on the prospect's goal picture instead of yours.", src="_shared/hyperframes/analysis-card"),
 dict(id="L1", name="Key point", kind="Soft Blue lower third", status="MOVED under the captions; ends 1 s earlier",
      copy="KEY POINT / See Your Goal Before You Start (unchanged)", src="lower-third template, now 24 px under the captions on the wide shot. It ends where the close shot starts on \"So take the first step\", because on the close shot that spot is your abs."),
 dict(id="C2", name="Closing button", kind="Soft Blue CTA button", status="MOVED under the captions",
      copy="Tap The Button Below / See Yourself With Abs (unchanged)", src="cta template, now 24 px under the caption line; that last shot is now the wide one so the button sits on your shorts."),
]
IDEAS = []
DECISIONS = [
 dict(short="Captions over the prospect's photos (keep / move)", q="On the two full prospect pictures (0:04.1 to 0:05.2 and 0:17.9 to 0:21.7) the caption line runs over the bottom of the picture, across his shorts, as it did over your pictures in round 1. The automatic checker flags any caption on a picture, and only your OK clears it.",
      opts="A (recommended): keep, as in round 1; it never covers his face or abs. B: shrink those pictures so the captions sit under them (the pictures get smaller)."),
 dict(short="Round 2 (approve / changes)", q="The whole 9:16 ad with your round 1 notes done. The changes and where to look are listed above the player.",
      opts="A (recommended): approve it, then I build the 16:9 from the same edit and run the full delivery. B: changes (name them by time)."),
]
DECIDED = json.load(open("round2/decided.json"))


def btn(i):
    c = CU["items"][i]
    return f'<button class="ctx" data-src="{quote(c["clip"].replace("round2/", ""))}" data-poster="{quote(c["clip"].replace("round2/", "").replace(".mp4", ".jpg"))}">Play it moving, in context</button>'


cards = []
for it in ITEMS:
    c = CU["items"][it["id"]]
    a, b = c["a"], c["b"]
    sp = (f'<details><summary>Speech before / during / after</summary><p><b>Before:</b> {E(speech(a - 3, a))}</p>'
          f'<p><b>During:</b> {E(speech(a, b))}</p><p><b>After:</b> {E(speech(b, b + 3))}</p></details>')
    chk = CK.get(it["id"])
    chk = f'<p class="meta">Checked: {E(chk)}</p>' if chk else ""
    cards.append(f"""<section class="card"><h3>{it['id']} · {E(it['name'])}</h3>
<a href="{quote(c['still'].replace('round2/', ''))}" target="_blank"><img loading="lazy" src="{quote(c['still'].replace('round2/', ''))}" alt="{E(it['name'])}"></a>
{btn(it['id'])}
<table><tr><th>On screen</th><td>{a:.2f} to {b:.2f} s</td></tr><tr><th>What it is</th><td>{E(it['kind'])}</td></tr>
<tr><th>Status</th><td>{E(it['status'])}</td></tr><tr><th>Copy</th><td>{E(it['copy'])}</td></tr><tr><th>Source</th><td>{E(it['src'])}</td></tr></table>
{chk}{sp}</section>""")

whole = CU["whole"]
STATUS = json.load(open("round2/status.json")) if os.path.exists("round2/status.json") else {}
TOT = PL["total"]
CHG = [("0:02.3 to 0:04.1", "0:00 to 0:07", "The two opening clips are now you: your ab wheel rollout (W1) on \"isn't a workout\" and you holding your salad (D1) on \"and it's not a diet\"."),
       ("0:04.1 to 0:05.2", "0:02 to 0:08", "The goal picture on \"It's a picture\" is now the AI prospect's (G1), not yours."),
       ("0:11.5 to 0:12.9", "0:09 to 0:15", "The lock screen on \"look at it every day\" shows the prospect's goal picture (K1)."),
       ("0:16.8 to 0:21.7", "0:15 to 0:23", "The generation demo is the prospect's real absbyai.com generation, then his goal picture (P1)."),
       ("0:22.9 to 0:24.9", "0:21 to 0:26", "First button moved down: just under the captions, on your shorts (C1)."),
       ("0:26.8 to 0:33.7", "0:25 to 0:35", "The analysis card scans the prospect's goal picture (A1)."),
       ("0:39.3 to 0:41.7", "0:37 to 0:43", "KEY POINT moved under the captions on the wide shot and now ends at \"So take the first step\" (L1)."),
       (f"0:42.8 to {mmss(TOT)}", f"0:41 to {mmss(TOT)}", "Closing button moved under the captions; that last shot is now the wide one so the button sits on your shorts (C2).")]
changes = "".join(f"<li><b>{E(a)}</b> (watch {E(w)}): {E(t)}</li>" for a, w, t in CHG)
dec = "".join(f"<li><b>{E(d['q'])}</b><br>{E(d['opts'])}</li>" for d in DECISIONS)
decided = "".join(f"<li>{E(x)}</li>" for x in DECIDED)
ideas = "".join(f"<li><b>{E(n)}</b>: {E(t)}</li>" for n, t in IDEAS)
reply = "\n".join(f"{i+1}. {d['short']}: " for i, d in enumerate(DECISIONS)) + "\nAnything else to change: "
WH = os.path.basename(whole["file"]); WR = WH.replace('.mp4', ' - REVIEW 540p.mp4')
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>First Step Abs AD R2</title><style>
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
<h1>The First Step To Getting Abs Isn't A Workout · ad · round 2</h1>
<p class="sub">RA-12, vertical 9:16. Your round 1 notes are done; everything else (the cut, your voice, the colour, framing, captions, the app tour T1 and the worn-out-beginner clip Q1) is exactly as round 1. Runs {PL['total']:.1f} seconds. Spend: $0 of AI generation (no new clips were made).</p>
<p class="sub"><b>Checks on the exact file:</b> {E(STATUS.get('checks', 'pending'))}</p>
<h2>What changed, and where to look</h2><ol>{changes}</ol>
<h2>Your decisions ({len(DECISIONS)})</h2><ol>{dec}</ol>
<h2>The whole ad, finished</h2>
<div class="player"><video id="v" controls preload="none" poster="stills/whole.jpg" src="{quote(WR)}"></video>
<div class="btns"><button class="on" data-src="{quote(WR)}" data-poster="stills/whole.jpg">Whole ad (540p)</button>
<button data-src="{quote(WH)}" data-poster="stills/whole.jpg">Whole ad, full 1080x1920</button></div>
<p class="sub" style="font-size:13px">Every "Play it moving, in context" button below loads into this one player. The full file is also in Videos to Review for VLC.</p></div>
<h2>What I decided (overrule anything)</h2><ul>{decided}</ul>
<h2>The changed items, in order, moving in context</h2>
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
open("round2/index.html", "w").write(page)
json.dump({"decisions": DECISIONS, "decided": DECIDED, "items": ITEMS}, open("round2/notes_r2.json", "w"), indent=1)
print("round2/index.html", len(page), "bytes")
