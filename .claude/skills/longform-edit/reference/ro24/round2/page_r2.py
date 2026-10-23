"""RO-24 round 2 review page (PRE-RENDER-APPROVAL "The review page"): locks, Dan's decisions, the first minute, the key (round 1 vs
his approved Bill Maher R2 key, measured), every graphic, photo scene and B-roll insert in its moving context, the AI clip ideas,
What I decided, checks, one reply box. One shared player that floats at the right on a wide screen.   python3 page_r2.py"""
import json, html, os, glob, shutil
W = '/Volumes/Expansion/_edit_work/RO-24/round2'; OUT = f'{W}/review'; C = f'{W}/checks'
E = html.escape; L = lambda p: json.load(open(p)) if os.path.exists(p) else None
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
def btn(src, label): return f"""<button onclick="play('{src}','{E(label)}')">Play: {E(label)}</button>"""
os.makedirs(f'{OUT}/stills', exist_ok=True); os.makedirs(f'{OUT}/photos', exist_ok=True)
for f in glob.glob(f'{W}/hf/stills/*.jpg'): shutil.copy(f, f'{OUT}/stills/')
shutil.copy(f'{W}/photos/contact_sheet.jpg', f'{OUT}/photos/contact_sheet.jpg')
for f in ('b1_salmon_still.jpg', 'b2_still.jpg'): shutil.copy(f'{W}/broll/{f}', f'{OUT}/stills/{f}')
plan = {g['id']: g for g in (L(f'{W}/hf/plan_graphics.json') or []) + (L(f'{W}/hf/plan_photos.json') or [])}
ctx = {c['id']: c for c in (L(f'{OUT}/context/index.json') or [])}
man = {m['id']: m for m in L(f'{W}/film_manifest.json')}
photos = L(f'{W}/photos/photos.json') or []
def copy_of(g):
    """the graphic's own words, per template (independent review R2: placeholders and raw lists had leaked onto the page)"""
    if not g: return ''
    out = []
    if g.get('topic'): out.append(g['topic'])
    if g.get('eyebrow'): out.append(g['eyebrow'])
    t = g.get('title') or g.get('headline')
    if t: out.append(' '.join(t) if isinstance(t, list) else t)
    if g.get('point'): out.append(g['point'])
    if g.get('heading'): out.append(g['heading'] + ':')
    for r in g.get('rows') or []:
        out.append(f"{r['label']}: {r['text'].format(r['value'])}" if isinstance(r, dict) else str(r))
    if g.get('points'): out.append(' / '.join(x.replace('\n', ' ') for x in g['points']))
    if g.get('beat'): out.append(f"{g['beat']['lead']} {g['beat']['a']} Vs {g['beat']['b']}")
    for k in ('stopped', 'stayed'):
        if isinstance(g.get(k), dict): out.append(g[k]['label'])
    for bt in g.get('buttons') or []: out.append(bt['big'])
    if g.get('shots'): out.append('photos: ' + ', '.join(x.get('name', '') for x in g['shots']))
    if g.get('source'): out.append(g['source'])
    return ' · '.join(x for x in out if x)
NAMES = {'B1': 'B-roll: "I still train every day and eat my protein" (your real ab-wheel rollout, then the AI salmon dinner)',
         'B2': 'B-roll choice: "I\'m lifting significantly more weight now" (AI dumbbell bench press)'}
def card(i):
    m = man[i]; g = plan.get(i); c = ctx.get(i)
    name = NAMES.get(i) or (g or {}).get('name') or i
    still = f'stills/{i}.jpg' if os.path.exists(f'{OUT}/stills/{i}.jpg') else (c['jpg'] if c else '')
    if i == 'B1': still = 'stills/b1_salmon_still.jpg'
    if i == 'B2': still = 'stills/b2_still.jpg'
    play = btn(c['mp4'], f'{i} in context') if c else '<p class="small">In the first minute above.</p>'
    return f"""<article><h3>{E(name)} <span class="tag">{i}</span> <span class="small">{mmss(m['a'])} to {mmss(m['b'])}</span></h3>
<a href="{still}"><img loading="lazy" src="{still}"></a>{play}<div class="copy">{E(copy_of(g))}</div></article>"""
ids = sorted(man, key=lambda i: man[i]['a'])
gfx = [i for i in ids if i.startswith('G')]; pho = [i for i in ids if i.startswith('P')]; bro = [i for i in ids if i.startswith('B')]
ideas = L(f'{W}/ai_ideas.json') or []
km = {k: (L(f'{C}/keys/m_{k}.json') or {}).get('summary') for k in ('R01', 'R02', 'R03', 'R04a')}
kc = {k: (L(f'{C}/keys/mc_{k}.json') or {}).get('summary') for k in ('R01', 'R02', 'R03', 'R04a')}
def avg(d, f):
    v = [x[f] for x in d.values() if x and f in x]; return sum(v) / len(v) if v else None
rows = []
if all(kc.values()): rows.append(('Edge flicker with your movement taken out, vs the camera\'s own picture (below 1.0 = steadier than the camera)', f"{avg(kc, 'mc_ratio'):.2f}", 'Bill Maher sample: 0.69'))
if all(km.values()):
    rows.append(('Dark rim on skin edges', f"{100 * avg(km, 'rim_fraction'):.1f} %", 'round 1 key on the fast-hands test: 5.3 %'))
    rows.append(('Floating specks over the whole first minute (before the speck fix: 31)', str(sum(x['speck_total'] for x in km.values())), 'almost all single faint pixels; the worst stretch at 0:47 went from 25 to 8'))
    rows.append(('See-through pixels inside you, per frame (mostly the clear arm of your glasses past your head)', f"{sum(x['seethru_px_total'] for x in km.values()) / sum(x['frames'] for x in km.values()):.1f}", ''))
keys = [('compare-hook', 'The hook, 0:09 to 0:21', 'Hair and edges while you talk.'), ('compare-wide-0m10', 'Wide shot, 0:09.6 to 0:15 (2x on hands and shorts)', 'Your hands in front of your shorts, where round 1 left a pale streak.'),
        ('compare-hands-0m51', 'Fast hands, 0:47 to 0:53 (2x)', 'The finger gaps round 1 never fully fixed.'), ('compare-hands-0m58', 'Hands, 0:58 to 1:03 (2x)', 'The last wide shot of the first minute.')]
key_html = ''.join(f"""<article><h3>{E(t)}</h3><a href="key/{k}.jpg"><img loading="lazy" src="key/{k}.jpg"></a>{btn(f'key/{k}.mp4', t)}<p class="small">{E(n)}</p></article>"""
                   for k, t, n in keys if os.path.exists(f'{OUT}/key/{k}.mp4'))
fm = 'first-minute/DRAFT - RO-24 round 2 - first minute'
hair = [L(f'{C}/hair-1080.json'), L(f'{C}/hair-540.json')]; ag = L(f'{OUT}/{fm}.mp4.audio_gate.json')
rev = sorted(glob.glob(f'{OUT}/INDEPENDENT-*.md'), key=os.path.getmtime); verdict = 'not run yet'
if rev:
    import re; v = re.findall(r'VERDICT:\s*([A-Z ]+)', open(rev[-1]).read()); verdict = v[-1].strip() if v else verdict
decisions = [
 '<b>Graphics (14):</b> approve them all, or name the ones to change. Each one plays below in context with your voice.',
 '<b>Celebrity photos (8 scenes):</b> approve, or name changes. The first 5 seconds is now the photo montage (your script\'s opening cue); say "open on me" if you would rather start on camera.',
 '<b>B-roll at 4:15</b> ("I\'m lifting significantly more weight now"): A) the AI clip of you doing dumbbell bench presses, labelled AI-generated (in the film now), or B) stay on camera. No real gym footage of you exists yet.',
 '<b>AI clips:</b> pick the ideas you want (up to about 5, or none). I make the start and end frames next round for your yes before any motion.']
decided = [
 'Key: your approved Bill Maher Fat 90-Year-Old R2 key, same maths, calibrated to this roll (its own clean plate per stretch of the take, the watch search band, the frame size). One setting changed: how far inside the edge it takes the skin colour from (4 instead of 2), because you are smaller in this frame and your hands move fast: the dark rim on moving arms went from 8.0 % to 4.4 % (round 1\'s key: 5.3 %).',
 'One cleanup on top of the approved key, for this roll\'s fast hands: faint pink specks that floated just outside your arm and hand (worst at 0:47, about 25 in two thirds of a second) are removed by the approved method\'s own speck rule applied to the faint edge band. A few tiny, faint ones remain (8 across that take, each under 15 px); you would only see them paused.',
 'Colour warm, voice A (Bill Maher\'s voice plus the bass lift), background kept as the recommended light studio with depth.',
 'Whole film timeline: the best take of every line (round 1\'s list), two restarts cut ("But most of the headlines left..." and "They started with Ozempic, they..."), one 1.8 s pause after "too." shortened, round 1\'s checked hook cuts kept. 6:52 long.',
 'Every audio join is now a short crossfade, so the room sound runs straight through; each join measured at the cut instant. Fixed: a breath split at 3:52 (two takes joined back into one), the tail of "33." and of "mandatory", a mouth sound at 4:37, dead air before "If you can\'t do that".',
 'Under the two side cards (the protein rule, the step-down list) you move right and stay in one wide shot while the card is up.',
 f'{len(photos)} celebrity photos, sources in the photo list: {sum(1 for x in photos if x.get("licence"))} free-licence (Wikimedia Commons), {sum(1 for x in photos if not x.get("licence"))} agency photos from news coverage, each credited on screen. Tracy Morgan: no sharp Tonight Show still exists, so a 2023 red carpet photo.',
 'B-roll at 2:48: your real ab-wheel rollout, then the AI salmon dinner (labelled).',
 'The first minute ends after "overdosing.", like round 1.',
 'Your olive shorts read a little browner than the real colour: the approved key strips green spill from everything, and the shorts are greenish. Next round I can keep the shorts\' own colour if you want.',
 'The Fat Joe, His Rule and Amy Schumer lower thirds stay up across one camera cut each, because their second fact is said after the cut.',
 'The ab-wheel B-roll shows the roll-out only; the return does not fit in the line it covers.',
 'Polish queued for round 3 (from the independent re-check): the step-down card\'s last row comes in on "keep losing" so it stays up about 3 s instead of 0.8 s, and the end screen\'s two small top lines go to CAPITALS like every other eyebrow.']
checks = [f"Hair clearance ({lab}): {h['frames_checked']} frames where you are on screen, closest hair {h['min_top']} px from the top (needs 20), {h['verdict']}" for lab, h in zip(('1080p', '540p review copy'), hair) if h]
if ag:
    rr = ag.get('rows', []); bad = [r['key'] for r in rr if not r.get('ok')]
    checks.append(f"Audio gate on the first minute: {len(rr) - len(bad)} of {len(rr)} rows pass" + (f"; fails: {', '.join(bad)}" if bad else '') +
                  (' (tone compares against the house reference voice; voice A is Bill Maher\'s EQ plus the bass lift, so it differs by design, as in round 1)' if bad == ['tone'] else ''))
checks += ['Voice: -14.2 LUFS for the whole film (-14.4 for the first minute alone), -1.5 dBTP; every join level-checked at the cut (seam scan + per-join listen).',
           'Graphics: face clearance on tight and wide frames, side-card clearance 156 px (needs 60), motion through every graphic\'s whole time on screen.',
           f'Independent reviewer: {verdict}.']
pend = ['The AI clips you pick: start and end frames for your yes, then motion.', 'Then the complete film: delivery gate, watch pass, independent review, captions file.']
X = dict(decisions=decisions, decided=decided, checks=checks, pending=pend)
reply = "1 Graphics: all OK / change: \n2 Photos: OK / change: \n   First 5 seconds: montage / open on me\n3 B-roll at 4:15: A / B\n4 AI clips: \n5 Anything else: "
fmlink = f'{fm} - REVIEW 540p.mp4'
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Celebrity Ozempic, round 2</title>
<style>:root{{--bg:#071221;--panel:#101f32;--line:#29425b;--ink:#edf5ff;--mute:#bdd0e4;--acc:#8cd6ff}}
body{{margin:0;background:var(--bg);color:var(--ink);font:17px system-ui;line-height:1.55}}main{{max-width:1240px;margin:0 auto;padding:28px 16px}}
@media(min-width:1500px){{main{{margin:0 0 0 2vw;max-width:calc(62vw)}}#dock{{position:fixed;right:1.5vw;top:16px;width:33vw;z-index:9}}}}
h1{{font-size:36px;letter-spacing:-1px;margin:0 0 8px}}h2{{font-size:25px}}p,li{{color:var(--mute)}}section{{margin:30px 0;padding:22px;background:var(--panel);border:1px solid var(--line);border-radius:18px}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}article{{min-width:0;background:#081626;padding:14px;border-radius:14px}}
img,video{{width:100%;border-radius:10px;background:black}}a{{color:var(--acc)}}.tag{{color:#8ed7ff;font-size:13px;font-weight:700}}.small{{font-size:14px;color:#9fb7cf}}
.copy{{font-size:14px;margin-top:8px;color:#d7e6f5}}.notice{{border-left:4px solid #67c5ff;padding:10px 18px;background:#172e46}}
textarea{{width:100%;box-sizing:border-box;min-height:200px;background:var(--bg);color:white;padding:14px;font:16px system-ui;border:1px solid #47607b;border-radius:10px}}
#dock{{background:#0b1a2c;padding:10px;border-radius:12px;border:1px solid var(--line);margin-bottom:16px}}#dock video{{max-height:60vh}}
button{{background:#1b4b72;color:white;border:1px solid #66acd9;border-radius:9px;padding:8px 12px;cursor:pointer;font-size:14px;margin-top:8px}}nav{{display:flex;gap:14px;flex-wrap:wrap}}
table{{font-size:14px;color:#cfe0f0;border-collapse:collapse}}td{{padding:4px 12px 4px 0;vertical-align:top}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<div id="dock"><div class="small" id="nowp">Pick any comparison, graphic, photo or B-roll below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div>
<main><h1>Reacting To Celebrity Ozempic Transformations <span class="small">LFC, round 2</span></h1>
<p>Round 2 is your approved Bill Maher key on this video, warm colour and voice A on the whole film, plus every graphic, celebrity photo and B-roll moment so far, each playing in place with your voice. The AI clips come next round from the ideas you pick here, then the complete film.</p>
<p class="notice"><b>Locked, reused as is:</b> your Bill Maher Fat 90-Year-Old R2 key (the house standard since 10/21), warm colour, voice A, the depth background, round 1's take list and hook cuts.</p>
<nav><a href="#decide">Your {len(decisions)} decisions</a><a href="#minute">First minute</a><a href="#key">Chroma key</a><a href="#gfx">Graphics</a><a href="#photos">Photos</a><a href="#broll">B-roll</a><a href="#ai">AI clip ideas</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(decisions)})</h2><ol>{''.join('<li>' + d + '</li>' for d in decisions)}</ol></section>
<section id="minute"><h2>The first minute (0:00 to 1:02.9)</h2><video controls preload="none" playsinline poster="{fm}.jpg" src="{fmlink}"></video>
<p class="small">The player shows the 540p review copy; <a href="{fm}.mp4">the 1080p file</a>. VLC copy: <i>Celebrity Ozempic LFC R2 - first minute</i> (MP4) in your Videos to Review folder. It opens on the photo montage, then Sharon Osbourne's photo, her lower third over you, and the "Ozempic face" freeze on her face.</p></section>
<section id="key"><h2>The chroma key: round 1 vs your approved key</h2><p class="small">Same compositor, colour and background on both sides; only the key differs.</p><div class="grid">{key_html}</div>
<table>{''.join(f'<tr><td>{E(a)}</td><td><b>{E(b)}</b></td><td class="small">{E(c)}</td></tr>' for a, b, c in rows)}</table></section>
<section id="gfx"><h2>Graphics ({len(gfx)}), each in context</h2><div class="grid">{''.join(card(i) for i in gfx)}</div></section>
<section id="photos"><h2>Celebrity photo scenes ({len(pho)})</h2><p class="small">All 20 photos with sources: <a href="photos/contact_sheet.jpg">contact sheet</a>.</p><div class="grid">{''.join(card(i) for i in pho)}</div></section>
<section id="broll"><h2>B-roll ({len(bro)})</h2><div class="grid">{''.join(card(i) for i in bro)}</div></section>
<section id="ai"><h2>AI clip ideas ({len(ideas)}): pick the ones you want</h2><ol>{''.join(f'<li><b>{E(x["id"])}</b> at {mmss(x["film_t"])}, {E(x["where"])}: {E(x["idea"])}</li>' for x in ideas)}</ol></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(d) + '</li>' for d in decided)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(d) + '</li>' for d in checks)}</ul><p class="small">Next: {E(' '.join(pend))}</p></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
open(f'{OUT}/index.html', 'w').write(page); print('page ok', len(gfx), len(pho), len(bro), 'ctx', len(ctx))
