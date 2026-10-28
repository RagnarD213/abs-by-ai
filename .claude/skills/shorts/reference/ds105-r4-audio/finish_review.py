from pathlib import Path
import json,shutil,subprocess,hashlib
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];P=W.parent/'round2/review'
v=W/'review/media/Why I Wear A Mouthpiece For SFC R4 - full 1080p.mp4';sha='061deb744eb1e83cf1917727095214c8e4ea68ffebf56d9f85042d80694eebe2'
assert hashlib.sha256(v.read_bytes()).hexdigest()==sha
j=json.loads((W/'evidence/FULL-delivery.json').read_text());rows={r['key']:r for r in j['rows']}
assert rows['compliance:negative_events']['ok'] is True,'Full gate rerun not complete/current'
expected={'audio:stamp','style:coverage','cut:splice_visibility'};failed={k for k,r in rows.items() if r['ok'] is False};assert failed==expected,failed
watch=json.loads((W/'evidence/FULL-watch.json').read_text());assert watch['inspected'] and watch['open_defects']==0 and len(watch['judged'])==27
stamp=json.loads(Path(str(v)+'.deliver_gate.json').read_text());assert stamp['sha256']==sha and stamp['verdict']=='FAIL'
counts=dict(passed=sum(r['ok'] is True for r in j['rows']),failed=len(failed),unmeasured=sum(r['ok'] is None and not r['na'] and not r['review'] for r in j['rows']),na=sum(bool(r['na']) for r in j['rows']))
(W/'records/final-gate-summary.json').write_text(json.dumps(dict(verdict=j['verdict'],counts=counts,failures=sorted(failed),version=j['gate_version'],sha256=sha),indent=2))
text=f'''Independent review found no confirmed new picture or audio defect. The exact B gentle cleanup is applied throughout. Every picture frame is unchanged from R2. Full offline model audio inspection confirmed complete speech and no confirmed added distortion; browser playback and seeking were tested muted, not represented as an audible listening pass.
The completed automated gate remains FAIL: {counts['passed']} passed, {counts['failed']} failed and {counts['unmeasured']} unmeasured. The remaining flags concern the chosen voice versus an older reference, camera-only coverage and deliberate wider/closer cuts. Built-in framing and caption-sync measurements remain unavailable; existing dense picture checks remain applicable because both picture streams are byte-identical. No thresholds were relaxed.
Normal loudness, clipping, duration, source-relative processing-damage and exact chosen-B preservation checks pass. This finished preview awaits Dan's final review. Nothing is published or scheduled. New audio QA batch estimated under $0.25, 4,775 tokens; invoice unavailable.
'''
(W/'records/qa-summary.txt').write_text(text)
report=W/'evidence/independent/review.md';notes=W/'review/notes/independent-review-R4.md'
add=f"\n\n## Final gate completion, recorded by production editor\n\nThe complete exact-file rerun finished: {counts['passed']} PASS / {counts['failed']} FAIL / {counts['unmeasured']} NOT MEASURED / {counts['na']} N/A, overall FAIL. The current-hash manual assessment record passes after the independent reviewer explicitly assessed all64 R4 samples; the initial old-SHA failure and corrected sheet-metadata binding evidence remain retained. Three genuine remaining failures are unwaived: {', '.join(sorted(failed))}. No movie bytes or thresholds changed.\n"
notes.write_text(report.read_text()+add)
shutil.copyfile(W/'evidence/FULL-gate.log',W/'review/notes/automated-checks-R4.txt')
shutil.copyfile(W/'evidence/listener/review.txt',W/'review/notes/audio-listening-R4.txt')
subprocess.run(['python3',str(W/'recipe/page.py')],check=True)
for rel in ['index.html','notes/independent-review-R4.md','notes/audio-listening-R4.txt','notes/automated-checks-R4.txt']:
 shutil.copyfile(W/'review'/rel,P/rel)
D=R/'Short-form video content/DS-105 mouthpiece/R4 review'
for name in ['FULL-delivery.json','FULL-gate.log','preservation.json','transient-source-comparison.json']:
 shutil.copyfile(W/'evidence'/name,D/name)
for name in ['independent-review-R4.md','audio-listening-R4.txt','automated-checks-R4.txt']:shutil.copyfile(W/'review/notes'/name,D/name)
for suffix in ['.audio_gate.json','.audio_untreated.json','.deliver_gate.json']:shutil.copyfile(Path(str(v)+suffix),D/(v.name+suffix))
shutil.copyfile(W/'audio/B-selected-full.wav',D/'B-selected-full.wav');shutil.copyfile(W/'records/selected-B-provenance.json',D/'selected-B-provenance.json')
state=json.loads((W/'execution-state.json').read_text());state.update(checkpoint='full_checks_complete_final_delivery_verification',master=str(v),sha256=sha,reviewUrl='http://127.0.0.1:9275/',finalGate=dict(verdict='FAIL',counts=counts,failed=sorted(failed)),independentReview='READY FOR DAN REVIEW; no confirmed new defects',approvalStatus='awaiting_Dan_finished_film_review',originalPicturesPreserved=True,voiceBApproved=True,fullFilmApproved=False)
(W/'execution-state.json').write_text(json.dumps(state,indent=2));print(json.dumps(counts))
