from pathlib import Path
import sys,json
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI'); W=Path(__file__).parent
sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import vertical as V
scene,_=V.media_card_scene('G05',26.2262,16/9,kicker='Bill Maher | Real Time (HBO)',caps=False)
tpl,cfg,assets=scene;cfg['hole']=[0,92,1080,608];cfg['radius']=0;cfg['kicker']={'x':36,'y':24,'px':32,'s':'Bill Maher | Real Time (HBO)'}
V.build([(tpl,cfg,assets)],W/'hf',render=True,snap=1)
m=[{'id':'G05','a':4.004,'b':30.2302,'kind':'overlay','mov':str(W/'hf/renders/G05.mov'),'hole':[0,92,1080,608],'words':'Bill Maher | Real Time (HBO)'}]
old=json.loads((W.parent/'round4/graphics-manifest.json').read_text())
m.extend(dict(x,kind=x.get('kind','overlay')) for x in old if x['id']!='G01')
(W/'graphics-manifest.json').write_text(json.dumps(m,indent=2))
