"""Export exact renderer facts for the maintained gates. No pass judgments are invented here."""
from pathlib import Path
import os,sys,json,hashlib,subprocess,datetime
import numpy as np
from PIL import Image
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=W/'round2';os.chdir(O)
sys.path[:0]=[str(O/'recipe'),str(R/'.claude/skills/_shared'),str(R/'.claude/skills/_shared/hyperframes')]
import cards,softblue as B,composite as CP
FPS=30000/1001;FF=str(R/'Media/video_edit/bin/ffmpeg');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rec=json.load(open(O/'build-record.json'));slots=rec['slots'];cut=rec['cut'];a1=json.load(open(O/'analysis-config.json'))[0];a1['a']-=rec['lead_trim_seconds'];a1['b']-=rec['lead_trim_seconds'];a1['reveal']=[t-rec['lead_trim_seconds'] for t in a1['reveal']];a1['band'][1]-=rec['lead_trim_seconds'];a1['scan']=[t-rec['lead_trim_seconds'] for t in a1['scan']]
for fmt,wh in [('9',(1080,1920)),('16',(1920,1080))]:
 out=O/f'checks{fmt}';out.mkdir(exist_ok=True);(out/'labels').mkdir(exist_ok=True)
 video=O/f'final/why do most guys never get abs | codex | {"9x16" if fmt=="9" else "16x9"} | RA-13 R2.mp4'
 if not video.exists():continue
 hv=sha(video)
 cap=json.load(open(O/f'cap{fmt}/caption_states.json'))['states'];man=rec['manifests'][fmt]
 P1=next(s for s in slots if s['name']=='P1');P2=next(s for s in slots if s['name']=='P2');p1a=P1['a'];nphone=round(1.57*FPS);real0=round(.60*FPS)
 blank=Image.new('RGB',(432,920),'white');_,phone=cards.phone(0,blank,fmt,room_for_label=True);_,goal=cards.goal(1,fmt);_,tour=cards.phone(0,blank,fmt)
 def chip(text,pos,size,name):
  im=Image.new('RGBA',wh);box=B.disclosure(im,text,xy=pos,anchor='mt',size=size);box=tuple(round(v) for v in box);im=im.crop(box);path=out/'labels'/f'{name}.png';im.save(path);return dict(image=str(path),image_sha256=sha(path),rect=[box[0],box[1],box[2]-box[0],box[3]-box[1]],visibility='full')
 pos=(540,1240) if fmt=='9' else (960,815);sz=22 if fmt=='9' else 20
 real=chip('Real picture of me. Not AI-generated.',pos,sz,'P1-real');ai=chip('AI-GENERATED',(540,1240) if fmt=='9' else (960,805),sz,'P1-ai')
 # A1 reference is the independent shared render, never a crop from the candidate.
 cfg=json.load(open(O/('hf9/configs/A1.json' if fmt=='9' else 'hf16/A1/config.json'))) if False else None
 import importlib.util
 sp=importlib.util.spec_from_file_location('ac_layout',R/'.claude/skills/_shared/hyperframes/analysis-card/build.py');AC=importlib.util.module_from_spec(sp);sp.loader.exec_module(AC)
 _,_,layout=AC.layout(a1,wh,bottom=1376 if fmt=='9' else 900);box=[round(x) for x in layout['chip']]
 fr=next(CP.reader(man[0]['mov'],start=round(.8*FPS),n=1,rgba=True,wh=wh));im=Image.fromarray(fr).crop(box);path=out/'labels/A1-ai.png';im.save(path);a1label=dict(image=str(path),image_sha256=sha(path),rect=[box[0],box[1],box[2]-box[0],box[3]-box[1]],visibility='full')
 tracks=[dict(name='P1-real',kind='real',beat=[p1a+real0/FPS,p1a+nphone/FPS],**real),dict(name='P1-goal',kind='ai',beat=[p1a+nphone/FPS,P1['b']],**ai),dict(name='A1-goal',kind='ai',beat=[a1['a'],a1['b']],**a1label)]
 def rect(box):return [round(box[0]),round(box[1]),round(box[2]-box[0]),round(box[3]-box[1])]
 # Physical opaque body of the shared shell, excluding its transparent padding and soft shadow.
 body=cards.S.phone_shell();size=(550,1137) if fmt=='9' else (366,756);xy=(265,80) if fmt=='9' else (777,40)
 a=np.array(body.resize(size).getchannel('A'));ys,xs=np.where(a>200);pbox=[xy[0]+int(xs.min()),xy[1]+int(ys.min()),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)]
 size=(624,1290) if fmt=='9' else (366,756);xy=(228,72) if fmt=='9' else (777,40);a=np.array(body.resize(size).getchannel('A'));ys,xs=np.where(a>200);tbox=[xy[0]+int(xs.min()),xy[1]+int(ys.min()),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)]
 regions=[dict(name='P1-phone',beat=[p1a,p1a+nphone/FPS],rect=pbox),dict(name='P1-photo',beat=[p1a+nphone/FPS,P1['b']],rect=rect(goal['photo'])),dict(name='P2-phone',beat=[P2['a'],P2['b']],rect=tbox),dict(name='A1-card',beat=[a1['a'],a1['b']],rect=rect(layout['card'])),dict(name='A1-photo',beat=[a1['a'],a1['b']],rect=rect(layout['photo']))]
 regions += [dict(name=x['name']+'-chip',beat=x['beat'],image=x['image'],rect=x['rect']) for x in tracks]
 regions += [dict(name='CTA',beat=[man[1]['a'],man[1]['b']],rect=rect(man[1]['box']))]
 graphics=[dict(name=s['name'],beat=[s['a'],s['b']],mov=str(O/f'media/{s["name"]}-{fmt}.mp4')) for s in slots if s['name'] in ('P1','P2')]+[dict(name=m['id'],beat=[m['a'],m['b']],mov=m['mov']) for m in man]
 joins=sorted(set([s['a'] for s in slots[1:]]+[p['t_in'] for p in cut['pieces'][1:]]))
 speech_file=out/'speech.json';tx_file=out/'transcript.json'
 plan=dict(target_seconds=rec['duration'],target_frames=rec['frames'],joins=joins,audio_joins=[p['t_in'] for p in cut['pieces'][1:]],covered=[[s['a'],s['b']] for s in slots if s['piece'] is None],punch=[[s['a'],s['b'],s['level']] for s in slots],punch_covered=[s['piece'] is None for s in slots],graphics=graphics,cards=[],ai_inserts=[dict(name=x['name'],beat=x['beat']) for x in tracks if x['kind']=='ai'],real_photos=[dict(name=x['name'],beat=x['beat']) for x in tracks if x['kind']=='real'],label_tracks=tracks,srt=str(O/f'cap{fmt}/captions.srt'),evidence_contract=dict(version=2,video_sha256=hv),caption_states=cap,graphic_regions=regions,talking_head_windows=[dict(name=s['name'],beat=[s['a'],s['b']],rect=[0,0,*wh],motion='tracking' if fmt=='9' else 'fixed-wide') for s in slots if s['piece'] is not None],words=rec['words'],source_audio=str(O/'audio/cut_trim.wav'),banned_source='/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4',banned_times=[26.5,27.5,29.5,31.0],watch_log=str(out/'watch/logs/watch_pass.json'),_cards_why='All content and chips end above the actual caption ink; captions continue throughout. Regions are exported from independent shared components.',_ending_still='The final 0.6-second tail follows speech; inspect every native freeze candidate independently.')
 if speech_file.exists():plan.update(speech_words=json.load(open(speech_file))['words'],speech_words_evidence=dict(method='delivered_asr',video_sha256=hv))
 if tx_file.exists():plan['transcript_words']=[dict(w=x['w']) for x in json.load(open(tx_file))['words']]
 nr=out/'negative-scan.json'
 if nr.exists():plan['negative_events_scan']=json.load(open(nr))
 (out/'plan.json').write_text(json.dumps(plan,indent=1));print('Plan',fmt,'sha',hv[:12],'states',len(cap),'labels',len(tracks))
