"""Write the measured per-shot crop centres into a build's crops.json.

Only talking-head shots inside the segments being re-cut are touched; every stock,
card and pip offset is left exactly as it shipped.
"""
import json, os, shutil, sys
SP="/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/39032698-3f11-4a8d-9382-8b0b6599b994/scratchpad"
ROOT="/Users/danielrose/Documents/Claude/Projects/Abs By AI/YouTube Long Form Video Content"
DIR={'v2':'six-ways-ai-abs','v3':'v3-top10-tips','v6':'v6-3min-home-workout'}

build, segs = sys.argv[1], set(sys.argv[2:])
p=os.path.join(ROOT,DIR[build],'shots','crops.json')
bak=p+'.pre-recentre'
if not os.path.exists(bak): shutil.copy2(p,bak)
cur=json.load(open(bak))                       # always start from the shipped values
fix=json.load(open(f"{SP}/fix_{build}.json"))
over=json.load(open(f"{SP}/override_{build}.json")) if os.path.exists(f"{SP}/override_{build}.json") else {}
n=0
for shot,f in fix.items():
    if f['seg'] not in segs: continue
    x = over.get(shot, f['x_new'])
    if abs(x-cur[shot])<1e-4: continue
    print(f"  {shot:12} {cur[shot]:.4f} -> {x:.4f}")
    cur[shot]=round(x,4); n+=1
for shot,x in over.items():                    # allow eye-corrected values for shots the
    if shot in cur and abs(x-cur[shot])>1e-4:  # automatic anchor gets wrong
        print(f"  {shot:12} {cur[shot]:.4f} -> {x:.4f}  (manual)")
        cur[shot]=round(x,4); n+=1
json.dump(cur,open(p,'w'),indent=1)
print(f"{build}: {n} crop offsets updated in {p}")
