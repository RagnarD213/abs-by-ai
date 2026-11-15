from pathlib import Path
import json,sys,hashlib,subprocess
ROOT=Path('/Users/danrrose/Projects/Claude/Projects/Abs By AI')
WORK=Path(__file__).parent;PARENT=WORK.parent
sys.path.insert(0,str(ROOT/'scripts/blotato'))
from tiktok_cover import build
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
state=json.loads((PARENT/'selected-picks.json').read_text())
approved=ROOT/'Short-form video content/covers/approved-sl21';approved.mkdir(exist_ok=True)
therapy=state['therapy'];files={}
for platform,ext in [('instagram','.png'),('youtube','.png'),('youtube_jpeg','.jpg')]:
 src=PARENT/'therapy-r4/layouts'/('instagram' if platform=='instagram' else 'youtube')/('X3-revised'+ext)
 dst=approved/(('Instagram' if platform=='instagram' else 'Youtube')+'_whattocut-short3_cover-R4-X3'+ext)
 if platform!='youtube_jpeg':assert sha(src)==next(r['sha256'] for r in therapy['revised_files'] if r['platform']==platform)
 data=src.read_bytes();dst.write_bytes(data);assert dst.read_bytes()==data
 files[platform]={'file':str(dst),'sha256':sha(dst),'bytes':len(data)}
therapy.update(status='approved',short=3,label='X3',approved_by='Dan',approved='2026-11-15',words='This looks good. Approved. Go ahead and finish the setup for all three Shorts.',files=files)
(PARENT/'selected-picks.json').write_text(json.dumps(state,indent=2))
(approved/'picks.json').write_text(json.dumps(state,indent=2))
stems=['whattocut-short1_restaurants-dont-care-about-your-fitness-goals','whattocut-short2_you-dont-deserve-a-vacation-until-youre-ripped','whattocut-short3_if-you-cant-afford-a-gym-you-cant-afford-therapy']
hashes=['544f74b7bb182d5a4350a8ffa740b2d6c8529a3259b82fb271b71cb311ea85d5','2c05d70ccc2055da840be8fe57b158e649bd90e94f62430dd49906b1997bce81','b6bd0e5666ab58497e36bc31acc11f3349f53e7b8ed6b81cb5963818965ec2fa']
rows=[];bundle=WORK/'backup-bundle';bundle.mkdir(exist_ok=True)
for n,(stem,digest,kind) in enumerate(zip(stems,hashes,['restaurants','vacation','therapy']),1):
 src=ROOT/'Short-form video content'/(stem+'.mp4');assert sha(src)==digest
 dst=bundle/src.name;data=src.read_bytes();dst.write_bytes(data);assert sha(dst)==digest
 for pl,r in state[kind]['files'].items():
  p=Path(r['file']);assert sha(p)==r['sha256'];d=bundle/'covers'/p.name;d.parent.mkdir(exist_ok=True);d.write_bytes(p.read_bytes());assert sha(d)==r['sha256']
 row={'short':n,'source':str(src),'stage_master':str(dst),'master_sha256':digest,'master_bytes':len(data),'covers':state[kind]['files']}
 rows.append(row)
(WORK/'approved-media.json').write_text(json.dumps(rows,indent=2));(bundle/'approval-and-files.json').write_text(json.dumps(rows,indent=2))
print('Approved cover installed; all three masters and nine cover originals hash verified.',flush=True)

def packets(path,stream):
 cmd=[str(ROOT/'Media/video_edit/bin/ffprobe'),'-v','error','-select_streams',stream,'-show_packets','-show_data_hash','sha256','-show_entries','packet=data_hash','-of','json',str(path)]
 return [x['data_hash'] for x in json.loads(subprocess.check_output(cmd))['packets']]
def decoded(path):
 cmd=[str(ROOT/'Media/video_edit/bin/ffmpeg'),'-v','error','-threads','2','-i',str(path),'-map','0:v:0','-an','-fps_mode','passthrough','-f','framemd5','-']
 return [x.split(',')[-1].strip() for x in subprocess.check_output(cmd,text=True).splitlines() if x and not x.startswith('#')]
checks=[]
for r in rows:
 out=WORK/f'sl21-short{r["short"]}-tiktok-cover-first.mp4'
 check=build(r['stage_master'],r['covers']['instagram']['file'],str(out));assert check['ok'],check
 check['audio_payload_identical']=packets(r['stage_master'],'a')==packets(out,'a')
 check['video_payload_identical_after_cover']=packets(r['stage_master'],'v')==packets(out,'v')[1:]
 if not check['video_payload_identical_after_cover']:check['decoded_picture_frames_identical_after_cover']=decoded(r['stage_master'])==decoded(out)[1:]
 assert check['audio_payload_identical'] and (check['video_payload_identical_after_cover'] or check.get('decoded_picture_frames_identical_after_cover'))
 check.update(short=r['short'],path=str(out),sha256=sha(out),bytes=out.stat().st_size)
 checks.append(check);(WORK/'tiktok-verification.json').write_text(json.dumps(checks,indent=2))
 print('TikTok',r['short'],'cover checked, original picture/audio preserved.',flush=True)
print('BUILD_DONE',flush=True)
