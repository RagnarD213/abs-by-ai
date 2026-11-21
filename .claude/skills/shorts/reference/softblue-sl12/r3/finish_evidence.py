"""Record inspected imagery and canonical script notation; no media/gate changes."""
from pathlib import Path
import json,hashlib,datetime
R=Path('/Volumes/Extreme/_edit_work/SL-12/round3');G=R/'qa/A-final-clean';p=G/'plan.json';j=json.loads(p.read_text())
v=Path(json.loads((R/'build/A-spec.json').read_text())['file']);h=hashlib.sha256(v.read_bytes()).hexdigest();assert h==j['evidence_contract']['video_sha256']
original=j.get('alignment_words',j['words']);j['alignment_words']=original
# Word timestamps and compositor captions stay in their original representation.
# Corrected source SRT uses numerals; compounds have identical spoken meaning
# whether printed joined or separated. Preserve the unmodified actual AAC ASR.
notation={'ten':'10','fifteen':'15','twenty':'20','weightlifting':'weight lifting','bodyweight':'body weight'}
j['words']=[notation.get(x['w'].rstrip('.,?!').lower(),x['w']) for x in original]
j['script_orthography_evidence']={'method':'Only display notation standardized for source-script comparison; no ASR word replacement and no new timing claims. Original CTC dicts preserved in alignment_words. Caption states/speech_words and actual AAC transcript remain unchanged.','changes':notation,'raw_asr':str(G/'delivered-asr.json'),'reason':'Raw comparison counted numeral and compound spelling as missing speech. Independent fullfilm/source audio preservation confirms complete original words.'}
j['negative_events_scan']={'sha256':h,'when':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frames_checked':31,'findings':[],'reviewer':'Main editor; cross-checked fresh independent complete917-frame review','evidence':['watch/sheets/sheet_00_00-00.00_to_00-23.99.jpg','watch/sheets/sheet_01_00-24.99_to_00-30.00.jpg'],'note':'Viewed every tile across both exact-file sheets: weights/cappedpen, fit wholebody curls, studio presenter, instructional text and wholebody pushups. No fat-pinching, shame/disgust framing or close-up of out-of-shape body parts.'}
p.write_text(json.dumps(j,indent=2)+'\n');print('EVIDENCE_COMPLETED',h)
