#!/usr/bin/env python3
"""RA-04 round 2c review page -> round2c/index.html: shot 3 rebuilt after Dan's body-angle rejection (2026-10-14)."""
import html
R = "/Volumes/Extreme/_edit_work/ra04/round2c"
E = html.escape
PHYS = [
 "He lies back on a reclined pad and pushes straight along the rails: his hip-to-feet line is 6 degrees from the rails at the start and 6 at the end (your round 2b frames were 26 to 43 degrees off; that was the 90-degree push).",
 "Bone lengths match between the frames: torso 266 / 267 px, thigh 204 / 210, shin 196 / 205 (within 4 %). The image model stretches legs whenever it straightens them, so I measured this on every candidate.",
 "The sled moves as one solid piece exactly along the 45-degree rails: plate, platform, bracket and both shoes all move about 30 px right and 30 px up. The frame, seat, background and his hips do not move at all.",
 "Both feet stay flat on the platform, which is square to the rails. Plates only on the side horn. One phone, in his good hand, in both frames.",
 "Because his knees start fairly open (127 degrees), straightening them pushes the sled only about 10 cm. That is what real legs this length can do, so it reads as a short, honest push. A deeper rep needs a start frame with the knees bent further, which means another round.",
]
DECIDED = [
 "<b>You were right, and it should never have reached you.</b> The round 2b frames had him sitting upright and pushing about 26 to 43 degrees away from the rails. I now measure his body angles on every frame (pose detection), and I prove each check on the frames you rejected before I trust it on new ones.",
 "<b>Seven independent reviews, six fails, then a pass.</b> Each frame pair went to a fresh reviewer with a body and physics checklist; that reviewer saw only the pictures. The fails, all fixed before you saw anything: the machine frame stretched between frames; the sled slid off its rails; the platform stood too upright; his legs grew 24 % longer; a leftover phone floated in the air; a phantom third toe; a dark patch on the pillar; his feet slid down the platform; a smeared platform corner; one shoe disappeared. The seventh review passed every item.",
 "<b>How the end frame is built now:</b> the image model kept redrawing the machine slightly differently, so the machine in the end frame is the start frame's machine, with the sled cut out and moved exactly along the rails in code. Only the man (straightened legs, face, phone) comes from the generated picture. His feet were nudged 22 px so they ride the platform.",
 "<b>Expression:</b> start, smiling at his phone; end, a teeth-showing grin with squinted eyes. The reviewer called it a straining smile that some could read as laughing.",
 "<b>One small flaw left:</b> the platform's lower-left edge is a little soft in the end frame (dark on dark, hard to see at normal size). Extending the cut-out to fix it dragged a piece of rail along with the sled, which is worse, so I kept the version that passed.",
 "<b>Where it plays:</b> slot A, 0:42.5 to 0:43.4 under \"adjust your plan.\" Budget $20 for this ad, $0 spent (all frames on the Codex subscription).",
]
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RA-04 Round 2c</title><style>
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
<div id="dock"><video id="pv" controls preload="none" playsinline poster="stills/F4h.jpg"></video><div class="t" id="pt">Pick a clip below</div></div>
<main>
<h1>Top 3 Tips For Getting Abs: round 2c</h1>
<p>AD, RA-04. Only shot 3 of "Broken arm at the squat rack" changed: rebuilt so his body and the machine move like a real leg press.</p>
<p class="lock"><b>Already locked:</b> first 30 seconds, Soft Blue analysis card, voice B with the extra bass, the result card fix, shots 1 and 2 frames.</p>
<div class="card"><h2 style="margin-top:0">Your decisions (1)</h2><ol><li><b>Shot 3, "Does leg presses instead": the new start and end frames</b>: Approve / Change (say what).</li></ol></div>

<h2>Shot 3: does leg presses instead <span class="lock" style="font-size:13px">AI1-3</span></h2>
<div class="card"><div class="imgs"><figure><img src="stills/F4h.jpg"><figcaption>NEW START: lying back, knees bent, smiling at his phone</figcaption></figure>
<figure><img src="stills/F5p.jpg"><figcaption>NEW END: legs straightened along the rails, smiling through the effort</figcaption></figure></div>
<table><tr><th>When</th><td>0:42.5 to 0:43.4</td></tr>
<tr><th>Before it</th><td>Shot 2: at the squat rack he takes out his phone, under "use Abs By AI to"</td></tr>
<tr><th>Plays under</th><td><b>"adjust your plan."</b></td></tr>
<tr><th>After it</th><td>Dan on camera: "If you can't make it to the gym one day..."</td></tr>
<tr><th>The action</th><td>Lying back on the pad, he lowers the phone to his chest and straightens his legs, pushing the sled a short way up the rails, cast arm resting in its sling.</td></tr>
<tr><th>If you say no</th><td>The knee-brace stock clip (B0126) stays in tip 3.</td></tr></table>
<h3 style="margin-top:14px">Body and physics checks (measured, then confirmed by an independent reviewer)</h3><ul>{''.join(f'<li>{E(p)}</li>' for p in PHYS)}</ul>
<p class="lock">The body measurement on the new frames (yellow: shoulder, hip, knee, ankle; blue: the rail line):</p>
<div class="imgs small"><figure><img src="stills/pose_F4h.jpg" loading="lazy"><figcaption>start</figcaption></figure><figure><img src="stills/pose_F5p.jpg" loading="lazy"><figcaption>end</figcaption></figure></div>
<p class="lock">Round 2b frames you sent back:</p>
<div class="imgs small"><figure><img src="stills/r2b_start.jpg" loading="lazy"><figcaption>2b start</figcaption></figure><figure><img src="stills/r2b_end.jpg" loading="lazy"><figcaption>2b end</figcaption></figure></div></div>

<h2>Tip 3 in context, all five frames on the real words</h2>
<div class="card"><button onclick="play('context/AI1-tip3-context v3 - REVIEW 540p.mp4','Tip 3, 0:35.5 to 0:45.5: frames as stills, motion pending')">Play it in context (0:35.5 to 0:45.5)</button>
<div class="imgs small"><figure><img src="stills/S1_a.jpg" loading="lazy"><figcaption>Shot 1 start (approved)</figcaption></figure><figure><img src="stills/F2_a.jpg" loading="lazy"><figcaption>Shot 1 end / shot 2 start (approved)</figcaption></figure><figure><img src="stills/F3b_a.jpg" loading="lazy"><figcaption>Shot 2 end (approved)</figcaption></figure></div></div>

<h2>What I decided (overrule anything)</h2>
<div class="card"><ul>{''.join(f'<li>{d}</li>' for d in DECIDED)}</ul></div>

<h2>Your reply</h2>
<div class="card"><textarea id="rb">RA-04 round 2c
1. Shot 3 frames: </textarea><button onclick="navigator.clipboard.writeText(document.getElementById('rb').value);this.textContent='Copied'">Copy</button></div>
</main>
<script>function play(src,t){{const v=document.getElementById('pv');v.src=encodeURI(src);document.getElementById('pt').textContent=t;v.play();}}</script>
</body></html>"""
assert "—" not in page and "–" not in page
open(f"{R}/index.html", "w").write(page); print("PAGE_OK")
