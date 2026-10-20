from pathlib import Path
import subprocess,sys,json,hashlib
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');FP=str(R/'Media/video_edit/bin/ffprobe')
subprocess.run([sys.executable,str(W/'render_response_finish.py')],check=True)
ref=W.parent/'round3/review/media/sample.mp4'
assert hashlib.sha256(ref.read_bytes()).hexdigest()=='1c07c3d3c585fe05a7a2f1274d4a62bec46de1e6be7bdbfb4214f44af2b7ace1'
counts={}
for field,name in [('light','sample'),('dark','dark')]:
 out=W/f'response-{field}.mp4'
 subprocess.run([F,'-v','error','-y','-i',str(W/f'response-prefix-{field}.mp4'),'-i',str(W.parent/f'round3/review/media/{name}.mp4'),'-i',str(W/f'response-tail-{field}.mp4'),'-filter_complex','[0:v]trim=end_frame=383,setpts=PTS-STARTPTS[a];[1:v]trim=end_frame=300,setpts=PTS-STARTPTS[b];[2:v]trim=start_frame=2:end_frame=5,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]','-map','[v]','-an','-r','30000/1001','-c:v','libx264','-preset','fast','-crf','14','-threads','2','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(out)],check=True)
 d=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_entries','stream=nb_read_frames,width,height,r_frame_rate','-of','json',str(out)]));v=d['streams'][0];assert int(v['nb_read_frames'])==686 and v['width']==1080 and v['height']==1920
 counts[field]={'frames':686,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
 subprocess.run([F,'-v','info','-i',str(out),'-i',str(W.parent/f'round3/review/media/{name}.mp4'),'-filter_complex','[0:v]trim=start_frame=383:end_frame=683,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]psnr','-an','-f','null','-'],stdout=open(W/f'approved-r3-reuse-{field}.log','w'),stderr=subprocess.STDOUT,check=True)
(W/'response-key-complete.json').write_text(json.dumps({'frames':686,'components':[{'kind':'new source key','frames':383,'source_start':1400.2322},{'kind':'exact approved R3 sample reused','frames':300,'source_start':1413.0116,'reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest()},{'kind':'new source key with two-frame temporal lead-in','frames':3,'source_start':1423.0216}],'outputs':counts},indent=2))
print('RESPONSE COMPLETE: 383 new frames, 300 approved R3 frames, 3 new tail frames.',flush=True)
