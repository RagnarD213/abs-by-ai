"""Fixed per-shot framing (no added movement). Within one roll (same setup, <60 s source gap) shots strictly alternate
W (full frame) / T (15% punch-in, anchored to the measured hair top) so no two neighbours share a scale. Across rolls,
measured head size decides: punch only when the two sides would read the same size, and never T next to T."""
import json,statistics as st
P=json.load(open('timeline.json'))['pieces'];Hd=json.load(open('heads_by_src.json'))
CW,CH=1500,844;S=1920/CW
def meas(p):
    s=[r for r in Hd.get(f"{p['source']}@{round(p['src_in'],2)}",[]) if r.get('face')]
    if not s:return None
    hf=[];tops=[];cx=[]
    for r in s:
        fh=r['chin']-r['fore'];top=r['top'] if r.get('top') is not None else r['fore']-0.45*fh
        hf.append((r['chin']-top)/1080);tops.append(top);cx.append(r['cx'])
    return dict(hf=st.median(hf),top=min(tops),cx=st.median(cx))
out=[];prev=None
for i,p in enumerate(P):
    m=meas(p) if p['source']!='C1541' else dict(hf=0.30,top=40,cx=1050)
    same_setup=prev is not None and P[i-1]['source']==p['source'] and -0.3<=p['src_in']-P[i-1]['src_out']<60
    if m and m['hf']<0.24 and not (prev and prev['level']=='T' and same_setup and prev.get('eff') and abs(m['hf']*S-prev['eff'])/prev['eff']<0.12):lvl='T'
    elif same_setup:lvl='W' if prev['level']=='T' else 'T'
    elif prev is not None and m and prev.get('eff') and prev['level']=='W' and abs(m['hf']-prev['eff'])/prev['eff']<0.12:lvl='T'
    else:lvl='W'
    if lvl=='T' and m and m['hf']>=0.40 and prev and prev.get('eff') and abs(m['hf']-prev['eff'])/prev['eff']>=0.12:lvl='W'  # never punch a close-up
    rec=dict(piece=i,beat=p['beat'],level=lvl,crop=None,head=round(m['hf'],3) if m else None,m=m)
    if lvl=='T':
        if p['source']=='C1541':rec['crop']=[375+148,0,1054,844]
        elif m:
            x0=int(min(1920-CW,max(0,m['cx']-CW/2)));y0=int(min(1080-CH,max(0,m['top']-120)))
            rec['crop']=[x0//2*2,y0//2*2,CW,CH]
        else:rec['crop']=[(1920-CW)//2,(1080-CH)//2,CW,CH]
    rec['eff']=(m['hf']*(S if lvl=='T' else 1)) if m else None
    rec['label']=f"{p['source']}-{lvl}" if same_setup or (prev and P[i-1]['source']==p['source']) else (f"H{round(rec['eff']*100)}{lvl}" if m else f"broll{i}")
    out.append(rec);prev=rec
# second pass: any visible join whose two sides read within 12% of one size gets a deeper (28%) punch on its T side
def crop_for(rec,p,sc):
    cw,ch=int(1920/sc)//2*2,int(1080/sc)//2*2;m=rec['m']
    if p['source']=='C1541':return [375+int((1350-1350/sc)/2)//2*2,0,int(1350/sc)//2*2,int(1080/sc)//2*2]
    if not m:return [(1920-cw)//2,(1080-ch)//2,cw,ch]
    x0=int(min(1920-cw,max(0,m['cx']-cw/2)));y0=int(min(1080-ch,max(0,m['top']-120)));return [x0//2*2,y0//2*2,cw,ch]
for i in range(1,len(out)):
    a,b=out[i-1],out[i]
    if not(a.get('eff') and b.get('eff')):continue
    if abs(a['eff']-b['eff'])/min(a['eff'],b['eff'])<0.12:
        t=b if b['level']=='T' else (a if a['level']=='T' else None)
        if t is None:t=b;t['level']='T'
        if t['m'] and t['m']['hf']>=0.40:continue
        t['crop']=crop_for(t,P[t['piece']],1.28);t['eff']=t['m']['hf']*1.28 if t['m'] else None;t['deep']=True
# third pass: at a join still within 12%, toggle the punch on one side if that clears BOTH of that shot's joins
def eff_of(r,lvl):
    m=r['m'];return (m['hf']*(1.28 if lvl=='T' else 1)) if m else None
def ok(i,lvl_i):
    e=eff_of(out[i],lvl_i)
    if e is None:return True
    for j in (i-1,i+1):
        if 0<=j<len(out) and out[j].get('eff'):
            if abs(e-out[j]['eff'])/min(e,out[j]['eff'])<0.12:return False
    return True
for i in range(1,len(out)):
    a,b=out[i-1],out[i]
    if not(a.get('eff') and b.get('eff')) or abs(a['eff']-b['eff'])/min(a['eff'],b['eff'])>=0.12:continue
    for k in (i,i-1):
        r=out[k];new='W' if r['level']=='T' else 'T'
        if new=='T' and r['m'] and r['m']['hf']>=0.40:continue
        if ok(k,new):
            r['level']=new;r['crop']=crop_for(r,P[k],1.28) if new=='T' else None;r['eff']=eff_of(r,new);break
# fourth pass: joins the r8 judge saw as identical on screen; explicit flips (second side, or first when second is a close-up)
FLIP={'why-drawbacks':'W','parts-chicken':'T','cucumber-english':'W','dayone':'T','chicken-why':'T'}
for k,r in enumerate(out):
    lv=FLIP.get(P[k]['beat'])
    if lv and r['level']!=lv:
        r['level']=lv;r['crop']=crop_for(r,P[k],1.28) if lv=='T' else None;r['eff']=eff_of(r,lv)
for r in out:
    r.pop('m',None);r['label']=(f"H{round(r['eff']*100)}{r['level']}" if r.get('eff') else f"broll{r['piece']}")
json.dump(out,open('framing.json','w'),indent=0)
print('deep punches',sum(1 for r in out if r.get('deep')))
same=[(i,out[i]['label']) for i in range(1,len(out)) if out[i]['label']==out[i-1]['label']]
print('T pieces',sum(r['level']=='T' for r in out),'of',len(out),'; adjacent same labels',same)
