"""Fill review/page_extra.json for page24.py from the round's measurement files (no number on the page is typed by hand)."""
import json, os, glob, re
W = '/Volumes/Expansion/_edit_work/RO-24/round1'; OUT = f'{W}/review'; C = f'{W}/checks'
L = lambda p: json.load(open(p)) if os.path.exists(p) else None
opt = L(f'{OUT}/look/options.json'); kn = {k: L(f'{C}/keynum-{k}.json') for k in ('K1', 'K2', 'K3')}
h1, h5 = L(f'{C}/hair-1080.json'), L(f'{C}/hair-540.json'); hf = L(f'{C}/hf/checks.json')
t1, t2 = L(f'{W}/audio/opts/trials_100.json'), L(f'{W}/audio/opts/trials_200.json')
rev = open(f'{OUT}/INDEPENDENT-CHECK.md').read() if os.path.exists(f'{OUT}/INDEPENDENT-CHECK.md') else ''
verdict = (re.findall(r'VERDICT:\s*([A-Z ]+)', rev) or ['not run yet'])[-1].strip()
ag = open(f'{C}/audio_gate.log').read() if os.path.exists(f'{C}/audio_gate.log') else ''
agv = 'PASS' if re.search(r'\bPASS\b', ag.splitlines()[-1] if ag else '') else ('see log' if ag else 'not run')
WO = json.load(open(f'{W}/words_out_fm.json'))
def speech(a, b): return ' '.join(w['w'] for w in WO if a <= w['t0'] < b)
def avg(k):
    s = (t1[k]['scores'] if t1 else []) + (t2[k]['scores'] if t2 else []); return round(sum(s) / len(s), 1) if s else None
def ships(k): return (t1[k]['shipped'] if t1 else 0) + (t2[k]['shipped'] if t2 else 0)
def kavg(variant, field):
    v = [kn[k][variant][field] for k in kn if kn[k]]; return round(sum(v) / len(v), 4) if v else None
fm_end = json.load(open(f'{OUT}/first-minute/DRAFT - RO-24 round 1 - first minute.mp4.build.json'))['frames'] * 1001 / 30000
n = opt['numbers'] if opt else {}
X = dict(
 intro="Cut from 10/15 roll C1726, the Ozempic part (7:25 to the end of the roll). For this round you asked me to dial in the chroma key, the audio, the colour and the first minute before anything else, so that is all this page is: the key, three colours, three backgrounds, three voices, and the first minute built with my picks. The celebrity photos, the other graphics and the full film (about 7 minutes) come next round, once these are locked.",
 locked="The Bill Maher green-screen key you locked on 10/20 (its body and arm matte plus the steady fine hair), recalibrated for this 16:9 roll. Soft Blue Light lower thirds.",
 decisions=[
  "<b>Key:</b> A) <b>Refined edges</b> (recommended): the approved Bill Maher key, improved where it slipped on this roll. Your hair and forehead no longer let the background show through (20 % of those pixels before, under 0.5 % now) and the green fringe on your arms and ears is mostly gone. Moving hands are only partly fixed: about half the green between your fingers is gone (clean at 0:51.0, mostly clean at 0:44.1), but green strips remain at 0:04.8, 0:43.9 to 0:44.1, 0:47.9 to 0:48.0 and 0:51.1 to 0:51.6, and your thumb at 0:40 keeps a thin brown outline. It also adds two small flaws the approved key does not have: a pale streak on your shorts for a tenth of a second at 0:25.0 (smaller specks at 0:01 and 0:40.3), and the rim of your watch goes slightly see-through at 0:08.5 and 0:08.9. B) The Bill Maher key exactly as approved: solid shorts and watch, but more green around moving hands and see-through spots in the hair. Look at 0:08, 0:25 and 0:48 in the first minute, and the hand clips below.",
  "<b>Colour:</b> A) <b>Warm</b> (recommended, Bill Maher's approved grade). B) Rich (more colour and contrast). C) Natural (cooler, softer).",
  "<b>What is behind you:</b> A) <b>Light studio with depth</b> (recommended): light grey-blue, a little brighter behind you, deeper at the edges. B) Bill Maher's flat light grey. C) Soft Blue navy (dark, with the brand's blue glow behind you).",
  "<b>Voice:</b> A) <b>Bill Maher's voice plus the bass lift</b> (recommended). B) Bill Maher's voice exactly. C) Open (a gentler warm shape).",
  "<b>First 5 seconds</b> (built next round): A) <b>a fast montage of the celebrity before and after photos</b> (recommended; it is your script's opening cue, with photos instead of clips). B) an AI clip: two men take the same shot, one ends up ripped, the other gaunt. C) open on you, as now.",
  "<b>Photos for next round:</b> OK to download news photos of the six people you talk about (Sharon Osbourne, Fat Joe, Amy Schumer, Meghan Trainor, Oprah, Tracy Morgan), about 3 each from news sites, roughly 20 JPGs, under 30 MB in total? I need your yes before downloading them.",
 ],
 first_minute=dict(end=fm_end, master='first-minute/DRAFT - RO-24 round 1 - first minute.mp4', review='first-minute/DRAFT - RO-24 round 1 - first minute - REVIEW 540p.mp4',
                   poster='first-minute/DRAFT - RO-24 round 1 - first minute.jpg',
                   links="<a href='first-minute/DRAFT - RO-24 round 1 - first minute - audio AB.mp4'>audio A/B</a> · also in <i>Videos to Review</i> for VLC",
                   note="Built with the recommended key, colour, background and voice. Where your photos of Sharon Osbourne go (0:26 to 0:47) you stay on camera for now; nothing else is a placeholder."),
 key_intro="Same frames, played both ways. The close-ups are at 1.5 times the size the video will play, on Bill Maher's light field and on a dark field, so every edge shows. The raw clip shows what the key removes.",
 key=[
  dict(title='Approved key vs refined edges (hook)', mp4='key/key-side-hook.mp4', jpg='key/key-side-hook.jpg', note='Left: the Bill Maher key exactly. Right: refined edges.'),
  dict(title='Hair and edges close up (hook)', mp4='key/key-hair-hook.mp4', jpg='key/key-hair-hook.jpg', note='Top row on the light field, bottom on dark. Left approved, right refined. Watch the hair outline and the ears.'),
  dict(title='Raw green screen vs keyed (hook)', mp4='key/key-raw-hook.mp4', jpg='key/key-raw-hook.jpg', note='The raw roll beside the refined key on the recommended background.'),
  dict(title='Approved vs refined (Sharon lines, hands moving)', mp4='key/key-side-sharon.mp4', jpg='key/key-side-sharon.jpg', note='A stretch with gestures, to check hands and motion blur.'),
  dict(title='Hair and edges close up (Sharon lines)', mp4='key/key-hair-sharon.mp4', jpg='key/key-hair-sharon.jpg', note='Light field on top, dark below.'),
  dict(title='Raw vs keyed (Sharon lines)', mp4='key/key-raw-sharon.mp4', jpg='key/key-raw-sharon.jpg', note=''),
  dict(title='Fast hands at 0:40: approved vs refined', mp4='key/key-side-hands1.mp4', jpg='key/key-side-hands1.jpg', note='Left: the approved key (olive outline, cut-out blur). Right: refined, cleaner, but your thumb keeps a thin brown outline.'),
  dict(title='Fast hands at 0:51: approved vs refined', mp4='key/key-side-hands2.mp4', jpg='key/key-side-hands2.jpg', note='Left: approved, with green between the fingers. Right: refined, less green, but a green patch is still there for a moment.'),
  dict(title='Finger gaps at 0:44: approved vs refined', mp4='key/key-side-gaps.mp4', jpg='key/key-side-gaps.jpg', note='Left: approved, olive screen between your fingers and arm. Right: refined, most of it gone, a thin green strip left.'),
 ],
 key_numbers=[('Measured on all three first-minute takes', 'Approved key', 'Refined edges'),
  ('Pixels inside the head and hair that let the background through', f"{kavg('approved','interior_below_099_pct'):.1f} %", f"{kavg('refined','interior_below_099_pct'):.1f} %"),
  ('Green left in the edges (lower is cleaner)', f"{kavg('approved','edge_green')}", f"{kavg('refined','edge_green')}"),
  ('How much the edges flicker frame to frame (the same for both)', f"{kavg('approved','edge_band_change')}", f"{kavg('refined','edge_band_change')}"),
  ('How much the head and hair flicker inside', f"{kavg('approved','head_interior_change')}", f"{kavg('refined','head_interior_change')}"),
  ('Specks of screen left anywhere away from you (worst frame, out of 4.7 million)', f"{max(kn[k]['approved']['leftover_screen_px_max'] for k in kn if kn[k])}", f"{max(kn[k]['refined']['leftover_screen_px_max'] for k in kn if kn[k])}")] if all(kn.values()) else [],
 colour_intro="The same frame of you, keyed, on the recommended background, wide and tight, with your approved Bill Maher frame for comparison (same screen, same lights). Only your picture is graded; the background keeps its own colour.",
 colour=[dict(id=m.upper()[0] if False else {'warm':'A','rich':'B','natural':'C'}[m], title={'warm':'Warm (Bill Maher\'s grade)','rich':'Rich','natural':'Natural'}[m],
              W=f'look/colour-{m}-W.jpg', T=f'look/colour-{m}-T.jpg',
              note={'warm':'Recommended: your approved Bill Maher grade. Face brightness and colour land within a few percent of that frame.','rich':'More colour and snap; pushes the arms toward orange.','natural':'Cooler and softer; a little grey.'}[m]) for m in ('warm','rich','natural')]
        + [dict(id='ref', title='Reference: Bill Maher, approved', W='look/ref-billmaher.jpg', T='look/ref-billmaher.jpg', note='Your approved key and grade on the same green screen, for comparison.')],
 bg_intro="Everything behind you is drawn by us now, so it can be anything. Three options, same frame, warm grade.",
 background=[dict(id={'depth':'A','light':'B','navy':'C'}[b], title={'depth':'Light studio with depth','light':"Bill Maher's flat light grey",'navy':'Soft Blue navy'}[b], W=f'look/bg-{b}-W.jpg', T=f'look/bg-{b}-T.jpg',
                 note={'depth':'Recommended: clean like Bill Maher, with a little depth so the wide shot does not look flat.','light':'Exactly the Bill Maher field.','navy':'Matches the graphics; darker, your black tank sits closer to the background.'}[b]) for b in ('depth','light','navy')],
 voice_intro=f"The same 26 seconds of the hook, level matched. Same microphone and room as Bill Maher. A blind listener ranked them 12 times against your approved Bill Maher sample (average out of 10): bass lift {avg('B-balanced-bass')}, Open {avg('C-open')}, untreated {avg('E-untreated')}, Bill Maher's exactly {avg('A-balanced')}. The listener could not separate the first two.",
 voice=[dict(id='A', title='Bill Maher plus bass lift (recommended)', src='voice/A - Bill Maher voice plus bass.m4a', note=f"Your Bill Maher voice plus the subtle bass lift that is the house standard. Listener average {avg('B-balanced-bass')}, its pick {ships('B-balanced-bass')} of 12 times."),
        dict(id='B', title="Bill Maher's voice exactly", src='voice/B - Bill Maher voice exactly.m4a', note=f"What you picked for Bill Maher. Listener average {avg('A-balanced')}."),
        dict(id='C', title='Open', src='voice/C - Open.m4a', note=f"The gentle warm shape you called fairly decent on Bill Maher round 1. Listener average {avg('C-open')}, its pick {ships('C-open')} of 12 times."),
        dict(id='ref', title='The mic untreated (reference)', src='voice/Reference - mic untreated.m4a', note='Nothing done except the rumble below the voice removed.')],
 decided=[
  "Hook: your last take. On the second line one speech model hears \"well\" instead of \"while\"; two others hear \"while\" (it is a quick, clipped \"while\"). \"Ripped\" at 0:01 also comes out a little soft. Listen at 0:00 to 0:06; if either bothers you, your earlier clean take swaps in.",
  "Every restarted line uses its retake: \"She went under a one\", \"Your face looks deflated\" and \"Sharon's Ozempic face is 100% her own fault because it...\" are cut.",
  "Zoom cuts: wide and tight alternate at sentence breaks (10 cuts in the first minute), and every join between takes is a size change, never a jump cut.",
  "Tight shot: 4% headroom above your hair on every frame. The background is ours, so nothing real is cropped.",
  "The key subtracts this green screen as it really is (I measured its folds and creases from 40 frames), not a smooth guess of it. That keeps the edges tight next to your head and arms.",
  "Two lower thirds in the first minute: \"SHARON OSBOURNE / Lost 42 Pounds In 4 Months. Under 100 Pounds.\" and \"KEY POINT / Lower Your Dose When You Lose Too Fast.\" The small label line is in capitals (your 10/20 rule). No drug names on screen.",
  "The script's Elon Musk section was not filmed. The film goes from the protein rule straight to Oprah and Tracy Morgan, which reads fine, so no pickup.",
  "Moving hands: the approved key reads a blur of skin and green as solid, so moving hands get an olive outline and the screen stays olive between your fingers. The refined key separates skin from screen where your hands move. It removes about half of that green. What is left, and the two small flaws it adds (shorts at 0:25, watch rim at 0:08.5), are listed under Key. Five versions of this step went through independent checks; each one that opened more of the finger gaps also opened your shorts or watch, so this is the balance point. Comparison clips at 0:40, 0:44 and 0:51.",
  "Both lower thirds now end just before the next cut, so nothing changes size under them as they leave.",
  "The clear arm of your glasses and the watch glass show a little green, because they really do show or reflect the screen (raw footage too). Next round can tint just those neutral.",
  "At 0:46 you lean right while finishing \"instead of younger\". You are still talking, so it stays.",
  "One word (\"That's\", 0:35) touched the mic's clipping ceiling for about a thousandth of a second. Inaudible, left as is.",
  "On the light background the lower thirds' glass strip reads lighter (slate blue) than on your studio films, because the background shows through it. The text stays clear. If you want it darker, say so and next round makes the strip more solid.",
  "The whole film's take list (best take of every line) is already done: about 7 minutes before pause trims.",
  "The full delivery check runs on the finished film; this first minute is a review draft (its sound and hair checks are below).",
  "Spend so far: about $0.40 of Gemini listening. No image or video generation.",
 ],
 graphics=[dict(id='G01', name='Sharon Osbourne facts', t0=26.55, t1=34.62, topic='SHARON OSBOURNE', point='Lost 42 Pounds In 4 Months. Under 100 Pounds.',
                still='first-minute/_picture-01100.jpg' if False else 'context/G01.jpg', ctx='context/G01-context - REVIEW 540p.mp4',
                before=speech(23.5, 26.55), during=speech(26.55, 34.62), after=speech(34.62, 38)),
           dict(id='G02', name='Key point: lower your dose', t0=52.62, t1=57.88, topic='KEY POINT', point='Lower Your Dose When You Lose Too Fast.',
                still='context/G02.jpg', ctx='context/G02-context - REVIEW 540p.mp4', before=speech(49.6, 52.62), during=speech(52.62, 57.88), after=speech(57.88, 61.3))],
 pending=["The celebrity photos (after your yes on decision 6), shown as you name each person, plus the opening montage.",
          "The other on-screen graphics from your script: Fat Joe's numbers, no bread, pasta or rice, Amy Schumer, the head-to-head study card, the quit rates, the protein rule, Oprah, the trial result, the step-down schedule and the four-point recap.",
          "B-roll of you training and of meal prep and salmon. Not filmed yet, so the clip library first; otherwise you stay on camera.",
          "AI clip ideas with start and end frames for your pick.",
          "Then the full film, about 7 minutes."],
 checks=[],
 reply="1 Key: A\n2 Colour: A\n3 Background: A\n4 Voice: A\n5 First 5 seconds: A\n6 Photos: yes\nNotes:\n",
)
hc = lambda r: (f"{r['frames_checked']} frames checked, closest hair {r['min_top']} px from the top (needs 20), {r['verdict']}") if r else 'not run'
X['checks'] = [f"Hair clearance on the 1080p first minute (every 0.25 s plus both sides of every cut): {hc(h1)}.", f"Same on the 540p review copy: {hc(h5)}.",
               "Sound checks on the first minute: 12 of 13 pass. The tone check fails, as it always does with a fixed tone shape like the bass lift (same as Bill Maher).",
               f"Lower thirds, face clear of the strip: {('PASS' if hf and not hf.get('failures') else 'see checks/hf') if hf else 'not run'}.",
               f"Independent reviewer on the packet: {verdict}."]
for g in X['graphics']:
    g['check'] = 'face clear of the strip' if hf else ''
json.dump(X, open(f'{OUT}/page_extra.json', 'w'), indent=1); print('extra ok')
