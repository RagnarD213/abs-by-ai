from pathlib import Path
import json,hashlib,copy,datetime
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');B=W/'round2';F=30000/1001;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();J=lambda p:json.load(open(p))
src=next((B/'final').glob('*16x9*.mp4.edit-sheet.json'));orig=J(src);r=J(O/'build-record.json');ps=J(O/'phone-source.json');p1=next(x for x in r['slots'] if x['name']=='P1');sw=round(ps['result_at']*F)/F
for fmt,label,wh in [('9','9x16',(1080,1920)),('16','16x9',(1920,1080))]:
 s=copy.deepcopy(orig);v=next((O/'final').glob('[!._]*'+label+'*.mp4'));s['video'].update(master=str(v),sha256=sha(v),width=wh[0],height=wh[1]);s['approvals'].update(round=3,source=str(R/'Handoffs/video-editing/RA-13-round3-decisions.json'),status='pending',scope=J(O/'WORK_PACKET.json'))
 s['pictures']=[x for x in s['pictures'] if x['id'] not in ['P1-real','P1-goal']]
 for p in s['pictures']:
  if p['id']=='A1-goal':p.update(sources=[dict(path='/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg',src_in=0,frames=0)],people='other',label_source='AI source B0550 matching after picture; source hash pinned in R3 packet.')
 for id,a,b,t in [('P1-generating',p1['a'],sw,ps['loader_t0']),('P1-result',sw,p1['b'],ps['result_t0'])]:s['pictures'].append(dict(id=id,t0=a,t1=b,kind='phone',sources=[dict(path='/Volumes/Extreme/_edit_work/ra04/round5/gen_white_man_rec.mp4',src_in=t,frames=round((b-a)*F))],label_kind='ai',label='AI-GENERATED',people='other',physique=True,approved_crop=ps['loader_crop'] if id=='P1-generating' else ps['result_crop'],library_id='B0550',label_source='Both source before and result are AI images of the same white man. Authenticated real app recording.',note='Same phone shell and geometry across the internal screen cut.'))
 for g in s['graphics']:
  if g['id']=='A1':
   a=J(O/'analysis-config.json')[0];lead=r['lead_trim_seconds'];a['a']-=lead;a['b']-=lead;a['reveal']=[t-lead for t in a['reveal']];a['band'][1]-=lead;a['scan']=[t-lead for t in a['scan']];g['config']=a
  elif g['id']=='P1':g.update(template='softblue:phone',config=dict(adapter=str(O/'recipe/cards.py'),build=str(O/'recipe/build_media.py'),source=ps,label='AI-GENERATED'),text=['AI-GENERATED'])
 if fmt=='9':
  for i,fr in enumerate(s['framing']):
   use=next((x for x in r['framing'] if x['format']=='9' and next(q for q in r['slots'] if q['name']==x['name'])['piece']==i),None)
   cw,ch=(630,1120) if i in [1,5,8] else (738,1312)
   if use:fr.update(crop=[cw,ch,use['exact_landing_head_x']-cw/2,use['y']],measured='Exact source cut-frame whole-head silhouette, then shared landing.vertical_track. Native integer crop and motion stats in motion-native.json; hair checks in framing.json.',track=use['track'])
   else:fr.update(crop=[cw,ch,fr['head']['cx']-cw/2,1240],measured='Underlying source is completely covered by approved opaque insert. Delivered visible camera holds recorded in framing.json.')
 s['provenance']=dict(written=datetime.datetime.now().isoformat(),by='Codex',revision=3,build_dir=str(O),baseline_sheet=str(src),baseline_sha256=sha(src),inputs={str(p):sha(p) for p in [O/'build-record.json',O/'framing.json',O/'phone-source.json',O/'preservation.json',O/'motion-native.json']})
 Path(str(v)+'.edit-sheet.json').write_text(json.dumps(s,indent=2));print(str(v)+'.edit-sheet.json')
