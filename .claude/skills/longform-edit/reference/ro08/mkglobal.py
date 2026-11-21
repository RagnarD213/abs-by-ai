"""RO-08 is cut from one roll (C1486); the two-roll RO-07 recipe runs unchanged. One GLOBAL source timeline (rolls end to end, frame-exact) lets
the single-roll recipe run unchanged: rolls.json {roll: {f0, n, path}}, lav.wav (global), words.json (global, medium.en words)."""
import json, subprocess, wave, numpy as np
W = "/Volumes/Extreme/_edit_work/ro08"; FPS = 30000/1001; SR = 48000
SHOOT = "/Volumes/Extreme/abs by ai 7:8 Jeff Chagrin shoot/main camera"
FP = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe"
R = {}; f0 = 0; chunks = []; words = []
for roll in ("C1486",):
    path = f"{SHOOT}/{roll}.MP4"
    nf = int(subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames", "-of", "csv=p=0", path],
                            capture_output=True, text=True).stdout.strip())
    R[roll] = dict(f0=f0, n=nf, path=path)
    wv = wave.open(f"{W}/lav/{roll}.wav"); a = np.frombuffer(wv.readframes(wv.getnframes()), np.int16)
    ns = int(round((f0+nf)/FPS*SR)) - int(round(f0/FPS*SR)); x = np.zeros(ns, np.int16); m = min(ns, len(a)); x[:m] = a[:m]; chunks.append(x)
    off = f0/FPS
    for s in json.load(open(f"{W}/asr_{roll}_medium.json"))["segments"]:
        for w in s["words"]: words.append(dict(word=w["word"], start=round(w["start"]+off, 3), end=round(w["end"]+off, 3), roll=roll))
    f0 += nf
# C1486 1126.7 to 1130.1: Whisper hid an abandoned sentence and its retake inside one 3.4 s "some". The retake's words, from a
# medium.en pass on the window alone (verify_asr.py C1486:1127.3:1131.0), replace the stretched word.
k = next(i for i, w in enumerate(words) if w["roll"] == "C1486" and 1126.5 < w["start"] < 1126.9 and w["end"] - w["start"] > 3)
fix = [("With", 1128.11, 1128.26), ("that", 1128.26, 1128.48), ("being", 1128.48, 1128.62), ("said", 1128.62, 1128.92), ("though,", 1128.92, 1129.14),
       ("you", 1129.40, 1129.48), ("do", 1129.48, 1129.66), ("have", 1129.66, 1129.90), ("some", 1129.90, 1130.08)]
words[k:k+1] = [dict(word=" " + a, start=b, end=c, roll="C1486") for a, b, c in fix]
json.dump(R, open(f"{W}/rolls.json", "w"), indent=1)
o = wave.open(f"{W}/lav.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(np.concatenate(chunks).tobytes()); o.close()
json.dump(dict(words=words), open(f"{W}/words.json", "w"))
print(len(R), "rolls,", f0, "frames =", round(f0/FPS, 1), "s;", len(words), "words")
