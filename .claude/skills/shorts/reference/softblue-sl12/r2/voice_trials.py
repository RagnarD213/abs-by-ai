"""Two bounded opening auditions: AI own-voice over the approved real curls, then original sentence."""
from pathlib import Path
import sys,json,wave,math,subprocess,os,hashlib
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=Path('/Volumes/Extreme/_edit_work/SL-12/round2');OLD=R.parent/'round1/asset-review'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import packet as P
spec=json.loads((R/'audio/level-manifest.json').read_text());rows=[]
for i,tag in enumerate(['parent-natural','parent-conversational']):
 s=next(x for x in spec['candidates'] if x['id']==tag);d=R/'audio'/('trial-'+tag);d.mkdir(exist_ok=True)
 words=P.ctc(Path(s['solo']),"Here's why lifting weights is mandatory if you're taking weight loss medication.",d/'words.json');P.captions(words,d/'captions.ass')
 nf=math.ceil((s['seconds']+.16)*P.FPS);nb=146;na=round(nf/P.FPS*48000);nbody=round(nb/P.FPS*48000)
 out=R/'review'/f'A-opening-voice-{i+1}.mp4'
 graph=f"[0:v]trim=end_frame={nf},setpts=PTS-STARTPTS,ass='{d/'captions.ass'}'[a];[1:v]trim=end_frame={nb},setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v];[2:a]aresample=48000,apad=whole_len={na},atrim=end_sample={na},asetpts=PTS-STARTPTS[aa];[1:a]aresample=48000,atrim=end_sample={nbody},asetpts=PTS-STARTPTS[bb];[aa][bb]concat=n=2:v=0:a=1[au]"
 if not out.exists():P.run([P.FF,'-v','error','-y','-i',str(OLD/'A-intro-context.mp4'),'-i',str(OLD/'A-training-context.mp4'),'-i',s['solo'],'-filter_complex',graph,'-map','[v]','-map','[au]','-frames:v',str(nf+nb),'-c:v','libx264','-preset','fast','-crf','18','-threads',os.environ.get('RENDERQ_CORES','4'),'-c:a','aac','-b:a','320k','-ar','48000','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)])
 rows.append(dict(number=i+1,id=tag,file=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),voice_seconds=s['seconds'],picture_join_seconds=nf/P.FPS,frames=nf+nb,seconds=(nf+nb)/P.FPS,scope='Opening audition only; AI own-voice over real approved curls, original first complete sentence follows; new AI B-roll motion not generated.'))
 P.run([P.FF,'-v','error','-y','-ss','1.2','-i',str(out),'-frames:v','1',str(R/'review'/f'A-opening-voice-{i+1}.jpg')])
(R/'audio/voice-trial-manifest.json').write_text(json.dumps(rows,indent=2)+'\n');print('VOICE_TRIALS_READY',flush=True)
