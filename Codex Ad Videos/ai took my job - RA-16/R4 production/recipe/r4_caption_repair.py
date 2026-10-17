"""Delay one early phrase caption, retain all approved picture and audio."""
import importlib.util,json,shutil,sys,subprocess,time
from pathlib import Path
P=Path(__file__).with_name('r4_render.py');sp=importlib.util.spec_from_file_location('r4',P);B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
B.buildcap.wait('RA16 R4 single caption onset repair')
old=B.O/'caption-repair1-candidate';old.mkdir(exist_ok=True)
for directory in ['masters','review','watch']:
 shutil.copytree(B.O/directory,old/directory,dirs_exist_ok=True,ignore=shutil.ignore_patterns('._*'))
for p in B.O.glob('*.json'):shutil.copy2(p,old/p.name)
B.render(['16x9'])
for name in ['r4_gate.py','r4_finalize_plan.py']:
 with open(B.O/'logs'/('caption-repair-'+name+'.log'),'w') as f:q=subprocess.run([sys.executable,str(B.O/'recipe'/name)],stdout=f,stderr=subprocess.STDOUT)
 if q.returncode:raise SystemExit((name,q.returncode))
B.write(B.O/'CAPTION_REPAIR_READY.json',{'status':'New exact candidates ready for review and full gates','changed_phrase':'And finally, AI adjusts','previous_onset':42.67596666666667,'new_onset':43.1431,'reason':'Confirmed quiet breath before audible And onset 43.17; prior phrase ends 42.66 before the graphic changes caption position. Source video, audio and graphics unchanged','at':time.time()})
print('CAPTION REPAIR CANDIDATES READY',flush=True)
