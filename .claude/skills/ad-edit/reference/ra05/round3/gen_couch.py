"""RA-05 round 3: the couch clip as TWO takes joined by a cut (Dan approved the START and END frames 2026-10-14,
round3-plan/decisions.json). Veo 3.1 Fast on Replicate, image only (no last_frame), 9:16, no audio.
usage: gen_couch.py <A|B> <tag> [seconds]   prompt: motion/<A|B>.txt (+ <A|B>.neg.txt)
Writes motion/<tag>.mp4 + <tag>.json, appends the cost to motion/ledger.json. Never overwrites a take."""
import base64, hashlib, io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ra05"; M = f"{W}/round3/motion"; MODEL = "google/veo-3.1-fast"; USD_S = 0.10
D = json.load(open(f"{W}/round3-plan/decisions.json"))
it = next(i for i in D["items"] if i["id"] == "COUCH"); assert it["motion_authorized"]
FR = {"A": "round2/frames/couch_START.png", "B": "round2/frames/couch_END.png"}
CAP = 10.0
def b64(rel):
    raw = open(f"{W}/{rel}", "rb").read(); assert hashlib.sha256(raw).hexdigest() == it["files"][rel], f"{rel} is not the frame Dan approved"
    im = Image.open(io.BytesIO(raw)).convert("RGB"); sw, sh = im.size; tw = round(sh * 9 / 16)
    im = im.crop(((sw - tw) // 2, 0, (sw - tw) // 2 + tw, sh)).resize((1080, 1920), Image.LANCZOS)   # centre 9:16 window, like the placeholder
    buf = io.BytesIO(); im.save(buf, "PNG"); return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
def spent():
    p = f"{M}/ledger.json"; return round(sum(e["usd"] for e in json.load(open(p))), 2) if os.path.exists(p) else 0.0
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
    sid, tag = sys.argv[1], sys.argv[2]; dur = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    assert spent() + dur*USD_S <= CAP, f"budget: ${spent()} spent of ${CAP}; ask Dan before passing it"
    out = f"{M}/{tag}.mp4"; assert not os.path.exists(out), f"{out} exists: pick a new tag"
    prompt = open(f"{M}/{sid}.txt").read().strip(); nf = f"{M}/{sid}.neg.txt"; neg = open(nf).read().strip() if os.path.exists(nf) else None
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    body = json.dumps({"input": {"prompt": prompt, "image": b64(FR[sid]), "duration": dur, "resolution": "1080p",
                                 "aspect_ratio": "9:16", "generate_audio": False, **({"negative_prompt": neg} if neg else {})}}).encode()
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers=H))
    print("submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    if p["status"] == "succeeded": urllib.request.urlretrieve(o, out)
    usd = dur*USD_S if p["status"] == "succeeded" else 0.0
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": MODEL, "duration": dur, "usd": usd,
               "prompt": prompt, "negative_prompt": neg, "frame": FR[sid], "when": time.strftime("%F %T")}, open(f"{M}/{tag}.json", "w"), indent=1)
    print(tag, p["status"], p.get("error"), "| spent on motion so far: $", ledger(dict(tag=tag, what=f"{MODEL} {dur}s", usd=usd, id=p["id"], status=p["status"])))
