"""Speech-only read of the film mix: cut the talking sections out of film_audio.wav and print their loudness + hold levels."""
import wave, numpy as np, subprocess, json, sys
W="/Volumes/Extreme/_edit_work/ro03"; FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
S=json.load(open(f"{W}/shots.json")); FPS=30000/1001
w=wave.open(f"{W}/film_audio.wav"); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).reshape(-1,2)
talk=[(s["out_f0"]/FPS,s["out_f1"]/FPS) for s in S if not s["piece"].startswith("set")]
x=np.concatenate([a[int(s*sr):int(e*sr)] for s,e in talk]); o=wave.open(f"{W}/tmp/tune/speech_only.wav","w"); o.setnchannels(2); o.setsampwidth(2); o.setframerate(sr); o.writeframes(x.tobytes()); o.close()
def lufs(p):
    r=subprocess.run([FF,"-nostats","-i",p,"-af","ebur128","-f","null","-"],capture_output=True,text=True).stderr
    import re; return float(re.findall(r"I:\s*(-?[\d.]+) LUFS",r)[-1])
m=a.astype(np.float32).mean(1)/32768
def rms(t0,t1): y=m[int(t0*sr):int(t1*sr)]; return round(float(20*np.log10(np.sqrt(np.mean(y*y))+1e-9)),1)
MK=json.load(open(f"{W}/marks.json"))
print("film LUFS", lufs(f"{W}/film_audio.wav"), "| speech-only LUFS", lufs(f"{W}/tmp/tune/speech_only.wav"), "| speech rms", [rms(a_,b_) for a_,b_ in ((0.3,5.6),(28.2,52),(78.2,105.9),(129.3,150.9))], "| holds rms", [rms(h+1,h+19) for h in MK["holds"]])
