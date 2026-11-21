"""One blinded Gemini audio QA call under Dan's standing <=$5 review authorization."""
from pathlib import Path
import os,sys,re,json,base64,urllib.request,urllib.error,hashlib,shutil,subprocess
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
MODEL='gemini-3.8-flash' # exact stable ID observed in this account's live model listing
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
E=W/'evidence/listener';E.mkdir(exist_ok=True)
assert not (E/'response.json').exists(),'Review already exists; do not bill twice'
raw=W.parent/'round2/audio/cut-raw.wav';ref=E/'source-reference.wav'
subprocess.run([C.FF,'-nostdin','-y','-v','error','-i',str(raw),'-af','atrim=start=13.72:end=25.80,asetpts=PTS-STARTPTS','-c:a','pcm_s24le',str(E/'raw.wav')],check=True)
I,TP,LRA=C.ebur(str(E/'raw.wav'))
subprocess.run([C.FF,'-nostdin','-y','-v','error','-i',str(E/'raw.wav'),'-af',f'volume={-16-I}dB','-c:a','pcm_s24le',str(ref)],check=True)
mapping={'sample-71':'C','sample-24':'A','sample-56':'B'}
paths=[ref]
for label,k in mapping.items():
 p=E/(label+'.wav');shutil.copyfile(W/f'review/media/{k}.wav',p);paths.append(p)
prompt='''Act as an independent audio engineer listening to real supplied audio. The first file is the unprocessed original lav recording, volume matched. The following three unlabeled files contain the SAME complete passage at matched integrated loudness. One is a previous finished mix and two are restrained cleanup candidates, in unknown order. Do not infer their identities from filenames. Judge what is actually audible. Natural voice identity and complete consonants/word endings matter more than removing every trace of noise.
For EACH file: quote the opening phrase and final phrase actually heard; confirm continuous speech begins immediately, with no long silence; identify any cut word. Describe audible clarity, background sound, warmth/body, harshness/sibilance, metallic/watery/underwater sound, pumping and damaged quiet word endings. Distinguish original speech/mouth noises from added processing artifacts. Compare each sample with the unprocessed source. Give severity and exact excerpt seconds for any defect. If a distinction is subtle, say so; do not invent a difference or force a winner.
End with a ranking for natural clarity, whether each is suitable to show the speaker as an audition, and a concise recommendation. We are NOT approving publication or choosing for the human. Return plain text. If you cannot hear these audio inputs, say that explicitly and do not fabricate listening.'''
(E/'prompt.txt').write_text(prompt)
(E/'binding.json').write_text(json.dumps(dict(mapping=mapping,inputs=[dict(file=str(p),sha256=C.sha256(str(p))) for p in paths],model=MODEL,estimated_max_usd=.25,max_output_tokens=4096),indent=2))
key=os.environ.get('GEMINI_API_KEY')
if not key:
 for line in Path.home().joinpath('.absbyai-secrets.env').read_text().splitlines():
  m=re.match(r'''\s*(?:export\s+)?GEMINI_API_KEY\s*=\s*["']?([^"'\s]+)''',line)
  if m:key=m.group(1);break
assert key,'Existing Gemini credential unavailable'
parts=[{'text':prompt}]
for p in paths:
 parts.extend([{'text':'File: '+p.stem},{'inline_data':{'mime_type':'audio/wav','data':base64.b64encode(p.read_bytes()).decode()}}])
body=dict(contents=[dict(parts=parts)],generationConfig=dict(temperature=.2,maxOutputTokens=4096))
req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/'+MODEL+':generateContent?key='+key,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
try:
 with urllib.request.urlopen(req,timeout=180) as res:out=json.load(res)
except Exception as e:
 detail=e.read().decode() if isinstance(e,urllib.error.HTTPError) else str(e)
 (E/'error.txt').write_text(type(e).__name__+': '+detail.replace(key,'[REDACTED]'))
 raise SystemExit('Gemini review failed; sanitized evidence saved')
(E/'response.json').write_text(json.dumps(out,indent=2))
answer=''.join(p.get('text','') for p in out.get('candidates',[{}])[0].get('content',{}).get('parts',[]) if not p.get('thought'))
(E/'review.txt').write_text(answer)
usage=out.get('usageMetadata',{});(E/'usage.json').write_text(json.dumps(dict(model=MODEL,usage=usage,cost='Invoice unavailable. Batch estimated below $0.25; token counts recorded.'),indent=2))
print(answer);print('USAGE',json.dumps(usage))
