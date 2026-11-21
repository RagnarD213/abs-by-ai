#!/usr/bin/env python3
"""Codex prompts for the SL-17 "I'm 41. My Life Is Top 1%." Shorts covers (2026-10-23). One prompt file per image plus a jobs
list. Per short: 'studio' = background plate behind Dan's real studio cutout (B); c = AI image of Dan acting the title out
(C, real photo as reference; memory cover-picks-ai-dan-acting-topic); d = Codex object/scene hero with the headline at the
bottom (D); e = two stacked panels (E). Masculine palettes only (memory thumbnail-masculine-colours). The Shorts' own clips
go in as references where they show the same thing (jump rope by the pool, the black-belt group photo)."""
from pathlib import Path
import json
from root import R
BASE=("Vertical 9:16 photorealistic image, rich saturated colour in a masculine palette (deep navy, charcoal, steel blue, forest green, "
 "amber, dark red; no pink, purple or pastel), crisp commercial lighting, high contrast, reads clearly at phone size. Absolutely no text, "
 "letters, numbers, digits, logos, brand marks, watermarks or labels anywhere; any screen, clock or package shows only simple shapes. ")
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
 "clearly defined abs. Do not show anyone touching or pinching their stomach. ")
EXPR="Expressive face that acts the headline out, as described below, but natural and believable, not cartoonish. "
CR='CLIPREF/'
J={
's1':dict(studio="a bright modern kitchen at golden hour: a dark stone counter with a large wooden salad bowl full of greens, "
  "grilled chicken on a board, glass meal-prep containers with rice, broccoli and salmon at the left and right edges, and a pair of "
  "dumbbells pushed to the far corner; forest green, charcoal and warm amber light.",
 c=DAN+EXPR+"He stands shirtless in dark athletic shorts at a dark stone kitchen counter, a row of glass meal-prep containers in "
  "front of him filled with grilled chicken, rice, broccoli and salad. He holds one finished container up toward the camera at chest "
  "height in one hand, a fork in the other, and looks at the camera with a confident, knowing half smile, one eyebrow slightly raised, "
  "as if saying 'this is where the abs are made'. A pair of dumbbells sits ignored on the counter's far end. Forest green, charcoal and "
  "warm amber kitchen light.",
 d="an old-fashioned brass balance scale on a dark slate surface. On the LOWER pan sits a big fresh salad bowl with grilled chicken "
  "and greens, clearly heavier; on the HIGHER pan sits a black iron dumbbell, lifted up because it is outweighed. Dramatic warm rim "
  "light, deep charcoal and forest green background.",
 e=("a sweaty man with short dark hair in a dark tank top on a gym bench after a hard workout, eating a greasy burger and fries from "
  "a takeaway box, a dumbbell at his feet, cold blue gym light, he looks tired and a little guilty; show him clothed and whole, "
  "no focus on his stomach.",
  "a lean, fit man with short dark hair in a fitted dark t-shirt at a bright kitchen table eating a big fresh salad with grilled "
  "chicken, relaxed closed-mouth smile, warm golden morning light. The same man as the top panel."),
 refs=dict(e=[CR+'saladbite.png'])),
's2':dict(studio="a calm backyard pool at sunrise: still blue water, a stone pool edge, a kettlebell and a coiled jump rope on a "
  "blue exercise mat at the left and right edges, oak trees, a soft orange and steel blue dawn sky.",
 c=DAN+EXPR+"He is shirtless in dark green athletic shorts, jumping rope fast by a backyard pool at sunrise, mid-skip with one foot "
  "lifted like a boxer, the rope a motion-blurred arc around him, sweat glistening. Wide-awake, energetic, determined face with a "
  "relaxed closed-mouth smile. Orange sunrise light and steel blue water; the attached second image shows the real pool and jump "
  "rope; match that setting.",
 d="a simple minimalist analog alarm clock with no numbers on its face (only plain tick marks), its hands at a few minutes past six, "
  "standing on a blue exercise mat at dawn beside a coiled black jump rope and a black kettlebell, low warm sunrise light raking "
  "across from a window, deep navy shadows.",
 e=("a man with short dark hair lying in bed at dawn, reaching out from under the duvet to switch off an alarm clock, sleepy, dim cold "
  "blue bedroom light; the clock face has no numbers.",
  "the same man minutes later, shirtless and lean, jumping rope fast on a backyard patio by a pool at sunrise, energised, warm orange "
  "light. The same man as the top panel."),
 refs=dict(c=[CR+'jumprope.png'])),
's3':dict(studio="an empty martial arts dojo: blue and black tatami mats, a heavy punching bag hanging at the left edge, a folded "
  "white gi with a black belt resting on a low wooden bench at the right edge, soft window light, deep navy and charcoal.",
 c=DAN+EXPR+"He is in a white judo/jiu-jitsu gi with a black belt, the jacket open showing his defined chest and abs, standing in a "
  "dojo on blue mats, gripping the lapels of a training partner (seen from behind, out of focus, in a blue gi) and about to throw him. "
  "Focused, calm, fierce eyes, mouth closed. Deep navy and charcoal dojo, warm rim light. The attached second image shows him in his "
  "real gi with his real black belt; match the gi and belt.",
 d="two martial arts belts on a dark blue tatami mat, side by side and neatly folded: a crisp new WHITE belt on the left and a worn, "
  "frayed BLACK belt on the right, a single spotlight from above, deep navy and black shadows, cinematic.",
 e=("a nervous, skinny beginner man with short dark hair in a stiff brand-new white gi with a white belt, standing at the edge of a "
  "dojo mat on his first day, unsure, cool grey light.",
  "the same man years later, fit and calm, in a worn white gi with a black belt, kneeling and bowing on a dojo mat, confident, warm "
  "golden light. Both panels must clearly show the same person."),
 refs=dict(c=[CR+'black-belt-group.png'],d=[],e=[])),
}
jobs=[]
refs=json.loads((R/'sources/refs.json').read_text()) if (R/'sources/refs.json').exists() else {}
(R/'assets/prompts').mkdir(parents=True,exist_ok=True);(R/'assets/gen').mkdir(parents=True,exist_ok=True)
cr=str(R/'sources/clipref')+'/'
for k,v in J.items():
 for w in ['studio','c','d','e']:
  t=PLATE+v[w] if w=='studio' else C+v[w] if w=='c' else D+v[w] if w=='d' else E.format(top=v[w][0],bottom=v[w][1])
  pf=R/'assets/prompts'/f'{k}-{w}.txt';pf.write_text(t+'\n')
  extra=[x.replace(CR,cr) for x in v.get('refs',{}).get(w,[])]
  ref=([refs[k]] if w=='c' and k in refs else [])+extra
  jobs.append(dict(key=k,which=w,prompt=str(pf),out=str(R/'assets/gen'/f'{k}-{w}.png'),ref=ref))
(R/'assets/jobs.json').write_text(json.dumps(jobs,indent=1));print(len(jobs),'jobs')
