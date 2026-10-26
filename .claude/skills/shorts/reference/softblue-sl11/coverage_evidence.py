from full import R,ROOT,FF,FPS,sha,dump,E
import json,subprocess,numpy as np
import renderq
with renderq.slot('Vacuum C alternate footage source verification',pool='quick',group='SL-11'):
 d=R/'build/C';v=d/'Vacuum-C-R1.mp4';T=json.loads((d/'timeline.json').read_text());shots=json.loads((d/'shots.json').read_text());demo=[s for s in shots if s['kind']=='demo'];frames=[]
 for sh in demo:frames.extend(range(sh['f0']+15,sh['f1'],30))
 select='+'.join(f'eq(n,{n})' for n in frames)
 cmd=[FF,'-nostdin','-v','error','-threads','1','-filter_threads','1','-i',str(v),'-vf',f'select={select},scale=in_color_matrix=bt709:in_range=tv,format=rgb24,crop=620:700:230:360,scale=100:100:flags=lanczos','-vsync','0','-f','rawvideo','-']
 # select expressions contain commas, so escape the expression as one filter argument.
 cmd[cmd.index('-vf')+1]=f"select='{select}',scale=in_color_matrix=bt709:in_range=tv,format=rgb24,crop=620:700:230:360,scale=100:100:flags=lanczos"
 raw=subprocess.check_output(cmd);actual=np.frombuffer(raw,np.uint8).reshape(-1,100,100,3);assert len(actual)==len(frames)
 rows=[]
 for n,a in zip(frames,actual):
  sh=next(x for x in demo if x['f0']<=n<x['f1']);x,y,w,h=sh['crop'];time=sh['raw0']+(n-sh['f0'])/FPS
  vf=f"scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le,lut3d=file='{sh['lut']}':interp=tetrahedral,crop={w}:{h}:{x}:{y},scale=1080:1610:flags=lanczos,format=rgb24,crop=620:700:230:50,scale=100:100:flags=lanczos"
  b=subprocess.check_output([FF,'-nostdin','-v','error','-threads','1','-filter_threads','1','-ss',str(max(0,time-2)),'-i',E.src(sh['roll']),'-ss',str(min(2,time)),'-frames:v','1','-vf',vf,'-f','rawvideo','-']);b=np.frombuffer(b,np.uint8).reshape(100,100,3);ncc=float(np.corrcoef(a.reshape(-1),b.reshape(-1))[0,1]);rows.append(dict(frame=n,output=n/FPS,roll=sh['roll'],source_seconds=time,ncc=ncc))
 coverage=sum(s['f1']-s['f0'] for s in demo)/T['frames']
 report=dict(video=str(v),sha256=sha(v),method='Fresh actual MP4 nativeframe upperbody ROI vs independently re-decoded original C1625 through locked parent LUT and crop; no overlay within ROI. Continuous demo coverage from hash-bound exactshots, sampled every30nativeframes as source-presence verification, combined with every-boundary independent native/fullmoving audit.',frames=T['frames'],alternate_source_frames=sum(s['f1']-s['f0'] for s in demo),coverage=coverage,main_narration_rolls=sorted(set(s['roll'] for s in shots if s['kind']=='talk')),alternate_source_rolls=sorted(set(s['roll'] for s in demo)),verified_samples=rows,min_ncc=min(z['ncc'] for z in rows),palette_gate_original_result='0% with source exercising on the same pool/roof palette; original FAIL retained',threshold_not_changed=True)
 dump(d/'coverage-source-evidence.json',report);assert report['min_ncc']>.97,report['min_ncc'];assert coverage>.3;print('VERIFIED ALTERNATE FOOTAGE',coverage,len(rows),report['min_ncc'],flush=True)
