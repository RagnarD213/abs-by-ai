#!/usr/bin/env python3
"""STEP 0b -- the editor's HD export, checked against the draft Dan last approved, BEFORE any cut.

Dan, 2026-09-11: "watch the video once before making the cut, just to ensure the high-definition
version is exactly the same as the last approved draft and that no new errors got introduced in
the high-definition version. This way, I can skip watching that final export."

So this is Dan's watch of the HD, done for him. The draft is the file his last round of notes was
written against; everything that is frame-identical to it he has already seen and approved. What
is left to look at is (a) every window where the HD differs, and (b) the faults an export can add
that the draft cannot show: a truncated audio stream, a silent second, clipping, a new frozen or
black run, a shifted timeline, a fake-HD upscale, the wrong frame size.

Usage:
    python3 hd_vs_draft.py --hd HIS_HD.mp4 --draft APPROVED_DRAFT.mp4 --out WORKDIR/hdcheck

Writes WORKDIR/hdcheck/hd_vs_draft.json (every measurement), strips/ (HD over draft, consecutive
frames at the start and end of every changed window, full resolution) and spot/ (ten full-res HD
frames). Exit 0 = IDENTICAL, nothing new. Exit 1 = the HD differs: every changed window must be
matched to one of Dan's notes before the cut starts. Exit 2 = an export fault or a check that
could not run -- stop and tell Dan; the vertical inherits the HD exactly.

Calibration (measured, not assumed): Ad 5, Muhammad's V3 HD vs the 1080p review copy the round-3
notes were written against -- per-frame MAD max 0.94 of 255, audio corr 0.9994, level within
0.03 dB. Ad 2, V1 480p vs V2 HD (`a2/refdiff.py`, where the MAD > 6 threshold comes from) --
exactly the five windows Muhammad had changed, nothing else.
"""
import argparse, json, os, subprocess, sys
import numpy as np

BIN = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin"
FF, FP = f"{BIN}/ffmpeg", f"{BIN}/ffprobe"
W, H = 96, 54            # grey thumbnails for the per-frame diff
MAD_THR = 6.0            # a changed frame (a2/refdiff.py calibration)
FREEZE_MAD, FREEZE_MIN = 0.15, 15   # a frozen run: >= 0.5 s of frames that do not move
BLACK_LUMA = 16.0
SR = 16000

R = []                   # (status, name, detail) -- status PASS / DIFF / FAIL
def row(status, name, detail): R.append((status, name, detail)); print(f"  {status:4}  {name}: {detail}")


def probe(p):
    j = json.loads(subprocess.run([FP, "-v", "error", "-show_streams", "-show_format", "-of", "json", p],
                                  capture_output=True, text=True, check=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    num, den = map(int, v["r_frame_rate"].split("/"))
    return {"w": int(v["width"]), "h": int(v["height"]), "fps": num / den, "fps_str": v["r_frame_rate"],
            "vcodec": v["codec_name"], "v_dur": float(v.get("duration") or j["format"]["duration"]),
            "a_dur": float(a["duration"]) if a and a.get("duration") else None,
            "a_ch": int(a["channels"]) if a else 0, "a_sr": int(a["sample_rate"]) if a else 0,
            "bitrate_kbps": round(int(j["format"].get("bit_rate", 0)) / 1000)}


def grey(p, fps_str):
    """Every frame at its own rate (never a -ss seek, never an -r resample unless the rates differ)."""
    b = subprocess.run([FF, "-v", "error", "-i", p, "-vf", f"fps={fps_str},scale={W}:{H}:flags=area,format=gray",
                        "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    n = len(b) // (W * H)
    return np.frombuffer(b[:n * W * H], np.uint8).reshape(n, H, W).astype(np.float32)


def pcm(p):
    return np.frombuffer(subprocess.run([FF, "-v", "error", "-i", p, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                        capture_output=True, check=True).stdout, np.float32)


def flat_clips(p):
    """Clipped runs on the NATIVE decode. A mono 16 kHz downmix invents 'clipped' samples: the Ad 5 HD
    at -1.0 dBTP read 8,901 of them that way and 0 natively."""
    ch = probe(p)["a_ch"] or 1
    m = np.abs(np.frombuffer(subprocess.run([FF, "-v", "error", "-i", p, "-vn", "-f", "f32le", "-"],
                                            capture_output=True, check=True).stdout, np.float32).reshape(-1, ch))
    c = 0
    for k in range(ch):
        d = np.diff(np.concatenate([[0], (m[:, k] >= 0.999).astype(np.int8), [0]]))
        c += int(((np.where(d == -1)[0] - np.where(d == 1)[0]) >= 3).sum())
    return c


def ebur(p):
    e = subprocess.run([FF, "-hide_banner", "-nostats", "-i", p, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    tail = e[e.rfind("Summary:"):]
    def num(key):
        for ln in tail.splitlines():
            if ln.strip().startswith(key):
                return float(ln.split(":")[1].split()[0])
        return None
    return {"lufs": num("I:"), "lra": num("LRA:"), "tp": num("Peak:")}


def runs(mask, merge=15):
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j < n and mask[j]: j += 1
            if out and i - out[-1][1] < merge: out[-1] = (out[-1][0], j)
            else: out.append((i, j))
            i = j
        else: i += 1
    return out


def frames_at(p, idx, w):
    """Exact frames BY INDEX, full res scaled to width w (A7.12: a time seek lands on the wrong frame)."""
    idx = sorted(set(int(i) for i in idx))
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    b = subprocess.run([FF, "-v", "error", "-i", p, "-vf", f"select='{sel}',scale={w}:-2,format=rgb24",
                        "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True).stdout
    return idx, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hd", required=True); ap.add_argument("--draft", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(f"{a.out}/strips", exist_ok=True); os.makedirs(f"{a.out}/spot", exist_ok=True)
    from PIL import Image, ImageDraw

    ph, pd = probe(a.hd), probe(a.draft)
    print(f"HD    {ph['w']}x{ph['h']} {ph['fps_str']} {ph['v_dur']:.3f}s {ph['bitrate_kbps']} kb/s")
    print(f"draft {pd['w']}x{pd['h']} {pd['fps_str']} {pd['v_dur']:.3f}s {pd['bitrate_kbps']} kb/s")

    # ---- 1. the export itself -------------------------------------------------------------
    row("PASS" if ph["h"] >= 1080 and ph["w"] * 9 == ph["h"] * 16 else "FAIL", "frame size is 16:9 HD",
        f"{ph['w']}x{ph['h']}")
    row("PASS" if ph["fps_str"] == pd["fps_str"] else "FAIL", "frame rate matches the draft",
        f"HD {ph['fps_str']} vs draft {pd['fps_str']} (a changed rate re-times every cut; skill A6.1)")
    if ph["a_dur"] is None:
        row("FAIL", "HD has an audio stream", "none found")
    else:
        row("PASS" if abs(ph["a_dur"] - ph["v_dur"]) < 0.15 else "FAIL", "audio STREAM runs the full picture",
            f"audio {ph['a_dur']:.3f}s vs video {ph['v_dur']:.3f}s (qc check 16: a mux once truncated at 2:24 and exited 0)")

    # ---- 2. picture, frame by frame ---------------------------------------------------------
    gh, gd = grey(a.hd, ph["fps_str"]), grey(a.draft, ph["fps_str"])
    row("PASS" if len(gh) == len(gd) else "DIFF", "frame count matches the draft", f"HD {len(gh)} vs draft {len(gd)}")
    # a shifted timeline (an extra frame at the head) makes every frame "different": find the lag first
    m = min(len(gh), len(gd), 900) - 30
    def lag_err(L):
        a_, b_ = (gh[L:L + m], gd[:m]) if L >= 0 else (gh[:m], gd[-L:-L + m])
        return float(np.abs(a_ - b_).mean())
    lag = min(range(-30, 31), key=lag_err)
    row("PASS" if lag == 0 else "DIFF", "timeline starts on the same frame", f"best lag {lag:+d} frames (HD vs draft)")
    if lag > 0: gh_al, gd_al = gh[lag:], gd
    else:       gh_al, gd_al = gh, gd[-lag:]
    n = min(len(gh_al), len(gd_al))
    mad = np.abs(gh_al[:n] - gd_al[:n]).mean(axis=(1, 2))
    np.save(f"{a.out}/mad.npy", mad)
    fps = ph["fps"]
    changed = runs(mad > MAD_THR)
    noise = float(np.percentile(mad, 99))
    row("PASS" if not changed else "DIFF", "picture identical to the draft",
        f"{len(changed)} changed window(s); MAD median {np.median(mad):.2f} p99 {noise:.2f} max {mad.max():.2f}")
    for s, e in changed:
        print(f"        CHANGED {s/fps:8.2f}-{e/fps:8.2f}s  frames {s+max(lag,0)}-{e+max(lag,0)} ({e-s} fr)  "
              f"mean MAD {mad[s:e].mean():.1f}")
    # frames past the shorter file are compared to nothing -- report them, never drop them silently
    tail = len(gh_al) - len(gd_al)
    row("PASS" if tail == 0 else "DIFF", "the end lines up with the draft",
        "same last frame" if tail == 0 else
        (f"HD runs {tail} frames ({tail/fps:.2f}s) PAST the draft's end at {n/fps:.2f}s -- an added end hold?"
         if tail > 0 else f"HD stops {-tail} frames ({-tail/fps:.2f}s) BEFORE the draft's end at {len(gd_al)/fps:.2f}s"))

    # frozen or black runs in the HD that the draft does not have (a new export fault)
    mh = np.abs(np.diff(gh_al[:n], axis=0)).mean(axis=(1, 2))
    md = np.abs(np.diff(gd_al[:n], axis=0)).mean(axis=(1, 2))
    new_freeze = [(s, e) for s, e in runs(mh < FREEZE_MAD, merge=1)
                  if e - s >= FREEZE_MIN and (md[s:e] < FREEZE_MAD).mean() < 0.8]
    row("PASS" if not new_freeze else "FAIL", "no NEW frozen run in the HD",
        "; ".join(f"{s/fps:.2f}-{e/fps:.2f}s" for s, e in new_freeze) or "none")
    lh, ld = gh_al[:n].mean(axis=(1, 2)), gd_al[:n].mean(axis=(1, 2))
    new_black = [(s, e) for s, e in runs((lh < BLACK_LUMA) & (ld >= BLACK_LUMA), merge=1)]
    row("PASS" if not new_black else "FAIL", "no NEW black frame in the HD",
        "; ".join(f"{s/fps:.2f}s ({e-s} fr)" for s, e in new_black) or "none")

    # ---- 3. audio, second by second -----------------------------------------------------------
    x, y = pcm(a.draft), pcm(a.hd)
    L = min(len(x), len(y))
    seg = slice(10 * SR, min(L, 20 * SR))
    xs, ys = x[seg] - x[seg].mean(), y[seg] - y[seg].mean()
    alag = max(range(-800, 801, 4), key=lambda q: float(np.dot(xs[800:-800], ys[800 + q:len(ys) - 800 + q])))
    row("PASS" if abs(alag) <= 8 else "DIFF", "audio starts in sync with the draft", f"lag {alag/SR*1000:+.1f} ms")
    if alag > 0: y = y[alag:]
    else:        x = x[-alag:]
    L = min(len(x), len(y)); secs = L // SR
    diff_s, silent_s, cors = [], [], []
    for s in range(secs):
        xa, ya = x[s*SR:(s+1)*SR], y[s*SR:(s+1)*SR]
        rx, ry = np.sqrt((xa**2).mean() + 1e-12), np.sqrt((ya**2).mean() + 1e-12)
        if 20 * np.log10(ry) < -60 and 20 * np.log10(rx) >= -60: silent_s.append(s)
        c = float(np.corrcoef(xa, ya)[0, 1]) if rx > 1e-4 and ry > 1e-4 else 1.0
        g = float(20 * np.log10(ry / rx)); cors.append(c)
        if c < 0.95 or abs(g) > 1.0: diff_s.append((s, round(c, 3), round(g, 2)))
    row("PASS" if not silent_s else "FAIL", "no NEW silent second in the HD", str(silent_s) if silent_s else "none")
    row("PASS" if not diff_s else "DIFF", "mix identical to the draft, second by second",
        f"median corr {np.median(cors):.4f}; {len(diff_s)} second(s) differ" +
        ("".join(f"\n        AUDIO {s//60}:{s%60:04.1f}  corr {c:.3f}  gain {g:+.2f} dB" for s, c, g in diff_s[:60])))
    clip_h, clip_d = flat_clips(a.hd), flat_clips(a.draft)
    row("PASS" if clip_h <= clip_d else "FAIL", "no NEW clipped runs (>= 3 samples flat at full scale, native decode)",
        f"HD {clip_h} vs draft {clip_d}")
    eh, ed = ebur(a.hd), ebur(a.draft)
    row("PASS" if None not in eh.values() else "FAIL", "loudness measured",
        f"HD {eh['lufs']} LUFS / LRA {eh['lra']} / TP {eh['tp']} dBTP  vs draft {ed['lufs']} / {ed['lra']} / {ed['tp']}"
        " (a TP change is often the fix Dan asked for -- say so)")

    # ---- 4. is it really HD? (an upscaled draft passes every row above) -----------------------
    # Energy above ~0.36 cycles/px on a 1920-wide frame exists only if the source had more than ~720 lines.
    # Measured 2026-09-11: Ad 5 HD -11.7 dB; the same frames upscaled from 540p -20.0 / -19.3, from 720p -19.0.
    spot = np.linspace(0.05, 0.95, 10) * (len(gh) - 1)
    idx, raw = frames_at(a.hd, spot, 1920)
    fr = np.frombuffer(raw, np.uint8).reshape(len(idx), -1, 1920, 3)
    def hi_mid_db(img):
        g = img.astype(np.float32).mean(axis=2); F = np.abs(np.fft.rfft2(g - g.mean())) ** 2
        r = np.maximum(np.abs(np.fft.fftfreq(g.shape[0]))[:, None], np.fft.rfftfreq(g.shape[1])[None, :])
        return float(10 * np.log10(F[(r > 0.36) & (r < 0.5)].sum() / F[(r > 0.08) & (r < 0.2)].sum()))
    vals = []
    for i, f in zip(idx, fr):
        Image.fromarray(f).save(f"{a.out}/spot/hd_{i:06d}.png"); vals.append(hi_mid_db(f))
    dr = float(np.median(vals))
    row("PASS" if dr > -16.0 else "FAIL", "HD carries detail an upscale cannot",
        f"high/mid band {dr:.1f} dB (real 1080p ~ -12; upscaled from 540p/720p ~ -19 to -20; gate -16)")

    # ---- 5. strips for the eye: every changed window, HD over draft, consecutive frames ---------
    for wi, (s, e) in enumerate(changed):
        for tag, c in (("in", s), ("out", e)):
            want = [c + d for d in (-2, -1, 0, 1, 2) if 0 <= c + d < n]
            ih, bh = frames_at(a.hd, [w + max(lag, 0) for w in want], 384)
            idr, bd = frames_at(a.draft, [w + max(-lag, 0) for w in want], 384)
            th = np.frombuffer(bh, np.uint8).reshape(len(ih), -1, 384, 3)
            td = np.frombuffer(bd, np.uint8).reshape(len(idr), -1, 384, 3)
            hh = th.shape[1]; sheet = Image.new("RGB", (384 * len(want), hh * 2 + 20), "black")
            for j in range(min(len(th), len(td))):
                sheet.paste(Image.fromarray(th[j]), (384 * j, 20)); sheet.paste(Image.fromarray(td[j]), (384 * j, 20 + hh))
            ImageDraw.Draw(sheet).text((4, 4), f"window {wi+1} {tag} @ {c/fps:.2f}s  TOP = HD  BOTTOM = draft  "
                                               f"frames {want[0]} to {want[-1]}", fill="yellow")
            sheet.save(f"{a.out}/strips/w{wi+1:02d}_{tag}_{c/fps:07.2f}s.png")

    fails = [r for r in R if r[0] == "FAIL"]; diffs = [r for r in R if r[0] == "DIFF"]
    verdict = "EXPORT FAULT" if fails else ("DIFFERS" if diffs else "IDENTICAL")
    json.dump({"hd": a.hd, "draft": a.draft, "probe_hd": ph, "probe_draft": pd, "verdict": verdict,
               "rows": [{"status": s, "name": nm, "detail": d} for s, nm, d in R],
               "picture_lag_frames": lag, "audio_lag_ms": alag / SR * 1000,
               "changed_windows": [{"t0": s / fps, "t1": e / fps, "frames": [s, e], "mean_mad": float(mad[s:e].mean())}
                                   for s, e in changed],
               "audio_diff_seconds": diff_s, "loudness_hd": eh, "loudness_draft": ed, "detail_ratio": dr},
              open(f"{a.out}/hd_vs_draft.json", "w"), indent=1)
    print(f"\nVERDICT: {verdict}  ({len(fails)} fail, {len(diffs)} differ)  -> {a.out}/hd_vs_draft.json")
    sys.exit(2 if fails else (1 if diffs else 0))


if __name__ == "__main__":
    try: main()
    except subprocess.CalledProcessError as e:   # a check that could not run is a FAILURE (AGENTS.md)
        print(f"FAIL: a measurement could not run: {e}"); sys.exit(2)
