#!/usr/bin/env python3
"""SL-16 Intermittent Fasting Shorts: Codex prompts for five cover choices per Short (mix of 2026-10-25).
A AI Dan acting the topic (yellow band), B second AI Dan scene (bottom stack), C real studio photo on a Codex scene,
D Codex choice: wrong-vs-right split comparison (no Dan: the contrast reads instantly), E Codex choice: third AI Dan, expressive."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from root import P,R,PH
base='Vertical 9:16 photorealistic editorial photography, masculine sophisticated saturated palette, crisp directional light, premium quality, meaningful large props readable on a phone. No text, letters, digits, logo, watermark, labels or written marks anywhere. No branded packaging or bottles with labels. '
plate='BACKGROUND ONLY, no person, no hands, no human figure. Upper 36% is uncluttered dark negative space for typography. Centre lower two thirds is clear for a large real portrait to be composited later; topic props toward lower side edges. '
ai='Use the attached real photo only as an identity reference. The man is clearly Dan from that photo, same face, short black hair, Asian features, lean and shredded, not bulky, same size as the reference. Shirtless in normal dark athletic shorts. Upper 36% empty dark background with no head or objects; person and action in lower 62%, centred with entire hair, head and torso visible, sharply defined abs, whole arms and natural hands with five fingers. No stomach touching, no pinching. Mouth closed. '
split='Two stacked photographic panels separated by a blank black horizontal band across the centre, band 20% of frame height. No subject, prop or hand touches the band. TOP panel: {top} BOTTOM panel: {bottom} '
data={
's1':dict(title='How To Start Fasting: Just Skip Breakfast',lines=['How To Start Fasting:','Just Skip Breakfast'],badge='INTERMITTENT FASTING',studio='studio-white-23',
 a='Dan sitting at a kitchen table sliding a full plate of pancakes, bacon and eggs away from him with one hand while holding a plain black mug of black coffee in the other, confident relaxed smile, warm morning sunlight, charcoal and amber kitchen.',
 b='Dan sitting down happily to a big lunch plate of grilled chicken, rice and vegetables at midday, a plain round wall clock with tick marks only and no numerals behind him showing two oclock, relaxed smile, bright teal and white daylight kitchen.',
 c='Bright morning kitchen in deep teal and warm gold, an untouched plate of pancakes and bacon at the far lower left edge, a plain black mug of black coffee at the far lower right edge, clear centre.',
 d=('A full American breakfast of pancakes with syrup, bacon, eggs and orange juice on a wooden table, cool blue morning light.','A single plain black ceramic mug of black coffee alone on the same wooden table, nothing else, warm golden sunlight.'),
 e='Dan standing at an open refrigerator early in the morning, holding a plain black mug of coffee and pushing the fridge door closed with his other hand, playful knowing look straight at the camera, deep navy kitchen lit by cool fridge light.'),
's2':dict(title='Carbs Are Killing Your Workday',lines=['Carbs Are Killing','Your Workday'],badge='AFTERNOON CRASH',studio='studio-gray-79',
 a='Dan slumped at a home office desk in an afternoon food coma, head propped heavily on one hand, eyelids half closed, an open box of glazed donuts and a slice of pizza beside his open laptop, sleepy expression, dim warm afternoon light.',
 b='Dan wide awake and focused at a standing desk typing on an open laptop, a big green salad with grilled chicken beside it, energetic bright daylight, confident smile.',
 c='Dark slate home office desk, an open box of glazed donuts at the far lower left edge and a pizza slice on a plate at the far lower right edge, clear centre, moody teal light.',
 d=('A box of glazed donuts and greasy pizza slices next to an open laptop on an office desk, dim sleepy orange light.','A grilled chicken salad and a black coffee next to an open laptop on the same office desk, bright crisp cool daylight.'),
 e='Dan sitting at an office desk firmly pushing an open box of glazed donuts away with one flat hand, looking at the camera with one eyebrow raised and a half smile, open laptop, dark slate office with teal edge light.'),
's3':dict(title='Never Break Your Fast With Alcohol',lines=['Never Break Your Fast','With Alcohol'],badge='ALCOHOL',studio='studio-blue-213',
 a='Dan sitting at a dark wooden bar counter with a hearty plate of grilled steak and vegetables in front of him, holding his open palm up toward a glass of whiskey to turn it down, confident relaxed smile, moody amber bar lighting.',
 b='Dan at a home dinner table eating his first meal of the day, grilled salmon and vegetables, with a tall glass of plain water, an unopened plain dark wine bottle pushed far to the side of the table, warm evening light.',
 c='Moody bar counter in deep burgundy and copper light, a cocktail glass at the far lower left edge and a plate of grilled steak at the far lower right edge, clear centre.',
 d=('A glass of whiskey and a cocktail on an empty bar counter with no food at all, ominous dark red light.','A hearty plate of grilled steak and vegetables with a tall glass of water on a dinner table, warm amber light.'),
 e='Dan standing behind a bar counter turning a plain empty wine glass upside down onto the counter, knowing look straight at the camera, dark navy bar with copper rim light.'),
's4':dict(title='Life Will Punch You In The Face',lines=['Life Will Punch You','In The Face'],badge='STICK TO THE PLAN',studio='studio-blue-74',
 a='Dan wearing red boxing gloves in a gritty boxing gym leaning back to dodge a heavy punching bag swinging toward his face, intense focused expression, dramatic red and charcoal light.',
 b='Dan standing calm in a chaotic morning kitchen holding a plain black mug of black coffee, around him a spilled cereal box on the counter, a pile of laundry and a buzzing phone, calm confident smile amid the chaos, warm sunlight.',
 c='Dark gritty boxing gym, a red heavy punching bag hanging at the far lower left edge and a pair of red boxing gloves on a bench at the far lower right edge, clear centre, dramatic red light.',
 d=('A neat row of meal prep containers knocked over and scattered across a kitchen counter, a pair of red boxing gloves lying beside them, harsh red light.','A single plain black mug of black coffee on a clean calm kitchen counter, peaceful morning light.'),
 e='Dan in a boxing ring corner with red boxing gloves raised in a guard, sweat on his shoulders, confident smirk at the camera, bright overhead ring lights and dark crowd-free background.')}
jobs=[]
for k,v in data.items():
 ref=[str(PH/f"{v['studio']}_FINAL_PRIMARY.jpg")]
 for which in 'abcde':
  if which in 'abe':prompt=base+ai+v[which];refs=ref
  elif which=='c':prompt=base+plate+v['c'];refs=[]
  else:prompt=base+split.format(top=v['d'][0],bottom=v['d'][1]);refs=[]
  pf=R/'assets/prompts'/f'{k}-{which}.txt';pf.write_text(prompt+'\n')
  jobs.append(dict(key=k,which=which,prompt=str(pf),out=str(R/'assets/gen'/f'{k}-{which}.png'),ref=refs))
(R/'assets/jobs.json').write_text(json.dumps(jobs,indent=2));(R/'design-plan.json').write_text(json.dumps(data,indent=2))
designs={k:{'A':'AI you acting it out: '+v['a'].split(',')[0].replace('Dan ',''),'B':'AI you, second scene: '+v['b'].split(',')[0].replace('Dan ',''),'C':f"Real studio photo ({v['studio']}) on an AI scene",'D':'Wrong vs right: two food photos with the title in the black band','E':'AI you, expressive: '+v['e'].split(',')[0].replace('Dan ','')} for k,v in data.items()}
notes={'decided':['Mix per your 2026-10-25 rule: A and B are two different AI pictures of you acting the topic out, C is a real studio photo (your real pixels, only the background is generated), D and E are my picks from your history: D a wrong-vs-right food comparison (reads at a glance, no person), E a third AI you, since AI you is what you pick most.',
 'Five different layouts per Short: A yellow band on top (your usual pick), B white and cyan headline at the bottom, C centred headline with a yellow marker, D black band across the middle, E big Impact headline on the left with a white frame.',
 'Same approved title on all five. No website mark, no claims, no photo labels. All four approved Short videos stay untouched.',
 'Short 4 shows boxing gear only, never Mike Tyson.'],'designs':designs}
(R/'notes.json').write_text(json.dumps(notes,indent=2));print('Prepared',len(jobs),'image jobs')
