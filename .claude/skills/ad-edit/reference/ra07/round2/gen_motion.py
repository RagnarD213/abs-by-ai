#!/usr/bin/env python3
"""RA-07 round 2: motion for the AI clips Dan approved on frames (decisions.json motion_authorized: I2, I3a, I5).

  python3 gen_motion.py I2 v1 [I3a v1 ...]      -> round2/motion/<ID>_<tag>.mp4 + .json, ledger.json

Kling v3 (Replicate kwaivgi/kling-v3-video), START + END image, standard mode, no audio. Same call as the approved Ad 13
opener (shortad-from-longform/reference/ad13-r2/gen_opener.py). Every take, failed ones included, goes in the ledger.
Cost is an ESTIMATE ($1.00 a take, the handoff's figure); the Replicate invoice is the record.
"""
import base64, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

D = "/Volumes/Extreme/_edit_work/ra07/round2/motion"
F1 = "/Volumes/Extreme/_edit_work/ra07/round1/frames"
T = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env"))
     if l.startswith("REPLICATE_API_TOKEN=")][0]
COMMON = ("Natural, realistic human motion at normal speed. Everyone keeps the same face, body and clothes throughout. "
          "The background stays completely still.")
NEG = ("camera movement, camera shake, zoom, pan, orbit, cuts, scene change, morphing, warping, extra fingers, missing fingers, "
       "fused fingers, distorted hands, extra arms, extra people, face distortion, changing faces, flicker, watermark, logo, "
       "slow motion, floating objects, objects appearing, objects disappearing, smoke, steam")
JOBS = {
 "I2": dict(start=f"{F1}/I2-start.png", end=f"{F1}/I2-end.png", duration=5, prompt=(
    # v3 (take 1: the white stack turned into a black binder; take 2: a second trainer appeared behind the clients)
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. Exactly four people in the "
    "whole clip: one trainer and three clients. Nobody else ever appears. The one personal trainer in the black polo, on the left, "
    "hands one loose white sheet of paper to the skinny young man in the grey t-shirt, then turns around and walks straight away "
    "from the camera toward the back of the gym on the LEFT side of the frame, holding the rest of the loose white sheets in his "
    "hand. He never passes behind the clients. Meanwhile the heavy-set man in the green t-shirt leans over to look at the young "
    "man's sheet and holds his own sheet up beside it, and the small older woman in the lilac tracksuit looks from her sheet to "
    "theirs: all three sheets are identical, and they glance at each other, puzzled. The sheets stay flat, solid white paper. "
    + COMMON)),
 "I3a": dict(start=f"{F1}/I3-start.png", end=f"{F1}/I3-end.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. The man sitting on the flat "
    "bench finishes pressing the dumbbell overhead with his right arm, then feels a sharp twinge in his shoulder: he winces and "
    "slowly lowers the dumbbell with his right hand all the way down until it rests on his right thigh at the bottom of the "
    "frame, and grips the top of his right shoulder with his left hand, eyes narrowed. The dumbbell stays solid and stays in "
    "his hand the whole way down. " + COMMON)),
 "I5": dict(start=f"{F1}/I5-start.png", end=f"{F1}/I5-end.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a gym hallway. The sweaty man knocks twice on the "
    "closed grey office door with his right hand, waits, reads the paper sign taped to the door, then turns to face the camera "
    "and shrugs, lost, with his right palm raised and his eyebrows up, the water bottle still in his left hand. The door stays "
    "closed. The paper sign stays taped flat to the door and unchanged, its words exactly BACK NEXT WEEK. " + COMMON)),
}
H = {"Authorization": "Bearer " + T, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


def run(jid, tag, mode="standard"):
    j = JOBS[jid]
    body = json.dumps({"input": {"prompt": j["prompt"], "negative_prompt": NEG, "start_image": b64(j["start"]),
                                 "end_image": b64(j["end"]), "duration": j["duration"], "mode": mode,
                                 "generate_audio": False}}).encode()
    p = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://api.replicate.com/v1/models/kwaivgi/kling-v3-video/predictions", data=body, headers=H)))
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(10)
        p = json.load(urllib.request.urlopen(urllib.request.Request(p["urls"]["get"], headers=H)))
    out = p.get("output"); out = out[0] if isinstance(out, list) else out
    name = f"{jid}_{tag}"
    if p["status"] == "succeeded":
        urllib.request.urlretrieve(out, f"{D}/{name}.mp4")
    usd = 1.00 if p["status"] == "succeeded" else 0.0
    rec = {"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"),
           "model": f"kwaivgi/kling-v3-video {mode}", "duration": j["duration"], "usd": usd,
           "usd_note": "ESTIMATE ($1.00 a take, handoff figure); the Replicate invoice is the record",
           "prompt": j["prompt"], "negative": NEG, "start": j["start"], "end": j["end"], "when": time.strftime("%F %T")}
    json.dump(rec, open(f"{D}/{name}.json", "w"), indent=1)
    print(name, p["status"], p.get("error"), flush=True)
    return dict(tag=name, item=jid, what=f"kling-v3 {mode} {j['duration']}s", usd=usd, id=p["id"], status=p["status"])


if __name__ == "__main__":
    a = sys.argv[1:]
    pairs = list(zip(a[0::2], a[1::2]))
    with ThreadPoolExecutor(len(pairs)) as ex:
        res = list(ex.map(lambda x: run(*x), pairs))
    lp = f"{D}/ledger.json"
    led = json.load(open(lp)) if os.path.exists(lp) else []
    led += res
    json.dump(led, open(lp, "w"), indent=1)
    print("ledger total $%.2f over %d takes" % (sum(x["usd"] for x in led), len(led)))
    print("MOTION_DONE")
