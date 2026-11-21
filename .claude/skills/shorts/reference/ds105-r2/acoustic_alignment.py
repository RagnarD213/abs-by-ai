from pathlib import Path
import os,sys,json,subprocess,re,wave,hashlib
import numpy as np
import torch,torchaudio
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');E=W/'evidence/checks';F=R/'Media/video_edit/bin/ffmpeg';torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','4')));v=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p.mp4';wav=E/'FULL-ctc16.wav'
subprocess.run([str(F),'-v','error','-y','-i',str(v),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)],check=True)
with wave.open(str(wav)) as q:a=np.frombuffer(q.readframes(q.getnframes()),dtype='<i2').astype(np.float32)/32768
b=torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H;model=b.get_model().eval();L={c:i for i,c in enumerate(b.get_labels())};words=json.load(open(W/'records/full-words.json'));pieces=json.load(open(W/'edit-plan.json'))['pieces'];out=[]
def norm(w):
 w={'20':'TWENTY','sixpackabs.com':'SIX PACK ABS DOT COM'}.get(w,w)
 return re.sub("[^A-Z' ]",'',w.upper().replace('-',' ')).strip()
for k,p in enumerate(pieces):
 start=p['out'];end=start+p['duration'];ww=[(j,x) for j,x in enumerate(words) if start<=x['t0']<end];x=torch.from_numpy(a[round(start*16000):round(end*16000)].copy())
 with torch.inference_mode():em,_=model(x.unsqueeze(0));em=torch.log_softmax(em,-1)
 toks=[];owners=[]
 for j,w in ww:
  txt=norm(w['w']);assert txt
  for ch in txt.replace(' ','|'):toks.append(L[ch]);owners.append(j)
  toks.append(L['|']);owners.append(-1)
 toks=toks[:-1];owners=owners[:-1];ali,sc=torchaudio.functional.forced_align(em,torch.tensor([toks],dtype=torch.int32),blank=0);spans=torchaudio.functional.merge_tokens(ali[0],sc[0].exp());assert len(spans)==len(toks);ratio=len(x)/em.shape[1]/16000;per={}
 for q,sp in enumerate(spans):
  assert int(sp.token)==toks[q];j=owners[q]
  if j<0:continue
  per.setdefault(j,dict(t=start+sp.start*ratio,e=start+sp.end*ratio,scores=[]));per[j]['e']=start+sp.end*ratio;per[j]['scores'].append(float(sp.score))
 for j,w in ww:out.append(dict(w=w['w'],word_index=j,t=round(per[j]['t'],4),e=round(per[j]['e'],4),score=float(np.mean(per[j]['scores'])),caption_map_t=w['t0']))
 print('CTC_PIECE',k,'words',len(ww),flush=True)
rec=dict(video_sha256=hashlib.sha256(v.read_bytes()).hexdigest(),timing_model='torchaudio WAV2VEC2_ASR_BASE_960H cached local model',method='Independent acoustic timing of exact previously source-confirmed transcript on delivered AAC, per selected source piece. This is forced alignment, not independent transcription or perceptual listening. No paid calls.',words=out)
(E/'FULL-ctc-words.json').write_text(json.dumps(rec,indent=2));rows=[]
for c in json.load(open(W/'records/FULL-captions.json')):
 q=min(out,key=lambda x:abs(x['caption_map_t']-c['t0']));rows.append(dict(caption=c['text'],t=c['t0'],acoustic_onset=q['t'],score=q['score'],offset_ms=round((c['t0']-q['t'])*1000,1)))
rr=dict(video_sha256=rec['video_sha256'],method=rec['method'],rows=rows,flags=[q for q in rows if abs(q['offset_ms'])>150]);(E/'caption-ctc-alignment.json').write_text(json.dumps(rr,indent=2));print('CTC_FLAGS',rr['flags'],flush=True)
