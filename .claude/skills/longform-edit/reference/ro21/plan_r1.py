"""RO-21 round 1 plan: every full-screen insert and every graphic over Dan, anchored to the words he says (film_words.json).
Writes round1/plan_r1.json (resolved film seconds). Phrases resolve to the first matching word at or after a given film time.
Kinds: ladder (custom HyperFrames, opaque), fact (before-card: AI level picture left, glass fact card right, opaque),
l3 (3A left card over Dan), lt (Motivation lower third over Dan), broll (full-screen clip, own picture), photo (real photo scene),
phone (app screen in the iPhone shell beside Dan), math (side list used as the protein worked example)."""
import json, re
B = '/Volumes/Expansion/_edit_work/RO-21'
W = json.load(open(f'{B}/round1/film_words.json'))
def norm(s): return re.sub(r"[^a-z0-9%']", '', s.lower().replace('-', ''))
def at(phrase, lo=0.0, end=False):
    toks = [norm(t) for t in phrase.split()]
    for i, w in enumerate(W):
        if w['t0'] < lo - 0.05: continue
        if all(i + k < len(W) and norm(W[i + k]['w']).startswith(t) for k, t in enumerate(toks)):
            return round(W[i + len(toks) - 1]['t1'] if end else w['t0'], 3)
    raise SystemExit(f'not found: {phrase!r} after {lo}')
AI = 'AI-GENERATED'; IMG = f'{B}/ai_images'
LV = {35: dict(head='Belly Sticks Out', detail='Man Boobs, Double Chin', h='belly', d='man'),
      30: dict(head='Belly Over Belt', detail='Love Handles, Puffy Face', h='belly', d='love'),
      25: dict(head='Soft Belly', detail='No Muscle Definition Anywhere', h='belly', d="don't"),
      20: dict(head='Flat In A Shirt', detail='Soft Without One, Love Handles', h='flat', d='soft'),
      15: dict(head='Upper Ab Outline', detail='Shoulders And Arms Show', h='outline', d='shoulders'),
      12: dict(head='Upper Abs Show', detail='Obliques And Jawline Show', h='upper', d='obliques'),
      10: dict(head='A Clear Four Pack', detail='Lower Abs Just Starting', h='clear', d='lower'),
      8:  dict(head='Full Six Pack', detail='Veins On Lower Abs And Arms', h='full', d='veins')}
P = []
def add(**k): P.append(k); return k
# ---------------- intro ----------------
lv = [35, 30, 25, 20, 15, 12, 10, 8]
hook_words = ['every', 'body', 'fat', 'percentage', 'looks', 'like', 'same', 'guy']
add(id='G01', kind='ladder', a=0.0, b=at('By the end'), why='Opening 0:00-0:05: the promise is visual, so the eight pictures ARE the hook',
    tiles=[dict(level=l, at=max(0.08, at(w) - 0.05)) for l, w in zip(lv, hook_words)])
add(id='B01', kind='broll', a=at("The scale can't"), b=at('Your body fat percentage tells'), src='B0502', src_in=0.4,
    why='Script graphic "two bodies, same weight" dropped: our AI pictures of Dan at two levels are not the same weight')
add(id='G03', kind='lt', a=at('When the government'), b=at('And that number') - 0.1, topic='THE AVERAGE MAN',
    parts=[['28% Body Fat', '28'], ['(CDC Body Scans)', 'body fat']])
add(id='G04', kind='lt', a=at('To see your upper'), b=at('These are AI') - 0.3, topic='UPPER ABS',
    parts=[['Start To Show Around 15%', '15%']])
add(id='G05', kind='ladder', a=at('These are AI') - 0.3, b=at('Then listen to'), why='Script: all eight side by side, pause on yours',
    tiles=[dict(level=l, at=at('These are AI') + 0.15 + 0.13 * i) for i, l in enumerate(lv)],
    band=[dict(s='Pause On The One That Looks Most Like You', at=at('Pause the video'))])
add(id='G06', kind='lt', a=at('Then listen to'), b=at('Let\'s start at') - 0.3, topic='HOW TO USE THIS',
    parts=[['Do Your Level\'s Step', 'action step'], ['Plus Every Level Below It', 'plus every']])
# ---------------- levels ----------------
starts = {35: "Let's start at 35", 30: 'Next is 30', 25: 'Now, 25', 20: "Now, let's talk about 20", 15: "Next let's talk about 15",
          12: "Let's talk about 12", 10: "Here's 10", 8: 'And finally, 8'}
fact_end = {35: 'If this is you', 30: "And don't let", 25: 'Your action step is to step', 20: 'Your action step is to join',
            15: 'Your action step is to cut way', 12: 'Your action step is to eat', 10: 'Your action step is to track', 8: 'Your action step is to train'}
lo = 55.0
for l in lv:
    a = at(starts[l], lo); b = at(fact_end[l], a); lo = a
    add(id=f'F{l:02d}', kind='fact', a=a, b=b, level=l, photo=f'{IMG}/L{l:02d}.png', label=AI,
        eyebrow=[f'{l}% BODY FAT', a], headline=[[LV[l]['head'], at(LV[l]['h'], a)]], detail=[LV[l]['detail'], at(LV[l]['d'], a)])
# action-step side cards (3A, over Dan), items land on their words
add(id='A35', kind='l3', a=at("And here's your action step"), b=at('Focus mainly') + 3.0, heading='Action Step At 35%',
    points=['Zepbound (Talk To Your Doctor)', '5-Minute Morning Workout', 'Fast Until 2 PM'], reveal=['Start', 'five', 'fasting'])
add(id='B02', kind='broll', a=at('Do squats'), b=at('Do those three'), src=['B0460', 'B0461', 'B0455'], why='squats, push-ups, plank at home, no equipment')
add(id='A30', kind='l3', a=at('Your action step is to cut every'), b=at('That means soda') - 0.05, heading='Action Step At 30%',
    points=['Cut Every Liquid Calorie', 'Weigh In Every Morning'], reveal=['cut every', 'calorie'])
add(id='B03', kind='broll', a=at('That means soda'), b=at('I drank large'), src=['stock:soda', 'stock:juice', 'stock:coffee', 'stock:milk', 'stock:coconut'],
    words=['soda', 'juice', 'sweet', 'milk', 'coconut'])
add(id='G12', kind='lt', a=at('Now I use a zero'), b=at('And yourself') - 0.2, topic='WHAT I DRINK NOW',
    parts=[['Zero Calorie Electrolyte Powder', 'zero']], why='the only stock powder shot reads as sugar: a lower third instead')
add(id='G07', kind='lt', a=at('If you don\'t weigh'), b=at('Now, 25') - 0.3, topic='EVERY MORNING', parts=[['Weigh Yourself', 'weigh yourself']])
add(id='A25', kind='l3', a=at('Your action step is to step'), b=at('Kettlebell deadlifts are') - 0.05, heading='Action Step At 25%',
    points=['10-Minute Kettlebell Workouts', 'Protein In Every Meal'], reveal=['10', 'protein'])
add(id='B05', kind='broll', a=at('Kettlebell deadlifts are'), b=at('Putting protein in every meal means'), src=['B0431', 'C1743'])
add(id='B06', kind='broll', a=at('large serving of meat'), b=at('Protein fills you'), src=['stock:meat', 'stock:fish', 'stock:eggs'], words=['meat', 'fish', 'eggs'])
add(id='A20', kind='l3', a=at('Your action step is to join'), b=at('My workout is') - 0.05, heading='Action Step At 20%',
    points=['A Real Gym, Total Body Every Day', 'Snack On Sardines And Eggs'], reveal=['join', 'swap'])
add(id='B07', kind='broll', a=at('My workout is'), b=at('Now, chips and'), src=['B0566', 'B0697', 'B0574'], why='15 min cardio, then the lifts, Oct 23 gym (Color C)')
add(id='G08', kind='l3', a=at('then one leg') - 0.6, b=at('Now, chips and') - 0.05, heading='My Daily Workout', overlay_on='B07',
    points=['15 Min Cardio', '1 Leg, 3 Upper Body, 1 Ab', '3 Sets Each'], reveal=['cardio', 'one leg', 'three sets'])
add(id='B08', kind='broll', a=at('Now, chips and'), b=at('I buy the prepackaged'), src=['stock:chips', 'stock:sardines', 'stock:eggs2'], words=['chips', 'sardines', 'packed'])
add(id='A15', kind='l3', a=at('Your action step is to cut way'), b=at('Now I didn\'t quit') - 0.05, heading='Action Step At 15%',
    points=['Cut Back On Alcohol And Restaurants', 'Order Meal Prep'], reveal=['cut way', 'Order meal'])
add(id='B09', kind='broll', a=at("Now I didn't quit"), b=at("That's less than"), src=['stock:cocktails', 'stock:mealprep'], words=['Now', 'meal'])
add(id='G09', kind='lt', a=at('for about $8'), b=at('Now, this is the level') - 0.3, topic='MEAL PREP', parts=[['$8 To $9 A Meal', '$8']])
add(id='A12', kind='l3', a=at('Your action step is to eat'), b=at('So let\'s say') - 0.05, heading='Action Step At 12%',
    points=['0.8 g Protein Per Lb Of Lean Mass', 'Sleep In A Cold Room'], reveal=['eat at least', 'sleep'])
a = at('You look like that picture')
add(id='P12', kind='fact', a=a, b=at('You have about 158'), level=12, photo=f'{IMG}/L12.png', label=AI, why='he points at "that picture"',
    eyebrow=['180 LB AT 12%', a], headline=[['That Picture', at('picture', a)]])
add(id='M12', kind='l3', a=at('You have about 158'), b=at('That\'s a large serving') + 2.0, heading='At 180 Lb And 12% Body Fat',
    points=['About 158 Lb Lean Mass', 'At Least 127 g Protein A Day'], reveal=['158', '127'])
add(id='B10', kind='broll', a=at('I sleep best'), b=at('In a University'), src=['stock:sleep'], why='thermostat stock never shows 63 (73 to 68): sleep shot only')
add(id='G10', kind='lt', a=at('In a University'), b=at("Here's 10") - 0.3, topic='UNIVERSITY OF CHICAGO STUDY',
    parts=[['Short Sleep: 55% Less Fat Lost', '55']])
add(id='A10', kind='l3', a=at('Your action step is to track'), b=at('You take a picture') - 0.05, heading='Action Step At 10%',
    points=['Track Every Calorie With AI'], reveal=['track'])
add(id='PH1', kind='phone', a=at('You take a picture'), b=at('Once you start'), src='B0544', why='approved RO-06 app tour screen, Dan beside it')
add(id='A08', kind='l3', a=at('Your action step is to train'), b=at('Cable crunches') - 0.05, heading='Action Step At 8%',
    points=['Train Abs Every Day'], reveal=['train'])
add(id='B11', kind='broll', a=at('Cable crunches'), b=at('Notice this is'), src=['B0574', 'B0584'], words=['Cable', 'leg'])
a = at("That's why I train abs every day now")
add(id='R08', kind='fact', a=a, b=at("So let's review"), level=8, photo=f'{B}/broll/R08_photo.jpg', label='Real photo of me, not AI-generated',
    why='script: the 8% picture, THEN ME TODAY', eyebrow=['ME TODAY, AT 41', a], headline=[['Abs Every Day', at('abs every day', a)]])
# recap
rec = [(35, '35 %', 'Zepbound, 5-Minute Morning Workout, Fast Until 2 PM'), (30, '30 %', 'Cut Liquid Calories, Weigh In Every Morning'),
       (25, '25 %', '10-Minute Kettlebell Workouts, Protein Every Meal'), (20, '20 %', 'Real Gym Every Day, Snack On Sardines And Eggs'),
       (15, '15 %', 'Less Alcohol And Restaurants, Order Meal Prep'), (12, '12%,', '0.8 g Protein Per Lb Lean Mass, Sleep Cold'),
       (10, '10%,', 'Track Every Calorie With AI'), (8, '8%,', 'Train Abs Every Day')]
ra = at("So let's review"); lo = ra; hl = []
for l, ph, s in rec:
    t = at(ph, lo); lo = t + 0.1; hl.append(dict(level=l, at=t, s=s))
add(id='G11', kind='ladder', a=ra, b=round(W[-1]['t1'] + 1.6, 3), why='Script: every level with its action step, highlighted as he says it',
    tiles=[dict(level=l, at=ra + 0.15 + 0.1 * i) for i, l in enumerate(lv)], title=['Every Level, Every Action Step'],
    highlight=[dict(level=h['level'], at=h['at']) for h in hl], band=[dict(lead=f"{h['level']}%", s=h['s'], at=h['at']) for h in hl])
for p in P:                            # every phrase -> film seconds (the transcript spells some words oddly: "zap -bound")
    if p.get('reveal'): p['reveal'] = [at(ph, p['a'] - 0.3) if isinstance(ph, str) else ph for ph in p['reveal']]
    if p.get('parts'): p['parts'] = [[x, at(ph, p['a'] - 0.3) if isinstance(ph, str) else ph] for x, ph in p['parts']]
FULL = ('ladder', 'fact', 'broll')
JOINS = [e['film_in'] for e in json.load(open(f'{B}/round1/edl_r1.json'))[1:]]
for p in P:                            # a full-screen insert that starts or ends within 0.4 s of a take join starts/ends ON the join:
    if p['kind'] in FULL:              # the insert hides the join, and no few-frame sliver of Dan is left between them
        for j in JOINS:
            if 0 < abs(p['a'] - j) < 0.4 and not any(q is not p and q['kind'] in FULL and q['a'] + 1e-3 < j < q['b'] - 1e-3 for q in P): p['a'] = j
            if 0 < abs(p['b'] - j) < 0.4 and not any(q is not p and q['kind'] in FULL and q['a'] + 1e-3 < j < q['b'] - 1e-3 for q in P): p['b'] = j
for p in P:                            # a card that ends just before a full-screen cut ends ON the cut: no 1-2 frame sliver of Dan
    if p['kind'] in ('l3', 'lt', 'phone'):
        nxt = [q['a'] for q in P if q['kind'] in FULL and 0 < q['a'] - p['b'] < 0.35]
        if nxt: p['b'] = min(nxt)
P.sort(key=lambda p: p['a'])
for p in P: assert p['b'] > p['a'] + 0.4, p['id']
json.dump(P, open(f'{B}/round1/plan_r1.json', 'w'), indent=1)
for p in P: print(f"{p['id']:4s} {p['kind']:8s} {p['a']:7.2f}-{p['b']:7.2f}  {p.get('heading') or p.get('topic') or p.get('src') or p.get('level') or ''}")
