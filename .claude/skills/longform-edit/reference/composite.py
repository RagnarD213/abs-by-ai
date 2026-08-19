import subprocess, sys
BIN="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/longform-raw/absbyai-0803-shoot/roughcuts"
SRC=f"{D}/SPLITSCREEN_v2_graded.mp4"; OUT=f"{D}/SPLITSCREEN_v3_graphics.mp4"
G="/tmp/sc/gfx"
# (key, start, end) in render time. Chips sit on the camera side, lower third.
CHIPS=[("intro",   2.0,   7.6),
       ("s1",     40.0,  45.6),   # beat: add photos
       ("s2",     63.5,  69.1),   # beat: servings
       ("s3",     78.0,  83.6),   # beat: why context matters
       ("s4",    115.4, 120.4),   # beat: analyze
       ("s5",    125.5, 131.1),   # beat: clarifying questions
       ("cal",   176.0, 182.4),   # he says "683 calories" at 176.6
       ("s6",    198.0, 203.6)]   # beat: log a serving
FADE=0.35
cmd=[f"{BIN}/ffmpeg","-y","-v","error","-i",SRC]
for k,a,b in CHIPS: cmd += ["-loop","1","-t",f"{b-a:.2f}","-i",f"{G}/chip_{k}.png"]
cmd += ["-i",f"{G}/wm.png"]
parts=[]; last="0:v"
for i,(k,a,b) in enumerate(CHIPS,start=1):
    dur=b-a
    parts.append(f"[{i}:v]format=rgba,fade=t=in:st=0:d={FADE}:alpha=1,"
                 f"fade=t=out:st={dur-FADE:.2f}:d={FADE}:alpha=1,setpts=PTS+{a}/TB[c{i}]")
    parts.append(f"[{last}][c{i}]overlay=0:0:enable='between(t,{a},{b})'[v{i}]")
    last=f"v{i}"
wm=len(CHIPS)+1
parts.append(f"[{last}][{wm}:v]overlay=0:0[vout]")
cmd += ["-filter_complex",";".join(parts),"-map","[vout]","-map","0:a",
        "-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",
        "-c:a","copy",OUT]
r=subprocess.run(cmd,capture_output=True,text=True)
print("rc",r.returncode); print(r.stderr[-1200:] if r.returncode else "OK -> "+OUT)
