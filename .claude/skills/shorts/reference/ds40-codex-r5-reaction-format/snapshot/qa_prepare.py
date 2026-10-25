from pathlib import Path
import sys,subprocess,json,hashlib,shutil
W=Path(__file__).parent;O=W.parent/'round4';R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media'
A=json.loads((W/'assembly.json').read_text()); master=A['master'];sha=A['sha256']
def aac(p):return hashlib.sha256(subprocess.check_output([F,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'])).hexdigest()
identity={'R4_AAC':aac(O/'review/media/bill-maher-fat-90-year-old-r4.mp4'),'R5_AAC':aac(master)};assert identity['R4_AAC']==identity['R5_AAC'];identity['all_AAC_bytes_identical']=True
(W/'audio-copy-identity.json').write_text(json.dumps(identity,indent=2))
subprocess.run([F,'-y','-v','error','-i',master,'-vf','scale=540:960','-c:v','libx264','-preset','fast','-crf','21','-threads','2','-c:a','copy','-movflags','+faststart',str(D/'phone.mp4')],check=True)
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as AC
AC.stash_untreated(master,AC.pcm(str(O/'mix-untreated.wav'),ss=1,dur=A['duration']-2),note='Same untreated source assembly as R4. R5 AAC has been verified byte-identical to the selected R4 mix.')
q=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/audio_gate.py'),master,'--untreated',master+'.audio_untreated.json','--ab',str(D/'reference-ab.mp4')],stdout=open(W/'audio-gate.log','w'),stderr=subprocess.STDOUT)
print('AUDIO_GATE',q.returncode,flush=True)
p=json.loads((O/'delivery-plan.json').read_text());p['scope']='CONTENT SFC R5: laptop reaction, full 16:9 panel behind foreground head/hair, revised portrait cuts and BMI detail. Existing approved Balanced voice and warm grade preserved. Current R2 house key.'
p['evidence_contract']={'version':2,'video_sha256':sha};p['joins']=A['visible_boundaries'];p['audio_joins']=A['audio_joins'];p['covered']=[[0,19.6196],[42.509133333,60.6606]];p['punch']=[[0,4.004,'small reaction'],[4.004,19.6196,'wide reaction'],[19.6196,30.2302,'close foreground response'],[30.2302,32.399033,'near'],[32.399033,38.004633,'tight'],[38.004633,42.509133,'near'],[42.509133,60.6606,'BMI'],[60.6606,64.8648,'near']];p['punch_covered']=[True,True,False,False,False,False,True,False]
M=json.loads((W/'graphics-manifest.json').read_text());p['graphics']=[{'name':m['id'],'beat':[m['a'],m['b']],'mov':m['mov']} for m in M];p['graphic_regions']=[{'name':m['id'],'beat':[m['a'],m['b']],'rect':[36,24,1008,55] if m['id']=='G05' else ([36,240,1008,1120] if m['id']=='G03' else [m['box'][0],m['box'][1],m['box'][2]-m['box'][0],m['box'][3]-m['box'][1]])} for m in M]
caps=json.loads((W/'caption-states.json').read_text())
for c in caps:
 c['name']='caption-'+str(c['id']);c['text']=c['word'];c['word']=c['text'].split()[0];x,y,x1,y1=c['rect'];c['rect']=[x,y,x1-x,y1-y]
p['caption_states']=caps;p['srt']=str(D/'bill-maher-fat-90-year-old-r5.srt');p['source_audio']=str(O/'mix-untreated.wav');p['watch_log']=str(W/'watch/watch_pass.json');p['junk_report']=str(O/'prerender-junk.json')
p['speech_words_evidence']={'method':'delivered_asr','video_sha256':sha,'description':'R4 transcript and final-AAC CTC alignment inherited only after verifying R5 elementary AAC is byte-identical. All original audio and timing preserved.','transcript':str(O/'finished-asr.json'),'alignment':str(O/'words-final-ctc.json'),'identity':str(W/'audio-copy-identity.json')}
p['talking_head_windows']=[{'beat':[0,4.004],'rect':[0,1152,432,768],'motion':'fixed-wide'},{'beat':[4.004,19.6196],'rect':[0,600,1080,1320],'motion':'fixed-wide'},{'beat':[19.6196,30.2302],'rect':[0,600,1080,1320],'motion':'fixed-tight'},{'beat':[30.2302,42.509133],'rect':[0,0,1080,1920],'motion':'fixed-wide-tight'},{'beat':[60.6606,64.8648],'rect':[0,0,1080,1920],'motion':'fixed-wide'}]
(W/'delivery-plan.json').write_text(json.dumps(p,indent=2));(W/'watch-plan.json').write_text(json.dumps(p,indent=2))
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),master,'--plan',str(W/'watch-plan.json'),'--out',str(W/'watch'),'--log',str(W/'watch/watch_pass.json'),'--clips'],stdout=open(W/'watch.log','w'),stderr=subprocess.STDOUT,check=True)
(W/'qa-prepared.json').write_text(json.dumps({'sha256':sha,'audio_gate_exit':q.returncode,'watch':'scanned; independent judgment pending'},indent=2));print('QA_PREPARED',flush=True)
