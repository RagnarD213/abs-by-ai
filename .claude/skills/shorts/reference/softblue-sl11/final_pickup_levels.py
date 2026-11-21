from full import R,ROOT,SR,wr,dump,sha,pcm
import sys,json,numpy as np
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
import renderq
with renderq.slot('Vacuum equal-loudness final pickup auditions',pool='quick',group='SL-11'):
 D=R/'audio/ai-voice';following=pcm(487.305,498.305);rows=[]
 for tag,src in [('natural',D/'natural-leveled.wav'),('brisk',D/'brisk-leveled.wav'),('yeti',R/'audio/yeti-test/take3-peak-safe.wav')]:
  loud,tp,lra=C.ebur(str(src));gain=-13.1-loud;x=C.pcm(str(src),ac=2)*10**(gain/20);p=D/(tag+'-final.wav');wr(p,x);actual=C.ebur(str(p));assert -15<=actual[0]<=-13 and actual[1]<=-1
  tail=2880;n=len(x);mix=np.concatenate([x[:-tail],x[-tail:]*np.linspace(1,0,tail)[:,None]+following[:tail]*np.linspace(0,1,tail)[:,None],following[tail:]])
  j=D/(tag+'-final-joined.wav');wr(j,mix);rows.append(dict(tag=tag,file=str(p),sha256=sha(p),source=str(src),source_sha256=sha(src),constant_gain_db=gain,lufs=actual[0],true_peak=actual[1],lra=actual[2],join=str(j),join_sha256=sha(j),join_at_seconds=n/SR))
 dump(D/'final-level-manifest.json',dict(method='Constant attenuation only on the new pickup to -13.1LUFS, original film audio untouched. All three choices equal integrated loudness; no new EQ, compression, resampling, dereverb or edits.',candidates=rows))
 choice=R/'audio/pickup-choice.json';d=json.loads(choice.read_text());d['file']=str(D/'natural-final.wav');d['level_manifest']=str(D/'final-level-manifest.json');dump(choice,d);print('FINAL AUDITIONS READY',[(r['tag'],r['lufs'],r['true_peak']) for r in rows],flush=True)
