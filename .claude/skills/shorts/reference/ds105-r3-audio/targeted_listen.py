from pathlib import Path
import json,re,base64,urllib.request,urllib.error,shutil
W=Path(__file__).resolve().parents[1];E=W/'evidence/targeted-listener';E.mkdir(exist_ok=True)
assert not (E/'response.json').exists()
mapping={'sample-17':'B','sample-83':'A','sample-42':'C'}
paths=[W/'review/media/A.wav']
for label,k in mapping.items():
 p=E/(label+'.wav');shutil.copyfile(W/f'review/media/{k}.wav',p);paths.append(p)
prompt='''Perform a targeted audio quality check. First audio is the CURRENT MIX, used as an audible baseline. Three anonymously labeled audition files follow, with identical speech timing and equal integrated volume. Some inputs may be identical; do not force differences. Ignore recording location and do not speculate about microphones, compressors or processing settings. Evaluate audible evidence only.
An earlier reviewer flagged watery/chirping sound near excerpt3.8–4.2s and7.5s, harsh consonants, and abrupt damage to the final "nose" near11.6–11.9s in one unspecified candidate. Determine for EACH anonymous file whether those are real newly introduced defects versus the current reference or ordinary source articulation/background. Quote the final complete words. A difference in background noise alone is not damaged speech. Report any lost phoneme, unnatural gating/pumping, and changed voice identity; distinguish slight texture from a clear defect. Give a naturalness verdict: acceptable for a human audition / must repair. If no meaningful audible distinction exists from current, say so. Avoid broad rankings. Keep the answer under600 words. If audio cannot be heard, say so explicitly.'''
(E/'prompt.txt').write_text(prompt)
import hashlib
(E/'binding.json').write_text(json.dumps(dict(mapping=mapping,model='gemini-3.8-flash',purpose='Reconcile concrete claimed defects and include an identical reference control',inputs=[dict(file=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]),indent=2))
key=None
for line in Path.home().joinpath('.absbyai-secrets.env').read_text().splitlines():
 m=re.match(r'''\s*(?:export\s+)?GEMINI_API_KEY\s*=\s*["']?([^"'\s]+)''',line)
 if m:key=m.group(1);break
assert key
parts=[dict(text=prompt)]
for i,p in enumerate(paths):parts.extend([dict(text='CURRENT REFERENCE' if i==0 else p.stem),dict(inline_data=dict(mime_type='audio/wav',data=base64.b64encode(p.read_bytes()).decode()))])
req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key='+key,data=json.dumps(dict(contents=[dict(parts=parts)],generationConfig=dict(temperature=.1,maxOutputTokens=3072))).encode(),headers={'Content-Type':'application/json'})
try:
 with urllib.request.urlopen(req,timeout=180) as r:out=json.load(r)
except Exception as e:
 detail=e.read().decode() if isinstance(e,urllib.error.HTTPError) else str(e)
 (E/'error.txt').write_text(detail.replace(key,'[REDACTED]'));raise SystemExit('Targeted listen failed; sanitized evidence saved')
(E/'response.json').write_text(json.dumps(out,indent=2));answer=''.join(p.get('text','') for p in out.get('candidates',[{}])[0].get('content',{}).get('parts',[]) if not p.get('thought'))
(E/'review.txt').write_text(answer);(E/'usage.json').write_text(json.dumps(out.get('usageMetadata',{}),indent=2));print(answer);print('USAGE',out.get('usageMetadata'))
