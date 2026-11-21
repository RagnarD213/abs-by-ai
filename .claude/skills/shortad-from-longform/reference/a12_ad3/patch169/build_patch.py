import sys; sys.path.insert(0,sys.argv[1]); from model import *
S=sys.argv[1]; M=np.load(S+'/matte2.npz'); outside,band,label,s,k,a,L=[M[x] for x in ('outside','band','label','s','k','a','L')]
V2P="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/batch1-ads/clips/ai-trainer-vs-robot-story-35s_v2.mp4"
Hall=his(2202,2339); V2=story(V2P,j0,J.max()+1)
Y,X=BB
proc=subprocess.Popen([FF,'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30000/1001','-i','-',
    '-vf','scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p','-c:v','ffv1','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',S+'/patch.mkv'],stdin=subprocess.PIPE)
chg=[]
for i,n in enumerate(range(2202,2339)):
    f=Hall[i].astype(np.float32); Pn=predict(n,V2,j0,None)[Y,X]
    c=Pn.copy()
    c=np.where(band[...,None], s*Pn+k, c)
    c=np.where(label[...,None], (1-a[...,None])*Pn+a[...,None]*L, c)
    c=np.where(outside[...,None], f[Y,X], c)
    out=f.copy(); out[Y,X]=c
    o8=np.clip(np.round(out),0,255).astype(np.uint8)
    chg.append(np.abs(o8.astype(int)-Hall[i]).mean())
    proc.stdin.write(o8.tobytes())
    if i in (40,100,125): cv2.imwrite(S+f'/patched_{n}.png',cv2.cvtColor(np.concatenate([Hall[i],o8],1)[60:1010,650:2*1920-640],cv2.COLOR_RGB2BGR))
proc.stdin.close(); proc.wait(); print('frames',len(chg),'mean change per frame min %.1f max %.1f'%(min(chg),max(chg)))
