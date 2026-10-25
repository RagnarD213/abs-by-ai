from pathlib import Path
import sys,math,json
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W/'recipe'));from render_r3 import C
out=W/'proofs/callout-v2';out.mkdir(exist_ok=True);frames=[]
for g,f in enumerate(C.reader(str(W/'proofs/craig-v2-in-audio-context.mp4'),start=44,n=185,wh=(1080,1920)),start=284):
 if g in [284,300,390,442,443,444,445,447,452,460,468]:Image.fromarray(f).save(out/f'native-{g}.png')
 im=Image.fromarray(f[92:700]).resize((540,304));cell=Image.new('RGB',(540,328),'white');cell.paste(im,(0,24));ImageDraw.Draw(cell).text((8,5),f'Frame {g} / {g*1001/30000:.3f}s',fill='black');frames.append(cell)
for k in range(math.ceil(len(frames)/30)):
 group=frames[k*30:(k+1)*30];sheet=Image.new('RGB',(2700,328*math.ceil(len(group)/5)),(220,230,240))
 for j,im in enumerate(group):sheet.paste(im,((j%5)*540,(j//5)*328))
 sheet.save(out/f'all-native-{k+1}.jpg',quality=94)
print('ALL_185_CALLOUT_FRAMES_READY',flush=True)
