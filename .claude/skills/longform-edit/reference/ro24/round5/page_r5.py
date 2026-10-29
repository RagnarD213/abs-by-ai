"""RO-24 round 5 review page (mid-round, frames first): the new A7 start/end frames (only if gate.py --verify passes), the four
finished changes playing in context (G06 card, P8 Amy Schumer abs photo, the tightened 7 DAYS A WEEK cut, A3), where each
approved AI clip stands, What I decided, checks, reply. The whole film follows once the last AI clips are made and cut in.
    python3 page_r5.py"""
import json, html, os, subprocess
R5 = '/Volumes/Expansion/_edit_work/RO-24/round5'; OUT = f'{R5}/review'
P = '/Users/danielrose/Projects/Claude/Projects/Abs By AI'; FC = f'{P}/.claude/skills/_shared/framecheck/gate.py'
E = html.escape; L = lambda p: json.load(open(p)) if os.path.exists(p) else None
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
def btn(src, label): return f"""<button onclick="play('{src}','{E(label)}')">Play: {E(label)}</button>"""
d = f'{R5}/ai/A7'
ok = subprocess.run(['python3', FC, f'{d}/start.png', f'{d}/end.png', '--verify'], capture_output=True, text=True, cwd=P).returncode == 0
assert ok, 'A7 frames do not pass gate --verify'
for f in ('start', 'end'):
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', f'{d}/{f}.png', '--out', f'{OUT}/ai/A7_{f}.jpg'], capture_output=True)
old = '/Volumes/Expansion/_edit_work/RO-24/round4/review/ai'
ctx = {c['id']: c for c in L(f'{OUT}/context/index.json') or []}
man = {m['id']: m for m in L(f'{R5}/film_manifest_r5.json')}
CH = [('G06', 'Head-to-head study card', man['G06']['a'],
       'Title "Zepbound Beats Ozempic In Studies", bars labelled Zepbound and Ozempic, and under them two very short bars on a full 0 to 100% track: '
       'quit over stomach side effects, Zepbound 2.7%, Ozempic 5.6%. The quit heading lands on "only", Ozempic\'s bar on "half", Zepbound\'s on "Zepbound".'),
      ('P8', 'Amy Schumer\'s abs photo', man['P8']['a'],
       'Her Instagram story of October 23, 2025 ("No filter no filler no clean mirror"), full screen from "and she posted pictures of her abs" to the cut. '
       'Credited "@amyschumer via Instagram". Cropped below the story\'s header; her face is out of her own shot, so her name chip identifies her.'),
      ('BG21', 'The 7 DAYS A WEEK pause', 345.18,
       'The 1.1 second silence after "...and why you should too." is now 0.4 seconds. Everything after it is 0.6 seconds earlier; nothing else moved.'),
      ('A3', 'AI clip A3, the newspaper', man['A3']['a'],
       'Made on your Flow subscription from your approved frames: he lowers the "Weight-Loss Drug Horror Stories" paper, spooked, over "Stories like this are used to scare people out of taking Zepbound."')]
def card(cid, lab, t, what):
    c = ctx.get(cid); a0 = max(0, t - 4)
    media = (f'<a href="{c["jpg"]}"><img loading="lazy" src="{c["jpg"]}"></a>' + btn(c['mp4'], f'{lab} in context')) if c else '<p class="small">context clip missing</p>'
    return f'<article><h3>{E(lab)} <span class="small">{mmss(t)}</span></h3>{media}<div class="copy">{E(what)}<br><span class="small">Watch from {mmss(a0)}.</span></div></article>'
STATUS = [('A1', 'Opening, two shots', 'Shot 1 made and passed (two men press their pens, glance at each other). Shot 2 not made: Flow refused its start frame three times ("Failed to upload"), then credits ran out.'),
          ('A3', 'Newspaper', 'Made, passed both checks, in the film at 2:13.4.'),
          ('A4', 'Steakhouse pasta', 'Made, but the independent film reviewer failed it: he grins at the pasta and the bowl ends in front of him, so it reads as "about to eat it". Being remade from your start frame with him shaking his head and pushing the bowl to the far edge of the table.'),
          ('A6', 'Buffet roll', 'Not made yet: Flow credits ran out.'),
          ('A7', 'Stairs vs jump', 'New frames below for your yes before any motion.'),
          ('A8', 'Bathroom scale', 'Not made yet: Flow credits ran out.')]
decisions = ['<b>A7 frames</b>: yes, or what to change. Motion starts only after your yes.',
             '<b>The last AI clips</b> (A1 shot 2, A6, A8 and the A4 remake): pay about $4 on the paid video API now, or wait for tomorrow\'s free Flow credits.',
             '<b>The four finished changes</b> below: approve, or give changes.']
decided = ['The study card now names the drugs, since you lifted the no-drug-names rule for videos entirely about weight-loss drugs. The quit bars sit on a full 0 to 100% track so you can see at a glance how few people quit.',
           'Amy\'s photo is the exact Instagram story the press reported on October 24, 2025. I left out the story\'s header and her caption sticker, and kept her mirror selfie whole.',
           'The pause: I removed 19 silent frames right before the cut into the photo cards, leaving a natural breath (0.4 s) between "why you should too" and the next line.',
           'A7: built the end frame first (him in a heap on flat lawn at the foot of the wall, in front), then the start from it, on one shared background so only the two men change. It took four independent reviews: the first three caught a background that changed behind the men, a ghost of a shoe on a step, the jumper\'s hair and trouser colour changing, and a half-missing shoe. All fixed.',
           'A1 stays as option A (the photo montage) in the opening until shot 2 exists; the two shots go in together.',
           'Spend so far: $0. Motion on your Flow subscription (3 clips, 30 credits); stills on the Codex subscription.']
checks = ['Every AI take used passed the motion check and a fresh independent reviewer on the exact frames used (A1 shot 1, A3; A4 passed both but was then failed by the film reviewer for what it shows).',
          'A7 frames: frame gate pass and a fresh independent reviewer pass (fourth build).',
          'Independent film review of this round\'s build: the card, the photo, the pause and A3 all passed; 423 sampled frames match round 4 everywhere outside the new items; the audio matches round 4 exactly apart from the trim. It failed only A4, which is now out.',
          'Hair clearance unchanged from round 4: closest 42 px from the top (needs 20). Loudness -14.5 LUFS, peak -1.2 dBTP.']
reply = '1 A7 frames: yes / change:\n2 Last AI clips: pay about $4 now / wait for free credits:\n3 Card, Amy photo, pause, A3: approve / changes:\n4 Anything else: '
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Celebrity Ozempic, round 5</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1240px;margin:0 auto;padding:28px 16px}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:calc(62vw)}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px}}p,li{{color:var(--mute)}}section{{margin:30px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}figure{{margin:0}}figcaption{{font-size:13px;color:#9fb7cf}}
img,video{{width:100%;border-radius:10px;background:black}}a{{color:var(--acc)}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:15px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
table{{width:100%;border-collapse:collapse;font-size:15px}}td{{border-top:1px solid var(--line);padding:8px;vertical-align:top;color:#d7e6f5}}
textarea{{width:100%;box-sizing:border-box;min-height:200px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px}}#dock video{{max-height:60vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid,.pair{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<div id="dock"><div class="small" id="nowp">Pick anything below to play it here.</div><video id="pv" controls muted preload="none" playsinline></video></div>
<main><h1>Reacting To Celebrity Ozempic Transformations <span class="small">LFC, round 5</span></h1>
<p>Your round 4 notes, done so far: the new A7 frames, the head-to-head card, Amy Schumer's abs photo, the 7 DAYS A WEEK pause, and the newspaper AI clip cut in. The whole film comes next, once the last AI clips are made and checked.</p>
<p class="notice"><b>Locked, unchanged:</b> everything you approved in round 4. After 5:45 the film is 0.6 seconds earlier (the pause), nothing else.</p>
<nav><a href="#decide">Your decisions</a><a href="#a7">A7 frames</a><a href="#changes">Finished changes</a><a href="#ai">AI clips</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(decisions)})</h2><ol>{''.join('<li>' + x + '</li>' for x in decisions)}</ol></section>
<section id="a7"><h2>A7: new start and end frames</h2>
<p class="small">Round 4 version, for comparison:</p><div class="pair"><figure><img src="ai/A7_old_start.jpg"><figcaption>Round 4 START</figcaption></figure><figure><img src="ai/A7_old_end.jpg"><figcaption>Round 4 END</figcaption></figure></div>
<p class="small">Round 5 (new):</p><div class="pair"><figure><a href="ai/A7_start.jpg"><img src="ai/A7_start.jpg"></a><figcaption>START</figcaption></figure><figure><a href="ai/A7_end.jpg"><img src="ai/A7_end.jpg"></a><figcaption>END</figcaption></figure></div>
<div class="copy"><b>Your line:</b> "Don't go from 5 mg to 0. Step down gradually, 1 mg per week." (at {mmss(461.24)})<br><b>The clip:</b> the man in the red shirt, on the left in front, crouches on top of the wall and jumps the full height down to the flat lawn, landing in a dazed, unhurt heap; the other man walks down the steps.<br>
<span class="small">Passed the frame check and a fresh independent reviewer who saw only the pictures. Labelled AI-GENERATED on screen. Motion is made only after your yes.</span></div></section>
<section id="changes"><h2>Finished changes, in context</h2><div class="grid">{''.join(card(*x) for x in CH)}</div></section>
<section id="ai"><h2>Where each AI clip stands</h2><table>{''.join(f'<tr><td><b>{i}</b></td><td>{E(n)}</td><td>{E(s)}</td></tr>' for i, n, s in STATUS)}</table></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in decided)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in checks)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
assert '—' not in page, 'em dash on the page'
open(f'{OUT}/index.html', 'w').write(page); print('page ok', sorted(ctx))
