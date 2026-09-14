import subprocess, numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
HIS="/Volumes/Extreme/_edit_work/ad3-vert/ref/ad3_v6hd.mp4"
V1="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/batch1-ads/clips/ai-trainer-vs-robot-story-35s.mp4"
FPS=30000/1001; T0=121/24; SL=T0/(137/FPS)
def t_of(n): return T0 + SL*(n-2065)/FPS
def read(path,n0,n1,w,h,vf_pre=''):
    vf=f"{vf_pre}select='between(n\\,{n0}\\,{n1-1})',format=rgb24"
    raw=subprocess.run([FF,'-nostdin','-v','error','-i',path,'-vf',vf,'-vsync','0','-f','rawvideo','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,h,w,3)
def his(n0,n1): return read(HIS,n0,n1,1920,1080,'scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,')
def story(path,j0,j1): return read(path,j0,j1,1080,1920,'scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,')
def jmap(n0,n1):
    out=[];last=-1
    for n in range(n0,n1):
        j=max(round(t_of(n)*24),last); last=j; out.append(j)
    return out
