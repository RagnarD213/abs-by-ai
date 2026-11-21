"""RO-20C round 6 (2026-10-20): video 3 rebuilt from the round 4 build with Dan's round 5 changes, round 4 left untouched.

  1. the intro (pickup P4, 0:00 to 0:06.9): the levels-split graphic over three AI clips (p4_r6.py -> round6/pickups/P4.mp4);
     the P4 voice is the locked one (round6/pickups/P4.voice.wav is a link to round3/pickups/P4.voice.wav)
  2. 1:47.4 and 4:12.3: the two lip-synced excuse clips (E1 hot dog guy, E2 pizza couch guy) as clip items over the presenter.
Everything else is films_r4 exactly (all its in-memory fixes run on import). Parts that do not change are links to the round 4 parts;
part 03 (film 43483..64194, both excuse clips) is spliced by splice_r6.py, which re-renders only the windows around them.

  films_r6.py seed      link the unchanged round 4 parts into round6/v3/parts (never part 00 or 03)
  films_r6.py picture   films_r4.picture("v3") into round6/v3 (renders nothing that is already there)
  films_r6.py audio     films_r4.audio("v3") into round6/v3 (same voice, bed and finish as round 4)"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import films_r4 as F
Bd = F.Bd; FPS = F.FPS
R6 = f"{F.W}/round6"
F.OUT = R6
F.PK = f"{R6}/pickups"
LS = f"{R6}/lipsync"
NEW = [dict(id="E1", kind="clip", start="I can't afford healthy food, Dan", end="there's nothing I can do", tail=0.0,
            src=[f"{R6}/veo/E1c-api-t1.mp4@0.25"], label="AI-GENERATED", people="other", physique=False,
            note="EXCUSE VOICE (round 5 request): overweight man at a table of hot dogs, fries and junk food. Its lip sync (E1-sync1) measured r 0.19 (real footage 0.3 to 0.5) and failed, so per VIDEO-RULES 2026-10-12 this is a mouth-closed take: he pouts and shrugs while Dan's voice does the line E1c frames 6 to 115, closed-mouth throughout (reviewed PASS); both full-length mouth-closed takes groaned mid-line, so the clip covers \"I can't afford ... eat healthy,\" and the film cuts back to Dan for \"but I can't, so there's nothing I can do\"",
            t0=45273/FPS, t1=45410/FPS),
       dict(id="E2", kind="clip", start="Oh, Dan, I don't have the money", end="on salmon every week", tail=0.0,
            src=[f"{LS}/E2-sync1-beardfix.mp4@0.75"], label="AI-GENERATED", people="other", physique=False,
            note="EXCUSE VOICE (round 5 request): a different man on a couch behind pizza, fried chicken and junk food, lips synced to Dan's own line (sync/lipsync-2-pro, with the take's sharp beard put back outside the lips by beardfix_r6.py). Only the reviewed stretch is used: Dan says \"Oh,\" on camera, this clip plays \"Dan, I don't have the money for $30 a pound\", then Dan on camera for \"on salmon every week\". Two mouth-closed retakes (E2c, E2d) failed review",
            t0=49638/FPS, t1=49703/FPS)]
if os.environ.get("R6_LIPSYNC"):                       # a fallback take (mouth closed) or a retake: E1=path,E2=path
    for kv in os.environ["R6_LIPSYNC"].split(","):
        k, v = kv.split("="); next(i for i in NEW if i["id"] == k)["src"] = [f"{v}@0.0"]
Bd.R[:] = sorted([i for i in Bd.R if i["id"] not in ("E1", "E2")] + NEW, key=lambda i: i["t0"])
DIRTY = [(45273 - 30, 45470 + 30), (49616 - 30, 49748 + 30)]      # film frames whose picture changes (with a second of margin)


def seed():
    src, dst = f"{F.W}/round4/v3/parts", f"{R6}/v3/parts"; os.makedirs(dst, exist_ok=True)
    for f in sorted(os.listdir(src)):
        if f.startswith((".", "00_", "03_")) or f.endswith(".txt"): continue
        d = f"{dst}/{f}"
        if not os.path.lexists(d): os.symlink(f"{src}/{f}", d)
    print("seeded", sorted(x for x in os.listdir(dst) if not x.startswith(".")))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "seed": seed()
    elif cmd == "picture":
        for p in ("00_pickup.mp4", "03_film.mp4.v.mp4"):
            assert not os.path.islink(f"{R6}/v3/parts/{p}"), f"{p} is a link to round 4: never write through it"
        F.picture("v3")
    elif cmd == "audio": F.audio("v3", *(sys.argv[2:3]))
    elif cmd == "check":
        for e in F.check("v3"): print("!!", e)
        print("check done")
