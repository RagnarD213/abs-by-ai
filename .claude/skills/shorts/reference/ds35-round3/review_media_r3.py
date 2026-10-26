from pathlib import Path
import sys,subprocess,shutil,json,hashlib
W=Path(__file__).resolve().parents[1];B=W.parent/'round2';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media';FPS=30000/1001
for v in ['scripted','off_the_cuff']:
 s=D/f'dad-bod-r3-{v}.mp4';out=D/f'dad-bod-r3-{v}-540p.mp4'
 subprocess.run([F,'-v','error','-y','-i',str(s),'-vf','scale=540:960:flags=lanczos','-c:v','libx264','-preset','fast','-crf','21','-threads',__import__('os').environ.get('RENDERQ_CORES','4'),'-c:a','copy','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)],check=True)
 subprocess.run([F,'-v','error','-y','-ss','10','-i',str(s),'-frames:v','1','-q:v','2',str(D/f'dad-bod-r3-{v}-poster.jpg')],check=True)
 shutil.copyfile(W/v/'captions.srt',D/f'dad-bod-r3-{v}.srt');shutil.copyfile(B/'review/media'/f'dad-bod-r2-{v}-audio-ab.wav',D/f'dad-bod-r3-{v}-audio-ab.wav')
 # Check EVERY phone-copy audio packet too, not simply its sample rate or length.
 sys.path.insert(0,str(W/'recipe'));from qa_r3 import packets
 assert packets(s)==packets(out)
 print('PHONE_COPY_READY',v,flush=True)
for name,a,b in [('craig',8,17),('abs',31,36)]:
 subprocess.run([F,'-v','error','-y','-ss',str(a),'-i',str(D/'dad-bod-r3-scripted.mp4'),'-t',str(b-a),'-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(D/f'dad-bod-r3-{name}-context.mp4')],check=True)
print('R3_REVIEW_MEDIA_COMPLETE',flush=True)
