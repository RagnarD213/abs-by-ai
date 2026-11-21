#!/usr/bin/env python3
"""Assemble measurements-RA-01.json (plan section 8). Every key is filled or carries a _why."""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ra01")
import ra01lib as L
from ra01lib import Aspect
from PIL import Image

CUT = json.load(open("cut.json")); B = json.load(open("beats.json"))
TRK = json.load(open("framing.json")); EXPO = json.load(open("expo.json"))
GRD = json.load(open("grade.json"))               # round 2, R5: exposure AND saturation, measured
SRC = json.load(open(L.ROLL + ".audio_source.json"))
GATE9 = json.load(open("master_9x16.mp4.audio_gate.json"))
M = json.load(open("probe/measure.json"))
A9, A6 = Aspect("9x16"), Aspect("16x9")

def lapvar(path, box=None):
    im = Image.open(path).convert("L")
    a = np.asarray(im, dtype=np.float64)
    if box: a = a[box[1]:box[3], box[0]:box[2]]
    k = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float)
    from scipy.signal import convolve2d
    return round(float(convolve2d(a, k, mode="valid").var()), 1)

def face_crop_png(video, t, out):
    subprocess.run([L.FF, "-nostdin", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1",
                    "-y", out], check=True)
    return out

env = json.load(open("env.json")); DB = np.array(env["db"])
# noise floor between words, inside the kept spans only
floor = []
for p in CUT["pieces"]:
    i0, i1 = int(p["src_in"]/env["hop"]), int(p["src_out"]/env["hop"])
    seg = DB[i0:i1]
    floor.extend(seg[seg < -45].tolist())
wind = [round(float(i*env["hop"]), 2) for i in range(len(DB)) if DB[i] > -20]

hair = [s["hair"] for s in TRK["samples"]]
mm = [v for v in M.values() if "hair_top" in v]
belly, waist, feet = 2093.0, 2170.0, float(np.median([v["mask_bot"] for v in M.values()]))
widths = [v["mask_x1"]-v["mask_x0"] for v in M.values()]

def probe(p):
    o = subprocess.run([L.FF.replace("ffmpeg", "ffprobe"), "-v", "error", "-show_entries",
                        "format=duration:stream=width,height,nb_frames", "-of", "json", p],
                       capture_output=True, text=True).stdout
    return json.loads(o)

out = {
 "roll": os.path.basename(L.ROLL),
 "decoded_size": [2160, 3840], "rotation_side_data": -90,
 "fps": "30000/1001", "duration_s": 218.218,
 "audio": {
   "streams": 1, "channels": 2, "dual_mono_corr": 1.000,
   "lav_snr_db": SRC["lav"]["snr_db"], "rms_dbfs": SRC["lav"]["rms_db"],
   "clip_count": SRC["lav"]["clipped"],
   "noise_floor_between_words_dbfs": round(float(np.median(floor)), 1),
   "decay_ms": next((r["value"] for r in GATE9["rows"] if r.get("key") == "edt"), None),
   "tone_err_db": next((r["value"] for r in GATE9["rows"] if r.get("key") == "tone"), {}),
   "lufs": next((r["value"] for r in GATE9["rows"] if r.get("key") == "lufs"), None),
   "true_peak_dbtp": next((r["value"] for r in GATE9["rows"] if r.get("key") == "tp"), None),
   "artifacts_vs_reference": next((r["value"] for r in GATE9["rows"] if r.get("key") == "artifacts"), {}),
   "do_no_harm": next((r["value"] for r in GATE9["rows"] if r.get("key") == "do_no_harm"), {}),
   "audio_gate_verdict": GATE9["verdict"],
   "audio_gate_failing_rows": [r["key"] for r in GATE9["rows"] if r.get("ok") is False],
   "bed": {"track": "Realizer.mp3 (Pixabay, no attribution)", "level": "-32 dB under the voice, ducked"},
   "wind_or_rain_events": {"_why": "no wind or rain inside the kept spans; the crew's 'I felt "
                           "raindrops' is at 1:38-1:41, after the last take this ad uses",
                           "loudest_frames_over_-20dBFS_in_roll": len(wind)},
   "chosen_map": SRC["map"] + "  " + SRC["filter"]},
 "grade": {"lut": os.path.basename(L.LUT % GRD["exposure"]),
           "exposure_chosen": GRD["exposure"], "saturation_chosen": GRD["saturation"],
           "filter": GRD["filter"],
           "rule": GRD["_rule"],
           "exposures_tested": {k: {"face_luma": v["face_luma"], "face_chroma_ab": v["face_chroma_ab"],
                                    "luma_err_vs_reference": v.get("luma_err")}
                                for k, v in EXPO["tests"].items()},
           "exposures_tested_round2": GRD["exposure_tests"],
           "saturations_tested_round2": GRD["saturation_tests"],
           "grid_round2": GRD["grid"],
           "reference_frame_used": "Website Conversion Video (post-generation)/website_video_16x9.mp4 "
                                   "at 30/60/95 s (approved rev 5/6) for LUMA; "
                                   "the approved Ad 1 vertical at 11 talking-head instants for CHROMA",
           "reference_face_luma": GRD["target_face_luma"],
           "reference_ad1_face_chroma": GRD["reference"]["ad1_vertical"]["chroma"],
           "chroma_floor_85pct_of_ad1": GRD["chroma_floor_85pct_of_ad1"],
           "chroma_floor_reached": GRD["chroma_floor_reached"],
           "face_chroma_pct_of_ad1": GRD["face_chroma_pct_of_ad1"],
           "sky_clip_pct": EXPO["sky_clip_pct"],
           "tree_noise_sd_flat_patch": EXPO["tree_noise_sd_flat_patch"],
           "proof_sheet": os.path.abspath("r2/grade/proof.jpg"),
           "why": ("R5: exposure 1.15 is the member of the 73 +- 5 luma band whose delivered pair "
                   "(at the chosen saturation) is both closest on luma and highest on chroma; "
                   "saturation is at the ruling's 1.25 cap and the 85 % chroma floor is NOT "
                   "reached -- see ROUND-2-EDITOR.md D6."),
           "sky_clip_pct_note": "measured on the round-1 exposure sweep (e1.30); recorded as-is"},
 "framing": {
   "hair_top_px_per_hold": [{"t": p["beat"][0], "level": p["level"], "hair_min": p["hair_min"],
                             "cx": p["cx"]} for p in B["punch"]],
   "hair_top_px_range": [round(min(hair), 1), round(float(np.median(hair)), 1), round(max(hair), 1)],
   "belly_px": belly, "waistband_px": waist, "feet_px": feet,
   "dan_width_frac": round(float(np.median(widths))/2160, 3),
   "near_crop_px": list(A9.levels["NEAR"]), "far_crop_px": list(A9.levels["FAR"]),
   "near_crop_px_16x9": list(A6.levels["NEAR"]), "far_crop_px_16x9": list(A6.levels["FAR"]),
   "near_upscale": round(1920/A9.levels["NEAR"][1], 3), "far_upscale": round(1920/A9.levels["FAR"][1], 3),
   "near_upscale_16x9": round(1080/A6.levels["NEAR"][1], 3),
   "far_upscale_16x9": round(1080/A6.levels["FAR"][1], 3),
   "head_h_px_source": {"min": round(min(s["head_h"] for s in TRK["samples"]), 1),
                        "median": round(float(np.median([s["head_h"] for s in TRK["samples"]])), 1),
                        "max": round(max(s["head_h"] for s in TRK["samples"]), 1)},
   "face_sharpness_lapvar": json.load(open("sharpness.json")) if os.path.exists("sharpness.json")
                            else {"_why": "sharpness.json not built"}},
 "focus": {"face_sharp": True,
           "notes": "hair strands and the glasses rim resolve at native scale on the graded frames; "
                    "visible grain in the trees after the exposure push (flat-patch sd "
                    f"{EXPO['tree_noise_sd_flat_patch']}), sky clipped on "
                    f"{EXPO['sky_clip_pct']}% of the upper 600 rows"},
 "eyeline": json.load(open("eyeline.json")) if os.path.exists("eyeline.json") else {"_why": "not measured"},
 "lighting": json.load(open("lighting.json")) if os.path.exists("lighting.json") else {"_why": "not measured"},
 "takes": {"full_passes": 1, "retakes": {"L5": 2}, "false_starts": 1,
           "crew_chatter_s": 0.0,
           "crew_chatter_note": "the crew's raindrop exchange runs 1:38-1:48, outside every kept span",
           "usable_span_s": round(CUT["span_end"], 2),
           "airtight_speech_s": round(CUT["dur"], 2)},
 "length": {"airtight_s": round(CUT["dur"], 2), "end_hold_s": B["end_hold"],
            "lines_cut": CUT["dropped"] or [],
            "final_9x16_s": None, "final_16x9_s": None},
}
for k, key in (("9x16", "final_9x16_s"), ("16x9", "final_16x9_s")):
    p = f"master_{k}.mp4"
    if os.path.exists(p):
        out["length"][key] = round(float(probe(p)["format"]["duration"]), 3)
json.dump(out, open("measurements-RA-01.json", "w"), indent=1)
print(json.dumps({k: (v if not isinstance(v, dict) else "...") for k, v in out.items()}, indent=1))
print("measurements-RA-01.json written")
