from pathlib import Path
import base64,json,re,os,urllib.request,time
W=Path(__file__).parent.parent
key=None
for l in open(os.path.expanduser('~/.absbyai-secrets.env')):
 m=re.match(r'\s*(?:export\s+)?GEMINI_API_KEY\s*=\s*[\"\']?([^\"\'\s]+)',l)
 if m:key=m.group(1)
assert key
parts=[{'text':'Review the THREE actual attached videos, labelled B,C,E. Inspect moving picture and listen to their actual audio. Do not simulate a review from filenames or titles. If you cannot inspect media, state that explicitly. For each: transcribe the first and last complete spoken sentence; identify clipped attacks/tails, stray setup words or noises, voice changes at edits, visible presenter jumps, jerky tracking, hair clipping, wrong food/action under the narration, unreadable or mismatched graphics/captions, black/frozen frames. Evaluate at normal playback speed. Report every real issue with exact video timestamp and correction. Say separately what you actually observed and any inability to watch/hear. No editing or generating content. Return a compact factual review for each video, verdict SHIP/REVISE/UNABLE, and remaining limitations.'}]
for S in 'BCE':
 p=W/f'review/candidates/{S}-review.mp4';parts += [{'text':'VIDEO '+S},{'inline_data':{'mime_type':'video/mp4','data':base64.b64encode(p.read_bytes()).decode()}}]
body={'contents':[{'parts':parts}],'generationConfig':{'temperature':0.1,'maxOutputTokens':5500}}
rq=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key='+key,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
try:
 r=json.load(urllib.request.urlopen(rq,timeout=240));d={'model':'gemini-3.1-pro-preview','usage':r.get('usageMetadata',{}),'answer':''.join(x.get('text','') for x in r.get('candidates',[{}])[0].get('content',{}).get('parts',[])),'estimated_cost_usd':0.50,'actual_charge':'not returned','media':'actual full540p videos B C E from exact masters'}
except Exception as e:d={'error':str(e).replace(key,'<secret>')}
(W/'audit/moving-review.json').write_text(json.dumps(d,indent=2));print(d.get('answer',d.get('error')),flush=True)
