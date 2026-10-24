"""SL-16: prompted disfluency sweep (VIDEO-RULES 2026-10-20 stumbles): Whisper small.en with initial_prompt "Um, uh, mm." on 10 s windows of
each short's cut audio; prints every um/uh/repeat and every word longer than 0.5 s."""
import json, re, sys, wave, numpy as np, whisper
m = whisper.load_model("small.en")
for S in sys.argv[1:]:
    w = wave.open(f"build/{S}/his_mix.wav"); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32).reshape(-1, 2).mean(1) / 32768
    import scipy.signal as ss; a = ss.resample_poly(x, 1, 3).astype(np.float32); out = []
    for s0 in np.arange(0, len(a) / 16000, 8.0):
        seg = a[int(s0 * 16000):int((s0 + 10) * 16000)]
        r = m.transcribe(seg, fp16=False, initial_prompt="Um, uh, mm. So, like, you know.", condition_on_previous_text=False, word_timestamps=True)
        for sg in r["segments"]:
            for wd in sg["words"]: out.append((round(s0 + wd["start"], 2), round(s0 + wd["end"], 2), wd["word"].strip()))
    flags = [o for o in out if re.sub(r"[^a-z]", "", o[2].lower()) in ("um", "uh", "mm", "er", "ah", "hmm") or (o[1] - o[0] > 0.5)]
    reps = [(out[i][0], out[i][2]) for i in range(1, len(out)) if re.sub(r"[^a-z]", "", out[i][2].lower()) == re.sub(r"[^a-z]", "", out[i - 1][2].lower()) and out[i][0] - out[i - 1][0] < 1.0 and len(out[i][2]) > 1]
    print(S, "FLAGS:", flags, "\n   REPEATS:", sorted(set(reps)), flush=True)
    json.dump(out, open(f"build/{S}/disfl.json", "w"))
