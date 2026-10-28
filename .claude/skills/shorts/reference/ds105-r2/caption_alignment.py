from pathlib import Path
import json,re,difflib,numpy as np
W=Path(__file__).resolve().parents[1];E=W/'evidence/checks';h=json.load(open(E/'FULL-delivered-words.json'))['words'];w=json.load(open(W/'records/full-words.json'));c=json.load(open(W/'records/FULL-captions.json'));norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
# Alignment in full transcript order; punctuation and split ASR spellings normalize without inventing words.
def tokenize(rows,st,en):
 out=[];i=0
 while i<len(rows):
  s=norm(rows[i]['w']);n=1
  if i+1<len(rows) and s=='weight' and norm(rows[i+1]['w'])=='lifting':s='weightlifting';n=2
  elif i+1<len(rows) and s in ['jiu','ju'] and norm(rows[i+1]['w'])=='jitsu':s='jujitsu';n=2
  elif i+1<len(rows) and s in ['6packabs','sixpackabs'] and norm(rows[i+1]['w'])=='com':s='sixpackabscom';n=2
  out.append(dict(s=s,a=rows[i][st],b=rows[i+n-1][en],i=i));i+=n
 return out
A=tokenize(w,'t0','t1');B=tokenize(h,'t','e');maps={}
for op,a,b,x,y in difflib.SequenceMatcher(None,[t['s'] for t in A],[t['s'] for t in B],autojunk=False).get_opcodes():
 if op=='equal':
  for q,z in zip(range(a,b),range(x,y)):maps[A[q]['i']]=B[z]
rows=[]
for cue in c:
 i=min(range(len(w)),key=lambda i:abs(w[i]['t0']-cue['t0']));hh=maps.get(i)
 rows.append(dict(t=cue['t0'],caption=cue['text'],asr_onset=hh['a'] if hh else None,offset_ms=round((cue['t0']-hh['a'])*1000,1) if hh else None))
valid=[q['offset_ms'] for q in rows if q['offset_ms'] is not None];rec=dict(video_sha256=json.load(open(E/'FULL-delivered-words.json'))['sha256'],method='Global sequence-ordered alignment of caption chunk FIRST word to fresh local delivered ASR; split words normalized. This is an additional ASR check, not independent acoustic alignment or a replacement/waiver of the shared gate energy-sync row.',cues=len(c),matched=len(valid),unmatched=len(c)-len(valid),median_ms=float(np.median(valid)),max_absolute_ms=max(abs(x) for x in valid),over150ms=[q for q in rows if q['offset_ms'] is not None and abs(q['offset_ms'])>150],rows=rows)
(E/'caption-asr-alignment.json').write_text(json.dumps(rec,indent=2));print({k:v for k,v in rec.items() if k not in ['rows','method']})
