"""RO-24 round 3 review page (PRE-RENDER-APPROVAL "The review page"): what is locked, Dan's decisions, the first 2:50 on the
new background template, every background type in context, the six interview clips, the photo scenes, the pairs for the rest
of the film, the open round 2 choices, What I decided, checks, one reply box. One shared player docked at the right.
    python3 page_r3.py"""
import json, html, os, re, glob, pathlib, sys
R3 = '/Volumes/Expansion/_edit_work/RO-24/round3'; OUT = f'{R3}/review'; C = f'{R3}/checks'
sys.path.insert(0, f'{R3}/recipe'); import timeline_r3 as TL
E = html.escape; L = lambda p: json.load(open(p)) if os.path.exists(p) else None
def mmss(t): return f'{int(t // 60)}:{t % 60:04.1f}'
def btn(src, label): return f"""<button onclick="play('{src}','{E(label)}')">Play: {E(label)}</button>"""
ctx = {c['id']: c for c in L(f'{OUT}/context/index.json') or []}
plan = {s['id']: s for s in L(f'{R3}/bg_plan.json')['segments']}
ins = L(f'{R3}/clips/inserts.json'); man = {m['id']: m for m in L(f'{R3}/film_manifest_r3.json')}
pp = {p['id']: p for p in L(f'{R3}/hf/plan_photos_r3.json')}
W = L(f'{R3}/film_words_r3.json')
FIXW = [(r' ([.,%?!])', r'\1'), (r'(\d) \.(\d)', r'\1.\2'), (r'GLP -1', 'GLP-1'), (r'six -pack', 'six-pack'), (r'head -to -head', 'head-to-head'),
        (r"old zempic", 'Ozempic'), (r'\bozempic\b', 'Ozempic'), (r'Ozenpik', 'Ozempic'), (r'Monjaro', 'Mounjaro'), (r'[Zz]ebbound|zetbound', 'Zepbound'),
        (r'get this gone', 'get this gaunt'), (r'over fat', 'overfat'), (r'2\.5mg', '2.5 mg'), (r'1\.5mg', '1.5 mg'), (r'0 \.8', '0.8'), (r'sixpackabs \.com', 'SixPackAbs.com')]
def said(a, b):
    s = ' '.join(w['w'] for w in W if a <= w['t0'] < b)
    for x, y in FIXW: s = re.sub(x, y, s)
    return s
NAMES = {'soft': '1. Their clip softened behind you', 'corner': '2. Their clip full screen, you in the corner', 'side': '2b. Their clip behind, you to the side',
         'wall': '3. The scrolling photo wall', 'panel': '4. Side panel: before and after, weight and medication', 'cards': '6. Floating photo cards',
         'bigtype': '7. The number and the drug, big and faint', 'set': '8. The studio set, their clip on the TV'}
def what(s):
    if s['type'] in ('corner', 'side', 'soft', 'set') and s.get('clip'): return f"{s.get('person') or ''}'s clip ({pathlib.Path(s['clip']['src']).stem.split('_')[0]}), muted"
    if s['type'] == 'panel': return f"{s['name']}: {s['pair']['years'][0]} / {s['pair']['years'][1]}, {s['stat']}"
    if s['type'] == 'bigtype': return ' / '.join(s['lines'])
    if s['type'] in ('cards', 'wall'): return f"{len(s['photos'])} photos" + (f" of {s['person']}" if s.get('person') and s['type'] == 'cards' and s['id'] != 'BG01' else ' of all six people')
    return ''
def bg_card(i):
    s = plan[i]; c = ctx.get(i)
    return f"""<article><h3>{E(NAMES[s['type']])} <span class="tag">{i}</span> <span class="small">{mmss(s['t0'])} to {mmss(s['t1'])}</span></h3>
<a href="{c['jpg']}"><img loading="lazy" src="{c['jpg']}"></a>{btn(c['mp4'], f'{i} in context ({mmss(c["ctx_a"])} to {mmss(c["ctx_b"])})')}
<div class="copy"><b>Behind you:</b> {E(what(s))}<br><b>Why:</b> {E(s['why'])}<br><span class="small">"{E(said(s['t0'], s['t1']))}"</span></div></article>"""
bgs = [i for i in sorted(plan, key=lambda k: plan[k]['t0']) if i in ctx]
types_shown = {plan[i]['type'] for i in bgs}
CLIPS = {'sharon': ('Sharon Osbourne', 'after "Let\'s start with one who shows you exactly what not to do."', 'Sharon Osbourne lost 42 pounds in about four months.'),
         'fatjoe': ('Fat Joe', 'after "Now, let\'s look at a guy who did it the right way."', 'Fat Joe was close to 480 pounds at his heaviest.'),
         'amy': ('Amy Schumer', 'after "Next up is Amy Schumer."', 'Amy Schumer lost about 30 pounds fast on Ozempic.'),
         'meghan': ('Meghan Trainor', 'after "Now here\'s someone who got it right."', 'Meghan Trainor took Mounjaro...'),
         'oprah': ('Oprah Winfrey', 'after "They both stopped and the weight came back."', 'Oprah stopped for about a year.'),
         'tracy': ('Tracy Morgan', 'after "Now she calls weight loss medication a lifetime thing."', 'And Tracy Morgan said it on The Tonight Show...')}
nm = json.load(open(f'{R3}/timemap.json'))['new_at']
def clip_card(n):
    I = ins[n]; c = ctx.get(f'clip-{n}'); person, before, after = CLIPS[n]; t = nm[n] * 1001 / 30000
    inctx = ctx.get(f'C_{n}')
    extra = btn(inctx['mp4'], f'{person} clip in context') if inctx else '<span class="small">In context in round 4 (after the first 3 minutes).</span>'
    return f"""<article><h3>{E(person)}: {E(I['source'])} <span class="small">{mmss(t)}, {I['dur']:.1f} s</span></h3>
<a href="{c['jpg']}"><img loading="lazy" src="{c['jpg']}"></a>{btn(c['mp4'], f'{person} clip on its own')} {extra}
<div class="copy"><b>Plays</b> {E(before)} Then you: "{E(after)}"<br><b>Says:</b> {E(I['says'])}<br><span class="small">Source: <a href="{I['youtube']}">{E(I['youtube'])}</a> (file {I['a']:.2f} to {I['b']:.2f} s). Loudness matched to your voice; picture as broadcast.</span></div></article>"""
PNAMES = {'P0': 'Opening montage: all six, with weight and medication', 'P1': 'Sharon Osbourne before and after', 'P2': 'Sharon Osbourne, "Ozempic face"', 'P3': 'Fat Joe before and after'}
def ph_card(i):
    c = ctx[i]; p = pp[i]
    shots = '; '.join(f"{s['name']} {'/'.join(s.get('years', []))} · {s['stat']}" for s in p['shots'])
    still = f'stills/{i}.jpg' if os.path.exists(f'{OUT}/stills/{i}.jpg') else c['jpg']
    return f"""<article><h3>{E(PNAMES[i])} <span class="tag">{i}</span> <span class="small">{mmss(c['a'])} to {mmss(c['b'])}</span></h3>
<a href="{still}"><img loading="lazy" src="{still}"></a>{btn(c['mp4'], f'{i} in context')}<div class="copy">{E(shots)}</div></article>"""
pairs = [c for c in ctx.values() if c['kind'] == 'pair']
ideas = L(f'{R3.replace("round3", "round2")}/ai_ideas.json') or []
for x in ideas: x['t3'] = TL.shift_t(x['film_t'])
b2 = man.get('B2'); b2t = b2['a'] if b2 else 0
hair = L(f'{C}/hair.json'); ag = L(f'{OUT}/preview/DRAFT - RO-24 round 3 - first 2m50s.mp4.audio_gate.json')
rev = sorted(glob.glob(f'{OUT}/INDEPENDENT-R3*.md'), key=os.path.getmtime); verdict = 'not run yet'
if rev:
    v = re.findall(r'VERDICT:\s*([A-Z ]+)', open(rev[-1]).read()); verdict = v[-1].strip() if v else verdict
decisions = [
 '<b>The background template</b> (the main one): lock it for every green-screen reaction video, or name what to change. All eight looks you approved are in the first 2:50, each card below plays it in context, and the rules that pick them are under "What I decided".',
 '<b>The interview clips</b> play full screen with their own sound where your script said [PLAY CLIP], then keep rolling silently behind you. OK, or shorten any (each card shows its exact words).',
 f'<b>Tracy Morgan</b> was not in the script: his Tonight Show moment ("I out-ate Ozempic. I gained 40 pounds", 13 s) plays right before your Tracy line at {mmss(nm["tracy"] * 1001 / 30000)}. Keep it there, or drop it (your line already quotes him).',
 f'<b>B-roll at {mmss(b2t)}</b> ("I\'m lifting significantly more weight now", open since round 2): A) the AI clip of you doing dumbbell bench presses, labelled AI-generated (in the film now), or B) stay on camera.',
 '<b>AI clips</b> (open since round 2): pick the ideas you want (up to about 5), or none. I make start and end frames next round for your yes before any motion.']
decided = [
 'The template is now a shared tool for every green-screen video (Claude and Codex): the eight looks, where you stand in each, and the rules that choose them.',
 'Rules: the background only changes on a camera cut, about every 8 to 20 seconds; never the same look twice in a row; right after the intro, the floating cards then the photo wall; right after a clip plays, it keeps rolling with you in the corner; a number you say gets the big type, unless a lower third already shows it; when you talk about someone\'s body changing, their before and after; otherwise the studio set or their clip softened, with "you to the side" now and then.',
 'Where you stand: centre for the softened clip, wall and cards; right of centre for the panel, big type, set and clip-behind; lower right for the corner (bigger than in the Shorts, as you asked). Every cut still changes between wide and tight, so no jump cuts.',
 'Behind you, only steady, clean footage of each person: I downloaded the full E! News and Page Six videos and used stretches with no quote boxes, product shots, transitions or flashing cameras (each one checked frame by frame).',
 'Studio set: you a touch dimmer, with a blue edge light from the set\'s blue lamps on one side and a warm one from its floor lamp on the other; the set slightly soft as if behind you; one set for the whole film. The set is an AI-made picture, so it carries the AI-GENERATED label while it is on screen (house rule; your mockup had none, say if you want it off).',
 'Corner layout: lower right, as in your approved mockup (the lower-left corner of the locked reaction Shorts format is for Shorts with your filmed reaction; this film has none). Wide and tight corner shots differ by the same step as your normal wide and tight shots, so a cut there is never a jump cut. The lower thirds stay where you approved them, so they pass over your chest in that layout; your face always stays clear of them.',
 'Clips are trimmed to your script\'s first and last words, cut on quiet moments, loudness matched to your voice. The film is now 8:38 (6:53 plus 1:45 of clips).',
 'Photo scenes: every person now shows their weight and medication in your approved wording, as before and after pairs where they lost weight; the opening montage now includes Tracy Morgan. Sharon\'s before and after appears in the intro, before her clip, in "Ozempic face", in the panel and in the floating cards, never the same pair twice.',
 'I found 15 more photos (credits on screen where a credit line shows; uncredited agency photos only in the walls, cards and the TV). Big type, cards and walls carry no credit line.',
 'The step-down card fix and the end screen capitals (from the round 2 re-check) move to round 4: both sit after the first 3 minutes and their backgrounds change with the template.',
 'Spend so far: $0 (all images and renders on the subscription and this Mac).']
checks = []
if hair: checks.append(f"Hair clearance: {hair['frames_checked']} rendered frames with you on screen, closest hair {hair['min_top']} px from the top (needs 20): {hair['verdict']}.")
if ag:
    rr = ag.get('rows', []); bad = [r['key'] for r in rr if not r.get('ok')]
    checks.append(f"Audio gate on the 2:50: {len(rr) - len(bad)} of {len(rr)} rows pass" + (f"; fails: {', '.join(bad)} (the gate measures your voice; the two interview clips with their music beds sit inside this file)" if bad else '') + '.')
checks.append('Independent review, first build: 6 problems to fix first (a background that strobed with camera flashes, a split-second source wipe behind you, one jump cut in the corner layout, two rough sound joins at the Sharon clip, a photo credit hidden by your shoulder). All six fixed, plus its notes on repeated photos, the big number\'s timing and the studio TV.')
checks.append(f'Independent reviewer on this build: {verdict}.')
reply = "1 Background template: lock / change: \n2 Clips: OK / change: \n3 Tracy clip: keep / drop\n4 B-roll bench press: A / B\n5 AI clips: \n6 Anything else: "
pv = 'preview/DRAFT - RO-24 round 3 - first 2m50s'
page = f"""<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Celebrity Ozempic, round 3</title>
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
@media(max-width:900px){{.grid{{grid-template-columns:1fr}}h1{{font-size:28px}}}}</style>
<div id="dock"><div class="small" id="nowp">Pick any background, clip or photo below to play it here.</div><video id="pv" controls preload="none" playsinline></video></div>
<main><h1>Reacting To Celebrity Ozempic Transformations <span class="small">LFC, round 3</span></h1>
<p>Round 3 builds the background template you asked for and puts it on the first 2:50: the intro, Sharon Osbourne with her E! News clip, into Fat Joe with his Page Six clip. Every one of the {len(types_shown)} looks you approved appears in it. The complete film comes in round 4, once you lock the template.</p>
<p class="notice"><b>Next:</b> round 4 builds the whole film on the template once you lock it. Under today's rule (Codex now has the green-screen jobs) round 4 goes to Codex, which starts from this template and this page.</p>
<p class="notice"><b>Locked, reused as is:</b> your approved key on every frame (nothing was re-keyed), warm colour, voice A, the cut and take list, and all 14 graphics.</p>
<nav><a href="#decide">Your {len(decisions)} decisions</a><a href="#preview">First 2:50</a><a href="#types">The backgrounds</a><a href="#clips">Interview clips</a><a href="#photos">Photo scenes</a><a href="#pairs">Pairs for later</a><a href="#ai">AI clip ideas</a><a href="#decided">What I decided</a><a href="#checks">Checks</a><a href="#reply">Reply</a></nav>
<section id="decide"><h2>Your decisions ({len(decisions)})</h2><ol>{''.join('<li>' + d + '</li>' for d in decisions)}</ol></section>
<section id="preview"><h2>The first 2:50 (0:00 to 2:50.5)</h2><video controls preload="none" playsinline poster="{pv}.jpg" src="{pv} - REVIEW 540p.mp4"></video>
<p class="small">The player shows the 540p copy; <a href="{pv}.mp4">the 1080p file</a>. VLC copy: <i>Celebrity Ozempic LFC R3 - first 2m50s</i> (MP4) in your Videos to Review folder.</p></section>
<section id="types"><h2>The backgrounds, in order ({len(bgs)} changes in 2:50)</h2><p class="small">Each plays its stretch with 3 seconds either side. The numbers are your numbers from the mockup sheets; 5 (the built TV wall) is out, as you said.</p><div class="grid">{''.join(bg_card(i) for i in bgs)}</div></section>
<section id="clips"><h2>The interview clips (6)</h2><div class="grid">{''.join(clip_card(n) for n in ('sharon', 'fatjoe', 'amy', 'meghan', 'oprah', 'tracy'))}</div></section>
<section id="photos"><h2>Photo scenes in the first 2:50 (4)</h2><div class="grid">{''.join(ph_card(i) for i in ('P0', 'P1', 'P2', 'P3'))}</div></section>
<section id="pairs"><h2>Before and after pairs for the rest of the film ({len(pairs)})</h2><p class="small">For the side panels in round 4. Credits under each.</p><div class="grid">{''.join(f'<article><a href="{c["jpg"]}"><img loading="lazy" src="{c["jpg"]}"></a><div class="copy">{E(", ".join(c.get("credits") or []))}</div></article>' for c in pairs)}</div></section>
<section id="ai"><h2>AI clip ideas ({len(ideas)}), open since round 2</h2><ol>{''.join(f'<li><b>{E(x["id"])}</b> at {mmss(x["t3"])}, {E(x["where"])}: {E(x["idea"])}</li>' for x in ideas)}</ol></section>
<section id="decided"><h2>What I decided (overrule anything)</h2><ul>{''.join('<li>' + E(d) + '</li>' for d in decided)}</ul></section>
<section id="checks"><h2>Checks</h2><ul>{''.join('<li>' + E(d) + '</li>' for d in checks)}</ul></section>
<section id="reply"><h2>One reply</h2><textarea id="r">{E(reply)}</textarea><p><button onclick="navigator.clipboard.writeText(document.getElementById('r').value)">Copy reply</button></p></section></main>
<script>function play(src,id){{const v=document.getElementById('pv');v.src=src;document.getElementById('nowp').textContent=id;v.play();if(window.innerWidth<1500)document.getElementById('dock').scrollIntoView({{behavior:'smooth'}});}}</script></html>"""
assert '—' not in page, 'em dash on the page'
open(f'{OUT}/index.html', 'w').write(page); print('page ok', len(bgs), 'backgrounds', len(types_shown), 'types')
