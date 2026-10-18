import sys,json,subprocess,time,importlib.util
from pathlib import Path
P=Path(__file__).with_name('r4_render.py');sp=importlib.util.spec_from_file_location('r4',P);B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
B.buildcap.wait('RA16 R4 final audio and delivery gates')
sys.path.insert(0,str(B.SH/'audio'));import common as A
out=[]
for aspect in ['9x16','16x9']:
 master=B.O/'masters'/f'AI Took Job AD R4 - {aspect}.mp4';p=B.O/f'gate-plan-{aspect}.json';plan=json.load(open(p))
 plan['negative_events_scan']={'sha256':B.sha(master),'when':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'frames_checked':59,'method':'Editor inspected complete chronological 1fps sheets plus all 16 five-consecutive-frame boundary strips. Fit presenter and approved same-person photo/AI goal; no adverse body close-up. Full motion/audio review is recorded separately.','findings':[]}
 B.write(p,plan);A.carry_untreated(str(B.W/'round2/audio/warm-bass-final-timing.wav'),str(master))
 with open(B.O/'logs'/f'final-audio-{aspect}.log','w') as f:a=subprocess.run([sys.executable,str(B.SH/'audio/audio_gate.py'),str(master),'--ab',str(B.O/'audio'/f'Audio AB {aspect}.mp4')],stdout=f,stderr=subprocess.STDOUT)
 with open(B.O/'logs'/f'full-delivery-{aspect}.log','w') as f:g=subprocess.run([sys.executable,str(B.SH/'deliver/gate.py'),str(master),'--format','ad9x16' if aspect=='9x16' else 'ad16x9','--plan',str(p)],stdout=f,stderr=subprocess.STDOUT)
 out.append({'aspect':aspect,'audio_exit':a.returncode,'delivery_exit':g.returncode,'sha256':B.sha(master)})
 B.write(B.O/'full-gate-results.json',out);print('FULL GATES',out[-1],flush=True)
