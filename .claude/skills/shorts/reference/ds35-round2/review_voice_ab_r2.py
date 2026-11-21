"""Review-only PCM A/B: pinned house reference then actual Dan, not interview.
Normal gate AB/stamps remain unchanged. No film or selected sound processing is altered.
"""
from pathlib import Path
import sys,json,wave,numpy as np,hashlib
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('Dad Bod correct actual voice comparison media',pool='quick')
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C,reference as REF
ref,meta=REF.resolve();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();a=C.pcm(ref,ss=20,dur=12,ac=2);records=[]
for v in ['scripted','off_the_cuff']:
 movie=W/'review/media'/('dad-bod-r2-'+v+'.mp4');b=C.pcm(str(movie),ss=20,dur=12,ac=2);s=np.concatenate([a,np.zeros((24000,2)),b]);p=W/'review/media'/('dad-bod-r2-'+v+'-audio-ab.wav')
 with wave.open(str(p),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(48000);f.writeframes(np.round(np.clip(s,-1,1)*32767).astype('<i2').tobytes())
 records.append(dict(version=v,path=str(p),sha256=sha(p),codec='PCM16 stereo48000',seconds=len(s)/48000,reference_source=ref,reference_sha256=sha(Path(ref)),reference_window=[20,32],actual_video_sha256=sha(movie),actual_film_window=[20,32],sequence='0-12s house reference,12-12.5s silence,12.5-24.5s actual Dan. No extra processing or level adjustment. Both originate from normal finished audio; reference is not substituted into film.'))
(W/'qa/review-voice-ab.json').write_text(json.dumps(records,indent=2));print('CORRECT_VOICE_AB_MEDIA_WRITTEN',flush=True)
