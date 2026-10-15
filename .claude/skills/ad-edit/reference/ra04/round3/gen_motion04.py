"""RA-04 round 3: AI motion for AI1-1..AI1-3 from Dan's approved frame pairs (round3-plan/decisions.json), Veo 3.1 Fast on Replicate
(image + last_frame, 9:16, 1080p, no audio). The 941x1672 frames are scaled to 1080x1920 first. Adapted from ro06/gen_motion.py.
usage: gen_motion04.py <AI1-1|AI1-2|AI1-3> <tag> [seconds]   prompt: round3/motion/<ID>.txt (+ <ID>.neg.txt)
Writes round3/motion/<tag>.mp4 + <tag>.json and appends the cost to round3/motion/ledger.json. Never overwrites a take.
Refuses to start when the ledger would pass the ad's budget (decisions.json budget_usd)."""
import base64, hashlib, io, json, os, sys, time, urllib.request, urllib.error, fcntl
from PIL import Image
W = "/Volumes/Extreme/_edit_work/ra04"; M = f"{W}/round3/motion"; MODEL = "google/veo-3.1-fast"; USD_S = 0.10
D = json.load(open(f"{W}/round3-plan/decisions.json"))
PAIRS = {"AI1-1": ("S1_a", "F2_a"), "AI1-2": ("F2_a", "F3b_a"), "AI1-3": ("F4h", "F5p"),
         "AI1-12": ("S1_a", "F3b_a")}   # round 3 retry: shots 1+2 as ONE take (the two-take join jumped: independent review 1)
SHA = {"S1_a": "0fb43996d74b3b4f3765081d5522e05ba9eca36c0d1b5b3b47a57a51646491da", "F2_a": "157edd1096409c066c96312093de036b79095a9d170e80cf5d5de49cb2ad4780",
       "F3b_a": "802a4c9e7014614ca85b8bda6a7e7e7265c45fb5953731146e133dd9bbbe6c0f", "F4h": "f49c75616613b51a49fd65aa8916a21be5a12f0af7bee52c6718350918278a8d",
       "F5p": "4e8095cfec446bdd192c1f0f12fd46be84a32dfa8f3b254cbf62e934145b0d07"}
def pair(cid):
    parts = ["AI1-1", "AI1-2"] if cid == "AI1-12" else [cid]   # the one-take retry spans two authorized pairs and their approved frames
    for c in parts: assert any(a.startswith(c + " ") for a in D["motion_authorized"]), f"{c} is not motion-authorized"
    approved = {h for it in D["items"] if it.get("verdict") == "approved" for h in it.get("sha256", [])}
    out = []
    for f in PAIRS[cid]:
        assert SHA[f] in approved, f"{f} is not an approved frame in decisions.json"
        out.append((f"{W}/round2/frames/{f}.png", SHA[f]))
    return out
def b64(p, h):
    raw = open(p, "rb").read(); assert hashlib.sha256(raw).hexdigest() == h, f"{p} is not the frame Dan approved"
    buf = io.BytesIO(); Image.open(io.BytesIO(raw)).convert("RGB").resize((1080, 1920), Image.LANCZOS).save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
def ledger(entry=None):
    p = f"{M}/ledger.json"
    with open(f"{M}/.ledger.lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        L = json.load(open(p)) if os.path.exists(p) else []
        if entry: L.append(entry); json.dump(L, open(p, "w"), indent=1)
        return round(sum(e["usd"] for e in L), 2)
def call(req):
    for k in range(6):
        try: return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:300]
            if e.code in (429, 500, 502, 503) or "E005" in body: time.sleep(15*(k+1)); continue
            raise SystemExit(f"HTTP {e.code}: {body}")
    raise SystemExit("gave up after 6 tries")
if __name__ == "__main__":
    cid, tag = sys.argv[1], sys.argv[2]; dur = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    out = f"{M}/{tag}.mp4"; assert not os.path.exists(out), f"{out} exists: pick a new tag"
    spent = ledger(); assert spent + dur*USD_S <= D["budget_usd"], f"budget: ${spent} spent of ${D['budget_usd']}; ask Dan first"
    (s, sh), (e, eh) = pair(cid)
    prompt = open(f"{M}/{cid}.txt").read().strip(); nf = f"{M}/{cid}.neg.txt"; neg = open(nf).read().strip() if os.path.exists(nf) else None
    token = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env")) if l.startswith("REPLICATE_API_TOKEN=")][0]
    H = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    body = json.dumps({"input": {"prompt": prompt, "image": b64(s, sh), "last_frame": b64(e, eh), "duration": dur, "resolution": "1080p",
                                 "aspect_ratio": "9:16", "generate_audio": False, **({"negative_prompt": neg} if neg else {})}}).encode()
    p = call(urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body, headers=H))
    print("submitted", p["id"], flush=True)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(8); p = call(urllib.request.Request(p["urls"]["get"], headers=H))
    o = p.get("output"); o = o[0] if isinstance(o, list) else o
    if p["status"] == "succeeded": urllib.request.urlretrieve(o, out)
    usd = dur*USD_S if p["status"] == "succeeded" else 0.0
    json.dump({"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"), "model": MODEL, "duration": dur, "usd": usd,
               "prompt": prompt, "negative_prompt": neg, "start": s, "end": e, "when": time.strftime("%F %T")}, open(f"{M}/{tag}.json", "w"), indent=1)
    print(tag, p["status"], p.get("error"), "| spent on motion so far: $", ledger(dict(tag=tag, what=f"{MODEL} {dur}s", usd=usd, id=p["id"], status=p["status"])))
