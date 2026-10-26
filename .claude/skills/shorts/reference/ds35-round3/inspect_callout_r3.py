from pathlib import Path
import sys,math,json
import numpy as np
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];sys.path.insert(0,str(W/'recipe'));from render_r3 import C
out=W/'proofs/callout-v4';out.mkdir(exist_ok=True);frames=[]
for g,f in enumerate(C.reader(str(W/'proofs/craig-v4-in-audio-context.mp4'),start=44,n=201,wh=(1080,1920)),start=284):
 if g in [284,300,350,390,417,425,442,443,444,445,447,452,460,468,484]:Image.fromarray(f).save(out/f'native-{g}.png')
 im=Image.fromarray(f[92:700]).resize((540,304));cell=Image.new('RGB',(540,328),'white');cell.paste(im,(0,24));ImageDraw.Draw(cell).text((8,5),f'Frame {g} / {g*1001/30000:.3f}s',fill='black');frames.append(cell)
for k in range(math.ceil(len(frames)/30)):
 group=frames[k*30:(k+1)*30];sheet=Image.new('RGB',(2700,328*math.ceil(len(group)/5)),(220,230,240))
 for j,im in enumerate(group):sheet.paste(im,((j%5)*540,(j//5)*328))
 sheet.save(out/f'all-native-{k+1}.jpg',quality=94)
print('ALL_201_WATCHING_FRAMES_READY',flush=True)

# Native-size comparison against the unchanged independent R2 response source.
B=W.parent/'round2'
a=Image.open(out/'native-484.png').convert('RGB')
for v in ['scripted','off_the_cuff']:
 response=next(C.reader(str(B/'review/media'/f'dad-bod-r2-{v}.mp4'),start=485,n=1,wh=(1080,1920)))
 b=Image.fromarray(response);b.save(out/f'{v}-response-485.png')
 sheet=Image.new('RGB',(2160,830),'white');sheet.paste(a.crop((0,480,1080,1280)),(0,30));sheet.paste(b.crop((0,480,1080,1280)),(1080,30));d=ImageDraw.Draw(sheet);d.text((8,8),'Watching484 /16.149s, full camera width',fill='black');d.text((1088,8),v+' response485 /16.183s, distinct23% punch-in',fill='black');sheet.save(out/f'handover-pair-{v}.png')
print('BOTH_NATIVE_HANDOVER_PAIRS_READY',flush=True)
