from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');D=R/'Codex Ad Videos/why do most guys never get abs - RA-13';J=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
audit=J(O/'independent-audit/audit.json');assert not audit['open_media_defects'],'Independent review still has media defects'
qc=D/'R3 QC';qc.mkdir(exist_ok=True);reb=D/'R3 Rebuild';reb.mkdir(exist_ok=True);videos=[];flags={}
for fmt,label,name in [('9','9x16','vertical'),('16','16x9','horizontal')]:
 C=O/f'checks{fmt}';g=J(C/'delivery-gate.json');w=J(C/'watch-final/logs/watch_pass.json');assert w['inspected'] and w['open_defects']==0
 v=next((O/'final').glob('[!._]*'+label+'*.mp4'));assert sha(v)==sha(D/v.name)==sha(R/f'Videos to Review/Most Guys Abs AD R3 - {name}.mp4')
 flags[label]=[dict(key=x['key'],detail=x['detail']) for x in g['rows'] if not x.get('ok') and not x.get('na')]
 videos.append(dict(format=label,path=str(D/v.name),sha256=sha(v),frames=1616,duration=1616/(30000/1001),delivery_gate=g['verdict'],open_rows=flags[label]))
 Q=qc/label;Q.mkdir(exist_ok=True)
 for p,n in [(C/'delivery-gate.json','delivery-gate.json'),(C/'watch-final/logs/watch_pass.json','watch-pass.json'),(C/'audio-gate.log','audio-gate.log'),(C/'hyperframes.log','hyperframes.log'),(C/'plan.json','plan.json'),(C/'negative-scan.json','negative-scan.json')]:shutil.copy2(p,Q/n)
 for p in (O/'final').glob(v.name+'.*'):
  if p.is_file() and not p.name.startswith('._'):shutil.copy2(p,D/p.name)
for p in (O/'recipe').glob('[!._]*.py'):shutil.copy2(p,reb/p.name)
for n in ['WORK_PACKET.json','build-record.json','framing.json','analysis-config.json','phone-source.json','preservation.json','head-silhouette-measurements.json','motion-native.json','crop-quantization-proof.json','asset-preflight-review.json','editor-selfqa.json','relocation.json','audio-selftest.json','edit-sheet-validation-9x16.json','edit-sheet-validation-16x9.json','scene-content-map.json']:shutil.copy2(O/n,reb/n)
shutil.copytree(O/'independent-audit',qc/'independent-audit',dirs_exist_ok=True)
shutil.copy2(O/'native-proof/report.json',qc/'native-frame-proof.json')
shutil.copy2(O/'checks9/Audio AB - reference then RA13.m4a',D/'Most Guys Abs AD R3 - Audio AB.m4a')
ledger=J(O/'cost-ledger-r3.json');ledger['runs']=[]
for p in O.rglob('*.receipt.json'):
 if p.name.startswith('._'):continue
 j=J(p);ledger['runs'].append(dict(receipt=str(p),model=j.get('model'),usage=j.get('usage'),actual_billed_usd=j.get('actual_billed_usd')))
(O/'cost-ledger-r3.json').write_text(json.dumps(ledger,indent=2));shutil.copy2(O/'cost-ledger-r3.json',D/'cost-ledger-r3.json')
summary='R3 independent picture and audio review passed both formats. Vertical head centering, one-phone white-man generation/results and matching analysis photo checked. Exact numerical gate results remain visible below; no thresholds changed.'
status=dict(category='AD',job='RA-13',round=3,review_delivery_complete=True,release_ready=all(v['delivery_gate']=='PASS' for v in videos),summary=summary,videos=videos,open_gate_rows=flags,independent_media_defects=[],review_url='http://127.0.0.1:8973/',when=datetime.datetime.now().isoformat(),provider_cost_ledger=str(D/'cost-ledger-r3.json'))
for p in [O/'delivery-status.json',D/'delivery-status-r3.json']:p.write_text(json.dumps(status,indent=2))
notes='''AD. Most Guys Abs AD R3. Both complete review candidates delivered.

Both: 53.9205 seconds, 1616 frames, 30000/1001 fps. Native vertical 1080x1920 and horizontal 1920x1080.
Review: http://127.0.0.1:8973/
Physical full-quality copies: Videos to Review/Most Guys Abs AD R3 - vertical.mp4 and horizontal.mp4.

Changes in the NEW full films:
Vertical centering: exact whole-head anchors at 0.000, 2.269, 25.158, 38.972, 42.609 and 46.580. Shared land-then-hold track. Watch 0 - 6, 24.5 - 29, and 38.5 - 48. Hair and crop sizes preserved.
14.348 - 25.158: existing B0550 white-man generation and his own settled after-only result, both inside the same unchanged phone frame. Internal screen cut at 20.587. Watch 13 - 27.
28.362 - 33.767: matching white-man after picture in the existing analysis scan, three bars and plan, both formats. Watch 27 - 35.

Preserved: full spoken edit and captions, Brighter Natural B, approved lighter-bass audio, horizontal static framing and close-shot headroom, P2 workout/food tour, repaired CTA. Original AAC packets are identical. Rejected lockscreen and stick-figure scenes remain absent. No new generation and no upload/setup.

Independent complete-candidate media review and native evidence are in R3 QC. Every-frame scans and native consecutive join/scene evidence supplement sampled full-video model reviews. No human continuous native-rate playback is claimed. All browser tests were muted and players left paused.

Exact numerical gate results, separate from the media revisions:
'''
notes+='\nNative-frame vertical crop measurements in source pixels (2160x3840):\n'
for row in J(O/'motion-native.json')['rows']:
 m=row['motion'];notes+=f"{row['name']}: travel {m['travel_px']} px; p90 speed {m['pan_p90_px_s']} px/s; moving {m['moving_frac']*100:.1f}%; head offset median/max {m['off_centre_px']['median']}/{m['off_centre_px']['max']} px.\n"
notes+='Motion uses actual integer crop coordinates; head offset uses source whole-head samples interpolated per frame. Exact finished landing positions are checked separately in native-proof/report.json.\n'
for fmt,rows in flags.items():notes+='\n'+fmt+':\n'+('\n'.join('- '+x['key']+': '+x['detail'] for x in rows) if rows else 'No failed numerical rows.')+'\n'
notes+='\nNo thresholds were changed and no PASS stamp was invented. These are private review candidates awaiting Dan, not finalized videos.\n\nNew generation: $0. Review estimate: under $3. Actual provider billing and editor/reviewer token totals unavailable where the runtime does not expose them; available model usage is retained in cost-ledger-r3.json.\n'
assert '\u2014' not in notes and '\u2013' not in notes
(O/'review-notes.txt').write_text(notes);(O/'review/R3 review notes.txt').write_text(notes);shutil.copy2(D/'Most Guys Abs AD R3 - Audio AB.m4a',O/'review/Most Guys Abs AD R3 - Audio AB.m4a');(D/'Most Guys Abs AD R3 - review notes.txt').write_text(notes)
print('FINAL REVIEW PACKAGE COMPLETE',flush=True)
