from pathlib import Path
import json,hashlib,urllib.request,datetime,sys
W=Path(__file__).resolve().parents[1];root=W/'review';base='http://127.0.0.1:9241/';records=[]
for v in ['scripted','off_the_cuff']:
 for suffix in ['.mp4','-540p.mp4','.srt','-audio-ab.wav']:
  rel='media/dad-bod-r3-'+v+suffix;p=root/rel;expected=hashlib.sha256(p.read_bytes()).hexdigest()
  with urllib.request.urlopen(urllib.request.Request(base+rel,method='HEAD'),timeout=15) as r:assert r.status==200 and int(r.headers['Content-Length'])==p.stat().st_size
  with urllib.request.urlopen(base+rel,timeout=30) as r:actual=hashlib.sha256(r.read()).hexdigest();assert r.status==200 and actual==expected
  ranges=[]
  if suffix.endswith('.mp4'):
   for a in [0,p.stat().st_size//2]:
    b=min(a+1023,p.stat().st_size-1)
    with urllib.request.urlopen(urllib.request.Request(base+rel,headers={'Range':f'bytes={a}-{b}'}),timeout=15) as r:
     data=r.read();assert r.status==206 and len(data)==b-a+1
     with p.open('rb') as f:f.seek(a);assert data==f.read(len(data))
     ranges.append([a,b])
  records.append(dict(path=rel,sha256=expected,bytes=p.stat().st_size,http200=True,ranges206=ranges))
out=dict(checked_at=datetime.datetime.now().astimezone().isoformat(),review_url=base,scope='Actual served current media bytes and large-file seeking, separate from final page UI/release approval.',files=records)
name=sys.argv[1] if len(sys.argv)>1 else 'http-review-media.json';(W/'qa'/name).write_text(json.dumps(out,indent=1));print('CURRENT_MEDIA_HTTP_AND_BYTE_RANGES_PASS',len(records))
