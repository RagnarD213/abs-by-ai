#!/usr/bin/env python3
"""THE ONE VOICE CHAIN -- the approved audio3.py chain (website video rev 2: "you got it nailed"),
with the source track taken from pick_lav's JSON, dereverb when the room measures wet, and the
EQ FITTED to the reference per roll (voicefit lineage) instead of copied.

  python3 voice_chain.py --in <video|wav> --out <out.wav|.mov|.mp4> [--source audio_source.json]
         [--video picture.mp4] [--bed music.mp3 --bed-db -30] [--extra sfx.wav] [--comp]
         [--target -14] [--tp -2.5] [--no-fit] [--eq "<af>"] [--frame-lock picture.mp4]

Stages (length-preserving, so pictures stay frame-locked):
  pull      lav track only, mono, per `audio_source.json` (refuses without it unless --in is a WAV
            or --pull is given); refuses SILENT input -- a stacked `pan` asks for a channel that no
            longer exists and ffmpeg renders silence, not an error (it blanked 4.48 s of a short)
  dereverb  only if the raw lav's early decay > 55 ms (spray-tan params alpha .62 d1 20 d2 150
            floor -24 smooth .30); EDT before/after is logged and written to the sidecar
  fit       highpass 70 + 9 parametric bands + a treble shelf, iterated against the reference on the
            gate's own metric, damped and smoothed so it is a voice EQ and never a comb
  dynamics  downward expander between words (audio3 EXPAND); compressor OFF unless --comp (<= 1.5:1)
  image     pan=stereo|c0=c0|c1=c0 (centred), bed <= -30 dB ducked by the voice, optional SFX
  finish    measured gain + alimiter (NEVER loudnorm: it goes dynamic), limiter delay measured by
            cross-correlation and removed, -14 LUFS, true peak -2.5 in PCM so the AAC lands <= -1.5
The gate (audio_gate.py) is the judge, not this script -- run it on the delivered file.
"""
import argparse, json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import reference as R
from dereverb import dereverb

EXPAND = "agate=threshold=0.012:ratio=1.8:range=0.35:attack=4:release=250:knee=6"
COMPRESS = "acompressor=threshold=0.126:ratio=1.5:attack=12:release=220:makeup=1.0"
DEREVERB = dict(alpha=0.62, d1_ms=20, d2_ms=150, floor_db=-24.0, smooth=0.30)
EDT_WET = 55.0


def write_wav(path, x, sr=C.SR):
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()


def read_wav_mono(path):
    x = C.pcm(path, ac=1); return x


def pull(src, source_json, explicit_pull, work):
    """lav track -> mono 48 k WAV. Returns (wav path, description)."""
    lav = os.path.join(work, "lav.wav")
    if src.lower().endswith(".wav") and not explicit_pull and not source_json:
        x = C.pcm(src, ac=1); how = "wav as given"
        nch = C.probe_audio(src)[0]["channels"]
        if nch > 1: print(f"  ⚠ --in WAV has {nch} channels; folded to mono (if these are two mics, run pick_lav first)")
    else:
        if explicit_pull:
            amap, af, how = "0:a:0", explicit_pull, f"--pull {explicit_pull}"
        else:
            s = C.load_source(source_json or src)
            amap, af, how = s["map"], s["filter"], f"{s['verdict']}: -map {s['map']} -af {s['filter']}"
        x = C.pcm(src, af=af, amap=amap, ac=1)
    if len(x) < C.SR:
        raise SystemExit("pull produced under one second of audio -- wrong map/filter?")
    dead, quiet = C.silent_seconds(x)
    rms = 10 * np.log10((x ** 2).mean() + 1e-15)
    if rms < -55 or dead > max(2, 0.2 * (len(x) / C.SR)):
        raise SystemExit(f"PULLED AUDIO IS SILENT ({rms:.1f} dBFS, {dead} dead seconds) -- the pull filter asks for "
                         f"a channel that does not exist (a stacked `pan`?). Refusing to render silence.")
    write_wav(lav, x)
    return lav, x, how


def fit_eq(lav_wav, ref, work, iters=6, damp=0.75):
    """voicefit.py: iterate the 10 gains on the gate's own metric; smooth + clamp so it is a voice EQ."""
    ss, dur = C.analysis_window(lav_wav)
    rb = np.array(ref["bands"])
    def chain(g):
        parts = ["highpass=f=70"]
        for c, gain in zip(C.CENTRES[:-1], g[:-1]):
            if abs(gain) >= 0.15: parts.append(f"equalizer=f={c}:t=q:w=1.3:g={gain:+.2f}")
        if abs(g[-1]) >= 0.15: parts.append(f"treble=g={g[-1]:+.2f}:f=6500:width_type=q:width=0.6")
        return ",".join(parts)
    def err_of(af):
        b, _, _, _ = C.analyse(C.pcm(lav_wav, af=af, ss=ss, dur=dur)); return b - rb
    g = np.zeros(10); err = err_of("highpass=f=70")
    print(f"  fit: raw tone error mean {np.abs(err).mean():.2f} dB, max {np.abs(err).max():.2f}")
    best = (np.abs(err).mean(), chain(g), g.copy())
    for it in range(iters):
        g = g - damp * err
        g[1:-1] = 0.15 * g[:-2] + 0.70 * g[1:-1] + 0.15 * g[2:]       # neighbours cannot alternate
        g = np.clip(g, -8, 8)
        af = chain(g); err = err_of(af)
        m = np.abs(err).mean()
        print(f"  fit {it+1}: mean {m:.2f} max {np.abs(err).max():.2f}  gains {np.round(g,1).tolist()}")
        if m < best[0]: best = (m, af, g.copy())
        if m < 0.35: break
    print(f"  fitted EQ (mean {best[0]:.2f} dB): {best[1]}")
    return best[1], [round(float(v), 2) for v in best[2]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="src", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--source", help="audio_source.json from pick_lav (default: <in>.audio_source.json)")
    ap.add_argument("--pull", help="explicit pull filter (testing only; production reads audio_source.json)")
    ap.add_argument("--video", help="picture to mux onto (-c:v copy); default: --in when it has video")
    ap.add_argument("--bed"); ap.add_argument("--bed-db", type=float, default=-30.0)
    ap.add_argument("--extra", help="a pre-rendered SFX/extra track mixed at 0 dB")
    ap.add_argument("--comp", action="store_true"); ap.add_argument("--target", type=float, default=-14.0)
    ap.add_argument("--tp", type=float, default=-2.5); ap.add_argument("--no-fit", action="store_true")
    ap.add_argument("--eq", help="use this EQ chain instead of fitting")
    ap.add_argument("--no-dereverb", action="store_true")
    ap.add_argument("--frame-lock", help="pad/trim the output to exactly this picture's duration")
    ap.add_argument("--finish-only", action="store_true",
                    help="input is an already-finished STEREO mix (e.g. the reference's own mix): no pull/dereverb/fit/expander, just measured gain + limiter to target")
    ap.add_argument("--work", help="work dir (default beside --out)")
    A = ap.parse_args()
    work = A.work or os.path.join(os.path.dirname(os.path.abspath(A.out)), "_voice_chain"); os.makedirs(work, exist_ok=True)
    ref_audio, ref = R.resolve()
    log = dict(version=C.STAMP_VERSION, src=os.path.abspath(A.src), out=os.path.abspath(A.out))

    # ---- finish-only: skip straight to the measured gain + limiter on the mix as given
    if A.finish_only:
        lav = A.src; x = C.pcm(A.src, ac=1); how = "finish-only (mix as given, channels kept)"
        log["pull"] = how; print(f"voice_chain  {os.path.basename(A.src)}  {how}  {len(x)/C.SR:.2f} s")
        voice = "aformat=channel_layouts=stereo"; eq = gains = None; log["voice"] = voice
    else:
        lav, x, how = pull(A.src, A.source, A.pull, work); log["pull"] = how
        print(f"voice_chain  {os.path.basename(A.src)}  pull: {how}  {len(x)/C.SR:.2f} s")

        # ---- dereverb if wet
        ss, dur = C.analysis_window(lav)
        e0 = C.edt(C.pcm(lav, ss=ss, dur=dur)); log["edt_raw"] = round(e0, 1)
        if e0 > EDT_WET and not A.no_dereverb:
            y = dereverb(x, sr=C.SR, **DEREVERB); write_wav(lav, y)
            e1 = C.edt(C.pcm(lav, ss=ss, dur=dur)); log["edt_dereverb"] = round(e1, 1); log["dereverb"] = DEREVERB
            print(f"  room: EDT {e0:.0f} ms > {EDT_WET:.0f} -> dereverb -> {e1:.0f} ms (his {ref['edt_ms']:.0f})")
        else:
            print(f"  room: EDT {e0:.0f} ms (<= {EDT_WET:.0f}, his {ref['edt_ms']:.0f}) -- no dereverb")

        # ---- EQ
        if A.eq: eq, gains = A.eq, None
        elif A.no_fit: eq, gains = "highpass=f=70", None
        else: eq, gains = fit_eq(lav, ref, work)
        log["eq"] = eq; log["eq_gains"] = gains
        voice = ",".join(v for v in [eq, EXPAND, (COMPRESS if A.comp else ""), "pan=stereo|c0=c0|c1=c0"] if v)
        log["voice"] = voice

    # ---- graph: [0]=lav wav, [1]=bed?, [2]=extra?
    inputs = ["-i", lav]; n = 1; parts = []; total = len(x) / C.SR
    if A.frame_lock: total = C.duration(A.frame_lock, "v:0")
    elif A.video or C.has_video(A.src): total = C.duration(A.video or A.src, "v:0")
    if A.bed:
        inputs += ["-i", A.bed]; bi = n; n += 1
        parts.append(f"[0:a]{voice},asplit=2[vmix][vkey]")
        parts.append(f"[{bi}:a]aloop=loop=-1:size={int(600*44100)},atrim=0:{total:.3f},asetpts=PTS-STARTPTS,"
                     f"volume={A.bed_db}dB,afade=t=in:st=0:d=1.5,afade=t=out:st={max(0,total-2.0):.3f}:d=2.0[mus]")
        parts.append("[mus][vkey]sidechaincompress=threshold=0.020:ratio=6:attack=12:release=420:makeup=1:level_sc=1[duck]")
        parts.append("[vmix][duck]amix=inputs=2:duration=first:normalize=0[pm]")
    else:
        parts.append(f"[0:a]{voice}[pm]")
    if A.extra:
        inputs += ["-i", A.extra]; ei = n; n += 1
        parts.append(f"[pm][{ei}:a]amix=inputs=2:duration=first:normalize=0[pm2]"); last = "pm2"
    else: last = "pm"
    fc = ";".join(parts) + f";[{last}]aresample=48000[premix]"

    def render(extra, fmt_args):
        return subprocess.run([C.FF, "-nostdin", "-v", "error"] + inputs + ["-filter_complex", f"{fc};[premix]{extra}[a]",
                              "-map", "[a]"] + fmt_args, capture_output=True)
    def ebur(extra):
        p = subprocess.run([C.FF, "-nostdin", "-nostats"] + inputs + ["-filter_complex", f"{fc};[premix]{extra},ebur128=peak=true[a]",
                           "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True).stderr
        import re; g = lambda k: float(re.findall(rf"{k}:\s*(-?[\d.]+)", p)[-1]); return g("I"), g("Peak"), g("LRA")
    I0, TP0, LRA0 = ebur("anull"); print(f"  premix  I {I0:.2f}  TP {TP0:.2f}  LRA {LRA0:.2f}")
    gain = A.target - I0
    lim = f"alimiter=limit={10**(A.tp/20):.4f}:attack=5:release=60:level=false"
    # limiter delay measured on the real programme by cross-correlation (audio2.py lesson)
    pcmargs = ["-ac", "2", "-ar", "48000", "-f", "f32le", "-"]
    refx = np.frombuffer(render(f"volume={gain:.3f}dB", pcmargs).stdout, dtype=np.float32).reshape(-1, 2)[:, 0]
    limx = np.frombuffer(render(f"volume={gain:.3f}dB,{lim}", pcmargs).stdout, dtype=np.float32).reshape(-1, 2)[:, 0]
    s0 = int(min(ss, max(0, total - 25)) * C.SR); s1 = s0 + int(min(20, total - 1) * C.SR)
    _, delay, _ = C.xcorr(limx[s0:s1], refx[s0:s1], max_ms=15.0)
    delay = max(0, delay); log["limiter_delay_samples"] = delay
    def fin(g):
        return f"volume={g:.3f}dB,{lim}" + (f",atrim=start_sample={delay},asetpts=N/SR/TB" if delay > 0 else "") + \
               f",apad=whole_dur={total:.3f},atrim=0:{total:.3f}"
    I1, TP1, LRA1 = ebur(fin(gain)); print(f"  gain {gain:+.2f} dB (limiter delay {delay}) -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
    for _ in range(3):                      # the limiter eats part of each trim; converge, do not assume
        if abs(I1 - A.target) <= 0.3: break
        gain += (A.target - I1); I1, TP1, LRA1 = ebur(fin(gain)); print(f"  gain {gain:+.2f} dB -> I {I1:.2f}  TP {TP1:.2f}  LRA {LRA1:.2f}")
    log.update(gain_db=round(gain, 2), lufs=round(I1, 2), tp_pcm=round(TP1, 2), lra=round(LRA1, 2), duration=round(total, 3))

    out = A.out; ext = out.lower().rsplit(".", 1)[-1]
    pic = A.video or (A.src if C.has_video(A.src) and ext in ("mov", "mp4") else None)
    cmd = [C.FF, "-nostdin", "-y", "-v", "error"] + inputs
    if pic: cmd += ["-i", pic]
    cmd += ["-filter_complex", f"{fc};[premix]{fin(gain)}[aout]"]
    if pic: cmd += ["-map", f"{n}:v", "-map", "[aout]", "-c:v", "copy"]
    else: cmd += ["-map", "[aout]"]
    if ext == "mp4": cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart"]
    else: cmd += ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"]
    cmd += ["-t", f"{total:.3f}", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr)
    json.dump(log, open(out + ".voice_chain.json", "w"), indent=1)
    print(f"  wrote {out}  ({total:.2f} s)  sidecar {os.path.basename(out)}.voice_chain.json\n  now: audio_gate.py {out}")


if __name__ == "__main__": main()
