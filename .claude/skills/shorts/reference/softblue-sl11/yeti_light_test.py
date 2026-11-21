from full import R,ROOT,SR,wr,dump,sha,rd,pcm
import sys,json,numpy as np,subprocess
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/audio'));import common as C
import renderq
with renderq.slot('Vacuum original Yeti light-touch diagnostic',pool='quick',group='SL-11'):
 d=R/'audio/yeti-test/light-finish';d.mkdir(exist_ok=True);source=R/'audio/yeti-test/take3-fit-input.wav';out=d/'Yeti-original-take3-gentle-leveling.wav'
 cmd=['python3',str(ROOT/'.claude/skills/_shared/audio/voice_chain.py'),'--in',str(source),'--out',str(out),'--work',str(d/'chain'),'--finish-only','--target','-14','--tp','-2.5','--oversample','4']
 with open(d/'chain.log','w') as log:p=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 assert p.returncode==0,p.returncode
 x=rd(out);tail=2880;following=pcm(487.305,498.305);n=len(x);mix=np.concatenate([x[:-tail],x[-tail:]*np.linspace(1,0,tail)[:,None]+following[:tail]*np.linspace(0,1,tail)[:,None],following[tail:]]);join=d/'Yeti-gentle-leveling-joined-to-film.wav';wr(join,mix)
 dump(d/'diagnostic.json',dict(purpose='Compare less processed original Yeti recording; approved B audio untouched',source_sha256=sha(source),output_sha256=sha(out),join_sha256=sha(join),raw_lufs_tp_lra=C.ebur(str(source)),new_lufs_tp_lra=C.ebur(str(out)),old_before_final_attenuation_lufs_tp_lra=C.ebur(str(R/'audio/yeti-test/take3-peak-safe.wav')),chain='Shared voice_chain finish-only: measured gain and peak limiter; noEQ/dereverb/gate/expander/compressor',current_input_device='system_profiler2026-10-26: YetiStereoMicrophone defaultinput; historical QuickTime capturedevice notembeddedinAIFF'))
 print('YETI LIGHT TEST READY',str(join),flush=True)
