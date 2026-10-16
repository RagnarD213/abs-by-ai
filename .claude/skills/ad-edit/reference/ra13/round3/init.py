from pathlib import Path
import json,shutil,hashlib
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');B=W/'round2';O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3')
for d in ['final','seg9','seg16','media','audio','hf9','hf16','context','stills','logs','checks9','checks16','review','preflight']: (O/d).mkdir(exist_ok=True,parents=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for f in ['track-all.json','words_individual.json','cta-layout.json','lead-trim.json'] :shutil.copy2(B/f,O/f)
for fmt in ['9','16']:
 (O/f'cap{fmt}').mkdir(exist_ok=True)
 for name in ['caption_states.json','captions.srt']:shutil.copy2(B/f'cap{fmt}'/name,O/f'cap{fmt}'/name)
 for s in json.load(open(B/'build-record.json'))['slots']:
  if s['piece'] is not None and fmt=='16':shutil.copy2(B/f'seg16/{s["name"]}.mp4',O/f'seg16/{s["name"]}.mp4')
 shutil.copy2(B/f'media/P2-{fmt}.mp4',O/f'media/P2-{fmt}.mp4')
for f in B.joinpath('audio').glob('*'):
 if f.is_file() and not f.name.startswith('._'):shutil.copy2(f,O/'audio'/f.name)
shutil.copy2(B/'recipe/cards.py',O/'recipe/cards.py')
cfg=json.load(open(B/'analysis-config.json'));cfg[0]['photo']='/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg';(O/'analysis-config.json').write_text(json.dumps(cfg,indent=2))
for n in ['quality_pass.py','prepare_checks.py','align_words.py','run_delivery_gates.py','review_files.py']:
 s=(B/'recipe'/n).read_text().replace("'round2'","'round3'").replace('RA-13 R2','RA-13 R3').replace('/round2/','/round3/')
 (O/'recipe'/n).write_text(s)
packet=dict(category='AD',job='RA-13',round=3,requested_changes=['Measure and center every vertical presenter landing using shared landing.py; preserve crop sizes and hair clearance.','B0550 generating then matching settled after-only results, unchanged phone geometry throughout.','Matching after_white_man.jpg in shared HyperFrames analysis in both formats.'],approved_elements=['All 1616 frames of spoken edit and captions','R2 lighter bass audio, exact AAC packets','Brighter Natural B','All horizontal presenter segment pixels and fixed framing','P2 workout/food phone tour and repaired CTA','No rejected lockscreen or stick figures'],authorization='Dan prompt plus handoff-20261016-ra13-round3-centering-white-man-phone.md authorizes both complete R3 review candidates; no setup.',inputs={str(p):sha(p) for p in [B/'build-record.json',B/'framing.json',Path('/Volumes/Extreme/_edit_work/ra04/round5/gen_white_man_rec.mp4'),Path('/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg')]},state='source preflight and capacity wait')
(O/'WORK_PACKET.json').write_text(json.dumps(packet,indent=2))
print('R3 INITIALIZED')
