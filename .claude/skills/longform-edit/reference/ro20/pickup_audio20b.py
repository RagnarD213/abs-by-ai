#!/usr/bin/env python3
"""RO-20 round 3b: Dan's four pickups re-recorded 2026-10-15 on the shoot lav (roll C1722, green screen set, left channel), cut to the
chosen takes and brought to the film voice. Same microphone as the film now, so the treatment starts from the film's own chain.
OPT=chain : the lav through voice_chain.py with voice 4's fixed EQ, no dereverb (room EDT 56 ms raw against the film's 52 ms after its
            light pass; not wet enough to need it), no expander (round3b/opts/chainA_nodr.wav), then level matched to the film's speech
OPT=match : the raw lav, 70 Hz high-pass, pickup_audio20's spectrum match with boosts capped at 0 dB, no synthetic room, no low cut
OPT=raw   : the raw lav, level matched only
Writes <OUT>/P#.voice.wav + words_P#.json. usage: OPT=chain OUT=dir pickup_audio20b.py"""
import json, os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("BOOST", "0"); os.environ.setdefault("LOWCUT", "0")
import pickup_audio20 as P
from scipy.signal import butter, sosfiltfilt, fftconvolve
W, SR = P.W, P.SR; R3B = f"{W}/round3b"
OPT = os.environ.get("OPT", "chain"); OUT = os.environ.get("OUT", f"{W}/round3/pickups"); os.makedirs(OUT, exist_ok=True)
SRC = f"{R3B}/src/c1722_lav_0-192_48k_mono.wav"            # roll C1722 0 to 192 s, -map 0:a:0 pan=mono|c0=c0 (pick_lav verdict single-live)
T = json.load(open(f"{R3B}/src/c1722_lav.transcript.json"))["words"]     # Whisper medium.en word times
TAKES = {"P1": [(35.90, 48.10)], "P2": [(53.00, 66.80)], "P3": [(116.30, 137.10)], "P4": [(166.05, 183.45)]}   # docs/PICKUPS_1017_SHOOT take map, last clean take (P2 take 1)
TAIL = {"P1": 0.45, "P2": 0.45, "P3": 5.4, "P4": 0.45}
FIXW = {"bawler.": "baller.", "bawler": "baller", ".com.": ".com."}
TRIM = float(os.environ.get("TRIM", "0"))                 # same mic as the film: level to the film's own active speech level
def main():
    film = np.concatenate([P.rd(f"{W}/voice/film_voice.wav", a, b) for a, b in ((840, 900), (905, 965), (1380, 1420), (1421, 1481))])
    F_act, F_lt = P.act_db(film), P.ltas(film); F_floor = np.percentile(P.frames_db(film, 4800), 3)
    raw = P.rd(SRC); sos = butter(2, 70, "hp", fs=SR, output="sos")
    if OPT == "chain": src = P.rd(f"{R3B}/opts/chainA_nodr.wav")
    elif OPT == "match":
        src = sosfiltfilt(sos, raw); sp = np.concatenate([src[int(a*SR):int(b*SR)] for r in TAKES.values() for a, b in r])
        h, g = P.match_fir(F_lt - P.ltas(sp) - (F_act - P.act_db(sp))); src = fftconvolve(src, h, "same")
        print("match EQ (dB, 79 Hz to 12.7 kHz):", " ".join(f"{v:+.1f}" for v in g))
    else: src = raw.copy()
    rep = {}
    for pid, rng in TAKES.items():
        (a, b), = rng; ws = [w for w in T if a - 0.01 <= w["t0"] < b]
        s0 = a; end = ws[-1]["t1"] + TAIL[pid]; x = src[int(s0*SR):int(end*SR)].copy()
        n = int(0.010*SR); x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
        if TAIL[pid] > 1:                                  # P3 ends video 2: his room after the last word, faded over a second, then silence for the end screen
            i0 = int((ws[-1]["t1"] + 0.25 - s0)*SR); f = int(1.0*SR); x[i0:i0+f] *= np.linspace(1, 0, f); x[i0+f:] = 0
        words = [dict(w=FIXW.get(w["w"], w["w"]), t0=round(w["t0"] - s0, 3), t1=round(w["t1"] - s0, 3)) for w in ws]
        y = x
        for _ in range(4): y = P.limit(y*10**((F_act + TRIM - P.act_db(y))/20), -2.0)
        floor = np.percentile(P.frames_db(y[:int((ws[-1]['t1'] - s0)*SR)], 4800), 3); tone_added = False
        if floor < F_floor - 3:                            # keep the film's room tone under the pickup only if the floor would drop at the join
            tone, _ = P.film_tone(film, len(y)); y = y + tone; tone_added = True
        P.wr(f"{OUT}/{pid}.voice.wav", y)
        json.dump(dict(duration=round(len(y)/SR, 3), words=words, takes=rng, source=SRC, opt=OPT), open(f"{OUT}/words_{pid}.json", "w"), indent=0)
        err = P.ltas(y) - F_lt - (P.act_db(y) - F_act)
        rep[pid] = dict(seconds=round(len(y)/SR, 2), active=round(P.act_db(y), 1), film_active=round(F_act, 1), floor=round(float(floor), 1), film_floor=round(float(F_floor), 1),
                        tone_added=tone_added, peak=round(20*np.log10(np.abs(y).max()), 1), tone_err_mean=round(float(np.abs(err).mean()), 2), text=" ".join(w["w"] for w in words))
        print(pid, {k: v for k, v in rep[pid].items() if k != "text"}); print("   residual per band:", " ".join(f"{v:+.1f}" for v in err))
    json.dump(dict(opt=OPT, pickups=rep), open(f"{OUT}/pickup_audio_report.json", "w"), indent=1)
if __name__ == "__main__": main()
