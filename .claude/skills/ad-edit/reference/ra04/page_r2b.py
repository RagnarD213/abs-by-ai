#!/usr/bin/env python3
"""RA-04 round 2b review page -> round2b/index.html: only shot 3 changed (Dan, 2026-10-14)."""
import html
R = "/Volumes/Extreme/_edit_work/ra04/round2b"
E = html.escape
PHYS = [
 "The machine is a real 45-degree leg press: low reclined seat, two rails running up at an angle, one sled riding on them.",
 "One flat steel platform is bolted to the sled. Both feet are flat on that platform, in both frames.",
 "Plates sit only on the two weight horns that stick out the sides of the sled, behind the platform. None in front of or under his feet.",
 "From start to end, the platform, both horns and all four plates move up the rails together as one piece: the plates keep the same spot against the platform's top edge (measured on both frames).",
 "Seat, rails, frame, background and his back on the pad do not move. Phone stays in his good hand the whole time, so nothing appears or vanishes.",
]
DECIDED = [
 "<b>Shots 1 and 2 recorded as approved</b>, frames unchanged (your \"All of the frames are looking good except for shot 3\").",
 "<b>Shot 3, start:</b> he sits in the leg press with the knees bent and feet on the platform, looking at his phone with a smile. I made two versions and kept the one whose machine is built right; the other had plates beside the platform and his legs folded unnaturally.",
 "<b>Shot 3, end:</b> made by editing the start frame, so the camera and machine stay put. I made two versions. The one I dropped had a bigger grin but its plates drifted about 40 px against the platform (the sled was not moving as one solid piece). The one I kept moves as one piece and shows the smile with real effort.",
 "<b>The phone stays in his right hand during the rep</b> (resting against his chest) so it never vanishes between frames.",
 "<b>Where it plays:</b> you didn't pick, so I'm using A (my recommendation): 0:39.1 to 0:43.4, with shot 3 under \"adjust your plan.\" Say B if you want the shorter slot.",
 "<b>Budget:</b> raised to $20 for this ad, as you approved. $0 spent: all frames were made on the Codex subscription. Next round: three 4 s Veo motion takes at $0.40 each, and I regenerate any take whose physics is off before you see it (the sled and plates moving together, feet staying on the platform, nothing appearing or vanishing).",
]
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RA-04 Round 2b</title><style>
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
textarea{{width:100%;box-sizing:border-box;min-height:90px;font:14px/1.4 ui-monospace,Menlo,monospace;border:1px solid var(--line);border-radius:8px;padding:10px}}
</style></head><body>
<div id="dock"><video id="pv" controls preload="none" playsinline poster="stills/F4c_a.jpg"></video><div class="t" id="pt">Pick a clip below</div></div>
<main>
<h1>Top 3 Tips For Getting Abs: round 2b</h1>
<p>AD, RA-04. Only shot 3 of "Broken arm at the squat rack" changed.</p>
<p class="lock"><b>Already locked:</b> first 30 seconds, Soft Blue analysis card, voice B with the extra bass, the result card fix, shots 1 and 2 frames.</p>
<div class="card"><h2 style="margin-top:0">Your decisions (1)</h2><ol><li><b>Shot 3, "Does leg presses instead": the new start and end frames</b>: Approve / Change (say what).</li></ol></div>

<h2>Shot 3: does leg presses instead <span class="lock" style="font-size:13px">AI1-3</span></h2>
<div class="card"><div class="imgs"><figure><img src="stills/F4c_a.jpg"><figcaption>NEW START: smiling at his phone, feet on the platform</figcaption></figure>
<figure><img src="stills/F5c_b.jpg"><figcaption>NEW END: still smiling, working through the rep</figcaption></figure></div>
<table><tr><th>When</th><td>0:42.5 to 0:43.4</td></tr>
<tr><th>Before it</th><td>Shot 2: at the squat rack he takes out his phone, under "use Abs By AI to"</td></tr>
<tr><th>Plays under</th><td><b>"adjust your plan."</b></td></tr>
<tr><th>After it</th><td>Dan on camera: "If you can't make it to the gym one day..."</td></tr>
<tr><th>The action</th><td>He glances up from his phone, still smiling, and pushes the sled up the rails once, cast arm resting in its sling.</td></tr>
<tr><th>If you say no</th><td>The knee-brace stock clip (B0126) stays in tip 3.</td></tr></table>
<h3 style="margin-top:14px">Physics checks I ran on both frames</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in PHYS)}</ul>
<p class="lock">Round 2 frames you sent back, for comparison:</p>
<div class="imgs small"><figure><img src="stills/old_F4b_a.jpg" loading="lazy"><figcaption>old start</figcaption></figure><figure><img src="stills/old_F5b_a.jpg" loading="lazy"><figcaption>old end</figcaption></figure></div></div>

<h2>Tip 3 in context, all five frames on the real words</h2>
<div class="card"><button onclick="play('context/AI1-tip3-context v2 - REVIEW 540p.mp4','Tip 3, 0:35.5 to 0:45.5: frames as stills, motion pending')">Play it in context (0:35.5 to 0:45.5)</button>
<div class="imgs small"><figure><img src="stills/S1_a.jpg" loading="lazy"><figcaption>Shot 1 start (approved)</figcaption></figure><figure><img src="stills/F2_a.jpg" loading="lazy"><figcaption>Shot 1 end / shot 2 start (approved)</figcaption></figure><figure><img src="stills/F3b_a.jpg" loading="lazy"><figcaption>Shot 2 end (approved)</figcaption></figure></div></div>

<h2>What I decided (overrule anything)</h2>
<div class="card"><ul>{''.join(f'<li>{d}</li>' for d in DECIDED)}</ul></div>

<h2>Your reply</h2>
<div class="card"><textarea id="rb">RA-04 round 2b
1. Shot 3 frames: </textarea><button onclick="navigator.clipboard.writeText(document.getElementById('rb').value);this.textContent='Copied'">Copy</button></div>
</main>
<script>function play(src,t){{const v=document.getElementById('pv');v.src=encodeURI(src);document.getElementById('pt').textContent=t;v.play();}}</script>
</body></html>"""
assert "—" not in page and "–" not in page
open(f"{R}/index.html", "w").write(page); print("PAGE_OK")
