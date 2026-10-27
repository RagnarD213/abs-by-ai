from pathlib import Path
import sys,json
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import vertical as V
c=json.loads((W/'hf/configs/R2_SourcePanel.json').read_text())[0];c['kicker'].update(px=25,s='Girls Like The Dad Bod Until We Showed Them This | ManVsStreet')
V.build([(R/'.claude/skills/_shared/hyperframes/media-card/media-card.template.htm',c,())],W/'hf',render=True,snap=1)
for v in ['scripted','off_the_cuff']:
 p=W/v/'graphics-manifest.json';m=json.loads(p.read_text());m[0]['words']=c['kicker']['s'];p.write_text(json.dumps(m,indent=2))
print('EXACT_SOURCE_TITLE_READY',flush=True)
