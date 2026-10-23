#!/usr/bin/env python3
"""Codex prompts for the SL-18 I'm 41. I Wasted My Life. Shorts covers (2026-10-22). One prompt file per image plus a
jobs list. Per short: 'studio' = background plate behind Dan's real studio cutout (B); c = AI image of Dan acting the title out
(C, real photo as reference; memory cover-picks-ai-dan-acting-topic); d, e = Codex designs (D headline at the bottom, E two
panels). Masculine palettes only (memory thumbnail-masculine-colours). The Shorts' own AI clips go in as references
where they show the same thing (DESK pill-and-water desk, DATEA dinner date)."""
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
EXPR=("Expressive face that acts the headline out, as described below, but natural and believable, not cartoonish. ")
BOTTLE="an orange prescription pill bottle with a plain blank white label and a white cap (no words on it)"
NODAN=DAN.replace("A calm, natural, relaxed expression; if he smiles it is a relaxed closed-mouth smile, never a toothy grin. ","")
AF='/Volumes/Expansion/_edit_work/SL-18/cover-refs/'
from root import R as _R
REF2=str(_R/'sources/ref-s2-studio-blue-137.jpg')
J={
's1':dict(studio="a dim home office at night: a dark wooden desk with a glowing laptop, "+BOTTLE+", a glass of water and an "
  "empty coffee mug at the left and right edges, a few white capsules on the desk, deep navy and charcoal with a cold blue screen "
  "glow and a warm amber desk lamp.",
 c=NODAN+EXPR+f"He stands shirtless in dark athletic shorts beside a dark wooden desk in a dim home office at night, a laptop glowing "
  f"behind him. He holds up {BOTTLE} at shoulder height between his thumb and two fingers and looks straight at the camera with a "
  "serious, knowing 'this will cost you later' look, one eyebrow slightly raised, mouth closed. Deep navy and charcoal, warm amber "
  "desk lamp, cold blue laptop glow. The bottle reads clearly as a prescription pill bottle.",
 d=f"{BOTTLE} lying on its side on a black glossy desk with a few white capsules spilled from it, and standing upright behind it a "
  "large glowing battery symbol made of light (a simple rounded rectangle outline with a small nub on top, like a phone's battery "
  "icon) whose fill has drained to a thin glowing red sliver at the bottom, the empty part dark. Cold cyan rim light, deep navy "
  "background. The attached image shows the film's bottle; match it.",
 e=("a man with short dark hair and glasses in a dark polo shirt at a desk in a bright modern home office in the morning, wired and "
  "buzzing with energy, typing fast with wide alert eyes, an orange pill bottle and a glass of water beside the keyboard, warm "
  "sunlight; the attached image shows this man and office, match him.",
  "the same man at the same desk late at night, slumped forward with his head down on his folded arms on the desk, exhausted and "
  "drained, the orange pill bottle tipped over and empty, cold dim blue light, the window dark."),
 refs=dict(d=[AF+'DESK-1.png'],e=[AF+'DESK-1.png'])),
's2':dict(studio="a dark modern home gym at night: a dumbbell rack and a padded weight bench at the left and right edges, a "
  "smartphone lying face down on the bench, a laptop open on a shelf, steel blue and charcoal with a warm amber accent light.",
 c=NODAN+EXPR+"He stands shirtless in dark athletic shorts in a dark home gym, a dumbbell held at his side in one hand, and with "
  "the other hand he places his smartphone face down on a weight bench beside him (the screen faces the bench and cannot be seen). "
  "He looks at the camera with a confident, relaxed closed-mouth smile, like 'not yet, I'm building'. Steel blue and charcoal, warm "
  "amber light.",
 d="a fit, confident man in his 30s with short dark hair, in a dark fitted shirt, and an elegant woman in a dark green dress laughing "
  "together across a small candlelit table in an upscale restaurant, warm chandeliers and wine glasses behind them, both seated and "
  "shown from the waist up, deep charcoal and warm amber. The tablecloth in the lower part of the frame falls into deep shadow. The "
  "attached image shows the film's restaurant; match its look.",
 e=("the man in the attached reference photo as he looked in his early 20s: the same face and identity, recognisably the same "
  "person, but younger, skinny and unkempt with messy hair, in a wrinkled grey hoodie, sitting alone on an unmade bed in a messy small "
  "apartment at night, hunched over his phone, the blue phone glow on his face, gloomy and lonely; the phone screen is not visible.",
  "the SAME man as in the top panel and the reference photo, today in his 40s, the same face, lean and muscular in a fitted dark "
  "shirt, relaxed and confident with a closed-mouth smile, at a candlelit restaurant table with an attractive woman in a dark green "
  "dress who is smiling at him, warm golden light. Both panels must clearly show the same person."),
 refs=dict(d=[AF+'DATEA-1.5.png'],e=[REF2])),
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
