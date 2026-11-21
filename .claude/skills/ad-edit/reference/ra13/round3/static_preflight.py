from pathlib import Path
import json,hashlib,ast
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');B=W/'round2'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();packet=json.load(open(O/'WORK_PACKET.json'))
assert packet['inputs']['/Volumes/Extreme/_edit_work/ra04/round5/gen_white_man_rec.mp4']=='108e0b9b9eaf17c6268c11aa62ad8f2745e92f0dc7c2a118438ffddb790b6d84'
assert packet['inputs']['/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg']=='dd9e88b936db9216163a8e3396669f976e388f185cb096113598e06ebb388763'
for p,h in packet['inputs'].items():assert sha(p)==h,(p,'changed')
for p in (O/'recipe').glob('[!._]*.py'):ast.parse(p.read_text());assert '\u2014' not in p.read_text() and '\u2013' not in p.read_text(),p
r=json.load(open(B/'build-record.json'));assert r['frames']==1616 and all(a['f1']==b['f0'] for a,b in zip(r['slots'],r['slots'][1:]));assert len([s for s in r['slots'] if s['piece'] is not None])==6
for p in (O/'seg16').glob('[!._]*.mp4'):assert sha(p)==sha(B/'seg16'/p.name)
assert packet['requested_changes'] and len(packet['requested_changes'])==3
(O/'static-preflight.json').write_text(json.dumps(dict(status='PASS',scope='Source and baseline hashes; recipe syntax; contiguous 1616-frame timeline; six actual presenter landings; horizontal segment byte identity. Actual pixels and moving media remain pending.',inputs=packet['inputs']),indent=2));print('STATIC PREFLIGHT PASS')
