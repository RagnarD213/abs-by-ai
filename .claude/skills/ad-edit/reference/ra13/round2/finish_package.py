from pathlib import Path
import json,shutil,hashlib,datetime
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=W/'round2';D=R/'Codex Ad Videos/why do most guys never get abs - RA-13';J=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
audit=J(O/'independent-audit/audit.json');assert not audit['open_media_defects'];rows={};videos=[]
for fmt,label in [('9','9x16'),('16','16x9')]:
 C=O/f'checks{fmt}';gate=J(C/'delivery-gate.json');cut=next(x for x in gate['rows'] if x['key']=='cut:splice_visibility');assert cut['value']['joins']==10,'Final corrected-inventory gate must finish first'
 watch=J(C/'watch-final/logs/watch_pass.json');assert watch['inspected'] and watch['open_defects']==0 and watch['boundaries']==17
 rows[label]=[dict(key=x['key'],detail=x['detail']) for x in gate['rows'] if not x.get('ok') and not x.get('na')];v=next((O/'final').glob('*'+label+'*.mp4'));assert sha(v)==sha(D/v.name)
 videos.append(dict(format=label,path=str(D/v.name),sha256=sha(v),frames=1616,duration=53.92053333333333,delivery_gate=gate['verdict'],open_rows=rows[label]))
 q=D/'QC'/label;q.mkdir(parents=True,exist_ok=True)
 for src,name in [(C/'delivery-gate.json','delivery-gate.json'),(C/'audio-gate.log','audio-gate.log'),(C/'hyperframes.log','hyperframes.log'),(C/'watch-final/logs/watch_pass.json','watch-pass.json'),(O/f'independent-audit/findings{fmt}-final.json','independent-findings.json')]:
  if isinstance(src,Path):shutil.copy2(src,q/name)
  else:raise AssertionError()
 # Exact-file sidecars retain their original full names beside the native review candidates.
 for p in (O/'final').glob(v.name+'.*'):
  if p.is_file() and not p.name.startswith('._'):shutil.copy2(p,D/p.name)
shutil.copy2(O/'checks9/Audio AB - reference then RA13.m4a',D/'Audio AB - reference then RA13.m4a')
rebuild=D/'Rebuild';rebuild.mkdir(exist_ok=True)
for p in (O/'recipe').glob('*.py'):
 if not p.name.startswith('._'):shutil.copy2(p,rebuild/p.name)
for n in ['build-record.json','framing.json','analysis-config.json','cta-layout.json','lead-trim.json','lock-verification.json','edit-sheet-validation.json','cta-repair.json','copy-verification.json','asset-context-review.json']:
 shutil.copy2(O/n,rebuild/n)
for src,n in [(W/'cut.json','original-cut.json'),(O/'words_individual.json','words_individual.json'),(O/'track-all.json','track-all.json'),(W/'round2-plan/decisions.json','decisions.json'),(W/'source/lav_selection.json','lav_selection.json'),(W/'source/roll.json','roll.json'),(W/'grade-options.json','grade-options.json'),(O/'audio/mix.wav.voice_chain.json','voice-chain.json'),(O/'audio/mix.wav.audio_untreated.json','audio-baseline.json')]:
 if src.exists():shutil.copy2(src,rebuild/n)
shutil.copy2(O/'audio/cut_trim.wav',rebuild/'untreated-cut.wav')
for n in ['audit.json','audit.md']:
 shutil.copy2(O/'independent-audit'/n,D/('Independent audit.'+n.split('.')[-1]))
summary='Independent picture and audio review passed both formats. Full automated delivery gates remain FAIL for the approved voice versus the studio reference, approved horizontal wide framing, and deliberate zoom cuts. These are R2 review candidates; the locked choices are preserved.'
status=dict(category='AD',job='RA-13',round=2,review_delivery_complete=True,release_ready=False,summary=summary,videos=videos,open_gate_rows=rows,independent_media_defects=[],review_url='http://127.0.0.1:8973/',actual_provider_billing_usd=None,estimated_session_review_usd_upper_bound=3,new_generation_usd=0,reviewer_usage='Codex editor/reviewer model and token usage unavailable; Gemini usage in attached receipts.',native_folder_open='Not opened automatically: Mac was locked.',when=datetime.datetime.now().isoformat())
(O/'delivery-status.json').write_text(json.dumps(status,indent=2));(D/'delivery-status.json').write_text(json.dumps(status,indent=2))
notes='''AD. Most Guys Abs AD R2. Delivered for review.

Both formats: 53.9205 seconds, 1616 frames at 30000/1001 fps.
9x16:1080x1920. 16x9:1920x1080. Same edit and bit-identical audio.
Review: http://127.0.0.1:8973/
Full-quality physical copies: Videos to Review/Most Guys Abs AD R2 - vertical.mp4 and horizontal.mp4.

Approved choices preserved: Brighter Natural B, vertical738x1312/630x1120, horizontal2144x1206/1728x972, lighter bass voice with no dereverb.
Horizontal close headroom reduced by20 source pixels, about30.9% of the original64.8px gap; crop size and fixed center1080 retained. Minimum sampled close hair clearance38source pixels.

Changes and short watch ranges on the NEW full film:
0.00: removed0.6006seconds of empty lead, all spoken words preserved. Watch0-3.
2.27-14.35,25.16-28.36,42.61-46.58: horizontal close headroom. Quick ranges2-6,24.5-29,42-47.
14.35-25.16: approved same-person real sunglasses photo to AI pool goal; brief presenter island covered. Watch13-27.
25.16-28.36: distorted proposed lockscreen clip removed, presenter carries the line. Watch24.5-29.
28.36-33.77: shared current analysis card, same photo/scan/three bars/plan, no printed numbers. Watch27-35.
33.77-38.97: retained workout and food phone tour; source scene changes at35.769. Watch32.5-40.
38.97-46.58: stick-figure workout clip removed, presenter carries the changing-plan lines. Watch39-47.
51.38-53.92: CTA moved clear of abs/captions. Vertical sits over shorts, horizontal in left pool. Same wording, no URL. Watch51-53.92.

Independent media audit: passed after CTA repair. Both full actual files were supplied with audio; model video sampling requested4fps high resolution. Separate all-frame scans and74 individually accounted native review images,17inspection points per format, include every required scene, freeze candidate, app-screen cut and finalfive frames. Identical observed images were carried only with verified SHA matching. No human native-rate playback is claimed.

Exact numerical delivery gates remain FAIL. No thresholds changed, no invented pass and no repeat request to approve locked voice or crops. The independent reviewer observed deliberate scale changes at flagged zoom cuts and continuous picture at the audio-only seam.
'''
# Plain language spacing for the human report.
import re
notes=re.sub(r'(?<=[A-Za-z])(?=\d)', ' ',notes);notes=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',notes);notes=notes.replace('under$','under $').replace('spend$','spend $').replace('9 x 16','9:16').replace('16 x 9','16:9').replace('AD R 2','AD R2').replace(':1080',': 1080').replace(':1920',': 1920').replace('finalfive','final five').replace('.mp 4','.mp4').replace('RA-13 R 2','RA-13 R2')

for label,rr in rows.items():
 notes+='\n'+label+' open numerical rows:\n'+'\n'.join('- '+x['key']+': '+x['detail'] for x in rr)+'\n'
notes+='''
All raw gate results and independent findings are in QC/. The audio A/B, edit sheet, framing proof and source-specific rebuild facts are included. Natural camera motion continues through the ending tail. No video was uploaded or published. Master-list status is delivered for review, not finalized.

Provider review estimate: under $3 for this session. Actual billed dollars unavailable; Gemini token receipts are retained. New generation spend $0. Codex editor/reviewer model and token totals unavailable.
'''
assert '\u2014' not in notes and '\u2013' not in notes
(D/'Most Guys Abs AD R2 - review notes.txt').write_text(notes);(O/'review-notes.txt').write_text(notes)
for fmt in ['9','16']:(O/f'checks{fmt}/automatic-stage.json').write_text(json.dumps(dict(status='All checks measured; review delivered, numerical gate failures retained.',delivery_gate='FAIL',native_watch_inspected=True,open_media_defects=0),indent=2))
p=W/'WORK_PACKET.json';d=J(p);d.update(state='R2 review delivered, numerical release flags retained',status='delivered_for_review',duration_estimate=53.9205333333,full_delivery=False,review_delivery_complete=True,release_ready=False,pending=['Dan review; numerical release flags remain explicit'],next='Review both R2 copies. Preserve locked choices. Do not upload using FAIL gate stamps.',delivery_status=str(O/'delivery-status.json'));p.write_text(json.dumps(d,indent=2))
qa=J(O/'editor-selfqa.json');qa.update(status='Media self-QA complete, numerical gates FAIL as recorded.',pending=[],repaired_cta='Viewed native ending strips and pairs for both; abs, face and captions clear.',additional_native_views='All9 new final-inventory images viewed by editor: P2cut and finalfive frames plus horizontalP1pair.',delivery_gate_status=rows);(O/'editor-selfqa.json').write_text(json.dumps(qa,indent=2))
runs=[]
for p in O.rglob('*.receipt.json'):
 if not p.name.startswith('._'):
  d=J(p);runs.append(dict(receipt=str(p),model=d['model'],usage=d['usage'],actual_billed_usd=d.get('actual_billed_usd')))
ledger=J(O/'cost-ledger-r2.json');ledger['runs']=runs;(O/'cost-ledger-r2.json').write_text(json.dumps(ledger,indent=2));shutil.copy2(O/'cost-ledger-r2.json',D/'cost-ledger-r2.json')
print('PACKAGE COMPLETE: both review candidates, all exact-file evidence, independent audit and open numerical flags recorded.')
