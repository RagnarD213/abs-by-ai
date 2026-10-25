from pathlib import Path
import json,hashlib,shutil,datetime
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');D=R/'Short-form video content/Dad Bod - DS-35';V=R/'Videos to Review';D.mkdir(parents=True,exist_ok=True);V.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
receipt=json.loads((W/'review/release-receipt.json').read_text());assert receipt['both_complete'] and receipt['independent_review_complete'] and receipt['browser_verified']
files=[]
for v,title in [('scripted','scripted'),('off_the_cuff','off the cuff')]:
 src=W/'review/media'/f'dad-bod-r3-{v}.mp4';g=json.loads(Path(str(src)+'.deliver_gate.json').read_text());assert g['verdict']=='PASS' and g['sha256']==sha(src)
 out=D/f'Dad Bod SFC R3 - {title}.mp4';vlc=V/out.name;shutil.copyfile(src,out);shutil.copyfile(src,vlc);assert sha(src)==sha(out)==sha(vlc)
 for suf in ['.deliver_gate.json','.audio_gate.json','.audio_untreated.json']:
  p=Path(str(src)+suf)
  if p.exists():shutil.copyfile(p,Path(str(out)+suf))
 shutil.copyfile(W/v/'captions.srt',out.with_suffix('.srt'))
 qd=D/f'R3 QA - {title}';qd.mkdir(exist_ok=True)
 for n in ['plan.json','gate-raw.json','gate-final.json','audio-packet-identity.json','full-speech-junk.json','corrected-caption-sync.json','audio-exact-provenance.json','preservation.json','watch_pass.json']:
  p=W/'qa'/v/n
  if p.exists():shutil.copyfile(p,qd/n)
 for p in (W/'independent'/v).glob('*.json'):shutil.copyfile(p,qd/('independent-'+p.name))
 p=W/'independent'/v/'report.md';shutil.copyfile(p,qd/'independent-report.md')
 files.append(dict(take=v,path=str(out),vlc_path=str(vlc),sha256=sha(out),seconds=json.loads((W/v/'edl.json').read_text())['total_seconds']))
rd=D/'Recipe - R3';rd.mkdir(exist_ok=True)
for p in (W/'recipe').glob('*.py'):shutil.copyfile(p,rd/p.name)
for n in ['decisions.json','asset-provenance.json','approval-manifest.json','execution-state.json']:
 p=W/n
 if p.exists():shutil.copyfile(p,rd/n)
notes=f'''CONTENT SFC: Dad Bod R3. Both complete films delivered for Dan's review, not approved, uploaded or scheduled.\n\nReview: {receipt['review_url']}\nWatch both0:09–0:16 for larger Craig photo, exact label/arrow and foreground hair. Scripted0:31–0:36 for stronger existing real studio-blue-11 abs photo on the unchanged card.\n\nBoth complete films and subtitles are here; full-quality VLC copies are in Videos to Review. Scripted57.5s, off-the-cuff61.1s. The selected Warm & Vivid look, Balanced voice, take-specific cuts, caption words/groups/timing, comparison and endings are preserved.\n\nBoth candidates passed the maintained delivery gate after fresh independent complete-file review and narrow supported declarations. Raw results remain. Fresh normal own-mix AAC gates differ from the generic reference tone because Dan explicitly chose Balanced; off-cuff mixed outdoor-source floor may also differ. EVERY final AAC packet/timing matches R2, including both540p copies. Original acoustic alignment is explicitly inherited via audio identity, with fresh actual R3 caption pixel/sync and whole-speech checks. Generic composite hair/headroom detection and SourcePanel full-background correlation limitations are retained with actual native output review. Read independent reports for exact evidence and limits. No private gate, changed threshold, hidden missing input or blanket composite exception.\n\nNew graphic assets use maintained Soft Blue Light HyperFrames templates. The larger native interview photo is behind Dan's accepted real foreground hair. The real studio photo was already finalized/touched up; current standing real-photo wording remains. No new body editing, AI visual, source download or paid quality-review call.\n\nSource reused: ManVsStreet, Girls Like The Dad Bod Until We Showed Them This, https://www.youtube.com/watch?v=LbwgABvQdUA ; same locked source inset. New metered generation/review spend$0; editor/reviewer token usage unavailable from runtime.\n\nWorking evidence: {W}\nAll prior locked approval files/hashes remain intact. R1/R2 review files and VLC copies are preserved pending finalization.\n'''
(D/'Review notes - R3.md').write_text(notes)
result=dict(delivered_at=datetime.datetime.now().astimezone().isoformat(),review_url=receipt['review_url'],files=files,status='delivered_for_Dan_review',not_approved=True,not_uploaded=True,new_paid_spend=0)
(W/'delivery-receipt.json').write_text(json.dumps(result,indent=2));print('R3_PACKAGED',json.dumps(files),flush=True)
