#!/usr/bin/env python3
"""RA-04 round 2 review page -> round2/index.html (PRE-RENDER-APPROVAL layout: decisions, player, AI frames, What I decided, reply)."""
import html, json
R = "/Volumes/Extreme/_edit_work/ra04/round2"
E = html.escape
SHOTS = [
 dict(n="Shot 1: walks up to the squat rack, shakes his head", s="S1_a", e="F2_a", t="0:39.1 to 0:41.4 (2.2 s)",
      under="when life gets in the way. When you get injured,",
      act="He walks from the back of the gym to the loaded squat rack, stops in front of it, looks at the barbell and shakes his head: not with this arm.",
      see="An ordinary man around 40 in a grey T-shirt, left forearm in a white cast and a navy sling, a loaded barbell on the rack beside him."),
 dict(n="Shot 2: checks his phone", s="F2_a", e="F3b_a", t="0:41.4 to 0:42.5 (1.1 s)",
      under="use Abs By AI to",
      act="Same spot, same camera. He finishes the head shake, takes his phone out with his good hand and reads it.",
      see="The back of the phone and a faint glow on his face. No screen content (a generated screen comes out as garbled text)."),
 dict(n="Shot 3: does leg presses instead", s="F4b_a", e="F5b_a", t="0:42.5 to 0:43.4 (0.9 s)",
      under="adjust your plan.",
      act="Cut to him seated in the leg press. He pushes the sled out once, cast arm resting in its sling.",
      see="The same man on a plain black 45-degree leg press, side-on, knees bent to legs extended."),
]
DEC = [
 ("Broken arm at the squat rack: the five frames", "Approve all five / Change (name the frame and what)"),
 ("Where it plays", "A (recommended): 0:39.1 to 0:43.4, 4.3 s, from \"when life gets in the way\"; the TIP 3 lower third ends when the clip starts. "
  "B: 0:40.4 to 0:43.4, 3.1 s, only \"When you get injured, use Abs By AI to adjust your plan.\" Three actions in 3.1 s is too fast; B would drop the walk-up."),
]
DECIDED = [
 "<b>Fixed the result card at 0:15.</b> The app recording now starts at 28.0 s. Round 1 showed the banned \"Meet the new you\" before/after screen for its first 8 frames (0.27 s). I scanned every frame of all three app cards against that screen: none left. Proof strip below.",
 "<b>Rebuilt the picture and the mix with voice B (the extra bass).</b> The new mix is sample-identical to the one you picked.",
 "<b>Kept \"completely free\" at 0:17 as filmed</b> (round 1 question you left unanswered).",
 "<b>Made each end frame by editing its start frame, so the camera never moves inside a shot.</b> My first drafts came from different angles; a start/end pair from two cameras makes the video model warp the room. Dropped the first walk-in frame: he walked toward the camera, away from the rack.",
 "<b>Phone screen stays hidden.</b> The phone shot lands on \"use Abs By AI\", so the words say what he is doing.",
 "<b>Ordinary-looking man, cast on his left arm, no logos or signage anywhere in the gym.</b> Checked every frame for extra fingers, wrong-arm casts and scrambled text.",
 "<b>Motion plan after your OK:</b> three 4 s Veo 3.1 Fast takes from these exact frame pairs, $0.40 each, $1.20 total; with a retake or two each, $3.60 at most (cap $10 for this ad, $0 spent: frames were made on the Codex subscription). I trim each take to its slot and never slow it. Every take passes the three sense checks (cause and effect, reads with the sound off, shows the line), mine and then an independent reviewer's, before you see it moving. AI-GENERATED chip on the clip.",
 "<b>If you say no:</b> the knee-brace stock clip (B0126) stays at 0:40.4 to 0:43.4, as in round 1.",
]
def pair(i, s):
    return f"""<section class="pair"><h3>{E(s['n'])} <span class="id">AI1-{i}</span></h3>
<div class="imgs"><figure><img src="stills/{s['s']}.jpg" loading="lazy"><figcaption>START</figcaption></figure>
<figure><img src="stills/{s['e']}.jpg" loading="lazy"><figcaption>END</figcaption></figure></div>
<table><tr><th>When</th><td>{s['t']}</td></tr><tr><th>Plays under</th><td><b>"{E(s['under'])}"</b></td></tr>
<tr><th>The action</th><td>{E(s['act'])}</td></tr><tr><th>What you see</th><td>{E(s['see'])}</td></tr>
<tr><th>Motion</th><td>Veo 3.1 Fast, 4 s take from this pair, trimmed to the slot, $0.40</td></tr></table></section>"""
reply = "RA-04 round 2\n" + "\n".join(f"{i+1}. {d[0]}: " for i, d in enumerate(DEC))
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RA-04 Round 2</title><style>
:root{{--bg:#eef4fb;--card:#fff;--ink:#14243a;--mute:#5a6b80;--line:#c9d8ea;--acc:#1f6fd1}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif}}
main{{max-width:900px;margin:0 auto;padding:20px 16px 80px}} @media(min-width:1300px){{main{{margin-left:max(16px,calc(50% - 620px))}}}}
h1{{font-size:24px;margin:0 0 4px}} h2{{font-size:19px;margin:28px 0 10px}} h3{{font-size:16px;margin:0 0 10px}}
.card,.pair{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}}
.id{{color:var(--mute);font-weight:400;font-size:13px}} .lock{{color:var(--mute)}}
ol.dec li{{margin:8px 0}} .imgs{{display:flex;gap:10px}} figure{{margin:0;flex:1}} figure img{{width:100%;border-radius:8px;display:block}}
figcaption{{font-size:12px;color:var(--mute);text-align:center}} table{{border-collapse:collapse;margin-top:10px;width:100%}}
th{{text-align:left;vertical-align:top;color:var(--mute);font-weight:600;padding:4px 10px 4px 0;width:120px}} td{{padding:4px 0}}
.words p{{margin:4px 0}} .strip img{{width:100%;border-radius:6px}} ul.dd li{{margin:7px 0}}
#dock{{background:#0c1a2c;border-radius:12px;padding:10px;margin:12px 0}} #dock video{{width:100%;max-height:70vh;display:block;border-radius:8px;background:#000}}
#dock .t{{color:#cfe0f5;font-size:13px;margin:6px 2px 0}} @media(min-width:1300px){{#dock{{position:fixed;right:24px;top:20px;width:380px;margin:0}}}}
button{{background:var(--acc);color:#fff;border:0;border-radius:8px;padding:7px 12px;font-size:14px;cursor:pointer;margin:4px 6px 4px 0}}
textarea{{width:100%;box-sizing:border-box;min-height:120px;font:14px/1.4 ui-monospace,Menlo,monospace;border:1px solid var(--line);border-radius:8px;padding:10px}}
</style></head><body>
<div id="dock"><video id="pv" controls preload="none" playsinline poster="stills/F2_a.jpg"></video><div class="t" id="pt">Pick a clip below</div></div>
<main>
<h1>Top 3 Tips For Getting Abs: round 2</h1>
<p>AD, RA-04. Short-form ad from roll C1664 (58.9 s, 9:16).</p>
<p class="lock"><b>Already locked:</b> first 30 seconds (your "First 30 seconds look good"), the Soft Blue analysis card, voice B with the extra bass.</p>
<div class="card"><h2 style="margin-top:0">Your decisions ({len(DEC)})</h2><ol class="dec">{''.join(f'<li><b>{E(a)}</b>: {E(b)}</li>' for a, b in DEC)}</ol></div>

<h2>Tip 3 in context: the frames on the real words</h2>
<div class="card"><button onclick="play('context/AI1-tip3-context - REVIEW 540p.mp4','Tip 3, 0:35.5 to 0:45.5: frames as stills, motion pending')">Play it in context (0:35.5 to 0:45.5)</button>
<div class="words"><p><b>Before:</b> "Number three, use AI to solve any problems" (Dan on camera, TIP 3 lower third)</p>
<p><b>Under the clip:</b> <b>"when life gets in the way. When you get injured, use Abs By AI to adjust your plan."</b></p>
<p><b>After:</b> "If you can't make it to the gym one day, have Abs By AI design you a home workout..." (Dan, then his real squats on the lawn)</p></div>
<p class="lock">The stills hold where motion will play. In the finished cut, the captions run over the clip as usual.</p></div>

<h2>New AI clip: "Broken arm at the squat rack" (three shots, five frames)</h2>
{''.join(pair(i + 1, s) for i, s in enumerate(SHOTS))}

<h2>What I decided (overrule anything)</h2>
<div class="card"><ul class="dd">{''.join(f'<li>{d}</li>' for d in DECIDED)}</ul></div>

<h2>Fixed: the result card at 0:15</h2>
<div class="card"><button onclick="play('context/G-flowb-context - REVIEW 540p.mp4','Result card, 0:12 to 0:21 (round 2)')">Play it in context (0:12 to 0:21)</button>
<p><b>Round 1, first 5 frames of the card</b> (the banned before/after screen):</p><div class="strip"><img src="stills/flowb_round1_first5.jpg" loading="lazy"></div>
<p><b>Round 2, first 5 frames</b> (the after picture alone):</p><div class="strip"><img src="stills/flowb_round2_first5.jpg" loading="lazy"></div></div>

<h2>Your reply</h2>
<div class="card"><textarea id="rb">{E(reply)}</textarea><button onclick="navigator.clipboard.writeText(document.getElementById('rb').value);this.textContent='Copied'">Copy</button></div>
</main>
<script>function play(src,t){{const v=document.getElementById('pv');v.src=encodeURI(src);document.getElementById('pt').textContent=t;v.play();}}</script>
</body></html>"""
open(f"{R}/index.html", "w").write(page)
assert "—" not in page and "–" not in page
print("PAGE_OK")
