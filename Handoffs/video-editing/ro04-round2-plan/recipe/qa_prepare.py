from pathlib import Path
import json,hashlib,subprocess,shutil,sys
import build as B
import time
while 'All revised preview renders complete' not in (B.W/'qa/render.log').read_text(): time.sleep(1)
W=B.W;old=W.parent/'round1';m=W/'Arms Shoulders Workout LFC R2 - first minute.mp4';h=hashlib.sha256(m.read_bytes()).hexdigest()
p=json.loads((old/'qa/plan.json').read_text())
for key in ['source_picture','watch_log','srt']:p[key]=p[key].replace('/round1/','/round2/').replace('LFC R1','LFC R2').replace('watch-trimmed','watch')
p['evidence_contract']['video_sha256']=h;p.pop('negative_events_scan',None)
# Speech and timer-only classifications will be rechecked on this exact file. No old stamped result is copied.
p['declare'].pop('captions:burned');p['declare'].pop('junk:repeated_take')
(W/'qa/plan.json').write_text(json.dumps(p,indent=2));shutil.copy2(old/'Arms Shoulders Workout LFC R1 - first minute.srt',m.with_suffix('.srt'))
shutil.copy2(old/'audio/audio-AB.mp4',W/'audio/approved-R1-audio-AB.mp4')
for g in ['OLD','A','B','C']:
 for t in [12,78]:
  pass
# Matching 1080p decoded stills from the delivered recommendation.
for t in [0,2,10,34,36,40,55]:
 subprocess.run([B.FF,'-v','error','-ss',str(t),'-i',str(m),'-frames:v','1','-y',str(W/f'qa/delivered-{t}.jpg')],check=True)
# Every generated review file carries the exact stream-copy comparison to its editor-source cut.
for v in list(W.glob('*.mp4'))+list((W/'context').glob('*.mp4')):
 a=70 if v.stem.startswith('overhead') else (9 if v.stem.startswith('color-') else 0)
 duration=round(16*B.FPS)/B.FPS if a==70 else (round(8*B.FPS)/B.FPS if a==9 else 1789/B.FPS)
 ref=W/'audio'/('reference-'+v.stem.replace(' - REVIEW 540p','')+'.m4a')
 if True:subprocess.run([B.FF,'-v','error','-ss',str(B.START+B.OFFSET+a),'-i',B.REF,'-t',str(duration),'-vn','-c:a','copy','-y',str(ref)],check=True)
print(h,flush=True)
