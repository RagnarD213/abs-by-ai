"""RO-07: AI motion from Dan's approved frame pairs (round2-plan/decisions.json, hashes in round1-hashes.sha256), Veo 3.1 Fast on Replicate
(image + last_frame, 1080p, no audio). The 1672x941 frames are scaled to 1920x1080 first. One prediction at a time.
usage: gen_motion.py <A2|A3> <tag> [seconds]   prompt: round2/motion/<ID>.txt (+ <ID>.neg.txt)
Writes round2/motion/<tag>.mp4 + <tag>.json and appends the cost to round2/motion/ledger.json. Never overwrites a take."""
import base64, hashlib, io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro07"; M = f"{W}/round2/motion"; MODEL = "google/veo-3.1-fast"; USD_S = 0.10
D = json.load(open(f"{W}/round2-plan/decisions.json")); DUR = {"A2": 8, "A3": 6}
FULL = {l.split()[1]: l.split()[0] for l in open(f"{W}/round2-plan/round1-hashes.sha256") if l.strip()}
def pair(cid):
    """the frame pair Dan approved: must be listed in decisions.json motion_authorized and match its recorded sha256"""
    assert cid in D["motion_authorized"], f"{cid}: motion is not authorized in decisions.json"
    return [(f"{W}/aiframes/{cid}-{k}.png", FULL[f"aiframes/{cid}-{k}.png"]) for k in ("start", "end")]
def b64(p, h):
    raw = open(p, "rb").read(); assert hashlib.sha256(raw).hexdigest() == h, f"{p} is not the frame Dan approved"
    buf = io.BytesIO(); Image.open(io.BytesIO(raw)).convert("RGB").resize((1920, 1080), Image.LANCZOS).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
def ledger(entry):
    p = f"{M}/ledger.json"; L = json.load(open(p)) if os.path.exists(p) else []
    L.append(entry); json.dump(L, open(p, "w"), indent=1); return round(sum(e["usd"] for e in L), 2)
def call(req):
    for k in range(6):
        try: return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code in (429, 500, 502, 503) or "E005" in body: time.sleep(15*(k+1)); continue
            raise SystemExit(f"HTTP {e.code}: {body}")
    raise SystemExit("gave up after 6 tries")
if __name__ == "__main__":
    cid, tag = sys.argv[1], sys.argv[2]; dur = int(sys.argv[3]) if len(sys.argv) > 3 else DUR[cid]
    out = f"{M}/{tag}.mp4"; assert not os.path.exists(out), f"{out} exists: pick a new tag"
    (s, sh), (e, eh) = pair(cid)
    prompt = open(f"{M}/{cid}.txt").read().strip(); nf = f"{M}/{cid}.neg.txt"; neg = open(nf).read().strip() if os.path.exists(nf) else None
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    body = json.dumps({"input": {"prompt": prompt, "image": b64(s, sh), "last_frame": b64(e, eh), "duration": dur, "resolution": "1080p",
                                 "aspect_ratio": "16:9", "generate_audio": False, **({"negative_prompt": neg} if neg else {})}}).encode()
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers=H))
    print("submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    if p["status"] == "succeeded": urllib.request.urlretrieve(o, out)
    usd = dur*USD_S if p["status"] == "succeeded" else 0.0
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": MODEL, "duration": dur, "usd": usd,
               "prompt": prompt, "negative_prompt": neg, "start": s, "end": e, "when": time.strftime("%F %T")}, open(f"{M}/{tag}.json", "w"), indent=1)
    print(tag, p["status"], p.get("error"), p.get("metrics"), "| spent on motion so far: $", ledger(dict(tag=tag, what=f"{MODEL} {dur}s", usd=usd, id=p["id"], status=p["status"])))
