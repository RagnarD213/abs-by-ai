"""Audited literal transcript of actual AAC, then independent MMS forced alignment.
Raw Whisper/CTC and caption timings stay untouched. Corrections cite actual delivered AV listens.
"""
from pathlib import Path
import os,sys,json,re,hashlib,wave
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ.setdefault(k,'1')
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('Dad Bod actual final AAC audited literal alignment',pool='heavy')
import torch,torchaudio,numpy as np
torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','4')))
b=torchaudio.pipelines.MMS_FA;m=b.get_model().eval();tokenizer=b.get_tokenizer();aligner=b.get_aligner()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
nums={'15':'fifteen','17':'seventeen','38':'thirty eight','40':'forty'}
for v in sys.argv[1:]:
 q=W/'qa'/v;out=q/'audited-delivered-mms.json'
 assert not out.exists(),out
 ar=json.loads((q/'delivered-asr.json').read_text());raw=[x['w'] for x in ar['words']];words=[];corrections=[];i=0
 while i<len(raw):
  if i==10:
   assert raw[i:i+2]==['that','body'];words+=['the','dad','bod.','Let','me'];corrections.append(dict(raw_indices=[10,12],raw=raw[10:12],audited=['the','dad','bod.','Let','me'],evidence='actual final AAC editor AV window1 literal transcript'))
   i+=2;continue
  if i==21:
   words.append('Sure.');corrections.append(dict(raw_indices=[21,21],raw=[],audited=['Sure.'],evidence='actual final AAC editor AV window1 literal transcript'))
  if v=='off_the_cuff' and i==97:
   assert raw[i].lower()=='quickly';words.append('Basically');corrections.append(dict(raw_indices=[97,98],raw=raw[i:i+1],audited=['Basically'],evidence='actual final AAC editor AV window2 literal transcript'));i+=1;continue
  if v=='off_the_cuff' and i==105:
   words.append('bod,');corrections.append(dict(raw_indices=[105,105],raw=[],audited=['bod,'],evidence='actual final AAC editor AV window2 literal transcript'))
  if raw[i].lower()=='six' and i+1<len(raw) and raw[i+1].lower().strip('.,')=='-pack':
   words.append('six-pack');corrections.append(dict(raw_indices=[i,i+2],raw=raw[i:i+2],audited=['six-pack'],evidence='compound word token normalization only'));i+=2;continue
  words.append(raw[i]);i+=1
 txt=[' '.join(nums.get(t,t) for t in re.sub("[^a-z0-9' ]",' ',x.lower()).split()) for x in words]
 wav=q/'ctc-delivered16.wav'
 with wave.open(str(wav)) as f:audio=torch.from_numpy(np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(np.float32)/32768.)
 assert sha(W/'review/media'/('dad-bod-r2-'+v+'.mp4'))==ar['video_sha256']
 with torch.inference_mode():em,_=m(audio.unsqueeze(0))
 flat=[];owners=[]
 for k,t in enumerate(txt):
  for token in t.split():flat.append(token);owners.append(k)
 aligned=aligner(em[0],tokenizer(flat));ratio=len(audio)/em.shape[1]/16000;spans=[[] for _ in words]
 for k,sp in zip(owners,aligned):spans[k].extend(sp)
 rows=[dict(w=w,t=round(sp[0].start*ratio,5),e=round(sp[-1].end*ratio,5),score=float(np.mean([x.score for x in sp]))) for w,sp in zip(words,spans)]
 rec=dict(video_sha256=ar['video_sha256'],wav_sha256=sha(wav),raw_asr_sha256=sha(q/'delivered-asr.json'),raw_ctc_sha256=sha(q/'delivered-ctc.json'),method='Full actual AAC medium.en transcript corrected only from literal delivered-file AV listening, aligned to the same full AAC waveform by MMS_FA. No expected captions or caption times used for alignment.',corrections=corrections,words=rows)
 out.write_text(json.dumps(rec,indent=1));print('AUDITED_ACTUAL_AAC_ALIGNMENT',v,len(rows),flush=True)
