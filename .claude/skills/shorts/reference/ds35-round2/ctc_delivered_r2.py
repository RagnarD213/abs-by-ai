"""Retiming actual delivered ASR with independent Wav2Vec2 CTC, adapted from maintained shorts/reference/zeeshan-master/gate/ctc_delivered.py. Never reads expected captions."""
from pathlib import Path
import os,sys,json,subprocess,hashlib,re,wave
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ.setdefault(k,'1')
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('DS35 delivered-ASR independent CTC timing '+','.join(sys.argv[1:]),pool='heavy')
import numpy as np,torch,torchaudio
from qa_full_r2 import sha,video
for version in sys.argv[1:]:
 if not (W/'qa'/version/'audio-exact-provenance.json').exists():subprocess.run([sys.executable,str(W/'recipe/audio_exact_r2.py'),version],check=True)
 if not (W/'qa'/version/'audio-editor_av/coverage.json').exists():subprocess.run([sys.executable,str(W/'recipe/listen_full_audio_r2.py'),'editor_av',version],check=True)
SR=16000;torch.set_num_threads(int(os.environ.get('RENDERQ_CORES','4')));bundle=torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H;model=bundle.get_model().eval();L={c:i for i,c in enumerate(bundle.get_labels())}
NUM={str(i):s for i,s in enumerate(['ZERO','ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE','THIRTEEN','FOURTEEN','FIFTEEN','SIXTEEN','SEVENTEEN','EIGHTEEN','NINETEEN','TWENTY'])};NUM.update({'30':'THIRTY','38':'THIRTY EIGHT','40':'FORTY','41':'FORTY ONE','90':'NINETY','100':'ONE HUNDRED'})
def norm(w):
 w=w.replace('%',' PERCENT');w=re.sub(r"[^A-Za-z0-9' ]",' ',w).upper();w=' '.join(NUM.get(t,t) for t in w.split());assert not re.search('[0-9]',w),('Unsupported number in actual ASR',w);return re.sub(r"[^A-Z' ]",'',w).strip()
for iid in sys.argv[1:]:
 Q=W/'qa'/iid;v=video(iid);plan=json.loads((Q/'plan.json').read_text());ar=json.loads((Q/'delivered-asr.json').read_text());assert ar['video_sha256']==plan['video_sha256']==sha(v)
 if (Q/'delivered-ctc.json').exists() and json.loads((Q/'delivered-ctc.json').read_text()).get('video_sha256')==ar['video_sha256']:continue
 wav=Q/'ctc-delivered16.wav';subprocess.run([str(R/'Media/video_edit/bin/ffmpeg'),'-v','error','-y','-i',str(v),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(wav)],check=True)
 with wave.open(str(wav)) as f:audio=torch.from_numpy(np.frombuffer(f.readframes(f.getnframes()),'<i2').astype(np.float32)/32768.)
 toks=[];owners=[]
 for k,c in enumerate(ar['words']):
  text=norm(c['w']);assert text
  for ch in text.replace(' ','|'):
   assert ch in L,ch;toks.append(L[ch]);owners.append(k)
  toks.append(L['|']);owners.append(-1)
 toks=toks[:-1];owners=owners[:-1]
 with torch.inference_mode():em,_=model(audio.unsqueeze(0));em=torch.log_softmax(em,-1)
 ali,sc=torchaudio.functional.forced_align(em,torch.tensor([toks],dtype=torch.int32),blank=0);spans=torchaudio.functional.merge_tokens(ali[0],sc[0].exp());assert len(spans)==len(toks),(iid,len(spans),len(toks));ratio=len(audio)/em.shape[1]/SR;per={}
 for j,sp in enumerate(spans):
  assert int(sp.token)==toks[j];k=owners[j]
  if k<0:continue
  per.setdefault(k,dict(t=sp.start*ratio,e=sp.end*ratio,scores=[]));per[k]['e']=sp.end*ratio;per[k]['scores'].append(float(sp.score))
 out=[dict(w=c['w'],t=round(per[k]['t'],4),e=round(per[k]['e'],4),ctc_mean_score=float(np.mean(per[k]['scores'])),asr_word_index=k) for k,c in enumerate(ar['words'])];assert len(out)==len(ar['words'])
 rec=dict(video_sha256=ar['video_sha256'],asr_sha256=sha(Q/'delivered-asr.json'),wav_sha256=sha(wav),timing_model='torchaudio WAV2VEC2_ASR_BASE_960H',method='Actual delivered ASR transcript aligned to actual delivered audio in one complete excerpt window, independently of all caption timings. Raw Whisper ASR unchanged.',words=out)
 (Q/'delivered-ctc.json').write_text(json.dumps(rec,indent=1));p=json.loads((Q/'plan.json').read_text());assert p['video_sha256']==rec['video_sha256'];p.update(speech_words=out,speech_words_evidence=dict(method='delivered_asr',video_sha256=rec['video_sha256'],asr_sha256=rec['asr_sha256'],timing_model=rec['timing_model'],ctc_sha256=sha(Q/'delivered-ctc.json')));(Q/'plan.json').write_text(json.dumps(p,indent=1));print('DELIVERED_CTC_COMPLETE',iid,len(out),flush=True)
