"""Exact candidate picture samples and independent approved-component comparisons."""
import sys,importlib.util,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sp=importlib.util.spec_from_file_location('r4',Path(__file__).with_name('r4_render.py'));B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
B.buildcap.wait('RA16 R4 native editor audit');O=B.O;Q=O/'editor-audit';Q.mkdir(exist_ok=True);C=B.HG.module('composite')
def readone(p,n,wh):return next(C.reader(str(p),start=n,n=1,wh=wh))
report=[]
for aspect,folder,wh in [('9x16','hf9',(1080,1920)),('16x9','hf16',(1920,1080))]:
 master=O/'masters'/f'AI Took Job AD R4 - {aspect}.mp4';sw,sh=(180,320) if aspect=='9x16' else (320,180)
 data=subprocess.check_output([B.FF,'-v','error','-i',str(master),'-vf',f'fps=2,scale={sw}:{sh}','-f','rawvideo','-pix_fmt','rgb24','-']);ar=np.frombuffer(data,np.uint8).reshape(-1,sh,sw,3)
 for start in range(0,len(ar),20):
  im=Image.new('RGB',(sw*5,(sh+24)*4),(12,20,30));d=ImageDraw.Draw(im)
  for i,f in enumerate(ar[start:start+20]):x=i%5*sw;y=i//5*(sh+24);im.paste(Image.fromarray(f),(x,y));d.text((x+2,y+sh+2),f'{(start+i)/2:.2f} s',fill='white')
  im.save(Q/f'{aspect}-sequence-{start//20:02}.jpg',quality=92)
 for id,frames,src in [('D01',[581,620,680,681,683,724],B.W/'round3'/f'DEMO-{aspect}-CLEAN.mp4'),('G01',[757,790,850,940,982],B.W/'round2'/folder/'renders/G01.mov')]:
  g0=581 if id=='D01' else 757;source_hash=B.sha(src)
  for g in frames:
   f=readone(master,g,wh);ref=readone(src,g-g0,wh);bottom=1376 if aspect=='9x16' else (900 if id=='G01' else 930)
   err=np.mean((f[:bottom].astype(float)-ref[:bottom])**2);psnr=99 if err==0 else 10*np.log10(255**2/err)
   canvas=Image.new('RGB',(960,880 if aspect=='9x16' else 300),(12,20,30));d=ImageDraw.Draw(canvas)
   for j,pic in enumerate([ref,f]):
    im=Image.fromarray(pic);im.thumbnail((470,840 if aspect=='9x16' else 264));canvas.paste(im,(j*480,25));d.text((j*480+4,3),('Independent approved component' if j==0 else f'Final {g/B.FPS:.3f}s f{g}'),fill='white')
   dest=Q/f'{aspect}-{id}-{g}-comparison.jpg';canvas.save(dest,quality=94)
   report.append(dict(aspect=aspect,id=id,frame=g,reference=str(src),reference_sha256=source_hash,reference_frame=g-g0,psnr_above_caption=round(float(psnr),2),proof=str(dest)))
B.write(Q/'independent-components.json',report);print('NATIVE EDITOR AUDIT MEDIA READY',flush=True)
