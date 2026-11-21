"""plan.json for _shared/deliver/gate.py --format longform, built from the same files the render used."""
import json,sys,os
FPS=30000/1001
TL=json.load(open('timeline.json'));P=TL['pieces'];FR=json.load(open('framing.json'));PL=json.load(open('gfx-plan.json'))
final=sys.argv[1];total=(P[-1]['out_f1']+round(4.0*FPS))/FPS
covers=[[c['a'],c['b']] for c in PL['cutaways']]+[[g['a'],g['b']] for g in PL['graphics'] if g['kind']=='title']+[[P[-1]['out_f1']/FPS,total]]
inside=lambda a,b:any(x-0.02<=a and b<=y+0.02 for x,y in covers)
punch=[];pc=[]
for p,f in zip(P,FR):
    a,b=p['out_f0']/FPS,p['out_f1']/FPS;punch.append([round(a,3),round(b,3),f['label']]);pc.append(inside(a,b))
import hashlib
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<23),b''):h.update(b)
    return h.hexdigest()
plan=dict(target_seconds=round(total,3),target_frames=P[-1]['out_f1']+round(4.0*FPS),ai_inserts=[],real_photos=[],
  joins=[round(p['out_f0']/FPS,3) for p in P[1:]],
  covered=[[round(a,3),round(b,3)] for a,b in covers],
  punch=punch,punch_covered=pc,
  graphics=[dict(name=g['key'],beat=[g['a'],g['b']]) for g in PL['graphics'] if g['kind']!='title'],
  cards=[[g['a'],g['b']] for g in PL['graphics'] if g['kind']=='title']+[[round(P[-1]['out_f1']/FPS,3),round(total,3)]],
  words=[dict(w=w['w'],t=round(w['t0'],3),e=round(w['t1'],3)) for w in json.load(open('mapped-words.json'))],
  srt=os.path.abspath(sys.argv[2]),
  source_audio=os.path.abspath('audio/voice_raw.wav'),
  banned_source="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/screen_capture_TAKE2.MP4",
  banned_times=[12.0,18.0,288.0],
  source_picture=os.path.abspath('PICTURE_NOGFX.mp4'),
  watch_log=os.path.abspath('logs/watch_pass.json'))
if os.path.exists('audio/final.whisper.json'):
    r=json.load(open('audio/final.whisper.json'));plan['transcript_words']=[dict(w=w['word'].strip()) for s in r['segments'] for w in s.get('words',[])]
if os.path.exists('review/negative_events.json'):
    ne=json.load(open('review/negative_events.json'))
    if ne.get('sha256')==sha(final):plan['negative_events_scan']=ne
json.dump(plan,open('plan.json','w'),indent=0);print('plan.json',len(plan['joins']),'joins',len(plan['graphics']),'graphics',len(plan['cards']),'cards')
