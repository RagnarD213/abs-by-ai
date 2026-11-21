#!/usr/bin/env python3
"""RA-04 round 3 review page -> round3/index.html: the broken-arm AI clip in MOTION, in context (only what changed since round 2c).
The independent review's verdict and notes come from round3/review/page_review.json (written after the review)."""
import html, json, os
R = "/Volumes/Extreme/_edit_work/ra04/round3"; E = html.escape
RV = json.load(open(f"{R}/review/page_review.json")) if os.path.exists(f"{R}/review/page_review.json") else {"verdict": "pending", "notes": []}
L = json.load(open(f"{R}/motion/ledger.json")); spent = round(sum(x["usd"] for x in L), 2)
SHOTS = [
 ("Shots 1 and 2: walks up to the rack, then takes out his phone (one unbroken take)", "0:39.1 to 0:42.5",
  "\"when life gets in the way. When you get injured, use Abs By AI to\"", ["ai1_0", "ai1_30", "ai1_45", "ai1_58", "ai1_72", "ai1_100"],
  "He walks up to the loaded squat rack and stops. At the barbell he puffs out a breath, a \"no way\" look, then frowns on \"get injured\". His hand goes to his pocket, the phone comes out on \"use Abs By AI\", and he reads it."),
 ("Shot 3: does leg presses instead", "0:42.5 to 0:43.4", "\"adjust your plan.\"", ["ai1_101", "ai1_128"],
  "Cut to the leg press: phone on his chest, smiling, he pushes the sled from the bottom of the rep to almost straight."),
]
PHYS = [
 "The sled moves as one piece along the rails: plates, horn and platform rim travel 105 px at 48 degrees (the rails are 45) and agree within 3 px of each other. The machine frame, seat, uprights and floor measure 0 px of movement.",
 "Both feet stay on the platform: the near shoe moves with the sled within 7 px (the limit is 12).",
 "He pushes along his body line: hip-to-feet line 5 degrees from the rails at the bottom of the rep and 6 at the top. His knee opens from 102 to 167 degrees as the sled rises.",
 "His legs keep their length: torso 269 / 263 px, thigh 201 / 200, shin 199 / 204 (all within 3 %). The reach at the top is what those bones allow (within 1 %).",
 "One phone, held flat on his chest in his right hand the whole shot. The cast stays on his left forearm in the sling in every shot.",
 "Shots 1 and 2: the rack, barbell, benches, pillar and lights hold still; the only changes away from him are gym members moving in the background. No hidden cuts or fades inside either take.",
]
DECIDED = [
 f"<b>Takes:</b> 12 generated on Veo 3.1 Fast from your approved frames. <b>${spent:.2f} of the $20 budget spent.</b>",
 "<b>The first independent review FAILED my first build, and it was right.</b> I had joined two separate takes at your middle frame (walk, then phone). The walk take did not land exactly on that frame, so at the join he jumped about an inch in one frame and an earring vanished. I rebuilt shots 1 and 2 as ONE take, from your approved first frame (walking in) to your approved last frame (reading the phone), so there is no join at all.",
 "<b>Shots 1 and 2:</b> of three single takes, I chose the 6-second one: it gets from the walk to the phone fast enough for the words. The other two spent 2 seconds fumbling in his pocket.",
 "<b>His reaction at the barbell:</b> he puffs his cheeks out for about half a second, a \"phew, no way\" breath, then frowns. None of the takes did a clean head shake. If the puff reads wrong to you, say so and I'll regenerate that moment.",
 "<b>Shot 3:</b> Veo made him do two reps in 4 seconds; I use one push, bottom to top. I chose the take where the phone stays still on his chest: in the other take the phone smeared as he turned it.",
 "<b>Speed:</b> 1.25x on all three shots, so every frame shown is a real generated frame. My first build ran 1.12x, which repeated 13 frames and made the sled stutter three times.",
 "<b>Placement:</b> slot A (your default), 0:39.1 to 0:43.4. The tip 3 lower third now fades out just before the clip, so \"Let AI Fix What Gets In Your Way\" is up for 1.9 seconds after the headline lands. The AI-GENERATED label sits top left, clear of him in every shot. Captions run at the usual height: over his shins at the rack and over the floor at the leg press, never his face, the phone or the machine.",
 "<b>One preview limit:</b> this preview is built over the round 2 film. The 2 seconds of you before the clip keep their round 2 crop, which the final render shifts by about 5 px. Everything else is what the final will show.",
]
rev_html = (f"<p><b>Independent review: {E(RV['verdict'])}</b></p><ul>" + "".join(f"<li>{n}</li>" for n in RV["notes"]) + "</ul>")
shots_html = "".join(f"""<div class="card"><h3>{E(t)}</h3><div class="imgs">{''.join(f'<figure><img src="stills/{s}.jpg" loading="lazy"></figure>' for s in st)}</div>
<table><tr><th>When</th><td>{w}</td></tr><tr><th>Plays under</th><td><b>{E(words)}</b></td></tr><tr><th>The action</th><td>{E(act)}</td></tr></table></div>""" for t, w, words, st, act in SHOTS)
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RA-04 Round 3</title><style>
:root{{--bg:#eef4fb;--card:#fff;--ink:#14243a;--mute:#5a6b80;--line:#c9d8ea;--acc:#1f6fd1}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:900px;margin:0 auto;padding:20px 16px 80px}} @media(min-width:1300px){{main{{margin-left:max(16px,calc(50% - 620px))}}}}
h1{{font-size:24px;margin:0 0 4px}} h2{{font-size:19px;margin:28px 0 10px}} h3{{font-size:16px;margin:0 0 10px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}}
.lock{{color:var(--mute)}} .imgs{{display:flex;gap:10px}} figure{{margin:0;flex:1}} figure img{{width:100%;border-radius:8px;display:block}}
figcaption{{font-size:12px;color:var(--mute);text-align:center}} .small figure{{flex:0 0 22%}}
table{{border-collapse:collapse;margin-top:10px;width:100%}} th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:4px 10px 4px 0;width:120px}} td{{padding:4px 0}}
ul li{{margin:6px 0}} #dock{{background:#0c1a2c;border-radius:12px;padding:10px;margin:12px 0}}
#dock video{{width:100%;max-height:70vh;display:block;border-radius:8px;background:#000}} #dock .t{{color:#cfe0f5;font-size:13px;margin:6px 2px 0}}
@media(min-width:1300px){{#dock{{position:fixed;right:24px;top:20px;width:380px;margin:0}}}}
button{{background:var(--acc);color:#fff;border:0;border-radius:8px;padding:7px 12px;font-size:14px;cursor:pointer;margin:4px 6px 4px 0}}
button.alt{{background:#5a6b80}}
textarea{{width:100%;box-sizing:border-box;min-height:90px;font:14px/1.4 ui-monospace,Menlo,monospace;border:1px solid var(--line);border-radius:8px;padding:10px}}
</style></head><body>
<div id="dock"><video id="pv" controls preload="metadata" playsinline src="context_review.mp4" poster="stills/ai1_72.jpg"></video><div class="t" id="pt">Tip 3 in context, 0:35.5 to 0:45.5</div>
<div><button class="alt" onclick="rate(1)">1x</button><button class="alt" onclick="rate(0.5)">0.5x</button><button class="alt" onclick="rate(0.25)">0.25x</button></div></div>
<main>
<h1>Top 3 Tips For Getting Abs: round 3</h1>
<p>AD, RA-04. Only one thing changed since round 2c: the broken-arm clip now MOVES, built from the five frames you approved, in slot A of tip 3.</p>
<p class="lock"><b>Already locked:</b> first 30 seconds, Soft Blue analysis card, voice B with the extra bass, the result card fix, all five broken-arm frames.</p>
<div class="card"><h2 style="margin-top:0">Your decision (1)</h2><ol><li><b>The broken-arm clip in motion, in context</b>: Approve / Change (say which shot and what). Approving it unlocks the full film (9:16 and 16:9).</li></ol>
<button onclick="play('context_review.mp4','Tip 3 in context, 0:35.5 to 0:45.5')">Play it in context (0:35.5 to 0:45.5)</button>
<button onclick="play('AI1 clip alone - REVIEW 540p.mp4','The clip alone, no captions')">Play the clip alone</button></div>

<h2>The shots</h2>{shots_html}

<h2>Physics checks on the leg press (measured on every frame used)</h2>
<div class="card"><ul>{''.join(f'<li>{E(p)}</li>' for p in PHYS)}</ul>
<p class="lock">Body measurement at the bottom and top of the push (yellow: shoulder, hip, knee, ankle; blue: the rail line):</p>
<div class="imgs small"><figure><img src="stills/pose_AI1-3_b_060.jpg" loading="lazy"><figcaption>bottom</figcaption></figure><figure><img src="stills/pose_AI1-3_b_087.jpg" loading="lazy"><figcaption>top</figcaption></figure></div>
{rev_html}</div>

<h2>What I decided (overrule anything)</h2>
<div class="card"><ul>{''.join(f'<li>{d}</li>' for d in DECIDED)}</ul></div>

<h2>Your reply</h2>
<div class="card"><textarea id="rb">RA-04 round 3
1. Broken-arm clip in motion: </textarea><button onclick="navigator.clipboard.writeText(document.getElementById('rb').value);this.textContent='Copied'">Copy</button></div>
</main>
<script>function play(src,t){{const v=document.getElementById('pv');v.src=encodeURI(src);document.getElementById('pt').textContent=t;v.play();}}
function rate(r){{document.getElementById('pv').playbackRate=r;}}</script>
</body></html>"""
assert "—" not in page and "–" not in page
open(f"{R}/index.html", "w").write(page); print("PAGE_OK")
