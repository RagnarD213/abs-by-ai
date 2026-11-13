"""RO-32 approved-master admission. Preserve actual FAIL stamps and narrow approved overrides."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[4]
MASTER=ROOT/"claude edited long form content/31 - I'm 41. Here Are The 10 Exercises I Do Every Week/FINAL_RO-32_Im-41-10-Exercises.mp4"
EVIDENCE=Path('/Volumes/Extreme/_edit_work/RO-32/round1/final_r3')
SHA='414b54da03280c49683dbe8d7bc4962ebceae13ab5bea16a6bbcffb3f03ef10d'
OVERRIDES={
'audio:stamp':'Dan approved this exact bass-lift mix. Only tone fails; preserve approved audio without alteration.',
'cut:jump_cut':'Two lower-third segment boundaries in one continuous source take, C1771-W2 at4:13/4:19. Not picture jump cuts. Preserve exact approved film.',
'captions:card_collision':'SRT is an optional subtitle sidecar, not burned-in captions over the cards. Approved film and optional subtitles remain separate.',
'captions:burned':'Graphic/lower-third text detected as subtitles. Film contains no burned subtitle track; Dan approved exact graphics.'}
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def check():
 assert digest(MASTER)==SHA,'Approved master changed'
 g=json.loads((EVIDENCE/'RO32_MASTER.mp4.deliver_gate.json').read_text());a=json.loads((EVIDENCE/'RO32_MASTER.mp4.audio_gate.json').read_text())
 sys.path.insert(0,str(ROOT/'.claude/skills/_shared/deliver'));import gate
 assert g['gate_version']==gate.GATE_VERSION
 assert g['sha256']==a['sha256']==SHA
 bad={k for k,v in g['rows'].items() if not v['ok']};assert bad==set(OVERRIDES),bad
 assert [v['key'] for v in a['rows'] if not v['ok']]==['tone']
 result={'master':str(MASTER),'sha256':SHA,'bytes':MASTER.stat().st_size,'gate_version':g['gate_version'],'original_gate_verdict':g['verdict'],'passing_rows':sum(v['ok'] for v in g['rows'].values()),'failing_rows':list(bad),'documented_overrides':OVERRIDES,'authorization':'Dan exact-film approval 2026-11-13: Okay, it looks good. This is approved. Proceed to setup. User reconfirmed preserve film and documented overrides on setup resume.','admission':'ACCEPTED_WITH_DOCUMENTED_OVERRIDES','gate_or_threshold_changes':False,'film_changed':False}
 (Path(__file__).parent/'exact-file-upload-gate.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':print(json.dumps(check(),indent=2))
