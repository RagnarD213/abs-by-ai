"""Round-1 colour options: the same 12 s (source 137.0-149.0, 'A typical one has about 80 calories...', wide) and the same tight still in
each of the three grades, plus stills of the approved RO-25 film for comparison. Audio: the recommended voice (warm bass) on the clip."""
import sys, subprocess, json, os
sys.path.insert(0, "/Volumes/Expansion/_edit_work/RO-29/round1/recipe")
import frames as F
W = "/Volumes/Expansion/_edit_work/RO-29/round1"; O = f"{W}/review/options"; FF = F.FF
NAMES = {"A": "Rich Balanced, warmer skin (your pick on the Zepbound film, same set)", "B": "Rich Balanced (the grade of the approved I'm 41 film)", "C": "Richer Colour (your pick on Boring Abs At 40, darker)"}
A0, D = 137.0, 12.0
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
    cw, ch, x, y = F.crop("W2", "cocktail.0r1")
    vf = f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=lanczos:in_color_matrix=bt709:in_range=tv,{g},format=yuv420p"
    out = f"{O}/colour-{k}.mp4"
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(A0), "-t", str(D), "-i", F.C1772, "-i", f"{O}/_sample_voice.wav", "-map", "0:v", "-map", "1:a",
                    "-vf", vf, "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", out, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-c:a", "copy", "-movflags", "+faststart", out[:-4] + " - REVIEW 540p.mp4"], check=True)
    for nm, (fm, sh, t) in {"wide": ("W2", "cocktail.0r1", 141.0), "tight": ("T2", "cocktail.0r2", 152.0)}.items():
        cw, ch, x, y = F.crop(fm, sh)
        subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", str(t), "-i", F.C1772, "-frames:v", "1", "-vf",
                        f"crop={cw}:{ch}:{x}:{y},scale=1920:1080:flags=lanczos:in_color_matrix=bt709:in_range=tv,{g}", "-q:v", "2", f"{O}/colour-{k}-{nm}.jpg"], check=True)
REF = "/Users/danielrose/Projects/Claude/Projects/Abs By AI/Codex Content Videos/Im 41 Wasted Life - RO-25/Im 41 Wasted Life | codex | 16x9 | RO-25.mp4"
subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-ss", "200", "-i", REF, "-frames:v", "1", "-vf", "scale=in_color_matrix=bt709:in_range=tv", "-q:v", "2", f"{O}/ref-RO25.jpg"], check=True)
json.dump(NAMES, open(f"{O}/colour.json", "w"), indent=1); print("colour options ok")
