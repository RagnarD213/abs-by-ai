#!/usr/bin/env python3
"""RA-07 round 6: motion for O1 (beside the out-of-order leg press, pulls out his phone).

  python3 round6/gen_motion6.py O1 v1 [O1L v2 ...]      -> round6/motion/<ID>_<tag>.mp4 + .json, ledger.json

PH-start.png + PH-end_v1a.png passed the frame gate and a fresh reviewer; Dan approved them 2026-10-17 (round6-plan/decisions.json).
Kling v3 standard, START + END image, no audio. O1 = 4 s, O1L = 5 s. Cost is an ESTIMATE; the Replicate invoice is the record.
Total spend before round 6: $12.00 (cap $20, Dan 2026-10-16).
"""
import base64, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

D = "/Volumes/Extreme/_edit_work/ra07/round6/motion"
F6 = "/Volumes/Extreme/_edit_work/ra07/round6/frames"
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, f"{REPO}/.claude/skills/_shared/framecheck")
from gate import require_pass
T = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env"))
     if l.startswith("REPLICATE_API_TOKEN=")][0]
COMMON = ("Natural, realistic human motion at normal speed. The man keeps the same face, body and clothes throughout. "
          "The background stays completely still.")
NEG = ("phone appearing from nowhere, two phones, bending phone, melting hand, walking, stepping, turning around, camera movement, camera shake, zoom, pan, orbit, cuts, scene change, morphing, warping, extra fingers, missing fingers, "
       "fused fingers, distorted hands, extra arms, extra people, face distortion, changing faces, flicker, watermark, logo, "
       "slow motion, floating objects, objects appearing, objects disappearing, smoke, steam, sliding feet, skating, moonwalk")
JOBS = {
 "O1": dict(start=f"{F6}/PH-start.png", end=f"{F6}/PH-end_v1a.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. A man in a navy t-shirt and grey "
    "shorts with a white towel over his left shoulder stands beside a black plate-loaded leg press, reading the yellow OUT OF ORDER sign "
    "hanging from its backrest. He has already stopped; his feet stay planted and never move. After a brief look at the sign, his right "
    "hand goes into his right shorts pocket, comes out holding a plain black phone, lifts it in front of his chest, and he looks down at "
    "it with a thoughtful look. One phone only, a rigid flat black phone, held in his right hand with five fingers. His left arm hangs "
    "still at his side. He does not walk, turn or lean. The leg press, the yellow sign, the weight plates, the dumbbell racks and the floor "
    "never move. The towel stays on his shoulder. " + COMMON)),
}
JOBS["O1L"] = dict(JOBS["O1"], duration=5)
JOBS["M1"] = dict(start="/Volumes/Extreme/_edit_work/ra07/round6/frames_m1/HC-start.png", end="/Volumes/Extreme/_edit_work/ra07/round6/frames_m1/HC-end.png", duration=4, prompt=(
    "Static locked-off camera on a tripod, no camera movement, no zoom. Real footage in a bright ordinary living room. A man in a black t-shirt and black shorts "
    "stands on the rug facing the camera holding a black hex dumbbell in each hand at his sides. He does one smooth dumbbell curl with his right arm (on the left of the picture): "
    "his upper arm stays against his side and the forearm lifts the dumbbell up to his shoulder; his eyes follow the dumbbell up while his head stays still. His left arm keeps its "
    "dumbbell hanging at his side. Each hand stays wrapped around its handle; exactly two rigid dumbbells. His feet stay planted, he does not walk, turn or lean. The sofa, the throw, "
    "the picture, the lamp, the curtains, the table and the rug never move. " + COMMON))
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
    usd = (1.00 if j["duration"] <= 4 else 1.25) if p["status"] == "succeeded" else 0.0
    rec = {"id": p["id"], "status": p["status"], "error": p.get("error"), "metrics": p.get("metrics"),
           "model": f"kwaivgi/kling-v3-video {mode}", "duration": j["duration"], "usd": usd,
           "usd_note": "ESTIMATE ($1.00 per 4 s take, $1.25 per 5 s); the Replicate invoice is the record",
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
    print("ledger: round 6 $%.2f over %d takes; with the $12.00 spent before round 6 the total is $%.2f of the $20 cap" % (sum(x["usd"] for x in led), len(led), 12 + sum(x["usd"] for x in led)))
    print("MOTION_DONE")
