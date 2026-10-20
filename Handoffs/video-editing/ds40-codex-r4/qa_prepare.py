from pathlib import Path
import sys,time,json,subprocess,hashlib,shutil
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg');D=W/'review/media'
while not (W/'assembly.json').exists():time.sleep(5)
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R4 exact-file checks and review copies')
A=json.loads((W/'assembly.json').read_text());P=json.loads((W/'plan.json').read_text());master=Path(A['master']);sha=A['sha256'];N=A['frames'];FPS=A['fps'];OP=P['opening_seconds'];ba=(P['opening_frames']+686)/FPS;bb=(P['opening_frames']+686+544)/FPS
# Inventory real cached-component transitions as well as visible cuts and the covered audio edit.
A['visible_boundaries']=[588/FPS,971/FPS,1274/FPS,1818/FPS]
A['component_joins']=[{'frame':250,'kind':'caption-onset repair prefix to unchanged decoded original tail'},{'frame':538,'kind':'continuous watching key to temporal-tail key'},{'frame':P['opening_frames']+383,'kind':'prefix key to approved R3 sample, deliberate picture punch'},{'frame':P['opening_frames']+683,'kind':'approved R3 sample to three continuous native-key tail frames'}]
A['boundaries']=sorted(set(A['boundaries']+[j['frame']/FPS for j in A['component_joins']]+A['audio_joins']))
(W/'assembly.json').write_text(json.dumps(A,indent=2))
subprocess.run([F,'-y','-v','error','-i',str(master),'-vf','scale=540:960','-c:v','libx264','-preset','fast','-crf','21','-threads','2','-c:a','copy','-movflags','+faststart',str(D/'phone.mp4')],check=True)
auxcache=W/'aux-cache.json'
if auxcache.exists():
 for item in json.loads(auxcache.read_text()):
  q=Path(item['path']);assert q.exists() and hashlib.sha256(q.read_bytes()).hexdigest()==item['sha256'],'Auxiliary media changed'
else:
 # Review-only source alternative requested in the original job. Preserve the actual source performance.
 subprocess.run([F,'-y','-v','error','-ss','1461.25','-i',P['source'],'-t','74.65','-vf','scale=1080:1920:in_color_matrix=bt709:in_range=tv:out_range=tv','-af','pan=stereo|c0=c0|c1=c0','-c:v','libx264','-preset','fast','-crf','21','-threads','2','-c:a','aac','-b:a','256k','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(D/'spontaneous-source-alternative.mp4')],check=True)
 # Full selected moving hair on both fields, including the actual opening tail and all dialogue footage.
 cmd=[F,'-y','-v','error'];parts=[]
 for i,name in enumerate(['watching','watching-tail','response','ending']):
  for field in ['light','dark']:cmd+=['-threads','2','-i',str(W/f'{name}-{field}.mp4')]
  trims=['trim=end_frame=538,','trim=start_frame=2,','','']
  for j in range(2):parts.append(f'[{i*2+j}:v]{trims[i]}setpts=PTS-STARTPTS,crop=750:450:175:200[v{i}{j}]')
  parts.append(f'[v{i}0][v{i}1]hstack=inputs=2[p{i}]')
 parts.append('[p0][p1][p2][p3]concat=n=4:v=1:a=0[v]');cmd+=['-filter_complex',';'.join(parts),'-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','16','-threads','2','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(D/'hair-light-dark.mp4')]
 subprocess.run(cmd,check=True)
 subprocess.run([F,'-v','error','-y','-ss',str(OP+1413.0116-1400.2322),'-i',str(W/'mix.wav'),'-t','10.01','-c:a','pcm_s24le',str(D/'r4-voice-check.wav')],check=True)
 shutil.copy2(W.parent/'round2/voice-balanced.wav',D/'approved-r3-voice.wav')
 aux=[D/x for x in ['spontaneous-source-alternative.mp4','hair-light-dark.mp4','r4-voice-check.wav','approved-r3-voice.wav']]
 auxcache.write_text(json.dumps([{'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()} for q in aux],indent=2))
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as AC
AC.stash_untreated(str(master),AC.pcm(str(W/'mix-untreated.wav'),ss=1,dur=A['duration']-2),note='Actual same-range untreated Bill original plus measured camera left lav assembly. No processing.')
audio=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/audio_gate.py'),str(master),'--untreated',str(master)+'.audio_untreated.json','--ab',str(D/'reference-ab.mp4')],stdout=open(W/'audio-gate.log','w'),stderr=subprocess.STDOUT)
print('Audio gate exit',audio.returncode,flush=True)
sys.path.insert(0,str(R/'.claude/skills'));from _shared.cut import speech as S
ww,src=S.transcribe(str(master),'small',quiet=False);(W/'finished-asr.json').write_text(json.dumps({'words':ww,'source':src,'sha256':sha},indent=2))
# Acoustic alignment is rerun on the exact AAC-bearing candidate, not inferred from its WAV parent.
subprocess.run([sys.executable,str(W/'align.py'),str(master),str(W/'words-final-ctc.json')],check=True)
subprocess.run([sys.executable,str(W/'bounded_alignment.py'),str(master),str(W/'words-final-ctc.json'),'final-aac'],check=True)
aligned=json.loads((W/'words-final-ctc.json').read_text())['words'];caps=json.loads((W/'caption-states.json').read_text());M=json.loads((W/'graphics-manifest.json').read_text())
# Evidence rectangles use x,y,width,height. Caption sync tests chunk onsets, not word highlights.
for c in caps:
 c['name']='caption-'+str(c['id']);c['text']=c['word'];c['word']=c['text'].split()[0]
 x,y,x1,y1=c['rect'];c['rect']=[x,y,x1-x,y1-y]
regions=[]
for m in M:
 if m['id']=='G03':regions.extend([{'beat':[m['a'],m['b']],'rect':[36,240,1008,1120]},{'beat':[m['a'],m['b']],'rect':[64,140,952,84]}])
 else:
  x,y,x1,y1=m['box'];regions.append({'name':m['id'],'beat':[m['a'],m['b']],'rect':[x,y,x1-x,y1-y]})
plan={'scope':'Complete CONTENT SFC R4. Scripted take with exact specified Bill Maher sentences first. R3 key, Balanced voice and warm grade locked. No new AI imagery.','target_frames':N,'target_seconds':N/FPS,'evidence_contract':{'version':2,'video_sha256':sha},'joins':A['visible_boundaries'],'audio_joins':A['audio_joins'],'covered':[[0,OP],[ba,bb]],'punch':[[0,OP,'WATCH'],[OP,(P['opening_frames']+383)/FPS,'NEAR'],[(P['opening_frames']+383)/FPS,ba,'TIGHT'],[ba,bb,'BMI'],[bb,N/FPS,'NEAR']],'punch_covered':[True,False,False,True,False],'graphics':[{'name':m['id'],'beat':[m['a'],m['b']],'mov':m['mov']} for m in M],'ai_inserts':[],'real_photos':[],'cards':[],'words':json.loads((W/'words-before-alignment.json').read_text())['words'],'transcript_words':ww,'speech_words':aligned,'speech_words_evidence':{'method':'delivered_asr','video_sha256':sha,'description':'Fresh Whisper transcript retained separately; wav2vec2 CTC acoustic alignment rerun on this exact candidate AAC audio using the independently verified complete spoken text.','transcript':str(W/'finished-asr.json'),'alignment':str(W/'words-final-ctc.json')},'caption_states':caps,'graphic_regions':regions,'talking_head_windows':[{'beat':[0,OP],'rect':[0,930,1080,990],'motion':'fixed-wide'},{'beat':[OP,ba],'rect':[0,0,1080,1920],'motion':'tracking'},{'beat':[bb,N/FPS],'rect':[0,0,1080,1920],'motion':'tracking'}],'srt':str(D/'bill-maher-fat-90-year-old-r4.srt'),'source_audio':str(W/'mix-untreated.wav'),'watch_log':str(W/'watch/watch_pass.json'),'junk_report':str(W/'prerender-junk.json'),'declare':{}}
(W/'delivery-plan.json').write_text(json.dumps(plan,indent=2))
watchplan=dict(plan,joins=A['boundaries']);(W/'watch-plan.json').write_text(json.dumps(watchplan,indent=2))
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),str(master),'--plan',str(W/'watch-plan.json'),'--out',str(W/'watch'),'--log',str(W/'watch/watch_pass.json'),'--clips'],stdout=open(W/'watch.log','w'),stderr=subprocess.STDOUT,check=True)
print('Native watch evidence ready',flush=True)
result=type('PendingFinalGate',(),{'returncode':None})()
print('Exact-file evidence ready; final delivery gate follows the independent watch judgment.',flush=True)
identity={}
for name,path in [('master',master),('phone',D/'phone.mp4')]:
 raw=subprocess.check_output([F,'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-']);identity[name]=hashlib.sha256(raw).hexdigest()
assert len(set(identity.values()))==1
(W/'audio-copy-identity.json').write_text(json.dumps(identity,indent=2));(W/'qa-preparation-complete.json').write_text(json.dumps({'master_sha256':sha,'audio_gate_exit':audio.returncode,'initial_gate_exit':result.returncode,'independent_review':'pending'},indent=2))
print('QA EVIDENCE PREPARED. Independent review still pending.',flush=True)
