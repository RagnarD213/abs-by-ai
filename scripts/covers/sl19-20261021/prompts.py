#!/usr/bin/env python3
"""Codex prompts for the SL-19 3 Healthy Foods That Made Me Fat Shorts covers (2026-10-21). One prompt file per image plus a
jobs list. Per short: 'studio' = background plate behind Dan's real studio cutout (B); c = AI image of Dan acting the title out
(C, real photo as reference; memory cover-picks-ai-dan-acting-topic); d, e = Codex designs (D headline at the bottom, E two
panels). Masculine palettes only (memory thumbnail-masculine-colours). Approved RO-17 AI frames go in as references where they
show the same thing (A3 scale, A2 couch, A10 sardine eater, S1 carton, S3 chicken cup)."""
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
CARTON="a plain white coconut water carton with a simple green coconut drawing and no words"
AF='/Volumes/Extreme/_edit_work/RO-17/round3/aiframes/'
J={
's1':dict(studio="a dark modern kitchen counter at night: a few plain coconut water cartons and red soda cans at the left and right "
  "edges, scattered white sugar cubes on black stone, a halved green coconut, deep teal and charcoal with warm amber accent light.",
 c=DAN.replace("A calm, natural, relaxed expression; if he smiles it is a relaxed closed-mouth smile, never a toothy grin. ","")+EXPR+
  f"He stands shirtless in dark athletic shorts in a modern kitchen, holding {CARTON} tipped over his open palm, and a stream of "
  "white sugar cubes pours out of the carton into his hand instead of liquid. He looks at the camera with raised eyebrows and a "
  "disbelieving, half-amused 'are you kidding me' look, mouth closed. Deep teal and charcoal kitchen, warm amber light.",
 d=f"{CARTON} standing next to a plain red soda can with no logo on a black stone counter, each with an identical tall pile of "
  "white sugar cubes in front of it, a few cubes tumbling, one hard spotlight, deep teal background. The attached image shows the "
  "approved carton; match it.",
 e=("a fresh green coconut split open with a straw, and instead of water a pile of white sugar cubes spilling out of it onto a dark "
  "counter, dramatic teal and amber light.","a tall glass of plain sparkling water on a dark counter with a slim unbranded "
  "electrolyte powder stick being poured in, the powder swirling, a fit man's hand holding the stick, clean cool light."),
 refs=dict(d=[AF+'S1-carton.png'])),
's2':dict(studio="a dark pantry and kitchen counter: big glass jars and open bags of trail mix (peanuts, almonds, raisins, chocolate "
  "candies) at the left and right edges, a few nuts scattered on dark wood, charcoal and warm amber light with deep red accents.",
 c=DAN.replace("A calm, natural, relaxed expression; if he smiles it is a relaxed closed-mouth smile, never a toothy grin. ","")+EXPR+
  "He stands shirtless in dark athletic shorts in a kitchen, holding a giant open bag of trail mix (peanuts, almonds, raisins, "
  "chocolate candies) in one hand and a tall double cheeseburger in the other, weighing them against each other, eyebrows raised, "
  "looking at the camera with a shocked 'which one is worse' look, mouth closed. No brand logos or wrappers with words. Charcoal "
  "and warm amber light.",
 d="an antique brass balance scale on a marble kitchen counter: the pan with a heap of trail mix (nuts, raisins, chocolate candies) "
  "sits low and heavy, the pan with a tall double cheeseburger is lifted high, warm window light, charcoal background. The attached "
  "image shows the approved scale; match it, with the trail mix side clearly heavier.",
 e=("a heavyset man in a grey hoodie on a dark couch at night with his hand deep in a giant bag of trail mix, TV glow on his face; "
  "the attached image shows this man and scene, match him.",
  "a single glass measuring cup filled with trail mix next to a double cheeseburger on a dark wooden board, side by side, the same "
  "size, warm spotlight, charcoal background."),
 refs=dict(e=[AF+'A2-start.png'],d=[AF+'A3-end.png'])),
's3':dict(studio="a dark slate kitchen counter: an open tin of sardines, a bowl of peeled hard-boiled eggs, a golden rotisserie "
  "chicken and plastic cups of chicken pieces at the left and right edges, deep forest green and charcoal with warm light.",
 c=DAN.replace("A calm, natural, relaxed expression; if he smiles it is a relaxed closed-mouth smile, never a toothy grin. ","")+EXPR+
  "He stands shirtless in dark athletic shorts at a kitchen counter, holding an open tin of sardines in one hand and lifting one "
  "sardine to his mouth with a fork in the other, a relaxed, satisfied look with a closed-mouth smile, eyes to the camera. On the "
  "counter in front of him: a bowl of peeled hard-boiled eggs and a rotisserie chicken. Deep forest green and charcoal, warm light.",
 d="an overhead flat-lay on dark slate of four high-protein snacks laid out in a neat row: an open tin of sardines, three peeled "
  "hard-boiled eggs in a small bowl, a golden rotisserie chicken on a board, and a clear plastic cup of grilled chicken pieces with "
  "a fork, crisp spotlight, deep forest green and charcoal. The attached image shows the approved chicken cup; match it.",
 e=("a fit man in a dark tank top relaxing on a couch at night eating sardines from a tin with a fork, content; the attached image "
  "shows this man and scene, match him.","a golden rotisserie chicken and a bowl of peeled hard-boiled eggs on a dark wooden board, "
  "warm spotlight, deep green background."),
 refs=dict(d=[AF+'S3-chickencup.png'],e=[AF+'A10-start.png'])),
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
