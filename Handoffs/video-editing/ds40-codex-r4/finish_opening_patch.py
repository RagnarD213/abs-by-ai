from pathlib import Path
import sys,json,subprocess,hashlib,shutil,os
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');FP=str(R/'Media/video_edit/bin/ffprobe')
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap;buildcap.wait('Bill Maher R4 opening caption onset repair')
A=json.loads((W/'assembly.json').read_text());oldsha=A['sha256'];old=Path(A['master']);C=W/'internal-candidate-d';C.mkdir(exist_ok=True)
for name in ['assembly.json','delivery-plan.json','watch-plan.json','caption-states.json','words-final-ctc.json','parent-self-qa.json','audio-gate-final.log','delivery-gate-initial.log']:
 if (W/name).exists():shutil.copy2(W/name,C/name)
for name in ['bill-maher-fat-90-year-old-r4.mp4','phone.mp4','bill-maher-fat-90-year-old-r4.srt']:
 shutil.copy2(W/'review/media'/name,C/name)
if (W/'watch').exists():os.rename(W/'watch',C/'watch')
shutil.copy2(W/'full-picture.mp4',C/'full-picture.mp4')
subprocess.run([sys.executable,str(W/'render_opening_patch.py')],stdout=open(W/'opening-patch-render.log','w'),stderr=subprocess.STDOUT,check=True)
lst=W/'opening-patch-concat.txt';lst.write_text("file 'opening-prefix-fixed.mp4'\nduration 8.341666666666667\nfile 'internal-candidate-d/full-picture.mp4'\ninpoint 8.341666666666667\n")
pic=W/'full-picture-repaired.mp4';subprocess.run([F,'-y','-v','error','-f','concat','-safe','0','-i',str(lst),'-map','0:v','-c:v','copy','-movflags','+faststart',str(pic)],check=True)
probe=json.loads(subprocess.check_output([FP,'-v','error','-count_frames','-show_entries','stream=nb_read_frames,duration,r_frame_rate','-of','json',str(pic)]));st=probe['streams'][0];assert int(st['nb_read_frames'])==A['frames'],probe;assert abs(float(st['duration'])-A['duration'])<.001,probe
# Verify every decoded native tail frame, not sparse thumbnails, retained the original pixels.
def tailmd5(p):
 raw=subprocess.check_output([F,'-v','error','-i',str(p),'-vf','trim=start_frame=250,setpts=PTS-STARTPTS','-an','-f','framemd5','-']);return [x for x in raw.decode().splitlines() if not x.startswith('#')]
x=tailmd5(C/'full-picture.mp4');y=tailmd5(pic);assert x==y,'Decoded tail pixels changed';assert len(x)==A['frames']-250
new=W/'candidate-repaired.mp4';subprocess.run([F,'-y','-v','error','-i',str(pic),'-i',str(C/old.name),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(new)],check=True)
def aud(p):return hashlib.sha256(subprocess.check_output([F,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()
ax,ay=aud(C/old.name),aud(new);assert ax==ay
os.replace(new,old);os.replace(pic,W/'full-picture.mp4');A['sha256']=hashlib.sha256(old.read_bytes()).hexdigest();A['caption_repair']={'prior_sha256':oldsha,'first_caption_onset':.260,'reason':'Independent final AAC CTC and native audio RMS show speech starts 0.26-0.30, while caption was at 0.000.','reencoded_picture_frames':[0,249],'unchanged_decoded_tail_frames':len(x),'all_native_tail_frame_md5_equal':True,'unchanged_AAC_sha256':ax}
(W/'assembly.json').write_text(json.dumps(A,indent=2));(W/'caption-repair.json').write_text(json.dumps(dict(A['caption_repair'],final_sha256=A['sha256'],probe=probe),indent=2));print('REPAIR COMPLETE',A['sha256'],flush=True)
subprocess.run([sys.executable,str(W/'qa_prepare.py')],stdout=open(W/'qa-repair.log','w'),stderr=subprocess.STDOUT,check=True)
