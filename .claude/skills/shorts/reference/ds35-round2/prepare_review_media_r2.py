from pathlib import Path
import sys,subprocess,shutil,json
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('Dad Bod paired complete phone copies',pool='heavy')
FF=str(R/'Media/video_edit/bin/ffmpeg')
for v in ['scripted','off_the_cuff']:
 d=W/'review/media';s=d/('dad-bod-r2-'+v+'.mp4');p=d/('dad-bod-r2-'+v+'-540p.mp4')
 if not p.exists():subprocess.run([FF,'-v','error','-nostdin','-y','-i',str(s),'-vf','scale=540:960:flags=lanczos','-c:v','libx264','-preset','fast','-crf','21','-threads','4','-c:a','copy','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(p)],check=True)
 poster=d/('dad-bod-r2-'+v+'-poster.jpg')
 if not poster.exists():subprocess.run([FF,'-v','error','-nostdin','-y','-ss','17.2','-i',str(s),'-frames:v','1','-q:v','2',str(poster)],check=True)
 shutil.copy2(W/v/'captions.srt',d/('dad-bod-r2-'+v+'.srt'))
 shutil.copy2(W/'qa'/v/'audio-ab.wav',d/('dad-bod-r2-'+v+'-audio-ab.wav'))
 print('REVIEW_MEDIA_READY',v,flush=True)
