from pathlib import Path
import sys,subprocess,shutil,json,hashlib
D=Path(__file__).parent;sys.path.insert(0,str(D));import batch as B
W=Path(B.WORK);ROOT=Path(B.lib.ROOT);OUT=W/'review';rows=[]
names={'A':'Eat Protein First','B':'Eat Less Without Counting','C':'Keep Your Steps Up'}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for q in iter(lambda:f.read(8*1024*1024),b''):h.update(q)
 return h.hexdigest()
subprocess.run([sys.executable,str(D/'page.py')],check=True)
vlc=ROOT/'Videos to Review';assert vlc.is_dir()
for S in 'ABC':
 f=OUT/(B.P.NAME[S]+'.mp4');p=vlc/('Calories Dont Matter SFC R2 - '+S+' - '+names[S]+'.mp4');shutil.copyfile(f,p)
 h=sha(f);assert sha(OUT/'media'/(S+'.mp4'))==h==sha(p)==sha(W/'build'/S/f.name)
 rows.append(dict(id=S,title=' '.join(B.P.TITLE[S][1]),sha256=h,bytes=f.stat().st_size,file=str(f),pageMedia=str(OUT/'media'/(S+'.mp4')),vlc=str(p)))
(W/'delivery-manifest.json').write_text(json.dumps(rows,indent=2))
print('Exact 1080p build/review/page/VLC hashes match for all three',flush=True)
