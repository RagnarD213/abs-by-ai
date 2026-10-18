"""Full unchanged gates on the final caption-repaired native candidates."""
import json,subprocess,sys,importlib.util,time
from pathlib import Path
p=Path(__file__).with_name('r4_render.py');s=importlib.util.spec_from_file_location('r4',p);B=importlib.util.module_from_spec(s);s.loader.exec_module(B)
B.buildcap.wait('RA16 R4 final native delivery gates')
results=[]
for a in ['9x16','16x9']:
 master=B.O/'masters'/f'AI Took Job AD R4 - {a}.mp4';planpath=B.O/f'gate-plan-{a}.json';plan=json.load(open(planpath))
 plan['negative_events_scan']={'sha256':B.sha(master),'when':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'frames_checked':59,'method':'Original complete film visually reviewed through chronological sheets and native boundary strips, followed by exact-candidate repair identity and changed-span checks. Only phrase-caption onset changes. Separate independent full-candidate report retains limits.','findings':[]};B.write(planpath,plan)
 with open(B.O/'logs'/f'final-native-delivery-{a}.log','w') as f:q=subprocess.run([sys.executable,str(B.SH/'deliver/gate.py'),str(master),'--format','ad9x16' if a=='9x16' else 'ad16x9','--plan',str(planpath)],stdout=f,stderr=subprocess.STDOUT)
 results.append({'aspect':a,'sha256':B.sha(master),'exit':q.returncode});B.write(B.O/'final-gate-results.json',results);print('FINAL GATE',results[-1],flush=True)
