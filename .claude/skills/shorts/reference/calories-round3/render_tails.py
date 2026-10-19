from pathlib import Path
import sys,subprocess,json
P=Path(__file__).parent;W=P.parent;R='/Users/danielrose/Documents/Claude/Projects/Abs By AI'
sys.path[:0]=[str(P),R+'/.claude/skills/_shared']
import batch as B,buildcap,cap_local,cv2
B.cv2=cv2
for S in 'AD':
 buildcap.wait('Calories R3 independent tail '+S)
 s=B.Short(S);start=s.shots[0]['f1'];d=Path(s.d);out=d/'independent-tail.mp4'
 e=subprocess.Popen([B.lib.FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate',B.FPSS,'-i','-','-an','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 for i in range(start,s.N):
  f,sh=s.picture(i);e.stdin.write(s.finish(f,sh,i).tobytes())
 e.stdin.close();assert e.wait()==0;s.close()
 (d/'independent-tail.json').write_text(json.dumps({'start_frame':start,'end_frame_exclusive':s.N,'frames':s.N-start,'file':str(out),'status':'independent assembly part, not complete Short or review delivery; no final stamps'},indent=2));print('TAIL READY',S,start,s.N,flush=True)
