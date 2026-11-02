from pathlib import Path
import sys,json,subprocess,os
D=Path(__file__).parent;sys.path.insert(0,str(D));import batch as Bt,lib
W=Path(Bt.WORK);FF=lib.FF
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');HF=ROOT/'.claude/skills/_shared/hyperframes';sys.path.insert(0,str(HF))
MASTER=ROOT/"claude edited long form content/11 - When Calories Don't Matter For Fat Loss/When Calories Don't Matter For Fat Loss | claude round 4 | 16x9 | RO-11.mp4"
def run(c):subprocess.run(c,check=True)
if not (W/'master_audio.wav').exists():run([FF,'-v','error','-y','-i',str(MASTER),'-vn','-af','aresample=async=1:min_hard_comp=0.005:first_pts=0','-ar','48000','-ac','2','-c:a','pcm_s16le',str(W/'master_audio.wav')])
# This is a short, source-graded insert from the approved parent; retain its whole height.
if not (W/'clips/eggs-parent.mp4').exists():run([FF,'-v','error','-y','-ss','376.243','-i',str(MASTER),'-t','4.237','-an','-c:v','libx264','-crf','16','-preset','fast','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(W/'clips/eggs-parent.mp4')])
Bt.cmd_audio('A');print('Audio pieces ready',flush=True)
import wave,numpy as np
x=wave.open(str(W/'master_audio.wav'));sr=x.getframerate();a=np.frombuffer(x.readframes(x.getnframes()),'<i2').reshape(-1,2)/32768
for t in [318.35,367.38,376.24,384.94]:
 rows=[]
 for s in np.arange(t-.16,t+.161,.02):
  z=a[int(s*sr):int((s+.02)*sr)];rows.append([round(s,3),round(float(20*np.log10(np.sqrt(np.mean(z*z))+1e-10)),1)])
 print('CUT_LEVELS',t,rows,flush=True)
# Each new graphic uses the existing HyperFrames templates.
import hfbuild as H,vertical as V
S='A';dur=Bt.timeline(S)[1];out=W/'build/A/hf';out.mkdir(parents=True,exist_ok=True)
size=88
while max(H.text_w(l,size) for l in Bt.P.TITLE[S][1])>952:size-=2
c=dict(id='header-A',dur=dur+1.7,drift=-2,canvas=[1080,310],line_px=size,accent=[64,50,7],eyebrow=dict(x=88,y=44,px=34,s='FAT LOSS'),lines=[dict(x=64,y=86+96*i,s=l,at=-1) for i,l in enumerate(Bt.P.TITLE[S][1])])
scenes=[(HF/'title-card/title-card.template.htm',c,())]
if not (out/'renders/header-A.mov').exists():V.build(scenes,out,render=True,snap=2.0)
scenes,meta=V.title_scenes('protein-study',0,11.7,'McMASTER, 2016','Same Calories. Different Results.',[])
c=scenes[0][1];c.update(canvas=[1080,1610],dur=11.7,drift=-3,accent=[80,85,78],eyebrow=dict(x=80,y=118,px=30,s='McMASTER, 2016'),line_px=62,lines=[dict(x=76,y=210,s='Same Calories.',at=.10),dict(x=76,y=290,s='Different Results.',at=.10)],rows=[dict(x=80,y=440,w=920,h=140,s='High Protein: 10.5 lb Fat Lost',t=.25),dict(x=80,y=620,w=920,h=140,s='And 2.5 lb Muscle Gained',t=3.45),dict(x=80,y=800,w=920,h=140,s='Lower Protein: 8 lb Fat Lost',t=5.65),dict(x=80,y=980,w=920,h=140,s='No Muscle Gained',t=8.45)],row_px=42,row_ty=43)
if not (out/'renders/protein-study.mov').exists():V.build(scenes,out,render=True,snap=10.5)
print('PREP COMPLETE',flush=True)
