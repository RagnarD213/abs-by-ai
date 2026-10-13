from pathlib import Path
import numpy as np,json
from scipy.ndimage import map_coordinates
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parents[1];out=W/'round1/stills'
variants={'A':('Existing Daylight','1.15',1.25,1,1,0),'B':('Brighter Natural','1.45',1.12,1.03,1,0),'C':('Brightest Natural','1.60',1.08,1.05,1,0)}
for code,(name,exp,sat,gamma,contrast,warm) in variants.items():
 lines=Path(f'/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e{exp}.cube').read_text().splitlines();n=int(next(s.split()[1] for s in lines if s.startswith('LUT_3D_SIZE')));rows=[list(map(float,s.split())) for s in lines if s and (s[0].isdigit() or s[0]=='-')];lut=np.asarray(rows).reshape(n,n,n,3)
 for tm in (256,289):
  a=np.asarray(Image.open(W/f'source/raw-{tm}.png').convert('RGB'),float)/255
  # Only the candidate crop is needed for this still comparison.
  cx=1110;cw,ch=738,1312;y=1260;a=a[y:y+ch,cx-cw//2:cx+cw//2]
  coords=np.stack([a[:,:,2],a[:,:,1],a[:,:,0]])*(n-1)
  v=np.stack([map_coordinates(lut[:,:,:,k],coords,order=1,mode='nearest') for k in range(3)],-1)
  l=v@np.array([.2126,.7152,.0722]);v=l[:,:,None]+(v-l[:,:,None])*sat
  v=np.clip((v-.5)*contrast+.5,0,1)**(1/gamma);v[:,:,0]+=warm;v[:,:,2]-=warm*.4
  im=Image.fromarray(np.uint8(np.clip(v,0,1)*255)).resize((540,960),Image.LANCZOS);im.save(out/f'{code}-{tm}.jpg',quality=94)
board=Image.new('RGB',(1620,1020),'#081323');d=ImageDraw.Draw(board)
for i,(code,v) in enumerate(variants.items()):
 board.paste(Image.open(out/f'{code}-256.jpg'),(540*i,60));d.text((540*i+20,20),f'{code}: {v[0]}',fill='white')
board.save(out/'color-comparison.jpg',quality=94)
print('Still candidates ready')
