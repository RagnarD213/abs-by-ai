from pathlib import Path
import sys,json,subprocess,importlib.util
D=Path(__file__).parent;sys.path.insert(0,str(D));import batch as B
sp=importlib.util.spec_from_file_location('sl13deliver',D/'deliver.py');Dl=importlib.util.module_from_spec(sp);sp.loader.exec_module(Dl)
S=sys.argv[1];W=Path(B.WORK);G=W/'build'/S/'gate';Dl.copy(S)
p=G/'plan.json';pl=json.loads(p.read_text())
for sh in json.loads((W/'build'/S/'shots.json').read_text()):
 if sh['kind']=='clip' and sh['roll'] in ['study','eating-window','fasting-fact','fasting-compare','movement-fact','steps-list']:
  pl['graphic_regions'].append(dict(name=sh['roll']+'_text',beat=[sh['f0']/B.FPS,sh['f1']/B.FPS],rect=[75,420,930,970]))
pl['negative_events_scan']['method']='Builder reviewed source and native proof images; A revised study and B/C full graphics/source proofs; independent exact-file watch judgment follows. No new AI footage, personal physique photos or app screens.'
p.write_text(json.dumps(pl,indent=1))
cmd=[sys.executable,str(Path(B.lib.ROOT)/'.claude/skills/_shared/deliver/watch.py'),Dl.dname(S),'--plan',str(p),'--out',str(G/'watch'),'--log',str(G/'logs/watch_pass.json')]
r=subprocess.run(cmd,capture_output=True,text=True);(G/'watch_run.log').write_text(r.stdout+r.stderr+'\nEXIT '+str(r.returncode));print(S,'WATCH_EXIT',r.returncode,flush=True)
print('POST COMPLETE',S,flush=True)
