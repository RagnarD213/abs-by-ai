#!/usr/bin/env python3
"""AD. Emit exact-file evidence and run existing gates after R4 assembly."""
import sys,json,subprocess,importlib.util,os,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
spec=importlib.util.spec_from_file_location('r4',Path(__file__).with_name('r4_render.py'));B=importlib.util.module_from_spec(spec);spec.loader.exec_module(B)
R,W,O,SH,FF,FPS,N,D=B.R,B.W,B.O,B.SH,B.FF,B.FPS,B.N,B.D
sys.path[:0]=[str(SH/'cut'),str(SH/'audio')]
import speech
# Keep the build's original queue position if this worker is launched by the render chain.
if os.environ.get('RA16_BUILD_WAIT_SINCE'):
 old=B.buildcap.builds;start=float(os.environ['RA16_BUILD_WAIT_SINCE']);B.buildcap.builds=lambda table=None,me=None,since=None:old(table=table,me=me,since=start)
def save(p,x):B.write(p,x)
def call(cmd,log):
 with open(log,'w') as f:q=subprocess.run(list(map(str,cmd)),stdout=f,stderr=subprocess.STDOUT)
 return q.returncode
def image_at(path,n):
 data=subprocess.check_output([FF,'-v','error','-i',str(path),'-vf',f"select='eq(n,{n})'",'-vsync','0','-frames:v','1','-f','image2pipe','-vcodec','png','-']);import io
 return Image.open(io.BytesIO(data)).convert('RGB')
def label_tracks(aspect,folder):
 # Independent approved component pixels, never crops taken from the candidate.
 import softblue as S
 mf=json.load(open(O/folder/'manifest.json'));out=[];g0=581
 # Demo first switch occurs when round(i/101.898*110) reaches source frame108.
 switch=next(i for i in range(144) if min(110,round((i/FPS)/3.4*110))>=108)
 goal=math.ceil(3.4*FPS)
 for kind,a,b,text,xy,size in [
  ('real',0,switch,'Real picture of me. Not AI-generated.',(540,1260) if aspect=='9x16' else (960,850),19 if aspect=='9x16' else 20),
  ('ai',switch,goal,'AI-GENERATED',(540,1260) if aspect=='9x16' else (960,850),19 if aspect=='9x16' else 20),
  ('ai',goal,144,'AI-GENERATED',(540,1230) if aspect=='9x16' else (960,840),19)]:
  source=W/'round3'/f'DEMO-{aspect}-CLEAN.mp4';ref=image_at(source,(a+b-1)//2);tmp=Image.new('RGB',ref.size);box=S.disclosure(tmp,text,xy=xy,anchor='mt',size=size);rect=[int(math.floor(box[0])),int(math.floor(box[1])),int(math.ceil(box[2])),int(math.ceil(box[3]))];chip=ref.crop(rect);dest=O/'evidence'/f'label-{aspect}-{kind}-{a}.png';chip.save(dest)
  out.append(dict(kind=kind,beat=[(g0+a)/FPS,(g0+b)/FPS],image=str(dest),image_sha256=B.sha(dest),rect=rect,visibility='full',sample_times=[(g0+(a+b)//2+.25)/FPS],search_px=4,source=str(source),source_sha256=B.sha(source)))
 # Analysis-card chip is fixed below the independent goal picture. Include exact source-chip pixels.
 m=next(x for x in mf if x['id']=='G01');rect=[394,906,684,970] if aspect=='9x16' else [319,908,646,980]
 ref=image_at(m['mov'],30);dest=O/'evidence'/f'label-{aspect}-analysis.png';ref.crop(rect).save(dest)
 out.append(dict(kind='ai',beat=[757/FPS,983/FPS],image=str(dest),image_sha256=B.sha(dest),rect=rect,visibility='full',search_px=4,source=m['mov'],source_sha256=B.sha(m['mov'])))
 return out

def sheet(aspect,master):
 framing=json.load(open(O/'framing.json'));rolls={'C1668':dict(path=B.SRC,width=2160,height=3840,fps=FPS)};edl=[];fr=[]
 # Picture timeline names each opaque approved asset as an independent roll.
 scenes=[dict(x,kind='presenter') for x in framing]
 scenes += [dict(id='D01',n0=581,n1=725,kind='opaque',path=str(W/'round3'/f'DEMO-{aspect}-CLEAN.mp4')),dict(id='G01',n0=757,n1=983,kind='opaque',path=str(W/'round2'/('hf9' if aspect=='9x16' else 'hf16')/'renders/G01.mov'))]
 scenes.sort(key=lambda x:x['n0'])
 for i,s in enumerate(scenes):
  if s['kind']=='presenter':
   roll='C1668';src=s['src0'];c=s['crops'][aspect];vals=json.load(open(s['measurements']));crop=[c['cw'],c['ch'],c['cx'][0]-c['cw']/2,c['y']];head={'hair_top':s['hair_min_source_px'],'cx':float(np.median([x['cx'] for x in vals])),'chin':float(np.median([x['fore']+x['face_h'] for x in vals]))};meas='Output-grid first/last and every sixth frame; MediaPipe face, Apple Vision and MediaPipe silhouettes. '+s['measurements']
  else:
   roll=s['id'];src=0;wh=(1080,1920) if aspect=='9x16' else (1920,1080);rolls[roll]=dict(path=s['path'],width=wh[0],height=wh[1],fps=FPS);crop=[*wh,0,0];head={'hair_top':0,'cx':wh[0]/2,'chin':wh[1]};meas='No talking presenter in full-screen approved component; virtual full component bounds, not a head measurement.'
  edl.append(dict(roll=roll,src_in=src,src_out=src+(s['n1']-s['n0'])/FPS*(B.SPEED if roll=='C1668' else 1),out_in=s['n0']/FPS,out_out=s['n1']/FPS,src_f0=round(src*FPS),out_f0=s['n0'],out_f1=s['n1'],shot=s['id'],join='first' if i==0 else 'cut',audio={'src_in':s['n0']/FPS,'src_out':s['n1']/FPS,'path':str(W/'round2/audio/warm-bass-final-timing.wav')}))
  fr.append(dict(name=s['id'],crop=crop,head=head,measured=meas))
 graphics=[];folder='hf9' if aspect=='9x16' else 'hf16'
 for m in json.load(open(W/'round2'/folder/'manifest.json')):
  it=next(x for x in B.PLAN if x['id']==m['id']);cfg=json.load(open(W/'round2'/folder/'configs'/m['template']/(m['id']+'.json')))[0]
  drivers=[dict(part='in',phrase=it['start'],t=it['t0']),dict(part='out',phrase=it['end'],t=it['t1'])]
  if it['kind']=='lt':
   text=[cfg['topic']]+[x[0] for x in cfg['parts']]
   drivers += [dict(part=a[0],phrase=a[1],t=b[1]) for a,b in zip(it['parts'],cfg['parts'])]
  else:
   text=cfg['rows']+[cfg['band'][0],cfg['label']]
   drivers += [dict(part=row,phrase=phrase,t=t) for row,phrase,t in zip(cfg['rows'],it['reveal'],cfg['reveal'])]+[dict(part=cfg['band'][0],phrase=it['band'][1],t=cfg['band'][1])]
  graphics.append(dict(id=m['id'],template=m['template'],config=cfg,text=text,t0=m['a'],t1=m['b'],layer='full' if m['kind']=='opaque' else 'overlay',driven_by=drivers))
 pics=[]
 for id,a,b,kind,label in [('D01-real',581,681,'real','Real picture of me. Not AI-generated.'),('D01-ai',681,725,'ai','AI-GENERATED'),('G01',757,983,'ai','AI-GENERATED')]:
  src=(W/'round3'/f'DEMO-{aspect}-CLEAN.mp4') if id.startswith('D01') else (W/'round2'/folder/'renders/G01.mov')
  pics.append(dict(id=id,t0=a/FPS,t1=b/FPS,kind='phone' if id.startswith('D01') else 'photo',sources=[dict(path=str(src),src_in=0,frames=b-a)],label_kind=kind,label=label,label_source='Approved R3 disclosure, preserved in exact independently hashed source',people='dan',physique=True,approved_crop=None,library_id=None,note='Approved same-person simulation. R3 source component reused.'))
 sh={'schema':'abs-edit-sheet/1','job':'RA-16','title':'AI Took Job','type':'AD','editor':'codex','video':dict(master=str(master),sha256=B.sha(master),fps=FPS,frames=N,duration=D,width=1080 if aspect=='9x16' else 1920,height=1920 if aspect=='9x16' else 1080,rolls=rolls),'grade':dict(filter=B.GRADE,order='at_source_size',lut='/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube',decode='bt709',note='Approved Color B; automatic -90 rotation to native portrait before crop.'),'edl':edl,'framing':fr,'words':dict(list=B.WORDS,timing='mapped-source',fixes=[['trainer','trainer.'],['and','And'],['seconds','seconds.']]),'graphics':graphics,'pictures':pics,'audio':dict(mix=str(master),untreated=str(W/'round2/audio/retained-accelerated.wav'),gate_stamp=str(master)+'.audio_gate.json',chain=str(W/'round2/audio/warm-bass-final-timing.wav.voice_chain.json'),music=None),'approvals':dict(status='pending',round=4,decisions=[dict(id='R3 components',verdict='approved',dan=json.load(open(W/'round3/round4-plan/decisions.json'))['user_exact_words'],scope='All R3 components in both formats; complete R4 film pending Dan')],source=str(W/'round3/round4-plan/decisions.json')),'provenance':dict(written='2026-10-16',by='Codex R4 editor',build_dir=str(O),inputs={str(Path(__file__)):B.sha(__file__),str(Path(__file__).with_name('r4_render.py')):B.sha(Path(__file__).with_name('r4_render.py'))})}
 dest=Path(str(master)+'.edit-sheet.json');save(dest,sh);return dest

def main():
 B.buildcap.wait('AI Took Job AD R4 final exact-file checks')
 # A single delivered-audio ASR serves both masters only after packet equality has been verified.
 reports=[]
 for aspect,folder,wh in [('9x16','hf9',(1080,1920)),('16x9','hf16',(1920,1080))]:
  master=O/'masters'/f'AI Took Job AD R4 - {aspect}.mp4';assert master.exists();h=B.sha(master)
  au=subprocess.check_output([FF,'-v','error','-i',str(master),'-map','0:a:0','-c','copy','-f','adts','-']);assert au
  ah=__import__('hashlib').sha256(au).hexdigest()
  if reports:assert ah==reports[0]['aac_sha256']
  if not reports:
   asrwords,asr_source=speech.transcribe(str(master));save(O/'delivered-asr.json',{'words':asrwords,'source':asr_source,'video_sha256':h});save(O/'delivered-words.json',asrwords)
  else:asrwords=json.load(open(O/'delivered-words.json'))
  labs=label_tracks(aspect,folder);save(O/f'label-tracks-{aspect}.json',labs)
  mf=json.load(open(O/folder/'manifest.json'));states=json.load(open(O/f'caption-states-{aspect}.json'));segs=json.load(open(O/'picture-segments.json'))
  graphics=[dict(name=m['id'],beat=[m['a'],m['b']],mov=m['mov']) for m in mf if m['id']!='D01']
  regions=[]
  for m in mf:
   if m['kind']=='glass':
    if aspect=='9x16':rect=m['box']
    else:rect=[86,760,1828,1016]
    regions.append(dict(beat=[round(m['a']*FPS)/FPS,round(m['b']*FPS)/FPS],rect=rect))
  # The analysis card's information and disclosure are distinct obstacles. Captions remain outside both.
  if aspect=='9x16':regions += [dict(beat=[757/FPS,983/FPS],rect=[36,996,1044,1376]),dict(beat=[757/FPS,983/FPS],rect=[394,906,684,970])]
  else:regions += [dict(beat=[757/FPS,983/FPS],rect=[825,150,1828,890]),dict(beat=[757/FPS,983/FPS],rect=[319,908,646,980])]
  joins=sorted(set([s['n0']/FPS for s in segs if s['n0']]+[581/FPS,725/FPS,757/FPS,983/FPS]))
  plan=dict(target_seconds=D,target_frames=N,joins=joins,audio_joins=[p['t_in'] for p in B.CUT['pieces'][1:]],covered=[[581/FPS,725/FPS],[757/FPS,983/FPS]],punch=[[s['n0']/FPS,s['n1']/FPS,2 if s['framing']=='near' else 1] for s in segs],graphics=graphics,cards=[[581/FPS,725/FPS],[757/FPS,983/FPS]],evidence_contract=dict(version=2,video_sha256=h),caption_states=states,speech_words=asrwords,speech_words_evidence=dict(method='delivered_asr',video_sha256=h),graphic_regions=regions,talking_head_windows=[dict(name=s['id']+' '+str(s['n0']),beat=[s['n0']/FPS,s['n1']/FPS],rect=[0,0,*wh],motion='tracking' if aspect=='9x16' else 'fixed-wide') for s in segs],label_tracks=labs,ai_inserts=[dict(name='AI goal '+str(i),beat=x['beat'],chip=x['image'],pos=x['rect'][:2]) for i,x in enumerate(labs) if x['kind']=='ai'],real_photos=[dict(name='Sunglasses source photo',beat=x['beat'],chip=x['image'],pos=x['rect'][:2]) for x in labs if x['kind']=='real'],words=[dict(w=w['w'],t=w['t0'],e=w['t1']) for w in B.WORDS],transcript_words=asrwords,source_audio=str(W/'round2/audio/retained-accelerated.wav'),watch_log=str(O/'watch'/aspect/'watch_pass.json'))
  planpath=O/f'gate-plan-{aspect}.json';save(planpath,plan)
  sh=sheet(aspect,master);rcsheet=call([sys.executable,SH/'edit-sheet/validate.py',sh,'--hash'],O/'logs'/f'sheet-{aspect}.log')
  rcaudio=call([sys.executable,SH/'audio/audio_gate.py',master,'--untreated',W/'round2/audio/retained-accelerated.wav','--ab',O/'audio'/f'Audio AB {aspect}.mp4'],O/'logs'/f'audio-gate-{aspect}.log')
  rcwatch=call([sys.executable,SH/'deliver/watch.py',master,'--plan',planpath,'--out',O/'watch'/aspect,'--log',O/'watch'/aspect/'watch_pass.json'],O/'logs'/f'watch-{aspect}.log')
  rcgate=call([sys.executable,SH/'deliver/gate.py',master,'--format','ad9x16' if aspect=='9x16' else 'ad16x9','--plan',planpath],O/'logs'/f'delivery-gate-{aspect}.log')
  reports.append(dict(aspect=aspect,path=str(master),sha256=h,aac_sha256=ah,sheet_exit=rcsheet,audio_gate_exit=rcaudio,watch_scan_exit=rcwatch,delivery_gate_exit=rcgate,watch_judgment='Pending exact-candidate independent image inspection. Initial gate may fail this row.'))
  save(O/'initial-check-results.json',reports);print('INITIAL CHECKS DONE',aspect,reports[-1],flush=True)
if __name__=='__main__':main()
