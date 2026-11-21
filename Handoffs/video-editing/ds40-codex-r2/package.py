from pathlib import Path
import subprocess,sys,time,json,hashlib
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media';A=R/'.claude/skills/_shared/audio'
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
for i in range(900):
 if 'RENDER DONE' in (W/'render.log').read_text() and 'DONE' in (W/'audio-refine.log').read_text():break
 time.sleep(2)
else:raise RuntimeError('render/audio timeout')
buildcap.wait('Bill Maher R2 review packaging')
variants=[('sample','wide','baseline'),('balanced','wide','balanced'),('clearer','wide','clearer'),('fuller','wide','fuller'),('dark','dark','baseline'),('oldwide','oldwide','baseline'),('hair','hair','baseline')]
for name,pic,voice in variants:
 subprocess.run([F,'-y','-v','error','-i',str(W/f'{pic}-picture.mp4'),'-i',str(W/f'voice-{voice}.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(D/f'{name}.mp4')],check=True)
for name in ['sample','balanced','clearer','fuller']:
 voice='baseline' if name=='sample' else name
 args=[sys.executable,str(A/'audio_gate.py'),str(D/f'{name}.mp4'),'--untreated',str(W/f'voice-{voice}.wav.audio_untreated.json')]
 if name=='sample':args+=['--ab',str(D/'reference-ab.mp4')]
 subprocess.run(args,stdout=open(W/f'gate-{name}.log','w'),stderr=subprocess.STDOUT)
subprocess.run([F,'-y','-v','error','-i',str(D/'sample.mp4'),'-vf','scale=540:960','-c:v','libx264','-crf','21','-preset','fast','-threads','2','-c:a','copy','-movflags','+faststart',str(D/'phone.mp4')],check=True)
print('PACKAGE DONE',flush=True)
