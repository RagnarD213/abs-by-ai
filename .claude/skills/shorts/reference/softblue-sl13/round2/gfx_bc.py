from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent));import batch as B
HF=Path(B.lib.ROOT)/'.claude/skills/_shared/hyperframes';sys.path.insert(0,str(HF));import hfbuild as H,vertical as V
W=Path(B.WORK)
def phr(s,p):
 ws=json.loads((W/'build'/s/'words.json').read_text());return ws[B.find_phrase(ws,p)]['t']
def config(id,dur,eyebrow,lines,rows=[]):
 return dict(id=id,dur=dur,drift=-3,canvas=[1080,1610],accent=[80,85,78],eyebrow=dict(x=80,y=118,px=30,s=eyebrow),line_px=62,lines=lines,rows=rows,row_px=42,row_ty=23)
def line(s,y,t=.1,px=62):return dict(x=76,y=y,s=s,at=t,px=px)
def row(s,y,t):return dict(x=80,y=y,w=920,h=100,s=s,t=max(0,t),marker='•')
for S in 'BC':
 out=W/'build'/S/'hf';out.mkdir(exist_ok=True);dur=B.timeline(S)[1];size=88
 while max(H.text_w(l,size) for l in B.P.TITLE[S][1])>952:size-=2
 if S=='C':size=min(size,68)  # fit the same two-line header geometry without logical text-box overlap
 c=dict(id='header-'+S,dur=dur+1.7,drift=-2,canvas=[1080,310],line_px=size,accent=[64,50,7],eyebrow=dict(x=88,y=44,px=34,s='FAT LOSS'),lines=[dict(x=64,y=86+96*i,s=l,at=-1) for i,l in enumerate(B.P.TITLE[S][1])])
 configs=[c]
 if S=='B':
  configs += [config('eating-window',9.0,'ILLINOIS STUDY',[line('A Smaller',220),line('Eating Window',300),line('4 Or 6 Hours A Day',610,phr(S,'4')-0.0,55)])]
  off=269.84-B.P.SEG[S][0][0]
  configs += [config('fasting-fact',6.37,'AFTER TWO MONTHS',[line('Eat Less.',210),line('Without Counting.',290),line('550 Fewer',530,phr(S,'550')-off,84),line('Calories Per Day',650,phr(S,'fewer calories')-off,54)])]
  off=291.26-B.P.SEG[S][0][0]
  configs += [config('fasting-compare',10.94,'ONE-YEAR STUDY',[line('Fasting Until Noon',210),line('425 Fewer',430,phr(S,'425')-off,78),line('Calories Per Day',535,phr(S,'fewer calories',) -off,52),line('Matched',760,phr(S,'They did just as well')-off,62),line('Counting Calories',845,phr(S,'They did just as well')-off,62)])]
  # The repeated fewer-calories phrase must be the 425 occurrence, not the earlier 550 result.
  configs[-1]['lines'][2]['at']=phr(S,'425')-off+1.40
 else:
  off=504.04-B.P.SEG[S][0][0]
  configs += [config('movement-fact',8.35,'MAYO CLINIC STUDY',[line('Same Extra Food.',210),line('10X Difference',850,phr(S,'ten times')-off,76)],
   [row('Less Than 1 lb Of Fat',470,phr(S,'less than a pound')-off),row('Over 9 lbs Of Fat',610,phr(S,'over nine pounds')-off)])]
  off=B.film2out(B.timeline(S)[0],539.57)
  configs += [config('steps-list',17.03,'PROTECT YOUR DEFICIT',[line('Keep Moving',180),line('Every Day',260),line('8–10K Steps',425,phr(S,'8–10K')-off,72)],
   [row('Walk After Dinner',585,phr(S,'Walk after dinner')-off),row('Phone Calls On Your Feet',715,phr(S,'take your phone calls')-off),row('Park At The Back',845,phr(S,'park at the back')-off),row('Use A Standing Desk',975,phr(S,'Work at a standing desk')-off)])]
 (out/'configs-r2.json').write_text(json.dumps(configs,indent=2))
 for c in configs:
  if not (out/'renders'/(c['id']+'.mov')).exists():V.build([(HF/'title-card/title-card.template.htm',c,())],out,render=True,snap=min(c['dur']-.3,max(2,c['dur']-.7)))
 B.cmd_gfx(S)
print('BC GFX COMPLETE')
