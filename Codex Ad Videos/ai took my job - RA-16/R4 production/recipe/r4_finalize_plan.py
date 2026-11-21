"""Correct evidence metadata only; preserve native media and all gate thresholds."""
import json,difflib,re,hashlib
from pathlib import Path
O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra16/round4')
def save(p,x):p.write_text(json.dumps(x,indent=2))
def norm(x):return re.sub('[^a-z0-9]','',x.lower())
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
source=json.load(open(O/'words-native.json'));said=json.load(open(O/'delivered-words.json'));pairs={}
for a,b,n in difflib.SequenceMatcher(None,[norm(x['w']) for x in source],[norm(x['w']) for x in said],autojunk=False).get_matching_blocks():
 for i in range(n):pairs[a+i]=b+i
for aspect in ['9x16','16x9']:
 p=O/f'gate-plan-{aspect}.json';plan=json.load(open(p));states=plan['caption_states'];srt=O/f'captions-{aspect}-evidence.srt'
 srt.write_text('\n\n'.join(f"{i+1}\n{stamp(x['beat'][0])} --> {stamp(x['beat'][1])}\n{x['word']}" for i,x in enumerate(states))+'\n')
 plan['srt']=str(srt);plan['caption_evidence_note']='SRT reconstructed from actual renderer PNG-state intervals, solely to inspect burned phrase-caption runtime and collision. No sidecar is a deliverable. Word-highlight sync code is incompatible with phrase states; see phrase-caption-audit JSON and full picture/audio reviews.'
 # Include the actual opaque picture segments between presenter holds. Omitting them incorrectly makes nonadjacent presenter holds appear adjacent.
 punch=[(x['n0']*1001/30000,x['n1']*1001/30000,2 if x['framing']=='near' else 1,False) for x in json.load(open(O/'picture-segments.json'))]+[(a,b,'opaque',True) for a,b in plan['covered']];punch.sort(key=lambda x:x[0]);plan['punch']=[list(x[:3]) for x in punch];plan['punch_covered']=[x[3] for x in punch]
 audit=[];previous=None;origin=None
 for state in states:
  continuation=previous is not None and previous["word"]==state["word"] and abs(previous["beat"][1]-state["beat"][0])<.001
  if not continuation:origin=state["beat"][0]
  words=state['word'].split();candidates=[i for i,w in enumerate(source) if norm(w['w'])==norm(words[0]) and abs(w['t0']-origin)<.5]
  i=min(candidates,key=lambda i:abs(source[i]['t0']-origin)) if candidates else None
  j=pairs.get(i);audit.append({'phrase':state['word'],'visible':state['beat'],'continuation':continuation,'phrase_origin':origin,'source_first_word':None if i is None else source[i],'delivered_asr_first_word':None if j is None else said[j],'start_offset_ms':None if j is None else round(1000*(origin-said[j]['t']),1)})
  previous=state
 vals=[x['start_offset_ms'] for x in audit if x['start_offset_ms'] is not None]
 save(O/f'phrase-caption-audit-{aspect}.json',{'method':'Actual rendered phrase start matched to delivered-ASR first word through source-to-ASR sequence alignment. This is a phrase-start audit, not a word-highlight PASS. All emitted PNG states independently verified in delivered pixels by graphic_clearance; reviewer checked continuous phrase captions.','video_sha256':plan['evidence_contract']['video_sha256'],'states':len(states),'matched_phrase_starts':len(vals),'max_abs_start_offset_ms':max(map(abs,vals)),'observations':audit})
 save(p,plan);print(aspect,'phrase starts',len(vals),'/',len(states),'max abs offset ms',max(map(abs,vals)))
