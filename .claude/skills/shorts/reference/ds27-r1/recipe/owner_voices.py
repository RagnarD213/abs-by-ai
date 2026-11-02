from pathlib import Path
import subprocess,sys,os
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];A=R/'.claude/skills/_shared/audio';F=str(R/'Media/video_edit/bin/ffmpeg');os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH'];os.environ['GATE_GROUP']='DS-27'
opts={'bass15':'highpass=f=70,equalizer=f=120:t=q:w=0.8:g=1.5','bass30':'highpass=f=70,equalizer=f=120:t=q:w=0.8:g=3.0','soft':'highpass=f=70,treble=g=-1.0:f=6500:width_type=q:width=0.6'}
for name,eq in opts.items():
 out=W/'audio'/(name+'.wav');p=subprocess.run([sys.executable,str(A/'voice_chain.py'),'--in',str(W/'audio/source-30.wav'),'--out',str(out),'--eq',eq,'--no-expander-because','Expanded C1719 auditions clipped word endings in five blind comparisons; retain intact tails while varying tone only.','--oversample','4','--work',str(W/'audio'/(name+'-work'))],capture_output=True,text=True);(W/'audio'/(name+'.log')).write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr[-600:]
 subprocess.run([F,'-v','error','-nostdin','-y','-i',str(out),'-c:a','libmp3lame','-b:a','128k',str(W/'review'/('voice-'+name+'.mp3'))],check=True)
 print('OWNER VOICE',name,flush=True)
