"""Is the listener telling edits from speech? The same prompt on five sentence gaps with no edit in them (middle of one take), plus the two joins, each twice, under neutral names."""
import base64, json, os, re, subprocess, urllib.request, random
FF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
key = next(l.split("=", 1)[1].strip().strip('"\'') for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if re.match(r"(export )?(GEMINI_API_KEY|GOOGLE_API_KEY)=", l))
P = "This is a recording of a man talking outdoors, and it may contain an audio edit. Write out the words you hear, then reply CLEAN or FAULT. FAULT only for what an ordinary viewer would notice: chopped word, hard start, click, sudden change in background sound, repeated word, stumble, or a gap that feels too short or too long. Say when in the clip."
W = json.load(open("/Volumes/Expansion/_edit_work/RO-37/round1/words_out.json"))
J = json.load(open("checks/joins.json"))
sys_path = __import__("sys").path; sys_path.insert(0, "recipe"); import r2
ws = [w for w in r2.WORDS if w.get("t0") is not None]
cand = [(a["t1"], b["t0"]) for a, b in zip(ws, ws[1:]) if a["w"][-1:] in ".?!" and .2 < b["t0"] - a["t1"] < .6 and all(abs(a["t1"] - j) > 6 for j in J)]
cov = [(c["t0"] - 3, c["t1"] + 3) for c in r2.CLIPS]; cand = [c for c in cand if not any(x <= c[0] <= y for x, y in cov)]
random.seed(11); ctl = random.sample(cand, min(5, len(cand))); print(len(cand), ctl)
items = [(f"ctl{i}", c[0] - 1.9, c[1] + 1.9) for i, c in enumerate(ctl)] + [("join1", 9.6, 13.4), ("join2", 161.0, 166.0)]
random.shuffle(items); res = {}
for name, a, b in items:
    p = f"checks/listen/x_{name}.mp3"; subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(a), "-to", str(b), "-i", "checks/mono.wav", "-b:a", "160k", p], check=True)
    for run in (1, 2):
        body = {"contents": [{"role": "user", "parts": [{"inlineData": {"mimeType": "audio/mpeg", "data": base64.b64encode(open(p, "rb").read()).decode()}}, {"text": P}]}]}
        r = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent", data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
        t = "".join(x.get("text", "") for x in json.load(urllib.request.urlopen(r, timeout=200))["candidates"][0]["content"]["parts"])
        res.setdefault(name, []).append(t); v = "FAULT" if "FAULT" in t.upper() else "CLEAN"; print(name, run, v, t[-130:].replace("\n", " "), flush=True)
json.dump(res, open("checks/listen/control.json", "w"), indent=0)
