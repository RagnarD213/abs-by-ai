"""RO-11 round 3 review page (PRE-RENDER-APPROVAL "The review page", later-round form: only what changed). Header with the
locks and Dan's words, his decisions, the two layouts on one card, what I decided, the seven cards three per row with
source and label, one floating player for "Play it moving, in context", the other layout collapsed, checks, one reply box.
usage: page3.py   (after round3.py stills/context and titles.py measure <round3>/checks/chips)"""
import json, html, os
W = "/Volumes/Extreme/_edit_work/ro11/round3"
rows = json.load(open(f"{W}/stills.json"))
chips = json.load(open(f"{W}/checks/chips/chips.json")) if os.path.exists(f"{W}/checks/chips/chips.json") else {}
E = html.escape
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
def play(cid, name): return f"<button onclick=\"play('context/{cid}-context - REVIEW 540p.mp4','{E(name)}')\">Play it moving, in context</button>"
WORDS = ("All right, everything is looking good except the full-screen graphics for each of the points, like sleep and alcohol... "
         "Those look a little empty. What I want you to do is to add an image to the right on each of those full-screen graphics to fill them out.")
decisions = [
    "<b>Layout.</b> <b>A, framed picture</b> (recommended: it is the same rounded frame as your fact cards, the whole picture shows, and the label "
    "sits under it instead of on you), or <b>B, the picture runs to the edge of the screen and fades into the blue</b>. Both are on the Sleep card just below; "
    "all seven are built in A, and all seven in B are folded up further down.",
    "<b>The seven pictures.</b> Approve, or name the card (T1 to T7) and what you want instead.",
    "<b>The ending.</b> <b>Add about 0.7 seconds of your smile after the last word</b> (recommended: you hold it on the roll, and the film now stops the instant you finish), or leave it as is.",
]
decided = [
    "<b>T1 Sleep.</b> Your pool-shoot photo asleep on the lounge chair, cropped in to you and the chair. Real-picture label.",
    "<b>T2 Alcohol.</b> The AI image of you holding a beer that we made for the alcohol thumbnail, the clean version with no type on it. AI-GENERATED label.",
    "<b>T3 Hormones.</b> Nothing of ours fits, so a free Pexels photo: a gloved hand holding two blood sample tubes. It is not the blood-draw clip at 3:01.",
    "<b>T4 Meal Timing.</b> Nothing of ours fits, so a free Pexels photo: a wall clock whose hours are forks and spoons. One glance says food and time.",
    "<b>T5 Protein.</b> A free Pexels photo of salmon, steaks and eggs, which is your line, \"meat, fish or eggs\". I looked at our own kitchen footage first: "
    "the only protein shot is the rotisserie chicken being pulled apart with gloves, and for two and a half seconds on a title card it reads as a carcass, so I passed on it.",
    "<b>T6 Exercise.</b> Your pool-shoot kettlebell photo (photo-29). The smiling one (photo-38) loses the kettlebell below the frame, and without it the pose does not read as exercise.",
    "<b>T7 Daily Movement.</b> A free Pexels photo of a man walking a park path. The stairs picture already in the folder is the same man and staircase as the clip at 8:38, so I did not use it.",
    "<b>Nothing new was generated.</b> Two pictures are yours, one is our existing AI image, four are free stock. Spend this round: $0. Video total is still about $3.50 of $5.",
    "<b>No picture repeats anything in the film.</b> Checked against all 12 clips and the 7 fact-card photos.",
    "<b>The words did not change:</b> same text, same size, same place, same timing. Each card is on screen exactly as long as before.",
    "<b>Motion.</b> The picture rises in with the headline in the first 0.7 seconds, then pushes in very slowly, the same move as the fact-card photos. The label rises and fades in with it.",
    "<b>The bright studio pictures</b> (the tubes, the food, the walker) are brought down about 10% so they do not glare against the dark blue.",
    "<b>The film is not rebuilt.</b> Everything you approved is untouched and re-checked by fingerprint. Round 4 rebuilds the film once you approve these.",
]
def card(r, lay="frame", cid=None, extra=""):
    cid = cid or r["id"]
    lic = E(r["licence"]) + (f", <a href='{r['url']}'>source page</a>" if r.get("url") else "")
    lab = E(r["label"]) if r["label"] else "none needed (stock, not a picture of you)"
    return f"""<article id="{cid}"><h3>{r['id']} <span class="tag">Factor {r['step']} of 7: {E(r['headline'])}</span> <span class="small">{mmss(r['t0'])} to {mmss(r['t1'])}</span></h3>
<a href="stills/{r['id']}_{lay}.jpg"><img loading="lazy" src="stills/{r['id']}_{lay}.jpg"></a>{play(cid, r['id'] + ' ' + r['headline']) if extra != 'noplay' else ''}
<div class="copy"><b>Picture</b>: {E(r['what'])}<br><b>Source</b>: {E(r['src'])} · {lic}<br><b>Label</b>: {lab}<br><a href="stills/{r['id']}_before.jpg">The card as it is in the film now (empty)</a></div>
<details><summary>Your words before / during / after</summary><p class="small"><b>before</b>: {E(r['before'])}<br><b>during</b>: {E(r['during'])}<br><b>after</b>: {E(r['after'])}</p></details></article>"""
t1 = rows[0]
two = f"""<div class="grid two"><article><h3>A, framed picture <span class="tag">recommended</span></h3><a href="stills/T1_frame.jpg"><img loading="lazy" src="stills/T1_frame.jpg"></a>{play('T1', 'Layout A on the Sleep card')}
<div class="copy">The rounded frame from your fact cards, as large as the right side allows. The label sits under the picture.</div></article>
<article><h3>B, runs to the edge</h3><a href="stills/T1_bleed.jpg"><img loading="lazy" src="stills/T1_bleed.jpg"></a>{play('T1B', 'Layout B on the Sleep card')}
<div class="copy">The picture fills the right side to the top, bottom and right edges and fades into the blue. The label has to sit on the picture, placed where you are not.</div></article></div>"""
def clr(k):
    c = chips.get(k); return f"{c['nearest_person_px']:.0f} px" if c else "?"
checks = [
    "<b>Locked files re-checked by fingerprint before starting:</b> the round 2 film, the plan, the graphics list, the cut, the shot list and the opener clip all match what you approved.",
    f"<b>Labels never touch you.</b> Measured on each rendered card with the person outline. Layout A (label under the frame): Sleep {clr('T1_frame')}, Alcohol {clr('T2_frame')}, "
    f"Exercise {clr('T6_frame')} from the nearest part of you. Layout B (label on the picture): Sleep {clr('T1_bleed')}, Alcohol {clr('T2_bleed')}, Exercise {clr('T6_bleed')}.",
    "<b>Cut in and out.</b> Read frame by frame on every moving clip: the card starts on the same frame as before, the picture and headline are settled inside 0.7 seconds, and the cut back to you is unchanged.",
    "<b>Your hair is whole</b> in both of your photos and in the AI image, with room above it, including at the end of the slow push.",
    "<b>A card with no picture still draws exactly as before</b> (compared pixel for pixel against the round 2 code), so nothing else in the film can shift.",
    "<b>Stock rights.</b> The four stock pictures are from Pexels (free to use, no credit needed). Source pages are linked under each card.",
]
reply = "1. Layout: A (framed) / B (runs to the edge)\n2. Pictures: approved / notes by card:\n3. Ending smile: add / leave\nOther notes:"
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RO-11 round 3: section cards</title>
<style>body{{margin:0;background:#071221;color:#edf5ff;font:17px system-ui;line-height:1.55}}main{{max-width:1280px;margin:auto;padding:28px 16px}}h1{{font-size:38px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:26px}}h3{{margin:0 0 8px}}p,li{{color:#bdd0e4}}section{{margin:32px 0;padding:22px;background:#101f32;border:1px solid #29425b;border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}.grid.two{{grid-template-columns:repeat(2,minmax(0,1fr))}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}img,video{{width:100%;border-radius:10px;background:black}}a{{color:#8cd6ff}}.tag{{color:#8ed7ff;font-size:14px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}textarea{{width:100%;box-sizing:border-box;min-height:150px;background:#071221;color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{position:sticky;top:0;z-index:5;background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid #29425b;margin-bottom:16px}}
@media(min-width:1500px){{body{{padding-right:min(30vw,520px)}}#dock{{position:fixed;top:16px;right:16px;width:calc(min(30vw,520px) - 40px);box-sizing:border-box;margin:0;box-shadow:0 8px 40px #000a}}}}
@media(max-width:1499px){{#dock video{{max-height:42vh}}}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}summary{{cursor:pointer}}@media(max-width:800px){{.grid,.grid.two{{grid-template-columns:1fr}}h1{{font-size:30px}}}}</style>
<main><h1>RO-11 / Round 3: the seven section cards</h1><p>"When Calories Don't Matter For Fat Loss". Only the seven full-screen section cards changed: each now has a picture on its right. Nothing else is on this page because nothing else changed.</p>
<p class="notice"><b>Already locked, untouched:</b> the round 2 film you watched (opener, cut, look, audio, every lower third, fact card, side list, the cycle card, the recap and all 12 clips), and on these cards the words, their size and their timing.<br>
<b>Your words:</b> "{E(WORDS)}"</p>
<nav><a href="#decide">Your {len(decisions)} decisions</a><a href="#layout">The two layouts</a><a href="#decided">What I decided</a><a href="#all">The seven cards</a><a href="#b">All seven in layout B</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<div id="dock"><div class="small" id="nowp">Press "Play it moving, in context" on any card to play it here, with 3 seconds of you either side.</div><video id="pv" controls preload="none" playsinline></video></div>
<section id="decide"><h2>Your decisions ({len(decisions)})</h2><ol>{''.join('<li>' + d + '</li>' for d in decisions)}</ol></section>
<section id="layout"><h2>Decision 1: the two layouts, on the Sleep card</h2>{two}</section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + d + '</li>' for d in decided)}</ul></section>
<section id="all"><h2>The seven cards, in order (layout A)</h2><p class="small">Each is the card at its settled frame, at its real time in the film. Click a picture to see it full size.</p>
<div class="grid">{''.join(card(r) for r in rows)}</div></section>
<section id="b"><h2>All seven in layout B</h2><details><summary>Open only if you are leaning toward B</summary><p class="small">Stills only. If you pick B, round 4 builds these into the film.</p>
<div class="grid">{''.join(f'<article><h3>{r["id"]} <span class="tag">{E(r["headline"])}</span></h3><a href="stills/{r["id"]}_bleed.jpg"><img loading="lazy" src="stills/{r["id"]}_bleed.jpg"></a></article>' for r in rows)}</div></details></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + d + '</li>' for d in checks)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id+', in context';v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth',block:'nearest'}});}}</script></html>"""
assert chr(8212) not in page and chr(8211) not in page
open(f"{W}/index.html", "w").write(page); print("page ok", len(rows), "cards")
