"""RO-05 graphics + cutaway plan, every entry anchored to a spoken word on the delivered timeline."""
import json,re
FPS=30000/1001
W=json.load(open('mapped-words.json'));TL=json.load(open('timeline.json'))['pieces']
n=lambda s:re.sub(r"[^a-z0-9$']","",s.lower())
def at(beat,phrase,end=False,k=0):
    ph=[n(x) for x in phrase.split()];ws=[w for w in W if w['beat']==beat]
    hits=[i for i in range(len(ws)-len(ph)+1) if [n(ws[i+j]['w']) for j in range(len(ph))]==ph]
    if len(hits)<=k:raise SystemExit(f"anchor not found: {beat} / {phrase}")
    i=hits[k];return round(ws[i+len(ph)-1]['t1'] if end else ws[i]['t0'],3)
def piece(beat):
    p=next(p for p in TL if p['beat']==beat);return p['out_f0']/FPS,p['out_f1']/FPS
G=[];C=[]
def g(key,kind,a,b,**kw):G.append(dict(key=key,kind=kind,a=round(a,3),b=round(b,3),**kw))
def cut(key,src,ss,a,b,**kw):C.append(dict(key=key,source=src,ss=ss,a=round(a,3),b=round(b,3),**kw))
M="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/"
OFF=json.load(open('sync/offsets.json'))
def gcover(key,beat,src_a=None,src_b=None):
    p=next(p for p in TL if p['beat']==beat);a0=p['out_f0']/FPS
    sa=p['src_in'] if src_a is None else src_a;sb=p['src_in']+p['src_dur'] if src_b is None else src_b
    a=a0+(sa-p['src_in'])/p['speed'];b=a0+(sb-p['src_in'])/p['speed']
    cut(key,'GP',OFF[p['source']]['gopro_t']+sa,a,b,speed=p['speed'])
def lcut(key,beat,dur=0.5):
    # L-cut: hold the previous shot's picture over the first `dur` s of this shot (covers an operator whip/look-away)
    i=next(k for k,p in enumerate(TL) if p['beat']==beat);p,q=TL[i],TL[i-1];a=p['out_f0']/FPS
    FRM0=json.load(open('framing.json'))
    cut(key,q['source'],q['src_in']+q['src_dur'],a,a+dur,crop=FRM0[i-1]['crop'])
def phone(key,beat):
    p=next(p for p in TL if p['beat']==beat);a=p['out_f0']/FPS
    cut(key,'PHONE',p['src_in']+1.6,a+1.6,a+6.6)   # only while the phone blocks the camera
# ---------------- 1 INTRO
g('topic','solid',at('intro','Today')-0.1,at('intro','habit.',True)+0.3,text='How I Make My Daily Salad')
cut('b-veg-topdown','C1545',10.2,at('intro','only')-0.3,at('intro','dollars.',True)+0.35)
cut('b-hero-fork','C1550',111.0,at('intro-benefits','leaner.')-0.2,at('intro-benefits','muscle',True)+0.4)
# ---------------- 2 WHY
cut('b-lowcarb-toss','C1548',91.0,at('why-fast','like')-0.1,at('why-fast','example,',True)+0.9)
g('k-lowcarb','keypoint',at('why-fast','However,'),at('why-fast','health.',True)+0.4,text='Break Your Fast With A LOW-CARB Meal')
a=at('why-drawbacks','number')
g('l-salad-bar','left-list',a-0.3,min(at('why-drawbacks','cheaper.',True)+0.4,piece('why-drawbacks')[1]-0.1),text='Why I Stopped Buying Salad-Bar Salads',
  items=['A 20-minute round trip','Skipped on weekends','About $20 vs. $4 at home'],
  reveals=[at('why-drawbacks','drive'),at('why-drawbacks','weekends'),at('why-drawbacks','$20')])
# ---------------- 3 PARTS
a,b=piece('parts-veg');g('t-parts','title',a,a+2.6,text=['WHAT GOES IN','MY DAILY SALAD'])
g('n-veg','number',at('parts-veg','raw'),at('parts-veg','salad.',True,1)+0.8 if False else at('parts-veg','raw')+4.6,num='01',text='Raw vegetables: the base')
cut('b-groceries-veg','C1533',14.2,at('parts-veg','This','',0) if False else at('parts-veg','base')-0.7,at('parts-veg','base')+2.7)
g('n-protein','number',at('parts-protein','is')-0.3,at('parts-protein','fast.',True)+0.3,num='02',text='Protein for breaking your fast')
cut('b-eggs-lineup','C1533',1.0,at('parts-eggs','and')-0.1 if False else piece('parts-eggs')[0]+1.4,piece('parts-eggs')[0]+3.8)
g('n-dressing','number',piece('parts-oliveoil')[0]+0.2,piece('parts-oliveoil')[0]+4.8,num='03',text='The dressing: olive oil')
cut('b-bottles','C1533',31.8,piece('parts-oliveoil')[0],piece('parts-oliveoil')[0]+5.0)
g('k-oliveoil','keypoint',piece('parts-oliveoil')[0]+5.2,at('parts-taste','dressing.',True)+0.3,text='Skip Store Dressing. Use OLIVE OIL')
# ---------------- 4 BUILD
a,b=piece('arugula');g('t-build','title',a,a+2.5,text=['HOW I PREP','7 SALADS AT ONCE'])
ING=[('arugula','arugula.','01','Arugula','5 cal per salad'),('carrots','carrots.','02','Shredded carrots','17 cal per salad'),
     ('tomatoes','tomatoes.','03','Grape tomatoes','8 cal per salad'),('brocc','Broccolini.','04','Broccolini','37 cal per salad'),
     ('cucumber','cucumber.','05','English cucumber',None),('onion','onion.','06','Red onion','9 cal per salad')]
for beat,word,num,name,sub in ING:
    t=at(beat,word) if beat!='arugula' else at('arugula-base','arugula.')
    if beat=='cucumber':t+=2.1
    g('i-'+name.split()[-1].lower(),'ingredient',t,t+5.5,num=num,text=name,sub=(sub+' · app estimate') if sub else None)
for beat,f in [('arugula-tl',3),('carrots-tl',3),('tomatoes-tl',4),('cuke-peel-tl',5)]:
    a,b=piece(beat);g('s-'+beat,'speed',a,b,factor=f)
for beat,f in [('cuke-seven~tl',3),('onion-skin~tl',3)]:
    a,b=piece(beat);g('s-'+beat,'speed',a,b,factor=f)
g('k-chop-late','keypoint',at('tomatoes','key')-0.7,at('tomatoes','key')+3.0,text='Chop As LATE As Possible',pos='top')
gcover('gp-brocc','brocc',None,next(p for p in TL if p['beat']=='brocc')['src_in']+1.2)
gcover('gp-carrots','carrots-vitamins',19.0,None)
gcover('gp-cuke','cuke-count',74.8,76.0)
gcover('gp-onion','onion',96.56,99.9)
# ---------------- 5 FRESH
a,b=piece('fresh');g('t-fresh','title',a,a+2.6,text=['HOW TO KEEP SALADS','FRESH FOR 7 DAYS'])
g('l-oxo','lower',at('fresh-oxo','OXO.')-0.2,at('fresh-oxo','it.',True)+0.3,text='Glass containers with clamp lids (OXO) · about $20 each',pos='top')
a,b=piece('boxup~tl');g('s-boxup','speed',a,b,factor=6)
g('k-fresh','keypoint',at('boxup-minimal','minimum'),at('boxup-minimal','containers.',True)+0.4,text='Minimal Chopping + SEALED GLASS = A Week Of Fresh Salads',pos='top')
# ---------------- 6 DAY ONE
a,b=piece('dayone');g('t-dayone','title',at('dayone','let\'s'),at('dayone','let\'s')+2.5,text=['DAY ONE:','FINISH AND DRESS IT'])
for beat,f in [('finish-chop-tl',4),('finish-onion-tl',3)]:
    a,b=piece(beat);g('s-'+beat,'speed',a,b,factor=f)
g('k-dress-first','keypoint',at('dress-why','important'),at('dress-why','it.',True,0)+0.4,text='Dress And Toss BEFORE The Protein Goes In',pos='top')
g('i-pepper','ingredient',at('dress-pepper','black'),at('dress-pepper','black')+4.0,num='07',text='Black pepper',sub=None)
g('i-garlic','ingredient',at('dress-garlic','Garlic'),at('dress-garlic','Garlic')+5.5,num='08',text='Garlic powder: about a tablespoon',sub=None)
g('i-adobo','ingredient',at('dress-adobo','adobo.'),at('dress-adobo','adobo.')+5.5,num='09',text='Adobo: a few sprinkles',sub='3 cal per salad · app estimate')
g('i-oil','ingredient',at('dress-pour','one'),at('dress-pour','one')+6.5,num='10',text='Olive oil: 2 tablespoons',sub='252 cal per salad · app estimate')
gcover('gp-pour','dress-pour',next(p for p in TL if p['beat']=='dress-pour')['src_in'],next(p for p in TL if p['beat']=='dress-pour')['src_in']+4.6)
g('k-measure','keypoint',piece('dress-pour')[0]+0.2,piece('dress-pour')[0]+4.4,text='MEASURE Your Oil: 120 Cal Per Tbsp',pos='top')
gcover('gp-vinegar','dress-vinegar',40.4,None)
g('i-vinegar','ingredient',[c for c in C if c['key']=='gp-vinegar'][0]['a']+0.2,[c for c in C if c['key']=='gp-vinegar'][0]['b']-0.1,num='11',text='White wine vinegar: about 2 tbsp',sub='0 cal')
# ---------------- 7 PROTEIN + TOPPINGS
cut('b-chicken-bag','C1548',116.7,piece('chicken-ready')[0],piece('chicken-ready')[0]+5.8)
g('i-chicken','ingredient',at('chicken-ready','protein.'),piece('chicken-ready')[0]+5.6,num='12',text='Rotisserie chicken',sub='173 cal · 22 g protein per salad · app estimate')
a,b=piece('chicken-dice~tl');g('s-chicken','speed',a,b,factor=2)
cut('b-eggs-pack','C1549',194.0,piece('eggs-why')[1]-2.6,piece('eggs-why')[1]+0.45)
g('i-eggs','ingredient',at('eggs-why','individually'),at('eggs-why','individually')+5.5,num='13',text='Hard-boiled eggs (2)',sub='162 cal · 13 g protein per salad · app estimate')
a,b=piece('eggs-chop~tl');g('s-eggs','speed',a,b,factor=3)
g('i-olives','ingredient',at('toppings-olives','olives,'),at('toppings-olives','olives,')+5.0,num='14',text='Green olives',sub='11 cal per salad · app estimate')
g('i-pico','ingredient',at('pico','peek'),at('pico','peek')+5.5,num='15',text='Pico de gallo',sub='6 cal per salad · app estimate')
cut('b-bite-bowl','C1551',0.1,piece('bite')[0]+(4.6-1.56),piece('bite')[1])
g('t-total','title',at('finished','about')-0.1,at('finished','about')+2.9,text=['ABOUT 700 CALORIES','PER SALAD'])
# ---------------- 8 MAKE IT YOUR OWN
a,b=piece('own-structure');g('t-own','title',a,a+2.4,text=['MAKE THE SALAD','YOUR OWN'])
g('k-structure','keypoint',at('own-structure','What'),at('own-structure','structure.',True)+0.5,text='Keep The FORMULA. Swap In Foods YOU Like',pos='top')
g('n-own1','number',at('own-structure','greens,') if False else at('own-cruciferous','Then')-2.6,at('own-cruciferous','Then')-0.1,num='01',text='Any leafy greens') if False else None
g('n-own2','number',at('own-cruciferous','Then'),at('own-cruciferous','vegetable.',True,1)+0.3,num='01',text='A cruciferous vegetable',pos='top')
g('n-own3','number',at('own-protein','You'),at('own-protein','like.',True)+0.3,num='02',text='Any solid protein',pos='top')
g('n-own4','number',at('own-oil','Olive'),at('own-oil2','bottle.',True)+0.3,num='03',text='The best olive oil you can afford',pos='top')
g('n-own5','number',at('own-spices','And'),at('own-spices','it.',True)+0.3,num='04',text='Salt, pepper, then your own spices',pos='top')
# ---------------- 9 TRACK IT
a,b=piece('track-remind');g('t-track','title',a,a+2.5,text=['TRACK THE WHOLE BATCH','WITH AI'])
phone('ph-dictate','demo-dictate')
g('k-context','keypoint',at('demo-context','If'),at('demo-context','skeleton',True)+0.4,text='Tell The AI Your OIL And PROTEIN Amounts',pos='right')
g('l-720','lower',at('demo-720','So'),at('demo-720','pictures.',True)+0.4,text='App: 683 cal · Weighed by hand: about 720 cal',pos='right')
# ---------------- 10 CTA
g('l-free','solid',at('cta-site','absbyai')-0.3,at('cta-site','absbyai')+4.5,text='Free At AbsByAI.com')
g('l-sub','lower',at('cta-bye','Thank'),piece('cta-bye')[1],text='Subscribe for more',pos='bottom')
G=[x for x in G if x]
for b in ('carrots','dress-oilvin','onion-segments','own-oil','onion-tips','tomatoes'):lcut('lc-'+b,b)
# multicam join covers: where the two sides of a join read the same size, open the second shot on the synced GoPro angle
FRM=json.load(open('framing.json'))
for i in range(1,len(TL)):
    a,b=FRM[i-1],FRM[i]
    if not(a.get('eff') and b.get('eff')) or abs(a['eff']-b['eff'])/min(a['eff'],b['eff'])>=0.12:continue
    p=TL[i];o=OFF.get(p['source'],{})
    if not o.get('covered') or p['speed']!=1:continue
    gt=o['gopro_t']+p['src_in']
    if gt>2370 or (p['src_dur'])<2.0:continue          # GoPro lens covered from ~2380 s
    t0=p['out_f0']/FPS
    if any(c['a']<t0+1.6 and c['b']>t0 for c in C) or any(x['kind']=='title' and x['a']<t0+1.6 and x['b']>t0 for x in G if x):continue
    gcover(f"gpj-{p['beat']}",p['beat'],p['src_in'],p['src_in']+1.2)
def _zone(x):
    if x['kind'] in('title','left-list'):return 'full'
    if x['kind']=='speed':return 'tr'
    if x['kind']=='ingredient' or x.get('pos')=='top':return 'tl'
    return 'bottom'
G.sort(key=lambda x:x['a'])
for i,x in enumerate(G):
    for y in G[i+1:]:
        if y['a']<x['b'] and (_zone(x)==_zone(y) or 'full' in (_zone(x),_zone(y))) and x['kind']!='title':
            x['b']=round(y['a']-0.25,3)
    assert x['b']-x['a']>=1.2,(x['key'],x['a'],x['b'])
json.dump(dict(graphics=G,cutaways=C),open('gfx-plan.json','w'),indent=1)
# overlap audit: two bottom lowers / two top cards may not overlap; cutaways may not overlap titles
def zone(x):
    if x['kind'] in('title','left-list'):return x['kind']
    if x['kind']=='speed':return 'tr'
    if x['kind']=='ingredient' or x.get('pos')=='top':return 'tl'
    return 'bottom'
bad=[]
for i,x in enumerate(G):
    for y in G[i+1:]:
        if x['a']<y['b'] and y['a']<x['b'] and (zone(x)==zone(y) or 'title' in (x['kind'],y['kind'])):bad.append((x['key'],y['key']))
for c in C:
    for y in G:
        if c['a']<y['b'] and y['a']<c['b'] and y['kind'] in('title','left-list'):bad.append((c['key'],y['key']))
print(len(G),'graphics',len(C),'cutaways; overlaps:',bad)
