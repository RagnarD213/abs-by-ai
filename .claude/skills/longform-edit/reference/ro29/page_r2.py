"""RO-29 round 2 review page: the full film, every change with its time and a jump button, what I decided, checks, reply."""
import html
O = "/Volumes/Expansion/_edit_work/RO-29/round2/review"; V = "RO-29 round 2 - full film - REVIEW 540p.mp4"
def mm(t): return f"{int(t//60)}:{t%60:04.1f}"
ch = [
 (0.0, 0.0, "0:00 The clickbait TikTok (new)", "Close on his fat hand holding the phone with a ridiculous CORTISOL BELLY COCKTAIL video. He sets the phone down against the carafe."),
 (3.1, 1.5, "0:03 The cocktail bartender (changed)", "The same phone stays on the island. He shakes, plants the shaker and ends on a triumphant, stupid toast."),
 (43.8, 41.5, "0:44 Fasting and grinding at the desk (new)", "AI you at the computer, wrecked, nothing but coffee, the clock spinning, day into night, cups piling up. It replaces the stock office worker on the calorie deficit line."),
 (109.6, 106.5, "1:50 The supplement receipt is out", "You stay on camera there. See What I decided: you wrote A4 with the words \"quitting the stressful job\", but A4 on the page was the supplement receipt, and you kept and changed the quitting clip."),
 (213.7, 211.0, "3:34 Quitting the stressful job (changed)", "He clearly mouths \"I quit\" right on your word \"quit\", then walks out with the box. It runs 1.2 seconds into your next line so the walk-out shows."),
 (221.2, 219.0, "3:41 The husband who can't (changed)", "He is ripped in a white tank top and she is clearly overweight, a big mismatch. His mouth stays mostly shut for now: lip sync is your call in question 1."),
 (270.2, 268.0, "4:30 Weighing the chicken after a fight (changed)", "He is in a tank top now, so you can tell he is ripped. She yells, turns and storms off while he weighs his food."),
 (12.1, 10.5, "0:12 and on: B-roll colour", "Every stock and library clip now has a real colour correction, each matched by measurement and then compared by eye. Before this only your pool clips had one. Jump here for the first one; the others are at 0:54, 1:30, 2:02, 2:17, 2:20, 2:50, 2:53, 3:14 and 4:34."),
]
rows = "".join(f"<li><button onclick='go({w})'>{mm(w)}</button> <b>{html.escape(t)}</b><br>{html.escape(d)}</li>" for _, w, t, d in ch)
dec = ["<b>A4 means the supplement receipt.</b> You kept \"Quitting the stressful job\" as A5 and asked for \"I quit\" on it, so I cut the supplement receipt, which was labelled A4 on the page. If you meant to cut the quitting clip, say so and I swap it back.",
       "<b>Your voice pick is in: warm bass plus.</b> Colour A too.",
       "<b>The two TikToks stay muted beside you.</b> You did not pick on that one, so I kept my recommendation.",
       "<b>The clock in the desk clip spins fast, played 1.2 times real speed.</b> It is a time-lapse on purpose, with one jump inside it where the cups would otherwise form out of thin air.",
       "<b>The meditation clip ends mid-lift.</b> In the last second of the take the slice changed hands, so I cut before that. The husband clip is cut short for the same kind of reason: his mouth opens near the end.",
       "<b>The bedroom clip got a lift.</b> It was much darker than you on camera, so his face reads now."]
chk = ["Independent reviewer on the first version of this film: did not ship it. All ten of its findings are fixed or listed below, and I checked each fix on the new film myself. That reviewer did not re-watch the new film.",
       "Audio: loudness -14.2, true peak -2.0, no clicks measured at any of the 14 joins, script fidelity 98%.",
       "The audio check's tone row is red because of the bass lift you picked. It always fails on that fixed lift. Every other audio row passes.",
       "<b>Nobody has listened to this yet.</b> Measurements are not a listening pass, and the outside listening tool gave unreliable answers. Two spots to listen for: 4:51 (the pause before \"So let's review\") and 3:39 to 3:57, where the room tone sits a bit higher than around it.",
       "A fresh judge went through every frame strip and sheet of this exact film (200 images, 94 joins): no defects.",
       "Hair room: closest 36 px, nothing cut off. No unflattering body shots in the scan.",
       "Delivery check rows still red, all explained: voice tone (above), B-roll share 38% against a 40% minimum (your new AI clips cover more of the film), and three false alarms that were checked by hand: a card change inside one continuous shot, and two caption rows that read graphics as captions. Captions are a separate file, not burned in."]
page = f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Cortisol Belly, round 2</title><style>
:root{{--bg:#0e1622;--card:#16212f;--tx:#e8eef6;--mu:#9fb0c3;--ac:#5fb4ff}}
body{{margin:0;background:var(--bg);color:var(--tx);font:16px/1.5 -apple-system,Segoe UI,sans-serif}}main{{max-width:980px;margin:0 auto;padding:16px}}
section{{background:var(--card);border-radius:12px;padding:16px 18px;margin:14px 0}}h1{{font-size:24px;margin:8px 0}}h2{{font-size:19px;margin:4px 0 10px}}
video{{width:100%;border-radius:8px;background:#000}}button{{background:var(--ac);color:#04121f;border:0;border-radius:6px;padding:3px 9px;font-weight:600;cursor:pointer}}
li{{margin:8px 0}}.t{{color:var(--mu)}}textarea{{width:100%;min-height:150px;background:#0b121c;color:var(--tx);border:1px solid #2a3a4f;border-radius:8px;padding:8px;font:15px/1.4 inherit;box-sizing:border-box}}
</style></head><body><main>
<h1>Cortisol Belly Is Real, But TikTok Has It Wrong (RO-29), round 2</h1>
<p>The full film with your notes in. You do not need to watch it all: the buttons below jump a few seconds before each change.</p>
<section><h2>The full film (5:29)</h2><video id=v controls preload=metadata src="{html.escape(V)}"></video>
<p class=t>Full quality for VLC: Videos to Review / Cortisol Belly LFC R2 - full film.mp4</p></section>
<section><h2>What changed ({len(ch)})</h2><ol>{rows}</ol></section>
<section><h2>Question for you (1)</h2><ol><li><b>Lip sync on the husband, about $0.50?</b> Without it his mouth stays mostly shut under your whiny voice, with small flashes where it opens. With it his lips match your line, the way you liked it on the Invest In Your Health videos. I recommend yes. Write "lip sync OK" below.</li></ol></section>
<section><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>'+x+'</li>' for x in dec)}</ul></section>
<section><h2>Checks</h2><ul>{''.join('<li>'+x+'</li>' for x in chk)}</ul></section>
<section><h2>One reply</h2><textarea id=r>1. Lip sync OK? 
2. Approve as final, or list changes (time + what):

</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section>
</main><script>function go(t){{const v=document.getElementById('v');v.currentTime=t;v.play()}}</script></body></html>"""
open(f"{O}/index.html", "w").write(page); print("page ok", len(ch))
