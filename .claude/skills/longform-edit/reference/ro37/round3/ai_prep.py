"""RO-37 round 3: the finished AI inserts, exact film length, 1920x1080 at 30000/1001, AI-GENERATED chip on.
  A2  : thumbs-up take, real speed
  A2b : sit-ups fast-forwarded with the wall clock spinning 6:00 -> 8:00 (Dan: "the clock spins to establish that this is
        fast-forwarded footage"); the take is retimed to the slot and the clock hands are repainted in code, because Veo's stay still
  A3, A4, A7r: real speed, the picked window
"""
import json, os, subprocess, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2, numpy as np, cv2
sys.path.insert(0, f"{r2.P}/.claude/skills/_shared"); import softblue as B
from PIL import Image
W3 = r2.W3; OW, OH = 1920, 1080
chip = Image.new("RGBA", (OW, OH), (0, 0, 0, 0)); B.disclosure(chip, "AI-GENERATED", xy=(56, 48))
CH = np.asarray(chip, np.float32); CA = CH[..., 3:4] / 255; CRGB = CH[..., :3]
PICK = json.load(open(f"{W3}/ai/picks.json"))      # {id: {take, ss (seconds into the take), speed}}
CX, CY, R_FACE = PICK["clock"]["cx"], PICK["clock"]["cy"], PICK["clock"]["r"]      # in 1920 output pixels


def frames(path, ss, n, speed):
    """n output frames at 29.97 from `ss`, speed x real time."""
    vf = f"setpts=PTS/{speed},fps=30000/1001,scale=1920:1080:flags=lanczos,format=rgb24"
    p = subprocess.Popen([r2.FF, "-nostdin", "-v", "error", "-ss", str(ss), "-i", path, "-an", "-vf", vf, "-frames:v", str(n), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    out = []
    for i in range(n):
        raw = p.stdout.read(OW * OH * 3)
        out.append(np.frombuffer(raw, np.uint8).reshape(OH, OW, 3).copy() if len(raw) == OW * OH * 3 else out[-1].copy())
    p.stdout.close(); p.wait()
    return out


def seq(path, segs, n):
    """n output frames sampled evenly along a list of [first, last) take-frame ranges (a rep loop, then the collapse): fast-forward."""
    cap = cv2.VideoCapture(path); src = []
    while True:
        ok, x = cap.read()
        if not ok: break
        src.append(cv2.resize(x, (OW, OH), interpolation=cv2.INTER_LANCZOS4)[..., ::-1])
    idx = [i for a, b in segs for i in range(a, b)]
    return [src[idx[min(len(idx) - 1, int(i * len(idx) / n))]].copy() for i in range(n)]


def clock(img, ang_min, ang_hour, wall):
    """Repaint the hands: the inside of the face (inside the tick ring) back to its plain white, then hour and minute hands."""
    S = 4; r = int(R_FACE * 1.1); x0, y0 = int(CX - r), int(CY - r)
    pad = img[y0:y0 + 2 * r, x0:x0 + 2 * r].copy()
    big = np.full((2 * r * S, 2 * r * S), 0, np.uint8); c = r * S
    def hand(l, tail, w, a, v=255):
        dx, dy = math.sin(a), -math.cos(a)
        cv2.line(big, (int(c - tail * S * dx), int(c - tail * S * dy)), (int(c + l * S * dx), int(c + l * S * dy)), v, int(w * S), cv2.LINE_AA)
    hand(R_FACE * 0.50, R_FACE * 0.06, R_FACE * 0.05, ang_hour)
    for k, f in enumerate((0, -0.06, -0.12, -0.18)):        # the fast minute hand smears a little, as a real spinning hand would
        hand(R_FACE * 0.78, R_FACE * 0.06, R_FACE * 0.028, ang_min + f, 255 - k * 70)
    m = cv2.resize(big, (2 * r, 2 * r), interpolation=cv2.INTER_AREA).astype(np.float32)[..., None] / 255
    yy, xx = np.mgrid[:2 * r, :2 * r].astype(np.float32); d = np.hypot(xx - r, yy - r)
    face = np.clip((R_FACE * 0.84 - d) / 2, 0, 1)[..., None]
    out = pad.astype(np.float32) * (1 - face) + wall * face
    out = out * (1 - m) + np.array([22, 22, 24], np.float32) * m
    img[y0:y0 + 2 * r, x0:x0 + 2 * r] = np.clip(out, 0, 255).astype(np.uint8)


def write(fs, out):
    p = subprocess.Popen([r2.FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", "30000/1001", "-i", "-", "-an", "-vf",
                          "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
                          "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out], stdin=subprocess.PIPE)
    for f in fs: p.stdin.write((f.astype(np.float32) * (1 - CA) + CRGB * CA + .5).astype(np.uint8).tobytes())
    p.stdin.close(); assert p.wait() == 0
    print(out, len(fs), flush=True)


for it in r2.AI3:
    pk = PICK[it["id"]]; n = r2.fr(it["t1"]) - r2.fr(it["t0"])
    if len(sys.argv) > 1 and it["id"] not in sys.argv[1:]: continue
    fs = seq(f"{W3}/veo/{pk['take']}", pk["segs"], n) if "segs" in pk else frames(f"{W3}/veo/{pk['take']}", pk["ss"], n, pk.get("speed", 1.0))
    if it["id"] == "A2b":
        wall = np.median(fs[0][int(CY - R_FACE * .35):int(CY - R_FACE * .15), int(CX + R_FACE * .1):int(CX + R_FACE * .4)].reshape(-1, 3), 0).astype(np.float32)
        turns = PICK["clock"].get("turns", 2.0)
        for i, f in enumerate(fs):
            u = min(1.0, i / max(1, int(n * PICK["clock"].get("spin_until", 0.9))))
            m = 2 * math.pi * turns * (u - 1); h = (8 + (turns * (u - 1))) * 2 * math.pi / 12
            clock(f, m, h, wall)
    write(fs, it["file"])
