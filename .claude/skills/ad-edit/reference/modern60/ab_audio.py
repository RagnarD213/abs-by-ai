#!/usr/bin/env python3
"""Head-to-head AUDIO A/B: the same sentence from the trial edit, then ours.

Matching spans are located by TRANSCRIPT, not by envelope correlation -- his cut
removed different amounts of pause so the offset drifts, and a short envelope window
false-matches readily (it put "the knowledge isn't the problem" 17 s out of place).
Run whisper_run.py over both audio tracks, then search the word list for the phrase.
"""
import importlib.util, subprocess
from PIL import ImageDraw
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
OURS, HIS = "modern_sample.mp4", "reference/muhammad_a.mp4"
spec = importlib.util.spec_from_file_location(
    "ml", "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference/motionlib.py")
ml = importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)

PAD = 0.18
# (caption, his start, his end, our start, our end)
SPANS = [
    ("“The knowledge isn't the problem.”",              35.24, 36.84, 37.95, 39.75),
    ("“You already know that if you had the motivation…”", 28.80, 33.38, 30.78, 35.55),
    ("“Visualizing your goal…”",                     44.06, 47.80, 47.00, 50.80),
]

def card(title, sub, path):
    im = ml.field_bg(ml.GREEN).convert("RGBA")
    d = ImageDraw.Draw(im)
    fB, fS = ml.font(128, "ExtraBold"), ml.font(50, "Medium")
    d.text((960, 452), title.upper(), font=fB, fill=ml.GREEN.ink, anchor="mm")
    w, _ = ml.text_size(title.upper(), fB)
    d.rectangle([960 - w / 2 - 24, 540, 960 + w / 2 + 24, 552], fill=ml.GREEN.accent)
    for i, l in enumerate(ml.wrap(sub, fS, 1440)):
        d.text((960, 640 + i * 64), l, font=fS, fill=ml.GREEN.ink_soft, anchor="mm")
    im.convert("RGB").save(path)

def clip(src, ss, to, title, sub, out):
    dur = to - ss + PAD * 2
    png = out.replace(".mp4", ".png"); card(title, sub, png)
    # decode the span to wav first: seeking into an AAC stream with -ss throws frame
    # errors on some files and can drop the first syllable
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-i", src, "-ss", f"{ss - PAD:.3f}",
                    "-t", f"{dur:.3f}", "-vn", "-ac", "2", "-ar", "48000",
                    "-c:a", "pcm_s16le", "-f", "wav", "_ab.wav"], check=True)
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-loop", "1", "-t", f"{dur:.3f}",
                    "-i", png, "-i", "_ab.wav", "-map", "0:v", "-map", "1:a",
                    "-r", "30000/1001", "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out], check=True)
    return out

def main():
    parts = []
    for k, (sub, h0, h1, o0, o1) in enumerate(SPANS):
        parts.append(clip(HIS,  h0, h1, "Trial edit",   sub, f"_ab{k}a.mp4"))
        parts.append(clip(OURS, o0, o1, "Our pipeline", sub, f"_ab{k}b.mp4"))
    with open("_ablist.txt", "w") as f:
        for p in parts: f.write(f"file '{p}'\n")
    subprocess.run([FF, "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", "_ablist.txt", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "audio_ab_trial_vs_ours.mp4"], check=True)
    print("audio_ab_trial_vs_ours.mp4 done")

if __name__ == "__main__":
    main()
