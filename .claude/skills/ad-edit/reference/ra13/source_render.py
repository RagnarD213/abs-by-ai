import sys,subprocess,json,os
from pathlib import Path
w=Path(__file__).resolve().parents[1];os.chdir(w)
r=Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI")
sys.path.insert(0,str(r/".claude/skills/_shared"))
import buildcap
buildcap.wait("RA-13 source checks and audio selftest")
ff=str(r/"Media/video_edit/bin/ffmpeg")
roll=json.load(open("source/roll.json"))["identity"]["current_path"]
with open("logs/audio-selftest.log","w") as f:
 p=subprocess.run(["zsh",str(r/".claude/skills/_shared/audio/selftest.sh")],stdout=f,stderr=subprocess.STDOUT)
print("selftest exit",p.returncode,flush=True)
subprocess.run([ff,"-v","error","-y","-ss","254","-i",roll,"-t","73","-vf","scale=in_color_matrix=bt709:in_range=tv,scale=540:960","-c:v","libx264","-preset","fast","-crf","24","-af","pan=mono|c0=0.5*c0+0.5*c1","-c:a","aac","-b:a","96k","-movflags","+faststart","source/takes.mp4"],check=True)
for tm in (256,269,289,313,324):
 subprocess.run([ff,"-v","error","-y","-ss",str(tm),"-i",roll,"-frames:v","1","-vf","scale=in_color_matrix=bt709:in_range=tv","source/raw-%s.png"%tm],check=True)
print("SOURCE READY",flush=True)
