#!/usr/bin/env python3
"""Codex prompts for the SL-07 If I Had Belly Fat Shorts covers (2026-10-18). One prompt file per image plus a jobs list.
Per short: 'studio' = background plate behind Dan's real studio cutout (B); c = AI image of Dan in the short's subject (C,
real photo as reference); d, e = Codex's own designs (D headline at the bottom, E two panels)."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[3];R=P/'Short-form video content/covers/review/sl07-20261018'
BASE="Vertical 9:16 photorealistic image, bold saturated colour, crisp commercial lighting, high contrast, reads clearly at phone size. Absolutely no text, letters, numbers, digits, logos, watermarks or labels anywhere; any screen or display is blank or shows only a picture. "
PLATE=BASE+"This is a BACKGROUND ONLY: no people. The top 30% is darker and simple so a headline can sit there; the scene is slightly out of focus with the interest at the sides and in the lower third, because a person will be placed in the centre later. Scene: "
C=BASE+"Composition: the top 34% of the frame is empty, dark and plain (soft out-of-focus background, no objects, no heads) because a headline band will cover it. The man fills the lower 64%, centred, his whole torso visible. Scene: "
D=BASE+"Composition: the subject sits in the upper-middle of the frame, between 10% and 58% of the height, centred. The bottom 40% is dark, plain and empty (a dark floor or deep shadow, no objects) because a headline will sit there. Subject: "
E=BASE+"Composition: a two-panel image stacked vertically. A plain solid black horizontal strip crosses the exact middle of the frame, 16% of the frame height, edge to edge, with nothing in it. TOP panel: {top} BOTTOM panel: {bottom} Each panel's subject is centred inside its own panel and no head or object touches the black strip."
DAN=("the man in the attached reference photo: keep his face, his short dark hair, his skin tone and his identity exactly, so he is clearly recognisable as the same person. "
 "He is lean and shredded, not bulky, the same size and build as in the reference, with clearly defined abs. Do not show anyone touching or pinching their stomach. ")
J={
's1':dict(studio="a bright modern bathroom at sunrise, a sleek glass bathroom scale on the tiled floor at the left edge, a large wall calendar of blank squares on the right wall, warm window light and teal tiles.",
 c=DAN+"He stands shirtless in dark athletic shorts in a bright modern bathroom at sunrise, smiling confidently at the camera with his arms relaxed, a wall calendar of blank squares behind him on the wall, warm window light.",
 d="a big paper wall calendar made of a grid of about ninety blank squares, most of them crossed off with bold red marker X marks, pinned on a dark blue wall, hard spotlight from above, a red marker resting on the ledge below.",
 e=("a tiny garden snail crawling slowly across a glass bathroom scale, flat dull grey light, everything dim and slow.","a fit sprinter exploding out of starting blocks on a red running track at sunrise, golden light, motion and energy, seen from the side, whole body in the panel.")),
's2':dict(studio="a calm white bathroom at sunrise with a glass digital scale on the floor at the right edge, a mug of coffee on the counter at the left, soft golden window light.",
 c=DAN+"He is shirtless in dark athletic shorts, standing on a glass digital bathroom scale in a bright white bathroom at sunrise, holding a mug of coffee, looking down at the blank scale display with a relaxed smile, golden morning light from a window.",
 d="a close-up of a man's bare feet standing on a sleek glass digital bathroom scale on white marble tiles, the scale display glowing soft blue and blank, low camera angle, golden sunrise light streaking across the floor.",
 e=("a dusty bathroom scale shoved under a bed in a dark, cluttered bedroom, cobwebs, cold blue gloom.","the same bathroom scale gleaming on a clean, sunlit white bathroom floor at sunrise, a fluffy white towel beside it, bright and fresh.")),
's3':dict(studio="a clean home garage gym at dawn: a kettlebell and a pair of dumbbells at the left edge, an exercise mat, the garage door half open to an orange sunrise sky, blue and orange light.",
 c=DAN+"He is shirtless in dark athletic shorts doing a kettlebell swing on a backyard patio at sunrise, the kettlebell at chest height in front of him with straight arms, body upright and strong, orange sunrise sky and trees behind him.",
 d="an old-style round analog alarm clock with plain tick marks and no numerals, its hands showing six o'clock, standing on a wooden floor next to a pair of laced running shoes and a black kettlebell, first light of dawn through a window, deep blue shadows.",
 e=("a man lying asleep on a couch in a dark living room at night, an untouched gym bag on the floor beside him, cold dim blue light.","a lean athletic man doing push-ups on an exercise mat in a bright living room at sunrise, golden light through the windows, side view, whole body in the panel.")),
's4':dict(studio="a modern dark-tiled bathroom with a sleek black bathroom scale on the floor at the right edge, a white towel on a hook at the left, cool blue light with a warm vanity glow.",
 c=DAN+"He is shirtless in dark athletic shorts in a modern bathroom, stepping off a sleek black bathroom scale with a confident grin and a thumbs up, a white towel over one shoulder, cool blue and warm light.",
 d="three small black cast-iron one-pound weights stacked neatly on top of a sleek white bathroom scale, dramatic spotlight from above, dark charcoal background, crisp shadows.",
 e=("a big holiday feast on a table: burgers, pizza, fries and pints of beer, warm red and orange light, indulgent and messy.","a man's bare feet stepping onto a white bathroom scale on clean tiles the next morning, cool clean daylight, the scale display blank.")),
's5':dict(studio="a bright modern kitchen with white marble counters, a plate of grilled chicken, rice and broccoli at the left edge and a bowl of fruit at the right edge, warm afternoon window light.",
 c=DAN+"He is shirtless in dark athletic shorts in a bright modern kitchen, holding up a smartphone and taking a photo of a plate of grilled salmon, rice and broccoli on the marble counter in front of him, smiling, warm window light.",
 d="a hand holding a smartphone above a plate of grilled salmon, rice and broccoli, the phone screen shows a photo of the same plate framed by four thin white corner brackets like a camera scan, no words or numbers on the screen, dark slate table, moody overhead light.",
 e=("a cluttered kitchen counter covered in a food scale, measuring cups, a calculator and a messy notebook of scribbles, flat dull grey light, tedious.","a smartphone held over a colourful plate of chicken, rice and vegetables taking a photo, bright clean light, effortless, the phone screen shows the food photo only.")),
}
REF={'s1':'photo-1','s2':'photo-2','s3':'photo-3','s4':'photo-4','s5':'photo-5'}   # replaced by refs.json once photos are picked
jobs=[]
refs=json.loads((R/'sources/refs.json').read_text()) if (R/'sources/refs.json').exists() else {}
for k,v in J.items():
 for w in ['studio','c','d','e']:
  t=PLATE+v[w] if w=='studio' else C+v[w] if w=='c' else D+v[w] if w=='d' else E.format(top=v[w][0],bottom=v[w][1])
  pf=R/'assets/prompts'/f'{k}-{w}.txt';pf.write_text(t+'\n')
  ref=refs.get(k,'') if w=='c' else ''
  jobs.append(dict(key=k,which=w,prompt=str(pf),out=str(R/'assets/gen'/f'{k}-{w}.png'),ref=ref))
(R/'assets/jobs.json').write_text(json.dumps(jobs,indent=1));print(len(jobs),'jobs')
