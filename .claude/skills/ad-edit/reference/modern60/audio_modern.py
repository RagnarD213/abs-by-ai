#!/usr/bin/env python3
"""Modern-edit 60s sample -- audio: voice EQ + ducked music bed + transition SFX + loudnorm.

The reference edit's "sounds better" comes from three things our cuts never had: a bed
that runs the whole length, a whoosh/pop on every graphic entrance, and pauses short
enough that the bed carries the gaps. Steps 1 and 3 are elsewhere; this is 1 and 2.

  python3 audio_modern.py          # builds sfxbed.wav then modern_sample.mp4
"""
import importlib.util, json, subprocess, os
import numpy as np

SKILL = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference"
spec = importlib.util.spec_from_file_location("sfxlib", f"{SKILL}/sfxlib.py")
sfxlib = importlib.util.module_from_spec(spec); spec.loader.exec_module(sfxlib)

FF    = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FFP   = FF.replace("ffmpeg", "ffprobe")
VIDEO = "modern_nocap.mov"
MUSIC = "music/Werq.mp3"          # Kevin MacLeod, incompetech.com -- CC BY 4.0 (attribution)
OUT   = "modern_sample.mp4"
SR    = sfxlib.SR

# Music sits ~18 dB below its own level before ducking; the sidechain then pulls it a
# further ~7 dB under speech, landing the bed near -20 dB relative to the voice.
MUSIC_DB   = -19.0
MUSIC_FADE = 1.4
# One-shots are normalised to full scale, so summed raw they land AT dialogue level and
# read as jarring. Measured target: SFX rms ~10 dB under the speech rms.
SFX_DB     = -11.0

# graphic entrance -> one-shot. Fired ~60 ms early so the transient leads the motion.
LEAD = 0.06
CUES = [
    (0.20,  "whoosh_soft", 0.55),   # callout stroke draws around the door photo
    (3.62,  "whoosh",      0.80),   # goal-picture card in
    (6.10,  "pop",         0.55),   # card swaps to the before photo
    (6.62,  "pop_soft",    0.60),   # "200 POUNDS" letters snap in
    (7.86,  "whoosh",      0.75),   # phone card in
    (9.72,  "whoosh_out",  0.45),   # phone card out
    (12.74, "whoosh",      0.70),   # today b-roll card in
    (14.79, "whoosh",      0.85),   # bullets panel slides in
    (14.79, "sub",         0.55),   # weight under the layout change
    (17.21, "pop_soft",    0.60),
    (20.90, "pop_soft",    0.60),
    (25.40, "pop_soft",    0.60),
    (29.49, "whoosh_out",  0.60),   # panel out
    (39.97, "whoosh_soft", 0.60),   # lower third slides in
    (46.30, "riser",       0.55),   # lift into the title card (lands on 47.05)
    (47.05, "whoosh",      0.80),
    (47.05, "sub",         0.50),
    (50.60, "whoosh_out",  0.55),   # title card out
    (59.02, "whoosh",      0.75),   # photoshop card in
    (63.62, "whoosh_out",  0.55),
]

def dur_of(path):
    return float(subprocess.run([FFP, "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", path], capture_output=True,
                                text=True).stdout.strip())

def build_sfx_bed(total):
    """Sum every one-shot into a single full-length stereo WAV.

    One pre-summed bed beats a chain of adelay/amix pairs: the filtergraph stays small,
    and levels are set in one place where they can be measured.
    """
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
    sfxlib.save("sfxbed.wav", bed[:int(total * SR)])
    print(f"sfxbed.wav  {len(CUES)} cues, peak {np.abs(bed).max():.2f}")

def measure(fc):
    """First loudnorm pass -- returns the measured values for the second."""
    p = subprocess.run([FF, "-nostdin", "-hide_banner", "-nostats", "-i", VIDEO,
                        "-i", MUSIC, "-i", "sfxbed.wav", "-filter_complex",
                        # a labelled output ends a chain -- the next filter needs its
                        # own link, not a comma
                        fc + ";[premix]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
                        "-map", "[a]", "-f", "null", "-"],
                       capture_output=True, text=True)
    txt = p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1]
    return json.loads(txt)

def main():
    total = dur_of(VIDEO)
    build_sfx_bed(total)
    chain = (
        # VOICE. Measured against the trial edit's own voice spectrum (2026-08-22):
        # ours was 5.5 dB down at 400-700 Hz and 4.2 dB down at 700-1200 Hz (thin, so
        # the voice reads as distant) while sitting 3 dB HOT at 3.2-8 kHz, which is
        # exactly the band the room's reverb lives in. That combination is what Dan
        # heard as echo. Fix the tilt, then expand the tails down.
        f"[0:a]highpass=f=75,"
        f"equalizer=f=530:t=q:w=1.0:g=4.5,"          # body
        f"equalizer=f=920:t=q:w=1.2:g=3.5,"          # chest / fullness
        f"equalizer=f=1550:t=q:w=1.4:g=1.5,"
        f"equalizer=f=4000:t=q:w=1.0:g=-3.2,"        # take the room off the top
        f"equalizer=f=6300:t=q:w=1.0:g=-2.2,"
        # Downward expander: pulls the reverb tail between words down. This is the
        # actual de-reverb; the EQ only stops the room being emphasised. Deliberately
        # GENTLE -- at threshold 0.030 / ratio 2.4 it ate the /f/ in "for free" and the
        # "n't" in "isn't", and the re-transcription QC caught it (97.9% -> 96.0%).
        # A fast attack matters more than depth: it must be open before the consonant.
        f"agate=threshold=0.018:ratio=1.8:range=0.45:attack=3:release=300:knee=8,"
        # gentle compression -- his read as "flatter", and a steadier voice also stops
        # the sidechain from pumping the music bed
        f"acompressor=threshold=0.10:ratio=3:attack=10:release=200:makeup=1.7,"
        f"asplit=2[vmix][vkey];"
        f"[1:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume={MUSIC_DB}dB,"
        f"afade=t=in:st=0:d=0.8,afade=t=out:st={total - MUSIC_FADE:.3f}:d={MUSIC_FADE}[mus];"
        # the bed ducks itself out of the way of every syllable
        # release is deliberately LONG: a short release lets the bed spring back up
        # between words, which is where it masked the quiet "n't" in "isn't"
        f"[mus][vkey]sidechaincompress=threshold=0.020:ratio=9:attack=12:release=420:"
        f"makeup=1:level_sc=1[duck];"
        f"[2:a]volume={SFX_DB}dB[sfx];"
        f"[vmix][duck][sfx]amix=inputs=3:duration=first:normalize=0,"
        f"aresample=48000[premix]"
    )
    m = measure(chain)
    print("measured:", {k: m[k] for k in ("input_i", "input_tp", "input_lra", "input_thresh")})
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:"
          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", VIDEO, "-i", MUSIC,
                    "-i", "sfxbed.wav", "-filter_complex", f"{chain};[premix]{ln}[aout]",
                    "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", OUT], check=True)
    print(OUT, "done")

if __name__ == "__main__":
    main()
