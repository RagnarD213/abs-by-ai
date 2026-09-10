#!/usr/bin/env python3
"""THE ONE AUDIO GATE. Measures the DELIVERED file against the pinned reference and STAMPS it.

  python3 audio_gate.py <finished.mp4|.mov|.wav> [--synthetic] [--ab out.mp4] [--video picture.mp4]
                        [--ref other.mp4] [--no-stamp] [--reference-rows-only] [--profile in-app-demo]
                        [--reference-mix his_mix.wav [--verbatim]]

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
 10 no processing damage        flux / HF swirl                          <= his x1.10
 11 do no harm                  flux / HF swirl vs THIS FILE UNTREATED   <= x1.35
                                 ⚠ NOT MEASURED = FAIL (2026-09-09). "Nobody looked" is not "it is fine".

--reference-mix --verbatim (Dan, 2026-09-10: "Use Zishan's audio"): the file carries an EDITOR'S finished mix
UNTOUCHED -- stream-copied, or only CUT for a cutdown. Every row then asks "is this his audio, unchanged?":
 V1 verbatim level              per-second level vs his mix             |median| <= 0.10 dB, every second within +/-0.50
 V2 verbatim image              L/R correlation vs his                  within 0.01 (not summed to mono, not widened)
 V3 verbatim loudness           integrated loudness and LRA vs his      within 0.30 LU each
  and rows 1 and 6 (absolute L/R and -14 LUFS) are DECLARED not applicable, with the reason: his level and his image
  ARE the standard. True peak, silence and length still gate.

--synthetic (make-ad, exercise demos: an AI voice, no camera) keeps 6, 8, 9 and the L/R row.
--profile in-app-demo moves row 6 to the -24 +/-1.5 LUFS Dan approved for in-app exercise demos.
  It is a named, measured profile recorded in the stamp -- there is no free --lufs-target, because a
  dial that makes a build pass is not a gate. It replaced exercisegeneration's "--no-stamp if the row
  fails", which shipped an UNSTAMPED file that nothing downstream could catch either.
The stamp `<file>.audio_gate.json` carries the file's sha256 + every number + PASS/FAIL, and
require_stamp.py is what every QC and delivery script calls. No stamp = not deliverable.
--ab writes his three sentences then ours, for Dan's ear, and its path goes in the stamp. (In --verbatim mode "his"
is the editor's own mix from the same window, not the pinned reference.)
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
# artifact_x 1.10: the build Dan rejected ran 1.29x his flux and 1.19x his swirl; the build he
# approved by ear on 2026-09-09 runs 1.01x and 0.81x. 1.10 separates them with margin.
# harm_x 1.35: measured 2026-09-09 on matched pairs (the SAME short, untreated vs processed).
#   approved a0.30  flux 1.05-1.21x untreated, swirl 1.21-1.28x
#   rejected a0.62  flux 1.30-1.61x,           swirl 1.57-1.94x
#   the chain WITHOUT any dereverb  flux 0.98x, swirl 0.96x -- so this row charges the DEREVERB,
#   not the EQ / expander / limiter / AAC encode.
# vb_* (VERBATIM, 2026-09-10): the rejected Zeeshan Ad 1 vertical -- his -23.5 LUFS mix lifted +9.9 dB into a
#   limiter and summed to mono -- measured median +9.90 dB, seconds +5.6..+9.9, L/R +1.000 vs his +0.970, loudness
#   -14.7 vs -23.5 LUFS, LRA 4.1 vs 5.9. Dan: "Zishan's audio sounds much better... Use Zishan's audio." A stream
#   copy of his track measures 0.00 on every one of these; a cutdown's AAC re-encode of his cut mix, hundredths.
LIM = dict(corr=0.97, comb_margin=0.35, edt=80.0, tone_mean=1.2, tone_max=2.5, floor=3.0, dry=1.5,
           artifact_x=1.10, harm_x=1.35,
           lufs=-14.0, lufs_tol=1.0, spread=3.0, tp=-1.0, silent=0, length=0.10,
           vb_med=0.10, vb_sec=0.50, vb_image=0.01, vb_lufs=0.30, vb_lra=0.30)
# ⚠ IN-APP DEMO PROFILE (2026-09-09, Phase 0). The exercise demos play inside the app under the
# member's own music, not on a platform feed, and Dan approved batch 1 at -23.9 / -24.2 LUFS; batch 2
# landed -23.4 to -24.9. Against the -14 broadcast row every one of them FAILS, and exercisegeneration's
# SKILL.md answered that by telling the session to pass --no-stamp -- shipping an UNSTAMPED file, which
# no downstream check can catch either. So the row keeps its teeth and gets the bound Dan actually
# approved. This is a NAMED PROFILE, never a free --lufs-target: a dial anyone can turn to make a build
# pass is not a gate. The profile is recorded in the stamp.
PROFILES = dict({"in-app-demo": dict(lufs=-24.0, lufs_tol=1.5)})
HARM_KEYS = ("flux", "swirl")     # gated; gap + sfm are reported only -- see common.artifacts
VERBATIM_WHY = "the editor's own mix, delivered untouched (Dan 2026-09-10: 'Use Zishan's audio')"


def gate(path, synthetic=False, ab=None, video=None, ref_override=None, stamp=True, ref_rows_only=False,
         reference_mix=None, untreated=None, profile=None, verbatim=False):
    LIMP = dict(LIM)
    if verbatim and not reference_mix:
        raise SystemExit("--verbatim needs --reference-mix <the editor's mix it must equal>")
    VB = bool(reference_mix and verbatim)
    if profile:
        if profile not in PROFILES:
            raise SystemExit(f"unknown profile {profile!r} -- known: {', '.join(PROFILES)}")
        LIMP.update(PROFILES[profile])
    if ref_override:
        ref_audio, ref = ref_override, R.measure(ref_override)
    else:
        ref_audio, ref = R.resolve()
    ss, dur = C.analysis_window(path)
    st = C.pcm(path, ss=ss, dur=dur, ac=2)
    mono = st.mean(1)
    rows, info_rows = [], []
    def row(key, ok, text, val, gated=True, why=None):
        if not gated:
            # REFERENCE-MIX MODE: this row measures the EDITOR'S OWN MIXING (his bed between the
            # words, his tone), not our chain, so it is recorded but cannot fail the file. In
            # --verbatim mode the reason is printed, so a reader can audit why the row does not apply.
            info_rows.append(dict(key=key, ok=bool(ok), text=text, value=val, why=why or "not ours to gate"))
            print("  info  " + text + f"   [{why or 'not ours to gate'}]"); return
        rows.append(dict(key=key, ok=bool(ok), text=text, value=val))
        print(("  PASS  " if ok else "  FAIL  ") + text)
    print(f"audio_gate  {os.path.basename(path)}  window {ss:.0f}s +{dur:.0f}s  vs  {ref['name']}"
          + ("  [synthetic]" if synthetic else "")
          + ("  [reference mix, VERBATIM]" if VB else "  [reference mix]" if reference_mix else ""))
    prov = None
    if reference_mix:
        # --reference-mix (shortad-from-longform, 2026-09-03): the delivered audio IS the editor's
        # finished mix. PROVENANCE IS VERIFIED, NOT ASSUMED: per-second, level-normalised correlation
        # against that mix must be >= 0.99 at the median (the qc.py check that separated his mix from a
        # loudnorm'd one at 0.970), or the flag is refused.
        # With provenance proven, comb / room / tone / floor / dryness / spread measure HIS mixing
        # (Ad 2's bed sits 6-7 dB hotter between words than Ad 1's, the pinned reference) and are
        # reported as information; loudness, true peak, silence, length and the L/R image still gate.
        # ⚠ Level-normalised provenance CANNOT HEAR A GAIN OR A LIMITER (2026-09-10): the rejected Zeeshan
        # vertical, his mix +9.9 dB into a limiter, read 0.9989 here. That is what --verbatim is for.
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
    if VB:
        # ⚠ VERBATIM (Dan, 2026-09-10): "Zishan's audio sounds much better... Use Zishan's audio." The editor's
        # finished mix IS the standard, so nothing of ours may change it: not its level (a gain), not its dynamics
        # (a limiter, a compressor, loudnorm), not its stereo image (a mono sum). Each row compares the delivered
        # audio to HIS, never to a target of ours -- a target his audio does not meet is exactly how we talked
        # ourselves into processing it (our -14 LUFS and L/R >= 0.98 rows would have FAILED Zeeshan's own mix).
        ref_st = C.pcm(reference_mix, ac=2); out_st = C.pcm(path, ac=2)
        n = min(len(ref_st), len(out_st)); W = C.SR
        am, bm = out_st[:n].mean(1), ref_st[:n].mean(1)
        devs = []
        for i in range(n // W):
            x, y = bm[i*W:(i+1)*W], am[i*W:(i+1)*W]
            rx = float(np.sqrt((x ** 2).mean()))
            if rx < 1e-3: continue
            devs.append(20 * np.log10(max(float(np.sqrt((y ** 2).mean())), 1e-9) / rx))
        devs = np.array(devs) if devs else np.array([99.0])
        med, lo, hi = float(np.median(devs)), float(devs.min()), float(devs.max())
        row("verbatim_level", abs(med) <= LIMP["vb_med"] and lo >= -LIMP["vb_sec"] and hi <= LIMP["vb_sec"],
            f"verbatim level: per-second level vs {os.path.basename(reference_mix)} median {med:+.2f} dB, "
            f"seconds {lo:+.2f}..{hi:+.2f} dB over {len(devs)} s (|median| <= {LIMP['vb_med']}, every second "
            f"within +/-{LIMP['vb_sec']}: no gain, no limiter, no compression)",
            dict(median=round(med, 3), min=round(lo, 3), max=round(hi, 3), seconds=len(devs)))
        def lrc(s):
            L, Rr = s[:, 0], s[:, 1]
            return float(np.corrcoef(L, Rr)[0, 1]) if L.std() > 1e-6 and Rr.std() > 1e-6 else 1.0
        cr, co = lrc(ref_st[:n]), lrc(out_st[:n])
        row("verbatim_image", abs(co - cr) <= LIMP["vb_image"],
            f"verbatim image: L/R correlation {co:+.4f} vs his {cr:+.4f} (within {LIMP['vb_image']}: "
            f"not summed to mono, not widened)", dict(ours=round(co, 4), his=round(cr, 4)))
        Ir, _, LRAr = C.ebur(reference_mix)
        Io, _, LRAo = C.ebur(path)
        row("verbatim_lufs", abs(Io - Ir) <= LIMP["vb_lufs"] and abs(LRAo - LRAr) <= LIMP["vb_lra"],
            f"verbatim loudness: {Io:.2f} LUFS / LRA {LRAo:.1f} LU vs his {Ir:.2f} / {LRAr:.1f} "
            f"(within {LIMP['vb_lufs']} LU / {LIMP['vb_lra']} LU)",
            dict(ours=[round(Io, 2), round(LRAo, 2)], his=[round(Ir, 2), round(LRAr, 2)]))
    G = not reference_mix          # rows that measure the editor's mixing gate only when the mix is ours
    # ⚠ do_no_harm charges OUR PROCESSING against this file's own untreated signal. A file that is
    # not ours has none to charge: --reference-rows-only measures HIS file to build the reference,
    # --reference-mix carries an editor's finished mix. In both, the row is informational.
    # In every other case -- our own delivery with no stashed baseline -- it FAILS (see below).
    GH = G and not ref_rows_only
    # 1 image
    nch = C.probe_audio(path)[0]["channels"]
    if nch >= 2:
        L, Rr = st[:, 0], st[:, 1]
        corr = float(np.corrcoef(L, Rr)[0, 1]) if L.std() > 1e-6 and Rr.std() > 1e-6 else 0.0
    else: corr = 1.0
    if not ref_rows_only:
        row("lr_corr", corr >= LIMP["corr"], f"one voice: L/R correlation {corr:+.4f} (>= +{LIMP['corr']})", round(corr, 4),
            gated=not VB, why=VERBATIM_WHY + "; verbatim_image gates that it is his" if VB else None)
    if not synthetic:
        bands, floor, dry, spread = C.analyse(mono)
        rb = np.array(ref["bands"]); rf = np.array(ref["floor"])
        err = np.abs(bands - rb)
        print("  band      ref    mix   diff")
        for lo_, r_, o in zip(C.EDGES, rb, bands): print(f"  {lo_:5d}Hz {r_:6.1f} {o:6.1f} {o-r_:+6.1f}")
        ripple = C.comb_ripple(mono)
        row("comb", ripple <= ref["comb_ripple"] + LIMP["comb_margin"],
            f"no comb: spectral ripple {ripple:.2f} dB vs his {ref['comb_ripple']:.2f} (<= his + {LIMP['comb_margin']})", round(ripple, 3), gated=G)
        e = C.edt(mono)
        row("edt", e <= LIMP["edt"], f"dry room: early decay {e:.0f} ms (<= {LIMP['edt']:.0f}; his {ref['edt_ms']:.0f})", round(e, 1), gated=G)
        row("tone", err.mean() <= LIMP["tone_mean"] and err.max() <= LIMP["tone_max"],
            f"tone: mean |err| {err.mean():.2f} dB (<= {LIMP['tone_mean']}), max {err.max():.2f} (<= {LIMP['tone_max']})",
            dict(mean=round(float(err.mean()), 3), max=round(float(err.max()), 3), bands=[round(float(b), 2) for b in bands]), gated=G)
        fd = floor - rf
        row("floor", bool((fd >= -LIMP["floor"]).all()),
            f"clean between words: voice-over-floor {floor.round(1).tolist()} vs his {rf.round(1).tolist()} (diff {fd.round(1).tolist()}, >= -{LIMP['floor']})",
            [round(float(v), 2) for v in floor], gated=G)
        # ⚠ DO NO HARM (2026-09-09). Every other row above measures level, tone, channels or
        # SUPPRESSION - and `edt`, `dryness` and `floor` all reward MORE of it. So the gate scored
        # the build Dan called "underwater" as BETTER: it hit EDT 32 ms (past his 40) while running
        # 1.29x his spectral flux, 1.19x his HF swirl and a floor 14 dB deeper than his. Measured,
        # our UNTREATED right channel was closer to him than that output on every damage metric.
        #
        # So: processing may not push a damage metric PAST HIS. flux = frame-to-frame spectral
        # change on speech (musical noise), swirl = modulation of the 3-9 kHz envelope. Both are
        # bounded against the reference, not against a constant, so a drier reference cannot make
        # this row unfailable. This single row would have blocked all three 09-02 batches.
        art = C.artifacts(mono)
        fx, sw = art["flux"], art["swirl"]
        row("artifacts", fx <= ref["flux"] * LIMP["artifact_x"] and sw <= ref["swirl"] * LIMP["artifact_x"],
            f"no processing damage: flux {fx:.3f} (his {ref['flux']:.3f}), HF swirl {sw:.3f} "
            f"(his {ref['swirl']:.3f}), both <= his x{LIMP['artifact_x']}",
            {k: round(float(v), 4) for k, v in art.items()}, gated=G)
        # ⚠ DO NO HARM, THE SECOND HALF (2026-09-09). The row above bounds us against HIS room.
        # This one bounds us against OUR OWN UNTREATED SIGNAL, and it is the rule that would have
        # blocked all three 09-02 batches: measured, the untreated right channel was closer to
        # Muhammad than the processed output on every damage metric. Processing that leaves the
        # file worse than doing nothing is not a trade-off, it is a bug - whatever EDT it buys.
        # The baseline is stashed by whichever stage held the untreated audio; see
        # common.stash_untreated (voice_chain calls it after the pull, dereverb.py on its input).
        base = C.load_untreated(untreated) if untreated else C.load_untreated(path)
        if base and all(k in base for k in HARM_KEYS):
            worst = max(art[k] / max(base[k], 1e-9) for k in HARM_KEYS)
            det = ", ".join(f"{k} {art[k]:.3f} vs untreated {base[k]:.3f} (x{art[k]/max(base[k],1e-9):.2f})"
                            for k in HARM_KEYS)
            info = ", ".join(f"{k} x{art[k]/max(base[k],1e-9):.2f}" for k in ("gap", "sfm") if k in base)
            row("do_no_harm", worst <= LIMP["harm_x"],
                f"no worse than untreated: {det}, both <= x{LIMP['harm_x']} "
                f"(untreated EDT {base.get('edt_ms')} ms)   [reported, not gated: {info}]",
                dict(ratios={k: round(art[k] / max(base[k], 1e-9), 3) for k in base if k in art},
                     untreated={k: base[k] for k in base if k in art}), gated=GH)
        elif reference_mix:
            # The delivered audio is the editor's own mix: there is no untreated signal of OURS to charge.
            # Declared, not "NOT MEASURED ... is a FAIL" followed by "[not ours to gate]" (2026-09-10).
            row("do_no_harm", True, "do no harm: n/a -- no stage of ours produced this audio "
                "(the editor's mix" + (", untouched" if VB else "") + ")", "n/a", gated=False,
                why=VERBATIM_WHY if VB else "the editor's finished mix")
        else:
            # ⚠ NOT MEASURED IS A FAILURE (2026-09-09, Phase 0). This used to append ok=True with
            # not_measured=True -- recorded, but passing. "Nobody looked" then reads as "it is fine"
            # to every downstream caller, which is the whole shape of the defect this row exists to
            # stop: the 09-02 batches shipped because the gate's silence was taken for approval.
            # The fix is one line in the producing stage: common.stash_untreated() while the
            # untreated audio still exists (voice_chain does it right after the pull, dereverb.py
            # on its input), or pass --untreated <that file>.audio_untreated.json here.
            row("do_no_harm", False,
                f"do no harm: NOT MEASURED -- no {os.path.basename(C.untreated_path(path))}; the stage "
                f"holding the untreated audio never called common.stash_untreated(). An unmeasured "
                f"row is a FAIL, not a pass -- re-run the chain, or pass --untreated <baseline.json>",
                "not_measured", gated=GH)
        row("dryness", dry >= ref["dryness"] - LIMP["dry"],
            f"words stop cleanly: drop {dry:.1f} dB 64 ms after a word vs his {ref['dryness']:.1f} (>= his - {LIMP['dry']})", round(dry, 2), gated=G)
    I, TP, LRA = C.ebur(path)
    if not ref_rows_only:
        row("lufs", abs(I - LIMP["lufs"]) <= LIMP["lufs_tol"],
            f"loudness: {I:.2f} LUFS ({LIMP['lufs']} +/-{LIMP['lufs_tol']}"
            + (f"; profile {profile}" if profile else "") + ")", round(I, 2),
            gated=not VB, why=VERBATIM_WHY + "; verbatim_lufs gates that it is his" if VB else None)
        if not synthetic:
            row("spread", spread >= ref["spread"] - LIMP["spread"],
                f"not crushed: speech spread p90-p10 {spread:.1f} dB vs his {ref['spread']:.1f} (>= his - {LIMP['spread']}); LRA {LRA:.1f} LU (his {ref['lra']:.1f})",
                dict(spread=round(spread, 2), lra=round(LRA, 2)), gated=G)
        row("tp", TP <= LIMP["tp"], f"no clipping: true peak {TP:.2f} dBTP (<= {LIMP['tp']})", round(TP, 2))
        # 9 nothing missing -- on the WHOLE file
        full = C.pcm(path, ac=1)
        dead, quiet = C.silent_seconds(full)
        row("silence", dead == LIMP["silent"], f"nothing missing: {dead} digitally silent second(s) (< -60 dBFS); {quiet} below -50 dBFS", dict(dead=dead, quiet=quiet))
        pic = video or (path if C.has_video(path) else None)
        if pic:
            la, lv = C.duration(path, "a:0"), C.duration(pic, "v:0")
            row("length", abs(la - lv) <= LIMP["length"], f"audio {la:.3f} s vs picture {lv:.3f} s (within {LIMP['length']} s)", dict(audio=round(la, 3), video=round(lv, 3)))
        else:
            print("  info  no picture to compare length against (pass --video)")
    fails = [r for r in rows if not r["ok"]]
    verdict = "PASS" if not fails else "FAIL"
    ab_path = None
    if ab:
        # his three sentences, then ours, from the same 12 s windows 20 s in (1 s in on a short). In --verbatim mode
        # "his" is the EDITOR'S OWN MIX from the same window -- the first Zeeshan A/B played the pinned (Muhammad)
        # reference as "his" and was mislabelled for that video (2026-09-10).
        our_ss = 20 if dur >= 60 else ss
        ab_src, ab_ss = (reference_mix, our_ss) if VB else (ref_audio, 20)
        subprocess.run([C.FF, "-nostdin", "-y", "-v", "error", "-ss", str(ab_ss), "-t", "12", "-i", ab_src,
                        "-ss", str(our_ss), "-t", "12", "-i", path, "-filter_complex",
                        "[0:a]aformat=channel_layouts=stereo[a];[1:a]aformat=channel_layouts=stereo[b];[a][b]concat=n=2:v=0:a=1[out]",
                        "-map", "[out]", "-vn", "-c:a", "aac", "-b:a", "192k", ab], check=True)
        ab_path = os.path.abspath(ab); print("  A/B written (his, then ours):", ab)
    print(f"\nAUDIO GATE {verdict}" + (f" -- {len(fails)} row(s): " + ", ".join(r["key"] for r in fails) if fails else ""))
    if stamp and not ref_rows_only:
        s = dict(version=C.STAMP_VERSION, file=os.path.abspath(path), sha256=C.sha256(path),
                 size=os.path.getsize(path), gated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                 reference=dict(name=ref["name"], sha256=ref.get("sha256")), synthetic=synthetic,
                 profile=profile, window=[ss, dur], limits=LIMP, rows=rows, verdict=verdict, ab=ab_path)
        if reference_mix:
            s["mode"] = "reference-verbatim" if VB else "reference-mix"
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
    ap.add_argument("--no-stamp", action="store_true", help="measure without writing the stamp. FOR "
                    "TESTING AND THE SELFTEST ONLY -- an unstamped file is refused by require_stamp.py, "
                    "so this is not a way to deliver a file that fails a row (2026-09-09).")
    ap.add_argument("--reference-rows-only", action="store_true", help="selftest: only the rows measured against the reference")
    ap.add_argument("--untreated", help="do-no-harm baseline: a media file or its .audio_untreated.json "
                                        "(default: <file>.audio_untreated.json)")
    ap.add_argument("--reference-mix", help="the editor's own finished mix this file carries (shortad path): provenance is verified per second; rows that measure HIS mixing become informational")
    ap.add_argument("--verbatim", action="store_true", help="with --reference-mix: the file must carry that mix "
                    "UNTOUCHED (Dan 2026-09-10) -- level, dynamics and stereo image are gated against HIS, and the "
                    "absolute -14 LUFS / L/R rows are declared not applicable. The shortad default.")
    ap.add_argument("--profile", choices=sorted(PROFILES), help="a named, measured limit set for audio that "
                    "is not destined for a platform feed (in-app-demo: -24 +/-1.5 LUFS, the level Dan "
                    "approved for the exercise demos). Recorded in the stamp. There is deliberately no "
                    "free --lufs-target: a dial that makes a build pass is not a gate.")
    A = ap.parse_args()
    ok, _ = gate(A.file, A.synthetic, A.ab, A.video, A.ref, not A.no_stamp, A.reference_rows_only,
                 reference_mix=A.reference_mix, untreated=A.untreated, profile=A.profile, verbatim=A.verbatim)
    sys.exit(0 if ok else 1)
