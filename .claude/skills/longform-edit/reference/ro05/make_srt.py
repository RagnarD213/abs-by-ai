"""SRT sidecar + chapters from the words mapped onto the delivered timeline (midpoint-inside-kept-range rule)."""
import json,re
FPS=30000/1001
W=json.load(open('mapped-words.json'));TL=json.load(open('timeline.json'))
END=(TL['pieces'][-1]['out_f1']+round(4.0*FPS))/FPS
FIX=[(r'\bRugola\b','arugula'),(r'\bpeek of the guile\b','pico de gallo'),(r'\ba peek of the guile\b','a pico de gallo'),
     (r'\bHUB\b','H-E-B'),(r'\brobot dressing\b','store-bought dressing'),(r'\bhealthiest bath\b','healthiest fat'),
     (r'\btasting fact\b','tasting fat'),(r'broccoli -ing','broccolini'),(r'\b(Aves|Ads|Asbi) by AI\b','Abs by AI'),
     (r'absbyai \.com','AbsByAI.com'),(r'\bsell it\b','salad'),(r'\bpre -made\b','pre-made'),(r'hard -boiled','hard-boiled'),
     (r'six -pack','six-pack'),(r'\bOK\b','Okay'),(r'\ba garlicky\b','and garlicky'),(r' %','%'),(r'\bY \'all\b',"Y'all"),(r'\bcarot -y\b','carrot-y')]
def join(tok):
    s=''
    for t in tok:
        s+=t if (not s or t[:1] in "'.,%)-" and not t.startswith('-')) else ' '+t
    return s.replace(' -','-') if False else s
def fix(s):
    for a,b in FIX:s=re.sub(a,b,s)
    return s
PL=json.load(open('gfx-plan.json'));CARDS=[(g['a'],g['b']) for g in PL['graphics'] if g['kind']=='title']+[(TL['pieces'][-1]['out_f1']/FPS,END)]
cues=[];cur=[]
def flush():
    global cur
    if cur:cues.append([cur[0]['t0'],cur[-1]['t1'],fix(join([w['w'] for w in cur]))]);cur=[]
for i,w in enumerate(W):
    if cur:
        gap=w['t0']-cur[-1]['t1'];txt=fix(join([x['w'] for x in cur+[w]]))
        if gap>=0.45 or len(txt)>84 or w['t1']-cur[0]['t0']>5.5 or w['beat']!=cur[-1]['beat'] and gap>0.2:flush()
    cur.append(w)
    if w['w'][-1:] in '.?!' and cur and (cur[-1]['t1']-cur[0]['t0'])>1.2:flush()
flush()
def wrap(s):
    if len(s)<=45:return s
    words=s.split();best=None
    for k in range(1,len(words)):
        a,b=' '.join(words[:k]),' '.join(words[k:]);m=max(len(a),len(b))
        if best is None or m<best[0]:best=(m,a+'\n'+b)
    return best[1]
merged=[]
for c in cues:
    if merged and len(c[2].split())<=2 and c[0]-merged[-1][1]<0.35:
        t=merged[-1][2]+' '+c[2]
        if max(len(x) for x in wrap(t).split('\n'))<=46 and len(t)<=92:merged[-1]=[merged[-1][0],c[1],t];continue
    if merged and len(merged[-1][2].split())<=2 and c[0]-merged[-1][1]<0.35:
        t=merged[-1][2]+' '+c[2]
        if max(len(x) for x in wrap(t).split('\n'))<=46 and len(t)<=92:merged[-1]=[merged[-1][0],c[1],t];continue
    merged.append(list(c))
cues=merged
out=[]
for i,(a,b,t) in enumerate(cues):
    b=max(b,a+0.5)
    if i+1<len(cues):b=min(b,cues[i+1][0]-0.01)
    for ca,cb in CARDS:
        if a<cb and b>ca:
            if a<ca:b=min(b,ca-0.02)
            else:a=max(a,cb+0.02)
    out.append([a,b,t])
fix=[]
for c in out:
    if fix and fix[-1][1]-fix[-1][0]<1.0:
        p=fix[-1];t=p[2]+' '+c[2]
        if len(t)<=88 and max(len(x) for x in wrap(t).split('\n'))<=46:fix.pop();c=[p[0],c[1],t]
        else:p[1]=p[0]+1.0;c[0]=max(c[0],p[1]+0.01)
    fix.append(c)
final=[]
for a,b,t in fix:
    b=max(b,a+0.5)
    for ca,cb in CARDS:
        if a<cb and b>ca:
            if a<ca:b=ca-0.02
            else:a=cb+0.02;b=max(b,a+0.8)
    if final and final[-1][1]>a:final[-1][1]=a-0.01
    if b-a<0.35 and final:final[-1][2]+=' '+t;continue
    final.append([a,b,t])
out=[(a,b,wrap(t)) for a,b,t in final]
def ts(t):h=int(t//3600);m=int(t%3600//60);s=t%60;return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}".replace(',1000',',999')
srt=''.join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{t}\n\n" for i,(a,b,t) in enumerate(out))
open('subtitles.srt','w').write(srt)
L=[max(len(x) for x in t.split('\n')) for _,_,t in out];print(len(out),'cues, max line',max(L),'chars, 3-line cues',sum(t.count('\n')>1 for _,_,t in out))
# chapters (section openers)
P=TL['pieces'];first=lambda b:next(p['out_f0']/FPS for p in P if p['beat']==b)
CH=[('intro','Why this salad is my most important nutrition habit'),('why-open','Why I break my fast with a low-carb salad'),
    ('why-wholefoods','Why I stopped buying salad-bar salads'),('parts-veg','The 3 parts: vegetables, protein, dressing'),
    ('arugula','Building 7 salads: arugula, carrots, tomatoes'),('brocc','Broccolini, cucumber and red onion'),
    ('fresh','How to keep salads fresh for 7 days'),('dayone','Day one: finish chopping and make the dressing'),
    ('chicken-ready','Protein: rotisserie chicken and eggs'),('toppings','Toppings, toss and the first bite'),
    ('own-structure','How to make it your own'),('track-remind','Tracking the whole batch with AI'),('cta-thanks','Get your own nutrition plan')]
lines=[]
for b,name in CH:
    t=0 if b=='intro' else first(b);lines.append(f"{int(t//60)}:{int(t%60):02d} {name}")
open('chapters.txt','w').write('\n'.join(lines)+'\n');print(open('chapters.txt').read())
