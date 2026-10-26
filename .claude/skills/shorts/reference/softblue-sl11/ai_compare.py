from full import R,ROOT,SR,wr,dump,sha,pcm,MASTER
import sys,json,numpy as np
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
import renderq
D=R/'audio/ai-voice'
with renderq.slot('Vacuum ownvoice audition leveling',pool='quick',group='SL-11'):
 cfg=json.loads((R/'audio/yeti-test/comparisons.json').read_text());target=cfg['reference_speech_rms'];cap=cfg['reference_peak'];follow=pcm(487.305,498.305);rows=[]
 def speech(x):
  f=C.frames(x,2048,1024);v=np.sqrt((f*f).mean(1)+1e-12);return float(20*np.log10(np.sqrt((v[v>np.percentile(v,60)]**2).mean())))
 for tag in ['natural','brisk']:
  p=D/(tag+'.wav');x=C.pcm(str(p));gain=target-speech(x)
  for _ in range(8):
   af=f'aresample=48000,volume={gain:.6f}dB,alimiter=limit={cap:.7f}:attack=5:release=60:level=false:latency=true';z=C.pcm(str(p),af=af);delta=target-speech(z)
   if abs(delta)<.15:break
   gain+=delta
  assert abs(z).max()<.79
  # Preserve generated words and native pacing, tiny protected edgefades only.
  z[:240]*=np.linspace(0,1,240);z[-240:]*=np.linspace(1,0,240)
  z=np.pad(z,(0,2880));solo=D/(tag+'-leveled.wav');wr(solo,np.repeat(z[:,None],2,axis=1))
  overlap=2880;pickup=np.repeat(z[:,None],2,axis=1);joined=np.concatenate([pickup[:-overlap],pickup[-overlap:]*np.linspace(1,0,overlap)[:,None]+follow[:overlap]*np.linspace(0,1,overlap)[:,None],follow[overlap:]])
  j=D/(tag+'-joined.wav');wr(j,joined);rows.append(dict(tag=tag,solo=str(solo),join=str(j),join_at_seconds=len(z)/SR,filter=af,speech_rms=speech(z),peak_db=20*np.log10(abs(z).max()),join_sha256=sha(j)))
 dump(D/'comparison-manifest.json',dict(reference=str(MASTER),target_speech_rms=target,candidates=rows));print('AI AUDITIONS READY',[(r['tag'],r['join_at_seconds']) for r in rows],flush=True)
