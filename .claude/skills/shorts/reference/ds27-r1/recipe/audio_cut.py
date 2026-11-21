from pathlib import Path
import subprocess,json,sys,os
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];F=str(R/'Media/video_edit/bin/ffmpeg');A=R/'.claude/skills/_shared/audio';S=json.load(open(W/'source.json'));P=json.load(open(W/'edl.json'));O=W/'build';O.mkdir(exist_ok=True);os.environ['GATE_GROUP']='DS-27';os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH']
def ff(args):subprocess.run([F,'-v','error','-nostdin','-y']+list(map(str,args)),check=True)
parts=[]
for i,p in enumerate(P):
 out=O/f'voice-source-{i}.wav';ff(['-ss',p['start'],'-i',S['path'],'-t',p['frames']/(30000/1001),'-map',S['lav']['map'],'-af',S['lav']['filter'],'-ac',1,'-ar',48000,out]);parts.append(out)
cat=O/'audio-concat.txt';cat.write_text(''.join("file '"+str(p)+"'\n" for p in parts));ff(['-f','concat','-safe',0,'-i',cat,'-c','copy',W/'untreated-cut.wav'])
cmd=[sys.executable,str(A/'voice_chain.py'),'--in',str(W/'untreated-cut.wav'),'--out',str(W/'voice.wav'),'--eq','anull','--no-expander-because','C1719 blind comparisons: expanded default and bass clip word tails; original repeatedly more natural than processed finalists. Preserve source timbre for Dan to choose.','--oversample','4','--work',str(W/'voice-work')]
p=subprocess.run(cmd,capture_output=True,text=True);(W/'evidence/voice-cut.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr[-1000:]
(W/'joins.json').write_text(json.dumps([p['out'] for p in P[1:]]));print('CUT VOICE READY',flush=True)
subprocess.run([sys.executable,str(A/'seamscan.py'),str(W/'voice.wav'),'--joins',str(W/'joins.json'),'--out',str(W/'evidence/seamscan.json')],check=True)
