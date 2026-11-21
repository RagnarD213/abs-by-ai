import glob, os, json, whisper
m = whisper.load_model("base")
out = {}
files = sorted(glob.glob("probes/*_probe.wav"))
for i, f in enumerate(files):
    b = os.path.basename(f).replace("_probe.wav","")
    r = m.transcribe(f, language="en", fp16=False, verbose=False)
    out[b] = r["text"].strip()
    print(f"[{i+1}/{len(files)}] {b}: {out[b][:400]}", flush=True)
json.dump(out, open("tx/probes.json","w"), indent=1)
print("PROBES DONE")
