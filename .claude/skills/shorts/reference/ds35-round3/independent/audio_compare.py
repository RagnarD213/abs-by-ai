from pathlib import Path
import json,subprocess,hashlib
W=Path('/Volumes/Expansion/_edit_work/DS-35/round3');B=W.parent/'round2';F='/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg';P='/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for v in ['scripted','off_the_cuff']:
 a=W/'review/media'/f'dad-bod-r3-{v}.mp4';b=B/'review/media'/f'dad-bod-r2-{v}.mp4';ds=[];pcm=[]
 for p in [a,b]:
  z=json.loads(subprocess.check_output([P,'-v','error','-select_streams','a:0','-show_packets','-show_data_hash','sha256','-show_entries','packet=pts,dts,duration,size,data_hash','-of','json',str(p)]))['packets'];ds.append(z)
  raw=subprocess.check_output([F,'-v','error','-i',str(p),'-map','0:a:0','-vn','-f','s24le','-acodec','pcm_s24le','-ac','2','-ar','48000','-']);pcm.append(dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)))
 r=dict(video_sha256=sha(a),baseline_sha256=sha(b),packets=len(ds[0]),every_packet_hash_pts_dts_duration_size_identical=ds[0]==ds[1],decoded_stereo_pcm=pcm,decoded_stereo_pcm_identical=pcm[0]==pcm[1],auditory_scope='No fresh heard or metered listening. Prior acoustic/listening judgments inherited only through exact packet and decoded stereo identity. Contradictory bounded R2 opinions retain uncertainty; signal preservation proves no new processing damage, not ideal room acoustics.')
 (W/'independent'/v/'audio-independent.json').write_text(json.dumps(r,indent=2));print(v,json.dumps(r),flush=True)
