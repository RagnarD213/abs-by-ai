from pathlib import Path
import subprocess,json,hashlib,re,os
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');F=R/'Media/video_edit/bin/ffmpeg';E=W/'evidence/finishing';E.mkdir(exist_ok=True)
a=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p.mp4';b=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p - aligned.mp4';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();audio=[]
for v in [a,b]:
 z=subprocess.check_output([str(F),'-v','error','-i',str(v),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','pipe:1'],text=True).strip();audio.append(z)
assert audio[0]==audio[1],audio
stats=E/'caption-only-picture-ssim.txt';log=E/'caption-only-picture-ssim.log'
with log.open('w') as f:subprocess.run([str(F),'-nostdin','-v','info','-i',str(a),'-i',str(b),'-filter_complex',f'[0:v]crop=1080:1400:0:0,format=yuv420p[a];[1:v]crop=1080:1400:0:0,format=yuv420p[b];[a][b]ssim=stats_file={stats}','-an','-f','null','-'],stdout=f,stderr=subprocess.STDOUT,check=True)
vals=[float(x) for x in re.findall(r'All:([0-9.]+)',stats.read_text())];assert len(vals)==1917
r=dict(initial_video_sha256=h(a),video_sha256=h(b),audio_packet_hash=audio[0],audio_packet_stream_byte_identical=True,picture_comparison=dict(region=[0,0,1080,1400],native_frames=len(vals),ssim_min=min(vals),ssim_mean=sum(vals)/len(vals),method='Every-native-frame camera/title/graphics comparison above caption ink. Independent decoded pictures; encoder may redistribute quantization around changed caption timing. No structural picture change in recipe.'),caption_chunks_initial=len(json.load(open(W/'records/FULL-captions.json'))),caption_chunks_repaired=len(json.load(open(W/'records/FULL-aligned-captions.json'))),text_chunks_identical=[x['text'] for x in json.load(open(W/'records/FULL-captions.json'))]==[x['text'] for x in json.load(open(W/'records/FULL-aligned-captions.json'))])
assert r['text_chunks_identical'];(E/'caption-only-preservation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r),flush=True)
