"""RA-15 round 2: AI motion for I2 (fridge), I4 (restaurant), I5 (cardboard cutout) from the frame pairs Dan approved on 2026-10-14
(round2-plan/decisions.json: motion_authorized true, frame sha256 recorded per item). Veo 3.1 Fast on Replicate, 9:16, 1080p, no audio,
$0.10 a second. The 941x1672 frames are scaled to 1080x1920 first. Ad cap $10 for the whole ad, retries included (refuses past it).
usage: gen_motion15.py <I2|I4|I5> <tag> <seconds 4|6|8> [pair|start]     prompt: round2/motion/<tag or ID>.txt (+ .neg.txt)
       gen_motion15.py ledger
Writes round2/motion/<tag>.mp4 + <tag>.json and appends to round2/motion/ledger.json. Never overwrites a take."""
import base64, hashlib, io, json, os, re, sys, time, urllib.request, urllib.error
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ra15"; M = f"{W}/round2/motion"; MODEL = "google/veo-3.1-fast"; USD_S = 0.10; CAP = 10.0
D = json.load(open(f"{W}/round2-plan/decisions.json")); IT = {i["id"]: i for i in D["items"]}
def frames(cid):
    it = IT[cid]; assert it.get("motion_authorized") is True, f"{cid}: motion is not authorized in decisions.json"
    return [(f"{W}/round1/frames/{cid}-{k}.png", it["files"][f"round1/frames/{cid}-{k}.png"]) for k in ("start", "end")]
def b64(p, h16):
    raw = open(p, "rb").read(); assert hashlib.sha256(raw).hexdigest()[:16] == h16, f"{p} is not the frame Dan approved"
    buf = io.BytesIO(); Image.open(io.BytesIO(raw)).convert("RGB").resize((1080, 1920), Image.LANCZOS).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
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
            if e.code in (429, 500, 502, 503) or "E005" in body: time.sleep(15 * (k + 1)); continue
            raise SystemExit(f"HTTP {e.code}: {body}")
    raise SystemExit("gave up after 6 tries")
if __name__ == "__main__":
    if sys.argv[1] == "ledger": print("spent on motion: $", spent()); sys.exit()
    cid, tag, dur = sys.argv[1], sys.argv[2], int(sys.argv[3]); mode = sys.argv[4] if len(sys.argv) > 4 else "pair"
    assert spent() + dur * USD_S <= CAP + 1e-9, f"this take would pass the ${CAP} ad cap (spent ${spent()}): ask Dan first"
    out = f"{M}/{tag}.mp4"; assert not os.path.exists(out), f"{out} exists: pick a new tag"
    base = re.sub(r"_v\d+$", "", tag); pf = next(p for p in (f"{M}/{tag}.txt", f"{M}/{base}.txt", f"{M}/{cid}.txt") if os.path.exists(p))
    prompt = open(pf).read().strip(); nf = pf[:-4] + ".neg.txt"; neg = open(nf).read().strip() if os.path.exists(nf) else None
    (s, sh), (e, eh) = frames(cid)
    inp = {"prompt": prompt, "duration": dur, "resolution": "1080p", "aspect_ratio": "9:16", "generate_audio": False, "image": b64(s, sh)}
    if mode == "pair": inp["last_frame"] = b64(e, eh)
    if neg: inp["negative_prompt"] = neg
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=json.dumps({"input": inp}).encode(), headers=H))
    print("submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    if p["status"] == "succeeded": urllib.request.urlretrieve(o, out)
    usd = dur * USD_S if p["status"] == "succeeded" else 0.0
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": MODEL, "duration": dur, "usd": usd, "mode": mode,
               "prompt": prompt, "negative_prompt": neg, "start": s, "end": e, "when": time.strftime("%F %T")}, open(f"{M}/{tag}.json", "w"), indent=1)
    print(tag, p["status"], p.get("error"), "| spent on motion so far: $", ledger(dict(tag=tag, clip=cid, what=f"{MODEL} {dur}s", usd=usd, id=p["id"], status=p["status"])))
