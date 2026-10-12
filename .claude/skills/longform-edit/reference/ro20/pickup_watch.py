#!/usr/bin/env python3
"""Watch a rec_mic output folder while Dan re-records the RO-20 pickups: transcribe each finished 30 s segment, log it, and
write OUT_DIR/STOP once every pickup's marker phrase has been heard twice (VIDEO-RULES, 2026-10-11 pickup procedure).
usage: pickup_watch.py OUT_DIR RECORDER_PID"""
import sys, os, time, json, glob, re, wave
import whisper
D, pid = sys.argv[1], int(sys.argv[2])
M = whisper.load_model("small.en")
MARK = {"P1": r"mega ?(baller|bowler|mower|bower|bala)", "P2": r"ludicrously expensive", "P3": r"six[- ]?pack abs",
        "P4": r"(now )?let'?s spend it"}
seen, text = set(), []
def alive():
    try: os.kill(pid, 0); return True
    except OSError: return False
def counts():
    t = " ".join(text).lower()
    return {k: len(re.findall(v, t)) for k, v in MARK.items()}
while True:
    live = alive()
    for p in sorted(glob.glob(f"{D}/seg_*.wav")):
        if p in seen: continue
        seen.add(p)
        w = wave.open(p); dur = w.getnframes()/w.getframerate(); w.close()
        r = M.transcribe(p, language="en", fp16=False, condition_on_previous_text=False)
        t = r["text"].strip(); text.append(t)
        json.dump(dict(seg=os.path.basename(p), seconds=dur, text=t), open(f"{D}/watch.jsonl", "a")); open(f"{D}/watch.jsonl", "a").write("\n")
        print(os.path.basename(p), f"{dur:.1f}s", t[:160], flush=True)
        c = counts(); print("heard:", c, flush=True)
        if all(v >= 2 for v in c.values()) and not os.path.exists(f"{D}/STOP"):
            time.sleep(20)                                   # let him finish the line he is on
            open(f"{D}/STOP", "w").write("all four pickups heard twice\n"); print("STOP written", flush=True)
    if not live: break
    time.sleep(3)
print("recorder finished; heard:", counts(), flush=True)
