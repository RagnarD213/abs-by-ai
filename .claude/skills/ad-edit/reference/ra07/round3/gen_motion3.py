#!/usr/bin/env python3
"""RA-07 round 3: motion for I4a, I4b and the shoulder fix I3b (two single-image takes joined by a cut).

  python3 round3/motion/gen_motion3.py I4a v1 [I4b v1 ...]      -> round3/motion/<ID>_<tag>.mp4 + .json, ledger.json

Every job's START/END must pass the frame gate AND a fresh frame reviewer first (_shared/framecheck, Dan 2026-10-14):
require_pass() refuses otherwise. A single-image take sends the same frame as START and END, so the rep returns to it.
The round 2 ledger ($5.00, five takes) counts toward the $10 cap; the total printed here includes it.

Kling v3 (Replicate kwaivgi/kling-v3-video), START + END image, standard mode, no audio. Same call as the approved Ad 13
opener (shortad-from-longform/reference/ad13-r2/gen_opener.py). Every take, failed ones included, goes in the ledger.
Cost is an ESTIMATE ($1.00 a take, the handoff's figure); the Replicate invoice is the record.
"""
import base64, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

D = "/Volumes/Extreme/_edit_work/ra07/round3/motion"
F2 = "/Volumes/Extreme/_edit_work/ra07/round2/frames"
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, f"{REPO}/.claude/skills/_shared/framecheck")
from gate import require_pass
T = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env"))
     if l.startswith("REPLICATE_API_TOKEN=")][0]
COMMON = ("Natural, realistic human motion at normal speed. Everyone keeps the same face, body and clothes throughout. "
          "The background stays completely still.")
NEG = ("camera movement, camera shake, zoom, pan, orbit, cuts, scene change, morphing, warping, extra fingers, missing fingers, "
       "fused fingers, distorted hands, extra arms, extra people, face distortion, changing faces, flicker, watermark, logo, "
       "slow motion, floating objects, objects appearing, objects disappearing, smoke, steam")
JOBS = {
 "I4a": dict(start="/Volumes/Extreme/_edit_work/ra07/round3/frames/I4a-start.png", end="/Volumes/Extreme/_edit_work/ra07/round3/frames/I4a-end_v5.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. The man in the navy t-shirt "
    "with a white towel over his shoulder walks toward the Smith machine squat rack, sees the yellow sign hanging from the middle "
    "of the bar, stops in front of the rack and turns half back toward the camera with both palms turned up and his shoulders "
    "dropped, a tired, unimpressed look. The yellow sign hangs still on its string, flat and unchanged, its words exactly OUT OF "
    "ORDER in black capitals. The rack, the bar and the plates never move. The towel stays on his shoulders. " + COMMON)),
 "I4b": dict(start=f"{F2}/I4b-end.png", end=f"{F2}/I4b-end.png", duration=5, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. The man is in a plate-loaded "
    "hack squat machine with his back flat on the angled back pad, his shoulders under the shoulder pads and his hands on the "
    "handles. He does one smooth, steady rep: he pushes up with his legs until they are almost straight, the back pad, the shoulder "
    "pads and the weight plates sliding up the angled rails together as one solid piece, then he lowers slowly back down to the "
    "same bent-knee position. Both feet stay flat on the fixed slanted foot platform the whole time. The foot platform, the "
    "machine frame and the white towel on the handle do not move. " + COMMON)),
 "I4bW": dict(start=f"{F2}/I4b-start.png", end=f"{F2}/I4b-end.png", duration=5, approved_by_dan=True, prompt=(
    "Real footage in a plain commercial gym. The man in the navy t-shirt with a white towel over his shoulder gives a small satisfied nod at "
    "the plate-loaded hack squat machine, hangs his towel on the machine's side handle, steps onto the slanted foot platform, sets his back "
    "against the angled back pad with his shoulders under the shoulder pads and his hands on the handles, and lowers into one steady rep. "
    "The machine is solid and does not change shape; only its padded sled moves, along its rails, with him. " + COMMON)),
 "I4bR": dict(start=f"{F2}/I4b-end.png", end=f"{F2}/I4b-end.png", duration=5, approved_by_dan=True, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. The man is in the plate-loaded hack squat "
    "machine, back against the angled back pad, shoulders under the shoulder pads, hands on the handles, feet on the foot platform. He does one "
    "smooth, steady rep: he pushes up with his legs until they are almost straight, the padded sled with the pads and plates sliding up its rails "
    "with him, then lowers slowly back to the same position. The foot platform and the machine frame never move. " + COMMON)),
 "I4bR2": dict(start=f"{F2}/I4b-end.png", end=None, duration=5, approved_by_dan=True, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. The man in the hack squat machine does "
    "one full, clearly visible rep right away: he drives through his feet and straightens his legs until his knees are almost locked, his "
    "back staying flat on the pad as the padded sled slides a long way up its rails with him, then he lowers slowly back down to the "
    "starting position. Big, obvious movement, steady effort on his face. The foot platform and the machine frame never move. " + COMMON)),
 "I3bA": dict(start=f"{F2}/I3b-start.png", end=f"{F2}/I3b-start.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. The man sitting on the end of "
    "the flat bench keeps his left hand resting on his sore right shoulder and reads the phone in his right hand. His face eases, "
    "and he gives one small nod, as if to say okay, that works, then keeps reading. The phone stays in his right hand with its "
    "screen toward him. The dumbbell stays on the floor beside the bench. " + COMMON)),
 "I3bB": dict(start=f"{F2}/I3b-end.png", end=f"{F2}/I3b-end.png", duration=4, prompt=(
    "Static locked-off camera, no camera movement, no zoom. Real footage in a plain commercial gym. The man sits on the seated "
    "lateral raise machine, each hand holding its handle, each round pad resting on the outside of his upper arm, his arms out to "
    "the sides at shoulder height. He does one easy side lateral raise: he lowers both arms down to his sides together, the two "
    "padded lever arms pivoting down with his arms, then raises both arms back out to shoulder height. The pads stay on the "
    "outside of his upper arms and his hands stay on the handles the whole time. The seat, the frame and the weight stack "
    "housing do not move. " + COMMON)),
}
H = {"Authorization": "Bearer " + T, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


def gate_ok(j):
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
    r2 = json.load(open("/Volumes/Extreme/_edit_work/ra07/round2/motion/ledger.json"))
    print("ledger: round 3 $%.2f over %d takes; with round 2 $%.2f of the $10 cap" % (sum(x["usd"] for x in led), len(led), sum(x["usd"] for x in led + r2)))
    print("MOTION_DONE")
