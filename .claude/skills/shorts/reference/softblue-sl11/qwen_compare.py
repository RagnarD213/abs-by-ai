from full import R,ROOT,SR,wr,dump,sha,pcm
import sys,json,numpy as np
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
import renderq
with renderq.slot('Vacuum direct-reference ownvoice audition',pool='quick',group='SL-11'):
 d=R/'audio/ai-voice';source=d/'qwen.wav';z=C.pcm(str(source));temp=d/'qwen-stereo.wav';wr(temp,np.repeat(z[:,None],2,axis=1));loud=C.ebur(str(temp))[0];gain=-13.1-loud
 for _ in range(3):
  af=f'aresample=48000,volume={gain:.6f}dB,alimiter=limit=0.7855626:attack=5:release=60:level=false:latency=true';x=C.pcm(str(temp),af=af,ac=2);x[:240]*=np.linspace(0,1,240)[:,None];x[-240:]*=np.linspace(1,0,240)[:,None];x=np.pad(x,((0,2880),(0,0)));final=d/'qwen-final.wav';wr(final,x);measure=C.ebur(str(final));delta=-13.1-measure[0]
  if abs(delta)<.15:break
  gain+=delta
 assert -15<=measure[0]<=-13 and measure[1]<=-1
 n=len(x);tail=2880;following=pcm(487.305,498.305);y=np.concatenate([x[:-tail],x[-tail:]*np.linspace(1,0,tail)[:,None]+following[:tail]*np.linspace(0,1,tail)[:,None],following[tail:]]);join=d/'qwen-final-joined.wav';wr(join,y)
 dump(d/'qwen-comparison.json',dict(model='qwen/qwen3-tts',source_sha256=sha(source),file=str(final),sha256=sha(final),filter=af,lufs=measure[0],true_peak=measure[1],join=str(join),join_sha256=sha(join),join_at_seconds=n/SR,ref_range=[487.365,501.224],generation_estimate_upper_usd=1));print('QWEN AUDITION READY',measure,n/SR,flush=True)
