"""Fresh exact-file checks; reuse acoustic alignment ONLY after identical AAC packets/timing are proved."""
from pathlib import Path
import sys,json,subprocess,hashlib,copy,os,datetime
W=Path(__file__).resolve().parents[1];B=W.parent/'round2';R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');FPS=30000/1001;FF=str(R/'Media/video_edit/bin/ffmpeg');FP=str(R/'Media/video_edit/bin/ffprobe')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=1))
def vid(v):return W/'review/media'/f'dad-bod-r3-{v}.mp4'
def pcm_hash(p):
 return subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-vn','-c:a','pcm_s32le','-f','hash','-hash','sha256','-'],text=True).strip()
def packets(p):
 x=json.loads(subprocess.check_output([FP,'-v','error','-select_streams','a:0','-show_packets','-show_data_hash','sha256','-show_entries','packet=pts,dts,duration,size,data_hash','-of','json',str(p)]));return x['packets']
def prep(v):
 q=W/'qa'/v;q.mkdir(parents=True,exist_ok=True);f=vid(v);old=B/'review/media'/f'dad-bod-r2-{v}.mp4';h=sha(f);op=packets(old);np=packets(f);assert op==np,'Audio changed'
 aa=pcm_hash(old);bb=pcm_hash(f);assert aa==bb,'Decoded playback audio differs'
 evidence=dict(decoded_stereo_pcm_sha256=aa,decoded_pcm_identical=True,video_sha256=h,baseline_sha256=sha(old),aac_packet_count=len(np),identical_packet_hashes_and_timestamps=True,method='ffprobe SHA256 on every AAC packet, pts/dts/duration/size; unchanged stream copy',inherited_acoustic_alignment=str(B/'qa'/v/'plan.json'),inherited_alignment_plan_sha256=sha(B/'qa'/v/'plan.json'),note='R2 ASR/MMS literal-transcript onsets reused by proven audio identity, not represented as a fresh ASR call. Fresh shared caption pixel/sync measurement runs on actual R3.')
 write(q/'audio-packet-identity.json',evidence)
 p=json.loads((B/'qa'/v/'plan.json').read_text());p.update(scope='CONTENT SFC R3 complete film; narrowly revised picture, stream-copied selected audio',video_sha256=h,evidence_contract={'version':2,'video_sha256':h},watch_log=str(q/'watch_pass.json'),captions_ass=str(W/v/'captions.ass'),srt=str(W/v/'captions.srt'),declare={})
 p.pop('independent_review',None);p.pop('negative_events_scan',None)
 assert sha(W/v/'captions.ass')==p['caption_source']['sha256'];p['caption_source']['ass']=str(W/v/'captions.ass')
 p['speech_words_evidence'].update(video_sha256=h,provenance=evidence)
 p['joins']=sorted(set(p['joins']+[284/FPS,469/FPS]+([973/FPS,1058/FPS] if v=='scripted' else [])))
 p['graphic_regions'] += [dict(name='R3 Craig label',beat=[284/FPS,469/FPS],rect=[8,100,457,80]),dict(name='R3 Craig photo arrow',beat=[284/FPS,469/FPS],rect=[10,190,445,705])]
 prov=json.loads((W/'asset-provenance.json').read_text())
 p['independent_scenes'].append(dict(id='R3 Craig callout',beat=[284/FPS,469/FPS],reference=prov['craig']['path'],reference_sha256=prov['craig']['sha256'],expected='One larger Daniel Craig lower-left, exact The Dad Bod she likes label and arrow; cover baked repeats, clear faces; remain until source audio ends',template=str(W/'hf/configs/R3_Craig.json')))
 if v=='scripted':
  for x in p['graphics']:
   if x['name']=='G04_After':x.update(name='R3_After',mov=str(W/'hf/renders/R3_After.mov'))
  for x in p['independent_scenes']:
   if x['id']=='G04_After':x.update(id='R3_After',reference=str(W/'hf/renders/R3_After.mov'),reference_sha256=sha(W/'hf/renders/R3_After.mov'),photo_reference=prov['photo']['path'],photo_sha256=prov['photo']['sha256'])
 p['qa_transcript_separation'].update(full_speech_plan=str(q/'full-speech-plan.json'),full_speech_row_results=str(q/'full-speech-junk.json'),caption_result=str(q/'corrected-caption-sync.json'))
 write(q/'plan.json',p)
 write(q/'caption-states.json',dict(video_sha256=h,caption_source=p['caption_source'],states=p['caption_states'],provenance='Unchanged exact caption rasters; new R3 actual-pixel verification required'))
 full=copy.deepcopy(p);full['speech_words']=p['delivered_speech_words_all'];write(q/'full-speech-plan.json',full)
 probe=json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(f)]));s=next(x for x in probe['streams'] if x['codec_type']=='video');assert (s['width'],s['height'],s['r_frame_rate'],int(s['nb_frames']))==(1080,1920,'30000/1001',p['target_frames']);write(q/'probe.json',probe)
 subprocess.run([FF,'-v','error','-xerror','-i',str(f),'-f','null','-'],check=True)
 print('EXACT_R3_PLAN_DECODE_AUDIO_IDENTITY',v,len(np),flush=True)
def watch(v):
 q=W/'qa'/v;subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/watch.py'),str(vid(v)),'--plan',str(q/'plan.json'),'--out',str(q/'watch'),'--log',str(q/'watch_pass.json'),'--clips'],check=True)
def rows(v):
 q=W/'qa'/v;sys.path.insert(0,str(R/'.claude/skills'));from _shared.deliver import gate as G
 for name,plan,keys in [('full-speech-junk','full-speech-plan.json',{'junk:repeated_take','junk:dead_air'}),('corrected-caption-sync','plan.json',{'captions:sync'})]:
  _,_,rr=G.run(str(vid(v)),'short',str(q/plan),keys);rec=dict(video_sha256=sha(vid(v)),gate_version=G.GATE_VERSION,scope='Fresh exact R3 shared measurements; unchanged sound alignment inherited via every-packet identity evidence',rows=[dict(key=x.key,ok=x.ok,detail=x.detail,value=x.value) for x in rr]);write(q/(name+'.json'),rec);print(name,v,[(x.key,x.ok) for x in rr],flush=True)
def gate(v):
 q=W/'qa'/v;r=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(vid(v)),'--format','short','--plan',str(q/'plan.json'),'--json',str(q/'gate-raw.json')]);print('RAW_GATE_RETURN',v,r.returncode,flush=True)
if __name__=='__main__':
 action,v=sys.argv[1:];globals()[action](v)
