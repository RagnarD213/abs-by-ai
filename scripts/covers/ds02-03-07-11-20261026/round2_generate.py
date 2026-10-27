"""Round 2 (Dan, 2026-10-27): Supplements gets a new concept. Dan: shirtless in the background, the three supplements in
the foreground on the table in front of him, no labels, focus on the supplements. Two takes of the same brief."""
import subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from plan import P,R,PH,STYLE,DAN
ref=str(PH/'studio-blue-145_FINAL_PRIMARY.jpg')
BRIEF=("Upper 30% of the frame is plain dark uncluttered background with nothing in it. A dark wood or stone table runs across the lower third "
 "of the frame. In the FOREGROUND on that table, large, sharp and in focus: three plain supplement containers with no label, no sticker, "
 "no print and no marks of any kind: a clear amber glass jar of golden fish oil softgels, a small amber glass dropper bottle, and a plain "
 "white capsule bottle with a few white capsules spilled beside it. They are the hero of the picture. Dan stands in the BACKGROUND behind "
 "the table, shirtless, slightly soft focus but clearly recognisable, relaxed confident closed-mouth smile at camera, arms relaxed at his sides "
 "or one hand resting on the table edge, defined abs visible above the table. ")
LOOKS={'r2a':"Warm amber kitchen light, charcoal background.",'r2b':"Cool steel-blue studio light with a warm rim on the bottles, deep navy background."}
out=R/'assets/gen';(R/'assets/prompts').mkdir(exist_ok=True)
procs=[]
for tag,look in LOOKS.items():
 pf=R/'assets/prompts'/f'ds03-{tag}.txt';pf.write_text(STYLE+DAN+BRIEF+look)
 log=open(R/'assets'/f'ds03-{tag}.log','w')
 procs.append(subprocess.Popen([str(P/'.claude/skills/_shared/codex-image.sh'),'--model','gpt-6.1-sol','--effort','high','--prompt-file',str(pf),'--out',str(out/f'ds03-{tag}.png'),'--image',ref],stdout=log,stderr=subprocess.STDOUT))
for p in procs:p.wait()
print('done',[p.returncode for p in procs])
