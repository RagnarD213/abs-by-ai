from pathlib import Path
import subprocess,sys,json,hashlib,os
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');D=Path('/Volumes/Extreme/_edit_work/RO-30/setup/install');FF=str(P/'Media/video_edit/bin/ffmpeg');FP=str(P/'Media/video_edit/bin/ffprobe');A=json.loads((D/'approval.json').read_text());source=Path(A['master'])
def run(c):return subprocess.check_output(c,stderr=subprocess.STDOUT)
def probe(p):return json.loads(run([FP,'-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_frames,duration:format=duration,size','-of','json',str(p)]))
def ah(p):return hashlib.sha256(run([FF,'-nostdin','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'])).hexdigest()
ref=probe(source);audio=ah(source);results={}
for key,rate in [('main','4000k'),('instagram','1800k')]:
 out=D/f'ro30-{key}-1080p.mp4'
 if not out.exists():
  with open(D/f'encode-{key}.log','w') as log:subprocess.run(['nice','-n','20',FF,'-nostdin','-v','error','-y','-hwaccel','videotoolbox','-i',str(source),'-map','0:v:0','-map','0:a:0','-c:v','h264_videotoolbox','-profile:v','high','-pix_fmt','yuv420p','-b:v',rate,'-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','copy','-movflags','+faststart',str(out)],check=True,stdout=log,stderr=subprocess.STDOUT)
 pr=probe(out);v=next(x for x in pr['streams'] if x['codec_type']=='video');same=ah(out)==audio;ok=int(v['nb_frames'])==8504 and v['width']==1920 and v['height']==1080 and abs(float(pr['format']['duration'])-283.750133)<.04 and same;assert ok
 results[key]=dict(path=str(out),probe=pr,audio_sha256=audio,audio_identical=same,ok=ok);print(key,out.stat().st_size,'verified',flush=True)
(D/'upload-verification.json').write_text(json.dumps(results,indent=2)+'\n')
sys.path.insert(0,str(P/'scripts/blotato'));import tiktok_cover
out=D/'ro30-tiktok-cover-first.mp4';r=tiktok_cover.build(str(D/'ro30-main-1080p.mp4'),A['cover'],str(out));r['audio_sha256']=ah(out);r['audio_identical']=r['audio_sha256']==audio;r['ok']=r['ok'] and r['audio_identical'];assert r['ok'];(D/'tiktok-verification.json').write_text(json.dumps(r,indent=2)+'\n');print('tiktok verified',flush=True)
