"""Every beat's LAST WORDS, re-transcribed FROM THE FINISHED RENDER, against the
words the EDL intended to keep. A -30dB silence assertion cannot see a clipped
trailing fricative (it is below threshold), so this is the discriminating test.
The window must EXTEND ~1.5s PAST the join. Ending it exactly at the join
truncates Whisper's audio and it silently drops the final word -- that produced 7
false "LAST WORD MISSING" reports. With trailing context the real signature is
different: the word is PRESENT but mis-spelled (crunches -> crunch), i.e. its
trailing fricative was cut."""
import json, subprocess, sys, whisper, re
BASE="/Volumes/Seagate 4TB/_edit_work/abwheel"
edl=json.load(open(f"{BASE}/edl.json"))
W={b:[w for s in json.load(open(f"{BASE}/{b}.whisper.json"))["segments"] for w in s.get("words",[])]
   for b in edl["sources"]}
offs,acc=[],0.0
for r in edl["ranges"]: offs.append(acc); acc+=round(r["end"]-r["start"],3)
m=whisper.load_model("small")
def norm(t): return re.sub(r"[^a-z0-9 ]",""," ".join(t.lower().split()))
print(f"{'beat':26s} {'intended tail':38s} | rendered tail")
bad=[]
for r,o in zip(edl["ranges"],offs):
    end=o+round(r["end"]-r["start"],3)
    intended=[w["word"].strip() for w in W[r["source"]]
              if w["start"]>=r["end"]-2.6 and w["start"]<r["end"]]
    if not intended: continue
    a=max(0,end-4.5); z=end+1.5
    subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{a:.2f}","-i",
        f"{BASE}/roughcuts/FINAL_abwheel.mp4","-t",f"{z-a:.2f}","-vn","-ac","1","-ar","16000",
        "/tmp/sc/_tail.wav"],check=True)
    got=m.transcribe("/tmp/sc/_tail.wav",language="en",fp16=False,verbose=False)["text"].strip()
    itxt=norm(" ".join(intended)); gtxt=norm(got)
    lastword=norm(intended[-1])
    hit = lastword and lastword in gtxt
    mark="" if hit else "  <-- LAST WORD MISSING"
    if not hit: bad.append(r["beat"])
    print(f"{r['beat']:26s} {' '.join(intended)[-38:]:38s} | {got[-58:]}{mark}")
print("\nsuspect beats:", bad or "none")
