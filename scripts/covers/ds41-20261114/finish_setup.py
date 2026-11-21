"""DS-41 approved cover installation, lossless TikTok derivative and verified CDN uploads."""
import argparse,hashlib,json,subprocess,sys,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
WORK=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
sys.path.insert(0,str(ROOT/'scripts/blotato'))
from danrosefit_migration import api_key,call
from tiktok_cover import build
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(name,obj):
    (WORK/'final'/name).write_text(json.dumps(obj,indent=2)+'\n')
a=json.loads((WORK/'final/approval.json').read_text())
assert a['final_cover_approved'] and a['final_approval_words']=='Approved'
master=(ROOT/'Short-form video content/Kevin James Cheat - DS-41/Kevin James Cheat SFC R2 - off the cuff.mp4').resolve()
assert sha(master.read_bytes())==a['film_sha256']
ig=Path(a['files']['Instagram jpg']['file'])
yt=Path(a['files']['YouTube jpg']['file'])
for k in ['Instagram jpg','YouTube jpg']:
    assert sha(Path(a['files'][k]['file']).read_bytes())==a['files'][k]['sha256']
p=argparse.ArgumentParser();p.add_argument('action',choices=['build','upload','upload-ready']);args=p.parse_args()
tt=WORK/'final/DS41-TikTok-Cover-First.mp4'
if args.action=='build':
    check=build(str(master),str(ig),str(tt))
    assert check['ok'],check
    def packets(path,stream):
        command=[str(ROOT/'Media/video_edit/bin/ffprobe'),'-v','error','-select_streams',stream,'-show_packets','-show_data_hash','sha256','-show_entries','packet=data_hash','-of','json',str(path)]
        return [x['data_hash'] for x in json.loads(subprocess.check_output(command))['packets']]
    check['audio_payload_identical']=packets(master,'a')==packets(tt,'a')
    check['video_payload_identical_after_cover']=packets(master,'v')==packets(tt,'v')[1:]
    if not check['video_payload_identical_after_cover']:
        def decoded(path):
            cmd=[str(ROOT/'Media/video_edit/bin/ffmpeg'),'-v','error','-threads','2','-i',str(path),'-map','0:v:0','-an','-fps_mode','passthrough','-f','framemd5','-']
            output=subprocess.check_output(cmd,text=True)
            return [x.split(',')[-1].strip() for x in output.splitlines() if x and not x.startswith('#')]
        check['decoded_picture_frames_identical_after_cover']=decoded(master)==decoded(tt)[1:]
    assert check['audio_payload_identical'] and (check['video_payload_identical_after_cover'] or check.get('decoded_picture_frames_identical_after_cover'))
    check.update(path=str(tt),sha256=sha(tt.read_bytes()),bytes=tt.stat().st_size)
    save('tiktok-verification.json',check);print(json.dumps(check,indent=2),flush=True)
else:
    files={'instagram':(ig,a['files']['Instagram jpg']['sha256']),'youtube':(yt,a['files']['YouTube jpg']['sha256']),'master':(master,a['film_sha256'])}
    if args.action=='upload':
        check=json.loads((WORK/'final/tiktok-verification.json').read_text())
        assert check['ok'] and check['audio_payload_identical'] and (check.get('video_payload_identical_after_cover') or check.get('decoded_picture_frames_identical_after_cover'))
        files['tiktok']=(tt,check['sha256'])
    statepath=WORK/'final/uploads.json';state=json.loads(statepath.read_text()) if statepath.exists() else {}
    for name,(path,digest) in files.items():
        data=path.read_bytes();assert sha(data)==digest
        if state.get(name,{}).get('sha256')==digest:
            assert sha(urllib.request.urlopen(state[name]['url'],timeout=180).read())==digest
            print('Existing upload reverified:',name,flush=True);continue
        record=call('POST','/media/uploads',api_key(),{'filename':'ds41-kevin-james-'+name+path.suffix})
        req=urllib.request.Request(record['presignedUrl'],data=data,method='PUT',headers={'Content-Type':'video/mp4' if path.suffix=='.mp4' else 'image/jpeg'})
        urllib.request.urlopen(req,timeout=180).read()
        assert sha(urllib.request.urlopen(record['publicUrl'],timeout=180).read())==digest
        state[name]={'url':record['publicUrl'],'path':str(path),'sha256':digest,'bytes':len(data),'remote_hash_verified':True}
        save('uploads.json',state);print('Uploaded and download-verified:',name,len(data),flush=True)
