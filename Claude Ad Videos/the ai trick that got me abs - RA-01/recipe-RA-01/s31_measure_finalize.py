#!/usr/bin/env python3
"""Fold round 1's late findings into measurements-RA-01.json, and prove every plan section 8 key
is present (a key that truly cannot be measured must carry a `_why`)."""
import json, os, sys

W = "/Volumes/Extreme/_edit_work/ra01"
M = json.load(open(f"{W}/measurements-RA-01.json"))

# --- the audio rows, re-read from the stamps that are actually on the delivered files ----------
for key in ("9x16", "16x9"):
    st = json.load(open(f"{W}/master_{key}.mp4.audio_gate.json"))
    rows = {r["key"]: r for r in st["rows"]}
    M.setdefault("audio", {}).setdefault("gate_per_master", {})[key] = {
        "verdict": st["verdict"],
        "failing_rows": [k for k, r in rows.items() if not r["ok"]],
        "artifacts": rows["artifacts"]["value"],
        "lufs": rows["lufs"]["value"], "true_peak_dbtp": rows["tp"]["value"],
        "gate_window_s": st["window"],
        "reference": st["reference"]["name"],
    }

# --- where the flux comes from (s28_fluxdiag.py) -----------------------------------------------
if os.path.exists(f"{W}/flux_diagnosis.json"):
    M["audio"]["flux_diagnosis"] = json.load(open(f"{W}/flux_diagnosis.json"))

# --- what adding the plan's SFX would do (s30_sfx_probe.py) ------------------------------------
if os.path.exists(f"{W}/sfx_probe.json"):
    M["audio"]["sfx_probe"] = json.load(open(f"{W}/sfx_probe.json"))
M["audio"]["sfx_in_delivered_mix"] = False
M["audio"]["sfx_why"] = ("plan section 6 asks for transition SFX from _shared/sfxlib.py on card ins; "
                         "round 2 ships none by ruling -- plan section 12 R7 accepts the deviation "
                         "(measured: they break the audio gate's `tone` row, sfx_probe.json)")

# --- the delivery gate, per master -------------------------------------------------------------
M["delivery_gate"] = {}
for key in ("9x16", "16x9"):
    p = f"{W}/master_{key}.mp4.deliver_gate.json"
    if not os.path.exists(p):
        M["delivery_gate"][key] = {"_why": "no deliver_gate stamp on disk for this master"}
        continue
    d = json.load(open(p))
    rows = d.get("rows") or {}          # {row key: {ok, detail, value}}

    def _st(r):
        if r.get("na") or r.get("not_applicable"):
            return "n/a"
        if r.get("ok") is None:
            return "NOT MEASURED"
        return "PASS" if r.get("ok") else "FAIL"

    states = {k: _st(r) for k, r in rows.items()}
    M["delivery_gate"][key] = {
        "gate_version": d.get("gate_version"),
        "verdict": d.get("verdict"),
        "sha256": d.get("sha256"),
        "when": d.get("when"),
        "failing_rows": [k for k, s in states.items() if s not in ("PASS", "n/a")],
        "rows": states,
        "row_detail": {k: rows[k].get("detail") for k, s in states.items() if s != "PASS"},
    }

# --- delivered geometry, straight off the files ------------------------------------------------
import subprocess
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe"
dur = {}
for key in ("9x16", "16x9"):
    p_ = f"{W}/master_{key}.mp4"
    dur[key] = (round(float(subprocess.run([FF, "-v", "error", "-show_entries", "format=duration",
                                            "-of", "csv=p=0", p_], capture_output=True,
                                           text=True).stdout.strip()), 6)
                if os.path.exists(p_) else None)
M["length"]["container_duration_s"] = dict(dur, ceiling_s=59.0,
                                           under_ceiling=all(v is not None and v <= 59.0
                                                             for v in dur.values()))

# --- round 2: the delivered-frame verification (s33_verify.py) ---------------------------------
for key in ("9x16", "16x9"):
    p_ = f"{W}/r2/verify_{key}.json"
    if os.path.exists(p_):
        M.setdefault("framing", {}).setdefault("delivered_verification", {})[key] = json.load(open(p_))
if os.path.exists(f"{W}/grade.json"):
    M["grade"]["grade_json"] = json.load(open(f"{W}/grade.json"))

# --- the plan section 8 completeness proof -----------------------------------------------------
REQUIRED = {
    "": ["decoded_size", "rotation_side_data", "fps", "duration_s"],
    "audio": ["streams", "channels", "dual_mono_corr", "lav_snr_db", "rms_dbfs", "clip_count",
              "noise_floor_between_words_dbfs", "decay_ms", "wind_or_rain_events", "chosen_map"],
    "grade": ["lut", "exposure_chosen", "exposures_tested", "reference_frame_used",
              "sky_clip_pct", "tree_noise_sd_flat_patch"],
    "framing": ["hair_top_px_per_hold", "belly_px", "waistband_px", "feet_px", "dan_width_frac",
                "near_crop_px", "far_crop_px", "near_upscale", "far_upscale",
                "face_sharpness_lapvar"],
    "focus": ["face_sharp", "notes"],
    "eyeline": ["method", "yaw_deg_est", "pitch_deg_est", "notes"],
    "lighting": ["sky_vs_face_luma_ratio", "shadow_side", "notes"],
    "takes": ["full_passes", "retakes", "false_starts", "crew_chatter_s", "usable_span_s",
              "airtight_speech_s"],
    "length": ["airtight_s", "lines_cut", "final_9x16_s", "final_16x9_s"],
}
missing = []
for sec, keys in REQUIRED.items():
    d = M if sec == "" else M.get(sec, {})
    for k in keys:
        v = d.get(k, "__ABSENT__")
        if v == "__ABSENT__":
            missing.append(f"{sec or '(top)'}.{k} ABSENT")
        elif v is None and not isinstance(d.get(k + "_why"), str):
            missing.append(f"{sec or '(top)'}.{k} is null with no _why")
M["_plan_s8_completeness"] = {"checked": sum(len(v) for v in REQUIRED.values()),
                              "missing": missing, "complete": not missing}

json.dump(M, open(f"{W}/measurements-RA-01.json", "w"), indent=1)
print(f"plan section 8: {M['_plan_s8_completeness']['checked']} keys checked, "
      f"{len(missing)} problem(s)" + (": " + "; ".join(missing) if missing else " -- complete"))
for key in ("9x16", "16x9"):
    dg = M["delivery_gate"][key]
    print(f"  {key}: audio {M['audio']['gate_per_master'][key]['verdict']} "
          f"(fails {M['audio']['gate_per_master'][key]['failing_rows']}) | "
          f"deliver {dg.get('verdict')} (fails {dg.get('failing_rows', dg.get('_why'))})")
