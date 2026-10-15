"""Actual-media Gemini review, with file upload for larger videos. No key or upload token is logged."""
from pathlib import Path
import sys,os,re,json,base64,hashlib,time,urllib.request,urllib.error,mimetypes
key=None
for line in Path('~/.absbyai-secrets.env').expanduser().read_text().splitlines():
 m=re.match(r'\s*(?:export\s+)?GEMINI_API_KEY\s*=\s*["\']?([^"\'\s]+)',line)
 if m:key=m.group(1)
assert key
model=os.environ.get('GM','gemini-3.1-pro-preview');fps=float(os.environ.get('REVIEW_FPS','4'))
prompt=Path(sys.argv[1]);out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
parts=[];records=[];uploaded=[]
for raw in sys.argv[3:]:
 p=Path(raw);mime=mimetypes.guess_type(str(p))[0] or 'application/octet-stream';h=hashlib.sha256(p.read_bytes()).hexdigest();parts.append({'text':'Actual file: '+p.name})
 if p.stat().st_size>10_000_000:
  data=json.dumps({'file':{'display_name':'RA13-'+p.stem[:40]}}).encode()
  req=urllib.request.Request('https://generativelanguage.googleapis.com/upload/v1beta/files',data=data,headers={'x-goog-api-key':key,'X-Goog-Upload-Protocol':'resumable','X-Goog-Upload-Command':'start','X-Goog-Upload-Header-Content-Length':str(p.stat().st_size),'X-Goog-Upload-Header-Content-Type':mime,'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=120) as r:url=r.headers['x-goog-upload-url']
  req=urllib.request.Request(url,data=p.read_bytes(),headers={'Content-Length':str(p.stat().st_size),'X-Goog-Upload-Offset':'0','X-Goog-Upload-Command':'upload, finalize'})
  with urllib.request.urlopen(req,timeout=300) as r:f=json.load(r)['file']
  for _ in range(60):
   if f.get('state')=='ACTIVE':break
   if f.get('state')=='FAILED':raise RuntimeError('File processing failed')
   time.sleep(5)
   req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/'+f['name'],headers={'x-goog-api-key':key})
   f=json.load(urllib.request.urlopen(req,timeout=120))
  else:raise RuntimeError('File processing deadline')
  part={'file_data':{'mime_type':mime,'file_uri':f['uri']}};uploaded.append(f['name'])
 else:part={'inline_data':{'mime_type':mime,'data':base64.b64encode(p.read_bytes()).decode()}}
 if mime.startswith('video/'):
  part['video_metadata']={'fps':fps}
  part['media_resolution']={'level':'MEDIA_RESOLUTION_HIGH'}
 parts.append(part);records.append({'path':str(p),'sha256':h,'bytes':p.stat().st_size,'mime':mime,'fps_requested':fps if mime.startswith('video/') else None})
parts.append({'text':prompt.read_text()})
body={'contents':[{'parts':parts}],'generationConfig':{'temperature':.1,'maxOutputTokens':8192}}
req=urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',data=json.dumps(body).encode(),headers={'Content-Type':'application/json','x-goog-api-key':key})
try:
 result=json.load(urllib.request.urlopen(req,timeout=600));answer=''.join(x.get('text','') for x in result['candidates'][0]['content']['parts']);out.write_text(answer+'\n');(out.with_suffix('.receipt.json')).write_text(json.dumps({'model':model,'request_media':records,'prompt_sha256':hashlib.sha256(prompt.read_bytes()).hexdigest(),'usage':result.get('usageMetadata'),'actual_billed_usd':None,'limits':'Video frames sampled at requested FPS; native scan/boundary review is separate'},indent=2));print(answer);print('USAGE',json.dumps(result.get('usageMetadata')))
except urllib.error.HTTPError as e:
 print('HTTP',e.code,e.read().decode()[:1500].replace(key,'<redacted>'));raise SystemExit(1)
finally:
 for name in uploaded:
  try:urllib.request.urlopen(urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/'+name,method='DELETE',headers={'x-goog-api-key':key}),timeout=60).close()
  except Exception:pass
