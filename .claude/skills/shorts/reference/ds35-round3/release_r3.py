"""Build a release receipt only after fresh exact-file independent and shared gates."""
from pathlib import Path
import json,hashlib,datetime
W=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=[]
for v in ['scripted','off_the_cuff']:
 f=W/'review/media'/f'dad-bod-r3-{v}.mp4';h=sha(f);q=W/'qa'/v
 r=json.loads((W/'independent'/v/'report.json').read_text());assert r['video_sha256']==h and r['review_complete'] and not r['open_export_defects']
 g=json.loads((q/'gate-final.json').read_text());assert g['verdict']=='PASS' and all(x['ok'] for x in g['rows'])
 stamp=json.loads(Path(str(f)+'.deliver_gate.json').read_text());assert stamp['verdict']=='PASS' and stamp['sha256']==h
 a=json.loads((q/'audio-packet-identity.json').read_text());assert a['video_sha256']==h and a['decoded_pcm_identical'] and a['identical_packet_hashes_and_timestamps']
 files.append(dict(take=v,path=str(f),sha256=h,independent_report_sha256=sha(W/'independent'/v/'report.json')))
for entry in json.loads((W/'approval-manifest.json').read_text()):assert sha(entry['path'])==entry['sha256'],entry
result=dict(checked_at=datetime.datetime.now().astimezone().isoformat(),both_complete=True,independent_review_complete=True,open_export_defects=0,browser_verified=False,review_url='http://127.0.0.1:9241/',files=files)
(W/'review/release-receipt.json').write_text(json.dumps(result,indent=1));print('EXACT_R3_RELEASE_CHECKS_COMPLETE')
