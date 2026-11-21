#!/usr/bin/env python3
"""Isolated crop-only comparison. Never writes into an approved build directory."""
import argparse, hashlib, importlib.util, json, subprocess
from pathlib import Path
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('landing', ROOT / '.claude/skills/_shared/cut/landing.py')
landing = importlib.util.module_from_spec(spec); spec.loader.exec_module(landing)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--ffmpeg', required=True)
    ap.add_argument('--seconds', type=float, default=35)
    a = ap.parse_args()
    if a.output.resolve() == a.build.resolve() or a.build.resolve() in a.output.resolve().parents:
        raise SystemExit('Use a separate proof directory')
    a.output.mkdir(parents=True, exist_ok=True)
    source = a.build / 'base_pic.mp4'
    cap = cv2.VideoCapture(str(source)); fps = cap.get(cv2.CAP_PROP_FPS)
    count = round(a.seconds * fps); width = 608
    segments = [dict(n0=s['n0'], n1=min(s['n1'],count)) for s in json.loads((a.build/'edl_picture.json').read_text()) if s['n0'] < count]
    n = np.arange(count); heads=[]; boxes=[]
    cache = a.output/'head-measurements.json'
    if cache.exists():
        d=json.loads(cache.read_text()); heads=d['heads']; boxes=d['boxes']
    else:
        det=mp.solutions.face_detection.FaceDetection(model_selection=1,min_detection_confidence=.5)
        for i in n:
            ok, im = cap.read()
            if not ok: raise RuntimeError(f'Cannot read frame {i}')
            r=det.process(cv2.cvtColor(cv2.resize(im,(640,360)),cv2.COLOR_BGR2RGB))
            if not r.detections: raise RuntimeError(f'No head detected at frame {i}')
            b=max(r.detections,key=lambda d:d.score[0]).location_data.relative_bounding_box
            heads.append((b.xmin+b.width/2)*1920)
            boxes.append([b.xmin*1920,b.ymin*1080,b.width*1920,b.height*1080])
            if i % 300 == 0: print('Measured',i,'/',count,flush=True)
        det.close(); cache.write_text(json.dumps(dict(heads=heads,boxes=boxes)))
    cap.release(); heads=np.array(heads)
    old=json.loads((a.build/'facetrack.json').read_text())
    before=np.zeros(count)
    for s in segments:
        dst=(n>=s['n0']) & (n<s['n1']); ns=np.array(old['n']); xs=np.array(old['x'])+width/2
        src=(ns>=s['n0']) & (ns<s['n1'])
        before[dst]=np.interp(n[dst],ns[src],xs[src])
    # Preserve the shared k=3 behavior at 4fps while measuring every native frame for validation.
    sample=set(np.rint(np.arange(0,count/fps,.25)*fps).astype(int))
    sample.update(s['n0'] for s in segments); sample.update(s['n1']-1 for s in segments)
    sn=np.array(sorted(v for v in sample if v<count))
    tn,tx,info=landing.vertical_track(sn,heads[sn],segments,width,fps)
    after=np.zeros(count)
    for s in segments:
        dst=(n>=s['n0']) & (n<s['n1']); src=(tn>=s['n0']) & (tn<s['n1'])
        after[dst]=np.interp(n[dst],tn[src],tx[src])
    # Render integer source crop coordinates. Metrics describe those exact requested pixels.
    before=np.rint(before-width/2)+width/2
    after=np.rint(after-width/2)+width/2
    cuts=[s['n0'] for s in segments]
    report=dict(source=str(source),fps=fps,frames=count,seconds=count/fps,crop_width=width,
        measurement='Head detected on every native frame. Source pixels; excludes picture-cut jumps. Moving >5 source px/s.',
        before=landing.motion_stats(n,heads,before,segments,width,fps),
        after=landing.motion_stats(n,heads,after,segments,width,fps),
        landing_error_px=max(abs(heads[i]-after[i]) for i in cuts),
        face_edge_clearance_px=min(min(boxes[i][0]-(after[i]-width/2),(after[i]+width/2)-(boxes[i][0]+boxes[i][2])) for i in n),
        method=info,cut_frames=cuts)
    for label, centres in [('before',before),('after',after)]:
        path=a.output/f'{label}.mp4'
        if path.exists(): raise SystemExit(f'Refusing to overwrite {path}')
        cap=cv2.VideoCapture(str(source))
        enc=subprocess.Popen([a.ffmpeg,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','540x960','-r',str(fps),'-i','-',
            '-an','-c:v','libx264','-threads','2','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(path)],stdin=subprocess.PIPE)
        for i in n:
            ok,im=cap.read()
            if not ok: raise RuntimeError(f'Cannot render {i}')
            left=int(centres[i]-width/2)
            if not 0<=left<=1920-width: raise RuntimeError('Crop outside source bounds')
            enc.stdin.write(cv2.resize(im[:,left:left+width],(540,960)).tobytes())
        enc.stdin.close()
        if enc.wait(): raise RuntimeError('Encoder failed')
        cap.release()
        report[label]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    report_path=a.output/'measurements.json';report_path.write_text(json.dumps(report,indent=2)+'\n')
    # All cut starts and largest lean: native frames, both crops, for visual inspection.
    picks=sorted(set(cuts+[int(np.argmax(np.abs(heads-after)))]))
    sheet=Image.new('RGB',(len(picks)*300,560),'#172333');draw=ImageDraw.Draw(sheet)
    cap=cv2.VideoCapture(str(source))
    for j,i in enumerate(picks):
        cap.set(cv2.CAP_PROP_POS_FRAMES,i);ok,im=cap.read();assert ok
        for row,centres in enumerate([before,after]):
            left=int(centres[i]-width/2)
            ph=Image.fromarray(cv2.cvtColor(im[:,left:left+width],cv2.COLOR_BGR2RGB));ph.thumbnail((145,500))
            sheet.paste(ph,(j*300+row*150,45))
        draw.text((j*300+5,10),f'Frame {i}: before / after',fill='white')
    cap.release();sheet.save(a.output/'cuts-and-largest-lean.jpg')
    (a.output/'index.html').write_text('<!doctype html><html><meta charset="utf-8"><title>Vertical centering proof</title><style>body{background:#142238;color:white;font:18px system-ui;max-width:1100px;margin:30px auto}video{max-height:70vh;width:45%}img{width:100%}</style><h1>Land on Dan, then hold</h1><p>35-second isolated Ad 2 crop test at the original frame rate. Before on the left, after on the right. Muted crop-only comparison; no approved video was rebuilt.</p><video controls src="before.mp4"></video> <video controls src="after.mp4"></video><p><a href="measurements.json">Measured results</a></p><img src="cuts-and-largest-lean.jpg"></html>')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
