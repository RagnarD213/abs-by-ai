#!/usr/bin/env python3
"""Ad 1 visual layout pass.
Pass 1 (shared): punch-in alternation over CUT_v1_graded.mp4 -> punched.mp4
Pass 2 (per variant): full-frame image/video inserts + CTA bar + end card -> ad1_vN_nocap.mp4
Punch switch times are snapped to word boundaries from the EDL-mapped transcript.
Face anchor (1099, 300) measured on a real frame; level B = 1.22x.
"""
import json, subprocess, sys, os

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
BASE = "CUT_v1_graded.mp4"
END = 267.891
CARD_END = 271.2
FPS = "30000/1001"
CTA_START = 112.94

# ---- render-time word list (for snapping) ----
edl = json.load(open("edl.json"))["ranges"]
wh = json.load(open("C1591.whisper.json"))
words_src = [w for s in wh["segments"] for w in s.get("words", [])]
rwords = []
off = 0.0
for rg in edl:
    for w in words_src:
        if rg["start"] - 0.05 <= w["start"] <= rg["end"]:
            rwords.append((off + w["start"] - rg["start"], off + w["end"] - rg["start"]))
    off += rg["end"] - rg["start"]

def snap(t):
    """Snap to the nearest word START in render time (a cut on a word onset reads as a normal cut)."""
    best = min(rwords, key=lambda ab: abs(ab[0] - t))
    return round(best[0] - 0.04, 3) if abs(best[0] - t) < 0.6 else t

PUNCH = [  # (start, end, level)
 (0.00, 2.18, 'A'), (2.18, 6.40, 'B'), (6.40, 27.40, 'A'), (27.40, 32.78, 'B'),
 (32.78, 43.80, 'A'), (43.80, 49.48, 'B'), (49.48, 59.06, 'A'), (59.06, 69.00, 'B'),
 (69.00, 84.00, 'A'), (84.00, 86.10, 'B'), (86.10, 92.56, 'A'), (92.56, 103.90, 'B'),
 (103.90, 116.60, 'A'), (116.60, 129.30, 'B'), (129.30, 142.98, 'A'), (142.98, 149.50, 'B'),
 (149.50, 163.00, 'A'), (163.00, 174.10, 'B'), (174.10, 188.00, 'A'), (188.00, 199.20, 'B'),
 (199.20, 209.30, 'A'), (209.30, 218.50, 'B'), (218.50, 226.50, 'A'), (226.50, 236.50, 'B'),
 (236.50, 246.25, 'A'), (246.25, 252.50, 'B'), (252.50, 263.70, 'A'), (263.70, END, 'B'),
]
# snap interior boundaries
snapped = [PUNCH[0][0]] + [snap(s) for (s, e, l) in PUNCH[1:]] + [END]
PUNCH = [(snapped[i], snapped[i + 1], PUNCH[i][2]) for i in range(len(PUNCH))]
for a, b, l in PUNCH:
    assert b > a, (a, b, l)

def pass1_punch():
    parts, concat = [], []
    for i, (a, b, l) in enumerate(PUNCH):
        crop = "crop=1574:886:198:54,scale=1920:1080:flags=lanczos," if l == 'B' else ""
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,{crop}setsar=1[v{i}]")
        concat.append(f"[v{i}]")
    fc = ";".join(parts) + f";{''.join(concat)}concat=n={len(PUNCH)}:v=1:a=0[vout]"
    cmd = [FF, "-nostdin", "-y", "-v", "error", "-i", BASE,
           "-filter_complex", fc, "-map", "[vout]", "-map", "0:a",
           "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
           "-r", FPS, "-c:a", "copy", "punched.mp4"]
    subprocess.run(cmd, check=True)
    print("punched.mp4 done")

# ---- inserts ----
IMG = [  # (start, end, asset_key)
 (6.40, 9.30, "p_before"),
 (17.20, 19.75, "p_shot1"), (19.75, 22.30, "p_shot2"),
 (22.30, 24.85, "p_shot3"), (24.85, 27.40, "p_shot4"),
 (79.90, 84.00, "p_goal"),
 (146.40, 149.50, "p_before"),
 (221.90, 226.50, "p_app_assess"),
 (232.00, 236.50, "p_app_workout"),
 (248.30, 252.50, "p_app_nutri"),
]
A_DIR = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets"
PHONE = f"{A_DIR}/batch1-ads/clips/ai-fat-dan-sees-ripped-dan-phone-10s.mp4"
APPFLOW = f"{A_DIR}/ad2-nutritionist/clips/app-flow-generate-future-self.mp4"
CRUDE = f"{A_DIR}/batch1-ads/clips/ai-clip-crude-photoshop.mp4"
VID = [  # (start, end, src, src_in, src_out, w_after_scale, crop_filter)
 (9.30, 14.30, PHONE, 5.0, 10.0, 608, ""),
 (64.00, 69.00, CRUDE, 0.0, 5.0, 602, ""),
 (159.00, 163.00, PHONE, 0.5, 4.5, 608, ""),
 (214.10, 218.50, APPFLOW, 24.0, 28.4, 570, "crop=1320:2500:0:175,"),
]

def pass2(variant):
    av = f"assets_v{variant}"
    inputs = ["-i", "punched.mp4"]
    fc = []
    cur = "[0:v]"
    idx = 1
    # opener: goal panel with push-in
    inputs += ["-loop", "1", "-t", "2.35", "-i", f"{av}/p_goal.jpg"]
    fc.append(f"[{idx}:v]scale=2304:1296,zoompan=z='1+0.10*on/66':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={FPS},setsar=1[op]")
    fc.append(f"{cur}[op]overlay=0:0:enable='between(t,0,2.18)'[s{idx}]")
    cur = f"[s{idx}]"; idx += 1
    # image inserts
    for (a, b, key) in IMG:
        inputs += ["-loop", "1", "-t", str(round(b - a + 0.3, 2)), "-i", f"{av}/{key}.jpg"]
        fc.append(f"[{idx}:v]setsar=1,setpts=PTS+{a}/TB[i{idx}]")
        fc.append(f"{cur}[i{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]")
        cur = f"[s{idx}]"; idx += 1
    # video inserts: panel bg + scaled clip + tag
    for (a, b, src, si, so, wid, cropf) in VID:
        dur = round(b - a, 3)
        inputs += ["-loop", "1", "-t", str(dur + 0.3), "-i", f"{av}/p_vidbg.jpg"]
        fc.append(f"[{idx}:v]setsar=1,setpts=PTS+{a}/TB[bg{idx}]")
        fc.append(f"{cur}[bg{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]")
        cur = f"[s{idx}]"; idx += 1
        inputs += ["-ss", str(si), "-t", str(dur + 0.2), "-i", src]
        x = (1920 - wid) // 2
        fc.append(f"[{idx}:v]{cropf}scale={wid}:1080:flags=lanczos,setsar=1,setpts=PTS-STARTPTS+{a}/TB[c{idx}]")
        fc.append(f"{cur}[c{idx}]overlay={x}:0:enable='between(t,{a},{b})'[s{idx}]")
        cur = f"[s{idx}]"; idx += 1
        inputs += ["-loop", "1", "-t", str(dur + 0.3), "-i", f"{av}/tag.png"]
        fc.append(f"[{idx}:v]setpts=PTS+{a}/TB[t{idx}]")
        fc.append(f"{cur}[t{idx}]overlay=(main_w-overlay_w)/2:40:enable='between(t,{a},{b})'[s{idx}]")
        cur = f"[s{idx}]"; idx += 1
    # end card: pad video to CARD_END with the card
    inputs += ["-loop", "1", "-t", str(round(CARD_END - END + 0.3, 2)), "-i", f"{av}/end_card.jpg"]
    fc.append(f"{cur}tpad=stop_mode=clone:stop_duration={round(CARD_END-END,3)}[padded]")
    fc.append(f"[{idx}:v]setsar=1,setpts=PTS+{END}/TB[ec]")
    fc.append(f"[padded][ec]overlay=0:0:enable='between(t,{END},{CARD_END})'[s{idx}]")
    cur = f"[s{idx}]"; idx += 1
    # CTA bar (persistent)
    inputs += ["-loop", "1", "-t", str(round(CARD_END - CTA_START + 0.3, 2)), "-i", f"{av}/cta_bar.png"]
    fc.append(f"[{idx}:v]setpts=PTS+{CTA_START}/TB[bar]")
    fc.append(f"{cur}[bar]overlay=0:984:enable='between(t,{CTA_START},{CARD_END})'[vout]")
    # audio: pad with silence to CARD_END
    fc.append(f"[0:a]apad,atrim=end={CARD_END}[aout]")
    out = f"ad1_v{variant}_nocap.mp4"
    cmd = [FF, "-nostdin", "-y", "-v", "error"] + inputs + [
        "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "aac", "-b:a", "192k", out]
    subprocess.run(cmd, check=True)
    print(out, "done")

if __name__ == "__main__":
    if "punch" in sys.argv: pass1_punch()
    if "v1" in sys.argv: pass2(1)
    if "v2" in sys.argv: pass2(2)
