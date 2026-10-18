"""Save task-only text records in a clean checkout; media stays private."""
import json,shutil,re
from pathlib import Path
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra16/round4');C=Path(json.load(open('/tmp/ra16-r4-save-checkout.json'))['path']);rel=Path('Codex Ad Videos/ai took my job - RA-16/R4 production');D=C/rel;D.mkdir(parents=True,exist_ok=True)
q=json.load(open(O/'final-review-status.json'));assert q['ready_for_dan_review']
paths=list((O/'recipe').glob('*.py'))+list(O.glob('*.json'))+[O/'INDEPENDENT_REVIEW.txt',O/'production-lessons.md']
for part in ['evidence','editor-audit','independent-extra','independent-repair']:
 paths+=list((O/part).glob('*.json'))
paths+=list((O/'watch').glob('*/watch_pass.json'))
for p in paths:
 if p.name.startswith(('._','superseded-')):continue
 dest=D/p.relative_to(O);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
for p in (O/'masters').glob('*.json'):
 dest=D/'master-checks'/p.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(p,dest)
shutil.copy2(O/'index.html',D/'index.html')
(D/'STATUS.txt').write_text('AD. R4 complete films delivered for Dan review. Both58.89seconds. Final gates retain approved tone and generic picture-metric flags; phrase-caption sync is not a highlighted-word test. Native media stays private. No publishing. See final-review-status.json and INDEPENDENT_REVIEW.txt.\n'.replace('Both58.89seconds','Both 58.89 seconds'))
report='AD. AI Took Job AD R4, complete films ready for Dan review, 2026-10-17.\n\n'+q['summary']+'\n\n'
for f in q['films']:
 report+=f"{f['aspect']}: {f['duration']:.6f} seconds,1765 frames at30000/1001. SHA256 {f['sha256']}\n".replace('seconds,1765','seconds, 1765').replace('at30000','at 30000')
 report+='Final delivery gate: '+f['delivery_gate_verdict']+'. Failed rows: '+', '.join(f['failed_rows'])+'. Unmeasured: '+', '.join(f['unmeasured_rows'])+'.\n\n'
report+='Final caption repair: the phrase And finally, AI adjusts begins at43.1431. Watch42-45seconds. The horizontal prior phrase clears before the graphic changes caption position.\n\nReview: http://127.0.0.1:8976/\nNative copies: Videos to Review and Codex Ad Videos/ai took my job - RA-16.\n\nNo generation spend. Combined model-review estimate was under$4; actual provider billing and desktop editor/reviewer usage are unavailable, not zero. Provider token counts are retained in final-review-status.json.\n\nThe main checkout has unrelated Git object/merge problems. Task-only records were saved through a clean remote checkout without modifying other sessions\' implementation. No video media is pushed.\n'
report=report.replace('at43.1431','at 43.1431').replace('Watch42-45seconds','Watch 42-45 seconds').replace('under$4','under $4')
assert '\u2014' not in report and '\u2013' not in report
rp=Path('Handoffs/video-editing/reports/RA-16-R4-review-report.txt');(C/rp).write_text(report);(R/rp).write_text(report)
lesson=Path('Media/codex-video-trial/skills/abs-edit-ad/references/ra16-r4-production-lessons.md');(C/lesson).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/'production-lessons.md',C/lesson)
entry='**AI Took Job AD R4 REVIEW 2026-10-17, Codex.** Both58.89-second full films checked and independently reviewed at :8976; native copies in Videos to Review. Approved choices retained; actual technical flags remain in the report. Next: Dan reviews both complete films. No publishing. Detail: `Handoffs/video-editing/reports/RA-16-R4-review-report.txt`.'.replace('Both58.89','Both 58.89')
for root in [R,C]:
 p=root/'AI_COORDINATION.md';text=p.read_text();matches=re.findall(r'^\*\*AI Took Job AD R4[^\n]*',text,re.M)
 if matches:text=text.replace(matches[0],entry,1)
 else:text=text.replace('# ACTIVE\n','# ACTIVE\n\n'+entry+'\n',1)
 p.write_text(text)
 p=root/'Handoffs/video-editing/00-MASTER.md';text=p.read_text();lines=text.splitlines();lines=[('| [RA-16](RA-16-ai-took-my-job.md) | AI Took My Job | C1668 | R4 complete9:16/16:9 films ready for Dan review, :8976; no publishing | S |'.replace('complete9','complete 9') if line.startswith('| [RA-16]') else line) for line in lines];p.write_text('\n'.join(lines)+'\n')
# Remove only this now-executed handoff from the remote OPEN list. Main file has another session's merge conflict and is left to its owner.
p=C/'Handoffs/README.md';text=p.read_text();text='\n'.join(line for line in text.splitlines() if not line.startswith('| [AI Took Job AD R4](handoff-20261016-ra16-round4-approved-assets-full-film.md)'))+'\n';p.write_text(text)
json.dump({'checkout':str(C),'paths':[str(rel),'AI_COORDINATION.md','Handoffs/README.md','Handoffs/video-editing/00-MASTER.md',str(rp),str(lesson)]},open('/tmp/ra16-r4-save-files.json','w'),indent=2)
print('Task-only records prepared, media excluded')
