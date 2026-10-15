#!/usr/bin/env python3
"""RA-04 round 5 cards, both aspects (run from /Volumes/Extreme/_edit_work/ra04):

  gen   the white man's real absbyai.com generation (round5/gen_white_man_rec.mp4, 1320x2868 at 60 fps, r5_record.py +
        r5_cast2mp4.py): the loader 3.40-5.80 s (one full scan sweep down his body, "Sculpting lean definition" on), window
        x 50-1270 y 715-2147 (the loader card whole: photo, status line, bar; the textarea above ends at y 668, the Generate button
        below starts at 2150), then a hard cut to the result 36.60 s on (settled from 36.2 s), window y 560-2110 (the app's own
        "AI-GENERATED IMAGE" label and the whole picture; "Lock in this goal" starts at 2150), with a 4 % push-in so the still result
        is not a frozen run. The banned before/after pair never renders (r5_record.py hides it in the page before Generate).
        Plate: the TIP 1 lower third stays up over this card, so the plate and its chip END ABOVE THE STRIP:
          9:16  hole 628x736 at y 150 (x 226), chip 68 px under it (y 954-1034); strip box y 1058-1306, captions at y 1400
          16:9  hole 548x644 at y 40 (x 686), chip on the field right of the hole's top corner; the lifted caption line's ascent box
                starts at y 709 (s07_captions.py: strip top 840 - 30 - ink 101), so the hole ends at 684 (25 px clear)
  lock  round5/lock_src.mp4 (r5_lock.py: A0074 with the white man's AI result on the screen) in round 4's slot and treatment:
        9:16 fills the frame with the AI-GENERATED chip at (60, 236); 16:9 in round 4's media-card plate (hf16/plates.json lock)

usage: python3 round5/r5_cards.py [plates] [gen] [lock]"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image
SH = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
sys.path.insert(0, SH); sys.path.insert(0, SH + "/hyperframes"); sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra04")
import softblue as SB
import composite as CP
FF = SB.FF; FD = 1001 / 30000
B = json.load(open("beats.json")); by = {c["name"]: c for c in B["cards"]}
REC = "round5/gen_white_man_rec.mp4"; RW, RH = 1320, 2868
LOADER_T0, RESULT_T0, PUSH = 3.40, 36.60, 0.04
WIN_LOADER = (50, 715, 1220, 1432); WIN_RESULT = (0, 560, 1320, 1550)
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-r", "30000/1001", "-colorspace", "bt709",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-x264-params", "keyint=30:min-keyint=1:scenecut=0"]
D709 = "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709"
GEO = {"9x16": dict(canvas=(1080, 1920), hole=[226, 150, 628, 736]),
       "16x9": dict(canvas=(1920, 1080), hole=[686, 40, 548, 644])}
want = set(sys.argv[1:]) or {"plates", "gen", "lock"}


def plates():
    from hv16 import V as V16
    import vertical as V9
    out = {}
    for key, V, d in (("9x16", V9, "hf9"), ("16x9", V16, "hf16")):
        g = GEO[key]; hx, hy, hw, hh = g["hole"]; W = g["canvas"][0]; label = "AI-GENERATED"
        cw_ = round(V.H.text_w(label, 23 * V.U, False) + 40 * V.U)
        chip = dict(x=round(W / 2 - cw_ / 2), y=hy + hh + 68, s=label, w=cw_) if key == "9x16" else dict(x=hx + hw + 36, y=hy + 8, s=label, w=cw_)
        n = by["gen"]["frames"]
        cfg = dict(id=("P_" if key == "9x16" else "P16_") + "gen", dur=round(n / (1 / FD) + 0.2, 3), canvas=list(g["canvas"]),
                   hole=[hx, hy, hw, hh], radius=26, chip=chip)
        V.build([(V.HERE / "media-card" / "media-card.template.htm", cfg, ())], os.path.abspath(d), render=True, snap=1.0)
        PL = json.load(open(f"{d}/plates.json"))
        PL["gen"] = dict(frames=n, hole=[hx, hy, hx + hw, hy + hh], mov=os.path.abspath(f"{d}/renders/{cfg['id']}.mov"), chip=chip)
        json.dump(PL, open(f"{d}/plates.json", "w"), indent=1); out[key] = PL["gen"]
        if key == "9x16": assert chip["y"] + 80 <= 1058 - 20, chip          # the chip ends above the TIP 1 strip (box top 1058)
        else: assert hy + hh <= 709 - 24, hh                                 # the hole ends above the lifted caption line
        print("plate", key, PL["gen"]["hole"], chip, flush=True)
    return out


def rec_frames(t0, n):
    """the recording's frames nearest to t0 + k*FD, k < n, as RGB arrays (1320x2868)"""
    want_idx = [int(round((t0 + k * FD) * 60)) for k in range(n)]
    a = want_idx[0]
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-ss", f"{a / 60 - 0.5 / 60:.5f}", "-i", REC, "-vf", f"{D709},format=rgb24",
                          "-frames:v", str(want_idx[-1] - a + 1), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    size = RW * RH * 3; i = a; cur = None
    for w in want_idx:
        while i <= w:
            b = p.stdout.read(size); assert len(b) == size, (t0, i); cur = np.frombuffer(b, np.uint8).reshape(RH, RW, 3); i += 1
        yield cur
    p.stdout.close(); p.wait()


def writer(out, W, H):
    return subprocess.Popen([FF, "-nostdin", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "30000/1001", "-i", "-",
                             "-vf", "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"] + ENC + [out], stdin=subprocess.PIPE)


def gen_media(wh):
    """the card's picture at the hole size: loader frames, then the result with the push-in, exactly by['gen'] frames"""
    n = by["gen"]["frames"]; nl = round(2.40 / FD); nr = n - nl
    x, y, w, h = WIN_LOADER
    for f in rec_frames(LOADER_T0, nl):
        yield np.asarray(Image.fromarray(f).resize(wh, Image.LANCZOS, box=(x, y, x + w, y + h)))
    # the push-in is anchored on the window's TOP edge: centred, it pushed the app's "AI-GENERATED IMAGE" label (40 px under the top)
    # off the card by its last frame (first build); top-anchored, only the bottom of his shorts goes
    x, y, w, h = WIN_RESULT; cx = x + w / 2
    for k, f in enumerate(rec_frames(RESULT_T0, nr)):
        s = 1 + PUSH * k / max(1, nr - 1); bw, bh = w / s, h / s
        yield np.asarray(Image.fromarray(f).resize(wh, Image.LANCZOS, box=(cx - bw / 2, y, cx + bw / 2, y + bh)))


def gen_card(key):
    W, H = GEO[key]["canvas"]; pl = json.load(open(("hf9" if key == "9x16" else "hf16") + "/plates.json"))["gen"]
    x0, y0, x1, y1 = pl["hole"]; n = by["gen"]["frames"]; e = writer(f"cards_{key}/gen.mp4", W, H); k = 0
    for f, ov in zip(gen_media((x1 - x0, y1 - y0)), CP.reader(pl["mov"], 0, n, True, (W, H))):
        c = np.zeros((H, W, 3), np.uint8); c[y0:y1, x0:x1] = f
        e.stdin.write(np.ascontiguousarray(CP.over(c, ov)).tobytes()); k += 1
    e.stdin.close(); assert e.wait() == 0 and k == n, (key, k, n); print("gen", key, n, "frames", flush=True)


def lock_cards():
    n = by["lock"]["frames"]; src = "round5/lock_src.mp4"
    m9 = "media/lock_r5.mp4"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", src, "-filter_complex",
                    f"[0:v]fps=30000/1001,setsar=1,trim=end_frame={n},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1[v]",
                    "-map", "[v]", "-frames:v", str(n)] + ENC + [m9], check=True)
    # 9:16: fills the frame, chip at (60, 236) as in round 4
    e = writer("cards_9x16/lock.mp4", 1080, 1920); box = None
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", m9, "-vf", f"{D709},format=rgb24", "-frames:v", str(n), "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    for _ in range(n):
        b = p.stdout.read(1080 * 1920 * 3); im = Image.frombuffer("RGB", (1080, 1920), b, "raw", "RGB", 0, 1).copy()
        box = SB.disclosure(im, "AI-GENERATED", (60, 236)); e.stdin.write(np.asarray(im).tobytes())
    e.stdin.close(); assert e.wait() == 0; p.wait()
    meta = json.load(open("cards_9x16/meta.json")); meta["lock"] = {"chip": "AI-GENERATED", "chip_box": box}
    pl9 = json.load(open("hf9/plates.json"))["gen"]; c = pl9["chip"]
    meta["gen"] = dict(chip=c["s"], chip_box=[c["x"], c["y"], c["x"] + c["w"], c["y"] + 80], hole=pl9["hole"])
    json.dump(meta, open("cards_9x16/meta.json", "w"), indent=1)
    # 16:9: round 4's lock plate
    pl = json.load(open("hf16/plates.json"))["lock"]; x0, y0, x1, y1 = pl["hole"]; wh = (x1 - x0, y1 - y0)
    e = writer("cards_16x9/lock.mp4", 1920, 1080)
    p = subprocess.Popen([FF, "-nostdin", "-v", "error", "-i", m9, "-vf", f"{D709},scale={wh[0]}:{wh[1]}:flags=lanczos,format=rgb24", "-frames:v", str(n),
                          "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    for ov in CP.reader(pl["mov"], 0, n, True, (1920, 1080)):
        b = p.stdout.read(wh[0] * wh[1] * 3); f = np.frombuffer(b, np.uint8).reshape(wh[1], wh[0], 3)
        c = np.zeros((1080, 1920, 3), np.uint8); c[y0:y1, x0:x1] = f; e.stdin.write(np.ascontiguousarray(CP.over(c, ov)).tobytes())
    e.stdin.close(); assert e.wait() == 0; p.wait()
    pl16 = json.load(open("hf16/plates.json")); meta = json.load(open("cards_16x9/meta.json"))
    c = pl16["gen"]["chip"]; meta["gen"] = dict(chip=c["s"], chip_box=[c["x"], c["y"], c["x"] + c["w"], c["y"] + 80], hole=pl16["gen"]["hole"])
    json.dump(meta, open("cards_16x9/meta.json", "w"), indent=1)
    print("lock cards", n, "frames; 9:16 chip", box, flush=True)


if "plates" in want: plates()
if "gen" in want:
    gen_card("9x16"); gen_card("16x9")
if "lock" in want: lock_cards()
print("R5_CARDS_COMPLETE")
