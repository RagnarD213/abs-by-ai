from pathlib import Path
import json,hashlib,shutil,sys,subprocess
R=Path(__file__).resolve().parents[4];W=Path('/Volumes/Expansion/_edit_work/ds16-publish');qa=json.loads((W/'hq-verification.json').read_text());assert qa['matches_approved_edit']
name='how to lose the last ten pounds of fat | muhammad | 9x16 | V3 HD.mp4'
D=R/'Short-form video content/How To Lose The Last Ten Pounds Of Fat - DS-16';E=Path('/Volumes/Extreme/Short-form video content/How To Lose The Last Ten Pounds Of Fat - DS-16');D.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for folder in [D,E]:
 p=folder/name
 if p.exists():assert sha(p)==qa['hq']['sha256']
 else:shutil.copy2(qa['hq']['path'],p)
 assert sha(p)==qa['hq']['sha256']
# English sidecar based on the unchanged approved timeline, not an extra burned caption layer.
asr=json.load(open('/Volumes/Extreme/_edit_work/revisions-20261103/muhammad/work/ds16_v3/cut16k.json'))
def ts(t):
 n=round(t*1000);return f'{n//3600000:02d}:{n//60000%60:02d}:{n//1000%60:02d},{n%1000:03d}'
srt='\n\n'.join(f"{i}\n{ts(seg['start'])} --> {ts(seg['end'])}\n{seg['text'].strip().replace('Zep Bound','Zepbound')}" for i,seg in enumerate(asr['segments'],1))+'\n'
for folder in [D,E]:(folder/Path(name).with_suffix('.srt')).write_text(srt)
record={'source':str(D/name),'sha256':qa['hq']['sha256'],'bytes':qa['hq']['bytes'],'external_copy':str(E/name),'subtitle':str(D/Path(name).with_suffix('.srt')),'subtitle_method':'Approved V3 ASR on same verified HQ timeline, Zepbound spelling corrected; film already has burned captions.','drive_id':qa['hq']['drive_id']}
(W/'master.json').write_text(json.dumps(record,indent=2))
sys.path.insert(0,str(R/'scripts/blotato'));import tiktok_cover
out=W/'last-ten-pounds-tiktok-X2.mp4';cover=str(R/'Short-form video content/covers/approved-ds16/Instagram_ds-16_last-ten-pounds_cover-X2.png')
qc=tiktok_cover.build(str(D/name),cover,str(out));assert qc['ok']
# The original packet payload, independently hash-checked, must be identical.
FF=str(R/'Media/video_edit/bin/ffmpeg')
def ah(p):return hashlib.sha256(subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()
qc.update(path=str(out),sha256=sha(out),bytes=out.stat().st_size,audio_payload_identical=ah(D/name)==ah(out));assert qc['audio_payload_identical'];(W/'tiktok-verification.json').write_text(json.dumps(qc,indent=2))
print('Master project/Extreme copies verified; TikTok',json.dumps(qc),flush=True)
