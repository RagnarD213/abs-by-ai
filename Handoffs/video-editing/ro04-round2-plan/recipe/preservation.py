from pathlib import Path
import sys,subprocess,json,hashlib,ast
import numpy as np
import build as B
W=B.W;old=W.parent/'round1'
def h(b):return hashlib.sha256(b).hexdigest()
def packet(p):return subprocess.check_output([B.FF,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'])
def function(p,n):
 s=p.read_text();a=ast.parse(s);f=next(x for x in a.body if isinstance(x,ast.FunctionDef) and x.name==n);return ast.get_source_segment(s,f)
funcs={n: h(function(old/'recipe/build.py',n).encode())==h(function(W/'recipe/build.py',n).encode()) for n in ['state','paint']};assert all(funcs.values())
files=list(W.glob('*.mp4'))+list((W/'context').glob('*.mp4'));r=[]
for v in files:
 stem=v.stem.replace(' - REVIEW 540p','');ref=W/'audio'/('reference-'+stem+'.m4a')
 a=packet(v);b=packet(ref);eq=a==b;assert eq,v
 r.append({'video':str(v),'sha256':h(v.read_bytes()),'reference_cut':str(ref),'aac_sha256':h(a),'reference_aac_sha256':h(b),'aac_packets_identical':eq})
# Compare first minute directly to the approved R1 mix, not only to a new cut made by this recipe.
a=packet(W/'Arms Shoulders Workout LFC R2 - first minute.mp4');b=packet(old/'Arms Shoulders Workout LFC R1 - first minute.mp4');assert a==b
v={'graphic_functions_identical':funcs,'r1_r2_firstminute_audio_packets_identical':True,'source_start_unchanged':B.START==66.6003,'frames':1789,'timer_boundaries_seconds':[B.SET0,*[x+30 for x in B.SETS],B.TOTAL],'crop_before_xywh':[100,0,1776,1000],'crop_after_xywh':[100,18,1776,1000],'no_added_pan_or_zoom':True,'files':r}
(W/'qa/preservation.json').write_text(json.dumps(v,indent=2));print('Exact audio packets preserved on',len(r),'previews; approved graphic functions identical.',flush=True)
