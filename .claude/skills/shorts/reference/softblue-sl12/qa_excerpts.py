#!/usr/bin/env python3
"""Bounded technical checks for asset excerpts, not a final delivery stamp."""
from pathlib import Path
import json,subprocess,hashlib,sys
import numpy as np
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');WORK=Path('/Volumes/Extreme/_edit_work/SL-12/round1');OUT=WORK/'asset-review';FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FP=str(ROOT/'Media/video_edit/bin/ffprobe')
sys.path.insert(0,str(Path(__file__).resolve().parent));import packet as P
results=[]
for q in P.CASES:
 p=OUT/(q['id']+'-context.mp4');d=json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(x for x in d['streams'] if x['codec_type']=='video');a=[x for x in d['streams'] if x['codec_type']=='audio'];n=round((q['b']-q['a'])*P.FPS)
 assert (v['width'],v['height'])==(1080,1920),(q['id'],v)
 assert int(v['nb_frames'])==n,(q['id'],v['nb_frames'],n)
 assert v['r_frame_rate']=='30000/1001',v['r_frame_rate']
 r={'id':q['id'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimensions':[1080,1920],'frames':n,'duration':round(n/P.FPS,3),'audio_tracks':len(a)}
 if q['text']:
  assert a and a[0]['channels']==2 and a[0]['sample_rate']=='48000',a
  # Source WAV was pulled once from the approved parent; AAC export is the only sound encoding.
  cmd=lambda f:np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(f),'-map','0:a:0','-ac','2','-ar','48000','-f','f32le','-']),np.float32).reshape(-1,2)
  x=cmd(OUT/q['id']/'speech.wav');y=cmd(p);m=min(len(x),len(y));r['pcm_zero_lag_correlation']=round(float(np.corrcoef(x[:m].reshape(-1),y[:m].reshape(-1))[0,1]),6);r['pcm_duration_difference_ms']=round((len(y)-len(x))/48,3)
  assert r['pcm_zero_lag_correlation']>.99,r
  words=json.loads((OUT/q['id']/'words.json').read_text());r['caption_alignment']='Wav2Vec2 CTC on exact excerpt, corrected source text';r['low_confidence_words']=[w for w in words if w['score']<.35]
 else:assert not a,'Opening footage is a silent visual sample; no pickup voice recorded.'
 results.append(r)
report={'scope':'asset excerpt technical checks only; not delivery gates or an audible listening pass','results':results,'audio_selftest':'4 fixture/reference-path failures, retained in audio-selftest.log; no bounds changed','source':'locked approved master; source and captions remain intact','final_short_checks':'pending final assembly and A pickup'}
(WORK/'excerpt-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
