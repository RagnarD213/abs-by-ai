"""RO-11 round 4 review page (later-round form: only what changed). The seven section cards with their pictures in layout B and
the ending, each from the delivered master, plus what I decided and one reply box. Media: round4/page/{stills,context}.
usage: page4.py   (after the master is gated and round4/page media is cut from it)"""
import json, html, os
W = "/Volumes/Extreme/_edit_work/ro11/round4"
R = [it for it in json.load(open("/Volumes/Extreme/_edit_work/ro11/plan_resolved.json")) if it["kind"] == "title"]
T = json.load(open("/Volumes/Extreme/_edit_work/ro11/round3/stills.json"))
by = {r["id"]: r for r in T}
E = html.escape
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def play(cid, name): return f"<button onclick=\"play('context/{cid}-context - REVIEW 540p.mp4','{E(name)}')\">Play it moving, in context</button>"
WORDS = ("All right, these are all looking good. All the pictures are approved, and let's use layout B. And let's add that extra "
         "0.7 seconds at the end, as you recommend.")
decided = [
    "<b>The seven cards are exactly what you approved:</b> your seven pictures, their crops and their labels, in layout B (the picture runs to the top, right and bottom edges and fades into the blue). The words, their size and their timing did not change.",
    "<b>Labels:</b> \"Real picture of me. Not AI-generated.\" on Sleep and Exercise, \"AI-GENERATED\" on Alcohol, none on the four stock pictures. On every card the label is clear of your face and abs.",
    "<b>The ending:</b> 0.7 seconds of your smile added after \"...videos like this one.\" You keep smiling, no blink, no reset. The added sound is room only, no breath or click. The film is now 9:58.9.",
    "<b>Motion check before the full film:</b> I rendered each of the six cards you had only seen as stills (Alcohol to Daily Movement) moving. The picture and label fade in together in about a quarter of a second and the left edge fades cleanly into the blue.",
    "<b>The tightest card is Alcohol.</b> At the end of the slow push the AI image's hair is about 13 pixels from the top edge. It is not cut. I left your approved crop alone.",
    "<b>Everything else is the film you already watched.</b> I compared this film to round 2 frame by frame: outside the seven cards and the ending, every frame and all the sound are the same.",
    "<b>Spend this round: $0.</b> Video total is still about $3.50 of the $5.",
]
def card(r):
    b = by[r["id"]]
    return f"""<article id="{r['id']}"><h3>{r['id']} <span class="tag">Factor {r['step']} of 7: {E(r['headline'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(r['t1'])}</span></h3>
<a href="stills/{r['id']}.jpg"><img loading="lazy" src="stills/{r['id']}.jpg"></a>{play(r['id'], r['id'] + ' ' + r['headline'])}
<div class="copy"><b>Picture</b>: {E(b['what'])}<br><b>Label</b>: {E(b['label']) if b['label'] else 'none (stock)'}</div></article>"""
end = """<article id="END"><h3>The ending <span class="tag">last 14 seconds</span> <span class="small">9:44.9 to 9:58.9</span></h3>
<video controls preload="none" playsinline poster="stills/T7.jpg" src="context/END-context - REVIEW 540p.mp4"></video>
<div class="copy">Your last word ends at 9:58.1; the film now holds your smile to 9:58.9, which is 0.7 s longer than the film you watched.</div></article>"""
reply = "1. Cards: approved / notes by card:\n2. Ending: approved / notes:\nOther notes:"
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-11 round 4</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}h3{{margin:0 0 8px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:130px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b;margin-bottom:16px}}
@media(min-width:1500px){{body{{padding-right:min(30vw,520px)}}#dock{{position:fixed;top:16px;right:16px;width:calc(min(30vw,520px) - 40px);box-sizing:border-box;margin:0;box-shadow:0 8px 40px #000a}}}}
@media(max-width:1499px){{#dock video{{max-height:42vh}}}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<main><h1>RO-11 / Round 4: the full film, rebuilt</h1><p>"When Calories Don't Matter For Fat Loss". The full film is rebuilt with the seven section cards in layout B and 0.7 seconds more of your smile at the end. Watch it in VLC: <b>Videos to Review/Calories Don't Matter LFC R4 - full film.mp4</b>. This page shows only what changed.</p>
<p class="notice"><b>Your words:</b> "{E(WORDS)}"</p>
<nav><a href="#decided">What I decided</a><a href="#cards">The seven cards</a><a href="#end">The ending</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Press "Play it moving, in context" on any card to play it here, with 3 seconds of you either side.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + d + '</li>' for d in decided)}</ul></section>
<section id="cards"><h2>The seven cards, from the finished film</h2><p class="small">Each still is the card settled, cut from the delivered file. Click a picture to see it full size.</p>
<div class="grid">{''.join(card(r) for r in R)}</div></section>
<section id="end"><h2>The ending</h2><div class="grid">{end}</div></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id+', in context';v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page
open(f"{W}/page/index.html", "w").write(page); print("page ok", len(R), "cards")
