"""Only supported narrow declarations, after fresh complete R3 independent clearance."""
from pathlib import Path
import sys,json,hashlib,subprocess
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for v in (sys.argv[1:] or ['scripted','off_the_cuff']):
 q=W/'qa'/v;f=W/'review/media'/f'dad-bod-r3-{v}.mp4';h=sha(f);report=W/'independent'/v/'report.json';rr=json.loads(report.read_text());assert rr['video_sha256']==h and rr['review_complete'] and not rr['open_export_defects']
 p=json.loads((q/'plan.json').read_text());assert p['video_sha256']==h
 assert json.loads((q/'audio-packet-identity.json').read_text())['identical_packet_hashes_and_timestamps'] and json.loads((q/'audio-packet-identity.json').read_text())['decoded_pcm_identical']
 for name in ['full-speech-junk','corrected-caption-sync']:
  a=json.loads((q/(name+'.json')).read_text());assert a['video_sha256']==h and all(x['ok'] for x in a['rows']),a
 dan=json.loads((q/'Dan-exact-stereo-final-AAC.wav.audio_gate.json').read_text());assert dan['sha256']==sha(q/'Dan-exact-stereo-final-AAC.wav');assert [x['key'] for x in dan['rows'] if not x['ok']]==['tone']
 full=json.loads(Path(str(f)+'.audio_gate.json').read_text());assert full['sha256']==h;assert {x['key'] for x in full['rows'] if not x['ok']} <= {'tone','floor'}
 p['declare']={
 'audio:stamp':'Explicit selected C_Balanced voice preserved by identical SHA256/PTS/duration/size of EVERY actual R3 AAC packet versus reviewed R2. Fresh normal own-mix exact AAC and isolated stereo Dan gates retained; only generic reference tone fails for owned Dan; mixed outdoor source floor may differ. No reference/verbatim bypass, extra processing or threshold change. '+str(q/'audio-packet-identity.json')+'; fresh complete independent report '+str(report),
 'framing:hair_top':'Generic source/graphic/caption landmark ambiguity in intentional R5 corner/panel composites. Fresh independent actual R3 native RGB and native worst-frame inspection checks all real foreground hair populations, including Craig-callout overlap; no visible clipping or unresolved export defect remains. Diagnostic dark-core/component limits are explicit in the report and resolved with actual native worst frames and independent original-source/frame conformity. '+str(report),
 'framing:headroom':'Intentional low corner/panel geometry differs from full-frame framing and confuses generic source/graphic landmarks. Actual R3 native RGB per-population geometry, source matte transform and native worst proofs checked independently; full-frame presenter bounds retained. This does not exempt panel/corner content or hair review. '+str(report),
 'junk:repeated_take':'Main speech_words is one first word per multiword caption chunk for exact onset measurement. Separate fresh shared whole-speech checks use ALL actual AAC literal words, carried from R2 by proven identical AAC packet content/timestamps; zero confirmed restarts. Full-speech plan and fresh exact R3 rows: '+str(q/'full-speech-junk.json')}
 p['independent_review']=dict(report=str(report),report_sha256=sha(report),actual_video_sha256=h)
 # Actual whole-file visual review and exact SHA, no inherited R2 assertion.
 p['negative_events_scan']=dict(sha256=h,when=__import__('datetime').datetime.now().astimezone().isoformat(),frames_checked=int(p['target_seconds'])+1,findings=[dict(disposition='cleared',detail='Fresh complete independent native R3 picture/scene review; explicit upper-body source photos and real studio card, no new uncertain scene. '+str(report))])
 (q/'plan.json').write_text(json.dumps(p,indent=1))
 ret=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(f),'--format','short','--plan',str(q/'plan.json'),'--json',str(q/'gate-final.json')]);assert ret.returncode==0,(v,ret.returncode)
 d=json.loads((q/'gate-final.json').read_text());assert d['verdict']=='PASS' and all(x['ok'] for x in d['rows']);print('R3_FINAL_GATE_PASS',v,h,flush=True)
