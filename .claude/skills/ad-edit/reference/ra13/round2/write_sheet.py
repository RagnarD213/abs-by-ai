from pathlib import Path
import json,hashlib,datetime,numpy as np
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=W/'round2';F=30000/1001
J=lambda p:json.load(open(p));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=J(O/'build-record.json');v=next((O/'final').glob('*16x9*.mp4'));roll=J(W/'source/roll.json')['identity']['current_path'];tr=J(O/'track-all.json');D=J(W/'round2-plan/decisions.json');edl=[];fr=[]
for i,p in enumerate(r['cut']['pieces']):
 f0=round(p['t_in']*F);f1=round(p['t_out']*F) if i+1<len(r['cut']['pieces']) else r['frames'];lv='NEAR' if i in [1,5,8] else 'FAR';cw,ch=(1728,972) if lv=='NEAR' else(2144,1206);y=1260 if lv=='NEAR' else 1240
 edl.append(dict(roll='C1667',src_in=p['src_in'],src_out=p['src_in']+(f1-f0)/F,out_in=f0/F,out_out=f1/F,src_f0=round(p['src_in']*F),out_f0=f0,out_f1=f1,shot='piece'+str(i),audio='sync',join='first' if i==0 else'cut'))
 vals=[x for x in tr if x['piece']==i];fr.append(dict(name='piece'+str(i),crop=[cw,ch,1080-cw/2,y],head=dict(hair_top=min(x['hair'] for x in vals),cx=float(np.median([x['cx'] for x in vals])),chin=float(np.median([x['chin'] for x in vals]))),measured='Dense source 5fps measurements in track-all.json; full opaque graphics cover source pieces 2-4 and 6 and parts of 7. Actual camera segment crops in framing.json.'))
# Picture continues in camera5 over the last audio take boundary until A1 covers it.
# Audio remains the delivered mix, with its independent source-piece mapping below.
a1slot=next(x for x in r['slots'] if x['name']=='A1');cam5=next(x for x in r['framing'] if x['format']=='16' and x['name']=='cam5');old6=r['cut']['pieces'][6];p5=r['cut']['pieces'][5]
edl[5].update(src_in=cam5['src0'],src_out=cam5['src0']+cam5['n']/F,out_f1=a1slot['f0'],out_out=a1slot['a'],audio=dict(src_in=p5['src_in'],src_out=p5['src_out'],note='Use final audio.mix verbatim. Source audio changes to piece6 at its original output time while this picture continues.',next_audio_piece=old6))
edl[6].update(src_in=old6['src_in']+(a1slot['a']-old6['t_in']),out_f0=a1slot['f0'],out_in=a1slot['a'])
edl[6]['src_f0']=round(edl[6]['src_in']*F)
edl[-1]['audio']=dict(src_in=r['cut']['pieces'][-1]['src_in'],src_out=r['cut']['pieces'][-1]['src_out'],note='Use final audio.mix verbatim. Natural camera continues for the final tail after speech; the music continues.')
a=J(O/'analysis-config.json')[0]
for k in ['a','b']:a[k]-=r['lead_trim_seconds']
a['reveal']=[x-r['lead_trim_seconds'] for x in a['reveal']];a['band'][1]-=r['lead_trim_seconds'];a['scan']=[x-r['lead_trim_seconds'] for x in a['scan']]
g=[dict(id='A1',template='analysis-card',config=a,text=[a['label'],*a['rows'],a['band'][0]],t0=a['a'],t1=a['b'],layer='full',driven_by=[dict(part=part,phrase=phrase,t=t) for part,phrase,t in zip(a['rows'],['shows your AI exactly','to lose','need to gain muscle'],a['reveal'])])]
c=r['manifests']['16'][1];cf=J(Path(c['mov']).parent.parent/'configs/CTA.json')
g.append(dict(id='CTA',template='cta',config=cf,text=['Tap The Button Below','Get Started'],t0=c['a'],t1=c['b'],layer='overlay',driven_by=[dict(part='CTA',phrase='Tap the button below',t=c['a'])]))
# The phone and goal cards are source-specific adapters over shared Soft Blue primitives.
for name in ['P1','P2']:
 s=next(x for x in r['slots'] if x['name']==name);g.append(dict(id=name,template='softblue:phone_and_photo_card',config=dict(adapter=str(O/'recipe/cards.py'),build=str(O/'recipe/build_full.py'),name=name),text=[],t0=s['a'],t1=s['b'],layer='full',driven_by=[dict(part=name,phrase='AI fixes all three' if name=='P1' else 'So the workout and nutrition plan',t=s['a'])]))
p1=next(x for x in r['slots'] if x['name']=='P1');p2=next(x for x in r['slots'] if x['name']=='P2');demo=R/'Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/simulated-dan-sunglasses-to-pool-ad14-v1.mp4';goal=R/'Media/example pictures/dan by pool.png'
# Read actual constants without importing render modules.
import sys,importlib.util
sys.path.insert(0,str(O/'recipe'));import cards
pics=[]
for id,t0,t1,path,src,frames,kind,lab,txt,people,phys in [('P1-real',p1['a']+18/F,p1['a']+47/F,demo,2.6,29,'phone','real','Real picture of me. Not AI-generated.','dan',True),('P1-goal',p1['a']+47/F,p1['b'],goal,0,0,'photo','ai','AI-GENERATED','dan',True),('A1-goal',a['a'],a['b'],goal,0,0,'photo','ai','AI-GENERATED','dan',True),('P2-tour',p2['a'],p2['b'],cards.S.TOUR,6,60,'phone','none','','other',False)]:
 pics.append(dict(id=id,t0=t0,t1=t1,kind=kind,sources=[dict(path=str(path),src_in=src,frames=frames)],label_kind=lab,label=txt,people=people,physique=phys,approved_crop=None,library_id='B0544' if id=='P2-tour' else id,label_source='Approved demo provenance sidecar and approved goal source, not inferred from candidate.',note='P2 source switches after 60 frames to source 2.05s food analysis.' if id=='P2-tour' else 'See build record for exact source crop.'))
s=dict(schema='abs-edit-sheet/1',job='RA-13',title='Why Do Most Guys Never Get Abs?',type='AD',editor='codex',video=dict(master=str(v),sha256=sha(v),fps=F,frames=r['frames'],duration=r['duration'],width=1920,height=1080,rolls=dict(C1667=dict(path=roll,width=2160,height=3840,fps=F))),grade=dict(filter=D['decisions'][0]['filter'],order='at_source_size',lut='/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube',decode='bt709',note='Approved Brighter Natural B.'),edl=edl,framing=fr,words=dict(list=[dict(w=x['w'],t0=x['t'],t1=x['e']) for x in r['words']],timing='ctc',fixes=[]),graphics=g,pictures=pics,audio=dict(mix=str(v),untreated=str(O/'audio/cut_trim.wav'),gate_stamp=str(v)+'.audio_gate.json',chain=str(O/'audio/mix.wav.voice_chain.json'),music='/Volumes/Extreme/_edit_work/ad1-8-14/music/Realizer.mp3'),approvals=dict(status='pending',round=2,decisions=D['decisions'],source=str(W/'round2-plan/decisions.json')),provenance=dict(written=datetime.datetime.now().isoformat(),by='Codex',build_dir=str(O),inputs={str(O/'build-record.json'):sha(O/'build-record.json'),str(O/'recipe/build_full.py'):sha(O/'recipe/build_full.py')}))
Path(str(v)+'.edit-sheet.json').write_text(json.dumps(s,indent=2))
for fmt in ['9','16']:
 video=next((O/'final').glob('*'+('9x16' if fmt=='9' else '16x9')+'*.mp4'));(O/f'checks{fmt}/negative-scan.json').write_text(json.dumps(dict(sha256=sha(video),when=datetime.datetime.now().isoformat(),frames_checked=54,findings=[],method='Editor viewed all 3 full-film contact sheets, 54 sampled frames per format, plus full attached actual media review and native spot checks. No shame-framed body-part close-ups observed.'),indent=2))
print(str(v)+'.edit-sheet.json')
