import sys, json, subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'recipe'))
import frames as F
F.E.SHOOT='/Volumes/Expansion/Abs By AI Raw Footage/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose'
FPS=30000/1001
meta=[]
for t in [390,450,455,470,490,505,551,556,566,580,590,530,540]:
    sh=F.shot_at(t);src=F.E.src(sh['roll']);ts=(sh['src_f0']+round(t*FPS)-sh['out_f0'])/FPS
    if not Path(src).exists():raise FileNotFoundError(src)
    lut=F.lut(sh)
    vf=f"scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix=bt709:in_range=tv,format=gbrpf32le,lut3d=file='{lut}':interp=tetrahedral,format=rgb24"
    p=R/'source'/f'clean-{t}.png'
    if not p.exists():subprocess.run([F.FF,'-nostdin','-v','error','-ss',str(ts),'-i',src,'-frames:v','1','-vf',vf,'-y',str(p)],check=True)
    meta.append(dict(t=t,shot=sh,source=src,source_t=ts,lut=lut,vf=vf))
    print(t,sh['roll'],round(ts,3),Path(lut).name,flush=True)
(R/'sources.json').write_text(json.dumps(meta,indent=2))
(R/'decisions.json').write_text(json.dumps(dict(date='2026-10-26',verbatim="Okay my picks for the shorts: let's do A, B, C",selected=['A','B','C'],scope='Segments selected; graphics and final films pending',owner='01a17836-0018-74b3-9c6f-5c6b3c57ba02',pickup_B='Proposed line 1; not yet recorded'),indent=2))
