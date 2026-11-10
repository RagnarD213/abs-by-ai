"""Per-frame camera motion (phase correlation on the whole frame, 480 wide) for a library clip: px/frame at 1080p window scale ~ x2.25."""
import sys, subprocess, json, numpy as np, cv2
R='/Users/danielrose/Projects/Claude/Projects/Abs By AI'; F=R+'/Media/video_edit/bin/ffmpeg'
L=json.load(open('/Users/danielrose/Projects/_edit_work/DS-78/round1/records/library.json'))
lib=sys.argv[1]; a=float(sys.argv[2]); b=float(sys.argv[3])
raw=subprocess.check_output([F,'-v','error','-ss',str(a),'-i',L[lib]['path'],'-t',str(b-a),'-vf','scale=480:270,format=gray','-f','rawvideo','-'])
fr=np.frombuffer(raw,np.uint8).reshape(-1,270,480).astype(np.float32); out=[]
win=cv2.createHanningWindow((480,270),cv2.CV_32F)
for i in range(1,len(fr)):
    (dx,dy),_=cv2.phaseCorrelate(fr[i-1],fr[i],win); out.append((round(a+i/29.97,2),round(float(np.hypot(dx,dy))*8,1)))  # x8: 480-wide -> 3840 native px
bad=[(t,m) for t,m in out if m>8]
print(lib,'native px/frame >8 at:',[t for t,m in bad][:60])
json.dump(out,open(f'/Users/danielrose/Projects/_edit_work/DS-78/round1/evidence/motion-{lib}-{a}.json','w'))
