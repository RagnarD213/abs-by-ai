#!/usr/bin/env python3
"""RA-07 round 5: motion for G1 (gym closed) and O1 (leg press out of order).

  python3 round5/gen_motion5.py G1 v1 [O1 v1 ...]      -> round5/motion/<ID>_<tag>.mp4 + .json, ledger.json

Both START/END pairs passed the frame gate and a fresh frame reviewer in round 4 (require_pass refuses otherwise).
Kling v3 standard, START + END image, no audio. Cost is an ESTIMATE ($1.00 a take); the Replicate invoice is the record.
Total spend before round 5: $10.00 (cap $20, Dan 2026-10-16); round 4 spent $0.
"""
import base64, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

D = "/Volumes/Extreme/_edit_work/ra07/round5/motion"
F4 = "/Volumes/Extreme/_edit_work/ra07/round4/frames"
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, f"{REPO}/.claude/skills/_shared/framecheck")
from gate import require_pass
T = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env"))
     if l.startswith("REPLICATE_API_TOKEN=")][0]
COMMON = ("Natural, realistic human motion at normal speed. The man keeps the same face, body and clothes throughout. "
          "The background stays completely still.")
NEG = ("camera movement, camera shake, zoom, pan, orbit, cuts, scene change, morphing, warping, extra fingers, missing fingers, "
       "fused fingers, distorted hands, extra arms, extra people, face distortion, changing faces, flicker, watermark, logo, "
       "slow motion, floating objects, objects appearing, objects disappearing, smoke, steam, sliding feet, skating, moonwalk")
JOBS = {
 "G1": dict(start=f"{F4}/GC-start_v2.png", end=f"{F4}/GC-end_v3.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage on a city sidewalk in daylight. A man in a black t-shirt, "
    "black shorts and grey running shoes walks along the sidewalk toward the black-framed glass door of a gym, his eyes on the red "
    "and white CLOSED sign hanging on the glass. He takes one last short step, his heel lands and his foot plants flat on the "
    "pavement, and he stops. Then he lets his arms open out from his sides, both hands turned palm up and empty at waist height, "
    "his shoulders drop and he tilts his head in a tired, resigned look at the sign. Each foot lands flat and stays planted, never "
    "sliding on the pavement. The door, the CLOSED sign hanging still on its string, the building and the dark gym interior never move. " + COMMON)),
 "O1": dict(start=f"{F4}/LP-start_v1.png", end=f"{F4}/LP-end_v4b.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. Seen from behind and slightly "
    "from the side, a man in a navy t-shirt and grey shorts with a white towel folded over his left shoulder walks toward the plate-loaded "
    "leg press, his head turned toward the yellow OUT OF ORDER sign hanging on its string from the backrest. He takes one last short step, "
    "his foot lands flat on the rubber floor and he stops. Then he glances back over his right shoulder toward the camera with a tired look "
    "and his shoulders lift in one small shrug. His hips and legs stay turned away from the camera, only his head turns. Each foot lands flat "
    "and stays planted, never sliding on the floor. The leg press, the yellow sign, the weight plates, the dumbbell rack and the floor never move. "
    "The towel stays on his shoulder. " + COMMON)),
}
H = {"Authorization": "Bearer " + T, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


def gate_ok(j):
    require_pass(j["start"], j["end"]); return
    # Dan approved the I4b frames in round 2 ("That looks good", motion authorized) before the frame gate existed; the gate's reviewer
    # later failed the END on machine geometry. Dan's approval stands for the frames; the TAKE is judged at playback speed (three questions).
    if not j.get("approved_by_dan"): require_pass(j["start"], j["end"] or j["start"])


def run(jid, tag, mode="standard"):
    j = JOBS[jid]
    gate_ok(j)
    body = json.dumps({"input": {"prompt": j["prompt"], "negative_prompt": NEG, "start_image": b64(j["start"]),
                                 **({"end_image": b64(j["end"])} if j["end"] else {}), "duration": j["duration"], "mode": mode,
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
    for jid, _ in pairs: gate_ok(JOBS[jid])      # refuse the whole batch before spending
    with ThreadPoolExecutor(len(pairs)) as ex:
        res = list(ex.map(lambda x: run(*x), pairs))
    lp = f"{D}/ledger.json"
    led = json.load(open(lp)) if os.path.exists(lp) else []
    led += res
    json.dump(led, open(lp, "w"), indent=1)
    print("ledger: round 5 $%.2f over %d takes; with the $10.00 spent before round 5 the total is $%.2f of the $20 cap" % (sum(x["usd"] for x in led), len(led), 10 + sum(x["usd"] for x in led)))
    print("MOTION_DONE")
