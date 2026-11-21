#!/usr/bin/env python3
"""Codex prompts for the Muhammad dedicated Shorts covers (2026-10-13). Writes one prompt file per image and a jobs list.
Per short: 'studio' = background plate behind Dan's real studio cutout; c/d/e = three AI designs, each for a different layout."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[3];R=P/'Short-form video content/covers/review/muhammad-batch-20261013'
BASE="Vertical 9:16 photorealistic image, bold saturated colour, crisp commercial lighting, high contrast, reads clearly at phone size. Absolutely no text, letters, numbers, logos, watermarks or labels anywhere. "
PLATE=BASE+"This is a BACKGROUND ONLY: no people. The top 35% is darker and simple so a headline can sit there; the scene is slightly out of focus with the interest in the lower two thirds and at the sides, because a person will be placed in the centre later. Scene: "
C=BASE+"Composition: the top 36% of the frame is empty, dark and plain (soft out-of-focus background, no objects, no heads) because a headline band will cover it. The subject fills the lower 60%, centred. Subject: "
D=BASE+"Composition: the subject sits in the upper-middle of the frame, between 14% and 58% of the height, centred. The bottom 40% is dark, plain and empty (a dark floor or deep shadow, no objects) because a headline will sit there. Subject: "
E=BASE+"Composition: a two-panel image stacked vertically. A plain solid black horizontal strip crosses the exact middle of the frame, 14% of the frame height, edge to edge, with nothing in it. TOP panel: {top} BOTTOM panel: {bottom} Each panel's subject is centred inside its own panel and no head or object touches the black strip."
MAN="a lean, shredded, athletic Asian man in his late thirties with short dark hair swept up, shirtless, green athletic shorts, the same build and size as the man in the attached reference image (lean and defined, not bulky), "
J={
'ds-12':dict(studio="a stylish dim men's dressing room with a large round backlit mirror, warm bulbs, dark walnut and teal tones.",
 c="a white marble bust of a handsome man with a razor sharp jawline and strong cheekbones, three quarter view, dramatic teal and orange rim light, dark studio.",
 d="a lean athletic man seen from behind at a bathroom mirror, his reflection showing a sharp jawline, clear skin and defined abs, warm vanity lights, dark surroundings.",
 e=("a rough, soft, rounded clay bust of a man's head with no definition, flat grey light.","the same bust finished in polished marble, chiseled jawline and cheekbones, golden rim light on a dark background.")),
'ds-23':dict(studio="a sunny backyard patio beside a blue swimming pool with a rack of dumbbells at the left edge, limestone wall, green trees, golden hour.",
 c=MAN+"standing facing the camera doing a dumbbell side lateral raise, both arms straight out to the sides at shoulder height with a slight bend in the elbows, small hex dumbbells, by a blue backyard pool with a limestone wall. Whole upper body and both dumbbells inside the frame.",
 d="one pair of small black hex dumbbells standing on dark concrete, lit by a hard blue and white rim light, fine dust in the air.",
 e=("one huge, heavy, oversized black dumbbell on a gym floor under harsh red light.","one small light dumbbell on a gym floor under clean bright green light, glowing.")),
'ds-08':dict(studio="a backyard swimming pool at dusk with warm patio lights and a limestone wall, deep blue water.",
 c="a man's hand holding a modern smartphone upright toward the camera; the lock screen shows a photo of a lean shirtless athletic man standing by a pool. No clock digits or text on the screen. Blurred pool background.",
 d="a single smartphone standing upright on a dark nightstand, its screen glowing with a photo of a lean athletic man by a pool, the glow lighting the dark room. No text on the screen.",
 e=("a dusty pile of workout plan binders, fitness DVDs and a tangled resistance band in a cardboard box, dull grey light, all covers blank.","one smartphone lying on a dark table, screen lit bright with a photo of a lean athletic shirtless man by a pool, blank of any text, golden glow.")),
'ds-09':dict(studio="a tidy home workout corner in a living room at sunrise: exercise mat, a kettlebell and adjustable dumbbells at the sides, warm window light.",
 c="a large chrome stopwatch standing next to a black kettlebell and a rolled exercise mat on a wooden living room floor, warm sunrise light from a window. The stopwatch face has plain tick marks only, no numbers.",
 d="a lean athletic man in a t-shirt and shorts doing a push-up on an exercise mat in a living room at sunrise, a laptop open on a desk behind him, side view, whole body inside the frame.",
 e=("a line of cars stuck in a traffic jam at dusk, red brake lights, seen through a windshield.","an exercise mat, a kettlebell and a pair of dumbbells on a sunlit living room floor at sunrise, calm and bright.")),
'ds-22':dict(studio="a blue exercise mat on a stone pool patio with an ab wheel lying at the left edge, blue pool water and a limestone house behind, bright daylight.",
 c=MAN+"kneeling on a blue exercise mat doing an ab wheel rollout, seen from the side, arms extended forward holding the ab wheel, body in one straight line from head to knees, hips not sagging, by a backyard pool. Whole body and the wheel inside the frame.",
 d="one ab wheel roller with black handles standing on a blue exercise mat, low dramatic camera angle, hard rim light, dark background.",
 e=("the same kind of lean shirtless athletic man in green shorts kneeling upright on a blue mat holding an ab wheel under his shoulders, the start position, side view.","the same man at full stretch in an ab wheel rollout from his knees, body long and straight just above the mat, side view.")),
'ds-14':dict(studio="a dim upscale bar back wall with rows of liquor bottles with blank labels, amber and teal light, heavily out of focus.",
 c="a man's hand, palm out, pushing away a short glass of whiskey with ice across a dark wooden bar top, amber light, bottles blurred behind.",
 d="three drinks in a row on a dark bar: a plain silver can with no label beside a glass of clear sparkling water with lime, a tall clear vodka soda with a lime wedge, and a dark cola with ice and a lime wedge. Clean product lighting.",
 e=("six shot glasses of brown liquor in a tight row on a wet bar top under harsh red light.","one tall glass of clear sparkling seltzer with ice and a lime wedge under clean cool white light.")),
'ds-24':dict(studio="a stone pool patio with a pair of small dumbbells resting at the right edge, blue water, limestone wall and green trees, soft afternoon light.",
 c=MAN+"doing a dumbbell rear delt fly: hinged forward at the hips with a flat back, chest toward the ground, both arms raised out wide to the sides like wings holding small dumbbells, seen from the front, by a backyard pool. Both arms and dumbbells inside the frame.",
 d="the muscular upper back and rear shoulders of a lean athletic man seen from behind, arms slightly out, rear deltoids sharply defined by hard side light, dark gym background. No face visible.",
 e=("a wooden artist's mannequin standing slouched, shoulders rolled forward and head down, flat grey light.","the same wooden mannequin standing tall with its chest up and shoulders pulled back, holding a tiny dumbbell in each hand, warm golden light.")),
'ds-21':dict(studio="an outdoor stone patio with a rack of black hex dumbbells at the left edge, pool water behind, green trees, late afternoon light.",
 c=MAN+"standing facing the camera doing a hammer curl with his left arm: the hex dumbbell is held vertically, thumb up, forearm curled to chest height, the other arm down at his side holding a second dumbbell, by a backyard pool with a limestone wall.",
 d="a steel claw hammer and a black hex dumbbell crossed over each other on a dark steel workbench, hard orange and blue rim light, a few sparks.",
 e=("a close-up of a muscular forearm and fist holding a hex dumbbell horizontally, palm up, under dull red light.","a close-up of the same muscular forearm holding the hex dumbbell vertically, thumb up, in a hammer curl grip, under bright green light.")),
}
REF={'ds-23':'sl-12.0.png','ds-22':'aw-9.5.png','ds-24':'rd-1.0.png','ds-21':'hc-13.5.png'}
jobs=[]
for k,v in J.items():
 for w in ['studio','c','d','e']:
  t=PLATE+v[w] if w=='studio' else C+v[w] if w=='c' else D+v[w] if w=='d' else E.format(top=v[w][0],bottom=v[w][1])
  pf=R/'assets/prompts'/f'{k}-{w}.txt';pf.write_text(t+'\n')
  ref=str(R/'sources'/REF[k]) if k in REF and (w=='c' or (k=='ds-22' and w=='e')) else ''
  jobs.append(dict(key=k,which=w,prompt=str(pf),out=str(R/'assets/gen'/f'{k}-{w}.png'),ref=ref))
(R/'assets/jobs.json').write_text(json.dumps(jobs,indent=1));print(len(jobs),'jobs')
