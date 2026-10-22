"""RO-24 screen study: per-pixel clean plate of the C1726 green screen vs the locked quadratic field.
Samples frames across the Ozempic section at half resolution (1920x1080, rgb48, accurate BT709), keeps
pixels that are clearly screen and far from Dan, takes the per-pixel median. Writes plate_half.npy (float32)
and coverage, and prints how far the locked 6-term quadratic sits from the plate (green excess units)."""
import subprocess, numpy as np, cv2, json, sys
SRC='/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1726.MP4'
FF='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'
W='/Volumes/Expansion/_edit_work/RO-24/round1/key'
VF='scale=in_color_matrix=bt709:in_range=tv:out_range=pc:flags=accurate_rnd+full_chroma_int,scale=1920:1080:flags=area,format=rgb48le'
def grab(t):
    raw=subprocess.check_output([FF,'-v','error','-ss',f'{t:.3f}','-i',SRC,'-frames:v','1','-an','-vf',VF,'-f','rawvideo','-'])
    return np.frombuffer(raw,'<u2').reshape(1080,1920,3).astype(np.float32)/65535
ts=np.linspace(445,1064,int(sys.argv[1]) if len(sys.argv)>1 else 40)
stack=[];masks=[]
for t in ts:
    im=grab(t); r,g,b=im.transpose(2,0,1); ex=g-np.maximum(r,b)
    fg=(ex<0.06).astype(np.uint8)
    fg=cv2.dilate(fg,np.ones((61,61),np.uint8))       # keep well clear of Dan, his hair and motion blur
    ok=(fg==0)&(ex>0.06)
    stack.append(np.where(ok[:,:,None],im,np.nan).astype(np.float16)); masks.append(ok)
S=np.stack(stack).astype(np.float32); cov=np.stack(masks).sum(0)
plate=np.nanmedian(S,axis=0)
# fill never-seen pixels with the quadratic fit of the plate, then blend in the residual smoothly
h,w=plate.shape[:2]; y,x=np.mgrid[:h,:w].astype(np.float32); x/=w; y/=h
X=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],-1); seen=cov>=3
coef=np.linalg.lstsq(X[seen][::7],plate[seen][::7],rcond=None)[0]; quad=X@coef
res=np.where(seen[:,:,None],plate-quad,0).astype(np.float32); wgt=seen.astype(np.float32)
num=cv2.GaussianBlur(res,(0,0),25); den=cv2.GaussianBlur(wgt,(0,0),25)[:,:,None]
fill=quad+num/np.maximum(den,1e-3)*np.clip(den/0.2,0,1)
full=np.where(seen[:,:,None],plate,fill).astype(np.float32)
np.save(f'{W}/plate_half.npy',full); np.save(f'{W}/plate_cov.npy',cov.astype(np.uint8)); np.save(f'{W}/plate_quadcoef.npy',coef)
ch=lambda a:a[...,1]-np.maximum(a[...,0],a[...,2])
d=np.abs(ch(full)-ch(quad))
print('frames',len(ts),'never-seen px',int((~seen).sum()),'of',seen.size)
for name,sl in [('all',np.s_[:,:]),('bottom 25%',np.s_[810:,:]),('top 25%',np.s_[:270,:]),('left third',np.s_[:,:640]),('right third',np.s_[:,1280:]),('around head x800-1300 y0-400',np.s_[0:400,800:1300])]:
    v=d[sl]; print(f'{name:32s} |plate-quad| green excess: p50 {np.percentile(v,50):.4f} p95 {np.percentile(v,95):.4f} max {v.max():.4f}')
print('screen green excess p50', float(np.median(ch(full))))
vis=np.clip(full,0,1); cv2.imwrite(f'{W}/plate_half.jpg',(vis[:,:,::-1]*255).astype(np.uint8))
dv=np.clip(d/0.03,0,1); cv2.imwrite(f'{W}/plate_minus_quad.jpg',(dv*255).astype(np.uint8))
cv2.imwrite(f'{W}/plate_cov.jpg',(np.clip(cov/len(ts),0,1)*255).astype(np.uint8))
