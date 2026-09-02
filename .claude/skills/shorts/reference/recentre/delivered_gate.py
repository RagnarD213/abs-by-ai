#!/usr/bin/env python3
"""Delivered-file centering gate for arbitrary 1080x1920 mp4s (built 2026-09-02 for the queue audit).
Output is a SHORTLIST: it over-fires on stock b-roll with people, graphics-in-graphic and handheld
shots. Read it with timeline.py next to strip.py contact sheets, never alone.
Work dir: $GATE_WORK (default ./gate_work).
Samples at 2 fps, Apple Vision person mask, torso-block anchor (recentre/anchor.py),
reports px off x=540 and asymmetric edge clipping. Usage: gate.py OUTJSON file1.mp4 ..."""
import glob, json, os, subprocess, sys
import numpy as np, cv2
ROOT="/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, f"{ROOT}/.claude/skills/shorts/reference/recentre")
from anchor import anchors
FF=f"{ROOT}/Media/video_edit/bin/ffmpeg"
HERE=os.path.dirname(os.path.abspath(__file__))
PM=f"{HERE}/personmask"   # swiftc -O -o personmask personmask.swift
SP=os.environ.get("GATE_WORK", os.path.join(os.getcwd(), "gate_work"))
outj=sys.argv[1]; files=sys.argv[2:]
res=json.load(open(outj)) if os.path.exists(outj) else {}
for src in files:
    key=os.path.join(os.path.basename(os.path.dirname(src)),os.path.basename(src))
    if key in res: continue
    d=f"{SP}/frames/{key.replace('/','__')}"; os.makedirs(d,exist_ok=True)
    for f in glob.glob(d+"/*"): os.remove(f)
    # skip the top 12% (title band region on band layouts is handled by treating full frame; we keep full frame)
    subprocess.run([FF,'-nostdin','-v','error','-y','-i',src,'-vf','fps=2,scale=480:-2',f'{d}/%03d.png'],check=True)
    pngs=sorted(glob.glob(f"{d}/[0-9][0-9][0-9].png"))
    r=subprocess.run([PM,d]+pngs,capture_output=True,text=True)
    per=[]
    for i,p in enumerate(pngs):
        m=cv2.imread(p.replace('.png','.mask.png'),cv2.IMREAD_GRAYSCALE)
        if m is None: continue
        mm=m>127; a=anchors(mm)
        if not a: continue
        h,w=mm.shape; k=1080/w
        colcov=mm.sum(0)/h
        per.append(dict(t=i/2.0, torso=a['torso'], off=(a['torso']*w-w/2)*k,
                        l=a['l'], r=a['r'], clipL=float(colcov[:3].max()), clipR=float(colcov[-3:].max())))
    if not per:
        res[key]=dict(n=0); json.dump(res,open(outj,'w'),indent=1); continue
    off=np.array([x['off'] for x in per])
    # per-second clustering: a "shot" ~ contiguous 3s windows; report worst 3s-window median
    win=[]; 
    for s in range(0,len(per),6):
        seg=off[s:s+6]
        if len(seg)>=3: win.append(dict(t0=s/2.0, med=float(np.median(seg))))
    worst=max(win,key=lambda x:abs(x['med'])) if win else dict(t0=0,med=float(np.median(off)))
    asym=[]
    for x in per:
        # asymmetric: subject clipped on one edge while a margin exists on the other
        cl=x['clipL']>0.15; cr=x['clipR']>0.15
        asym.append((cl and x['r']<0.90) or (cr and x['l']>0.10))
    res[key]=dict(n=len(per), median_off=float(np.median(off)), mean_abs=float(np.mean(np.abs(off))),
                  p90_abs=float(np.percentile(np.abs(off),90)), worst_window=worst,
                  asym_frac=float(np.mean(asym)), frac_over60=float(np.mean(np.abs(off)>60)),
                  frac_over110=float(np.mean(np.abs(off)>110)), per=per)
    json.dump(res,open(outj,'w'),indent=1)
    print(f"{key}: n={len(per)} med={res[key]['median_off']:+.0f} p90={res[key]['p90_abs']:.0f} worst3s={worst['med']:+.0f}@{worst['t0']}s asym={res[key]['asym_frac']:.2f} >60:{res[key]['frac_over60']:.2f}",flush=True)
