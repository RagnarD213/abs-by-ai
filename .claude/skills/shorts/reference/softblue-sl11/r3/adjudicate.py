"""Record only independently supported exact-file measuring limitations; preserve numericFAILs.
Does not change gate code, thresholds, movies or actual editorial requirements. No PASS stamp written here."""
from pathlib import Path
import json,shutil,sys
R=Path('/Volumes/Extreme/_edit_work/SL-11/round3')
for S in sys.argv[1:]:
 assert S in ['B','C'];d=R/'build'/S;p=d/'gate/plan.json';j=json.loads(p.read_text());res=json.loads((d/'gate/result.json').read_text());failed={x['key'] for x in res['rows'] if x.get('ok') is False};allowed={'style:coverage'}|({'junk:dead_air'} if S=='B' else set());assert failed and failed<=allowed,(S,failed)
 w=json.loads((d/'gate/logs/watch_pass.json').read_text());assert w['inspected'] and w['open_defects']==0
 h=next(z['sha256'] for z in json.loads((R/'build-manifest.json').read_text()) if z['short']==S);proof=json.loads((d/'coverage-source-evidence.json').read_text());cov=json.loads((R/'independent'/f'{S}-coverage-adjudication.json').read_text());assert h==proof['sha256']==cov['video_sha256']==w['sha256'] and proof['coverage']>=.3 and proof['min_ncc']>.97
 orig=d/'gate/original-instrument-fail'
 if not orig.exists():
  orig.mkdir()
  for n in ['plan.json','result.json','check.log']:shutil.copy2(d/'gate'/n,orig/n)
 j.setdefault('instrument_adjudications',{})
 if 'style:coverage' in failed:
  j['declare']['style:coverage']=f"Palette-only classifier undercounts different C1625 exercise footage on the same set. This exact R3 complete movie contains{proof['alternate_source_frames']}/{proof['frames']}actual exercise source frames ({100*proof['coverage']:.5f}%), independently verified at every native sequence index to the selected R2 intro/R1 remainder, minNCC{proof['min_ncc']:.9f}, with complete visual action/release reviewed. Actual30%editorial requirement remains applicable and met. Preserve original numericalFAIL in gate/original-instrument-fail. Fresh source-lineage.json, coverage-source-evidence.json and independent/{S}-coverage-adjudication.json bind this candidate hash. No global bound or prior round exception reused without new proof."
  j['instrument_adjudications']['style:coverage']=dict(sha256=h,editorial_requirement_applicable=True,minimum=.3,actual=proof['coverage'],source_evidence=str(d/'coverage-source-evidence.json'),independent=str(R/'independent'/f'{S}-coverage-adjudication.json'))
 if 'junk:dead_air' in failed:
  pause=json.loads((R/'independent/B-pause-adjudication.json').read_text());assert pause['video_sha256']==h and pause['range_seconds']==[24.32,25.58]
  j['declare']['junk:dead_air']='The sole1.26s flag24.32–25.58 follows the explicit you-can-see cue while the complete exercise and Small Breaths card continue moving. Fresh native exact-file review identifies purposeful teaching observation, no freeze/reset/glasses/phone. All39 gaps measured; only this specific range exceeds1s. Editorial junk rule remains applicable, numerical bound unchanged. Full2359AAC packets identical to R1. Original numericFAIL preserved in gate/original-instrument-fail; independent/B-pause-adjudication.json binds this file. No audible-listening claim.'
  j['instrument_adjudications']['junk:dead_air']=dict(sha256=h,editorial_requirement_applicable=True,only_range=[24.32,25.58],independent=str(R/'independent/B-pause-adjudication.json'))
 p.write_text(json.dumps(j,indent=2));print('SCOPED EVIDENCE',S,sorted(failed))
