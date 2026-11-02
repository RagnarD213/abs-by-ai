from pathlib import Path
import sys,json,importlib.util,os,subprocess
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];os.environ['GATE_GROUP']='DS-27';os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH'];p=R/'scripts/video/hyperframes_graphics.py';s=importlib.util.spec_from_file_location('hg',p);H=importlib.util.module_from_spec(s);s.loader.exec_module(H)
# Resolve edges by the complete spoken phrase within each graphic's own window.
P=H.module('from_plan');words=P.Words(W/'words_out.json');plans=json.load(open(W/'plan_resolved.json'))
for g in plans:
 lo=g['t0']-1;hi=max(g['t1'],g['t0']+8)
 g['t0']=words.at(g['start'],lo,hi,'in');g['t1']=words.at(g['end'],g['t0'],hi,'out')
(W/'plan_resolved.json').write_text(json.dumps(plans,indent=2))
H.build(W/'plan_resolved.json',W/'words_out.json',None,W/'hf16',render=False)
(W/'graphics-sheet.json').write_text(json.dumps({'graphics':H.edit_sheet_graphics(W/'plan_resolved.json',W/'words_out.json',W/'hf16')},indent=2))
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/hyperframes/vertical.py'),'--sheet',str(W/'graphics-sheet.json'),'--out',str(W/'hf'),'--render','--snap'],check=True)
