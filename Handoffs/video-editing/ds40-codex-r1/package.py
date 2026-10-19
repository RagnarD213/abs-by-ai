from pathlib import Path
import subprocess,sys,time,json
W=Path(__file__).parent;ROOT=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(ROOT/'Media/video_edit/bin/ffmpeg');D=W/'review/media'
sys.path.insert(0,str(ROOT/'.claude/skills/_shared'));import buildcap
for i in range(360):
 if 'FINISH DONE' in (W/'finish.log').read_text():break
 time.sleep(2)
else:raise RuntimeError('finish timeout')
buildcap.wait('Codex sample packaging')
for name,pic,voice in [('warm','warm','open'),('bright','bright','open'),('dark','edge-dark','open'),('voice-original','natural','raw')]:
 subprocess.run([F,'-y','-hide_banner','-loglevel','error','-i',str(W/f'{pic}-picture.mp4'),'-i',str(W/f'voice-{voice}.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(D/f'{name}.mp4')],check=True)
subprocess.run([F,'-y','-hide_banner','-loglevel','error','-i',str(D/'sample.mp4'),'-vf','scale=540:960','-c:v','libx264','-preset','fast','-crf','22','-threads','3','-c:a','copy','-movflags','+faststart',str(D/'review-540p.mp4')],check=True)
print('PACKAGED',flush=True)
