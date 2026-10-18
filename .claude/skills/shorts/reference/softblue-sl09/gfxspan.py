"""When Zeeshan's lower-third box (navy glass, x 90-1830, rows ~760-1025) and the J verdict card (top-left) are on screen, per frame."""
import json, subprocess, numpy as np
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"; FPS=30000/1001
R={"A":(680.5,739.5),"H":(926.5,986.0),"I":(988.0,1066.5),"J":(1065.5,1114.0),"K":(194.0,238.5)}
ref=None; out={}
for S,(a0,a1) in R.items():
    raw=subprocess.run([FF,"-v","error","-ss",f"{a0:.3f}","-i","master.mp4","-t",f"{a1-a0:.3f}","-vf","scale=480:270:in_color_matrix=bt709","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8).reshape(-1,270,480,3).astype(np.int16)
    # lower third: the box's left accent bar region + navy fill in rows 190..256, cols 22..458
    reg=fr[:,190:256,22:458]; R_,G_,B_=reg[...,0],reg[...,1],reg[...,2]
    navy=((B_-R_>18)&(B_<140)&(R_<70)).mean((1,2))
    # verdict card: top-left cols 15..158 rows 20..210, navy and bright text
    reg2=fr[:,20:210,15:158]; navy2=((reg2[...,2]-reg2[...,0]>25)&(reg2[...,0]<60)).mean((1,2))
    t=a0+np.arange(len(fr))/FPS
    def spans(sig,th):
        on=sig>th; sp=[]; i=0
        while i<len(on):
            if on[i]:
                j=i
                while j<len(on) and on[j]: j+=1
                if j-i>5: sp.append((round(float(t[i]),3),round(float(t[j-1]),3)))
                i=j
            else: i+=1
        return sp
    out[S]=dict(lt=spans(navy,0.25),card=spans(navy2,0.25),lt_sig=[round(float(x),2) for x in navy[::3]])
    print(S,"lower thirds",out[S]["lt"],"| card",out[S]["card"])
json.dump(out,open("gfx_spans.json","w"))
