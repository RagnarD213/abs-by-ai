from pathlib import Path
import sys,json,urllib.request,hashlib
from full import R,ROOT,sha,dump
sys.path.insert(0,str(ROOT/'.claude/skills/_shared'));import review_server as RS
runtime=Path.home()/'Library/Application Support/AbsByAI Reviews/9411'
records=RS.snapshot(R/'review',runtime/'page');dump(runtime/'manifest.json',dict(source=str(R/'review'),files=records))
rows=[]
for film in json.loads((R/'delivery-manifest.json').read_text())['films']:
 for kind in ['review_full','review_phone']:
  file=Path(film[kind]);relative=file.relative_to(R/'review').as_posix();url='http://127.0.0.1:9411/'+relative
  with urllib.request.urlopen(url,timeout=30) as res:body=res.read();status=res.status;assert status==200
  digest=hashlib.sha256(body).hexdigest();assert digest==sha(file)
  with urllib.request.urlopen(urllib.request.Request(url,headers={'Range':'bytes=100-199'}),timeout=30) as res:assert res.status==206 and len(res.read())==100;content_range=res.headers['Content-Range']
  rows.append(dict(short=film['short'],kind=kind,url=url,status=status,range_status=206,content_range=content_range,sha256=digest))
with urllib.request.urlopen('http://127.0.0.1:9411/',timeout=10) as res:page=res.read().decode();assert 'Three Complete Shorts' in page and 'provisional' not in page
assert len(rows)==6;dump(R/'review-http-checks.json',rows);print('Six full/phone files: HTTP200, range206 and exact hashes verified; page ready')
