"""RO-08 round 2: AI motion from Dan's approved frames (round2-plan/decisions.json; hashes in round2-plan/round2-start-hashes.sha256),
Veo 3.1 Fast on Replicate (image + last_frame, 1080p, no audio, $0.10 a second). The 1672x941 frames are scaled to 1920x1080 first.
A take is named by its clip key: A1..A8, O6 (the split screen opener) and OTa..OTd (the four moves of the time-lapse opener, key frames
OT-1 -> OT-2 -> OT-3-r2 -> OT-4 -> OT-5). Safe to run several at once: each take writes its own <tag>.json and the ledger is the sum of those.
usage: gen_motion08.py <key> <tag> [seconds]      prompt: round2/motion/<key>.txt (+ <key>.neg.txt); PROMPT=<name> uses another prompt file;
NOLAST=1 sends the START frame only (the no-lip-sync fallback).   gen_motion08.py ledger   prints the total spent."""
import base64, glob, hashlib, io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ro08"; M = f"{W}/round2/motion"; MODEL = "google/veo-3.1-fast"; USD_S = 0.10; CAP = 15.0
D = json.load(open(f"{W}/round2-plan/decisions.json"))
FR = {**{f"A{i}": (f"A{i}-start", f"A{i}-end") for i in range(1, 9)}, "A6": ("A6-start", "A6-end-r2"), "O6": ("O6-start-r3", "O6-end-r3"),
      "OTa": ("OT-1", "OT-2"), "OTb": ("OT-2", "OT-3-r2"), "OTc": ("OT-3-r2", "OT-4"), "OTd": ("OT-4", "OT-5")}
DUR = {"A1": 6, "A2": 8, "A3": 6, "A4": 6, "A5": 6, "A6": 8, "A7": 6, "A8": 8, "O6": 8, "OTa": 4, "OTb": 4, "OTc": 4, "OTd": 6}
FULL = {l.split(None, 1)[1].strip(): l.split()[0] for l in open(f"{W}/round2-plan/round2-start-hashes.sha256") if l.strip()}
def pair(key):
    """the frames Dan approved: the clip must be in decisions.json motion_authorized and each frame must match its recorded sha256"""
    auth = "OT" if key.startswith("OT") else key
    assert auth in D["motion_authorized"], f"{key}: motion is not authorized in decisions.json"
    return [(f"{W}/aiframes/{n}.png", FULL[f"aiframes/{n}.png"]) for n in FR[key]]
def b64(p, h):
    raw = open(p, "rb").read(); assert hashlib.sha256(raw).hexdigest() == h, f"{p} is not the frame Dan approved"
    buf = io.BytesIO(); Image.open(io.BytesIO(raw)).convert("RGB").resize((1920, 1080), Image.LANCZOS).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
def spent():
    tot = 0.0; rows = []
    for p in sorted(glob.glob(f"{M}/*.json")):
        if os.path.basename(p) == "ledger.json": continue
        j = json.load(open(p)); rows.append(dict(tag=os.path.basename(p)[:-5], what=f"{j.get('model')} {j.get('duration', j.get('seconds'))}s", usd=j.get("usd", 0.0), id=j.get("id"), status=j.get("status"), when=j.get("when")))
        tot += j.get("usd", 0.0)
    json.dump(dict(cap_usd=CAP, total_usd=round(tot, 3), takes=rows), open(f"{M}/ledger.json", "w"), indent=1); return round(tot, 3)
def call(req):
    for k in range(6):
        try: return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code in (429, 500, 502, 503) or "E005" in body: time.sleep(15*(k+1)); continue
            raise SystemExit(f"HTTP {e.code}: {body}")
        except (urllib.error.URLError, TimeoutError): time.sleep(10*(k+1))
    raise SystemExit("gave up after 6 tries")
def token(): return [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
if __name__ == "__main__":
    if sys.argv[1] == "ledger": print("spent on AI motion and lip sync so far: $", spent(), "of $", CAP); sys.exit()
    key, tag = sys.argv[1], sys.argv[2]; dur = int(sys.argv[3]) if len(sys.argv) > 3 else DUR[key]
    out = f"{M}/{tag}.mp4"; assert not os.path.exists(out) and not os.path.exists(f"{M}/{tag}.json"), f"{tag} exists: pick a new tag"
    assert spent() + dur*USD_S <= CAP, f"this take would pass the ${CAP} cap Dan set"
    (s, sh), (e, eh) = pair(key)
    pn = os.environ.get("PROMPT", key); prompt = open(f"{M}/{pn}.txt").read().strip(); nf = f"{M}/{pn}.neg.txt"; neg = open(nf).read().strip() if os.path.exists(nf) else None
    H = {"Authorization": "Bearer " + token(), "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    body = json.dumps({"input": {"prompt": prompt, "image": b64(s, sh), **({} if os.environ.get("NOLAST") else {"last_frame": b64(e, eh)}), "duration": dur, "resolution": "1080p",
                                 "aspect_ratio": "16:9", "generate_audio": False, **({"negative_prompt": neg} if neg else {})}}).encode()
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers=H))
    print(tag, "submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    if p["status"] == "succeeded": urllib.request.urlretrieve(o, out)
    usd = dur*USD_S if p["status"] == "succeeded" else 0.0
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": MODEL, "duration": dur, "usd": usd, "key": key,
               "prompt": prompt, "negative_prompt": neg, "start": s, "end": None if os.environ.get("NOLAST") else e, "when": time.strftime("%F %T")}, open(f"{M}/{tag}.json", "w"), indent=1)
    print(tag, p["status"], p.get("error"), p.get("metrics"), "| spent so far: $", spent(), flush=True)
