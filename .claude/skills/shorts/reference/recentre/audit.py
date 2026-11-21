"""Final per-shot and per-short framing verdict, anchored on the torso block."""
import cv2, numpy as np, json, glob, sys, os
SP="/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/39032698-3f11-4a8d-9382-8b0b6599b994/scratchpad"
sys.path.insert(0,SP); from anchor import anchors
ZOOM = {'v3': {'A-p0-s00','D-p0-s00','G-p0-s00','H-p0-s00','I-p0-s00','K-p0-s00','L-p0-s00'}}
def geom(build, shot):
    """(half-width as a frame fraction, source-fraction -> delivered-px scale).
    zoom shots take a 496x880 window from the top instead of the full-height 608."""
    w = 496 if shot in ZOOM.get(build, ()) else 608
    return (w/1920.0)/2, 1920*(1080.0/w)

SLUG={'v2':{'A':('short2','sean-ray-vision-board'),'B':('short1','sugar-free-gum-trick'),
            'D':('short5','ask-ai-to-interview-you'),'E':('short3','supplements-3-percent'),
            'G':('short6','hire-a-maid-not-a-trainer'),'I':('short4','macro-tracking-obsolete'),
            'J':('short7','chicken-soup-trick')},
      'v3':{'A':('short1','no-abs-until-you-see-abs'),'B':('short6','vacuum-exercises'),
            'C':('short11','bubble-gut-vacuums'),'D':('short3','liquid-calories-milk'),
            'E':('short2','whey-protein-insulin'),'F':('short5','jelly-bean-vs-soda'),
            'G':('short7','fast-until-2pm'),'H':('short9','break-fast-low-carb'),
            'I':('short8','weigh-yourself-every-day'),'K':('short10','eight-hours-is-not-sleep'),
            'L':('short4','train-abs-every-day')},
      'v6':{'M':('short1','gained-muscle-in-quarantine'),'N':('short3','look-at-the-sky-deadlift'),
            'O':('short4','towel-row-karate-chop'),'P':('short2','knee-yourself-in-the-face'),
            'R':('short5','you-always-have-three-minutes')}}

def run(build):
    meta=json.load(open(f"{SP}/fr/{build}.json")); shots={}
    for sh in meta['shots']:
        A=[]
        for f in sorted(glob.glob(f"{SP}/mk/{build}/{sh['shot']}/*.mask.png")):
            m=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
            if m is None: continue
            a=anchors(m>127)
            if a: A.append(a)
        # a shot where the presenter is absent from most frames is stock footage, not him
        if len(A) < 0.6*max(1,sh['n']): continue
        T=np.array([a['torso'] for a in A])
        L=np.array([a['l'] for a in A]); R=np.array([a['r'] for a in A])
        HALF, SCALE = geom(build, sh['shot'])
        x_old=sh['x']; x_new=float(np.clip(np.median(T),HALF,1-HALF))
        o0,o1=x_old-HALF,x_old+HALF
        clipL=np.maximum(0,o0-L); clipR=np.maximum(0,R-o1)
        marL=np.maximum(0,L-o0); marR=np.maximum(0,o1-R)
        asym=np.maximum(np.minimum(clipL,marR),np.minimum(clipR,marL))*SCALE
        shots[sh['shot']]=dict(seg=sh['seg'],dur=sh['dur'],n=len(A),
            x_old=round(x_old,4), x_new=round(x_new,4),
            off_px=round((x_old-x_new)*SCALE,1),
            asym_med=round(float(np.median(asym)),1),
            asym_p75=round(float(np.percentile(asym,75)),1))
    json.dump(shots,open(f"{SP}/fix_{build}.json","w"),indent=1)
    segs={}
    for k,v in shots.items(): segs.setdefault(v['seg'],[]).append((k,v))
    out=[]
    for seg,rs in segs.items():
        tot=sum(v['dur'] for _,v in rs)
        w=sum(v['off_px']*v['dur'] for _,v in rs)/tot
        i=int(np.argmax([abs(v['off_px']) for _,v in rs]))
        asym=sum(v['asym_med']*v['dur'] for _,v in rs)/tot
        num,slug=SLUG[build][seg]
        out.append(dict(file=f"{build}-{num}_{slug}", seg=seg, subj_s=round(tot,1),
                        off=round(w), off_max=round(rs[i][1]['off_px']), worst=rs[i][0],
                        asym=round(asym), nshots=len(rs)))
    return out

allr=[]
for b in sys.argv[1:] or ['v2','v3','v6']: allr+=run(b)
allr.sort(key=lambda r:-abs(r['off']))
print(f"{'short file':40}{'subj s':>7}{'shots':>6}{'offset':>8}{'worst':>7}  {'cut-off px':>10}  verdict")
for r in allr:
    v='RE-EDIT' if abs(r['off'])>=60 or abs(r['off_max'])>=110 else ('borderline' if abs(r['off'])>=35 else 'ok')
    print(f"{r['file']:40}{r['subj_s']:7.1f}{r['nshots']:6}{r['off']:8}{r['off_max']:7}  {r['asym']:10}  {v}")
json.dump(allr,open(f"{SP}/verdicts.json","w"),indent=1)
