from pathlib import Path
import json,subprocess,hashlib,sys
sys.path.insert(0,str(Path(__file__).parent));from exact_file_gate import check,digest,MASTER,ROOT
O=Path('/Users/danielrose/Projects/_edit_work/RO32-setup/publish');F=str(ROOT/'Media/video_edit/bin/ffmpeg');P=str(ROOT/'Media/video_edit/bin/ffprobe')
def probe(p):return json.loads(subprocess.check_output([P,'-v','error','-count_packets','-show_streams','-show_format','-of','json',str(p)]))
def audio(p):
 z=subprocess.Popen([F,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','data','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE);h=hashlib.sha256()
 for b in iter(lambda:z.stdout.read(1024*1024),b''):h.update(b)
 err=z.stderr.read().decode();assert z.wait()==0,err;return h.hexdigest()
check();base=probe(MASTER);bv=next(x for x in base['streams'] if x['codec_type']=='video');ba=next(x for x in base['streams'] if x['codec_type']=='audio');ah=audio(MASTER);result={}
for name in ['main','instagram']:
 p=O/f'ro32-{name}-1080p.mp4';v=probe(p);vs=next(x for x in v['streams'] if x['codec_type']=='video');a=next(x for x in v['streams'] if x['codec_type']=='audio')
 assert vs['nb_frames']==bv['nb_frames'] and vs['avg_frame_rate']==bv['avg_frame_rate'] and (vs['width'],vs['height'])==(1920,1080)
 assert abs(float(vs['duration'])-float(bv['duration']))<.001
 assert audio(p)==ah and a['nb_read_packets']==ba['nb_read_packets']
 assert p.stat().st_size<(300000000 if name=='instagram' else 400000000)
 cmd=[F,'-v','info','-threads','2','-i',str(MASTER),'-threads','2','-i',str(p),'-filter_complex_threads','2','-filter_complex','[0:v]fps=1,scale=640:360,setpts=PTS-STARTPTS[a];[1:v]fps=1,scale=640:360,setpts=PTS-STARTPTS[b];[a][b]ssim','-an','-f','null','-']
 proc=subprocess.run(cmd,capture_output=True,text=True);assert proc.returncode==0,proc.stderr[-1000:];import re;match=re.search(r'SSIM Y:.*All:([0-9.]+)',proc.stderr);assert match,proc.stderr[-1000:];ssim=float(match.group(1));assert ssim>=.95,ssim
 result[name]={'file':str(p),'sha256':digest(p),'bytes':p.stat().st_size,'frames':int(vs['nb_frames']),'fps':vs['avg_frame_rate'],'duration':float(vs['duration']),'size':[vs['width'],vs['height']],'audio_packets':a['nb_read_packets'],'audio_payload_sha256':ah,'audio_payload_identical_to_master':True,'sampled_640px_ssim':ssim,'ok':True}
 (O/'upload-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(name,json.dumps(result[name]),flush=True)
