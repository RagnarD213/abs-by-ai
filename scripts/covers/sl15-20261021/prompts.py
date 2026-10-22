#!/usr/bin/env python3
"""Codex prompts for the SL-15 My First Spray Tan Shorts covers (2026-10-21). One prompt file per image plus a jobs list.
Per short: 'studio' = background plate behind Dan's real studio cutout (B); c = AI image of Dan in the short's subject (C,
real photo as reference); d, e = Codex designs (D headline at the bottom, E two panels). Masculine palettes only (navy,
charcoal, bronze, amber, dark red; memory thumbnail-masculine-colours). Approved RO-19 AI frames (A1 vampire under the
umbrella, A4 the spray-tan appointment) go in as references for short 2's E panels."""
from pathlib import Path
import json
from root import R
BASE=("Vertical 9:16 photorealistic image, rich saturated colour in a masculine palette (deep navy, charcoal, bronze, amber, "
 "dark red; no pink, purple or pastel), crisp commercial lighting, high contrast, reads clearly at phone size. Absolutely no text, "
 "letters, numbers, digits, logos, brand marks, watermarks or labels anywhere; any bottle or product is plain and unlabelled. ")
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
DAN=("the man in the attached reference photo: keep his face, his short dark hair, his identity exactly, so he is clearly "
 "recognisable as the same person. He is lean and shredded, not bulky, the same size and build as in the reference, with "
 "clearly defined abs. A calm, natural, relaxed expression; if he smiles it is a relaxed closed-mouth smile, never a toothy grin. "
 "Do not show anyone touching or pinching their stomach. ")
AF='/Volumes/Extreme/_edit_work/ro19/aiframes/'
J={
's1':dict(studio="a professional photo studio: a large white octagonal softbox on a stand at the left edge, a flash head on a stand "
  "with a silver umbrella at the right edge, a seamless charcoal paper backdrop, warm amber rim light and deep navy shadows.",
 c=DAN+"His skin has an even, deep bronze tan, which makes every line of his abs and chest pop with contrast. He stands shirtless "
  "in dark athletic shorts in a professional photo studio, posing for a photo shoot with a relaxed confident stance, one hand on "
  "his hip, while a studio flash on the left fires a bright burst at him and a large softbox glows behind. Charcoal backdrop, "
  "warm amber and navy light.",
 d="three male bodybuilders on a competition stage, each with an extremely deep, dark bronze competition tan and oiled skin, "
  "standing side by side doing a front double-biceps pose under bright white stage spotlights, a black stage curtain behind "
  "them, haze in the light beams; all three men complete from head to knees, faces calm and natural.",
 e=("a fit, lean man with extremely pale, ghostly white, pasty skin, much paler than normal, like he has never seen the sun, standing "
  "shirtless in a photo studio, lit flat by a harsh direct camera flash that bleaches him almost white and washes out his muscles so "
  "his abs barely show, a plain grey backdrop, shown from the thighs up.","the SAME man, the same face and the same body, now with an even, deep, dark bronze tan, clearly much darker than the top panel, standing in the same photo studio "
  "under warm directional studio light, his abs and chest sharply defined by the contrast, shown from the thighs up, confident.")),
's2':dict(studio="a bright tropical beach at noon with harsh overhead sun: a large navy beach umbrella at the left edge throwing a "
  "deep shadow, a plain unlabelled sunscreen bottle and a folded towel on the sand at the right edge, turquoise sea and blazing "
  "white sky glare, strong amber sunlight.",
 c=DAN+"His skin has an even, deep bronze tan. He stands shirtless in dark swim shorts in the cool shade under a large navy "
  "beach umbrella on a bright tropical beach at noon, holding a plain unlabelled white sunscreen bottle in one hand, relaxed "
  "and calm, a slight closed-mouth smile. Harsh white sun blazes on the sand behind him, he stays in the shade.",
 d="a professional spray-tan airbrush gun held in a gloved hand, spraying a fine glowing bronze mist cloud that fills the "
  "middle of the frame, inside a dark pop-up tanning tent, dramatic warm amber backlight making the mist glow, deep navy shadows.",
 e=("a pale vampire with slicked-back black hair, black and red cape and fangs, shirtless in black swim shorts, cowering under a "
  "black umbrella on a bright sunny tropical beach, hand up against the sun; the attached first image shows this vampire and "
  "scene, match him.","a fit man in navy shorts standing in a black pop-up spray-tan tent with his arms slightly out while a "
  "technician in a white polo sprays him with a fine bronze mist from an airbrush gun, calm spa room; the attached second image "
  "shows this appointment, match it."),
 refs=dict(e=[AF+'A1-start.png',AF+'A4-start.png'])),
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
