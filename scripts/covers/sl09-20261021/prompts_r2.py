#!/usr/bin/env python3
"""SL-09 covers round 2 (Dan, 2026-10-21). Short 1: none of A-E; three new designs (F, G, H), each an AI image of Dan
"extremely sleep-deprived and also training hard ... bags under my eyes, look like a sleep-deprived zombie, but also ripped
... doing a seated military press, lifting extremely hard and intensely with a ton of different weights". Short 3: E, with a
new bottom picture of Dan "extremely sleep-deprived and cracked out, like I can't sleep ... as a result of adrenaline-filled
fast driving before bed". Short 4: three new designs (F, G, H) with Dan like the man in E: "at the table, shirtless with a cup
of coffee, giving a thumbs up, but looking like a sleep-deprived zombie". Appends its jobs to assets/jobs.json (gen.sh runs
only jobs without an output)."""
import json
from root import R
from prompts import BASE,AF
LAND=BASE.replace('Vertical 9:16','Horizontal 16:9 (landscape)')
ME=("the man in the first attached reference photo: keep his face, his short dark hair, his skin tone and his identity exactly, so he "
 "is clearly recognisable as the same person. He is lean and shredded, not bulky, the same size and build as in the reference, "
 "shirtless, with clearly defined abs. Do not show anyone touching or pinching their stomach. ")
ZOMBIE=("He looks like a sleep-deprived zombie: heavy dark bags under bloodshot, half-open eyes, pale grey skin around the eyes, "
 "his short hair messy, a dazed, exhausted thousand-yard stare. ")
LIFT=("He is doing a seated military press on an upright bench, lifting extremely hard and intensely: jaw clenched, veins standing "
 "out on his arms and neck, every muscle straining. The weights carry no numbers or markings. ")
TOPC=("Composition: the top 34% of the frame is empty, dark and plain (soft out-of-focus gym, no objects, no heads, no weights) because "
 "a headline band will cover it. Everything else, the man, the bench and every weight, sits in the lower 64%, centred. ")
BOTD=("Composition: the man, the bench and every weight sit in the upper part of the frame, between 6% and 60% of the height, centred. "
 "The bottom 40% is a dark, plain gym floor in deep shadow with nothing on it, because a headline will sit there. ")
TOPA=("Composition: the top 27% of the frame is dark and plain (a dim gym ceiling, no objects, no weights) because a headline will sit "
 "there. The man fills the rest of the frame, centred, from the top of the weights down to the bench. ")
GYM="A gritty, dimly lit gym at night, one hard spotlight from above, deep navy and steel blue with warm amber accents."
J={
 's1-f':(TOPC+ME+ZOMBIE+LIFT+"The barbell rests at his collarbone at the bottom of the press, loaded with a huge stack of plates of many "
  "different sizes on each side (black, red, blue and green plates), the bar bending slightly. "+GYM,['s1']),
 's1-g':(BOTD.replace('the man, the bench and every weight sit in the upper part of the frame, between 6% and 60% of the height, centred.',
  'a close shot: the man fills the full width of the frame, the dumbbells above his head near the top, his face large and clearly visible.').replace(
  'The bottom 40% is a dark, plain gym floor in deep shadow with nothing on it, because a headline will sit there.',
  'His whole body continues naturally down the frame: his hips, his legs and the bench fill the bottom 40%, falling into deep, dark shadow with little detail, because a headline will sit over them. Nothing cuts across his body.')
  +ME+ZOMBIE+LIFT+"He presses two enormous, heavy dumbbells overhead, arms bent at the middle of the press with the dumbbells just above "
  "his head, the camera close in front of him so his exhausted face is large. "+GYM,['s1']),
 's1-h':(TOPA+ME+ZOMBIE+LIFT+"The barbell is halfway up, level with his forehead, loaded with a huge stack of plates of many different "
  "sizes on each side, chalk dust in the air, plates and kettlebells stacked behind him. "+GYM,['s1']),
}
LANDS=("Composition: the man is centred, his head in the middle of the frame, nothing important within 15% of the left and right edges. ")
J['s3-e2']=(LAND+LANDS+ME+"He lies in bed at night wide awake and cannot sleep, wired and cracked out after an adrenaline-filled fast drive "
 "home: eyes wide open and bloodshot, heavy dark bags under them, pale and jittery, staring at the ceiling, gripping the sheets, his "
 "car keys and phone on the nightstand, the bedside clock a plain glowing face with no numerals. Dark bedroom, cold blue moonlight "
 "through the blinds with a red glow from the street outside.",['s3'])
K=("The second attached image shows the scene and pose to copy: a man sitting at a wooden kitchen table in a bright morning kitchen, a "
 "white mug of coffee in one hand, giving a weak thumbs up with the other with a forced, tired smile. Put the man from the first image "
 "in that scene and pose, shirtless. ")
J['s4-f']=(TOPC.replace('soft out-of-focus gym, no objects, no heads, no weights','soft out-of-focus kitchen wall, no objects, no heads').replace('the man, the bench and every weight','the man, the table and the mug')
 +ME+K+ZOMBIE+"Bright morning light.",['s4','K1'])
J['s4-g']=(BOTD.replace('the man, the bench and every weight','the man, his thumbs up and the mug').replace('a dark, plain gym floor in deep shadow','the dark wooden table top in deep shadow')
 +ME+K+ZOMBIE+"Bright morning light on him, the table in front falling into shadow.",['s4','K1'])
J['s4-h']=(LAND+LANDS+ME+K+ZOMBIE+"Bright morning light, framed from the table up to just above his head, like the second image.",['s4','K1'])
refs=json.loads((R/'sources/refs.json').read_text());refs['K1']=AF+'K1_start.png'
jobs=json.loads((R/'assets/jobs.json').read_text());have={(j['key'],j['which']) for j in jobs}
for name,(text,rr) in J.items():
 k,w=name.split('-');pf=R/'assets/prompts'/f'{name}.txt';pf.write_text((text if text.startswith('Horizontal') else BASE+text)+'\n')
 if (k,w) not in have:jobs.append(dict(key=k,which=w,prompt=str(pf),out=str(R/'assets/gen'/f'{name}.png'),ref=[refs[x] for x in rr]))
(R/'assets/jobs.json').write_text(json.dumps(jobs,indent=1));print(len(J),'round 2 jobs;',len(jobs),'in all')
