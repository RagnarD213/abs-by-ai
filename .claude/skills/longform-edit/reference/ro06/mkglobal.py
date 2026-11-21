"""RO-06 is cut from 25 rolls. One GLOBAL source timeline (rolls laid end to end, frame-exact) lets the single-roll
recipe run unchanged: rolls.json {roll: {f0, n, path}}, lav.wav (global), words.json (global, sidecar small words)."""
import json, subprocess, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro06"; FPS = 30000/1001; SR = 48000
SHOOT = "/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera"
FP = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe"
R = {}; f0 = 0; chunks = []; words = []
small = json.load(open(f"{W}/words_small.json"))
for n in range(1557, 1582):
    roll = f"C{n}"; path = f"{SHOOT}/{roll}.MP4"
    nf = int(subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "csv=p=0", path],
                            capture_output=True, text=True).stdout.strip())
    R[roll] = dict(f0=f0, n=nf, path=path)
    wv = wave.open(f"{W}/lav/{roll}.wav"); a = np.frombuffer(wv.readframes(wv.getnframes()), np.int16)
    ns = int(round((f0+nf)/FPS*SR)) - int(round(f0/FPS*SR)); x = np.zeros(ns, np.int16); m = min(ns, len(a)); x[:m] = a[:m]; chunks.append(x)
    off = f0/FPS
    for w in small[roll]: words.append(dict(word=w["word"], start=round(w["start"]+off, 3), end=round(w["end"]+off, 3), roll=roll))
    f0 += nf
json.dump(R, open(f"{W}/rolls.json", "w"), indent=1)
o = wave.open(f"{W}/lav.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(np.concatenate(chunks).tobytes()); o.close()
json.dump(dict(words=words), open(f"{W}/words.json", "w"))
print(len(R), "rolls,", f0, "frames =", round(f0/FPS, 1), "s;", len(words), "words")
