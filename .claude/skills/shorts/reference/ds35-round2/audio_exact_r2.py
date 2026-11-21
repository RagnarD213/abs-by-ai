"""Normal own-mix final AAC qualification, proper original baseline and stereo preservation.
Earlier raw evidence retained. Does not modify, reprocess or remux a video.
"""
from pathlib import Path
import sys,json,subprocess,shutil,os
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');v=sys.argv[1];q=W/'qa'/v;vid=W/'review/media'/('dad-bod-r2-'+v+'.mp4');FF=str(R/'Media/video_edit/bin/ffmpeg');sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
archive=q/'audio-first-measurements';archive.mkdir(exist_ok=True)
for p in [Path(str(vid)+'.audio_gate.json'),q/'Dan-from-final-AAC.wav.audio_gate.json',q/'Dan-from-final-AAC.wav']:
 if p.exists() and not (archive/p.name).exists():shutil.copy2(p,archive/p.name)
dan=q/'Dan-exact-stereo-final-AAC.wav';subprocess.run([FF,'-v','error','-nostdin','-y','-ss',str(469/(30000/1001)),'-i',str(vid),'-vn','-ac','2','-ar','48000','-c:a','pcm_s24le',str(dan)],check=True)
records=[]
for target,raw in [(vid,W/v/'mix-untreated.wav'),(dan,W/v/'audio/lav.wav')]:
 a,b=C.analysis_window(str(target));x=C.pcm(str(raw),ss=a,dur=b);C.stash_untreated(str(target),x,note='Actual untreated source mix, identical timeline and normal gate analysis window. '+str(raw))
 records.append(dict(target=str(target),target_sha256=C.sha256(str(target)),untreated_source=str(raw),untreated_sha256=C.sha256(str(raw)),analysis_window=[a,b],baseline=str(target)+'.audio_untreated.json'))
 cmd=[sys.executable,str(R/'.claude/skills/_shared/audio/audio_gate.py'),str(target)]
 if target==vid:cmd+=['--ab',str(q/'audio-ab.wav')]
 with (q/('audio-exact-'+('full' if target==vid else 'Dan')+'.log')).open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 print('NORMAL_OWN_EXACT_AAC',v,target.name,r.returncode,flush=True)
out=dict(scope='Current exact final AAC, owned/normal mode; no reference/verbatim bypass. Stereo maintained. Proper untreated baselines replace missing-baseline first measurements, retained in archive.',video_sha256=C.sha256(str(vid)),records=records)
(q/'audio-exact-provenance.json').write_text(json.dumps(out,indent=2))
