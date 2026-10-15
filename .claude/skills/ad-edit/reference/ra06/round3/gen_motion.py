#!/usr/bin/env python3
"""RA-06 round 3: motion for the AI clips Dan approved on frames (round3-plan/decisions.json motion_authorized: I1, I3, I4).

  python3 gen_motion.py I1 v1 [I3 v1 ...]      -> round3/motion/<ID>_<tag>.mp4 + .json, ledger.json

Kling v3 (Replicate kwaivgi/kling-v3-video), START + END image, standard mode, no audio: the call RA-07 round 2 used.
Every take, failed ones included, goes in the ledger. Cost is an ESTIMATE ($1.00 a take); the Replicate invoice is the record.
Frames are re-hashed against round2/frames/HASHES.txt before any call.
"""
import base64, hashlib, json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

D = "/Volumes/Extreme/_edit_work/ra06/round3/motion"
F = "/Volumes/Extreme/_edit_work/ra06/round2/frames"
T = [l.split("=", 1)[1].strip().strip("\"'") for l in open(os.path.expanduser("~/.absbyai-secrets.env"))
     if l.startswith("REPLICATE_API_TOKEN=")][0]
COMMON = ("Natural, realistic human motion at normal speed. Everyone keeps the same face, body and clothes throughout. "
          "The background stays completely still.")
NEG = ("camera movement, camera shake, zoom, pan, orbit, cuts, scene change, morphing, warping, extra fingers, missing fingers, "
       "fused fingers, distorted hands, extra arms, extra people, face distortion, changing faces, flicker, watermark, logo, "
       "text, letters, numbers, slow motion, floating objects, objects appearing, objects disappearing, smoke, steam")
HASH = {"I1": ("6ff2a15af054ec6b", "86346750b48a17e5"), "I3": ("007f091edf75e32d", "4cb5bee5f1850ac3"),
        "I4": ("83a3e87dc69cec66", "c1112686f9f54468")}
PROMPTS_V1 = None  # v1 prompts kept in motion/<ID>_v1.json
PROMPTS = {
 # v3/v4 (v1, v2 failed the same way: after the teenager's hand-off, the other two men's sheets appeared in their hands)
 "I1": (5, "Static locked-off camera, no camera movement, no zoom. Real footage at the front desk of a plain commercial gym. "
    "Exactly four people in the whole clip: one trainer in a navy polo shirt at the photocopier and three waiting men. Nobody "
    "else ever appears. Without looking up, the trainer picks up three loose white sheets from the top of the stack, fans them "
    "out in his left hand and holds them out sideways toward the three men. All three men step in together and reach for the "
    "fan at the same moment, and each pulls one sheet out of the trainer's hand: the skinny teenager in the black hoodie, the "
    "heavyset man in the grey t-shirt and the grey-haired man with the black knee brace. The trainer's hand is empty afterwards. "
    "The men step back and hold their sheets at chest height; the teenager and the heavyset man compare them: identical. Each "
    "man holds exactly one sheet, and every sheet came out of the trainer's hand in plain view. The sheets are thin, flat, "
    "loose white paper. The stack stays on the copier. " + COMMON),
 "I3": (5, "Static locked-off camera, no camera movement, no zoom. Real footage in a plain gym. The man stands still and "
    "relaxed, facing the camera, arms at his sides, breathing naturally, feet planted; he does not walk or turn. A thin soft "
    "blue horizontal line of light moves slowly and steadily down from just above his head to his knees over the whole clip, "
    "staying level. As the line passes each part of his body, faint thin blue outline shapes appear exactly there and then "
    "stay fixed on his body: around his shoulders, upper arms, chest, midsection and thighs, and a faint grid of small blue "
    "dots on his t-shirt. Once drawn, the outlines never move, crawl, wobble or change shape. Nothing appears below the line. "
    "No text, numbers or labels anywhere. " + COMMON),
 "I4": (4, "Static locked-off camera, no camera movement, no zoom. Real footage in a brick-wall gym. Exactly two characters "
    "in the whole clip: the bald bearded trainer in the black t-shirt and the silver humanoid robot. The trainer holds his "
    "cardboard box against his body with his left arm the whole time. With his right hand he pushes the push bar of the glass "
    "exit door: the door swings wide open outward and STAYS open, and he walks forward out through the open doorway, glancing "
    "back once over his shoulder. He never steps back and the door never closes while he is in it. Meanwhile the robot lifts "
    "the small white towel high above its head and waves it side to side in a cheerful goodbye. Everything in the box stays "
    "in the box. " + COMMON),
}
H = {"Authorization": "Bearer " + T, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}


def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


def sha16(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


def run(jid, tag, mode="standard"):
    dur, prompt = PROMPTS[jid]
    st, en = f"{F}/{jid}-start.png", f"{F}/{jid}-end.png"
    assert (sha16(st), sha16(en)) == HASH[jid], f"{jid}: frames differ from the approved hashes"
    body = json.dumps({"input": {"prompt": prompt, "negative_prompt": NEG, "start_image": b64(st), "end_image": b64(en),
                                 "duration": dur, "mode": mode, "aspect_ratio": "9:16", "generate_audio": False}}).encode()
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
           "model": f"kwaivgi/kling-v3-video {mode}", "duration": dur, "usd": usd,
           "usd_note": "ESTIMATE ($1.00 a take); the Replicate invoice is the record",
           "prompt": prompt, "negative": NEG, "start": st, "end": en, "frames_sha16": HASH[jid], "when": time.strftime("%F %T")}
    json.dump(rec, open(f"{D}/{name}.json", "w"), indent=1)
    print(name, p["status"], p.get("error"), flush=True)
    return dict(tag=name, item=jid, what=f"kling-v3 {mode} {dur}s", usd=usd, id=p["id"], status=p["status"])


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
