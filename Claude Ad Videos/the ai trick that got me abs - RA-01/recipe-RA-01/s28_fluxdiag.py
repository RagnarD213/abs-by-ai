#!/usr/bin/env python3
"""RA-01 round 1: WHERE does the `artifacts` flux come from?

Four measurements on the CURRENT files, all through `_shared/audio/common.artifacts` -- the same
function the gate uses -- so the numbers are directly comparable with the stamp:

  (a) the untreated lav cut          cut_audio.wav
  (b) the voice chain, NO bed        rebuilt here with --bed omitted
  (c) the voice chain WITH the bed   mix.wav  (what the masters carry)
  (d) the delivered master's audio   decoded back out of master_9x16.mp4

Nothing is changed. This only measures.  SFX: this build has none (see ROUND-1-EDITOR.md), so
there is no SFX term to measure.
"""
import json, os, subprocess, sys, wave
import numpy as np

ROOT = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
SH = f"{ROOT}/.claude/skills/_shared/audio"
FF = f"{ROOT}/Media/video_edit/bin/ffmpeg"
sys.path.insert(0, SH)
import common as C                                     # noqa: E402
import reference as R                                   # noqa: E402

W = "/Volumes/Extreme/_edit_work/ra01"
TMP = "/Volumes/Extreme/_edit_work/ra01/fluxdiag"
os.makedirs(TMP, exist_ok=True)


def mono(path):
    """Read a wav (any channel count) as mono float32 at the module sample rate."""
    out = f"{TMP}/_rd_{os.path.basename(path)}.wav"
    subprocess.run([FF, "-v", "error", "-y", "-i", path, "-map", "0:a:0",
                    "-ac", "1", "-ar", str(C.SR), "-c:a", "pcm_s16le", out], check=True)
    w = wave.open(out)
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
    w.close()
    return x


# The gate measures its window, not the tail; match it: 1.0 s in to the last word.
STAMP = json.load(open(f"{W}/master_9x16.mp4.audio_gate.json"))
W0, W1 = STAMP["window"]
print(f"gate window {W0:.3f}..{W1:.3f}s  (matching the stamp exactly)")


def art(path, label):
    x = mono(path)
    x = x[int(W0 * C.SR):int(W1 * C.SR)]
    a = C.artifacts(x)
    print(f"  {label:<44s} flux {a['flux']:.4f}   swirl {a['swirl']:.4f}   "
          f"sfm {a['sfm']:.4f}   gap {a['gap']:.2f}")
    return a


# (b) rebuild the chain with NO bed, everything else identical (same fitted EQ, same target).
nobed = f"{TMP}/mix_nobed.wav"
if not os.path.exists(nobed):
    subprocess.run([sys.executable, f"{SH}/voice_chain.py", "--in", f"{W}/cut_audio.wav",
                    "--out", nobed, "--work", f"{TMP}/work_nobed"], check=True)

# (d) the delivered master's own audio
deliv = f"{TMP}/delivered_9x16.wav"
if not os.path.exists(deliv):
    subprocess.run([FF, "-v", "error", "-y", "-i", f"{W}/master_9x16.mp4", "-map", "0:a:0",
                    "-c:a", "pcm_s16le", deliv], check=True)

_refpath, _refmeta = R.resolve()
_rx = mono(_refpath)
ref = C.artifacts(_rx)
bound = ref["flux"] * 1.10
print(f"\nreference ({os.path.basename(_refpath)}) flux {ref['flux']:.4f}   "
      f"bound = his x1.10 = {bound:.4f}\n")

res = {}
res["a_untreated_lav_cut"] = art(f"{W}/cut_audio.wav", "(a) untreated lav cut")
res["b_chain_no_bed_no_sfx"] = art(nobed, "(b) voice chain, no bed, no SFX")
res["c_chain_with_bed"] = art(f"{W}/mix.wav", "(c) voice chain + bed (mix.wav)")
res["d_delivered_master"] = art(deliv, "(d) delivered master audio (AAC)")

for k, v in res.items():
    v["flux_over_bound"] = round(v["flux"] / bound, 4)
    v["passes_bound"] = bool(v["flux"] <= bound)

out = {"reference_flux": ref["flux"], "bound_flux": round(bound, 4),
       "window": [W0, W1], "sfx_in_build": None,
       "sfx_why": "this build carries no transition SFX at all (plan section 6 asked for them on card "
                  "ins); so there is no SFX term in the flux and none can be removed to pass",
       "bed": {"track": "Realizer.mp3", "level_db": -32},
       "measurements": res}
json.dump(out, open(f"{W}/flux_diagnosis.json", "w"), indent=1)
print(f"\nwrote {W}/flux_diagnosis.json")
