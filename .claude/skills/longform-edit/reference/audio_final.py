#!/usr/bin/env python3
"""Final mix: voice + music bed + SFX, then one corrective measured loudnorm.

VOICE: the chain fitted in fitvoice.py -- light, because the right channel of this
shoot already measures within 0.87 dB of the reference cut's voice. No compressor: the
reference measures LRA 13.6 and ours 10.8, so the read is already the tighter of the two.

MUSIC: Pixabay "Organic Flow" (Content Licence: commercial use, NO attribution). Chosen
by pick_bed.py, which scores every candidate against the reference cut's OWN bed sampled
in his speech gaps. It won on flatness (0.4 dB over 4 s blocks, the best of seven) but
carried 4.5 dB of shape error -- too much energy at 400-3000 Hz, which is where the voice
lives. That is the fixable half, so it is fixed: the EQ below lands the shape error at
0.53 dB against his bed profile. Ducked by the voice with a long release, because a short
one lets the bed spring back between words.

SFX: synthesised in sfxlib (no library, no licence to track), one cue per graphic
entrance -- which is what the reference edit does and our cut had none of.
"""
import json, os, subprocess, sys
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared")
import numpy as np, sfxlib
import spec

FF = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
SR = 48000
VOICE_WAV = "audio/voice_tight.wav"
MUSIC     = "music/organic_flow.mp3"
DUR       = json.load(open("plan.json"))["dur"]
MUSIC_DB  = -21.0        # under the voice; the reference bed sits ~-20 dB RMS under his
SFX_DB    = -15.0
LEAD      = 0.10         # a whoosh reads as ON the cut when it starts just before it

EQ   = ("equalizer=f=88:t=q:w=0.9:g=1.4,equalizer=f=430:t=q:w=1.3:g=-1.0,"
        "equalizer=f=3800:t=q:w=1.3:g=-1.8,equalizer=f=10000:t=q:w=0.8:g=-1.2")
GATE = "agate=threshold=0.0035:ratio=2.0:range=0.35:attack=4:release=280:knee=8"
VOICE = f"highpass=f=62,{GATE},{EQ},pan=stereo|c0=c0|c1=c0"
BED_EQ = ("equalizer=f=320:t=q:w=0.9:g=-4,equalizer=f=800:t=q:w=0.9:g=-6,"
          "equalizer=f=2200:t=q:w=1.0:g=-9,equalizer=f=5500:t=q:w=0.9:g=-4")

def cues():
    C = []
    for a, d, kind, key, pl in spec.G:
        if kind in ("title", "endcard"):
            C += [(a - 0.55, "riser", 0.55), (a, "whoosh", 1.0), (a, "sub", 0.8)]
        elif kind == "section":
            C.append((a, "whoosh_soft", 0.9))
        elif kind == "lower":
            C.append((a, "whoosh_soft", 0.75))
        elif kind == "number":
            C += [(a, "whoosh", 0.85), (a, "sub", 0.6)]
        elif kind == "stack":
            for (bt, _) in pl["items"]: C.append((a + bt, "pop_soft", 0.9))
    for a, d, kind, key, note in spec.INSERTS:
        if kind == "inset": C.append((a, "whoosh_soft", 0.6))
    return sorted(C)

def build_sfx(C):
    pack = {
        "whoosh":      sfxlib.whoosh(0.42, 420, 4200, 900),
        "whoosh_soft": sfxlib.whoosh(0.34, 500, 2600, 800, q=1.0, seed=11),
        "pop_soft":    sfxlib.pop(700, 0.10, 0.40),
        "riser":       sfxlib.riser(0.55),
        "sub":         sfxlib.sub_drop(),
    }
    bed = np.zeros(int(DUR * SR) + SR)
    for (t, name, g) in C:
        y = pack[name] * g
        i = int(max(0.0, t - LEAD) * SR)
        bed[i:i + len(y)] += y
    peak = np.abs(bed).max()
    if peak > 0.9: bed *= 0.9 / peak
    sfxlib.save("sfx/bed.wav", bed[:int(DUR * SR)])
    print(f"sfx/bed.wav  {len(C)} cues, peak {peak:.2f}")

if __name__ == "__main__":
    # 2026-09-02: the cue list and SFX synthesis above are this skill's; the CHAIN is the shared module.
    # voice_chain fits the EQ per roll, keeps the compressor off, ducks the bed at <= -30 dB, mixes the
    # SFX bed as --extra and finishes with measured gain + alimiter to -14 LUFS / -2.5 dBTP in PCM
    # (the AAC then lands <= -1.5). The old two-pass loudnorm + hand-fitted VOICE/BED_EQ live in git.
    import subprocess as _sp
    os.makedirs("sfx", exist_ok=True)
    C = cues(); build_sfx(C)
    r = _sp.run(["python3", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py", "--in", VOICE_WAV, "--out", "audio/final_mix.wav",
                 "--bed", MUSIC, "--bed-db", str(MUSIC_DB), "--extra", "sfx/bed.wav"])
    raise SystemExit(r.returncode)
