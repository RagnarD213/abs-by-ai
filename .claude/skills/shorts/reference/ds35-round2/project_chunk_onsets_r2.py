"""Choose each J2 chunk's first ASR word through full transcript order. Never pair sparse repeated first words directly. All unmatched chunks remain explicit failures."""
from pathlib import Path
import sys,json,re,hashlib,difflib
W=Path(__file__).resolve().parents[1];norm=lambda s:re.sub('[^a-z0-9]','',str(s).lower());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for iid in sys.argv[1:]:
 Q=W/'qa'/iid;p=json.loads((Q/'plan.json').read_text());raw=json.loads((Q/'delivered-ctc.json').read_text());assert raw['video_sha256']==p['video_sha256'];speech=raw['words'];states=p['caption_states'];caps=[];first=[]
 for i,c in enumerate(states):
  toks=c['cue_text'].split();first.append(len(caps));caps.extend(dict(word=w,chunk=i) for w in toks)
 sm=difflib.SequenceMatcher(None,[norm(w['word']) for w in caps],[norm(w['w']) for w in speech],autojunk=False);mapping={a+j:b+j for a,b,n in sm.get_matching_blocks() for j in range(n)};rows=[];projected=[]
 for i,j in enumerate(first):
  c=states[i];c['word']=caps[j]['word'];k=mapping.get(j);r=dict(chunk=i,cue_text=c['cue_text'],caption_first_word_index=j,asr_word_index=k,matched=k is not None)
  if k is not None:r.update(asr_word=speech[k]['w'],onset=speech[k]['t'],caption_start=c['beat'][0],offset_ms=round((c['beat'][0]-speech[k]['t'])*1000,1));projected.append(dict(speech[k],chunk_index=i))
  rows.append(r)
 rec=dict(video_sha256=p['video_sha256'],delivered_ctc_sha256=sha(Q/'delivered-ctc.json'),scope='Every J2 chunk onset, not individual-word highlighting. Matched against full ordered caption/ASR word sequences before selecting first words. Caption timestamps never choose a matching speech word.',caption_words=len(caps),asr_words=len(speech),all_word_matches=len(mapping),all_word_pairs=[dict(caption_word_index=j,asr_word_index=k,caption_word=caps[j]['word'],asr_word=speech[k]['w']) for j,k in sorted(mapping.items())],chunk_onsets=rows,unmatched_chunks=[r for r in rows if not r['matched']])
 f=Q/'chunk-onset-projection.json';f.write_text(json.dumps(rec,indent=1));p.update(delivered_speech_words_all=speech,speech_words=projected,speech_words_evidence=dict(method='delivered_asr',video_sha256=p['video_sha256'],timing_model=raw['timing_model'],ctc_sha256=sha(Q/'delivered-ctc.json'),chunk_projection_sha256=sha(f),scope='All chunk onsets selected by full ordered transcript alignment. Unmatched chunks remain in caption_states; cannot be silently omitted.'));(Q/'plan.json').write_text(json.dumps(p,indent=1));print('CHUNK_PROJECTION',iid,len(projected),'of',len(states),'unmatched',len(rec['unmatched_chunks']),flush=True)
