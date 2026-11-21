from pathlib import Path
import subprocess,concurrent.futures,json,time
P=Path(__file__).resolve().parent
scenes={
'ad13-B':('acid yellow','A large chrome dumbbell beside a calculator, rolled blank paper receipts and a modest stack of US-style cash. Fitness coaching cost visual. Glossy black tabletop, razor-sharp yellow edge light.'),
'ad13-C':('warm gold','Surreal editorial product photography: a gigantic cast-iron kettlebell whose round body is a transparent glass jar filled with crumpled blank receipts and coins. Cash and two short blank receipt curls surround its base. A physical metaphor for expensive fitness coaching, immediately understandable.'),
'ra01-B':('electric cyan','Large upright premium black smartphone with completely blank black glass screen and cyan illuminated edge, beside a heavy chrome dumbbell. Dramatic modern fitness-tech product photography, glowing slim circuit lines on floor.'),
'ra01-C':('electric violet','A spectacular futuristic polished chrome rectangular portal with a radiant violet interior, beside a real cast-iron dumbbell. The portal is empty, an abstract visual for using AI to imagine fitness goals. Chrome, black glass, dramatic premium science fiction, absolutely no person or body reflection.'),
'ad10-B':('orange','A large black iron kettlebell beside an open slim laptop with completely blank dark screen, a closed notebook and coffee mug. On a rich charcoal home-office desk. Fitness and a busy working father, punchy commercial photography.'),
'ad10-C':('signal yellow','An oversized sculptural yellow analog alarm clock with blank face and hands but no numerals, leaning against a black kettlebell. Surreal premium product photograph conveying training in a busy schedule. Massive scale, crisp texture, forceful simplicity.'),
'ad4-B':('bright red','Oversized unbranded white supplement jars, amber capsule bottles and scattered gold softgel capsules on a dark glossy counter. One bottle tipped with a few capsules spilling. Blank labels. Sharp photorealistic textures, high contrast red rim light.'),
'ad4-C':('electric green','Huge transparent optical magnifying glass inspecting an unbranded white supplement bottle and three large gold softgel capsules. A green beam behind the lens evokes analysis, not a medical procedure. Premium dramatic macro product photography, dark counter, exceptionally sharp.'),
'ad3-B':('electric cyan','An oversized chrome stopwatch, blank clipboard and thick black dumbbell on a charcoal gym bench. Premium dramatic commercial photograph about personal training costs, bold cyan rim lighting, crisp reflection.'),
'ad3-C':('electric blue','A beautifully engineered chrome robotic gripper hand firmly holding a real black dumbbell in the bottom-left of the image. Only the robot hand and part of mechanical forearm, no human. Dramatic futuristic fitness coaching visual, photoreal steel and cobalt edge lights.'),
'ad6-B':('warm amber','A premium warm-lit home gym with a large chrome dumbbell and upright black weight plate on a bench in lower-left. Strong amber sunlight and rich dark wall. Crisp, energetic, mature masculine atmosphere with no people, no writing.'),
'ad6-C':('golden orange','An oversized black iron kettlebell at the start of a short flight of dramatic golden illuminated steps inside a dark modern gym. A warm sunrise beam over the steps. Ambitious premium editorial fitness photo, crisp architectural lines, no people.')}
common='Create ONE landscape 16:9 photographic background plate for a high-click-through YouTube fitness thumbnail. NO PEOPLE, no faces, no human bodies, no text, no letters, no logos, no watermark. Composition is critical: the main large props occupy the LOWER LEFT quadrant (x 5-47 percent, y 55-100 percent). Upper left 50 percent is dark quiet negative space reserved for a large headline. RIGHT HALF must be simple dark atmospheric background reserved for a real photographic man added later. Do not place any important object in the right half. Deep black and charcoal base with one accent color. Bold subject-specific photographic environment, striking close-up props, commercial sharpness, dramatic studio light, no blur, no panels or collage. '
for key,(color,scene) in scenes.items():
 (P/'prompts'/f'{key}.txt').write_text(common+'Accent color: '+color+'. Scene: '+scene)
def run(key):
 start=time.time();out=P/'generated'/f'{key}.png'
 if out.exists():return {'id':key,'existing':True}
 log=P/'generated'/f'{key}.log'
 with log.open('w') as f:
  r=subprocess.run(['.claude/skills/_shared/codex-image.sh','--prompt-file',str(P/'prompts'/f'{key}.txt'),'--out',str(out)],stdout=f,stderr=subprocess.STDOUT)
 return {'id':key,'exit':r.returncode,'seconds':round(time.time()-start),'output':log.read_text()[-1800:]}
if __name__=='__main__':
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  for future in concurrent.futures.as_completed([ex.submit(run,k) for k in scenes]):
   result=future.result();results.append(result);print(json.dumps(result),flush=True);(P/'generation-log.json').write_text(json.dumps(results,indent=2))
