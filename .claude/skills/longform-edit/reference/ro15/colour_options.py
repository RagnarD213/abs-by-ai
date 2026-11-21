"""RO-15 round-1 colour options (from RO-31): the same 12 s (source 100-112, wide) and the same tight still in
each of the three grades, plus stills of the approved RO-25 film for comparison. Audio: the recommended voice (warm bass) on the clip."""
import sys, subprocess, json, os
sys.path.insert(0, "/Volumes/Extreme/_edit_work/RO-15/round1/recipe")
import frames as F
W = "/Volumes/Extreme/_edit_work/RO-15/round1"; O = f"{W}/review/options"; FF = F.FF
NAMES = {"C": "Look C, the locked 9/23 studio colour (website video, RO-10 to RO-18). Recommended.", "C-rich": "Look C with a little more colour and contrast (saturation +12 %)", "C-bright": "Look C a touch brighter in the mids (same colour)"}
A0, D = 146.0, 12.0
# the voice for the sample: the recommended option's chain on this exact passage
raw = f"{O}/_sample_raw.wav"
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(A0), "-t", str(D), "-i", f"{W}/lav.wav", raw], check=True)
eq = open(f"{W}/fit/eq.txt").read().strip()
VC = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py"
if eq.startswith("FINISH:"):   # the recommended voice: untreated lav, rumble filter only, finished to loudness (no gate)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", raw, "-af", eq[7:] + ",pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", f"{O}/_sample_st.wav"], check=True)
    subprocess.run(["python3", VC, "--in", f"{O}/_sample_st.wav", "--out", f"{O}/_sample_voice.wav", "--finish-only", "--work", f"{O}/_sample_work"], check=True, capture_output=True)
else:
    subprocess.run(["python3", VC, "--in", raw, "--pull", "anull", "--out", f"{O}/_sample_voice.wav", "--eq", eq, "--work", f"{O}/_sample_work"], check=True, capture_output=True)
for k, g in F.GRADES.items():
    vf = F.vf("W2", "open.0r1", k).replace("format=rgb24", "format=yuv420p") if False else F.vf("W2", "open.0r1", k) + ",format=yuv420p"
    out = f"{O}/colour-{k}.mp4"
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(A0), "-t", str(D), "-i", F.C1709, "-i", f"{O}/_sample_voice.wav", "-map", "0:v", "-map", "1:a",
                    "-vf", vf, "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-c:a", "copy", "-movflags", "+faststart", out[:-4] + " - REVIEW 540p.mp4"], check=True)
    for nm, (fm, sh, t) in {"wide": ("W2", "open.0r1", 150.0), "tight": ("T2", "persp.0r0", 235.0)}.items():
        F.frame_src(t, fm, sh, k).save(f"{O}/colour-{k}-{nm}.jpg", quality=92)
REF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/claude edited long form content/17 - 3 Healthy Foods That Made Me Fat/3 Healthy Foods That Made Me Fat | claude round 5 | 16x9 | RO-17.mp4"
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", "26", "-i", REF, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv", "-q:v", "2", f"{O}/ref-RO17.jpg"], check=True)
json.dump(NAMES, open(f"{O}/colour.json", "w"), indent=1); print("colour options ok")
