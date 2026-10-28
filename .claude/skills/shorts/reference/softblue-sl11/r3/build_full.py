from pathlib import Path
import json,subprocess,os,hashlib
R=Path('/Volumes/Extreme/_edit_work/SL-11/round3');ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');OLD=R.parent/'round1';R2=R.parent/'round2';FF=str(ROOT/'Media/video_edit/bin/ffmpeg');FPS=30000/1001
owner=json.loads((R/'round-controller.json').read_text());assert owner['phase']=='complete' and owner['productionOwner']=='01a183c0-a300-7f30-a67f-53dc4607d97c'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for x in json.loads((R/'preserved-files.json').read_text()):assert sha(x['path'])==x['sha256'],x['path']
(R/'review/films').mkdir(parents=True,exist_ok=True);manifest=[]
for S in 'ABC':
 d=R/'build'/S;d.mkdir(parents=True,exist_ok=True);intro=180 if S=='B' else 75;src=R2/'review/media'/f'{S}1-intro-context.mp4';old=OLD/'build'/S/f'Vacuum-{S}-R1.mp4';T=json.loads((OLD/'build'/S/'timeline.json').read_text());out=R/'review/films'/f'Vacuum-{S}-R3-1080p.mp4'
 if out.exists():raise RuntimeError('Existing full output requires checkpoint verification, not duplicate execution')
 graph=f'[0:v]trim=start_frame=0:end_frame={intro},setpts=PTS-STARTPTS[a];[1:v]trim=start_frame={intro},setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]'
 args=[FF,'-v','error','-y','-threads','1','-filter_complex_threads','1','-i',str(src),'-i',str(old),'-filter_complex',graph,'-map','[v]','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-threads',os.environ.get('RENDERQ_CORES','4'),'-pix_fmt','yuv420p','-r','30000/1001','-frames:v',str(T['frames']),'-c:a','copy','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)]
 with open(d/'render.log','w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True)
 manifest.append(dict(short=S,file=str(out),sha256=sha(out),frames=T['frames'],seconds=T['seconds'],intro_frames=intro,intro_seconds=intro/FPS,approved_intro=str(src),approved_intro_sha256=sha(src),r1_reference=str(old),r1_reference_sha256=sha(old),change='Only first intro picture replaced with approved option1; remainder retains R1 picture/timing, full AAC audio packet stream copied',complete_film_approved=False))
 (R/'build-manifest.json').write_text(json.dumps(manifest,indent=2));print('BUILT',S,T['frames'],flush=True)
