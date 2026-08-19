import subprocess, os, sys
BIN="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot"
CAM=f"{D}/C1541.MP4"; SCR=f"{D}/screen_capture_TAKE2.MP4"
OUT="/tmp/sc/segs_g"; os.makedirs(OUT,exist_ok=True)
GRADE=("colorchannelmixer=rr=0.984:gg=1.000:bb=1.017,"
       "curves=all='0/0 0.050/0.004 0.25/0.27 0.50/0.565 0.80/0.855 1/1'")
SCR_CROP="crop=1320:2500:0:175,scale=570:1080"
CAM_CROP="crop=1350:1080:375:0"
BEATS=[
 ("INTRO",0.78,15.14,None),("SETUP: open app",33.70,47.86,8.0),
 ("SETUP: pick meal prep",48.96,59.96,24.0),("STEP: add photos",60.42,65.00,36.0),
 ("STEP: greens",66.32,68.92,41.0),("STEP: use photo",71.36,72.52,47.5),
 ("STEP: proteins",74.60,77.66,53.0),("STEP: shot",81.76,83.48,57.0),
 ("STEP: use photo 2",86.94,88.12,63.0),("STEP: olive oil",88.82,97.66,66.0),
 ("STEP: servings + context",100.86,115.20,78.0),("WHY context matters",117.04,144.66,93.0),
 ("STEP: dictate context",146.50,157.06,121.0),("STEP: analyze",160.64,162.58,134.5),
 ("GOTCHA: takes longer",172.58,179.52,138.0),("GOTCHA: questions",201.98,233.36,183.0),
 ("RESULT: itemized macros",237.96,265.62,214.5),("RESULT: accuracy",288.08,296.32,255.0),
 ("STEP: save",299.58,305.08,270.0),("RECAP: log a serving",308.68,340.24,285.0),
]
paths=[]
for i,(beat,cs,ce,ss) in enumerate(BEATS):
    dur=round(ce-cs,3); out=f"{OUT}/seg_{i:02d}.mp4"; paths.append(out)
    fo=max(0.0,dur-0.03)
    af=f"afade=t=in:st=0:d=0.03,afade=t=out:st={fo:.3f}:d=0.03"
    if ss is None:
        fc=f"[0:v]scale=1920:1080,{GRADE},setsar=1,fps=30[v];[0:a]{af}[a]"
        cmd=[f"{BIN}/ffmpeg","-y","-v","error","-ss",str(cs),"-t",str(dur),"-i",CAM,
             "-filter_complex",fc,"-map","[v]","-map","[a]"]
    else:
        # GRADE applied to CAMERA ONLY - the screen recording is already neutral
        fc=(f"[1:v]{SCR_CROP},setsar=1[p];[0:v]{CAM_CROP},{GRADE},setsar=1[d];"
            f"[p][d]hstack=inputs=2,fps=30[v];[0:a]{af}[a]")
        cmd=[f"{BIN}/ffmpeg","-y","-v","error","-ss",str(cs),"-t",str(dur),"-i",CAM,
             "-ss",str(ss),"-t",str(dur),"-i",SCR,
             "-filter_complex",fc,"-map","[v]","-map","[a]"]
    cmd+=["-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
          "-c:a","aac","-ar","48000","-ac","2",out]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode!=0: print("FAIL",i,beat,r.stderr[:500]); sys.exit(1)
    print(f"  [{i:02d}] {beat}",flush=True)
with open("/tmp/sc/concat_g.txt","w") as f:
    for p in paths: f.write("file '%s'\n"%p)
print("graded segments done")
