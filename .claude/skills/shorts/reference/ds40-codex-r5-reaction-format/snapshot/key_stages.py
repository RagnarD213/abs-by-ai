import sys,os,subprocess,json
from pathlib import Path
W=Path(__file__).parent;C=W/'recipe';name=sys.argv[1];p=next(x for x in json.loads((W/'plan.json').read_text())['pieces'] if x['id']==name); d=W/'key'/name
os.environ['MIN_FRAMES']='0'
subprocess.run([sys.executable,str(C/'stage1_key.py'),str(p['t0']),str(p['n']/(30000/1001)),str(d/'c1')],cwd=C,check=True)
files=sorted((d/'c1').glob('f*.npy')); assert len(files)>=p['n'];
for extra in files[p['n']:]:extra.unlink()
subprocess.run([sys.executable,str(C/'srcprep.py'),str(p['t0']),str(p['n']),str(d/'source.npy')],cwd=C,check=True)
subprocess.run([sys.executable,str(C/'stage15_temporal.py'),str(d/'c1'),str(d/'source.npy'),str(d/'c15'),str(W/f'watch-{name}.json')],cwd=C,check=True)
