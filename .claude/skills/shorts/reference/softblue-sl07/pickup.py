#!/usr/bin/env python3
"""SL-07 pickups (VIDEO-RULES 2026-10-11, "A Short opens like a dedicated video"). Dan records one sentence per short on
the desk Yeti; this makes it sit in front of the film's approved mix so the join is not heard.
  pickup.py asr RAW.wav                 Whisper word times of the recording -> pickups/<raw>.asr.json (+ prints the takes)
  pickup.py fit RAW.wav                 fit the tone EQ on ALL of his takes (about 40 s of speech) toward the FILM's voice on
                                        this roll (the gate's 10 bands, voice_chain.fit_eq), not the default reference
  pickup.py make X RAW.wav T0 T1        treat one take -> pickups/X.wav (stereo, exactly the head of short X) + X.report.json
What `make` does, in order: cut on silence with a short pad, the fitted EQ, level matched to the film line that follows it
(speech-frame RMS, the first 4 s after the join), a true-peak cap at the film's own peak, an 8 ms fade in and a 15 ms de-click at the join (RO-16's mix has no
music bed, so nothing runs under it).
No dereverb, no gate, no noise reduction (memory audio-never-over-strip): the room is measured and REPORTED, not chased."""
import json, os, subprocess, sys, wave
import numpy as np
ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
sys.path.insert(0, ROOT + "/.claude/skills/_shared/audio"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, voice_chain as VC
import plans as P
WORK = "/Volumes/Extreme/_edit_work/sl07"; PK = WORK + "/pickups"; SR = 48000
FF = C.FF
def rd(path, a=None, b=None):
    w = wave.open(path); sr, ch = w.getframerate(), w.getnchannels(); assert sr == SR, (path, sr)
    if a is not None: w.setpos(max(0, int(a * SR)))
    n = w.getnframes() - w.tell() if b is None else int((b - (a or 0)) * SR)
    return np.frombuffer(w.readframes(n), "<i2").astype(np.float64).reshape(-1, ch) / 32768
def wr(path, x):
    x = np.atleast_2d(x.T).T if x.ndim == 1 else x
    w = wave.open(path, "w"); w.setnchannels(x.shape[1]); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes()); w.close()
def speech_rms(x):
    """dB RMS of the speech frames (top 40 % of 2048-pt frames, the gate's own definition of speech)."""
    fr = C.frames(x, 2048, 1024); r = np.sqrt((fr ** 2).mean(1) + 1e-12); return float(20 * np.log10(np.sqrt((r[r > np.percentile(r, 60)] ** 2).mean())))
def film_ref():
    """the film's voice on this roll: 10 band levels of the approved mix's speech frames. RO-16's mix has no music bed
    (measured: its pauses sit 36 dB under its speech), so nothing runs under the pickup."""
    p = PK + "/film_ref.json"
    if os.path.exists(p): return json.load(open(p))
    x = rd(WORK + "/master_audio.wav", 587, 700).mean(1); b, fl, dry, spread = C.analyse(x)
    r = dict(bands=[float(v) for v in b], edt_ms=C.edt(x), dry=dry, peak=float(np.abs(rd(WORK + "/master_audio.wav")).max()),
             floor_db=float(20 * np.log10(np.sqrt((rd(WORK + "/master_audio.wav", 636.50, 636.85) ** 2).mean()) + 1e-9)))
    json.dump(r, open(p, "w"), indent=1); return r
def cmd_asr(raw):
    import whisper, scipy.signal as ss
    x = rd(raw).mean(1); a = ss.resample_poly(x, 16000, SR).astype(np.float32)
    r = whisper.load_model("small.en").transcribe(a, fp16=False, condition_on_previous_text=False, word_timestamps=True)
    ws = [dict(w=w["word"].strip(), t=round(w["start"], 3), e=round(w["end"], 3)) for s in r["segments"] for w in s["words"]]
    json.dump(dict(words=ws, segments=[dict(t=s["start"], e=s["end"], text=s["text"].strip()) for s in r["segments"]]), open(raw[:-4] + ".asr.json", "w"), indent=0)
    for s in r["segments"]: print("%7.2f-%7.2f %s" % (s["start"], s["end"], s["text"].strip()))
def cmd_fit(raw, spans):
    """spans: every take of every line [(t0, t1), ...]; the EQ is fitted on all of them joined."""
    x = np.concatenate([rd(raw, a - 0.05, b + 0.1).mean(1) for a, b in spans]); wr(PK + "/fit_in.wav", x)
    ref = film_ref(); os.makedirs(PK + "/fit", exist_ok=True)
    af, gains, _ = VC.fit_eq(PK + "/fit_in.wav", ref, PK + "/fit", iters=10)
    y = C.pcm(PK + "/fit_in.wav", af=af); b = C.analyse(y)[0]; err = b - np.array(ref["bands"])
    json.dump(dict(eq=af, gains=gains, tone_err_mean=float(np.abs(err).mean()), tone_err_max=float(np.abs(err).max()), edt_ms_yeti=C.edt(x), edt_ms_film=ref["edt_ms"]), open(PK + "/fit.json", "w"), indent=1)
    print("fitted:", af, "| tone error mean %.2f max %.2f dB | room: Yeti %.0f ms, film %.0f ms" % (np.abs(err).mean(), np.abs(err).max(), C.edt(x), ref["edt_ms"]))
def cmd_fit1(X, raw, t0, t1):
    """fit the tone EQ on ONE take (tiled 4x so the analysis has enough speech frames) toward the film's voice. The six-take
    fit left each take 3 to 6 dB off in single bands (his distance to the Yeti changes take to take) and a blind listener
    called both pickups boomy (listen/trials.json, 2026-10-13)."""
    x = np.tile(rd(raw, t0 - 0.02, t1 + 0.05).mean(1), 4); wr(PK + f"/fit_in_{X}.wav", x)
    ref = film_ref(); os.makedirs(PK + f"/fit_{X}", exist_ok=True)
    af, gains, _ = VC.fit_eq(PK + f"/fit_in_{X}.wav", ref, PK + f"/fit_{X}", iters=14)
    y = C.pcm(PK + f"/fit_in_{X}.wav", af=af); err = C.analyse(y)[0] - np.array(ref["bands"])
    json.dump(dict(eq=af, gains=gains, tone_err_mean=float(np.abs(err).mean()), tone_err_max=float(np.abs(err).max()), err=[float(v) for v in err],
                   edt_ms_yeti=json.load(open(PK + "/fit.json"))["edt_ms_yeti"], edt_ms_film=ref["edt_ms"]), open(PK + f"/fit_{X}.json", "w"), indent=1)
    print(X, "fitted:", af, "| tone error mean %.2f max %.2f dB |" % (np.abs(err).mean(), np.abs(err).max()), " ".join("%+.1f" % v for v in err))
def cmd_make(X, raw, t0, t1, lead=0.10, tail=0.16):
    ref = film_ref(); fit = json.load(open(PK + (f"/fit_{X}.json" if os.path.exists(PK + f"/fit_{X}.json") else "/fit.json"))); a = P.SEG[X][0][0]
    wr(PK + f"/{X}_cut.wav", rd(raw, t0 - lead, t1 + tail).mean(1))
    v = C.pcm(PK + f"/{X}_cut.wav", af=fit["eq"])
    film = rd(WORK + "/master_audio.wav", a, a + 4.0).mean(1)
    g = 10 ** ((speech_rms(film) - speech_rms(v)) / 20); v = v * g
    cap = ref["peak"]; pk = np.abs(v).max()
    if pk > cap:                                    # a soft knee onto the film's own peak, only where it is exceeded
        thr = cap * 0.8; over = np.abs(v) > thr; v[over] = np.sign(v[over]) * (thr + (cap - thr) * np.tanh((np.abs(v[over]) - thr) / (cap - thr)))
    n = len(v); k = int(0.008 * SR); v[:k] *= np.linspace(0, 1, k); k = int(0.015 * SR); v[-k:] *= np.linspace(1, 0, k)
    out = np.repeat(v[:, None], 2, 1); wr(PK + f"/{X}.wav", out)                 # dual mono, as the film's mix is (L/R correlation 1.000)
    ph = PK + f"/{X}.PLACEHOLDER"
    if os.path.exists(ph): os.remove(ph)
    rep = dict(short=X, raw=raw, take=[t0, t1], seconds=n / SR, gain_db=float(20 * np.log10(g)), speech_rms_pickup=speech_rms(v), speech_rms_film_next=speech_rms(film),
               peak=float(np.abs(out).max()), film_peak=cap, eq=fit["eq"], tone_err_mean=fit["tone_err_mean"], tone_err_max=fit["tone_err_max"],
               edt_ms_pickup=C.edt(np.concatenate([v] * 3)), edt_ms_film=ref["edt_ms"],
               floor_db_pickup=float(20 * np.log10(np.sqrt((v[:int(lead * SR * 0.8)] ** 2).mean()) + 1e-9)), floor_db_film=ref["floor_db"])
    json.dump(rep, open(PK + f"/{X}.report.json", "w"), indent=1); print(json.dumps(rep, indent=1))
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "asr": cmd_asr(sys.argv[2])
    elif c == "ref": print(json.dumps(film_ref(), indent=1))
    elif c == "fit": cmd_fit(sys.argv[2], json.loads(sys.argv[3]))
    elif c == "make": cmd_make(sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]))
    elif c == "fit1": cmd_fit1(sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]))
