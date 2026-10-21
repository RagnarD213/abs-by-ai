#!/usr/bin/env python3
"""Codex prompts for the SL-09 Oura Ring Review Shorts covers (2026-10-21). One prompt file per image plus a jobs list.
Per short: 'studio' = background plate behind Dan's real studio cutout (B); c = AI image of Dan in the short's subject (C,
real photo as reference); d, e = Codex designs (D headline at the bottom, E two panels). Masculine palettes only (navy,
charcoal, steel, dark red, amber; memory thumbnail-masculine-colours). Approved SL-09 AI frames (J1 ring on sheets, J2w ring
and strap, K1 tired thumbs-up man) go in as references where they show the same thing."""
from pathlib import Path
import json
from root import R
BASE=("Vertical 9:16 photorealistic image, rich saturated colour in a masculine palette (deep navy, charcoal, steel blue, amber, "
 "dark red; no pink, purple or pastel), crisp commercial lighting, high contrast, reads clearly at phone size. Absolutely no text, "
 "letters, numbers, digits, logos, brand marks, watermarks or labels anywhere; any screen shows only simple shapes or a picture. ")
PLATE=BASE+("This is a BACKGROUND ONLY: no people, no hands. The top 30% is darker and simple so a headline can sit there; the scene "
 "is slightly out of focus with the interest at the left and right edges and in the lower third, because a person will be placed "
 "in the centre later. Scene: ")
C=BASE+("Composition: the top 34% of the frame is empty, dark and plain (soft out-of-focus background, no objects, no heads) because "
 "a headline band will cover it. The man fills the lower 64%, centred, his whole torso and his abs visible, framed from mid-thigh up. Scene: ")
D=BASE+("Composition: the subject sits in the upper-middle of the frame, between 10% and 58% of the height, centred. The bottom 40% is "
 "dark, plain and empty (a dark surface or deep shadow, no objects) because a headline will sit there. Subject: ")
E=BASE+("Composition: a two-panel image stacked vertically. A plain solid black horizontal strip crosses the exact middle of the frame, "
 "16% of the frame height, edge to edge, with nothing in it. TOP panel: {top} BOTTOM panel: {bottom} Each panel's subject is centred "
 "inside its own panel and no head or object touches the black strip.")
DAN=("the man in the attached reference photo: keep his face, his short dark hair, his skin tone and his identity exactly, so he is "
 "clearly recognisable as the same person. He is lean and shredded, not bulky, the same size and build as in the reference, with "
 "clearly defined abs. A calm, natural, relaxed expression; if he smiles it is a relaxed closed-mouth smile, never a toothy grin. "
 "Do not show anyone touching or pinching their stomach. ")
RING="a slim matte black smart ring (a plain smooth band, no logo)"
STRAP="a plain black knit fabric fitness strap with no screen and no logo"
AF='/Volumes/Extreme/_edit_work/sl09/round2/aiframes/'
J={
's1':dict(studio="a dark, moody home gym at dawn: dumbbell racks at the left and right edges, black rubber floor, a tall window with "
  "deep blue early light, warm amber accent lights, navy and amber.",
 c=DAN+f"He is shirtless in dark athletic shorts in a home gym at dawn, mid-set, holding a heavy hexagonal dumbbell in each hand at "
  f"his sides, arms pumped, standing tall and strong, {RING} on his index finger, deep blue window light and warm amber accents.",
 d=f"a man's hand wearing {RING} on the index finger, gripping the knurled steel handle of a heavy black hexagonal dumbbell resting "
  "on a gym floor, chalk dust floating in the air, one hard spotlight from above, dark navy background, crisp detail.",
 e=("a tired man in a grey t-shirt sitting on the edge of his bed at dawn rubbing his eyes, messy hair, dim cold blue light, shown "
  "from the waist up.","a fit, shirtless athletic man doing a hard dumbbell row on a bench in a bright home gym, focused and energetic, "
  "warm golden light, side view, his whole body in the panel.")),
's2':dict(studio="a moody bedroom at night: a bed with dark navy sheets at the right edge, a nightstand at the left edge with a "
  "smartphone glowing on it, a large window with blurred city lights, deep navy blue with one warm amber lamp.",
 c=DAN+f"He sits shirtless in dark athletic shorts on the edge of his bed in a calm bedroom at night, holding his smartphone up "
  "toward the camera so its screen is visible: the screen shows only a simple bright line chart whose line drops off a cliff "
  f"(a single line, no numbers or words). He wears {RING}. He looks at the camera with a calm, knowing closed-mouth smile. Warm "
  "amber lamp light and deep navy shadows.",
 d=f"a smartphone lying face up on a dark wooden nightstand at night, its screen glowing with a single bright line chart that falls "
  f"off a cliff like a crashing stock graph (only the line, no numbers or words), {RING} lying beside the phone, and in the blurred "
  "dark background a man and a woman arguing in a doorway lit red. Deep navy and dark red light.",
 e=("a man and a woman arguing in a dim kitchen at night, she points at him and he holds his hands up, tense dark red and amber light, "
  "both shown from the waist up.","a man sleeping peacefully alone in a bright, calm, tidy bedroom in the morning, crisp white sheets, "
  "golden morning light, very restful.")),
's3':dict(studio="a city street at night seen through a car windshield: blurred red and white light trails streaking at the left "
  "and right edges, a dark empty road ahead, deep navy blue with red accents.",
 c=DAN+f"He sits shirtless in dark athletic shorts on his bed in a calm, dim bedroom at night, leaning back against the pillows "
  "with wireless headphones over his ears, eyes relaxed, calm, a slight closed-mouth smile, car keys left on the nightstand beside "
  "a warm lamp. Deep navy blue and warm amber light.",
 d="a sleek dark grey electric sports sedan racing down an empty highway at night, seen from a low side angle, long red and white "
  "light trails, strong motion blur, wet asphalt reflecting city lights, no license plate visible.",
 e=("the inside of a car speeding at night: a driver's hands gripping the steering wheel tightly, blurred city lights streaking past "
  "the windows, tense dark red light.","a man sleeping peacefully in bed in a dark, calm bedroom, soft deep blue moonlight, very still "
  "and restful.")),
's4':dict(studio="a calm bedroom at dawn: a rumpled white bed at the right edge, a nightstand at the left edge with a glowing "
  "smartphone and a round alarm clock with plain tick marks and no numerals, cool blue morning light through window blinds, navy and white.",
 c=DAN+f"He sits shirtless in dark athletic shorts on the side of his bed in the morning, holding his phone toward the camera so "
  "its screen is visible: the screen shows only a simple sleep chart of blue bars with many tall jagged spikes (bars only, no "
  f"numbers or words). He wears {RING}. His eyebrows are slightly raised, surprised, his mouth closed. Cool blue morning light.",
 d=f"{RING} resting on rumpled white bed sheets at dawn next to a smartphone whose screen shows a simple sleep chart of blue and "
  "amber bars with many tall jagged spikes (bars only, no numbers or words), soft cool morning light, shallow depth of field. "
  "The first attached image shows the ring on the sheets as approved; match that ring.",
 e=("a tired man with messy hair and dark circles under his eyes sitting at a kitchen table with a mug of coffee, giving a weak "
  "thumbs up with a forced smile, bright morning kitchen; the attached image shows this man and scene, match him.",
  "a close-up of a smartphone held in a hand, its screen showing a sleep chart of blue bars full of tall jagged spikes (bars only, "
  "no numbers or words), cold blue light, dark background."),
 refs=dict(d=[AF+'J1_start.png'],e=[AF+'K1_start.png'])),
's5':dict(studio=f"a sleek dark product studio with soft spotlights: {RING} on a small black pedestal at the left edge and {STRAP} "
  "on a small black pedestal at the right edge, charcoal and steel blue background, crisp reflections.",
 c=DAN+f"He stands shirtless in dark athletic shorts in a bright modern living room, holding up {RING} between the thumb and finger "
  f"of one hand and {STRAP} in the other hand, comparing the two, a relaxed confident closed-mouth smile, warm window light.",
 d=f"{RING} and {STRAP} side by side on a dark slate surface, product hero shot, dramatic spotlight on each, a thin glowing vertical "
  "line of steel blue light dividing them, charcoal background. The attached image shows the approved ring and strap; match them.",
 e=(f"a close-up of a man's hand wearing {RING} on his index finger, resting on white bed sheets, soft morning light.",
  f"a close-up of a man's wrist wearing {STRAP}, his hand gripping a dumbbell handle in a gym, warm amber light."),
 refs=dict(d=[AF+'J2w_end.png'])),
}
jobs=[]
refs=json.loads((R/'sources/refs.json').read_text()) if (R/'sources/refs.json').exists() else {}
(R/'assets/prompts').mkdir(parents=True,exist_ok=True);(R/'assets/gen').mkdir(parents=True,exist_ok=True)
for k,v in J.items():
 for w in ['studio','c','d','e']:
  t=PLATE+v[w] if w=='studio' else C+v[w] if w=='c' else D+v[w] if w=='d' else E.format(top=v[w][0],bottom=v[w][1])
  pf=R/'assets/prompts'/f'{k}-{w}.txt';pf.write_text(t+'\n')
  ref=[refs[k]] if w=='c' and k in refs else v.get('refs',{}).get(w,[])
  jobs.append(dict(key=k,which=w,prompt=str(pf),out=str(R/'assets/gen'/f'{k}-{w}.png'),ref=ref))
(R/'assets/jobs.json').write_text(json.dumps(jobs,indent=1));print(len(jobs),'jobs')
