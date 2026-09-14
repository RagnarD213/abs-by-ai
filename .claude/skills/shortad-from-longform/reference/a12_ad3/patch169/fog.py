import subprocess, numpy as np, cv2, sys
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
def frames(p):
    raw=subprocess.run([FF,'-v','error','-i',p,'-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,1284,716)
S=sys.argv[1]
files=[('orig','/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/batch1-ads/shots/s3.mp4')]+[(f't{i}',f'{S}/gen/t{i}.mp4') for i in range(4)]
for name,p in files:
    F=frames(p)
    # mirror + air in front of face region, plus whole-frame haze proxy
    out=[]
    for f in F:
        m=f[360:660,440:700].astype(np.float32)
        lap=cv2.Laplacian(m,cv2.CV_32F).var()
        out.append(lap)
    out=np.array(out); b=out[:24].mean()
    print(name, 'mirror sharpness rel. to first second, per 12 frames:', ' '.join('%.2f'%(out[i:i+12].mean()/b) for i in range(0,121,12)), '| min %.2f'%(out.min()/b))
