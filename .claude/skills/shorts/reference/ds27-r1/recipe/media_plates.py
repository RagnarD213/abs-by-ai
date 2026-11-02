from pathlib import Path
import sys,os,json
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];os.environ['GATE_GROUP']='DS-27';sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import vertical as V
items={}
for gid,dur,kicker,label in [('EQUIPMENT',11,'My Home Workout Setup',None),('CLIENT',6,'Consistent Home Workouts','AI-GENERATED')]:
 scene,hole=V.media_card_scene(gid,dur,16/9,label=label,kicker=kicker,max_w=1080)
 V.build([scene],W/'hf-media',render=True,snap=3);items[gid]=dict(hole=hole,mov=str(W/'hf-media/renders'/(gid+'.mov')),config=scene[1])
(W/'media-plates.json').write_text(json.dumps(items,indent=2))
