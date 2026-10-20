from pathlib import Path
import subprocess,json,sys
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg')
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R4 selected-source Balanced audio')
P=json.loads((W/'plan.json').read_text());P['dialogue_ranges']=[[1400.2322,1436.36],[1439.8,1448.9148]]
(W/'plan.json').write_text(json.dumps(P,indent=2))
cmd=[F,'-y','-v','error','-i',P['source'],'-filter_complex','[0:a:0]pan=mono|c0=c0,asplit=2[a][b];[a]atrim=start=1400.2322:end=1436.36,asetpts=PTS-STARTPTS[a1];[b]atrim=start=1439.8:end=1448.9148,asetpts=PTS-STARTPTS[b1];[a1][b1]concat=n=2:v=0:a=1[out]','-map','[out]','-ar','48000','-c:a','pcm_s24le',str(W/'lav.wav')]
subprocess.run(cmd,check=True)
eq='highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7'
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/voice_chain.py'),'--in',str(W/'lav.wav'),'--out',str(W/'voice-balanced.wav'),'--work',str(W/'audio-balanced'),'--eq',eq,'--no-expander-because','Exact approved R2 Balanced chain. Preserve complete word tails.','--target','-14.1','--tp','-1.5','--oversample','4'],check=True)
subprocess.run([F,'-y','-v','error','-ss','135','-i',str(W/'bill-maher-source.f251.webm'),'-t','18.018','-ac','2','-ar','48000','-c:a','pcm_s24le',str(W/'bill-original.wav')],check=True)
print('AUDIO PREPARED',flush=True)
