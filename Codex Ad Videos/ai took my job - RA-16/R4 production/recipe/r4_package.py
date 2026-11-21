"""Copy actual final evidence and matching hashes into the private delivery package."""
from pathlib import Path
import json,shutil,hashlib,re
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra16/round4');D=R/'Codex Ad Videos/ai took my job - RA-16';P=D/'R4 production'
P.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert (O/'INDEPENDENT_REVIEW.json').exists(),'Independent verdict required'
status=json.load(open(O/'final-review-status.json'));assert status['ready_for_dan_review']
for part in ['recipe','evidence','editor-audit','watch','logs','independent-extra']:
 shutil.copytree(O/part,P/part,dirs_exist_ok=True,ignore=shutil.ignore_patterns('._*','__pycache__','*.pyc'))
for p in O.glob('*.json'):shutil.copy2(p,P/p.name)
for p in O.glob('INDEPENDENT_REVIEW.*'):shutil.copy2(p,P/p.name)
shutil.copy2(O/'production-lessons.md',P/'production-lessons.md')
for p in (O/'masters').glob('*.framing_proof.jpg'):shutil.copy2(p,P/'evidence'/p.name)
for p in (O/'masters').glob('*.json'):shutil.copy2(p,D/p.name)
for p in (O/'audio').glob('Audio AB*.mp4'):shutil.copy2(p,D/p.name)
for a in ['9x16','16x9']:
 m=O/'masters'/f'AI Took Job AD R4 - {a}.mp4';shutil.copy2(m,D/m.name)
 v=O/'review'/f'AI Took Job AD R4 - {a} - REVIEW.mp4';shutil.copy2(v,D/v.name)
 assert sha(D/m.name)==sha(m)
notes='AD. AI Took Job AD R4. Complete films for Dan review, not publication.\n\n'+status['summary']+'\n\nBoth films contain 1765 frames at 30000/1001 and run 58.892167 seconds. Approved Color B, medium crop pair 1, complete intro, warm bass voice and D01/G01/G02/G03 content were retained. Sound is packet-identical in both formats. Final word ends about 58.74 seconds.\n\nR4 corrects final framing and applies captions once. The phrase "And finally, AI adjusts" starts at 43.1431 seconds, after the confirmed quiet breath. Watch 42-45 seconds for that final repair. The first full-render attempt was rejected in editor QA because a silhouette model classified trees as hair. The repaired source measurement stays connected to the measured face and excludes background components; source crop windows remain 800x1422/612x1088 vertically and 2160x1216/1728x972 horizontally. Validated source hair required only small upward adjustments. Original rejected candidates remain isolated outside delivery.\n\nWatch in the new full film: phone 19.39-24.19, analysis 25.26-32.80, plan lower third 32.80-38.10, life-change lower third 42.68-47.41. Useful watch ranges 17-27, 30-40, 41-49 seconds. This is the first full-film review; opening and complete ending also need Dan review.\n\nReview page http://127.0.0.1:8976/; full native copies also in Videos to Review. No upload, ad setup or publishing occurred.\n\nEvidence distinguishes exact native automated scans, local chronological and boundary image observations, model full video/audio observations at 5 fps, independent review, and Dan approval. No continuous human watch or native audio perception is claimed. Costs and available usage are recorded in final-review-status.json; unavailable billing or session counters are not zero.\n'
assert '\u2014' not in notes and '\u2013' not in notes
(D/'R4 notes.txt').write_text(notes)
(P/'STATUS.txt').write_text('AD. R4 complete films delivered for Dan review. See R4 notes.txt, final-review-status.json and INDEPENDENT_REVIEW.txt. Not published or finalized.\n')
print('Private delivery package copied and native master hashes verified')
