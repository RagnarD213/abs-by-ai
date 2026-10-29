from pathlib import Path
import sys,re,json,base64,urllib.request,urllib.error,subprocess,hashlib
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');E=W/'evidence/listener';E.mkdir(exist_ok=True)
assert not (E/'response.json').exists(),'Already reviewed; do not bill twice'
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
v=W/'review/media/Why I Wear A Mouthpiece For SFC R4 - full 1080p.mp4';raw=W.parent/'round2/audio/cut-raw.wav';paths=[]
for p,name in [(raw,'Source-unprocessed'),(v,'Finished-selected-B')]:
 out=E/(name+'.wav');subprocess.run([C.FF,'-nostdin','-v','error','-y','-i',str(p),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(out)],check=True);paths.append(out)
prompt='''Listen to the full supplied64-second recordings. The first is the untreated source lav on the exact cut; the second is the finished video audio with the speaker's already chosen gentle cleanupB. Do not choose a different sound or invent processing settings. This is a final quality check for newly damaged speech, not a preference ranking. Both contain the same original speaker; level can differ.
Confirm you can actually hear both, quote the actual first sentence and complete final sentence, and say whether any word is missing/cut off. Listen through the entire finished track for unnatural voice change, watery/metallic/chirping artifacts, harshness, pumping, damaged quiet endings and audible edit clicks/gaps. Compare any suspected defect with the untreated source before calling it added damage. Specifically audit audio joins at7.841 and59.092 and candidate transients around5.949,30.444,36.001,45.098,55.198 and61.252; classify natural/source sound versus added click only when audible. Do not infer setting/location or treatment mechanisms. Give exact finished timestamps and severity for confirmed defects, otherwise say none confirmed. State whether it is suitable for the speaker to review as a finished Short. Do not claim publication approval. If uncertain or unable to hear, state that plainly. Keep responseunder600words.'''
(E/'prompt.txt').write_text(prompt)
(E/'binding.json').write_text(json.dumps(dict(model='gemini-3.8-flash',video_sha256=C.sha256(str(v)),inputs=[dict(file=str(p),sha256=C.sha256(str(p))) for p in paths],estimated_max_usd=.25,purpose='Full64s chosenB audio integrity and source comparison'),indent=2))
key=None
for line in Path.home().joinpath('.absbyai-secrets.env').read_text().splitlines():
 m=re.match(r'''\s*(?:export\s+)?GEMINI_API_KEY\s*=\s*["']?([^"'\s]+)''',line)
 if m:key=m.group(1);break
assert key
parts=[dict(text=prompt)]
for p in paths:parts.extend([dict(text=p.stem),dict(inline_data=dict(mime_type='audio/wav',data=base64.b64encode(p.read_bytes()).decode()))])
body=json.dumps(dict(contents=[dict(parts=parts)],generationConfig=dict(temperature=.1,maxOutputTokens=3072))).encode();assert len(body)<20_000_000
req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key='+key,data=body,headers={'Content-Type':'application/json'})
try:
 with urllib.request.urlopen(req,timeout=180) as r:out=json.load(r)
except Exception as e:
 msg=e.read().decode() if isinstance(e,urllib.error.HTTPError) else str(e);(E/'error.txt').write_text(msg.replace(key,'[REDACTED]'));raise SystemExit('Full audio review failed; sanitized evidence saved')
(E/'response.json').write_text(json.dumps(out,indent=2));answer=''.join(p.get('text','') for p in out.get('candidates',[{}])[0].get('content',{}).get('parts',[]) if not p.get('thought'))
(E/'review.txt').write_text(answer);(E/'usage.json').write_text(json.dumps(dict(model='gemini-3.8-flash',usage=out.get('usageMetadata',{}),estimated_under_usd=.25,invoice='unavailable'),indent=2));print(answer);print('USAGE',out.get('usageMetadata'))
