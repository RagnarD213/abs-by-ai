"""Transcribe the assembled voice (medium.en) and print it per piece join, so every join can be read for clipped or doubled words."""
import sys, json
sys.path.insert(0, "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/cut")
import speech
W = "/Volumes/Expansion/_edit_work/RO-37/round1"; FPS = 30000/1001
ws, _ = speech.transcribe(f"{W}/{sys.argv[1] if len(sys.argv) > 1 else 'assembled_untreated.wav'}", model="medium.en")
json.dump(ws, open(f"{W}/asr_assembled.json", "w"))
S = json.load(open(f"{W}/shots.json")); joins = [s["out_f0"]/FPS for s in S if not s["reframe"]][1:]
for j in joins:
    near = [w for w in ws if j - 2.2 <= w["t"] <= j + 2.2]
    print(f"{j:7.2f} | " + " ".join(("‖" if w["t"] >= j and (k == 0 or near[k-1]["t"] < j) else "") + w["w"].strip() for k, w in enumerate(near)))
