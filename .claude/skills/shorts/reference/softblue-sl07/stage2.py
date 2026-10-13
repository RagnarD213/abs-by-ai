"""stage2.py X: narrow second-stage corrections on top of pickup.py fit1 (150, 255, 3600 Hz, then 82 Hz), chosen by the gate's own 10-band tone error."""
import sys, json, itertools, numpy as np
sys.path.insert(0,"/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"); import common as C
PK="/Volumes/Extreme/_edit_work/sl07/pickups"; X=sys.argv[1]
ref=np.array(json.load(open(PK+"/film_ref.json"))["bands"]); f=json.load(open(f"{PK}/fit_{X}.json")); base=f["eq"]; best=None
for g0,g1,g2,g3 in itertools.product((0,-3,-6),(0,1.5,3,4.5),(0,-1.5,-3,-4.5),(0,1.5,3)):
    af=base+f",equalizer=f=82:t=q:w=2.5:g={g0:+.1f},equalizer=f=150:t=q:w=2.4:g={g1:+.1f},equalizer=f=255:t=q:w=2.4:g={g2:+.1f},equalizer=f=3600:t=q:w=1.6:g={g3:+.1f}"
    err=C.analyse(C.pcm(f"{PK}/fit_in_{X}.wav",af=af))[0]-ref; sc=(np.abs(err).mean(),np.abs(err).max())
    if best is None or sc[0]+0.3*sc[1]<best[0][0]+0.3*best[0][1]: best=(sc,af,err,(g0,g1,g2,g3))
sc,af,err,g=best; f.update(eq=af,tone_err_mean=float(sc[0]),tone_err_max=float(sc[1]),err=[float(v) for v in err],second_stage=dict(g82=g[0],g150=g[1],g255=g[2],g3600=g[3])); json.dump(f,open(f"{PK}/fit_{X}.json","w"),indent=1)
print(X,"second stage",g,"-> tone error mean %.2f max %.2f |"%sc," ".join("%+.1f"%v for v in err))
