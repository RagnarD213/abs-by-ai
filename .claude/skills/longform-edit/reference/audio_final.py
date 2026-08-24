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

def chain():
    return (
        f"[0:a]{VOICE},asplit=2[vmix][vkey];"
        f"[1:a]{BED_EQ},aloop=loop=4:size={int(130*44100)},atrim=0:{DUR:.3f},"
        f"asetpts=PTS-STARTPTS,volume={MUSIC_DB}dB,afade=t=in:st=0:d=1.2,"
        f"afade=t=out:st={DUR-2.0:.3f}:d=2.0,aresample=48000[mus];"
        f"[mus][vkey]sidechaincompress=threshold=0.020:ratio=9:attack=12:release=420:"
        f"makeup=1:level_sc=1[duck];"
        f"[2:a]volume={SFX_DB}dB[sfx];"
        f"[vmix][duck][sfx]amix=inputs=3:duration=first:normalize=0,aresample=48000[premix]"
    )

def measure(fc):
    p = subprocess.run([FF, "-nostdin", "-hide_banner", "-nostats",
        "-i", VOICE_WAV, "-i", MUSIC, "-i", "sfx/bed.wav", "-filter_complex",
        fc + ";[premix]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
        "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True)
    return json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1])

if __name__ == "__main__":
    os.makedirs("sfx", exist_ok=True)
    C = cues(); build_sfx(C)
    fc = chain(); m = measure(fc)
    print("measured:", {k: m[k] for k in ("input_i", "input_tp", "input_lra")})
    # TP target -2.5, not -1.5, because the DELIVERED file is AAC and the AAC encoder
    # overshoots. Measured on this mix, all three at 256k:
    #     loudnorm TP     PCM dBTP    delivered AAC        integrated
    #        -1.5           -1.50        +0.28  FAIL         -14.15
    #        -2.0             --         -0.44  FAIL (gate is -0.5)
    #        -2.5             --         -1.47  PASS         -14.74
    # so the encoder adds ~1.8 dB here and the headroom costs ~0.3 LUFS per 0.5 dB.
    # That trade is worth taking; it is NOT the alimiter trade the skill warns about,
    # which costs a dB of loudness per dB of peak.
    ln = (f"loudnorm=I=-14:TP=-2.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error",
        "-i", VOICE_WAV, "-i", MUSIC, "-i", "sfx/bed.wav",
        "-filter_complex", f"{fc};[premix]{ln}[aout]", "-map", "[aout]",
        "-t", f"{DUR:.3f}", "-c:a", "pcm_s24le", "audio/final_mix.wav"], check=True)
    print("audio/final_mix.wav done")
