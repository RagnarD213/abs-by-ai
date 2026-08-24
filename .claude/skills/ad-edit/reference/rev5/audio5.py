#!/usr/bin/env python3
"""rev5 audio: lav voice chain -> centred stereo, ducked CC0 music bed, transition SFX,
two-pass loudnorm to -14 LUFS.

Source is already the RIGHT channel only, in mono (tight_full.py). That is the fix that
matters: the roll carries two different microphones 7.8 ms apart with the far one
polarity-inverted, and carrying both is a comb filter no EQ can undo.

Music: Pixabay "Background Music" (pixabay.com/music/acoustic-group-background-music-320427/).
The Pixabay Content Licence allows commercial use with NO attribution required -- chosen
over the CC-BY Kevin MacLeod track the 60 s sample used, which would have obliged us to
credit a music library inside a paid ad. Picked by measurement (pick_bed.py): closest
spectral shape to the bed under Muhammad's own mix, and the flattest of four candidates.

  python3 audio5.py            # sfxbed.wav then rev5_16x9.mp4
"""
import importlib.util, json, os, subprocess, sys
import numpy as np

SK = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec = importlib.util.spec_from_file_location("sfxlib", f"{SK}/sfxlib.py")
sfxlib = importlib.util.module_from_spec(spec); spec.loader.exec_module(sfxlib)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beats5 as B

FF  = "/Volumes/Extreme/_edit_work/bin/ffmpeg"
FFP = FF.replace("ffmpeg", "ffprobe")
VIDEO = os.environ.get("VIN", f"{HERE}/rev5_nocap.mov")
OUT   = os.environ.get("VOUT", f"{HERE}/rev5_nocap_audio.mov")
MUSIC = f"{HERE}/music/acoustic_bg.mp3"
SR    = sfxlib.SR

MUSIC_DB   = -19.0
MUSIC_FADE = 1.6
SFX_DB     = -11.0
LEAD       = 0.06          # fire the transient just before the motion starts

# Full-screen / panel graphics get an entrance whoosh and an exit; panels also get a sub
# under the layout change; bullet appearances get a soft pop; title cards get a riser.
CARDS   = ["gen", "phone", "today", "look", "before1", "fatdad", "afterpic",
           "cta1", "cta2", "superior", "title"]
PANELS  = ["bullets", "free", "planbul"]
CHIPS   = ["lower3", "lower3b", "lower3c", "step1"]
NAME2BEAT = {"gen": B.GEN, "phone": B.PHONE, "today": B.TODAY, "look": B.LOOKNOW,
             "before1": B.BEFORE1, "fatdad": B.FATDAD, "afterpic": B.AFTERPIC,
             "cta1": B.CTA1, "cta2": B.CTA2, "superior": B.SUPERIOR, "title": B.TITLE,
             "bullets": B.BULLETS, "free": B.FREECARD, "planbul": B.PLANBUL,
             "lower3": B.LOWER3, "lower3b": B.LOWER3B, "lower3c": B.LOWER3C,
             "step1": B.STEP1}
CLIP_BEATS = [B.DADCLIP, B.BBUILD, B.SHOP, B.AMAZING, B.BEN1, B.BEN2, B.BEN3, B.BEN4,
              B.MEALPREP, B.ASSESS, B.SEQ, B.WORKOUT, B.NUTRI, B.ENDCARD]

def cues():
    c = []
    for n in CARDS:
        a, b = NAME2BEAT[n]
        c += [(a, "whoosh", 0.80), (b, "whoosh_out", 0.55)]
    for n in PANELS:
        a, b = NAME2BEAT[n]
        c += [(a, "whoosh", 0.85), (a, "sub", 0.55), (b, "whoosh_out", 0.60)]
    for n in CHIPS:
        a, b = NAME2BEAT[n]
        c += [(a, "whoosh_soft", 0.60), (b, "whoosh_out", 0.40)]
    for (a, b) in CLIP_BEATS:
        c += [(a, "whoosh", 0.70), (b, "whoosh_out", 0.45)]
    c.append((B.TITLE[0] - 0.72, "riser", 0.55))
    c.append((B.CALLOUT[0] + 0.20, "whoosh_soft", 0.55))
    # bullet-by-bullet pops
    for n in PANELS:
        a, b = NAME2BEAT[n]
        for t in np_bullets(n, a, b): c.append((t, "pop_soft", 0.60))
    c.append((B.GEN[0] + (B.GEN[1]-B.GEN[0])*0.62, "pop", 0.55))
    c = sorted(t for t in c if 0 <= t[0] < B.DUR)
    # Beats run back to back all through this ad, so an exit whoosh lands on top of the
    # next card's entrance whoosh and the pair reads as one muddy noise. Drop the exit
    # whenever something else enters within 0.35 s.
    ents = [t for t, n, _ in c if n in ("whoosh", "whoosh_soft")]
    return [(t, n, g) for (t, n, g) in c
            if n != "whoosh_out" or not any(abs(t - e) < 0.35 for e in ents)]

def np_bullets(name, a, b):
    """Bullet entrance times, taken from the same phrases gfx5 syncs the bullets to."""
    P = {"bullets": ["how I got limitless", "what I needed to do", "how you can generate"],
         "free":    ["completely free"],
         "planbul": ["works around your injuries", "It targets your lagging",
                     "And it uses a specific equipment"]}
    out = []
    for ph in P.get(name, []):
        try: out.append(B.at(ph, after=a - 0.5))
        except KeyError: pass
    return [t for t in out if a < t < b]

def dur_of(path):
    return float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", path], capture_output=True,
                                text=True).stdout.strip())

def build_sfx_bed(total, CUES):
    pack = {k: sfxlib.__dict__[fn](**kw) for k, (fn, kw) in {
        "whoosh":      ("whoosh", dict(dur=0.42, f0=420, f1=4200, f2=900)),
        "whoosh_soft": ("whoosh", dict(dur=0.34, f0=500, f1=2600, f2=800, q=1.0, seed=11)),
        "whoosh_out":  ("whoosh", dict(dur=0.36, f0=3200, f1=900, f2=320, q=1.1, seed=19)),
        "pop":         ("pop",    dict(freq=920)),
        "pop_soft":    ("pop",    dict(freq=700, dur=0.10, drop=0.40)),
        "riser":       ("riser",  dict(dur=0.75)),
        "sub":         ("sub_drop", dict()),
    }.items()}
    bed = np.zeros(int(total * SR) + SR)
    for (t, name, gain) in CUES:
        y = pack[name] * gain
        i = int(max(0.0, t - LEAD) * SR)
        bed[i:i + len(y)] += y
    peak = np.abs(bed).max()
    if peak > 0.9: bed *= 0.9 / peak
    sfxlib.save(f"{HERE}/sfxbed.wav", bed[:int(total * SR)])
    print(f"sfxbed.wav  {len(CUES)} cues, peak {peak:.2f}")

VOICE = (
    "highpass=f=80,"
    "equalizer=f=320:t=q:w=1.1:g=-4.6,"      # the lav chest bump
    "equalizer=f=170:t=q:w=1.0:g=-0.2,"
    "equalizer=f=1700:t=q:w=1.3:g=-2.0,"     # boxiness
    "equalizer=f=560:t=q:w=1.0:g=1.4,"       # body
    "equalizer=f=2600:t=q:w=1.1:g=2.6,"      # intelligibility
    "treble=g=4.6:f=3500:width_type=q:width=0.7,"   # the air a lav never has
    "agate=threshold=0.010:ratio=1.6:range=0.5:attack=3:release=300:knee=8,"
    "acompressor=threshold=0.10:ratio=3:attack=10:release=200:makeup=1.7,"
    "pan=stereo|c0=c0|c1=c0"                 # a talking head belongs dead centre
)

def chain(total):
    return (
        f"[0:a]{VOICE},asplit=2[vmix][vkey];"
        # the bed is 143 s and the ad is 236 s: loop it, with the loop point crossfaded
        f"[1:a]aloop=loop=2:size={int(140*44100)},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
        f"volume={MUSIC_DB}dB,afade=t=in:st=0:d=1.0,"
        f"afade=t=out:st={total - MUSIC_FADE:.3f}:d={MUSIC_FADE}[mus];"
        # long release: a short one lets the bed spring back between words, which is
        # where it masked a quiet "n't" on the 60 s sample
        f"[mus][vkey]sidechaincompress=threshold=0.020:ratio=9:attack=12:release=420:"
        f"makeup=1:level_sc=1[duck];"
        f"[2:a]volume={SFX_DB}dB[sfx];"
        f"[vmix][duck][sfx]amix=inputs=3:duration=first:normalize=0,"
        f"aresample=48000[premix]"
    )

def measure(fc):
    p = subprocess.run([FF, "-nostdin", "-hide_banner", "-nostats", "-i", VIDEO,
                        "-i", MUSIC, "-i", f"{HERE}/sfxbed.wav", "-filter_complex",
                        fc + ";[premix]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
                        "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True)
    txt = p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1]
    return json.loads(txt)

def main():
    total = dur_of(VIDEO)
    C = cues()
    build_sfx_bed(total, C)
    fc = chain(total)
    m = measure(fc)
    print("measured:", {k: m[k] for k in ("input_i", "input_tp", "input_lra")})
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:"
          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", VIDEO, "-i", MUSIC,
                    "-i", f"{HERE}/sfxbed.wav", "-filter_complex", f"{fc};[premix]{ln}[aout]",
                    # -t: the overlay pass runs ~0.3 s past the audio because looped
                    # image inputs are padded; trim both streams back to the cut length
                    "-map", "0:v", "-map", "[aout]", "-t", f"{B.DUR:.3f}", "-c:v", "copy",
                    "-c:a", "pcm_s16le", OUT], check=True)
    print(OUT, "done")

if __name__ == "__main__":
    if "cues" in sys.argv:
        for t, n, g in cues(): print(f"  {t:7.2f}  {n:<12} {g}")
    else:
        main()
