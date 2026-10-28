"""RO-24 round 4 review page: the AI start/end frames first (only pairs that pass gate.py --verify: frame gate + independent
frame-reviewer), then the whole film on the locked background template once it exists, what changed since round 3 with
watch ranges, the four later clips and photo scenes in context, Tracy and B2 with timestamps, What I decided, checks, reply.
    python3 page_r4.py"""
import json, html, os, re, glob, shutil, subprocess, pathlib
R4 = '/Volumes/Expansion/_edit_work/RO-24/round4'; R3 = R4.replace('round4', 'round3'); OUT = f'{R4}/review'; C = f'{R4}/checks'
P = '/Users/danielrose/Projects/Claude/Projects/Abs By AI'; FC = f'{P}/.claude/skills/_shared/framecheck/gate.py'
E = html.escape; L = lambda p: json.load(open(p)) if os.path.exists(p) else None
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
def btn(src, label): return f"""<button onclick="play('{src}','{E(label)}')">Play: {E(label)}</button>"""
W = L(f'{R4}/film_words_r4.json')
FIXW = [(r' ([.,%?!])', r'\1'), (r'(\d) \.(\d)', r'\1.\2'), (r'GLP -1', 'GLP-1'), (r'head -to -head', 'head-to-head'), (r'\bozempic\b', 'Ozempic'),
        (r'Ozenpik', 'Ozempic'), (r'Monjaro', 'Mounjaro'), (r'[Zz]ebbound|zetbound', 'Zepbound'), (r'(\d)mg', r'\1 mg'), (r'0 \.8', '0.8'), (r'sixpackabs \.com', 'SixPackAbs.com')]
def said(a, b):
    s = ' '.join(w['w'] for w in W if a <= w['t0'] < b)
    for x, y in FIXW: s = re.sub(x, y, s)
    return s

# ---- AI frames: (id, folder, pairs [(start, end, label)], line time, line, idea, where it goes)
AI = [('A1', 'A1', [('s1_start.png', 's1_end.png', 'Shot 1'), ('s2_start.png', 's2_end.png', 'Shot 2, after a cut')], 0.0,
       'Do some people get ripped from taking weight loss medication? Well for other people, it totally destroys their life.',
       'Two men take the same shot at the same moment. Cut to months later: one ripped and calm, the other gaunt and grey at his reflection.',
       'Option B for the first 6 seconds, in place of the photo montage (which stays as option A). Two shots joined by a cut, because one take cannot jump months ahead.'),
      ('A3', 'A3', [('start.png', 'end.png', '')], 133.49, 'Stories like this are used to scare people out of taking Zepbound.',
       'A man reads a newspaper over breakfast, sees the front page and slowly lowers it, spooked.', 'Full screen for about 3 seconds, then back to the photo cards.'),
      ('A4', 'A4', [('start.png', 'end.png', '')], 181.03, 'He said he stays away from the bread, the pasta, and the rice.',
       'A waiter sets bread and pasta in front of a big man, who calmly slides both away and goes for his steak.', 'Full screen for the line; the Fat Joe lower third then comes on over you.'),
      ('A6', 'A6', [('start.png', 'end.png', '')], 409.67, 'I out ate Ozempic. I\'ve gained 40 pounds.',
       'A man at a buffet keeps stacking food until it is a wobbling tower, then reaches for one more roll.', 'Full screen for the line, out of the Tracy Morgan photo.'),
      ('A7', 'A7', [('start.png', 'end.png', '')], 461.87, 'Don\'t go from 5 mg to 0. Step down gradually, 1 mg per week.',
       'One man walks down a long staircase step by step; the other leaps off the top and lands in a heap.', 'Full screen for the line, then the "Step Down Slowly" list builds as now.'),
      ('A8', 'A8', [('start.png', 'end.png', '')], 469.95, 'and keep weighing yourself daily.',
       'A man steps on a bathroom scale first thing in the morning, glances down, nods.', 'About 2 seconds full screen, the list\'s second row lands as it ends.')]
def verified(d, s, e):
    r = subprocess.run(['python3', FC, f'{d}/{s}', f'{d}/{e}', '--verify'], capture_output=True, text=True, cwd=P)
    return r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1:] or ['']
ai_cards, ai_ready, ai_wait = [], [], []
for cid, fold, pairs, t, line, idea, where in AI:
    d = f'{R4}/ai/{fold}'; ok_all = True; imgs = ''
    for s, e, lab in pairs:
        ok, _ = verified(d, s, e); ok_all &= ok
        if ok:
            for f in (s, e):
                dst = f'{OUT}/ai/{cid}_{f.replace(".png", ".jpg")}'
                subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '88', f'{d}/{f}', '--out', dst], capture_output=True)
            imgs += (f'<p class="small">{E(lab)}</p>' if lab else '') + '<div class="pair">' + ''.join(
                f'<figure><a href="ai/{cid}_{f.replace(".png", ".jpg")}"><img src="ai/{cid}_{f.replace(".png", ".jpg")}"></a><figcaption>{k}</figcaption></figure>'
                for f, k in ((s, 'START'), (e, 'END'))) + '</div>'
    if ok_all:
        ai_ready.append(cid)
        ai_cards.append(f"""<article class="wide"><h3>{cid} <span class="small">at {mmss(t)}</span></h3>{imgs}<div class="copy"><b>Your line:</b> "{E(line)}"<br>
<b>The clip:</b> {E(idea)}<br><b>Where it goes:</b> {E(where)}<br><span class="small">Passed the frame check and a separate reviewer who saw only the pictures. Labelled AI-GENERATED on screen. Motion is made only after your yes (Google Flow subscription).</span></div></article>""")
    else:
        ai_wait.append(cid)

# ---- film (when built)
NAME = 'RO24_R4_MASTER'; FIN = f'{R4}/final'; film = os.path.exists(f'{OUT}/final/{NAME} - REVIEW 540p.mp4')   # copied into review/ by the delivery step
ctx = {c['id']: c for c in L(f'{OUT}/context/index.json') or []}
hair = L(f'{C}/hair.json'); hc = L(f'{C}/hair_corner.json'); ag = L(f'{FIN}/{NAME}.mp4.audio_gate.json')
rev = sorted(glob.glob(f'{OUT}/ROUND-4-REVIEW*.md'), key=os.path.getmtime); verdict = 'running' if film else 'after the film is built'
if rev:
    v = re.findall(r'VERDICT:\s*([A-Z ]+)', open(rev[-1]).read()); verdict = v[-1].strip() if v else verdict
man = {m['id']: m for m in L(f'{R4}/film_manifest_r4.json')}
CH = [('Amy Schumer photo pair', 'P4', 'Her 2024 and 2026 photos with "50 lb, Mounjaro" (round 2 showed one recent photo).'),
      ('Meghan Trainor photo pair', 'P5', 'Her 2019 and 2025 photos with "60 lb, Mounjaro". It now runs 2 s from "Now here\'s someone who got it right" (it had shrunk to under a second when her clip went in).'),
      ('Oprah photo pair', 'P6', 'Her 2022 and 2025 photos with "Down to 155 lb, GLP-1".'),
      ('Tracy Morgan photo', 'P7', 'Now follows his Tonight Show clip directly (a 0.7 s flash of you between them is gone), with "On Ozempic, gained 40 lb".'),
      ('Step Down Slowly list', 'G12', 'The last row now comes in on "if you keep losing", while you say it (it used to land 2 s late).'),
      ('End screen', 'G14', 'The small top lines are now in capitals; the buttons are placed clear of you on the new background.')]
def chg(lab, i, what):
    m = man[i]; c = ctx.get(i); a0, b0 = max(0, m['a'] - 4), m['b'] + 4
    return f"""<article><h3>{E(lab)} <span class="small">{mmss(m['a'])}</span></h3>{f'<a href="{c["jpg"]}"><img loading="lazy" src="{c["jpg"]}"></a>' + btn(c['mp4'], f'{lab}, {mmss(a0)} to {mmss(b0)}') if c else ''}
<div class="copy">{E(what)}<br><span class="small">Watch {mmss(a0)} to {mmss(b0)}.</span></div></article>"""
bgs = [c for c in ctx.values() if c['kind'] == 'bg']
NAMES = {'soft': 'Their clip softened behind you', 'corner': 'Their clip full screen, you in the corner', 'side': 'Their clip behind, you to the side',
         'wall': 'The photo wall', 'panel': 'Side panel: before and after', 'cards': 'Floating photo cards', 'bigtype': 'The number, big and faint', 'set': 'The studio set'}
plan = {s['id']: s for s in L(f'{R4}/bg_plan.json')['segments']}
def bg_card(c):
    s = plan[c['id']]
    return f"""<article><h3>{E(NAMES[s['type']])} <span class="small">{mmss(s['t0'])}</span></h3><a href="{c['jpg']}"><img loading="lazy" src="{c['jpg']}"></a>
{btn(c['mp4'], f"{c['id']} in context")}<div class="copy"><b>Why:</b> {E(s['why'].replace(" (editor's override)", ''))}<br><span class="small">"{E(said(s['t0'], s['t1'])[:220])}"</span></div></article>"""
tracy = man['C_tracy']; b2 = man['B2']
decisions = [f'<b>AI clip frames</b> ({len(ai_ready)} of 6 ready{", " + ", ".join(ai_wait) + " still in checking" if ai_wait else ""}): yes or no to each, and any change. Motion starts only after your yes.']
if film:
    decisions += [f'<b>The whole film</b> (8:38): approve, or give timestamped changes.',
                  f'<b>Tracy Morgan clip</b> at {mmss(tracy["a"])}: I kept it right before your line "And Tracy Morgan said it on The Tonight Show" (the clip plays first, then you quote him, the way the reaction videos open on the clip). Watch {mmss(tracy["a"] - 4)} to {mmss(tracy["b"] + 6)}. Keep, or move it after your line.',
                  f'<b>B-roll at {mmss(b2["a"])}</b>: the AI clip of you on the bench press (labelled AI-GENERATED) over "I\'m lifting significantly more weight now". Watch {mmss(b2["a"] - 4)} to {mmss(b2["b"] + 4)}. Keep, or stay on camera.']
decided = [
 'The locked background template now runs the whole film: 30 background changes, every one tied to what you are saying, each with its reason on its card. The first 2:50 is exactly the round 3 film you approved.',
 'Behind you in the later sections: only clean, steady stretches of each person\'s own interview (Amy on Howard Stern, Meghan on ET, Oprah, Tracy on The Tonight Show), downloaded in full HD, scanned frame by frame for flashes, with channel logos zoomed out of frame.',
 'My calls where the rules allowed two answers: "cut the carbs you overeat" keeps Fat Joe behind you (Amy is not introduced yet); "nearly everyone regains" gets the wall of all of them; your 1.5 mg dose gets the big number; the studio set\'s TV never repeats a photo pair the film just showed; the close sits on a calm background so the end-screen buttons stay clear of you.',
 'A fix in the shared template: the softened-clip background now honours the logo zoom (ET\'s yellow logo showed through the blur at 5:55).',
 'The AI clips are not in this film yet: their spots show you on camera. Once you approve frames, I make the motion on your Google Flow subscription, check every take, and cut them in.',
 'Spend this round: $0 (frames on the Codex subscription, everything else on this Mac).']
checks = []
if hair: checks.append(f"Hair clearance: {hair['frames_checked']} rendered frames of you, closest hair {hair['min_top']} px from the top (needs 20): {hair['verdict']}." + (f" Corner layout: closest {hc['min_top']} px, {hc['verdict']}." if hc else ''))
if ag:
    rr = ag.get('rows', []); bad = [r['key'] for r in rr if not r.get('ok')]
    checks.append(f"Audio gate on the whole film: {len(rr) - len(bad)} of {len(rr)} rows pass" + (f"; fails: {', '.join(bad)}. This is your approved voice A, unchanged since round 2: the tone row measures it against Muhammad's reference and has failed it every round; the interview clips carry their own music beds." if bad else '') + '.')
checks.append(f'AI frames: every pair shown passed the frame gate (body, props, background measured) and a fresh reviewer who saw only the pictures.')
checks.append(f'Independent review of the whole film: {verdict}.')
reply = '1 AI frames (yes / no / change, per clip):\n  A1:\n  A3:\n  A4:\n  A6:\n  A7:\n  A8:\n' + ('2 Whole film: approve / changes:\n3 Tracy clip: keep / move\n4 Bench press B-roll: keep / drop\n' if film else '') + '5 Anything else: '
filmsec = (f"""<section id="film"><h2>The whole film (8:38)</h2><video controls preload="none" playsinline poster="final/{NAME}.jpg" src="final/{NAME} - REVIEW 540p.mp4"></video>
<p class="small">540p in the player. Full-quality copy for VLC: <i>Celebrity Ozempic LFC R4 - full film</i> in your Videos to Review folder.</p></section>
<section id="changes"><h2>What changed since round 3, with watch ranges</h2><p class="small">0:00 to 2:50 is the approved round 3 film, unchanged. Everything after 2:50 is new on the template; the cards below are the items that changed from round 2's versions.</p><div class="grid">{''.join(chg(*x) for x in CH)}</div></section>
<section id="bgs"><h2>The backgrounds after 2:50 ({len(bgs)})</h2><div class="grid">{''.join(bg_card(c) for c in sorted(bgs, key=lambda c: c['a']))}</div></section>"""
           if film else '<section id="film"><h2>The whole film</h2><p class="notice">Rendering now. This page updates with the film, its changes and watch ranges as soon as it is built and checked.</p></section>')
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Celebrity Ozempic, round 4</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1240px;margin:0 auto;padding:28px 16px}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:calc(62vw)}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px}}p,li{{color:var(--mute)}}section{{margin:30px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}article.wide{{margin-bottom:16px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}figure{{margin:0}}figcaption{{font-size:13px;color:#9fb7cf}}
img,video{{width:100%;border-radius:10px;background:black}}a{{color:var(--acc)}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:15px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
textarea{{width:100%;box-sizing:border-box;min-height:240px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px}}#dock video{{max-height:60vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<div id="dock"><div class="small" id="nowp">Pick anything below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div>
<main><h1>Reacting To Celebrity Ozempic Transformations <span class="small">LFC, round 4</span></h1>
<p>Round 4 puts the whole film on the background template you locked, with all six interview clips and every before and after photo, and shows the start and end frames for the six AI clips you picked (A1, A3, A4, A6, A7, A8).</p>
<p class="notice"><b>Locked, reused as is:</b> the background template, your approved key, warm colour, voice A, the cut, graphics G01 to G14, the intro wording, photos P0 to P3 and the six clip trims.</p>
<nav><a href="#decide">Your decisions</a><a href="#ai">AI frames</a><a href="#film">Whole film</a>{'<a href="#changes">What changed</a><a href="#bgs">Backgrounds</a>' if film else ''}<a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(decisions)})</h2><ol>{''.join('<li>' + d + '</li>' for d in decisions)}</ol></section>
<section id="ai"><h2>AI clip frames: start and end ({len(ai_ready)} of 6)</h2>{''.join(ai_cards)}{f'<p class="small">Still being checked: {", ".join(ai_wait)}. They appear here once they pass.</p>' if ai_wait else ''}</section>
{filmsec}
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(d) + '</li>' for d in decided)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(d) + '</li>' for d in checks)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
assert '—' not in page, 'em dash on the page'
open(f'{OUT}/index.html', 'w').write(page); print('page ok: AI ready', ai_ready, 'waiting', ai_wait, 'film', film)
