from pathlib import Path
import os,sys,json,subprocess,hashlib,shutil
import numpy as np
R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');W=Path(__file__).resolve().parents[1];P=W.parent/'round2';B=W.parent/'round3'
os.environ['GATE_GROUP']='DS-105';os.environ['PATH']=str(R/'Media/video_edit/bin')+':'+os.environ['PATH']
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
S=json.loads((W/'round-controller.json').read_text());assert S['phase']=='complete' and S['productionOwner']=='01a182b7-eccb-7c82-aa31-9c48d25c0e76'
assert not (W/'records/delivered.json').exists(),'Already delivered; do not rebuild'
def sha(p):return C.sha256(str(p))
def ff(args):subprocess.run([C.FF,'-nostdin','-v','error','-y']+list(map(str,args)),check=True)
def run(args,log):
 with (W/'evidence'/log).open('w') as f:p=subprocess.run(list(map(str,args)),stdout=f,stderr=subprocess.STDOUT)
 print(log,'exit',p.returncode,flush=True);return p.returncode
master=P/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p - aligned.mp4';small=P/'review/media/Why I Wear A Mouthpiece For SFC R2 - REVIEW 540p - aligned.mp4'
assert sha(master)=='6fcfdbe2e8b3ab0e2accb992c35b75d68f6732553b30b19c7fdc912f03d719ee'
chosen=B/'audio/B-full.wav';pick=B/'review/media/B.wav';o=json.loads((B/'records/options.json').read_text())['B'];assert sha(pick)==o['sha256']
x=C.pcm(str(chosen),ss=13.72,dur=12.08,ac=1);y=C.pcm(str(pick),ac=1);n=min(len(x),len(y));x=x[:n];y=y[:n];g=float(np.dot(x,y)/np.dot(x,x));corr=float(np.corrcoef(x,y)[0,1]);assert corr>.9999999
assert abs(20*np.log10(g)-o['comparison_gain_db'])<.001
(W/'records/selected-B-provenance.json').write_text(json.dumps(dict(approved_audition_sha256=sha(pick),full_pcm_sha256=sha(chosen),excerpt_correlation=corr,audition_constant_gain_db=float(20*np.log10(g)),treatment=o['filters'],delay_compensated_already_samples=1200,additional_processing='None; existing fullB PCM is reused, AAC encoded once.'),indent=2))
D=json.loads((W/'decisions.json').read_text());(W/'execution-state.json').write_text(json.dumps(dict(disposition='in_progress',revision=D['revisionId'],revision_application_count=1,checkpoint='muxing_selected_full_B'),indent=2))
shutil.copyfile(chosen,W/'audio/B-selected-full.wav');shutil.copyfile(B/'audio/B-chain.wav.voice_chain.json',W/'audio/B-selected-full.wav.voice_chain.json')
v=W/'review/media/Why I Wear A Mouthpiece For SFC R4 - full 1080p.mp4';s=W/'review/media/Why I Wear A Mouthpiece For SFC R4 - REVIEW 540p.mp4'
ff(['-i',master,'-i',chosen,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-map_metadata','0','-t','63.9639','-movflags','+faststart',v])
ff(['-i',small,'-i',v,'-map','0:v:0','-map','1:a:0','-c','copy','-map_metadata','0','-t','63.9639','-movflags','+faststart',s])
def packets(p,stream):
 return subprocess.check_output([C.FF,'-nostdin','-v','error','-i',str(p),'-map',stream,'-c','copy','-f','hash','-hash','sha256','pipe:1'],text=True).strip()
pic=[]
for a,b in [(master,v),(small,s)]:
 h=packets(a,'0:v:0');h2=packets(b,'0:v:0');assert h==h2;pic.append(dict(original=str(a),current=str(b),video_packet_hash=h,byte_identical=True))
assert packets(v,'0:a:0')==packets(s,'0:a:0')
raw=P/'audio/cut-raw.wav';ss,dd=C.analysis_window(str(v));C.stash_untreated(str(v),C.pcm(str(raw),ss=ss,dur=dd,ac=1),'Exact untreated same lav/cut map; selected gentleB fullPCM reused without another processing pass.')
C.carry_untreated(str(v),str(s))
run([sys.executable,R/'.claude/skills/_shared/audio/audio_gate.py',v,'--ab',W/'review/media/voice-reference-comparison.mp4'],'FULL-audio.log')
run([sys.executable,R/'.claude/skills/_shared/audio/audio_gate.py',s],'REVIEW-audio.log')
decoded=C.pcm(str(v),ac=1);base=C.pcm(str(chosen),ac=1);N=min(len(decoded),len(base));corrs=[];lags=[]
for start in range(0,N-48000+1,48000):
 a=decoded[start:start+48000];b=base[start:start+48000];corrs.append(float(np.corrcoef(a,b)[0,1]));lags.append(C.xcorr(a,b,max_ms=5)[1])
assert min(corrs)>.99 and max(map(abs,lags))<=2,(min(corrs),max(map(abs,lags)))
# Confirm cleanup delay correction does not cut the closing word. Last source word ends63.643s.
tail=[]
for start in [63.40,63.50,63.60,63.70,63.80,63.90]:
 part=decoded[int(start*48000):int(min(start+.05,63.964)*48000)];tail.append(dict(t=start,rms_db=float(20*np.log10(np.sqrt(np.mean(part**2))+1e-12))))
proof=dict(final_sha256=sha(v),small_sha256=sha(s),picture=pic,shared_audio_packet_hash=packets(v,'0:a:0'),aac_to_selectedB_min_per_second_correlation=min(corrs),max_relative_lag_samples=max(map(abs,lags)),closing_tail=tail,selectedB_provenance=str(W/'records/selected-B-provenance.json'))
(W/'evidence/preservation.json').write_text(json.dumps(proof,indent=2))
ff(['-i',v,'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',W/'evidence/FULL-exact.wav'])
jp=W/'evidence/audio-joins.json';jp.write_text(json.dumps([7.841166666666667,59.09236666666667]))
run([sys.executable,R/'.claude/skills/_shared/audio/seamscan.py',W/'evidence/FULL-exact.wav','--joins',jp,'--out',W/'evidence/FULL-seams.json'],'FULL-seams.log')
# Existing actual-picture every-frame headroom and visual findings remain applicable by exact video-packet identity.
# Fresh speech and watch evidence below bind the new delivered hash; no older report is falsely called a new run.
sys.path.insert(0,str(R/'.claude/skills/_shared/cut'));import speech
heard,where=speech.transcribe(str(v),quiet=False)
plan=json.loads((P/'evidence/finishing/FULL-plan.json').read_text());plan['evidence_contract']['video_sha256']=sha(v);plan['speech_words']=heard;plan['transcript_words']=[dict(w=x['w']) for x in heard];plan['speech_words_evidence']=dict(method='delivered_asr',video_sha256=sha(v));plan.pop('watch_log',None)
(W/'evidence/FULL-delivered-words.json').write_text(json.dumps(dict(sha256=sha(v),source=where,words=heard),indent=2))
pp=W/'evidence/FULL-plan.json';pp.write_text(json.dumps(plan,indent=2))
run([sys.executable,R/'.claude/skills/_shared/deliver/watch.py',v,'--plan',pp,'--out',W/'evidence/FULL-watch','--log',W/'evidence/FULL-watch.json','--clips'],'FULL-watch.log')
plan['watch_log']=str(W/'evidence/FULL-watch.json');pp.write_text(json.dumps(plan,indent=2))
print('CANDIDATE_READY',v,sha(v),flush=True)
