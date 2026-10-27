#!/usr/bin/env python3
"""SL-16 cover round 2 (Dan 2026-10-27): s1 two trash-can breakfast designs, s3 A revised (offered drink turned down),
s4 new title with three designs (salad + two Codex picks). s2 A only changes title (no new picture)."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from root import R,PH
from prepare import base,ai
plan=json.loads((R/'design-plan.json').read_text())
ref=lambda k:str(PH/f"{plan[k]['studio']}_FINAL_PRIMARY.jpg")
J=[
 ('s1','r2f',ai+'Dan standing in a bright kitchen tipping a full plate of breakfast food into an open kitchen trash can: a short stack of pancakes, strips of bacon, fried eggs and toast clearly sliding off the plate into the bin, instantly recognisable as breakfast. In his other hand he holds a plain black mug of black coffee. Confident relaxed closed-mouth smile at the camera. Warm morning sunlight, charcoal and amber kitchen.',[ref('s1')]),
 ('s1','r2g',ai+'Dan seen from a slightly low angle beside a sleek steel pedal trash can in a deep navy kitchen at sunrise, dumping a plate piled with pancakes with syrup, bacon, sausage and fried eggs into it, the breakfast food mid-fall into the bin and clearly identifiable. His other hand holds a plain white mug of black coffee at chest height. Playful knowing look at the camera, cool blue light with warm sunrise rim light.',[ref('s1')]),
 ('s3','r2a','Revise the attached cover picture (first image) and keep its scene, lighting, bar, steak plate and the man exactly as they are, except: another person\'s hand and forearm only (no face or body of that person) reaches in from the right edge offering him a glass of whiskey. Dan turns it down: his hand is raised toward the offered glass with his open palm facing it, fingers up, a clear polite no-thanks gesture. A tall glass of plain water stands on the counter right next to him. '+ai+'Same man, same face as the identity reference (second image).',[str(R/'assets/gen/s3-a.png'),ref('s3')]),
 ('s4','r2f',ai+'Dan sitting at a bright kitchen table eating a big fresh green salad with grilled chicken, fork lifted with a normal bite, relaxed and happy, clean simple setting with fresh daylight, deep green and white kitchen.',[ref('s4')]),
 ('s4','r2g',ai+'Dan at a kitchen counter calmly sliding away a cluttered pile of seven mismatched meal prep containers, supplement tubs without labels and a measuring scale, while holding one simple plate of grilled chicken, rice and broccoli in his other hand. Simple beats complicated at a glance. Confident smile, warm charcoal and amber kitchen.',[ref('s4')]),
 ('s4','r2h',ai+'Dan standing in a modern kitchen crumpling a long multi-page paper meal plan into a ball in one hand (blank paper with only faint abstract grey lines, no readable writing), and holding a single simple plate of grilled steak and vegetables in the other hand. Knowing confident look at camera, cool teal light.',[ref('s4')]),
]
jobs=[]
for k,w,prompt,refs in J:
 pf=R/'assets/prompts'/f'{k}-{w}.txt';pf.write_text(base+prompt+'\n')
 jobs.append(dict(key=k,which=w,prompt=str(pf),out=str(R/'assets/gen'/f'{k}-{w}.png'),ref=refs))
(R/'assets/jobs_r2.json').write_text(json.dumps(jobs,indent=2));print(len(jobs),'jobs')
