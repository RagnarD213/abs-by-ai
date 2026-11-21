#!/usr/bin/env python3
"""Codex prompts for the SL-06 Top 5 Zepbound Tips Shorts covers (2026-10-22). One prompt file per image plus a jobs list.
Per short: 'studio' = background plate behind Dan's real studio cutout (B); c = AI image of Dan in the short's subject (C, real
photo as reference, relaxed closed-mouth smile, no straining flex: VIDEO-RULES 2026-10-21); d, e = Codex designs (D headline at
the bottom, E two panels). Masculine palettes only (memory thumbnail-masculine-colours). The approved SL-06 intro stills go in as
references where they show the same thing; their printed labels never come through (no brand names in organic graphics yet)."""
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
NOLABEL=("Any vial is a small clear glass vial with a silver cap and a plain blank white label with no writing; any syringe is a "
 "plain insulin syringe with an orange cap; any injector pen is a plain dark grey pen with no markings. ")
REFNOTE="The attached image is an approved still from the video: match its objects, mood and lighting, but remove every word, number and label from it. "
DANREF=DAN+"No straining flex and no tensed or trembling pose: he stands or sits naturally, shoulders relaxed. "
AF='/Volumes/Extreme/_edit_work/sl06/round7/frames/';AF6='/Volumes/Extreme/_edit_work/sl06/round6/frames/'
J={
's1':dict(studio="a dark home gym at night: a black leather weight bench and dumbbell racks at the left and right edges, two small "
  "glass vials standing on the bench at one edge, warm amber spotlights on black, steel blue haze. "+NOLABEL,
 c=DANREF+"He stands shirtless in dark athletic shorts in a dark home gym, holding up one small glass vial between his thumb and "
  "finger at chest height and looking at the camera with a calm, relaxed closed-mouth smile, the vial clearly visible. A plain "
  "insulin syringe lies on a bench beside him. Warm amber and charcoal light. "+NOLABEL,
 d="two small glass vials side by side on a black leather gym bench, the left vial slightly smaller, one hard warm spotlight from "
  "above, dumbbell racks out of focus behind, deep charcoal and amber. "+NOLABEL+REFNOTE,
 e=("an extreme close-up of a plain insulin syringe drawing a small dose of clear liquid out of a small glass vial, the plunger "
  "pulled back only a little, crisp macro detail, steel blue and charcoal. "+NOLABEL,
  "a fit shirtless man in dark shorts walking out of a home gym at night with a towel on his shoulder, calm and relaxed, seen "
  "from the chest up, warm amber light. "),
 refs=dict(d=[AF+'A_r7.jpg'])),
's2':dict(studio="a dark wooden counter in a moody locker room at night: a plain injector pen lying in shadow at the left edge, a "
  "small glass vial and an insulin syringe in a pool of warm light at the right edge, lockers in deep charcoal behind. "+NOLABEL,
 c=DANREF+"He stands shirtless in dark athletic shorts in a locker room, holding a small glass vial in one hand and a plain "
  "insulin syringe in the other at chest height, calm relaxed closed-mouth smile, eyes to the camera. A plain dark injector pen "
  "lies on the wooden bench beside him, ignored. Warm amber and charcoal light. "+NOLABEL,
 d="a plain dark grey injector pen lying in deep shadow on the left of a dark wooden counter, and on the right a small glass vial "
  "and an insulin syringe lit by a warm spotlight, strong contrast between the dark side and the lit side, charcoal background. "
  +NOLABEL+REFNOTE,
 e=("a plain dark grey injector pen lying alone on a dark counter in cold blue shadow, slightly desaturated, moody. "+NOLABEL,
  "a small glass vial and a plain insulin syringe side by side on a clean dark counter in a warm golden spotlight, crisp and "
  "inviting. "+NOLABEL),
 refs=dict(d=[AF+'B_r7.jpg'])),
's3':dict(studio="a clean dark bathroom counter at night: alcohol swab packets, a small glass vial, insulin syringes and a black "
  "stopwatch at the left and right edges, cool steel blue light with one warm accent. "+NOLABEL+"The stopwatch has a plain face "
  "with tick marks only, no numbers.",
 c=DANREF+"He sits on the edge of a dark bathroom counter, shirtless in dark athletic shorts, calmly wiping the front of his "
  "thigh with a small white alcohol swab, a plain insulin syringe with its cap on resting in his other hand, relaxed closed-mouth "
  "smile, looking at the camera. Cool steel blue light with a warm accent. "+NOLABEL,
 d="an overhead flat lay on black stone of a simple injection kit laid out in a neat column: a small glass vial, a white alcohol "
  "swab packet, a plain insulin syringe, and a black stopwatch with a plain face (tick marks only, no numbers), hard crisp light. "
  +NOLABEL+REFNOTE,
 e=("a close-up of a man's hand wiping the front of his bare thigh with a small white alcohol swab, clean and clinical, cool "
  "light, no needle in the picture.",
  "a black stopwatch with a plain face (tick marks only, no numbers) next to a plain insulin syringe on a dark counter, the "
  "stopwatch hand near the top, warm spotlight. "+NOLABEL),
 refs=dict(d=[AF+'C_r7.jpg'])),
's4':dict(studio="a cosy home at Thursday evening: a big window with an orange and navy sunset at one edge, a warm table lamp "
  "and a wall calendar grid at the other edge with one vertical column of squares circled in red marker, deep navy and amber. "
  "The calendar has empty squares only, no numbers or words.",
 c=DANREF+"He stands shirtless in dark athletic shorts in a home gym in the evening, holding up a small glass vial at chest "
  "height, relaxed closed-mouth smile, eyes to the camera. Behind him on the wall is a calendar grid with one column of squares "
  "circled in red marker; the calendar has empty squares only, no numbers or words. Warm amber evening light. "+NOLABEL,
 d="a white paper wall calendar grid on a dark wall, empty squares with no numbers or words, one whole vertical column of "
  "squares circled in thick red marker, and below it on a dark desk a small glass vial and a plain insulin syringe under a warm "
  "desk lamp, evening, deep navy and amber. "+NOLABEL,
 e=("a white paper wall calendar grid with empty squares (no numbers or words) and one whole vertical column circled in thick red "
  "marker, warm evening lamp light on a dark wall.",
  "a fit, relaxed man in a navy t-shirt enjoying a calm weekend breakfast outdoors on a sunny patio, coffee and eggs, easy smile "
  "with his mouth closed, bright morning light."),
 refs=dict(c=[])),
's5':dict(studio="a modern home staircase at golden hour: wide wooden steps going down at the left and right edges, a black gym "
  "bag on one step and a glass meal-prep container of chicken and broccoli on another, warm amber and charcoal.",
 c=DANREF+"He walks calmly down a modern wooden staircase at home, shirtless in dark athletic shorts, a black gym bag over one "
  "shoulder and a glass meal-prep container of chicken and broccoli in his hand, relaxed closed-mouth smile, looking at the "
  "camera, framed so his torso and abs are clear. Warm golden-hour light.",
 d="a black gym duffel bag and a glass meal-prep container of grilled chicken and broccoli standing on a dark wooden step at the "
  "top of a staircase that goes down into warm light, a small empty glass vial lying beside them, moody amber and charcoal. "
  +NOLABEL+REFNOTE,
 e=("a black gym duffel bag, a pair of training shoes and a glass meal-prep container of chicken and broccoli on a dark gym "
  "bench, warm spotlight.",
  "a fit man in dark athletic clothes calmly walking down a long modern concrete staircase outdoors, step by step, seen from the "
  "front at a distance, golden hour."),
 refs=dict(d=[AF+'E2_r7.jpg'])),
's6':dict(studio="a dark kitchen counter at night: grilled chicken breasts, a bowl of eggs, Greek yogurt and a protein shake at "
  "the left and right edges, dark slate, warm amber light, deep green accents.",
 c=DANREF+"He stands shirtless in dark athletic shorts at a dark kitchen counter, holding a plate piled with sliced grilled "
  "chicken breast and green beans at chest height, relaxed closed-mouth smile, eyes to the camera. Warm amber kitchen light.",
 d="a white plate of sliced grilled chicken breast and green beans in the foreground under a warm spotlight, and behind it, out "
  "of focus and in shadow, a big bowl of creamy pasta pushed back, dark wooden table, charcoal and amber. "+REFNOTE,
 e=("an overhead view of high-protein foods on dark slate: grilled chicken breast, peeled hard-boiled eggs, a bowl of Greek "
  "yogurt and a piece of salmon, crisp light, deep green and charcoal.",
  "a bowl of chips, crackers and a pile of bread rolls on a dark counter in cold grey shadow, slightly desaturated, pushed away by "
  "a man's hand."),
 refs=dict(d=[AF+'F_r7.jpg'])),
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
