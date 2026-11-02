from pathlib import Path
import sys,subprocess,json,os,shutil
D=Path(__file__).parent;sys.path.insert(0,str(D));import batch as B
import importlib.util
sp=importlib.util.spec_from_file_location("sl13_deliver",D/"deliver.py");Dl=importlib.util.module_from_spec(sp);sp.loader.exec_module(Dl)
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(B.WORK)
Dl.copy('A')
G=W/'build/A/gate';pl=json.loads((G/'plan.json').read_text());pl['graphic_regions'].append(dict(name='study_text',beat=[33.50,45.21],rect=[75,420,930,970]))
pl['negative_events_scan']['method']='Builder inspected both complete proof sheets and native stills; independent proof review found no layout defect. No AI clips, physique photos or app screens. Full exact-file watch pass and independent judge follow.'
(G/'plan.json').write_text(json.dumps(pl,indent=1))
V=Dl.dname('A')
cmd=[sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),V,'--plan',str(G/'plan.json'),'--out',str(G/'watch'),'--log',str(G/'logs/watch_pass.json')]
p=subprocess.run(cmd,capture_output=True,text=True);(G/'watch_run.log').write_text(p.stdout+p.stderr+'\nEXIT '+str(p.returncode));print('WATCH_EXIT',p.returncode,flush=True)
# Asset contexts all use this exact 1080p candidate.
p=subprocess.run([sys.executable,str(D/'page.py')]);assert p.returncode==0
review=R/'Videos to Review';review.mkdir(exist_ok=True);v=review/'Calories Dont Matter SFC R1 - A - Eat Protein First.mp4';shutil.copyfile(V,v);print('VLC',v,flush=True)
print('POST COMPLETE',flush=True)
