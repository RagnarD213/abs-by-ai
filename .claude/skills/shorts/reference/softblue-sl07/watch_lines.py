"""Watch pickups/t3/seg_*.wav as rec_mic writes them; transcribe each new segment (with the one before it, so a line that
straddles a boundary is still heard) and stop the recorder (touch STOP) once both pickup lines were read at least twice
and 20 s have passed with no further take. Prints every line heard."""
import glob, os, re, sys, time, wave, json, numpy as np
D = "/Volumes/Extreme/_edit_work/sl07/pickups/t5"
KEY = {"B": "fat loss plan is working", "D": "work out every single morning"}
import whisper, scipy.signal as ss
M = whisper.load_model("small.en")
def rd(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32).reshape(-1, w.getnchannels()).mean(1) / 32768; return x
done = set(); hits = {"B": [], "D": []}; last_hit = None; t0 = time.time()
while time.time() - t0 < 1850:
    segs = sorted(glob.glob(D + "/seg_*.wav"))
    new = [s for s in segs if s not in done]
    for s in new:
        k = segs.index(s); x = rd(s); off = k * 30.0
        if 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-7) < -50: done.add(s); continue          # room tone only
        if k: x = np.concatenate([rd(segs[k - 1])[-8 * 48000:], x]); off -= 8.0
        a = ss.resample_poly(x, 16000, 48000).astype(np.float32); a = a * min(10.0, 0.5 / (np.abs(a).max() + 1e-6))
        r = M.transcribe(a, fp16=False, condition_on_previous_text=False)
        for g in r["segments"]:
            txt = g["text"].strip(); print("%7.1f %s" % (off + g["start"], txt), flush=True)
            for key, ph in KEY.items():
                if ph in re.sub(r"[^a-z ]", "", txt.lower()) and not any(abs(h - (off + g["start"])) < 2.0 for h in hits[key]):
                    hits[key].append(off + g["start"]); last_hit = time.time()
        done.add(s)
    if len(hits["B"]) >= 2 and len(hits["D"]) >= 2 and last_hit and time.time() - last_hit > 45:
        open(D + "/STOP", "w").write("both lines heard\n"); print("STOP: B takes at", hits["B"], "D takes at", hits["D"], flush=True); break
    if not os.path.exists(D) or os.path.exists(D + "/STOP"): break
    time.sleep(5)
json.dump(hits, open(D + "/hits.json", "w")); print("watcher done", hits)
