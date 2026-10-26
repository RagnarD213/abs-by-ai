"""Full final AAC coverage in three overlapping bounded listens, with actual file/hash evidence.
Role reviewer is called only by fresh independent agent. Shared batch budget includes all12 calls.
"""
from pathlib import Path
import subprocess,sys,os,json,hashlib,re,fcntl
W=Path(__file__).resolve().parents[1];O=W.parent/'round1';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');FF=str(R/'Media/video_edit/bin/ffmpeg')
sys.path.insert(0,str(W/'recipe'));from qa_full_r2 import sha
role,v=sys.argv[1:];assert role in ['editor','editor_av','reviewer'];vid=W/'review/media'/('dad-bod-r2-'+v+'.mp4');e=json.loads((W/v/'edl.json').read_text());base=W/'qa'/v/('audio-'+role);base.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
windows=[(0,22),(21,43),(42,e['total_seconds'])];rows=[]
reference=O/'options/listening-J/C_Balanced.mp3' if v=='scripted' else O/'options/listening-off-R-matched/C_Balanced.mp3'
for i,(a,b) in enumerate(windows):
 d=base/str(i+1);d.mkdir(exist_ok=True);answer=d/'answer.txt';assert not answer.exists(),'Do not repeat a completed provider call; inspect its checkpoint'
 files=[]
 for source,name in [(vid,'actual-final-AAC.wav'),(W/v/'mix-untreated.wav','untreated-same-words.wav')]:
  p=d/name;subprocess.run([FF,'-v','error','-nostdin','-y','-ss',str(a),'-i',str(source),'-t',str(b-a),'-vn','-ar','48000','-ac','2','-c:a','pcm_s16le',str(p)],check=True);files.append(p)
 lufs=[C.ebur(str(p))[0] for p in files];matched=d/'untreated-level-matched.wav';subprocess.run([FF,'-v','error','-nostdin','-y','-i',str(files[1]),'-af',f'volume={lufs[0]-lufs[1]:.6f}dB','-c:a','pcm_s16le',str(matched)],check=True)
 prompt=f'''You are a fresh dialogue mixer checking sound, completely, for the {role} quality audit. Listen to the ENTIRE actual-final-AAC.wav window ({a:.3f} to {b:.3f} seconds of a {e['total_seconds']:.3f}-second complete dedicated organic Short). The first file is actual sound decoded from the exact completed video AAC, the second is SAME original speech with constant-gain-only loudness matching. The third file is Dan's APPROVED Balanced voice audition, different passage in some windows, for the chosen natural character only. Do not replace that preference or choose a brighter preset. Judge actual audible damage, clarity, harshness, room echo, hiss, missing or doubled words/syllables, chopped endings, pumping/metallic texture and clicks. Verify the interview gives way once to Dan near film15.65–16.55 if covered here, and no source voice continues under him. Window edges can land inside an utterance; they are diagnostic extracts with 1second overlap, not final edits, so do not flag a window edge itself as a cut in the complete film. Report every internal audible fault with LOCAL window timestamp and exact words, separating uncertainty and a sound already in the untreated source. Provide literal heard transcript, actual first/last word, PASS/FAIL/UNCERTAIN for final-export sound, and whether any artifact is worse than untreated. No image or general legal assessment. Do not invent transcript words from this prompt.'''
 av=[]
 if role in ['editor_av','reviewer']:
  motion=d/'actual-picture-context-540p.mp4'
  subprocess.run([FF,'-v','error','-nostdin','-y','-ss',str(a),'-i',str(vid),'-t',str(b-a),'-an','-vf','scale=540:960','-c:v','libx264','-threads',os.environ.get('RENDERQ_CORES','2'),'-preset','fast','-crf','16','-movflags','+faststart',str(motion)],check=True);av=[str(motion)]
  prompt+=' Also review the ENTIRE corresponding actual-picture-context-540p.mp4: it is a muted picture excerpt from that same exact final candidate; actual-final-AAC.wav is its sound with the same start. Evaluate moving picture, Dan hair/face/captions/graphics, all source changes, the audible-horizontal to silent-horizontal handover, real-photo X/check, before/after/photos/labels where present, purposeful size cuts, all visible joins, no freeze/black/missing asset. Judge the full timed sequence, with exact whole-film offsets above. State per-file picture/sound/captions verdicts and actual defects only. Excerpt edges are diagnostic, not final-film cuts. This three-window pass covers the entire complete film with overlaps; do not substitute it for the separate native every-frame scan/strips. No whole-video 60second provider retry.'
 (d/'prompt.txt').write_text(prompt)
 prov=dict(role=role,version=v,video=str(vid),video_sha256=sha(vid),window=[a,b],overlap_seconds=1,actual_audio_sha256=sha(files[0]),untreated_source_sha256=sha(W/v/'mix-untreated.wav'),original_lufs=lufs,untreated_constant_gain_db=lufs[0]-lufs[1],selected_reference=str(reference),selected_reference_sha256=sha(reference));(d/'provenance.json').write_text(json.dumps(prov,indent=2))
 ret=subprocess.run([sys.executable,str(W/'recipe/quality_listen_r2.py'),str(d/'prompt.txt')]+av+[str(files[0]),str(matched),str(reference)],capture_output=True,text=True,env=dict(os.environ,GM='gemini-3.1-pro-preview'));answer.write_text(ret.stdout+ret.stderr)
 row=dict(**prov,returncode=ret.returncode,answer=str(answer),usage=ret.stdout.split('USAGE')[-1].strip() if 'USAGE' in ret.stdout else None);rows.append(row);(base/'coverage.json').write_text(json.dumps(dict(rows=rows,coverage_complete=i==2,expected_windows=windows,actual_bill='unavailable'),indent=2));print('BOUNDED_SOUND',role,v,i+1,ret.returncode,flush=True)
 # Single writer at a time for this ledger; reviewer caller must serialize with the editor stage.
 ledger=W/'quality-review-budget.json'
 with (W/'quality-review-budget.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX);rec=json.loads(ledger.read_text());rec['provider_call_count']+=1;assert rec['provider_call_count']<=rec['max_calls'];rec['provider_usage'].append(dict(scope=role+' full audio/AV '+v,window=[a,b],returncode=ret.returncode,usage=row['usage'],answer=str(answer)));ledger.write_text(json.dumps(rec,indent=2))
 if ret.returncode:raise SystemExit('Provider failed/refused; no automatic retry')
print('FULL_FINAL_AUDIO_COVERED',role,v,flush=True)
