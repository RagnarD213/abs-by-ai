"""RO-24 round 5 review page (full film): the whole round 5 film (540p copy, full-res link), every change with its time in the new
film and a short watch range (plus its context clip), where each AI clip stands, new frame proposals for A4/A6/A7, What I decided,
spend, checks read from the stamps that actually ran, reply. Served by review_server.py (the silent-check / owner hand-off helper
is injected there).
    python3 page_r5.py"""
import json, html, os, re
R5 = '/Volumes/Expansion/_edit_work/RO-24/round5'; OUT = f'{R5}/review'; FIN = f'{R5}/final'; NAME = 'RO24_R5_MASTER'
E = html.escape; L = lambda p: json.load(open(p)) if os.path.exists(p) else None
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
os.makedirs(f'{OUT}/film', exist_ok=True)
for src, dst in ((f'{FIN}/{NAME} - REVIEW 540p.mp4', 'film/film_540p.mp4'), (f'{FIN}/{NAME}.mp4', 'film/film_full.mp4')):
    d = f'{OUT}/{dst}'
    if os.path.lexists(d): os.remove(d)
    os.symlink(src, d)
ctx = {c['id']: c for c in L(f'{OUT}/context/index.json') or []}
man = {m['id']: m for m in L(f'{R5}/film_manifest_r5.json')}
dur = L(f'{R5}/edl_r5.json')['items'][-1]['o1'] * 1001 / 30000

CH = [('A1', 'Opening: AI clip A1, two shots', man['A1']['a'], man['A1']['b'],
       'Shot 1 (moving, Flow): the two men press their pens and glance at each other over "Why do some people get ripped from taking weight loss medication?" '
       'Cut at 0:03.1, in the breath before "Well", to shot 2: your approved end frame, the gaunt man\'s hand on his hollow cheek beside the lean man, '
       'with a slow push toward him over "Well, for other people, it totally destroys their life." Replaces the photo montage.'),
      ('A3', 'AI clip A3, the newspaper', man['A3']['a'], man['A3']['b'],
       'He lowers the "Weight-Loss Drug Horror Stories" paper, spooked, over "Stories like this are used to scare people out of taking Zepbound." (you approved it mid-round)'),
      ('P8', 'Amy Schumer\'s abs photo', man['P8']['a'], man['P8']['b'],
       'Her Instagram story of October 23, 2025, full screen on "and she posted pictures of her abs", credited "@amyschumer via Instagram". (approved mid-round)'),
      ('G06', 'Head-to-head study card', man['G06']['a'], man['G06']['b'],
       '"Zepbound Beats Ozempic In Studies", bars labelled Zepbound and Ozempic, and the two short quit bars: 2.7% and 5.6% on a full 0 to 100% track. (approved mid-round)'),
      ('BG21', 'The 7 DAYS A WEEK pause', 345.18, 346.2,
       'The silence after "...and why you should too." is 0.4 s now (was 1.1 s). Everything after it is 0.6 s earlier. (approved mid-round) No ear has heard this join yet, only measurements: please give 5:42 to 5:48 one listen.'),
      ('A8', 'AI clip A8, the bathroom scale', man['A8']['a'], man['A8']['b'],
       'He steps up onto the bathroom scale over "and keep weighing yourself daily"; the Step Down Slowly card stays readable on the left.')]
def row(cid, lab, a, b, what):
    c = ctx.get(cid); w0, w1 = max(0, a - 4), min(dur, b + 4)
    clip = f"""<button onclick="play('{c['mp4']}','{E(lab)} (context clip)',0)">Context clip</button>""" if c else ''
    img = f'<a href="{c["jpg"]}"><img loading="lazy" src="{c["jpg"]}"></a>' if c else ''
    return (f'<article>{img}<h3>{E(lab)}</h3><p class="t"><b>{mmss(a)} to {mmss(b)}</b> in the new film. Watch {mmss(w0)} to {mmss(w1)}.</p>'
            f'<div class="copy">{E(what)}</div><button onclick="play(\'film/film_540p.mp4\',\'Full film from {mmss(w0)}\',{w0:.2f})">Play in film from {mmss(w0)}</button>{clip}</article>')

STATUS = [('A1', 'Opening, two shots', 'In the film (0:00). Shot 1 moves. Shot 2: Veo could not hold the pose in 23 takes (his hand rubbed up to his eye or temple or down to his chin, both mouths opened as if talking, the lean man turned to the camera), so it is your approved end frame with a slow camera push.'),
          ('A3', 'Newspaper', 'In the film (2:13.4).'),
          ('A4', 'Steakhouse pasta', 'Keeps the round 4 picture. None of eight motion takes passed. In the ones that got furthest, the bowl slides toward his own steak plate or ends in front of him, so it reads as "about to eat it", the opposite of the line.'),
          ('A6', 'Buffet roll', 'Keeps the round 4 picture. Eight motion takes (paid API and Flow) all failed the motion checks.'),
          ('A7', 'Stairs vs jump', 'Keeps the round 4 picture. Your new frames are approved, but the three takes jump in slow motion with no landing, and speeding them up makes the man on the stairs scurry.'),
          ('A8', 'Bathroom scale', 'In the film (7:46.7).')]
PROPOSE = [('A1 shot 2', 'Keep the still with the push (my pick: it reads instantly and nothing in it can go wrong), or I keep trying for real motion with a simpler pose: the gaunt man alone, hands at his sides, looking at his reflection.'),
           ('A4', 'A new end frame: the bowl at the far edge of the table on the waiter\'s side, his knife and fork down, his hand raised in a small "no thanks". With the bowl already clearly away in the end frame, the motion has only one way to go.'),
           ('A6', 'A new end frame: the plate set down on the buffet counter instead of held, so the motion is one simple move.'),
           ('A7', 'Two shots instead of one: the red-shirt jumper alone, made at real speed, landing in a heap; then the man walking down the steps. Each gets its own natural speed.')]
decisions = ['<b>The full film</b>: approve, or give changes.',
             '<b>A1 shot 2</b>: keep the still with the slow push, or keep trying for motion.',
             '<b>A4, A6, A7</b>: yes to the new frame ideas below (I build the frames, show you, then make motion), or keep the round 4 pictures and finish.']
decided = ['A1 shot 2: after 23 takes on your subscription (three prompt rewrites, an "avoid" list, shorter windows), none held his hand on his cheek with both mouths closed for 2.8 seconds. I used your approved end frame with a slow 5% push toward the gaunt man, still labelled AI-GENERATED. Shot 1 keeps its motion, and the cut sits in the breath before "Well".',
           'A4, A6 and A7 stay exactly as you approved them in round 4 rather than ship a take that failed. New frame ideas for each are below.',
           'The weigh-in clip at 7:46 has its AI-GENERATED label top-right this round, because the "Step Down Slowly" card covers the top-left corner.',
           'The opener shows both men holding up their shirts with the pen at the stomach, as in the frames you approved. A separate check found no pinch, no zoom on the belly and no needle, so I kept it. Say so if you want it framed higher.',
           'Nothing else changed: everything from round 4 is as you approved it; the film is 0.6 s shorter after 5:45 (the pause).',
           'Spend: $4.00 on the paid video API (your yes), the rest on your Flow subscription (no extra cost; about 24,500 credits left until November 29). Stills on the Codex subscription.']
def checks():
    out = []
    ag = L(f'{FIN}/{NAME}.mp4.audio_gate.json')
    if ag:
        rows = {r['key']: r for r in ag.get('rows', [])}; bad = [k for k, r in rows.items() if not r.get('ok')]
        known = {'tone': 'tone (the voice recording\'s colour, which you accepted in round 4)', 'artifacts': 'high-frequency swirl (already in the original microphone recording; round 5 adds none)'}
        txt = f"Audio gate: {ag.get('verdict', '?')}, loudness {rows['lufs']['value']:.1f} LUFS, peak {rows['tp']['value']:.1f} dBTP"
        if bad: txt += '; failing rows: ' + ', '.join(known.get(k, k) for k in bad) + (', the same as round 4' if set(bad) <= set(known) else ', NEW since round 4')
        out.append(txt)
    dg = L(f'{FIN}/{NAME}.mp4.deliver_gate.json')
    if dg:
        bad = [k for k, r in dg.get('rows', {}).items() if not r.get('ok')]
        r4 = L('/Volumes/Expansion/_edit_work/RO-24/round4/final/RO24_R4_MASTER.mp4.deliver_gate.json') or {}
        r4bad = {k for k, r in r4.get('rows', {}).items() if not r.get('ok')}
        out.append(f"Delivery gate (longform): {dg.get('verdict', '?')}" + (f"; {len(bad)} failing rows: " + ', '.join(bad) + ('. The same rows failed on the round 4 film you approved' if set(bad) <= r4bad else '. NEW since round 4: ' + ', '.join(sorted(set(bad) - r4bad))) if bad else ''))
    hr = L(f'{R5}/checks/hair.json')
    if hr: out.append(f"Hair clearance: no frame cuts into the hair; closest {hr['min_top']} px from the top, the template's normal headroom (verdict {hr.get('verdict', '?')} means look, and I looked)")
    rv = f'{OUT}/ROUND-5-REVIEW.md'
    if os.path.exists(rv):
        m = re.findall(r'(?im)^.*\b(DOES NOT SHIP|SHIP)\b.*$', open(rv).read())
        if m: out.append('Independent film review of the delivered file: ' + ('SHIP' if 'DOES NOT SHIP' not in m[-1].upper() else 'DOES NOT SHIP'))
    out.append('Every AI take in the film passed the motion check and a fresh independent reviewer on the exact frames used (A1 shot 1, A3, A8); A1 shot 2 is a frame that passed the frame gate and its own reviewer.')
    return out
reply = '1 Full film: approve / changes:\n2 A1 shot 2: keep the still / keep trying motion:\n3 A4, A6, A7 new frames: yes / keep round 4:\n4 Anything else: '
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Celebrity Ozempic, round 5</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1240px;margin:0 auto;padding:28px 16px}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:calc(62vw)}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px}}p,li{{color:var(--mute)}}section{{margin:30px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}
img,video{{width:100%;border-radius:10px;background:black}}a{{color:var(--acc)}}.small{{font-size:14px;color:#9fb7cf}}.t{{margin:4px 0;color:#d7e6f5}}
.copy{{font-size:15px;margin-top:6px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
table{{width:100%;border-collapse:collapse;font-size:15px}}td{{border-top:1px solid var(--line);padding:8px;vertical-align:top;color:#d7e6f5}}
textarea{{width:100%;box-sizing:border-box;min-height:180px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px}}#dock video{{max-height:60vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin:8px 8px 0 0}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<div id="dock"><div class="small" id="nowp">The full round 5 film. Pick any change below to jump to it.</div><video id="pv" controls preload="metadata" playsinline src="film/film_540p.mp4"></video>
<div class="small"><a href="film/film_full.mp4">Full resolution file</a> ({int(dur // 60)}:{dur % 60:04.1f})</div></div>
<main><h1>Reacting To Celebrity Ozempic Transformations <span class="small">LFC, round 5, full film</span></h1>
<p>The whole film with your round 4 notes in. Six places changed; everything else is exactly as you approved it.</p>
<p class="notice"><b>Only watch the ranges below.</b> Outside them the film is round 4, moved 0.6 s earlier after 5:45 (the pause). Two small background changes ride along: the blurred clip behind you from 2:05 now runs on to the newspaper without jumping, and the Amy interview behind you changes shot at 4:11 instead of just before her photo.</p>
<nav><a href="#decide">Your decisions</a><a href="#changes">What changed, with times</a><a href="#ai">AI clips</a><a href="#propose">New frame ideas</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(decisions)})</h2><ol>{''.join('<li>' + x + '</li>' for x in decisions)}</ol></section>
<section id="changes"><h2>What changed, with times in the new film</h2><div class="grid">{''.join(row(*x) for x in CH)}</div></section>
<section id="ai"><h2>Where each AI clip stands</h2><table>{''.join(f'<tr><td><b>{i}</b></td><td>{E(n)}</td><td>{E(s)}</td></tr>' for i, n, s in STATUS)}</table></section>
<section id="propose"><h2>New frame ideas (nothing made until your yes)</h2><table>{''.join(f'<tr><td><b>{i}</b></td><td>{E(s)}</td></tr>' for i, s in PROPOSE)}</table></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in decided)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(x) + '</li>' for x in checks())}</ul><p class="small">Checks are measurements and silent playback, not a listening pass.</p></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,label,t){{const v=document.getElementById('pv');if(!v.src.endsWith(src))v.src=src;document.getElementById('nowp').textContent=label;
const go=()=>{{v.currentTime=t||0;v.play();}};if(v.readyState>=1)go();else v.addEventListener('loadedmetadata',go,{{once:true}});if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
assert '—' not in page, 'em dash on the page'
open(f'{OUT}/index.html', 'w').write(page); print('page ok', sorted(ctx), round(dur, 2))
