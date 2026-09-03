#!/usr/bin/env python3
"""THE ONE AUDIO GATE. Measures the DELIVERED file against the pinned reference and STAMPS it.

  python3 audio_gate.py <finished.mp4|.mov|.wav> [--synthetic] [--ab out.mp4] [--video picture.mp4]
                        [--ref other.mp4] [--no-stamp] [--reference-rows-only]

Rows (each traces to something Dan rejected on, or to the platform standard):
  1 one voice, not two mics    L/R correlation at lag 0                >= +0.97
  1b no comb                   spectral ripple 300-6k (two mics summed) <= ref + 0.35 dB
  2 a dry room                 early decay time after a word            <= 80 ms   (his 40; approved rev 2 = 75; the rejected batch 85)
  3 tone                       10-band speech spectrum vs his           mean <= 1.2 dB, max <= 2.5
  4 clean between words        voice-over-floor 80-250 / 250-1k / 1-4k  within 3 dB of his
  5 words stop cleanly         level drop 64 ms after a word            >= his - 1.5 dB
  6 loud enough                integrated loudness                      -14 +/-1 LUFS
  7 not crushed                speech spread p90-p10 (speech frames)    >= his - 3.0 dB; LRA reported
  8 no clipping on phones      true peak of the delivered file          <= -1.0 dBTP (platform ceiling; the chain lands -2.5 in PCM)
  9 nothing missing            digitally silent seconds 0; audio length within 0.10 s of the picture

--synthetic (make-ad, exercise demos: an AI voice, no camera) keeps 6, 8, 9 and the L/R row.
The stamp `<file>.audio_gate.json` carries the file's sha256 + every number + PASS/FAIL, and
require_stamp.py is what every QC and delivery script calls. No stamp = not deliverable.
--ab writes his three sentences then ours, for Dan's ear, and its path goes in the stamp.
"""
import argparse, json, os, subprocess, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import reference as R

# ⚠ EVERY LIMIT TRACES TO A FILE DAN APPROVED OR REJECTED, not to "his number + margin" (2026-09-02):
#   edt 80     approved: website video rev 2 = 75 ms ("you got it nailed"); rejected: spray-tan short = 85 ("echoey");
#              his = 40. The chain dereverbs anything over EDT_WET=55, so what we render lands near his.
#   spread 3.0 approved: Ad 2 rev 2 = 7.6 dB, website rev 2 = 5.5 (his 8.2). No crushed rejection measured
#              yet -- tighten this when one is (the Ad-1 vertical loudnorm case, if that file turns up).
#   tp -1.0    the platform ceiling; Ad 2 rev 2 measures -1.30 (the handoff's -1.5 was a mis-measurement).
#   the rest   the handoff's table, unchanged (tone / floor / dryness were what rev 1 and spray-tan failed on).
LIM = dict(corr=0.97, comb_margin=0.35, edt=80.0, tone_mean=1.2, tone_max=2.5, floor=3.0, dry=1.5,
           lufs=-14.0, lufs_tol=1.0, spread=3.0, tp=-1.0, silent=0, length=0.10)


def gate(path, synthetic=False, ab=None, video=None, ref_override=None, stamp=True, ref_rows_only=False,
         reference_mix=None):
    if ref_override:
        ref_audio, ref = ref_override, R.measure(ref_override)
    else:
        ref_audio, ref = R.resolve()
    ss, dur = C.analysis_window(path)
    st = C.pcm(path, ss=ss, dur=dur, ac=2)
    mono = st.mean(1)
    rows, info_rows = [], []
    def row(key, ok, text, val, gated=True):
        if not gated:
            # REFERENCE-MIX MODE: this row measures the EDITOR'S OWN MIXING (his bed between the
            # words, his tone), not our chain, so it is recorded but cannot fail the file.
            info_rows.append(dict(key=key, ok=bool(ok), text=text, value=val)); print("  info  " + text + "   [his mix, not gated]"); return
        rows.append(dict(key=key, ok=bool(ok), text=text, value=val))
        print(("  PASS  " if ok else "  FAIL  ") + text)
    print(f"audio_gate  {os.path.basename(path)}  window {ss:.0f}s +{dur:.0f}s  vs  {ref['name']}"
          + ("  [synthetic]" if synthetic else "") + ("  [reference mix]" if reference_mix else ""))
    prov = None
    if reference_mix:
        # --reference-mix (shortad-from-longform, 2026-09-03): the delivered audio IS the editor's
        # finished mix moved by one constant gain. PROVENANCE IS VERIFIED, NOT ASSUMED: per-second,
        # level-normalised correlation against that mix must be >= 0.99 at the median (the qc.py
        # check that separated his mix from a loudnorm'd one at 0.970), or the flag is refused.
        # With provenance proven, comb / room / tone / floor / dryness / spread measure HIS mixing
        # (Ad 2's bed sits 6-7 dB hotter between words than Ad 1's, the pinned reference) and are
        # reported as information; loudness, true peak, silence, length and the L/R image still gate.
        a = C.pcm(path, ac=1); b = C.pcm(reference_mix, ac=1)
        n = min(len(a), len(b)); W = C.SR; cors = []
        for i in range(n // W):
            x, y = b[i*W:(i+1)*W], a[i*W:(i+1)*W]
            if np.sqrt((x ** 2).mean()) < 1e-3: continue
            x = x - x.mean(); y = y - y.mean(); d = np.sqrt((x ** 2).sum() * (y ** 2).sum())
            if d > 0: cors.append(float(np.dot(x, y) / d))
        prov = float(np.median(cors)) if cors else 0.0
        row("provenance", prov >= 0.99, f"reference mix: per-second level-normalised correlation with "
            f"{os.path.basename(reference_mix)} median {prov:.4f} over {len(cors)} s (>= 0.99)", round(prov, 4))
    G = not reference_mix          # rows that measure the editor's mixing gate only when the mix is ours
    # 1 image
    nch = C.probe_audio(path)[0]["channels"]
    if nch >= 2:
        L, Rr = st[:, 0], st[:, 1]
        corr = float(np.corrcoef(L, Rr)[0, 1]) if L.std() > 1e-6 and Rr.std() > 1e-6 else 0.0
    else: corr = 1.0
    if not ref_rows_only: row("lr_corr", corr >= LIM["corr"], f"one voice: L/R correlation {corr:+.4f} (>= +{LIM['corr']})", round(corr, 4))
    if not synthetic:
        bands, floor, dry, spread = C.analyse(mono)
        rb = np.array(ref["bands"]); rf = np.array(ref["floor"])
        err = np.abs(bands - rb)
        print("  band      ref    mix   diff")
        for lo, r_, o in zip(C.EDGES, rb, bands): print(f"  {lo:5d}Hz {r_:6.1f} {o:6.1f} {o-r_:+6.1f}")
        ripple = C.comb_ripple(mono)
        row("comb", ripple <= ref["comb_ripple"] + LIM["comb_margin"],
            f"no comb: spectral ripple {ripple:.2f} dB vs his {ref['comb_ripple']:.2f} (<= his + {LIM['comb_margin']})", round(ripple, 3), gated=G)
        e = C.edt(mono)
        row("edt", e <= LIM["edt"], f"dry room: early decay {e:.0f} ms (<= {LIM['edt']:.0f}; his {ref['edt_ms']:.0f})", round(e, 1), gated=G)
        row("tone", err.mean() <= LIM["tone_mean"] and err.max() <= LIM["tone_max"],
            f"tone: mean |err| {err.mean():.2f} dB (<= {LIM['tone_mean']}), max {err.max():.2f} (<= {LIM['tone_max']})",
            dict(mean=round(float(err.mean()), 3), max=round(float(err.max()), 3), bands=[round(float(b), 2) for b in bands]), gated=G)
        fd = floor - rf
        row("floor", bool((fd >= -LIM["floor"]).all()),
            f"clean between words: voice-over-floor {floor.round(1).tolist()} vs his {rf.round(1).tolist()} (diff {fd.round(1).tolist()}, >= -{LIM['floor']})",
            [round(float(v), 2) for v in floor], gated=G)
        row("dryness", dry >= ref["dryness"] - LIM["dry"],
            f"words stop cleanly: drop {dry:.1f} dB 64 ms after a word vs his {ref['dryness']:.1f} (>= his - {LIM['dry']})", round(dry, 2), gated=G)
    I, TP, LRA = C.ebur(path)
    if not ref_rows_only:
        row("lufs", abs(I - LIM["lufs"]) <= LIM["lufs_tol"], f"loudness: {I:.2f} LUFS ({LIM['lufs']} +/-{LIM['lufs_tol']})", round(I, 2))
        if not synthetic:
            row("spread", spread >= ref["spread"] - LIM["spread"],
                f"not crushed: speech spread p90-p10 {spread:.1f} dB vs his {ref['spread']:.1f} (>= his - {LIM['spread']}); LRA {LRA:.1f} LU (his {ref['lra']:.1f})",
                dict(spread=round(spread, 2), lra=round(LRA, 2)), gated=G)
        row("tp", TP <= LIM["tp"], f"no clipping: true peak {TP:.2f} dBTP (<= {LIM['tp']})", round(TP, 2))
        # 9 nothing missing -- on the WHOLE file
        full = C.pcm(path, ac=1)
        dead, quiet = C.silent_seconds(full)
        row("silence", dead == LIM["silent"], f"nothing missing: {dead} digitally silent second(s) (< -60 dBFS); {quiet} below -50 dBFS", dict(dead=dead, quiet=quiet))
        pic = video or (path if C.has_video(path) else None)
        if pic:
            la, lv = C.duration(path, "a:0"), C.duration(pic, "v:0")
            row("length", abs(la - lv) <= LIM["length"], f"audio {la:.3f} s vs picture {lv:.3f} s (within {LIM['length']} s)", dict(audio=round(la, 3), video=round(lv, 3)))
        else:
            print("  info  no picture to compare length against (pass --video)")
    fails = [r for r in rows if not r["ok"]]
    verdict = "PASS" if not fails else "FAIL"
    ab_path = None
    if ab:
        # his three sentences, then ours, from the same 12 s windows 20 s in (1 s in on a short)
        our_ss = 20 if dur >= 60 else ss
        subprocess.run([C.FF, "-nostdin", "-y", "-v", "error", "-ss", "20", "-t", "12", "-i", ref_audio,
                        "-ss", str(our_ss), "-t", "12", "-i", path, "-filter_complex",
                        "[0:a]aformat=channel_layouts=stereo[a];[1:a]aformat=channel_layouts=stereo[b];[a][b]concat=n=2:v=0:a=1[out]",
                        "-map", "[out]", "-vn", "-c:a", "aac", "-b:a", "192k", ab], check=True)
        ab_path = os.path.abspath(ab); print("  A/B written (his, then ours):", ab)
    print(f"\nAUDIO GATE {verdict}" + (f" -- {len(fails)} row(s): " + ", ".join(r["key"] for r in fails) if fails else ""))
    if stamp and not ref_rows_only:
        s = dict(version=C.STAMP_VERSION, file=os.path.abspath(path), sha256=C.sha256(path),
                 size=os.path.getsize(path), gated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                 reference=dict(name=ref["name"], sha256=ref.get("sha256")), synthetic=synthetic,
                 window=[ss, dur], limits=LIM, rows=rows, verdict=verdict, ab=ab_path)
        if reference_mix:
            s["mode"] = "reference-mix"
            s["reference_mix"] = dict(source=os.path.abspath(reference_mix), sha256=C.sha256(reference_mix),
                                      per_second_corr_median=round(prov, 4))
            s["info_rows"] = info_rows
        json.dump(s, open(C.stamp_path(path), "w"), indent=1)
        print(f"stamp: {C.stamp_path(path)}")
    return verdict == "PASS", rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--synthetic", action="store_true"); ap.add_argument("--ab")
    ap.add_argument("--video", help="the picture this audio belongs to, when `file` is audio-only")
    ap.add_argument("--ref", help="gate against a different reference file (testing only)")
    ap.add_argument("--no-stamp", action="store_true")
    ap.add_argument("--reference-rows-only", action="store_true", help="selftest: only the rows measured against the reference")
    ap.add_argument("--reference-mix", help="the editor's own finished mix this file carries verbatim (shortad path): provenance is verified per second; rows that measure HIS mixing become informational")
    A = ap.parse_args()
    ok, _ = gate(A.file, A.synthetic, A.ab, A.video, A.ref, not A.no_stamp, A.reference_rows_only, reference_mix=A.reference_mix)
    sys.exit(0 if ok else 1)
