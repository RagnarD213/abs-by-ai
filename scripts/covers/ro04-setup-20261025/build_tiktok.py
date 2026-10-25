from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts/blotato'))
import tiktok_cover
OUT=Path('/Volumes/Expansion/_edit_work/ro04-publish');OUT.mkdir(parents=True,exist_ok=True)
master=ROOT/'Codex Content Videos/Arms Shoulders Workout Only - RO-04/Arms Shoulders Workout Only | codex | 16x9 | RO-04.mp4'
cover=ROOT/'social media graphics/youtube/thumbnails/Arms Shoulders Workout Only/Arms Shoulders Workout Only - thumbnail FINAL.png'
assert hashlib.sha256(master.read_bytes()).hexdigest()=='140fd719899dc17d9d8d4217326a73dbdba6150fb1012c89eae7105518f8b7df'
assert hashlib.sha256(cover.read_bytes()).hexdigest()=='548af7f873776f406634dd20195732f83935ecc8c41453fa73532c77fe3266d2'
dest=OUT/'Arms Shoulders Workout Only - TikTok cover first.mp4'
record=OUT/'tiktok-verification.json'
if record.exists() and dest.exists():
    old=json.loads(record.read_text())
    if old.get('ok') and old.get('sha256')==hashlib.sha256(dest.read_bytes()).hexdigest():
        print('Existing verified TikTok derivative retained');sys.exit(0)
result=tiktok_cover.build(str(master),str(cover),str(dest))
assert result['ok'],result
def audiohash(path):
    import subprocess
    command=[str(ROOT/'Media/video_edit/bin/ffmpeg'),'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-']
    data=subprocess.check_output(command)
    return hashlib.sha256(data).hexdigest()
result['source_audio_payload_sha256']=audiohash(master)
result['derivative_audio_payload_sha256']=audiohash(dest)
assert result['source_audio_payload_sha256']==result['derivative_audio_payload_sha256']
result['audio_payload_identical']=True
result['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();result['bytes']=dest.stat().st_size
result['source_master_sha256']='140fd719899dc17d9d8d4217326a73dbdba6150fb1012c89eae7105518f8b7df'
result['approved_cover_sha256']='548af7f873776f406634dd20195732f83935ecc8c41453fa73532c77fe3266d2'
record.write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
