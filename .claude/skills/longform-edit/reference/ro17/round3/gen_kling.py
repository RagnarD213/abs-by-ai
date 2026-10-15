#!/usr/bin/env python3
"""gen_kling.py ID DUR TAKE PROMPT_FILE -> takes/<ID>_t<TAKE>.mp4 via Kling v3 (Replicate kwaivgi/kling-v3-video), START+END,
standard mode, no audio. Used where Veo's filter refuses a pair (A7: E005 twice). Estimate $1.00 a take, logged in spend.jsonl."""
import base64, json, os, sys, time, urllib.request
R3 = "/Volumes/Extreme/_edit_work/RO-17/round3"; REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, REPO + "/.claude/skills/_shared/framecheck")
T = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
H = {"Authorization": "Bearer " + T, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
NEG = ("camera movement, camera shake, zoom, pan, cuts, scene change, morphing, warping, extra fingers, distorted hands, extra arms, "
       "extra people, face distortion, flicker, watermark, logo, text, slow motion, floating objects, objects appearing, objects disappearing")
def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()
if __name__ == "__main__":
    from gate import require_pass
    i, dur, take, pf = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    s, e = f"{R3}/aiframes/{i}-start.png", f"{R3}/aiframes/{i}-end.png"; require_pass(s, e)
    body = json.dumps({"input": {"prompt": open(pf).read(), "negative_prompt": NEG, "start_image": b64(s), "end_image": b64(e),
                                 "duration": dur, "mode": "standard", "generate_audio": False}}).encode()
    p = json.load(urllib.request.urlopen(urllib.request.Request("https://api.replicate.com/v1/models/kwaivgi/kling-v3-video/predictions", data=body, headers=H)))
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(10); p = json.load(urllib.request.urlopen(urllib.request.Request(p["urls"]["get"], headers=H)))
    out = f"{R3}/motion/takes/{i}_t{take}.mp4"; ok = p["status"] == "succeeded"
    if ok:
        url = p["output"] if isinstance(p["output"], str) else p["output"][0]
        open(out, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})).read())
    rec = dict(id=i, take=take, dur=dur, usd=1.0, ok=ok, out=out, prompt=pf, model="kling-v3 standard (estimate)", err=str(p.get("error"))[:300] if not ok else "")
    open(f"{R3}/motion/spend.jsonl", "a").write(json.dumps(rec) + "\n"); print(json.dumps(rec))
