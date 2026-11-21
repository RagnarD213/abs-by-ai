from pathlib import Path
import time,json,sys,subprocess,hashlib
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Extreme/_edit_work/ra13/round2')
# Existing delivered CTC + Whisper alignment is reusable only because every AAC packet is identical.
for fmt in ['9','16']:
 while not (O/'cta-repair.json').exists() or not any(x['format']==fmt for x in json.load(open(O/'cta-repair.json'))):time.sleep(10)
 assert next(x for x in json.load(open(O/'cta-repair.json')) if x['format']==fmt)['audio_bit_identical']
 subprocess.run([sys.executable,str(O/'recipe/prepare_checks.py')],check=True)
 D=O/f'checks{fmt}';v=next((O/'final').glob('*'+('9x16' if fmt=='9' else'16x9')+'*.mp4'))
 sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
 buildcap.wait('RA13 repaired exact-file checks '+fmt)
 with open(D/'audio-gate.log','w') as f:subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/audio_gate.py'),str(v),'--untreated',str(O/'audio/mix.wav.audio_untreated.json'),'--ab',str(D/'Audio AB - reference then RA13.m4a')],stdout=f,stderr=subprocess.STDOUT)
 with open(D/'native-watch.log','w') as f:subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),str(v),'--plan',str(D/'plan.json'),'--out',str(D/'watch'),'--log',str(D/'watch/logs/watch_pass.json')],stdout=f,stderr=subprocess.STDOUT,check=True)
 old=json.load(open(O/f'before-cta-repair/checks{fmt}/watch-image-hashes.json'));now={str(p.relative_to(D/'watch')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (D/'watch').rglob('*.jpg') if not p.name.startswith('._')};json.dump(dict(identical=[k for k in now if now[k]==old.get(k)],changed=[k for k in now if now[k]!=old.get(k)],old=old,new=now),open(D/'watch-carry-forward.json','w'),indent=2)
 print('REPAIRED WATCH READY',fmt,flush=True)
subprocess.run([sys.executable,str(O/'recipe/write_sheet.py')],check=True)
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/edit-sheet/validate.py'),str(next((O/'final').glob('*16x9*.mp4.edit-sheet.json'))),'--hash','--json',str(O/'edit-sheet-validation.json')],check=True)
subprocess.run([sys.executable,str(O/'recipe/prepare_checks.py')],check=True)
print('BOTH REPAIRED EVIDENCE READY',flush=True)
