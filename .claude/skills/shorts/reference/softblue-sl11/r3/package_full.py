from pathlib import Path
import json,hashlib,shutil,subprocess
R=Path('/Volumes/Extreme/_edit_work/SL-11/round3');ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();names={'A':'How To Do A Standing Stomach Vacuum','B':'Stop Holding Your Breath During Stomach Vacuums','C':'Start With One 20-Second Vacuum Every Morning'}
rows=[]
for z in json.loads((R/'build-manifest.json').read_text()):
 S=z['short'];v=Path(z['file']);h=sha(v);assert h==z['sha256'];d=R/'build'/S
 for suffix in ['.audio_gate.json','.deliver_gate.json']:
  j=json.loads(Path(str(v)+suffix).read_text());assert j['verdict']=='PASS' and j['sha256']==h,(S,suffix)
 w=json.loads((d/'gate/logs/watch_pass.json').read_text());assert w['inspected'] and w['open_defects']==0 and w['sha256']==h
 VLC=ROOT/'Videos to Review'/f'The Vacuum SFC R3 - Short {S} - {names[S]}.mp4';shutil.copy2(v,VLC);assert sha(VLC)==h
 # New final delivery filename preserves the earlier R1 reviewed file and its approvals.
 out=ROOT/'Short-form video content'/f'vacuum-short{list(names).index(S)+1}_{names[S]} - R3.mp4';shutil.copy2(v,out);assert sha(out)==h
 for suffix in ['.audio_gate.json','.deliver_gate.json']:shutil.copy2(Path(str(v)+suffix),Path(str(out)+suffix))
 rows.append(dict(z,title=names[S],delivery=str(out),vlc=str(VLC),audio_gate='PASS',delivery_gate='PASS',independent_open_defects=0,watch_log=str(d/'gate/logs/watch_pass.json')))
for p in json.loads((R/'preserved-files.json').read_text()):assert sha(p['path'])==p['sha256'],p['path']
manifest=dict(stage='Complete R3 A/B/C rendered/checked and delivered for Dan full-film review; not approved/uploaded/scheduled',revision_id='01a183f2-c529-7812-9188-1334a686a97d',selected_intro=1,review_url='http://127.0.0.1:9411/',complete_films_approved=False,publishing=False,paid_spend=0,downloads=[],preserved_hashes=35,files=rows)
(R/'delivery-manifest.json').write_text(json.dumps(manifest,indent=2));p=R/'revision-progress.json';j=json.loads(p.read_text());j.update(status='delivered',checkpoint='R3 choice processed once; all3 complete films pass exact audio/delivery/watch checks; delivered for Dan review. No final-film approval or publishing.',delivery_manifest=str(R/'delivery-manifest.json'));p.write_text(json.dumps(j,indent=2));print('PACKAGED THREE CHECKED FILMS',flush=True)
