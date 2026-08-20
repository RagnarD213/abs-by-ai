#!/usr/bin/env python3
"""Ad 1 rev-1 layout — LOCKED STYLE: J2 graphics + CTA bar, MadMuscles captions (burned later).
Pass 1: punch alternation over CUT_v2_graded.mp4 (anchors computed from the new EDL).
Pass 2: inserts (stock clips, Ken Burns photos, phone mockup, before->generating->after)
        + CTA bar + end card -> ad1_rev1_nocap.mp4
"""
import json, subprocess, sys

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
BASE = "CUT_v2_graded.mp4"
FPS = "30000/1001"
AV = "assets_v1"

edl = json.load(open("edl.json"))["ranges"]
wh = json.load(open("C1591.whisper.json"))
words_src = [w for s in wh["segments"] for w in s.get("words", [])]
rwords, offs = [], []
off = 0.0
for rg in edl:
    offs.append((rg["start"], rg["end"], off))
    for w in words_src:
        if rg["start"] - 0.05 <= w["start"] <= rg["end"]:
            rwords.append((off + w["start"] - rg["start"], off + w["end"] - rg["start"]))
    off += rg["end"] - rg["start"]
END = round(off, 3)
CARD_END = round(END + 3.3, 3)

def r(src):
    for a, b, o in offs:
        if a - 0.3 <= src <= b + 0.3:
            return round(o + src - a, 2)
    raise ValueError(src)

def snap(t):
    best = min(rwords, key=lambda ab: abs(ab[0] - t))
    return round(best[0] - 0.04, 3) if abs(best[0] - t) < 0.6 else t

# ---- anchors (source seconds -> render) ----
CTA_START = r(168.12)            # "Just tap the button below" (CTA 1)
STK1 = (46.00, 50.00)            # frustrated overweight man (render, unchanged region)
STK2 = (r(176.95), r(178.70))    # "You're more attractive to women."
STK3 = (r(178.70), r(180.40))    # "Men respect you more."
STK4 = (r(180.40), r(186.90))    # "You feel better ... live longer too."
BEFORE2 = (r(208.26), r(211.40))
PHONEMOCK = (r(220.82), r(225.00))
SEQ = (r(275.94), r(282.60))     # before -> generating -> after
ASSESS = (r(283.76), r(288.40))
WORKOUT = (r(293.88), r(298.40))
NUTRI = (r(355.20), r(359.40))

PUNCH_RAW = [
 (0.00, 2.18, 'A'), (2.18, 6.40, 'B'), (6.40, 27.40, 'A'), (27.40, 32.78, 'B'),
 (32.78, 43.84, 'A'), (43.84, 50.00, 'B'), (50.00, 59.06, 'A'), (59.06, 69.00, 'B'),
 (69.00, 84.00, 'A'), (84.00, 86.10, 'B'), (86.10, 96.44, 'A'),
 (96.44, r(158.96), 'B'), (r(158.96), r(171.80), 'A'), (r(171.80), r(176.95), 'B'),
 (r(176.95), r(186.90), 'B'),           # covered by stock 2-4
 (r(186.90), r(204.90), 'A'),           # "And here's the truth..." j3 handled next
 (r(204.90), BEFORE2[1], 'B'),          # j3 switch + before2 cover
 (BEFORE2[1], PHONEMOCK[0], 'A'),
 (PHONEMOCK[0], PHONEMOCK[1], 'A'),     # covered
 (PHONEMOCK[1], r(235.90), 'B'),
 (r(235.90), r(249.78), 'A'),
 (r(249.78), r(261.00), 'B'),
 (r(261.00), r(271.10), 'A'),
 (r(271.10), SEQ[0], 'B'),
 (SEQ[0], SEQ[1], 'B'),                 # covered
 (SEQ[1], ASSESS[0], 'A'),
 (ASSESS[0], WORKOUT[0], 'A'),          # assess covered; visible sliver stays A
 (WORKOUT[0], WORKOUT[1], 'B'),         # covered
 (WORKOUT[1], r(354.68) if False else None, 'X'),
]
# rebuild tail cleanly
J4 = r(354.70)
PUNCH_RAW = [p for p in PUNCH_RAW if p[2] != 'X']
PUNCH_RAW += [(WORKOUT[1], J4, 'A'), (J4, NUTRI[1], 'B'), (NUTRI[1], r(372.14), 'A'), (r(372.14), END, 'B')]

# merge adjacent same-level, snap boundaries
merged = []
for a, b, l in PUNCH_RAW:
    if merged and merged[-1][2] == l:
        merged[-1] = (merged[-1][0], b, l)
    else:
        merged.append((a, b, l))
snapped = [merged[0][0]] + [snap(s) for (s, e, l) in merged[1:]] + [END]
PUNCH = []
for i in range(len(merged)):
    a, b = snapped[i], snapped[i + 1]
    if b > a: PUNCH.append((a, b, merged[i][2]))

def pass1():
    parts, concat = [], []
    for i, (a, b, l) in enumerate(PUNCH):
        crop = "crop=1574:886:198:54,scale=1920:1080:flags=lanczos," if l == 'B' else ""
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS,{crop}setsar=1[v{i}]")
        concat.append(f"[v{i}]")
    fc = ";".join(parts) + f";{''.join(concat)}concat=n={len(PUNCH)}:v=1:a=0[vout]"
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", BASE,
        "-filter_complex", fc, "-map", "[vout]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "copy", "punched2.mp4"], check=True)
    print("punched2.mp4 done")

A_DIR = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets"
PHONE = f"{A_DIR}/batch1-ads/clips/ai-fat-dan-sees-ripped-dan-phone-10s.mp4"
CRUDE = f"{A_DIR}/batch1-ads/clips/ai-clip-crude-photoshop.mp4"
APPFLOW = f"{A_DIR}/ad2-nutritionist/clips/app-flow-generate-future-self.mp4"
STK = "stock/%s.mp4"
AFCROP = "crop=1320:2500:0:175,"

# static image inserts: (start, end, asset)
IMG = [
 (6.40, 9.30, "p_before"),
 (79.90, 84.00, "p_goal"),
 (BEFORE2[0], BEFORE2[1], "p_before"),
 (ASSESS[0], ASSESS[1], "p_app_assess"),
 (WORKOUT[0], WORKOUT[1], "p_app_workout"),
 (NUTRI[0], NUTRI[1], "p_app_nutri"),
]
# Ken Burns image inserts (zoompan): (start, end, asset, direction)
KB = [
 (17.20, 19.75, "p_shot1", "in"), (19.75, 22.30, "p_shot2", "out"),
 (22.30, 24.85, "p_shot3", "in"), (24.85, 27.40, "p_shot4", "out"),
 (PHONEMOCK[0], PHONEMOCK[1], "p_phone_mock", "in"),
]
# video inserts: (start, end, src, src_in, width, crop, tag?)  full-frame stock use w=0
VID = [
 (9.30, 14.30, PHONE, 5.0, 608, "", True),
 (STK1[0], STK1[1], STK % "3802827", 2.0, 0, "", False),
 (64.00, 69.00, CRUDE, 0.0, 602, "", True),
 (STK2[0], STK2[1], STK % "4866855", 0.7, 0, "", False),
 (STK3[0], STK3[1], STK % "6296483", 2.5, 0, "", False),
 (STK4[0], STK4[1], STK % "9184994", 15.0, 0, "", False),
 (SEQ[0], round(SEQ[0]+2.2,2), APPFLOW, 0.6, 570, AFCROP, False),   # before alone
 (round(SEQ[0]+2.2,2), round(SEQ[0]+4.4,2), APPFLOW, 20.0, 570, AFCROP, False),  # generating
 (round(SEQ[0]+4.4,2), SEQ[1], APPFLOW, 29.4, 570, AFCROP, True),   # after alone, tagged
]

def pass2():
    inputs = ["-i", "punched2.mp4"]
    fc, idx = [], 1
    cur = "[0:v]"
    # opener with push-in
    inputs += ["-loop", "1", "-t", "2.35", "-i", f"{AV}/p_goal.jpg"]
    fc.append(f"[{idx}:v]scale=2304:1296,zoompan=z='1+0.10*on/66':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={FPS},setsar=1[op]")
    fc.append(f"{cur}[op]overlay=0:0:enable='between(t,0,2.18)'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
    for (a, b, key) in IMG:
        inputs += ["-loop", "1", "-t", str(round(b - a + 0.3, 2)), "-i", f"{AV}/{key}.jpg"]
        fc.append(f"[{idx}:v]setsar=1,setpts=PTS+{a}/TB[i{idx}]")
        fc.append(f"{cur}[i{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
    for (a, b, key, direc) in KB:
        n = max(2, int((b - a) * 29.97))
        z = f"1+0.09*on/{n}" if direc == "in" else f"1.09-0.09*on/{n}"
        inputs += ["-loop", "1", "-t", str(round(b - a + 0.3, 2)), "-i", f"{AV}/{key}.jpg"]
        fc.append(f"[{idx}:v]scale=2304:1296,zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps={FPS},setsar=1,setpts=PTS+{a}/TB[k{idx}]")
        fc.append(f"{cur}[k{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
    for (a, b, src, si, wid, cropf, tag) in VID:
        dur = round(b - a, 3)
        if wid:  # panel treatment
            inputs += ["-loop", "1", "-t", str(dur + 0.3), "-i", f"{AV}/p_vidbg.jpg"]
            fc.append(f"[{idx}:v]setsar=1,setpts=PTS+{a}/TB[bg{idx}]")
            fc.append(f"{cur}[bg{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
            inputs += ["-ss", str(si), "-t", str(dur + 0.2), "-i", src]
            x = (1920 - wid) // 2
            fc.append(f"[{idx}:v]{cropf}scale={wid}:1080:flags=lanczos,setsar=1,setpts=PTS-STARTPTS+{a}/TB[c{idx}]")
            fc.append(f"{cur}[c{idx}]overlay={x}:0:enable='between(t,{a},{b})'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
        else:    # full-frame stock (16:9 cover)
            inputs += ["-ss", str(si), "-t", str(dur + 0.2), "-i", src]
            fc.append(f"[{idx}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,setpts=PTS-STARTPTS+{a}/TB[c{idx}]")
            fc.append(f"{cur}[c{idx}]overlay=0:0:enable='between(t,{a},{b})'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
        if tag:
            ty = 300 if src == APPFLOW else 40
            inputs += ["-loop", "1", "-t", str(dur + 0.3), "-i", f"{AV}/tag.png"]
            fc.append(f"[{idx}:v]setpts=PTS+{a}/TB[t{idx}]")
            fc.append(f"{cur}[t{idx}]overlay=(main_w-overlay_w)/2:{ty}:enable='between(t,{a},{b})'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
    # end card
    inputs += ["-loop", "1", "-t", str(round(CARD_END - END + 0.3, 2)), "-i", f"{AV}/end_card.jpg"]
    fc.append(f"{cur}tpad=stop_mode=clone:stop_duration={round(CARD_END-END,3)}[pad]")
    fc.append(f"[{idx}:v]setsar=1,setpts=PTS+{END}/TB[ec]")
    fc.append(f"[pad][ec]overlay=0:0:enable='between(t,{END},{CARD_END})'[s{idx}]"); cur = f"[s{idx}]"; idx += 1
    # CTA bar
    inputs += ["-loop", "1", "-t", str(round(CARD_END - CTA_START + 0.3, 2)), "-i", f"{AV}/cta_bar.png"]
    fc.append(f"[{idx}:v]setpts=PTS+{CTA_START}/TB[bar]")
    fc.append(f"{cur}[bar]overlay=0:984:enable='between(t,{CTA_START},{CARD_END})'[vout]")
    fc.append(f"[0:a]apad,atrim=end={CARD_END}[aout]")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error"] + inputs + [
        "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-r", FPS, "-c:a", "aac", "-b:a", "192k", "ad1_rev1_nocap.mp4"], check=True)
    print("ad1_rev1_nocap.mp4 done  END=", END, "CARD_END=", CARD_END)

if __name__ == "__main__":
    print("anchors: CTA=%.2f STK2=%s STK3=%s STK4=%s BEFORE2=%s PHONEMOCK=%s SEQ=%s ASSESS=%s WORKOUT=%s NUTRI=%s END=%.2f"
          % (CTA_START, STK2, STK3, STK4, BEFORE2, PHONEMOCK, SEQ, ASSESS, WORKOUT, NUTRI, END))
    if "punch" in sys.argv: pass1()
    if "layout" in sys.argv: pass2()
