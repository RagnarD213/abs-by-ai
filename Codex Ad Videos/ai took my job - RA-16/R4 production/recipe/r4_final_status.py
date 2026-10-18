"""Honest private-review disposition with actual unchanged numerical gate failures."""
import json,hashlib,time
from pathlib import Path
O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra16/round4')
def read(p):return json.load(open(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
review=read(O/'INDEPENDENT_REVIEW.json');films=[]
assert review.get('ready_for_dan_review') is True,'Independent reviewer has not cleared private review'
assert review.get('confirmed_open_defects')==[],'Confirmed film defects remain'
for a in ['9x16','16x9']:
 master=O/'masters'/f'AI Took Job AD R4 - {a}.mp4';h=sha(master);g=read(Path(str(master)+'.deliver_gate.json'));audio=read(Path(str(master)+'.audio_gate.json'));watch=read(O/'watch'/a/'watch_pass.json')
 assert g['sha256']==h and audio['sha256']==h
 assert g['rows']['watch:pass']['ok'] is True,(a,'independent watch not complete')
 assert any(x['aspect']==a and x['sha256']==h for x in review['masters']),(a,'review has wrong native identity')
 films.append({'aspect':a,'master':str(master),'sha256':h,'duration':g['duration'],'frames':1765,'fps':'30000/1001','delivery_gate_verdict':g['verdict'],'passed_rows':sum(x['ok'] is True for x in g['rows'].values()),'failed_rows':{k:v for k,v in g['rows'].items() if v['ok'] is False},'unmeasured_rows':{k:v for k,v in g['rows'].items() if v['ok'] is None},'audio_gate':audio,'watch_result':g['rows']['watch:pass']})
summary='Both complete films are ready for Dan review. Editor and independent picture/audio review found no remaining correction to the film content after one early phrase caption was delayed to its audible onset. Exact native scans found no black frames, freezes, unexplained jumps or naked splices. Approved Color B, crop pair 1, intro, warm bass voice and all R3 assets are retained. Automated delivery gates remain FAIL: approved voice tone and generic style/framing/cut metrics are outside their preset bounds; the word-highlight sync test cannot score phrase captions. These results remain in the record. This is private review, with final approval and release pending.'
status={'category':'AD','title':'AI Took Job AD R4','when':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'ready_for_dan_review':True,'approved_for_release':False,'dan_final_approval':'pending','published':False,'summary':summary,'films':films,'independent_review':{'path':str(O/'INDEPENDENT_REVIEW.json'),'sha256':sha(O/'INDEPENDENT_REVIEW.json'),'verdict':review.get('verdict')},'approved_inputs':str(O/'approval-verification.json'),'caption_repair':read(O/'CAPTION_REPAIR_READY.json'),'spend':{'new_generation_usd':0,'combined_quality_review_estimate_cap_usd':4,'actual_billed_usd':None,'editor_gemini_usage':{'input':42335,'visible_output':706,'thinking':4983},'independent_gemini_usage':{'input':42111,'visible_output':1704,'thinking':3583},'editor_and_reviewer_desktop_usage':'Unavailable in runtime; not zero','note':'Both initial full-film model reviews were within the under-$4 combined estimate. Actual billed provider charge unavailable. See review report for its estimate.'}}
assert '\u2014' not in summary and '\u2013' not in summary
(O/'final-review-status.json').write_text(json.dumps(status,indent=2))
old=read(O/'editor-self-QA.json');old['caption_repair_final']={'scope':'Only the phrase at 42.676 delayed to 43.1431 in both films; all final identities, independent review and machine flags in final-review-status.json','status_path':str(O/'final-review-status.json')};(O/'editor-self-QA.json').write_text(json.dumps(old,indent=2))
print(summary)
